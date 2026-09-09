"""Fichas de límites existentes: no cerrar alertas ni generalizar al padre."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import revisar_cola_comas as c

PACKAGE = ROOT / 'docs/revision_comas_lote1_2026-09-08/revisiones.json'


class CommaReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = c.read_rows(ROOT / 'data/processed/consolidado_base_referencia.xlsx')
        cls.package = json.loads(PACKAGE.read_text())

    def one(self, e):
        p = e['ID_Padre']
        rows = copy.deepcopy([r for r in self.rows if r['ID_Padre'] == p])
        package = copy.deepcopy(self.package)
        package['Revisiones'] = [copy.deepcopy(e)]
        package['Padres'] = {str(p): package['Padres'][str(p)]}
        return rows, package

    def test_forty_limits_thirty_six_parents_and_no_mutation(self):
        before = copy.deepcopy(self.rows); reviews = copy.deepcopy(self.package)
        self.assertEqual(len(c.validate_reviews(self.rows, self.package)), 40)
        self.assertEqual(len(self.package['Padres']), 36)
        self.assertEqual(self.rows, before); self.assertEqual(self.package, reviews)

    def test_queue_progress_is_not_alert_closure(self):
        queue = c.build_queue(self.rows, self.package)
        self.assertEqual(len(queue), 167)
        self.assertEqual(sum(q['Estado_Lectura'] == c.STATE for q in queue), 40)
        self.assertEqual(sum(q['Estado_Lectura'] == c.PENDING for q in queue), 127)
        self.assertEqual({q['Motivo_Original'] for q in queue}, {'FINAL_SIN_PUNTUACION'})
        self.assertEqual(sum(bool(r['Motivos_Revision']) for r in self.rows), 465)

    def test_all_parent_literal_texts_conserved(self):
        for p, evidence in self.package['Padres'].items():
            rows = [r for r in self.rows if r['ID_Padre'] == int(p)]
            self.assertEqual(c.sha(evidence['Texto_Padre']), evidence['SHA256_Texto_Padre'])
            self.assertEqual(c.compact(evidence['Texto_Padre']), ''.join(c.compact(r['Texto']) for r in rows))
            self.assertEqual(evidence['SHA256_Particion'], c.parent_signature(rows))

    def test_each_side_rejects_text_actor_method_date_change(self):
        for e in self.package['Revisiones']:
            for side in ['Izquierda', 'Derecha']:
                for field, value in [('Texto', 'Otro texto,'), ('Actor_Final', 'Otra persona'),
                                     ('Fuente_Actor', 'CONTEXTO_REVISADO_INVALIDO'), ('Fecha', '1900-01-01')]:
                    rows, package = self.one(e)
                    r = next(r for r in rows if r['ID_Intervencion'] == e[side]['ID_Intervencion']); r[field] = value
                    with self.subTest(e=e['Revision_ID'], side=side, field=field), self.assertRaises(ValueError):
                        c.validate_reviews(rows, package)

    def test_role_or_anchor_change_invalidates_reading(self):
        for e in self.package['Revisiones']:
            for field in ['Rol_Final', 'ID_Ancla_Actor', 'ID_Antecedente_Continuidad']:
                rows, package = self.one(e); rows[0][field] = 'cambiado'
                with self.assertRaises(ValueError): c.validate_reviews(rows, package)

    def test_other_segment_change_invalidates_whole_parent_evidence(self):
        e = next(e for e in self.package['Revisiones'] if e['ID_Padre'] == 2583)
        for field in ['Texto', 'Fecha']:
            rows, package = self.one(e); rows[-1][field] = 'Cambio'
            with self.assertRaises(ValueError): c.validate_reviews(rows, package)

    def test_insertion_between_endpoints_rejected(self):
        for e in self.package['Revisiones']:
            rows, package = self.one(e); i = next(i for i,r in enumerate(rows) if r['ID_Intervencion'] == e['Izquierda']['ID_Intervencion'])
            inserted = copy.deepcopy(rows[i]); inserted['ID_Intervencion'] += '-intercalada'
            rows.insert(i+1, inserted)
            with self.assertRaises(ValueError): c.validate_reviews(rows, package)

    def test_registry_tampering_rejected(self):
        e = self.package['Revisiones'][0]
        for field, value in [('Estado', 'RESUELTO'), ('Justificacion', ''), ('Limitacion', ''), ('Reservas', 'sin lista')]:
            rows, package = self.one(e); package['Revisiones'][0][field] = value
            with self.assertRaises(ValueError): c.validate_reviews(rows, package)
        for field in ['SHA256_Texto_Padre', 'SHA256_Particion', 'Texto_Padre', 'Fecha', 'Lectura']:
            rows, package = self.one(e); package['Padres'][str(e['ID_Padre'])][field] = 'cambiado'
            with self.assertRaises(ValueError): c.validate_reviews(rows, package)

    def test_duplicate_or_missing_review_key_rejected(self):
        e = self.package['Revisiones'][0]; rows, package = self.one(e)
        package['Revisiones'].append(copy.deepcopy(e))
        with self.assertRaises(ValueError): c.validate_reviews(rows, package)
        rows, package = self.one(e); del package['Revisiones'][0]['Derecha']
        with self.assertRaises(ValueError): c.validate_reviews(rows, package)

    def test_source_hash_check(self):
        c.check_sources(self.package)
        package = copy.deepcopy(self.package)
        first = next(iter(package['SHA256_Fuentes'])); package['SHA256_Fuentes'][first] = '0'*64
        with self.assertRaises(ValueError): c.check_sources(package)
        with self.assertRaises(ValueError): c.check_sources({'SHA256_Fuentes': {}})
        with self.assertRaises(ValueError): c.check_sources({'SHA256_Fuentes': {'../otro': '0'*64}})

    def test_review_does_not_erase_joint_damage_or_duplicate(self):
        e = next(e for e in self.package['Revisiones'] if e['ID_Padre'] == 2667)
        rows, package = self.one(e); c.validate_reviews(rows, package)
        self.assertIn('y el Gerente de', rows[1]['Texto'])
        self.assertEqual(rows[1]['Motivos_Revision'], 'FINAL_SIN_PUNTUACION;TEXTO_DANADO_POR_COTEJAR')
        e = next(e for e in self.package['Revisiones'] if e['ID_Padre'] == 2723)
        rows, package = self.one(e); c.validate_reviews(rows, package)
        self.assertEqual(rows[1]['Motivos_Revision'], 'DUPLICADO_NO_FORMULA')

    def test_literal_residue_and_cargo_reservations_survive(self):
        byparent = {e['ID_Padre']: e for e in self.package['Revisiones']}
        self.assertTrue(byparent[2535]['Izquierda']['Texto'].endswith('/ ,'))
        self.assertTrue(byparent[2535]['Reservas'])
        self.assertTrue(byparent[2576]['Reservas'])
        self.assertIn('División Política Monetaria', self.package['Padres']['2576']['Texto_Padre'])

    def test_existing_continuities_and_returns_not_merged(self):
        for p, nxt in [(2027,2028),(2673,2674),(2785,2786)]:
            a = [r for r in self.rows if r['ID_Padre'] == p][-1]
            b = next(r for r in self.rows if r['ID_Padre'] == nxt)
            self.assertEqual(a['ID_Turno'], b['ID_Turno'])
        for p in [1809,2615,2671,2704]:
            rows = [r for r in self.rows if r['ID_Padre'] == p]
            for left, right in zip(rows, rows[1:]):
                if left['Actor_Final'] != right['Actor_Final']:
                    self.assertNotEqual(left['ID_Turno'], right['ID_Turno'])

    def test_prior_diagnostic_cases_not_implicitly_reviewed(self):
        queue = c.build_queue(self.rows, self.package)
        for p in [301,631,1386,1737,2555,2697,2896,3044,4096,5252,6415,7176]:
            self.assertTrue(all(q['Estado_Lectura'] == c.PENDING for q in queue if q['ID_Padre'] == p))

    def test_cli_and_source_files_unchanged(self):
        before = PACKAGE.read_bytes()
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(sys, 'argv', ['revisar_cola_comas', '--revisiones', str(PACKAGE), '--salida', temp]), patch('builtins.print'):
                c.main()
            summary = json.loads((Path(temp)/'resumen.json').read_text())
            self.assertEqual((summary['Limites_Subgrupo'], summary['Limites_Con_Ficha'], summary['Limites_Sin_Ficha']), (167,40,127))
            self.assertEqual(summary['Alertas_Cerradas'], 0)
        self.assertEqual(PACKAGE.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
