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


def speaker_intervals(review):
    """Interfaz compatible: un padre puede tener varios intervalos independientes."""
    if not review:
        return []
    return [{k:v for k,v in review.items() if k != 'Revisiones_Adicionales'}] + review.get('Revisiones_Adicionales', [])


def load_speaker_reviews(raw_by_id, path=SPEAKER_REVIEWS):
    entries = json.loads(Path(path).read_text(encoding='utf-8'))
    result, ids = {}, set()
    def validate(entry):
        rid = entry['ID_Padre']
        target = raw_by_id.get(rid)
        if entry['Revision_ID'] in ids:
            raise ValueError('Revisión de hablante duplicada')
        ids.add(entry['Revision_ID'])
        if not target or str(target['Fecha'])[:10] != entry['Fecha']:
            raise ValueError('Revisión de hablante: padre/fecha no coinciden')
        text = str(target['Texto'])
        if text_hash(text) != entry['SHA256_Texto_Padre']:
            raise ValueError('Revisión de hablante: cambió el texto de origen')
        if entry.get('Tipo_Limite') not in (None, 'COORDINACION_Y_EXPLICITA', 'CONCATENACION_EXPLICITA_REVISADA', 'RESPUESTA_A_LO_QUE_EXPLICITA', 'RESPUESTA_POR_LO_QUE_EXPLICITA', 'GERUNDIO_SENALANDO_EXPLICITO', 'CESION_RELATIVA_EXPLICITA', 'CESION_AGRADECIMIENTO_RELATIVO_EXPLICITO', 'OPINION_TRAS_CITA_CERRADA_REVISADA', 'RETORNO_TRAS_CITA_CERRADA_REVISADA', 'APERTURA_POST_NOMINA_REVISADA', 'RESPUESTA_A_LO_CUAL_MUESTRA_REVISADA', 'RESPUESTA_A_LO_CUAL_EXPLICITA', 'GERUNDIO_INDICANDO_FISCAL_EXPLICITO', 'CESION_HACE_PRESENTE_RELATIVA_EXPLICITA', 'GERUNDIO_NOMINAL_EXPLICITO_REVISADO', 'RESPUESTA_PASIVA_NOMINAL_REVISADA', 'RESPUESTA_LO_QUE_NOMINAL_REVISADA', 'CESION_AGRADECIMIENTO_ANALISIS_REVISADA', 'RESPUESTA_PASIVA_VARIANTE_REVISADA', 'DECLARACION_TRAS_ASUNCION_REVISADA', 'INICIO_CARGO_TRAS_CESION_NOMINAL_REVISADA'):
            raise ValueError('Tipo de límite revisado inválido')
        start, end = entry['Inicio'], entry['Fin']
        if not 0 <= start < end <= len(text) or not text[start:end].startswith(entry['Cita_Inicio']):
            raise ValueError('Intervalo de hablante inválido')
        anchor = entry.get('Cita_Ancla_Posterior')
        if 'Cita_Ancla_Posterior' in entry and (not isinstance(anchor, str) or not anchor
                or end == len(text) or not text[end:].startswith(anchor)):
            raise ValueError('Ancla posterior revisada sin cita/límite válido')
        if not entry['Actor'] or not entry['Justificacion'] or not entry['Evidencia']:
            raise ValueError('Revisión de hablante sin evidencia')
        for ev in entry['Evidencia']:
            row = raw_by_id.get(ev['ID_Padre'])
            if not row or str(row['Fecha'])[:10] != entry['Fecha']:
                raise ValueError('Evidencia de hablante fuera de sesión')
            if not ev['Cita'] or normalize_quote(ev['Cita']) not in normalize_quote(row['Texto']):
                raise ValueError('Cita de hablante inexistente')
        return {**entry, '_Texto_Intervalo':text[start:end],
                '_Inicio_Compacto':len(re.sub(r'\s+', '', text[:start]))}
    for entry in entries:
        rid = entry['ID_Padre']
        if rid in result:
            raise ValueError('Revisión de hablante duplicada')
        extras = entry.get('Revisiones_Adicionales', [])
        if not isinstance(extras, list):
            raise ValueError('Intervalos adicionales inválidos')
        validated = validate(entry)
        compiled = []
        end = entry['Fin']
        for extra in extras:
            if (not isinstance(extra, dict) or 'Revisiones_Adicionales' in extra
                    or extra.get('ID_Padre') != rid or extra.get('Fecha') != entry['Fecha']
                    or extra.get('SHA256_Texto_Padre') != entry['SHA256_Texto_Padre']):
                raise ValueError('Intervalo adicional fuera de padre/fecha/hash')
            item = validate(extra)
            if item['Inicio'] < end:
                raise ValueError('Intervalos revisados solapados o desordenados')
            end = item['Fin']
            compiled.append(item)
        if extras:
            validated['Revisiones_Adicionales'] = compiled
        result[rid] = validated
    return result


def validate_speaker_reviews(rows, reviews):
    """F1: el intervalo revisado debe sobrevivir completo y con su actor/documento."""
    errors = []
    compact = lambda t: re.sub(r'\s+', '', t)
    for row in rows:
        if row['Fuente_Actor'] == SPEAKER_REVIEW_SOURCE:
            applicable = [e for e in speaker_intervals(reviews.get(row['ID_Padre']))
                          if row['Actor_Final']==e['Actor'] and compact(row['Texto']).startswith(compact(e['Cita_Inicio']))]
            if len(applicable) != 1:
                errors.append(f'ID {row["ID"]}: hablante revisado sin evidencia aplicable')
    for rid, root in reviews.items():
        for entry in speaker_intervals(root):
            group = [r for r in rows if r['ID_Padre']==rid]
            matches = [i for i,r in enumerate(group) if r['Fuente_Actor']==SPEAKER_REVIEW_SOURCE
                       and r['Actor_Final']==entry['Actor'] and compact(r['Texto']).startswith(compact(entry['Cita_Inicio']))]
            if len(matches) != 1:
                errors.append(f'{entry["Revision_ID"]}: falta inicio revisado único')
                continue
            if ('_Inicio_Compacto' in entry and sum(len(compact(r['Texto'])) for r in group[:matches[0]]) != entry['_Inicio_Compacto']):
                errors.append(f'{entry["Revision_ID"]}: inicio revisado desplazado')
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
