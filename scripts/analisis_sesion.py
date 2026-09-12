#!/usr/bin/env python3
"""Auditoría de una sesión completa antes de leerla.

Uso: python scripts/analisis_sesion.py 2008-03-13 [--limite 40]

**Por qué existe.** Leer una reunión entera a ciegas no escala: 106 filas y
133.000 caracteres por sesión. Este script no decide nada y no corrige nada;
produce la lista de candidatos que hay que leer completos, y deja constancia de
lo que la sesión NO tiene, que también es información (varias sesiones se
cerraron sin una sola corrección).

**Qué revisa, en este orden:**

1. Cobertura: filas, caracteres, actores, cuántas filas ya están leídas.
2. Cola multihablante: las filas de la sesión que están en la cola medida del
   lote10 (detector permisivo, ya filtrada de falsos positivos por mismo actor).
3. Los cuatro detectores de ``escanear_corpus`` (acento, partida, partida_letra,
   deletreada) restringidos a la sesión. No son reglas: exigen contraparte
   frecuente en el corpus y aun así se revisan uno por uno.
4. Pre-cernido de nombres: qué asistentes aparecen nombrados en cada fila. Sirve
   para sospechar una segunda voz; por sí solo no decide nada (§23 del criterio:
   «contar nombres no decide nada»).
5. Signos sospechosos: caracteres fuera del repertorio, dobles espacios, punto
   duplicado, comillas rectas, paréntesis desbalanceados, fila que termina en
   letra suelta o sin puntuación.

Vive bajo control de versiones a propósito: las versiones anteriores estaban en
``.cache/`` y un reinicio del espacio de trabajo las borró.
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import correcciones_ocr_v1 as core  # noqa: E402
import escanear_corpus as esc  # noqa: E402
from diagnosticar_finales import read_rows  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
COLA = RAIZ / 'docs/multihablante_lote10_2026-09-12/cola_revision_hablantes.json'
LECTURAS = RAIZ / 'docs/continuidad_lote9_2026-09-09/lecturas.json'

# Repertorio admitido: ASCII imprimible más la tipografía española y los signos
# que el corpus usa de verdad. Cualquier otra cosa es residuo de OCR o de fuente.
#
# Las viñetas y los signos de moneda entraron medidos, no por gusto: «•» aparece
# 141 veces en 31 actos como marcador de lista de las presentaciones, y «€» 63
# veces en 19. Sin ellos el chequeo daba falso positivo en cada sesión que traía
# una lámina. Lo que sí queda fuera y conviene mirar cuando toque su sesión:
# «±» (5 en 2 actos), «►» (2), «─» (2), «®» (2, en 2015-03-19:6691:1), «´» (1) y
# el guion blando \xad (1).
REPERTORIO = re.compile(
    r'[^A-Za-z0-9 \n\r\t.,;:!¡?¿\'"()\[\]\-–—/\\%$&*+=<>#°·…«»‘’“”‚„†‡‰'
    r'ÁÉÍÓÚÜÑáéíóúüñºª§|{}^_`~•€¥£]')
PUNTO_DOBLE = re.compile(r'\.\.(?!\.)')
ESPACIO_DOBLE = re.compile(r'  +')
COMILLA_RECTA = re.compile(r'["\']')
LETRA_SUELTA_FINAL = re.compile(r'\s([A-Za-zÁÉÍÓÚÜÑáéíóúüñ])\.?$')
SIN_PUNTUACION_FINAL = re.compile(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüüñ0-9\)\]»”]$')
# Cierre de enumeración: «a)», «ii)»… No son paréntesis de verdad.
#
# Sólo letras y numerales romanos. Los dígitos entraron al principio y hubo que
# sacarlos: medido en el corpus, « 1)»/« 2)»/« 50)» dan 4 apariciones y las cuatro
# son el cierre de un paréntesis de verdad («(más de 50)», «(1 en 1)»), mientras
# que las enumeraciones de letra y romanas son 48. Con los dígitos dentro, el
# chequeo restaba un cierre legítimo y volvía a dar falso positivo —lo hizo en
# 2008-12-11:2206:1, que tiene 6 y 6 balanceados—.
ENUMERACION = re.compile(r'(?:^|[\s;:])((?:[a-z]|[ivx]+)\))')

# Verbos de habla en forma personal y sujetos con tratamiento. Es la red
# independiente de la cola del lote10 (ver la sección 2b más abajo).
_VERBOS = ('señala', 'indica', 'comenta', 'agrega', 'menciona', 'responde', 'acota',
           'complementa', 'pregunta', 'consulta', 'sostiene', 'plantea', 'destaca',
           'advierte', 'precisa', 'explica', 'recuerda', 'añade', 'expresa',
           'manifiesta', 'puntualiza', 'reitera', 'estima', 'considera')
VERBO_HABLA = re.compile(r'\b(?:' + '|'.join(_VERBOS) + r')(?:n|ron|mos)?\b')
SUJETO = re.compile(
    r'(?:el|la|los|las)?\s*(?:señor|señora|don|doña)\s+'
    r'([A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+(?:\s+[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+){1,3})')

# Las otras cinco firmas del censo del §49. Cada una abre alguno de los cinco
# cortes aplicados, y ninguna estaba cubierta antes de medirlo.
CARGOS = ('Gerente', 'Consejero', 'Presidente', 'Vicepresidente', 'Ministro', 'Ministra',
          'Asesor', 'Secretario', 'Fiscal', 'Economista', 'Jefe', 'Subsecretario')

# Firmas 3 y 7: traspaso de la palabra, y sus variantes.
TRASPASO = re.compile(
    r'(?:ofrece|concede|cede|da|otorga)\s+(?:la\s+)?palabra\s+(?:a|al|para)\b|da\s+paso\s+a\b')
TRASPASO_VAR = re.compile(
    r'(?:cede|otorga|concede|ofrece|da|pasa|entiende)\s+(?:el\s+uso\s+de\s+)?(?:la\s+)?palabra\b'
    r'|da\s+paso\s+a\b|invita\s+(?:a|al)\b'
    r'|solicita\s+(?:a|al)\b[^.;]{0,80}?(?:presente|exponga|informe)\b'
    r'|corresponde\s+(?:la\s+)?(?:palabra|presentaci[oó]n|exposici[oó]n)\s+(?:a|al)\b'
    r'|(?:queda|est[aá])\s+(?:a\s+)?cargo\s+de\b'
    r'|para\s+que\s+(?:inicie|presente|exponga)\s+la\s+(?:exposici[oó]n|presentaci[oó]n)\b', re.I)

# Firma 4: un tercero responde dentro de la fila. Fue la única que produjo un
# corte (padre 1706, §48) y ninguna red anterior la cubría.
RESPONDE = re.compile(
    r'((?:el|la|los|las)\s+)?(?:señor|señora|don|doña)?\s*'
    r'(Presidente|Vicepresidente|Consejero|Ministro|Ministra|Gerente|Asesor|Secretario|Fiscal'
    r'|Economista|Jefe)\b[^.;]{0,60}?'
    r'\b(responde|contesta|replica|aclara|repregunta)\b', re.I)

# Firma 5: sujeto pospuesto — «Menciona la señora Ministra que…». Así abren los
# cortes 1564 y 1995.
POSPUESTO = re.compile(
    r'\b(' + '|'.join(v.capitalize() for v in _VERBOS) + r')\s+(?:el|la|los|las)\s+'
    r'(?:(?:señor|señora|don|doña)\s+)?'
    r'([A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+(?:\s+(?:de|del|la|las|los)\s+|\s+)?'
    r'[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+(?:\s+[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+)?)')

# Firma 6: cargo como sujeto, sin nombre — «El Gerente de División Política
# Financiera manifiesta…». Así abre el corte 2960.
CARGO_SUJETO = re.compile(
    r'\b(?:El|La|el|la)\s+((?:' + '|'.join(CARGOS) + r')'
    r'(?:\s+(?:de|del|General|División|Área)\s+[A-ZÁÉÍÓÚÜÑ][\wáéíóúüñ]*){0,4})\s+'
    r'(?:señor|señora|don|doña\s+)?(?:[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+\s+){0,3}?'
    r'\b(' + '|'.join(_VERBOS) + r')\b')



def cargar(base):
    reg = core.cargar()
    ok, problemas, corregidas, _ = core.validar(reg=reg, base=base)
    if not ok:
        for p in problemas[:10]:
            print('ERROR:', p)
        raise SystemExit(1)
    filas = read_rows(base)
    virgen = {r['ID_Intervencion']: (r['Texto'] or '') for r in filas}
    salida = {rid: corregidas.get(rid, t) for rid, t in virgen.items()}
    actor = {r['ID_Intervencion']: r['Actor_Final'] for r in filas}
    rol = {r['ID_Intervencion']: (r.get('Rol_Final') or '') for r in filas}
    motivos = {r['ID_Intervencion']: (r.get('Motivos_Revision') or '') for r in filas}
    return virgen, salida, actor, rol, motivos


def seccion(numero, titulo):
    print('\n' + '=' * 78)
    print(f'{numero}. {titulo}')
    print('=' * 78)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('fecha', help='YYYY-MM-DD')
    ap.add_argument('--base', type=Path, default=core.BASE)
    ap.add_argument('--limite', type=int, default=40)
    a = ap.parse_args()
    prefijo = f'RPM-{a.fecha}:'

    virgen, salida, actor, rol, motivos = cargar(a.base)
    ids = [rid for rid in virgen if rid.startswith(prefijo)]
    if not ids:
        print(f'No hay filas para {a.fecha}')
        return 1
    sesion = {rid: salida[rid] for rid in ids}
    leidas = set(json.loads(LECTURAS.read_text(encoding='utf-8'))['Casos'])

    seccion(1, 'Cobertura')
    actores = collections.Counter(actor[rid] for rid in ids)
    print(f'filas          : {len(ids)}')
    print(f'caracteres     : {sum(len(t) for t in sesion.values()):,}')
    print(f'ya leídas      : {len([r for r in ids if r in leidas])} de {len(ids)}')
    print(f'actores ({len(actores)}):')
    for nombre, n in actores.most_common():
        print(f'   {n:>4}  {nombre}')

    seccion(2, 'Cola multihablante (lote10, ya filtrada)')
    cola = json.loads(COLA.read_text(encoding='utf-8'))['Casos']
    en_cola = [c for c in cola if c['Fecha'] == a.fecha]
    if not en_cola:
        print('ninguna fila de esta sesión está en la cola de 74')
    for c in en_cola:
        print(f'   padre {c["ID_Padre"]} @{c["Inicio"]} estricto={c["Actor_Estricto"]} '
              f'permisivo={c["Actor_Permisivo"]}')
        print(f'      «{c["Oracion"][:150]}»')

    seccion('2b', 'Segunda voz por verbo de habla (red independiente de la cola)')
    # Por qué existe esta sección. La cola del lote10 se construyó con
    # TurnDetector sobre los 7.219 padres crudos, y los cuatro cortes curados que
    # sí se publicaron (657, 1564, 1995, 2960) NO estaban en ella: vienen de
    # LECTURA_DIRIGIDA_POR_AGENTE. La cola y la lectura encuentran conjuntos
    # disjuntos, así que revisar sólo la cola no es separar multihablantes.
    #
    # Esta red es distinta y corre sobre la BASE construida: busca filas de un
    # solo segmento donde otra persona —no el actor de la fila— es sujeto de un
    # verbo de habla en forma personal. Propone, no decide: en las diez primeras
    # sesiones dio 13 candidatos y los 13 eran falsos (7 ruido de OCR sobre el
    # propio actor, 6 menciones: apoyar una opinión, dar la bienvenida, concordar
    # con, citar a un tercero). Aun así es la red que encuentra lo que la cola no.
    n_seg = collections.Counter(rid.split(':')[0] + ':' + rid.split(':')[1] for rid in ids)
    encontrados = 0
    for rid in ids:
        if n_seg[':'.join(rid.split(':')[:2])] > 1:
            continue                       # el motor ya la partió
        texto = sesion[rid]
        actor_row = actor[rid] or ''
        ap = actor_row.split()[-1] if actor_row.split() else ''
        otros = set()
        for m in SUJETO.finditer(texto):
            nombre = m.group(1)
            apellido = nombre.split()[-1]
            if apellido == ap or apellido in actor_row:
                continue
            if VERBO_HABLA.search(texto[m.end():m.end() + 70]):
                otros.add(nombre)
        if otros:
            encontrados += 1
            print(f'   {rid} | {actor_row} | {len(texto)} ch')
            print(f'      posible segunda voz: {", ".join(sorted(otros))}')
    print(f'\n   {encontrados} filas de un solo segmento con otra persona como sujeto '
          f'de un verbo de habla.\n   Ojo: casi todas son menciones (apoyar, dar la '
          f'bienvenida, concordar, citar) y no cambios de voz;\n   y parte del ruido es '
          f'el propio actor con el nombre dañado por OCR. Se leen una por una.')

    seccion('2c', 'Las otras cinco firmas de cambio de hablante (censo del §49)')
    # El §49 midió las siete firmas que exhiben los cinco cortes aplicados. La 2b
    # de arriba es la firma 2; aquí van la 3 (traspaso con texto largo después),
    # la 4 (un tercero responde), la 5 (sujeto pospuesto), la 6 (cargo como sujeto
    # sin nombre) y la 7 (variantes de traspaso).
    #
    # En el corpus entero las cinco dieron 0 cortes pendientes. Se dejaron aquí de
    # todos modos porque el cero de un corpus no garantiza el cero de la próxima
    # acta, y porque la firma 4 fue la única que produjo un corte y ninguna red
    # anterior la cubría.
    def distancia(x, y):
        if abs(len(x) - len(y)) > 2:
            return 9
        prev = list(range(len(y) + 1))
        for i, cx in enumerate(x, 1):
            cur = [i]
            for j, cy in enumerate(y, 1):
                cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (cx != cy)))
            prev = cur
        return prev[-1]

    def es_el_mismo(nombre, actor_row, rol_row):
        """Descarta al propio actor escrito distinto.

        Tres formas de escribirlo mal se midieron: el apellido dañado por OCR
        («José De Gregario», «Manuel Mari^án»), el cargo en vez del nombre, y el
        cargo con abreviatura —«Ministro de Hacienda (S)» es la Ministra
        Subrogante, y sin eso las firmas 5 y 6 daban un falso positivo por sesión.
        """
        partes = [p for p in re.split(r'\s+', actor_row.lower()) if len(p) > 3]
        if any(distancia(w.lower().strip('^'), p) <= 2 for w in nombre.split() for p in partes):
            return True
        primero = nombre.split()[0]
        if primero in CARGOS and rol_row and primero.lower()[:5] in rol_row.lower():
            return True
        return False

    total_2c = 0
    for rid in ids:
        if n_seg[':'.join(rid.split(':')[:2])] > 1:
            continue
        texto = sesion[rid]
        actor_row = actor[rid] or ''
        rol_row = rol[rid] or ''
        avisos = []
        for etiqueta, patron in (('traspaso', TRASPASO), ('traspaso, variante', TRASPASO_VAR)):
            for m in patron.finditer(texto):
                fin = texto.find('.', m.end())
                fin = len(texto) if fin < 0 else fin
                if len(texto) - (fin + 1) >= 400:
                    avisos.append((etiqueta, texto[m.start():fin + 1].strip()[:110]))
        for m in RESPONDE.finditer(texto):
            if not es_el_mismo(m.group(2), actor_row, rol_row) and len(texto) - m.start() >= 150:
                avisos.append(('un tercero responde', f'{m.group(2)} {m.group(3)}'))
        for m in POSPUESTO.finditer(texto):
            if not es_el_mismo(m.group(2), actor_row, rol_row) and len(texto) - m.start() >= 150:
                avisos.append(('sujeto pospuesto', f'{m.group(1)} {m.group(2)}'))
        for m in CARGO_SUJETO.finditer(texto):
            if not es_el_mismo(m.group(1), actor_row, rol_row) and len(texto) - m.start() >= 200:
                avisos.append(('cargo como sujeto', m.group(1)))
        if avisos:
            total_2c += 1
            print(f'   {rid} | {actor_row} | rol: {rol_row or "—"} | {len(texto)} ch')
            for etiqueta, detalle in avisos:
                print(f'      [{etiqueta}] {detalle}')
    print(f'\n   {total_2c} filas con alguna de las cinco firmas. Se leen todas: en el corpus\n'
          '   entero la gran mayoría era el propio actor con el nombre o el cargo escrito\n'
          '   distinto, o una mención. La única que produjo un corte fue «un tercero\n'
          '   responde» (padre 1706, §48).')

    seccion(3, 'Detectores sobre la sesión (candidatos, no reglas)')
    freq, canon = esc.construir_indices(salida)
    # Los detectores imprimen directamente; se les pasa sólo la sesión.
    for nombre, funcion, args in (
            ('acento', esc.detector_acento, (sesion, freq, canon, 20, a.limite)),
            ('partida', esc.detector_partida, (sesion, freq, 20, a.limite)),
            ('partida_letra', esc.detector_partida_letra, (sesion, freq, 1, a.limite)),
            ('deletreada', esc.detector_deletreada, (sesion, freq, 20, a.limite))):
        print(f'\n--- {nombre} ---')
        funcion(*args)

    seccion(4, 'Pre-cernido: asistentes nombrados en cada fila')
    nombres = sorted({n for n in actores if n and n.lower() != 'consejo'}, key=len, reverse=True)
    otros = [n for n in nombres]
    hits = 0
    for rid in ids:
        texto = sesion[rid]
        encontrados = [n for n in otros if n in texto and texto.count(n)]
        if len(encontrados) >= 1:
            hits += 1
            if hits <= a.limite:
                print(f'   {rid}: {", ".join(encontrados[:4])}')
    print(f'\n   {hits} de {len(ids)} filas nombran a algún asistente '
          '(esto no decide nada: §23)')

    seccion(5, 'Signos sospechosos')
    chequeos = (
        ('carácter fuera de repertorio', lambda t: REPERTORIO.findall(t)),
        ('doble espacio', lambda t: ESPACIO_DOBLE.findall(t)),
        ('punto duplicado', lambda t: PUNTO_DOBLE.findall(t)),
        ('comilla recta', lambda t: COMILLA_RECTA.findall(t)),
        # Los cierres sueltos de una enumeración («a) b) c)», «i) ii) iii)») no son
        # paréntesis desbalanceados. Dio falso positivo en 2008-03-13 y otra vez en
        # 2009-02-12, así que se descuentan antes de contar.
        ('paréntesis desbalanceado',
         lambda t: (lambda n: ['('] * n if n > 0 else [])(
             t.count('(') - (t.count(')') - len(ENUMERACION.findall(t))))),
        ('termina en letra suelta', lambda t: LETRA_SUELTA_FINAL.findall(t)),
        ('termina sin puntuación', lambda t: SIN_PUNTUACION_FINAL.findall(t)),
    )
    for etiqueta, funcion in chequeos:
        total = 0
        ejemplos = []
        for rid in ids:
            encontrados = funcion(sesion[rid])
            if encontrados:
                total += len(encontrados)
                if len(ejemplos) < 6:
                    ejemplos.append((rid, encontrados[:3]))
        print(f'\n   {etiqueta}: {total}')
        for rid, e in ejemplos:
            print(f'      {rid} -> {e}')

    # «Termina sin puntuación» no es necesariamente un hallazgo nuevo: el motor ya
    # levanta FINAL_SIN_PUNTUACION y esa alerta sostiene una reserva abierta que no
    # se cierra añadiendo el punto. Se separan los dos casos para no volver a
    # proponer lo mismo cada sesión.
    con_alerta = [r for r in ids
                  if 'FINAL_SIN_PUNTUACION' in motivos[r] and SIN_PUNTUACION_FINAL.search(sesion[r])]
    if con_alerta:
        print(f'\n   de las filas sin puntuación final, {len(con_alerta)} ya llevan '
              f'FINAL_SIN_PUNTUACION (reserva abierta, no se cierra con un punto): '
              f'{", ".join(con_alerta[:5])}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
