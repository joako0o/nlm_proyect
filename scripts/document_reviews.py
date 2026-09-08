"""Opiniones escritas leídas por terceros: autor != lector != asistencia.

Sólo particiones individuales con hash y evidencia; no detección por proximidad.
Los cuatro tramos conservan todo el texto y el escrito no se segmenta por voces
mencionadas dentro de sus comillas. El esquema principal permanece compatible.
"""
import collections
import json
from pathlib import Path
from curation import text_hash, normalize_quote
from turns import normalize

PATH = Path(__file__).resolve().parents[1] / 'data/curation/revisiones_documentos_leidos.json'
AUTHOR_SOURCE = 'DOCUMENTO_ESCRITO_REVISADO'
READER_SOURCE = 'LECTOR_DOCUMENTO_REVISADO'
ROLE_SOURCE = 'CARGO_DOCUMENTAL_REVISADO'
DOCUMENT_TYPE = 'OPINION_ESCRITA'
NOTICE = 'TEXTO_ESCRITO_LEIDO_POR_TERCERO'
FIELDS = ['Revision_ID','ID_Padre','ID_Documento','ID_Intervencion','ID_Turno','Fecha','Autor','Lector',
          'Rol_Autor','Rol_Lector','Fuente_Rol','Asistencia_Autor','Inicio','Fin','SHA256_Texto_Padre']


def load_document_reviews(raw, path=PATH):
    result, ids = {}, set()
    for entry in json.loads(Path(path).read_text(encoding='utf-8')):
        p, rid = entry['ID_Padre'], entry['Revision_ID']
        if p in result or rid in ids:
            raise ValueError('Documento revisado duplicado')
        source = raw.get(p)
        if not source or str(source['Fecha'])[:10] != entry['Fecha']:
            raise ValueError('Documento: padre/fecha no coinciden')
        text = source['Texto']
        if text_hash(text) != entry['SHA256_Texto_Padre']:
            raise ValueError('Documento: cambió el texto de origen')
        bounds = entry['Limites']
        if (len(bounds) != 5 or any(type(i) is not int for i in bounds)
                or bounds[0] != 0 or bounds[-1] != len(text)
                or any(a >= z for a,z in zip(bounds,bounds[1:]))):
            raise ValueError('Documento: partición inválida')
        chunks = [text[a:z].strip() for a,z in zip(bounds,bounds[1:])]
        if (not all(chunks) or not chunks[1].startswith('Al proseguir con la Sesión, el señor Presidente informa')
                or not chunks[3].startswith('Concluida la lectura')
                or text[bounds[2]] != '“' or text[bounds[3]-1] != '”'
                or chunks[2].count('“') != 1 or chunks[2].count('”') != 1):
            raise ValueError('Documento: límites de lectura/cita inválidos')
        if (entry['Tipo_Revision'] != 'LECTURA_DIRIGIDA_POR_AGENTE'
                or entry['Asistencia_Autor'] != 'NO_INFERIDA_DEL_DOCUMENTO'
                or not entry['Justificacion'] or not entry['Limitacion']
                or entry['Autor'] == entry['Lector'] or entry['Rol_Autor'] != 'Ministro de Hacienda'
                or entry['Rol_Lector'] != 'Presidente del Banco Central'):
            raise ValueError('Documento: alcance/autor/lector inválidos')
        proof = normalize_quote(entry['Cita_Procedencia'])
        if (proof != normalize_quote(chunks[1]) or 'por escrito' not in proof
                or 'lectura' not in proof
                or f"{entry['Rol_Autor']} señor {entry['Autor_Mencion']}" not in proof):
            raise ValueError('Documento: falta evidencia explícita de autoría y lectura')
        result[p] = {**entry, '_Texto':text, '_Tramos':chunks}
        ids.add(rid)
    return result


def document_parts(text, date, initial_actor, review, detector):
    if (text != review['_Texto'] or date != review['Fecha']
            or initial_actor != review['Actor_Origen']):
        raise ValueError('Documento: fuente/fecha/actor previo incompatibles')
    first = detector.speaker(review['_Tramos'][0], date)
    if (not first or first['actor'] != review['Actor_Anterior']
            or detector.resolve_alias(normalize(review['Autor_Mencion']),date) != review['Autor']
            or detector.resolve_role(date,review['Rol_Lector']) != review['Lector']):
        raise ValueError('Documento: autor/lector/sujeto incompatibles con evidencia')
    return list(zip(review['_Tramos'],
                    [review['Actor_Anterior'],review['Lector'],review['Autor'],review['Lector']],
                    [first['method'],READER_SOURCE,AUTHOR_SOURCE,READER_SOURCE]))


def validate_document_reviews(rows, reviews):
    """F1 de los cuatro intervalos y su semántica, además de integridad general."""
    errors, records = [], []
    grouped = collections.defaultdict(list)
    compact = lambda t: ''.join((t or '').split())
    for row in rows:
        grouped[row['ID_Padre']].append(row)
        if (row['Fuente_Actor'] in {AUTHOR_SOURCE,READER_SOURCE}
                or row.get('Fuente_Rol') == ROLE_SOURCE or row.get('Tipo_Acta') == DOCUMENT_TYPE
                or NOTICE in (row.get('Motivos_Revision') or '')) and row['ID_Padre'] not in reviews:
            errors.append(f"ID {row['ID']}: documento/lector sin revisión")
    for p,e in reviews.items():
        group = grouped[p]
        actors = [e['Actor_Anterior'],e['Lector'],e['Autor'],e['Lector']]
        methods = [None,READER_SOURCE,AUTHOR_SOURCE,READER_SOURCE]
        valid = len(group) == 4
        if valid:
            valid = all(compact(row['Texto']) == compact(t) and row['Actor_Final'] == actor
                        and str(row['Fecha'])[:10] == e['Fecha']
                        and (method is None or row['Fuente_Actor'] == method)
                        for row,t,actor,method in zip(group,e['_Tramos'],actors,methods))
        if not valid:
            errors.append(f"{e['Revision_ID']}: cambiaron intervalos/actores/lector")
            continue
        doc = group[2]
        if (doc.get('Tipo_Acta') != DOCUMENT_TYPE or doc.get('Relacion_Turno') != 'DOCUMENTO_PERSONAL'
                or doc.get('Fuente_Rol') != ROLE_SOURCE or doc.get('Rol_Final') != e['Rol_Autor']
                or doc.get('Rol_Lista_Asistencia') or doc.get('ID_Ancla_Actor')
                or doc.get('ID_Antecedente_Continuidad') or NOTICE not in (doc.get('Motivos_Revision') or '')):
            errors.append(f"{e['Revision_ID']}: documento confundido con habla/asistencia o sin aviso")
        if any(row.get('Tipo_Acta') == DOCUMENT_TYPE for row in [group[0],group[1],group[3]]):
            errors.append(f"{e['Revision_ID']}: escrito invade otros tramos")
        records.append(dict(Revision_ID=e['Revision_ID'], ID_Padre=p, ID_Documento=doc['ID'],
                            ID_Intervencion=doc.get('ID_Intervencion',''), ID_Turno=doc.get('ID_Turno',''), Fecha=e['Fecha'], Autor=e['Autor'],
                            Lector=e['Lector'], Rol_Autor=e['Rol_Autor'], Rol_Lector=e['Rol_Lector'], Fuente_Rol=ROLE_SOURCE,
                            Asistencia_Autor=e['Asistencia_Autor'], Inicio=e['Limites'][2],Fin=e['Limites'][3],
                            SHA256_Texto_Padre=e['SHA256_Texto_Padre']))
    return errors, records
