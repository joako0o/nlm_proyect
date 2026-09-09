"""Tres refinamientos funcionales v4, sin regla global ni cambio de hablante.

La evidencia histórica de movimiento4788 permanece intacta: se refina sólo su
primer tramo para tipificar/validar la salida v4 con el validador institucional
original. La segmentación histórica y los perfiles v1/v2/v3 no cambian.
"""
import copy
import hashlib
import json
from pathlib import Path
from revisar_continuidad_barreras import READINGS, BASE, BASE_SHA, validate
from diagnosticar_finales import read_rows

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT/'data/curation/refinamiento_funcional_v4.json'
PARENTS = {4788,4849,4899}
PREVIOUS = {4788:'RPM-2012-04-17:4787:2',4849:'RPM-2012-05-17:4848:1',4899:'RPM-2012-06-14:4898:1'}


def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()


def load_refinements(raw, path=PATH):
    pkg=json.loads(Path(path).read_text())
    if (not isinstance(pkg,dict) or type(pkg.get('Version')) is not int or pkg['Version']!=4
            or pkg.get('Perfil')!='funcional-v4' or not isinstance(pkg.get('Revisiones'),dict)
            or set(pkg.get('Revisiones',{}))!={str(p) for p in PARENTS}
            or pkg.get('SHA256_Lecturas_Lote4')!=hashlib.sha256(READINGS.read_bytes()).hexdigest()
            or hashlib.sha256(BASE.read_bytes()).hexdigest()!=BASE_SHA):
        raise ValueError('Refinamiento funcional fuera de versión/evidencia')
    ledger=json.loads(READINGS.read_text());rows=read_rows(BASE)
    validate(rows,ledger,raw)
    by_id={r['ID_Intervencion']:r for r in rows}
    ids=set()
    try:
        for p in PARENTS:
            e=pkg['Revisiones'][str(p)];old=by_id[e['ID_Fila_Original']]
            proof=ledger['Casos'][PREVIOUS[p]];bound=proof['Limite_Funcional_No_Aplicado']
            prefix=bound['Prefijo_Personal'];previous=by_id[PREVIOUS[p]]
            if (type(e['ID_Padre']) is not int or e['ID_Padre']!=p or old['ID_Padre']!=p or old['Numero_Segmento']!=1
                    or e['Fecha']!=str(raw[p]['Fecha'])[:10] or e['Fecha']!=str(old['Fecha'])[:10]
                    or e['ID_Anterior']!=PREVIOUS[p] or e['Texto_Original']!=old['Texto']
                    or e['Actor']!=old['Actor_Final'] or e['Actor']!='Rodrigo Vergara Montes'
                    or e['Fuente_Actor']!=old['Fuente_Actor'] or e['Fuente_Actor']!='SUJETO_ROL_NOMBRE'
                    or e['SHA256_Texto_Padre']!=hashlib.sha256(raw[p]['Texto'].encode()).hexdigest()
                    or e['Texto_Personal']!=prefix.rstrip() or e['Separador']!=prefix[len(prefix.rstrip()):]
                    or e['Texto_Constancia']!=bound['Constancia_Y_Residuo']
                    or e['Texto_Personal']+e['Separador']+e['Texto_Constancia']!=e['Texto_Original']
                    or not e['Separador'].isspace() or e['Tipo_Personal']!='' or e['Tipo_Constancia']!='ACUERDO_CONSEJO'
                    or e['Justificacion']!=proof['Justificacion'] or not e['Aplicacion']
                    or not e['Revision_ID'] or e['Revision_ID'] in ids
                    or previous['Actor_Final']!=e['Actor'] or previous['Tipo_Acta'] or previous['Motivos_Revision']
                    or previous['ID_Ancla_Actor']!=previous['ID_Intervencion']):
                raise ValueError('Extremos, fuente o decisión funcional modificados')
            ids.add(e['Revision_ID'])
        old_institutions=json.loads((ROOT/'data/curation/revisiones_continuaciones_acta.json').read_text())
        old=next(e for e in old_institutions if e['ID_Padre']==4788)
        if pkg['SHA256_Revision_Institucional_4788']!=digest(old):
            raise ValueError('Cambió la revisión institucional histórica')
    except (KeyError,TypeError,StopIteration) as exc:
        raise ValueError('Registro funcional incompleto') from exc
    return {int(k):v for k,v in pkg['Revisiones'].items()}


def refine_segments(parent, segments, reviews):
    e=(reviews or {}).get(parent)
    if not e:
        return segments
    if (not segments or segments[0]!=(e['Texto_Original'],e['Actor'],e['Fuente_Actor'])
            or sum(t==e['Texto_Original'] for t,_,_ in segments)!=1):
        raise ValueError('La partición anterior no coincide con la prueba funcional')
    return [(e['Texto_Personal'],e['Actor'],e['Fuente_Actor']),
            (e['Texto_Constancia'],e['Actor'],e['Fuente_Actor']),*segments[1:]]


def refined_institutions(institutions, reviews):
    """Refinamiento declarado sólo de4788; el validador original recibe cinco tramos.

    No se reconstruyen filas viejas para ocultar fallos en la salida. Los demás
    campos y los tres tramos de llegada/excusa/retorno permanecen idénticos.
    """
    if not reviews:return institutions
    result=copy.deepcopy(institutions)
    e=reviews[4788];old=result[4788]['Tramos_Resultado']
    if len(old)!=4 or old[0]['Texto']!=e['Texto_Original']:
        raise ValueError('Movimiento4788 no corresponde a su antecedente')
    personal={**old[0],'Texto':e['Texto_Personal'],'Tipo_Acta':''}
    constancia={**old[0],'Texto':e['Texto_Constancia'],'Tipo_Acta':'ACUERDO_CONSEJO'}
    result[4788]['Tramos_Resultado']=[personal,constancia,*old[1:]]
    result[4788]['Refinamiento_Funcional']=e['Revision_ID']
    return result


def validate_refinements(rows,reviews):
    errors=[];idx={r['ID_Intervencion']:r for r in rows}
    for p,e in reviews.items():
        parts=[r for r in rows if r['ID_Padre']==p]
        if len(parts)!=(5 if p==4788 else 3):
            errors.append(f'{p}: falta partición funcional');continue
        a,b=parts[:2];previous=idx.get(e['ID_Anterior'])
        for r,text,tipo in [(a,e['Texto_Personal'],''),(b,e['Texto_Constancia'],'ACUERDO_CONSEJO')]:
            if (r['Texto']!=text or r['Actor_Final']!=e['Actor'] or r['Fuente_Actor']!=e['Fuente_Actor']
                    or str(r['Fecha'])[:10]!=e['Fecha'] or (r.get('Tipo_Acta') or '')!=tipo):
                errors.append(f'{p}: función, texto o hablante incorrectos')
        if (not previous or a.get('ID_Turno')!=previous.get('ID_Turno')
                or a.get('ID_Antecedente_Continuidad')!=e['ID_Anterior']
                or a.get('Relacion_Turno')!='CONTINUIDAD_EXPLICITA'
                or a.get('ID_Ancla_Actor')!=a['ID_Intervencion']
                or b.get('ID_Turno')==a.get('ID_Turno') or b.get('Relacion_Turno')!='INSTITUCIONAL'
                or b.get('ID_Ancla_Actor') or b.get('ID_Antecedente_Continuidad')):
            errors.append(f'{p}: continuidad, ancla o constancia incorrectas')
    return errors


def active_refinements(raw,intrapara_profile=None):
    """Impide combinar v4 con un perfil de continuidad incompleto por ambiente."""
    import os
    from intrapara_profiles import profile_name, required_intrapara
    path=os.environ.get('NLM_FUNCTIONAL_REVIEWS')
    if not path:return {}
    intra=os.environ.get('NLM_INTRAPARA_REVIEWS')
    intrapara_profile=required_intrapara(intrapara_profile)
    if not intra or profile_name(intra)!=intrapara_profile:
        raise ValueError(f'El refinamiento funcional requiere las pruebas {intrapara_profile}')
    return load_refinements(raw,path)
