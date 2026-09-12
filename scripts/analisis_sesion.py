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
REPERTORIO = re.compile(
    r'[^A-Za-z0-9 \n\r\t.,;:!¡?¿\'"()\[\]\-–—/\\%$&*+=<>#°·…«»‘’“”‚„†‡‰ÁÉÍÓÚÜÑáéíóúüñ°ºª§|{}^_`~]')
PUNTO_DOBLE = re.compile(r'\.\.(?!\.)')
ESPACIO_DOBLE = re.compile(r'  +')
COMILLA_RECTA = re.compile(r'["\']')
LETRA_SUELTA_FINAL = re.compile(r'\s([A-Za-zÁÉÍÓÚÜÑáéíóúüñ])\.?$')
SIN_PUNTUACION_FINAL = re.compile(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüüñ0-9\)\]»”]$')


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
    return virgen, salida, actor


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

    virgen, salida, actor = cargar(a.base)
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
        ('paréntesis desbalanceado',
         lambda t: ['('] if t.count('(') != t.count(')') else []),
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
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
