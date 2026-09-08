"""Enlaces discursivos acotados: no reasignan actores ni crean anclas globales."""
import json
from pathlib import Path
from curation import text_hash, normalize_quote

PATH=Path(__file__).resolve().parents[1]/'data/curation/revisiones_continuidad_hablantes.json'
RELATION='CONTINUIDAD_REVISADA'

def compact(text):return ''.join(text.split())

def load_reviewed_links(raw,path=PATH):
    result={};ids=set()
    for e in json.loads(Path(path).read_text(encoding='utf-8')):
        left,right=e['Anterior'],e['Siguiente'];key=(left['ID_Padre'],right['ID_Padre'])
        if (key in result or e['Revision_ID'] in ids or key[1]!=key[0]+1
                or e['Tipo_Revision']!='LECTURA_DIRIGIDA_POR_AGENTE'
                or not all(e[k] for k in ['Actor','Justificacion','Limitacion','Evidencia'])):
            raise ValueError('Continuidad revisada: falta alcance o enlace duplicado/no contiguo')
        for side in [left,right]:
            r=raw.get(side['ID_Padre']);a,z=side['Inicio'],side['Fin']
            if (not r or str(r['Fecha'])[:10]!=e['Fecha'] or text_hash(r['Texto'])!=side['SHA256_Texto_Padre']
                    or type(a) is not int or type(z) is not int or not 0<=a<z<=len(r['Texto'])
                    or r['Texto'][a:z].strip()!=side['Texto']):
                raise ValueError('Continuidad revisada: fuente/fecha/hash/intervalo cambió')
        if (compact(raw[key[0]]['Texto'][left['Fin']:]) or right['Inicio']!=0
                or left['Fuente_Actor']!='CONTEXTO_REVISADO'
                or right['Fuente_Actor'] not in {'SUJETO_NOMBRE','SUJETO_ROL_NOMBRE','SUJETO_ROL_SESION'}):
            raise ValueError('Continuidad revisada: extremos/fuentes incompatibles')
        for ev in e['Evidencia']:
            r=raw.get(ev['ID_Padre'])
            if (not r or str(r['Fecha'])[:10]!=e['Fecha'] or not ev['Cita']
                    or normalize_quote(ev['Cita']) not in normalize_quote(r['Texto'])):
                raise ValueError('Continuidad revisada: evidencia inválida')
        result[key]=e;ids.add(e['Revision_ID'])
    return result

def matching_link(prev,row,reviews):
    if not prev:return None
    e=(reviews or {}).get((prev.get('ID_Padre'),row.get('ID_Padre')))
    if not e:return None
    for r,side in [(prev,e['Anterior']),(row,e['Siguiente'])]:
        if (str(r['Fecha'])[:10]!=e['Fecha'] or r['Actor_Final']!=e['Actor']
                or r['Fuente_Actor']!=side['Fuente_Actor'] or compact(r['Texto'])!=compact(side['Texto'])):
            return None
    return e

def validate_reviewed_links(rows,reviews):
    errors=[];seen=set();previous=None
    for row in rows:
        e=matching_link(previous,row,reviews)
        if e:
            key=(previous['ID_Padre'],row['ID_Padre'])
            if key in seen:errors.append('Continuidad revisada repetida')
            seen.add(key)
            if (row.get('Relacion_Turno')!=RELATION or row.get('ID_Turno')!=previous.get('ID_Turno')
                    or row.get('ID_Antecedente_Continuidad')!=previous.get('ID_Intervencion')
                    or previous.get('ID_Ancla_Actor')
                    or row.get('ID_Ancla_Actor')!=row.get('ID_Intervencion')):
                errors.append(f"{e['Revision_ID']}: enlace/antecedente/ancla no coincide")
        elif row.get('Relacion_Turno')==RELATION:
            errors.append('Continuidad revisada sin evidencia registrada')
        previous=row
    if seen!=set(reviews):errors.append('Continuidad revisada: faltan extremos exactos/contiguos en salida')
    return errors
