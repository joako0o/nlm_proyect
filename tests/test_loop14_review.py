"""LOOP14: exposiciones completas, cierres personales y límites institucionales."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, validate_speaker_reviews, speaker_intervals
from context_warnings import load_context_warnings, contextual_motives
from continuity import boundary, update_state, continuation_start, annotate_turns

REVIEWED=(178,214,288,305,351,390,438,492,557,587,615,727,836,1605,1607,2036)
PRESIDENT='José De Gregorio Rebeco'

class LoopFourteenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)
        cls.warnings=load_context_warnings(cls.raw)
    def parts(self,p):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p))
    def test_reviews_are_bounded_not_global_anchors(self):
        for p in REVIEWED:
            e=self.reviews[p]
            self.assertEqual(e['Tipo_Revision'],'LECTURA_DIRIGIDA_POR_AGENTE')
            self.assertIn('L14',e['Revision_ID'])
            self.assertEqual(len(speaker_intervals(e)),1)
            parts=[x for x in self.parts(p) if x[2]=='CONTEXTO_REVISADO']
            self.assertEqual(len(parts),1)
            self.assertEqual(''.join(parts[0][0].split()),''.join(self.raw[p]['Texto'][e['Inicio']:e['Fin']].split()))
    def test_introductions_do_not_certify_following_presentations(self):
        for p in [351,727]:
            self.assertEqual(len(self.parts(p)[-1][0]),61)
            self.assertIn('sólo',self.reviews[p]['Justificacion'].lower())
    def test_long_presentations_are_not_split_by_numbering(self):
        for p in [178,214,288,305,390,438,492,557,587,615,1605,2036]:
            self.assertEqual(sum(m=='CONTEXTO_REVISADO' for t,a,m in self.parts(p)),1)
            self.assertGreater(len(next(t for t,a,m in self.parts(p) if m=='CONTEXTO_REVISADO')),5000)
    def test_presidential_returns_not_absorbed(self):
        for p in [178,214,288,305,587]:
            parts=self.parts(p);i=next(i for i,x in enumerate(parts) if x[2]=='CONTEXTO_REVISADO')
            self.assertEqual(parts[i+1][1],'Vittorio Corbo Lioi')
            self.assertNotIn('ofrece la palabra para comentarios',parts[i][0])
    def test_jadresic_references_are_not_new_speakers(self):
        parts=self.parts(1607)
        self.assertEqual([a for t,a,m in parts],[PRESIDENT,'Esteban Jadresic Marinovic'])
        self.assertIn('García',parts[1][0]);self.assertIn('Schmidt-Hebbel',parts[1][0])
    def test_damage_warning_survives_speaker_review(self):
        e=self.warnings[587];self.assertEqual(e['Motivo'],'TEXTO_DANADO_POR_COTEJAR')
        t,a,m=next(x for x in self.parts(587) if x[2]=='CONTEXTO_REVISADO')
        self.assertIn('apreciación del Agrega que',t)
        row=dict(ID_Padre=587,Fecha=e['Fecha'],Texto=t,Actor_Final=a)
        self.assertEqual(contextual_motives(row,self.warnings),[e['Motivo']])
    def test_cargo_discrepancy_not_repaired_by_name(self):
        t,a,m=self.parts(836)[0]
        self.assertIn('Análisis Financiero',t)
        self.assertEqual(b.roster_role_for(self.raw[836]['Fecha'],a),'Gerente de Análisis Internacional')
        self.assertEqual(contextual_motives(dict(ID_Padre=836,Fecha=self.raw[836]['Fecha'],Texto=t,Actor_Final=a),self.warnings),['CARGO_EN_DISCURSO_POR_VERIFICAR'])
    def test_warnings_do_not_spill_to_presidential_handoffs(self):
        for p in [587,836]:
            e=self.warnings[p]
            self.assertFalse(contextual_motives(dict(ID_Padre=p,Fecha=e['Fecha'],Texto='El Presidente ofrece la palabra.',Actor_Final=PRESIDENT),self.warnings))
    def test_review_hash_change_is_rejected(self):
        entries=json.loads((Path(__file__).resolve().parents[1]/'data/curation/revisiones_hablantes.json').read_text())
        for p in [615,836,1607]:
            e=next(e for e in entries if e['ID_Padre']==p);raw=copy.deepcopy(self.raw);raw[p]['Texto']+=' X'
            with tempfile.TemporaryDirectory() as d:
                path=Path(d)/'reviews.json';path.write_text(json.dumps([e]))
                with self.assertRaises(ValueError):load_speaker_reviews(raw,path)
    def test_direct_opening_and_closing_need_subject_and_predicate(self):
        for verb in ['abre la sesión','pone término a la sesión']:
            t='Siendo las 16:00 horas, el Presidente señor José De Gregorio '+verb+' de la tarde.'
            self.assertEqual(b.TURN_DETECTOR.speaker(t,'2010-07-15')['actor'],PRESIDENT)
            self.assertEqual(b.segment_turns(t,'2010-07-15',b.CONSEJO)[0][1:],(PRESIDENT,'SUJETO_ROL_NOMBRE'))
    def test_subordinate_closing_does_not_borrow_predicate(self):
        for t in ['El Presidente señor José De Gregorio, quien pone término a la sesión, está presente.',
                  'El Presidente señor José De Gregorio solicita que el señor Marshall abre la sesión.',
                  'Se comenta que el Presidente señor José De Gregorio pone término a la sesión.']:
            candidate=b.TURN_DETECTOR.speaker(t,'2010-07-15')
            if t.startswith('El Presidente señor José De Gregorio solicita'):
                self.assertEqual(candidate['actor'],PRESIDENT)
            else:self.assertIsNone(candidate)
    def test_quoted_closing_not_a_live_turn(self):
        for verb in ['abre la sesión','pone término a la sesión']:
            self.assertIsNone(b.TURN_DETECTOR.speaker('“El Presidente señor José De Gregorio '+verb+'.”','2010-07-15'))
    def test_impersonal_closing_stays_institutional(self):
        t='Se levanta la Sesión a las 18:00 horas.'
        self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2010-07-15'))
        self.assertEqual(b.segment_turns(t,'2010-07-15',PRESIDENT)[0][1:],(b.CONSEJO,'ACTA/META'))
    def test_reopening_is_separate_from_personal_closing(self):
        for p in [2489,2538]:
            parts=self.parts(p);i=next(i for i,x in enumerate(parts) if 'pone término' in x[0])
            self.assertEqual(parts[i][1],PRESIDENT)
            self.assertEqual(parts[i+1][1:],(b.CONSEJO,'ACTA/META'))
            self.assertNotIn('se reanuda la Sesión',parts[i][0])
    def test_displaced_session_number_not_rewritten(self):
        parts=self.parts(2489)
        t=next(t for t,a,m in parts if a==b.CONSEJO)
        self.assertEqual(t,'N° 137, Siendo las 16:00 horas, se reanuda la Sesión de Política Monetaria')
        self.assertTrue(b._inst_transition(t))
    def test_displaced_number_exception_is_literal_only(self):
        for t in ['N° 138, Siendo las 16:00 horas, se reanuda la Sesión de Política Monetaria',
                  'Basura, Siendo las 16:00 horas, se reanuda la Sesión de Política Monetaria',
                  'Recuerda N° 137, Siendo las 16:00 horas, se reanuda la Sesión de Política Monetaria']:
            self.assertFalse(b._inst_transition(t))
    def test_new_clauses_block_following_inherited_continuation(self):
        for verb in ['abre la sesión','pone término a la sesión']:
            t='El Presidente señor José De Gregorio '+verb+'.'
            self.assertTrue(boundary(t))
            state={};update_state(state,PRESIDENT,'SUJETO_ROL_NOMBRE',t,'2010-07-15',b.TURN_DETECTOR,b.split_sentences,1)
            self.assertTrue(state['barrier'])
            self.assertFalse(continuation_start('La situación es compleja.',PRESIDENT,state,b.TURN_DETECTOR,b.split_sentences,'2010-07-15'))
    def test_opening_preserves_damaged_suffix_not_minister_speech(self):
        parts=self.parts(3269)
        self.assertEqual([a for t,a,m in parts],[PRESIDENT,PRESIDENT])
        self.assertTrue(parts[-1][0].endswith('A continuación,.'))
        self.assertIn('Rodrigo Álvarez',parts[-1][0])
    def test_parent_178_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[178]['Texto'].encode()).hexdigest(),'652f4f30978b72c57dba90549181aedf6c1e6c6dfcdc80b4c72295d2868a45c4')
        parts=self.parts(178)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 6176, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 69, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[178]['Texto'].split()))
        if 178 in self.reviews:
            rows=[dict(ID=i,ID_Padre=178,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{178:self.reviews[178]}))
    def test_parent_214_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[214]['Texto'].encode()).hexdigest(),'59621219a98a0640a272d6c40555e25b621ab0acb45f9f293dbb4dd1bdf9f092')
        parts=self.parts(214)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 128, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 396, 'ACTA/META'), ('Vittorio Corbo Lioi', 158, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 6670, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 69, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[214]['Texto'].split()))
        if 214 in self.reviews:
            rows=[dict(ID=i,ID_Padre=214,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{214:self.reviews[214]}))
    def test_parent_288_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[288]['Texto'].encode()).hexdigest(),'20574c48f323e6f7e46f4215ce96d7c77224a84faddb02e2faa31fc1aea7e754')
        parts=self.parts(288)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 128, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 219, 'ACTA/META'), ('Vittorio Corbo Lioi', 158, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 5347, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 69, 'SUJETO_ROL_NOMBRE'), ('Klaus Schmidt-Hebbel Dunker', 1943, 'SUJETO_ROL_NOMBRE'), ('Esteban Jadresic Marinovic', 1148, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[288]['Texto'].split()))
        if 288 in self.reviews:
            rows=[dict(ID=i,ID_Padre=288,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{288:self.reviews[288]}))
    def test_parent_305_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[305]['Texto'].encode()).hexdigest(),'ae317d3bc1c17cc39e2b4b6fedfae96160a059370cea65e08f36cdf854e88df0')
        parts=self.parts(305)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 128, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 73, 'ACTA/META'), ('Vittorio Corbo Lioi', 420, 'SUJETO_ROL_SESION'), ('Rodrigo Valdés Pulido', 5220, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 69, 'SUJETO_ROL_NOMBRE'), ('Luis Óscar Herrera Barriga', 2091, 'SUJETO_ROL_NOMBRE'), ('Esteban Jadresic Marinovic', 1609, 'SUJETO_ROL_NOMBRE'), ('Vittorio Corbo Lioi', 218, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[305]['Texto'].split()))
        if 305 in self.reviews:
            rows=[dict(ID=i,ID_Padre=305,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{305:self.reviews[305]}))
    def test_parent_351_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[351]['Texto'].encode()).hexdigest(),'12b2b8d5bcf3ff9c80fce347a385be482406fc0bd46c8bdd5131277755a2edc9')
        parts=self.parts(351)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 159, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 61, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[351]['Texto'].split()))
        if 351 in self.reviews:
            rows=[dict(ID=i,ID_Padre=351,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{351:self.reviews[351]}))
    def test_parent_390_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[390]['Texto'].encode()).hexdigest(),'84ee6aeebcd6c0deccdff8e52e5d0f7107c001c5b6b3eb4607956769100e71f8')
        parts=self.parts(390)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 7445, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[390]['Texto'].split()))
        if 390 in self.reviews:
            rows=[dict(ID=i,ID_Padre=390,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{390:self.reviews[390]}))
    def test_parent_438_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[438]['Texto'].encode()).hexdigest(),'ddf1a5e42cc6d95d375bad3861c88fee58dd8e8bd07e78b33f13e8143e68fc3b')
        parts=self.parts(438)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 6328, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[438]['Texto'].split()))
        if 438 in self.reviews:
            rows=[dict(ID=i,ID_Padre=438,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{438:self.reviews[438]}))
    def test_parent_492_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[492]['Texto'].encode()).hexdigest(),'911d907bfc1ef4ac5d4d090d87356cb587c3e824d9f45a5ed3b84a0640ff62b9')
        parts=self.parts(492)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 7569, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[492]['Texto'].split()))
        if 492 in self.reviews:
            rows=[dict(ID=i,ID_Padre=492,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{492:self.reviews[492]}))
    def test_parent_557_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[557]['Texto'].encode()).hexdigest(),'2929bc31ec92d588298f14da36ba897530c6f447334efdfefaef77596c8d21fe')
        parts=self.parts(557)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 8855, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[557]['Texto'].split()))
        if 557 in self.reviews:
            rows=[dict(ID=i,ID_Padre=557,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{557:self.reviews[557]}))
    def test_parent_587_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[587]['Texto'].encode()).hexdigest(),'b8d468c7a57de79ef3307ce0cb7da39ffad243f8462fde54d9cd830bd9eed57a')
        parts=self.parts(587)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 194, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 247, 'SUJETO_NOMBRE'), ('Nicolás Eyzaguirre Guzmán', 115, 'SUJETO_ROL_SESION'), ('Pablo García Silva', 134, 'SUJETO_NOMBRE'), ('Manuel Marfán Lewis', 318, 'SUJETO_ROL_NOMBRE'), ('Vittorio Corbo Lioi', 454, 'SUJETO_ROL_NOMBRE'), ('Nicolás Eyzaguirre Guzmán', 753, 'SUJETO_ROL_NOMBRE'), ('Vittorio Corbo Lioi', 128, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 73, 'ACTA/META'), ('Vittorio Corbo Lioi', 464, 'SUJETO_ROL_SESION'), ('Rodrigo Valdés Pulido', 7516, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 88, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[587]['Texto'].split()))
        if 587 in self.reviews:
            rows=[dict(ID=i,ID_Padre=587,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{587:self.reviews[587]}))
    def test_parent_615_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[615]['Texto'].encode()).hexdigest(),'4f372c1c6f371baec6e2e29993f339a7509232a67cb724f97f4627363077daf8')
        parts=self.parts(615)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 7442, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[615]['Texto'].split()))
        if 615 in self.reviews:
            rows=[dict(ID=i,ID_Padre=615,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{615:self.reviews[615]}))
    def test_parent_727_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[727]['Texto'].encode()).hexdigest(),'bd50b967cae2dde601931f5df0eac5638ddfd6bec2cdea185dae705309046d4d')
        parts=self.parts(727)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 281, 'SUJETO_ROL_SESION'), ('Consejo del Banco Central de Chile', 173, 'ACTA/META'), ('Vittorio Corbo Lioi', 161, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 61, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[727]['Texto'].split()))
        if 727 in self.reviews:
            rows=[dict(ID=i,ID_Padre=727,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{727:self.reviews[727]}))
    def test_parent_836_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[836]['Texto'].encode()).hexdigest(),'f6c87594bd2e8c0945c17eafc889714341875b919c4fb095fb6e6a028575deb0')
        parts=self.parts(836)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sergio Lehmann Beresi', 356, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[836]['Texto'].split()))
        if 836 in self.reviews:
            rows=[dict(ID=i,ID_Padre=836,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{836:self.reviews[836]}))
    def test_parent_1605_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1605]['Texto'].encode()).hexdigest(),'b62522063c66e20f9c9c424c845098b7079843bc53472db8da841b0ac9940c9b')
        parts=self.parts(1605)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 106, 'SUJETO_ROL_SESION'), ('Pablo García Silva', 5165, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1605]['Texto'].split()))
        if 1605 in self.reviews:
            rows=[dict(ID=i,ID_Padre=1605,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{1605:self.reviews[1605]}))
    def test_parent_1607_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1607]['Texto'].encode()).hexdigest(),'3606ac7493bd04bd6fab572e45bc728be7842902df9481774957c2c4b25d5f69')
        parts=self.parts(1607)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 118, 'SUJETO_ROL_SESION'), ('Esteban Jadresic Marinovic', 2271, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1607]['Texto'].split()))
        if 1607 in self.reviews:
            rows=[dict(ID=i,ID_Padre=1607,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{1607:self.reviews[1607]}))
    def test_parent_2036_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2036]['Texto'].encode()).hexdigest(),'2bd6724033b82362ea10dd5c01cdf76f81602b599756d04bd9e7abd5261ecaa5')
        parts=self.parts(2036)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Pablo García Silva', 7012, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2036]['Texto'].split()))
        if 2036 in self.reviews:
            rows=[dict(ID=i,ID_Padre=2036,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{2036:self.reviews[2036]}))
    def test_parent_2489_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2489]['Texto'].encode()).hexdigest(),'8228c25429875ed16687a057b116aecbd0e53a440d3e1351858d9604a239bf87')
        parts=self.parts(2489)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Andrés Velasco Brañes', 394, 'SUJETO_ROL_SESION'), ('José De Gregorio Rebeco', 1201, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 200, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 74, 'ACTA/META'), ('José De Gregorio Rebeco', 131, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2489]['Texto'].split()))
        if 2489 in self.reviews:
            rows=[dict(ID=i,ID_Padre=2489,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{2489:self.reviews[2489]}))
    def test_parent_2490_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2490]['Texto'].encode()).hexdigest(),'c58910b473817dd8ab08354194fe19d6e9911f403fcbc422eab6871e45ddd0ac')
        parts=self.parts(2490)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 161, 'SUJETO_ROL_SESION'), ('Pablo García Silva', 5122, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2490]['Texto'].split()))
        if 2490 in self.reviews:
            rows=[dict(ID=i,ID_Padre=2490,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{2490:self.reviews[2490]}))
    def test_parent_2538_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2538]['Texto'].encode()).hexdigest(),'ba193e9d9d081c6016b241441619908695da897d4903a4dcbb84152ba5e3b726')
        parts=self.parts(2538)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 204, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 200, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 74, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2538]['Texto'].split()))
        if 2538 in self.reviews:
            rows=[dict(ID=i,ID_Padre=2538,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{2538:self.reviews[2538]}))
    def test_parent_3269_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3269]['Texto'].encode()).hexdigest(),'445405ded961630c8adf14a97808353da4cb503509b96ef3991f63d8545c6df3')
        parts=self.parts(3269)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 96, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 247, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3269]['Texto'].split()))
        if 3269 in self.reviews:
            rows=[dict(ID=i,ID_Padre=3269,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{3269:self.reviews[3269]}))
