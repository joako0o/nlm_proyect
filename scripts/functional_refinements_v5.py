"""Refinamiento funcional v5: veintinueve constancias de Vergara, sin regla global.

Extiende a veintinueve padres el criterio que funcional-v4 aplicó a 4788, 4849 y
4899, sin tocar ese registro ni ampliar su alcance. Cada corte está respaldado por
la lectura completa del lote8 y por el antecedente nominal del padre anterior.

No se cambia ningún hablante: Rodrigo Vergara conserva la atribución del aporte
personal y de la constancia, aunque el contenido de ésta sea institucional.
"""
import hashlib
import json
from pathlib import Path

from diagnosticar_finales import read_rows

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/curation/refinamiento_funcional_v5.json'
BASE = ROOT / 'data/releases/continuidad_procedimental_v6/consolidado_base_referencia.xlsx'
BASE_SHA = '1dfce989aa1ded2fb4bc99557750c48bd3d01ee5a690708044a659065e45c7c4'
READINGS = ROOT / 'docs/continuidad_lote8_2026-09-09/lecturas.json'
V4_PATH = ROOT / 'data/curation/refinamiento_funcional_v4.json'
V4_SHA = 'd636f4a6f33bdef932956ca13834f247daf6cafd5d54bcb50440283a701220b8'
ACTOR = 'Rodrigo Vergara Montes'

PARENTS = (4973, 5039, 5159, 5221, 5267, 5330, 5398, 5453, 5514, 5566, 5634, 5699,
           5752, 5812, 5857, 5903, 5962, 6006, 6055, 6179, 6234, 6340, 6438, 6484,
           6517, 6547, 6754, 6806, 6863)


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_readings(rows, readings, raw):
    """Revalida la lectura lote8 contra la entrega v6 y el origen, sin confiar en el JSON.

    El antecedente debe ser la ÚLTIMA fila del padre anterior: si otra voz se
    intercalara, el aporte personal no continuaría una intervención en curso.
    """
    by_id = {r['ID_Intervencion']: r for r in rows}
    by_parent = {}
    for r in rows:
        by_parent.setdefault(r['ID_Padre'], []).append(r)
    for rid, case in readings['Casos'].items():
        p = case['ID_Padre']
        row = by_id[rid]
        siblings = by_parent[p]
        previous = by_parent[p - 1][-1]
        if (row['Texto'] != case['Texto_Original'] or row['ID_Padre'] != p
                or row['Numero_Segmento'] != 1 or row['Actor_Final'] != ACTOR
                or row['Fuente_Actor'] != 'SUJETO_ROL_NOMBRE'
                or row['Tipo_Acta'] != 'ACUERDO_CONSEJO' or row['Motivos_Revision']
                or len(siblings) != 2):
            raise ValueError(f'{rid}: la fila v6 ya no coincide con la lectura lote8')
        padre = readings['Padres'][str(p)]
        if raw[p]['Texto'] != padre['Texto_Padre']:
            raise ValueError(f'{p}: el texto de origen cambió')
        if (padre['SHA256_Texto_Padre']
                != hashlib.sha256(raw[p]['Texto'].encode()).hexdigest()
                or case['Texto_Personal'] + case['Separador'] + case['Texto_Constancia']
                != case['Texto_Original']
                or not case['Separador'].isspace()
                or case['Corte'] != len(case['Texto_Original']) - len(case['Texto_Constancia'])
                - len(case['Separador'])):
            raise ValueError(f'{rid}: el corte ya no conserva el texto')
        if not case['Texto_Personal'].rstrip().endswith('.'):
            raise ValueError(f'{rid}: el aporte personal no cierra una oración')
        if case['ID_Anterior'] != previous['ID_Intervencion']:
            raise ValueError(f'{rid}: el antecedente ya no es la última fila del padre anterior')
        if (previous['Actor_Final'] != ACTOR or previous['Tipo_Acta']
                or previous['Motivos_Revision']
                or previous['ID_Ancla_Actor'] != previous['ID_Intervencion']):
            raise ValueError(f'{rid}: el antecedente perdió su condición de inicio explícito')
    return True


def load_refinements(raw, path=PATH):
    package = json.loads(Path(path).read_text())
    if (not isinstance(package, dict) or type(package.get('Version')) is not int
            or package['Version'] != 5 or package.get('Perfil') != 'funcional-v5'
            or not isinstance(package.get('Revisiones'), dict)
            or set(package['Revisiones']) != {str(p) for p in PARENTS}
            or package.get('SHA256_Lecturas_Lote8') != file_sha(READINGS)
            or package.get('SHA256_Base') != BASE_SHA or file_sha(BASE) != BASE_SHA
            or package.get('SHA256_Registro_Funcional_V4') != file_sha(V4_PATH)):
        raise ValueError('Refinamiento funcional v5 fuera de versión o de evidencia')
    readings = json.loads(READINGS.read_text())
    rows = read_rows(BASE)
    validate_readings(rows, readings, raw)
    by_id = {r['ID_Intervencion']: r for r in rows}
    ids = set()
    try:
        for p in PARENTS:
            entry = package['Revisiones'][str(p)]
            case = readings['Casos'][entry['ID_Fila_Original']]
            old = by_id[entry['ID_Fila_Original']]
            previous = by_id[entry['ID_Anterior']]
            sha_padre = readings['Padres'][str(p)]['SHA256_Texto_Padre']
            if (type(entry['ID_Padre']) is not int or entry['ID_Padre'] != p
                    or old['ID_Padre'] != p or old['Numero_Segmento'] != 1
                    or entry['Fecha'] != str(raw[p]['Fecha'])[:10]
                    or entry['Fecha'] != str(old['Fecha'])[:10]
                    or entry['ID_Anterior'] != case['ID_Anterior']
                    or entry['Texto_Original'] != old['Texto']
                    or entry['Actor'] != old['Actor_Final'] or entry['Actor'] != ACTOR
                    or entry['Fuente_Actor'] != old['Fuente_Actor']
                    or entry['Fuente_Actor'] != 'SUJETO_ROL_NOMBRE'
                    or entry['SHA256_Texto_Padre'] != sha_padre
                    or entry['SHA256_Texto_Padre']
                    != hashlib.sha256(raw[p]['Texto'].encode()).hexdigest()
                    or entry['Texto_Personal'] != case['Texto_Personal']
                    or entry['Separador'] != case['Separador']
                    or entry['Texto_Constancia'] != case['Texto_Constancia']
                    or entry['Texto_Personal'] + entry['Separador'] + entry['Texto_Constancia']
                    != entry['Texto_Original']
                    or not entry['Separador'].isspace()
                    or entry['Tipo_Personal'] != '' or entry['Tipo_Constancia'] != 'ACUERDO_CONSEJO'
                    or entry['Justificacion'] != case['Justificacion']
                    or entry['Limitacion'] != case['Limitacion'] or not entry['Aplicacion']
                    or entry['Revision_ID'] != f'FUNCIONAL_V5_{PARENTS.index(p) + 1:02d}_{p}'
                    or entry['Revision_ID'] in ids
                    or previous['Actor_Final'] != entry['Actor'] or previous['Tipo_Acta']
                    or previous['Motivos_Revision']
                    or previous['ID_Ancla_Actor'] != previous['ID_Intervencion']):
                raise ValueError('Extremos, fuente o decisión funcional v5 modificados')
            ids.add(entry['Revision_ID'])
    except (KeyError, TypeError) as exc:
        raise ValueError('Registro funcional v5 incompleto') from exc
    return {int(k): v for k, v in package['Revisiones'].items()}


def refine_segments(parent, segments, reviews):
    entry = (reviews or {}).get(parent)
    if not entry:
        return segments
    if (not segments or segments[0] != (entry['Texto_Original'], entry['Actor'],
                                        entry['Fuente_Actor'])
            or sum(t == entry['Texto_Original'] for t, _, _ in segments) != 1):
        raise ValueError('La partición anterior no coincide con la prueba funcional v5')
    return [(entry['Texto_Personal'], entry['Actor'], entry['Fuente_Actor']),
            (entry['Texto_Constancia'], entry['Actor'], entry['Fuente_Actor']), *segments[1:]]


def validate_refinements(rows, reviews):
    """Exige tres tramos, continuidad explícita del aporte y constancia institucional."""
    errors = []
    idx = {r['ID_Intervencion']: r for r in rows}
    for p, entry in sorted(reviews.items()):
        parts = [r for r in rows if r['ID_Padre'] == p]
        if len(parts) != 3:
            errors.append(f'{p}: falta partición funcional v5')
            continue
        a, b = parts[:2]
        previous = idx.get(entry['ID_Anterior'])
        for r, text, tipo in [(a, entry['Texto_Personal'], ''),
                              (b, entry['Texto_Constancia'], 'ACUERDO_CONSEJO')]:
            if (r['Texto'] != text or r['Actor_Final'] != entry['Actor']
                    or r['Fuente_Actor'] != entry['Fuente_Actor']
                    or str(r['Fecha'])[:10] != entry['Fecha']
                    or (r.get('Tipo_Acta') or '') != tipo):
                errors.append(f'{p}: función, texto o hablante incorrectos en v5')
        if (not previous or a.get('ID_Turno') != previous.get('ID_Turno')
                or a.get('ID_Antecedente_Continuidad') != entry['ID_Anterior']
                or a.get('Relacion_Turno') != 'CONTINUIDAD_EXPLICITA'
                or a.get('ID_Ancla_Actor') != a['ID_Intervencion']
                or b.get('ID_Turno') == a.get('ID_Turno')
                or b.get('Relacion_Turno') != 'INSTITUCIONAL'
                or b.get('ID_Ancla_Actor') or b.get('ID_Antecedente_Continuidad')):
            errors.append(f'{p}: continuidad, ancla o constancia incorrectas en v5')
    return errors


def active_refinements(raw, intrapara_profile=None):
    """Sólo se activa con el perfil intrapadre exigido y con el registro v4 intacto."""
    import os
    from intrapara_profiles import profile_name, required_intrapara
    path = os.environ.get('NLM_FUNCTIONAL_V5_REVIEWS')
    if not path:
        return {}
    intra = os.environ.get('NLM_INTRAPARA_REVIEWS')
    functional_v4 = os.environ.get('NLM_FUNCTIONAL_REVIEWS')
    intrapara_profile = required_intrapara(intrapara_profile)
    try:
        v4_sha = file_sha(functional_v4) if functional_v4 else None
    except OSError:
        v4_sha = None
    # La base de v5 es la entrega v6, construida con intrapadre-v4. Un perfil
    # intrapadre menor no reproduce esa base, así que el registro no aplica.
    if (intrapara_profile != 'intrapadre-v4' or not intra
            or profile_name(intra) != intrapara_profile
            or v4_sha != V4_SHA or file_sha(V4_PATH) != V4_SHA):
        raise ValueError(f'El refinamiento funcional v5 requiere el registro v4 y las '
                         f'pruebas intrapadre-v4, no {intrapara_profile}')
    return load_refinements(raw, path)
