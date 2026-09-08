"""Cuatro ciclos: votaciones, cargos/retornos, cláusulas y concatenaciones.

Las fuentes fijadas por hash hacen fallar cambios posteriores no releídos.
No se infiere un actor nuevo de cualquier conector o mención de cargo.
"""
import hashlib
from pathlib import Path
import re
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews
from turns import normalize

CLARO = 'Sebastián Claro Edwards'
MARSHALL = 'Enrique Marshall Rivera'
MARFAN = 'Manuel Marfán Lewis'
SOTO = 'Claudio Soto Gamboa'
GARCIA = 'Pablo García Silva'
LEHMANN = 'Sergio Lehmann Beresi'
PRESIDENT = 'José De Gregorio Rebeco'
VELASCO = 'Andrés Velasco Brañes'
DESORMEAUX = 'Jorge Desormeaux Jiménez'
COWAN = 'Kevin Cowan Logan'
VOTES = (2883,3017,3073,3122,3273,3340,3428,3429,3488,3637)
OTHERS = (754,1335,1858,1923,2514,2555,2576,2583,2608,2624,2818,2838,2915,6564)


class LoopReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {r[0]: dict(Fecha=b.to_date_str(r[1]), Texto=r[5], Actor=r[2]) for r in b.data}
        cls.reviews = load_speaker_reviews(cls.raw)

    def parts(self, p):
        r = self.raw[p]
        return b.segment_turns(r['Texto'], r['Fecha'], r['Actor'], review=self.reviews.get(p))

    def test_missing_separator_does_not_swallow_magendzo_reply(self):
        parts = self.parts(754)
        self.assertEqual([a for t,a,m in parts], ['Vittorio Corbo Lioi',MARFAN,
                         'Igal Magendzo Weinberger',MARFAN,'Rodrigo Valdés Pulido'])
        self.assertTrue(parts[1][0].endswith('dinero como todo'))
        self.assertIn('M2 y del M3', parts[2][0])
        self.assertTrue(parts[3][0].startswith('Comenta el Consejero'))

    def test_lehmann_resumes_after_ocr_marker_then_president_returns(self):
        parts = self.parts(1858)
        self.assertEqual([a for t,a,m in parts], [PRESIDENT,LEHMANN,PRESIDENT,LEHMANN])
        self.assertTrue(parts[0][0].endswith('.LI I'))
        self.assertGreater(len(parts[1][0]), 1000)
        self.assertIn('Ante una consulta', parts[1][0])

    def test_president_final_vote_is_not_marfan_vote(self):
        parts = self.parts(2838)
        self.assertEqual([a for t,a,m in parts], [MARFAN,PRESIDENT])
        self.assertTrue(parts[0][0].endswith('política monetaria'))
        self.assertTrue(parts[1][0].startswith('Para finalizar con la votación'))
        self.assertIn('estímulo monetario actual', parts[1][0])

    def test_soto_salary_and_inflation_exposition_is_one_interval(self):
        parts = self.parts(2915)
        self.assertEqual([a for t,a,m in parts], [GARCIA,CLARO,GARCIA,SOTO])
        self.assertTrue(parts[2][0].endswith('público. i'))
        self.assertGreater(len(parts[3][0]), 1500)
        self.assertIn('Refiriéndose ahora al IPC', parts[3][0])

    def test_source_hashes_are_still_the_read_versions(self):
        for parent, digest in SOURCE_HASHES.items():
            with self.subTest(parent=parent):
                self.assertEqual(hashlib.sha256(self.raw[parent]['Texto'].encode()).hexdigest(), digest)

    def test_ten_vote_handoffs_keep_next_paragraph_speaker(self):
        for p in VOTES:
            with self.subTest(parent=p):
                parts = self.parts(p)
                expected = [MARSHALL, MARFAN] if p == 3429 else [CLARO, MARSHALL]
                self.assertEqual([a for t,a,m in parts], expected)
                self.assertTrue(parts[1][0].startswith('Prosiguiendo con la votación'))
                self.assertEqual(parts[1][2], 'SUJETO_ROL_NOMBRE')
                self.assertEqual(self.parts(p+1)[0][1], expected[1])

    def test_substantive_marshall_exposition_is_not_a_thanks_formula(self):
        from procedural import is_formula
        parts = self.parts(3340)
        self.assertGreater(len(parts[-1][0]), 2600)
        self.assertFalse(is_formula(parts[-1][0]))
        self.assertIn('economía mantendrá un ritmo de crecimiento vigoroso', parts[-1][0])

    def test_marfan_starts_after_marshall_vote(self):
        parts = self.parts(3429)
        self.assertIn('para dejarla en 2,5%', parts[0][0])
        self.assertNotIn('para dejarla en 2,5%', parts[1][0])
        self.assertIn('Vicepresidente señor Manuel Marfán', parts[1][0])

    def test_role_variants_recover_named_speakers_without_rewriting(self):
        self.assertEqual([a for t,a,m in self.parts(1335)],
                         ['Igal Magendzo Weinberger','Esteban Jadresic Marinovic',MARFAN,
                          'Igal Magendzo Weinberger','Rodrigo Valdés Pulido'])
        parts = self.parts(2514)
        self.assertEqual([a for t,a,m in parts], [GARCIA,COWAN])
        self.assertTrue(parts[1][0].startswith('El Gerente División Política Financiera'))
        self.assertIn('Gerente de Estudios', self.parts(1335)[-1][0])
        self.assertTrue(self.parts(1335)[-2][0].endswith('fi'))

    def test_soto_and_fuentes_return_to_long_presentations(self):
        parts = self.parts(2624)
        self.assertEqual([a for t,a,m in parts], [VELASCO,SOTO,PRESIDENT])
        self.assertGreater(len(parts[1][0]), 1600)
        self.assertIn('Respecto de los salarios', parts[1][0])
        parts = self.parts(6564)
        self.assertEqual([a for t,a,m in parts], ["Alberto Naudon Dell'Oro",'Miguel Fuentes Díaz'])
        self.assertGreater(len(parts[1][0]), 2800)
        self.assertIn('A título de conclusiones', parts[1][0])

    def test_marfan_marshall_distinction_and_late_soto_return(self):
        parts = self.parts(2818)
        self.assertEqual([a for t,a,m in parts],
                         [SOTO,MARFAN,MARSHALL,SOTO,MARSHALL,SOTO,MARSHALL,SOTO,PRESIDENT])
        self.assertTrue(parts[2][0].startswith('Esa moderación se refiere'))
        self.assertEqual(parts[2][2], 'CONTEXTO_REVISADO')
        self.assertTrue(parts[-2][0].startswith('Al continuar con su exposición'))
        self.assertGreater(len(parts[-2][0]), 4400)

    def test_four_reviewed_coordinations_keep_returns(self):
        expected = {
            1923:[PRESIDENT,VELASCO,LEHMANN,PRESIDENT,LEHMANN,PRESIDENT,GARCIA,LEHMANN],
            2555:[MARSHALL,MARFAN,DESORMEAUX,GARCIA,LEHMANN],
            2583:[PRESIDENT,SOTO,GARCIA,PRESIDENT,COWAN,SOTO],
            2608:[LEHMANN,VELASCO,LEHMANN,VELASCO,DESORMEAUX,LEHMANN],
        }
        for p, actors in expected.items():
            with self.subTest(parent=p):
                self.assertEqual([a for t,a,m in self.parts(p)], actors)
        self.assertGreater(len(self.parts(2608)[-1][0]), 2300)
        self.assertIn('En materia de inflación', self.parts(2608)[-1][0])

    def test_en_tanto_query_is_separate_and_cowan_stays_after_it(self):
        parts = self.parts(2576)
        self.assertEqual([a for t,a,m in parts], [MARFAN,PRESIDENT,COWAN])
        self.assertTrue(parts[1][0].startswith('en tanto el Presidente'))
        self.assertIn('encuesta', parts[2][0])

    def test_leads_do_not_license_mentions_without_speech(self):
        for lead in ['Prosiguiendo con la votación','Prosiguiendo con la presentación',
                     'Al continuar con su exposición','Al continuar con la exposición']:
            text = lead + ', el Consejero señor Enrique Marshall está presente.'
            self.assertIsNone(b.TURN_DETECTOR.speaker(text, '2010-01-14'))
        text = 'El Presidente señor Corbo señala: “Prosiguiendo con la votación, el Consejero señor Marfán agradece al staff”.'
        parts = b.segment_turns(text, '2005-02-10', 'Vittorio Corbo Lioi')
        self.assertEqual([a for t,a,m in parts], ['Vittorio Corbo Lioi'])

    def test_role_mentions_and_handoffs_are_not_recipient_turns(self):
        self.assertEqual([a for t,a,m in self.parts(1037)], [VELASCO])
        self.assertEqual([a for t,a,m in self.parts(1338)],
                         ['Vittorio Corbo Lioi', b.CONSEJO, 'Esteban Jadresic Marinovic', 'Vittorio Corbo Lioi'])
        text = 'Prosiguiendo con la votación, el Presidente señor Corbo ofrece la palabra al Consejero señor Marfán.'
        self.assertEqual(b.TURN_DETECTOR.speaker(text, '2005-02-10')['actor'], 'Vittorio Corbo Lioi')
        for text in ['Gerente de Estudios', 'Gerente División Política Financiera']:
            self.assertEqual(normalize(normalize(text)), normalize(text))
        self.assertEqual(normalize('gerente de estudios de mercado'), 'gerente de estudios de mercado')

    def test_all_twenty_four_parents_preserve_all_characters_except_whitespace(self):
        compact = lambda t: re.sub(r'\s+', '', t)
        for p in VOTES + OTHERS:
            with self.subTest(parent=p):
                self.assertEqual(compact(''.join(t for t,a,m in self.parts(p))),
                                 compact(self.raw[p]['Texto']))


# SHA-256 fijados tras la lectura dirigida; no calcular expectativas al ejecutar el test.
SOURCE_HASHES = {
    754: 'b7c4a87739ebd1dfe19eb41114f3b9e8cfd6a369d9df1f0aea88bbb9d647ed15',
    1858: 'c668fe3a84ffbe1c49fdaa321f2e8245900792d6bcb7598bb38f5c701d31ca03',
    2838: '7334060401fd9477090cc4a154e523e3ef13244b82d218474a25306067f72057',
    2915: '2846284cf82661bf08549e333c70548724dabb87369bcf60f50731b81ac8b63f',
    1335: '91a5d6f8e99116c167be930a64678a9a4cff64d9064dceb53b76db4aaa4cc9c7',
    1923: '43bc8834429e7dd1c19c068121fef592958a11556fefa8518eaa78d6c5a615c0',
    2514: 'de6365639352e8f20e9a47f6bd42c1ecdb1554bf6ddce0a3d348144ad7677842',
    2555: '87f91292fa7a7a4e9c3b127208f35fc4f40ffd63501d876480ebe9fcd5f099c7',
    2576: 'f67e13fe2661a51169488c061e3e559f72aa33aeeab04a5dd9286e589006453e',
    2583: '105634b0b84cf0d7ba5bc9c6bb568cb655251f608fbd0f799fba7e5e16bbb0df',
    2608: '9be87c4bedff1acd74d3960aa69b54e1f9c5099b04d017c829b72ebcc03f9cd3',
    2624: '68b0e2fd9ba820095d05d97e01d443a03192ba6f72b201723023239c40be1f63',
    2818: '828325324617efc79af0035732c4aad81e99c35c4e35243c97243953ff4a81fe',
    2883: '586cef63fdda1d7049911eba8d6195d7cddb19aacb3f02d0c59eb51c6d2c25a9',
    3017: 'd54a31350aea59c7c2add7a1e24dfdf0fca701f97e9f62597e5abe3ab50c5ebd',
    3073: 'e6d9f4b914fd4d565132055016de41e3dab024825bbc77279339ac9b2c21e5b0',
    3122: 'b12d09394db43d2fc01edf0ce20a4616c73b3a2f653d387354719d57158060e5',
    3273: 'f54c9cb0430f042dd34818cc007fef5f33ade99858d7821826e2aa66dff6b0db',
    3340: '91ef4f79ce4cd49e2cd5dde464676e1a9abb978bab6a39915baadf0133e93a3c',
    3428: '9da9a4b3802c84cb37c69dde8ffdfe074a100190d15f89fc4bc5ef2af9de7d83',
    3429: '0a54b53086970e44421f109c95ce7ba46b9661f481944ad87e5358c914843897',
    3488: '0370e5078bb80b774cdb5a2ab8ec8acf5c146dad71d66e23cbd7f052b53a4c45',
    3637: '6ec06aca470f159930e45cc96e844ee663ebf675b164042a6a0f577e1a2f34c7',
    6564: '3245c4c1a11ca8aa29e0933d6dba4093d875a13d0ad81722563995eddd47dbcd',
}

if __name__ == '__main__':
    unittest.main()
