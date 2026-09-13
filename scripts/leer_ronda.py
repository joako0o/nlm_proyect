#!/usr/bin/env python3
"""Lector seguro para las rondas del plan lote 9.

La salida de bash se trunca por el medio conservando cabeza y cola, así que
una ronda larga puede registrarse sin haberse leído su primera fila. Este
lector existe para controlar el tamaño de lo emitido.

Uso:
    leer_seguro.py N          lista las filas de la ronda N con su largo
    leer_seguro.py N k        imprime una fila completa
    leer_seguro.py N a:b      imprime las filas a..b INCLUSIVE, completas,
                              y el total de caracteres emitidos

Nunca trunca: si el rango pedido es demasiado grande, lo dice en vez de
imprimir a medias.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, 'scripts')
from diagnosticar_finales import read_rows  # noqa: E402

PLAN = Path('docs/continuidad_lote9_2026-09-09/plan_rondas.json')
BASE = (Path('data/releases/continuidad_procedimental_v7')
        / 'consolidado_base_referencia_final.xlsx')
TECHO = 20000
AVISO = 18000


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    ronda = int(sys.argv[1])
    doc = json.loads(PLAN.read_text(encoding='utf-8'))
    item = next((r for r in doc['Rondas'] if r['Ronda'] == ronda), None)
    if item is None:
        print(f'no existe la ronda {ronda}')
        return 1
    ids = item['IDs']
    filas = {r['ID_Intervencion']: r for r in read_rows(BASE)}
    sel = [filas[i] for i in ids]

    if len(sys.argv) == 2:
        print(f"RONDA {ronda} | sesion {item['Sesion']} | {len(sel)} filas")
        for k, r in enumerate(sel):
            print('[%d] %s | %s | %d ch | %s' % (
                k, r['ID_Intervencion'], r['Actor_Final'],
                len(r['Texto'] or ''), r.get('Motivos_Revision')))
        return 0

    spec = sys.argv[2]
    if ':' in spec:
        a, b = (int(x) for x in spec.split(':'))
    else:
        a = b = int(spec)
    trozo = sel[a:b + 1]
    if not trozo:
        print('rango vacio')
        return 1
    emitido = 0
    cuerpo = []
    for k, r in enumerate(trozo, a):
        partes = r.get('Partes') or ['']
        bloque = ('#### [%d/%d] %s | %s | motivos: %s | %d ch | parte %s de %d\n%s'
                  % (k, len(sel) - 1, r['ID_Intervencion'], r['Actor_Final'],
                     r.get('Motivos_Revision'), len(r['Texto'] or ''),
                     partes, len(partes), r['Texto'] or ''))
        emitido += len(bloque) + 1
        cuerpo.append(bloque)
    if emitido > TECHO:
        print(f'ALTO: el rango {spec} emitiría {emitido} caracteres, sobre el '
              f'techo de {TECHO}. Achica el rango; no se imprime a medias.')
        return 1
    if emitido > AVISO:
        print(f'aviso: {emitido} caracteres emitidos, sobre los {AVISO} seguros')
    print('\n'.join(cuerpo))
    print(f'--- filas {a}-{b} | {emitido} chars emitidos ---')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
