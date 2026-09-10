"""Inventario de los 71 pares del lote6 recalculado sobre la entrega v7.

No modifica las carpetas del lote6 ni del lote8: publica una vista nueva bajo
docs/ o .cache/. Los 29 cortes funcionales de v5 dejaron de ser límites porque el
aporte personal quedó agrupado con su antecedente; se informan explícitamente.
Los 24 pares restantes conservan la causa medida en el triaje del lote7.
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
import functional_refinements_v5 as f5

ROOT = Path(__file__).resolve().parents[1]
V5 = ROOT / 'data/releases/continuidad_procedimental_v5/consolidado_base_referencia.xlsx'
V6 = f5.BASE
V7 = ROOT / 'data/releases/continuidad_procedimental_v7/consolidado_base_referencia.xlsx'
V7_SHA = '84889a846ec0b3a2fce88d37f1d5a0a3676b33dcd962c428de7cdbb3c992d9a7'
V6_SHA = f5.BASE_SHA
LOTE7 = ROOT / 'docs/continuidad_lote7_2026-09-09/triaje_53.json'
LOTE8 = f5.READINGS
PARES_LOTE6 = 71
APLICADOS_V5 = len(f5.PARENTS)
CAMPOS = ['Izquierda', 'Derecha', 'Actor', 'Mismo_Padre', 'Caracteres_Izquierda',
          'Caracteres_Derecha', 'Fuente_Izquierda', 'Fuente_Derecha', 'Motivos_Izquierda',
          'Motivos_Derecha', 'Indicadores', 'Estado', 'Estado_Revision_Dirigida',
          'Causa_Lote7', 'Alcance_Lectura', 'Evidencia', 'Siguiente_Accion',
          'Enlace_Aplicado_V6', 'Corte_Aplicado_V7']


def applied_row(rows, left, right, estado):
    """Los pares ya agrupados no son límites: se describen con datos de v7."""
    by_id = {r['ID_Intervencion']: r for r in rows}
    a, b = by_id[left], by_id[right]
    return dict(Izquierda=left, Derecha=right, Actor=a['Actor_Final'],
                Mismo_Padre=a['ID_Padre'] == b['ID_Padre'],
                Caracteres_Izquierda=len(a['Texto']), Caracteres_Derecha=len(b['Texto']),
                Fuente_Izquierda=a['Fuente_Actor'], Fuente_Derecha=b['Fuente_Actor'],
                Motivos_Izquierda=a.get('Motivos_Revision') or '',
                Motivos_Derecha=b.get('Motivos_Revision') or '',
                Indicadores=estado, Estado=estado)


def causas_lote7():
    """Mapa extremo_izquierdo -> causa medida. Falla si la clasificación no cuadra."""
    paquete = json.loads(LOTE7.read_text())
    registros = paquete.get('Registros')
    if not isinstance(registros, list) or len(registros) != 53:
        raise ValueError('El triaje lote7 debe clasificar exactamente 53 pares')
    causas = {}
    for r in registros:
        left = r['Izquierda']
        if left in causas:
            raise ValueError(f'{left} aparece dos veces en el triaje lote7')
        causas[left] = r['Causa']
    return causas


def exports(rows, pkg):
    causas = causas_lote7()
    revisadas = json.loads(f5.PATH.read_text())['Revisiones']
    cortes = {e['ID_Fila_Original'] for e in revisadas.values()}
    # Límite interno creado por el corte: aporte personal contra su constancia.
    internos = {(e['ID_Fila_Original'], e['ID_Fila_Original'].rsplit(':', 1)[0] + ':2')
                for e in revisadas.values()}
    prior = inherited_statuses(rows)
    result = []
    lote6_cubiertos = set()
    for r in inventory(rows):
        left, right = r['Izquierda'], r['Derecha']
        if (left, right) not in internos:
            lote6_cubiertos.add((left, right))
        causa = causas.get(left, '')
        if (left, right) in internos:
            state = 'SEPARACION_FUNCIONAL_V5_INTERNA'
            read = 'PADRE_COMPLETO_EN_LOTE8'
            source = str(LOTE8.relative_to(ROOT))
            causa = 'APORTE_PERSONAL_Y_CONSTANCIA_EN_UNA_FILA'
            action = ('Límite creado por el corte v5: debe seguir separado. La constancia es '
                      'INSTITUCIONAL y no se une al aporte personal.')
        elif left in RESERVAS_ABIERTAS:
            read = 'PADRES_Y_GRUPOS_COMPLETOS_EN_LOTE6'
            state = DECISIONES_LOTE6[left][1]
            source = str(LOTE6_READINGS.relative_to(ROOT))
            action = pkg['Casos'][left]['Siguiente_Accion']
        elif left in prior:
            _, state, source = prior[left]
            read = 'RESPALDO_ANTERIOR_NO_RELECTURA_EN_LOTE6'
            action = 'Mantener separación; no tratarla como un enlace pendiente.'
        else:
            # Un par cortado en v5 ya no puede seguir siendo límite.
            if right in cortes:
                raise ValueError(f'{left}→{right} sigue siendo límite pese al corte v5')
            if not causa:
                raise ValueError(f'{left}→{right} es límite sin causa medida en el lote7')
            state = 'SIN_ADJUDICACION_EN_ESTE_INVENTARIO'
            source = str(LOTE7.relative_to(ROOT))
            read = 'CAUSA_MEDIDA_EN_LOTE7'
            action = 'Ver la causa medida en el triaje del lote7 antes de decidir una lectura.'
        result.append({**r, 'Estado_Revision_Dirigida': state, 'Causa_Lote7': causa,
                       'Alcance_Lectura': read, 'Evidencia': source, 'Siguiente_Accion': action,
                       'Enlace_Aplicado_V6': 'NO', 'Corte_Aplicado_V7': 'NO'})
    for left, right in sorted(NEW_PAIRS):
        result.append({**applied_row(rows, left, right, 'AGRUPADO_EN_V6'), 'Causa_Lote7': '',
                       'Estado_Revision_Dirigida': 'ENLACE_INTRAPADRE_APLICADO_V6',
                       'Alcance_Lectura': 'PADRES_Y_GRUPOS_COMPLETOS_EN_LOTE6',
                       'Evidencia': 'docs/continuidad_lote6_2026-09-09/lecturas.json',
                       'Siguiente_Accion': 'Enlace aplicado y probado en v6; no generalizar a otros casos.',
                       'Enlace_Aplicado_V6': 'SI', 'Corte_Aplicado_V7': 'NO'})
    # Los 29 cortes de v5: el aporte personal quedó en el turno de su antecedente.
    for padre in sorted(f5.PARENTS):
        entry = revisadas[str(padre)]
        left, right = entry['ID_Anterior'], entry['ID_Fila_Original']
        by_id = {r['ID_Intervencion']: r for r in rows}
        if by_id[left]['ID_Turno'] != by_id[right]['ID_Turno']:
            raise ValueError(f'{left}→{right} no quedó agrupado en v7')
        result.append({**applied_row(rows, left, right, 'AGRUPADO_EN_V7_POR_CORTE_V5'),
                       'Causa_Lote7': 'APORTE_PERSONAL_Y_CONSTANCIA_EN_UNA_FILA',
                       'Estado_Revision_Dirigida': 'SEPARACION_FUNCIONAL_APLICADA_V5',
                       'Alcance_Lectura': 'PADRE_COMPLETO_EN_LOTE8',
                       'Evidencia': str(LOTE8.relative_to(ROOT)),
                       'Siguiente_Accion': ('Corte aplicado y probado en v7; la constancia mantiene '
                                            'ACUERDO_CONSEJO y Vergara conserva la atribución.'),
                       'Enlace_Aplicado_V6': 'NO', 'Corte_Aplicado_V7': 'SI'})
    # Rendición de cuentas: los 71 pares del lote6 más los 29 límites internos del corte.
    cubiertos = lote6_cubiertos | set(sorted(NEW_PAIRS)) | {
        (revisadas[str(p)]['ID_Anterior'], revisadas[str(p)]['ID_Fila_Original'])
        for p in f5.PARENTS}
    if len(cubiertos) != PARES_LOTE6:
        raise ValueError(f'La vista debe rendir los {PARES_LOTE6} pares del lote6, no {len(cubiertos)}')
    vistos = sum(1 for r in result if r['Estado_Revision_Dirigida'] == 'SEPARACION_FUNCIONAL_V5_INTERNA')
    if vistos != APLICADOS_V5:
        raise ValueError(f'El corte debe crear {APLICADOS_V5} límites internos, no {vistos}')
    if len(result) != PARES_LOTE6 + APLICADOS_V5:
        raise ValueError(f'La vista debe tener {PARES_LOTE6 + APLICADOS_V5} filas, no {len(result)}')
    result.sort(key=lambda r: r['Izquierda'])
    return result


def resumen(before, after, result):
    estados = collections.Counter(r['Estado_Revision_Dirigida'] for r in result)
    return dict(
        Pares_Lote6=PARES_LOTE6, Pares_Visibles_En_V7=len(result),
        Pares_Salidos_Del_Inventario_Por_Agrupacion=len(NEW_PAIRS) + APLICADOS_V5,
        Salidos_Por_Enlace_V6=[list(p) for p in sorted(NEW_PAIRS)],
        Salidos_Por_Corte_V7=sorted(f5.PARENTS),
        Estados=dict(estados),
        Causas_De_Los_Sin_Adjudicar=dict(collections.Counter(
            r['Causa_Lote7'] for r in result
            if r['Estado_Revision_Dirigida'] == 'SIN_ADJUDICACION_EN_ESTE_INVENTARIO')),
        Filas=len(after),
        Grupos_Antes=len({r['ID_Turno'] for r in before}),
        Grupos_Despues=len({r['ID_Turno'] for r in after}),
        Alertas_Antes=sum(bool(r['Motivos_Revision']) for r in before),
        Alertas_Despues=sum(bool(r['Motivos_Revision']) for r in after),
        Alertas_Cerradas=0,
        Reservas_Abiertas=sorted(RESERVAS_ABIERTAS),
        SHA256_V5=hashlib.sha256(V5.read_bytes()).hexdigest(),
        SHA256_V6=V6_SHA, SHA256_V7=hashlib.sha256(V7.read_bytes()).hexdigest(),
        SHA256_Lecturas_Lote8=hashlib.sha256(LOTE8.read_bytes()).hexdigest(),
        Nota=('29 pares dejaron de ser límites al separarse aporte personal y constancia en '
              'v7; las tres reservas del lote6 siguen abiertas. Los pares sin adjudicación no '
              'son errores ni casos nunca leídos y no estiman la cobertura semántica del corpus.'))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', type=Path, required=True)
    out = parser.parse_args(argv).salida.resolve()
    if out.exists() or not any((ROOT / r).resolve() in out.parents for r in ('.cache', 'docs')):
        raise ValueError('Se requiere destino nuevo bajo .cache/ o docs/, nunca data/')
    if hashlib.sha256(V5.read_bytes()).hexdigest() != V5_SHA:
        raise ValueError('La entrega v5 cambió')
    if hashlib.sha256(V6.read_bytes()).hexdigest() != V6_SHA:
        raise ValueError('La entrega v6 cambió')
    if hashlib.sha256(V7.read_bytes()).hexdigest() != V7_SHA:
        raise ValueError('La entrega v7 cambió')
    before, after = read_rows(V6), read_rows(V7)
    result = exports(after, json.loads(LOTE6_READINGS.read_text()))
    out.mkdir(parents=True)
    with (out / 'inventario_estado_v7.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(result)
    summary = resumen(before, after, result)
    (out / 'resumen.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
