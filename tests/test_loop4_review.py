"""Votos, complementos y retornos: conservar exposiciones y daños de origen."""
import copy
import hashlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, validate_speaker_reviews, SPEAKER_REVIEWS

PRES = 'José De Gregorio Rebeco'
MARSHALL = 'Enrique Marshall Rivera'
CLARO = 'Sebastián Claro Edwards'
MARFAN = 'Manuel Marfán Lewis'
SOTO = 'Claudio Soto Gamboa'
LEHMANN = 'Sergio Lehmann Beresi'
HERRERA = 'Luis Óscar Herrera Barriga'
COWAN = 'Kevin Cowan Logan'

class LoopFourTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {r[0]: dict(Fecha=b.to_date_str(r[1]), Texto=r[5], Actor=r[2]) for r in b.data}
        cls.reviews = load_speaker_reviews(cls.raw)

    def parts(self, p):
        r = self.raw[p]
        return b.segment_turns(r['Texto'], r['Fecha'], r['Actor'], review=self.reviews.get(p))

    def test_read_source_hashes(self):
        for p, digest in SOURCE_HASHES.items():
            self.assertEqual(hashlib.sha256(self.raw[p]['Texto'].encode()).hexdigest(), digest)

    def test_conservation(self):
        compact = lambda t: re.sub(r'\s+', '', t)
        for p in SOURCE_HASHES:
            self.assertEqual(compact(''.join(t for t, a, m in self.parts(p))), compact(self.raw[p]['Texto']))

    def test_3800_vicepresident_warning_is_not_soto_reply(self):
        parts = self.parts(3800)
        self.assertEqual([a for t, a, m in parts], [SOTO, MARFAN])
        self.assertEqual([len(t) for t, a, m in parts], [141, 710])
        self.assertIn('Indica que si bien esta encuesta', parts[1][0])
        self.assertTrue(parts[1][0].endswith('si fuera el caso.'))

    def test_3810_claro_vote_before_marshall_thanks(self):
        parts = self.parts(3810)
        self.assertEqual([a for t, a, m in parts], [CLARO, MARSHALL])
        self.assertTrue(parts[0][0].endswith('por una alza de la TPM en 25 puntos base.'))
        self.assertTrue(parts[1][0].startswith('Al continuarse con la votación'))
        self.assertIn('staff e\\ apoyo', parts[1][0])
        self.assertEqual(parts[1][2], 'SUJETO_ROL_NOMBRE')
        self.assertNotIn(3810, self.reviews)

    def test_3813_president_full_vote_and_institutional_agreement(self):
        parts = self.parts(3813)
        self.assertEqual([a for t, a, m in parts], [MARFAN, PRES, b.CONSEJO])
        self.assertTrue(parts[0][0].endswith('en esta oportunidad.'))
        self.assertTrue(parts[1][0].startswith('Al concluir con la votación'))
        self.assertIn('En Chile, subraya', parts[1][0])
        self.assertIn('ios próximos meses', parts[1][0])
        self.assertTrue(parts[1][0].endswith('hasta 3,5% anual.'))
        self.assertTrue(parts[2][0].startswith('En virtud de lo anterior, el Consejo adoptó'))

    def test_marshall_and_marfan_multiparagraph_votes(self):
        from test_continuity import sequence
        for left, right, actor in [(3810, 3811, MARSHALL), (3812, 3813, MARFAN)]:
            rows = sequence([(p, self.raw[p]['Fecha'], self.raw[p]['Actor'], self.raw[p]['Texto'])
                             for p in [left, right]])
            before = [r for r in rows if r['ID_Padre'] == left][-1]
            after = next(r for r in rows if r['ID_Padre'] == right)
            self.assertEqual(before['Actor_Final'], actor)
            self.assertEqual(before['ID_Turno'], after['ID_Turno'])

    def test_vote_leads_require_uncited_speech_subject(self):
        for lead in ['Al continuarse con la votación', 'Al concluir con la votación']:
            for text in [lead + ', según el señor Presidente, la cifra cambia.',
                         lead + ', el señor Presidente está presente.',
                         '“' + lead + ', el señor Presidente señala que la cifra cambia.”']:
                self.assertIsNone(b.TURN_DETECTOR.speaker(text, '2011-02-17'))

    def test_3887_damaged_vote_not_reconstructed_and_marshall_exposition_whole(self):
        parts = self.parts(3887)
        self.assertEqual([a for t, a, m in parts], [CLARO, MARSHALL])
        self.assertEqual([len(t) for t, a, m in parts], [5698, 2667])
        self.assertIn('a 4%. En consecuencia', parts[0][0])
        self.assertTrue(parts[0][0].endswith('vota por aumentar la tasa'))
        self.assertIn('staff e\\ apoyo', parts[1][0])
        self.assertIn('En el frente interno, menciona', parts[1][0])
        self.assertTrue(parts[1][0].endswith('no pueden pasar desapercibidas.'))

    def test_3906_two_different_growth_assessments(self):
        parts = self.parts(3906)
        self.assertEqual([a for t, a, m in parts], [PRES, CLARO])
        self.assertEqual([len(t) for t, a, m in parts], [135, 122])
        self.assertIn('mayor crecimiento', parts[0][0])
        self.assertIn('menor crecimiento', parts[1][0])

    def test_4220_three_speakers_not_all_president(self):
        parts = self.parts(4220)
        self.assertEqual([a for t, a, m in parts], [PRES, LEHMANN, HERRERA])
        self.assertEqual([len(t) for t, a, m in parts], [120, 52, 177])
        self.assertEqual(parts[1][0], 'El señor Lehmann se compromete a revisar el gráfico,')

    def test_inner_boundaries_need_review_not_global_comma_or_capital_rules(self):
        for p, count in [(3887, 1), (3906, 1), (4220, 2)]:
            r = self.raw[p]
            self.assertEqual(len(b.segment_turns(r['Texto'], r['Fecha'], r['Actor'])), count)

    def test_inner_boundaries_reject_wrong_actor_and_quotes(self):
        for p in [3887, 3906, 4220, 4341]:
            r = self.raw[p]
            review = copy.deepcopy(self.reviews[p]); review['Actor'] = SOTO
            with self.assertRaisesRegex(ValueError, 'límite válido'):
                b.segment_turns(r['Texto'], r['Fecha'], r['Actor'], review=review)
            for left, right in [('“', '”'), ('«', '»'), ('"', '"')]:
                review = copy.deepcopy(self.reviews[p]); review['Inicio'] += 1; review['Fin'] += 1
                with self.assertRaisesRegex(ValueError, 'límite válido'):
                    b.segment_turns(left + r['Texto'] + right, r['Fecha'], r['Actor'], review=review)

    def test_reviewed_whole_intervals_and_source_hashes_are_enforced(self):
        selected = SOURCE_HASHES.keys() & self.reviews.keys()
        for p in selected:
            rows = [dict(ID=i, ID_Padre=p, Texto=t, Actor_Final=a, Fuente_Actor=m)
                    for i, (t, a, m) in enumerate(self.parts(p), 1)]
            self.assertEqual(validate_speaker_reviews(rows, {p: self.reviews[p]}), [])
            next(r for r in rows if r['Fuente_Actor'] == 'CONTEXTO_REVISADO')['Texto'] += ' añadido'
            self.assertTrue(validate_speaker_reviews(rows, {p: self.reviews[p]}))
        entries = [r for r in json.loads(SPEAKER_REVIEWS.read_text()) if r['ID_Padre'] in selected]
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'reviews.json'; path.write_text(json.dumps(entries))
            for p in selected:
                raw = copy.deepcopy(self.raw); raw[p]['Texto'] += ' cambio'
                with self.assertRaisesRegex(ValueError, 'texto de origen'):
                    load_speaker_reviews(raw, path)

    def test_commitment_is_not_a_quoted_or_hypothetical_turn(self):
        for t in ['Según el señor Lehmann, la cifra cambia.',
                  'El señor Lehmann podría comprometerse a revisar las cifras.',
                  'El Presidente señala que el señor Lehmann se compromete a revisar las cifras.',
                  '“El señor Lehmann se compromete a revisar las cifras.”']:
            candidate = b.TURN_DETECTOR.speaker(t, '2011-08-18')
            self.assertTrue(candidate is None or candidate['actor'] == PRES)

    def test_5231_explicit_subject_without_splitting_exposition(self):
        parts = self.parts(5231)
        self.assertEqual([(a, m) for t, a, m in parts], [(LEHMANN, 'SUJETO_NOMBRE')])
        self.assertEqual(parts[0][0], self.raw[5231]['Texto'])
        self.assertIn('En todo caso, indica', parts[0][0])

    def test_context_review_does_not_invent_cross_paragraph_anchor(self):
        from continuity import update_state
        part = self.parts(3887)[-1]
        state = {}
        update_state(state, part[1], part[2], part[0], '2011-03-17', b.TURN_DETECTOR, b.split_sentences, 1)
        self.assertIsNone(state['anchor'])
        self.assertEqual(self.parts(3888)[0][1], MARSHALL)
        # Misma exposición textual, pero un ID_Turno común requiere ancla admisible.

    def test_4224_lehmann_returns_after_cowan_and_keeps_cds_presentation(self):
        parts = self.parts(4224)
        self.assertEqual([a for t, a, m in parts], [COWAN, LEHMANN])
        self.assertEqual([len(t) for t, a, m in parts], [441, 966])
        self.assertIn('Agrega que los CDS de Italia', parts[1][0])
        self.assertIn('Société Générale', parts[1][0])
        self.assertTrue(parts[1][0].endswith('un nivel levemente elevado.'))

    def test_4341_vicepresident_complement_then_lehmann_precision(self):
        parts = self.parts(4341)
        self.assertEqual([a for t, a, m in parts], [PRES, LEHMANN, MARFAN, LEHMANN])
        self.assertEqual([len(t) for t, a, m in parts], [134, 75, 95, 245])
        self.assertTrue(parts[2][0].endswith('otorgan su garantía.'))
        self.assertTrue(parts[3][0].startswith('El señor Lehmann precisa'))
        self.assertIn('Grecia, Portugal Irlanda', parts[3][0])

    def test_4357_mention_within_marfan_is_not_lehmann_return(self):
        parts = self.parts(4357)
        self.assertEqual([a for t, a, m in parts], [MARFAN, LEHMANN])
        self.assertEqual([len(t) for t, a, m in parts], [654, 580])
        self.assertIn('—que el señor Lehmann denomina de carácter especulativo—', parts[0][0])
        self.assertTrue(parts[1][0].startswith('Al finalizar su presentación'))
        self.assertIn('En su opinión', parts[1][0])
        self.assertTrue(parts[1][0].endswith('durante el año 2012.'))

    def test_presentation_returns_are_bounded_not_global_proximity_rules(self):
        for p, actors in [(4224, [COWAN, LEHMANN]), (4357, [MARFAN])]:
            r = self.raw[p]
            self.assertEqual([a for t, a, m in b.segment_turns(r['Texto'], r['Fecha'], r['Actor'])], actors)

    def test_5647_new_warning_is_not_automatic_adjudication(self):
        from review_flags import review_reasons
        parts = self.parts(5647)
        self.assertEqual([a for t, a, m in parts], ['Rodrigo Vergara Montes'])
        self.assertNotIn(5647, self.reviews)
        row = dict(Texto=parts[0][0], Actor_Final=parts[0][1], Fecha=self.raw[5647]['Fecha'],
                   Fuente_Rol='LISTA_ASISTENCIA', Fuente_Actor=parts[0][2], Duplicado_Exacto='NO')
        self.assertIn('POSIBLE_OTRO_HABLANTE_O_MENCION', review_reasons(row, b.TURN_DETECTOR, b.split_sentences))
        # Protección de alcance: la atribución heredada NO se certifica como pura.


SOURCE_HASHES = {3800: 'c66c98897c02a55f09fce3132dc22e01e596a2238fc17edb9ea35ed8490da1d8', 3810: 'b2a82d5e9b5ea1cdc554782387e55ea02e32196a7849a235d716a6780ba8dfb0', 3811: '004744d099a3eb017aa26042e2e2277c3a65010277c5e1c27a485df588e029a4', 3812: '0ed3f509c2af6728020f56725cbc4343a9fd3678c274c935deb0720b680d56e0', 3813: '2ba6c82805ab531cf13a65ea7b23a3982511b8f5fd3c3612ec8ce082a6c7c06f', 3814: 'bd28fc2f4f7b628f124961a478ed15eae93a20133e77cfabf69b552820a6ebc8', 3887: 'd8c21b38a94635b583aee621d4346374a9cb9226d2d1edb43800462c4a230453', 3888: 'a7f3086e6c10fae71e8fd07e54381e0686b27afadd7ec00caa93058bf5dd6cab', 3906: '0b1afd119abf98fbd8223feff96a54c4851530b1e679836940e7ba4cec23e83d', 4220: 'c3073064f00dd768b5377883a55412c982531bd486682a450dd51c7e411de802', 4338: '5a012b1a865527b70df3bbbfe1fe3b73b07ca3ada81d57e2649ef4aea2ab19c6', 5231: '1165efb10ed3873613a9d39565c20713ebaa28d4ff4cf4e3c4f5184ce20f8d40', 5647: '09ec80183f30efee597fe32f0ee0cc3a8e631cd90dc74017e7cb5597d278623c', 4224: '9aa4dcbac22b640a6a916b017e2225fdc46da85624ff836af69d724028d09530', 4225: '2f42616bf276092f9929202420d430e54bb951c95a73784e2ec18785783969f7', 4341: '26e27a214f5df2531eebd2342363d90cc66c5be18e8ed880636f1a49b6bae3c6', 4357: 'ec97f28400a25507951819d1299790fb312612007cdf10b667f56d6f36502123'}

if __name__ == '__main__':
    unittest.main()
