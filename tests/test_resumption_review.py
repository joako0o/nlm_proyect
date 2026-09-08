"""Suspensión, expositor mencionado y retornos con variantes de cargo."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews
from turns import normalize

CORBO = 'Vittorio Corbo Lioi'
VALDES = 'Rodrigo Valdés Pulido'
VELASCO = 'Andrés Velasco Brañes'
MARFAN = 'Manuel Marfán Lewis'
SCHMIDT = 'Klaus Schmidt-Hebbel Dunker'
SOTO = 'Claudio Soto Gamboa'
GARCIA = 'Pablo García Silva'


class ResumptionReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {r[0]: dict(Fecha=b.to_date_str(r[1]), Texto=r[5], Actor=r[2]) for r in b.data}
        cls.reviews = load_speaker_reviews(cls.raw)

    def parts(self, parent):
        r = self.raw[parent]
        return b.segment_turns(r['Texto'], r['Fecha'], r['Actor'], review=self.reviews.get(parent))

    def test_may_suspension_presentation_and_chair_return(self):
        parts = self.parts(664)
        self.assertEqual([a for t, a, m in parts],
                         [CORBO, VELASCO, CORBO, b.CONSEJO, CORBO, VALDES, CORBO])
        self.assertTrue(parts[1][0].endswith('no solamente la'))
        self.assertIn('13:20', parts[2][0])
        self.assertIn('16:00', parts[3][0])
        self.assertGreater(len(parts[5][0]), 8300)
        self.assertTrue(parts[5][0].endswith('precios financieros.'))
        self.assertIn('ofrece la palabra', parts[-1][0])

    def test_velasco_has_his_own_predicate_without_later_suspension(self):
        text = self.raw[664]['Texto']
        text = text[text.index('Finalmente,'):text.index('El Presidente, señor Vittorio Corbo, suspende')]
        candidate = b.TURN_DETECTOR.speaker(text, self.raw[664]['Fecha'])
        self.assertEqual(candidate['actor'], VELASCO)

    def test_april_presentation_then_question_and_replies(self):
        parts = self.parts(644)
        self.assertEqual([a for t, a, m in parts],
                         [CORBO, b.CONSEJO, CORBO, VALDES, CORBO, SCHMIDT,
                          MARFAN, SCHMIDT, MARFAN, SCHMIDT, MARFAN, SCHMIDT])
        self.assertGreater(len(parts[3][0]), 3700)
        self.assertTrue(parts[5][0].endswith('Ello'))
        self.assertTrue(parts[6][0].startswith('Consulta el Consejero señor Marfán'))
        self.assertTrue(parts[7][0].startswith('El señor Schmidt-Hebbel, responde'))

    def test_june_introduction_and_next_parent_keep_valdes(self):
        parts = self.parts(727)
        self.assertEqual([a for t, a, m in parts], [CORBO, b.CONSEJO, CORBO, VALDES])
        self.assertTrue(parts[-1][0].endswith('informó lo siguiente:'))
        following = self.parts(728)
        self.assertEqual([a for t, a, m in following], [VALDES])
        self.assertGreater(len(following[0][0]), 9500)

    def test_july_advance_of_presentation_does_not_fragment_it(self):
        parts = self.parts(770)
        self.assertEqual([a for t, a, m in parts], [CORBO, b.CONSEJO, CORBO, VALDES])
        self.assertTrue(parts[-1][0].startswith('El señor Gerente de División mencionado informó'))
        self.assertIn('Señala el señor Gerente de División Estudios', parts[-1][0])
        self.assertGreater(len(parts[-1][0]), 7600)
        self.assertTrue(parts[-1][0].endswith('comentarios.'))

    def test_cowan_name_does_not_rewrite_damaged_role_or_assign_reference(self):
        parts = self.parts(1904)
        self.assertEqual([a for t, a, m in parts], ['Beltrán de Ramón Acevedo', 'Kevin Cowan Logan'])
        self.assertTrue(parts[0][0].endswith('■J'))
        self.assertIn('Política l\\/lonetaria', parts[1][0])
        self.assertIn('mencionaba el señor Gerente de División Operaciones Financieras', parts[1][0])
        self.assertEqual(b.roster_role_for(self.raw[1904]['Fecha'], parts[1][1]),
                         'Gerente de División Política Financiera')

    def test_soto_not_lehmann_gets_national_presentation(self):
        parts = self.parts(2460)
        self.assertEqual([a for t, a, m in parts], ['José De Gregorio Rebeco', SOTO, GARCIA])
        self.assertIn('Sergio Lehmann', parts[0][0])
        self.assertIn('IMACEC', parts[1][0])

    def test_both_soto_returns_include_following_exposition(self):
        parts = self.parts(2462)
        self.assertEqual([a for t, a, m in parts],
                         [VELASCO, SOTO, VELASCO, GARCIA, SOTO, GARCIA,
                          VELASCO, GARCIA, SOTO, VELASCO, MARFAN, VELASCO])
        self.assertTrue(parts[4][0].startswith('El Gerente Análisis Macroeconómico señor Claudio Soto señala'))
        self.assertIn('Continuando con su exposición', parts[4][0])
        self.assertTrue(parts[8][0].startswith('El Gerente Análisis Macroeconómico señor Claudio Soto explica'))
        self.assertIn('venta de viviendas', parts[8][0])
        self.assertIn('Ante la solicitud del señor Ministro', parts[8][0])

    def test_role_view_normalization_is_bounded_and_idempotent(self):
        text = 'El Gerente Análisis Macroeconómico señor Claudio Soto explica la actividad.'
        self.assertEqual(normalize(text), normalize(text.replace('Gerente Análisis', 'Gerente de Análisis')))
        self.assertEqual(normalize(normalize(text)), normalize(text))
        self.assertEqual(normalize('análisis macroeconómico'), 'analisis macroeconomico')
        self.assertEqual(normalize('Gerente Análisis Internacional'), 'gerente analisis internacional')

    def test_reported_information_is_not_a_turn(self):
        for text in [
            'El Presidente señor Corbo señala que el Ministro señor Andrés Velasco le informó del dato.',
            'Como informó el señor Rodrigo Valdés, las cifras subieron.',
            'La información del señor Rodrigo Valdés parece suficiente.',
            'El Presidente señor Corbo agradece al Gerente Análisis Macroeconómico señor Claudio Soto su presentación.',
        ]:
            with self.subTest(text=text):
                candidate = b.TURN_DETECTOR.speaker(text, '2006-05-11')
                self.assertTrue(candidate is None or candidate['actor'] == CORBO)

    def test_same_role_mentioned_with_speech_resolves_named_recipient(self):
        previous = 'El Presidente señor Corbo solicita al Gerente de División Estudios, don Rodrigo Valdés, que presente las opciones.'
        text = 'El señor Gerente de División mencionado informó lo siguiente:'
        context = b.TURN_DETECTOR.referents(previous, '2006-05-11')
        candidate = b.TURN_DETECTOR.speaker(text, '2006-05-11', CORBO, context)
        self.assertEqual(candidate['actor'], VALDES)
        self.assertEqual(candidate['method'], 'ANAFORA_LOCAL')

    def test_all_affected_parents_conserve_source_characters(self):
        compact = lambda t: re.sub(r'\s+', '', t)
        for p in [644, 664, 727, 770, 1904, 2460, 2462]:
            with self.subTest(parent=p):
                self.assertEqual(compact(''.join(t for t, a, m in self.parts(p))),
                                 compact(self.raw[p]['Texto']))


if __name__ == '__main__':
    unittest.main()
