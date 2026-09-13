"""Pruebas del detector de palabras partidas de ``scripts/escanear_corpus.py``.

El detector tenía su lección escrita en el docstring (``re.finditer`` no solapa)
y ninguna prueba. Por eso sobrevivió un punto ciego: la guarda «ninguna mitad con
frecuencia >= 50» bloqueaba todo ``m ayor`` porque el token ``m`` aparece 78 veces
en el corpus. Una letra suelta es frecuente *precisamente* porque la OCR parte
palabras. Medido: el detector daba 0 candidatos cuando quedaban 62 en 39 filas.
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
    """Devuelve el total de candidatos que reporta el detector."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        ec.detector_partida(salida, freq, min_frec, limite=100)
    for linea in buf.getvalue().splitlines():
        if 'total candidatos:' in linea:
            return int(linea.split('total candidatos:')[1].split()[0])
    raise AssertionError('el detector no informó total: %r' % buf.getvalue())


class TestDetectorPartida(unittest.TestCase):
    def test_detecta_letra_suelta_aunque_la_letra_sea_frecuente(self):
        """El caso que estaba roto: «m ayor» con «m» muy frecuente."""
        freq = Counter({'mayor': 4467, 'm': 78, 'de': 5000, 'el': 4000})
        salida = {'RPM-1999-01-01:1:1': 'un margen m ayor que el previsto de antemano'}
        self.assertEqual(correr(salida, freq), 1)

    def test_no_junta_cuando_la_primera_mitad_es_una_palabra(self):
        """«a», «y», «o», «e», «u» son palabras: la guarda tiene que seguir ahí."""
        freq = Counter({'ayor': 30, 'a': 37528, 'y': 39198, 'de': 5000, 'el': 4000})
        salida = {'RPM-1999-01-01:1:1': 'un margen a yor que el previsto de antemano'}
        self.assertEqual(correr(salida, freq), 0)

    def test_no_junta_dos_palabras_corrientes(self):
        """«de la» no es una palabra partida por más que «dela» figure en freq."""
        freq = Counter({'dela': 40, 'de': 5000, 'la': 9000, 'tasa': 800})
        salida = {'RPM-1999-01-01:1:1': 'la tasa dela reunión'}
        self.assertEqual(correr(salida, freq), 0)

    def test_no_junta_si_la_palabra_junta_no_es_frecuente(self):
        freq = Counter({'mayor': 3, 'm': 78})
        salida = {'RPM-1999-01-01:1:1': 'un margen m ayor'}
        self.assertEqual(correr(salida, freq), 0)

    def test_las_letras_palabra_estan_declaradas(self):
        self.assertEqual(ec.LETRAS_PALABRA, {'a', 'y', 'o', 'e', 'u', 'A'})


class TestLaGuardaNoSePuedeAbrir(unittest.TestCase):
    """§27: la guarda «primera mitad con frecuencia >= 50» tiene un punto ciego.

    «presenta ción» -> «presentación» no se detecta porque «presenta» aparece 513
    veces. La tentación es relajar la guarda cuando la segunda mitad no es palabra
    (freq < 20). Medido sobre las 9.723 filas: eso da 23 candidatas y **5 son
    falsos positivos que corromperían texto correcto**, porque la diferencia entre
    «presenta ción» y «con sumo cuidado» es semántica y no estadística: en ambos
    casos la primera mitad es común, la segunda no es palabra y la unión sí lo es.
    Estas pruebas existen para que nadie "arregle" la guarda más adelante.
    """

    def test_no_junta_con_sumo_cuidado(self):
        """«con sumo cuidado» es español correcto; «consumo cuidado» no existe."""
        freq = Counter({'consumo': 2130, 'con': 9000, 'sumo': 3, 'cuidado': 400})
        salida = {'RPM-1999-01-01:1:1': 'debe ser monitoreada con sumo cuidado'}
        self.assertEqual(correr(salida, freq), 0)

    def test_no_junta_de_terminada(self):
        """«Después de terminada la cosecha»: «de terminada» son dos palabras."""
        freq = Counter({'determinada': 28, 'de': 9000, 'terminada': 12,
                        'la': 9000, 'cosecha': 90, 'Después': 800})
        salida = {'RPM-1999-01-01:1:1': 'Después de terminada la cosecha, había'}
        self.assertEqual(correr(salida, freq), 0)

    def test_no_junta_esta_a_prueba(self):
        """«sometida a prueba»: «aprueba» es otra palabra con otro significado."""
        freq = Counter({'aprueba': 123, 'a': 37540, 'prueba': 200,
                        'sometida': 30, 'será': 2000})
        salida = {'RPM-1999-01-01:1:1': 'será sometida a prueba en las semanas'}
        self.assertEqual(correr(salida, freq), 0)

    def test_el_punto_ciego_existe_y_se_corrige_a_mano(self):
        """Documenta el caso que la guarda sí pierde, para que quede registrado.

        No es un fallo que haya que esconder: la política es curar fila por fila,
        así que «presenta ción» se corrigió a mano en la sesión 2008-10-09.
        """
        freq = Counter({'presentación': 1241, 'presenta': 513, 'ción': 2,
                        'resumir': 60, 'la': 9000, 'apropiado': 90})
        salida = {'RPM-1999-01-01:1:1': 'apropiado resumir la presenta ción y que'}
        self.assertEqual(correr(salida, freq), 0)


if __name__ == '__main__':
    unittest.main()
