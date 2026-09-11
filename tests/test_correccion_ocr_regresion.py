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
    # §16 — acento espurio: con esa tilde la palabra no existe
    'índica': '§16 (acento espurio)',
    'financíamiento': '§16 (acento espurio)',
    'nomínales': '§16 (acento espurio)',
    'íncertidumbre': '§16 (acento espurio)',
    'índexación': '§16 (acento espurio)',
    'Índexación': '§16 (acento espurio)',
    'Macroeconómíco': '§16 (acento espurio)',
    'vísta': '§16 (acento espurio)',
    'medíante': '§16 (acento espurio)',
    'tambíén': '§16 (acento espurio)',
    'perecíbles': '§16 (acento espurio)',
    'desapalancamíento': '§16 (acento espurio)',

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
MIN_CORREGIDAS = 1140
MIN_OPERACIONES = 1654

# Las marcas abiertas SÍ pueden bajar, y está bien que bajen: cotejar una fila
# contra el PDF original y comprobar que el corpus era fiel la mueve a
# NO_REQUIERE_COTEJO. Eso es cerrar trabajo, no perderlo. Lo que nunca puede
# bajar es el total de casos adjudicados (abiertos + cerrados) ni el número de
# cierres ya documentados; si no, borrar revisiones del registro se vería como
# una mejora y el piso anterior (MIN_MARCADAS) premiaba dejar preguntas abiertas.
MIN_CASOS_ADJUDICADOS = 187   # 153 abiertas + 34 cerradas al cierre del §17
MIN_CIERRES_COTEJO = 34

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
        n_ops = sum(len(e['Operaciones']) for e in self.reg['Correcciones'])
        self.assertGreaterEqual(n_ops, MIN_OPERACIONES)

    def test_los_casos_adjudicados_no_retroceden(self):
        """Cerrar un cotejo baja las marcas abiertas: es el resultado esperado.

        Lo que no puede bajar es el total de casos adjudicados ni los cierres ya
        documentados. Sin este test, eliminar revisiones del registro subiría la
        proporción de filas resueltas y nadie lo notaría.
        """
        rev = self.reg['Revisiones_Sin_Correccion']
        cerradas = [r for r in rev if r['Marca'] == 'NO_REQUIERE_COTEJO']
        abiertas = [r for r in rev if r['Marca'] != 'NO_REQUIERE_COTEJO']
        self.assertGreaterEqual(len(rev), MIN_CASOS_ADJUDICADOS,
                                f'quedan {len(rev)} revisiones (< {MIN_CASOS_ADJUDICADOS}): '
                                'se perdieron casos del registro')
        self.assertGreaterEqual(len(cerradas), MIN_CIERRES_COTEJO,
                                f'{len(cerradas)} cierres (< {MIN_CIERRES_COTEJO})')
        self.assertEqual(len(abiertas) + len(cerradas), len(rev),
                         'toda revisión está abierta o cerrada; no hay tercer estado')
        # Un cierre sin explicación es indistinguible de un borrado. El motivo más
        # corto registrado mide 62 caracteres; 40 deja margen sin ser decorativo.
        cortos = [r['ID_Intervencion'] for r in cerradas if len(r['Motivo'].strip()) < 40]
        self.assertEqual(cortos, [], f'cierres sin justificación real: {cortos}')

    def test_el_cotejo_contra_pdf_cerro_las_marcas_verificadas(self):
        """Las actas de 2005-06-09 y 2005-07-12 están en data/raw/, así que esas
        cuatro filas se pudieron cotejar de verdad: el documento escribe «Luis
        Oscar Herrera» sin tilde y «Óscar» no aparece ninguna vez. El corpus era
        fiel, de modo que la marca se cierra sin tocar el texto.
        """
        for rid in ('RPM-2005-06-09:279:1', 'RPM-2005-06-09:280:6',
                    'RPM-2005-07-12:296:1', 'RPM-2005-07-12:305:6'):
            self.assertNotIn(rid, self.marcas, f'{rid} sigue en Cotejar_PDF tras el cotejo')
        for rid in ('RPM-2005-06-09:279:1', 'RPM-2005-07-12:305:6'):
            self.assertIn('Luis Oscar Herrera', self.salida[rid])
            self.assertNotIn('Luis Óscar Herrera', self.salida[rid],
                             f'{rid}: se le añadió una tilde que el original no tiene')

    def test_los_espacios_con_cifras_del_encabezado_se_repusieron(self):
        """«celebrada el12» sale pegado en la capa de texto del PDF; el mismo
        encabezado en el PDF de 2005-06-09 sale con espacio, lo que prueba que es
        un artefacto y no una variante del acta.
        """
        esperados = {
            'RPM-2005-07-12:296:1': 'celebrada el 12 de julio de 2005',
            'RPM-2005-02-10:58:1': 'Celebrada el 10 de febrero de 2005',
            'RPM-2005-03-10:140:1': 'Celebrada el 10 de marzo de 2005',
            'RPM-2009-03-12:2383:1': 'celebrada el 12 de marzo de 2009',
            'RPM-2010-04-15:3023:1': 'celebrada el 15 de abril de 2010',
            'RPM-2010-11-16:3494:1': 'celebrada el 16 de noviembre de 2010',
            'RPM-2015-02-12:6618:3': 'que sube a 100%',
        }
        for rid, forma in esperados.items():
            self.assertIn(forma, self.salida[rid], f'{rid}: falta {forma!r}')

    def test_no_quedan_porcientos_duplicados(self):
        """«6%%» no es notación posible; se leyeron las 6 ocurrencias del corpus."""
        n = sum(t.count('%%') for t in self.salida.values())
        self.assertEqual(n, 0, f'quedan {n} signos de porcentaje duplicados')

    def test_las_cifras_ambiguas_quedan_marcadas_no_adivinadas(self):
        """Donde el OCR separó cifras y el valor no es recuperable sin el original,
        la fila queda marcada: adivinar «6 4%» como «6,4%» sería editar el discurso.
        """
        for rid in ('RPM-2005-05-12:225:1', 'RPM-2007-02-08:1073:2',
                    'RPM-2007-12-13:1576:2', 'RPM-2008-02-07:1651:1',
                    'RPM-2008-12-11:2237:2', 'RPM-2009-03-12:2402:1',
                    'RPM-2009-04-09:2474:1', 'RPM-2009-05-07:2533:1',
                    'RPM-2009-09-08:2694:1'):
            self.assertIn(rid, self.marcas, f'{rid}: cifra ambigua sin marcar')


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

    def test_los_pares_minimos_legitimos_no_se_tocaron(self):
        """La otra mitad de §16: lo que NO se corrige.

        El escáner de acentos da 1.094 candidatos y el grueso son pares mínimos
        legítimos del español. Corregirlos sería destruir texto válido, y es el
        error más fácil de cometer con un detector de acentos. Estos conteos son
        un suelo: si bajan, una pasada se está comiendo formas correctas.
        """
        # Suelos medidos POR TOKEN en la salida. No sirven los conteos por
        # substring: 'cuánto' da 128 por substring porque incluye 'cuántos', y
        # 'período' da 786 porque incluye 'períodos'. Con esos números el test
        # fallaba sin que se hubiera dañado nada.
        piso = {'éstos': 137, 'cuánto': 124, 'terminó': 20, 'período': 661,
                'dónde': 41, 'cambió': 21, 'hacía': 32, 'inició': 23,
                # §16 grupo B: leídas una por una y declaradas correctas
                'continua': 16, 'publica': 13, 'seria': 7, 'multimodal': 4}
        import re as _re
        for forma, minimo in piso.items():
            # por token, no por substring: «continua» cabe dentro de «continuar»
            n = sum(1 for t in self.salida.values()
                    for m in _re.finditer(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+', t)
                    if m.group() == forma)
            self.assertGreaterEqual(
                n, minimo,
                f'«{forma}» bajó a {n} (< {minimo}): es una forma legítima, '
                f'no un defecto; una pasada la está corrigiendo de más')

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
