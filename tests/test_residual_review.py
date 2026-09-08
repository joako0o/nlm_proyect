"""Respuesta en gerundio adjudicada y separación de acuerdos institucionales."""
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, SPEAKER_REVIEWS

INSTITUTIONAL = (219,294,310,503,526,594,654,674,780,1020)
FORMULA = 'En mérito de lo anterior, el Consejo, por la unanimidad de sus miembros, adopta el siguiente Acuerdo'
PRES = 'José De Gregorio Rebeco'
MARSHALL = 'Enrique Marshall Rivera'
SOTO = 'Claudio Soto Gamboa'


class ResidualReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {r[0]: dict(Fecha=b.to_date_str(r[1]), Texto=r[5], Actor=r[2]) for r in b.data}
        cls.reviews = load_speaker_reviews(cls.raw)

    def parts(self, p):
        r = self.raw[p]
        return b.segment_turns(r['Texto'], r['Fecha'], r['Actor'], review=self.reviews.get(p))

    def synthetic(self, text, actor=PRES):
        review = dict(Actor=actor,Inicio=text.index('señalando'),Fin=len(text),
                      Tipo_Limite='GERUNDIO_SENALANDO_EXPLICITO')
        return b.segment_turns(text, '2010-03-18', MARSHALL, review=review)

    def test_source_hashes_are_read_versions(self):
        self.assertEqual(set(SOURCE_HASHES), set(INSTITUTIONAL)|{2981})
        for p,h in SOURCE_HASHES.items():
            self.assertEqual(hashlib.sha256(self.raw[p]['Texto'].encode()).hexdigest(), h)

    def test_president_answer_and_soto_complement_are_separate(self):
        parts = self.parts(2981)
        self.assertEqual([a for t,a,m in parts],
                         [MARSHALL,SOTO,'Pablo García Silva',SOTO,MARSHALL,PRES,SOTO])
        self.assertGreater(len(parts[3][0]), 3200)
        self.assertTrue(parts[4][0].endswith('- 0,7%,'))
        self.assertTrue(parts[5][0].startswith('señalando el señor Presidente que'))
        self.assertIn('Agrega que como consecuencia del terremoto', parts[5][0])
        self.assertTrue(parts[6][0].startswith('El señor Soto complementa'))
        self.assertEqual(parts[5][2], 'CONTEXTO_REVISADO')
        for separator in [',', ';']:
            text = 'El señor Marshall pregunta'+separator+' señalando el señor Presidente que la cifra es anual.'
            reviewed = self.synthetic(text)
            self.assertEqual(len(reviewed), 2)
            self.assertEqual(reviewed[-1][1], PRES)
            self.assertTrue(reviewed[-1][0].startswith('señalando '))

    def test_no_general_rule_for_all_gerunds(self):
        r = self.raw[2981]
        self.assertEqual(len(b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])), 6)
        self.assertEqual({p for p,r in self.reviews.items() if r.get('Tipo_Limite')=='GERUNDIO_SENALANDO_EXPLICITO'}, {2981,1386,2938})

    def test_wrong_review_actor_is_rejected(self):
        review = copy.deepcopy(self.reviews[2981]);review['Actor'] = SOTO
        r = self.raw[2981]
        with self.assertRaisesRegex(ValueError, 'límite válido'):
            b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=review)

    def test_quoted_gerund_is_not_an_actual_turn(self):
        r = self.raw[2981]
        for left,right in [('“','”'),('«','»'),('"','"')]:
            review = copy.deepcopy(self.reviews[2981]);review['Inicio']+=1;review['Fin']+=1
            with self.assertRaisesRegex(ValueError, 'límite válido'):
                b.segment_turns(left+r['Texto']+right,r['Fecha'],r['Actor'],review=review)

    def test_gerund_requires_prior_clause_separator(self):
        for separator in ['', '.']:
            with self.assertRaisesRegex(ValueError, 'límite válido'):
                self.synthetic('El señor Marshall pregunta'+separator+' señalando el señor Presidente que la cifra es anual.')

    def test_pointing_at_someone_or_object_is_not_speaking_subject(self):
        for tail in ['señalando al señor Presidente que la cifra es anual.',
                     'señalando que el señor Presidente está presente.',
                     'señalando el gráfico del señor Presidente.']:
            with self.assertRaisesRegex(ValueError, 'válid'):
                self.synthetic('El señor Marshall pregunta, '+tail)

    def test_gerund_requires_declarative_que_after_subject(self):
        with self.assertRaisesRegex(ValueError, 'declaración válida'):
            self.synthetic('El señor Marshall pregunta, señalando el señor Presidente con el dedo hacia el gráfico.')

    def test_changed_source_invalidates_gerund_review(self):
        entries = [e for e in json.loads(SPEAKER_REVIEWS.read_text()) if e['ID_Padre']==2981]
        raw = copy.deepcopy(self.raw);raw[2981]['Texto'] += ' Cambio.'
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'review.json';p.write_text(json.dumps(entries))
            with self.assertRaisesRegex(ValueError, 'texto de origen'):
                load_speaker_reviews(raw, p)

    def test_ten_agreements_begin_at_formal_council_declaration(self):
        for p in INSTITUTIONAL:
            with self.subTest(parent=p):
                parts = self.parts(p)
                i = next(i for i,(text,_,_) in enumerate(parts) if text.startswith(FORMULA))
                self.assertEqual(parts[i][1:], (b.CONSEJO,'ACTA/META'))
                self.assertEqual(parts[i-1][1], 'Vittorio Corbo Lioi')
                self.assertNotIn(FORMULA, parts[i-1][0])

    def test_institutional_rule_is_not_for_mentions_or_proposals(self):
        for text in [
            'El Presidente señala que '+FORMULA+'.',
            'En mérito de lo anterior, el Presidente recuerda que el Consejo, por la unanimidad de sus miembros, adopta el siguiente Acuerdo.',
            FORMULA.replace('adopta','podría adoptar')+'.',
            FORMULA.replace('adopta','debería adoptar')+'.',
        ]:
            with self.subTest(text=text):
                self.assertFalse(b._inst_transition(text))
        text = 'El Presidente señor Corbo señala: “'+FORMULA+'”.'
        self.assertEqual([a for t,a,m in b.segment_turns(text,'2006-07-13','Vittorio Corbo Lioi')],
                         ['Vittorio Corbo Lioi'])

    def test_all_changed_parents_preserve_source(self):
        compact = lambda s: re.sub(r'\s+', '', s)
        for p in INSTITUTIONAL+(2981,):
            self.assertEqual(compact(''.join(t for t,a,m in self.parts(p))), compact(self.raw[p]['Texto']))

    def test_780_unknown_start_is_not_resolved_by_assumption(self):
        # Sólo el inicio explícito es revisado; el puente anterior sigue provisional.
        self.assertGreater(self.reviews[780]['Inicio'],self.raw[780]['Texto'].index('En la economía nacional'))
        parts = self.parts(780)
        self.assertIn('En la economía nacional', parts[0][0])
        self.assertNotIn('Lo que sí ha cambiado', parts[0][0])
        self.assertTrue(parts[1][0].startswith('Lo que sí ha cambiado, indica el señor Corbo'))
        self.assertTrue(parts[2][0].startswith('Señala el Presidente, señor Corbo'))
        self.assertTrue(parts[3][0].startswith(FORMULA))
        self.assertIn(780,b.load_context_warnings(self.raw))


SOURCE_HASHES = {
    219: '2c50da93f36422325838d10674bc4d7f4845066b9b44d895ff31457d335fb7c7',
    294: '8f881e1fbf3705df4784fd5ffd1bb3763558de7f072fa61ff9a36ac9a899d9e7',
    310: '5307857369033ea9db7f617cbd4839a3e94aa677c2819954dcc81d0462a2ca09',
    503: 'c36eb48257e5350bb9c5e5406fbbb80d69b55e61a618f1ef6a877cd46913f664',
    526: '5c87ccf649bc2eaba65852ad9c41c7c7655e7a1daaf9ce304dabf3c0feab5967',
    594: '545f96745fdc53223cf8677c88df62046e5e7c8a459ea9ebe172cb128c7da7ea',
    654: '6a1f93cdb3885e7b9c1ef2721b64f2e9c8a3ae50bde5c5a5ea1619d71b8590d1',
    674: '3a93ebe7b059886af563851f2dbd2ad999d14d396dea16aa4e255ab36bf7d6ab',
    780: 'c9325d0aa5f9fa57bef82bb441e6a5ef228ee0db912c062c1c0fdc09d758cf13',
    1020: '78a541c15e76f15c589d26248c9ac7ba54b9d067ab58b761c57dbeb07edaf253',
    2981: 'a786b1a89d62184cd923e9ac5c70552d8e5cc4077caf17ea0e5f6f8a0c686f36',
}

if __name__ == '__main__':
    unittest.main()
