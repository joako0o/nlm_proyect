"""Loop9: contratos de los 60 padres afectados, más límites negativos/contextuales.
Las fixtures congelan resultados comparados; no certifican lectura humana integral.
"""
import hashlib
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, validate_speaker_reviews
from continuity import annotate_turns, boundary

class LoopNineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)
    def parts(self,p):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p))
    def test_new_predicates_need_a_speaking_subject(self):
        for verb in ['proporciona un comentario','hace un comentario','efectúa varias reflexiones',
                     'hace énfasis','pone énfasis','hace la salvedad','clarifica','especifica','colige',
                     'deduce','calcula','compara','disiente','no descarta','no advierte',
                     'se compromete a informar','se compromete a actualizar','se compromete a analizar',
                     'se compromete a presentar','se compromete a continuar monitoreando',
                     'admite','tiende a compartir','tiende a coincidir','suscribe plenamente','lo confirma']:
            t=f'El señor Sergio Lehmann {verb} la evolución de las cifras.'
            self.assertEqual(b.TURN_DETECTOR.speaker(t,'2013-08-13')['actor'],'Sergio Lehmann Beresi',t)
            for bad in ['“'+t+'”', 'Se cita que '+t, 'Según '+t.lower(),
                        f'La opinión del señor Sergio Lehmann {verb} la evolución de las cifras.']:
                self.assertIsNone(b.TURN_DETECTOR.speaker(bad,'2013-08-13'),bad)
    def test_concessive_attaches_to_same_subject(self):
        t='El señor Alberto Naudon, si bien comparte el planteamiento del Consejero señor Sebastián Claro, cita el caso de Suecia.'
        self.assertEqual(b.TURN_DETECTOR.speaker(t,'2015-02-12')['actor'],"Alberto Naudon Dell'Oro")
    def test_concessive_cannot_borrow_a_different_subjects_verb(self):
        for t in ['El señor Alberto Naudon, si bien el Consejero señor Sebastián Claro señala riesgos, está presente.',
                  'El señor Alberto Naudon, si bien está presente, escucha al Consejero.',
                  'La opinión del señor Alberto Naudon, si bien comparte el argumento, es citada.',
                  'El señor Alberto Naudon tiende a sentarse a la mesa.',
                  'El señor Alberto Naudon se compromete a asistir a la reunión.']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2015-02-12'),t)
    def test_opening_and_welcome_do_not_make_recipient_a_speaker(self):
        for verb in ['da inicio a la Reunión de Política Monetaria','da la bienvenida al Ministro de Hacienda señor Felipe Larraín']:
            t=f'El Presidente señor Rodrigo Vergara {verb}.'
            parts=b.segment_turns(t,'2013-08-13','Rodrigo Vergara Montes')
            self.assertEqual([a for text,a,m in parts],['Rodrigo Vergara Montes'])
    def test_closing_is_a_downstream_continuity_barrier(self):
        for verb in ['da por finalizada la sesión','da por concluida la sesión']:
            t=f'El Presidente señor Rodrigo Vergara {verb}.'
            self.assertTrue(boundary(t))
            rows=[dict(ID_Intervencion=str(i),ID_Bloque_Texto=str(i),Fecha='2013-08-13',
                       Actor_Final='Rodrigo Vergara Montes',Texto=text,Fuente_Actor='SUJETO_ROL_NOMBRE',
                       Tipo_Acta='INTERVENCION',Motivos_Revision='') for i,text in enumerate([t,'El Presidente señor Rodrigo Vergara señala otro punto.'])]
            annotate_turns(rows)
            self.assertNotEqual(rows[0]['ID_Turno'],rows[1]['ID_Turno'])
    def test_return_lead_requires_predicate_not_attendance(self):
        pre='Al continuar con su presentación, el señor Claudio Soto '
        self.assertEqual(b.TURN_DETECTOR.speaker(pre+'reitera las proyecciones.','2012-03-15')['actor'],'Claudio Soto Gamboa')
        for t in [pre+'está presente.', '“'+pre+'reitera las proyecciones.”',
                  'Al continuar con su presentación según el señor Claudio Soto reitera las proyecciones.']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2012-03-15'),t)
    def test_4719_opinion_is_bounded_between_soto_returns(self):
        parts=self.parts(4719)
        self.assertEqual([a for t,a,m in parts],['Claudio Soto Gamboa','Enrique Marshall Rivera','Claudio Soto Gamboa','Rodrigo Cerda Norambuena','Luis Óscar Herrera Barriga','Claudio Soto Gamboa'])
        self.assertTrue(parts[1][0].startswith('En opinión del Consejero señor Enrique Marshall'))
        self.assertTrue(parts[2][0].startswith('Al continuar con su presentación'))
        self.assertEqual(len(parts[-1][0]),4926)
    def test_4706_vial_not_a_mention_within_marfan(self):
        parts=self.parts(4706)
        self.assertEqual([a for t,a,m in parts],['Manuel Marfán Lewis','Joaquín Vial Ruiz-Tagle'])
        self.assertIn('En su opinión',parts[1][0])
    def test_6600_6601_four_distinct_views_then_fuentes_returns(self):
        self.assertEqual([a for t,a,m in self.parts(6600)],['Miguel Fuentes Díaz','Sebastián Claro Edwards'])
        self.assertEqual([a for t,a,m in self.parts(6601)],["Alberto Naudon Dell'Oro",'Beltrán de Ramón Acevedo','Pablo García Silva'])
        self.assertEqual([a for t,a,m in self.parts(6602)],['Miguel Fuentes Díaz'])
    def test_reviews_validate_exact_intervals_and_reject_overassignment(self):
        for p in [4706,4719,6600,6601]:
            rows=[dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p))]
            self.assertFalse(validate_speaker_reviews(rows,{p:self.reviews[p]}))
            row=next(r for r in rows if r['Fuente_Actor']=='CONTEXTO_REVISADO')
            row['Texto']+=' texto ajeno'
            self.assertTrue(validate_speaker_reviews(rows,{p:self.reviews[p]}))
    def test_no_general_opinion_rule_introduced(self):
        for lead in ['En opinión del señor Sergio Lehmann','A juicio del Consejero señor Sebastián Claro']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(lead+', las tasas son bajas.','2013-08-13'))
    def test_tam_bien_ocr_is_not_rewritten_in_output(self):
        parts=self.parts(6955)
        self.assertIn('tam bién',parts[0][0])
        self.assertEqual(parts[0][1],'Beltrán de Ramón Acevedo')
    def test_4096_soto_explanation_not_attached_to_presidents_request(self):
        parts=self.parts(4096)
        self.assertEqual(parts[3][1],'José De Gregorio Rebeco')
        self.assertEqual(parts[4][1],'Claudio Soto Gamboa')
        self.assertTrue(parts[4][0].startswith('El señor Claudio Soto especifica'))
    def test_3395_return_preserves_next_soto_paragraph(self):
        self.assertEqual([a for t,a,m in self.parts(3395)],['José De Gregorio Rebeco','Claudio Soto Gamboa','José De Gregorio Rebeco','Claudio Soto Gamboa'])
        self.assertEqual([a for t,a,m in self.parts(3396)],['Claudio Soto Gamboa'])
    def test_2626_specification_is_cowan_not_de_gregorio(self):
        parts=self.parts(2626)
        self.assertEqual([a for t,a,m in parts],['José De Gregorio Rebeco','Kevin Cowan Logan'])
        self.assertTrue(parts[1][0].startswith('a lo cual el Gerente de División Política Financiera especifica'))
    def test_3982_confirming_reply_is_lehmann(self):
        self.assertEqual([(a,t.strip()) for t,a,m in self.parts(3982)][-1],('Sergio Lehmann Beresi','El señor Lehmann lo confirma.'))
    def test_five_welcomes_keep_session_narrative_and_handoff_distinct(self):
        for p in [3631,3702,3801,3881,4320]:
            parts=self.parts(p)
            self.assertEqual([a for t,a,m in parts],['José De Gregorio Rebeco',b.CONSEJO,'José De Gregorio Rebeco'])
            self.assertIn('da la bienvenida',parts[-1][0])
            self.assertIn('concede la palabra',parts[-1][0])
    def test_pending_joint_passages_not_solved_by_opinion_reviews(self):
        self.assertFalse({780,3191,5367,5647,6185,2126}&set(self.reviews))

FIXTURES = {81: {'hash': 'f90369e73f9c615d024061e1f00d851e9f6c5badf8d839df77fda14d16d05dce',
      'parts': [('Jorge Desormeaux Jiménez', 767, 'SUJETO_ROL_NOMBRE')]},
 597: {'hash': '26a0f87470296053ca6a3b4f4465f0825ccfdb971bbc188d17fb30db77effb13',
       'parts': [('Vittorio Corbo Lioi', 606, 'SUJETO_ROL_NOMBRE')]},
 2015: {'hash': 'fbe4082b81378d2f5cc60789ea8bccd6c73126a8cb84d11d9103ee5a12c07eca',
        'parts': [('Sebastián Claro Edwards', 402, 'SUJETO_ROL_NOMBRE')]},
 2397: {'hash': '43039a562f42e9cadfef7c063187093f63e51a5ba091a71aba36a628e397eae2',
        'parts': [('Sebastián Claro Edwards', 1537, 'SUJETO_ROL_NOMBRE')]},
 2557: {'hash': 'aaaefcb1d507e4216d6c731aac9dadd0984a66d2bea81737c2c3399f90c763db',
        'parts': [('Jorge Desormeaux Jiménez', 266, 'SUJETO_ROL_NOMBRE')]},
 2626: {'hash': '32317abc356a527a5a80a4035251e40a2b0680fbc14f5cab511d02200201f588',
        'parts': [('José De Gregorio Rebeco', 297, 'SUJETO_ROL_NOMBRE'),
                  ('Kevin Cowan Logan', 143, 'SUJETO_ROL_SESION')]},
 2830: {'hash': '491ac84ca533a9da1d7dbfd1f85626186a43aeab95f0882663b0d995cc64b798',
        'parts': [('José De Gregorio Rebeco', 133, 'SUJETO_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 426, 'ACTA/META'),
                  ('José De Gregorio Rebeco', 181, 'SUJETO_ROL_NOMBRE')]},
 2875: {'hash': '130cfe9812c54e581dfc4c2d8a9d46092a7a31da68109450c501a8304a3b2e37',
        'parts': [('José De Gregorio Rebeco', 79, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 1038, 'ACTA/META')]},
 2951: {'hash': '396974d2aae86df70234ed39e01ce0d68b185a83d7ad82f30237a8a2f3ccc578',
        'parts': [('Manuel Marfán Lewis', 3638, 'SUJETO_ROL_NOMBRE')]},
 3008: {'hash': 'e06a08c6d205aadcc7918c9243c489cb14ee76fe353db9d8ec7e6684b525e9e8',
        'parts': [('José De Gregorio Rebeco', 61, 'SUJETO_ROL_SESION'),
                  ('Consejo del Banco Central de Chile', 332, 'ACTA/META'),
                  ('Felipe Larraín Bascuñán', 413, 'SUJETO_ROL_SESION')]},
 3109: {'hash': 'f2a1f75ab21cc2a640fe19ade11f383544c10a4074425163766187c71bcea186',
        'parts': [('José De Gregorio Rebeco', 144, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 632, 'ACTA/META')]},
 3184: {'hash': 'e9e9f22c4c211c6b0257e84dac8d74e9fb6e0199d07acc27451883db772e8eb6',
        'parts': [('Manuel Marfán Lewis', 258, 'SUJETO_ROL_NOMBRE')]},
 3269: {'hash': '445405ded961630c8adf14a97808353da4cb503509b96ef3991f63d8545c6df3',
        'parts': [('José De Gregorio Rebeco', 96, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 247, 'ACTA/META')]},
 3283: {'hash': '41900b75d3b72836b4039bc9a4847dcd8289b0cf4600e40c77faf946b33ec2e7',
        'parts': [('José De Gregorio Rebeco', 140, 'SUJETO_ROL_NOMBRE')]},
 3328: {'hash': 'a57a126f7057d8456abecec3f31fa577474ac2049e19150e8b9782503bed9226',
        'parts': [('José De Gregorio Rebeco', 142, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 245, 'ACTA/META'),
                  ('Pablo García Silva', 449, 'SUJETO_ROL_SESION')]},
 3346: {'hash': 'fe59b53c2af691c994bbc9a0a8622acd8906261a7ac78d4bc160942f3912800b',
        'parts': [('José De Gregorio Rebeco', 556, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 5112, 'SUJETO_ROL_SESION')]},
 3373: {'hash': 'b1f5ffbfe38c837df8b4e6da8f81a4d8aec31e5216911f436080461e1ba06656',
        'parts': [('Manuel Marfán Lewis', 388, 'SUJETO_ROL_NOMBRE')]},
 3395: {'hash': '79cda47028cc2c8eb21577526a4e1212bbe884035e30a27495045a9dc6e94cf7',
        'parts': [('José De Gregorio Rebeco', 64, 'SUJETO_ROL_NOMBRE'),
                  ('Claudio Soto Gamboa', 145, 'SUJETO_NOMBRE'),
                  ('José De Gregorio Rebeco', 232, 'SUJETO_ROL_SESION'),
                  ('Claudio Soto Gamboa', 258, 'SUJETO_NOMBRE')]},
 3396: {'hash': '188b886c5a36d41fe2f8d6a1520f9c15261973e8d411c78104be93c4274c57b4',
        'parts': [('Claudio Soto Gamboa', 912, 'SUJETO_ROL_SESION')]},
 3398: {'hash': 'c0d3a27609cebaeefe0b28b41fc954a396f436b7debb1f0a7ebd910c1bbf2b97',
        'parts': [('José De Gregorio Rebeco', 243, 'SUJETO_ROL_NOMBRE')]},
 3434: {'hash': '06b772d68bf9c0c582e88d61b8980d3eb212c8f89160ee99b6d88e54fc21bf29',
        'parts': [('José De Gregorio Rebeco', 457, 'SUJETO_ROL_NOMBRE'),
                  ('Felipe Jaque', 2535, 'SUJETO_NOMBRE'),
                  ('José De Gregorio Rebeco', 241, 'SUJETO_ROL_NOMBRE'),
                  ('Felipe Jaque', 1551, 'SUJETO_NOMBRE')]},
 3475: {'hash': '7f0878895140617039f15048feab5edf4202c89a4924957ae313aae373bd1705',
        'parts': [('Luis Óscar Herrera Barriga', 677, 'SUJETO_ROL_NOMBRE')]},
 3502: {'hash': '3dc8f826126784cdfe0447ab189759d3c4bc6e47523276f08be07ce659bf5ece',
        'parts': [('Luis Óscar Herrera Barriga', 329, 'SUJETO_ROL_NOMBRE')]},
 3584: {'hash': 'd516c59e80eb65b23bf269f70a7c379883c20d020bd04351a9939d9f23183ac8',
        'parts': [('José De Gregorio Rebeco', 593, 'SUJETO_ROL_NOMBRE')]},
 3631: {'hash': 'faddb80354d4b9edf64f11cab59c3c7345c2c0894d6523d8c4cb5e3e21ba2cb2',
        'parts': [('José De Gregorio Rebeco', 166, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 74, 'ACTA/META'),
                  ('José De Gregorio Rebeco', 272, 'SUJETO_ROL_NOMBRE')]},
 3644: {'hash': '52cf94d31ada54e7e13ed4dad3ce68666917b1b3457188c10164ca8970deee35',
        'parts': [('José De Gregorio Rebeco', 593, 'SUJETO_ROL_NOMBRE')]},
 3691: {'hash': '77cb13b13d353128cf9cc0002345ab6473cfd62ac3cfd7a4d4a37a50fba74db5',
        'parts': [('Manuel Marfán Lewis', 690, 'SUJETO_ROL_NOMBRE')]},
 3702: {'hash': 'd7f84e900ecb628526ce032fdd24bba9d7c8711c01d0b45e570a7b11b88b0afd',
        'parts': [('José De Gregorio Rebeco', 166, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 74, 'ACTA/META'),
                  ('José De Gregorio Rebeco', 272, 'SUJETO_ROL_NOMBRE')]},
 3719: {'hash': '976e04d1e701d046c154bb09e68803fe455a0d31903bb804bb81a00eb44d53e9',
        'parts': [('José De Gregorio Rebeco', 588, 'SUJETO_ROL_NOMBRE')]},
 3801: {'hash': '99c86e420c37b51c52834a242ced8ddb108502dddfd5eee5686bf80e6345ff2b',
        'parts': [('José De Gregorio Rebeco', 180, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 74, 'ACTA/META'),
                  ('José De Gregorio Rebeco', 277, 'SUJETO_ROL_NOMBRE')]},
 3816: {'hash': '853e0a2d777357b86a11f408ee7fa6dd8e0dfcee700fd4fa4a9a6d2b0df60740',
        'parts': [('José De Gregorio Rebeco', 598, 'SUJETO_ROL_NOMBRE')]},
 3881: {'hash': 'e458cff26e259c2153c6d296cc745629ff93b821d3e99b929c09bb1240dffc1c',
        'parts': [('José De Gregorio Rebeco', 173, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 286, 'ACTA/META'),
                  ('José De Gregorio Rebeco', 257, 'SUJETO_ROL_NOMBRE')]},
 3982: {'hash': '62a39f76e15b89081033d033ce75021869c825a0803ab669593c9b804d7121b3',
        'parts': [('José De Gregorio Rebeco', 75, 'SUJETO_ROL_NOMBRE'),
                  ('Sergio Lehmann Beresi', 29, 'SUJETO_NOMBRE')]},
 3983: {'hash': '13df7c3a6719e282440fa60d93e0b72e84f7328acc5be0288c5dc25b8e10e3b4',
        'parts': [('Sergio Lehmann Beresi', 2129, 'SUJETO_ROL_NOMBRE')]},
 4057: {'hash': 'a8e47df95134c346bee42e52306dd0133e19d7417d0ac9904330f19cb0906742',
        'parts': [('José De Gregorio Rebeco', 543, 'SUJETO_ROL_NOMBRE')]},
 4096: {'hash': '5f4ff97d1bf62139df57fc62450655d2224118f57a85824a8baaa0a87cb42821',
        'parts': [('Claudio Soto Gamboa', 657, 'SUJETO_NOMBRE'),
                  ('Kevin Cowan Logan', 150, 'SUJETO_ROL_SESION'),
                  ('Claudio Soto Gamboa', 71, 'SUJETO_NOMBRE'),
                  ('José De Gregorio Rebeco', 160, 'SUJETO_ROL_NOMBRE'),
                  ('Claudio Soto Gamboa', 670, 'SUJETO_NOMBRE'),
                  ('Rodrigo Vergara Montes', 224, 'SUJETO_ROL_NOMBRE'),
                  ('Claudio Soto Gamboa', 1886, 'SUJETO_NOMBRE')]},
 4320: {'hash': '0a2c0d5fb5238fb1b7f5a049f8af282191c69e518b1dfa4c229acb3471050483',
        'parts': [('José De Gregorio Rebeco', 211, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 75, 'ACTA/META'),
                  ('José De Gregorio Rebeco', 354, 'SUJETO_ROL_NOMBRE')]},
 4516: {'hash': 'a10b4a186f366f46d9f4db81986e0716f46729d9a8182e0e8c7605ae255e6a68',
        'parts': [('Rodrigo Vergara Montes', 620, 'SUJETO_ROL_NOMBRE')]},
 4574: {'hash': '045077d5ab568d195b7d54184aa2311d5dccd98dc3737d4159356cedeb789ae2',
        'parts': [('Rodrigo Vergara Montes', 1228, 'SUJETO_ROL_NOMBRE')]},
 4626: {'hash': '86e45c68f85892e8866bec309eefed3bcc7413a8be811c8fddbc1b07e806f7ba',
        'parts': [('Claudio Soto Gamboa', 264, 'SUJETO_NOMBRE')]},
 4706: {'hash': '8e65497a8b4518d55a9c8b37d059e7c5a2b48c569de3e1cf0c10dec3b4b87700',
        'parts': [('Manuel Marfán Lewis', 205, 'SUJETO_ROL_SESION'),
                  ('Joaquín Vial Ruiz-Tagle', 436, 'CONTEXTO_REVISADO')]},
 4719: {'hash': '121041df1ffef7059ba39259476dc086e7db959457e4a97c2395bcfc6bd4d7f4',
        'parts': [('Claudio Soto Gamboa', 59, 'SUJETO_NOMBRE'),
                  ('Enrique Marshall Rivera', 197, 'CONTEXTO_REVISADO'),
                  ('Claudio Soto Gamboa', 2716, 'SUJETO_NOMBRE'),
                  ('Rodrigo Cerda Norambuena', 437, 'SUJETO_ROL_NOMBRE'),
                  ('Luis Óscar Herrera Barriga', 369, 'SUJETO_ROL_SESION'),
                  ('Claudio Soto Gamboa', 4926, 'SUJETO_NOMBRE')]},
 5121: {'hash': 'c0f9acf8395d0ccdceeb5df2cee13128b956e1507c4d5783388adf46b9cba782',
        'parts': [('Manuel Marfán Lewis', 385, 'SUJETO_ROL_NOMBRE')]},
 5243: {'hash': '835ecd08589bbb49a7e3ecc0327d7de5930ef121840a299874aac3d5f197d555',
        'parts': [('Enrique Marshall Rivera', 829, 'SUJETO_ROL_NOMBRE'),
                  ('Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE')]},
 5313: {'hash': '2c4168b49100aafd940012a22a8c363c36c76316c77041fe40160993ddbaecd5',
        'parts': [('Luis Óscar Herrera Barriga', 2174, 'SUJETO_ROL_NOMBRE'),
                  ('Rodrigo Vergara Montes', 230, 'SUJETO_ROL_NOMBRE'),
                  ('Consejo del Banco Central de Chile', 150, 'ACTA/META')]},
 5466: {'hash': 'e49247a33ae51326043dcfc3c6baee4cf7eafacc9472953407e7748cf5eed746',
        'parts': [('Rodrigo Vergara Montes', 645, 'SUJETO_ROL_NOMBRE')]},
 6094: {'hash': 'c74bde152f5fafc235eb28ec7b9750affc2de8e0253973b793fd0ecd9c24b68b',
        'parts': [('Rodrigo Vergara Montes', 1377, 'SUJETO_ROL_NOMBRE')]},
 6315: {'hash': 'f032a1e9e29ae8c46201153f9ff6e09e6314e244112c11f43d6bea41b947302f',
        'parts': [('Miguel Fuentes Díaz', 1697, 'SUJETO_NOMBRE')]},
 6600: {'hash': 'b19a99b55b3be58146041603ebb0b21b65dc3888431de87b953d1ce080e7c21f',
        'parts': [('Miguel Fuentes Díaz', 1827, 'SUJETO_NOMBRE'),
                  ('Sebastián Claro Edwards', 531, 'CONTEXTO_REVISADO')]},
 6601: {'hash': 'd09e27e7abe213204a5ddda08e3ac34f9a4e28ec328e41b536ab9c26a7da7c51',
        'parts': [("Alberto Naudon Dell'Oro", 833, 'SUJETO_ROL_NOMBRE'),
                  ('Beltrán de Ramón Acevedo', 311, 'SUJETO_ROL_NOMBRE'),
                  ('Pablo García Silva', 542, 'CONTEXTO_REVISADO')]},
 6650: {'hash': 'd6bec464e13dc742f230943e6589c7a617e5039384f07e32db03ef685a62adde',
        'parts': [('Elías Albagli Iruretagoyena', 627, 'SUJETO_ROL_NOMBRE')]},
 6661: {'hash': 'f880b41e37cd6ce44a993dec3132bd7f9152a45b3bd8a754aad32fe5a6ea15af',
        'parts': [('Rodrigo Vergara Montes', 900, 'SUJETO_ROL_NOMBRE')]},
 6832: {'hash': '6370447606c35d031186bee01ce066eb76499d180d575227a306f24fe6efcf3c',
        'parts': [('Miguel Fuentes Díaz', 247, 'SUJETO_NOMBRE')]},
 6923: {'hash': '9a9c5ee7e7061b15d9814e5effff71755561e6997f996487926fd426d002ca4c',
        'parts': [('Sebastián Claro Edwards', 881, 'SUJETO_ROL_NOMBRE')]},
 6955: {'hash': 'fce6dfa63ca0c2ec8e993a0ce453035b100443d1ea557144ae8e789da08b8759',
        'parts': [('Beltrán de Ramón Acevedo', 1501, 'SUJETO_ROL_NOMBRE')]},
 7014: {'hash': '80337ce32056f707925fbb51275513e7175f1cddcb2746455989a7df1e49bcd7',
        'parts': [('Rodrigo Vergara Montes', 164, 'SUJETO_ROL_NOMBRE')]},
 7025: {'hash': '757ce75a5846cfe865de0cf631f18d61b888fee44cc28652392a173c27ed9440',
        'parts': [('Miguel Fuentes Díaz', 2855, 'SUJETO_NOMBRE')]},
 7061: {'hash': '3be81dbe27148f06cb6c0e751d6ae2f589e615751f929cb2a06a21f2c76fdc63',
        'parts': [("Alberto Naudon Dell'Oro", 1176, 'SUJETO_NOMBRE')]},
 7070: {'hash': '20a25939709416187413fd977bd55700db4d6daf7a8ec0f9bfd84ff236a7d537',
        'parts': [('Joaquín Vial Ruiz-Tagle', 1203, 'SUJETO_ROL_NOMBRE')]},
 7089: {'hash': '96debfcb2ae10be81e9b043ca558b879eb384f3dbc79282a7fbf566c36c54730',
        'parts': [("Alberto Naudon Dell'Oro", 377, 'SUJETO_NOMBRE')]}}

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
for p,e in FIXTURES.items():setattr(LoopNineTests,f'test_parent_{p}',fixture_test(p,e))

if __name__=='__main__':unittest.main()
