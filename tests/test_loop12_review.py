"""Loop12: respuestas acotadas, residuos conjuntos y anclas posteriores.
Las fixtures comprueban conservación, no certifican lectura humana del corpus.
"""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, validate_speaker_reviews, speaker_intervals
from context_warnings import load_context_warnings, contextual_motives, validate_context_warnings, has_context_warning, JOINT_MOTIVE
from continuity import annotate_turns

class LoopTwelveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)
    def parts(self,p,review=None,text=None):
        r=self.raw[p];return b.segment_turns(text or r['Texto'],r['Fecha'],r['Actor'],review=review if review is not None else self.reviews.get(p))
    def load_entry(self,e):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'review.json';path.write_text(json.dumps([e]));return load_speaker_reviews(self.raw,path)
    def test_5647_answer_and_long_return_belong_to_lehmann(self):
        parts=self.parts(5647)
        self.assertEqual([a for t,a,m in parts],['Rodrigo Vergara Montes','Sergio Lehmann Beresi'])
        self.assertTrue(parts[1][0].startswith('por lo que el señor Sergio Lehmann'))
        for country in ['Perú','Brasil','Colombia','Corea']:self.assertIn(country,parts[1][0])
        self.assertIn('cambiarías',parts[1][0])
    def test_causal_answer_not_generalized_without_review(self):
        r=self.raw[5647];parts=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertEqual(len(parts),1)
    def test_causal_answer_requires_exact_connector(self):
        r=self.raw[5647];t=r['Texto'].replace('por lo que','porque que')
        with self.assertRaises(ValueError):self.parts(5647,text=t)
    def test_causal_answer_requires_preceding_comma(self):
        r=self.raw[5647];t=r['Texto'].replace('diaria, por','diaria; por')
        with self.assertRaises(ValueError):self.parts(5647,text=t)
    def test_causal_answer_rejects_wrong_actor(self):
        e=copy.deepcopy(self.reviews[5647]);e['Actor']='Rodrigo Vergara Montes'
        with self.assertRaises(ValueError):self.parts(5647,review=e)
    def test_causal_answer_cannot_start_inside_quote(self):
        e=copy.deepcopy(self.reviews[5647]);e['Inicio']+=1;e['Fin']+=1
        with self.assertRaises(ValueError):self.parts(5647,review=e,text='“'+self.raw[5647]['Texto'])
    def test_5367_has_herrera_fuentes_claro_not_one_expositor(self):
        parts=self.parts(5367)
        self.assertEqual([a for t,a,m in parts],['Miguel Fuentes Díaz','Luis Óscar Herrera Barriga','Miguel Fuentes Díaz','Sebastián Claro Edwards'])
        self.assertIn('Se solicita por parte de los señores Consejeros',parts[0][0])
        self.assertIn('B A N C O C E N T R A L D E C H IL E',parts[0][0])
        self.assertNotIn('Se solicita',parts[1][0]);self.assertIn('endeudamiento',parts[3][0])
    def test_3191_only_final_garcia_is_adjudicated(self):
        parts=self.parts(3191)
        self.assertEqual([a for t,a,m in parts],['Enrique Marshall Rivera','Pablo García Silva'])
        self.assertIn('señor Presidente y el señor Claudio Soto coinciden',parts[0][0])
        self.assertIn('Sebastián Claro',parts[0][0]);self.assertIn('Manuel Marfán',parts[1][0])
        self.assertNotEqual(parts[0][2],'CONTEXTO_REVISADO')
    def test_joint_warnings_cover_exact_residues_not_recovered_speakers(self):
        warnings=load_context_warnings(self.raw)
        for p in [3191,5367]:
            rows=[dict(ID=i,ID_Padre=p,Fecha=self.raw[p]['Fecha'],Texto=t,Actor_Final=a,Motivos_Revision=JOINT_MOTIVE if i==0 else '') for i,(t,a,m) in enumerate(self.parts(p))]
            self.assertFalse(validate_context_warnings(rows,{p:warnings[p]}))
            self.assertEqual(contextual_motives(rows[0],warnings),[JOINT_MOTIVE])
            for row in rows[1:]:self.assertEqual(contextual_motives(row,warnings),[])
            rows[0]['Actor_Final']='Sebastián Claro Edwards'
            self.assertTrue(validate_context_warnings(rows,{p:warnings[p]}))
    def test_registered_warning_motives_share_continuity_barrier(self):
        from context_warnings import DECISIONS
        for motive in DECISIONS:
            self.assertTrue(has_context_warning('FINAL_SIN_PUNTUACION;'+motive))
            rows=[dict(ID_Intervencion=str(i),ID_Bloque_Texto=str(i),Fecha='2010-06-15',Texto='El señor Pablo García señala una cifra.',Actor_Final='Pablo García Silva',Fuente_Actor='SUJETO_NOMBRE',Tipo_Acta='',Motivos_Revision=motive if i==0 else '') for i in range(2)]
            annotate_turns(rows);self.assertNotEqual(rows[0]['ID_Turno'],rows[1]['ID_Turno']);self.assertFalse(rows[1]['ID_Antecedente_Continuidad'])
        self.assertFalse(has_context_warning('FINAL_SIN_PUNTUACION'))
        self.assertFalse(has_context_warning('PREFIJO_'+JOINT_MOTIVE))
    def test_explicit_end_preserves_same_actor_and_different_sources(self):
        for p in [1092,2790]:
            parts=self.parts(p)
            self.assertEqual(len(parts),2);self.assertEqual(parts[0][1],parts[1][1])
            self.assertEqual([m for t,a,m in parts],['CONTEXTO_REVISADO','SUJETO_NOMBRE'])
            self.assertTrue(parts[1][0].startswith(self.reviews[p]['Cita_Ancla_Posterior']))
    def test_end_alone_does_not_create_a_cut(self):
        e=copy.deepcopy(self.reviews[2790]);del e['Cita_Ancla_Posterior']
        self.assertEqual(len(self.parts(2790,review=e)),1)
    def test_explicit_end_quote_must_match_source(self):
        e=copy.deepcopy(self.reviews[2790]);e['Cita_Ancla_Posterior']='No existe'
        with self.assertRaises(ValueError):self.load_entry(e)
        with self.assertRaises(ValueError):self.parts(2790,review=e)
    def test_explicit_end_rejects_nonstring_and_empty(self):
        for v in [None,False,[],123,'']:
            e=copy.deepcopy(self.reviews[2790]);e['Cita_Ancla_Posterior']=v
            with self.assertRaises(ValueError):self.load_entry(e)
            with self.assertRaises(ValueError):self.parts(2790,review=e)
    def test_explicit_end_must_be_sentence_boundary(self):
        e=copy.deepcopy(self.reviews[2790]);e['Fin']+=1;e['Cita_Ancla_Posterior']=self.raw[2790]['Texto'][e['Fin']:e['Fin']+80]
        with self.assertRaises(ValueError):self.parts(2790,review=e)
    def test_explicit_end_rejects_anaphora(self):
        e=copy.deepcopy(self.reviews[2790]);t=self.raw[2790]['Texto'];e['Fin']=t.index('Menciona que las noticias');e['Cita_Ancla_Posterior']='Menciona que las noticias'
        with self.assertRaises(ValueError):self.parts(2790,review=e)
    def test_explicit_end_rejects_different_speaker(self):
        e=copy.deepcopy(self.reviews[1899]);e['Cita_Ancla_Posterior']='El Gerente señor Claudio Soto comenta'
        with self.assertRaises(ValueError):self.parts(1899,review=e)
    def test_explicit_end_restores_soto_anchor_not_review_anchor(self):
        rows=[]
        for p in [2790,2791]:
            for i,(t,a,m) in enumerate(self.parts(p)):
                rows.append(dict(ID_Intervencion=f'{p}:{i}',ID_Bloque_Texto=f'{p}:{i}',Fecha=self.raw[p]['Fecha'],Texto=t,Actor_Final=a,Fuente_Actor=m,Tipo_Acta='',Motivos_Revision=''))
        annotate_turns(rows)
        self.assertFalse(rows[0]['ID_Ancla_Actor']);self.assertNotEqual(rows[0]['ID_Turno'],rows[1]['ID_Turno'])
        self.assertEqual(rows[1]['ID_Turno'],rows[2]['ID_Turno']);self.assertEqual(rows[2]['ID_Antecedente_Continuidad'],'2790:1')
    def test_return_to_marfan_and_chair_are_not_consumed(self):
        self.assertEqual([a for t,a,m in self.parts(1899)],['Manuel Marfán Lewis','Claudio Soto Gamboa','Manuel Marfán Lewis'])
        self.assertEqual([a for t,a,m in self.parts(5207)],['Claudio Soto Gamboa','Rodrigo Vergara Montes',b.CONSEJO])
    def test_unresolved_identity_and_inline_mention_not_forced(self):
        self.assertFalse({6185,2126,3989}&set(self.reviews))
        self.assertTrue(any(e["Actor"]=="Miguel Ricaurte Bermúdez" for e in speaker_intervals(self.reviews[6443])))  # separación local; variante pendiente
        self.assertIn(780,b.load_context_warnings(self.raw))  # puente inicial todavía pendiente
        self.assertIn(6530,b.load_context_warnings(self.raw))  # nombre literal no certificado
    def test_local_ocr_variants_preserved(self):
        for p,cue in [(392,'Klauss Schmidt'),(3385,'Marfán Manuel'),(790,'si posible')]:
            self.assertIn(cue,self.parts(p)[0][0])
    def test_parent_392_exact_segments_and_conservation(self):
        parts=self.parts(392)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Klaus Schmidt-Hebbel Dunker', 858, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[392]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=392,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{392:self.reviews[392]}))
    def test_parent_629_exact_segments_and_conservation(self):
        parts=self.parts(629)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Andrés Velasco Brañes', 248, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[629]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=629,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{629:self.reviews[629]}))
    def test_parent_790_exact_segments_and_conservation(self):
        parts=self.parts(790)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 164, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[790]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=790,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{790:self.reviews[790]}))
    def test_parent_1092_exact_segments_and_conservation(self):
        parts=self.parts(1092)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Esteban Jadresic Marinovic', 276, 'CONTEXTO_REVISADO'), ('Esteban Jadresic Marinovic', 2821, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1092]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=1092,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{1092:self.reviews[1092]}))
    def test_parent_1128_exact_segments_and_conservation(self):
        parts=self.parts(1128)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 82, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1128]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=1128,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{1128:self.reviews[1128]}))
    def test_parent_1758_exact_segments_and_conservation(self):
        parts=self.parts(1758)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Andrés Velasco Brañes', 509, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1758]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=1758,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{1758:self.reviews[1758]}))
    def test_parent_1842_exact_segments_and_conservation(self):
        parts=self.parts(1842)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('María Olivia Recart Herrera', 1116, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1842]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=1842,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{1842:self.reviews[1842]}))
    def test_parent_1899_exact_segments_and_conservation(self):
        parts=self.parts(1899)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 490, 'CONTEXTO_REVISADO'), ('Claudio Soto Gamboa', 1416, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 141, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1899]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=1899,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{1899:self.reviews[1899]}))
    def test_parent_2790_exact_segments_and_conservation(self):
        parts=self.parts(2790)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 594, 'CONTEXTO_REVISADO'), ('Claudio Soto Gamboa', 3179, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2790]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=2790,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{2790:self.reviews[2790]}))
    def test_parent_3189_exact_segments_and_conservation(self):
        parts=self.parts(3189)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 476, 'CONTEXTO_REVISADO'), ('Pablo García Silva', 82, 'SUJETO_NOMBRE'), ('Manuel Marfán Lewis', 706, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3189]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=3189,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{3189:self.reviews[3189]}))
    def test_parent_3191_exact_segments_and_conservation(self):
        parts=self.parts(3191)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 520, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 471, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3191]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=3191,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{3191:self.reviews[3191]}))
    def test_parent_3385_exact_segments_and_conservation(self):
        parts=self.parts(3385)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 510, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3385]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=3385,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{3385:self.reviews[3385]}))
    def test_parent_5207_exact_segments_and_conservation(self):
        parts=self.parts(5207)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 2098, 'CONTEXTO_REVISADO'), ('Rodrigo Vergara Montes', 209, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 75, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5207]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=5207,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{5207:self.reviews[5207]}))
    def test_parent_5367_exact_segments_and_conservation(self):
        parts=self.parts(5367)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Miguel Fuentes Díaz', 2995, 'SUJETO_NOMBRE'), ('Luis Óscar Herrera Barriga', 409, 'CONTEXTO_REVISADO'), ('Miguel Fuentes Díaz', 223, 'SUJETO_NOMBRE'), ('Sebastián Claro Edwards', 314, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5367]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=5367,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{5367:self.reviews[5367]}))
    def test_parent_5647_exact_segments_and_conservation(self):
        parts=self.parts(5647)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 221, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 675, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5647]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=5647,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{5647:self.reviews[5647]}))
    def test_parent_7019_exact_segments_and_conservation(self):
        parts=self.parts(7019)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Pablo García Silva', 186, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[7019]['Texto'].split()))
        rows=[dict(ID=i,ID_Padre=7019,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{7019:self.reviews[7019]}))
    def test_warning_2126_is_exact_and_not_an_attribution_fix(self):
        warnings=load_context_warnings(self.raw);e=warnings[2126]
        self.assertEqual(e['Actor_Provisional'],'Sebastián Claro Edwards')
        self.assertEqual(e['Motivo'],'PASAJES_CONJUNTOS_POR_DELIMITAR');self.assertIn('Vicepresidente y el Consejero',e['Texto_Intervalo'])
        rows=[dict(ID=i,ID_Padre=2126,Fecha=self.raw[2126]['Fecha'],Texto=t,Actor_Final=(b.detect(t,self.raw[2126]['Fecha'])[0] if m is None else a),Motivos_Revision='') for i,(t,a,m) in enumerate(self.parts(2126))]
        matching=[r for r in rows if contextual_motives(r,warnings)]
        self.assertEqual(len(matching),1);matching[0]['Motivos_Revision']=e['Motivo']
        self.assertFalse(validate_context_warnings(rows,{2126:e}))
        matching[0]['Texto']+=' agregado';self.assertTrue(validate_context_warnings(rows,{2126:e}))
    def test_warning_3989_is_exact_and_not_an_attribution_fix(self):
        warnings=load_context_warnings(self.raw);e=warnings[3989]
        self.assertEqual(e['Actor_Provisional'],'José De Gregorio Rebeco')
        self.assertEqual(e['Motivo'],'PASAJES_CONJUNTOS_POR_DELIMITAR');self.assertIn('Enrique Marshall coinciden',e['Texto_Intervalo'])
        rows=[dict(ID=i,ID_Padre=3989,Fecha=self.raw[3989]['Fecha'],Texto=t,Actor_Final=a,Motivos_Revision='') for i,(t,a,m) in enumerate(self.parts(3989))]
        matching=[r for r in rows if contextual_motives(r,warnings)]
        self.assertEqual(len(matching),1);matching[0]['Motivos_Revision']=e['Motivo']
        self.assertFalse(validate_context_warnings(rows,{3989:e}))
        matching[0]['Texto']+=' agregado';self.assertTrue(validate_context_warnings(rows,{3989:e}))
    def test_warning_2661_archived_after_loop24_separation(self):
        warnings=load_context_warnings(self.raw);self.assertNotIn(2661,warnings)
        archive=json.loads(Path('data/curation/alertas_contextuales_retiradas.json').read_text())
        old=next(e['Alerta_Original'] for e in archive if e['Alerta_Original']['ID_Padre']==2661)
        self.assertEqual(old['Actor_Provisional'],'Jorge Desormeaux Jiménez')
        self.assertEqual(old['Motivo'],'PASAJES_CONJUNTOS_POR_DELIMITAR')
        self.assertEqual(' '.join(t for t,a,m in self.parts(2661)[4:6]),old['Texto_Intervalo'])
        self.assertEqual([a for t,a,m in self.parts(2661)[4:6]],['Jorge Desormeaux Jiménez','Sergio Lehmann Beresi'])
    def test_warning_2704_archived_after_loop23_separation(self):
        warnings=load_context_warnings(self.raw);self.assertNotIn(2704,warnings)
        archive=json.loads(Path('data/curation/alertas_contextuales_retiradas.json').read_text())
        old=next(e['Alerta_Original'] for e in archive if e['Alerta_Original']['ID_Padre']==2704)
        self.assertEqual(old['Actor_Provisional'],'Enrique Marshall Rivera')
        self.assertEqual(old['Motivo'],'PASAJES_CONJUNTOS_POR_DELIMITAR')
        self.assertEqual(len(old['Texto_Intervalo']),210)
        self.assertEqual([(a,len(t)) for t,a,m in self.parts(2704)[-2:]],[('Enrique Marshall Rivera',161),('Claudio Soto Gamboa',48)])
    def test_warning_2667_is_exact_and_not_an_attribution_fix(self):
        warnings=load_context_warnings(self.raw);e=warnings[2667]
        self.assertEqual(e['Actor_Provisional'],'Sergio Lehmann Beresi')
        self.assertEqual(e['Motivo'],'TEXTO_DANADO_POR_COTEJAR');self.assertIn('y el Gerente de',e['Texto_Intervalo'])
        rows=[dict(ID=i,ID_Padre=2667,Fecha=self.raw[2667]['Fecha'],Texto=t,Actor_Final=a,Motivos_Revision='') for i,(t,a,m) in enumerate(self.parts(2667))]
        matching=[r for r in rows if contextual_motives(r,warnings)]
        self.assertEqual(len(matching),1);matching[0]['Motivos_Revision']=e['Motivo']
        self.assertFalse(validate_context_warnings(rows,{2667:e}))
        matching[0]['Texto']+=' agregado';self.assertTrue(validate_context_warnings(rows,{2667:e}))
    def test_warning_3107_is_exact_and_not_an_attribution_fix(self):
        warnings=load_context_warnings(self.raw);e=warnings[3107]
        self.assertEqual(e['Actor_Provisional'],'Matías Bernier Bórquez')
        self.assertEqual(e['Motivo'],'TEXTO_DANADO_POR_COTEJAR');self.assertIn('han sido que no ha renovado',e['Texto_Intervalo'])
        rows=[dict(ID=i,ID_Padre=3107,Fecha=self.raw[3107]['Fecha'],Texto=t,Actor_Final=a,Motivos_Revision='') for i,(t,a,m) in enumerate(self.parts(3107))]
        matching=[r for r in rows if contextual_motives(r,warnings)]
        self.assertEqual(len(matching),1);matching[0]['Motivos_Revision']=e['Motivo']
        self.assertFalse(validate_context_warnings(rows,{3107:e}))
        matching[0]['Texto']+=' agregado';self.assertTrue(validate_context_warnings(rows,{3107:e}))
    def test_explicit_end_cannot_reach_end_of_parent(self):
        e=copy.deepcopy(self.reviews[2790]);e['Fin']=len(self.raw[2790]['Texto']);e['Cita_Ancla_Posterior']='X'
        with self.assertRaises(ValueError):self.load_entry(e)
        with self.assertRaises(ValueError):self.parts(2790,review=e)
    def test_damage_warning_does_not_remove_reviewed_bernier(self):
        parts=self.parts(3107)
        self.assertEqual(parts[-1][1:2],('Matías Bernier Bórquez',))
        self.assertEqual(parts[-1][2],'CONTEXTO_REVISADO')
        self.assertIn('Agrega que el ha ido',parts[-1][0])
