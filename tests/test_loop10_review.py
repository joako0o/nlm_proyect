"""Loop10: 60 padres cambiados y una regresión adversarial de discurso referido.
Fixtures estáticas no equivalen a certificación humana integral del padre.
"""
import copy
import hashlib
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, validate_speaker_reviews
from continuity import annotate_turns

class LoopTenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)
    def parts(self,p):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p))
    def test_five_predicates_require_subject_not_mention(self):
        for verb in ['está en desacuerdo','visualiza','asigna una alta probabilidad','llama a ser cuidadosos','deja planteada la pregunta']:
            t=f'El señor Sergio Lehmann {verb} respecto del escenario.'
            self.assertEqual(b.TURN_DETECTOR.speaker(t,'2013-08-13')['actor'],'Sergio Lehmann Beresi')
            for bad in ['“'+t+'”','Según '+t.lower(),'La opinión del señor Sergio Lehmann '+verb+' respecto del escenario.']:
                self.assertIsNone(b.TURN_DETECTOR.speaker(bad,'2013-08-13'),bad)
    def test_new_asides_require_a_main_predicate(self):
        for aside in ['acerca de la cifra','a raíz de la caída','en razón de la sorpresa','insistiendo sobre el tema',
                      'ante comentarios de la prensa','haciendo referencia al dato','continuando con su exposición',
                      'continuando su comentario','también con respecto a demanda','atendido lo expuesto',
                      'haciendo un cálculo preliminar','junto con agradecer las opiniones expuestas',
                      'en nombre suyo y del Consejo','antes de retirarse de la Reunión','pensado en los agricultores']:
            pre=f'El señor Sergio Lehmann, {aside}, '
            self.assertEqual(b.TURN_DETECTOR.speaker(pre+'señala la cifra.','2013-08-13')['actor'],'Sergio Lehmann Beresi',aside)
            self.assertIsNone(b.TURN_DETECTOR.speaker(pre+'está presente.','2013-08-13'))
            self.assertIsNone(b.TURN_DETECTOR.speaker('“'+pre+'señala la cifra.”','2013-08-13'))
    def test_asides_do_not_borrow_a_relative_verb(self):
        for t in ['El señor Sergio Lehmann, acerca de lo que señala el Presidente, está presente.',
                  'El señor Sergio Lehmann, haciendo referencia a lo que indica el Presidente, está presente.',
                  'El señor Sergio Lehmann, en razón de lo que comenta el Presidente, está presente.']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2013-08-13'),t)
    def test_reported_past_blocks_borrowed_predicate(self):
        t='En cuanto al tema a que se refirió la señora Ministra de Hacienda Subrogante, estima que está vinculado al tipo de cambio.'
        self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2009-01-08'))
    def test_se_refirio_does_not_open_a_new_current_turn(self):
        for t in ['En cambio, el Gerente de División Operaciones Financieras señor Jadresic, se refirió a la inflación.',
                  'El señor José De Gregorio se refirió a las expectativas.']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2007-01-11'))
    def test_2325_minister_is_topic_not_speaker(self):
        parts=self.parts(2325)
        self.assertEqual([a for t,a,m in parts],['Pablo García Silva'])
        self.assertIn('a que se refirió la señora Ministra',parts[0][0])
    def test_2325_mention_annotation_preserves_warning_and_actor(self):
        from mention_reviews import load_mention_reviews, validate_mention_reviews
        reviews={k:v for k,v in load_mention_reviews(self.raw).items() if v['ID_Padre']==2325}
        r=self.parts(2325)[0]
        rows=[dict(ID=1,ID_Padre=2325,Fecha=self.raw[2325]['Fecha'],Texto=r[0],Actor_Final=r[1],Motivos_Revision='POSIBLE_OTRO_HABLANTE_O_MENCION')]
        original=copy.deepcopy(rows)
        errors,annotations=validate_mention_reviews(rows,reviews)
        self.assertFalse(errors)
        self.assertEqual(rows,original)
        self.assertEqual(annotations[1]['Revision_Lectura_Dirigida'],'MEN-20260908-2325')

    def test_2052_one_contiguous_lehmann_exposition(self):
        parts=self.parts(2052)
        self.assertEqual([(a,len(t)) for t,a,m in parts],[('Sergio Lehmann Beresi',2801)])
        self.assertIn('En cuanto al mercado financiero',parts[0][0])
    def test_3011_cespedes_starts_at_named_handoff_not_later_opinion(self):
        parts=self.parts(3011)
        self.assertEqual([(a,len(t)) for t,a,m in parts],[('Pablo García Silva',8431),('José De Gregorio Rebeco',172),('Luis Felipe Céspedes Cifuentes',3157)])
        self.assertTrue(parts[-1][0].startswith('El Gerente aludido menciona'))
        self.assertTrue(parts[-1][0].endswith('A continuación,.'))
    def test_all_new_review_intervals_survive_and_reject_overassignment(self):
        self.assertEqual(len(NEW_REVIEWS),37)
        for p in NEW_REVIEWS:
            rows=[dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p))]
            self.assertFalse(validate_speaker_reviews(rows,{p:self.reviews[p]}),p)
            next(r for r in rows if r['Fuente_Actor']=='CONTEXTO_REVISADO')['Texto']+=' ajeno'
            self.assertTrue(validate_speaker_reviews(rows,{p:self.reviews[p]}),p)
    def test_no_global_opinion_rule(self):
        for lead in ['En opinión del Consejero señor Sebastián Claro','A juicio del Vicepresidente señor Manuel Marfán']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(lead+', la cifra resulta elevada.','2013-08-13'))
    def test_soto_advisor_is_subject_not_minister(self):
        t='El Asesor Macroeconómico del Ministro de Hacienda señor Claudio Soto plantea una duda.'
        self.assertEqual(b.TURN_DETECTOR.speaker(t,'2015-10-15')['actor'],'Claudio Soto Gamboa')
        for bad in ['“'+t+'”','Se cita que '+t,'El Asesor Macroeconómico del Ministro de Hacienda señor Claudio Soto está presente.']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(bad,'2015-10-15'),bad)
    def test_7079_two_distinct_interruptions_of_fuentes(self):
        self.assertEqual([a for t,a,m in self.parts(7079)],['Miguel Fuentes Díaz','Claudio Soto Gamboa','Miguel Fuentes Díaz','Sebastián Claro Edwards'])
    def test_four_bounded_returns_preserve_expositor(self):
        for p,actor in [(2674,'Claudio Soto Gamboa'),(4634,'Claudio Soto Gamboa'),(6257,'Miguel Fuentes Díaz'),(7021,'Miguel Fuentes Díaz')]:
            parts=self.parts(p);i=next(i for i,(t,a,m) in enumerate(parts) if m=='CONTEXTO_REVISADO')
            self.assertEqual(parts[i-1][1],actor)
            self.assertEqual(parts[i+1][1],actor)
            self.assertNotEqual(parts[i][1],actor)
    def test_6118_ocr_v_is_preserved_with_review_start(self):
        self.assertTrue(self.parts(6118)[1][0].startswith('V A juicio'))
    def test_5402_claro_question_breaks_old_lehmann_link(self):
        rows=[]
        for p in [5402,5403]:
            for i,(t,a,m) in enumerate(self.parts(p)):
                rows.append(dict(ID_Intervencion=f'{p}:{i}',ID_Bloque_Texto=f'{p}:{i}',Fecha=self.raw[p]['Fecha'],Actor_Final=a,Texto=t,Fuente_Actor=m,Tipo_Acta='INTERVENCION',Motivos_Revision=''))
        annotate_turns(rows)
        self.assertEqual([r['Actor_Final'] for r in rows],['Sergio Lehmann Beresi','Sebastián Claro Edwards','Sergio Lehmann Beresi'])
        self.assertEqual(len({r['ID_Turno'] for r in rows}),3)
    def test_no_new_context_review_creates_an_anchor(self):
        for p in NEW_REVIEWS:
            r=next((t,a,m) for t,a,m in self.parts(p) if m=='CONTEXTO_REVISADO')
            rows=[dict(ID_Intervencion='1',ID_Bloque_Texto='1',Fecha=self.raw[p]['Fecha'],Actor_Final=r[1],Texto=r[0],Fuente_Actor=r[2],Tipo_Acta='INTERVENCION',Motivos_Revision='')]
            annotate_turns(rows)
            self.assertFalse(rows[0]['ID_Ancla_Actor'])
    def test_unresolved_joint_passages_not_forced(self):
        self.assertFalse({6185,780}&set(self.reviews))
        for p in [3191,5367]:
            self.assertGreater(self.reviews[p]["Inicio"],0)  # el prefijo conjunto no se adjudica
    def test_5402_long_prefix_and_mixed_ocr_quotes_preserved(self):
        parts=self.parts(5402)
        self.assertEqual(len(parts[0][0]),5443)
        self.assertIn('“Aaa"',parts[0][0])
        self.assertIn('“AA-“',parts[0][0])
    def test_3056_marfan_return_is_not_cut_off_at_old_boundary(self):
        parts=self.parts(3056)
        self.assertEqual([(a,len(t)) for t,a,m in parts],[('Pablo García Silva',222),('Manuel Marfán Lewis',426),('Pablo García Silva',560)])
    def test_unchanged_1013_keeps_reported_jadresic_with_valdes(self):
        parts=self.parts(1013)
        self.assertEqual([a for t,a,m in parts],['Esteban Jadresic Marinovic','Pablo García Silva','Rodrigo Valdés Pulido'])
        self.assertIn('se refirió al lugar',parts[-1][0])

NEW_REVIEWS = [3011, 3056, 3435, 3442, 3523, 4148, 4252, 4256, 4342, 4477, 4589, 4709, 4903, 4922, 5347, 5470, 5793, 6118, 6163, 6257, 6305, 6456, 6791, 6839, 6869, 6900, 6902, 6953, 6985, 7021, 7079, 7142, 7174, 2674, 4634, 5402, 6069]

FIXTURES = {343: {'hash': '9f9b7ffb3b62c9d672fa0edf604932839443641b609f8c1eebb0ea4bc347edcd',
       'parts': [('Nicolás Eyzaguirre Guzmán', 334, 'SUJETO_ROL_SESION')]},
 345: {'hash': '21c76b023772de1210ab06694beae81ec3c9f5127a47b2f70f253cb5e72d9ba2',
       'parts': [('Nicolás Eyzaguirre Guzmán', 717, 'SUJETO_ROL_SESION')]},
 1013: {'hash': 'd6f7c23182d45ebac141a198989c60a3c0ed44c67bcd1c9ce89834edba44b264',
        'parts': [('Esteban Jadresic Marinovic', 997, 'SUJETO_ROL_NOMBRE'),
                  ('Pablo García Silva', 1691, 'SUJETO_ROL_NOMBRE'),
                  ('Rodrigo Valdés Pulido', 2471, 'SUJETO_ROL_SESION')]},
 1145: {'hash': '33a56f7bc0fe1b7dc8720d34f8753fb22e11607768f3a6ad691a2101aa466a3d',
        'parts': [('Andrés Velasco Brañes', 625, 'SUJETO_ROL_SESION')]},
 1326: {'hash': '76c715447b48fd6fa9ead7cb966f5534de7595bdd7d1574bd75a3ad772115cce',
        'parts': [('Manuel Marfán Lewis', 687, 'SUJETO_ROL_NOMBRE')]},
 2052: {'hash': '1e4a41afd22b86379ac23070950673300633fad1c31a13f177aa0c448a3e513c',
        'parts': [('Sergio Lehmann Beresi', 2801, 'SUJETO_NOMBRE')]},
 2196: {'hash': 'f1fe2ad3738eb3e10c4ddaef1b3d45b062151ad43777421be9a770637506be1c',
        'parts': [('Sergio Lehmann Beresi', 531, 'SUJETO_ROL_NOMBRE')]},
 2325: {'hash': 'd455969408a4d0055eb49dd5ea8733ef374941d57c75ce676ec765abaff3d396',
        'parts': [('Pablo García Silva', 1131, 'SUJETO_ROL_NOMBRE')]},
 2380: {'hash': 'c52f858903f878479c47d6451e19ff5ee3e252270ff447a40ec2f34539e2a336',
        'parts': [('Sebastián Claro Edwards', 162, 'SUJETO_ROL_NOMBRE'),
                  ('José De Gregorio Rebeco', 281, 'SUJETO_ROL_NOMBRE')]},
 2415: {'hash': '9bdd78e2ded2e9325e2771c0fb953e289a2e5f71e61234a63ba0a80cc6b3a548',
        'parts': [('Claudio Soto Gamboa', 796, 'SUJETO_ROL_NOMBRE')]},
 2481: {'hash': 'b38412d39c03ef706fb6e320629278dfc6dc393b3d3c8d8d36bacb902676a95d',
        'parts': [('Claudio Soto Gamboa', 2720, 'SUJETO_ROL_NOMBRE')]},
 2596: {'hash': '4e4b6a7c22f16ed220d06f11d516393b0849a8b6eb082e3114205f7b06d568a3',
        'parts': [('José De Gregorio Rebeco', 136, 'SUJETO_ROL_NOMBRE')]},
 2674: {'hash': 'd0bf1f145f07f3db3c185f7076213df875edad8f8c7939c209fd9dbbdae088aa',
        'parts': [('Claudio Soto Gamboa', 4095, 'SUJETO_NOMBRE'),
                  ('Kevin Cowan Logan', 386, 'SUJETO_ROL_NOMBRE'),
                  ('Igal Magendzo Weinberger', 237, 'SUJETO_ROL_NOMBRE'),
                   ('Pablo García Silva', 387, 'SUJETO_ROL_SESION'),
                  ('Claudio Soto Gamboa', 635, 'SUJETO_ROL_NOMBRE'),
                  ('Enrique Marshall Rivera', 1159, 'CONTEXTO_REVISADO'),
                  ('Claudio Soto Gamboa', 889, 'SUJETO_ROL_SESION'),
                  ('Andrés Velasco Brañes', 447, 'SUJETO_ROL_SESION')]},
 3011: {'hash': '212971befc4adbd893cf91d44cdc721c9d91794cf6b5ceff054c690f917c2bc7',
        'parts': [('Pablo García Silva', 8431, 'SUJETO_NOMBRE'),
                  ('José De Gregorio Rebeco', 172, 'SUJETO_ROL_SESION'),
                  ('Luis Felipe Céspedes Cifuentes', 3157, 'CONTEXTO_REVISADO')]},
 3056: {'hash': '42abadbe62a4b9d8acc7829cd02560885a62283c8afb7a4b942ef67b505e4465',
        'parts': [('Pablo García Silva', 222, 'SUJETO_NOMBRE'),
                  ('Manuel Marfán Lewis', 426, 'CONTEXTO_REVISADO'),
                  ('Pablo García Silva', 560, 'SUJETO_NOMBRE')]},
 3299: {'hash': '2097c4b5e5ee13d264697b26978a91ea4a52162b28dc0bca403adf4c7e21a24e',
        'parts': [('José De Gregorio Rebeco', 285, 'SUJETO_ROL_NOMBRE')]},
 3435: {'hash': '408a15649a9bf0bfa68ebace2bf8384574659414f04f0db75f02ec5de54098bd',
        'parts': [('Sebastián Claro Edwards', 587, 'SUJETO_ROL_NOMBRE'),
                  ('Enrique Marshall Rivera', 494, 'CONTEXTO_REVISADO')]},
 3442: {'hash': '314f83216d0a83272023f6739638c4b1e88e5b5801785acd7b2ce96819647eb6',
        'parts': [('Luis Óscar Herrera Barriga', 361, 'SUJETO_ROL_NOMBRE'),
                  ('Felipe Jaque', 1388, 'SUJETO_NOMBRE'),
                  ('Manuel Marfán Lewis', 395, 'SUJETO_ROL_NOMBRE'),
                  ('Beltrán de Ramón Acevedo', 136, 'CONTEXTO_REVISADO'),
                  ('Felipe Jaque', 1854, 'SUJETO_NOMBRE')]},
 3446: {'hash': 'e9b4168d636d3ec307cf528c4a10f4274d1d5758d2a8d83d6069926e3d0df972',
        'parts': [('Rodrigo Vergara Montes', 158, 'SUJETO_ROL_NOMBRE'),
                  ('Felipe Jaque', 1592, 'SUJETO_NOMBRE')]},
 3523: {'hash': 'f6fb765747617be89ae3aee127743ae4bc31fc03eef36eb3a6a6a2585b0b3733',
        'parts': [('José De Gregorio Rebeco', 186, 'SUJETO_ROL_NOMBRE'),
                  ('Manuel Marfán Lewis', 281, 'CONTEXTO_REVISADO')]},
 4122: {'hash': '5d46c848761c8c1d5a1a36adf29e609cc2d1db20406fdc3adfd49d89e72315eb',
        'parts': [('Sebastián Claro Edwards', 299, 'SUJETO_ROL_NOMBRE')]},
 4148: {'hash': '833b05a345071ecde297364fdc6fb1f5ea95415860633c5e52f18fc0295dca67',
        'parts': [('Sergio Lehmann Beresi', 112, 'SUJETO_NOMBRE'),
                  ('Manuel Marfán Lewis', 313, 'CONTEXTO_REVISADO')]},
 4252: {'hash': '65f701da89f7e3dc0ad46b31af072e1292dbdd1825b27df9aeffc376fb2d06cb',
        'parts': [('Luis Óscar Herrera Barriga', 263, 'SUJETO_NOMBRE'),
                  ('Rodrigo Vergara Montes', 225, 'CONTEXTO_REVISADO')]},
 4256: {'hash': '64d2d7fd882d086ce79cb2e3e32263502289d97739175f2973d48e5a1f876f1c',
        'parts': [('Luis Óscar Herrera Barriga', 241, 'SUJETO_ROL_NOMBRE'),
                  ('Matías Bernier Bórquez', 531, 'CONTEXTO_REVISADO')]},
 4342: {'hash': '0cfd5cd60e21054b532fa8494f65f04f7f9e0bdec560fb2b023081500d6bbfa3',
        'parts': [('Luis Óscar Herrera Barriga', 289, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 1940, 'SUJETO_NOMBRE'),
                  ('Luis Óscar Herrera Barriga', 284, 'SUJETO_NOMBRE'),
                  ('Sebastián Claro Edwards', 657, 'CONTEXTO_REVISADO')]},
 4477: {'hash': '47c0bba0d3bb372835a65c3ed726e0e38f449493a111cdbd5320c8a895285604',
        'parts': [('Luis Óscar Herrera Barriga', 568, 'SUJETO_ROL_NOMBRE'),
                  ('Enrique Marshall Rivera', 541, 'CONTEXTO_REVISADO'),
                  ('Sergio Lehmann Beresi', 567, 'SUJETO_NOMBRE'),
                  ('Luis Óscar Herrera Barriga', 499, 'SUJETO_NOMBRE')]},
 4547: {'hash': '9e12c90738c2fa93674d91e6aa1197a52251a15fe28a32d053cbb0b10c316222',
        'parts': [('Sebastián Claro Edwards', 351, 'SUJETO_ROL_NOMBRE')]},
 4589: {'hash': '60a94f37adc90db6a75ff56faaf01ea73b603b39d41443b737d11713c25ff1d0',
        'parts': [('Enrique Marshall Rivera', 545, 'SUJETO_ROL_NOMBRE'),
                  ('Joaquín Vial Ruiz-Tagle', 1230, 'CONTEXTO_REVISADO')]},
 4634: {'hash': '80eb62212a5aa92ac5c6cf62ae82f3a334c834a55735908510ab7c893d022133',
        'parts': [('Claudio Soto Gamboa', 2171, 'SUJETO_NOMBRE'),
                  ('Enrique Marshall Rivera', 188, 'CONTEXTO_REVISADO'),
                  ('Claudio Soto Gamboa', 2098, 'SUJETO_NOMBRE')]},
 4709: {'hash': '95dd01344d7e54a56db17c4f1e55886c66894b3af5e7b8167f40b2e6b333c234',
        'parts': [('Rodrigo Vergara Montes', 106, 'SUJETO_ROL_NOMBRE'),
                  ('Manuel Marfán Lewis', 162, 'CONTEXTO_REVISADO')]},
 4903: {'hash': '35c0ddc674d67a974cbd7c8fbaaf21e9528e469c4e2eeeb1e36a8f852c05b525',
        'parts': [('Rodrigo Vergara Montes', 166, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 462, 'CONTEXTO_REVISADO')]},
 4922: {'hash': 'cce0f4536e90e20bc6df32073fec5bedabb0c018d34368c21253d4e529bec501',
        'parts': [('Manuel Marfán Lewis', 236, 'SUJETO_ROL_NOMBRE'),
                  ('Sebastián Claro Edwards', 343, 'CONTEXTO_REVISADO')]},
 5197: {'hash': '749caf6ca66d30fa4b6bf22beb925ee0323c88d6b38c2333dc3d6a869e8a1399',
        'parts': [('Sebastián Claro Edwards', 279, 'SUJETO_ROL_NOMBRE')]},
 5347: {'hash': '3865fcaf2db17ecdf49b18873d36d31019e34fe1802bc662751d53a6a3eb199c',
        'parts': [('Sebastián Claro Edwards', 245, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 354, 'SUJETO_NOMBRE'),
                  ('Sebastián Claro Edwards', 397, 'CONTEXTO_REVISADO')]},
 5402: {'hash': '01f2b95bfac5a9cb9d42c72263c5fab8b96178c6ff3b6a3522871244522edc4e',
        'parts': [('Sergio Lehmann Beresi', 5443, 'SUJETO_NOMBRE'),
                  ('Sebastián Claro Edwards', 756, 'CONTEXTO_REVISADO')]},
 5403: {'hash': 'df9deb04d671749d859d3c0992138e3965672244975cfb2e2d5265180cce6ced',
        'parts': [('Sergio Lehmann Beresi', 653, 'SUJETO_NOMBRE')]},
 5470: {'hash': '0caa8c05ea24a2d8c6213b77d6c0def6dd2fefb3b63046d7250308678f0e80f4',
        'parts': [('Rodrigo Vergara Montes', 362, 'SUJETO_ROL_NOMBRE'),
                  ('Joaquín Vial Ruiz-Tagle', 181, 'CONTEXTO_REVISADO')]},
 5793: {'hash': '51b9611ad1506d09a871c40802b8fef43181e75e337d3ea92db7b94cb1705b1f',
        'parts': [('Rodrigo Vergara Montes', 1890, 'SUJETO_ROL_NOMBRE'),
                  ('Sebastián Claro Edwards', 199, 'CONTEXTO_REVISADO')]},
 6069: {'hash': '0e0d413e49eeaffb3ec3aa5084c3fc3b5ced1bd7b85aca2c8db7bdcbe7e25842',
        'parts': [('Sergio Lehmann Beresi', 3827, 'SUJETO_NOMBRE'),
                  ('Sebastián Claro Edwards', 314, 'CONTEXTO_REVISADO')]},
 6118: {'hash': '0ad5752390a1a76a704b1e2ba88432734ba20ec8657e063d065c85e9ab892579',
        'parts': [('Sebastián Claro Edwards', 490, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 839, 'CONTEXTO_REVISADO')]},
 6163: {'hash': 'b78e43d2474fb5990b165eae82f83bb4be4d077b0debddef9be73b0b96783443',
        'parts': [('Matías Bernier Bórquez', 113, 'SUJETO_NOMBRE'),
                  ('Pablo García Silva', 758, 'CONTEXTO_REVISADO'),
                  ('Rodrigo Vergara Montes', 246, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 145, 'ACTA/META')]},
 6257: {'hash': 'acdf92efa4c69d62e1da8a7cd479b8793ed2fef2dbb413dd7b837dafef94e973',
        'parts': [('Miguel Fuentes Díaz', 5614, 'SUJETO_NOMBRE'),
                  ('Claudio Soto Gamboa', 584, 'SUJETO_ROL_NOMBRE'),
                  ('Miguel Fuentes Díaz', 576, 'SUJETO_NOMBRE'),
                  ('Sebastián Claro Edwards', 536, 'CONTEXTO_REVISADO'),
                  ('Miguel Fuentes Díaz', 1270, 'SUJETO_NOMBRE'),
                  ('Joaquín Vial Ruiz-Tagle', 537, 'SUJETO_ROL_NOMBRE')]},
 6305: {'hash': '8c06f981eb49b6a13c21442f3f51a0bb05e9d0f2d35f29ec96a494c0e961af12',
        'parts': [('Rodrigo Vergara Montes', 187, 'SUJETO_ROL_NOMBRE'),
                  ('Joaquín Vial Ruiz-Tagle', 2300, 'CONTEXTO_REVISADO')]},
 6421: {'hash': 'b0e0187b2593aee9bb2b11a49c6b2e6383f323b9b0927ca82f91640fe0d2a4ac',
        'parts': [('Rodrigo Vergara Montes', 878, 'SUJETO_ROL_NOMBRE'),
                  ('Enrique Orellana Cifuentes', 1305, 'SUJETO_NOMBRE')]},
 6456: {'hash': '2cf01efe8f76c5b08f445bd3650fba098de46d4c849f34b0cf2279b9efed120a',
        'parts': [('Pablo García Silva', 828, 'SUJETO_ROL_NOMBRE'),
                  ('Joaquín Vial Ruiz-Tagle', 394, 'CONTEXTO_REVISADO')]},
 6654: {'hash': '32da280b3518d11072f5209cea88282fed6c98087db5828b1a81b71d5f6f3cdf',
        'parts': [("Alberto Naudon Dell'Oro", 598, 'SUJETO_NOMBRE')]},
 6791: {'hash': '9c304c09d9108fc6a5f77ed50f99a16d2335ac77ea161ac8fe7beb69d95557c2',
        'parts': [('Enrique Marshall Rivera', 701, 'SUJETO_ROL_NOMBRE'),
                  ('Joaquín Vial Ruiz-Tagle', 237, 'CONTEXTO_REVISADO')]},
 6807: {'hash': '3cbf67d828141b3678c86c4d90717c12cc0e9962a93c3c26e451b1533b17fcd2',
        'parts': [('Rodrigo Vergara Montes', 260, 'SUJETO_ROL_NOMBRE')]},
 6808: {'hash': '32abf83e1251ea0d3989e22a0b41f9fbc50367ff3d1d859cdb2c80dee08bc3c3',
        'parts': [('Rodrigo Valdés Pulido', 633, 'SUJETO_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 1940, 'ACTA/META')]},
 6839: {'hash': 'ac3f9bde743958289d886c153a9de0c7002fecc39d6708c6c88ad3d99ca1f718',
        'parts': [("Alberto Naudon Dell'Oro", 89, 'SUJETO_NOMBRE'),
                  ('Joaquín Vial Ruiz-Tagle', 328, 'CONTEXTO_REVISADO')]},
 6869: {'hash': 'b360455f893041859218c9183c36903a3c995e1f0ab8bba710efcddad08e652c',
        'parts': [('Diego Gianelli Gómez', 291, 'SUJETO_NOMBRE'),
                  ('Pablo García Silva', 297, 'CONTEXTO_REVISADO')]},
 6900: {'hash': '39f7ebc108765e6081840859f0d67208a3ebe3c435ed42ccf523a815537c8c75',
        'parts': [("Alberto Naudon Dell'Oro", 155, 'SUJETO_NOMBRE'),
                  ('Pablo García Silva', 934, 'CONTEXTO_REVISADO')]},
 6902: {'hash': 'de137d0db0d6f1057cae4020c2bf39efac22eebdd0d6d7be5a42426e2371db60',
        'parts': [('Rodrigo Vergara Montes', 811, 'SUJETO_ROL_NOMBRE'),
                  ('Pablo García Silva', 818, 'CONTEXTO_REVISADO'),
                  ('Joaquín Vial Ruiz-Tagle', 485, 'SUJETO_ROL_NOMBRE')]},
 6953: {'hash': '8c322205a1d0c46d862b13d708ef3595796b7fa1981d8891bbb4d7b445ae3dd2',
        'parts': [('Pablo García Silva', 1047, 'SUJETO_ROL_NOMBRE'),
                  ('Sebastián Claro Edwards', 1045, 'CONTEXTO_REVISADO')]},
 6959: {'hash': '052db85b8d370783158991bda2043150db2bbb38222f3565e4f1aaf1480901d0',
        'parts': [('Sebastián Claro Edwards', 638, 'SUJETO_ROL_NOMBRE')]},
 6985: {'hash': '7a324d6452b0874e06d6d850ef72cf1d509c5df0aaff5d765507641365b56230',
        'parts': [('Sebastián Claro Edwards', 308, 'SUJETO_ROL_NOMBRE'),
                  ('Diego Gianelli Gómez', 1920, 'SUJETO_NOMBRE'),
                  ('Alejandro Micco', 289, 'SUJETO_ROL_NOMBRE'),
                  ('Sebastián Claro Edwards', 749, 'CONTEXTO_REVISADO')]},
 7021: {'hash': '4e8ac52f3404358ea42f8a506309b98ed9cb4e4b0d4d8ee4d3ac45d609c33012',
        'parts': [('Miguel Fuentes Díaz', 783, 'SUJETO_NOMBRE'),
                  ('Joaquín Vial Ruiz-Tagle', 409, 'CONTEXTO_REVISADO'),
                  ('Miguel Fuentes Díaz', 636, 'SUJETO_NOMBRE')]},
 7079: {'hash': 'b8863670ba2b9aff431960086659639e5b9a83fc8e3139cf21be09fdbe995faf',
        'parts': [('Miguel Fuentes Díaz', 556, 'SUJETO_NOMBRE'),
                  ('Claudio Soto Gamboa', 216, 'SUJETO_ROL_NOMBRE'),
                  ('Miguel Fuentes Díaz', 779, 'SUJETO_NOMBRE'),
                  ('Sebastián Claro Edwards', 804, 'CONTEXTO_REVISADO')]},
 7125: {'hash': '98eb62b766027b19efad46b3c97600325cd6d4a9529cd0a7e0d899e1d3054893',
        'parts': [("Alberto Naudon Dell'Oro", 1655, 'SUJETO_NOMBRE'),
                  ('Rodrigo Vergara Montes', 127, 'SUJETO_ROL_NOMBRE')]},
 7142: {'hash': 'ab2c975eee1e94dffb93fe375f0f9256bd3efae2cc1daa9ccc0a04127d8617da',
        'parts': [('Sebastián Claro Edwards', 522, 'SUJETO_ROL_NOMBRE'),
                  ('Joaquín Vial Ruiz-Tagle', 1123, 'CONTEXTO_REVISADO'),
                  ('Mario Marcel Cullell', 1738, 'SUJETO_ROL_NOMBRE')]},
 7174: {'hash': '1ef8e74178fb41930d6178ed35cc14cbd4078386dd6e9698a9edf641e4442dd5',
        'parts': [('Pablo García Silva', 526, 'SUJETO_ROL_NOMBRE'),
                  ('Rodrigo Vergara Montes', 133, 'CONTEXTO_REVISADO')]}}

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
for p,e in FIXTURES.items():setattr(LoopTenTests,f'test_parent_{p}',fixture_test(p,e))

if __name__=='__main__':unittest.main()
