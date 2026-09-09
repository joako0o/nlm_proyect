"""Inventario de los71 pares del lote6 recalculado sobre la entrega v6.

No modifica la carpeta del lote6: publica una vista nueva bajo docs/ o .cache/.
Los dos enlaces aplicados ya no son límites (están agrupados), así que se
informan explícitamente con sus campos medidos en v6 y se rinde la cuenta
completa de los71 pares del lote6.
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
from diagnosticar_finales import read_rows
from auditar_continuidad_turnos import inventory
from revisar_reservas_complejas import inherited_statuses, READINGS as LOTE6_READINGS
from reviewed_intrapara_v4 import NEW_PAIRS, RESERVAS_ABIERTAS, DECISIONES_LOTE6, BASE_SHA as V5_SHA

ROOT = Path(__file__).resolve().parents[1]
V5 = ROOT / 'data/releases/continuidad_procedimental_v5/consolidado_base_referencia.xlsx'
V6 = ROOT / 'data/releases/continuidad_procedimental_v6/consolidado_base_referencia.xlsx'
PARES_LOTE6 = 71
CAMPOS = ['Izquierda', 'Derecha', 'Actor', 'Mismo_Padre', 'Caracteres_Izquierda',
          'Caracteres_Derecha', 'Fuente_Izquierda', 'Fuente_Derecha', 'Motivos_Izquierda',
          'Motivos_Derecha', 'Indicadores', 'Estado', 'Estado_Revision_Dirigida',
          'Alcance_Lectura', 'Evidencia', 'Siguiente_Accion', 'Enlace_Aplicado_V6']


def applied_row(rows, left, right):
    """Los pares ya agrupados no son límites: se describen con datos de v6."""
    by_id = {r['ID_Intervencion']: r for r in rows}
    a, b = by_id[left], by_id[right]
    return dict(Izquierda=left, Derecha=right, Actor=a['Actor_Final'],
                Mismo_Padre=a['ID_Padre'] == b['ID_Padre'],
                Caracteres_Izquierda=len(a['Texto']), Caracteres_Derecha=len(b['Texto']),
                Fuente_Izquierda=a['Fuente_Actor'], Fuente_Derecha=b['Fuente_Actor'],
                Motivos_Izquierda=a.get('Motivos_Revision') or '',
                Motivos_Derecha=b.get('Motivos_Revision') or '',
                Indicadores='AGRUPADO_EN_V6', Estado='AGRUPADO_EN_V6')


def exports(rows, pkg):
    prior = inherited_statuses(rows)
    result = []
    for r in inventory(rows):
        left = r['Izquierda']
        if left in RESERVAS_ABIERTAS:
            read = 'PADRES_Y_GRUPOS_COMPLETOS_EN_LOTE6'
            state = DECISIONES_LOTE6[left][1]
            source = str(LOTE6_READINGS.relative_to(ROOT))
            action = pkg['Casos'][left]['Siguiente_Accion']
        elif left in prior:
            _, state, source = prior[left]
            read = 'RESPALDO_ANTERIOR_NO_RELECTURA_EN_LOTE6'
            action = 'Mantener separación; no tratarla como un enlace pendiente.'
        else:
            state, source = 'SIN_ADJUDICACION_EN_ESTE_INVENTARIO', ''
            read = 'NO_EVALUADO_EN_ESTE_LOTE_NO_EQUIVALE_A_NUNCA_LEIDO'
            action = 'Localizar fichas previas y comprobar su alcance antes de decidir una nueva lectura.'
        result.append({**r, 'Estado_Revision_Dirigida': state, 'Alcance_Lectura': read,
                       'Evidencia': source, 'Siguiente_Accion': action, 'Enlace_Aplicado_V6': 'NO'})
    for left, right in sorted(NEW_PAIRS):
        result.append({**applied_row(rows, left, right),
                       'Estado_Revision_Dirigida': 'ENLACE_INTRAPADRE_APLICADO_V6',
                       'Alcance_Lectura': 'PADRES_Y_GRUPOS_COMPLETOS_EN_LOTE6',
                       'Evidencia': 'docs/continuidad_lote6_2026-09-09/lecturas.json',
                       'Siguiente_Accion': 'Enlace aplicado y probado en v6; no generalizar a otros casos.',
                       'Enlace_Aplicado_V6': 'SI'})
    result.sort(key=lambda r: r['Izquierda'])
    if len(result) != PARES_LOTE6:
        raise ValueError(f'La vista debe rendir los {PARES_LOTE6} pares del lote6, no {len(result)}')
    return result


def resumen(before, after, result):
    return dict(
        Pares_Lote6=PARES_LOTE6, Pares_Visibles_En_V6=len(result),
        Pares_Salidos_Del_Inventario_Por_Agrupacion=len(NEW_PAIRS),
        Salidos_Por_Agrupacion=[list(p) for p in sorted(NEW_PAIRS)],
        Estados=dict(collections.Counter(r['Estado_Revision_Dirigida'] for r in result)),
        Filas=len(after), Grupos_Antes=len({r['ID_Turno'] for r in before}),
        Grupos_Despues=len({r['ID_Turno'] for r in after}),
        Alertas_Antes=sum(bool(r['Motivos_Revision']) for r in before),
        Alertas_Despues=sum(bool(r['Motivos_Revision']) for r in after),
        Reservas_Abiertas=sorted(RESERVAS_ABIERTAS),
        SHA256_V5=hashlib.sha256(V5.read_bytes()).hexdigest(),
        SHA256_V6=hashlib.sha256(V6.read_bytes()).hexdigest(),
        Nota=('Dos pares dejaron de ser límites al agruparse en v6; las tres reservas del lote6 '
              'siguen abiertas. Los pares sin adjudicación no son errores ni casos nunca leídos '
              'y no estiman la cobertura semántica del corpus.'))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', type=Path, required=True)
    out = parser.parse_args(argv).salida.resolve()
    if out.exists() or not any((ROOT / r).resolve() in out.parents for r in ('.cache', 'docs')):
        raise ValueError('Se requiere destino nuevo bajo .cache/ o docs/, nunca data/')
    if hashlib.sha256(V5.read_bytes()).hexdigest() != V5_SHA:
        raise ValueError('La entrega v5 cambió')
    before, after = read_rows(V5), read_rows(V6)
    result = exports(after, json.loads(LOTE6_READINGS.read_text()))
    out.mkdir(parents=True)
    with (out / 'inventario_estado_v6.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(result)
    summary = resumen(before, after, result)
    (out / 'resumen.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
