"""Continuaciones de acta revisadas: no son intervenciones individuales.

Registro separado de hablantes y documentos personales. Padres completos o interrupción inicial individualmente revisada,
con evidencia del antecedente inmediato, ambos congelados por hash/fecha.
No habilita herencia institucional general ni elimina el OCR dañado.
"""
import json
import re
from pathlib import Path
from curation import text_hash, normalize_quote

PATH = Path(__file__).resolve().parents[1]/'data/curation/revisiones_continuaciones_acta.json'
ACTOR = 'Consejo del Banco Central de Chile'
NOTE = 'Continuación de acta revisada: '
RESUME_NOTE = 'Reanudación nominal revisada: '
INTERRUPTION = 'INTERRUPCION_Y_REANUDACION_REVISADA'
MOVEMENT = 'MOVIMIENTO_ASISTENTES_REVISADO'
MOVEMENT_NOTE = 'Movimiento de asistentes revisado: '
# Formas constatadas, admitidas sólo con ficha individual y límites congelados.
# No son un detector general ni convierten asistencia en habla de los nombrados.
MOVEMENT_FORMS = {
    'LLEGADA': 'A continuación, y siendo las 16:25 horas, se incorpora a la Sesión el Ministro de Hacienda señor Felipe Larraín.',
    'RETIRO': 'El Ministro de Hacienda señor Rodrigo Valdés y su Asesor, el señor Claudio Soto, se retiran de la Sala de Consejo.',
}

def is_movement(entry):
    return entry.get('Tipo_Alcance') == MOVEMENT


def _signature(parts):
    return [(normalize_quote(t), a, m) for t, a, m in parts]


def _validate_movement(entry, raw):
    text=entry['Texto_Padre'];a,z=entry['Inicio'],entry['Fin']
    if (type(a) is not int or type(z) is not int or not 0<a<z<len(text)
            or text[a:z]!=entry['Texto_Acta']
            or entry['Texto_Acta']!=MOVEMENT_FORMS.get(entry['Movimiento'])
            or not re.search(r'(?:\.\s+|Sesión N° \d+ Página \d+ de \d+\s+)$',text[:a])
            or text[:a].count('"')%2 or text[:a].count('“')>text[:a].count('”')
            or text[:a].count('«')>text[:a].count('»')):
        raise ValueError('Acta: movimiento sin forma literal, límite o fuera de cita')
    parts=entry['Tramos_Resultado']
    if (not 3<=len(parts)<=5 or len([r for r in parts if r['Texto']==entry['Texto_Acta']])!=1
            or ''.join(''.join(r['Texto'].split()) for r in parts)!=''.join(text.split())
            or parts[1]['Texto']!=entry['Texto_Acta'] or parts[1]['Actor']!=ACTOR
            or parts[1]['Fuente_Actor']!='ACTA/META' or parts[1]['Tipo_Acta']!='ACTA_INSTITUCIONAL'
            or not entry['Evidencia']):
        raise ValueError('Acta: partición de movimiento no conserva el origen')
    for ev in entry['Evidencia']:
        source=raw.get(ev['ID_Padre'])
        if (not source or str(source['Fecha'])[:10]!=entry['Fecha']
                or text_hash(source['Texto'])!=ev['SHA256_Texto_Padre']
                or not ev['Cita'] or normalize_quote(ev['Cita']) not in normalize_quote(source['Texto'])):
            raise ValueError('Acta: evidencia del movimiento inválida')


def _movement_parts(text, entry, segmenter):
    if segmenter is None:
        raise ValueError('Acta: movimiento requiere comprobar segmentación nativa')
    parts=(segmenter(text[:entry['Inicio']].strip(),entry['Actor_Inicial'])
           +[(entry['Texto_Acta'],ACTOR,'ACTA/META')]
           +segmenter(text[entry['Fin']:].strip(),ACTOR))
    expected=[(r['Texto'],r['Actor'],r['Fuente_Actor']) for r in entry['Tramos_Resultado']]
    if _signature(parts)!=_signature(expected):
        raise ValueError('Acta: cambiaron las voces o límites alrededor del movimiento')
    return parts


def is_interruption(entry):
    return entry.get('Tipo_Alcance') == INTERRUPTION



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
        if e.get('Tipo_Alcance') not in (None, INTERRUPTION, MOVEMENT):
            raise ValueError('Acta: alcance desconocido')
        if (e['Texto_Padre'] != target['Texto'] or not e['Cita_Antecedente']
                or not before['Texto'].rstrip().endswith(e['Cita_Antecedente'])
                or e['Decision'] != (MOVEMENT if is_movement(e) else INTERRUPTION if is_interruption(e) else 'CONTINUACION_INSTITUCIONAL_NO_HABLA_PERSONAL')
                or not e['Justificacion'] or not e['Limitacion']):
            raise ValueError('Continuación de acta sin alcance o antecedente literal')
        if is_movement(e):
            _validate_movement(e,raw)
        if is_interruption(e):
            split=e['Limite'];text=target['Texto']
            expected=('El señor Presidente interrumpe la sesión por diez minutos, para permitir el ingreso de un '
                'grupo de reporteros que tomará imágenes de los miembros del Consejo con el nuevo Ministro '
                'de Hacienda señor Andrés Velasco. Una vez realizado este cometido, se reinicia la sesión con '
                'la exposición de don Pablo García,')
            if (type(split) is not int or not 0<split<len(text)
                    or text[:split].strip()!=e['Texto_Acta'] or text[split:].strip()!=e['Texto_Exposicion']
                    or normalize_quote(e['Texto_Acta'])!=expected
                    or not e['Texto_Exposicion'].startswith('quien señala que ')
                    or e['Nombre_Expositor']!='Pablo García' or e['Actor_Expositor']!='Pablo García Silva'):
                raise ValueError('Acta: interrupción/reanudación sin límites y evidencia exacta')
            archive=e['Enlace_Retirado']
            for side,parent in [('Anterior',prev),('Siguiente',p)]:
                row=archive[side]
                if (row['ID_Padre']!=parent or str(row['Fecha'])[:10]!=e['Fecha']
                        or normalize_quote(row['Texto'])!=normalize_quote(raw[parent]['Texto'])
                        or row['Actor_Final']!=e['Actor_Expositor']):
                    raise ValueError('Acta: archivo del enlace retirado incompatible')
            if (archive['Anterior']['ID_Turno']!=archive['Siguiente']['ID_Turno'] or not archive['Motivo']):
                raise ValueError('Acta: enlace previo no compartido o sin motivo de retiro')
        result[p] = e
        ids.add(e['Revision_ID'])
    return result


def institutional_type(text, entry):
    if is_movement(entry):
        matches=[r for r in entry['Tramos_Resultado'] if normalize_quote(r['Texto'])==normalize_quote(text)]
        if len(matches)!=1:
            raise ValueError('Acta: tipo fuera de partición del movimiento')
        return matches[0]['Tipo_Acta']
    if is_interruption(entry):
        if text==entry['Texto_Acta']:return 'ACTA_INSTITUCIONAL'
        if text==entry['Texto_Exposicion']:return ''
        raise ValueError('Acta: tramo fuera de la partición revisada')
    if text != entry['Texto_Padre']:
        raise ValueError('Continuación de acta: cambió el texto')
    # «comunicado oportunamente» es un participio del trámite, no el comunicado RPM.
    return 'ACTA_INSTITUCIONAL'


def institutional_parts(text, entry, detector=None, segmenter=None):
    if text != entry['Texto_Padre']:
        raise ValueError('Continuación de acta: cambió el texto')
    if is_movement(entry):
        return _movement_parts(text,entry,segmenter)
    if is_interruption(entry):
        projected='El señor '+entry['Nombre_Expositor']+' '+entry['Texto_Exposicion'][len('quien '):]
        candidate=detector.speaker(projected,entry['Fecha']) if detector else None
        if not candidate or candidate['actor']!=entry['Actor_Expositor']:
            raise ValueError('Acta: reanudación sin expositor nominal compatible')
        return [(entry['Texto_Acta'],ACTOR,'ACTA/META'),
                (entry['Texto_Exposicion'],entry['Actor_Expositor'],'SUJETO_NOMBRE')]
    return [(text, ACTOR, 'ACTA/META')]


def validate_institutional_reviews(rows, reviews):
    errors, seen = [], set()
    movements={p:e for p,e in reviews.items() if is_movement(e)}
    for p,e in movements.items():
        group=[r for r in rows if r['ID_Padre']==p]
        expected=e['Tramos_Resultado']
        if len(group)!=len(expected):
            errors.append(f'{p}: movimiento sin partición completa')
        else:
            for row,want in zip(group,expected):
                event=want['Texto']==e['Texto_Acta']
                if (str(row['Fecha'])[:10]!=e['Fecha']
                        or normalize_quote(row['Texto'])!=normalize_quote(want['Texto'])
                        or row['Actor_Final']!=want['Actor'] or row['Fuente_Actor']!=want['Fuente_Actor']
                        or (row.get('Tipo_Acta') or '')!=want['Tipo_Acta']
                        or ((MOVEMENT_NOTE+e['Revision_ID']+' (') in (row.get('Nota') or ''))!=event
                        or (event and (row.get('ID_Ancla_Actor') or row.get('ID_Antecedente_Continuidad')
                                       or row['Rol_Final']!='Consejo' or row['Fuente_Rol']!='ACTA_INSTITUCIONAL'))):
                    errors.append(f'{p}: movimiento confundido con habla o tramos adyacentes alterados')
        seen.add(p)
    partial={p:e for p,e in reviews.items() if is_interruption(e)}
    for p,e in partial.items():
        group=[r for r in rows if r['ID_Padre']==p]
        if len(group)!=2:
            errors.append(f'{p}: interrupción sin dos tramos completos');continue
        meta,body=group
        if (normalize_quote(meta['Texto'])!=normalize_quote(e['Texto_Acta'])
                or normalize_quote(body['Texto'])!=normalize_quote(e['Texto_Exposicion'])
                or any(str(r['Fecha'])[:10]!=e['Fecha'] for r in group)
                or meta['Actor_Final']!=ACTOR or meta['Fuente_Actor']!='ACTA/META'
                or meta['Fuente_Rol']!='ACTA_INSTITUCIONAL' or meta['Rol_Final']!='Consejo'
                or meta['Tipo_Acta']!='ACTA_INSTITUCIONAL'
                or meta.get('ID_Ancla_Actor') or meta.get('ID_Antecedente_Continuidad')
                or body['Actor_Final']!=e['Actor_Expositor'] or body['Fuente_Actor']!='SUJETO_NOMBRE'
                or body['Fuente_Rol']!='LISTA_ASISTENCIA' or body['Rol_Final']!='Gerente de Análisis Macroeconómico'
                or body['Tipo_Acta'] or body.get('ID_Antecedente_Continuidad')
                or body.get('ID_Ancla_Actor')!=body.get('ID_Intervencion')
                or NOTE+e['Revision_ID']+' (' not in (meta.get('Nota') or '')
                or RESUME_NOTE+e['Revision_ID']+' (' not in (body.get('Nota') or '')):
            errors.append(f'{p}: interrupción o exposición alterada/confundida con otra voz')
        seen.add(p)
    for row in rows:
        if row['ID_Padre'] in partial or row['ID_Padre'] in movements:continue
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
        elif NOTE in note or RESUME_NOTE in note or MOVEMENT_NOTE in note:
            errors.append(f'{p}: continuación de acta sin evidencia registrada')
    for p in reviews.keys()-seen:
        errors.append(f'{p}: falta continuación de acta revisada')
    return errors
