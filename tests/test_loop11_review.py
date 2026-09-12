"""Loop11: varios intervalos independientes, cita cerrada y conservación.
Las fixtures son contratos de regresión, no lectura humana integral del corpus.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, speaker_intervals, validate_speaker_reviews
from continuity import annotate_turns

class LoopElevenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)
        cls.entries=json.loads(Path('data/curation/revisiones_hablantes.json').read_text())
    def parts(self,p):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p))
    def load_entries(self,entries):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'reviews.json';p.write_text(json.dumps(entries))
            return load_speaker_reviews(self.raw,p)
    def root(self,p):
        return copy.deepcopy(next(e for e in self.entries if e['ID_Padre']==p))
    def rows(self,p):
        return [dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p))]
    def test_root_and_interval_counts_are_distinct(self):
        self.assertEqual(len(self.reviews),357)
        self.assertEqual(sum(len(speaker_intervals(r)) for r in self.reviews.values()),386)
        self.assertEqual({p for p,r in self.reviews.items() if len(speaker_intervals(r))>1},{506,644,664,1090,1923,2622,4923,5367,6009,6015,6016,6443,2957,3476,5108,6277,6021,631,6862,2674,2525,2738,2704,3268,2661,2788})
    def test_empty_and_single_review_compatibility(self):
        self.assertEqual(speaker_intervals(None),[])
        single=self.reviews[4706]
        self.assertEqual(speaker_intervals(single),[single])
    def test_all_intervals_in_two_dialogues_validate(self):
        for p in [2622,4923]:
            self.assertFalse(validate_speaker_reviews(self.rows(p),{p:self.reviews[p]}))
    def test_secondary_interval_cannot_be_missing(self):
        for p in [2622,4923]:
            rows=self.rows(p);last=max(i for i,r in enumerate(rows) if r['Fuente_Actor']=='CONTEXTO_REVISADO')
            rows[last]['Fuente_Actor']='SUJETO_NOMBRE'
            self.assertTrue(validate_speaker_reviews(rows,{p:self.reviews[p]}))
    def test_secondary_interval_cannot_change_actor(self):
        rows=self.rows(4923);rows[-1]['Actor_Final']='Rodrigo Vergara Montes'
        self.assertTrue(validate_speaker_reviews(rows,{4923:self.reviews[4923]}))
    def test_secondary_interval_cannot_expand(self):
        rows=self.rows(4923);rows[-1]['Texto']+=' añadido'
        self.assertTrue(validate_speaker_reviews(rows,{4923:self.reviews[4923]}))
    def test_source_offsets_detect_displacement(self):
        rows=self.rows(4923);rows[0]['Texto']+=' añadido'
        self.assertTrue(any('desplazado' in e for e in validate_speaker_reviews(rows,{4923:self.reviews[4923]})))
    def test_secondary_hash_date_and_parent_must_match(self):
        for field,value in [('SHA256_Texto_Padre','0'*64),('Fecha','2000-01-01'),('ID_Padre',4954)]:
            e=self.root(4923);e['Revisiones_Adicionales'][0][field]=value
            with self.assertRaises(ValueError):self.load_entries([e])
    def test_secondary_requires_its_own_evidence_and_quote(self):
        for field,value in [('Evidencia',[]),('Cita_Inicio','inexistente'),('Justificacion','')]:
            e=self.root(4923);e['Revisiones_Adicionales'][0][field]=value
            with self.assertRaises(ValueError):self.load_entries([e])
    def test_duplicate_revision_ids_across_intervals_rejected(self):
        e=self.root(4923);e['Revisiones_Adicionales'][0]['Revision_ID']=e['Revision_ID']
        with self.assertRaisesRegex(ValueError,'duplicada'):self.load_entries([e])
    def test_overlapping_intervals_rejected(self):
        e=self.root(4923);e['Fin']=e['Revisiones_Adicionales'][0]['Fin']
        with self.assertRaisesRegex(ValueError,'solapados'):self.load_entries([e])
    def test_out_of_order_intervals_rejected(self):
        e=self.root(4923);secondary=e.pop('Revisiones_Adicionales')[0];secondary['Revisiones_Adicionales']=[e]
        with self.assertRaisesRegex(ValueError,'solapados'):self.load_entries([secondary])
    def test_nested_or_nonlist_secondary_entries_rejected(self):
        e=self.root(4923);e['Revisiones_Adicionales'][0]['Revisiones_Adicionales']=[]
        with self.assertRaises(ValueError):self.load_entries([e])
        e=self.root(4923);e['Revisiones_Adicionales']={}
        with self.assertRaises(ValueError):self.load_entries([e])
    def test_duplicate_starts_rejected_even_without_loader(self):
        e=copy.deepcopy(self.reviews[4923]);e['Revisiones_Adicionales'][0]['Inicio']=e['Inicio']
        r=self.raw[4923]
        with self.assertRaisesRegex(ValueError,'duplicados'):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)
    def test_4923_three_speakers_with_two_independent_opinions(self):
        self.assertEqual([a for t,a,m in self.parts(4923)],['Claudio Soto Gamboa','Rodrigo Vergara Montes','Enrique Marshall Rivera'])
    def test_2622_presidential_opinion_and_later_soto_coordination(self):
        parts=self.parts(2622)
        self.assertEqual([a for t,a,m in parts],['Enrique Marshall Rivera','José De Gregorio Rebeco','Claudio Soto Gamboa','José De Gregorio Rebeco','Pablo García Silva','Claudio Soto Gamboa'])
        self.assertIn('Anális is',parts[-1][0])
    def test_4954_question_stays_with_soto_then_marfan_returns(self):
        parts=self.parts(4954)
        self.assertEqual([(a,len(t)) for t,a,m in parts],[('Manuel Marfán Lewis',229),('Claudio Soto Gamboa',119),('Manuel Marfán Lewis',206)])
        self.assertTrue(parts[1][0].endswith('Chile?”'))
        self.assertTrue(parts[2][0].startswith('En opinión'))
    def test_4954_without_review_does_not_generalize_quote_boundary(self):
        r=self.raw[4954];parts=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertEqual([a for t,a,m in parts],['Manuel Marfán Lewis','Claudio Soto Gamboa'])
        for t in ['En opinión del Vicepresidente señor Manuel Marfán, las cifras aumentan.',
                  'A juicio del Consejero señor Enrique Marshall, las cifras aumentan.']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(t,r['Fecha']))
    def test_quote_review_rejects_wrong_actor(self):
        e=copy.deepcopy(self.reviews[4954]);e['Actor']='Claudio Soto Gamboa';r=self.raw[4954]
        with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)
    def test_quote_review_requires_closed_quote_and_punctuation(self):
        e=copy.deepcopy(self.reviews[4954]);r=self.raw[4954]
        for replacement in ['Chile? ','Chile ”','Chile?“']:
            t=r['Texto'].replace('Chile?”',replacement)
            self.assertEqual(len(t),len(r['Texto']))
            with self.assertRaises(ValueError):b.segment_turns(t,r['Fecha'],r['Actor'],review=e)
    def test_14_review_does_not_remove_relative_guard(self):
        r=self.raw[14]
        self.assertIsNone(b.TURN_DETECTOR.speaker(r['Texto'],r['Fecha']))
        self.assertEqual(self.parts(14)[0][2],'CONTEXTO_REVISADO')
    def test_normalization_preserves_output_and_is_idempotent(self):
        from turns import normalize
        for p,needle in [(178,'A l respecto'),(1756,'Interino'),(2662,'División de Estudios'),(2622,'Anális is')]:
            t=self.raw[p]['Texto'];self.assertEqual(normalize(t),normalize(normalize(t)))
            self.assertIn(needle,''.join(t for t,a,m in self.parts(p)))
    def test_new_role_variant_needs_predicate_not_attendance(self):
        for title in ['El Gerente de División de Estudios','El Gerente Interino señor Claudio Soto']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(title+' está presente.','2009-08-13'))
            self.assertIsNone(b.TURN_DETECTOR.speaker('“'+title+' señala una cifra.”','2009-08-13'))
    def test_bounded_opinions_keep_expositor_returns(self):
        for p,actor in [(3310,'Claudio Soto Gamboa'),(4437,'Claudio Soto Gamboa')]:
            parts=self.parts(p);i=next(i for i,(t,a,m) in enumerate(parts) if m=='CONTEXTO_REVISADO')
            self.assertEqual(parts[i-1][1],actor);self.assertEqual(parts[i+1][1],actor)
    def test_each_secondary_remains_without_anchor(self):
        for t,a,m in self.parts(4923)[1:]:
            rows=[dict(ID_Intervencion='1',ID_Bloque_Texto='1',Fecha=self.raw[4923]['Fecha'],Texto=t,Actor_Final=a,Fuente_Actor=m,Tipo_Acta='INTERVENCION',Motivos_Revision='')]
            annotate_turns(rows);self.assertFalse(rows[0]['ID_Ancla_Actor'])
    def test_ricaurte_and_joint_priorities_remain_unadjudicated(self):
        self.assertFalse({6185,2126}&set(self.reviews))
        self.assertTrue(any(e["Actor"]=="Miguel Ricaurte Bermúdez" for e in speaker_intervals(self.reviews[6443])))  # separación local; variante pendiente
        self.assertIn(780,b.load_context_warnings(self.raw))  # puente inicial todavía pendiente

    def test_both_context_warning_scopes_validate_without_certifying_actor(self):
        from context_warnings import load_context_warnings, validate_context_warnings
        warnings=load_context_warnings(self.raw)
        rows=[dict(ID=i,ID_Padre=p,Fecha=e['Fecha'],Actor_Final=e['Actor_Provisional'],Texto=e['Texto_Intervalo'],Motivos_Revision=e['Motivo']) for i,(p,e) in enumerate(warnings.items())]
        self.assertEqual(set(warnings),{180,5573,6282,4433,3191,5367,2126,3989,2667,3107,587,836,644,664,770,1012,1047,1155,506,780,6530,4364,6013,6015,1003,1424,1663,1860,2473,2865,2957,2990,3476,3619,2349,3050,3315,205,510,1013,1728,2695,2803,2969,5366,6021,7182,518,520,632,2141,4289,4446,6862,1904,2463,2525,2674,2938,2885,3268,3775,5643,2680,2788,2958,3008,4055,1004,2948,3071,4064,2510,3045,1298,1379,3340,202,2701,3147,5078,665,6250,6456})
        self.assertFalse(validate_context_warnings(rows,warnings))
        self.assertTrue(validate_context_warnings(rows[:-1],warnings))
        rows[-1]['Motivos_Revision']=''
        self.assertTrue(validate_context_warnings(rows,warnings))
    def archived_6443_warning(self):
        from context_warnings import load_context_warnings
        archive=json.loads((Path(b.__file__).resolve().parents[1]/'data/curation/alertas_contextuales_retiradas.json').read_text())
        e=next(x['Alerta_Original'] for x in archive if x['Alerta_Original']['ID_Padre']==6443)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'warning.json';path.write_text(json.dumps([e]))
            return load_context_warnings(self.raw,path)[6443]
    def test_identity_warning_rejects_unregistered_or_wrong_motive(self):
        from context_warnings import load_context_warnings, validate_context_warnings
        e=self.archived_6443_warning()
        row=dict(ID=1,ID_Padre=6443,Fecha=e['Fecha'],Actor_Final=e['Actor_Provisional'],Texto=e['Texto_Intervalo'],Motivos_Revision=e['Motivo'])
        self.assertTrue(validate_context_warnings([row],{}))
        row['Motivos_Revision']='CARGO_EN_DISCURSO_POR_VERIFICAR'
        self.assertTrue(validate_context_warnings([row],{6443:e}))
    def test_identity_warning_blocks_downstream_group_even_for_same_actor(self):
        from context_warnings import load_context_warnings
        e=self.archived_6443_warning()
        rows=[dict(ID_Intervencion=str(i),ID_Bloque_Texto=str(i),Fecha=e['Fecha'],Actor_Final=e['Actor_Provisional'],Texto=t,Fuente_Actor='SUJETO_ROL_NOMBRE',Tipo_Acta='INTERVENCION',Motivos_Revision=e['Motivo'] if i==0 else '') for i,t in enumerate([e['Texto_Intervalo'],'El señor Beltrán de Ramón señala otro punto.'])]
        annotate_turns(rows)
        self.assertNotEqual(rows[0]['ID_Turno'],rows[1]['ID_Turno'])
    def test_6443_separation_replaces_archived_warning_not_global_identity(self):
        from context_warnings import load_context_warnings
        e=self.archived_6443_warning()
        self.assertEqual(e['Decision'],'PENDIENTE_SEPARACION_E_IDENTIDAD')
        self.assertIn('Miguel Ricaurte retoma',e['Texto_Intervalo'])
        self.assertIn('En opinión del Consejero señor Pablo García',e['Texto_Intervalo'])
        self.assertEqual([a for t,a,m in self.parts(6443)],['Beltrán de Ramón Acevedo','Pablo García Silva','Miguel Ricaurte Bermúdez','Beltrán de Ramón Acevedo','Miguel Ricaurte Bermúdez'])
        self.assertNotIn(6443,load_context_warnings(self.raw))

FIXTURES = {14: {'hash': '6792502ab9eed5ccfe5c098a7c1da6ede20c10af3703e1d2f664ab48e3519085',
      'parts': [('Esteban Jadresic Marinovic', 822, 'CONTEXTO_REVISADO')]},
 178: {'hash': '652f4f30978b72c57dba90549181aedf6c1e6c6dfcdc80b4c72295d2868a45c4',
       'parts': [('Rodrigo Valdés Pulido', 6176, 'CONTEXTO_REVISADO'),
                 ('Vittorio Corbo Lioi', 69, 'SUJETO_ROL_NOMBRE')]},
 641: {'hash': '7d8b40fbdb92b4a37db1c001784df62a618c1242134f8ab827492bd3369b80b1',
       'parts': [('Manuel Marfán Lewis', 251, 'SUJETO_ROL_NOMBRE'),
                 ('Rodrigo Valdés Pulido', 107, 'SUJETO_ROL_SESION')]},
 1756: {'hash': '82ecad4950a7c495754f614feb390b2ce252b64caa4fe5e0e1ea6c3df14f00e5',
        'parts': [('Claudio Soto Gamboa', 109, 'SUJETO_ROL_NOMBRE')]},
 2220: {'hash': 'c647f47ec64ddaa910485cc65bd47e481e4aadd23ec31dc06255fe0e4085f899',
        'parts': [('Pablo García Silva', 433, 'CONTEXTO_REVISADO'),
                  ('Sebastián Claro Edwards', 356, 'SUJETO_ROL_NOMBRE')]},
 2622: {'hash': '5426afc76089e253b26fd2f323058ac46d92490efc1ff8e87529fa762600108d',
        'parts': [('Enrique Marshall Rivera', 586, 'SUJETO_ROL_NOMBRE'),
                  ('José De Gregorio Rebeco', 203, 'CONTEXTO_REVISADO'),
                  ('Claudio Soto Gamboa', 52, 'SUJETO_NOMBRE'),
                  ('José De Gregorio Rebeco', 165, 'SUJETO_ROL_SESION'),
                  ('Pablo García Silva', 70, 'SUJETO_ROL_SESION'),
                  ('Claudio Soto Gamboa', 151, 'CONTEXTO_REVISADO')]},
 2635: {'hash': '0e2243330049b9e11e9fefa42ca1e942ccb675f8d11d95f0d884c0a9dade1851',
        'parts': [('José De Gregorio Rebeco', 147, 'SUJETO_ROL_NOMBRE'),
                  ('Claudio Soto Gamboa', 666, 'SUJETO_NOMBRE'),
                  ('José De Gregorio Rebeco', 151, 'SUJETO_ROL_NOMBRE'),
                  ('Pablo García Silva', 207, 'SUJETO_ROL_SESION'),
                  ('José De Gregorio Rebeco', 128, 'CONTEXTO_REVISADO')]},
 2662: {'hash': 'ff85299eb677bad979ef217ccd1d910e2bd9ad4a1efb36e1a6dc275b4404e6f2',
        'parts': [('Pablo García Silva', 482, 'SUJETO_ROL_SESION'),
                  ('Sebastián Claro Edwards', 234, 'SUJETO_ROL_NOMBRE'),
                  ('Pablo García Silva', 629, 'SUJETO_NOMBRE'),
                  ('Sergio Lehmann Beresi', 771, 'SUJETO_ROL_SESION')]},
 2664: {'hash': 'c78ff05d7a93005e5594a4cb2ce2b32fe95a9200f9df39fc2d2251b92b50c8a8',
        'parts': [('José De Gregorio Rebeco', 235, 'SUJETO_ROL_SESION'),
                  ('Pablo García Silva', 162, 'SUJETO_ROL_SESION'),
                  ('Sergio Lehmann Beresi', 55, 'SUJETO_NOMBRE')]},
 2670: {'hash': '81bbb42efb6bfd5442c5d2d760088e7730f873b620e1211cd81ecfb3bac3f574',
        'parts': [('José De Gregorio Rebeco', 73, 'SUJETO_ROL_NOMBRE'),
                  ('Pablo García Silva', 706, 'SUJETO_ROL_SESION')]},
 2671: {'hash': '2df6e74c87d01b6606585e58d81dc64d258928adc998231a1617c61761c985e6',
        'parts': [('Claudio Soto Gamboa', 1060, 'SUJETO_NOMBRE'),
                  ('Pablo García Silva', 285, 'SUJETO_ROL_SESION'),
                  ('Claudio Soto Gamboa', 170, 'SUJETO_NOMBRE')]},
 2674: {'hash': 'd0bf1f145f07f3db3c185f7076213df875edad8f8c7939c209fd9dbbdae088aa',
        'parts': [('Claudio Soto Gamboa', 2116, 'SUJETO_NOMBRE'),
                  ('Enrique Marshall Rivera', 470, 'CONTEXTO_REVISADO'),
                  ('Claudio Soto Gamboa', 1507, 'SUJETO_ROL_SESION'),
                  ('Kevin Cowan Logan', 386, 'SUJETO_ROL_NOMBRE'),
                  ('Igal Magendzo Weinberger', 237, 'SUJETO_ROL_NOMBRE'),
                  ('Pablo García Silva', 387, 'SUJETO_ROL_SESION'),
                  ('Claudio Soto Gamboa', 635, 'SUJETO_ROL_NOMBRE'),
                  ('Enrique Marshall Rivera', 1159, 'CONTEXTO_REVISADO'),
                  ('Claudio Soto Gamboa', 889, 'SUJETO_ROL_SESION'),
                  ('Andrés Velasco Brañes', 447, 'SUJETO_ROL_SESION')]},
 2703: {'hash': '7584c8bd29e362e16b866d26c5b015051836c37361c096a590a53fde9c53b19c',
        'parts': [('José De Gregorio Rebeco', 335, 'CONTEXTO_REVISADO'),
                  ('Kevin Cowan Logan', 757, 'SUJETO_NOMBRE'),
                  ('Claudio Soto Gamboa', 622, 'SUJETO_ROL_SESION'),
                  ('José De Gregorio Rebeco', 200, 'SUJETO_ROL_NOMBRE'),
                  ('Andrés Velasco Brañes', 579, 'SUJETO_ROL_NOMBRE'),
                  ('Claudio Soto Gamboa', 1592, 'SUJETO_ROL_SESION')]},
 2776: {'hash': 'cc97a9800038fe3d56153c639f94908d66d3312a7567e4f1fa4a70b2a208fa47',
        'parts': [('José De Gregorio Rebeco', 719, 'SUJETO_ROL_SESION'),
                  ('Jorge Desormeaux Jiménez', 187, 'SUJETO_ROL_SESION'),
                  ('José De Gregorio Rebeco', 264, 'SUJETO_NOMBRE'),
                  ('Manuel Marfán Lewis', 961, 'SUJETO_ROL_NOMBRE'),
                  ('Igal Magendzo Weinberger', 872, 'SUJETO_ROL_NOMBRE'),
                  ('Jorge Desormeaux Jiménez', 1501, 'CONTEXTO_REVISADO'),
                  ('Andrés Velasco Brañes', 1494, 'SUJETO_ROL_SESION')]},
 3173: {'hash': '116fa6cab93f68943f267b70ac731716db423d5f93540483115290c912e00362',
        'parts': [('Claudio Soto Gamboa', 165, 'SUJETO_NOMBRE'),
                  ('Manuel Marfán Lewis', 354, 'CONTEXTO_REVISADO')]},
 3262: {'hash': '6a4a3a629c984e1254b46026403b9657c6e9432e4dfa4a2b354dda79afb658ca',
        'parts': [('Manuel Marfán Lewis', 259, 'CONTEXTO_REVISADO'),
                  ('Claudio Soto Gamboa', 1000, 'SUJETO_ROL_SESION')]},
 3310: {'hash': 'caac7007271cb2ee3ef53a531ad9d2b9a98bd7af9ef5602ca6a187b135decfe9',
        'parts': [('Claudio Soto Gamboa', 340, 'SUJETO_NOMBRE'),
                  ('Manuel Marfán Lewis', 467, 'SUJETO_ROL_NOMBRE'),
                  ('Claudio Soto Gamboa', 100, 'SUJETO_NOMBRE'),
                  ('Pablo García Silva', 758, 'CONTEXTO_REVISADO'),
                  ('Claudio Soto Gamboa', 1137, 'SUJETO_NOMBRE'),
                  ('Rodrigo Cerda Norambuena', 385, 'SUJETO_ROL_NOMBRE'),
                  ('Claudio Soto Gamboa', 498, 'SUJETO_NOMBRE')]},
 4297: {'hash': 'c06f51527a55eb27667f87de169c7ed0c266d425ab1fc9beb756e9a58ae96e2f',
        'parts': [('Manuel Marfán Lewis', 831, 'CONTEXTO_REVISADO')]},
 4437: {'hash': '87940dd907ce3841cc8533528dc2d2788522887088a6bc5d32ccad2bb82a68d7',
        'parts': [('Claudio Soto Gamboa', 546, 'SUJETO_NOMBRE'),
                  ('Enrique Orellana Cifuentes', 231, 'CONTEXTO_REVISADO'),
                  ('Claudio Soto Gamboa', 219, 'SUJETO_NOMBRE')]},
 4665: {'hash': '4ad98fc33e28fa007c50552157d7c5eeb4b123985964b3ab0b5cc33c0d43e614',
        'parts': [('Kevin Cowan Logan', 804, 'SUJETO_NOMBRE'),
                  ('Luis Óscar Herrera Barriga', 492, 'CONTEXTO_REVISADO')]},
 4923: {'hash': '77916e8773747cbfbcb68b2e6dc4e954888a7c308ac197bbccb4c3832db88439',
        'parts': [('Claudio Soto Gamboa', 1247, 'SUJETO_NOMBRE'),
                  ('Rodrigo Vergara Montes', 140, 'CONTEXTO_REVISADO'),
                  ('Enrique Marshall Rivera', 225, 'CONTEXTO_REVISADO')]},
 4954: {'hash': '759550ba8d4a134cf097a00dc6d73ee3ed2e5502f2573a035b261a8c899e98f0',
        'parts': [('Manuel Marfán Lewis', 229, 'SUJETO_ROL_NOMBRE'),
                  ('Claudio Soto Gamboa', 119, 'SUJETO_NOMBRE'),
                  ('Manuel Marfán Lewis', 206, 'CONTEXTO_REVISADO')]},
 6060: {'hash': '44d79739742e26d59bf29fd4bb5b867a6b891ec5bf26e858f19caa045da6d371',
        'parts': [('Rodrigo Vergara Montes', 98, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 505, 'CONTEXTO_REVISADO')]},
 6308: {'hash': 'de05707a4bef7dfab0e52d8d551aee1072018d927d1a02e2af645345696ddeba',
        'parts': [('Pablo García Silva', 1830, 'SUJETO_ROL_NOMBRE'),
                  ('Rodrigo Vergara Montes', 2306, 'CONTEXTO_REVISADO')]},
 6443: {'hash': 'c2f9531c9d1bfad7d90bd4731fed1edd0d36feed20585aeb0a4be34609fa6f1a',
        'parts': [('Beltrán de Ramón Acevedo', 734, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 305, 'CONTEXTO_REVISADO'), ('Miguel Ricaurte Bermúdez', 7178, 'CONTEXTO_REVISADO'), ('Beltrán de Ramón Acevedo', 480, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 6399, 'CONTEXTO_REVISADO')]},
 6447: {'hash': '599825c4dce422c925abe439ae377e9a55c0b7c71f25600d9449827f94d2fdc3',
        'parts': [('Joaquín Vial Ruiz-Tagle', 2829, 'SUJETO_ROL_NOMBRE'),
                  ('Pablo García Silva', 1696, 'CONTEXTO_REVISADO')]},
 6505: {'hash': 'fa5742308ae4d2bb9e981ce8c6772bbfc3cc0aa3d8daf53795769e8c6068b3e9',
        'parts': [("Alberto Naudon Dell'Oro", 2969, 'CONTEXTO_REVISADO'),
                  ('Rodrigo Vergara Montes', 246, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 151, 'ACTA/META')]},
 7063: {'hash': '114ed441c32c084d80d9a7ac2ac548d0219afaeee908358ba7ea16786c869b90',
        'parts': [('Diego Gianelli Gómez', 4658, 'SUJETO_NOMBRE'),
                  ('Rodrigo Valdés Pulido', 307, 'CONTEXTO_REVISADO')]},
 7066: {'hash': '19dd9e44506c0a6875b2ce88187b3d9764ad1eb79755c7213c11e0a520f0c5b9',
        'parts': [('Pablo García Silva', 227, 'SUJETO_ROL_NOMBRE'),
                  ('Beltrán de Ramón Acevedo', 227, 'CONTEXTO_REVISADO')]}}

def fixture_test(p,e):
    def test(self):
        self.assertEqual(hashlib.sha256(self.raw[p]['Texto'].encode()).hexdigest(),e['hash'])
        parts=self.parts(p);actual=[]
        for t,a,m in parts:
            if m is None:
                d=b.detect(t,self.raw[p]['Fecha']);self.assertIsNotNone(d);a,_,m,_=d
            actual.append((a,len(' '.join(t.split())),m))
        self.assertEqual(actual,[tuple(x) for x in e['parts']])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[p]['Texto'].split()))
    return test
for p,e in FIXTURES.items():setattr(LoopElevenTests,f'test_parent_{p}',fixture_test(p,e))

if __name__=='__main__':unittest.main()
