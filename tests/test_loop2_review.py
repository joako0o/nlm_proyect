"""Segundo bloque de ciclos: prefijos, referencias y respuestas documentadas."""
import copy
import hashlib
import re
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews
from turns import normalize

PRES = 'José De Gregorio Rebeco'
GARCIA = 'Pablo García Silva'
SOTO = 'Claudio Soto Gamboa'
MARSHALL = 'Enrique Marshall Rivera'
MARFAN = 'Manuel Marfán Lewis'
DESORMEAUX = 'Jorge Desormeaux Jiménez'
VELASCO = 'Andrés Velasco Brañes'
LEHMANN = 'Sergio Lehmann Beresi'
DERAMON = 'Beltrán de Ramón Acevedo'
MAGENDZO = 'Igal Magendzo Weinberger'
PARENTS = (298,753,1718,1873,1946,2167,2206,2408,2588,2678,2681,2814,2896,2910,2981,2983,3007,3147)


class LoopTwoReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {r[0]: dict(Fecha=b.to_date_str(r[1]), Texto=r[5], Actor=r[2]) for r in b.data}
        cls.reviews = load_speaker_reviews(cls.raw)

    def parts(self, p, review=None):
        r = self.raw[p]
        return b.segment_turns(r['Texto'], r['Fecha'], r['Actor'],
                               review=self.reviews.get(p) if review is None else review)

    def test_read_sources_still_have_fixed_hashes(self):
        self.assertEqual(set(SOURCE_HASHES), set(PARENTS))
        for p, digest in SOURCE_HASHES.items():
            self.assertEqual(hashlib.sha256(self.raw[p]['Texto'].encode()).hexdigest(), digest)

    def test_all_affected_parents_preserve_source_characters(self):
        compact = lambda s: re.sub(r'\s+', '', s)
        for p in PARENTS:
            with self.subTest(parent=p):
                self.assertEqual(compact(''.join(t for t,a,m in self.parts(p))), compact(self.raw[p]['Texto']))

    def test_first_cycle_questions_and_chair_handoff(self):
        for p, expected in [(298,['Esteban Jadresic Marinovic','Nicolás Eyzaguirre Guzmán']),
                            (2167,[MARSHALL,PRES,VELASCO]),
                            (2408,[DESORMEAUX,SOTO,DERAMON,SOTO])]:
            self.assertEqual([a for t,a,m in self.parts(p)], expected)
        self.assertIn('8,25%', self.parts(2167)[0][0])
        self.assertNotIn('8,25%', self.parts(2167)[1][0])

    def test_normalization_of_thematic_phrase_does_not_rewrite_source(self):
        text = 'En lo que dice relación con los mercados financieros'
        self.assertEqual(normalize(text), 'respecto a los mercados financieros')
        self.assertEqual(normalize(normalize(text)), normalize(text))
        self.assertIn(text, self.parts(298)[1][0])
        self.assertEqual(normalize('lo que dice el Ministro'), 'lo que dice el ministro')

    def test_claro_asks_about_soto_exposition_then_soto_answers(self):
        parts = self.parts(1946)
        self.assertEqual([a for t,a,m in parts], [GARCIA,VELASCO,'Sebastián Claro Edwards',SOTO,MARFAN])
        self.assertTrue(parts[2][0].startswith('En relación al comentario del expositor'))
        self.assertIn('Claudio Soto', parts[2][0])
        self.assertTrue(parts[3][0].startswith('El Gerente señor Soto señala'))

    def test_marshall_comment_and_president_question_not_expositor_turns(self):
        parts = self.parts(1873)
        self.assertEqual([a for t,a,m in parts], [PRES,MARSHALL,PRES,GARCIA])
        self.assertEqual(parts[1][2], 'CONTEXTO_REVISADO')
        self.assertTrue(parts[2][0].startswith('En cuanto al comentario del expositor'))
        self.assertNotIn(SOTO, [a for t,a,m in parts])

    def test_delivered_data_is_reference_not_questioner(self):
        parts = self.parts(2206)
        self.assertEqual([a for t,a,m in parts], [SOTO,DESORMEAUX,SOTO])
        self.assertGreater(len(parts[0][0]), 6000)
        self.assertIn('datos que ha entregado el señor Claudio Soto', parts[1][0])

    def test_nested_reference_still_allows_real_outer_subject(self):
        text = 'El Consejero señor Marfán, en relación a lo comentado por el señor Soto, consulta por la inflación.'
        candidate = b.TURN_DETECTOR.speaker(text, '2009-06-16')
        self.assertEqual(candidate['actor'], MARFAN)
        text = 'En relación al comentario del expositor señor Claudio Soto, el Consejero señor Sebastián Claro consulta por la inflación.'
        self.assertEqual(b.TURN_DETECTOR.speaker(text, '2009-06-16')['actor'], 'Sebastián Claro Edwards')

    def test_magendzo_presentation_is_one_long_interval(self):
        parts = self.parts(753)
        self.assertEqual([a for t,a,m in parts], ['Vittorio Corbo Lioi',MAGENDZO])
        self.assertGreater(len(parts[1][0]), 7100)
        self.assertTrue(parts[1][0].startswith('Los mercados financieros nacionales'))
        self.assertIn('En cuanto a la expansividad', parts[1][0])
        self.assertTrue(parts[1][0].endswith('de los contemplados.'))

    def test_en_tanto_explanations_and_lehmann_return(self):
        expected = {2896:['Rodrigo Vergara Montes',LEHMANN,GARCIA,LEHMANN],
                    2910:[PRES,SOTO,GARCIA], 2983:[SOTO,GARCIA]}
        for p, actors in expected.items():
            self.assertEqual([a for t,a,m in self.parts(p)], actors)
        self.assertGreater(len(self.parts(2896)[-1][0]), 1200)
        self.assertIn('En cuanto a actividad', self.parts(2896)[-1][0])

    def test_reviewed_response_without_comma_preserves_connector_and_returns(self):
        parts = self.parts(1718)
        self.assertEqual(len(parts), 15)
        self.assertEqual([a for t,a,m in parts[9:12]], [MARSHALL,MARFAN,VELASCO])
        self.assertTrue(parts[9][0].endswith('Dirección del Trabajo'))
        self.assertTrue(parts[10][0].startswith('a lo que el Consejero Marfán agrega'))
        self.assertEqual({p for p,r in self.reviews.items() if r.get('Tipo_Limite')=='RESPUESTA_A_LO_QUE_EXPLICITA'}, {1718})
        self.assertIn('como dice el señor Cowan', parts[4][0])
        self.assertEqual(parts[4][1], MAGENDZO)

    def test_unreviewed_response_is_not_globally_split(self):
        r = self.raw[1718]
        parts = b.segment_turns(r['Texto'], r['Fecha'], r['Actor'])
        self.assertEqual(len(parts), 14)
        self.assertIn('a lo que el Consejero Marfán agrega', parts[9][0])

    def test_response_wrong_actor_is_rejected(self):
        review = copy.deepcopy(self.reviews[1718]);review['Actor'] = PRES
        with self.assertRaisesRegex(ValueError, 'límite válido'):
            self.parts(1718, review)

    def test_response_inside_quotes_is_rejected(self):
        r = self.raw[1718]
        for left,right in [('“','”'),('«','»'),('"','"')]:
            review = copy.deepcopy(self.reviews[1718]);review['Inicio']+=1;review['Fin']+=1
            with self.assertRaisesRegex(ValueError, 'límite válido'):
                b.segment_turns(left+r['Texto']+right,r['Fecha'],r['Actor'],review=review)

    def test_response_requires_exact_connector_and_whitespace(self):
        r = self.raw[1718];review = copy.deepcopy(self.reviews[1718]);start=review['Inicio']
        for text in [r['Texto'][:start]+'a lo cual'+r['Texto'][start+8:],
                     r['Texto'][:start-1]+'x'+r['Texto'][start:]]:
            with self.assertRaisesRegex(ValueError, 'límite válido'):
                b.segment_turns(text,r['Fecha'],r['Actor'],review=review)

    def test_response_without_finite_speech_is_rejected(self):
        text = 'El Presidente señor Corbo señala el dato a lo que el Consejero señor Marfán presta atención.'
        review = dict(Actor=MARFAN,Inicio=text.index('a lo que'),Fin=len(text),Tipo_Limite='RESPUESTA_A_LO_QUE_EXPLICITA')
        with self.assertRaisesRegex(ValueError, 'límite válido'):
            b.segment_turns(text,'2005-02-10','Vittorio Corbo Lioi',review=review)

    def test_completed_presentation_stays_separate_from_chair_handoff(self):
        for p, expected in [(2588,['Sebastián Claro Edwards',SOTO,PRES]),
                            (2678,[GARCIA,DESORMEAUX]), (2681,[GARCIA,PRES]),
                            (2814,['Sebastián Claro Edwards',PRES,SOTO]),
                            (3147,[PRES,DERAMON,PRES])]:
            self.assertEqual([a for t,a,m in self.parts(p)], expected)
        self.assertGreater(len(self.parts(2681)[0][0]), 11000)
        self.assertIn('coméntanos', self.parts(2814)[1][0])
        self.assertEqual(self.parts(2589)[0][1], 'Kevin Cowan Logan')
        self.assertEqual(self.parts(2815)[0][1], SOTO)

    def test_inflation_return_preserves_soto_long_development(self):
        parts = self.parts(2981)
        self.assertEqual(parts[2][1], GARCIA)
        self.assertEqual(parts[3][1], SOTO)
        self.assertTrue(parts[3][0].startswith('Refiriéndose ahora a la inflación'))
        self.assertGreater(len(parts[3][0]), 3200)
        self.assertIn('En cuanto al escenario post terremoto', parts[3][0])
        # La respuesta posterior con gerundio tiene su regresión en test_residual_review.

    def test_marfan_suggestion_does_not_absorb_garcia_reply(self):
        parts = self.parts(3007)
        self.assertEqual([a for t,a,m in parts], [MARFAN,GARCIA,MARFAN,GARCIA])
        self.assertTrue(parts[2][0].startswith('Por último, el señor Vicepresidente sugiere'))
        self.assertTrue(parts[3][0].endswith('No habiendo más comentarios,.'))

    def test_new_leads_do_not_create_subjects_without_speech(self):
        for lead in ['Antes de proseguir','Finalizada la presentación','Concluida la presentación',
                     'No habiendo más comentarios','Refiriéndose ahora a la inflación',
                     'Complementando los comentarios efectuados']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(lead+', el señor Claudio Soto está presente.','2009-06-16'))
        text = 'El Presidente señor José De Gregorio indica: “Finalizada la presentación, el señor Claudio Soto señala el resultado”.'
        self.assertEqual([a for t,a,m in b.segment_turns(text,'2009-06-16',PRES)], [PRES])


SOURCE_HASHES = {
    298: '54df4164b45cdc505bf5190ddbc29934296d1570f42f8111ca3452a85a9c44fb',
    753: '134a1c4db0c47848dd7f6d71c335ea61bfaca73163aec04e68344a48cb29fae7',
    1718: '04c5c08361b0f0aad7e36344d87ea824e9d958c8dd5968a02df2d59df9a08414',
    1873: '67c7dbe426ded0d8a2363ef725c24db9ba222f34ccd53031e5a1a8e8778f4382',
    1946: '6e91f08f9c5f4d29fa452912e9bd60f73183a2dcdc5e14018d919bc57e17adf0',
    2167: '10ffe024136b613fd598d95b9ba354dd58fb564f98a7f1e470e45a01ab0aa4b9',
    2206: '0e3701a343a69b37bca7f15e6fc5e6e5ef78b99e64c9ba3b156acae404e1f411',
    2408: 'bcbbbeca35ea9f58e2ee2bee5ba89b071c4b170a774c5d4ea6dc6769eb39062f',
    2588: '308fcd93e412425c734009f703e20ae3342a274ae895499e715edd0db75c2b56',
    2678: '100d2bc8807cacb4f2fb5607e067d8aa204c2130422d2160bc1735bcd8a997f4',
    2681: 'fa73f79441ebbcdca6a45eb115f3036316c8430d796c3a0d10431628bd4076c9',
    2814: '380a77040ce70f311c2744e5784ecbf914362f85e5790048fd1d720105ce1d0f',
    2896: '5c291d2bd39d4ad3592f3af1d10fb50b339e89b490b62d2144677f9ccb499fea',
    2910: 'f0dc602ee9987ce7b0994b174cfe5424517ee74f66523b466f917475f06b8bf2',
    2981: 'a786b1a89d62184cd923e9ac5c70552d8e5cc4077caf17ea0e5f6f8a0c686f36',
    2983: '97896e4b05b1681642d27c1d16210ccf1efc1ea39c8ca90eb5799adfb2aa744a',
    3007: 'e0908bbc45f2d390a1dbb57075ebed230b41d7d106b50c38988e2890d139394f',
    3147: '89cda9f19ba68255595049376f5a771810604217912df600004dd509e382e5f4',
}

if __name__ == '__main__':
    unittest.main()
