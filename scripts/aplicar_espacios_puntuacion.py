#!/usr/bin/env python3
"""Construye el lote que repone el espacio indebidamente insertado antes de ``,``
``.``, ``;`` y ``%``.

    python scripts/aplicar_espacios_puntuacion.py -o lote.json [--aplicar]
                                                  [--fusion 40] [--excluir-fila ID]

Por qué existe una herramienta y no un reemplazo global: ``Antes`` tiene que ser
único dentro del texto virgen de la fila y no puede solaparse con operaciones ya
registradas. Con ~490 ocurrencias repartidas en ~290 filas, muchas caen a pocos
caracteres de distancia, y una ventana de contexto fija las haría chocar. La
herramienta **fusiona** las ocurrencias cercanas en una sola operación y agranda
la ventana hasta que el tramo es único.

Qué no toca, y por qué:

- ``.`` precedido de otro ``.`` o seguido de otro ``.``: es la familia del punto
  duplicado y de los puntos suspensivos, que piden otro tratamiento.
- ``;`` o ``,`` precedidos del mismo signo: idem.
- El espacio se quita, no se reordena nada más: la operación no puede alterar
  ninguna palabra, sólo el blanco anterior al signo.

La evidencia de que esto es defecto y no una característica del original está en
§18: los dos PDFs del repositorio dan **0** ocurrencias del patrón, y las 90
filas del corpus de esas mismas dos sesiones también dan 0.

Sin ``--aplicar`` sólo informa.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import correcciones_ocr_v1 as core  # noqa: E402
from diagnosticar_finales import read_rows  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
AGREGAR = RAIZ / 'scripts' / 'agregar_correcciones_ocr.py'

JUST = ('Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la '
        'cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de '
        'fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas '
        'del corpus de esas mismas sesiones también, así que no es una característica del acta. '
        'La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.')


def ocurrencias(texto: str) -> list[tuple[int, int]]:
    """Devuelve (inicio_del_blanco, fin_del_signo) para cada espacio indebidamente
    colocado antes de ``,`` ``.`` o ``;``."""
    out = []
    # Lookahead y lookbehind, no grupos capturados: con ``(\S)(\s+)([,.;%])`` el
    # signo queda consumido por el match y ``re.finditer`` no lo vuelve a ofrecer
    # como carácter anterior del siguiente. En «2 ,5 % .» eso perdía el tercer
    # espacio. Es la misma lección de §15 sobre finditer, reaparecida aquí.
    for m in re.finditer(r'(?<=\S)\s+(?=[,.;%])', texto):
        ini, fin = m.start(), m.end() + 1        # fin incluye el signo
        prev, punc = texto[m.start() - 1], texto[m.end()]
        # Signo duplicado, y en el caso del punto también los suspensivos: son
        # otra familia y quitar el espacio dejaría «,,» o «..». Se miran los dos
        # lados; la primera versión miraba sólo el anterior y dejaba pasar «,,».
        if prev == punc or texto[fin:fin + 1] == punc:
            continue
        out.append((ini, fin))
    return out


def grupos(oc: list[tuple[int, int]], fusion: int) -> list[list[tuple[int, int]]]:
    g: list[list[tuple[int, int]]] = []
    for o in oc:
        if g and o[0] - g[-1][-1][1] <= fusion:
            g[-1].append(o)
        else:
            g.append([o])
    return g


def quitar_blancos(texto: str, ini: int, fin: int,
                   oc: list[tuple[int, int]]) -> str:
    """Devuelve ``texto[ini:fin]`` sin el blanco de cada ocurrencia del grupo."""
    trozo = texto[ini:fin]
    for oi, of in oc:
        signo = re.search(r'\s+', texto[oi:of]).group(0)
        trozo = trozo.replace(texto[oi:of], texto[oi:of].replace(signo, '', 1), 1)
    return trozo


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--salida', default='.cache/lote_espacios_puntuacion.json')
    ap.add_argument('--fusion', type=int, default=40,
                    help='ocurrencias a esta distancia o menos se fusionan en una operación')
    ap.add_argument('--excluir-fila', action='append', default=[])
    ap.add_argument('--aplicar', action='store_true')
    a = ap.parse_args()

    base = {r['ID_Intervencion']: r for r in read_rows(core.BASE)}
    reg = json.loads((RAIZ / 'data' / 'curation' / 'correcciones_ocr_v1.json')
                     .read_text(encoding='utf-8'))
    ya = {e['ID_Intervencion']: e['Operaciones'] for e in reg['Correcciones']}

    lote = {'Correcciones': [], 'Revisiones_Sin_Correccion': []}
    n_ops = n_filas = n_saltadas = 0

    for rid, fila in base.items():
        if rid in a.excluir_fila:
            continue
        t = fila['Texto'] or ''
        oc = ocurrencias(t)
        if not oc:
            continue
        # no pisar tramos ya cubiertos por operaciones registradas
        ocupados = []
        for op in ya.get(rid, []):
            i = t.find(op['Antes'])
            if i >= 0:
                ocupados.append((i, i + len(op['Antes'])))
        ops = []
        for g in grupos(oc, a.fusion):
            ini, fin = g[0][0], g[-1][1]
            # La ventana mínima que sea única en el texto virgen. El control de
            # solape va sobre la ventana que se va a escribir, no sobre el tramo
            # núcleo: la primera versión comparaba (ini, fin) y dejaba pasar
            # ventanas ensanchadas que sí chocaban con operaciones registradas.
            # Los márgenes crecen, así que en cuanto uno solapa, los mayores
            # también: se salta el grupo entero.
            antes = despues = None
            for margen in (0, 2, 4, 7, 10, 20, 35, 60, 110, 200):
                x, y = max(0, ini - margen), min(len(t), fin + margen)
                if any(x < b and a_ < y for a_, b in ocupados):
                    break
                cand = t[x:y]
                if cand and t.count(cand) == 1:
                    antes = cand
                    despues = t[x:ini] + quitar_blancos(t, ini, fin, g) + t[fin:y]
                    break
            if antes is None or antes == despues:
                n_saltadas += len(g)
                continue
            ctx_i = max(0, ini - 70)
            ops.append({'Tipo': 'ESPACIO_INDEBIDO', 'Antes': antes, 'Despues': despues,
                        'Contexto': t[ctx_i:min(len(t), fin + 70)], 'Justificacion': JUST})
        if ops:
            lote['Correcciones'].append({'ID_Intervencion': rid, 'Operaciones': ops})
            n_ops += len(ops)
            n_filas += 1

    Path(a.salida).write_text(json.dumps(lote, ensure_ascii=False, indent=2) + '\n',
                              encoding='utf-8')
    print('ocurrencias detectadas y resueltas: %d en %d filas' % (n_ops, n_filas))
    print('saltadas (solape con operación previa o tramo no único): %d' % n_saltadas)
    print('lote escrito en', a.salida)
    if not a.aplicar:
        return 0
    r = subprocess.run([sys.executable, str(AGREGAR), a.salida, '--parche'])
    return r.returncode


if __name__ == '__main__':
    raise SystemExit(main())
