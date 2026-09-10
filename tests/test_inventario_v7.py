"""Inventario v7 y triaje lote7: rendición de cuentas de los 71 pares del lote6.

Ambos scripts publican una vista nueva y fallan cerrados si la contabilidad no
cuadra. Estos tests los ejecutan de verdad, no reimplementan su lógica.
"""
import collections
import csv
import json
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import functional_refinements_v5 as f5
import inventario_procedimental_v7 as inv7
import triaje_lote7
from diagnosticar_finales import read_rows
from reviewed_intrapara_v4 import RESERVAS_ABIERTAS

LOTE7 = ROOT / 'docs/continuidad_lote7_2026-09-09/triaje_53.json'
INVENTARIO = ROOT / 'docs/procedimental_v7_2026-09-09/inventario_estado_v7.csv'


def run(script, dest):
    proc = subprocess.run([sys.executable, str(ROOT / 'scripts' / script), '--salida', str(dest)],
                          cwd=ROOT, capture_output=True, text=True)
    if proc.returncode:
        raise AssertionError(f'{script} falló: {proc.stderr[-800:]}')
    return proc.stdout


class InventarioV7Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {r['ID_Intervencion']: r
                    for r in read_rows(ROOT / 'data/releases/continuidad_procedimental_v7'
                                       / 'consolidado_base_referencia.xlsx')}
        with INVENTARIO.open(encoding='utf-8-sig') as fh:
            cls.vista = list(csv.DictReader(fh))
        cls.triaje = json.loads(LOTE7.read_text())

    # ---------- triaje ----------
    def test_triaje_has_both_endpoints_and_unchanged_counts(self):
        self.assertEqual(self.triaje['Version'], 2)
        self.assertEqual(self.triaje['Pares'], 53)
        self.assertEqual(len(self.triaje['Registros']), 53)
        self.assertEqual(self.triaje['SHA256_Base'], f5.BASE_SHA)
        # La versión 1 guardaba el extremo derecho en unas causas y el izquierdo en
        # otras; ahora cada registro debe llevar ambos y servir como clave de par.
        izquierdas = [r['Izquierda'] for r in self.triaje['Registros']]
        self.assertEqual(len(set(izquierdas)), 53)
        for r in self.triaje['Registros']:
            self.assertIn(r['Izquierda'], self.rows)
            self.assertIn(r['Derecha'], self.rows)
        conteo = collections.Counter(r['Causa'] for r in self.triaje['Registros'])
        self.assertEqual(dict(conteo), triaje_lote7.ESPERADOS)
        self.assertEqual(conteo['APORTE_PERSONAL_Y_CONSTANCIA_EN_UNA_FILA'], 29)

    def test_triaje_is_reproducible(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as temp:
            run('triaje_lote7.py', Path(temp) / 'nuevo')
            otro = json.loads((Path(temp) / 'nuevo/triaje_53.json').read_text())
        self.assertEqual(otro['Registros'], self.triaje['Registros'])

    def test_triaje_refuses_a_destination_outside_docs_or_cache(self):
        proc = subprocess.run([sys.executable, str(ROOT / 'scripts/triaje_lote7.py'),
                               '--salida', str(ROOT / 'data/processed/x')],
                              cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('destino nuevo', proc.stderr)

    # ---------- inventario ----------
    def test_inventory_accounts_for_all_71_lote6_pairs(self):
        self.assertEqual(len(self.vista), 71 + 29)
        estados = collections.Counter(r['Estado_Revision_Dirigida'] for r in self.vista)
        self.assertEqual(estados['SIN_ADJUDICACION_EN_ESTE_INVENTARIO'], 24)
        self.assertEqual(estados['SEPARACION_FUNCIONAL_APLICADA_V5'], 29)
        self.assertEqual(estados['SEPARACION_FUNCIONAL_V5_INTERNA'], 29)
        self.assertEqual(estados['ENLACE_INTRAPADRE_APLICADO_V6'], 2)
        self.assertEqual(estados['SEPARACION_RESPALDADA_PREVIAMENTE'], 10)
        self.assertEqual(estados['SEPARACION_FUNCIONAL_V4'], 3)
        self.assertEqual(sum(v for k, v in estados.items() if k.startswith('RESERVA_')), 3)
        resumen = json.loads((INVENTARIO.parent / 'resumen.json').read_text())
        self.assertEqual(resumen['Pares_Lote6'], 71)
        self.assertEqual(resumen['Alertas_Cerradas'], 0)
        self.assertEqual(resumen['Alertas_Antes'], 467)
        self.assertEqual(resumen['Alertas_Despues'], 484)

    def test_the_24_unadjudicated_all_carry_a_measured_cause(self):
        sin = [r for r in self.vista
               if r['Estado_Revision_Dirigida'] == 'SIN_ADJUDICACION_EN_ESTE_INVENTARIO']
        self.assertEqual(len(sin), 24)
        causas = collections.Counter(r['Causa_Lote7'] for r in sin)
        self.assertNotIn('', causas)
        self.assertEqual(sum(causas.values()), 24)
        # Ninguno de los 24 es un caso del clúster ya resuelto.
        self.assertNotIn('APORTE_PERSONAL_Y_CONSTANCIA_EN_UNA_FILA', causas)
        for r in sin:
            self.assertEqual(r['Alcance_Lectura'], 'CAUSA_MEDIDA_EN_LOTE7')

    def test_the_29_cuts_are_grouped_and_their_inner_limit_stays_open(self):
        revisadas = json.loads(f5.PATH.read_text())['Revisiones']
        for padre in f5.PARENTS:
            entry = revisadas[str(padre)]
            ant, fila = entry['ID_Anterior'], entry['ID_Fila_Original']
            self.assertEqual(self.rows[ant]['ID_Turno'], self.rows[fila]['ID_Turno'])
            constancia = fila.rsplit(':', 1)[0] + ':2'
            self.assertNotEqual(self.rows[fila]['ID_Turno'], self.rows[constancia]['ID_Turno'])
            self.assertEqual(self.rows[constancia]['Relacion_Turno'], 'INSTITUCIONAL')
            self.assertEqual(self.rows[constancia]['Tipo_Acta'], 'ACUERDO_CONSEJO')
        internos = [r for r in self.vista
                    if r['Estado_Revision_Dirigida'] == 'SEPARACION_FUNCIONAL_V5_INTERNA']
        self.assertEqual(len(internos), 29)
        for r in internos:
            self.assertIn('debe seguir separado', r['Siguiente_Accion'])

    def test_reserves_stay_open_in_the_inventory(self):
        abiertas = [r for r in self.vista if r['Izquierda'] in RESERVAS_ABIERTAS]
        self.assertEqual(len(abiertas), 3)
        for r in abiertas:
            self.assertTrue(r['Estado_Revision_Dirigida'].startswith('RESERVA_'))
            self.assertEqual(r['Corte_Aplicado_V7'], 'NO')
            self.assertNotEqual(self.rows[r['Izquierda']]['ID_Turno'],
                                self.rows[r['Derecha']]['ID_Turno'])

    def test_inventory_is_reproducible(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as temp:
            run('inventario_procedimental_v7.py', Path(temp) / 'nuevo')
            with (Path(temp) / 'nuevo/inventario_estado_v7.csv').open(encoding='utf-8-sig') as fh:
                otra = list(csv.DictReader(fh))
        self.assertEqual(otra, self.vista)

    def test_inventory_rejects_a_changed_v7_release(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as temp:
            destino = Path(temp) / 'nuevo'
            with unittest.mock.patch.object(inv7, 'V7_SHA', '0' * 64):
                with self.assertRaises(ValueError):
                    inv7.main(['--salida', str(destino)])


if __name__ == '__main__':
    unittest.main()
