"""Loop8: límites y evidencia explícita; no certificación integral del corpus."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews
from context_warnings import PATH, MOTIVE, load_context_warnings, contextual_motives, validate_context_warnings
from continuity import annotate_turns

class LoopEightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)
        cls.warnings={4433:load_context_warnings(cls.raw)[4433]}
    def parts(self,p):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p))
    def test_direct_predicates_require_subject_not_citation(self):
        for verb in ['da inicio a su presentación','procede a responder','se suma a lo expresado','discrepa',
                     'adhiere','califica','acoge','atribuye','recomienda','reafirma','ratifica','exhibe',
                     'hace alusión','quiere hacer un comentario','desea plantear']:
            t=f'El señor Sergio Lehmann {verb} lo ocurrido.'
            self.assertEqual(b.TURN_DETECTOR.speaker(t,'2013-08-13')['actor'],'Sergio Lehmann Beresi')
            for bad in ['“'+t+'”', 'Se cita que '+t, 'Según '+t.lower(),
                        f'La opinión del señor Sergio Lehmann {verb} lo ocurrido.']:
                self.assertIsNone(b.TURN_DETECTOR.speaker(bad,'2013-08-13'),bad)
    def test_se_suma_is_not_a_general_movement_or_attendance_rule(self):
        for t in ['El señor Sergio Lehmann se suma a la mesa.',
                  'El señor Sergio Lehmann se suma a la reunión.',
                  'El señor Sergio Lehmann se suma al grupo de asistentes.']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2013-08-13'))
    def test_opening_aside_number_and_main_verb_are_required(self):
        pre='El Presidente señor José De Gregorio, junto con dar inicio a la Reunión de Política Monetaria '
        t=pre+'N° 143, señala que fija la próxima sesión.'
        self.assertEqual(b.TURN_DETECTOR.speaker(t,'2010-02-11')['actor'],'José De Gregorio Rebeco')
        for bad in [pre+'N° 1430, señala una cifra.',pre+'N° xx, señala una cifra.',
                    pre+'N° 143, está presente.', '“'+t+'”',
                    pre+'N° 143 y tras escuchar al Consejero, señala una cifra.']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(bad,'2010-02-11'),bad)
    def test_parenthetical_still_cannot_borrow_other_speakers_verb(self):
        for t in ['El señor Claudio Soto, aludiendo a la cifra, explica el gráfico.',
                  'El señor Claudio Soto, en referencia al dato, explica el gráfico.']:
            self.assertEqual(b.TURN_DETECTOR.speaker(t,'2013-08-13')['actor'],'Claudio Soto Gamboa')
        for t in ['El señor Claudio Soto, aludiendo a lo que señala el Presidente, está presente.',
                  'La opinión del señor Claudio Soto, en referencia al dato, explica la diferencia.']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2013-08-13'))
    def test_vittoho_recognized_without_rewriting_text(self):
        for p in [263,266,1493,1495]:
            self.assertIn('Vittoho',self.parts(p)[0][0])
            self.assertEqual(self.parts(p)[0][1],'Vittorio Corbo Lioi')
    def test_3422_incomplete_larrain_not_completed_or_given_to_president(self):
        parts=self.parts(3422)
        self.assertEqual([(a,len(t)) for t,a,m in parts],[('Felipe Larraín Bascuñán',80),('José De Gregorio Rebeco',201)])
        self.assertTrue(parts[0][0].endswith('por el señor'))
    def test_263_chair_handoff_is_not_institutional_attendance(self):
        parts=self.parts(263)
        self.assertEqual([a for t,a,m in parts],['Vittorio Corbo Lioi',b.CONSEJO,'Vittorio Corbo Lioi'])
        self.assertIn('no se encuentra presente',parts[1][0])
        self.assertIn('Rodrigo Valdés',parts[2][0])
    def test_4469_response_begins_at_opinion_not_later_graph(self):
        parts=self.parts(4469)
        self.assertEqual([(a,len(t)) for t,a,m in parts],[('Manuel Marfán Lewis',293),('Sergio Lehmann Beresi',2353)])
        self.assertTrue(parts[1][0].startswith('En opinión del señor Sergio Lehmann'))
        self.assertEqual(parts[1][2],'CONTEXTO_REVISADO')
    def test_long_presentations_and_returns_are_whole(self):
        for p,n,actor in [(6767,8530,'Miguel Fuentes Díaz'),(6802,6081,'Sebastián Claro Edwards'),
                          (4360,2740,'Claudio Soto Gamboa'),(6065,2790,'Sergio Lehmann Beresi')]:
            self.assertIn((actor,n),[(a,len(t)) for t,a,m in self.parts(p)])
    def test_no_global_anchor_for_reviewed_opinion(self):
        self.assertNotIn('CONTEXTO_REVISADO',b.EXPLICIT)
    def warning_rows(self):
        e=self.warnings[4433]
        return [dict(ID=1,ID_Padre=4433,Fecha=e['Fecha'],Texto=e['Texto_Intervalo'],Actor_Final=e['Actor_Provisional'],Motivos_Revision=MOTIVE)]
    def test_context_warning_preserves_provisional_actor_and_interval(self):
        rows=self.warning_rows();before=copy.deepcopy(rows)
        self.assertEqual(contextual_motives(rows[0],self.warnings),[MOTIVE])
        self.assertEqual(validate_context_warnings(rows,self.warnings),[])
        self.assertEqual(rows,before)
        part=self.parts(4433)[1]
        self.assertEqual((part[1],len(part[0])),('Sergio Lehmann Beresi',705))
    def test_context_warning_requires_current_source(self):
        raw=copy.deepcopy(self.raw);raw[4433]['Texto']+=' añadido'
        with self.assertRaises(ValueError):load_context_warnings(raw)
    def test_context_warning_rejects_missing_added_or_moved_alert(self):
        for field,value in [('Motivos_Revision',''),('Texto','texto truncado'),('Actor_Final','Claudio Soto Gamboa'),('Fecha','2010-01-01')]:
            rows=self.warning_rows();rows[0][field]=value
            self.assertTrue(validate_context_warnings(rows,self.warnings))
        self.assertTrue(validate_context_warnings(self.warning_rows(),{}))
        self.assertTrue(validate_context_warnings([],self.warnings))
        self.assertTrue(validate_context_warnings(self.warning_rows()*2,self.warnings))
    def test_context_warning_registry_rejects_duplicates_bounds_and_scope(self):
        entries=json.loads(PATH.read_text())
        variants=[entries+entries]
        for key,value in [('Inicio',-1),('Fin',999999),('Decision','RESUELTO'),('Motivo','OTRA'),('Texto_Intervalo','recortado')]:
            bad=copy.deepcopy(entries);bad[0][key]=value;variants.append(bad)
        for bad in variants:
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'a.json';p.write_text(json.dumps(bad))
                with self.assertRaises(ValueError):load_context_warnings(self.raw,p)
    def test_uncertain_role_blocks_next_paragraph_even_same_actor(self):
        rows=self.warning_rows()
        rows[0].update(Fuente_Actor='SUJETO_ROL_SESION',ID_Intervencion='a',ID_Bloque_Texto='a')
        rows.append(dict(rows[0],ID=2,ID_Padre=4434,ID_Intervencion='b',ID_Bloque_Texto='b',Texto='El señor Sergio Lehmann señala otro antecedente.',Fuente_Actor='SUJETO_NOMBRE',Motivos_Revision=''))
        annotate_turns(rows)
        self.assertNotEqual(rows[0]['ID_Turno'],rows[1]['ID_Turno'])
        self.assertFalse(rows[1]['ID_Antecedente_Continuidad'])
    def test_qualified_returns_keep_the_whole_exposition(self):
        self.assertEqual([(a,len(t)) for t,a,m in self.parts(2519)],[('Andrés Velasco Brañes',255),('Sergio Lehmann Beresi',4384)])
        self.assertEqual([(a,len(t)) for t,a,m in self.parts(5279)],[('Manuel Marfán Lewis',274),('Sergio Lehmann Beresi',720)])
    def test_qualified_return_leads_reject_quotes_and_non_speech(self):
        for lead in ['Prosiguiendo con su exposición','Al proseguir con su presentación']:
            t=lead+', el señor Sergio Lehmann exhibe un gráfico.'
            self.assertEqual(b.TURN_DETECTOR.speaker(t,'2013-08-13')['actor'],'Sergio Lehmann Beresi')
            self.assertIsNone(b.TURN_DETECTOR.speaker('“'+t+'”','2013-08-13'))
            self.assertIsNone(b.TURN_DETECTOR.speaker(lead+', el señor Sergio Lehmann está presente.','2013-08-13'))
    def test_subordinate_verb_does_not_certify_parent14_subject(self):
        r=self.raw[14]
        self.assertIsNone(b.TURN_DETECTOR.speaker(r['Texto'],r['Fecha']))
        self.assertEqual(b.detect(r['Texto'],r['Fecha'])[0],'Esteban Jadresic Marinovic')
    def test_joint_priority_cases_remain_unadjudicated(self):
        self.assertFalse({3191,5367,5647,6185}&set(self.reviews))

FIXTURES = {14: {'hash': '6792502ab9eed5ccfe5c098a7c1da6ede20c10af3703e1d2f664ab48e3519085',
      'parts': [('Esteban Jadresic Marinovic', 822, 'CONTEXTO_REVISADO')]},
 263: {'hash': '96eda138e68b826252bf8e478180268914379363aefa31b07b338fc3ebfc6f79',
       'parts': [('Vittorio Corbo Lioi', 127, 'SUJETO_ROL_NOMBRE'),
                 ('Consejo del Banco Central de Chile', 219, 'ACTA/META'),
                 ('Vittorio Corbo Lioi', 157, 'SUJETO_ROL_NOMBRE')]},
 266: {'hash': '90b2cec121ec43deedd3e666e510e6f5c14c0bb7bc7a41f7e1135ea7c3361214',
       'parts': [('Vittorio Corbo Lioi', 68, 'SUJETO_ROL_NOMBRE')]},
 877: {'hash': '704b3dcff03591e6654214c69ee2bd8b2d99fe85d173dd3dd58feeb8f044ddd3',
       'parts': [('Vittorio Corbo Lioi', 3777, 'SUJETO_ROL_NOMBRE')]},
 1493: {'hash': '34d330224548a03b15b28106d09c039fa5c46333349d2685be19d0018d47a0a1',
        'parts': [('Vittorio Corbo Lioi', 950, 'SUJETO_ROL_NOMBRE')]},
 1495: {'hash': '3e4705732d2eb8fcae3860038053ea5b7d5bc9715c505b7bcd38a4522ca8a623',
        'parts': [('Vittorio Corbo Lioi', 92, 'SUJETO_ROL_NOMBRE')]},
 1579: {'hash': 'f27ce85b5d92945091ef4bd019fb0498447c412960e589674a90a1370db1b2fd',
        'parts': [('Pablo García Silva', 1037, 'SUJETO_ROL_NOMBRE')]},
 1869: {'hash': '3038ec9cc21822adcbd84f23f63c503ca08b6954fe9b77335072cba5b90ee69e',
        'parts': [('José De Gregorio Rebeco', 194, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 2582, 'SUJETO_ROL_NOMBRE'),
                  ('José De Gregorio Rebeco', 1020, 'SUJETO_ROL_NOMBRE'),
                  ('Claudio Soto Gamboa', 707, 'SUJETO_ROL_NOMBRE'),
                  ('José De Gregorio Rebeco', 175, 'SUJETO_ROL_SESION'),
                  ('Claudio Soto Gamboa', 211, 'SUJETO_ROL_NOMBRE'),
                  ('José De Gregorio Rebeco', 381, 'SUJETO_ROL_SESION'),
                  ('Sergio Lehmann Beresi', 338, 'SUJETO_ROL_NOMBRE')]},
 1905: {'hash': '6994287186d6bcbbcd598a3b95b9ec3ab2a80c78f9b1768fe068cd96aee8033e',
        'parts': [('Kevin Cowan Logan', 1295, 'SUJETO_ROL_NOMBRE')]},
 2148: {'hash': '851d8921c01fccb5edaff5ebbe55dae7c0ffe6383418ac3e48a9dac78a15005b',
        'parts': [('Pablo García Silva', 696, 'SUJETO_ROL_NOMBRE')]},
 2420: {'hash': '9049ab76af1ba93c0cbac435ae163e731ff4a46e65ea2ff4be2f2ffa4617a5b5',
        'parts': [('Pablo García Silva', 344, 'SUJETO_ROL_NOMBRE')]},
 2512: {'hash': '4eb46b23f580cefbb2ec6119b52cef6463a98b7d81e83c3d206e15541f5fae6d',
        'parts': [('José De Gregorio Rebeco', 227, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 2284, 'SUJETO_ROL_SESION')]},
 2519: {'hash': '1da8e499c47d73217b8e2bb4d3e42b09e98fd1969af3344655c6c331ed712164',
        'parts': [('Andrés Velasco Brañes', 255, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 4384, 'SUJETO_ROL_SESION')]},
 2553: {'hash': 'f46f37396402a970fa58085c0e40dea2595d9839c65390670af052caab2b3371',
        'parts': [('José De Gregorio Rebeco', 289, 'SUJETO_ROL_NOMBRE')]},
 2554: {'hash': '7ee1b93d9bd0fad6b050061245b2daf27b7d18190c6ab8b4ccd18a5a2d708aea',
        'parts': [('José De Gregorio Rebeco', 163, 'SUJETO_ROL_SESION'),
                  ('Sergio Lehmann Beresi', 1157, 'SUJETO_NOMBRE')]},
 2556: {'hash': '87c4d448807f225de266a32394d91e922aca7e212a58ace4488d50f57280acee',
        'parts': [('Sergio Lehmann Beresi', 1434, 'SUJETO_NOMBRE'),
                  ('Sebastián Claro Edwards', 102, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 910, 'SUJETO_NOMBRE')]},
 2558: {'hash': '1215f09b695eb97388f2e4136be9f6818d195bdd6613e66df4ba9f59e8c268e1',
        'parts': [('José De Gregorio Rebeco', 436, 'SUJETO_ROL_NOMBRE')]},
 2572: {'hash': '2b8a2910167346c99b07811f20e30f141e309d0f3d6a82dc619ec9cedf094e61',
        'parts': [('Pablo García Silva', 648, 'SUJETO_ROL_NOMBRE')]},
 2605: {'hash': '83394ab2b5f1c0cef254b5fb66c914dd7aa514c087c635a91db6b1e8d3eb015c',
        'parts': [('José De Gregorio Rebeco', 434, 'SUJETO_ROL_NOMBRE')]},
 2615: {'hash': 'f74b46b3f7861d0a3219bd0d29f067787560bbac87a8836324f319f9580a419b',
        'parts': [('Claudio Soto Gamboa', 651, 'SUJETO_ROL_NOMBRE'),
                  ('Andrés Velasco Brañes', 132, 'SUJETO_ROL_SESION'),
                  ('Claudio Soto Gamboa', 1116, 'SUJETO_ROL_SESION')]},
 2657: {'hash': '54b0ce326ec93d8f67e0a83c3073633abd453a0e0db1819a1aebcfabf2cc1220',
        'parts': [('José De Gregorio Rebeco', 298, 'SUJETO_ROL_NOMBRE')]},
 2658: {'hash': 'cddc49a5deac614ded108f169e1f298b2989a52994dc063205eb82989a1643eb',
        'parts': [('José De Gregorio Rebeco', 158, 'SUJETO_ROL_SESION')]},
 2690: {'hash': 'f8dea11acc3a25c5dfb0a45d22716b91184942c4b6e2f74692d52b57b282890a',
        'parts': [('José De Gregorio Rebeco', 296, 'SUJETO_ROL_NOMBRE')]},
 2691: {'hash': '42cc4197c9de53dd8c1382f55d10fa756e90afe2a56332c0910b064c63dc61eb',
        'parts': [('José De Gregorio Rebeco', 158, 'SUJETO_ROL_SESION'),
                  ('Sergio Lehmann Beresi', 9730, 'SUJETO_ROL_SESION')]},
 2714: {'hash': 'f405bfba5a4c269752aedbfa976022fe5a9b7a7b880629dd4b808546eacb6b8b',
        'parts': [('José De Gregorio Rebeco', 296, 'SUJETO_ROL_NOMBRE')]},
 2715: {'hash': 'cddc49a5deac614ded108f169e1f298b2989a52994dc063205eb82989a1643eb',
        'parts': [('José De Gregorio Rebeco', 158, 'SUJETO_ROL_SESION')]},
 2725: {'hash': '0df50e33911db1ae05d6e9d207251daccffb93d9adbcaf998ea97991c0e96655',
        'parts': [('Sergio Lehmann Beresi', 984, 'SUJETO_NOMBRE'),
                  ('Sebastián Claro Edwards', 466, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 870, 'SUJETO_NOMBRE'),
                  ('Pablo García Silva', 567, 'SUJETO_ROL_SESION'),
                  ('Sergio Lehmann Beresi', 773, 'SUJETO_NOMBRE')]},
 2842: {'hash': '0cbaa5ca2f37b47d547411b65be1bb6e9a7eb1d8702bcb59e7be4d1264db679b',
        'parts': [('José De Gregorio Rebeco', 297, 'SUJETO_ROL_NOMBRE')]},
 2843: {'hash': '1c2516679fe71a5b311e2c23b91041c5860415a451b62a6d51d18ff68ac3659c',
        'parts': [('José De Gregorio Rebeco', 158, 'SUJETO_ROL_SESION'),
                  ('Sergio Lehmann Beresi', 2109, 'SUJETO_NOMBRE')]},
 2864: {'hash': '48b5aa906a90da454033632a1beb27594f73879f047c779d91e253a317793c25',
        'parts': [('Claudio Soto Gamboa', 495, 'SUJETO_NOMBRE')]},
 2890: {'hash': 'a4ede6f9587a75b08e38444981f61c85fe1bac9cef78ed772250bdc569d26fc7',
        'parts': [('José De Gregorio Rebeco', 280, 'SUJETO_ROL_NOMBRE')]},
 2891: {'hash': '809fe7bbe43a0f32e6341fe036d46984d0081f04239de54f6542f45f71eea799',
        'parts': [('José De Gregorio Rebeco', 270, 'SUJETO_ROL_SESION'),
                  ('Sergio Lehmann Beresi', 4135, 'SUJETO_NOMBRE'),
                  ('Pablo García Silva', 277, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 2361, 'SUJETO_ROL_SESION'),
                  ('José De Gregorio Rebeco', 242, 'SUJETO_ROL_NOMBRE')]},
 2972: {'hash': 'eb7cf305389ac91ee745dbc2c964578b15bce406515d7631eb6a5a3597235961',
        'parts': [('José De Gregorio Rebeco', 214, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 1155, 'SUJETO_ROL_SESION'),
                  ('José De Gregorio Rebeco', 100, 'SUJETO_ROL_SESION')]},
 3024: {'hash': 'a620a46e868619fb1a12ab23a063c3a802ba78b8940f2dffd2470fbe27771e98',
        'parts': [('José De Gregorio Rebeco', 445, 'SUJETO_ROL_NOMBRE')]},
 3025: {'hash': '831ad02798e01df9676ee2b3bf6c7e607be530d8b22a7bf197c2eb4c25e27140',
        'parts': [('José De Gregorio Rebeco', 157, 'SUJETO_ROL_SESION'),
                  ('Sergio Lehmann Beresi', 4763, 'SUJETO_NOMBRE')]},
 3080: {'hash': '1a47cc4151bb9875ec6db7569e1405832d715f4e86567c6a9668c1c851e362b2',
        'parts': [('José De Gregorio Rebeco', 494, 'SUJETO_ROL_NOMBRE')]},
 3129: {'hash': 'e898f2ff7958277a5af8793029bf47cf4ab374b8af4d2ef2b031d10015708717',
        'parts': [('José De Gregorio Rebeco', 500, 'SUJETO_ROL_NOMBRE')]},
 3208: {'hash': 'ddb8eabe866c3f88f8f9de0c8d4399dbd2c73d0ef174a22aed13b482b663574f',
        'parts': [('José De Gregorio Rebeco', 686, 'SUJETO_ROL_NOMBRE')]},
 3279: {'hash': 'fb44c19a563c001187cac8a176d2b60a4ca1f86b8c36162f3d28c939c4960c06',
        'parts': [('José De Gregorio Rebeco', 623, 'SUJETO_ROL_NOMBRE')]},
 3321: {'hash': 'fba359677b4edf04f147ad34096ff76523c2e36f70d204f97e276048fb2ab810',
        'parts': [('Enrique Marshall Rivera', 415, 'SUJETO_ROL_NOMBRE')]},
 3422: {'hash': 'ef3c3928494fe65244e10d3d17d9fdc7e9fea18879d5b6858a93bf15a9dec583',
        'parts': [('Felipe Larraín Bascuñán', 80, 'SUJETO_ROL_NOMBRE'),
                  ('José De Gregorio Rebeco', 201, 'SUJETO_ROL_NOMBRE')]},
 3425: {'hash': '1ee72dcd559e64a245a4b95206c9b9f3a5203349ea8e6370c9d59c7eb833e527',
        'parts': [('Felipe Larraín Bascuñán', 5667, 'SUJETO_ROL_NOMBRE')]},
 3473: {'hash': 'c03fa580e2e237483bd5cbb34e226f2f3dd0140c2f40a6dcb13d40886faa3244',
        'parts': [('Manuel Marfán Lewis', 767, 'SUJETO_ROL_NOMBRE')]},
 3495: {'hash': '624f76dd5ac7368325fe3481388730aadeafc3ce207bdb9c31b2e875b978b795',
        'parts': [('José De Gregorio Rebeco', 596, 'SUJETO_ROL_NOMBRE')]},
 3603: {'hash': '658196268ec185b672bbaebd8e60e7d60dd63f781ce63dbdc6ff760483ccfac6',
        'parts': [('Claudio Soto Gamboa', 3162, 'SUJETO_ROL_NOMBRE')]},
 3634: {'hash': '3a927e79ea5647847f82f8d5c17a5227b001953ac06df0a1ca175f11af9cc269',
        'parts': [('Felipe Larraín Bascuñán', 5208, 'SUJETO_ROL_NOMBRE')]},
 3753: {'hash': 'eb6cbe0313be464d4dc7fffea4cca57741682da26ef054bdedffbe39c10ea2f2',
        'parts': [('José De Gregorio Rebeco', 276, 'SUJETO_ROL_NOMBRE')]},
 3986: {'hash': 'e94660367719dd8881da15378b24c0ba4453eeff780f3bfea7fd2922270de19a',
        'parts': [('José De Gregorio Rebeco', 335, 'SUJETO_ROL_NOMBRE')]},
 3992: {'hash': 'f98b060fede0b27886a60d14636820867f316a74eac08b528bb7ec00820473a2',
        'parts': [('Luis Óscar Herrera Barriga', 261, 'SUJETO_NOMBRE')]},
 4000: {'hash': '548a9b0aad9b738dea69f9eda257e7ffeb0b7a7263f3753ce1e850a4b0851b66',
        'parts': [('Sergio Lehmann Beresi', 828, 'SUJETO_NOMBRE')]},
 4231: {'hash': 'f645b2f01446ce089ec6a3af855672366f711a0f0b4691ca0b75db281ad27a77',
        'parts': [('Sergio Lehmann Beresi', 385, 'SUJETO_NOMBRE')]},
 4360: {'hash': 'f3f1e1fd9e022e4982028484e0dd685e729cb874ae406d76a54aadda8bc65a44',
        'parts': [('Rodrigo Vergara Montes', 272, 'SUJETO_ROL_NOMBRE'),
                  ('Claudio Soto Gamboa', 2740, 'SUJETO_NOMBRE')]},
 4433: {'hash': '68ceefd19fe4d0a89c1d8a1fc92c1bb6ea10583e71ecb2e6e23565572e038e65',
        'parts': [('Claudio Soto Gamboa', 4022, 'SUJETO_NOMBRE'),
                  ('Sergio Lehmann Beresi', 705, 'SUJETO_ROL_SESION'),
                  ('Claudio Soto Gamboa', 1482, 'SUJETO_NOMBRE')]},
 4469: {'hash': '477cdd6de26fa8fd1d32d6395425a1cd75131055f480907a1fde5af1086cd9f9',
        'parts': [('Manuel Marfán Lewis', 293, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 2353, 'CONTEXTO_REVISADO')]},
 4532: {'hash': '2e48b657755a825dea92e1397bb9eecbd60370955a056410152307218a9329cc',
        'parts': [('Enrique Marshall Rivera', 223, 'SUJETO_ROL_NOMBRE')]},
 4592: {'hash': 'ca324ac4c09320e588677604c6cb7c22143706e527753ef360260e0e3bcf7379',
        'parts': [('Luis Óscar Herrera Barriga', 868, 'SUJETO_ROL_NOMBRE')]},
 4674: {'hash': '586381cac236d394e48760867172d1c7e810743b6700224418809bf00c7d1127',
        'parts': [('Sergio Lehmann Beresi', 1978, 'SUJETO_NOMBRE')]},
 4683: {'hash': '2cd15b280baf081e4a68c2f0878e79aaafee7e7f810032d58efed27f0b62e841',
        'parts': [('Sergio Lehmann Beresi', 1058, 'SUJETO_NOMBRE'),
                  ('Rodrigo Cerda Norambuena', 435, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 602, 'SUJETO_NOMBRE')]},
 4746: {'hash': '9e89343fcc0ac4b2ff9175b9c0d44a41968471a6daedf20137f3461b2d2089e4',
        'parts': [('Sergio Lehmann Beresi', 1877, 'SUJETO_NOMBRE')]},
 4860: {'hash': '9f352654dd5d1808c917972e690b0d2d1b780a037e1418a8d8fc3a4f5c3f194d',
        'parts': [('Manuel Marfán Lewis', 210, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 495, 'SUJETO_NOMBRE')]},
 4861: {'hash': '33a146c58a618f73d5855791b1ff96950715e84cc9f1a2d32d97a19d1b1f7945',
        'parts': [('Sergio Lehmann Beresi', 1294, 'SUJETO_ROL_SESION')]},
 4882: {'hash': '0301368de69a4499c8c21021b58ff4d8b568ea77892c0fa3ec0fb669ecd18a43',
        'parts': [('Rodrigo Vergara Montes', 684, 'SUJETO_ROL_NOMBRE')]},
 4985: {'hash': '3af9df5604d6bd0a531f5589e02ea93c35a99383049ecde207ae4b45b9bbef8b',
        'parts': [('Rodrigo Vergara Montes', 786, 'SUJETO_ROL_NOMBRE')]},
 5011: {'hash': '6b3e963c4f65c287fea20bffd2597abc48a6f1cfcc117dcecc7bbb0f9bd0df5f',
        'parts': [('Claudio Soto Gamboa', 1577, 'SUJETO_ROL_NOMBRE')]},
 5059: {'hash': 'd9d6af9e6a37fca75f3ba268743d24af916ccd7d7d4bafe4e2226f9a96780235',
        'parts': [('Kevin Cowan Logan', 2206, 'SUJETO_ROL_NOMBRE')]},
 5063: {'hash': 'a5f371275dcc2b96afacd393c7d7ae9f9f9f9769f83b1d39e7d304c9f1f63c3d',
        'parts': [('Sergio Lehmann Beresi', 1828, 'SUJETO_ROL_NOMBRE')]},
 5074: {'hash': '0b470333bf5d990f14ba190d0ade1b4d1c468cc7ca6b9eb34ab285bc91c95c92',
        'parts': [('Sebastián Claro Edwards', 623, 'SUJETO_ROL_NOMBRE')]},
 5103: {'hash': '94722e76268a0561bcd8ff20ae6ed23d4f907d94c020fce383194a1114e3f275',
        'parts': [('Sergio Lehmann Beresi', 594, 'SUJETO_NOMBRE')]},
 5104: {'hash': '4cb7910fad41f76bbe37a35811f385bfc698c4271a1b88ae6d39881aef1c3334',
        'parts': [('Sergio Lehmann Beresi', 355, 'SUJETO_NOMBRE')]},
 5117: {'hash': 'cb25fa80f351ceaec94f1af6ab8a13de27b97b09eb525c7cfac6b9e75fa15790',
        'parts': [('Manuel Marfán Lewis', 1631, 'SUJETO_ROL_NOMBRE')]},
 5167: {'hash': '7216eb1b42e53309bc503c818398d3cfb6d1c42043461b14f89f3a3f216e781b',
        'parts': [('Sergio Lehmann Beresi', 623, 'SUJETO_NOMBRE')]},
 5177: {'hash': 'd730591a8dcb8faf96083d3d646177b9b6f12716c61e295fa6132fa410989a76',
        'parts': [('Rodrigo Vergara Montes', 857, 'SUJETO_ROL_NOMBRE')]},
 5178: {'hash': 'ca16c4687f45db890aa0750c80f21f07cf95f163266d9e0d1a8f76ed8e15a216',
        'parts': [('Luis Óscar Herrera Barriga', 1825, 'SUJETO_ROL_NOMBRE'),
                  ('Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE')]},
 5206: {'hash': '610893544b1a36385d6336f3f134e978c661cff446b795ec7bbc319b0ed4c0b2',
        'parts': [('Rodrigo Vergara Montes', 835, 'SUJETO_ROL_NOMBRE')]},
 5242: {'hash': '08ba9672c748dcc7bdb80c66ca2fe661b959f1a527d4c26c33bf06806eea6f7d',
        'parts': [('Rodrigo Vergara Montes', 370, 'SUJETO_ROL_NOMBRE')]},
 5279: {'hash': '1f5f02fc452a89ddcbc7400ace1f4cf6f4a8094c006f358b807acb51b432df6e',
        'parts': [('Manuel Marfán Lewis', 274, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 720, 'SUJETO_NOMBRE')]},
 5280: {'hash': '6d76da7c9013296b49fdc3acbbb4b16c40b5962ce48ff291872bd6b379e45ec4',
        'parts': [('Sergio Lehmann Beresi', 4913, 'SUJETO_NOMBRE')]},
 5283: {'hash': '1aac79dc98431832e40ae941d630c550038a6550d20677f9bc7ed862c04f348d',
        'parts': [('Manuel Marfán Lewis', 1209, 'SUJETO_ROL_NOMBRE')]},
 5311: {'hash': '3904c6659c53c6fc0ae609aa541b8f61739d641476ee580ebaae5e36f840f317',
        'parts': [('Manuel Marfán Lewis', 235, 'SUJETO_ROL_NOMBRE')]},
 5761: {'hash': 'e771e00f3865f7d4e32d41e18b790d5f4f5ce155983e7d5ff100dbef8ac67d6e',
        'parts': [('Manuel Marfán Lewis', 417, 'SUJETO_ROL_NOMBRE')]},
 5840: {'hash': 'b023a39ad38c861b6f9ca4fc12c7721cfcfd5e633d6b770d1b0b43a14a1627e1',
        'parts': [('Claudio Soto Gamboa', 2214, 'SUJETO_NOMBRE')]},
 5884: {'hash': 'c46ddb7b7f3f9c013d0f301c430da95c831b09fd41dae3fab8f4b1c83829ed58',
        'parts': [('Claudio Soto Gamboa', 2181, 'SUJETO_ROL_NOMBRE'),
                  ('Rodrigo Vergara Montes', 246, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 70, 'ACTA/META')]},
 5986: {'hash': 'dbc43ff7937bb160b941fad8d047e26ab53a395862580ceab30b2e3e9ae41ffa',
        'parts': [('Joaquín Vial Ruiz-Tagle', 840, 'SUJETO_ROL_NOMBRE')]},
 6024: {'hash': '90cdd9da007ede9f201df96fce0a1788606bbc08f60ef979de7f4456fa3a7f27',
        'parts': [('Rodrigo Vergara Montes', 689, 'SUJETO_ROL_NOMBRE')]},
 6038: {'hash': '70e8ee4c2ffb4c66a7fe2008897fa783aaccd02b8c513df55f3ff9a38c94bf13',
        'parts': [('Kevin Cowan Logan', 879, 'SUJETO_ROL_NOMBRE')]},
 6065: {'hash': '1f194faae41ae324be5b27d487656c4020bfba63bde975e86a591ce24b24e637',
        'parts': [('Luis Óscar Herrera Barriga', 521, 'SUJETO_ROL_NOMBRE'),
                  ('Pablo García Silva', 462, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 2790, 'SUJETO_NOMBRE')]},
 6093: {'hash': 'f49672b25fef6fda749e7ad5a4e1e166e310376dcac2fa88989b5afa2b6be22b',
        'parts': [('Luis Óscar Herrera Barriga', 1680, 'SUJETO_ROL_NOMBRE'),
                  ('Rodrigo Vergara Montes', 246, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 145, 'ACTA/META')]},
 6192: {'hash': 'a7de89248379321ffff9fc70d4c83b6c7b2bfd7c603763645a93958abf2bf284',
        'parts': [('Sergio Lehmann Beresi', 1421, 'SUJETO_NOMBRE'),
                  ('Rodrigo Vergara Montes', 239, 'SUJETO_ROL_NOMBRE')]},
 6326: {'hash': 'fcba5ee6c66f458fe8a39a0c1a45c114c3d1666883eae5475cc5487ea0ebae3c',
        'parts': [('Miguel Fuentes Díaz', 2370, 'SUJETO_ROL_NOMBRE'),
                  ('Rodrigo Vergara Montes', 246, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 151, 'ACTA/META')]},
 6403: {'hash': '5832a4aa8a511ebc163bbf7b152a1521624843fe7f4a154cac01cd6ce56150ee',
        'parts': [('Sergio Lehmann Beresi', 1315, 'SUJETO_NOMBRE')]},
 6452: {'hash': 'cdc30ed22a4bd5b93daa22c262fd65c699365f2bce5926a4349db0632e129d45',
        'parts': [('Miguel Fuentes Díaz', 1706, 'SUJETO_NOMBRE')]},
 6671: {'hash': '40f9450fa31aa79fd4a363284c84ce51c2457cceb56c27c6dd05a6715b267cca',
        'parts': [('Rodrigo Vergara Montes', 207, 'SUJETO_ROL_NOMBRE')]},
 6714: {'hash': '6beed3cb7bde056952591ac6f5113bf2b328da2151bb5e001a7b279165b035b9',
        'parts': [('Diego Gianelli Gómez', 1977, 'SUJETO_NOMBRE')]},
 6724: {'hash': '0490e982536ea341b7d6c07495fd8810bdf7f1d4d350ba6441905c10cfe33269',
        'parts': [('Beltrán de Ramón Acevedo', 261, 'SUJETO_ROL_NOMBRE')]},
 6767: {'hash': '17bc45501fce3628a86bf4c45dda8fac9ed0a3fc07000cc7fdf11753a042bfee',
        'parts': [('Miguel Fuentes Díaz', 8530, 'SUJETO_ROL_NOMBRE')]},
 6797: {'hash': '6cb20c96b06839d7a4ad471d6d4e2b224cbc81897f113cf801bf8d9d80195a52',
        'parts': [('Rodrigo Valdés Pulido', 3390, 'SUJETO_ROL_NOMBRE')]},
 6802: {'hash': 'c304c1e84fec802098c4236d8776d1d6f66fee30ac2e5ea426da4530b89dec00',
        'parts': [('Sebastián Claro Edwards', 6081, 'SUJETO_ROL_NOMBRE')]},
 6830: {'hash': '66f4dd0e7ec257338885b025fec608b9a8fbcfa42615a5c56318aac7642e4820',
        'parts': [('Miguel Fuentes Díaz', 3988, 'SUJETO_ROL_NOMBRE')]},
 6884: {'hash': 'e75d0d68e2b7bdd266de9d4b24c0b37a19d1c66bb2257d60f49094f0ca72cdb6',
        'parts': [("Alberto Naudon Dell'Oro", 2533, 'SUJETO_ROL_NOMBRE'),
                  ('Rodrigo Vergara Montes', 170, 'SUJETO_ROL_NOMBRE')]},
 6885: {'hash': '1b337776ae14c077b2f8e361ed4a7d58aa53e2d3c07b2ab0a01a791577ecbed2',
        'parts': [('Miguel Fuentes Díaz', 3554, 'SUJETO_ROL_NOMBRE')]},
 6904: {'hash': 'e39547d170bf30de1099ac1522f7953749413b138b948aa0546dd007ab0a6d3f',
        'parts': [("Alberto Naudon Dell'Oro", 1746, 'SUJETO_NOMBRE'),
                  ('Rodrigo Vergara Montes', 225, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 145, 'ACTA/META')]},
 6927: {'hash': 'e12a1b3fd59332657abeeef97fb40a93d889a5bd4bc50162bce4d37263910e0e',
        'parts': [('Miguel Fuentes Díaz', 1588, 'SUJETO_ROL_NOMBRE')]},
 7004: {'hash': '9ec56b22cdeb69f2288ff024f63dcb8e518e5e958b8ccc8083fd21f708234073',
        'parts': [('Miguel Fuentes Díaz', 1142, 'SUJETO_ROL_NOMBRE')]},
 7006: {'hash': 'afe46a5a971e719b2fa0a537b195326d4f0d5b5522731734ee7b9dd06d3e808a',
        'parts': [("Alberto Naudon Dell'Oro", 151, 'SUJETO_ROL_NOMBRE')]},
 7030: {'hash': '9f8abfe111e4f0aa75b80167714e9de85f6626d44fa6c99429b82fd85993a066',
        'parts': [('Pablo García Silva', 2052, 'SUJETO_ROL_NOMBRE')]},
 7072: {'hash': 'd2d54b77da059065ec41729572a792d4795bd0e2d862cbe8b72fd3a1c20b4d68',
        'parts': [('Miguel Fuentes Díaz', 1841, 'SUJETO_ROL_NOMBRE')]},
 7126: {'hash': 'dd0b77816461a178c190bcca87e199a4ac175f2212e68cfe1ae9b8851487250a',
        'parts': [('Miguel Fuentes Díaz', 4061, 'SUJETO_ROL_NOMBRE')]},
 7175: {'hash': 'c4b74aba5a9408cca9542dd180fd3dc7ff840399ab9ef5832078e40fb81dc67c',
        'parts': [("Alberto Naudon Dell'Oro", 776, 'SUJETO_NOMBRE'),
                  ('Mario Marcel Cullell', 350, 'SUJETO_ROL_NOMBRE')]},
 7180: {'hash': '62c123a542f8e3bf7e6344ac0bb8abd924e17d2ad7045a40ad6c8958249cf2bf',
        'parts': [('Miguel Fuentes Díaz', 3052, 'SUJETO_ROL_NOMBRE')]},
 7199: {'hash': 'e27f143311b098bf603896d8fc2c2036b373b39a722f6a3a5a4907e3b423d81d',
        'parts': [('Rodrigo Vergara Montes', 296, 'SUJETO_ROL_NOMBRE')]}}

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
for p,e in FIXTURES.items():setattr(LoopEightTests,f'test_parent_{p}',fixture_test(p,e))

if __name__=='__main__':unittest.main()
