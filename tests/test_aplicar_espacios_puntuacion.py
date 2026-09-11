"""Pruebas de las funciones puras de ``scripts/aplicar_espacios_puntuacion.py``.

Lo que importa aquí son las exclusiones: un detector que no distingue un espacio
indebido de unos puntos suspensivos rompe texto correcto en silencio.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
import aplicar_espacios_puntuacion as esp  # noqa: E402


class TestOcurrencias(unittest.TestCase):
    def casos(self, texto):
        return [(texto[i:j], texto[max(0, i-12):j+8]) for i, j in esp.ocurrencias(texto)]

    def test_detecta_el_espacio_antes_de_coma_punto_pyc_y_porcentaje(self):
        t = 'por su parte , además 5,0 % y 3 ; luego 4 .'
        # El tramo incluye el signo: sirve de borde derecho a la ventana de
        # contexto. Lo que se quita después es sólo el blanco que va delante.
        self.assertEqual([t[i:j] for i, j in esp.ocurrencias(t)],
                         [' ,', ' %', ' ;', ' .'])

    def test_no_toca_los_puntos_suspensivos(self):
        t = 'y entonces ... dijo que no'
        self.assertEqual(esp.ocurrencias(t), [])

    def test_no_toca_el_punto_duplicado_que_es_otra_familia(self):
        t = 'en dicha Tasa.. Agrega el señor'
        self.assertEqual(esp.ocurrencias(t), [])

    def test_no_toca_coma_ni_pyc_duplicados(self):
        self.assertEqual(esp.ocurrencias('uno ,, dos'), [])
        self.assertEqual(esp.ocurrencias('uno ;; dos'), [])
        self.assertEqual(esp.ocurrencias('5 %% anual'), [])

    def test_un_punto_normal_no_es_ocurrencia(self):
        self.assertEqual(esp.ocurrencias('Agrega que no. Luego sigue'), [])

    def test_no_pierde_ocurrencias_consecutivas(self):
        """§20: con grupos capturados el signo queda consumido por el match y
        ``re.finditer`` no lo vuelve a ofrecer como carácter anterior del
        siguiente, así que «2 ,5 % .» perdía el tercer espacio. Es la misma
        lección de §15 sobre finditer, reaparecida en esta herramienta.
        """
        t = 'alcanza a 2 ,5 % . En cuanto'
        self.assertEqual([t[i:j] for i, j in esp.ocurrencias(t)],
                         [' ,', ' %', ' .'])

    def test_devuelve_posiciones_utilizables(self):
        t = 'abc , def'
        (i, j), = esp.ocurrencias(t)
        self.assertEqual(t[i:j], ' ,')
        self.assertEqual(t[:i] + t[i:j].replace(' ', '', 1) + t[j:], 'abc, def')


class TestGrupos(unittest.TestCase):
    def test_fusiona_las_cercanas(self):
        oc = [(10, 12), (30, 32), (200, 202)]
        g = esp.grupos(oc, fusion=40)
        self.assertEqual([grp[0][0] for grp in g], [10, 200])
        self.assertEqual(len(g[0]), 2)

    def test_separa_las_lejanas(self):
        oc = [(0, 2), (500, 502)]
        self.assertEqual(len(esp.grupos(oc, fusion=40)), 2)

    def test_fusion_cero_no_fusiona_nada(self):
        oc = [(10, 12), (30, 32)]
        self.assertEqual(len(esp.grupos(oc, fusion=0)), 2)


class TestQuitarBlancos(unittest.TestCase):
    def test_quita_solo_el_blanco_de_cada_ocurrencia(self):
        t = 'uno , dos ; tres'
        oc = esp.ocurrencias(t)
        ini, fin = oc[0][0], oc[-1][1]
        out = esp.quitar_blancos(t, ini, fin, oc)
        self.assertEqual(out, ', dos;')   # sólo el tramo [ini:fin], sin lo que sigue
        # ninguna letra se perdió
        self.assertEqual(''.join(out.split()), ''.join(t[ini:fin].split()))


if __name__ == '__main__':
    unittest.main()
