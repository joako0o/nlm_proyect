"""Pruebas intrapadre v1; opt-in, sin ampliar las pruebas entre padres.

Dos pares leídos. Un registro distinto requiere otra revisión/versionado, no
una heurística de mismo actor o una promoción global de CONTEXTO_REVISADO.
"""
import json
from pathlib import Path
from curation import text_hash

PATH = Path(__file__).resolve().parents[1] / 'data/curation/continuidades_intrapadre_v1.json'
RELATION = 'CONTINUIDAD_INTRAPADRE_REVISADA'
ALLOWED = {
    ('RPM-2009-11-12:2796:2', 'RPM-2009-11-12:2796:3'): (2796, '2009-11-12', 'Enrique Marshall Rivera'),
    ('RPM-2010-03-18:3012:2', 'RPM-2010-03-18:3012:3'): (3012, '2010-03-18', 'Beltrán de Ramón Acevedo'),
}
EXPLICIT = {'SUJETO_NOMBRE', 'SUJETO_ROL_NOMBRE', 'SUJETO_ROL_SESION'}


def compact(text):
    return ''.join(text.split())


def load_intrapara_links(raw, path=PATH):
    # El API histórico sigue cerrado exactamente a v1.
    return _load_bounded_links(raw, path, 1, 'CONTINUIDAD_INTRAPADRE_V1', ALLOWED)


def _load_bounded_links(raw, path, version, scope, allowed):
    package = json.loads(Path(path).read_text(encoding='utf-8'))
    if (not isinstance(package, dict) or type(package.get('Version')) is not int or package.get('Version') != version
            or package.get('Alcance') != scope
            or not isinstance(package.get('Revisiones'), list)):
        raise ValueError('Paquete intrapadre incompatible')
    result, ids = {}, set()
    for e in package['Revisiones']:
        try:
            left, right = e['Anterior'], e['Siguiente']
            key = (left['ID_Intervencion'], right['ID_Intervencion'])
            if key not in allowed or key in result or not e['Revision_ID'] or e['Revision_ID'] in ids:
                raise ValueError('Par intrapadre fuera de alcance o duplicado')
            p, date, actor = allowed[key]
            source = raw[p]
            if (e['ID_Padre'] != p or e['Fecha'] != date or e['Actor'] != actor
                    or str(source['Fecha'])[:10] != date or e['Texto_Padre'] != source['Texto']
                    or text_hash(source['Texto']) != e['SHA256_Texto_Padre']
                    or not e['Justificacion'] or not e['Limitacion']
                    or left['Fuente_Actor'] != 'CONTEXTO_REVISADO'
                    or right['Fuente_Actor'] not in EXPLICIT):
                raise ValueError('Fuente o atribución intrapadre incompatible')
            for side in [left, right]:
                a, z = side['Inicio'], side['Fin']
                if (type(a) is not int or type(z) is not int or not 0 <= a < z <= len(source['Texto'])
                        or source['Texto'][a:z] != side['Texto']):
                    raise ValueError('Intervalo intrapadre modificado')
            if (left['Fin'] > right['Inicio'] or compact(source['Texto'][left['Fin']:right['Inicio']])
                    or e['Evidencia'] != [left['Texto'], right['Texto']]):
                raise ValueError('Intervalos no contiguos o evidencia incompleta')
            result[key] = e
            ids.add(e['Revision_ID'])
        except (KeyError, TypeError) as exc:
            raise ValueError('Prueba intrapadre incompleta') from exc
    if set(result) != set(allowed):
        raise ValueError('La versión intrapadre requiere todos sus pares exactos')
    return result


def matching_intrapara(prev, row, reviews):
    if not prev:
        return None
    e = (reviews or {}).get((prev.get('ID_Intervencion'), row.get('ID_Intervencion')))
    if not e:
        return None
    for r, side in [(prev, e['Anterior']), (row, e['Siguiente'])]:
        if (r.get('ID_Padre') != e['ID_Padre'] or str(r['Fecha'])[:10] != e['Fecha']
                or r['Actor_Final'] != e['Actor'] or r['Fuente_Actor'] != side['Fuente_Actor']
                or r['Texto'] != side['Texto']
                or r.get('Tipo_Acta') or r.get('Motivos_Revision')):
            return None
    if prev.get('ID_Ancla_Actor'):
        return None
    return e


def validate_intrapara_links(rows, reviews):
    errors, seen, previous = [], set(), None
    for row in rows:
        e = matching_intrapara(previous, row, reviews)
        if e:
            key = (previous['ID_Intervencion'], row['ID_Intervencion'])
            if key in seen:
                errors.append('Prueba intrapadre repetida')
            seen.add(key)
            if (row.get('Relacion_Turno') != RELATION or row.get('ID_Turno') != previous.get('ID_Turno')
                    or row.get('ID_Antecedente_Continuidad') != previous['ID_Intervencion']
                    or previous.get('ID_Ancla_Actor')
                    or row.get('ID_Ancla_Actor') != row['ID_Intervencion']):
                errors.append(e['Revision_ID'] + ': enlace/antecedente/ancla inválidos')
        elif row.get('Relacion_Turno') == RELATION:
            errors.append('Continuidad intrapadre sin prueba aplicable')
        previous = row
    if seen != set(reviews or {}):
        errors.append('Faltan los extremos intrapadre exactos y contiguos')
    return errors
