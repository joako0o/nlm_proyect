"""Cesión con agradecimiento relativo y retorno de opinión adjudicado."""
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

PRES='José De Gregorio Rebeco'
MARFAN='Manuel Marfán Lewis'
MARSHALL='Enrique Marshall Rivera'
CLARO='Sebastián Claro Edwards'
PARENTS=(3123,3187,3966)
PREFIX='Al continuar con la votación, el señor Presidente concede la palabra al Vicepresidente, señor Manuel Marfán, '
THANKS='quien agradece, en primer término, el análisis del staff.'
KIND='CESION_AGRADECIMIENTO_RELATIVO_EXPLICITO'


class HandoffOpinionReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)

    def parts(self,p):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p))

    def thanks(self,prefix=PREFIX,fragment=THANKS,actor=MARFAN):
        review=dict(Inicio=len(prefix),Fin=len(prefix+fragment),Actor=actor,Tipo_Limite=KIND)
        return b.segment_turns(prefix+fragment,'2010-05-13',PRES,review=review)

    def test_fixed_read_source_hashes(self):
        self.assertEqual(set(SOURCE_HASHES),set(PARENTS))
        for p,h in SOURCE_HASHES.items():
            self.assertEqual(hashlib.sha256(self.raw[p]['Texto'].encode()).hexdigest(),h)

    def test_source_conservation(self):
        compact=lambda t:re.sub(r'\s+','',t)
        for p in PARENTS:
            self.assertEqual(compact(''.join(t for t,a,m in self.parts(p))),compact(self.raw[p]['Texto']))

    def test_vote_handoff_and_thanks_are_separate(self):
        parts=self.parts(3123)
        self.assertEqual([a for t,a,m in parts],[MARSHALL,PRES,MARFAN])
        self.assertEqual([len(t) for t,a,m in parts],[5484,108,57])
        self.assertTrue(parts[0][0].endswith('mantener la TPM en su actual nivel de 0,50%.'))
        self.assertTrue(parts[1][0].startswith('Al continuar con la votación'))
        self.assertEqual(parts[2][0],THANKS)
        self.assertEqual(parts[2][2],'CONTEXTO_REVISADO')

    def test_no_general_relative_thanks_detection(self):
        r=self.raw[3123];plain=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertEqual([a for t,a,m in plain],[MARSHALL,PRES])
        self.assertIn(THANKS,plain[-1][0])
        self.assertEqual({p for p,r in self.reviews.items() if r.get('Tipo_Limite')==KIND},{3123})
        self.assertIsNone(b.TURN_DETECTOR.reviewed_relative_handoff(PREFIX,THANKS,'2010-05-13'))

    def test_recipient_not_giver_or_staff_is_author_of_thanks(self):
        parts=self.thanks()
        self.assertEqual([a for t,a,m in parts],[PRES,MARFAN])
        self.assertEqual(parts[1][0],THANKS)
        for wrong in [PRES,MARSHALL]:
            with self.assertRaisesRegex(ValueError,'límite válido'):
                self.thanks(actor=wrong)

    def test_thanks_requires_exact_effective_act(self):
        for fragment in ['quien agradecerá, en primer término, el análisis del staff.',
                         'quien debería agradecer el análisis del staff.',
                         'a quien agradece, en primer término, el análisis del staff.',
                         'quien recibe el agradecimiento del staff.',
                         'quien agradece a otro participante.']:
            with self.subTest(fragment=fragment),self.assertRaisesRegex(ValueError,'límite válido'):
                self.thanks(fragment=fragment)

    def test_thanks_requires_complete_unambiguous_contiguous_handoff(self):
        for prefix in [PREFIX.replace('señor Manuel Marfán,','señor Manuel Marfán y el señor Marshall,'),
                       PREFIX.replace('concede la palabra','recuerda la opinión'),
                       PREFIX.replace('Al continuar con la votación, ','Según un informe, '),
                       PREFIX.rstrip(', ')+'. ',
                       PREFIX.rstrip(', ')+'. El señor Marshall agrega, ',
                       PREFIX.replace('señor Manuel Marfán,','señor Desconocido,')]:
            with self.subTest(prefix=prefix),self.assertRaisesRegex(ValueError,'límite válido'):
                self.thanks(prefix=prefix)

    def test_thanks_rejects_quotation(self):
        for l,r in [('“','”'),('«','»'),('"','"')]:
            with self.assertRaisesRegex(ValueError,'límite válido'):
                self.thanks(prefix=l+PREFIX,fragment=THANKS+r)

    def test_president_vicepresident_and_president_return(self):
        parts=self.parts(3187)
        self.assertEqual([a for t,a,m in parts],[PRES,MARFAN,PRES])
        self.assertEqual([len(t) for t,a,m in parts],[183,157,476])
        self.assertTrue(parts[1][0].startswith('Dado eso, el señor Vicepresidente manifiesta'))
        self.assertTrue(parts[2][0].startswith('En opinión del señor Presidente,'))
        self.assertIn('Plantea que el crecimiento del dinero',parts[2][0])
        self.assertIn('Pregunta, entonces',parts[2][0])

    def test_opinion_return_is_not_globally_inferred_from_proximity(self):
        r=self.raw[3187];plain=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertEqual([a for t,a,m in plain],[PRES,MARFAN])
        self.assertIn('En opinión del señor Presidente',plain[-1][0])

    def test_new_leads_keep_reference_and_subject_guards(self):
        for text in ['Dado eso, según el señor Vicepresidente, la cifra aumenta.',
                     'Dado eso, el señor Vicepresidente está presente.',
                     'Dado eso, la opinión del señor Vicepresidente indica una diferencia.',
                     'Al continuar con la votación, según el señor Presidente, la cifra cambia.',
                     'Al continuar con la votación, el señor Presidente está presente.',
                     '“Dado eso, el señor Vicepresidente manifiesta que la cifra cambia.”']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(text,'2010-05-13'))

    def test_claro_vote_then_marshall_presentation(self):
        parts=self.parts(3966)
        self.assertEqual([a for t,a,m in parts],[CLARO,MARSHALL])
        self.assertTrue(parts[0][0].endswith('Claro vota por subir la TPM a 4,5%.'))
        self.assertTrue(parts[1][0].startswith('Al continuar con la votación, el Consejero señor Enrique Marshall'))
        self.assertIn('agradeciendo al staff eI apoyo',parts[1][0])
        self.assertIn('Añade que un factor de riesgo nuevo',parts[1][0])
        self.assertNotIn(3966,self.reviews)

    def test_preserves_previous_marshall_continuity_and_new_3967_link(self):
        from test_continuity import sequence
        for left,right in [(3122,3123),(3966,3967)]:
            rows=sequence([(p,self.raw[p]['Fecha'],self.raw[p]['Actor'],self.raw[p]['Texto']) for p in [left,right]])
            before=[r for r in rows if r['ID_Padre']==left][-1]
            after=next(r for r in rows if r['ID_Padre']==right)
            self.assertEqual(before['Actor_Final'],MARSHALL)
            self.assertEqual(before['ID_Turno'],after['ID_Turno'])
        self.assertEqual(self.raw[3124]['Actor'],MARFAN)
        self.assertTrue(self.raw[3124]['Texto'].startswith('El señor Manuel Marfán manifiesta'))

    def test_review_intervals_survive_and_reject_truncation(self):
        for p in [3123,3187]:
            rows=[dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p),1)]
            self.assertEqual(validate_speaker_reviews(rows,{p:self.reviews[p]}),[])
            next(r for r in rows if r['Fuente_Actor']=='CONTEXTO_REVISADO')['Texto']+=' añadido'
            self.assertTrue(validate_speaker_reviews(rows,{p:self.reviews[p]}))

    def test_changed_sources_invalidate_reviews(self):
        entries=[r for r in json.loads(SPEAKER_REVIEWS.read_text()) if r['ID_Padre'] in [3123,3187]]
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'reviews.json';path.write_text(json.dumps(entries))
            for p in [3123,3187]:
                raw=copy.deepcopy(self.raw);raw[p]['Texto']+=' cambio'
                with self.assertRaisesRegex(ValueError,'texto de origen'):
                    load_speaker_reviews(raw,path)


SOURCE_HASHES = {3123: 'c84f302301f80057608ad0c754229a67ba49fb00415d524684d51d9814b2c2f6', 3187: 'dd1a3ab5eec7f3c17674b647721fd084db357372e242755580bae90d813e7f87', 3966: 'e3c3d3154e3c2b44d5e0d8b626b4e5e44f897820ef7050c9cb666df6861b7f67'}

if __name__=='__main__':
    unittest.main()
