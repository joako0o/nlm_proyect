"""Auditoría no aplicada: sólo dos candidatos y controles de no fusión."""
import copy
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import auditar_continuidad_turnos as audit
import revisar_cola_comas as proof
from reviewed_continuity import load_reviewed_links

PACKAGE = Path('docs/auditoria_continuidad1_2026-09-09/revisiones.json')


class ContinuityAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = proof.read_rows(ROOT / 'data/processed/consolidado_base_referencia.xlsx')
        cls.pkg = json.loads((ROOT / PACKAGE).read_text())

    def parent(self, p):
        return [x for x in self.rows if x['ID_Padre'] == p]

    def test_inventory_counts_not_approvals(self):
        inv = audit.inventory(self.rows)
        self.assertEqual(len(inv), 92)
        self.assertEqual(sum(x['Mismo_Padre'] for x in inv), 43)
        self.assertEqual(sum(not x['Mismo_Padre'] for x in inv), 49)
        self.assertTrue(all(x['Estado'] == 'INVENTARIO_NO_APROBACION' for x in inv))
        self.assertFalse(any(x['Actor'] == 'Consejo del Banco Central de Chile' for x in inv))

    def test_context_only_indicator_does_not_mean_clean_text(self):
        inv = audit.inventory(self.rows)
        candidates = [x for x in inv if x['Indicadores'] == 'IZQUIERDA_SIN_FUENTE_PROPAGABLE'
                      and x['Fuente_Izquierda'] == 'CONTEXTO_REVISADO'
                      and x['Fuente_Derecha'] in audit.EXPLICIT]
        self.assertEqual(len(candidates), 21)
        self.assertTrue(all(x['Mismo_Padre'] for x in candidates))
        self.assertEqual(sum(not x['Motivos_Izquierda'] and not x['Motivos_Derecha'] for x in candidates), 20)
        dup = next(x for x in candidates if ':2685:' in x['Izquierda'])
        self.assertEqual(dup['Motivos_Izquierda'], 'DUPLICADO_NO_FORMULA')

    def test_inventory_excludes_different_actors_dates_and_joined_pairs(self):
        a = copy.deepcopy(self.rows[0])
        b = copy.deepcopy(a)
        a.update(Actor_Final='Persona A', ID_Turno='T1')
        b.update(Actor_Final='Persona B', ID_Turno='T2')
        self.assertEqual(audit.inventory([a, b]), [])
        b['Actor_Final'] = a['Actor_Final']
        b['Fecha'] = '1900-01-01'
        self.assertEqual(audit.inventory([a, b]), [])
        b['Fecha'] = a['Fecha']
        b['ID_Turno'] = a['ID_Turno']
        self.assertEqual(audit.inventory([a, b]), [])

    def test_seven_complete_parents(self):
        audit.validate(self.rows, self.pkg)
        self.assertEqual(set(map(int, self.pkg['Padres'])), audit.READ_PARENTS)
        self.assertEqual(sum(len(e['Texto_Padre']) for e in self.pkg['Padres'].values()), 28893)
        for e in self.pkg['Padres'].values():
            for side in ['Vecino_Anterior', 'Vecino_Siguiente']:
                self.assertLessEqual(len(e[side]['Texto']), 250)
                self.assertEqual(e[side]['Lectura'], 'VENTANA_HASTA_250_CARACTERES')

    def test_exact_scenario_changes_and_no_applied_links(self):
        changes, summary = audit.simulate(self.rows, self.pkg)
        self.assertEqual({x['ID_Intervencion'] for x in changes}, {
            'RPM-2009-11-12:2796:3', 'RPM-2009-11-12:2797:1', 'RPM-2010-03-18:3012:3'})
        self.assertTrue(all(x['Estado'] == 'SIMULADO_NO_APLICADO' for x in changes))
        self.assertEqual(summary['Grupos_Publicados'], 9257)
        self.assertEqual(summary['Grupos_Solo_Escenario'], 9255)
        self.assertEqual(summary['Propuestas_Simuladas'], 2)
        self.assertEqual(summary['Enlaces_Aplicados'], 0)
        self.assertEqual(summary['Alertas_Cerradas'], 0)

    def test_no_mutation_of_rows_or_package(self):
        before = copy.deepcopy((self.rows, self.pkg))
        audit.simulate(self.rows, self.pkg)
        self.assertEqual((self.rows, self.pkg), before)
        self.assertEqual(sum(bool(x['Motivos_Revision']) for x in self.rows), 465)
        self.assertEqual(len(self.rows), 9691)

    def test_scenario_loses_no_existing_group(self):
        changes, _ = audit.simulate(self.rows, self.pkg)
        changed = {x['ID_Intervencion']: x['Grupo_Solo_Escenario'] for x in changes}
        groups = {}
        for row in self.rows:
            groups.setdefault(row['ID_Turno'], set()).add(changed.get(row['ID_Intervencion'], row['ID_Turno']))
        self.assertTrue(all(len(values) == 1 for values in groups.values()))
        actors, dates = {}, {}
        for row in self.rows:
            group = changed.get(row['ID_Intervencion'], row['ID_Turno'])
            actors.setdefault(group, set()).add(row['Actor_Final'])
            dates.setdefault(group, set()).add(str(row['Fecha'])[:10])
        self.assertTrue(all(len(v) == 1 for v in actors.values()))
        self.assertTrue(all(len(v) == 1 for v in dates.values()))

    def test_marshall_long_vote_and_claro_remain_distinct(self):
        rows = self.parent(2796)
        self.assertEqual([len(x['Texto']) for x in rows], [5097, 343, 5287])
        self.assertEqual(len(self.parent(2797)[0]['Texto']), 2105)
        self.assertEqual(rows[2]['ID_Turno'], self.parent(2797)[0]['ID_Turno'])
        self.assertNotEqual(rows[0]['ID_Turno'], rows[1]['ID_Turno'])
        self.assertIn('ALAR', self.parent(2797)[0]['Texto'])

    def test_3012_physical_parts_and_anchors_not_changed(self):
        rows = self.parent(3012)
        self.assertEqual([len(x['Texto']) for x in rows], [109, 375, 1867])
        self.assertIsNone(rows[1]['ID_Ancla_Actor'])
        self.assertEqual(rows[2]['ID_Ancla_Actor'], rows[2]['ID_Intervencion'])
        self.assertNotEqual(rows[1]['ID_Turno'], rows[2]['ID_Turno'])
        self.assertNotEqual(rows[0]['Actor_Final'], rows[1]['Actor_Final'])

    def test_duplicate_and_damage_are_excluded_not_erased(self):
        self.assertEqual(self.parent(2685)[1]['Motivos_Revision'], 'DUPLICADO_NO_FORMULA')
        self.assertEqual(self.parent(2885)[2]['Motivos_Revision'], 'TEXTO_DANADO_POR_COTEJAR')
        self.assertTrue(self.parent(2885)[2]['Texto'].endswith('Para concluir con la votación,.'))
        changes, _ = audit.simulate(self.rows, self.pkg)
        self.assertFalse(any(':2685:' in x['ID_Intervencion'] or ':2885:' in x['ID_Intervencion'] for x in changes))

    def test_negative_acta_and_alternance_controls(self):
        self.assertEqual(len({x['ID_Turno'] for x in self.parent(1901)}), 3)
        self.assertEqual(self.parent(1901)[1]['Actor_Final'], 'Consejo del Banco Central de Chile')
        self.assertEqual(len({x['Actor_Final'] for x in self.parent(2779)}), 3)
        self.assertEqual(self.parent(2779)[1]['Texto'], 'El señor Soto asiente,')
        self.assertEqual(len({x['ID_Turno'] for x in self.parent(2779)}), 3)

    def test_proposal_scope_cannot_be_expanded_or_applied(self):
        for field, value in [('Alcance', 'APLICAR'), ('Miembros_Derechos_Leidos', [])]:
            pkg = copy.deepcopy(self.pkg)
            pkg['Propuestas'][next(iter(pkg['Propuestas']))][field] = value
            with self.assertRaises(ValueError):
                audit.validate(self.rows, pkg)
        pkg = copy.deepcopy(self.pkg)
        pkg['Propuestas']['RPM-2009-08-13:2685:2'] = copy.deepcopy(next(iter(pkg['Propuestas'].values())))
        with self.assertRaises(ValueError):
            audit.validate(self.rows, pkg)

    def test_every_proposed_endpoint_field_is_bound(self):
        for key, members in audit.PROPOSALS.items():
            for identity in [key, members[0]]:
                for field in proof.BOUND_FIELDS:
                    rows = copy.deepcopy(self.rows)
                    next(x for x in rows if x['ID_Intervencion'] == identity)[field] = 'Cambio'
                    with self.subTest(identity=identity, field=field), self.assertRaises(ValueError):
                        audit.validate(rows, self.pkg)

    def test_parent_source_window_and_group_mutations_rejected(self):
        for name in ['Texto_Padre', 'SHA256_Particion', 'Vecino_Anterior', 'Vecino_Siguiente']:
            pkg = copy.deepcopy(self.pkg)
            pkg['Padres']['2796'][name] = {} if 'Vecino' in name else 'Cambio'
            with self.assertRaises(ValueError):
                audit.validate(self.rows, pkg)
        pkg = copy.deepcopy(self.pkg)
        key = next(iter(pkg['SHA256_Fuentes']))
        pkg['SHA256_Fuentes'][key] = '0' * 64
        with self.assertRaises(ValueError):
            audit.validate(self.rows, pkg)
        rows = copy.deepcopy(self.rows)
        rows[0]['ID_Turno'] = 'CAMBIO'
        with self.assertRaises(ValueError):
            audit.validate(rows, self.pkg)

    def test_cannot_include_unread_group_members_even_with_new_group_digest(self):
        rows = copy.deepcopy(self.rows)
        target = self.parent(2796)[2]['ID_Turno']
        next(x for x in rows if x['ID_Padre'] == 2798)['ID_Turno'] = target
        pkg = copy.deepcopy(self.pkg)
        pkg['SHA256_Grupos_Actuales'] = audit.group_signature(rows)
        with self.assertRaisesRegex(ValueError, 'miembros no revisados'):
            audit.validate(rows, pkg)

    def test_decisions_complete_and_no_silent_upgrades(self):
        pkg = copy.deepcopy(self.pkg)
        pkg['Decisiones'][2]['Estado'] = 'SIMULAR_SIN_APLICAR'
        with self.assertRaises(ValueError):
            audit.validate(self.rows, pkg)
        pkg = copy.deepcopy(self.pkg)
        pkg['Decisiones'].pop()
        with self.assertRaises(ValueError):
            audit.validate(self.rows, pkg)

    def test_productive_api_still_rejects_same_parent(self):
        original = json.loads((ROOT / 'data/curation/revisiones_continuidad_hablantes.json').read_text())
        self.assertEqual(len(original), 24)
        e = copy.deepcopy(original[0])
        e['Siguiente']['ID_Padre'] = e['Anterior']['ID_Padre']
        (ROOT / '.cache').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as tmp:
            path = Path(tmp) / 'fixture.json'
            path.write_text(json.dumps([e]))
            with self.assertRaisesRegex(ValueError, 'no contiguo'):
                load_reviewed_links({}, path)

    def cli(self, output):
        return subprocess.run([sys.executable, 'scripts/auditar_continuidad_turnos.py',
                               '--revisiones', str(PACKAGE), '--salida', str(output)],
                              cwd=ROOT, capture_output=True, text=True, timeout=60)

    def test_cli_reproducible_and_explicitly_simulated(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as tmp:
            a, b = Path(tmp) / 'a', Path(tmp) / 'b'
            for target in [a, b]:
                result = self.cli(target)
                self.assertEqual(result.returncode, 0, result.stderr)
            for name in ['inventario.csv', 'decisiones.csv', 'cambios_solo_escenario.csv', 'resumen.json']:
                self.assertEqual((a / name).read_bytes(), (b / name).read_bytes())
            with (a / 'cambios_solo_escenario.csv').open(encoding='utf-8-sig') as f:
                changes = list(csv.DictReader(f))
            self.assertEqual(len(changes), 3)
            self.assertTrue(all(x['Estado'] == 'SIMULADO_NO_APLICADO' for x in changes))

    def test_cli_rejects_overwrite(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as tmp:
            path = Path(tmp)
            (path / 'resumen.json').write_text('No sobrescribir')
            self.assertNotEqual(self.cli(path).returncode, 0)
            self.assertEqual((path / 'resumen.json').read_text(), 'No sobrescribir')
            self.assertFalse((path / 'inventario.csv').exists())

    def test_cli_rejects_data_output(self):
        self.assertNotEqual(self.cli(ROOT / 'data').returncode, 0)


if __name__ == '__main__':
    unittest.main()
