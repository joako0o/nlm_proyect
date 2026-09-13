"""Gate v7: veintinueve refinamientos funcionales sobre la entrega v6.

El esperado se deriva de la entrega v6 firmada y de la lectura lote8, NO del
constructor. Compara TODAS las filas, TODOS los campos y TODOS los miembros de
cada grupo. Las alertas de las filas nuevas se recalculan con review_flags, el
mismo módulo que usa el constructor, no se copian a mano.
"""
import argparse
import collections
import csv
import hashlib
import json
import re
from pathlib import Path

import build_base_referencia as builder
from context_warnings import contextual_motives, load_context_warnings
from diagnosticar_finales import read_rows
from functional_refinements_v5 import BASE, BASE_SHA, PATH, PARENTS, load_refinements, validate_refinements
from review_flags import review_reasons

ROOT = Path(__file__).resolve().parents[1]
CLEAN = lambda t: re.sub(r'\s*\n\s*', '\n', re.sub(r'[ \t]+', ' ', t))
FILAS_V6 = 9694
GRUPOS_V6 = 9234
ALERTAS_V6 = 467


def expected_rows(before, reviews, raw):
    """Deriva la salida esperada: sólo los 29 cortes, nada más."""
    by_id = {r['ID_Intervencion']: r for r in before}
    expected, lineage, rename = [], [], {}
    for old in before:
        p = old['ID_Padre']
        entry = reviews.get(p)
        num = old['Numero_Segmento']
        if entry and num == 1:
            if old['Texto'] != entry['Texto_Original']:
                raise ValueError('La entrega v6 no coincide con el registro funcional v5')
            previous = by_id[entry['ID_Anterior']]
            a = {**old, 'Texto': entry['Texto_Personal'], 'Tipo_Acta': None,
                 'ID_Turno': previous['ID_Turno'], 'Relacion_Turno': 'CONTINUIDAD_EXPLICITA',
                 'ID_Antecedente_Continuidad': previous['ID_Intervencion'],
                 'ID_Ancla_Actor': old['ID_Intervencion']}
            b = {**old, 'Texto': entry['Texto_Constancia'], 'Numero_Segmento': 2,
                 'ID_Intervencion': old['ID_Intervencion'].rsplit(':', 1)[0] + ':2',
                 'ID_Bloque_Texto': old['ID_Bloque_Texto'].rsplit('B', 1)[0] + 'B2'}
            parts = [('PERSONAL', a, 0, len(a['Texto'])),
                     ('CONSTANCIA', b, len(a['Texto']) + len(entry['Separador']),
                      len(old['Texto']))]
        else:
            r = dict(old)
            if entry:
                bloque = int(old['ID_Bloque_Texto'].rsplit('B', 1)[1])
                r.update(Numero_Segmento=num + 1,
                         ID_Intervencion=old['ID_Intervencion'].rsplit(':', 1)[0] + f':{num + 1}',
                         ID_Bloque_Texto=old['ID_Bloque_Texto'].rsplit('B', 1)[0] + f'B{bloque + 1}')
            rename[old['ID_Intervencion']] = r['ID_Intervencion']
            parts = [('INTEGRA', r, 0, len(r['Texto']))]
        for kind, r, start, end in parts:
            r['ID'] = len(expected) + 1
            expected.append(r)
            lineage.append(dict(ID_Anterior=old['ID_Intervencion'], ID_Nuevo=r['ID_Intervencion'],
                                ID_Padre=p, Parte=kind, Inicio_En_Fila_Anterior=start,
                                Fin_En_Fila_Anterior=end,
                                SHA256_Texto=hashlib.sha256(r['Texto'].encode()).hexdigest()))
    # Duplicados: el constructor los cuenta sobre TODOS los segmentos post-corte.
    exact = collections.Counter(CLEAN(r['Texto']) for r in expected)
    touched = {r['ID_Intervencion'] for e in reviews.values()
               for r in ({'ID_Intervencion': e['ID_Fila_Original']},
                         {'ID_Intervencion': e['ID_Fila_Original'].rsplit(':', 1)[0] + ':2'})}
    context_alerts = load_context_warnings(raw)
    for r in expected:
        dup = exact[CLEAN(r['Texto'])] > 1
        r['Duplicado_Exacto'] = 'SI' if dup else 'NO'
        r['Duplicado_Formula'] = ('SI' if dup and builder.is_formula(CLEAN(r['Texto'])) else 'NO')
        if r['ID_Intervencion'] in touched:
            # Recalcular con el mismo motor de alertas, no asumir el resultado.
            reasons = sorted(set(review_reasons(r, builder.TURN_DETECTOR, builder.split_sentences)
                                 + contextual_motives(r, context_alerts)))
            r['Estado_Revision'] = 'PENDIENTE_REVISION' if reasons else 'SIN_ALERTAS_AUTOMATICAS'
            r['Motivos_Revision'] = ';'.join(reasons) or None
    for r in expected:
        for key in ('ID_Ancla_Actor', 'ID_Antecedente_Continuidad'):
            r[key] = rename.get(r[key], r[key])
    return expected, lineage


def members(rows):
    grupos = collections.defaultdict(list)
    for r in rows:
        grupos[r['ID_Turno']].append(r['ID_Intervencion'])
    return dict(grupos)


def compare(before, after, reviews):
    want, lineage = expected_rows(before, reviews,
                                  {int(r['ID']): r for r in read_rows(ROOT / 'data/raw/consolidado_final.xlsx')})
    if len(after) != len(want):
        raise ValueError(f'Cardinalidad distinta del refinamiento v5: {len(after)} vs {len(want)}')
    for n, (a, b) in enumerate(zip(want, after), 1):
        if a != b:
            campos = [k for k in set(a) | set(b) if a.get(k) != b.get(k)]
            raise ValueError(f'Fila {n} ({a.get("ID_Intervencion")}): campos no autorizados: {campos}')
    if members(want) != members(after):
        raise ValueError('Membresía global modificada')
    errores = validate_refinements(after, reviews)
    if errores:
        raise ValueError(errores)
    nuevas = sorted(r['ID_Intervencion'] for r in after
                    if 'DUPLICADO_NO_FORMULA' in (r['Motivos_Revision'] or '')
                    and r['ID_Intervencion'].rsplit(':', 1)[0] in
                    {e['ID_Fila_Original'].rsplit(':', 1)[0] for e in reviews.values()}
                    and r['ID_Intervencion'].endswith(':2'))
    report = dict(Perfil='procedimental-v7', Baseline='procedimental-v6', Pasa=True,
                  Filas_Antes=len(before), Filas_Despues=len(after),
                  Refinamientos=len(reviews), Continuidades_Personales=len(reviews),
                  Grupos_Antes=len(members(before)), Grupos_Despues=len(members(after)),
                  Comparacion=('Todas las filas, todos los campos y todos los miembros de cada '
                               'grupo; sin excepciones globales'),
                  Alertas_Antes=sum(bool(r['Motivos_Revision']) for r in before),
                  Alertas_Despues=sum(bool(r['Motivos_Revision']) for r in after),
                  Alertas_Cerradas=0,
                  Alertas_Nuevas=nuevas,
                  Motivo_Nuevo=('DUPLICADO_NO_FORMULA: constancias textualmente idénticas entre '
                                'sesiones; no se elimina texto ni se declara error'),
                  Padres_Con_Alertas=len({r['ID_Padre'] for r in after if r['Motivos_Revision']}),
                  SHA256_Baseline=BASE_SHA,
                  SHA256_Registro=hashlib.sha256(PATH.read_bytes()).hexdigest())
    return report, lineage


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    args = parser.parse_args()
    if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASE_SHA:
        raise ValueError('La entrega procedimental v6 cambió')
    raw = {r['ID']: r for r in read_rows(ROOT / 'data/raw/consolidado_final.xlsx')}
    reviews = load_refinements(raw)
    target = args.candidate / BASE.name
    report, lineage = compare(read_rows(BASE), read_rows(target), reviews)
    report['SHA256_Candidato'] = hashlib.sha256(target.read_bytes()).hexdigest()
    with (args.candidate / 'linaje_funcional.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(lineage[0]), quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(lineage)
    (args.candidate / 'comparacion_funcional.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
