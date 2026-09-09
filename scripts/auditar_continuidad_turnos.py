"""Auditoría y escenario aislado de continuidad: nunca escribe en data/.

El inventario no aprueba enlaces. Sólo simula dos pares intrapadre leídos,
con evidencia y grupos completos acotados; no modifica el motor productivo,
las anclas, los intervalos ni las pruebas de continuidad publicadas.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import revisar_cola_comas as proof
from continuity import boundary, SECTION, EXPLICIT, CONTINUED, CONSEJO
from context_warnings import has_context_warning
from turns import normalize

SCOPE = 'AUDITORIA_CONTINUIDAD_1_SIN_APLICAR'
READ_PARENTS = {2796, 2797, 3012, 2685, 2885, 1901, 2779}
PROPOSALS = {
    'RPM-2009-11-12:2796:2': ('RPM-2009-11-12:2796:3', 'RPM-2009-11-12:2797:1'),
    'RPM-2010-03-18:3012:2': ('RPM-2010-03-18:3012:3',),
}
DECISIONS = {2796: 'SIMULAR_SIN_APLICAR', 3012: 'SIMULAR_SIN_APLICAR',
             2685: 'CONTINUIDAD_PLAUSIBLE_CON_AVISO_DUPLICADO',
             2885: 'NO_SIMULAR_POR_DANO', 1901: 'SEPARAR_POR_ACTA',
             2779: 'SEPARAR_POR_OTRA_VOZ'}


def inventory(rows):
    result = []
    for a, b in zip(rows, rows[1:]):
        if (a['Actor_Final'] != b['Actor_Final'] or a['Actor_Final'] == CONSEJO
                or str(a['Fecha'])[:10] != str(b['Fecha'])[:10]
                or a['ID_Turno'] == b['ID_Turno']):
            continue
        indicators = []
        if a.get('Tipo_Acta') or b.get('Tipo_Acta'):
            indicators.append('TIPO_ACTA_O_DOCUMENTO')
        if boundary(a['Texto']):
            indicators.append('BARRERA_LEXICA_IZQUIERDA')
        if SECTION.search(normalize(b['Texto'])):
            indicators.append('SECCION_DERECHA')
        if any(has_context_warning(x.get('Motivos_Revision')) for x in [a, b]):
            indicators.append('ALERTA_CONTEXTUAL')
        if any('POSIBLE_OTRO_HABLANTE_O_MENCION' in (x.get('Motivos_Revision') or '') for x in [a, b]):
            indicators.append('POSIBLE_OTRA_VOZ')
        if a['Fuente_Actor'] not in EXPLICIT | CONTINUED:
            indicators.append('IZQUIERDA_SIN_FUENTE_PROPAGABLE')
        if b['Fuente_Actor'] not in EXPLICIT | CONTINUED:
            indicators.append('DERECHA_SIN_FUENTE_PROPAGABLE')
        result.append(dict(Izquierda=a['ID_Intervencion'], Derecha=b['ID_Intervencion'],
                           Actor=a['Actor_Final'], Mismo_Padre=a['ID_Padre'] == b['ID_Padre'],
                           Caracteres_Izquierda=len(a['Texto']), Caracteres_Derecha=len(b['Texto']),
                           Fuente_Izquierda=a['Fuente_Actor'], Fuente_Derecha=b['Fuente_Actor'],
                           Motivos_Izquierda=a.get('Motivos_Revision') or '',
                           Motivos_Derecha=b.get('Motivos_Revision') or '',
                           Indicadores=';'.join(indicators), Estado='INVENTARIO_NO_APROBACION'))
    return result


def window(row, tail=False):
    return dict(ID_Intervencion=row['ID_Intervencion'],
                Texto=row['Texto'][-250:] if tail else row['Texto'][:250],
                SHA256_Fila=proof.parent_signature([row]), Lectura='VENTANA_HASTA_250_CARACTERES')


def validate(rows, package):
    if (not isinstance(package, dict) or package.get('Version') != 1
            or package.get('Alcance') != SCOPE or not isinstance(package.get('Padres'), dict)
            or {int(p) for p in package['Padres']} != READ_PARENTS
            or not isinstance(package.get('Decisiones'), list)):
        raise ValueError('Paquete de auditoría incompatible')
    proof.check_sources(package)
    if package['SHA256_Grupos_Actuales'] != group_signature(rows):
        raise ValueError('Los grupos publicados cambiaron')
    positions = {r['ID_Intervencion']: i for i, r in enumerate(rows)}
    if len(positions) != len(rows):
        raise ValueError('Intervalos duplicados')
    for p, evidence in package['Padres'].items():
        indices = [i for i, r in enumerate(rows) if r['ID_Padre'] == int(p)]
        if not indices:
            raise ValueError('Padre ausente')
        lo, hi = indices[0], indices[-1]
        if lo == 0 or hi + 1 >= len(rows) or indices != list(range(lo, hi + 1)):
            raise ValueError('Padre discontinuo o vecinos ausentes')
        pr = rows[lo:hi + 1]
        if (evidence['Lectura'] != 'PADRE_COMPLETO'
                or evidence['Fecha'] != str(pr[0]['Fecha'])[:10]
                or evidence['SHA256_Particion'] != proof.parent_signature(pr)
                or evidence['SHA256_Texto_Padre'] != proof.sha(evidence['Texto_Padre'])
                or proof.compact(evidence['Texto_Padre']) != ''.join(proof.compact(x['Texto']) for x in pr)
                or evidence['Vecino_Anterior'] != window(rows[lo - 1], tail=True)
                or evidence['Vecino_Siguiente'] != window(rows[hi + 1])):
            raise ValueError('Fuente, partición o ventana modificada')
    seen = set()
    for e in package['Decisiones']:
        p = e['ID_Padre']
        if (p in seen or e['Estado'] != DECISIONS.get(p) or not e['Justificacion']
                or not e['Reservas'] or not e['Siguiente_Accion']):
            raise ValueError('Decisión fuera de alcance, incompleta o duplicada')
        seen.add(p)
    if seen != set(DECISIONS):
        raise ValueError('Faltan decisiones o controles negativos')
    if set(package.get('Propuestas', {})) != set(PROPOSALS):
        raise ValueError('Sólo se simulan los dos pares leídos')
    for key, members in PROPOSALS.items():
        i = positions[key]
        a, b = rows[i:i + 2]
        evidence = package['Propuestas'][key]
        if (evidence.get('Alcance') != 'SIMULACION_SIN_APLICAR'
                or evidence.get('Miembros_Derechos_Leidos') != list(members)
                or evidence['Izquierda'] != proof.endpoint(a) or evidence['Derecha'] != proof.endpoint(b)
                or b['ID_Intervencion'] != members[0] or a['ID_Padre'] != b['ID_Padre']
                or a['Actor_Final'] != b['Actor_Final'] or a['Actor_Final'] == CONSEJO
                or a['Fuente_Actor'] != 'CONTEXTO_REVISADO' or a['ID_Ancla_Actor']
                or b['Fuente_Actor'] not in EXPLICIT or b['ID_Ancla_Actor'] != b['ID_Intervencion']
                or a.get('Motivos_Revision') or b.get('Motivos_Revision')
                or a.get('Tipo_Acta') or b.get('Tipo_Acta')
                or boundary(a['Texto']) or SECTION.search(normalize(b['Texto']))):
            raise ValueError('Propuesta no compatible con extremos/anclas/barreras')
        left_group = [x for x in rows if x['ID_Turno'] == a['ID_Turno']]
        right_group = [x for x in rows if x['ID_Turno'] == b['ID_Turno']]
        if ([x['ID_Intervencion'] for x in left_group] != [key]
                or tuple(x['ID_Intervencion'] for x in right_group) != members
                or any(x['Actor_Final'] != a['Actor_Final'] or x.get('Motivos_Revision')
                       or x.get('Tipo_Acta') or str(x['Fecha'])[:10] != str(a['Fecha'])[:10]
                       for x in right_group)):
            raise ValueError('La propuesta afectaría miembros no revisados del grupo')
    return positions


def group_signature(rows):
    # Foto explícita de esta base para poder comparar los ID publicados y simulados.
    return proof.sha(json.dumps([(x['ID_Intervencion'], x['ID_Turno']) for x in rows], ensure_ascii=False))


def simulate(rows, package):
    positions = validate(rows, package)
    changes, mapping = [], {}
    for key, members in PROPOSALS.items():
        a = rows[positions[key]]
        b = rows[positions[members[0]]]
        mapping[b['ID_Turno']] = a['ID_Turno']
    for row in rows:
        if row['ID_Turno'] in mapping:
            changes.append(dict(ID_Intervencion=row['ID_Intervencion'], Actor=row['Actor_Final'],
                                Grupo_Publicado=row['ID_Turno'], Grupo_Solo_Escenario=mapping[row['ID_Turno']],
                                Estado='SIMULADO_NO_APLICADO'))
    before = {x['ID_Turno'] for x in rows}
    after = {mapping.get(x['ID_Turno'], x['ID_Turno']) for x in rows}
    summary = dict(Pares_Inventariados=len(inventory(rows)), Padres_Completos_Leidos=len(package['Padres']),
                   Caracteres_Origen_Leidos=sum(len(e['Texto_Padre']) for e in package['Padres'].values()),
                   Propuestas_Simuladas=2, Filas_Con_Grupo_Distinto_Solo_En_Escenario=len(changes),
                   Grupos_Publicados=len(before), Grupos_Solo_Escenario=len(after),
                   Enlaces_Aplicados=0, Cortes_Aplicados=0, Alertas_Cerradas=0,
                   Limite='Escenario de agrupación, no entrega productiva. Conserva todos los textos, actores, '
                          'roles, métodos, anclas y alertas; no aprueba los otros pares inventariados.')
    return changes, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=proof.ROOT / 'data/processed/consolidado_base_referencia.xlsx')
    parser.add_argument('--revisiones', type=Path, required=True)
    parser.add_argument('--salida', type=Path, required=True)
    args = parser.parse_args()
    output = proof.safe_output(args.salida, args.base)
    names = ['inventario.csv', 'decisiones.csv', 'cambios_solo_escenario.csv', 'resumen.json']
    for name in names:
        dest = output / name
        if dest.exists() or dest.resolve() in {args.base.resolve(), args.revisiones.resolve()}:
            raise ValueError('Salida existente o coincidente con entrada')
    package = json.loads(args.revisiones.read_text(encoding='utf-8'))
    rows = proof.read_rows(args.base)
    changes, summary = simulate(rows, package)
    decisions = [{**e, 'Reservas': ' | '.join(e['Reservas'])} for e in package['Decisiones']]
    for name, data in zip(names[:3], [inventory(rows), decisions, changes]):
        with (output / name).open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(data[0]), quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(data)
    summary.update(SHA256_Base=hashlib.sha256(args.base.read_bytes()).hexdigest(),
                   SHA256_Revisiones=hashlib.sha256(args.revisiones.read_bytes()).hexdigest())
    (output / names[3]).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
