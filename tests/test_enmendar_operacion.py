"""Pruebas de ``scripts/enmendar_operacion.py``.

La regla de §15 es que dos defectos en el mismo tramo se resuelven extendiendo
la operación existente, no apilando otra. Estas pruebas protegen que la
enmienda no cree una operación nueva ni pise otra por accidente.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
import enmendar_operacion as en  # noqa: E402

RID = 'RPM-2014-06-12:6282:1'


def registro_minimo():
    return {
        'Version': 1,
        'Marcas_Adicionales': [],
        'Revisiones_Sin_Correccion': [],
        'Correcciones': [{
            'ID_Intervencion': RID,
            'Operaciones': [
                {'Tipo': 'ESPACIO_INDEBIDO', 'Antes': 'producirán .las caídas',
                 'Despues': 'producirán.las caídas', 'Contexto': 'c',
                 'Justificacion': 'Espacio indebido.'},
                {'Tipo': 'ACENTO_FALTANTE', 'Antes': 'otra cosa',
                 'Despues': 'otra cosa más', 'Contexto': 'c',
                 'Justificacion': 'Tilde.'},
            ],
        }],
    }


class TestEnmendarOperacion(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.reg = Path(self.tmp.name) / 'reg.json'
        self.reg.write_text(json.dumps(registro_minimo(), ensure_ascii=False),
                            encoding='utf-8')
        self._reg, self._argv = en.REG, sys.argv
        en.REG = self.reg
        self.addCleanup(lambda: setattr(en, 'REG', self._reg))
        self.addCleanup(lambda: setattr(sys, 'argv', self._argv))

    def correr(self, enmiendas, aplicar=False):
        p = Path(self.tmp.name) / 'enm.json'
        p.write_text(json.dumps(enmiendas, ensure_ascii=False), encoding='utf-8')
        sys.argv = ['enmendar_operacion.py', str(p)] + (['--aplicar'] if aplicar else [])
        return en.main()

    def ops(self):
        return json.loads(self.reg.read_text(encoding='utf-8'))['Correcciones'][0]['Operaciones']

    def test_enmienda_en_el_lugar_sin_crear_operacion_nueva(self):
        rc = self.correr([{
            'ID_Intervencion': RID, 'Antes': 'producirán .las caídas',
            'Tipo': 'SIMBOLO_SUELTO', 'Despues': 'producirán las caídas',
            'Justificacion': 'El punto es espurio: la oración sigue.'}], aplicar=True)
        self.assertEqual(rc, 0)
        ops = self.ops()
        self.assertEqual(len(ops), 2, 'no debe añadir una operación, sino enmendar')
        self.assertEqual(ops[0]['Tipo'], 'SIMBOLO_SUELTO')
        self.assertEqual(ops[0]['Despues'], 'producirán las caídas')
        # el Antes no se toca: es lo que ancla la operación al texto virgen
        self.assertEqual(ops[0]['Antes'], 'producirán .las caídas')
        # la otra operación de la fila queda intacta
        self.assertEqual(ops[1]['Tipo'], 'ACENTO_FALTANTE')

    def test_sin_aplicar_no_escribe(self):
        antes = self.reg.read_text(encoding='utf-8')
        self.correr([{'ID_Intervencion': RID, 'Antes': 'producirán .las caídas',
                      'Tipo': 'SIMBOLO_SUELTO', 'Despues': 'producirán las caídas',
                      'Justificacion': 'x' * 50}])
        self.assertEqual(self.reg.read_text(encoding='utf-8'), antes)

    def test_rechaza_un_tipo_fuera_de_vocabulario(self):
        rc = self.correr([{'ID_Intervencion': RID, 'Antes': 'producirán .las caídas',
                           'Tipo': 'ARREGLO_MAGICO', 'Despues': 'producirán las caídas',
                           'Justificacion': 'x' * 50}], aplicar=True)
        self.assertEqual(rc, 1)
        self.assertEqual(self.ops()[0]['Tipo'], 'ESPACIO_INDEBIDO')

    def test_rechaza_un_antes_que_no_existe(self):
        rc = self.correr([{'ID_Intervencion': RID, 'Antes': 'tramo inexistente',
                           'Tipo': 'SIMBOLO_SUELTO', 'Despues': 'otra cosa',
                           'Justificacion': 'x' * 50}], aplicar=True)
        self.assertEqual(rc, 1)

    def test_rechaza_una_enmienda_que_no_cambia_nada(self):
        rc = self.correr([{'ID_Intervencion': RID, 'Antes': 'producirán .las caídas',
                           'Tipo': 'ESPACIO_INDEBIDO', 'Despues': 'producirán.las caídas',
                           'Justificacion': 'x' * 50}], aplicar=True)
        self.assertEqual(rc, 1)

    def test_rechaza_un_despues_igual_al_antes(self):
        rc = self.correr([{'ID_Intervencion': RID, 'Antes': 'producirán .las caídas',
                           'Tipo': 'SIMBOLO_SUELTO', 'Despues': 'producirán .las caídas',
                           'Justificacion': 'x' * 50}], aplicar=True)
        self.assertEqual(rc, 1)


if __name__ == '__main__':
    unittest.main()
