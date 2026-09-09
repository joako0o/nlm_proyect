"""Alertas contextuales con fuente/hash: no corrigen ni certifican atribuciones."""
import json
from pathlib import Path
from curation import text_hash
PATH=Path(__file__).resolve().parents[1]/'data/curation/alertas_contextuales.json'
MOTIVE='CARGO_EN_DISCURSO_POR_VERIFICAR'
IDENTITY_MOTIVE='HABLANTES_POR_IDENTIDAD_PENDIENTE'
JOINT_MOTIVE='PASAJES_CONJUNTOS_POR_DELIMITAR'
DAMAGE_MOTIVE='TEXTO_DANADO_POR_COTEJAR'
NAME_MOTIVE='NOMBRE_EN_DISCURSO_POR_VERIFICAR'
BOUNDARY_MOTIVE='HABLANTES_POR_DELIMITAR'
DECISIONS={BOUNDARY_MOTIVE:'PENDIENTE_DELIMITACION_DE_VOCES', NAME_MOTIVE:'PENDIENTE_CONTRASTE_NOMBRE', DAMAGE_MOTIVE:'PENDIENTE_COTEJO_TEXTUAL', JOINT_MOTIVE:'PENDIENTE_DELIMITACION_CONJUNTA', MOTIVE:'PENDIENTE_CONTRASTE_CARGO',
           IDENTITY_MOTIVE:'PENDIENTE_SEPARACION_E_IDENTIDAD'}

def has_context_warning(motives):
    return bool(set(DECISIONS) & set((motives or '').split(';')))

def compact(text):return ''.join(text.split())

def load_context_warnings(raw,path=PATH):
    result={}
    for e in json.loads(Path(path).read_text(encoding='utf-8')):
        p=e['ID_Padre'];r=raw.get(p)
        if p in result or any(v['Revision_ID']==e['Revision_ID'] for v in result.values()):
            raise ValueError('Alerta contextual duplicada')
        if not r or str(r['Fecha'])[:10]!=e['Fecha'] or text_hash(r['Texto'])!=e['SHA256_Texto_Padre']:
            raise ValueError('Alerta contextual: fuente/fecha/hash cambió')
        a,z=e['Inicio'],e['Fin'];text=r['Texto']
        if (type(a) is not int or type(z) is not int or not 0<=a<z<=len(text)
                or text[a:z].strip()!=e['Texto_Intervalo'] or not e['Texto_Intervalo']):
            raise ValueError('Alerta contextual: intervalo inválido')
        if (e['Motivo'] not in DECISIONS or e['Decision']!=DECISIONS.get(e['Motivo'])
                or not e['Actor_Provisional'] or not e['Justificacion'] or not e['Limitacion']):
            raise ValueError('Alerta contextual: falta alcance')
        result[p]={**e,'_Texto':compact(e['Texto_Intervalo'])}
    return result

def contextual_motives(row,reviews):
    e=(reviews or {}).get(row['ID_Padre'])
    if (e and str(row['Fecha'])[:10]==e['Fecha'] and row['Actor_Final']==e['Actor_Provisional']
            and compact(row['Texto'])==e['_Texto']):
        return [e['Motivo']]
    return []

def validate_context_warnings(rows,reviews):
    errors=[];seen=set()
    for r in rows:
        applicable=contextual_motives(r,reviews)
        if applicable:
            if r['ID_Padre'] in seen:errors.append('Alerta contextual repetida en salida')
            seen.add(r['ID_Padre'])
        if set(applicable)!=(set(DECISIONS) & set((r.get('Motivos_Revision') or '').split(';'))):
            errors.append(f"ID {r['ID']}: alerta contextual sin evidencia o ausente")
    for p in reviews:
        if p not in seen:errors.append(f'{p}: cambió el intervalo/actor de alerta contextual; revisar de nuevo')
    return errors
