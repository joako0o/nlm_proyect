"""Pruebas de ``scripts/cerrar_marcas_cotejadas.py``.

La herramienta escribe sobre el registro real, así que cada prueba la apunta a una
copia temporal. Lo que se protege aquí es que un cierre mal formado no se escriba:
el registro es el gold standard y un ``Marca`` pisado a mano no deja rastro.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
import cerrar_marcas_cotejadas as cm  # noqa: E402

ABIERTA = 'NOMBRE_PROPIO_POR_COTEJAR'
MOTIVO_OK = 'COTEJADO CONTRA PDF. El documento escribe el nombre sin tilde; el corpus es fiel.'


def registro_minimo():
    return {
        'Version': 1,
        'Correcciones': [],
        'Marcas_Adicionales': [],
        'Revisiones_Sin_Correccion': [
            {'ID_Intervencion': 'RPM-2005-06-09:279:1', 'Marca': ABIERTA,
             'Motivo': 'SIN_VERIFICAR.', 'Texto_Original_Fragmento': 'don Luis Oscar Herrera'},
            {'ID_Intervencion': 'RPM-2006-10-12:881:1 / RPM-2006-10-12:882:1',
             'Marca': 'CIFRA_INCONSISTENTE_POR_COTEJAR', 'Motivo': 'Dos cifras.',
             'Texto_Original_Fragmento': 'frag'},
            {'ID_Intervencion': 'RPM-2007-01-01:10:1', 'Marca': 'NO_REQUIERE_COTEJO',
             'Motivo': 'NO_ES_OCR. Ya cerrado antes.', 'Texto_Original_Fragmento': 'x'},
            {'ID_Intervencion': 'RPM-2008-01-01:20:1', 'Marca': ABIERTA,
             'Motivo': 'a', 'Texto_Original_Fragmento': 'uno'},
            {'ID_Intervencion': 'RPM-2008-01-01:20:1', 'Marca': ABIERTA,
             'Motivo': 'b', 'Texto_Original_Fragmento': 'dos'},
        ],
    }


class TestCerrarMarcasCotejadas(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.reg = Path(self.tmp.name) / 'reg.json'
        self.reg.write_text(json.dumps(registro_minimo(), ensure_ascii=False),
                            encoding='utf-8')
        self._reg_orig, self._argv = cm.REG, sys.argv
        cm.REG = self.reg
        self.addCleanup(self._restaurar)

    def _restaurar(self):
        cm.REG, sys.argv = self._reg_orig, self._argv

    def correr(self, cierres, aplicar=False):
        p = Path(self.tmp.name) / 'cierres.json'
        p.write_text(json.dumps(cierres, ensure_ascii=False), encoding='utf-8')
        sys.argv = ['cerrar_marcas_cotejadas.py', str(p)] + (['--aplicar'] if aplicar else [])
        return cm.main()

    def leido(self):
        return json.loads(self.reg.read_text(encoding='utf-8'))

    # --- camino feliz ---

    def test_cierra_una_marca_y_la_escribe(self):
        rc = self.correr([{'ID_Intervencion': 'RPM-2005-06-09:279:1',
                           'Marca': 'NO_REQUIERE_COTEJO', 'Motivo': MOTIVO_OK}], aplicar=True)
        self.assertEqual(rc, 0)
        r = self.leido()['Revisiones_Sin_Correccion'][0]
        self.assertEqual(r['Marca'], 'NO_REQUIERE_COTEJO')
        self.assertEqual(r['Motivo'], MOTIVO_OK)
        # el fragmento original se conserva: es la evidencia de qué se cotejó
        self.assertEqual(r['Texto_Original_Fragmento'], 'don Luis Oscar Herrera')

    def test_sin_aplicar_no_escribe_nada(self):
        antes = self.reg.read_text(encoding='utf-8')
        rc = self.correr([{'ID_Intervencion': 'RPM-2005-06-09:279:1',
                           'Marca': 'NO_REQUIERE_COTEJO', 'Motivo': MOTIVO_OK}])
        self.assertEqual(rc, 0)
        self.assertEqual(self.reg.read_text(encoding='utf-8'), antes)

    # --- rechazos: nada se escribe si algo falla ---

    def test_rechaza_una_marca_fuera_del_vocabulario(self):
        rc = self.correr([{'ID_Intervencion': 'RPM-2005-06-09:279:1',
                           'Marca': 'YA_ESTA_BIEN', 'Motivo': MOTIVO_OK}], aplicar=True)
        self.assertEqual(rc, 1)
        self.assertEqual(self.leido()['Revisiones_Sin_Correccion'][0]['Marca'], ABIERTA)

    def test_rechaza_un_cierre_sin_motivo(self):
        """Un cierre sin explicación es indistinguible de un borrado."""
        rc = self.correr([{'ID_Intervencion': 'RPM-2005-06-09:279:1',
                           'Marca': 'NO_REQUIERE_COTEJO', 'Motivo': '   '}], aplicar=True)
        self.assertEqual(rc, 1)
        self.assertEqual(self.leido()['Revisiones_Sin_Correccion'][0]['Marca'], ABIERTA)

    def test_rechaza_una_fila_que_no_tiene_revision(self):
        rc = self.correr([{'ID_Intervencion': 'RPM-1999-01-01:1:1',
                           'Marca': 'NO_REQUIERE_COTEJO', 'Motivo': MOTIVO_OK}], aplicar=True)
        self.assertEqual(rc, 1)

    def test_rechaza_cerrar_dos_veces_la_misma_marca(self):
        rc = self.correr([{'ID_Intervencion': 'RPM-2007-01-01:10:1',
                           'Marca': 'NO_REQUIERE_COTEJO', 'Motivo': MOTIVO_OK}], aplicar=True)
        self.assertEqual(rc, 1)

    def test_exige_desambiguar_cuando_la_fila_tiene_varias_revisiones(self):
        rc = self.correr([{'ID_Intervencion': 'RPM-2008-01-01:20:1',
                           'Marca': 'NO_REQUIERE_COTEJO', 'Motivo': MOTIVO_OK}], aplicar=True)
        self.assertEqual(rc, 1)
        # con el fragmento sí se puede
        rc = self.correr([{'ID_Intervencion': 'RPM-2008-01-01:20:1',
                           'Texto_Original_Fragmento': 'dos',
                           'Marca': 'NO_REQUIERE_COTEJO', 'Motivo': MOTIVO_OK}], aplicar=True)
        self.assertEqual(rc, 0)
        cerradas = [r for r in self.leido()['Revisiones_Sin_Correccion']
                    if r['ID_Intervencion'] == 'RPM-2008-01-01:20:1'
                    and r['Marca'] == 'NO_REQUIERE_COTEJO']
        self.assertEqual(len(cerradas), 1)
        self.assertEqual(cerradas[0]['Texto_Original_Fragmento'], 'dos')

    def test_se_niega_a_cerrar_una_entrada_que_cubre_varias_filas(self):
        """El registro admite «fila1 / fila2» y construir() marca ambas. Cerrar una
        cerraría la otra sin que nadie lo pida."""
        rc = self.correr([{'ID_Intervencion': 'RPM-2006-10-12:882:1',
                           'Marca': 'NO_REQUIERE_COTEJO', 'Motivo': MOTIVO_OK}], aplicar=True)
        self.assertEqual(rc, 1)
        r = self.leido()['Revisiones_Sin_Correccion'][1]
        self.assertEqual(r['Marca'], 'CIFRA_INCONSISTENTE_POR_COTEJAR')


if __name__ == '__main__':
    unittest.main()
