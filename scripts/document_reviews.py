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
        received = entry.get('Tipo_Procedencia') == 'PLANTEAMIENTO_RECIBIDO_PARA_LECTURA'
        coordinated = entry.get('Tipo_Procedencia') == 'LECTURA_COORDINADA_RECIBIDA_REVISADA'
        comments = entry.get('Tipo_Procedencia') == 'LECTURA_COMENTARIOS_RECIBIDOS_REVISADA'
        nominal = entry.get('Tipo_Procedencia') == 'LECTURA_NOMINAL_POR_ESCRITO_REVISADA'
        return_variant = entry.get('Tipo_Retorno') == 'RETORNO_LECTURA_VARIANTE_REVISADA'
        arrival = entry.get('Tipo_Anterior') == 'INCORPORACION_INSTITUCIONAL_REVISADA'
        mixed = entry.get('Tipo_Comillas') == 'PAR_MIXTO_REVISADO'
        handoff = entry.get('Tipo_Retorno') == 'CESION_TRAS_LECTURA_REVISADA'
        if (entry.get('Tipo_Procedencia') not in (None, 'PLANTEAMIENTO_RECIBIDO_PARA_LECTURA', 'LECTURA_COORDINADA_RECIBIDA_REVISADA', 'LECTURA_COMENTARIOS_RECIBIDOS_REVISADA', 'LECTURA_NOMINAL_POR_ESCRITO_REVISADA')
                or entry.get('Tipo_Retorno') not in (None, 'CESION_TRAS_LECTURA_REVISADA', 'RETORNO_LECTURA_VARIANTE_REVISADA')
                or entry.get('Tipo_Anterior') not in (None, 'INCORPORACION_INSTITUCIONAL_REVISADA')
                or entry.get('Tipo_Comillas') not in (None, 'PAR_MIXTO_REVISADO')):
            raise ValueError('Documento: modalidad revisada inválida')
        return_valid = (chunks[3] == entry.get('Cita_Retorno')
                        and chunks[3].startswith('A continuación, el Presidente señor ')
                        and ' da paso a la votación, concediéndole la palabra al Consejero señor ' in chunks[3]
                        if handoff else chunks[3].startswith('Concluida la lectura'))
        if return_variant:
            return_valid = (chunks[3] == entry.get('Cita_Retorno') and (
                chunks[3] == 'Finalizada la lectura de los comentarios del señor Ministro de Hacienda, el señor Presidente da paso a la votación.'
                or (chunks[3].startswith('Al proseguir con la Reunión, el Presidente señor ')
                    and ' da paso a la votación, concediéndole la palabra al Consejero señor ' in chunks[3])))
        # Variantes opt-in: el hash y la cita completa siguen siendo obligatorios.
        if nominal:
            intro_valid = chunks[1].startswith(('El Presidente señor ',
                'Al proseguir con la Sesión, el Presidente señor '))
        else:
            intro_valid = coordinated or comments or chunks[1].startswith(
                'Al proseguir con la Sesión, el señor Presidente informa')
        pair = entry.get('Comillas', ['“','”']) if mixed else ['“','”']
        if mixed and (not isinstance(pair,list) or pair not in [['"','”'],['“','"']]
                      or sum(chunks[2].count(c) for c in '“”"') != 2):
            raise ValueError('Documento: par mixto sin delimitación única')
        quote_valid = (text[bounds[2]] == pair[0] and text[bounds[3]-1] == pair[1]
                       and all(chunks[2].count(c)==pair.count(c) for c in set(pair)))
        if not all(chunks) or not intro_valid or not return_valid or not quote_valid:
            raise ValueError('Documento: límites de lectura/cita inválidos')
        if arrival and (not nominal or entry['Actor_Anterior'] != 'Consejo del Banco Central de Chile'
                or chunks[0] != entry.get('Cita_Anterior')
                or chunks[0] != 'El Presidente señor Rodrigo Vergara se integra a la Sesión y pasa a presidirla.'):
            raise ValueError('Documento: incorporación institucional sin evidencia exacta')
        if (entry['Tipo_Revision'] != 'LECTURA_DIRIGIDA_POR_AGENTE'
                or entry['Asistencia_Autor'] != 'NO_INFERIDA_DEL_DOCUMENTO'
                or not entry['Justificacion'] or not entry['Limitacion']
                or entry['Autor'] == entry['Lector'] or entry['Rol_Autor'] != 'Ministro de Hacienda'
                or entry['Rol_Lector'] != 'Presidente del Banco Central'):
            raise ValueError('Documento: alcance/autor/lector inválidos')
        proof = normalize_quote(entry['Cita_Procedencia'])
        # Variante individual: texto recibido que se anuncia para lectura literal.
        # No inferir formato de envío ni asistencia, y no aceptar una mera opinión citada.
        received_proof = ('Al proseguir con la Sesión, el señor Presidente informa que el Ministro de Hacienda señor '
                          +entry['Autor_Mencion']+', por intermedio de su Asesor señor Rodrigo Cerda, '
                          +'le ha hecho llegar su planteamiento, al que dará lectura a continuación:')
        if coordinated:
            provenance_valid = proof == ('e informa que el Ministro de Hacienda señor '+entry['Autor_Mencion']
                +', por intermedio de su Asesor señor Rodrigo Cerda, le ha hecho llegar su planteamiento, al que dará lectura a continuación.')
        elif comments:
            provenance_valid = proof == ('y, a continuación, debido a la imposibilidad del Ministro de Hacienda, señor '
                +entry['Autor_Mencion']+', de asistir a la sesión de la tarde, da lectura a los comentarios que hizo llegar a través de su asesor, señor Rodrigo Cerda:')
        else:
            provenance_valid = (proof == received_proof if received else 'por escrito' in proof)
        author_phrase = entry['Rol_Autor']+(', señor ' if comments else ' señor ')+entry['Autor_Mencion']
        if (proof != normalize_quote(chunks[1]) or not provenance_valid
                or 'lectura' not in proof or author_phrase not in proof):
            raise ValueError('Documento: falta evidencia explícita de autoría y lectura')
        result[p] = {**entry, '_Texto':text, '_Tramos':chunks}
        ids.add(rid)
    return result


def document_parts(text, date, initial_actor, review, detector):
    if (text != review['_Texto'] or date != review['Fecha']
            or initial_actor != review['Actor_Origen']):
        raise ValueError('Documento: fuente/fecha/actor previo incompatibles')
    arrival = review.get('Tipo_Anterior') == 'INCORPORACION_INSTITUCIONAL_REVISADA'
    if arrival:
        candidate = detector.speaker(review['_Tramos'][0].replace('se integra a la Sesión y pasa a presidirla.', 'informa.'), date)
        if not candidate or candidate['actor'] != review['Lector']:
            raise ValueError('Documento: incorporación sin presidente compatible')
        first = {'actor':'Consejo del Banco Central de Chile', 'method':'ACTA/META'}
    else:
        first = detector.speaker(review['_Tramos'][0], date)
    if (not first or first['actor'] != review['Actor_Anterior']
            or detector.resolve_alias(normalize(review['Autor_Mencion']),date) != review['Autor']
            or detector.resolve_role(date,review['Rol_Lector']) != review['Lector']):
        raise ValueError('Documento: autor/lector/sujeto incompatibles con evidencia')
    if review.get('Tipo_Procedencia') in {'LECTURA_COORDINADA_RECIBIDA_REVISADA','LECTURA_COMENTARIOS_RECIBIDOS_REVISADA'} and review['Actor_Anterior'] != review['Lector']:
        raise ValueError('Documento: lectura coordinada sin lector antecedente')
    if review.get('Tipo_Procedencia') == 'LECTURA_NOMINAL_POR_ESCRITO_REVISADA':
        projected = review['_Tramos'][1]
        lead = 'Al proseguir con la Sesión, '
        if projected.startswith(lead):projected=projected[len(lead):]
        intro = detector.speaker(projected, date)
        if not intro or intro['actor'] != review['Lector']:
            raise ValueError('Documento: anuncio nominal sin lector compatible')
    if review.get('Tipo_Retorno') == 'RETORNO_LECTURA_VARIANTE_REVISADA':
        projected = review['_Tramos'][3]
        for lead in ['Finalizada la lectura de los comentarios del señor Ministro de Hacienda, ', 'Al proseguir con la Reunión, ']:
            if projected.startswith(lead):projected=projected[len(lead):];break
        tail = detector.speaker(projected.replace('da paso a la votación', 'ofrece la palabra', 1), date)
        if not tail or tail['actor'] != review['Lector']:
            raise ValueError('Documento: retorno variante sin lector compatible')
    if review.get('Tipo_Retorno') == 'CESION_TRAS_LECTURA_REVISADA':
        # Proyección sólo para validar el sujeto; no reescribir la cesión exportada.
        tail = detector.speaker(review['_Tramos'][3].replace(
            'da paso a la votación, concediéndole la palabra al', 'ofrece la palabra al', 1), date)
        if not tail or tail['actor'] != review['Lector']:
            raise ValueError('Documento: retorno sin lector presidencial compatible')
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
        if e.get('Tipo_Anterior') == 'INCORPORACION_INSTITUCIONAL_REVISADA':
            before=group[0]
            if (before['Fuente_Actor'] != 'ACTA/META' or before.get('Fuente_Rol') != 'ACTA_INSTITUCIONAL'
                    or before.get('Rol_Final') != 'Consejo' or before.get('Tipo_Acta') != 'ACTA_INSTITUCIONAL'
                    or before.get('ID_Ancla_Actor') or before.get('ID_Antecedente_Continuidad')):
                errors.append(f"{e['Revision_ID']}: incorporación confundida con habla personal")
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
