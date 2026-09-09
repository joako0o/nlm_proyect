"""Fichas acotadas de acta/discurso; nunca nuevos turnos o cierres."""
import copy
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import revisar_cola_comas as personal
import revisar_comas_institucionales as inst

PATHS = [Path(f'docs/revision_comas_lote{n}_2026-09-08/revisiones.json') for n in range(1, 6)]
INSTITUTIONAL = Path('docs/revision_comas_lote6_2026-09-08/revisiones.json')


class InstitutionalCommaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = personal.read_rows(ROOT / 'data/processed/consolidado_base_referencia.xlsx')
        cls.packages = [json.loads((ROOT / p).read_text()) for p in PATHS]
        cls.package = json.loads((ROOT / INSTITUTIONAL).read_text())

    def parent(self, p):
        return [r for r in self.rows if r['ID_Padre'] == p]

    def one(self, e):
        indices = [i for i, r in enumerate(self.rows) if r['ID_Padre'] == e['ID_Padre']]
        rows = copy.deepcopy(self.rows[indices[0] - 1:indices[-1] + 2])
        pkg = copy.deepcopy(self.package)
        pkg['Revisiones'] = [copy.deepcopy(e)]
        pkg['Padres'] = {str(e['ID_Padre']): pkg['Padres'][str(e['ID_Padre'])]}
        return rows, pkg

    def test_five_complete_parents_and_ten_native_neighbors(self):
        self.assertEqual(len(inst.validate_institutional_reviews(self.rows, self.package)), 5)
        self.assertEqual(sum(len(p['Texto_Padre']) for p in self.package['Padres'].values()), 10169)
        neighbors = [p[k]['Intervalo'] for p in self.package['Padres'].values()
                     for k in ['Vecino_Anterior', 'Vecino_Siguiente']]
        self.assertEqual(len({n['ID_Intervencion'] for n in neighbors}), 10)
        self.assertEqual(sum(len(n['Texto']) for n in neighbors), 26227)

    def test_cumulative_counts_and_no_mutation(self):
        before = copy.deepcopy((self.rows, self.packages, self.package))
        queue = inst.build_combined_queue(self.rows, self.packages, self.package)
        self.assertEqual(len(queue), 167)
        self.assertEqual(sum(q['Clase_Ficha'] == 'PERSONAL' for q in queue), 162)
        self.assertEqual(sum(q['Clase_Ficha'] == 'ACTA_DISCURSO' for q in queue), 5)
        self.assertFalse(any(q['Estado_Lectura'] == personal.PENDING for q in queue))
        self.assertEqual(len({q['ID_Padre'] for q in queue}), 151)
        self.assertEqual((self.rows, self.packages, self.package), before)
        self.assertEqual(sum(bool(r['Motivos_Revision']) for r in self.rows), 465)

    def test_personal_validator_still_rejects_all_five(self):
        for e in self.package['Revisiones']:
            _, pkg = self.one(e)
            pkg['Revisiones'][0]['Estado'] = personal.STATE
            with self.assertRaisesRegex(ValueError, 'sólo revisa límites personales'):
                personal.validate_reviews(self.rows, pkg)
        queue = personal.build_queue(self.rows, personal.combine_packages(self.packages))
        self.assertEqual(sum(q['Estado_Lectura'] == personal.PENDING for q in queue), 5)

    def test_partial_package_does_not_approve_other_boundaries(self):
        _, pkg = self.one(self.package['Revisiones'][0])
        queue = inst.build_combined_queue(self.rows, self.packages, pkg)
        self.assertEqual(sum(q['Estado_Lectura'] == inst.STATE for q in queue), 1)
        self.assertEqual(sum(q['Estado_Lectura'] == personal.PENDING for q in queue), 4)

    def test_previous_packages_frozen(self):
        hashes = [
            'efd48b25aaa63ca591eb1bd2ca7923edff8bc2ede898c0635f73719b660b80fc',
            'bb343dc2fd538d47a701f9d80a82200d1d9b13088cd70789f79e77efa0b70a99',
            '28f16b295bb6d3502e39545ac3fcef19f9054817aa6b2f7765e9ca4faa94ca52',
            'f90d96e3580f815cced0516449c9dee9dddf3ffd5958b07e78df78a7a4bbbef9',
            'cdc7c5c793a71f7ba003a2628bd9c9ec5c49046cf0435dd29c66cea33449e9f3',
        ]
        for p, expected in zip(PATHS, hashes):
            self.assertEqual(hashlib.sha256((ROOT / p).read_bytes()).hexdigest(), expected)

    def test_scope_version_and_incomplete_package_rejected(self):
        for field, value in [('Version', 2), ('Alcance', 'GLOBAL'),
                             ('Revisiones', {}), ('Padres', [])]:
            pkg = copy.deepcopy(self.package)
            pkg[field] = value
            with self.assertRaises(ValueError):
                inst.validate_institutional_reviews(self.rows, pkg)
        for field in ['Criterio', 'Derecha', 'Limitacion']:
            pkg = copy.deepcopy(self.package)
            del pkg['Revisiones'][0][field]
            with self.assertRaises(ValueError):
                inst.validate_institutional_reviews(self.rows, pkg)

    def test_duplicate_fiches_and_cross_type_ids_rejected(self):
        pkg = copy.deepcopy(self.package)
        pkg['Revisiones'].append(copy.deepcopy(pkg['Revisiones'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicado'):
            inst.validate_institutional_reviews(self.rows, pkg)
        pkg = copy.deepcopy(self.package)
        pkg['Revisiones'][0]['Revision_ID'] = self.packages[0]['Revisiones'][0]['Revision_ID']
        with self.assertRaisesRegex(ValueError, 'duplicado'):
            inst.build_combined_queue(self.rows, self.packages, pkg)

    def test_no_generic_extension_to_other_boundaries(self):
        pkg = copy.deepcopy(self.package)
        pkg['Revisiones'][0]['Izquierda']['ID_Intervencion'] = 'RPM-2009-09-08:2705:6'
        with self.assertRaisesRegex(ValueError, 'inventario'):
            inst.validate_institutional_reviews(self.rows, pkg)
        for field, value in [('Criterio', 'GERUNDIO_GLOBAL'), ('Estado', personal.STATE),
                             ('Justificacion', ''), ('Reservas', 'sin reservas')]:
            pkg = copy.deepcopy(self.package)
            pkg['Revisiones'][0][field] = value
            with self.assertRaises(ValueError):
                inst.validate_institutional_reviews(self.rows, pkg)

    def test_endpoint_fields_are_bound_for_each_fiche(self):
        for e in self.package['Revisiones']:
            for side in ['Izquierda', 'Derecha']:
                for field in personal.BOUND_FIELDS:
                    rows, pkg = self.one(e)
                    row = next(r for r in rows if r['ID_Intervencion'] == e[side]['ID_Intervencion'])
                    row[field] = 'Cambio'
                    with self.subTest(parent=e['ID_Padre'], side=side, field=field):
                        with self.assertRaises(ValueError):
                            inst.validate_institutional_reviews(rows, pkg)

    def test_each_external_neighbor_is_bound(self):
        for e in self.package['Revisiones']:
            for index in [0, -1]:
                for field in ['Texto', 'Actor_Final', 'Fecha', 'Tipo_Acta', 'ID_Ancla_Actor', 'Motivos_Revision']:
                    rows, pkg = self.one(e)
                    rows[index][field] = 'Cambio'
                    with self.assertRaises(ValueError):
                        inst.validate_institutional_reviews(rows, pkg)

    def test_nonfocal_parent_mutation_invalidates_fiche(self):
        for p in [1901, 2112, 5252]:
            e = next(e for e in self.package['Revisiones'] if e['ID_Padre'] == p)
            rows, pkg = self.one(e)
            rows[1]['Texto'] += ' Cambio.'
            with self.assertRaises(ValueError):
                inst.validate_institutional_reviews(rows, pkg)

    def test_cross_acta_and_neighbor_merges_rejected(self):
        pairs = [(601, 0, 2), (1901, 1, 3), (5252, 1, 3), (2803, 2, 3)]
        for p, a, b in pairs:
            e = next(e for e in self.package['Revisiones'] if e['ID_Padre'] == p)
            rows, pkg = self.one(e)
            rows[b]['ID_Turno'] = rows[a]['ID_Turno']
            with self.subTest(parent=p), self.assertRaisesRegex(ValueError, 'relaciones locales'):
                inst.validate_institutional_reviews(rows, pkg)

    def test_global_group_renumbering_not_frozen(self):
        rows = copy.deepcopy(self.rows)
        for r in rows:
            r['ID_Turno'] = 'Renumerado:' + r['ID_Turno']
        self.assertEqual(len(inst.validate_institutional_reviews(rows, self.package)), 5)

    def test_source_hash_and_parent_text_guards(self):
        for field in ['SHA256_Texto_Padre', 'SHA256_Particion', 'Texto_Padre']:
            pkg = copy.deepcopy(self.package)
            pkg['Padres']['601'][field] = 'Cambio'
            with self.assertRaises(ValueError):
                inst.validate_institutional_reviews(self.rows, pkg)
        pkg = copy.deepcopy(self.package)
        key = next(iter(pkg['SHA256_Fuentes']))
        pkg['SHA256_Fuentes'][key] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Fuente original modificada'):
            inst.validate_institutional_reviews(self.rows, pkg)

    def test_missing_or_surplus_evidence_rejected(self):
        for operation in ['missing_parent', 'surplus_parent', 'missing_neighbor']:
            pkg = copy.deepcopy(self.package)
            if operation == 'missing_parent':
                del pkg['Padres']['601']
            elif operation == 'surplus_parent':
                pkg['Padres']['600'] = copy.deepcopy(pkg['Padres']['601'])
            else:
                del pkg['Padres']['601']['Vecino_Anterior']
            with self.assertRaises(ValueError):
                inst.validate_institutional_reviews(self.rows, pkg)

    def test_adjacency_and_duplicates_in_rows_rejected(self):
        e = self.package['Revisiones'][0]
        rows, pkg = self.one(e)
        with self.assertRaises(ValueError):
            inst.validate_institutional_reviews(rows[1:], pkg)
        rows, pkg = self.one(e)
        rows.append(copy.deepcopy(rows[0]))
        with self.assertRaisesRegex(ValueError, 'duplicados'):
            inst.validate_institutional_reviews(rows, pkg)

    def test_601_long_exposition_not_absorbed_or_linked_across_acta(self):
        rows = self.parent(601)
        self.assertEqual([len(r['Texto']) for r in rows], [307, 3688])
        self.assertTrue(rows[1]['Texto'].startswith('quien señala'))
        self.assertEqual(rows[1]['ID_Ancla_Actor'], rows[1]['ID_Intervencion'])
        self.assertNotEqual(self.parent(600)[-1]['ID_Turno'], rows[1]['ID_Turno'])
        self.assertEqual(rows[0]['Motivos_Revision'], 'FINAL_SIN_PUNTUACION')

    def test_1901_and_2112_preserve_restarts_and_later_presentations(self):
        self.assertEqual([len(r['Texto']) for r in self.parent(1901)], [130, 74, 178])
        self.assertEqual([len(r['Texto']) for r in self.parent(2112)], [397, 988, 74, 279])
        self.assertIn('16;00', self.parent(2112)[2]['Texto'])
        self.assertEqual(str(self.parent(2112)[-1]['Fecha'])[:10], '2008-10-09')
        self.assertIn('abril de 2009', self.parent(2112)[-1]['Texto'])
        self.assertEqual(len(self.parent(1902)[0]['Texto']), 7969)
        self.assertEqual(len(self.parent(2113)[0]['Texto']), 12059)

    def test_2803_roster_damage_and_unlinked_2804(self):
        a, b = self.parent(2803)
        self.assertEqual([len(a['Texto']), len(b['Texto'])], [1445, 296])
        self.assertEqual(a['Tipo_Acta'], 'ACTA_CABECERA')
        self.assertIn('Marlys Pabst Cortés,', a['Texto'])
        self.assertEqual(b['Motivos_Revision'], 'TEXTO_DANADO_POR_COTEJAR')
        self.assertTrue(b['Texto'].endswith('A continuación,.'))
        self.assertIsNone(b['ID_Ancla_Actor'])
        self.assertNotEqual(b['ID_Turno'], self.parent(2804)[0]['ID_Turno'])
        self.assertNotEqual(str(a['Fecha'])[:10], str(self.parent(2802)[0]['Fecha'])[:10])

    def test_5252_future_arrival_is_not_vergara_speech(self):
        rows = self.parent(5252)
        self.assertEqual([len(r['Texto']) for r in rows], [1712, 158, 162, 223])
        self.assertEqual(rows[2]['Actor_Final'], 'Manuel Marfán Lewis')
        self.assertEqual(rows[2]['Fuente_Actor'], 'CONTEXTO_REVISADO')
        self.assertIsNone(rows[2]['ID_Ancla_Actor'])
        self.assertEqual(rows[3]['ID_Ancla_Actor'], rows[3]['ID_Intervencion'])
        self.assertEqual(len({r['ID_Turno'] for r in rows}), 4)
        arrival = self.parent(5257)[0]
        self.assertEqual(arrival['Actor_Final'], inst.COUNCIL)
        self.assertIn('se integra a la Sesión', arrival['Texto'])

    def test_personal_package_cannot_borrow_other_evidence(self):
        packages = copy.deepcopy(self.packages)
        packages[0]['Padres'].pop(next(iter(packages[0]['Padres'])))
        with self.assertRaises(ValueError):
            inst.build_combined_queue(self.rows, packages, self.package)

    def cli(self, output):
        cmd = [sys.executable, 'scripts/revisar_comas_institucionales.py']
        for path in PATHS:
            cmd += ['--personales', str(path)]
        cmd += ['--institucionales', str(INSTITUTIONAL), '--salida', str(output)]
        return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=60)

    def test_cli_reproducible_and_refuses_overwrite(self):
        cache = ROOT / '.cache'
        cache.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=cache) as tmp:
            a, b = Path(tmp) / 'a', Path(tmp) / 'b'
            for output in [a, b]:
                result = self.cli(output)
                self.assertEqual(result.returncode, 0, result.stderr)
            for name in ['cola_comas.csv', 'comas_sin_ficha.csv', 'resumen.json']:
                self.assertEqual((a / name).read_bytes(), (b / name).read_bytes())
            with (a / 'comas_sin_ficha.csv').open(encoding='utf-8-sig') as f:
                self.assertEqual(list(csv.DictReader(f)), [])
            original = {p.name: p.read_bytes() for p in a.iterdir()}
            result = self.cli(a)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('salida ya existe', result.stderr)
            self.assertEqual({p.name: p.read_bytes() for p in a.iterdir()}, original)

    def test_cli_protects_data_directory(self):
        result = self.cli(ROOT / 'data')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('fuera de datos', result.stderr)


if __name__ == '__main__':
    unittest.main()
