"""Tres comas con motivos adicionales: límite, identidad y modalidad separados.

Registro acotado fuera de la subcola de167. No altera datos ni amplía los dos
validadores previos. Las reservas permanecen abiertas incluso con límite leído.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import revisar_cola_comas as base
from revisar_comas_institucionales import neighbor_evidence, local_links

SCOPE = 'COMAS_CON_MOTIVOS_ADICIONALES_20260908'
STATE = 'LIMITE_REVISADO_CON_RESERVA_ABIERTA'
CASES = {
    'RPM-2009-08-13:2680:2': dict(
        Motivo='TEXTO_DANADO_POR_COTEJAR', Reserva='HORA_Y_NUMERACION_PENDIENTES',
        Naturaleza='ACTA_A_CESION_PERSONAL', Identidad='SIN_NUEVA_RESOLUCION_DE_IDENTIDAD',
        Control=2656),
    'RPM-2009-11-12:2779:2': dict(
        Motivo='FRAGMENTO_BREVE', Reserva='MODALIDAD_DEL_ASENTIMIENTO_NO_DETERMINADA',
        Naturaleza='ASENTIMIENTO_NARRADO_SIN_PALABRAS_TRANSCRITAS',
        Identidad='SIN_NUEVA_RESOLUCION_DE_IDENTIDAD', Control=None),
    'RPM-2010-02-11:2957:2': dict(
        Motivo='NOMBRE_EN_DISCURSO_POR_VERIFICAR', Reserva='NOMBRE_LITERAL_PENDIENTE_DE_COTEJO',
        Naturaleza='PREGUNTA_Y_RESPUESTA_DIFERENCIADAS',
        Identidad='ATRIBUCION_LOCAL_PROVISIONAL', Control=2889),
}


def validate_reviews(rows, package):
    if (not isinstance(package, dict) or package.get('Version') != 1 or package.get('Alcance') != SCOPE
            or not isinstance(package.get('Revisiones'), list)
            or not isinstance(package.get('Padres'), dict)
            or not isinstance(package.get('Controles'), dict)):
        raise ValueError('Paquete de reservas incompatible')
    base.check_sources(package)
    positions = {r['ID_Intervencion']: i for i, r in enumerate(rows)}
    if len(positions) != len(rows):
        raise ValueError('Intervalos duplicados')
    cases = {c['ID_Intervencion']: c for c in base.diagnose(rows)}
    result, ids, controls = {}, set(), set()
    for e in package['Revisiones']:
        try:
            key = e['Izquierda']['ID_Intervencion']
            if key not in CASES:
                raise ValueError('Fuera del inventario de tres reservas')
            expected = CASES[key]
            case = cases.get(key)
            if not e['Revision_ID'] or e['Revision_ID'] in ids or key in result:
                raise ValueError('Ficha duplicada')
            if (not case or case['Categoria'] != base.CATEGORY or case['Solo_Este_Motivo']
                    or case['Motivos_Adicionales'] != [expected['Motivo']]
                    or e['Estado'] != STATE or e['Estado_Limite'] != 'SEPARACION_EXISTENTE_RESPALDADA'
                    or e['Estado_Reserva'] != expected['Reserva']
                    or e['Naturaleza'] != expected['Naturaleza']
                    or e['Estado_Identidad'] != expected['Identidad']
                    or not e['Justificacion'] or not e['Limitacion']
                    or not isinstance(e['Reservas'], list) or not e['Reservas']
                    or not isinstance(e['Siguiente_Accion'], str) or not e['Siguiente_Accion']):
                raise ValueError('Motivos, decisión o reserva abierta incompatibles')
            i = positions[key]
            left, right = rows[i:i + 2]
            p = e['ID_Padre']
            if (left['ID_Padre'] != p or right['ID_Padre'] != p
                    or str(left['Fecha'])[:10] != e['Fecha'] or str(right['Fecha'])[:10] != e['Fecha']
                    or e['Izquierda'] != base.endpoint(left) or e['Derecha'] != base.endpoint(right)
                    or e['Motivos_Originales'] != left['Motivos_Revision']):
                raise ValueError('Extremo, fecha o motivos originales modificados')
            indices = [j for j, r in enumerate(rows) if r['ID_Padre'] == p]
            lo, hi = indices[0], indices[-1]
            if lo == 0 or hi + 1 >= len(rows) or indices != list(range(lo, hi + 1)):
                raise ValueError('Padre discontinuo o vecinos ausentes')
            evidence = package['Padres'][str(p)]
            validate_parent(rows[lo:hi + 1], evidence, e['Fecha'])
            if (evidence['Vecino_Anterior'] != neighbor_evidence(rows[lo - 1])
                    or evidence['Vecino_Siguiente'] != neighbor_evidence(rows[hi + 1])
                    or evidence['Enlaces_Locales'] != local_links(rows[lo - 1:hi + 2])):
                raise ValueError('Vecinos o enlaces modificados')
            control = expected['Control']
            if control is not None:
                controls.add(str(control))
                cr = [r for r in rows if r['ID_Padre'] == control]
                validate_parent(cr, package['Controles'][str(control)], e['Fecha'])
            if left['ID_Turno'] == right['ID_Turno']:
                raise ValueError('Fusión del límite revisado')
            result[key] = e
            ids.add(e['Revision_ID'])
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError('Evidencia de reserva incompleta') from exc
    if (set(package['Padres']) != {str(e['ID_Padre']) for e in result.values()}
            or set(package['Controles']) != controls):
        raise ValueError('Padres o controles sobrantes/ausentes')
    validate_previous(package, {e['ID_Padre'] for e in result.values()})
    return result


def validate_previous(package, parents):
    """Contrasta los antecedentes citados, sin convertirlos en nuevas decisiones."""
    expected = {
        2680: {'HAB-20260908-L24-2680-257', 'ALERTA-20260908-L24-2680'},
        2779: {'HAB-20260907-2779'},
        2957: {'HAB-20260908-L18-2957-1', 'HAB-20260908-L18-2957-2', 'ALERTA-20260908-L18-2957'},
    }
    wanted = set().union(*(expected[p] for p in parents))
    refs = package.get('Antecedentes')
    if not isinstance(refs, list):
        raise ValueError('Faltan antecedentes')
    seen, loaded = set(), {}

    def records(obj):
        if isinstance(obj, dict):
            if 'Revision_ID' in obj:
                yield obj
            for value in obj.values():
                yield from records(value)
        elif isinstance(obj, list):
            for value in obj:
                yield from records(value)

    for ref in refs:
        try:
            path, rid = ref['Fuente'], ref['Revision_ID']
            if (path not in {'data/curation/revisiones_hablantes.json', 'data/curation/alertas_contextuales.json'}
                    or path not in package['SHA256_Fuentes'] or rid in seen or rid not in wanted):
                raise ValueError('Antecedente fuera de alcance o duplicado')
            if path not in loaded:
                loaded[path] = {x['Revision_ID']: x for x in records(
                    json.loads((base.ROOT / path).read_text(encoding='utf-8')))}
            original = loaded[path][rid]
            if (ref['ID_Padre'] != original['ID_Padre']
                    or ref['SHA256_Registro'] != base.sha(json.dumps(original, ensure_ascii=False, sort_keys=True))
                    or ref['Justificacion_Anterior'] != original['Justificacion']):
                raise ValueError('Antecedente modificado')
            seen.add(rid)
        except (KeyError, TypeError) as exc:
            raise ValueError('Antecedente incompleto') from exc
    if seen != wanted:
        raise ValueError('Antecedentes ausentes')


def validate_parent(rows, evidence, date):
    if (not rows or evidence['Fecha'] != date or evidence['Lectura'] != 'PADRE_COMPLETO'
            or any(str(r['Fecha'])[:10] != date for r in rows)
            or evidence['SHA256_Texto_Padre'] != base.sha(evidence['Texto_Padre'])
            or evidence['SHA256_Particion'] != base.parent_signature(rows)
            or base.compact(evidence['Texto_Padre']) != ''.join(base.compact(r['Texto']) for r in rows)):
        raise ValueError('Texto o partición modificados')


def build_risk_table(rows, package):
    reviews = validate_reviews(rows, package)
    return [dict(ID_Intervencion=key, ID_Padre=e['ID_Padre'], Fecha=e['Fecha'],
                 Actor_Izquierda_Actual=e['Izquierda']['Actor'],
                 Actor_Derecha_Actual=e['Derecha']['Actor'], Motivos_Originales=e['Motivos_Originales'],
                 Estado_Limite=e['Estado_Limite'], Estado_Identidad=e['Estado_Identidad'],
                 Naturaleza=e['Naturaleza'], Estado_Reserva=e['Estado_Reserva'],
                 Siguiente_Accion=e['Siguiente_Accion'], Reservas=' | '.join(e['Reservas']))
            for key, e in reviews.items()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=base.ROOT / 'data/processed/consolidado_base_referencia.xlsx')
    parser.add_argument('--revisiones', type=Path, required=True)
    parser.add_argument('--salida', type=Path, required=True)
    args = parser.parse_args()
    output = base.safe_output(args.salida, args.base)
    names = ('riesgos_abiertos.csv', 'resumen.json')
    for name in names:
        dest = output / name
        if dest.exists() or dest.resolve() in {args.base.resolve(), args.revisiones.resolve()}:
            raise ValueError('Salida existente o coincidente con entrada')
    package = json.loads(args.revisiones.read_text(encoding='utf-8'))
    table = build_risk_table(base.read_rows(args.base), package)
    if not table:
        raise ValueError('No hay fichas de reserva para exportar')
    with (output / names[0]).open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(table[0]), quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(table)
    summary = dict(Casos_Con_Ficha=len(table), Reservas_Abiertas=len(table),
                   Identidades_Provisionales=sum(e['Estado_Identidad'] == 'ATRIBUCION_LOCAL_PROVISIONAL' for e in table),
                   Asentimientos_Sin_Palabras_Transcritas=sum(e['Naturaleza'] == 'ASENTIMIENTO_NARRADO_SIN_PALABRAS_TRANSCRITAS' for e in table),
                   Alertas_Cerradas=0, Nuevos_Cortes=0, Nuevos_Enlaces=0, Reasignaciones=0,
                   SHA256_Base=hashlib.sha256(args.base.read_bytes()).hexdigest(),
                   SHA256_Revisiones=hashlib.sha256(args.revisiones.read_bytes()).hexdigest(),
                   Limite='Tres lecturas con reservas abiertas, fuera de la subcola de167; no tres identidades confirmadas, palabras recuperadas o correcciones.')
    (output / names[1]).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
