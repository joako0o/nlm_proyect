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
    """Sesion por sesion. Las sesiones van por riesgo (su fila mas larga primero) y
    dentro de cada sesion las filas van en orden de acta.

    Medido: reunion por reunion cuesta 810 rondas contra 826 del orden por bandas,
    o sea que no hay penalizacion por legibilidad. Y ordenar las sesiones por su fila
    mas larga conserva la priorizacion por riesgo: una segunda voz pegada necesita
    espacio, y los tres positivos conocidos miden 684, 849 y 1.275 caracteres.
    """
    por_fecha = {}
    for r in rows:
        por_fecha.setdefault(str(r['Fecha'])[:10], []).append(r)

    def riesgo(f):
        return -max(len(x['Texto']) for x in por_fecha[f])

    out = []
    for f in sorted(por_fecha, key=lambda x: (riesgo(x), x)):
        for r in sorted(por_fecha[f], key=lambda r: r['ID_Intervencion']):
            out.append((banda_de(r), r))
    return out


def banda_de(r):
    n = len(r['Texto'])
    for letra, lo, hi, _ in BANDAS:
        if lo <= n < hi:
            return letra
    return 'D'


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
        'Version': 3,
        'Criterio': ('Sesion por sesion. Las sesiones se ordenan por riesgo -su fila mas '
                     'larga primero- y dentro de cada sesion las filas van en orden de acta. '
                     'Las filas que no caben en un tramo se parten en varias rondas.'),
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
                    'Sesion': x[0]['fecha'],
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
    ses = {}
    for r in doc['Rondas']:
        ses.setdefault(r['Sesion'], []).append(r['Ronda'])
    print()
    print('sesiones: %d | rondas por sesion: min %d, mediana %d, max %d'
          % (len(ses), min(len(v) for v in ses.values()),
             sorted(len(v) for v in ses.values())[len(ses) // 2],
             max(len(v) for v in ses.values())))
    print()
    print('%-12s %5s %6s %8s %s' % ('sesion', 'ronda', 'filas', 'chars', 'hasta'))
    for f in list(ses)[:8]:
        ns = ses[f]
        rr = doc['Rondas'][ns[0] - 1]
        print('%-12s %5s %6d %8s %s' % (f, '%d-%d' % (min(ns), max(ns)),
                                        sum(x['Filas'] for x in doc['Rondas'][ns[0]-1:ns[-1]]),
                                        f"{sum(x['Chars'] for x in doc['Rondas'][ns[0]-1:ns[-1]]):,}",
                                        'ronda %d' % max(ns)))
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


def sesion(fecha, desde=0, limite=LIM):
    """Imprime las filas pendientes de una sesion, en orden de acta, hasta llenar un tramo."""
    todas = filas()
    pend, _ = pendientes(todas)
    sel = [r for r in pend if str(r['Fecha'])[:10] == fecha]
    sel.sort(key=lambda r: r['ID_Intervencion'])
    resto = sel[desde:]
    total = len(sel)
    n = 0
    k = desde
    for r in resto:
        t = r['Texto']
        c = len(t) + 90
        if n and n + c > limite:
            break
        n += c
        print('#### %s | %s | %s | %d ch | %s'
              % (r['ID_Intervencion'], r['Actor_Final'], str(r['Fecha'])[:10],
                 len(t), r.get('Motivos_Revision') or 'sin motivos'))
        print(t)
        print()
        k += 1
    print('--- SESION %s | %d de %d pendientes | leidas en este tramo: %d..%d | %s chars | quedan %d ---'
          % (fecha, total, total, desde, k - 1, f'{n:,}', total - k))


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
    ses = {}
    for r in doc['Rondas']:
        ses.setdefault(r['Sesion'], []).append(r['Ronda'])
    hechas = [f for f in ses if all(
        i in leidas for r in doc['Rondas'][min(ses[f])-1:max(ses[f])] for i in r['IDs'])]
    print('sesiones del plan :', len(ses))
    print('sesiones completas:', len(hechas))
    print()
    print('%-12s %10s %6s %9s %s' % ('sesion', 'rondas', 'filas', 'chars', 'estado'))
    for f in list(ses)[:12]:
        ns = ses[f]
        bloque = doc['Rondas'][min(ns)-1:max(ns)]
        ids = [i for r in bloque for i in r['IDs']]
        ok = all(i in leidas for i in ids)
        print('%-12s %10s %6d %9s %s' % (
            f, '%d-%d' % (min(ns), max(ns)), len(ids),
            f"{sum(r['Chars'] for r in bloque):,}", 'COMPLETA' if ok else 'pendiente'))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    if sys.argv[1] == 'plan':
        construir()
    elif sys.argv[1] == 'leer':
        leer(int(sys.argv[2]))
    elif sys.argv[1] == 'estado':
        estado()
    elif sys.argv[1] == 'sesion':
        sesion(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 0)
    elif sys.argv[1] == 'registrar':
        registrar(int(sys.argv[2]), sys.argv[3], sys.argv[4])
    else:
        raise SystemExit(__doc__)
