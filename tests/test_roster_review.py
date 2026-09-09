"""Regresiones de listas de asistentes y lectura contextual de la ronda adicional."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from roster import parse_opening, match_role, canonical_role
from curation import load_speaker_reviews, validate_speaker_reviews
from turns import normalize


class RosterReviewTests(unittest.TestCase):
    def test_real_councillor_lists_stop_before_other_attendees(self):
        expected={'manuel marfan lewis','enrique marshall rivera','sebastian claro edwards'}
        for date in ['2008-06-10','2009-02-12']:
            with self.subTest(date=date):
                roster=b.ROSTER_BY_DATE[date]
                self.assertEqual({n for n,r in roster.items() if r=='Consejero/a'},expected)
                for actor,role in [('Claudio Soto Gamboa','Gerente de Análisis Macroeconómico'),
                                   ('Pablo García Silva','Gerente de División Estudios'),
                                   ('Sergio Lehmann Beresi','Gerente de Análisis Internacional'),
                                   ('Kevin Cowan Logan','Gerente de División Política Financiera'),
                                   ('Beltrán de Ramón Acevedo','Gerente de División Operaciones Financieras'),
                                   ('Matías Bernier Bórquez','Gerente de Mercados Financieros Nacionales')]:
                    self.assertEqual(b.roster_role_for(date,actor),role)

    def test_list_delimiters(self):
        prefix='En Santiago de Chile, con la asistencia del Vicepresidente don Jorge Desormeaux Jiménez y de los Consejeros don Manuel Marfán Lewis, don Enrique Marshall Rivera y don Sebastián Claro Edwards'
        for separator in ['. Asisten también: ', ', Asisten también: ', '; Asiste ', '. ', ', ']:
            with self.subTest(separator=separator):
                roster=parse_opening(prefix+separator+'Ministra de Hacienda Subrogante, doña María Olivia Recart Herrera; Gerente de Análisis Macroeconómico, don Claudio Soto Gamboa.')
                self.assertEqual(sum(r=='Consejero/a' for r in roster.values()),3)
                self.assertEqual(match_role(roster,'Claudio Soto Gamboa'),'Gerente de Análisis Macroeconómico')
                self.assertEqual(match_role(roster,'María Olivia Recart Herrera'),'Ministra de Hacienda (S)')

    def test_macroeconomic_role_resolves_in_affected_session(self):
        self.assertEqual(b.strict_role('2009-02-12','Gerente de Análisis Macroeconómico'),'Claudio Soto Gamboa')

    def test_congratulation_belongs_to_minister_not_recipient(self):
        r=next(r for r in b.data if r[0]==1600)
        parts=b.segment_turns(r[5],b.to_date_str(r[1]),r[2])
        self.assertEqual([a for t,a,m in parts],['Andrés Velasco Brañes'])
        self.assertEqual(parts[0][0],r[5])

    def test_madgenzo_ocr_keeps_original_text(self):
        for p in [958,961,967]:
            r=next(r for r in b.data if r[0]==p)
            with self.subTest(parent=p):
                parts=b.segment_turns(r[5],b.to_date_str(r[1]),r[2])
                self.assertTrue(parts[0][2].startswith('SUJETO_'))
                self.assertEqual(parts[0][1],'Igal Magendzo Weinberger')
                self.assertIn('Madgenzo',''.join(t for t,a,m in parts))

    def test_madgenzo_replies_are_not_absorbed_by_other_speakers(self):
        r=next(r for r in b.data if r[0]==1003)
        parts=b.segment_turns(r[5],b.to_date_str(r[1]),r[2])
        self.assertEqual([a for t,a,m in parts],['Vittorio Corbo Lioi','José De Gregorio Rebeco',
            'Igal Magendzo Weinberger','José De Gregorio Rebeco','Rodrigo Valdés Pulido',
            'Igal Magendzo Weinberger','Andrés Velasco Brañes','Igal Magendzo Weinberger',
            'Vittorio Corbo Lioi','Rodrigo Valdés Pulido'])

    def test_roster_fix_recovers_garcia_reply_without_cutting_soto_mention(self):
        r=next(r for r in b.data if r[0]==1879)
        parts=b.segment_turns(r[5],b.to_date_str(r[1]),r[2])
        self.assertEqual([a for t,a,m in parts],['Jorge Desormeaux Jiménez','Claudio Soto Gamboa','Pablo García Silva'])
        self.assertIn('Tal como lo ha explicado el Gerente señor Claudio Soto',parts[-1][0])

    def test_ocr_normalization_is_idempotent_and_bounded(self):
        for text in ['Igal Madgenzo','El Presidente seño Rodrigo Vergara','El Ministro de Hacienda seños Rodrigo Valdés']:
            self.assertEqual(normalize(normalize(text)),normalize(text))
        self.assertEqual(normalize('en el seno del Consejo'),'en el seno del consejo')


class ContextReviewTests(unittest.TestCase):
    def setUp(self):
        self.raw={r[0]:{'Fecha':b.to_date_str(r[1]),'Texto':r[5],'Actor':r[2]} for r in b.data}
        self.reviews=load_speaker_reviews(self.raw)

    def parts(self,p):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews[p])

    def test_soto_exposition_then_marfan_question(self):
        parts=self.parts(2336)
        self.assertEqual([a for t,a,m in parts],['Claudio Soto Gamboa','Manuel Marfán Lewis'])
        self.assertTrue(parts[-1][0].startswith('En relación a un comentario'))
        self.assertEqual(parts[-1][2],'CONTEXTO_REVISADO')

    def test_foreign_president_is_topic_not_local_speaker(self):
        parts=self.parts(6394)
        self.assertEqual([a for t,a,m in parts],['Sergio Lehmann Beresi'])
        self.assertEqual(parts[0][2],'CONTEXTO_REVISADO')
        self.assertEqual(parts[0][0],self.raw[6394]['Texto'])
        self.assertIsNone(b.TURN_DETECTOR.speaker(self.reviews[6394]['Cita_Inicio'],'2014-09-11'))

    def test_all_documented_intervals_survive(self):
        rows=[]
        for p in self.reviews:
            rows.extend(dict(ID=len(rows)+i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m)
                        for i,(t,a,m) in enumerate(self.parts(p),1))
        self.assertEqual(validate_speaker_reviews(rows,self.reviews),[])

    def test_no_generalization_of_foreign_president_review(self):
        r=self.raw[6394]
        # Sin decisión dirigida no sustituir automáticamente el actor original.
        parts=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertNotEqual(parts[0][2],'CONTEXTO_REVISADO')


if __name__=='__main__':
    unittest.main()
