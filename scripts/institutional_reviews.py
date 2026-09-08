"""Continuaciones de acta revisadas: no son intervenciones individuales.

Registro separado de hablantes y documentos personales. Sólo padres completos
con evidencia del antecedente inmediato, ambos congelados por hash/fecha.
No habilita herencia institucional general ni elimina el OCR dañado.
"""
import json
from pathlib import Path
from curation import text_hash, normalize_quote

PATH = Path(__file__).resolve().parents[1]/'data/curation/revisiones_continuaciones_acta.json'
ACTOR = 'Consejo del Banco Central de Chile'
NOTE = 'Continuación de acta revisada: '


def load_institutional_reviews(raw, path=PATH):
    result, ids = {}, set()
    for e in json.loads(Path(path).read_text(encoding='utf-8')):
        p, prev = e['ID_Padre'], e['ID_Antecedente']
        target, before = raw.get(p), raw.get(prev)
        if p in result or e['Revision_ID'] in ids:
            raise ValueError('Continuación de acta duplicada')
        if (not target or not before or prev != p-1
                or str(target['Fecha'])[:10] != e['Fecha'] or str(before['Fecha'])[:10] != e['Fecha']
                or text_hash(target['Texto']) != e['SHA256_Texto_Padre']
                or text_hash(before['Texto']) != e['SHA256_Texto_Antecedente']):
            raise ValueError('Continuación de acta: fuente/antecedente/fecha/hash inválidos')
        if (e['Texto_Padre'] != target['Texto'] or not e['Cita_Antecedente']
                or not before['Texto'].rstrip().endswith(e['Cita_Antecedente'])
                or e['Decision'] != 'CONTINUACION_INSTITUCIONAL_NO_HABLA_PERSONAL'
                or not e['Justificacion'] or not e['Limitacion']):
            raise ValueError('Continuación de acta sin alcance o antecedente literal')
        result[p] = e
        ids.add(e['Revision_ID'])
    return result


def institutional_type(text, entry):
    if text != entry['Texto_Padre']:
        raise ValueError('Continuación de acta: cambió el texto')
    # «comunicado oportunamente» es un participio del trámite, no el comunicado RPM.
    return 'ACTA_INSTITUCIONAL'


def institutional_parts(text, entry):
    if text != entry['Texto_Padre']:
        raise ValueError('Continuación de acta: cambió el texto')
    return [(text, ACTOR, 'ACTA/META')]


def validate_institutional_reviews(rows, reviews):
    errors, seen = [], set()
    for row in rows:
        p = row['ID_Padre']
        e = reviews.get(p)
        note = row.get('Nota') or ''
        if e:
            if p in seen:
                errors.append(f'{p}: continuación de acta dividida sin revisión')
            seen.add(p)
            if (str(row['Fecha'])[:10] != e['Fecha'] or row['Actor_Final'] != ACTOR
                    or row['Fuente_Actor'] != 'ACTA/META' or row['Fuente_Rol'] != 'ACTA_INSTITUCIONAL'
                    or row['Tipo_Acta'] != 'ACTA_INSTITUCIONAL' or row['Rol_Final'] != 'Consejo'
                    or normalize_quote(row['Texto']) != normalize_quote(e['Texto_Padre'])
                    or NOTE+e['Revision_ID']+' (' not in note
                    or row.get('ID_Ancla_Actor') or row.get('ID_Antecedente_Continuidad')):
                errors.append(f'{p}: continuación de acta alterada o tratada como habla personal')
        elif NOTE in note:
            errors.append(f'{p}: continuación de acta sin evidencia registrada')
    for p in reviews.keys()-seen:
        errors.append(f'{p}: falta continuación de acta revisada')
    return errors
