"""Asentimiento expreso, respuesta contrastiva y complementos del expositor."""
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, validate_speaker_reviews, SPEAKER_REVIEWS

COWAN='Kevin Cowan Logan'
SOTO='Claudio Soto Gamboa'
MARSHALL='Enrique Marshall Rivera'
MARFAN='Manuel Marfán Lewis'
DERAMON='Beltrán de Ramón Acevedo'
BERNIER='Matías Bernier Bórquez'
GARCIA='Pablo García Silva'
PARENTS=(2779,3107,3158)


class AssentReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)

    def parts(self,p,review=None,text=None):
        r=self.raw[p]
        return b.segment_turns(r['Texto'] if text is None else text,r['Fecha'],r['Actor'],
                               review=self.reviews[p] if review is None else review)

    def test_fixed_hashes_of_read_sources(self):
        self.assertEqual(set(SOURCE_HASHES),set(PARENTS))
        for p,h in SOURCE_HASHES.items():
            self.assertEqual(hashlib.sha256(self.raw[p]['Texto'].encode()).hexdigest(),h)

    def test_conservation_of_all_source_characters(self):
        compact=lambda s:re.sub(r'\s+','',s)
        for p in PARENTS:
            self.assertEqual(compact(''.join(t for t,a,m in self.parts(p))),compact(self.raw[p]['Texto']))

    def test_cowan_assent_and_marshall_are_three_distinct_acts(self):
        parts=self.parts(2779)
        self.assertEqual([a for t,a,m in parts],[COWAN,SOTO,MARSHALL])
        self.assertEqual([len(t) for t,a,m in parts],[222,22,366])
        self.assertEqual(parts[1][0],'El señor Soto asiente,')
        self.assertEqual(parts[1][2],'SUJETO_NOMBRE')
        self.assertTrue(parts[2][0].startswith('mientras que el Consejero señor Enrique Marshall responde'))
        self.assertIn('En su opinión, en este sector',parts[2][0])
        self.assertEqual(parts[2][2],'CONTEXTO_REVISADO')

    def test_assent_does_not_invent_spoken_words(self):
        text='El señor Soto asiente.'
        self.assertEqual(b.segment_turns(text,'2009-11-12',COWAN),[(text,SOTO,'SUJETO_NOMBRE')])
        self.assertNotIn('sí',self.parts(2779)[1][0].lower())

    def test_non_person_asiente_and_reported_reference_are_not_turns(self):
        for text in ['Espera que un nuevo escenario se asiente antes de cambiar la instancia de política.',
                     'Como asiente el señor Soto, se considera el análisis.',
                     'Se pregunta si el señor Soto asiente.',
                     'El escenario se asiente según el señor Soto.',
                     'El señor Soto podría asentir.']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(text,'2009-11-12'))

    def test_quoted_assent_and_contrast_do_not_create_new_speakers(self):
        for l,r in [('“','”'),('«','»'),('"','"')]:
            self.assertIsNone(b.TURN_DETECTOR.speaker(l+'El señor Soto asiente.'+r,'2009-11-12'))
            self.assertIsNone(b.TURN_DETECTOR.speaker(l+'mientras que el señor Marshall responde que las cifras difieren.'+r,'2009-11-12'))

    def test_contrast_requires_speaking_subject_not_mention(self):
        text='mientras que el Consejero señor Enrique Marshall responde que las cifras difieren.'
        self.assertEqual(b.TURN_DETECTOR.speaker(text,'2009-11-12')['actor'],MARSHALL)
        for text in ['mientras que según el señor Marshall responde el mercado.',
                     'mientras que el señor Marshall está presente.',
                     'mientras que la respuesta del señor Marshall menciona una cifra.']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(text,'2009-11-12'))

    def test_unreviewed_contrast_and_coordination_remain_unsplit(self):
        r=self.raw[2779];parts=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertEqual([a for t,a,m in parts],[COWAN,SOTO])
        self.assertIn('mientras que',parts[1][0])
        r=self.raw[3158];parts=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertIn('y el señor Claudio Soto agrega',parts[0][0])

    def test_incompatible_inner_review_actor_rejected(self):
        for p in [2779,3158]:
            review=copy.deepcopy(self.reviews[p]);review['Actor']=COWAN
            with self.assertRaisesRegex(ValueError,'límite válido'):
                self.parts(p,review)

    def test_inner_reviews_reject_quotes(self):
        for p in [2779,3158]:
            for l,r in [('“','”'),('«','»'),('"','"')]:
                review=copy.deepcopy(self.reviews[p]);review['Inicio']+=1;review['Fin']+=1
                with self.assertRaisesRegex(ValueError,'límite válido'):
                    self.parts(p,review,l+self.raw[p]['Texto']+r)

    def test_contrast_review_requires_prior_separator(self):
        text=self.raw[2779]['Texto'];i=text.index('asiente,')+len('asiente')
        with self.assertRaisesRegex(ValueError,'límite válido'):
            self.parts(2779,text=text[:i]+' '+text[i+1:])

    def test_bernier_complement_keeps_previous_expositions_and_damaged_text(self):
        parts=self.parts(3107)
        self.assertEqual([a for t,a,m in parts],[MARFAN,DERAMON,BERNIER])
        self.assertEqual([len(t) for t,a,m in parts],[2900,1558,336])
        self.assertIn('y últimamente.',parts[2][0])
        self.assertIn('Agrega que el ha ido disminuyendo',parts[2][0])
        self.assertTrue(parts[2][0].endswith('ha traído nuevos bonos.'))

    def test_soto_initial_complement_stays_with_later_presentation(self):
        parts=self.parts(3158)
        self.assertEqual([a for t,a,m in parts],[GARCIA,SOTO])
        self.assertEqual([len(t) for t,a,m in parts],[82,746])
        self.assertTrue(parts[0][0].endswith('millones de personas'))
        self.assertTrue(parts[1][0].startswith('y el señor Claudio Soto agrega'))
        self.assertIn('400.000 personas.',parts[1][0])
        self.assertIn('El señor Soto prosigue',parts[1][0])
        self.assertIn('Añade que la serie de empleo por cuenta propia',parts[1][0])

    def test_exact_review_intervals_and_truncation_detection(self):
        for p in PARENTS:
            rows=[dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p),1)]
            self.assertEqual(validate_speaker_reviews(rows,{p:self.reviews[p]}),[])
            row=next(r for r in rows if r['Fuente_Actor']=='CONTEXTO_REVISADO');row['Texto']=row['Texto'][:-10]
            self.assertTrue(validate_speaker_reviews(rows,{p:self.reviews[p]}))

    def test_source_change_invalidates_review(self):
        entries=[e for e in json.loads(SPEAKER_REVIEWS.read_text()) if e['ID_Padre'] in PARENTS]
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'reviews.json';p.write_text(json.dumps(entries))
            for parent in PARENTS:
                raw=copy.deepcopy(self.raw);raw[parent]['Texto']+=' cambio'
                with self.assertRaisesRegex(ValueError,'texto de origen'):
                    load_speaker_reviews(raw,p)


SOURCE_HASHES = {2779: '4f8c900b02547f37065c1b6bf660952ba8303456339e42fd0bea158cfa9a5fb4', 3107: '70bdecaab346768f17df7bd8fbb422e87221bb826b91abc769adb5af4c7160c3', 3158: '304d470f585515c6478f844583b9dc073579f13e33b24c8f5bf487417b9ff08b'}

if __name__ == '__main__':
    unittest.main()
