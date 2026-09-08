"""Retornos de exposición y respuesta OCR: sujetos explícitos y continuidad."""
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
from turns import normalize

PRES='José De Gregorio Rebeco'
LEHMANN='Sergio Lehmann Beresi'
GARCIA='Pablo García Silva'
HERRERA='Luis Óscar Herrera Barriga'
MARFAN='Manuel Marfán Lewis'
PARENTS=(3221,3233,3468)


class ReturnReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)

    def parts(self,p,review=None):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p) if review is None else review)

    def test_fixed_read_source_hashes(self):
        self.assertEqual(set(SOURCE_HASHES),set(PARENTS))
        for p,h in SOURCE_HASHES.items():
            self.assertEqual(hashlib.sha256(self.raw[p]['Texto'].encode()).hexdigest(),h)

    def test_complete_source_conservation(self):
        compact=lambda s:re.sub(r'\s+','',s)
        for p in PARENTS:
            self.assertEqual(compact(''.join(t for t,a,m in self.parts(p))),compact(self.raw[p]['Texto']))

    def test_lehmann_return_after_president(self):
        parts=self.parts(3221)
        self.assertEqual([a for t,a,m in parts],[PRES,LEHMANN])
        self.assertEqual([len(t) for t,a,m in parts],[296,2217])
        self.assertEqual(parts[1][2],'SUJETO_ROL_SESION')
        self.assertTrue(parts[1][0].startswith('Al proseguir, el Gerente de Análisis Internacional señala'))
        self.assertIn('lo que está hoy está proyectando',parts[1][0])
        self.assertIn('World Economic Out/ook',parts[1][0])
        self.assertIn('Añade que ellos han revisado',parts[1][0])

    def test_lehmann_continuity_with_next_source_parent(self):
        from test_continuity import sequence
        rows=sequence([(p,self.raw[p]['Fecha'],self.raw[p]['Actor'],self.raw[p]['Texto']) for p in [3221,3222]])
        returned=next(r for r in rows if r['ID_Padre']==3221 and r['Actor_Final']==LEHMANN)
        following=next(r for r in rows if r['ID_Padre']==3222)
        self.assertEqual(returned['ID_Turno'],following['ID_Turno'])
        self.assertEqual(following['Relacion_Turno'],'CONTINUIDAD_EXPLICITA')
        self.assertNotIn(3221,self.reviews)

    def test_return_prefix_remains_exact_and_rejects_mentions(self):
        for text in ['Al proseguir con su exposición, el señor Lehmann señala que las tasas suben.',
                     'Al proseguir, según el señor Lehmann, las tasas suben.',
                     'Al proseguir, la presentación del señor Lehmann señala que las tasas suben.',
                     'Al proseguir, el señor Lehmann está presente.',
                     'Al proseguir, el Gerente de División indica que las tasas suben.']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(text,'2010-07-15'))

    def test_return_inside_quotes_is_not_new_speaker(self):
        for l,r in [('“','”'),('«','»'),('"','"')]:
            text=l+'Al proseguir, el señor Lehmann señala que las tasas suben.'+r
            self.assertIsNone(b.TURN_DETECTOR.speaker(text,'2010-07-15'))

    def test_ai_normalization_is_initial_only_and_idempotent(self):
        text='Ai respecto, el señor Pablo García responde.'
        self.assertEqual(normalize(text),'al respecto, el senor pablo garcia responde.')
        self.assertEqual(normalize(normalize(text)),normalize(text))
        self.assertIn('ai respecto',normalize('Se conserva Ai respecto en una cita.'))
        self.assertEqual(normalize('AI en un informe'),'ai en un informe')

    def test_garcia_reply_retains_literal_ocr(self):
        parts=self.parts(3233)
        self.assertEqual([a for t,a,m in parts],[PRES,GARCIA])
        self.assertEqual([len(t) for t,a,m in parts],[90,232])
        self.assertTrue(parts[1][0].startswith('Ai respecto,'))
        self.assertEqual(parts[1][2],'SUJETO_NOMBRE')
        self.assertNotIn(3233,self.reviews)

    def test_ai_prefix_cannot_invent_a_subject_or_unquote(self):
        for text in ['Ai respecto, hace notar una inconsistencia entre fuentes.',
                     'Ai respecto, según el señor Pablo García, la cifra aumenta.',
                     '“Ai respecto, el señor Pablo García responde que la cifra aumenta.”']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(text,'2010-07-15'))

    def test_herrera_then_marfan_summary_and_continuations(self):
        parts=self.parts(3468)
        self.assertEqual([a for t,a,m in parts],[HERRERA,MARFAN])
        self.assertEqual([len(t) for t,a,m in parts],[502,421])
        self.assertIn('comprender la preocupación del señor Vicepresidente',parts[0][0])
        self.assertTrue(parts[1][0].startswith('Para resumir, el Vicepresidente señor Manuel Marfán plantea'))
        self.assertIn('Por este motivo, estima',parts[1][0])
        self.assertIn('Lo otro, indica',parts[1][0])
        self.assertEqual(parts[1][2],'CONTEXTO_REVISADO')

    def test_summary_boundary_requires_individual_review(self):
        r=self.raw[3468]
        parts=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertEqual([a for t,a,m in parts],[HERRERA])

    def test_summary_interval_validation_rejects_truncation(self):
        rows=[dict(ID=i,ID_Padre=3468,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(3468),1)]
        self.assertEqual(validate_speaker_reviews(rows,{3468:self.reviews[3468]}),[])
        rows[-1]['Texto']=rows[-1]['Texto'][:-10]
        self.assertTrue(validate_speaker_reviews(rows,{3468:self.reviews[3468]}))

    def test_changed_source_invalidates_summary_review(self):
        entries=[e for e in json.loads(SPEAKER_REVIEWS.read_text()) if e['ID_Padre']==3468]
        raw=copy.deepcopy(self.raw);raw[3468]['Texto']+=' cambio'
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'review.json';path.write_text(json.dumps(entries))
            with self.assertRaisesRegex(ValueError,'texto de origen'):
                load_speaker_reviews(raw,path)


SOURCE_HASHES = {3221: 'b60d361f9c18ceffdda41d956392300183e237a651c68f796f70f817826bdc73', 3233: 'ec9064f45a4199559c2aeff706eb8fea5298b3234717848e53830e626c781a96', 3468: 'acb924a2fa0ed98c0a7792bf9d4daa03999e832b42b279337ba044fffea5358f'}

if __name__ == '__main__':
    unittest.main()
