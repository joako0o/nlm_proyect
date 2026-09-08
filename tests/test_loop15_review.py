"""LOOP15: intervalos largos, daños visibles y retorno nominal de Schmidt-Hebbel."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews,speaker_intervals,validate_speaker_reviews
from context_warnings import load_context_warnings,contextual_motives
from continuity import annotate_turns

IDS=(644,664,770,817,867,932,976,1012,1047,1090,1155,1209,1251,1297)
DAMAGE=(644,664,770,1012,1047,1155)

class LoopFifteenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)
        cls.warnings=load_context_warnings(cls.raw)
    def parts(self,p):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews[p])
    def test_new_intervals_are_bounded_and_survive(self):
        for p in IDS:
            intervals=[e for e in speaker_intervals(self.reviews[p]) if '-L15-' in e['Revision_ID']]
            self.assertEqual(len(intervals),2 if p==1090 else 1)
            rows=[dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p))]
            self.assertFalse(validate_speaker_reviews(rows,{p:self.reviews[p]}))
    def test_all_option_presentations_are_one_interval(self):
        for p in IDS:
            actor='Igal Magendzo Weinberger' if p==1297 else 'Rodrigo Valdés Pulido'
            parts=[(t,a,m) for t,a,m in self.parts(p) if a==actor]
            self.assertEqual(len(parts),1)
            self.assertEqual(parts[0][2],'CONTEXTO_REVISADO')
            self.assertGreater(len(parts[0][0]),3700)
    def test_context_reviews_never_become_global_anchors(self):
        for p in IDS:
            rows=[dict(ID=i,ID_Padre=p,ID_Intervencion=f'{p}:{i}',ID_Bloque_Texto=f'{p}:{i}',Fecha=self.raw[p]['Fecha'],Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p))]
            annotate_turns(rows)
            for r in rows:
                if r['Fuente_Actor']=='CONTEXTO_REVISADO':self.assertFalse(r['ID_Ancla_Actor'])
    def test_new_damage_warnings_match_only_reviewed_expositions(self):
        for p in DAMAGE:
            e=self.warnings[p];self.assertEqual(e['Motivo'],'TEXTO_DANADO_POR_COTEJAR')
            matched=[]
            for t,a,m in self.parts(p):
                if contextual_motives(dict(ID_Padre=p,Fecha=e['Fecha'],Texto=t,Actor_Final=a),self.warnings):matched.append((a,m))
            self.assertEqual(matched,[('Rodrigo Valdés Pulido','CONTEXTO_REVISADO')])
    def test_damage_is_not_reconstructed_or_reordered(self):
        self.assertIn('costos laborales U 5.',self.raw[644]['Texto'])
        self.assertIn('la persistencia que 8.',self.raw[664]['Texto'])
        self.assertTrue(self.parts(770)[-1][0].endswith('comentarios.'))
        self.assertIn('inflacionaria efectiva y de los Señala',self.raw[1012]['Texto'])
        self.assertIn('más de medio punto por debajo • El IPC',self.raw[1047]['Texto'])
        self.assertIn('que en el último IPOM y que, aunque',self.raw[1155]['Texto'])
    def test_marfan_question_remains_separate(self):
        parts=self.parts(644)
        i=next(i for i,(t,a,m) in enumerate(parts) if a=='Manuel Marfán Lewis' and m=='CONTEXTO_REVISADO')
        self.assertEqual(parts[i-1][1],'Klaus Schmidt-Hebbel Dunker')
        self.assertEqual(parts[i+1][1],'Klaus Schmidt-Hebbel Dunker')
        self.assertEqual(len(parts[i][0]),164)
    def test_magendzo_not_inferred_as_valdes_from_topic(self):
        parts=self.parts(1297)
        self.assertEqual([a for t,a,m in parts],['Vittorio Corbo Lioi',b.CONSEJO,'Vittorio Corbo Lioi','Igal Magendzo Weinberger','Vittorio Corbo Lioi'])
    def test_schmidt_hebbel_return_no_longer_absorbed_by_president(self):
        parts=self.parts(1090)
        self.assertEqual([(a,len(t)) for t,a,m in parts[-3:]],[('Vittorio Corbo Lioi',88),('Klaus Schmidt-Hebbel Dunker',1293),('Pablo García Silva',1133)])
        self.assertTrue(parts[-2][0].startswith('Señala el Gerente de Investigación Económica, señor Klaus Schmidt- Hebbel'))
        self.assertIn('elegir la opción de mantener de tasa.',parts[-2][0])
    def test_no_global_ocr_alias_rule_added(self):
        r=self.raw[1090]
        parts=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertFalse(any(a=='Klaus Schmidt-Hebbel Dunker' for t,a,m in parts))
    def test_644_old_question_is_a_secondary_interval(self):
        intervals=speaker_intervals(self.reviews[644])
        self.assertEqual([e['Actor'] for e in intervals],['Rodrigo Valdés Pulido','Manuel Marfán Lewis'])
        self.assertEqual(intervals[1]['Revision_ID'],'HAB-20260907-644')
        self.assertEqual((intervals[1]['Inicio'],intervals[1]['Fin']),(6928,7093))
    def test_664_previous_suspension_is_not_extended(self):
        intervals=speaker_intervals(self.reviews[664])
        self.assertEqual([e['Actor'] for e in intervals],['Vittorio Corbo Lioi','Rodrigo Valdés Pulido'])
        self.assertEqual((intervals[0]['Inicio'],intervals[0]['Fin']),(433,562))
    def test_overlapping_secondary_interval_is_rejected(self):
        e=copy.deepcopy(self.reviews[1090]);extra=e['Revisiones_Adicionales'][0];extra['Inicio']=e['Inicio'];extra['Cita_Inicio']=e['Cita_Inicio']
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'r.json';path.write_text(json.dumps([e]))
            with self.assertRaises(ValueError):load_speaker_reviews(self.raw,path)
    def test_changed_parent_hash_invalidates_new_review(self):
        raw=copy.deepcopy(self.raw);raw[1297]['Texto']+=' X'
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'r.json';path.write_text(json.dumps([self.reviews[1297]]))
            with self.assertRaises(ValueError):load_speaker_reviews(raw,path)
    def test_parent_644_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[644]['Texto'].encode()).hexdigest(),'4d0ec7f0ca45ca994334bb8094622dd350fe8225fe1958d6d7d6120f2f008c73')
        parts=self.parts(644)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 128, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 182, 'ACTA/META'), ('Vittorio Corbo Lioi', 161, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 3750, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 88, 'SUJETO_ROL_NOMBRE'), ('Klaus Schmidt-Hebbel Dunker', 2613, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 164, 'CONTEXTO_REVISADO'), ('Klaus Schmidt-Hebbel Dunker', 304, 'SUJETO_NOMBRE'), ('Manuel Marfán Lewis', 139, 'SUJETO_ROL_NOMBRE'), ('Klaus Schmidt-Hebbel Dunker', 250, 'SUJETO_NOMBRE'), ('Manuel Marfán Lewis', 66, 'SUJETO_NOMBRE'), ('Klaus Schmidt-Hebbel Dunker', 535, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[644]['Texto'].split()))
    def test_parent_664_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[664]['Texto'].encode()).hexdigest(),'5f08e3e94c1cf7b833c59ccac25bcd8879a94e3fecdfbd7140aedb258ced277d')
        parts=self.parts(664)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 177, 'SUJETO_ROL_NOMBRE'), ('Andrés Velasco Brañes', 254, 'SUJETO_ROL_NOMBRE'), ('Vittorio Corbo Lioi', 128, 'CONTEXTO_REVISADO'), ('Consejo del Banco Central de Chile', 73, 'ACTA/META'), ('Vittorio Corbo Lioi', 161, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 8397, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 88, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[664]['Texto'].split()))
    def test_parent_770_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[770]['Texto'].encode()).hexdigest(),'2f9a853d5b516583af1afa0664630b0a3410c6d0e0c0753ba120c2385d233e73')
        parts=self.parts(770)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 128, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 73, 'ACTA/META'), ('Vittorio Corbo Lioi', 161, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 7648, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[770]['Texto'].split()))
    def test_parent_817_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[817]['Texto'].encode()).hexdigest(),'c82ae466d627e3393c23c79526c3b49b743a25dd2142ebd3c25e7ce327a3a4e7')
        parts=self.parts(817)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 8294, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[817]['Texto'].split()))
    def test_parent_867_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[867]['Texto'].encode()).hexdigest(),'fb50f164d8d6c47c411249e0bb17cbc74c0bd1acba9fd50636def4ac16966791')
        parts=self.parts(867)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 8147, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[867]['Texto'].split()))
    def test_parent_932_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[932]['Texto'].encode()).hexdigest(),'7103de43988e091269617368e53bdb797c49346833bfab1d94efb76908968d19')
        parts=self.parts(932)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 6877, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[932]['Texto'].split()))
    def test_parent_976_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[976]['Texto'].encode()).hexdigest(),'1d5bd53cca3eb35346704d65ffd82b66cdd306996fe967e95ac4ba8f4234cc58')
        parts=self.parts(976)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 6855, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[976]['Texto'].split()))
    def test_parent_1012_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1012]['Texto'].encode()).hexdigest(),'0afb5e84f53b88628d535271bf8cb8565c2767fa9cee38b9b954cf22d7b0027a')
        parts=self.parts(1012)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 346, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 74, 'ACTA/META'), ('Vittorio Corbo Lioi', 159, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 6177, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 88, 'SUJETO_ROL_NOMBRE'), ('Klaus Schmidt-Hebbel Dunker', 3202, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1012]['Texto'].split()))
    def test_parent_1047_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1047]['Texto'].encode()).hexdigest(),'29ff75555fccc0dfe58590a195403611c122e91d0d66784988345dc5cd6ba2aa')
        parts=self.parts(1047)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 851, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 74, 'ACTA/META'), ('Vittorio Corbo Lioi', 159, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 9413, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 88, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1047]['Texto'].split()))
    def test_parent_1090_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1090]['Texto'].encode()).hexdigest(),'7c2dd5abcf6706c7742199974f43d796751490d66ae4aaf9a32975d7d9143f4a')
        parts=self.parts(1090)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 128, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 74, 'ACTA/META'), ('Vittorio Corbo Lioi', 159, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 7839, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 88, 'SUJETO_ROL_NOMBRE'), ('Klaus Schmidt-Hebbel Dunker', 1293, 'CONTEXTO_REVISADO'), ('Pablo García Silva', 1133, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1090]['Texto'].split()))
    def test_parent_1155_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1155]['Texto'].encode()).hexdigest(),'8e97bf84d589f034801c28f0f4546e6297f1db9fba4fc6ebfd912225f1e4d03f')
        parts=self.parts(1155)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 10547, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1155]['Texto'].split()))
    def test_parent_1209_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1209]['Texto'].encode()).hexdigest(),'51a216decb3d83b08119c793b34385fdcac203065aa6d9c2a6ebf6ac36975d60')
        parts=self.parts(1209)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 506, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 74, 'ACTA/META'), ('Vittorio Corbo Lioi', 159, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 8709, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 70, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1209]['Texto'].split()))
    def test_parent_1251_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1251]['Texto'].encode()).hexdigest(),'52eadd5f8d937e4144aa6d9728ecce45443ba9cfd7916d268455ae138b26c6a9')
        parts=self.parts(1251)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 128, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 172, 'ACTA/META'), ('Vittorio Corbo Lioi', 159, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 9099, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 70, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1251]['Texto'].split()))
    def test_parent_1297_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1297]['Texto'].encode()).hexdigest(),'d2c26e36cc19ad64a1252f280a083833ca98d326dc83a7c9f9e4d9d7ee859ee5')
        parts=self.parts(1297)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 459, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 74, 'ACTA/META'), ('Vittorio Corbo Lioi', 165, 'SUJETO_ROL_NOMBRE'), ('Igal Magendzo Weinberger', 9961, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 88, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1297]['Texto'].split()))
