"""Lote6 de lectura/triage sobre v5: no aplica enlaces ni escribe en data/."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
from diagnosticar_finales import read_rows
from auditar_continuidad_turnos import inventory, group_signature, window
from revisar_cola_comas import parent_signature, endpoint, compact, sha
from revisar_continuidad_barreras import CASES as LOTE4_CASES

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/releases/continuidad_procedimental_v5/consolidado_base_referencia.xlsx'
BASE_SHA='4da18c4e86f583fdf4d5d0cd9be49b9aac20fb40379cd391b5f4c7763cf9e168'
READINGS=ROOT/'docs/continuidad_lote6_2026-09-09/lecturas.json'
PRIOR3=ROOT/'docs/continuidad_lote3_2026-09-09/lecturas.json'
PRIOR4=ROOT/'docs/continuidad_lote4_2026-09-09/lecturas.json'
FUNCTIONAL=ROOT/'data/curation/refinamiento_funcional_v4.json'
PARENTS={780,2661,2863,2864,3646,5252}
CASES={'RPM-2006-07-13:780:2':('RPM-2006-07-13:780:3','RESERVA_COTEJO_INICIO'),
       'RPM-2009-08-13:2661:6':('RPM-2009-08-13:2661:7','RESERVA_CONFIRMACION_NARRADA'),
       'RPM-2010-01-14:2863:2':('RPM-2010-01-14:2863:3','PROPUESTA_LOCAL_NO_APLICADA'),
       'RPM-2011-01-13:3646:2':('RPM-2011-01-13:3646:3','PROPUESTA_LOCAL_NO_APLICADA'),
       'RPM-2012-12-13:5252:3':('RPM-2012-12-13:5252:4','RESERVA_LIMITE_ACTA_PERSONA')}
SOURCES={str(p.relative_to(ROOT)) for p in (BASE,ROOT/'data/raw/consolidado_final.xlsx',PRIOR3,PRIOR4,FUNCTIONAL,ROOT/'docs/continuidad_lote5_2026-09-09/lecturas.json')}


def snapshot(row):return {k:(str(v)[:10] if k=='Fecha' else v) for k,v in row.items()}


def validate(rows,pkg,raw=None):
    """Exige baseline, fuentes, padres enteros, grupos y decisiones cerrados."""
    try:
        if (type(pkg['Version']) is not int or pkg['Version']!=1
                or pkg['Alcance']!='LECTURA_RESERVAS_LOTE6_SIN_APLICAR'
                or set(pkg['SHA256_Fuentes'])!=SOURCES
                or pkg['SHA256_Fuentes'][str(BASE.relative_to(ROOT))]!=BASE_SHA
                or pkg['SHA256_Grupos']!=group_signature(rows)
                or set(pkg['Padres'])!={str(p) for p in PARENTS} or set(pkg['Casos'])!=set(CASES)):
            raise ValueError('Lote/baseline/fuentes fuera de alcance')
        for source in SOURCES:
            if hashlib.sha256((ROOT/source).read_bytes()).hexdigest()!=pkg['SHA256_Fuentes'][source]:
                raise ValueError('Fuente o ficha histórica modificada')
        if raw is None:raw={r['ID']:r for r in read_rows(ROOT/'data/raw/consolidado_final.xlsx')}
        idx={r['ID_Intervencion']:i for i,r in enumerate(rows)}
        if len(idx)!=len(rows):raise ValueError('IDs repetidos')
        for p,e in pkg['Padres'].items():
            ids=[i for i,r in enumerate(rows) if r['ID_Padre']==int(p)]
            if not ids or ids!=list(range(ids[0],ids[-1]+1)) or ids[0]==0 or ids[-1]+1>=len(rows):
                raise ValueError('Padre incompleto o sin vecinos')
            pr=rows[ids[0]:ids[-1]+1]
            if (e['Lectura']!='PADRE_COMPLETO_EN_PARTICION_LITERAL'
                    or e['Fecha']!=str(raw[int(p)]['Fecha'])[:10]
                    or e['Texto_Padre']!=raw[int(p)]['Texto'] or e['SHA256_Texto_Padre']!=sha(e['Texto_Padre'])
                    or e['SHA256_Particion']!=parent_signature(pr)
                    or compact(e['Texto_Padre'])!=compact(''.join(r['Texto'] for r in pr))
                    or e['Vecino_Anterior']!=window(rows[ids[0]-1],True)
                    or e['Vecino_Siguiente']!=window(rows[ids[-1]+1])):
                raise ValueError('Fuente, partición o ventana alterada')
        prior=json.loads(PRIOR3.read_text());covered=set()
        inv={(r['Izquierda'],r['Derecha']) for r in inventory(rows)}
        for left,(right,state) in CASES.items():
            e=pkg['Casos'][left];a,b=rows[idx[left]:idx[left]+2]
            groups={side:[snapshot(r) for r in rows if r['ID_Turno']==end['ID_Turno']]
                    for side,end in [('Izquierda',a),('Derecha',b)]}
            if (b['ID_Intervencion']!=right or e['Derecha']!=right or (left,right) not in inv
                    or e['Estado']!=state or e['Aplicado'] is not False
                    or e['Estado_Anterior']!=prior['Casos'][left]['Decision']
                    or e['Grupos_Leidos']!=groups or not all(e[k] for k in ['Justificacion','Siguiente_Accion','Limite'])):
                raise ValueError('Par, estado, aplicación o grupo cambiado')
            covered.update(r['ID_Padre'] for g in groups.values() for r in g)
        if covered!=PARENTS:raise ValueError('Faltan padres de miembros de grupo')
        inherited_statuses(rows)  # Comprobar también las13 separaciones heredadas.
    except (KeyError,TypeError,IndexError) as exc:
        raise ValueError('Paquete incompleto') from exc


def inherited_statuses(rows):
    """Respaldo anterior, NO una nueva lectura completa de estos trece pares."""
    idx={r['ID_Intervencion']:r for r in rows};prior=json.loads(PRIOR4.read_text());result={}
    for left,(right,state) in LOTE4_CASES.items():
        if not state.startswith('SEPARAR_'):continue
        e=prior['Casos'][left]
        if e['Derecha']!=right or e['Decision']!=state:raise ValueError('Decisión heredada alterada')
        for side,rid in [('Izquierda',left),('Derecha',right)]:
            want=next(r for r in e['Grupos_Leidos'][side] if r['ID_Intervencion']==rid)
            if endpoint(idx[rid])!={k:want[k] for k in endpoint(idx[rid])}:
                raise ValueError('Extremo de separación histórica alterado')
        result[left]=(right,'SEPARACION_RESPALDADA_PREVIAMENTE','docs/continuidad_lote4_2026-09-09/lecturas.json')
    functional=json.loads(FUNCTIONAL.read_text())
    for e in functional['Revisiones'].values():
        left=e['ID_Fila_Original'];right=left.rsplit(':',1)[0]+':2';a,b=idx[left],idx[right]
        if (a['Texto']!=e['Texto_Personal'] or b['Texto']!=e['Texto_Constancia']
                or a['Actor_Final']!=e['Actor'] or b['Actor_Final']!=e['Actor']
                or a['Tipo_Acta'] or b['Tipo_Acta']!='ACUERDO_CONSEJO'):
            raise ValueError('Refinamiento funcional anterior alterado')
        result[left]=(right,'SEPARACION_FUNCIONAL_V4','data/curation/refinamiento_funcional_v4.json')
    inv={(r['Izquierda'],r['Derecha']) for r in inventory(rows)}
    if len(result)!=13 or any((left,e[0]) not in inv for left,e in result.items()):
        raise ValueError('Falta una separación respaldada')
    return result


def exports(rows,pkg):
    validate(rows,pkg);prior=inherited_statuses(rows);result=[]
    for r in inventory(rows):
        left=r['Izquierda'];e=pkg['Casos'].get(left)
        if e:
            state=e['Estado'];source=str(READINGS.relative_to(ROOT));read='PADRES_Y_GRUPOS_COMPLETOS_EN_LOTE6'
            action=e['Siguiente_Accion']
        elif left in prior:
            _,state,source=prior[left];read='RESPALDO_ANTERIOR_NO_RELECTURA_EN_LOTE6'
            action='Mantener separación; no tratarla como un enlace pendiente.'
        else:
            state='SIN_ADJUDICACION_EN_ESTE_INVENTARIO';source='';read='NO_EVALUADO_EN_ESTE_LOTE_NO_EQUIVALE_A_NUNCA_LEIDO'
            action='Localizar fichas previas y comprobar su alcance antes de decidir una nueva lectura.'
        result.append({**r,'Estado_Revision_Dirigida':state,'Alcance_Lectura':read,'Evidencia':source,'Siguiente_Accion':action,'Enlace_Aplicado_Lote6':'NO'})
    decisions=[dict(Izquierda=l,Derecha=e['Derecha'],Estado=e['Estado'],Estado_Anterior=e['Estado_Anterior'],
                    Aplicado='NO',Justificacion=e['Justificacion'],Siguiente_Accion=e['Siguiente_Accion']) for l,e in pkg['Casos'].items()]
    blockers=[r for r in decisions if r['Estado'].startswith('RESERVA_')]
    estados=collections.Counter(r['Estado_Revision_Dirigida'] for r in result)
    sin=estados['SIN_ADJUDICACION_EN_ESTE_INVENTARIO']
    summary=dict(Pares_Inventariados=len(result),Estados=dict(estados),
                 Pares_Releidos=5,Padres_Completos=len(pkg['Padres']),Caracteres_Origen=sum(len(e['Texto_Padre']) for e in pkg['Padres'].values()),
                 Propuestas_No_Aplicadas=2,Reservas=3,Enlaces_Aplicados=0,Cortes_Aplicados=0,Alertas_Cerradas=0,
                 Filas=len(rows),Grupos=len({r['ID_Turno'] for r in rows}),Filas_Alertadas=sum(bool(r['Motivos_Revision']) for r in rows),
                 Nota=(f'Las {sin} filas sin adjudicación en este inventario no son {sin} errores ni {sin} casos '
                       'nunca leídos. No estima cobertura semántica del corpus.'))
    return result,decisions,blockers,summary


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--salida',type=Path,required=True)
    out=parser.parse_args(argv).salida.resolve()
    if out.exists() or not any((ROOT/r).resolve() in out.parents for r in ('.cache','docs')):
        raise ValueError('Se requiere destino nuevo bajo .cache/ o docs/, nunca data/')
    pkg=json.loads(READINGS.read_text());rows=read_rows(BASE);inv,dec,block,summary=exports(rows,pkg)
    out.mkdir(parents=True)
    for name,data in [('inventario_estado.csv',inv),('decisiones.csv',dec),('reservas_y_siguiente_accion.csv',block)]:
        with (out/name).open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(data[0]),quoting=csv.QUOTE_ALL);writer.writeheader();writer.writerows(data)
    (out/'resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
