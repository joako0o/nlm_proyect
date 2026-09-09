"""Lote7: lectura no cierra daño, modalidad o identidad provisional."""
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
import revisar_cola_comas as b
import revisar_comas_institucionales as institutional
import revisar_comas_con_reservas as review

PACKAGE = Path('docs/revision_comas_lote7_2026-09-08/revisiones.json')


class ReservedCommaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = b.read_rows(ROOT / 'data/processed/consolidado_base_referencia.xlsx')
        cls.pkg = json.loads((ROOT / PACKAGE).read_text())

    def parent(self, p):
        return [x for x in self.rows if x['ID_Padre'] == p]

    def one(self, e):
        p = e['ID_Padre']
        ids = [i for i, x in enumerate(self.rows) if x['ID_Padre'] == p]
        rows = copy.deepcopy(self.rows[ids[0] - 1:ids[-1] + 2])
        pkg = copy.deepcopy(self.pkg)
        pkg['Revisiones'] = [copy.deepcopy(e)]
        pkg['Padres'] = {str(p): pkg['Padres'][str(p)]}
        pkg['Antecedentes'] = [x for x in pkg['Antecedentes'] if x['ID_Padre'] == p]
        control = review.CASES[e['Izquierda']['ID_Intervencion']]['Control']
        pkg['Controles'] = {} if control is None else {str(control): pkg['Controles'][str(control)]}
        if control:
            rows = copy.deepcopy(self.parent(control)) + rows
        return rows, pkg

    def test_three_fiches_and_reading_units(self):
        self.assertEqual(len(review.validate_reviews(self.rows, self.pkg)), 3)
        self.assertEqual(sum(len(x['Texto_Padre']) for x in self.pkg['Padres'].values()), 5022)
        self.assertEqual(sum(len(x['Texto_Padre']) for x in self.pkg['Controles'].values()), 3053)
        self.assertEqual(sum(len(x[k]['Intervalo']['Texto']) for x in self.pkg['Padres'].values()
                             for k in ['Vecino_Anterior', 'Vecino_Siguiente']), 18783)
        self.assertEqual(len(self.pkg['Antecedentes']), 6)

    def test_only_additional_motive_cases_in_inventory(self):
        cases = [x for x in b.diagnose(self.rows)
                 if x['Categoria'] == b.CATEGORY and not x['Solo_Este_Motivo']]
        self.assertEqual({x['ID_Intervencion'] for x in cases}, set(review.CASES))
        self.assertEqual({x['ID_Padre'] for x in self.pkg['Revisiones']}, {2680, 2779, 2957})

    def test_separate_dimensions_and_immutable_inputs(self):
        before = copy.deepcopy((self.rows, self.pkg))
        table = review.build_risk_table(self.rows, self.pkg)
        self.assertEqual(len(table), 3)
        self.assertTrue(all(x['Estado_Limite'] == 'SEPARACION_EXISTENTE_RESPALDADA' for x in table))
        self.assertEqual(sum(x['Estado_Identidad'] == 'ATRIBUCION_LOCAL_PROVISIONAL' for x in table), 1)
        self.assertEqual(len({x['Estado_Reserva'] for x in table}), 3)
        self.assertEqual((self.rows, self.pkg), before)
        self.assertEqual(sum(bool(x['Motivos_Revision']) for x in self.rows), 465)

    def test_2680_restart_damage_number_and_long_continuity(self):
        rows = self.parent(2680)
        self.assertEqual([len(x['Texto']) for x in rows], [180, 75, 164, 489])
        self.assertEqual(rows[1]['Motivos_Revision'], 'FINAL_SIN_PUNTUACION;TEXTO_DANADO_POR_COTEJAR')
        self.assertIn('16; 15', rows[1]['Texto'])
        self.assertIn('N° 141', rows[1]['Texto'])
        self.assertIn('N° 142', self.pkg['Controles']['2656']['Texto_Padre'])
        self.assertEqual(rows[-1]['ID_Turno'], self.parent(2681)[0]['ID_Turno'])
        self.assertEqual(len(self.parent(2681)[0]['Texto']), 11085)
        self.assertTrue(rows[-1]['Texto'].endswith('A continuación,.'))
        self.assertIsNone(rows[-1]['Motivos_Revision'])
        self.assertNotEqual(rows[0]['ID_Turno'], rows[2]['ID_Turno'])

    def test_2779_assent_is_not_transcribed_words(self):
        rows = self.parent(2779)
        self.assertEqual([len(x['Texto']) for x in rows], [222, 22, 366])
        self.assertEqual(rows[1]['Texto'], 'El señor Soto asiente,')
        self.assertEqual(rows[1]['Motivos_Revision'], 'FINAL_SIN_PUNTUACION;FRAGMENTO_BREVE')
        e = next(e for e in self.pkg['Revisiones'] if e['ID_Padre'] == 2779)
        self.assertEqual(e['Naturaleza'], 'ASENTIMIENTO_NARRADO_SIN_PALABRAS_TRANSCRITAS')
        self.assertEqual(e['Estado_Reserva'], 'MODALIDAD_DEL_ASENTIMIENTO_NO_DETERMINADA')
        self.assertEqual(rows[2]['Actor_Final'], 'Enrique Marshall Rivera')
        self.assertIsNone(rows[2]['ID_Ancla_Actor'])
        self.assertNotEqual(rows[1]['ID_Turno'], self.parent(2780)[0]['ID_Turno'])

    def test_2957_provisional_name_and_distinct_reply(self):
        rows = self.parent(2957)
        self.assertEqual([len(x['Texto']) for x in rows], [772, 73, 117, 907, 1626])
        self.assertIn('Rabio García', rows[1]['Texto'])
        self.assertEqual(rows[1]['Motivos_Revision'], 'FINAL_SIN_PUNTUACION;NOMBRE_EN_DISCURSO_POR_VERIFICAR')
        self.assertEqual(rows[1]['Actor_Final'], 'Pablo García Silva')
        for x in rows[1:3]:
            self.assertEqual(x['Fuente_Actor'], 'CONTEXTO_REVISADO')
            self.assertIsNone(x['ID_Ancla_Actor'])
        roster = self.pkg['Controles']['2889']['Texto_Padre']
        self.assertIn('Pablo García Silva', roster)
        self.assertIn('Mariana García Schmidt', roster)
        e = next(e for e in self.pkg['Revisiones'] if e['ID_Padre'] == 2957)
        self.assertEqual(e['Estado_Identidad'], 'ATRIBUCION_LOCAL_PROVISIONAL')
        self.assertEqual(self.parent(2956)[-1]['ID_Turno'], rows[0]['ID_Turno'])
        self.assertEqual(self.parent(2958)[0]['Motivos_Revision'], 'TEXTO_DANADO_POR_COTEJAR')

    def test_cannot_promote_identity_or_close_reserve(self):
        for e in self.pkg['Revisiones']:
            for field, value in [('Estado_Identidad', 'CONFIRMADA'), ('Estado_Reserva', 'CERRADA'),
                                 ('Estado', b.STATE), ('Naturaleza', 'PALABRAS_PRONUNCIADAS'),
                                 ('Reservas', []), ('Siguiente_Accion', '')]:
                rows, pkg = self.one(e)
                pkg['Revisiones'][0][field] = value
                with self.assertRaises(ValueError):
                    review.validate_reviews(rows, pkg)

    def test_every_endpoint_bound_field_invalidates_fiche(self):
        for e in self.pkg['Revisiones']:
            for side in ['Izquierda', 'Derecha']:
                for field in b.BOUND_FIELDS:
                    rows, pkg = self.one(e)
                    row = next(x for x in rows if x['ID_Intervencion'] == e[side]['ID_Intervencion'])
                    row[field] = 'Cambio'
                    with self.subTest(p=e['ID_Padre'], side=side, field=field), self.assertRaises(ValueError):
                        review.validate_reviews(rows, pkg)

    def test_removing_extra_warning_is_not_route_to_approval(self):
        for e in self.pkg['Revisiones']:
            rows, pkg = self.one(e)
            next(x for x in rows if x['ID_Intervencion'] == e['Izquierda']['ID_Intervencion'])['Motivos_Revision'] = 'FINAL_SIN_PUNTUACION'
            with self.assertRaises(ValueError):
                review.validate_reviews(rows, pkg)

    def test_neighbors_and_rosters_bound(self):
        for e in self.pkg['Revisiones']:
            for neighbor in ['Vecino_Anterior', 'Vecino_Siguiente']:
                rows, pkg = self.one(e)
                key = pkg['Padres'][str(e['ID_Padre'])][neighbor]['Intervalo']['ID_Intervencion']
                next(x for x in rows if x['ID_Intervencion'] == key)['Texto'] += ' Cambio'
                with self.assertRaises(ValueError):
                    review.validate_reviews(rows, pkg)
        for p in [2656, 2889]:
            rows = copy.deepcopy(self.rows)
            next(x for x in rows if x['ID_Padre'] == p)['Texto'] += ' Cambio'
            with self.assertRaises(ValueError):
                review.validate_reviews(rows, self.pkg)

    def test_prior_records_are_verified_not_just_cited(self):
        for field in ['SHA256_Registro', 'Justificacion_Anterior', 'Fuente', 'Revision_ID']:
            pkg = copy.deepcopy(self.pkg)
            pkg['Antecedentes'][0][field] = 'Cambio'
            with self.assertRaises(ValueError):
                review.validate_reviews(self.rows, pkg)
        pkg = copy.deepcopy(self.pkg)
        pkg['Antecedentes'].pop()
        with self.assertRaises(ValueError):
            review.validate_reviews(self.rows, pkg)

    def test_source_and_raw_hashes_fail_closed(self):
        pkg = copy.deepcopy(self.pkg)
        pkg['SHA256_Fuentes']['data/curation/revisiones_hablantes.json'] = '0' * 64
        with self.assertRaises(ValueError):
            review.validate_reviews(self.rows, pkg)
        for p in pkg['Padres']:
            pkg = copy.deepcopy(self.pkg)
            pkg['Padres'][p]['SHA256_Texto_Padre'] = '0' * 64
            with self.assertRaises(ValueError):
                review.validate_reviews(self.rows, pkg)

    def test_duplicate_unknown_and_missing_evidence(self):
        pkg = copy.deepcopy(self.pkg)
        pkg['Revisiones'].append(copy.deepcopy(pkg['Revisiones'][0]))
        with self.assertRaises(ValueError):
            review.validate_reviews(self.rows, pkg)
        pkg = copy.deepcopy(self.pkg)
        pkg['Revisiones'][0]['Izquierda']['ID_Intervencion'] = 'RPM-2006-03-16:601:1'
        with self.assertRaises(ValueError):
            review.validate_reviews(self.rows, pkg)
        for field in ['Controles', 'Padres']:
            pkg = copy.deepcopy(self.pkg)
            pkg[field].pop(next(iter(pkg[field])))
            with self.assertRaises(ValueError):
                review.validate_reviews(self.rows, pkg)

    def test_old_validators_not_weakened(self):
        for e in self.pkg['Revisiones']:
            _, pkg = self.one(e)
            pkg['Revisiones'][0]['Estado'] = b.STATE
            with self.assertRaises(ValueError):
                b.validate_reviews(self.rows, pkg)
            pkg['Alcance'] = institutional.SCOPE
            pkg['Revisiones'][0]['Estado'] = institutional.STATE
            with self.assertRaises(ValueError):
                institutional.validate_institutional_reviews(self.rows, pkg)

    def test_merges_and_lost_links_rejected(self):
        for p, left_key, right_key in [
            (2680, 'RPM-2009-08-13:2680:1', 'RPM-2009-08-13:2680:3'),
            (2779, 'RPM-2009-11-12:2779:2', 'RPM-2009-11-12:2780:1'),
            (2957, 'RPM-2010-02-11:2957:2', 'RPM-2010-02-11:2957:3'),
        ]:
            e = next(e for e in self.pkg['Revisiones'] if e['ID_Padre'] == p)
            rows, pkg = self.one(e)
            index = {x['ID_Intervencion']: x for x in rows}
            index[right_key]['ID_Turno'] = index[left_key]['ID_Turno']
            with self.assertRaises(ValueError):
                review.validate_reviews(rows, pkg)
        rows = copy.deepcopy(self.rows)
        next(x for x in rows if x['ID_Padre'] == 2681)['ID_Turno'] = 'ENLACE_ROTO'
        with self.assertRaises(ValueError):
            review.validate_reviews(rows, self.pkg)

    def test_legacy_subqueue_stays_167(self):
        pkgs = [json.loads((ROOT / f'docs/revision_comas_lote{n}_2026-09-08/revisiones.json').read_text()) for n in range(1, 7)]
        queue = institutional.build_combined_queue(self.rows, pkgs[:5], pkgs[5])
        self.assertEqual(len(queue), 167)
        self.assertFalse(set(review.CASES) & {q['ID_Intervencion'] for q in queue})
        expected = json.loads((ROOT / 'docs/revision_comas_lote6_2026-09-08/resumen.json').read_text())
        for n in range(1, 7):
            path = ROOT / f'docs/revision_comas_lote{n}_2026-09-08/revisiones.json'
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, expected['SHA256_Lotes'][str(path.relative_to(ROOT))])

    def test_group_renumbering_does_not_change_relations(self):
        rows = copy.deepcopy(self.rows)
        for x in rows:
            x['ID_Turno'] = 'NUEVO:' + x['ID_Turno']
        self.assertEqual(len(review.validate_reviews(rows, self.pkg)), 3)

    def cli(self, output):
        return subprocess.run([sys.executable, 'scripts/revisar_comas_con_reservas.py',
                               '--revisiones', str(PACKAGE), '--salida', str(output)],
                              cwd=ROOT, capture_output=True, text=True, timeout=60)

    def test_cli_reproducible_open_reserves_and_no_overwrite(self):
        (ROOT / '.cache').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as tmp:
            a, z = Path(tmp) / 'a', Path(tmp) / 'z'
            for target in [a, z]:
                result = self.cli(target)
                self.assertEqual(result.returncode, 0, result.stderr)
            for name in ['riesgos_abiertos.csv', 'resumen.json']:
                self.assertEqual((a / name).read_bytes(), (z / name).read_bytes())
            summary = json.loads((a / 'resumen.json').read_text())
            self.assertEqual(summary['Reservas_Abiertas'], 3)
            self.assertEqual(summary['Alertas_Cerradas'], 0)
            with (a / 'riesgos_abiertos.csv').open(encoding='utf-8-sig') as f:
                self.assertEqual(len(list(csv.DictReader(f))), 3)
            before = {p.name: p.read_bytes() for p in a.iterdir()}
            self.assertNotEqual(self.cli(a).returncode, 0)
            self.assertEqual(before, {p.name: p.read_bytes() for p in a.iterdir()})

    def test_cli_protects_data(self):
        self.assertNotEqual(self.cli(ROOT / 'data').returncode, 0)


if __name__ == '__main__':
    unittest.main()
