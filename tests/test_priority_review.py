"""Cesión relativa, intercambio Ministro/Lehmann y primer lote de prioridades."""
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
from curation import load_speaker_reviews, validate_speaker_reviews, SPEAKER_REVIEWS

PRES = 'José De Gregorio Rebeco'
CESPEDES = 'Luis Felipe Céspedes Cifuentes'
VELASCO = 'Andrés Velasco Brañes'
LEHMANN = 'Sergio Lehmann Beresi'
DESORMEAUX = 'Jorge Desormeaux Jiménez'
CLARO = 'Sebastián Claro Edwards'
SOTO = 'Claudio Soto Gamboa'
GARCIA = 'Pablo García Silva'
MARFAN = 'Manuel Marfán Lewis'
PARENTS = (2644,2661,2785,2805,2855)
RELATIVE = 'quien comienza su exposición señalando que la inflación converge a la meta.'
HANDOFF = 'El Presidente concede la palabra al Gerente de Investigación Económica, señor Luis Felipe Céspedes, '


class PriorityReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews = load_speaker_reviews(cls.raw)

    def parts(self,p,review=None):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p) if review is None else review)

    def relative(self,prefix=HANDOFF,fragment=RELATIVE,actor=CESPEDES):
        text=prefix+fragment
        review=dict(Inicio=len(prefix),Fin=len(text),Actor=actor,Tipo_Limite='CESION_RELATIVA_EXPLICITA')
        return b.segment_turns(text,'2009-07-09',PRES,review=review)

    def test_fixed_source_hashes(self):
        self.assertEqual(set(SOURCE_HASHES),set(PARENTS))
        for p,h in SOURCE_HASHES.items():
            self.assertEqual(hashlib.sha256(self.raw[p]['Texto'].encode()).hexdigest(),h)

    def test_complete_source_conservation(self):
        compact=lambda t:re.sub(r'\s+','',t)
        for p in PARENTS:
            self.assertEqual(compact(''.join(t for t,a,m in self.parts(p))),compact(self.raw[p]['Texto']))

    def test_cespedes_full_exposition_between_chair_handoffs(self):
        parts=self.parts(2644)
        self.assertEqual([a for t,a,m in parts],[PRES,CESPEDES,PRES])
        self.assertEqual([len(t) for t,a,m in parts],[99,4101,142])
        self.assertTrue(parts[1][0].startswith('quien comienza su exposición señalando que'))
        self.assertIn('Lo anterior, manifiesta el señor Céspedes',parts[1][0])
        self.assertIn('El Gerente de Investigación Económica agrega',parts[1][0])
        self.assertIn('escenario de nesgo',parts[1][0])
        self.assertTrue(parts[2][0].endswith('señor Beltrán De Ramón.'))
        self.assertEqual(parts[1][2],'CONTEXTO_REVISADO')

    def test_relative_does_not_become_a_global_rule(self):
        r=self.raw[2644]
        plain=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertEqual(len(plain[0][0]),3067)
        self.assertEqual(plain[0][1],PRES)
        self.assertEqual({p for p,r in self.reviews.items() if r.get('Tipo_Limite')=='CESION_RELATIVA_EXPLICITA'},{2644})

    def test_valid_relative_keeps_literal_pronoun(self):
        parts=self.relative()
        self.assertEqual([a for t,a,m in parts],[PRES,CESPEDES])
        self.assertEqual(parts[1][0],RELATIVE)
        self.assertTrue(parts[0][0].endswith('Céspedes,'))

    def test_relative_rejects_wrong_recipient(self):
        with self.assertRaisesRegex(ValueError,'límite válido'):
            self.relative(actor=SOTO)

    def test_relative_requires_actual_exposition_not_invitation_or_future(self):
        for fragment in ['quien está presente en la sesión.',
                         'quien comenzará su exposición señalando que la inflación bajará.',
                         'quien debería comenzar su exposición señalando que la inflación bajará.',
                         'quien comienza su exposición sobre inflación.',
                         'para que comience su exposición señalando que la inflación bajará.']:
            with self.subTest(fragment=fragment),self.assertRaisesRegex(ValueError,'límite válido'):
                self.relative(fragment=fragment)

    def test_relative_requires_single_complete_giver_and_recipient(self):
        for prefix in [HANDOFF.replace('Céspedes,','Céspedes y el señor Soto,'),
                       HANDOFF.replace('El Presidente','Según el Presidente'),
                       HANDOFF.replace('El Presidente','El Presidente recuerda que el señor Marshall'),
                       HANDOFF.replace('Gerente de Investigación Económica, señor Luis Felipe Céspedes','señor Desconocido'),
                       HANDOFF.replace('concede la palabra','menciona'),
                       HANDOFF.replace('Céspedes,','Céspedes con quien discutió,')]:
            with self.subTest(prefix=prefix),self.assertRaisesRegex(ValueError,'límite válido'):
                self.relative(prefix=prefix)

    def test_relative_rejects_missing_comma_and_noncontiguous_handoff(self):
        for prefix in [HANDOFF.rstrip(', ')+ ' ',HANDOFF.rstrip(', ')+'. ',
                       HANDOFF.rstrip(', ')+'. El señor Marshall agrega, ']:
            with self.subTest(prefix=prefix),self.assertRaisesRegex(ValueError,'límite válido'):
                self.relative(prefix=prefix)

    def test_relative_rejects_quotation(self):
        for l,r in [('“','”'),('«','»'),('"','"')]:
            with self.subTest(quote=l),self.assertRaisesRegex(ValueError,'límite válido'):
                self.relative(prefix=l+HANDOFF,fragment=RELATIVE+r)

    def test_2661_minister_and_lehmann_both_recovered(self):
        parts=self.parts(2661)
        self.assertEqual([a for t,a,m in parts],
                         [VELASCO,LEHMANN,DESORMEAUX,LEHMANN,DESORMEAUX,LEHMANN,LEHMANN,VELASCO,PRES,VELASCO,LEHMANN,CLARO])
        self.assertEqual(parts[9][0],'El efecto debiera ser menor y al revés, acota el Ministro,')
        self.assertEqual(parts[10][0],'y el señor Lehmann complementa que será necesario afinar el análisis.')
        self.assertEqual(parts[9][2],'SUJETO_ROL_SESION')
        self.assertEqual(parts[10][2],'CONTEXTO_REVISADO')
        self.assertTrue(parts[11][0].startswith('Sobre ese mismo punto'))

    def test_2661_previous_turns_and_passive_posterior_anchor_preserved(self):
        parts=self.parts(2661);r=self.raw[2661]
        plain=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertEqual(parts[:4],plain[:4])
        self.assertEqual(parts[6:9],plain[5:8])
        self.assertEqual(len(parts[6][0]),1322)
        self.assertEqual(parts[5],('acotación que es confirmada por el señor Lehmann.',LEHMANN,'CONTEXTO_REVISADO'))
        self.assertEqual(' '.join(t for t,a,m in parts[4:6]),plain[4][0])
        self.assertIn('Explica que si los inmigrantes tienen habilidades',parts[8][0])
        self.assertEqual(len(plain),10)
        self.assertIn('y el señor Lehmann complementa',plain[-2][0])

    def test_minister_prefix_is_narrow_and_preserves_reference_guards(self):
        for text in ['El efecto debiera ser menor y al revés, según el Ministro, el mercado cambia.',
                     'El efecto debiera ser menor y al revés, como acota el Ministro, cambia el escenario.',
                     'El efecto podría ser mayor, acota el Ministro.',
                     '“El efecto debiera ser menor y al revés, acota el Ministro.”']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(text,'2009-08-13'))

    def test_2785_soto_reply_and_presentation_remain_together(self):
        parts=self.parts(2785)
        self.assertEqual([a for t,a,m in parts],[CLARO,SOTO])
        self.assertEqual(len(parts[1][0]),1528)
        self.assertTrue(parts[1][0].startswith('a lo cual, el señor Claudio Soto responde'))
        self.assertIn('El Gerente de Análisis Macroeconómico retoma su presentación',parts[1][0])
        self.assertIn('UF mayores Luego',parts[0][0])

    def test_comma_reply_retains_explicit_anchor_and_next_paragraph(self):
        from test_continuity import sequence
        self.assertNotIn(2785,self.reviews)
        self.assertEqual(self.parts(2785)[1][2],'SUJETO_NOMBRE')
        paragraphs=[(p,self.raw[p]['Fecha'],self.raw[p]['Actor'],self.raw[p]['Texto']) for p in [2785,2786]]
        rows=sequence(paragraphs)
        reply=next(r for r in rows if r['ID_Padre']==2785 and r['Actor_Final']==SOTO)
        following=next(r for r in rows if r['ID_Padre']==2786)
        self.assertEqual(reply['ID_Turno'],following['ID_Turno'])
        self.assertEqual(following['Relacion_Turno'],'CONTINUIDAD_EXPLICITA')

    def test_comma_reply_keeps_quote_separator_and_subject_guards(self):
        for text in ['El señor Claro señala: “Las tasas bajan, a lo cual, el señor Soto responde que suben.”',
                     'El señor Claro señala algo a lo cual, el señor Soto responde que suben.',
                     'El señor Claro señala que las tasas bajan, a lo cual, el señor Soto está atento.']:
            parts=b.segment_turns(text,'2009-11-12',CLARO)
            self.assertEqual([a for t,a,m in parts],[CLARO])

    def test_2805_president_close_does_not_fragment_previous_presenter(self):
        parts=self.parts(2805)
        self.assertEqual([a for t,a,m in parts],[LEHMANN,MARFAN,LEHMANN,MARFAN,GARCIA,PRES])
        self.assertEqual(len(parts[0][0]),4385)
        self.assertTrue(parts[-1][0].startswith('Esa es una decisión que han adoptado'))
        self.assertEqual(len(parts[-1][0]),139)

    def test_2855_soto_presentation_not_chair(self):
        parts=self.parts(2855)
        self.assertEqual([a for t,a,m in parts],[PRES,SOTO])
        self.assertEqual(len(parts[1][0]),1026)
        self.assertIn('da inicio a su presentación',parts[1][0])
        self.assertIn('A nivel sectorial, el señor Claudio Soto menciona',parts[1][0])

    def test_all_reviewed_intervals_are_exact(self):
        for p in set(PARENTS)&self.reviews.keys():
            rows=[dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p),1)]
            self.assertEqual(validate_speaker_reviews(rows,{p:self.reviews[p]}),[])
            next(r for r in rows if r['Fuente_Actor']=='CONTEXTO_REVISADO')['Texto']+=' añadido'
            self.assertTrue(validate_speaker_reviews(rows,{p:self.reviews[p]}))

    def test_changed_source_invalidates_each_review(self):
        entries=[e for e in json.loads(SPEAKER_REVIEWS.read_text()) if e['ID_Padre'] in PARENTS]
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'reviews.json';path.write_text(json.dumps(entries))
            for p in set(PARENTS)&self.reviews.keys():
                raw=copy.deepcopy(self.raw);raw[p]['Texto']+=' Cambio.'
                with self.assertRaisesRegex(ValueError,'texto de origen'):
                    load_speaker_reviews(raw,path)


SOURCE_HASHES = {2644: 'ae1569d32298477457ba5b1aa72c320ca31d97394f54ce521043c9cb9dd751cb', 2661: 'ba871e522560a087da27e178ffbdc31badc52e41f09e7fa9b434fb31d9a632c4', 2785: '825dbd4c482de6443f3a7ec8cdfc944325ab880d82f71aec565499b0c70a9e8f', 2805: '932234f15936d5c993a83019c0833d3699871eeac5304df12b7afaa03d4400b7', 2855: 'eb4218cbe44c2721cdf95cb802e0f9da9c381168075ee768487ac0b9f45e5fdc'}

if __name__ == '__main__':
    unittest.main()
