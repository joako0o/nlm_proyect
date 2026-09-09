"""Comparación global contra v3: tres refinamientos y sólo tres continuidades.

El esperado se deriva del histórico firmado y de la lectura, NO del constructor
ni de las filas candidatas. Compara cada campo y la membresía de TODOS los grupos.
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
from functional_refinements import BASE, BASE_SHA, ROOT, PATH, load_refinements, validate_refinements
from diagnosticar_finales import read_rows


def expected_rows(before,reviews):
    by_id={r['ID_Intervencion']:r for r in before}
    expected=[];lineage=[];rename={}
    for old in before:
        p=old['ID_Padre'];e=reviews.get(p);num=old['Numero_Segmento']
        if e and num==1:
            if old['Texto']!=e['Texto_Original']:
                raise ValueError('Baseline no coincide con el registro')
            previous=by_id[e['ID_Anterior']]
            a={**old,'Texto':e['Texto_Personal'],'Tipo_Acta':None,
               'Estado_Revision':'SIN_ALERTAS_AUTOMATICAS','Motivos_Revision':None,
               'ID_Turno':previous['ID_Turno'],'Relacion_Turno':'CONTINUIDAD_EXPLICITA',
               'ID_Antecedente_Continuidad':previous['ID_Intervencion'],'ID_Ancla_Actor':old['ID_Intervencion']}
            b={**old,'Texto':e['Texto_Constancia'],'Numero_Segmento':2,
               'ID_Intervencion':old['ID_Intervencion'].rsplit(':',1)[0]+':2',
               'ID_Bloque_Texto':old['ID_Bloque_Texto'].rsplit('B',1)[0]+'B2'}
            if p in (4849,4899):
                b.update(Duplicado_Exacto='SI',Estado_Revision='PENDIENTE_REVISION',Motivos_Revision='DUPLICADO_NO_FORMULA')
            #4788 conserva exactamente FINAL_SIN_PUNTUACION en el pie, no en el aporte.
            parts=[('PERSONAL',a,0,len(a['Texto'])),('CONSTANCIA',b,len(a['Texto'])+len(e['Separador']),len(old['Texto']))]
        else:
            r=dict(old)
            if e:
                r.update(Numero_Segmento=num+1,
                         ID_Intervencion=old['ID_Intervencion'].rsplit(':',1)[0]+f':{num+1}',
                         ID_Bloque_Texto=old['ID_Bloque_Texto'].rsplit('B',1)[0]+f'B{int(old["ID_Bloque_Texto"].rsplit("B",1)[1])+1}')
            rename[old['ID_Intervencion']]=r['ID_Intervencion']
            parts=[('INTEGRA',r,0,len(r['Texto']))]
        for kind,r,start,end in parts:
            r['ID']=len(expected)+1;expected.append(r)
            lineage.append(dict(ID_Anterior=old['ID_Intervencion'],ID_Nuevo=r['ID_Intervencion'],
                                ID_Padre=p,Parte=kind,Inicio_En_Fila_Anterior=start,Fin_En_Fila_Anterior=end,
                                SHA256_Texto=hashlib.sha256(r['Texto'].encode()).hexdigest()))
    for r in expected:
        for key in ('ID_Ancla_Actor','ID_Antecedente_Continuidad'):
            r[key]=rename.get(r[key],r[key])
    return expected,lineage


def members(rows):
    groups=collections.defaultdict(list)
    for r in rows:groups[r['ID_Turno']].append(r['ID_Intervencion'])
    return dict(groups)


def compare(before,after,reviews):
    want,lineage=expected_rows(before,reviews)
    if len(after)!=len(want):raise ValueError('Cardinalidad distinta del refinamiento aprobado')
    for n,(a,b) in enumerate(zip(want,after),1):
        if a!=b:
            fields=[k for k in set(a)|set(b) if a.get(k)!=b.get(k)]
            raise ValueError(f'Fila {n}: campos no autorizados: {fields}')
    if members(want)!=members(after):raise ValueError('Membresía global modificada')
    errors=validate_refinements(after,reviews)
    if errors:raise ValueError(errors)
    report=dict(Perfil='funcional-v4',Baseline='intrapadre-v3',Pasa=True,
                Filas_Antes=len(before),Filas_Despues=len(after),Refinamientos=3,Continuidades_Personales=3,
                Grupos_Antes=len(members(before)),Grupos_Despues=len(members(after)),
                Comparacion='Todas las filas, todos los campos y todos los miembros de cada grupo; sin excepciones globales',
                Alertas_Antes=sum(bool(r['Motivos_Revision']) for r in before),
                Alertas_Despues=sum(bool(r['Motivos_Revision']) for r in after),
                Padres_Con_Alertas=len({r['ID_Padre'] for r in after if r['Motivos_Revision']}),
                Nuevas_Alertas=['RPM-2012-05-17:4849:2','RPM-2012-06-14:4899:2'],
                Motivo_Nuevo='DUPLICADO_NO_FORMULA: dos constancias idénticas, no se elimina texto ni se declara error',
                Alertas_Cerradas=0,Alerta_Desplazada={'Desde':'RPM-2012-04-17:4788:1','Hasta':'RPM-2012-04-17:4788:2','Motivo':'FINAL_SIN_PUNTUACION'},
                SHA256_Baseline=BASE_SHA,SHA256_Registro=hashlib.sha256(PATH.read_bytes()).hexdigest())
    return report,lineage


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate',type=Path,required=True);args=parser.parse_args()
    raw={r['ID']:r for r in read_rows(ROOT/'data/raw/consolidado_final.xlsx')}
    reviews=load_refinements(raw)
    target=args.candidate/BASE.name
    report,lineage=compare(read_rows(BASE),read_rows(target),reviews)
    report['SHA256_Candidato']=hashlib.sha256(target.read_bytes()).hexdigest()
    with (args.candidate/'linaje_funcional.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(lineage[0]),quoting=csv.QUOTE_ALL)
        writer.writeheader();writer.writerows(lineage)
    (args.candidate/'comparacion_funcional.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
