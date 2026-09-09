"""Seguimiento acotado de cinco fronteras acta/discurso; no cambia el pipeline.

No amplía el validador de respuestas personales ni detecta turnos por gerundios,
cesiones, asistencia o proximidad. Aplica fichas leídas, con padre y vecinos
vigentes, a cinco límites identificados del diagnóstico de 2026-09-08.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import revisar_cola_comas as personal

SCOPE = 'COMAS_ACTA_DISCURSO_20260908'
STATE = 'LIMITE_INSTITUCIONAL_REVISADO_SIN_CIERRE'
COUNCIL = 'Consejo del Banco Central de Chile'
# Inventario cerrado de esta revisión, no patrones generalizables de atribución.
CASES = {
    'RPM-2006-03-16:601:1': (
        'INTERRUPCION_REINICIO_EXPOSICION', 'ACTA_INSTITUCIONAL',
        'Pablo García Silva', 'El señor Presidente interrumpe la sesión', 'quien señala'),
    'RPM-2008-06-10:1901:2': (
        'REANUDACION_CESION', 'META_SESION', 'José De Gregorio Rebeco',
        'Siendo las 16:00 horas', 'El Presidente señor José De Gregorio ofrece la palabra'),
    'RPM-2008-10-09:2112:3': (
        'REANUDACION_AGENDA', 'META_SESION', 'José De Gregorio Rebeco',
        'Siendo las 16;00 horas', 'El Presidente señor José De Gregorio fija la Reunión'),
    'RPM-2009-12-15:2803:1': (
        'ASISTENCIA_AGENDA', 'ACTA_CABECERA', 'José De Gregorio Rebeco',
        'ACTA CORRESPONDIENTE', 'El Presidente, señor José De Gregorio, junto con dar inicio'),
    'RPM-2012-12-13:5252:2': (
        'REANUDACION_PRESIDENCIA_COMENTARIO', 'META_SESION', 'Manuel Marfán Lewis',
        'Siendo las 16:30 horas', 'haciendo presente que el Presidente señor Rodrigo Vergara'),
}


def neighbor_evidence(row):
    return dict(Intervalo=personal.endpoint(row),
                SHA256_Fila=personal.parent_signature([row]),
                Lectura='INTERVALO_VECINO_COMPLETO')


def local_links(rows):
    """Todos los pares locales: detecta también fusiones a través del acta.

    No congela la numeración global de los turnos, sólo sus equivalencias.
    """
    return [dict(Izquierda=a['ID_Intervencion'], Derecha=b['ID_Intervencion'],
                 Mismo_Turno=a['ID_Turno'] == b['ID_Turno'])
            for i, a in enumerate(rows) for b in rows[i + 1:]]


def validate_institutional_reviews(rows, package):
    if (not isinstance(package, dict) or package.get('Version') != 1
            or package.get('Alcance') != SCOPE
            or not isinstance(package.get('Revisiones'), list)
            or not isinstance(package.get('Padres'), dict)):
        raise ValueError('Paquete institucional incompatible')
    personal.check_sources(package)
    locations = {r['ID_Intervencion']: i for i, r in enumerate(rows)}
    if len(locations) != len(rows):
        raise ValueError('Intervalos duplicados en la base')
    candidates = {c['ID_Intervencion']: c for c in personal.diagnose(rows)}
    result, seen = {}, set()
    for e in package['Revisiones']:
        try:
            key = e['Izquierda']['ID_Intervencion']
            if key not in CASES:
                raise ValueError('Límite fuera del inventario institucional acotado')
            if not e['Revision_ID'] or e['Revision_ID'] in seen or key in result:
                raise ValueError('Ficha o límite institucional duplicado')
            criterion, act_type, actor, start_left, start_right = CASES[key]
            case = candidates.get(key)
            if (not case or case['Categoria'] != personal.CATEGORY
                    or not case['Solo_Este_Motivo'] or e['Estado'] != STATE
                    or e['Criterio'] != criterion or not e['Justificacion']
                    or not e['Limitacion'] or not isinstance(e['Reservas'], list)):
                raise ValueError('Decisión o criterio institucional incompatible')
            i = locations[key]
            left, right = rows[i:i + 2]
            p = e['ID_Padre']
            if (left['ID_Padre'] != p or right['ID_Padre'] != p
                    or str(left['Fecha'])[:10] != e['Fecha']
                    or str(right['Fecha'])[:10] != e['Fecha']
                    or left['Actor_Final'] != COUNCIL or left['Fuente_Actor'] != 'ACTA/META'
                    or left['Tipo_Acta'] != act_type or right['Actor_Final'] != actor
                    or right['Tipo_Acta'] is not None or right['Fuente_Actor'] == 'ACTA/META'
                    or not left['Texto'].startswith(start_left)
                    or not right['Texto'].startswith(start_right)):
                raise ValueError('Frontera acta/discurso, actor o fecha modificados')
            if (e['Izquierda'] != personal.endpoint(left)
                    or e['Derecha'] != personal.endpoint(right)):
                raise ValueError('Extremo institucional modificado')
            indices = [j for j, r in enumerate(rows) if r['ID_Padre'] == p]
            lo, hi = indices[0], indices[-1]
            if indices != list(range(lo, hi + 1)) or lo == 0 or hi + 1 >= len(rows):
                raise ValueError('Padre discontinuo o vecinos ausentes')
            pr = rows[lo:hi + 1]
            evidence = package['Padres'][str(p)]
            if (evidence['Fecha'] != e['Fecha'] or evidence['Lectura'] != 'PADRE_COMPLETO'
                    or evidence['SHA256_Texto_Padre'] != personal.sha(evidence['Texto_Padre'])
                    or evidence['SHA256_Particion'] != personal.parent_signature(pr)
                    or personal.compact(evidence['Texto_Padre']) != ''.join(
                        personal.compact(r['Texto']) for r in pr)):
                raise ValueError('Texto o partición del padre modificado')
            if (evidence['Vecino_Anterior'] != neighbor_evidence(rows[lo - 1])
                    or evidence['Vecino_Siguiente'] != neighbor_evidence(rows[hi + 1])
                    or evidence['Enlaces_Locales'] != local_links(rows[lo - 1:hi + 2])):
                raise ValueError('Vecinos o relaciones locales modificados')
            if left['ID_Turno'] == right['ID_Turno']:
                raise ValueError('Acta absorbida por el turno personal')
            result[key] = e
            seen.add(e['Revision_ID'])
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError('Ficha institucional incompleta') from exc
    if set(package['Padres']) != {str(e['ID_Padre']) for e in result.values()}:
        raise ValueError('Evidencia institucional sobrante o ausente')
    return result


def build_combined_queue(rows, personal_packages, institutional_package):
    # Ningún lote puede suplir las fuentes o la evidencia omitidas por otro.
    for package in personal_packages:
        personal.check_sources(package)
        personal.validate_reviews(rows, package)
    combined = personal.combine_packages(personal_packages)
    institutional = validate_institutional_reviews(rows, institutional_package)
    for name, digest in institutional_package['SHA256_Fuentes'].items():
        if name in combined['SHA256_Fuentes'] and digest != combined['SHA256_Fuentes'][name]:
            raise ValueError('Fuentes incompatibles entre tipos de ficha')
    ids = {e['Revision_ID'] for e in combined['Revisiones']}
    if ids & {e['Revision_ID'] for e in institutional.values()}:
        raise ValueError('Revision_ID duplicado entre tipos de ficha')
    queue = personal.build_queue(rows, combined)
    for q in queue:
        e = institutional.get(q['ID_Intervencion'])
        q['Clase_Ficha'] = 'PERSONAL' if q['Estado_Lectura'] == personal.STATE else 'SIN_FICHA'
        if e:
            if q['Estado_Lectura'] != personal.PENDING:
                raise ValueError('Límite duplicado entre tipos de ficha')
            q.update(Estado_Lectura=STATE, Revision_ID=e['Revision_ID'],
                     Reservas=' | '.join(e['Reservas']), Clase_Ficha='ACTA_DISCURSO')
    return queue


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=personal.ROOT / 'data/processed/consolidado_base_referencia.xlsx')
    parser.add_argument('--personales', type=Path, action='append', required=True)
    parser.add_argument('--institucionales', type=Path, required=True)
    parser.add_argument('--salida', type=Path, required=True)
    args = parser.parse_args()
    output = personal.safe_output(args.salida, args.base)
    names = ('cola_comas.csv', 'comas_sin_ficha.csv', 'resumen.json')
    # Este cierre de seguimiento no sobrescribe entradas ni exportaciones previas.
    inputs = {p.resolve() for p in [args.base, args.institucionales, *args.personales]}
    for name in names:
        dest = output / name
        if dest.resolve() in inputs or dest.exists():
            raise ValueError('La salida ya existe o coincide con una entrada: ' + str(dest))
    packages = [json.loads(p.read_text(encoding='utf-8')) for p in args.personales]
    institutional = json.loads(args.institucionales.read_text(encoding='utf-8'))
    rows = personal.read_rows(args.base)
    queue = build_combined_queue(rows, packages, institutional)
    pending = [q for q in queue if q['Estado_Lectura'] == personal.PENDING]
    for name, data in [('cola_comas.csv', queue), ('comas_sin_ficha.csv', pending)]:
        with (output / name).open('w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=list(queue[0]), quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(data)
    summary = dict(
        Limites_Subgrupo=len(queue), Limites_Con_Ficha=len(queue) - len(pending),
        Limites_Personales_Con_Ficha=sum(q['Clase_Ficha'] == 'PERSONAL' for q in queue),
        Limites_Institucionales_Con_Ficha=sum(q['Clase_Ficha'] == 'ACTA_DISCURSO' for q in queue),
        Limites_Sin_Ficha=len(pending),
        Padres_Con_Ficha=len({q['ID_Padre'] for q in queue if q['Clase_Ficha'] != 'SIN_FICHA'}),
        Alertas_Cerradas=0, Lotes_Personales=len(packages),
        SHA256_Base=hashlib.sha256(args.base.read_bytes()).hexdigest(),
        SHA256_Lotes={str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in [*args.personales, args.institucionales]},
        Limite='Registro de lectura: no cierre de alertas, certificación global o nuevo corte/enlace. '
               'Las fichas acta/discurso son independientes del validador personal.')
    (output / 'resumen.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
