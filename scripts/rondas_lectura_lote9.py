#!/usr/bin/env python
"""Plan de rondas de lectura del eje multihablante, version 2.

Dos cambios respecto de la version 1:

1. Las rondas son coherentes por sesion. Leer filas sueltas de reuniones distintas
   no deja juzgar si una segunda voz quedo pegada: para eso hace falta ver el flujo
   de hablantes alrededor. Se ordena por banda de largo y, dentro de la banda, por
   fecha e ID.

2. Se publica un manifiesto legible (CSV) con los IDs de cada ronda, para que el
   alcance sea visible antes de empezar.

Uso:
    python scripts/rondas_lectura_lote9.py plan
    python scripts/rondas_lectura_lote9.py leer N
    python scripts/rondas_lectura_lote9.py estado
"""
import csv
import json
import pathlib
import sys

sys.path.insert(0, 'scripts')
from diagnosticar_finales import read_rows  # noqa: E402

V7 = pathlib.Path('data/releases/continuidad_procedimental_v7/consolidado_base_referencia.xlsx')
LECT = pathlib.Path('docs/continuidad_lote9_2026-09-09/lecturas.json')
PLAN = pathlib.Path('docs/continuidad_lote9_2026-09-09/plan_rondas.json')
MANIF = pathlib.Path('docs/continuidad_lote9_2026-09-09/plan_rondas.csv')
LIM = 18000
CORTE_TEXTO = 17500

BANDAS = [
    ('A', 1500, 10 ** 9, 'muy largas'),
    ('B', 800, 1500, 'largas'),
    ('C', 400, 800, 'medianas'),
    ('D', 0, 400, 'cortas'),
]


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


def orden(rows):
    """Banda de largo primero, sesion despues."""
    out = []
    for letra, lo, hi, _ in BANDAS:
        sel = [r for r in rows if lo <= len(r['Texto']) < hi]
        sel.sort(key=lambda r: (str(r['Fecha'])[:10], r['ID_Intervencion']))
        for r in sel:
            out.append((letra, r))
    return out


def construir():
    rows = filas()
    pend, leidas = pendientes(rows)

    items = []
    for letra, r in orden(pend):
        t = r['Texto']
        if len(t) <= CORTE_TEXTO:
            items.append((letra, r, t, ''))
        else:
            n = -(-len(t) // CORTE_TEXTO)
            for k in range(n):
                items.append((letra, r, t[k * CORTE_TEXTO:(k + 1) * CORTE_TEXTO],
                              ' (parte %d/%d)' % (k + 1, n)))

    rondas, actual, n = [], [], 0
    for letra, r, t, parte in items:
        c = len(t) + len(cab(r, parte)) + 2
        if actual and n + c > LIM:
            rondas.append(actual)
            actual, n = [], 0
        actual.append({'id': r['ID_Intervencion'], 'parte': parte, 'chars': len(t),
                       'banda': letra, 'fecha': str(r['Fecha'])[:10],
                       'actor': r['Actor_Final']})
        n += c
    if actual:
        rondas.append(actual)

    doc = {
        'Version': 2,
        'Criterio': ('Banda de largo (A>=1500, B 800-1499, C 400-799, D<400) y dentro de '
                     'cada banda por fecha e ID, para que cada ronda sea una sesion '
                     'coherente. Las filas que no caben se parten en varias rondas.'),
        'Limite_Chars_Por_Ronda': LIM,
        'Base': str(V7),
        'Filas_Corpus': len(rows),
        'Filas_Ya_Leidas': len(leidas),
        'Filas_Pendientes': len(pend),
        'Bandas': [{'Banda': b, 'Desde': lo, 'Hasta': (hi if hi < 10 ** 9 else None),
                    'Descripcion': d,
                    'Filas': sum(1 for r in pend if lo <= len(r['Texto']) < hi)}
                   for b, lo, hi, d in BANDAS],
        'Rondas': [{'Ronda': k + 1, 'Filas': len(x),
                    'Chars': sum(i['chars'] for i in x),
                    'Bandas': sorted({i['banda'] for i in x}),
                    'Sesiones': sorted({i['fecha'] for i in x}),
                    'IDs': [i['id'] for i in x],
                    'Items': x} for k, x in enumerate(rondas)],
    }
    PLAN.parent.mkdir(parents=True, exist_ok=True)
    PLAN.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding='utf-8')

    with MANIF.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Ronda', 'Bandas', 'Tramos', 'Chars', 'Sesiones',
                    'Primera_Fecha', 'Ultima_Fecha', 'IDs'])
        for r in doc['Rondas']:
            w.writerow([r['Ronda'], '+'.join(r['Bandas']), r['Filas'], r['Chars'],
                        len(r['Sesiones']), r['Sesiones'][0], r['Sesiones'][-1],
                        ' '.join(r['IDs'])])

    print('plan    :', PLAN)
    print('manifiesto:', MANIF)
    print('rondas %d | pendientes %s | ya leidas %s'
          % (len(rondas), f'{len(pend):,}', f'{len(leidas):,}'))
    print()
    print('%-6s %-14s %8s %8s' % ('banda', 'rango', 'filas', 'rondas'))
    ini = 1
    for b in doc['Bandas']:
        nr = sum(1 for r in doc['Rondas'] if r['Bandas'] == [b['Banda']])
        rng = ('%d+' % b['Desde']) if b['Hasta'] is None else '%d-%d' % (b['Desde'], b['Hasta'] - 1)
        print('%-6s %-14s %8s %8d' % (b['Banda'] + ' ' + b['Descripcion'], rng,
                                      f"{b['Filas']:,}", nr))
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
        total += len(t)
        print('#### [%d] %s%s | %s | %s | %d ch | %s'
              % (n, it['id'], it['parte'], f['Actor_Final'], str(f['Fecha'])[:10],
                 len(t), f.get('Motivos_Revision') or 'sin motivos'))
        print(t)
        print()
    print('--- RONDA %d/%d | banda %s | %d tramos | %s chars | ult. fila %s ---'
          % (n, len(doc['Rondas']), '+'.join(r['Bandas']), r['Filas'],
             f'{total:,}', r['Items'][-1]['id'] + r['Items'][-1]['parte']))


def registrar(n, hallazgo, justificacion):
    """Anota en lecturas.json las filas de una ronda ya leida."""
    doc_plan = json.loads(PLAN.read_text(encoding='utf-8'))
    if not 1 <= n <= len(doc_plan['Rondas']):
        raise SystemExit('ronda fuera de rango: 1..%d' % len(doc_plan['Rondas']))
    ronda = doc_plan['Rondas'][n - 1]
    por_id = {x['ID_Intervencion']: x for x in filas()}

    lect = json.loads(LECT.read_text(encoding='utf-8'))
    casos = lect['Casos']
    nuevos = 0
    for it in ronda['Items']:
        rid = it['id']
        if rid in casos:
            print('  ya estaba:', rid)
            continue
        f = por_id[rid]
        casos[rid] = {
            'ID_Intervencion': rid,
            'ID_Padre': rid.split(':')[1],
            'Actor': f['Actor_Final'],
            'Caracteres': len(f['Texto']),
            'Hallazgo': hallazgo,
            'Lectura': 'COMPLETA',
            'Universo': 'PLAN_RONDAS_BANDA_' + it['banda'],
            'Ronda_Plan': n,
            'Justificacion': justificacion,
        }
        nuevos += 1
    lect['Total_Leidas'] = len(casos)
    lect['Filas_Con_Dos_Voces_Confirmadas'] = sorted(
        k for k, v in casos.items()
        if (v.get('Hallazgo') or v.get('Hallazgo_Cola_Entrega')) == 'DOS_VOCES')
    LECT.write_text(json.dumps(lect, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('ronda %d: %d filas anotadas como %s | total leidas %d'
          % (n, nuevos, hallazgo, len(casos)))


def estado():
    doc = json.loads(PLAN.read_text(encoding='utf-8'))
    todas = filas()
    pend, leidas = pendientes(todas)
    ids_plan = {i for r in doc['Rondas'] for i in r['IDs']}
    print('corpus            :', f'{len(todas):,}')
    print('leidas registradas:', f'{len(leidas):,}')
    print('pendientes hoy    :', f'{len(pend):,}')
    print('rondas del plan   :', len(doc['Rondas']))
    print('filas del plan    :', f'{len(ids_plan):,}')
    print('fuera del plan    :', f'{len({r["ID_Intervencion"] for r in pend} - ids_plan):,}')
    por_banda = {}
    for r in doc['Rondas']:
        por_banda.setdefault('+'.join(r['Bandas']), []).append(r['Ronda'])
    for b, ns in sorted(por_banda.items()):
        print('  banda %-4s rondas %d..%d (%d)' % (b, min(ns), max(ns), len(ns)))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    if sys.argv[1] == 'plan':
        construir()
    elif sys.argv[1] == 'leer':
        leer(int(sys.argv[2]))
    elif sys.argv[1] == 'estado':
        estado()
    elif sys.argv[1] == 'registrar':
        registrar(int(sys.argv[2]), sys.argv[3], sys.argv[4])
    else:
        raise SystemExit(__doc__)
