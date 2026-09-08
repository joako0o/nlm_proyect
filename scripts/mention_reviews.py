"""Lecturas de menciones en la cola actual, sin alterar actores ni alertas.

No dependen de pertenecer a la instantánea histórica de 783 intervalos.
Una lectura sólo se adjunta a la fila exacta cuyo texto, actor y límites siguen
vigentes. No adjudica otros motivos de alerta ni crea un ancla de continuidad.
"""
import collections
import json
import re
from pathlib import Path
from curation import normalize_quote, text_hash

PATH = Path(__file__).resolve().parents[1] / 'data/curation/revisiones_menciones_actuales.json'
FIELDS = ('Estado_Lectura_Dirigida', 'Revision_Lectura_Dirigida', 'Alcance_Lectura_Dirigida')
MOTIVE = 'POSIBLE_OTRO_HABLANTE_O_MENCION'
DECISION = 'MENCION_LEGITIMA_REVISADA'


def compact(text):
    return re.sub(r'\s+', '', text)


def load_mention_reviews(raw_by_id, path=PATH):
    result, intervals = {}, set()
    for entry in json.loads(Path(path).read_text(encoding='utf-8')):
        rid = entry['Revision_ID']
        parent = entry['ID_Padre']
        source = raw_by_id.get(parent)
        start, end = entry['Inicio'], entry['Fin']
        key = (parent, start, end)
        if rid in result or key in intervals:
            raise ValueError('Lectura de mención duplicada')
        if not source or str(source['Fecha'])[:10] != entry['Fecha']:
            raise ValueError('Lectura de mención: padre/fecha no coinciden')
        text = source['Texto']
        if text_hash(text) != entry['SHA256_Texto_Padre']:
            raise ValueError('Lectura de mención: cambió el texto de origen')
        if not 0 <= start < end <= len(text) or not entry['Cita_Inicio'] or not text[start:end].startswith(entry['Cita_Inicio']):
            raise ValueError('Intervalo de mención inválido')
        if (entry['Decision'] != DECISION or entry['Motivo_Revisado'] != MOTIVE
                or entry['Tipo_Revision'] != 'LECTURA_DIRIGIDA_POR_AGENTE'
                or not entry['Actor'] or not entry['Justificacion'] or not entry['Limitacion']
                or not entry['Evidencia']):
            raise ValueError('Lectura de mención sin alcance/evidencia válida')
        for ev in entry['Evidencia']:
            row = raw_by_id.get(ev['ID_Padre'])
            quote = normalize_quote(ev['Cita'])
            if not row or str(row['Fecha'])[:10] != entry['Fecha']:
                raise ValueError('Evidencia de mención fuera de sesión')
            if not quote or quote not in normalize_quote(row['Texto']):
                raise ValueError('Cita de mención inexistente')
        result[rid] = {**entry, '_Texto': compact(text[start:end]),
                       '_Inicio': len(compact(text[:start])), '_Fin': len(compact(text[:end]))}
        intervals.add(key)
    return result


def validate_mention_reviews(rows, reviews):
    """Devuelve errores y anotaciones separadas; nunca modifica las filas recibidas."""
    groups = collections.defaultdict(list)
    positions = collections.Counter()
    for row in rows:
        parent = row['ID_Padre']
        start = positions[parent]
        end = start + len(compact(row['Texto']))
        positions[parent] = end
        groups[parent].append((start, end, row))
    errors, annotations = [], {}
    for rid, entry in reviews.items():
        matches = [r for start, end, r in groups[entry['ID_Padre']]
                   if (start, end) == (entry['_Inicio'], entry['_Fin'])]
        if (len(matches) != 1 or matches[0]['Actor_Final'] != entry['Actor']
                or str(matches[0]['Fecha'])[:10] != entry['Fecha']
                or compact(matches[0]['Texto']) != entry['_Texto']):
            errors.append(f'{rid}: cambió actor/texto/límite; revisar la mención de nuevo')
            continue
        row = matches[0]
        annotations[row['ID']] = dict(zip(FIELDS, (
            entry['Decision'], rid,
            entry['Motivo_Revisado'] + ': ' + entry['Justificacion'] + ' ' + entry['Limitacion'])))
    return errors, annotations


def annotation_for(row, annotations):
    return {key: (annotations or {}).get(row['ID'], {}).get(key, '') for key in FIELDS}
