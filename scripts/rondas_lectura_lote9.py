#!/usr/bin/env python
"""Plan de rondas de lectura del eje multihablante, y lector de una ronda.

Uso:
    python .cache/rondas.py plan              # genera docs/continuidad_lote9_2026-09-09/plan_rondas.json
    python .cache/rondas.py leer N            # imprime la ronda N
    python .cache/rondas.py estado            # progreso

Criterio de orden: largo decreciente. Una segunda voz pegada al final de una fila
necesita espacio; los tres positivos conocidos miden 684, 849 y 1.275 caracteres,
asi que las filas largas van primero y el plan se puede cortar en cualquier punto
habiendo cubierto lo de mayor riesgo.

Las filas que no caben en un tramo se parten en varias rondas (Parte 1/2, ...).
"""
import json
import pathlib
import sys

sys.path.insert(0, 'scripts')
from diagnosticar_finales import read_rows  # noqa: E402

V7 = pathlib.Path('data/releases/continuidad_procedimental_v7/consolidado_base_referencia.xlsx')
LECT = pathlib.Path('docs/continuidad_lote9_2026-09-09/lecturas.json')
PLAN = pathlib.Path('docs/continuidad_lote9_2026-09-09/plan_rondas.json')
LIM = 18000
CORTE_TEXTO = 17500


def cab(r, parte=''):
    return '#### %s%s | %s | %s | %d ch | %s' % (
        r['ID_Intervencion'], parte, r['Actor_Final'], str(r['Fecha'])[:10],
        len(r['Texto']), (r.get('Motivos_Revision') or 'sin motivos'))


def filas():
    rows = read_rows(V7)
    for r in rows:
        r['Texto'] = r.get('Texto') or ''
        r['ID_Intervencion'] = str(r['ID_Intervencion'])
    return rows


def pendientes(rows):
    lect = json.loads(LECT.read_text(encoding='utf-8'))
    leidas = set(lect['Casos'])
    return [r for r in rows if r['ID_Intervencion'] not in leidas], leidas


def construir():
    rows = filas()
    pend, leidas = pendientes(rows)
    items = []
    for r in sorted(pend, key=lambda x: -len(x['Texto'])):
        t = r['Texto']
        if len(t) <= CORTE_TEXTO:
            items.append((r, t, ''))
        else:
            n = -(-len(t) // CORTE_TEXTO)
            for k in range(n):
                items.append((r, t[k * CORTE_TEXTO:(k + 1) * CORTE_TEXTO],
                              ' (parte %d/%d)' % (k + 1, n)))

    rondas, actual, n = [], [], 0
    for r, t, parte in items:
        c = len(t) + len(cab(r, parte)) + 2
        if actual and n + c > LIM:
            rondas.append(actual)
            actual, n = [], 0
        actual.append({'id': r['ID_Intervencion'], 'parte': parte, 'chars': len(t)})
        n += c
    if actual:
        rondas.append(actual)

    doc = {
        'Version': 1,
        'Criterio': 'Largo decreciente; las filas que no caben se parten en varias rondas.',
        'Limite_Chars_Por_Ronda': LIM,
        'Base': str(V7),
        'Filas_Corpus': len(rows),
        'Filas_Ya_Leidas': len(leidas),
        'Filas_Pendientes': len(pend),
        'Rondas': [{'Ronda': k + 1, 'Filas': len(x),
                    'Chars': sum(i['chars'] for i in x),
                    'IDs': sorted({i['id'] for i in x}),
                    'Items': x} for k, x in enumerate(rondas)],
    }
    PLAN.parent.mkdir(parents=True, exist_ok=True)
    PLAN.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding='utf-8')
    print('plan escrito en', PLAN)
    print('rondas: %d | filas pendientes: %s | ya leidas: %s'
          % (len(rondas), f'{len(pend):,}', f'{len(leidas):,}'))
    return doc


def leer(n):
    doc = json.loads(PLAN.read_text(encoding='utf-8'))
    if not 1 <= n <= len(doc['Rondas']):
        raise SystemExit('ronda fuera de rango: 1..%d' % len(doc['Rondas']))
    r = doc['Rondas'][n - 1]
    por_id = {x['ID_Intervencion']: x for x in filas()}
    total = 0
    for it in r['Items']:
        f = por_id[it['id']]
        t = f['Texto']
        if it['parte']:
            k = int(it['parte'].split('/')[0].split()[-1]) - 1
            t = t[k * CORTE_TEXTO:(k + 1) * CORTE_TEXTO]
        total += len(t) + 90
        print('#### [%d] %s%s | %s | %s | %d ch | %s'
              % (n, it['id'], it['parte'], f['Actor_Final'], str(f['Fecha'])[:10],
                 len(t), f.get('Motivos_Revision') or 'sin motivos'))
        print(t)
        print()
    print('--- RONDA %d/%d | %d tramos | %s chars texto | ~%s emitidos ---'
          % (n, len(doc['Rondas']), r['Filas'], f'{total:,}', f'{total:,}'))


def estado():
    doc = json.loads(PLAN.read_text(encoding='utf-8'))
    todas = filas()
    pend, leidas = pendientes(todas)
    print('corpus            :', f"{len(todas):,}")
    print('leidas registradas:', f"{len(leidas):,}")
    print('pendientes hoy    :', f"{len(pend):,}")
    print('rondas del plan   :', len(doc['Rondas']))
    ids_plan = {i for r in doc['Rondas'] for i in r['IDs']}
    print('filas del plan    :', f'{len(ids_plan):,}')
    print('fuera del plan    :', f'{len({r["ID_Intervencion"] for r in pend} - ids_plan):,}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    if sys.argv[1] == 'plan':
        construir()
    elif sys.argv[1] == 'leer':
        leer(int(sys.argv[2]))
    elif sys.argv[1] == 'estado':
        estado()
    else:
        raise SystemExit(__doc__)
