"""Regresiones de la revisión dirigida: citas, cargos, minutas y verbos explícitos."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from turns import normalize
from curation import load_role_reviews, ROLE_REVIEWS
from qa_preparacion import validate


class DirectedSpeakerTests(unittest.TestCase):
    def row(self,parent):
        return next(r for r in b.data if r[0]==parent)

    def parts(self,parent):
        r=self.row(parent)
        return b.segment_turns(r[5],b.to_date_str(r[1]),r[2])

    def test_marfan_ocr_not_jadresic(self):
        self.assertEqual([a for _,a,_ in self.parts(702)],['Manuel Marfán Lewis'])
        self.assertTrue(self.parts(702)[0][2].startswith('SUJETO_'))

    def test_ocr_variants_are_only_recognition(self):
        r=self.row(702)
        self.assertIn('Mari^án',self.parts(702)[0][0])
        self.assertEqual(self.parts(702)[0][0],r[5].strip())

    def test_ocr_normalization_is_idempotent(self):
        for t in ['Sergio Lehman','Sergio Lehmann','Luis Osear Herrera','Manuel Mari^án', 'E1 Presidente', 'Jorge Desorm eaux']:
            with self.subTest(text=t):
                self.assertEqual(normalize(normalize(t)),normalize(t))
        self.assertIn('sergio lehmann',normalize('Sergio Lehmann'))
        self.assertNotIn('lehmannn',normalize('Sergio Lehmann'))

    def test_explicit_locutions(self):
        examples={85:'Manuel Marfán Lewis',98:'Pablo García Silva',112:'Mario Marcel Cullell',
                  162:'Manuel Marfán Lewis',564:'José De Gregorio Rebeco',607:'Rodrigo Valdés Pulido',
                  854:'Rodrigo Valdés Pulido',1245:'Manuel Marfán Lewis',1290:'Andrés Velasco Brañes'}
        for parent,actor in examples.items():
            with self.subTest(parent=parent):
                parts=self.parts(parent)
                self.assertEqual(parts[0][1],actor)
                self.assertTrue(parts[0][2] and parts[0][2].startswith('SUJETO_'),parts[0])

    def test_intention_is_not_recipient_speech(self):
        t='El Consejero señor Marfán quiere que el Presidente señor Corbo explique el escenario.'
        self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2005-02-10'))

    def test_anade_starts_real_reply(self):
        t='El señor Pablo García señala que no hay sorpresas. El Consejero señor Marfán añade que hay riesgos.'
        parts=b.segment_turns(t,'2005-02-10','Pablo García Silva')
        self.assertEqual([a for _,a,_ in parts],['Pablo García Silva','Manuel Marfán Lewis'])

    def test_personal_minutes_are_authored_not_dialogue(self):
        for parent,actor in [(196,'Vittorio Corbo Lioi'),(197,'José De Gregorio Rebeco'),(198,'María Elena Ovalle Molina')]:
            with self.subTest(parent=parent):
                self.assertEqual(self.parts(parent),[(self.row(parent)[5],actor,'ENCABEZADO_MINUTA')])

    def test_mention_of_minute_is_not_authorship(self):
        self.assertIsNone(b.TURN_DETECTOR.minute_author('El Consejero señor Marfán comenta la minuta del Presidente señor Corbo.', '2005-03-10'))

    def test_multiple_minutes_not_swallowed(self):
        t=self.row(196)[5]+' '+self.row(197)[5]
        self.assertIsNone(b.TURN_DETECTOR.minute_author(t,'2005-03-10'))

    def test_unclosed_minute_abstains(self):
        self.assertIsNone(b.TURN_DETECTOR.minute_author(self.row(196)[5][:-1],'2005-03-10'))

    def test_state_is_reset_before_segmenting_new_session(self):
        state={'date':'2005-01-11','actor':'Vittorio Corbo Lioi','anchor':1,
               'roles':{'Gerente':'Pablo García Silva'},'last_sentence':'El Gerente señor Pablo García señala que hay riesgos.'}
        b.segment_turns('La actividad aumenta.','2005-02-10','Vittorio Corbo Lioi',state)
        self.assertEqual(state['date'],'2005-02-10')
        self.assertNotIn('anchor',state)
        self.assertNotIn('Gerente',state.get('roles',{}))


class DocumentedRoleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={int(r[0]):{'Fecha':b.to_date_str(r[1]),'Texto':r[5]} for r in b.data}
        cls.entries=json.loads(ROLE_REVIEWS.read_text())

    def load(self,entries=None,raw=None):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'roles.json'
            path.write_text(json.dumps(entries if entries is not None else self.entries))
            return load_role_reviews(self.raw if raw is None else raw,path)

    def test_six_role_decisions_have_verified_quotes(self):
        reviews=self.load()
        self.assertEqual(len(reviews),6)
        self.assertEqual({p for p,a in reviews},{41,234,243,246,406,980})

    def test_direct_and_session_evidence_are_distinguished(self):
        reviews=self.load()
        self.assertEqual(sum(r['Fuente_Rol']=='TEXTO_EXPLICITO_REVISADO' for r in reviews.values()),4)
        self.assertEqual(sum(r['Fuente_Rol']=='CONTEXTO_SESION_REVISADO' for r in reviews.values()),2)

    def test_changed_source_blocks_review(self):
        raw=copy.deepcopy(self.raw)
        raw[41]['Texto']+=' Cambio.'
        with self.assertRaisesRegex(ValueError,'cambió el texto'):
            self.load(raw=raw)

    def test_missing_quote_blocks_review(self):
        entries=copy.deepcopy(self.entries)
        entries[0]['Evidencia'][0]['Cita']='Texto inexistente'
        with self.assertRaisesRegex(ValueError,'cita'):
            self.load(entries)

    def test_evidence_from_other_session_rejected(self):
        entries=copy.deepcopy(self.entries)
        entries[0]['Evidencia'][0]['ID_Padre']=243
        with self.assertRaisesRegex(ValueError,'misma sesión'):
            self.load(entries)

    def test_duplicate_review_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicada'):
            self.load(self.entries+[self.entries[0]])

    def test_role_not_in_quote_rejected(self):
        entries=copy.deepcopy(self.entries)
        entries[0]['Rol']='Consejero'
        with self.assertRaisesRegex(ValueError,'cargo y nombre'):
            self.load(entries)

    def test_not_mislabelled_attendance(self):
        entries=copy.deepcopy(self.entries)
        entries[0]['Fuente_Rol']='LISTA_ASISTENCIA'
        with self.assertRaisesRegex(ValueError,'fuente inválida'):
            self.load(entries)

    def test_forged_reviewed_role_in_output_fails_f1(self):
        from test_preparation import IntegrityTests
        row,raw,final=IntegrityTests().fixture()
        row['Fuente_Rol']='TEXTO_EXPLICITO_REVISADO'
        errors=validate([row],[raw],{},[final])
        self.assertTrue(any('sin evidencia aplicable' in e for e in errors))


class ReviewedResumptionTests(unittest.TestCase):
    def setUp(self):
        from curation import load_speaker_reviews
        self.raw={int(r[0]):{'Fecha':b.to_date_str(r[1]),'Texto':r[5]} for r in b.data}
        self.reviews=load_speaker_reviews(self.raw)
        self.review=self.reviews[2110]

    def parts(self):
        return b.segment_turns(self.raw[2110]['Texto'],'2008-10-09','Pablo García Silva',review=self.review)

    def rows(self):
        return [dict(ID=i,ID_Padre=2110,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(),1)]

    def test_expositor_resumes_after_short_garcia_comment(self):
        parts=self.parts()
        self.assertEqual([a for t,a,m in parts],['Pablo García Silva','Felipe Jaque','Pablo García Silva','Felipe Jaque'])
        self.assertEqual(parts[-1][2],'CONTEXTO_REVISADO')
        self.assertTrue(parts[-1][0].startswith(self.review['Cita_Inicio']))
        self.assertEqual(parts[-1][0],self.review['_Texto_Intervalo'])
        self.assertNotIn('Refiriéndose',parts[-2][0])

    def test_reviewed_resumption_passes_f1(self):
        from curation import validate_speaker_reviews
        self.assertEqual(validate_speaker_reviews(self.rows(),{2110:self.review}),[])

    def test_forged_resumption_fails(self):
        from curation import validate_speaker_reviews
        rows=self.rows();rows[-1]['Actor_Final']='Pablo García Silva'
        self.assertTrue(validate_speaker_reviews(rows,self.reviews))

    def test_truncated_reviewed_interval_fails(self):
        from curation import validate_speaker_reviews
        rows=self.rows();rows[-1]['Texto']=rows[-1]['Texto'][:-20]
        self.assertTrue(validate_speaker_reviews(rows,self.reviews))

    def test_missing_review_fails(self):
        from curation import validate_speaker_reviews
        self.assertTrue(validate_speaker_reviews(self.rows(),{}))
        self.assertTrue(validate_speaker_reviews([],self.reviews))

    def test_changed_parent_invalidates_resumption(self):
        from curation import load_speaker_reviews
        self.raw[2110]['Texto']+=' cambio'
        with self.assertRaisesRegex(ValueError,'cambió el texto'):
            load_speaker_reviews(self.raw)

    def test_review_must_start_on_sentence_boundary(self):
        self.review['Inicio']+=1
        with self.assertRaisesRegex(ValueError,'límite válido'):
            self.parts()

    def test_minute_followed_by_quoted_speech_is_not_swallowed(self):
        minute=next(r[5] for r in b.data if r[0]==196)
        text=minute+' El Consejero señor Marfán señala: “No estoy de acuerdo.”'
        self.assertIsNone(b.TURN_DETECTOR.minute_author(text,'2005-03-10'))

    def test_long_minute_keeps_all_characters_in_bounded_cells(self):
        text='Minuta del Presidente señor Corbo: “'+'La inflación sigue estable. '*1600+'”'
        parts=b.segment_turns(text,'2005-03-10','Vittorio Corbo Lioi')
        self.assertGreater(len(parts),1)
        self.assertEqual(parts[0][2],'ENCABEZADO_MINUTA')
        self.assertTrue(all(len(t)<=32767 for t,a,m in parts))
        import re
        self.assertEqual(re.sub(r'\s+','',''.join(t for t,a,m in parts)),re.sub(r'\s+','',text))

    def test_detected_new_turns_regressions(self):
        expected={1815:['Jorge Desormeaux Jiménez','Sergio Lehmann Beresi','José De Gregorio Rebeco'],
                  1450:['Jorge Desormeaux Jiménez','José De Gregorio Rebeco'],
                  1621:['José De Gregorio Rebeco','Sergio Lehmann Beresi','Manuel Marfán Lewis','Sergio Lehmann Beresi','Andrés Velasco Brañes'],
                  2261:['Claudio Soto Gamboa','Sebastián Claro Edwards','Claudio Soto Gamboa'],
                  2993:['José De Gregorio Rebeco','Claudio Soto Gamboa'],
                  6156:['Matías Bernier Bórquez','Rodrigo Vergara Montes'],
                  6733:['Miguel Fuentes Díaz','Alberto Arenas de Mesa','Miguel Fuentes Díaz']}
        for parent,actors in expected.items():
            r=next(r for r in b.data if r[0]==parent)
            with self.subTest(parent=parent):
                parts=b.segment_turns(r[5],b.to_date_str(r[1]),r[2])
                self.assertEqual([a for t,a,m in parts],actors)


if __name__=='__main__':
    unittest.main()
