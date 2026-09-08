"""Regresiones positivas y negativas. No basta con contar filas/actores."""
import sys
import unittest
import re
import tempfile
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_base_referencia as builder
import qa_gate_f0 as qa
from roster import match_role
from turns import TurnDetector


class TurnTests(unittest.TestCase):
    def split(self, text, actor='Manuel Marfán Lewis', date='2006-03-16'):
        return builder.segment_turns(text, date, actor)

    def source(self, parent):
        row = next(r for r in builder.data if r[0] == parent)
        return self.split(row[5], row[2], builder.to_date_str(row[1]))

    def assert_passage_actor(self, parent, passage, expected):
        matches = [(t,a,m) for t,a,m in self.source(parent) if passage in t]
        self.assertEqual(len(matches), 1, (parent, passage))
        self.assertEqual(matches[0][1], expected)

    def test_corbo_marfan(self):
        turns = self.source(611)
        self.assertEqual([a for _,a,_ in turns], ['Vittorio Corbo Lioi', 'Manuel Marfán Lewis'])

    def test_garcia_lehmann(self):
        self.assertEqual([a for _,a,_ in self.source(2722)],
                         ['Pablo García Silva', 'Sergio Lehmann Beresi'])

    def test_lehmann_mentions_claro(self):
        turns = self.source(5403)
        self.assertEqual(len(turns), 1)
        self.assertEqual(turns[0][1], 'Sergio Lehmann Beresi')

    def test_fuentes_marcel(self):
        actors = [a for _,a,_ in self.source(7188)]
        self.assertEqual(actors, ['Miguel Fuentes Díaz', 'Mario Marcel Cullell'])

    def test_naudon_marcel(self):
        self.assertEqual([a for _,a,_ in self.source(7201)],
                         ["Alberto Naudon Dell'Oro", 'Mario Marcel Cullell'])

    def test_desormeaux_mentions_marfan_not_speaker(self):
        turns = self.source(217)
        self.assertEqual([a for _,a,_ in turns], ['Jorge Desormeaux Jiménez', 'María Elena Ovalle Molina'])
        self.assertIn('al igual que el Consejero señor Manuel Marfán', turns[0][0])

    def test_handoff_and_response(self):
        turns = self.source(506)
        self.assert_passage_actor(506, 'el Gerente mencionado indica', 'Sergio Lehmann Beresi')
        self.assert_passage_actor(506, 'consulta el señor Ministro de Hacienda', 'Nicolás Eyzaguirre Guzmán')
        self.assert_passage_actor(506, 'Exposición El señor Gerente señala', 'Sergio Lehmann Beresi')
        self.assertIn('Jorge Desormeaux Jiménez', [a for _,a,_ in turns])

    def test_subgerente_handoff(self):
        self.assert_passage_actor(1608, 'Señala el señor Subgerente General', 'Leonardo Hernández Tagle')
        self.assertEqual(self.source(1608)[0][1], 'José De Gregorio Rebeco')

    def test_same_speaker_continues(self):
        t = 'El señor García señala que hay riesgos. El señor García agrega que son acotados.'
        self.assertEqual(len(self.split(t, 'Pablo García Silva')), 1)

    def test_reference_is_not_transition(self):
        t = 'El Consejero señor Marfán señala que coincide con el Presidente señor Corbo y agradece sus comentarios.'
        self.assertEqual([a for _,a,_ in self.split(t)], ['Manuel Marfán Lewis'])

    def test_request_does_not_assign_recipient(self):
        t = 'El Presidente señor Vittorio Corbo ofrece la palabra al Consejero señor Manuel Marfán.'
        self.assertEqual([a for _,a,_ in self.split(t)], ['Vittorio Corbo Lioi'])

    def test_nested_quote_not_turn(self):
        t = 'El señor Marfán recuerda la frase “El Presidente señor Corbo señala que hay riesgos”.'
        self.assertEqual(len(self.split(t)), 1)

    def test_linebreaks_do_not_break_name(self):
        t = 'El Presidente señor Vittorio\nCorbo señala que hay riesgos. El Consejero señor Manuel\nMarfán responde que son acotados.'
        self.assertEqual([a for _,a,_ in self.split(t)], ['Vittorio Corbo Lioi','Manuel Marfán Lewis'])

    def test_subject_inversion(self):
        t = 'Al respecto, consulta el señor Ministro de Hacienda si hay riesgos.'
        self.assertEqual(self.split(t)[0][1], 'Andrés Velasco Brañes')

    def test_nominal_consulta_in_lead(self):
        t = 'En respuesta a la consulta del Consejero señor Marfán, el Presidente señor Vittorio Corbo indica que no hay cambios.'
        self.assertEqual(self.split(t)[0][1], 'Vittorio Corbo Lioi')

    def test_missing_punctuation_between_speakers(self):
        t = 'El Consejero señor Marfán señala que el escenario es favorable El Presidente señor Vittorio Corbo agrega que hay riesgos.'
        parts = self.split(t)
        self.assertEqual([a for _,a,_ in parts], ['Manuel Marfán Lewis','Vittorio Corbo Lioi'])
        self.assertEqual(re.sub(r'\s+', '', ''.join(p[0] for p in parts)), re.sub(r'\s+', '', t))

    def test_ambiguous_alias_abstains(self):
        from unittest.mock import patch
        with patch.object(builder, 'roster_role_for', return_value='Cargo'):
            self.assertIsNone(builder.strict_alias('herrera', '2007-07-12'))

    def test_duplicate_attendance_aliases_same_person(self):
        self.assertEqual(builder.strict_role('2005-04-07', 'Gerente de Análisis Macroeconómico'), 'Pablo García Silva')
        self.assertEqual(builder.strict_role('2010-09-16', 'Gerente de Análisis Internacional'), 'Sergio Lehmann Beresi')

    def test_long_text_is_incorporated_without_truncation(self):
        row = builder.load_full_texts()[297]
        parts = self.split(row['Texto_Completo'], row['Actor'], row['Fecha'])
        self.assertTrue(all(len(t) <= 32767 for t,_,_ in parts))
        self.assertEqual(re.sub(r'\s+', '', ''.join(t for t,_,_ in parts)), re.sub(r'\s+', '', row['Texto_Completo']))
        self.assertIn('CONTINUACION_XLSX', [m for _,_,m in parts])
        self.assertIn('US$ 52 y US$ 50 el 2005 y 2006', row['Texto_Completo'])

    def test_corrupt_full_text_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)/'bad.jsonl'
            p.write_text(json.dumps({'ID': 297, 'Texto_Completo': 'abc', 'Longitud_Texto_Completo': 4}))
            with self.assertRaises(ValueError):
                builder.load_full_texts(p)

    def test_duplicate_full_text_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)/'bad.jsonl'
            line=json.dumps({'ID': 297, 'Texto_Completo': 'abc', 'Longitud_Texto_Completo': 3})
            p.write_text(line+'\n'+line+'\n')
            with self.assertRaises(ValueError):
                builder.load_full_texts(p)

    def test_fuzzy_ambiguous_role_abstains(self):
        self.assertIsNone(match_role({'juan perez abc': 'R1', 'juan perez abd': 'R2'}, 'Juan Pérez ABE'))


class PDFTests(unittest.TestCase):
    def test_numbers_are_preserved(self):
        from build_textos_completos import clean_pdf_line
        for text in ['El precio fue US$ 50', '25 puntos base', '3.5% anual', 'El año 2005', '2006', '52 y US$ 50']:
            with self.subTest(text=text):
                self.assertEqual(clean_pdf_line(text), text)

    def test_footers_are_removed(self):
        from build_textos_completos import clean_pdf_line
        for text in ['12.07.2005 2.-','12.07.2005 9.', '12.07.2005', 'Sesión N° 80', 'Política monetaria', '8.-']:
            with self.subTest(text=text):
                self.assertEqual(clean_pdf_line(text), '')


class IntegrityTests(unittest.TestCase):
    def fixture(self):
        import datetime as dt
        from crear_consolidado_final import SOURCE_COLUMNS
        raw={'ID':1, 'Fecha':dt.datetime(2005,1,11), 'Pagina':1, 'Texto':'Texto de prueba.', 'Actor':'Vittorio Corbo Lioi', 'Rol':'Presidente del Banco Central'}
        row={'ID':1,'ID_Padre':1,'Fecha':raw['Fecha'],'Página':1,'Id_Sesion':'RPM-2005-01-11',
             'ID_Intervencion':'RPM-2005-01-11:1:1','ID_Bloque_Texto':'RPM-2005-01-11:1:B1','Numero_Segmento':1,
             'Actor_Final':raw['Actor'],'Rol_Final':raw['Rol'],'Texto':raw['Texto'],
             'Fuente_Actor':'ORIGINAL','Fuente_Rol':'PENDIENTE_REVISION','Fuente_Texto':'XLSX_ORIGINAL',
             'Texto_Truncado':'NO','Duplicado_Exacto':'NO','Duplicado_Formula':'NO','Duplicado_Exacto_Origen':'NO',
             'Tipo_Acta':None,'Tema_Original':'inflación','Tema_Categoria':'inflacion',
             'Palabra_Clave_Original':'inflación','Palabra_Clave_Categoria':'inflacion',
             'Estado_Revision':'PENDIENTE_REVISION','Motivos_Revision':'CARGO_SIN_CONFIRMACION_ASISTENCIA'}
        from continuity import annotate_turns
        annotate_turns([row])
        final={k:row[k] for k in SOURCE_COLUMNS}
        return row,raw,final

    def test_valid_fixture(self):
        from qa_preparacion import validate
        row,raw,final=self.fixture()
        self.assertEqual(validate([row],[raw],{},[final]),[])

    def test_text_loss_fails(self):
        from qa_preparacion import validate
        row,raw,final=self.fixture()
        row['Texto']='Texto.'
        self.assertTrue(any('pérdida/alteración' in e for e in validate([row],[raw],{},[final])))

    def test_wrong_duplicate_flag_fails(self):
        from qa_preparacion import validate
        row,raw,final=self.fixture()
        row['Duplicado_Exacto']='SI'
        self.assertTrue(any('duplicado incorrecto' in e for e in validate([row],[raw],{},[final])))

    def test_final_projection_mismatch_fails(self):
        from qa_preparacion import validate
        row,raw,final=self.fixture()
        final['Texto']='Otro texto.'
        self.assertTrue(any('proyección distinta' in e for e in validate([row],[raw],{},[final])))


class CategoryTests(unittest.TestCase):
    def test_accents(self):
        for text, category in [('inflación','inflacion'), ('votación','decision_tpm'),
                               ('discusión','debate'), ('inversión','actividad_interna'),
                               ('actividad económica','actividad_interna'), ('suspensión','apertura_cierre')]:
            with self.subTest(text=text):
                self.assertEqual(builder.cat(text), category)
                self.assertEqual(builder.cat(builder.norm(text)), category)


class DecisionTests(unittest.TestCase):
    def test_percentage_point_delta(self):
        self.assertEqual(qa.parse_decision('El Consejo acordó aumentar la tasa de política monetaria en 0,25% hasta 3,5% anual.'), ('aumentar',25,3.5))

    def test_multiline_decision(self):
        self.assertEqual(qa.parse_decision('Se acuerda\naumentar la tasa de política\nmonetaria en 25 puntos base, hasta 3,5% anual.'), ('aumentar',25,3.5))

    def test_from_to(self):
        self.assertEqual(qa.parse_decision('Se acuerda reducir la TPM desde 5,25% a 5% anual.'), ('reducir',-25,5.0))

    def test_target_and_delta_must_both_match(self):
        self.assertFalse(qa.decision_matches_reference(('aumentar',25,4.0),3.0,3.25,25))
        self.assertFalse(qa.decision_matches_reference(('aumentar',50,3.25),3.0,3.25,25))
        self.assertTrue(qa.decision_matches_reference(('aumentar',25,3.25),3.0,3.25,25))

    def test_verb_sign_must_match(self):
        self.assertFalse(qa.decision_matches_reference(('reducir',None,3.25),3.0,3.25,25))

    def test_recap_not_current(self):
        t='En la reunión de política monetaria de enero, el Consejo acordó mantener la tasa de política monetaria en 3%.'
        self.assertFalse(builder._is_current_decision(t))
        self.assertEqual(qa.extract_decision_rows([{'Texto':t}]), [])

    def test_missing_coverage_fails(self):
        self.assertFalse(qa.audit([], [])['pasa'])

    def test_multiple_formulas_in_one_sentence(self):
        import datetime as dt
        rows=[{'ID':1,'Actor_Final':qa.CONSEJO,'Fecha_str':'2005-01-11','Tipo_Acta':'ACUERDO_CONSEJO',
               'Texto':'Se acuerda mantener la TPM en 3%; se acuerda mantener la TPM en 4%.'}]
        result=qa.audit(rows,[(dt.date(2004,1,1),3.0)])
        self.assertTrue(any('referencia' in e for e in result['errores']))

    def test_contradictory_candidates_fail(self):
        import datetime as dt
        rows=[]
        for i,rate in enumerate([3.0,4.0]):
            rows.append({'ID':i,'Actor_Final':qa.CONSEJO,'Fecha_str':'2005-01-11',
                         'Tipo_Acta':'ACUERDO_CONSEJO','Texto':f'Se acuerda mantener la TPM en {rate}% anual.'})
        result=qa.audit(rows,[(dt.date(2004,1,1),3.0)])
        self.assertTrue(any('ID 1:' in e and 'referencia' in e for e in result['errores']))


if __name__ == '__main__':
    unittest.main()
