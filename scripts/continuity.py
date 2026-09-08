"""Continuidad discursiva entre filas: una exposición puede ocupar muchos padres.

Nunca se fusiona ni se borra el texto de origen. Se documenta una relación entre
filas contiguas. La proximidad o la coincidencia de nombres, por sí solas, no
son evidencia suficiente para reasignar al actor de una fila.
"""
from context_warnings import has_context_warning
import re
from turns import normalize

CONSEJO = 'Consejo del Banco Central de Chile'
EXPLICIT = {'SUJETO_ROL_NOMBRE', 'SUJETO_NOMBRE', 'SUJETO_ROL_SESION'}
CONTINUED = {'CONTINUIDAD_PARRAFO', 'CONTINUACION_XLSX', 'ANAFORA_CONTINUIDAD'}

# Barreras aunque el siguiente registro sea del mismo actor.
BOUNDARY = re.compile(r'\b(?:ofrece|concede|cede|da)\s+la\s+palabra\b|'
                      r'\bsolicita\s+al\b|\bsuspend[ei]\w*\s+la\s+sesion\b|'
                      r'\bda por (?:finalizada|concluida) la sesion\b|\bpone termino a la sesion\b|'
                      r'\babre la sesion\b|\breanuda\w*\s+la\s+sesion\b|\bse\s+levanta\s+la\s+sesion\b')
SECTION = re.compile(r'^(?:[a-z]\)\s*)?(?:minuta\s+(?:del|de la)|fundamentacion\s+de\s+voto|'
                     r'votacion|acuerdo|comunicado|acta\s+correspondiente)\b')
PERSON_CUE = re.compile(r'\b(?:el|la)\s+(?:senor|senora|presidente|vicepresidente|consejero|consejera|'
                        r'gerente|ministro|ministra|subgerente)\b')


def boundary(text):
    return bool(BOUNDARY.search(normalize(text)))


def continuation_start(text, actor, state, detector, sentence_spans, date):
    """Sólo continúa desde un ancla explícita vigente, compatible con la fuente.

    Una persona distinta en Actor_Original NO se sustituye por herencia ciega.
    Si hay sujetos/cargos sin resolver o una nueva sección, nos abstenemos.
    """
    if not state or state.get('date') != date or actor != state.get('actor') or not state.get('anchor'):
        return False
    if actor == CONSEJO or state.get('barrier') or SECTION.search(normalize(text)):
        return False
    for a,b in sentence_spans(text):
        sent = text[a:b]
        if not sent.strip():
            continue
        if detector.speaker(sent, date, actor, state.get('roles')):
            return False
        # No convertir un sujeto que el parser no reconoce en continuación segura.
        if PERSON_CUE.search(normalize(sent)):
            return False
        return True
    return False


def update_state(state, actor, method, text, date, detector, sentence_spans, evidence_id, institutional=False):
    """Avanza el contexto sólo con atribución resuelta; nunca cruza sesiones."""
    if state.get('date') != date:
        state.clear()
    state['date'] = date
    state['actor'] = actor
    if method in EXPLICIT:
        state['anchor'] = evidence_id
    elif method not in CONTINUED:
        state['anchor'] = None
    state['barrier'] = actor == CONSEJO or institutional or boundary(text)
    state['pending'] = detector.handoff(text, date)
    if actor == CONSEJO or institutional:
        state['roles'] = {}
        state['last_sentence'] = ''
    else:
        spans = [(a,b) for a,b in sentence_spans(text) if text[a:b].strip()]
        state['last_sentence'] = text[spans[-1][0]:spans[-1][1]] if spans else ''
    for a,b in sentence_spans(text):
        candidates = detector.candidates(text[a:b], date, actor, allow_embedded=True)
        if any(c['actor'] != actor for c in candidates):
            state['barrier'] = True
            break


def annotate_turns(rows):
    """Agrega identificadores de turno y eslabones de evidencia, sin reasignar.

    Los grupos son conservadores: ni mismo actor sin ancla ni una vuelta tras
    otra persona reabren un turno anterior. Una alerta interna impide propagar
    el ancla al siguiente párrafo, pero se conserva el grupo ya establecido.
    """
    last = None
    counts = {}
    for row in rows:
        date = str(row['Fecha'])[:10]
        actor = row['Actor_Final']
        text = row['Texto']
        source = row['Fuente_Actor']
        prev = last if last and str(last['Fecha'])[:10] == date else None
        institutional = actor == CONSEJO or row.get('Tipo_Acta') in ('ACUERDO_CONSEJO','COMUNICADO','META_SESION','ACTA_CABECERA','ACTA_INSTITUCIONAL')
        same = bool(prev and prev['Actor_Final'] == actor)
        blocked = (not prev or institutional or prev.get('_blocks_continuity') or SECTION.search(normalize(text)))
        previous_anchor = prev.get('ID_Ancla_Actor') if prev else None
        same_physical_block = bool(same and prev['ID_Bloque_Texto'] == row['ID_Bloque_Texto'] and source == 'CONTINUACION_XLSX')
        joined = bool(same and not blocked and previous_anchor and (source in EXPLICIT | CONTINUED or same_physical_block))
        if joined:
            turn = prev['ID_Turno']
            antecedent = prev['ID_Intervencion']
            relation = 'CONTINUIDAD_EXPLICITA' if source in EXPLICIT else source
            anchor = row['ID_Intervencion'] if source in EXPLICIT else previous_anchor
        else:
            counts[date] = counts.get(date,0)+1
            turn = f'RPM-{date}:T{counts[date]}'
            antecedent = ''
            anchor = row['ID_Intervencion'] if source in EXPLICIT and not institutional else ''
            relation = 'DOCUMENTO_PERSONAL' if source in ('ENCABEZADO_MINUTA', 'DOCUMENTO_ESCRITO_REVISADO') else ('INSTITUCIONAL' if institutional else ('INICIO_EXPLICITO' if source in EXPLICIT else 'SIN_CONTINUIDAD_CONFIRMADA'))
        row.update(ID_Turno=turn, Relacion_Turno=relation,
                   ID_Antecedente_Continuidad=antecedent, ID_Ancla_Actor=anchor)
        row['_blocks_continuity'] = (institutional or boundary(text) or
            'POSIBLE_OTRO_HABLANTE_O_MENCION' in (row.get('Motivos_Revision') or '') or
            has_context_warning(row.get('Motivos_Revision')) or
            source not in EXPLICIT | CONTINUED)
        last = row
    for row in rows:
        row.pop('_blocks_continuity', None)
    return rows
