#!/usr/bin/env python3
"""Regresión de la curaduría OCR: fija las basales medidas para que no retrocedan.

Antes de este módulo sólo 3 de 69 tests mencionaban una forma dañada concreta, y
ninguno fijaba los resultados de las pasadas transversales. El peligro no era
teórico: en la ronda 192 traté ``IPCX`` como un ``IPCX1`` truncado y estuve a
punto de destruir 180 apariciones legítimas. Estos tests existen para que un
cambio así falle en vez de publicarse.

Todo se mide **re-ejecutando** ``correcciones_ocr_v1.validar()`` sobre la base
virgen, no leyendo el release del disco: así el test no depende de que alguien
se haya acordado de reconstruir.

Convención de los umbrales:

* Los **ceros son exactos**. Una forma dañada llevada a 0 nunca debe reaparecer.
* Los conteos que crecen al corregir usan ``>=``: pueden subir cuando se aplique
  una pasada nueva, no bajar.
* ``COMILLAS_RECTAS_MAX`` es el residuo de un defecto aún sin regla: sólo puede
  bajar.
"""
from __future__ import annotations

import sys
import unittest
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'scripts'))

import correcciones_ocr_v1 as core  # noqa: E402
from diagnosticar_finales import read_rows  # noqa: E402

# Formas dañadas llevadas a cero por las pasadas §9 a §14. Cada una con la
# pasada que la resolvió, para que el mensaje de fallo diga dónde mirar.
FORMAS_EN_CERO = {
    # §14 — familia de siglas con I leída como l
    'IPCXI': '§14 (siglas I->l)',
    'dellPC': '§14 (siglas I->l)',
    'ellPoM': '§14 (siglas I->l)',
    'ÍPCX1': '§14 (siglas I->l)',
    'dellPoM': '§14 (siglas I->l)',
    'IPX1': '§14 (siglas I->l)',
    'IPCX 1': '§14 (siglas I->l)',
    'ellPP': '§14 (siglas I->l)',
    'ellPC': '§14 (siglas I->l)',
    'ellPCX1': '§14 (siglas I->l)',
    'IPX': '§14 (siglas I->l)',
    'iPCX': '§14 (siglas I->l)',
    'deIIPCX': '§14 (siglas I->l)',
    '■': '§14 (21 residuos SIMBOLO_SUELTO)',
    # §13
    'X!': '§13 (X! -> Xl)',
    'subpri me': '§13 (palabra partida)',
    'llegarla': '§13 (llegarla -> llegaría)',
    # §12
    'fiy to quality': '§10/§12 (fiy -> fly)',
    'fIy to quality': '§10/§12 (fIy -> fly)',
    # §11 y anteriores
    'IRC': '§1 (IRC -> IPC)',
    'nesgo': '§1 (nesgo -> riesgo)',
    'yeso': '§1 (caer yeso -> caer y eso)',
    'Consesus': 'r190 (Consesus -> Consensus)',
    'perecióles': 'r185 (perecióles -> perecibles)',
}

# Sólo puede bajar: son comillas rectas que quedaron sin par completo y sin
# dirección deducible (§6 y §9 bis resolvieron las demás).
COMILLAS_RECTAS_MAX = 5

# Crecen al corregir; nunca deben bajar.
MIN_CORREGIDAS = 921
MIN_MARCADAS = 135
MIN_OPERACIONES = 1334
MIN_IPCX = 656       # IPCX legítimo preservado + el restaurado por §14
MIN_IPCX1 = 480


class TestRegresionCuraduriaOCR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ok, cls.problemas, cls.corregidas, cls.marcas = core.validar(base=core.BASE)
        cls.base = {r['ID_Intervencion']: r for r in read_rows(core.BASE)}
        # texto efectivo del corpus: la corrección donde la hay, la base si no
        cls.salida = {}
        for rid, fila in cls.base.items():
            cls.salida[rid] = cls.corregidas.get(rid, fila['Texto'] or '')
        cls.reg = core.cargar()

    def test_la_validacion_pasa(self):
        """El contrato completo del validador, incluido el control del Despues."""
        self.assertTrue(self.ok, '\n'.join(self.problemas[:20]))

    def test_el_control_del_despues_detecta_una_palabra_inventada(self):
        """Prueba negativa: sin ella el test anterior pasaría vacíamente."""
        import copy
        mal = copy.deepcopy(self.reg)
        entrada = mal['Correcciones'][0]
        entrada['Operaciones'][0]['Despues'] += ' zarrapastroso'
        ok, problemas, _, _ = core.validar(reg=mal, base=core.BASE)
        self.assertFalse(ok, 'el validador dejó pasar un reemplazo con una palabra inventada')
        self.assertTrue(any('zarrapastroso' in p for p in problemas))

    def test_las_formas_danadas_siguen_en_cero(self):
        """Ninguna forma ya resuelta puede reaparecer en la salida."""
        reaparecidas = {}
        for forma, origen in FORMAS_EN_CERO.items():
            n = sum(t.count(forma) for t in self.salida.values())
            if n:
                reaparecidas[forma] = (n, origen)
        self.assertEqual(
            {}, reaparecidas,
            'formas dañadas que volvieron a aparecer en la salida '
            '(forma -> (apariciones, pasada que la resolvió)):')

    def test_las_formas_legitimas_no_se_destruyeron(self):
        """El caso que casi ocurre en la ronda 192.

        ``IPCX`` no es un ``IPCX1`` truncado: es una segunda medida de inflación
        subyacente y aparece 180 veces suelto en contextos reales. Si una pasada
        futura lo trata como defecto, este test falla.
        """
        n_ipcx = sum(t.count('IPCX') for t in self.salida.values())
        n_ipcx1 = sum(t.count('IPCX1') for t in self.salida.values())
        self.assertGreaterEqual(
            n_ipcx, MIN_IPCX,
            f'IPCX bajó a {n_ipcx} (< {MIN_IPCX}): una pasada se está comiendo la '
            f'sigla legítima, no sólo la dañada')
        self.assertGreaterEqual(n_ipcx1, MIN_IPCX1, f'IPCX1 bajó a {n_ipcx1}')

    def test_las_comillas_rectas_no_aumentan(self):
        n = sum(t.count('"') for t in self.salida.values())
        self.assertLessEqual(
            n, COMILLAS_RECTAS_MAX,
            f'comillas rectas subieron a {n} (> {COMILLAS_RECTAS_MAX})')

    def test_ninguna_operacion_reescribe_la_fila_completa(self):
        """Ninguna operación puede sustituir el texto entero por otra cosa.

        Se admite una única excepción, la deduplicación: si la fila es la misma
        oración dos veces (``RPM-2015-08-13:6926:2``, 341 = 170×2+1 caracteres),
        reemplazarla por la oración una sola vez es ``PALABRA_DUPLICADA`` y es
        correcto. Lo que se prohíbe es la reescritura: ``Despues`` tiene que ser
        una reducción de ``Antes``, no un texto distinto.
        """
        reescrituras = []
        for entrada in self.reg['Correcciones']:
            rid = entrada['ID_Intervencion']
            texto = self.base[rid]['Texto'] or ''
            for op in entrada['Operaciones']:
                if op['Antes'] != texto:
                    continue
                if op['Despues'] in op['Antes'] and len(op['Despues']) < len(op['Antes']):
                    continue
                reescrituras.append(f'{rid}: «{op["Despues"][:60]}»')
        self.assertEqual([], reescrituras,
                         'operaciones que reescriben la fila completa:')

    def test_el_texto_del_release_es_byte_a_byte_el_de_la_base(self):
        """La prueba que importa: ``Texto`` sale intacto del release.

        ``construir()`` añade ``Texto_Corregido`` y ``Cotejar_PDF`` como columnas
        nuevas; nunca escribe sobre ``Texto``. Se compara contra la base virgen
        fila por fila.
        """
        destino = RAIZ / 'data' / 'releases' / 'correccion_ocr_v1' / 'consolidado_texto_corregido.xlsx'
        if not destino.exists():
            self.skipTest(f'release no construido: {destino}')
        alteradas = []
        for fila in read_rows(destino):
            rid = fila['ID_Intervencion']
            if rid in self.base and fila['Texto'] != self.base[rid]['Texto']:
                alteradas.append(rid)
        self.assertEqual([], alteradas[:20],
                         f'{len(alteradas)} filas con Texto alterado en el release')

    def test_los_totales_no_retroceden(self):
        self.assertGreaterEqual(len(self.corregidas), MIN_CORREGIDAS)
        self.assertGreaterEqual(len(self.marcas), MIN_MARCADAS)
        n_ops = sum(len(e['Operaciones']) for e in self.reg['Correcciones'])
        self.assertGreaterEqual(n_ops, MIN_OPERACIONES)

    def test_toda_operacion_lleva_contexto_y_justificacion(self):
        """Ninguna corrección puede quedar sin trazabilidad."""
        vacias = []
        for entrada in self.reg['Correcciones']:
            rid = entrada['ID_Intervencion']
            for n, op in enumerate(entrada['Operaciones'], 1):
                for campo in ('Contexto', 'Justificacion'):
                    if not (op.get(campo) or '').strip():
                        vacias.append(f'{rid} op{n}: falta {campo}')
        self.assertEqual([], vacias[:20])

    def test_no_quedan_palabras_partidas(self):
        """La pasada transversal de §15: 317 pares de palabra partida -> 0.

        Contado por posiciones de token, no con un regex de pares: ``re.finditer``
        no solapa y en «un crecim iento» consume ``un``+``crecim``, dejando la
        pareja real sin evaluar. Ese bug hizo que el detector reportara «0
        candidatos» cuando todavía quedaban 3 ``crecim iento`` en la salida.

        Y no se cuentan substrings: ``so n`` cabe dentro de ``perso na`` y
        ``ta n`` dentro de ``es ta n``, así que ``str.count`` infla.
        """
        import re
        tok = re.compile(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+')
        freq = Counter()
        for t in self.salida.values():
            freq.update(tok.findall(t))
        restantes = []
        for rid in sorted(self.salida):
            t = self.salida[rid]
            ks = list(tok.finditer(t))
            for k in range(len(ks) - 1):
                a, b = ks[k], ks[k + 1]
                if t[a.end():b.start()] != ' ':
                    continue
                junta = a.group() + b.group()
                if junta not in freq or freq[junta] < 20:
                    continue
                if freq.get(a.group(), 0) >= 50 or freq.get(b.group(), 0) >= 50:
                    continue
                restantes.append(f'{rid}: «{a.group()} {b.group()}» -> «{junta}»')
        self.assertEqual([], restantes[:20],
                         f'{len(restantes)} palabras partidas siguen en la salida:')

    def test_las_marcas_usan_el_vocabulario_cerrado(self):
        for marcas in self.marcas.values():
            for m in marcas:
                self.assertIn(m, core.MARCAS_VALIDAS | {core.MOTIVO_QUE_MARCA})


if __name__ == '__main__':
    unittest.main()
