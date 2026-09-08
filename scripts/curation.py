"""Revisiones documentadas, versionadas y ancladas al texto de origen.

No son verificación contra el PDF ni modifican la asistencia. Si cambian las
entradas o las citas ya no existen, la construcción falla antes de publicarse.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLE_REVIEWS = ROOT/'data/curation/revisiones_roles.json'
REVIEW_SOURCES = {'TEXTO_EXPLICITO_REVISADO','CONTEXTO_SESION_REVISADO'}


def normalize_quote(text):
    return re.sub(r'\s+',' ',str(text)).strip()


def text_hash(text):
    return hashlib.sha256(str(text).encode('utf-8')).hexdigest()


def load_role_reviews(raw_by_id, path=ROLE_REVIEWS):
    entries = json.loads(Path(path).read_text(encoding='utf-8'))
    result = {}
    ids = set()
    for entry in entries:
        rid = entry['ID_Padre']
        actor = entry['Actor']
        key = (rid, actor)
        if entry['Revision_ID'] in ids or key in result:
            raise ValueError('Revisión de cargo duplicada')
        ids.add(entry['Revision_ID'])
        target = raw_by_id.get(rid)
        if not target or str(target['Fecha'])[:10] != entry['Fecha']:
            raise ValueError(f'{entry["Revision_ID"]}: padre/fecha no coinciden')
        if text_hash(target['Texto']) != entry['SHA256_Texto_Padre']:
            raise ValueError(f'{entry["Revision_ID"]}: cambió el texto de origen; revisar de nuevo')
        if not actor or not entry['Rol'] or entry['Fuente_Rol'] not in REVIEW_SOURCES:
            raise ValueError('Revisión de cargo incompleta o fuente inválida')
        if not entry.get('Evidencia') or not entry.get('Justificacion'):
            raise ValueError('Revisión sin evidencia/justificación')
        for ev in entry['Evidencia']:
            evidence_row = raw_by_id.get(ev['ID_Padre'])
            if not evidence_row or str(evidence_row['Fecha'])[:10] != entry['Fecha']:
                raise ValueError('La evidencia no pertenece a la misma sesión')
            quote = normalize_quote(ev['Cita'])
            if not quote or quote not in normalize_quote(evidence_row['Texto']):
                raise ValueError('La cita de evidencia no existe en la fuente')
            if normalize_quote(entry['Rol']) not in quote or normalize_quote(ev['Nombre_en_Cita']) not in quote:
                raise ValueError('La cita debe incluir cargo y nombre explícitos')
        if entry['Fuente_Rol'] == 'TEXTO_EXPLICITO_REVISADO' and not any(ev['ID_Padre']==rid for ev in entry['Evidencia']):
            raise ValueError('La evidencia directa debe estar en el propio padre')
        result[key] = entry
    return result


SPEAKER_REVIEWS = ROOT/'data/curation/revisiones_hablantes.json'
SPEAKER_REVIEW_SOURCE = 'CONTEXTO_REVISADO'


def load_speaker_reviews(raw_by_id, path=SPEAKER_REVIEWS):
    """Intervalos revisados explícitamente; no generaliza 'expositor' a otras filas."""
    entries = json.loads(Path(path).read_text(encoding='utf-8'))
    result, ids = {}, set()
    for entry in entries:
        rid = entry['ID_Padre']
        target = raw_by_id.get(rid)
        if rid in result or entry['Revision_ID'] in ids:
            raise ValueError('Revisión de hablante duplicada')
        ids.add(entry['Revision_ID'])
        if not target or str(target['Fecha'])[:10] != entry['Fecha']:
            raise ValueError('Revisión de hablante: padre/fecha no coinciden')
        text = str(target['Texto'])
        if text_hash(text) != entry['SHA256_Texto_Padre']:
            raise ValueError('Revisión de hablante: cambió el texto de origen')
        if entry.get('Tipo_Limite') not in (None, 'COORDINACION_Y_EXPLICITA', 'CONCATENACION_EXPLICITA_REVISADA', 'RESPUESTA_A_LO_QUE_EXPLICITA', 'GERUNDIO_SENALANDO_EXPLICITO', 'CESION_RELATIVA_EXPLICITA', 'CESION_AGRADECIMIENTO_RELATIVO_EXPLICITO'):
            raise ValueError('Tipo de límite revisado inválido')
        start, end = entry['Inicio'], entry['Fin']
        if not 0 <= start < end <= len(text) or not text[start:end].startswith(entry['Cita_Inicio']):
            raise ValueError('Intervalo de hablante inválido')
        if not entry['Actor'] or not entry['Justificacion'] or not entry['Evidencia']:
            raise ValueError('Revisión de hablante sin evidencia')
        for ev in entry['Evidencia']:
            row = raw_by_id.get(ev['ID_Padre'])
            if not row or str(row['Fecha'])[:10] != entry['Fecha']:
                raise ValueError('Evidencia de hablante fuera de sesión')
            if not ev['Cita'] or normalize_quote(ev['Cita']) not in normalize_quote(row['Texto']):
                raise ValueError('Cita de hablante inexistente')
        result[rid] = {**entry, '_Texto_Intervalo':text[start:end]}
    return result


def validate_speaker_reviews(rows, reviews):
    """F1: el intervalo revisado debe sobrevivir completo y con su actor/documento."""
    errors = []
    compact = lambda t: re.sub(r'\s+', '', t)
    for row in rows:
        if row['Fuente_Actor'] == SPEAKER_REVIEW_SOURCE:
            entry = reviews.get(row['ID_Padre'])
            if not entry or row['Actor_Final'] != entry['Actor'] or not compact(row['Texto']).startswith(compact(entry['Cita_Inicio'])):
                errors.append(f'ID {row["ID"]}: hablante revisado sin evidencia aplicable')
    for rid, entry in reviews.items():
        group = [r for r in rows if r['ID_Padre']==rid]
        matches = [i for i,r in enumerate(group) if r['Fuente_Actor']==SPEAKER_REVIEW_SOURCE]
        if len(matches) != 1:
            errors.append(f'{entry["Revision_ID"]}: falta inicio revisado único')
            continue
        expected = compact(entry['_Texto_Intervalo'])
        actual = ''
        for row in group[matches[0]:]:
            if row['Actor_Final'] != entry['Actor']:
                break
            actual += compact(row['Texto'])
            if len(actual) >= len(expected):
                break
        if actual != expected:
            errors.append(f'{entry["Revision_ID"]}: intervalo revisado alterado')
    return errors
