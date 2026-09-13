"""Contratos del registro curado de correcciones de OCR (v1).

Política bajo prueba: ``Texto`` verbatim intacto, correcciones en la columna
paralela ``Texto_Corregido``, lo no resuelto marcado en ``Cotejar_PDF`` con
vocabulario controlado, cero reglas automáticas, residuos de fuente
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

    def validar(self, reg=None):
        return m.validar(reg or self.reg, m.BASE)

    def test_politica_declarada(self):
        p = self.reg['Politica']
        self.assertEqual(p['Texto_Verbatim'], 'INTACTO')
        self.assertEqual(p['Columna_Nueva'], 'Texto_Corregido')
        self.assertEqual(p['Columna_Cotejo'], 'Cotejar_PDF')
        self.assertIs(p['Reglas_Automaticas'], False)
        self.assertEqual(p['Residuos_Fuente'], 'ELIMINAR')

    def test_validacion_pasa(self):
        ok, problemas, corregidas, marcas = self.validar()
        self.assertTrue(ok, problemas)
        self.assertTrue(corregidas, 'el registro no corrige ninguna fila')
        self.assertTrue(marcas, 'el registro no marca ninguna fila para cotejo')

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
        _, _, corregidas, _ = self.validar()
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
        ok, problemas, _, _ = self.validar(reg)
        self.assertFalse(ok)
        self.assertTrue(any('zzz_no_existe_zzz' in p for p in problemas))

    def test_justificacion_vacia_hace_fallar(self):
        reg = json.loads(json.dumps(self.reg))
        reg['Correcciones'][0]['Operaciones'][0]['Justificacion'] = '   '
        ok, problemas, _, _ = self.validar(reg)
        self.assertFalse(ok)
        self.assertTrue(any('Justificacion' in p for p in problemas))

    def test_tipo_desconocido_hace_fallar(self):
        reg = json.loads(json.dumps(self.reg))
        reg['Correcciones'][0]['Operaciones'][0]['Tipo'] = 'REESCRITURA_LIBRE'
        ok, problemas, _, _ = self.validar(reg)
        self.assertFalse(ok)
        self.assertTrue(any('tipo desconocido' in p for p in problemas))

    def test_reglas_automaticas_activadas_hace_fallar(self):
        reg = json.loads(json.dumps(self.reg))
        reg['Politica']['Reglas_Automaticas'] = True
        ok, problemas, _, _ = self.validar(reg)
        self.assertFalse(ok)
        self.assertTrue(any('Reglas_Automaticas' in p for p in problemas))

    def test_operaciones_de_una_fila_no_pueden_pisarse(self):
        """Regresión: una operación cuyo ``Antes`` sólo existe después de aplicar
        otra de la misma fila debe rechazarse. Fue un error real en 943:1."""
        reg = json.loads(json.dumps(self.reg))
        rid = 'RPM-2006-10-12:943:1'
        entrada = next(e for e in reg['Correcciones'] if e['ID_Intervencion'] == rid)
        texto = self.filas[rid]['Texto']
        entrada['Operaciones'] = [
            {'Tipo': 'PUNTUACION', 'Antes': 'la inflación proyectada.”',
             'Despues': 'la inflación proyectada.', 'Contexto': 'x', 'Justificacion': 'y'},
            {'Tipo': 'RESIDUO_PAGINACION',
             'Antes': 'la inflación proyectada.\n17.30 horas.',
             'Despues': 'la inflación proyectada.', 'Contexto': 'x', 'Justificacion': 'y'},
        ]
        self.assertNotIn('la inflación proyectada.\n17.30 horas.', texto,
                         'el caso de prueba dejó de ser un caso de prueba')
        ok, problemas, _, _ = self.validar(reg)
        self.assertFalse(ok)
        self.assertTrue(any('texto virgen' in p for p in problemas), problemas)

    # --- columna Cotejar_PDF ---

    def test_revisiones_descartadas_tienen_motivo_y_marca(self):
        self.assertTrue(self.reg['Revisiones_Sin_Correccion'])
        for r in self.reg['Revisiones_Sin_Correccion']:
            self.assertTrue(r['Motivo'].strip())
            self.assertTrue(r['Texto_Original_Fragmento'].strip())
            self.assertIn(r['Marca'], m.MARCAS_VALIDAS, r['Marca'])

    def test_marcas_adicionales_existen_en_la_base(self):
        for a in self.reg['Marcas_Adicionales']:
            self.assertIn(a['ID_Intervencion'], self.filas, a['ID_Intervencion'])
            self.assertIn(a['Marca'], m.MARCAS_VALIDAS)

    def test_marca_fuera_del_vocabulario_hace_fallar(self):
        reg = json.loads(json.dumps(self.reg))
        reg['Revisiones_Sin_Correccion'][0]['Marca'] = 'REVISAR_A_OJO'
        ok, problemas, _, _ = self.validar(reg)
        self.assertFalse(ok)
        self.assertTrue(any('fuera del vocabulario' in p for p in problemas))

    def test_no_requiere_cotejo_no_genera_marca(self):
        reg = json.loads(json.dumps(self.reg))
        reg['Revisiones_Sin_Correccion'] = [
            {'ID_Intervencion': 'RPM-2006-10-12:892:1',
             'Texto_Original_Fragmento': 'pero si está vinculado',
             'Motivo': 'condicional correcto', 'Marca': 'NO_REQUIERE_COTEJO'}]
        reg['Marcas_Adicionales'] = []
        ok, _, _, marcas = self.validar(reg)
        self.assertTrue(ok)
        self.assertNotIn('RPM-2006-10-12:892:1', marcas)

    def test_las_tres_reservas_quedan_marcadas(self):
        _, _, _, marcas = self.validar()
        for rid in ('RPM-2006-07-13:780:2', 'RPM-2006-07-13:780:3',
                    'RPM-2009-08-13:2661:6', 'RPM-2009-08-13:2661:7',
                    'RPM-2012-12-13:5252:3', 'RPM-2012-12-13:5252:4'):
            self.assertIn('RESERVA_ABIERTA_POR_COTEJO', marcas.get(rid, []), rid)

    def test_texto_danado_se_arrastra_solo_a_la_marca(self):
        _, _, _, marcas = self.validar()
        arrastradas = [rid for rid, r in self.filas.items()
                       if m.MOTIVO_QUE_MARCA in (r.get('Motivos_Revision') or '')]
        self.assertTrue(arrastradas, 'no hay filas con TEXTO_DANADO_POR_COTEJAR en la base')
        for rid in arrastradas:
            self.assertIn(m.MOTIVO_QUE_MARCA, marcas[rid], rid)


class TestSalidaVersionada(unittest.TestCase):

    def test_verbatim_intacto_y_columnas_solo_donde_corresponde(self):
        _, _, esperadas, marcas = m.validar()
        tmp = Path(tempfile.mkdtemp(prefix='ocr_v1_'))
        try:
            self.assertEqual(m.construir(m.BASE, tmp), 0)
            salida = tmp / 'consolidado_texto_corregido.xlsx'
            self.assertTrue(salida.exists())
            filas = list(m.read_rows(salida))
            fuente = {r['ID_Intervencion']: r for r in m.read_rows(m.BASE)}
            self.assertEqual(len(filas), len(fuente))
            n_txt = n_mar = 0
            for r in filas:
                rid = r['ID_Intervencion']
                self.assertEqual(r['Texto'], fuente[rid]['Texto'],
                                 f'{rid}: Texto verbatim fue modificado')
                val = r.get('Texto_Corregido')
                if val:
                    n_txt += 1
                    self.assertIn(rid, esperadas)
                    self.assertEqual(val, esperadas[rid])
                    self.assertNotEqual(val, r['Texto'])
                else:
                    self.assertNotIn(rid, esperadas)
                mar = r.get('Cotejar_PDF')
                if mar:
                    n_mar += 1
                    self.assertEqual(sorted(mar.split(';')), sorted(marcas[rid]))
                    for x in mar.split(';'):
                        self.assertTrue(x in m.MARCAS_VALIDAS or x == m.MOTIVO_QUE_MARCA, x)
                else:
                    self.assertNotIn(rid, marcas)
            self.assertEqual(n_txt, len(esperadas))
            self.assertEqual(n_mar, len(marcas))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
