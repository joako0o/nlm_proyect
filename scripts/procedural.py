"""Fórmulas repetidas: heurística histórica y decisiones de lectura exactas.

Una coincidencia revisada exige el texto entero (salvo espacios). No basta
«solicita» ni «concede» para declarar procedimental un discurso sustantivo.
"""
import json
from pathlib import Path
from curation import normalize_quote, text_hash

PATH = Path(__file__).resolve().parents[1]/'data/curation/formulas_revisadas.json'


def load_formula_reviews(path=PATH, raw_by_id=None):
    reviews = {}
    ids = set()
    for e in json.loads(Path(path).read_text(encoding='utf-8')):
        text = normalize_quote(e['Texto'])
        if not text or text_hash(text) != e['SHA256_Texto']:
            raise ValueError('Fórmula revisada: hash/texto inválido')
        if text in reviews or e['Revision_ID'] in ids:
            raise ValueError('Fórmula revisada duplicada')
        if e['Decision'] != 'FORMULA_PROCEDIMENTAL_REVISADA' or not e['Padres'] or not e['Justificacion']:
            raise ValueError('Fórmula revisada sin decisión/evidencia')
        if raw_by_id is not None:
            for parent in e['Padres']:
                if parent not in raw_by_id or text not in normalize_quote(raw_by_id[parent]['Texto']):
                    raise ValueError('Fórmula revisada sin cita en padre de origen')
        reviews[text] = e
        ids.add(e['Revision_ID'])
    return reviews


FORMULA_REVIEWS = load_formula_reviews()


def is_formula(text):
    return normalize_quote(text) in FORMULA_REVIEWS or any(
        x in text.lower() for x in ['suspende','levanta la sesión','aprueba el texto',
        'ofrece la palabra','agradece la presentación','agradece la exposición',
        'se levanta la sesión','a continuación, concede'])
