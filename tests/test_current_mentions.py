"""Lecturas acotadas: anotaciones separadas de alertas, actor y cola histórica."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_base_referencia as b
from mention_reviews import (load_mention_reviews, validate_mention_reviews,
                             annotation_for, PATH, FIELDS, compact)
from procedural import load_formula_reviews, is_formula
from review_queue import build_report


class CurrentMentionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {r[0]: dict(Fecha=b.to_date_str(r[1]), Texto=r[5], Actor=r[2]) for r in b.data}
        cls.reviews = load_mention_reviews(cls.raw)
        from curation import load_speaker_reviews
        speakers = load_speaker_reviews(cls.raw)
        cls.rows = []
        for parent in sorted(e['ID_Padre'] for e in cls.reviews.values()):
            r = cls.raw[parent]
            for text, actor, method in b.segment_turns(r['Texto'], r['Fecha'], r['Actor'], review=speakers.get(parent)):
                if not method:
                    detected = b.detect(text, r['Fecha'])
                    if detected:
                        actor, _, method, _ = detected
                cls.rows.append(dict(ID=len(cls.rows)+1, ID_Padre=parent, Fecha=r['Fecha'], Texto=text,
                                     Actor_Final=actor, Fuente_Actor=method, ID_Turno='fixture',
                                     Estado_Revision='PENDIENTE_REVISION', Duplicado_Formula='NO',
                                     Motivos_Revision='POSIBLE_OTRO_HABLANTE_O_MENCION'))

    def load_entries(self, entries, raw=None):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'r.json'
            p.write_text(json.dumps(entries))
            return load_mention_reviews(raw if raw is not None else self.raw, p)

    def test_ten_exact_intervals_are_documented(self):
        self.assertEqual({e['ID_Padre'] for e in self.reviews.values()}, {320,1336,1420,2228,2768,3147,4574,4656,5658,6587})
        self.assertEqual(len(self.reviews), 10)

    def test_valid_annotations_do_not_modify_rows_or_warnings(self):
        rows = copy.deepcopy(self.rows)
        errors, annotations = validate_mention_reviews(rows, self.reviews)
        self.assertEqual(errors, [])
        self.assertEqual(len(annotations), 10)
        self.assertEqual(rows, self.rows)
        for values in annotations.values():
            self.assertEqual(values[FIELDS[0]], 'MENCION_LEGITIMA_REVISADA')
            self.assertIn('Sólo se adjudica este aviso', values[FIELDS[2]])

    def test_source_change_requires_new_reading(self):
        raw = copy.deepcopy(self.raw)
        raw[320]['Texto'] += ' Cambio.'
        with self.assertRaisesRegex(ValueError, 'texto de origen'):
            load_mention_reviews(raw)

    def test_wrong_date_and_nonexistent_evidence_are_rejected(self):
        for field, value, message in [('Fecha', '2005-08-12', 'fecha'),
                                      ('Evidencia', [{'ID_Padre':320,'Cita':'cita inventada'}], 'Cita'),
                                      ('Evidencia', [{'ID_Padre':4656,'Cita':'El Presidente'}], 'sesión')]:
            entries = json.loads(PATH.read_text())
            entries[0][field] = value
            with self.subTest(field=field, value=value), self.assertRaisesRegex(ValueError, message):
                self.load_entries(entries)

    def test_invalid_boundary_or_empty_quote_is_rejected(self):
        for field, value in [('Inicio', -1), ('Fin', 999999), ('Cita_Inicio', '')]:
            entries = json.loads(PATH.read_text())
            entries[0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'Intervalo'):
                self.load_entries(entries)

    def test_cannot_expand_decision_to_all_alerts(self):
        entries = json.loads(PATH.read_text())
        entries[0]['Motivo_Revisado'] = 'TODOS'
        with self.assertRaisesRegex(ValueError, 'alcance'):
            self.load_entries(entries)

    def test_duplicate_review_is_rejected(self):
        entries = json.loads(PATH.read_text())
        entries.append(copy.deepcopy(entries[0]))
        with self.assertRaisesRegex(ValueError, 'duplicada'):
            self.load_entries(entries)

    def test_changed_output_actor_blocks_annotation(self):
        rows = copy.deepcopy(self.rows)
        rows[0]['Actor_Final'] = 'Jorge Desormeaux Jiménez'
        errors, annotations = validate_mention_reviews(rows, self.reviews)
        self.assertEqual(len(errors), 1)
        self.assertNotIn(rows[0]['ID'], annotations)

    def test_changed_output_text_or_boundary_blocks_annotation(self):
        for replacement in ['Texto alterado.', self.rows[0]['Texto'] + ' Frase adicional.']:
            rows = copy.deepcopy(self.rows)
            rows[0]['Texto'] = replacement
            errors, annotations = validate_mention_reviews(rows, self.reviews)
            self.assertEqual(len(errors), 1)
            self.assertNotIn(rows[0]['ID'], annotations)

    def test_annotation_follows_interval_not_old_numeric_id(self):
        rows = [{**r, 'ID':r['ID']+10000} for r in self.rows]
        errors, annotations = validate_mention_reviews(rows, self.reviews)
        self.assertEqual(errors, [])
        self.assertTrue(all(rid > 10000 for rid in annotations))
        self.assertEqual(annotation_for(self.rows[0], annotations), dict.fromkeys(FIELDS, ''))

    def test_real_marfan_to_garcia_change_is_not_erased(self):
        rows = [r for r in self.rows if r['ID_Padre'] == 1336]
        self.assertEqual([r['Actor_Final'] for r in rows], ['Manuel Marfán Lewis', 'Pablo García Silva'])
        _, annotations = validate_mention_reviews(self.rows, self.reviews)
        self.assertNotIn(rows[0]['ID'], annotations)
        self.assertIn(rows[1]['ID'], annotations)

    def test_presenters_start_in_following_parents(self):
        for p, surname in [(4575, 'Ricaurte'), (4657, 'Lehmann')]:
            r = self.raw[p]
            parts = b.segment_turns(r['Texto'], r['Fecha'], r['Actor'])
            self.assertEqual(len(parts), 1)
            self.assertIn(surname, parts[0][1])

    def test_exact_new_formula_preserves_substantive_tail(self):
        formulas = load_formula_reviews(raw_by_id=self.raw)
        entry = next(e for e in formulas.values() if e['Revision_ID']=='FORM-20260907-PRESENTACION-VALDES')
        self.assertEqual(entry['Padres'], [644,664,727,770])
        text = entry['Texto']
        self.assertTrue(is_formula(text))
        self.assertTrue(is_formula(text.replace('División Estudios', 'División\nEstudios')))
        self.assertFalse(is_formula(text + ' Propone subir la tasa en 50 puntos base.'))
        self.assertFalse(is_formula(text + ' El señor Gerente de División mencionado informó lo siguiente: la inflación subió.'))
        self.assertFalse(is_formula(text.replace('solicita', 'recomienda')))

    def test_new_formula_does_not_reassign_presenter(self):
        from curation import load_speaker_reviews
        reviews = load_speaker_reviews(self.raw)
        for p in [644,664,727,770]:
            r = self.raw[p]
            parts = b.segment_turns(r['Texto'], r['Fecha'], r['Actor'], review=reviews.get(p))
            matching = [i for i,(text,_,_) in enumerate(parts)
                        if 'solicita al Gerente de División' in text and 'Opciones de Política Monetaria' in text]
            self.assertEqual(len(matching), 1)
            i = matching[0]
            self.assertEqual(parts[i][1], 'Vittorio Corbo Lioi')
            self.assertEqual(parts[i+1][1], 'Rodrigo Valdés Pulido')

    def test_workbook_annotation_does_not_close_historical_legacy_warning(self):
        row = copy.deepcopy(next(r for r in self.rows if r['ID_Padre']==4574))
        row['Motivos_Revision'] += ';ATRIBUCION_HEURISTICA_LEGADA'
        old = {**row, 'Fecha':str(row['Fecha'])[:10], 'Inicio_Compacto':0,
               'Fin_Compacto':len(compact(row['Texto'])), 'SHA256_Texto':'fixture'}
        reviews = {k:v for k,v in self.reviews.items() if v['ID_Padre']==4574}
        errors, annotations = validate_mention_reviews([row], reviews)
        self.assertEqual(errors, [])
        with tempfile.TemporaryDirectory() as d, patch('review_queue.load_baseline', return_value=(
                {'Filas':[old], 'SHA256_Base':'fixture'}, {})):
            summary = build_report([row], Path(d), mention_annotations=annotations)
            self.assertEqual(summary['estados'], {'PENDIENTE_LECTURA_CONTEXTUAL':1})
            self.assertEqual(summary['menciones_actuales_documentadas'], 1)
            w = openpyxl.load_workbook(Path(d)/'revision_783.xlsx', read_only=True)
            values = list(w['Alertas_actuales'].values)
            result = dict(zip(values[0], values[1]))
            self.assertEqual(result['Motivos_Revision'], row['Motivos_Revision'])
            self.assertEqual(result[FIELDS[0]], 'MENCION_LEGITIMA_REVISADA')
            w.close()


if __name__ == '__main__':
    unittest.main()
