"""Contratos del registro curado de correcciones de OCR (v1).

Política bajo prueba: ``Texto`` verbatim intacto, correcciones en la columna
paralela ``Texto_Corregido``, cero reglas automáticas, residuos de fuente
eliminados. Cada operación debe estar curada con contexto y justificación, y
``Antes`` debe existir literalmente en el texto fuente.
"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'scripts'))

import correcciones_ocr_v1 as m  # noqa: E402


class TestRegistroCurado(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.reg = m.cargar()
        cls.filas = {r['ID_Intervencion']: r for r in m.read_rows(m.BASE)}

    def test_politica_declarada(self):
        p = self.reg['Politica']
        self.assertEqual(p['Texto_Verbatim'], 'INTACTO')
        self.assertEqual(p['Columna_Nueva'], 'Texto_Corregido')
        self.assertIs(p['Reglas_Automaticas'], False)
        self.assertEqual(p['Residuos_Fuente'], 'ELIMINAR')

    def test_validacion_pasa(self):
        ok, problemas, corregidas = m.validar(self.reg, m.BASE)
        self.assertTrue(ok, problemas)
        self.assertTrue(corregidas, 'el registro no corrige ninguna fila')

    def test_antes_existe_literal_en_el_texto_fuente(self):
        """El corazón de la política: nada se adivina."""
        for e in self.reg['Correcciones']:
            texto = self.filas[e['ID_Intervencion']]['Texto']
            for op in e['Operaciones']:
                self.assertIn(op['Antes'], texto,
                              f"{e['ID_Intervencion']}: «{op['Antes']}» no está en el texto")

    def test_toda_operacion_esta_curada(self):
        for e in self.reg['Correcciones']:
            self.assertTrue(e['Operaciones'], e['ID_Intervencion'])
            for op in e['Operaciones']:
                self.assertIn(op['Tipo'], m.TIPOS_VALIDOS, op['Tipo'])
                for campo in ('Contexto', 'Justificacion'):
                    self.assertTrue(op[campo].strip(),
                                    f"{e['ID_Intervencion']}: falta {campo}")
                self.assertNotEqual(op['Antes'], op['Despues'])

    def test_aplicar_no_toca_el_original(self):
        for e in self.reg['Correcciones']:
            original = self.filas[e['ID_Intervencion']]['Texto']
            copia = original
            m.aplicar_a_texto(copia, e['Operaciones'], e['ID_Intervencion'])
            self.assertEqual(copia, original, 'aplicar_a_texto mutó el texto fuente')

    def test_no_vuelve_a_corregir_sobre_lo_corregido(self):
        """Aplicar dos veces no debe apilar cambios: al no estar ya ``Antes``,
        no se reemplaza nada y el texto sale igual."""
        _, _, corregidas = m.validar(self.reg, m.BASE)
        for e in self.reg['Correcciones']:
            rid = e['ID_Intervencion']
            una = corregidas[rid]
            dos, problemas = m.aplicar_a_texto(una, e['Operaciones'], rid)
            self.assertEqual(dos, una, f'{rid}: se volvió a modificar un texto ya corregido')
            self.assertTrue(problemas,
                            f'{rid}: debió reportar que «Antes» ya no está en el texto')

    def test_antes_inexistente_hace_fallar_la_validacion(self):
        reg = json.loads(json.dumps(self.reg))
        reg['Correcciones'].append({
            'ID_Intervencion': next(iter(self.filas)),
            'Operaciones': [{'Tipo': 'PALABRA_ERRONEA',
                             'Antes': 'zzz_no_existe_zzz',
                             'Despues': 'nada',
                             'Contexto': 'x', 'Justificacion': 'y'}]})
        ok, problemas, _ = m.validar(reg, m.BASE)
        self.assertFalse(ok)
        self.assertTrue(any('zzz_no_existe_zzz' in p for p in problemas))

    def test_justificacion_vacia_hace_fallar(self):
        reg = json.loads(json.dumps(self.reg))
        reg['Correcciones'][0]['Operaciones'][0]['Justificacion'] = '   '
        ok, problemas, _ = m.validar(reg, m.BASE)
        self.assertFalse(ok)
        self.assertTrue(any('Justificacion' in p for p in problemas))

    def test_tipo_desconocido_hace_fallar(self):
        reg = json.loads(json.dumps(self.reg))
        reg['Correcciones'][0]['Operaciones'][0]['Tipo'] = 'REESCRITURA_LIBRE'
        ok, problemas, _ = m.validar(reg, m.BASE)
        self.assertFalse(ok)
        self.assertTrue(any('tipo desconocido' in p for p in problemas))

    def test_reglas_automaticas_activadas_hace_fallar(self):
        reg = json.loads(json.dumps(self.reg))
        reg['Politica']['Reglas_Automaticas'] = True
        ok, problemas, _ = m.validar(reg, m.BASE)
        self.assertFalse(ok)
        self.assertTrue(any('Reglas_Automaticas' in p for p in problemas))

    def test_revisiones_descartadas_tienen_motivo(self):
        self.assertTrue(self.reg['Revisiones_Sin_Correccion'])
        for r in self.reg['Revisiones_Sin_Correccion']:
            self.assertTrue(r['Motivo'].strip())
            self.assertTrue(r['Texto_Original_Fragmento'].strip())


class TestSalidaVersionada(unittest.TestCase):

    def test_texto_verbatim_sale_intacto_y_solo_las_corregidas_llevan_columna(self):
        _, _, esperadas = m.validar()
        tmp = Path(tempfile.mkdtemp(prefix='ocr_v1_'))
        try:
            self.assertEqual(m.construir(m.BASE, tmp), 0)
            salida = tmp / 'consolidado_texto_corregido.xlsx'
            self.assertTrue(salida.exists())
            filas = list(m.read_rows(salida))
            self.assertEqual(len(filas), len(list(m.read_rows(m.BASE))))
            fuente = {r['ID_Intervencion']: r for r in m.read_rows(m.BASE)}
            con_columna = 0
            for r in filas:
                rid = r['ID_Intervencion']
                self.assertEqual(r['Texto'], fuente[rid]['Texto'],
                                 f'{rid}: Texto verbatim fue modificado')
                val = r.get('Texto_Corregido')
                if val:
                    con_columna += 1
                    self.assertIn(rid, esperadas)
                    self.assertEqual(val, esperadas[rid])
                    self.assertNotEqual(val, r['Texto'])
                else:
                    self.assertNotIn(rid, esperadas)
            self.assertEqual(con_columna, len(esperadas))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
