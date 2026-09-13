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

import re
import sys
import unittest
import collections
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'scripts'))

import correcciones_ocr_v1 as core  # noqa: E402
from diagnosticar_finales import read_rows  # noqa: E402
from escanear_corpus import TOKEN  # noqa: E402

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

# Sólo puede bajar. Quedan 4, y el comentario anterior («sin par completo y sin
# dirección deducible») era inexacto: dos sí tienen dirección deducible pero les
# falta la otra mitad del par (2417:1 «serrucho".» sin apertura; 2430:1
# «aplicando "mecánicamente» sin cierre), y las otras dos caen en bloques de
# basura (4064:1, 4510:1). Convertir una comilla suelta sin su par no arregla
# nada y podría equivocarse, así que se dejan. La que sí tenía par completo y
# dirección deducible (6967:1 «"dilema del prisionero".») se resolvió en §28.
COMILLAS_RECTAS_MAX = 3

# Crecen al corregir; nunca deben bajar.
MIN_CORREGIDAS = 1734
MIN_OPERACIONES = 2980

# §18 y §20: espacio indebidamente insertado antes de , . ; %. La familia medía
# 551 ocurrencias en la base y bajó a 4. Una es una palabra letra a letra (§11,
# otra familia), otra cae en un tramo de basura que necesita cotejo, y dos no se
# pueden resolver sin modificar el Antes de una operación vecina, que es lo que
# la ancla al texto virgen. El techo está aquí para que la familia no vuelva a
# crecer y para que tocar el residuo sea visible.
ESPACIO_ANTES_DE_SIGNO_MAX = 4
RESIDUO_ESPACIO_ANTES_DE_SIGNO = {
    'RPM-2006-04-13:653:1', 'RPM-2009-02-12:2319:1',
    'RPM-2010-12-16:3619:1', 'RPM-2015-08-13:6952:1',
}


# Las marcas abiertas SÍ pueden bajar, y está bien que bajen: cotejar una fila
# contra el PDF original y comprobar que el corpus era fiel la mueve a
# NO_REQUIERE_COTEJO. Eso es cerrar trabajo, no perderlo. Lo que nunca puede
# bajar es el total de casos adjudicados (abiertos + cerrados) ni el número de
# cierres ya documentados; si no, borrar revisiones del registro se vería como
# una mejora y el piso anterior (MIN_MARCADAS) premiaba dejar preguntas abiertas.
MIN_CASOS_ADJUDICADOS = 208   # 174 abiertas + 34 cierres al cierre de la sesion 2009-07-09
MIN_CIERRES_COTEJO = 34

# §19: punto pegado a letra. De las 45 ocurrencias, 36 son abreviatura legítima
# (EE.UU., S.E., S.A., U.F., v.gr., 2005.IV) y 4 son basura que quedó marcada.
# Las 5 que eran defecto real se corrigieron. Lo que queda tiene que seguir
# siendo una de esas dos cosas: si aparece un punto pegado nuevo, o es una
# abreviatura que hay que añadir a la lista, o es un defecto sin marcar.
PUNTO_PEGADO_MAX = 40
PUNTO_PEGADO_ABREV = {'EE.', ' S.', ' U.', '(v.', ' v.', '05.'}
PUNTO_PEGADO_MARCADAS = {
    'RPM-2008-04-10:1747:1', 'RPM-2008-06-10:1858:1',
    'RPM-2011-03-17:3815:1', 'RPM-2014-06-12:6274:1',
}

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
        # índices de frecuencia del corpus corregido: los usan las pruebas de
        # familias de palabras partidas
        cls.freq = Counter()
        for t in cls.salida.values():
            cls.freq.update(TOKEN.findall(t))

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
        destino = RAIZ / 'data' / 'releases' / 'correccion_ocr_v2' / 'consolidado_texto_corregido.xlsx'
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

    def test_el_espacio_antes_de_signo_se_quito(self):
        """§18: 546 ocurrencias en la base → 19 en la salida.

        El residuo no es olvido: esas 19 caen dentro de la ventana de una
        operación ya registrada, y resolverlas exige extender esa operación en
        vez de apilarle otra encima (§15). El conjunto está fijado para que
        resolver una obligue a bajar el techo, y para que aparecer una nueva se
        vea enseguida.
        """
        import aplicar_espacios_puntuacion as esp
        vivos = {rid for rid, t in self.salida.items() if esp.ocurrencias(t)}
        n = sum(len(esp.ocurrencias(t)) for t in self.salida.values())
        self.assertLessEqual(n, ESPACIO_ANTES_DE_SIGNO_MAX,
                             f'la familia volvió a crecer: {n} ocurrencias')
        self.assertEqual(vivos, RESIDUO_ESPACIO_ANTES_DE_SIGNO,
                         'cambió el conjunto de filas con residuo')

    def test_las_operaciones_de_espacio_solo_quitan_espacios(self):
        """Una operación de este tipo no puede tocar ninguna letra ni ninguna
        cifra. Si lo hace, está borrando texto en vez de quitar un blanco."""
        import re
        malas = []
        for e in self.reg['Correcciones']:
            for op in e['Operaciones']:
                if op['Tipo'] != 'ESPACIO_INDEBIDO':
                    continue
                if re.sub(r'\s+', '', op['Antes']) != re.sub(r'\s+', '', op['Despues']):
                    malas.append((e['ID_Intervencion'], op['Antes'][:40]))
        self.assertEqual(malas, [], f'operaciones que alteran texto: {malas[:3]}')

    def test_la_barra_invertida_con_barra_desaparecio_salvo_la_marcada(self):
        """§22: la OCR escribe la «M» como «í\\/l», «l\\/l», «i\\/l», «Í\\/1».

        Quince ocurrencias. Catorce se corrigieron porque la forma resultante es
        la del propio corpus y aparece miles de veces; la que queda es
        «lí\\/IACEC», donde «IACEC» aparece una sola vez en todo el corpus (ésta)
        y las candidatas son IPCX1 o IPCSAE. Ambigua, marcada, no adivinada.
        """
        bs = chr(92)
        vivos = [i for i, t in self.salida.items() if (bs + '/') in t]
        self.assertEqual(vivos, ['RPM-2009-03-12:2400:1'],
                         f'la secuencia reapareció o se corrigió la ambigua: {vivos}')
        self.assertIn('RPM-2009-03-12:2400:1', self.marcas,
                      'la única fila que conserva la secuencia debe estar marcada')

    def test_la_barra_por_letra_desaparecio_sin_tocar_los_usos_legitimos(self):
        """§21: la OCR escribe «v», «l» e «I» como «/».

        El riesgo no era corregirlas sino arrasar con la barra legítima, que en
        este corpus es frecuente: ``y/o``, ``peso/dólar``, ``trimestre/trimestre``,
        ``t/t``, ``a/a``. El test fija las dos puntas: cero formas dañadas y los
        usos legítimos intactos respecto de la base.
        """
        danadas = ['obsen/ado', 'obsen/ada', 'obsen/ando', 'obsen/an', 'obsen/a',
                   'obsen/ó', 'Resen/a', 'resen/as', 'cun/a', 'inten/ención',
                   'sw/aps', 'Financia/', 'se/ection', 'Defau/t', '/PoM', '/poM']
        vivos = [k for k in danadas if any(k in t for t in self.salida.values())]
        self.assertEqual(vivos, [], f'formas con barra por letra sin corregir: {vivos}')

        # «y/o» baja de 39 a 38 y está bien: la número 39 estaba dentro de
        # «7ay/or», que es «Taylor» dañado (regla de Taylor) y se corrigió antes
        # de este pase. No es un uso legítimo perdido, es basura que se fue.
        caidas_permitidas = {'y/o': 1}
        for legitimo in ('y/o', 'peso/dólar', 'trimestre/trimestre', 't/t', 'a/a',
                         'público/privado', 'WTI/Brent'):
            antes = sum((self.base.get(i) or {}).get('Texto', '').count(legitimo)
                        for i in self.salida)
            despues = sum(t.count(legitimo) for t in self.salida.values())
            self.assertEqual(antes - despues, caidas_permitidas.get(legitimo, 0),
                             f'«{legitimo}» cambió: {antes} -> {despues}')

    def test_el_punto_pegado_a_letra_solo_queda_en_abreviaturas_y_marcas(self):
        """§19: 45 ocurrencias en la base, 40 en la salida.

        Las 40 son 36 abreviaturas legítimas más 4 filas de basura marcada. Las 5
        que eran defecto real se corrigieron, y una de ellas (`6282:1`) no era
        falta de espacio sino punto espurio: la oración seguía, así que reponer
        el espacio habría inventado un punto y aparte.
        """
        import re
        raras = []
        n = 0
        for rid, t in self.salida.items():
            for m in re.finditer(r'\.[A-Za-zÁÉÍÓÚÑáéíóúñ]', t):
                n += 1
                if t[max(0, m.start() - 2):m.start() + 1] in PUNTO_PEGADO_ABREV:
                    continue
                if rid in PUNTO_PEGADO_MARCADAS and rid in self.marcas:
                    continue
                raras.append((rid, t[max(0, m.start() - 26):m.end() + 14]))
        self.assertLessEqual(n, PUNTO_PEGADO_MAX, f'la familia creció: {n}')
        self.assertEqual(raras, [], f'puntos pegados sin justificar: {raras[:3]}')



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

    def test_el_apostrofo_por_espacio_desaparecio_salvo_en_nombres_propios(self):
        """§58: la OCR pone un apóstrofo donde iba un espacio, o parte una palabra.

        Cuatro casos corregidos, todos sin lectura alternativa: «elementos'tácticos»,
        «en'el caso», «el'f comportamiento» y el encabezado fijo «BANCO CENT'RAL DE
        CHILE». Lo que queda es el apóstrofo legítimo de los nombres propios
        extranjeros, y se enumera forma por forma en lugar de fiarse de una cuenta:
        Moody's, Standard & Poor's, Dell'Oro y People's Bank of China, en sus
        variantes con apóstrofo recto, tipográfico y acento agudo.

        La única excepción es «L1oyd's»: el daño es evidente («1» por «l»), pero la
        forma canónica no está atestiguada en el corpus («L1oyd» aparece 1 vez y
        «Lloyd» 0), así que la regla del §34 no la cubre y la guarda de vocabulario
        de correcciones_ocr_v1.py rechaza introducir una palabra ajena al corpus y a
        TERMINOS_FORANEOS. Se dejó el texto intacto y se marcó para cotejo.
        """
        letra = 'A-Za-z\u00c1\u00c9\u00cd\u00d3\u00da\u00d1\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1'
        pat = re.compile(f'[{letra}]+[\'\u00b4`\u2019][{letra}]+')
        legitimos = {"poor\u2019s", 'poor\'s', "moody\u2019s", "moody's", "moody\u00b4s",
                     "dell\u2019oro", "people\u2019s", "oyd's"}
        vistos = collections.Counter()
        for texto in self.salida.values():
            vistos.update(m.group(0).lower() for m in pat.finditer(texto))
        self.assertEqual(set(vistos) - legitimos, set(),
                         f'apareció un apóstrofo entre letras fuera de los nombres propios '
                         f'conocidos: {sorted(set(vistos) - legitimos)}')
        self.assertEqual(sum(vistos.values()), 66,
                         f'el total de apóstrofos entre letras cambió ({sum(vistos.values())}); '
                         f'si bajó se corrigió un nombre propio legítimo, si subió hay un '
                         f'defecto nuevo sin marcar')
        self.assertIn('RPM-2008-10-09:2106:1', self.marcas,
                      'la fila con el nombre propio dañado sin forma canónica debe estar marcada')
        self.assertEqual([i for i, t in self.salida.items()
                          if "CENT'RAL" in t or "elementos't" in t
                          or "en'el" in t or "el'f" in t], [],
                         'alguno de los cuatro defectos del §58 reapareció')

    def test_claudia_por_claudio_solo_queda_con_tratamiento_femenino(self):
        """§59: la OCR escribe «Claudia» donde va «Claudio», y el género lo decide.

        Veintinueve casos: 27 «señor/don Claudia Soto» contra 1.275 «Claudio Soto», y
        2 «señor/don Claudia Raddatz» contra 75 «Claudio Raddatz». El discriminador no
        es la frecuencia sino el tratamiento que la propia fila usa: «señor» y «don» son
        masculinos. Las tres «Claudia» que sobreviven van con «doña» y son mujeres
        distintas —Claudia Varela Lértora y Claudia Sotz Pantoja—, y ni «Claudio Varela»
        ni «Claudio Sotz» aparecen nunca en el corpus, así que ahí no hay forma canónica
        que oponer.

        Una de las 29 no se corrigió con el lote sino partiendo en tres una operación
        previa (2010-03-18:2990:1): abarcaba los dos espacios y el nombre a la vez, y
        cambiar una letra dentro de un ESPACIO_INDEBIDO rompe la prueba que exige que
        esas operaciones sólo quiten espacios.
        """
        n = lambda pat: sum(len(re.findall(pat, t)) for t in self.salida.values())
        # Se cuenta TODA la familia Claudi*, no sólo «Claudia»: la variante
        # «Claudias Soto» (2010-10-14:3454:1) convivía en la misma fila con un
        # «Claudia Soto» y el primer hallazgo la ocultó. «Claudios Soto»
        # (2011-10-13:4364:2) ya estaba corregido por una sesión anterior.
        self.assertEqual(n(r'Claudi(?!o\b)\w*'), 3,
                         'quedó una forma dañada de la familia o se corrigió una legítima')
        self.assertEqual(sorted(i for i, t in self.salida.items() if 'Claudia' in t),
                         ['RPM-2006-04-13:626:1', 'RPM-2006-05-11:655:1', 'RPM-2012-02-14:4573:1'],
                         'las tres «Claudia» restantes deben ser las de «doña»')
        self.assertEqual(n(r'(?:señor|don)\s+Claudi(?!o\b)\w*'), 0,
                         'queda un nombre de pila dañado con tratamiento masculino')
        self.assertGreaterEqual(n(r'\bClaudio Soto\b'), 1275,
                                '«Claudio Soto» bajó: se está revirtiendo una corrección')
        self.assertGreaterEqual(n(r'\bClaudio Raddatz\b'), 75)

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
        #
        # 'hacía' bajó de 32 a 17 el 2026-09-13 y NO es un ensanche para que pase
        # un cambio: las 32 apariciones se enumeraron una por una. 17 son el verbo
        # («hacía presente», «hacía referencia», «hacía mención», «hacía
        # necesario», «lo hacía moderadamente», «el mercado hacía del actuar»…) y
        # 15 son la preposición «hacia» con la tilde mal puesta, siempre rigiendo
        # un complemento de dirección («hacía delante», «hacía adelante», «hacía la
        # baja», «hacía América Latina», «hacía las economías emergentes», «hacía el
        # tercer trimestre»), donde el verbo no tiene sujeto ni complemento
        # posible. Se corrigieron esas 15 (§40) y el suelo quedó en las 17
        # legítimas. La guardia sigue haciendo su trabajo: si una pasada futura se
        # come alguno de los 17 verbos, esto vuelve a fallar.
        piso = {'éstos': 137, 'cuánto': 124, 'terminó': 20, 'período': 661,
                'dónde': 41, 'cambió': 21, 'hacía': 17, 'inició': 23,
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

    def test_no_quedan_partidas_con_segunda_mitad_de_una_letra(self):
        """La familia nueva: «clim a», «profundizarl o», «Análisi s».

        ``detector_partida`` no puede verla porque su guarda
        ``freq[segunda mitad] >= 50`` bloquea las letras, y esa guarda no se puede
        abrir (``TestLaGuardaNoSePuedeAbrir``). La ve ``detector_partida_letra``,
        que discrimina por la primera mitad: si es marginal en el corpus no es una
        palabra, y si al pegarle la letra aparece una que sí lo es, el espacio
        sobra. Medido al nacer: 40 candidatos en las 9.723 filas, 40 verdaderos.

        Queda una sola excepción y está documentada: ``RPM-2005-03-10:147:1``
        («m e d id o»), donde el par es la cola de una carrera letra por letra y lo
        que hay que corregir es la carrera entera, no el par.
        """
        restantes = []
        for rid in sorted(self.salida):
            t = self.salida[rid]
            ks = list(TOKEN.finditer(t))
            for k in range(len(ks) - 1):
                a, b = ks[k], ks[k + 1]
                if len(b.group()) != 1 or len(a.group()) < 2:
                    continue
                if t[a.end():b.start()] != ' ':
                    continue
                junta = a.group() + b.group()
                if self.freq.get(junta, 0) < 1:
                    continue
                fa = self.freq.get(a.group(), 0)
                if fa > 1 and fa * 20 > self.freq[junta]:
                    continue
                restantes.append(f'{rid}: «{a.group()} {b.group()}» -> «{junta}»')
        self.assertEqual(['RPM-2005-03-10:147:1: «id o» -> «ido»'], restantes,
                         f'la familia cambi\u00f3: {restantes[:10]}')

    def test_las_marcas_usan_el_vocabulario_cerrado(self):
        for marcas in self.marcas.values():
            for m in marcas:
                self.assertIn(m, core.MARCAS_VALIDAS | {core.MOTIVO_QUE_MARCA})


if __name__ == '__main__':
    unittest.main()
