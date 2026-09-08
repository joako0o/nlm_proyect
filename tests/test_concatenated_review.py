"""Cambios explícitos sin puntuación: sólo con revisión anclada, no regla global."""
import copy
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, SPEAKER_REVIEWS


class ConcatenatedReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {r[0]: dict(Fecha=b.to_date_str(r[1]), Texto=r[5], Actor=r[2]) for r in b.data}
        cls.reviews = load_speaker_reviews(cls.raw)

    def parts(self, p, review=None, text=None):
        r = self.raw[p]
        return b.segment_turns(text if text is not None else r['Texto'], r['Fecha'], r['Actor'],
                               review=review if review is not None else self.reviews[p])

    def test_exact_registered_concatenated_parents(self):
        self.assertEqual({p for p, r in self.reviews.items()
                          if r.get('Tipo_Limite') == 'CONCATENACION_EXPLICITA_REVISADA'},
                         {514, 644, 653, 664, 754, 1010, 1623, 1652, 1858, 2667, 2838, 2915, 3887, 5286, 5360, 5367})

    def test_attribution_sequences_and_full_source_conservation(self):
        expected = {
            514: ['Vittorio Corbo Lioi', 'Beltrán de Ramón Acevedo'],
            653: ['Jorge Desormeaux Jiménez', 'José De Gregorio Rebeco'],
            1010: ['Manuel Marfán Lewis', 'Igal Magendzo Weinberger', 'Rodrigo Valdés Pulido',
                   'Manuel Marfán Lewis', 'José De Gregorio Rebeco'],
            1623: ['Jorge Desormeaux Jiménez', 'Igal Magendzo Weinberger'],
            1652: ['José De Gregorio Rebeco', 'Manuel Marfán Lewis', 'Pablo García Silva',
                   'Manuel Marfán Lewis', 'Beltrán de Ramón Acevedo', 'Manuel Marfán Lewis',
                   'Beltrán de Ramón Acevedo'],
        }
        compact = lambda t: re.sub(r'\s+', '', t)
        for p, actors in expected.items():
            with self.subTest(parent=p):
                parts = self.parts(p)
                self.assertEqual([a for t, a, m in parts], actors)
                self.assertEqual(compact(''.join(t for t, a, m in parts)), compact(self.raw[p]['Texto']))

    def test_magendzo_long_presentation_and_source_digit_survive(self):
        parts = self.parts(1623)
        self.assertTrue(parts[0][0].endswith('7'))
        self.assertGreater(len(parts[1][0]), 11000)
        self.assertIn('Por otra parte, menciona el señor Magendzo', parts[1][0])
        self.assertTrue(parts[1][0].endswith('o incluso vuelvan a aumentar.'))

    def test_vicepresident_continues_to_his_vote_without_completing_desormeaux(self):
        parts = self.parts(653)
        self.assertTrue(parts[0][0].endswith('dado que el'))
        self.assertIn('Sin embargo, indica el señor Vicepresidente', parts[1][0])
        self.assertTrue(parts[1][0].endswith('vota en ese sentido.'))

    def test_unreviewed_concatenation_remains_unsplit(self):
        r = self.raw[514]
        self.assertEqual(len(b.segment_turns(r['Texto'], r['Fecha'], r['Actor'])), 1)

    def test_incompatible_actor_is_rejected(self):
        review = copy.deepcopy(self.reviews[514])
        review['Actor'] = 'Manuel Marfán Lewis'
        with self.assertRaisesRegex(ValueError, 'límite válido'):
            self.parts(514, review)

    def test_inside_quotation_is_rejected(self):
        for opening, closing in [('“', '”'), ('«', '»'), ('"', '"')]:
            with self.subTest(quote=opening):
                review = copy.deepcopy(self.reviews[514])
                review['Inicio'] += 1
                review['Fin'] += 1
                with self.assertRaisesRegex(ValueError, 'límite válido'):
                    self.parts(514, review, opening + self.raw[514]['Texto'] + closing)

    def test_no_whitespace_boundary_is_rejected(self):
        review = copy.deepcopy(self.reviews[514])
        start = review['Inicio']
        text = self.raw[514]['Texto'][:start-1] + self.raw[514]['Texto'][start:]
        review['Inicio'] -= 1
        review['Fin'] -= 1
        with self.assertRaisesRegex(ValueError, 'límite válido'):
            self.parts(514, review, text)

    def test_mention_without_speech_is_rejected_even_with_review(self):
        text = 'El Presidente señor Corbo saluda El Consejero señor Marfán está presente.'
        review = dict(Inicio=text.index('El Consejero'), Fin=len(text), Actor='Manuel Marfán Lewis',
                      Tipo_Limite='CONCATENACION_EXPLICITA_REVISADA')
        with self.assertRaisesRegex(ValueError, 'límite válido'):
            b.segment_turns(text, '2005-02-10', 'Vittorio Corbo Lioi', review=review)

    def test_source_change_invalidates_concatenation_review(self):
        entries = [e for e in json.loads(SPEAKER_REVIEWS.read_text()) if e['ID_Padre'] == 514]
        raw = copy.deepcopy(self.raw)
        raw[514]['Texto'] += ' Texto distinto.'
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'reviews.json'
            path.write_text(json.dumps(entries))
            with self.assertRaisesRegex(ValueError, 'cambió el texto de origen'):
                load_speaker_reviews(raw, path)


if __name__ == '__main__':
    unittest.main()
