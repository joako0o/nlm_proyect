"""El triaje de puntuación no modifica filas ni convierte indicios en cierres."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import diagnosticar_finales as d


def row(i=1, parent=10, actor='Persona A', text='Pregunta,', **kw):
    value = dict(ID=i, ID_Padre=parent, ID_Intervencion=f'RPM-2000-01-01:{parent}:{i}',
                 Fecha='2000-01-01', Actor_Final=actor, Texto=text, Fuente_Actor='SUJETO_NOMBRE',
                 ID_Turno=f'T{i}', ID_Antecedente_Continuidad='', Motivos_Revision=d.MOTIVE)
    value.update(kw)
    return value


class DiagnosticTests(unittest.TestCase):
    def test_no_mutation_or_adjudication(self):
        rows = [row(), row(2, actor='Persona B', text='Responde.')]
        before = copy.deepcopy(rows)
        result = d.diagnose(rows)
        self.assertEqual(rows, before)
        self.assertEqual(result[0]['Estado'], 'CANDIDATO_NO_ADJUDICADO')
        self.assertEqual(result[0]['SHA256_Texto_Exportado'], d.sha('Pregunta,'))
        self.assertEqual(result[0]['Siguiente']['Texto'], 'Responde.')

    def test_comma_different_actor_in_same_parent(self):
        self.assertEqual(d.pattern(row(), row(2, actor='Persona B')), 'COMA_ANTES_DE_OTRO_ACTOR_EN_PADRE')

    def test_institution_is_not_claimed_to_be_personal_voice(self):
        a = row(actor='Consejo del Banco Central de Chile', text='Se reanuda,')
        self.assertEqual(d.pattern(a, row(2)), 'COMA_ANTES_DE_OTRO_ACTOR_EN_PADRE')
        self.assertEqual(d.diagnose([a])[0]['Actor'], a['Actor_Final'])

    def test_same_actor_same_parent_not_a_new_voice(self):
        self.assertEqual(d.pattern(row(), row(2)), 'COMA_OTRO_CONTEXTO')
        self.assertEqual(d.relation(row(), row(2)), 'MISMO_PADRE_MISMO_ACTOR')

    def test_existing_cross_parent_link_requires_matching_antecedent(self):
        a = row(); b = row(2, parent=11, ID_Turno=a['ID_Turno'], ID_Antecedente_Continuidad=a['ID_Intervencion'])
        self.assertEqual(d.pattern(a, b), 'COMA_CON_ENLACE_YA_EXISTENTE')
        b['ID_Antecedente_Continuidad'] = 'no-coincide'
        self.assertEqual(d.pattern(a, b), 'COMA_MISMO_ACTOR_SIN_ENLACE')

    def test_same_actor_does_not_imply_link(self):
        self.assertEqual(d.pattern(row(), row(2, parent=11)), 'COMA_MISMO_ACTOR_SIN_ENLACE')

    def test_date_change_is_not_continuity_even_if_ids_match(self):
        a = row(); b = row(2, parent=11, Fecha='2000-02-01', ID_Turno=a['ID_Turno'], ID_Antecedente_Continuidad=a['ID_Intervencion'])
        self.assertEqual(d.relation(a, b), 'OTRA_SESION')
        self.assertEqual(d.pattern(a, b), 'COMA_OTRO_CONTEXTO')

    def test_no_following_row(self):
        self.assertEqual(d.relation(row(), None), 'SIN_FILA_SIGUIENTE')

    def test_editorial_literals_remain_in_text(self):
        for text in ['Discurso. Sesión N° 184 Página 23 de 26', 'Discurso. B A N C O C E N T R A L D E C H I L E']:
            r = row(text=text)
            self.assertEqual(d.pattern(r, None), 'PIE_EDITORIAL_LITERAL')
            self.assertEqual(d.diagnose([r])[0]['Texto'], text)

    def test_normal_institution_name_is_not_spaced_footer(self):
        self.assertEqual(d.pattern(row(text='Es un informe del Banco Central de Chile'), None), 'OTRO_FINAL_SIN_PUNTUACION')

    def test_embedded_footer_not_at_end_does_not_match(self):
        text = 'Sesión N° 184 Página 23 de 26. Sigue otra pregunta,'
        self.assertEqual(d.pattern(row(text=text), None), 'COMA_OTRO_CONTEXTO')

    def test_heading_is_not_live_speech(self):
        text = 'Anuncia al expositor. Exposición Síntesis del mes'
        self.assertEqual(d.pattern(row(text=text), None), 'ENCABEZADO_LITERAL')

    def test_short_tail_includes_ambiguous_conjunction_without_deleting_it(self):
        for tail in ['Y', 'f', '/', 'Lf \\']:
            r = row(text='Una frase. ' + tail)
            self.assertEqual(d.pattern(r, None), 'COLA_BREVE_TRAS_PUNTUACION')
            self.assertTrue(d.diagnose([r])[0]['Texto'].endswith(tail))

    def test_function_word_is_only_candidate(self):
        for text in ['Ofrece la palabra para', 'Se aprecia una caída en las', 'Señala que dado que el']:
            self.assertEqual(d.pattern(row(text=text), None), 'TERMINO_FUNCIONAL_ABIERTO')
        self.assertEqual(d.pattern(row(text='La decisión requiere actuar'), None), 'OTRO_FINAL_SIN_PUNTUACION')

    def test_all_three_previous_tail_patterns(self):
        for end, word in [('a los asistentes para', 'comentarios'), ('para proceder a la', 'votación'), ('comentarios sobre el escenario', 'interno')]:
            prev = row(text='Un discurso. ' + word + '.')
            current = row(2, parent=11, text='El Presidente ofrece la palabra ' + end)
            before = copy.deepcopy([prev, current])
            self.assertEqual(d.previous_tail_clue(current, prev), word)
            self.assertEqual([prev, current], before)

    def test_previous_tail_never_crosses_date_or_same_parent(self):
        a = row(text='Algo. votación.')
        for b in [row(2, parent=11, Fecha='2000-02-01'), row(2)]:
            b['Texto'] = 'El Presidente ofrece la palabra para proceder a la'
            self.assertEqual(d.previous_tail_clue(b, a), '')

    def test_previous_tail_requires_standalone_word_and_procedural_form(self):
        b = row(2, parent=11, text='El Presidente ofrece la palabra para proceder a la')
        self.assertEqual(d.previous_tail_clue(b, row(text='Explica su votación.')), '')
        b['Texto'] = 'Dice que proceder a la'
        self.assertEqual(d.previous_tail_clue(b, row(text='Algo. votación.')), '')

    def test_other_motives_are_preserved_and_not_counted_as_only(self):
        rows = [row(Motivos_Revision=d.MOTIVE + ';TEXTO_DANADO_POR_COTEJAR')]
        result = d.diagnose(rows)
        self.assertFalse(result[0]['Solo_Este_Motivo'])
        self.assertEqual(result[0]['Motivos_Adicionales'], ['TEXTO_DANADO_POR_COTEJAR'])
        self.assertEqual(d.summarize(result)['Filas_Solo_Este_Motivo'], 0)

    def test_no_alert_not_a_candidate_even_when_text_looks_truncated(self):
        self.assertEqual(d.diagnose([row(Motivos_Revision=None)]), [])
        self.assertEqual(d.diagnose([row(Motivos_Revision=d.MOTIVE + '_OTRO')]), [])

    def test_duplicate_id_or_incomplete_input_rejected(self):
        with self.assertRaises(ValueError): d.diagnose([row(), row()])
        with self.assertRaises(ValueError): d.diagnose([{}])
        with self.assertRaises(ValueError): d.diagnose([row(text=' ')])

    def test_output_cannot_target_data_or_input(self):
        source = ROOT / 'data/processed/consolidado_base_referencia.xlsx'
        for target in [source, ROOT / 'data', ROOT / 'data/curation', ROOT / '.git', ROOT / 'scripts', ROOT / 'tests']:
            with self.assertRaises(ValueError): d.safe_output(target, source)

    def test_cli_exports_without_changing_source(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'base.xlsx'; output = Path(temp) / 'diagnostico'
            wb = openpyxl.Workbook(); sheet = wb.active; sheet.title = 'Consolidado'
            r = row(); sheet.append(list(r)); sheet.append(list(r.values())); wb.save(source); wb.close()
            before = source.read_bytes()
            with patch.object(sys, 'argv', ['diagnosticar_finales', '--base', str(source), '--salida', str(output)]), patch('builtins.print'):
                d.main()
            self.assertEqual(source.read_bytes(), before)
            result = json.loads((output / 'finales_resumen.json').read_text())
            self.assertEqual(result['Filas_Solo_Este_Motivo'], 1)
            self.assertEqual(len(list(output.iterdir())), 3)

    def test_published_loop32_counts_and_clue_snapshot(self):
        cases = d.diagnose(d.read_rows(ROOT / 'data/processed/consolidado_base_referencia.xlsx'))
        summary = d.summarize(cases)
        self.assertEqual((summary['Filas_Con_Motivo'], summary['Filas_Solo_Este_Motivo'], summary['Padres_Solo_Este_Motivo']), (317, 302, 275))
        self.assertEqual(summary['Categorias_Solo_Este_Motivo'], {
            'COLA_BREVE_TRAS_PUNTUACION': 42, 'COMA_ANTES_DE_OTRO_ACTOR_EN_PADRE': 167,
            'COMA_OTRO_CONTEXTO': 2, 'ENCABEZADO_LITERAL': 1,
            'OTRO_FINAL_SIN_PUNTUACION': 67, 'PIE_EDITORIAL_LITERAL': 13, 'TERMINO_FUNCIONAL_ABIERTO': 10})
        self.assertEqual({c['ID_Padre'] for c in cases if c['Indicio_Cola_Anterior']}, {771,1077,1544,1652,2121,2166,2293,2434})
        self.assertEqual({c['Estado'] for c in cases}, {'CANDIDATO_NO_ADJUDICADO'})


if __name__ == '__main__':
    unittest.main()
