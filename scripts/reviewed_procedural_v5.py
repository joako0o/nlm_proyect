"""Seis continuidades de conducción revisadas; ninguna excepción léxica global.

Se aplican DESPUÉS del motor histórico. No alteran segmentación, fuentes, anclas
ni propagación. La evidencia exige los grupos completos de la base v4 inmutable.
"""
import argparse
import collections
import csv
import hashlib
import json
import os
from pathlib import Path
from diagnosticar_finales import read_rows
from revisar_cola_comas import parent_signature, compact, sha
from auditar_continuidad_turnos import inventory, group_signature, window

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/releases/funcional_v4/consolidado_base_referencia.xlsx'
BASE_SHA='a8038f8c18933990a84a870fb607f2053e8daccc0dbea634dc612635fe41a5df'
READINGS=ROOT/'docs/continuidad_lote5_2026-09-09/lecturas.json'
PRIOR=ROOT/'docs/continuidad_lote4_2026-09-09/lecturas.json'
PRIOR_SHA='5f0a7e58a8134f46aa6ec7d01cb2aa7610ce3b011341b9d889564822a7e22a8f'
PATH=ROOT/'data/curation/continuidades_procedimentales_v5.json'
FUNCTIONAL_SHA='d636f4a6f33bdef932956ca13834f247daf6cafd5d54bcb50440283a701220b8'
RELATION='CONTINUIDAD_PROCEDIMENTAL_REVISADA'
PAIRS=(('RPM-2007-12-13:1603:1','RPM-2007-12-13:1604:1'),
       ('RPM-2008-01-10:1630:1','RPM-2008-01-10:1631:1'),
       ('RPM-2008-05-08:1840:1','RPM-2008-05-08:1841:1'),
       ('RPM-2008-12-11:2203:1','RPM-2008-12-11:2204:1'),
       ('RPM-2010-07-15:3269:2','RPM-2010-07-15:3270:1'),
       ('RPM-2010-09-16:3421:5','RPM-2010-09-16:3421:6'))
PARENTS={1603,1604,1630,1631,1840,1841,2202,2203,2204,3269,3270,3421}


def file_sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def snapshot(row):
    return {k:(str(v)[:10] if k=='Fecha' else v) for k,v in row.items()}


def validate_readings(rows,pkg,raw):
    try:
        if (type(pkg['Version']) is not int or pkg['Version']!=5
                or pkg['Alcance']!='CONTINUIDAD_PROCEDIMENTAL_SEIS_PARES'
                or pkg['SHA256_Base']!=BASE_SHA or pkg['SHA256_Grupos']!=group_signature(rows)
                or pkg['SHA256_Lecturas_Lote4']!=PRIOR_SHA or file_sha(PRIOR)!=PRIOR_SHA
                or set(pkg['Padres'])!={str(p) for p in PARENTS}
                or set(pkg['Casos'])!={a for a,b in PAIRS}):
            raise ValueError('Lectura procedimental fuera de alcance/baseline')
        positions={r['ID_Intervencion']:i for i,r in enumerate(rows)}
        if len(positions)!=len(rows):raise ValueError('IDs repetidos')
        for p,e in pkg['Padres'].items():
            inds=[i for i,r in enumerate(rows) if r['ID_Padre']==int(p)]
            if not inds or inds!=list(range(inds[0],inds[-1]+1)) or inds[0]==0 or inds[-1]+1>=len(rows):
                raise ValueError('Padre ausente/discontinuo/sin contexto')
            rs=rows[inds[0]:inds[-1]+1]
            if (e['Lectura']!='PADRE_COMPLETO_EN_PARTICION_LITERAL'
                    or e['Fecha']!=str(raw[int(p)]['Fecha'])[:10]
                    or e['Texto_Padre']!=raw[int(p)]['Texto']
                    or e['SHA256_Texto_Padre']!=sha(e['Texto_Padre'])
                    or e['SHA256_Particion']!=parent_signature(rs)
                    or compact(e['Texto_Padre'])!=compact(''.join(r['Texto'] for r in rs))
                    or e['Vecino_Anterior']!=window(rows[inds[0]-1],True)
                    or e['Vecino_Siguiente']!=window(rows[inds[-1]+1])):
                raise ValueError('Lectura, fuente, partición o ventana alterada')
        prior=json.loads(PRIOR.read_text());covered=set()
        inv={(e['Izquierda'],e['Derecha']) for e in inventory(rows)}
        for left,right in PAIRS:
            e=pkg['Casos'][left];a,b=rows[positions[left]:positions[left]+2]
            groups={s:[snapshot(r) for r in rows if r['ID_Turno']==end['ID_Turno']]
                    for s,end in [('Izquierda',a),('Derecha',b)]}
            if (b['ID_Intervencion']!=right or e['Derecha']!=right or (left,right) not in inv
                    or e['Decision']!='AGRUPAR_CONDUCCION_CONTIGUA_REVISADA'
                    or e['Reserva_Anterior']!=prior['Casos'][left]['Decision']
                    or not e['Justificacion'] or not e['Limitacion'] or e['Grupos_Leidos']!=groups
                    or a['Actor_Final']!='José De Gregorio Rebeco' or a['Actor_Final']!=b['Actor_Final']
                    or any(r['Tipo_Acta'] or r['Motivos_Revision'] for r in (a,b))):
                raise ValueError('Extremos, grupos o decisión alterados')
            covered.update(r['ID_Padre'] for g in groups.values() for r in g)
        if covered!=PARENTS:raise ValueError('Miembros no leídos')
    except (KeyError,TypeError,IndexError) as exc:
        raise ValueError('Paquete de lectura incompleto') from exc


def load_reviews(raw,path=PATH):
    pkg=json.loads(Path(path).read_text())
    if (not isinstance(pkg,dict) or type(pkg.get('Version')) is not int or pkg['Version']!=5
            or pkg.get('Perfil')!='procedimental-v5' or pkg.get('Pares')!=[list(p) for p in PAIRS]
            or pkg.get('SHA256_Base')!=BASE_SHA or file_sha(BASE)!=BASE_SHA
            or pkg.get('SHA256_Lecturas')!=file_sha(READINGS)
            or pkg.get('SHA256_Registro_Funcional_V4')!=FUNCTIONAL_SHA
            or file_sha(ROOT/'data/curation/refinamiento_funcional_v4.json')!=FUNCTIONAL_SHA):
        raise ValueError('Registro procedimental/versiones incompatibles')
    readings=json.loads(READINGS.read_text());validate_readings(read_rows(BASE),readings,raw)
    return {(left,right):readings['Casos'][left] for left,right in PAIRS}


def active_reviews(raw,intrapara_profile=None):
    path=os.environ.get('NLM_PROCEDURAL_REVIEWS')
    if not path:return {}
    from intrapara_profiles import profile_name, required_intrapara
    intra=os.environ.get('NLM_INTRAPARA_REVIEWS');functional=os.environ.get('NLM_FUNCTIONAL_REVIEWS')
    intrapara_profile=required_intrapara(intrapara_profile)
    if (not intra or profile_name(intra)!=intrapara_profile
            or not functional or file_sha(functional)!=FUNCTIONAL_SHA):
        raise ValueError(f'procedimental requiere refinamiento v4 y pruebas {intrapara_profile}')
    return load_reviews(raw,path)


def _same_content(row,want):
    # Antes de exportar XLSX los vacíos son ''; después, None. Sólo normalizar eso.
    actual=snapshot(row)
    return all((actual.get(k) if actual.get(k) is not None else '') == (v if v is not None else '')
               for k,v in want.items() if k not in ('ID_Turno','Relacion_Turno','ID_Antecedente_Continuidad'))


def matching_review(previous,row,reviews):
    if not previous:return None
    e=(reviews or {}).get((previous.get('ID_Intervencion'),row.get('ID_Intervencion')))
    if e and _same_content(previous,e['Grupos_Leidos']['Izquierda'][-1]) and _same_content(row,e['Grupos_Leidos']['Derecha'][0]):
        return e
    return None


def apply_reviews(rows,reviews):
    if not reviews:return rows
    if set(reviews)!=set(PAIRS):raise ValueError('Sólo se aplican las seis pruebas completas')
    idx={r['ID_Intervencion']:i for i,r in enumerate(rows)};mapping={}
    for left,right in PAIRS:
        a,b=rows[idx[left]:idx[left]+2];e=matching_review(a,b,reviews)
        if not e or b['ID_Intervencion']!=right or a['ID_Turno']==b['ID_Turno']:
            raise ValueError('Prueba no coincide o ya aplicada')
        for side,end in [('Izquierda',a),('Derecha',b)]:
            got=[r for r in rows if r['ID_Turno']==end['ID_Turno']];want=e['Grupos_Leidos'][side]
            if (len(got)!=len(want) or any(not _same_content(r,w) for r,w in zip(got,want))
                    or any((r.get('Relacion_Turno'),r.get('ID_Antecedente_Continuidad') or '')!=
                           (w['Relacion_Turno'],w['ID_Antecedente_Continuidad'] or '') for r,w in zip(got,want))):
                raise ValueError('Grupo inicial no coincide con la lectura completa')
        mapping[b['ID_Turno']]=a['ID_Turno']
    for left,right in PAIRS:
        rows[idx[right]].update(Relacion_Turno=RELATION,ID_Antecedente_Continuidad=left)
    labels={};counts=collections.Counter()
    for r in rows:
        key=mapping.get(r['ID_Turno'],r['ID_Turno']);date=str(r['Fecha'])[:10]
        if key not in labels:
            counts[date]+=1;labels[key]=f'RPM-{date}:T{counts[date]}'
        r['ID_Turno']=labels[key]
    errors=validate_reviews(rows,reviews)
    if errors:raise ValueError(errors)
    return rows


def validate_reviews(rows,reviews):
    errors=[];seen=set();previous=None
    for r in rows:
        e=matching_review(previous,r,reviews)
        if e:
            key=(previous['ID_Intervencion'],r['ID_Intervencion']);seen.add(key)
            want=[x['ID_Intervencion'] for side in ['Izquierda','Derecha'] for x in e['Grupos_Leidos'][side]]
            got=[x['ID_Intervencion'] for x in rows if x['ID_Turno']==r['ID_Turno']]
            if (r['Relacion_Turno']!=RELATION or r['ID_Antecedente_Continuidad']!=key[0]
                    or r['ID_Turno']!=previous['ID_Turno'] or got!=want):
                errors.append(f'{key}: enlace o membresía procedimental incorrectos')
        elif r.get('Relacion_Turno')==RELATION:
            errors.append(f'{r["ID_Intervencion"]}: relación procedimental sin prueba exacta')
        previous=r
    if seen!=set(reviews or {}):errors.append('Faltan pruebas procedimentales aplicables')
    return errors


def export_inventory(output):
    """Lectura/inventario reproducibles antes de aplicación; jamás escribe data/."""
    output=output.resolve()
    if output.exists() or not any((ROOT/r).resolve() in output.parents for r in ('.cache','docs')):
        raise ValueError('Usar destino nuevo bajo .cache/ o docs/')
    raw={r['ID']:r for r in read_rows(ROOT/'data/raw/consolidado_final.xlsx')};reviews=load_reviews(raw)
    rows=read_rows(BASE);old=read_rows(ROOT/'data/releases/continuidad_intrapadre_v3'/BASE.name)
    inv=[{**e,'Decision_Lote5':reviews.get((e['Izquierda'],e['Derecha']),{}).get('Decision','FUERA_DE_ESTE_LOTE')}
         for e in inventory(rows)]
    oldpairs={(e['Izquierda'],e['Derecha']) for e in inventory(old)};newpairs={(e['Izquierda'],e['Derecha']) for e in inv}
    summary=dict(Pares_V3=len(oldpairs),Pares_V4=len(newpairs),Pares_Comunes=len(oldpairs&newpairs),
                 Retirados_Desde_V3=sorted(oldpairs-newpairs),Nuevos_Desde_V3=sorted(newpairs-oldpairs),
                 Pares_Leidos=6,Padres_Completos=12,Caracteres_Leidos=sum(len(raw[p]['Texto']) for p in PARENTS),
                 Fuera_De_Este_Lote=len(inv)-6,Enlaces_Aprobados=6,Aplicacion='Sólo el perfil procedimental-v5; este exportador no modifica datos')
    decisions=[dict(Izquierda=l,Derecha=r,Decision=e['Decision'],Justificacion=e['Justificacion'],Limitacion=e['Limitacion']) for (l,r),e in reviews.items()]
    output.mkdir(parents=True)
    for name,values in [('inventario_v4.csv',inv),('decisiones.csv',decisions)]:
        with (output/name).open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(values[0]),quoting=csv.QUOTE_ALL);writer.writeheader();writer.writerows(values)
    (output/'resumen_lectura.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--salida',type=Path,required=True)
    print(json.dumps(export_inventory(parser.parse_args().salida),ensure_ascii=False,indent=2))
