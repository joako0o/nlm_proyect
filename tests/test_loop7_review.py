"""Loop7: regresión de alcance; no certificación semántica exhaustiva."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews
from procedural import FORMULA_REVIEWS,is_formula
from continuity import annotate_turns
PRES='Rodrigo Vergara Montes'

class LoopSevenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)
    def parts(self,p):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p))
    def test_direct_predicates_are_not_mention_windows(self):
        for verb in ['alude','corrobora','resume','hace el alcance','llama la atención']:
            text=f'El Consejero señor Sebastián Claro {verb} lo ocurrido.'
            self.assertEqual(b.TURN_DETECTOR.speaker(text,'2013-08-13')['actor'],'Sebastián Claro Edwards')
            for bad in ['“'+text+'”','Se cita que '+text,'Según '+text.lower(),
                        f'La opinión del Consejero señor Sebastián Claro {verb} lo ocurrido.']:
                self.assertIsNone(b.TURN_DETECTOR.speaker(bad,'2013-08-13'),bad)
    def test_en_tanto_requires_subject_and_immediate_predicate(self):
        self.assertEqual(b.TURN_DETECTOR.speaker('El señor Claudio Soto, en tanto, agrega una precisión.','2013-08-13')['actor'],'Claudio Soto Gamboa')
        for t in ['El señor Claudio Soto, en tanto, está presente.',
                  'El señor Claudio Soto, en tanto, los Consejeros opinan.',
                  'Según el señor Claudio Soto, en tanto, la inflación alude a otro fenómeno.',
                  '“El señor Claudio Soto, en tanto, agrega una precisión.”']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2013-08-13'))
    def test_handoff_prefixes_remain_bounded(self):
        for lead in ['No habiendo más consultas ni comentarios en lo concerniente al escenario internacional',
                     'No habiendo más consultas ni comentarios en io concerniente al escenario internacional',
                     'No habiendo más consultas ni comentarios respecto del escenario internacional',
                     'No existiendo otras consultas o comentarios']:
            tail=', el Presidente señor Rodrigo Vergara da paso a la exposición del escenario interno.'
            self.assertEqual(b.TURN_DETECTOR.speaker(lead+tail,'2013-08-13')['actor'],PRES)
            for text in ['“'+lead+tail+'”',lead+' adicionales sobre la votación'+tail,
                         lead+', según el Presidente señor Rodrigo Vergara, da paso a la exposición.',
                         lead+', el Presidente señor Rodrigo Vergara está presente.']:
                self.assertIsNone(b.TURN_DETECTOR.speaker(text,'2013-08-13'),text)
    def test_recipient_does_not_start_presentation_in_handoff(self):
        for p in [4990,5286,5360,6080,6663]:
            part=self.parts(p)[-1]
            self.assertEqual(part[1],PRES)
            self.assertIn('da paso a la exposición',part[0])
    def test_5717_separates_handoff_and_actual_return(self):
        self.assertEqual([(a,len(t)) for t,a,m in self.parts(5717)], [('Claudio Soto Gamboa',895),(PRES,237),('Claudio Soto Gamboa',2954)])
        self.assertTrue(self.parts(5717)[2][0].startswith('El Gerente de Análisis Macroeconómico señor Claudio Soto inicia'))
    def test_6607_fuentes_returns_before_new_topic_and_stays_whole(self):
        self.assertEqual([(a,len(t)) for t,a,m in self.parts(6607)],[('Miguel Fuentes Díaz',1696),('Joaquín Vial Ruiz-Tagle',278),('Miguel Fuentes Díaz',4103)])
        self.assertIn('prosigue con su presentación destacando',self.parts(6607)[-1][0])
    def test_5113_lehmann_return_keeps_2772_characters(self):
        self.assertEqual([(a,len(t)) for t,a,m in self.parts(5113)],[('Sergio Lehmann Beresi',564),('Rodrigo Cerda Norambuena',391),('Sergio Lehmann Beresi',2772)])
    def test_3315_soto_starts_at_en_tanto_not_later_alude(self):
        self.assertEqual([len(t) for t,a,m in self.parts(3315)],[165,1239])
        self.assertTrue(self.parts(3315)[1][0].startswith('El señor Claudia Soto, en tanto,'))
    def test_2668_three_roles_are_not_collapsed(self):
        self.assertEqual([(a,len(t)) for t,a,m in self.parts(2668)],[('José De Gregorio Rebeco',390),('Pablo García Silva',247),('Claudio Soto Gamboa',2239)])
        self.assertEqual(b.TURN_DETECTOR.resolve_role(self.raw[2668]['Fecha'],'Gerente de División Estudios'),'Pablo García Silva')
    def test_opinion_reviews_are_not_a_global_rule(self):
        for p,start in [(4415,'En opinión del señor Sergio Lehmann,'),(5412,'En opinión del Consejero señor Enrique Marshall,')]:
            r=self.raw[p]
            without=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
            self.assertEqual(len(without),1)
            self.assertTrue(self.parts(p)[1][0].startswith(start))
    def test_curated_ocr_is_conserved(self):
        self.assertTrue(self.parts(5286)[0][0].endswith('. i'))
        self.assertIn('/y',self.parts(5286)[0][0])
        self.assertTrue(self.parts(5360)[0][0].endswith('B A N C O C E N T R A L D E C H I L E'))
        self.assertIn('en io concerniente',self.parts(5976)[-1][0])
    def test_unreviewed_damaged_handoffs_are_not_forced(self):
        for p in [5286,5360]:
            r=self.raw[p];self.assertEqual(len(b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])),1)
            e=copy.deepcopy(self.reviews[p]);e['Actor']='Claudio Soto Gamboa'
            with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)
    def test_repeated_procedural_text_is_not_deleted(self):
        part=self.parts(6926)[-1]
        self.assertEqual(part[1],PRES)
        self.assertEqual(part[0].count('No habiendo más consultas'),2)
        self.assertEqual(len(part[0]),341)
    def test_three_formulas_require_entire_exact_text(self):
        entries=[e for e in FORMULA_REVIEWS.values() if e['Revision_ID'].startswith('FORM-20260907-PASO-INTERNO')]
        self.assertEqual(len(entries),3)
        for e in entries:
            t=e['Texto'];self.assertTrue(is_formula(t));self.assertTrue(is_formula('  '+t.replace(' ','  ')+'  '))
            self.assertFalse(is_formula(t+' Recomienda reducir la tasa de política monetaria.'))
            self.assertFalse(is_formula('La situación económica es compleja. '+t))
    def test_joint_and_ambiguous_cases_are_not_reviewed_as_single_speaker(self):
        self.assertFalse({6185}&set(self.reviews))
        for p in [3191,5367]:
            self.assertGreater(self.reviews[p]["Inicio"],0)  # el prefijo conjunto no se adjudica
    def test_long_6185_is_not_split_on_conforme_senala(self):
        parts=self.parts(6185)
        self.assertEqual(len(parts),1)
        self.assertEqual(len(parts[0][0]),20118)
        self.assertEqual(parts[0][1],'Sergio Lehmann Beresi')
        self.assertIn('conforme señala el Gerente de Mercados Nacionales señor Matías Bernier',parts[0][0])

# Fixtures fijadas después de contrastar los cambios de los cuatro ensayos.
# Ver docs/REVISION_LOOP7_2026-09-07.md: lectura de límites != pureza integral.
FIXTURES = {2668: {'hash': '7696cae883f2ac1a8f1761e6a582e04c3f16b1697089534135a840419f6a5eb0',
        'parts': [['José De Gregorio Rebeco', 390, 'SUJETO_ROL_NOMBRE'],
                  ['Pablo García Silva', 247, 'CONTEXTO_REVISADO'],
                  ['Claudio Soto Gamboa', 2239, 'SUJETO_ROL_SESION']]},
 2719: {'hash': 'e01e62d856277cddd3c7424dee60af7bc206a93143b9d71622d0ebcebc9ddc19',
        'parts': [['José De Gregorio Rebeco', 243, 'SUJETO_ROL_NOMBRE'],
                  ['Sergio Lehmann Beresi', 762, 'SUJETO_NOMBRE']]},
 2724: {'hash': 'c5d864f739c9664cf1a51aa542e584e94a1d061eabae7d9db03bdd436552fdb2',
        'parts': [['Pablo García Silva', 238, 'SUJETO_NOMBRE'], ['Sergio Lehmann Beresi', 601, 'SUJETO_ROL_SESION']]},
 2729: {'hash': '3d49ac2056f15fb707b4bc08367ae9ab56b264d5555f97d52886d21c500d0c4f',
        'parts': [['Jorge Desormeaux Jiménez', 391, 'SUJETO_ROL_NOMBRE']]},
 2813: {'hash': '87671708adb0a3268da33a14e078073ba240fe989df2b0b6cd9c4c893dbb1929',
        'parts': [['Enrique Marshall Rivera', 420, 'SUJETO_ROL_NOMBRE']]},
 2986: {'hash': 'c67843ec005e2c4237d17abe5ca4d210d8158bec6662c20d743f88d7060b9f3a',
        'parts': [['Sebastián Claro Edwards', 257, 'SUJETO_ROL_NOMBRE']]},
 3036: {'hash': '5bf137e41fcf6e2db1b7fd8cec27e237974fd8ea23877dc0dd5fcbd99c04dc9d',
        'parts': [['José De Gregorio Rebeco', 167, 'SUJETO_ROL_SESION']]},
 3059: {'hash': 'aa3f6718fb185fec90ae4c4540deffa9c5fe69aedb2522835b479b1c4919a8b2',
        'parts': [['Sebastián Claro Edwards', 754, 'SUJETO_ROL_NOMBRE']]},
 3131: {'hash': '2b2e5c99827186efa1ede163eeff250d07509d42d0fec09dfb550811656ee976',
        'parts': [['Sebastián Claro Edwards', 694, 'SUJETO_ROL_NOMBRE'],
                  ['Sergio Lehmann Beresi', 399, 'SUJETO_NOMBRE'],
                  ['José De Gregorio Rebeco', 308, 'SUJETO_ROL_NOMBRE']]},
 3152: {'hash': '83d4c625e16ed8cdce453a40e86555a64d70ed38c3385cf34969a1a45f23f3ad',
        'parts': [['Sebastián Claro Edwards', 260, 'SUJETO_ROL_NOMBRE']]},
 3161: {'hash': '496b346628b36e8efe4f0a49d71c52b7284977e5cbc5187e3155a3c68e506f56',
        'parts': [['Enrique Marshall Rivera', 109, 'SUJETO_ROL_NOMBRE']]},
 3186: {'hash': '65a440f8ebabefcb64efd154c3e8bc226708372a0611c86f931a7f47e7e71a77',
        'parts': [['Sebastián Claro Edwards', 156, 'SUJETO_ROL_NOMBRE']]},
 3256: {'hash': 'f183b1feaba61b7ad5ea401773b9058677852ba7b6b5dd6c8c47486bf49a6dba',
        'parts': [['Pablo García Silva', 306, 'SUJETO_ROL_NOMBRE']]},
 3298: {'hash': 'dbc17baf722e6c766c8f8d697713f797fcd4a534930dce008c13ec5fa8a03021',
        'parts': [['Manuel Marfán Lewis', 537, 'SUJETO_ROL_NOMBRE'],
                  ['Claudio Soto Gamboa', 733, 'SUJETO_ROL_SESION']]},
 3315: {'hash': 'f01ccc15a4a4e8729c22c1be73c903c44a151b872713a01b36c5a49508f1c4e3',
        'parts': [['Ricardo Vicuña Poblete', 165, 'SUJETO_ROL_NOMBRE'],
                  ['Claudio Soto Gamboa', 1239, 'SUJETO_NOMBRE']]},
 3376: {'hash': '61a15ddf126fe458dafcdcf2d4f6fa271df2cfa0f1e90f314c21f570e939fc80',
        'parts': [['Pablo García Silva', 285, 'SUJETO_ROL_NOMBRE']]},
 3534: {'hash': '437444b8a064ec18314d72dd27f1eaab32b1cbbc3456b982a45c9ca7f4b12c90',
        'parts': [['Sebastián Claro Edwards', 270, 'SUJETO_ROL_NOMBRE']]},
 3624: {'hash': '42fc5570d1b2fad06e4dd7404d4ff5945e67c35968ea958d55dc3c301b41b331',
        'parts': [['Kevin Cowan Logan', 188, 'SUJETO_ROL_NOMBRE'],
                  ['Luis Felipe Céspedes Cifuentes', 293, 'SUJETO_ROL_NOMBRE']]},
 3854: {'hash': 'd269d810d86b79fe1df9306d02627b6c0fafafad4d03528446e76c600a635fbd',
        'parts': [['Enrique Marshall Rivera', 253, 'SUJETO_ROL_NOMBRE']]},
 3896: {'hash': '77027ba617f3f6adbc456f95480b15a036f0615293d034c4db1f222858c0521c',
        'parts': [['José De Gregorio Rebeco', 228, 'SUJETO_ROL_NOMBRE']]},
 3930: {'hash': '5680ed04d3020cf771478c0dbe9b1ba161117822fdc850442a2f7f9953d12126',
        'parts': [['Claudio Soto Gamboa', 462, 'SUJETO_NOMBRE']]},
 4067: {'hash': '0adfaeefb630514777ddb4c8189290b808050855b15bad3c344ea0b73037ce2c',
        'parts': [['Sebastián Claro Edwards', 178, 'SUJETO_ROL_NOMBRE']]},
 4146: {'hash': 'fb071c80197820506552cad3a86509c8ba362ed1fd94e3660ccf47338fd10e65',
        'parts': [['Sebastián Claro Edwards', 883, 'SUJETO_ROL_NOMBRE']]},
 4161: {'hash': 'bec89b775709961c221443ac4c10ca0d18f9b603de85b2c77518ad29fc374a67',
        'parts': [['José De Gregorio Rebeco', 226, 'SUJETO_ROL_NOMBRE']]},
 4163: {'hash': '0dc4630e9d951deaefa1c7ee992ac6fc6e7cf39f5d3ed9246749e1e8dfe592fb',
        'parts': [['José De Gregorio Rebeco', 127, 'SUJETO_ROL_NOMBRE']]},
 4164: {'hash': '3ef3626867812057c079b4d424bd3d4cc08a8e8c9e4b531d3bd26dc2f004012d',
        'parts': [['Manuel Marfán Lewis', 572, 'SUJETO_ROL_NOMBRE']]},
 4180: {'hash': 'c7fd54d17118d536c46085492c8903f510926eaf9e76cbfa3aed74529b3e609d',
        'parts': [['Luis Óscar Herrera Barriga', 84, 'SUJETO_NOMBRE']]},
 4230: {'hash': 'ee1ead30c8eb1be19910592ba0d79b5cc788e2ea66262b350f02e963bfc2bf24',
        'parts': [['José De Gregorio Rebeco', 139, 'SUJETO_ROL_NOMBRE'],
                  ['Sergio Lehmann Beresi', 557, 'SUJETO_NOMBRE']]},
 4286: {'hash': '3ea2a22e3496b534cb9c50595c44673fb111ceb97b9aa284f4b8993c59f410dc',
        'parts': [['Rodrigo Vergara Montes', 141, 'SUJETO_ROL_NOMBRE']]},
 4354: {'hash': '8e4d2660b10563b25cc67473082dd962d8210507de932a2ad53390462f0c1685',
        'parts': [['Rodrigo Vergara Montes', 190, 'SUJETO_ROL_NOMBRE']]},
 4355: {'hash': '988e505c0c2b28896a2c0117047de4f7a28a368f8550296dfb7abbc11390a776',
        'parts': [['Sebastián Claro Edwards', 455, 'SUJETO_ROL_NOMBRE']]},
 4408: {'hash': '312361058f10953f0968c08f29acb5c6901b966260a812e10b5063e19c4cb249',
        'parts': [['Rodrigo Vergara Montes', 89, 'SUJETO_ROL_NOMBRE'],
                  ['Sergio Lehmann Beresi', 3019, 'SUJETO_NOMBRE']]},
 4415: {'hash': '9826d571e2ba93eff3a164a59522467693773ba281dff410abd39f2333cd7b28',
        'parts': [['Sebastián Claro Edwards', 879, 'SUJETO_ROL_NOMBRE'],
                  ['Sergio Lehmann Beresi', 464, 'CONTEXTO_REVISADO']]},
 4417: {'hash': '06331c1379a3a1c559b7681b1d9c2cb7b2c45974b33166c01fc34975c49a6ff8',
        'parts': [['Luis Óscar Herrera Barriga', 649, 'SUJETO_NOMBRE']]},
 4560: {'hash': '22ef9a1b7c8ce7868b5c634cf451f44e864c42bd3fb9fe6879ce32aeddfc0c89',
        'parts': [['Sebastián Claro Edwards', 532, 'SUJETO_ROL_NOMBRE']]},
 4617: {'hash': 'f1ea9451ad35d6b1de4525dc85811d701a995fa453425902af3019d809d375d5',
        'parts': [['Kevin Cowan Logan', 263, 'SUJETO_ROL_NOMBRE']]},
 4636: {'hash': '2bfeb3457de062fb9c5c70ac2a2f24b6cb15c64939d69c93406ada14f77e44ba',
        'parts': [['Beltrán de Ramón Acevedo', 342, 'SUJETO_ROL_NOMBRE']]},
 4696: {'hash': 'bcefdf1c62cc9ac6c8d754528374ff400e4adaef990f3469b9c5ac1f392105f0',
        'parts': [['Luis Óscar Herrera Barriga', 283, 'SUJETO_ROL_NOMBRE']]},
 4737: {'hash': 'a4dd12f01d4e218c85068e15e531941db7ea121d548694ddcda8480e6d87c867',
        'parts': [['Sebastián Claro Edwards', 539, 'SUJETO_ROL_NOMBRE']]},
 4743: {'hash': '4040cd13df0463aa710ca0dfff3b1e3476e5f83a9dc475d5aff71d7adc006929',
        'parts': [['Sergio Lehmann Beresi', 263, 'SUJETO_NOMBRE'],
                  ['Rodrigo Cerda Norambuena', 140, 'SUJETO_ROL_NOMBRE']]},
 4801: {'hash': '3ff57ac853440e38fc98aa9c9e66e54e5af266536b67091ded46d8346d5cfeb5',
        'parts': [['Enrique Marshall Rivera', 853, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 276, 'SUJETO_ROL_NOMBRE'],
                  ['Enrique Marshall Rivera', 227, 'SUJETO_ROL_NOMBRE']]},
 4816: {'hash': '413fac5f67afdd2a4f9923d6b76d78367061bfdc7606e4ad72d31111aee50f16',
        'parts': [['Sebastián Claro Edwards', 1486, 'SUJETO_ROL_NOMBRE']]},
 4820: {'hash': 'cc00d578cfb0a47c1a66275b42b91b78dad5746ea0a11628a5d107e6288babba',
        'parts': [['Manuel Marfán Lewis', 626, 'SUJETO_ROL_NOMBRE'],
                  ['Luis Óscar Herrera Barriga', 872, 'SUJETO_ROL_NOMBRE'],
                  ['Sergio Lehmann Beresi', 236, 'SUJETO_NOMBRE'],
                  ['Rodrigo Vergara Montes', 228, 'SUJETO_ROL_NOMBRE']]},
 4868: {'hash': '896656e97552bd131d5d01a43e3f498e16b60e96f896d6f0bca1200195697a24',
        'parts': [['Rodrigo Vergara Montes', 748, 'SUJETO_ROL_NOMBRE']]},
 4932: {'hash': 'ac2381139cbaad5ba1a41d6b8211b8bb3f55ac06daf8c1bd0401172fe7765b9e',
        'parts': [['Sebastián Claro Edwards', 358, 'SUJETO_ROL_NOMBRE']]},
 4934: {'hash': 'c47ec203958df0aef505b005f1e883a428243af44e7d1a30f0e5fe792b91a0ac',
        'parts': [['Rodrigo Vergara Montes', 201, 'SUJETO_ROL_NOMBRE']]},
 4990: {'hash': 'ec25a58ed0878c79dbcc3d21f76c862c82eb441c9d31a0637d3cc196934223f5',
        'parts': [['Enrique Marshall Rivera', 582, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE']]},
 4998: {'hash': '33a94acba0093d50fa189b219d70253bfee9889c095fe22772a0dab42e6e738d',
        'parts': [['Claudio Soto Gamboa', 1087, 'SUJETO_ROL_NOMBRE']]},
 5047: {'hash': 'da64add2753844af02dc74cc5cb04a99dea269819abc740e89e305fbd762d282',
        'parts': [['Manuel Marfán Lewis', 725, 'SUJETO_ROL_NOMBRE']]},
 5065: {'hash': 'f6c1606a59248b14aaad9bf2e01425d685d8dcae2cdaee5791d9ff28e62b29ca',
        'parts': [['Luis Opazo Roco', 607, 'SUJETO_ROL_NOMBRE'], ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE']]},
 5079: {'hash': 'aeb39a21685ff3a56030e233e2bb969d574fcb57c5d1b68628eac8cffe522e63',
        'parts': [['Manuel Marfán Lewis', 239, 'SUJETO_ROL_NOMBRE'], ['Sergio Lehmann Beresi', 451, 'SUJETO_NOMBRE']]},
 5113: {'hash': 'a7963b1950bf868de0de303aba83eb3289c5a0df92d896a41f00753b62b536c6',
        'parts': [['Sergio Lehmann Beresi', 564, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Cerda Norambuena', 391, 'SUJETO_ROL_NOMBRE'],
                  ['Sergio Lehmann Beresi', 2772, 'SUJETO_NOMBRE']]},
 5122: {'hash': 'f38a0edb04e1c69ef7e3a4c8de6e242974d2cf89eb142e28ac7b37eb30396975',
        'parts': [['Luis Óscar Herrera Barriga', 3068, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE']]},
 5138: {'hash': 'd1bf4b4c226cf08910e29a672c62d5f3e4851152f190ed9b37a12f7e7eec59f2',
        'parts': [['Sebastián Claro Edwards', 577, 'SUJETO_ROL_NOMBRE']]},
 5178: {'hash': 'ca16c4687f45db890aa0750c80f21f07cf95f163266d9e0d1a8f76ed8e15a216',
        'parts': [('Luis Óscar Herrera Barriga', 1825, 'SUJETO_ROL_NOMBRE'),
                  ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE']]},
 5229: {'hash': '813aaf1b2e373d4f15f5cf54e76bbb357fac154d9f4d5c4e7bf3c8344ff750d7',
        'parts': [['Sergio Lehmann Beresi', 901, 'SUJETO_NOMBRE']]},
 5243: {'hash': '835ecd08589bbb49a7e3ecc0327d7de5930ef121840a299874aac3d5f197d555',
        'parts': [['Enrique Marshall Rivera', 829, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE']]},
 5282: {'hash': 'f51212eae1f78fc3502d17b9c8427e564e10671b1e36e9550ab3f8fe985d737d',
        'parts': [['Sebastián Claro Edwards', 594, 'SUJETO_ROL_NOMBRE']]},
 5286: {'hash': '2945a9a880aa7af5712d3c0773d384454ef9e6211db29c5f66c21850b351f7fe',
        'parts': [['Sergio Lehmann Beresi', 513, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'CONTEXTO_REVISADO']]},
 5303: {'hash': '7d8b646a30b0e76dadab0d59d1508c302d3d196adc1581416da3426ed382d4f2',
        'parts': [['Sebastián Claro Edwards', 512, 'SUJETO_ROL_NOMBRE']]},
 5360: {'hash': 'eab669191a29177eebc03a13070ca3f0ae2aa083ae09e3a4b8cc336cb1cb4c48',
        'parts': [['Luis Óscar Herrera Barriga', 1734, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 250, 'CONTEXTO_REVISADO']]},
 5372: {'hash': '62389e3945431e40221154643910f65d7f5190bf3dd1fd11e0aca9195c64b7e8',
        'parts': [['Miguel Fuentes Díaz', 603, 'SUJETO_NOMBRE']]},
 5412: {'hash': '0337a96b6d939ef65fb94bfe8112b1042487a54992e92d0306be6f79fca00aff',
        'parts': [['Sebastián Claro Edwards', 1118, 'SUJETO_ROL_NOMBRE'],
                  ['Enrique Marshall Rivera', 509, 'CONTEXTO_REVISADO']]},
 5417: {'hash': '0b110bda9616e8ae883f11941a200a9a2e9fa9dbf59505decb1561693a02c268',
        'parts': [['Enrique Marshall Rivera', 349, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'CONTEXTO_REVISADO']]},
 5435: {'hash': '34fa4a1097cadde33d7b21fa5e4e7b4656e839c6290806252253ca78494a9ed2',
        'parts': [['Kevin Cowan Logan', 2173, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 230, 'SUJETO_ROL_NOMBRE'],
                  ['Consejo del Banco Central de Chile', 145, 'ACTA/META']]},
 5473: {'hash': '15f5f06e654f768e6d6b48df3c2806c2c8986e6b623515a0161ae927e53881bd',
        'parts': [['Sebastián Claro Edwards', 1786, 'SUJETO_ROL_NOMBRE']]},
 5522: {'hash': 'aaa1fe7ce32241462341e79427388d1d0d4721d55c7010a029bed81fa4bf357d',
        'parts': [['Manuel Marfán Lewis', 328, 'SUJETO_ROL_NOMBRE']]},
 5534: {'hash': '3c8226a91c676ea7c6798e8e7e76f289534e462537b7e7eb84822bcc215fcd8f',
        'parts': [['Sergio Lehmann Beresi', 156, 'SUJETO_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE']]},
 5589: {'hash': '60c0b62019e1388f2d4b00c17632d0e793624aec252a94e92aba919f8c6f0503',
        'parts': [['Luis Óscar Herrera Barriga', 1801, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE']]},
 5605: {'hash': '5cbad232ea7177bc6234a5d8763d10d7c250f1110660dceb160ffa08275ddfc1',
        'parts': [['Matías Bernier Bórquez', 305, 'SUJETO_ROL_NOMBRE']]},
 5657: {'hash': '442a21b5b9a451e0ee0b7e557a899e50f85fb565383818ffadda80336606f7ae',
        'parts': [['Enrique Marshall Rivera', 390, 'SUJETO_ROL_NOMBRE']]},
 5662: {'hash': 'f7a4494a7003b286eddde25741da674b84b44dee4031bf3557c3ad9a862613a1',
        'parts': [['Joaquín Vial Ruiz-Tagle', 440, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE']]},
 5717: {'hash': 'd3747a05c28d3c716a683ed72e7676f2cf2dc16d243d0a9f57e54013609ea517',
        'parts': [['Claudio Soto Gamboa', 895, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE'],
                  ['Claudio Soto Gamboa', 2954, 'SUJETO_ROL_NOMBRE']]},
 5769: {'hash': '824b323a4b036716b3422c02cb7354d92616a0fbf5eb4d60d9a770f24191114c',
        'parts': [['Luis Óscar Herrera Barriga', 701, 'SUJETO_NOMBRE']]},
 5777: {'hash': '072aa09aa9f4250ac9bcdf96a82ae82e6ccfbf629179a962885d4f289270f10d',
        'parts': [['Sergio Lehmann Beresi', 876, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE']]},
 5794: {'hash': '71adddbc01e42d834ef075005208bbfe315e079eb8bfb28d8028bf2bc25fd90a',
        'parts': [['Manuel Marfán Lewis', 289, 'SUJETO_ROL_NOMBRE']]},
 5822: {'hash': '6ae328fb600ab8ecadaf0873540047ef0f51da4f3045c9423480212acf58f19b',
        'parts': [['Joaquín Vial Ruiz-Tagle', 1490, 'SUJETO_ROL_NOMBRE']]},
 5827: {'hash': '23b1e4434fe9f6673ff191029c75f10abef24f184f297e2b9b6ecb682262164d',
        'parts': [['Luis Óscar Herrera Barriga', 1803, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE']]},
 5870: {'hash': '3f7449ec86d2ce9bd2b12371354ce21b5864b0261d1a890082443bccbdcf290c',
        'parts': [['Sergio Lehmann Beresi', 799, 'SUJETO_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE']]},
 5917: {'hash': '64752f452f1e3c9da9692a7e0712338a4ff59eaf5e2d99452dcd501791ef3942',
        'parts': [['Manuel Marfán Lewis', 980, 'SUJETO_ROL_NOMBRE']]},
 5928: {'hash': 'dc0a2b628419f08fcc3a5e9e60d5eb9e1b47d3943bce0b1c783ce278265df604',
        'parts': [['Rodrigo Vergara Montes', 339, 'SUJETO_ROL_NOMBRE']]},
 5976: {'hash': '35870bf9ead1e1afa00cc4df3791f7ed9788e15d3c4e5a1062a394783851e0df',
        'parts': [['Sergio Lehmann Beresi', 703, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE']]},
 5981: {'hash': '893c91d223a4b730fd135b1493936df7a2185d9d98030aaf57c921b3fc17551f',
        'parts': [['Kevin Cowan Logan', 253, 'SUJETO_ROL_NOMBRE']]},
 5991: {'hash': '74becdbf6d4ca32f59b425ce9aeb847784d75b257ac9857a970b200a4229ba60',
        'parts': [['Claudio Soto Gamboa', 1349, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 246, 'SUJETO_ROL_NOMBRE'],
                  ['Consejo del Banco Central de Chile', 70, 'ACTA/META']]},
 5995: {'hash': '69db8264203bdf07f0debc00264d7ec0b33f1bad321e41fe16ee1b48c31bcd8b',
        'parts': [['Luis Óscar Herrera Barriga', 3848, 'SUJETO_NOMBRE']]},
 5996: {'hash': '7ed033fdcee7792c62f70fddd1c1275ab56568b274bde101c75bb2abe301d7c5',
        'parts': [['Luis Óscar Herrera Barriga', 605, 'SUJETO_ROL_NOMBRE']]},
 6026: {'hash': '2724a5e90edfaf7a7130a3b0c4a5edf7e997020e5b1c2a6d1773d0f1f1bbe83e',
        'parts': [['Kevin Cowan Logan', 498, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE']]},
 6080: {'hash': '1927366a7ca513fc5361b647012606e5c7aa9490c5a21a2b4f20112d69c696e5',
        'parts': [['Sergio Lehmann Beresi', 266, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 248, 'SUJETO_ROL_NOMBRE']]},
 6092: {'hash': 'fddd8a31e4f07b00748334fe4186b85154ce9fc1015b72566bc84fc4095646ff',
        'parts': [['Sebastián Claro Edwards', 769, 'SUJETO_ROL_NOMBRE']]},
 6132: {'hash': '68a61cc245d4b0016a56691a07783cea8250b557fa8669c20d277ba89cc7a4de',
        'parts': [['Luis Óscar Herrera Barriga', 369, 'SUJETO_NOMBRE'],
                  ['Sergio Lehmann Beresi', 760, 'SUJETO_NOMBRE'],
                  ['Rodrigo Vergara Montes', 239, 'SUJETO_ROL_NOMBRE']]},
 6192: {'hash': 'a7de89248379321ffff9fc70d4c83b6c7b2bfd7c603763645a93958abf2bf284',
        'parts': [('Sergio Lehmann Beresi', 1421, 'SUJETO_NOMBRE'),
                  ['Rodrigo Vergara Montes', 239, 'SUJETO_ROL_NOMBRE']]},
 6213: {'hash': '4ca38c6ed71ad9e8cadb8626bd0733bc6c30f4c05c91aabafbd334b6b3a278e7',
        'parts': [['Sebastián Claro Edwards', 479, 'SUJETO_ROL_NOMBRE']]},
 6308: {'hash': 'de05707a4bef7dfab0e52d8d551aee1072018d927d1a02e2af645345696ddeba',
        'parts': [['Pablo García Silva', 1830, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 2306, 'CONTEXTO_REVISADO']]},
 6321: {'hash': 'a536380e6d37acafa0f245351017f2ac0657b44714dc1b5cf6b16b6413b21796',
        'parts': [['Sebastián Claro Edwards', 1459, 'SUJETO_ROL_NOMBRE']]},
 6355: {'hash': '67e40ccd2475ffc51aaa44505bcaeed4d5ac2a921f3420c0d6c08c5d83da7058',
        'parts': [['Enrique Marshall Rivera', 500, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 239, 'SUJETO_ROL_NOMBRE']]},
 6396: {'hash': 'c5d80824a267dcc5cacbc83f7221ea5b3354aae961d03f3d5140f759db0e2f98',
        'parts': [['Sebastián Claro Edwards', 321, 'SUJETO_ROL_NOMBRE']]},
 6404: {'hash': '6f575c37e6558bcf0cbc61758acb34a8a5139b307d58e423805c23983de52a8d',
        'parts': [["Alberto Naudon Dell'Oro", 700, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 239, 'SUJETO_ROL_NOMBRE']]},
 6417: {'hash': '0c219f9053401e2bb8110b30918ccbfc2f7e47818088500100943ac27ea750fa',
        'parts': [['Sebastián Claro Edwards', 1004, 'SUJETO_ROL_NOMBRE']]},
 6491: {'hash': 'd436dcfa251f2d0bafe4e1dd45a29755c5c2ecaa28ec5014bdd0a57c394339ec',
        'parts': [["Alberto Naudon Dell'Oro", 502, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 239, 'SUJETO_ROL_NOMBRE']]},
 6530: {'hash': '563bd75f4a960704d95076f464c81bcf11b388e19b38a1e7019e46d5899cc2e0',
        'parts': [['Claudio Raddatz Kiefer', 883, 'CONTEXTO_REVISADO'],
                  ['Rodrigo Vergara Montes', 239, 'SUJETO_ROL_NOMBRE']]},
 6570: {'hash': '704f0a42aa997130620b899baaa246d0f443bd2eb01917eae6f0aead2fead39d',
        'parts': [['Joaquín Vial Ruiz-Tagle', 505, 'SUJETO_ROL_NOMBRE']]},
 6599: {'hash': '9509ea6bce01dcd8955ddfd9d40d5bf738ddcd23d5ee198b694df2fbdd228241',
        'parts': [['Rodrigo Vergara Montes', 161, 'SUJETO_ROL_NOMBRE']]},
 6607: {'hash': 'e37436bf247b8b247efede3083006048915bca183423e15aa2f4fb3c72b1a27d',
        'parts': [['Miguel Fuentes Díaz', 1696, 'SUJETO_NOMBRE'],
                  ['Joaquín Vial Ruiz-Tagle', 278, 'SUJETO_ROL_NOMBRE'],
                  ['Miguel Fuentes Díaz', 4103, 'SUJETO_NOMBRE']]},
 6663: {'hash': '73f177ba0a80d5e203c00552c57cd9582ab4d87d6fe32f6a1937515ac3324890',
        'parts': [['Rodrigo Vergara Montes', 238, 'SUJETO_ROL_NOMBRE']]},
 6701: {'hash': 'e1f22ccc0bff3d4e8636ecaefaaf0c8aec3626c5ab3ed7354cbad1f70356ad52',
        'parts': [['Sebastián Claro Edwards', 277, 'SUJETO_ROL_NOMBRE']]},
 6715: {'hash': 'd1ea037a7cf124f2be474e54b71dfb69e91190985a92218f249530085eaf5670',
        'parts': [["Alberto Naudon Dell'Oro", 1585, 'SUJETO_NOMBRE'],
                  ['Rodrigo Vergara Montes', 170, 'SUJETO_ROL_NOMBRE']]},
 6732: {'hash': '6d40c0aaa7b0ead0d7136a37946af7a176e9e7d465b2b3b4743612909b5ba886',
        'parts': [['Rodrigo Vergara Montes', 243, 'SUJETO_ROL_NOMBRE']]},
 6829: {'hash': '09edd0227cbe27e86a38eebc31bcf906d46030a92ff2e99d476bf6a59ca48c55',
        'parts': [['Diego Gianelli Gómez', 353, 'SUJETO_NOMBRE'],
                  ['Rodrigo Vergara Montes', 170, 'SUJETO_ROL_NOMBRE']]},
 6884: {'hash': 'e75d0d68e2b7bdd266de9d4b24c0b37a19d1c66bb2257d60f49094f0ca72cdb6',
        'parts': [("Alberto Naudon Dell'Oro", 2533, 'SUJETO_ROL_NOMBRE'),
                  ['Rodrigo Vergara Montes', 170, 'SUJETO_ROL_NOMBRE']]},
 6926: {'hash': '6eedffb37bf071487155a8394e8fae4da94ec5eb0788056eb83512bc45b17613',
        'parts': [["Alberto Naudon Dell'Oro", 1914, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 341, 'SUJETO_ROL_NOMBRE']]},
 6988: {'hash': '5a6f66419aa4bb8ecaa685d40ca8f15737498a227bdd0836e407f3d131e5f75e',
        'parts': [['Sebastián Claro Edwards', 654, 'SUJETO_ROL_NOMBRE']]},
 7003: {'hash': 'f2c909d3f32e6b968fe702565f2dc4cacef206a7cfb2cb50b18c4f510922c1cb',
        'parts': [['Rodrigo Alfaro', 211, 'SUJETO_ROL_NOMBRE'], ['Rodrigo Vergara Montes', 170, 'SUJETO_ROL_NOMBRE']]},
 7071: {'hash': '9acee9890ee2b9a1c7cf1640f7a958ca97c83fdd64b96f572c88fcff570983d6',
        'parts': [["Alberto Naudon Dell'Oro", 1689, 'SUJETO_NOMBRE'],
                  ['Rodrigo Vergara Montes', 170, 'SUJETO_ROL_NOMBRE']]},
 7125: {'hash': '98eb62b766027b19efad46b3c97600325cd6d4a9529cd0a7e0d899e1d3054893',
        'parts': [["Alberto Naudon Dell'Oro", 1655, 'SUJETO_NOMBRE'],
                  ['Rodrigo Vergara Montes', 127, 'SUJETO_ROL_NOMBRE']]},
 7179: {'hash': '4d798ca38f58d3cd625b68491e0219b965428df3166793bd9080221b037ad27f',
        'parts': [['Sebastián Claro Edwards', 926, 'SUJETO_ROL_NOMBRE'],
                  ['Mario Marcel Cullell', 361, 'SUJETO_ROL_NOMBRE'],
                  ['Rodrigo Vergara Montes', 170, 'SUJETO_ROL_NOMBRE']]}}

def fixture_test(p,e):
    def test(self):
        self.assertEqual(hashlib.sha256(self.raw[p]['Texto'].encode()).hexdigest(),e['hash'])
        parts=self.parts(p)
        # La segmentación devuelve None cuando sigue siendo necesaria la
        # atribución legada del constructor; no presentarla como sujeto resuelto.
        actual=[]
        for text,actor,method in parts:
            if method is None:
                detected=b.detect(text,self.raw[p]['Fecha'])
                self.assertIsNotNone(detected)
                actor,_,method,_=detected
            actual.append((actor,len(text),method))
        self.assertEqual(actual,[tuple(x) for x in e['parts']])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[p]['Texto'].split()))
    return test
for p,e in FIXTURES.items():setattr(LoopSevenTests,f'test_parent_{p}',fixture_test(p,e))

if __name__=='__main__':unittest.main()
