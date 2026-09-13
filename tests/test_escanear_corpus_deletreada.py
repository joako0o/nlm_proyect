"""Pruebas del detector de palabras deletreadas de ``scripts/escanear_corpus.py``.

La familia apareció en §26 leyendo la sesión 2007-08-09: el OCR esparce la palabra
en trozos cortos (``n o tic ia s`` -> ``noticias``). ``detector_partida`` no la
veía porque busca una partición en DOS mitades. El detector nuevo nació con tres
defectos que cada uno produjo un conteo falso, y esta prueba existe para que no
vuelvan: sin fronteras detectaba de más, el regex greedioso perdía la candidata
buena, y el umbral de frecuencia bloqueaba las letras sueltas.
"""
from __future__ import annotations

import io
import sys
import unittest
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
import escanear_corpus as ec  # noqa: E402


def correr(salida, freq, min_frec=20):
    """Devuelve (total, lista de pares (fragmento, unida)) que reporta."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        ec.detector_deletreada(salida, freq, min_frec, limite=100)
    total = None
    pares = []
    for linea in buf.getvalue().splitlines():
        if 'total candidatos:' in linea:
            total = int(linea.split('total candidatos:')[1].split()[0])
        elif '->' in linea and 'frec' in linea:
            frag = linea.split('->')[0].strip().strip("'")
            unida = linea.split('->')[1].split('(frec')[0].strip()
            pares.append((frag, unida))
    if total is None:
        raise AssertionError('el detector no informó total: %r' % buf.getvalue())
    return total, pares


class TestDetectorDeletreada(unittest.TestCase):
    def test_detecta_una_palabra_esparcida_en_cinco_trozos(self):
        """El caso real de 1357:1: «n o tic ia s» -> «noticias»."""
        freq = Counter({'noticias': 944, 'las': 5000, 'han': 4000,
                        'sido': 3000, 'negativas': 200})
        salida = {'RPM-1999-01-01:1:1':
                  'en el margen las n o tic ia s han sido negativas'}
        total, pares = correr(salida, freq)
        self.assertEqual(total, 1)
        self.assertIn(('n o tic ia s', 'noticias'), pares)

    def test_no_detecta_el_final_de_una_palabra_larga(self):
        """Trampa 1: sin frontera izquierda, «panorama de» daba «ma de»->«made»."""
        freq = Counter({'made': 30, 'panorama': 100, 'de': 9000,
                        'mediano': 800, 'plazo': 700, 'un': 9000})
        salida = {'RPM-1999-01-01:1:1':
                  'apuntaban a un panorama de mediano plazo'}
        total, _ = correr(salida, freq)
        self.assertEqual(total, 0)

    def test_no_se_pierde_porque_el_regex_sea_greedioso(self):
        """Trampa 2: la carrera maximal «n o tic ia s han sido» no es palabra.

        ``re.finditer`` entrega sólo la carrera completa y no vuelve atrás por un
        filtro posterior; si no se enumeran sub-ventanas, la candidata buena se
        pierde entera y el detector da 0 con ``freq['noticias'] = 944``.
        """
        freq = Counter({'noticias': 944, 'las': 5000, 'han': 4000,
                        'sido': 3000, 'negativas': 200, 'Sin': 900,
                        'embargo': 300, 'la': 9000, 'producción': 400})
        salida = {'RPM-1999-01-01:1:1':
                  'las n o tic ia s han sido negativas. Sin embargo, la producción'}
        total, pares = correr(salida, freq)
        self.assertGreaterEqual(total, 1)
        self.assertIn(('n o tic ia s', 'noticias'), pares)

    def test_detecta_tres_letras_sueltas_aunque_cada_letra_sea_frecuente(self):
        """Trampa 3: «T a s a» -> «Tasa», con «T»=38, «a»=37540, «s»=90.

        Las letras sueltas son frecuentes *precisamente* porque este defecto las
        esparce por el corpus; pedir freq == 0 las bloqueaba a todas.
        """
        freq = Counter({'Tasa': 4902, 'T': 38, 'a': 37540, 's': 90,
                        'de': 9000, 'Política': 1500, 'Monetaria': 900})
        salida = {'RPM-1999-01-01:1:1':
                  'ajustes de 25 puntos base de la T a s a de Política Monetaria'}
        total, pares = correr(salida, freq)
        self.assertEqual(total, 1)
        self.assertIn(('T a s a', 'Tasa'), pares)

    def test_no_junta_una_secuencia_legitima_de_palabras_cortas(self):
        """«y o» -> «yo» y «a los» son palabras reales separadas por espacio."""
        freq = Counter({'yo': 500, 'y': 39186, 'o': 3430, 'a': 37540,
                        'los': 8000, 'consejeros': 300})
        salida = {'RPM-1999-01-01:1:1': 'dijo que y o a los consejeros'}
        total, _ = correr(salida, freq)
        self.assertEqual(total, 0)

    def test_exige_que_la_palabra_unida_esté_establecida(self):
        """Unir en una palabra de frecuencia 4 no es evidencia (§21: hace falta
        prueba, no plausibilidad)."""
        freq = Counter({'espere': 4, 'es': 9000, 'pere': 1, 'que': 100805,
                        'la': 9000, 'tasa': 3000, 'suba': 200})
        salida = {'RPM-1999-01-01:1:1': 'no es pere que la tasa suba'}
        total, _ = correr(salida, freq)
        self.assertEqual(total, 0)

    def test_deja_la_mas_larga_en_cada_posicion_de_inicio(self):
        """«a ctu a lm e n te» -> «actualmente», no «actu» ni «actual»."""
        freq = Counter({'actualmente': 213, 'a': 37540, 'de': 9000,
                        'inflación': 4000, 'en': 9000, 'el': 9000})
        salida = {'RPM-1999-01-01:1:1':
                  'la inflación a ctu a lm e n te en el país'}
        total, pares = correr(salida, freq)
        self.assertEqual(total, 1)
        self.assertEqual(pares[0], ('a ctu a lm e n te', 'actualmente'))


if __name__ == '__main__':
    unittest.main()
