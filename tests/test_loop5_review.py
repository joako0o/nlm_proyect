"""Lote posterior al PR: suspensiones, opinión intermedia y retorno del expositor."""
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
VERGARA = 'Rodrigo Vergara Montes'
LEHMANN = 'Sergio Lehmann Beresi'
CLARO = 'Sebastián Claro Edwards'
HERRERA = 'Luis Óscar Herrera Barriga'
MARFAN = 'Manuel Marfán Lewis'
SOTO = 'Claudio Soto Gamboa'
PARENTS = (4384, 4420, 4421, 4502)

class LoopFiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {r[0]: dict(Fecha=b.to_date_str(r[1]), Texto=r[5], Actor=r[2]) for r in b.data}
        cls.reviews = load_speaker_reviews(cls.raw)

    def parts(self, p):
        r = self.raw[p]
        return b.segment_turns(r['Texto'], r['Fecha'], r['Actor'], review=self.reviews[p])

    def test_read_source_hashes(self):
        self.assertEqual(set(SOURCE_HASHES), set(PARENTS))
        for p, h in SOURCE_HASHES.items():
            self.assertEqual(hashlib.sha256(self.raw[p]['Texto'].encode()).hexdigest(), h)

    def test_all_characters_conserved_except_whitespace(self):
        compact = lambda t: re.sub(r'\s+', '', t)
        for p in PARENTS:
            self.assertEqual(compact(''.join(t for t,a,m in self.parts(p))), compact(self.raw[p]['Texto']))

    def test_4384_suspension_not_marfan_and_reopening_not_president(self):
        parts = self.parts(4384)
        self.assertEqual([a for t,a,m in parts], [MARFAN, PRES, b.CONSEJO])
        self.assertEqual([len(t) for t,a,m in parts], [477,134,143])
        self.assertIn('caída de las tasas largas', parts[0][0])
        self.assertTrue(parts[1][0].endswith('hasta las 16 horas.'))
        self.assertIn('Felipe Larraín', parts[2][0])

    def test_4420_claro_opinion_and_lehmann_reply(self):
        parts = self.parts(4420)
        self.assertEqual([a for t,a,m in parts], [LEHMANN,CLARO,LEHMANN])
        self.assertEqual([len(t) for t,a,m in parts], [706,214,559])
        self.assertTrue(parts[1][0].startswith('En opinión del Consejero'))
        self.assertTrue(parts[2][0].startswith('El señor Lehmann manifiesta'))
        self.assertIn('En todo caso, destaca', parts[2][0])

    def test_4421_return_begins_at_graph_not_only_last_sentence(self):
        parts = self.parts(4421)
        self.assertEqual([a for t,a,m in parts], [HERRERA,LEHMANN])
        self.assertEqual([len(t) for t,a,m in parts], [798,698])
        self.assertTrue(parts[1][0].startswith('A continuación, el señor Sergio Lehmann exhibe'))
        self.assertIn('lámina N°31', parts[1][0])
        self.assertIn('Al finalizar su presentación', parts[1][0])

    def test_4502_full_soto_exposition_president_suspension_and_literal_ocr(self):
        parts = self.parts(4502)
        self.assertEqual([a for t,a,m in parts], [SOTO,VERGARA,b.CONSEJO])
        self.assertEqual([len(t) for t,a,m in parts], [2418,127,79])
        self.assertIn('Finalmente, y con respecto a las proyecciones', parts[0][0])
        self.assertTrue(parts[0][0].endswith('al primer trimestre del próximo año.'))
        self.assertEqual(parts[2][0], b._DAMAGED_REOPENING)

    def test_opinion_requires_review_but_explicit_exhibit_is_recognized(self):
        for p, expected in [(4420,[LEHMANN]), (4421,[HERRERA, LEHMANN])]:
            r = self.raw[p]
            self.assertEqual([a for t,a,m in b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])], expected)

    def test_damaged_reopening_is_not_general_ocr_cleanup(self):
        self.assertTrue(b._inst_transition(b._DAMAGED_REOPENING))
        for text in [b._DAMAGED_REOPENING.replace('179.', '180.'),
                     b._DAMAGED_REOPENING.replace('i,-', 'x,-'),
                     'Señala que ' + b._DAMAGED_REOPENING,
                     '“' + b._DAMAGED_REOPENING + '”']:
            self.assertFalse(b._inst_transition(text))

    def test_damaged_reopening_in_quotes_does_not_create_turn(self):
        for left,right in [('“','”'), ('«','»'), ('"','"')]:
            text = 'El señor Claudio Soto señala: ' + left + 'Una nota. ' + b._DAMAGED_REOPENING + right
            spans = b.split_sentences(text)
            self.assertNotIn(text.index('i,-'), {a for a,z in spans})
            self.assertEqual([a for t,a,m in b.segment_turns(text,'2011-12-13',SOTO)], [SOTO])

    def test_damaged_reopening_boundary_requires_previous_full_stop(self):
        text = 'El señor Claudio Soto señala, ' + b._DAMAGED_REOPENING
        self.assertNotIn(text.index('i,-'), {a for a,z in b.split_sentences(text)})

    def test_review_interval_is_complete_and_excludes_next_speaker(self):
        for p in PARENTS:
            rows = [dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m)
                    for i,(t,a,m) in enumerate(self.parts(p),1)]
            self.assertEqual(validate_speaker_reviews(rows,{p:self.reviews[p]}), [])
            next(r for r in rows if r['Fuente_Actor']=='CONTEXTO_REVISADO')['Texto'] += ' añadido'
            self.assertTrue(validate_speaker_reviews(rows,{p:self.reviews[p]}))

    def test_changed_source_invalidates_adjudications(self):
        entries = [r for r in json.loads(SPEAKER_REVIEWS.read_text()) if r['ID_Padre'] in PARENTS]
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'reviews.json'; path.write_text(json.dumps(entries))
            for p in PARENTS:
                raw = copy.deepcopy(self.raw); raw[p]['Texto'] += ' cambio'
                with self.assertRaisesRegex(ValueError,'texto de origen'):
                    load_speaker_reviews(raw,path)

SOURCE_HASHES = {4384: '676ed7ecb74f6614b9dd3e0b8c994fbb8d61906b392c0562190e1702da2bb50c', 4420: '66abf8300f14697017cd856c2b8997949aca3d2c1b4c0b9b33f2fc1c01a1f55e', 4421: '57211987e157632d672d5b6c80ffb891f26cc85a50934ef34aac492a2d93014d', 4502: '27734eade5ca7028a64f4adb81a95a7b77122b152a94cfb7030a5c728b15f7b2'}

if __name__ == '__main__':
    unittest.main()
