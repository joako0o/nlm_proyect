"""Pruebas de ``detector_partida_letra`` (``scripts/escanear_corpus.py``).

El detector nace de un caso concreto: en la sesión 2007-01-11 la fila
``RPM-2007-01-11:1054:1`` tenía «sea necesario profundizarl o» y ``detector_partida``
daba 0 candidatos en las 50 filas de la sesión. No es un bug que se pueda
arreglar abriendo su guarda: lo que bloquea el caso es ``freq[segunda mitad] >= 50``
y la segunda mitad es una letra (``a`` aparece 37.528 veces, ``o``, ``e``, ``s``),
frecuente *porque* este defecto la esparce. ``TestLaGuardaNoSePuedeAbrir``
(``test_escanear_corpus_partida.py``) ya midió que relajar por ahí mete
«con sumo cuidado» -> «consumo».

De ahí que esto sea otro detector: discrimina por la **primera** mitad (marginal
en el corpus) y no por la frecuencia de la palabra junta. Medido en §31 sobre las
9.723 filas: 40 candidatos, 40 verdaderos.
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


def correr(salida, freq, min_frec=1):
    """Devuelve el total de candidatos que reporta el detector."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        ec.detector_partida_letra(salida, freq, min_frec, limite=100)
    for linea in buf.getvalue().splitlines():
        if 'total candidatos:' in linea:
            return int(linea.split('total candidatos:')[1].split()[0])
    raise AssertionError('el detector no informó total: %r' % buf.getvalue())


class TestDetectorPartidaLetra(unittest.TestCase):
    def test_ve_lo_que_detector_partida_no_puede_ver(self):
        """«clim a»: la segunda mitad es «a», que tiene 37.528 apariciones."""
        freq = Counter({'clima': 58, 'clim': 1, 'a': 37528, 'de': 9000,
                        'confianza': 300, 'un': 9000})
        salida = {'RPM-1999-01-01:1:1': 'ha propiciado un clim a de confianza'}
        self.assertEqual(correr(salida, freq), 1)
        # y el detector viejo, con la misma entrada, no lo ve
        buf = io.StringIO()
        with redirect_stdout(buf):
            ec.detector_partida(salida, freq, 30, limite=100)
        self.assertIn('total candidatos: 0', buf.getvalue())

    def test_no_exige_que_la_palabra_junta_sea_frecuente(self):
        """«profundizarl o»: el destino aparece 1 vez y aun así es candidato.

        Es el caso que motivó el detector. Con ``min_frec`` alto se pierde, y por
        eso ``main()`` lo llama con 1 y no con los 20-30 de los otros detectores.
        """
        freq = Counter({'profundizarlo': 1, 'profundizarl': 1, 'o': 30000,
                        'sea': 900, 'necesario': 400})
        salida = {'RPM-1999-01-01:1:1': 'sea necesario profundizarl o. En su opinión'}
        self.assertEqual(correr(salida, freq), 1)

    def test_acepta_la_pieza_que_el_ocr_partio_mas_de_una_vez(self):
        """«estim a» aparece 4 veces; ``freq <= 1`` solo no bastaría."""
        freq = Counter({'estima': 1283, 'estim': 4, 'a': 37528, 'Se': 3000,
                        'que': 100000})
        salida = {'RPM-1999-01-01:1:1': 'Se estim a que la cifra llegará mañana'}
        self.assertEqual(correr(salida, freq), 1)

    def test_no_junta_cuando_la_primera_pieza_es_una_palabra_corriente(self):
        """«llegar a esa conclusión» es español: «llegara» no es la lectura."""
        freq = Counter({'llegara': 11, 'llegar': 142, 'a': 37528, 'esa': 2000,
                        'conclusión': 300, 'no': 9000, 'existen': 200})
        salida = {'RPM-1999-01-01:1:1': 'no existen antecedentes para llegar a esa conclusión'}
        self.assertEqual(correr(salida, freq), 0)

    def test_no_toca_los_casos_que_protege_la_guarda_del_otro_detector(self):
        """Los cuatro de ``TestLaGuardaNoSePuedeAbrir`` siguen fuera.

        Ninguno tiene segunda mitad de una letra, que es la condición de entrada
        de este detector: por eso ampliar por acá no reabre aquel problema.
        """
        casos = [
            (Counter({'consumo': 2130, 'con': 9000, 'sumo': 3, 'cuidado': 400}),
             'debe ser monitoreada con sumo cuidado'),
            (Counter({'determinada': 28, 'de': 9000, 'terminada': 12, 'la': 9000,
                      'cosecha': 90, 'Después': 800}),
             'Después de terminada la cosecha, había'),
            (Counter({'aprueba': 123, 'a': 37540, 'prueba': 200, 'sometida': 30,
                      'será': 2000}),
             'será sometida a prueba en las semanas'),
            (Counter({'presentación': 1241, 'presenta': 513, 'ción': 2,
                      'resumir': 60, 'la': 9000, 'apropiado': 90}),
             'apropiado resumir la presenta ción y que'),
        ]
        for freq, texto in casos:
            with self.subTest(texto=texto):
                self.assertEqual(correr({'RPM-1999-01-01:1:1': texto}, freq), 0)

    def test_no_inventa_un_destino_que_no_esta_en_el_corpus(self):
        """Si la forma junta no existe, no hay evidencia: no es candidato."""
        freq = Counter({'Abenomics': 1, 'a': 37528, 'política': 4000, 'de': 9000})
        salida = {'RPM-1999-01-01:1:1': 'las Abenomics a la japonesa de política'}
        self.assertEqual(correr(salida, freq), 0)

    def test_exige_un_unico_espacio_entre_las_dos_piezas(self):
        """Con dos espacios el detector no empareja: es otro tipo de daño."""
        freq = Counter({'clima': 58, 'clim': 1, 'a': 37528, 'de': 9000,
                        'confianza': 300, 'un': 9000})
        salida = {'RPM-1999-01-01:1:1': 'ha propiciado un clim  a de confianza'}
        self.assertEqual(correr(salida, freq), 0)

    def test_no_toma_una_primera_pieza_de_una_sola_letra(self):
        """«a prueba» no es «aprueba»: la pieza corta tiene que ser la segunda."""
        freq = Counter({'aprueba': 123, 'a': 37540, 'prueba': 200, 'será': 2000})
        salida = {'RPM-1999-01-01:1:1': 'será a prueba en las semanas próximas'}
        self.assertEqual(correr(salida, freq), 0)


if __name__ == '__main__':
    unittest.main()
