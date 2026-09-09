"""Seguimiento bilateral de comas, independiente del pipeline y sin cerrar avisos.

Sólo aplica fichas con ambos intervalos y padre completo vigentes. El registro
separa trabajo de lectura de la alerta mecánica: revisar un límite no elimina
puntuación, certifica OCR ni valida otros límites del mismo padre.
"""
import argparse
import collections
import copy
import csv
import hashlib
import json
from pathlib import Path

from diagnosticar_finales import ROOT, diagnose, read_rows, safe_output, sha

STATE = 'LIMITE_REVISADO_SIN_CIERRE'
PENDING = 'SIN_FICHA_BILATERAL'
CATEGORY = 'COMA_ANTES_DE_OTRO_ACTOR_EN_PADRE'
# No depender de ID numérico o de la numeración global de grupos. Sí del texto,
# límites, actor/cargo y evidencia de continuidad de todas las filas del padre.
BOUND_FIELDS = ('ID_Intervencion', 'Fecha', 'Actor_Final', 'Rol_Final', 'Fuente_Actor',
                'Fuente_Rol', 'Tipo_Acta', 'Texto', 'Motivos_Revision',
                'ID_Antecedente_Continuidad', 'ID_Ancla_Actor', 'Relacion_Turno')


def compact(text):
    return ''.join(text.split())


def parent_signature(rows):
    values = [{k: str(r[k])[:10] if k == 'Fecha' else r[k] for k in BOUND_FIELDS} for r in rows]
    return sha(json.dumps(values, ensure_ascii=False, sort_keys=True))


def endpoint(row):
    return dict(ID_Intervencion=row['ID_Intervencion'], Actor=row['Actor_Final'],
                Fuente_Actor=row['Fuente_Actor'], SHA256_Texto=sha(row['Texto']), Texto=row['Texto'])


def validate_reviews(rows, package):
    """Devuelve fichas aplicables o falla; nunca modifica filas o registros."""
    if package.get('Version') != 1:
        raise ValueError('Versión de fichas no admitida')
    cases = {c['ID_Intervencion']: c for c in diagnose(rows)}
    locations = {r['ID_Intervencion']: i for i, r in enumerate(rows)}
    parents = collections.defaultdict(list)
    for r in rows:
        parents[r['ID_Padre']].append(r)
    seen, result = set(), {}
    if not isinstance(package.get('Revisiones'), list) or not isinstance(package.get('Padres'), dict):
        raise ValueError('Paquete de revisión incompleto')
    for e in package['Revisiones']:
        try:
            rid = e['Revision_ID']; key = e['Izquierda']['ID_Intervencion']; p = e['ID_Padre']
            case = cases.get(key)
            if not rid or rid in seen or key in result:
                raise ValueError('Ficha o límite duplicado')
            seen.add(rid)
            if (not case or case['Categoria'] != CATEGORY or not case['Solo_Este_Motivo']
                    or e['Estado'] != STATE or not e['Justificacion'] or not e['Limitacion']
                    or not isinstance(e['Reservas'], list)):
                raise ValueError('Alcance o decisión no válidos')
            pos = locations[key]
            left, right = rows[pos], rows[pos + 1]
            evidence = package['Padres'][str(p)]
            if (left['ID_Padre'] != p or right['ID_Padre'] != p
                    or str(left['Fecha'])[:10] != e['Fecha'] or str(right['Fecha'])[:10] != e['Fecha']
                    or evidence['Fecha'] != e['Fecha']):
                raise ValueError('Padre/fecha/adyacencia incompatibles')
            if any(r['Actor_Final'] == 'Consejo del Banco Central de Chile' for r in [left, right]):
                raise ValueError('Este lote sólo revisa límites personales')
            for side, row in [('Izquierda', left), ('Derecha', right)]:
                if e[side] != endpoint(row):
                    raise ValueError('Intervalo, actor, método o texto cambiado')
            if (evidence['SHA256_Texto_Padre'] != sha(evidence['Texto_Padre'])
                    or evidence['SHA256_Particion'] != parent_signature(parents[p])
                    or compact(evidence['Texto_Padre']) != ''.join(compact(r['Texto']) for r in parents[p])
                    or evidence['Lectura'] != 'PADRE_COMPLETO'):
                raise ValueError('Texto o partición del padre cambiado')
            result[key] = e
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError('Ficha incompleta o incompatible') from exc
    if set(package['Padres']) != {str(e['ID_Padre']) for e in result.values()}:
        raise ValueError('Evidencia de padres sobrante o ausente')
    return result


def build_queue(rows, package):
    reviews = validate_reviews(rows, package)
    cases = [c for c in diagnose(rows) if c['Categoria'] == CATEGORY and c['Solo_Este_Motivo']]
    queue = []
    for c in cases:
        review = reviews.get(c['ID_Intervencion'])
        queue.append(dict(ID_Intervencion=c['ID_Intervencion'], ID_Padre=c['ID_Padre'],
            Fecha=c['Fecha'], Actor_Izquierda=c['Actor'], Actor_Derecha=c['Siguiente']['Actor_Final'],
            Estado_Lectura=STATE if review else PENDING,
            Revision_ID=review['Revision_ID'] if review else '',
            Motivo_Original='FINAL_SIN_PUNTUACION',
            Reservas=' | '.join(review['Reservas']) if review else '',
            Final_Izquierda=c['Texto'][-240:], Inicio_Derecha=c['Siguiente']['Texto'][:240]))
    return queue


def check_sources(package):
    """La fuente original del registro también debe seguir vigente."""
    sources = package.get('SHA256_Fuentes')
    if not isinstance(sources, dict) or not sources:
        raise ValueError('Faltan hashes de fuentes')
    for name, expected in sources.items():
        path = (ROOT / name).resolve()
        if ROOT / 'data' not in path.parents:
            raise ValueError('Fuente fuera de data/')
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Fuente original modificada: ' + name)


def combine_packages(packages):
    """Acumula lotes sin modificar originales ni contar un límite dos veces."""
    if not packages:
        raise ValueError('Se requiere al menos un lote')
    combined = dict(Version=1, SHA256_Fuentes={}, Padres={}, Revisiones=[])
    ids, limits = set(), set()
    for package in packages:
        if not isinstance(package, dict) or package.get('Version') != 1:
            raise ValueError('Lote o versión incompatible')
        try:
            if not isinstance(package['Revisiones'], list):
                raise ValueError('Revisiones debe ser una lista')
            for name, expected in package['SHA256_Fuentes'].items():
                if name in combined['SHA256_Fuentes'] and combined['SHA256_Fuentes'][name] != expected:
                    raise ValueError('Hashes de fuente incompatibles entre lotes')
                combined['SHA256_Fuentes'][name] = expected
            for parent, evidence in package['Padres'].items():
                if parent in combined['Padres'] and combined['Padres'][parent] != evidence:
                    raise ValueError('Evidencia de padre incompatible entre lotes')
                combined['Padres'][parent] = copy.deepcopy(evidence)
            for e in package['Revisiones']:
                rid, key = e['Revision_ID'], e['Izquierda']['ID_Intervencion']
                if rid in ids or key in limits:
                    raise ValueError('Ficha o límite duplicado entre lotes')
                ids.add(rid); limits.add(key)
                combined['Revisiones'].append(copy.deepcopy(e))
        except (KeyError, TypeError, AttributeError) as exc:
            raise ValueError('Lote incompleto') from exc
    return combined


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=ROOT / 'data/processed/consolidado_base_referencia.xlsx')
    parser.add_argument('--revisiones', type=Path, action='append', required=True,
                        help='Lote de fichas; repetir la opción para acumular varios')
    parser.add_argument('--salida', type=Path, required=True)
    args = parser.parse_args()
    output = safe_output(args.salida, args.base)
    names = ('cola_comas.csv', 'comas_sin_ficha.csv', 'resumen.json')
    destinations = {(output / name).resolve() for name in names}
    if destinations & ({args.base.resolve()} | {p.resolve() for p in args.revisiones}):
        raise ValueError('No se puede sobrescribir una entrada')
    packages = [json.loads(p.read_text(encoding='utf-8')) for p in args.revisiones]
    rows = read_rows(args.base)
    # Cada lote debe ser válido por sí solo: otro no puede suplir sus omisiones.
    for item in packages:
        check_sources(item)
        validate_reviews(rows, item)
    package = combine_packages(packages)
    queue = build_queue(rows, package)
    pending = [q for q in queue if q['Estado_Lectura'] == PENDING]
    for name, data in [('cola_comas.csv', queue), ('comas_sin_ficha.csv', pending)]:
        with (output / name).open('w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=list(queue[0]) if queue else ['ID_Intervencion'], quoting=csv.QUOTE_ALL)
            writer.writeheader(); writer.writerows(data)
    summary = dict(Limites_Subgrupo=len(queue), Limites_Con_Ficha=len(queue) - len(pending),
                   Limites_Sin_Ficha=len(pending), Padres_Con_Ficha=len(package['Padres']),
                   Alertas_Cerradas=0, SHA256_Base=hashlib.sha256(args.base.read_bytes()).hexdigest(),
                   SHA256_Revisiones=(hashlib.sha256(args.revisiones[0].read_bytes()).hexdigest()
                                     if len(args.revisiones) == 1 else None),
                   SHA256_Lotes={str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in args.revisiones},
                   Lotes=len(args.revisiones),
                   Limite='Seguimiento de lectura, no cierre de alertas ni certificación de padres completos. Los límites no revisados no se validan por proximidad.')
    (output / 'resumen.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
