"""Intercambios acotados: complemento, exposición concatenada y pregunta breve."""
import copy
import hashlib
import re
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, validate_speaker_reviews

MARFAN = 'Manuel Marfán Lewis'
GARCIA = 'Pablo García Silva'
LEHMANN = 'Sergio Lehmann Beresi'
DESORMEAUX = 'Jorge Desormeaux Jiménez'
SOTO = 'Claudio Soto Gamboa'
VELASCO = 'Andrés Velasco Brañes'
PRES = 'José De Gregorio Rebeco'
DERAMON = 'Beltrán de Ramón Acevedo'
MARSHALL = 'Enrique Marshall Rivera'
PARENTS = (2566,2667,2704)


class ExchangeReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {r[0]: dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews = load_speaker_reviews(cls.raw)

    def parts(self, p, review=None, text=None):
        r = self.raw[p]
        return b.segment_turns(r['Texto'] if text is None else text, r['Fecha'], r['Actor'],
                               review=self.reviews[p] if review is None else review)

    def test_fixed_source_hashes(self):
        self.assertEqual(set(SOURCE_HASHES),set(PARENTS))
        for p,h in SOURCE_HASHES.items():
            self.assertEqual(hashlib.sha256(self.raw[p]['Texto'].encode()).hexdigest(),h)

    def test_full_conservation(self):
        compact = lambda s: re.sub(r'\s+','',s)
        for p in PARENTS:
            self.assertEqual(compact(''.join(t for t,a,m in self.parts(p))),compact(self.raw[p]['Texto']))

    def test_desormeaux_complements_and_lehmann_returns(self):
        parts = self.parts(2566)
        self.assertEqual([a for t,a,m in parts],[MARFAN,GARCIA,LEHMANN,DESORMEAUX,LEHMANN])
        self.assertEqual(parts[3][2],'CONTEXTO_REVISADO')
        self.assertTrue(parts[3][0].startswith('planteamiento al cual el Vicepresidente'))
        self.assertTrue(parts[4][0].startswith('Continuando con su exposición, el señor Lehmann'))
        self.assertIn('Agrega, que en cuanto a los tipos de cambio real',parts[4][0])

    def test_previous_expositions_not_split_by_length_or_mentions(self):
        parts = self.parts(2566)
        self.assertEqual([len(t) for t,a,m in parts],[396,1405,639,319,579])
        self.assertIn('Asimismo, responde al Consejero señor Manuel Marfán',parts[2][0])
        r = self.raw[2566]
        before = b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertEqual(parts[:2],before[:2])

    def test_no_unreviewed_inner_clause_splitting(self):
        for p,count in [(2566,3),(2667,3),(2704,2)]:
            r = self.raw[p]
            self.assertEqual(len(b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])),count)

    def test_new_lead_requires_actual_subject_predicate(self):
        t = 'planteamiento al cual el Vicepresidente señor Jorge Desormeaux complementa, señalando que las tasas suben.'
        self.assertEqual(b.TURN_DETECTOR.speaker(t,'2009-06-16')['actor'],DESORMEAUX)
        for t in ['planteamiento al cual se refiere la presentación del señor Desormeaux.',
                  'planteamiento al cual el Vicepresidente señor Jorge Desormeaux está atento.',
                  'planteamiento al cual, según el Vicepresidente señor Jorge Desormeaux, responde el mercado.']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2009-06-16'))

    def test_new_lead_does_not_admit_another_finite_speaker_clause(self):
        t = 'planteamiento al cual se refiere el señor Lehmann, el Vicepresidente señor Jorge Desormeaux complementa que las tasas suben.'
        c = b.TURN_DETECTOR.speaker(t,'2009-06-16')
        self.assertTrue(c is None or c['actor']!=DESORMEAUX)

    def test_quoted_lead_is_not_a_new_turn(self):
        for l,r in [('“','”'),('«','»'),('"','"')]:
            t = l+'planteamiento al cual el Vicepresidente señor Jorge Desormeaux complementa que las tasas suben.'+r
            self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2009-06-16'))

    def test_inner_review_requires_compatible_actor(self):
        for p in [2566,2667]:
            review = copy.deepcopy(self.reviews[p]);review['Actor'] = PRES
            with self.assertRaisesRegex(ValueError,'límite válido'):
                self.parts(p,review)

    def test_inner_review_rejects_quoted_boundaries(self):
        for p in [2566,2667]:
            for l,r in [('“','”'),('«','»'),('"','"')]:
                review = copy.deepcopy(self.reviews[p]);review['Inicio']+=1;review['Fin']+=1
                with self.assertRaisesRegex(ValueError,'límite válido'):
                    self.parts(p,review,l+self.raw[p]['Texto']+r)

    def test_complement_requires_clause_separator(self):
        review = self.reviews[2566];text = self.raw[2566]['Texto']
        comma = text.rfind(',',0,review['Inicio'])
        with self.assertRaisesRegex(ValueError,'límite válido'):
            self.parts(2566,text=text[:comma]+' '+text[comma+1:])

    def test_soto_presentation_keeps_damage_and_gerente_continuity(self):
        parts = self.parts(2667)
        self.assertEqual([a for t,a,m in parts],[VELASCO,LEHMANN,SOTO])
        self.assertTrue(parts[1][0].endswith('y el Gerente de'))
        self.assertEqual(len(parts[2][0]),1134)
        self.assertTrue(parts[2][0].startswith('Al continuar con la exposición sobre consumo'))
        self.assertIn('el señor Gerente menciona',parts[2][0])
        self.assertIn('Luego, el señor Soto manifiesta',parts[2][0])
        self.assertEqual(parts[2][2],'CONTEXTO_REVISADO')

    def test_president_question_then_deramon_answer(self):
        parts = self.parts(2704)
        self.assertEqual([a for t,a,m in parts],[DERAMON,PRES,DERAMON,MARSHALL,SOTO])
        self.assertEqual(parts[1][0],'Es decir, no es problema de demanda, consulta el señor Presidente,')
        self.assertTrue(parts[2][0].startswith('a lo cual el señor de Ramón manifiesta'))
        self.assertIn('Podría ser que subsistan los problemas de oferta',parts[2][0])

    def test_passive_confirmation_recovered_by_loop23(self):
        # LOOP23: la confirmación pasiva recibió una revisión individual.
        last = self.parts(2704)[-1]
        self.assertEqual(last[1],SOTO)
        self.assertTrue(last[0].endswith('lo cual es confirmado por el señor Claudio Soto.'))

    def test_reviewed_intervals_survive_exactly_and_fail_on_truncation(self):
        for p in PARENTS:
            rows = [dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m)
                    for i,(t,a,m) in enumerate(self.parts(p),1)]
            self.assertEqual(validate_speaker_reviews(rows,{p:self.reviews[p]}),[])
            revised = next(r for r in rows if r['Fuente_Actor']=='CONTEXTO_REVISADO')
            revised['Texto'] = revised['Texto'][:-10]
            self.assertTrue(validate_speaker_reviews(rows,{p:self.reviews[p]}))


SOURCE_HASHES = {2566: '4888d369b51dbde449be28d6dce158afb565cba3b64bd42387d31090aef16769', 2667: '8ecd52eb4de993a9dac5b2f1a9cf06e13d9c74a70d29e9021e9a113c68debc4a', 2704: '1b67ddf55051af63a23c5ac9d1b0bcdab007b6a164bd979c55e116b2ca631ff9'}

if __name__ == '__main__':
    unittest.main()
