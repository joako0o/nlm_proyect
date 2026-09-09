"""Lote4: lectura de barreras/filas mixtas; no modifica datos ni aplica enlaces."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from auditar_continuidad_turnos import inventory, group_signature, window
from revisar_cola_comas import parent_signature, endpoint, check_sources, compact, sha
from diagnosticar_finales import read_rows

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'data/releases/continuidad_intrapadre_v3/consolidado_base_referencia.xlsx'
BASE_SHA = 'b4a169701c212c15f302b5c3c572eae65e3d4de8d6a71d38754ccec4606aa992'
READINGS = ROOT/'docs/continuidad_lote4_2026-09-09/lecturas.json'
PRIOR = ROOT/'docs/continuidad_lote3_2026-09-09/lecturas.json'
MARKER = 'En consecuencia, el Presidente señor Rodrigo Vergara deja constancia que se acuerda por unanimidad'
CASES = {'RPM-2007-12-13:1603:1': ('RPM-2007-12-13:1604:1',
                           'RESERVA_CESIONES_CONSECUTIVAS'),
 'RPM-2008-01-10:1630:1': ('RPM-2008-01-10:1631:1',
                           'RESERVA_CESIONES_CONSECUTIVAS'),
 'RPM-2008-05-08:1840:1': ('RPM-2008-05-08:1841:1',
                           'RESERVA_CESIONES_CONSECUTIVAS'),
 'RPM-2008-12-11:2203:1': ('RPM-2008-12-11:2204:1', 'RESERVA_CESION_REITERADA'),
 'RPM-2010-01-14:2875:1': ('RPM-2010-01-14:2875:2', 'SEPARAR_POR_PAUSA'),
 'RPM-2010-02-11:2958:1': ('RPM-2010-02-11:2958:2', 'SEPARAR_POR_PAUSA'),
 'RPM-2010-03-18:3008:1': ('RPM-2010-03-18:3008:2', 'SEPARAR_POR_PAUSA'),
 'RPM-2010-05-13:3109:1': ('RPM-2010-05-13:3109:2', 'SEPARAR_POR_PAUSA'),
 'RPM-2010-06-15:3193:1': ('RPM-2010-06-15:3193:2', 'SEPARAR_POR_PAUSA'),
 'RPM-2010-07-15:3269:1': ('RPM-2010-07-15:3269:2', 'SEPARAR_POR_PAUSA'),
 'RPM-2010-07-15:3269:2': ('RPM-2010-07-15:3270:1',
                           'RESERVA_REANUDACION_Y_CESION'),
 'RPM-2010-08-12:3328:1': ('RPM-2010-08-12:3328:2', 'SEPARAR_POR_PAUSA'),
 'RPM-2010-09-16:3421:4': ('RPM-2010-09-16:3421:5', 'SEPARAR_POR_PAUSA'),
 'RPM-2010-09-16:3421:5': ('RPM-2010-09-16:3421:6',
                           'RESERVA_REANUDACION_Y_RECONOCIMIENTO'),
 'RPM-2010-11-16:3572:1': ('RPM-2010-11-16:3572:2', 'SEPARAR_POR_PAUSA'),
 'RPM-2011-09-15:4332:1': ('RPM-2011-09-15:4333:1',
                           'SEPARAR_VOTO_Y_CONSTANCIA'),
 'RPM-2012-04-17:4787:2': ('RPM-2012-04-17:4788:1', 'RESERVA_TRAMO_MIXTO'),
 'RPM-2012-05-17:4848:1': ('RPM-2012-05-17:4849:1', 'RESERVA_TRAMO_MIXTO'),
 'RPM-2012-06-14:4898:1': ('RPM-2012-06-14:4899:1', 'RESERVA_TRAMO_MIXTO')}
PARENTS = {3328, 2958, 2202, 2203, 2204, 4898, 4899, 3108, 3109, 1840, 1841, 4787, 4788, 2875, 3008, 1603, 1604, 3269, 3270, 3421, 1630, 1631, 4332, 4333, 4848, 4849, 3571, 3572, 3193}


def select(rows):
    inv = inventory(rows)
    return [e for e in inv if 'BARRERA_LEXICA_IZQUIERDA' in e['Indicadores']] + [
        e for e in inv if e['Indicadores'] == 'TIPO_ACTA_O_DOCUMENTO'][:4]


def functional_boundary(row, raw_text):
    text = row['Texto']
    if text.count(MARKER) != 1 or raw_text.count(text) != 1:
        raise ValueError('Límite funcional no unívoco')
    pos = text.index(MARKER)
    return dict(ID_Intervencion=row['ID_Intervencion'],Inicio_Fila_En_Padre=raw_text.index(text),
                Posicion_En_Fila=pos,Prefijo_Personal=text[:pos],Constancia_Y_Residuo=text[pos:],
                SHA256_Fila=sha(text),Alcance='PROPUESTA_FUNCIONAL_NO_APLICADA_NO_CAMBIO_DE_HABLANTE')


def validate(rows, package, raw=None):
    """Verifica todos los miembros y padres; el estado no autoriza modificaciones."""
    try:
        if (type(package['Version']) is not int or package['Version'] != 1
                or package['Alcance'] != 'CONTINUIDAD_LOTE4_SIN_APLICAR'
                or set(package['Casos']) != set(CASES)
                or set(package['Padres']) != {str(p) for p in PARENTS}
                or {e['Izquierda'] for e in select(rows)} != set(CASES)
                or package['SHA256_Grupos'] != group_signature(rows)
                or package['SHA256_Fuentes'].get(str(BASE.relative_to(ROOT))) != BASE_SHA
                or package['SHA256_Lecturas_Lote3'] != hashlib.sha256(PRIOR.read_bytes()).hexdigest()):
            raise ValueError('Lote, selección, historial o baseline incompatible')
        check_sources(package)
        if raw is None:
            raw = {r['ID']:r for r in read_rows(ROOT/'data/raw/consolidado_final.xlsx')}
        for p,e in package['Padres'].items():
            ids = [i for i,r in enumerate(rows) if r['ID_Padre'] == int(p)]
            if not ids or ids != list(range(ids[0],ids[-1]+1)):
                raise ValueError('Padre ausente o discontinuo')
            i,j = ids[0],ids[-1]+1
            if i == 0 or j >= len(rows):
                raise ValueError('Falta contexto externo')
            pr = rows[i:j]
            if (e['Lectura'] != 'PADRE_COMPLETO_EN_PARTICION_LITERAL'
                    or e['Texto_Padre'] != raw[int(p)]['Texto']
                    or e['Fecha'] != str(raw[int(p)]['Fecha'])[:10]
                    or e['Fecha'] != str(pr[0]['Fecha'])[:10]
                    or e['SHA256_Texto_Padre'] != sha(e['Texto_Padre'])
                    or e['SHA256_Particion'] != parent_signature(pr)
                    or compact(e['Texto_Padre']) != compact(''.join(r['Texto'] for r in pr))
                    or e['Vecino_Anterior'] != window(rows[i-1],True)
                    or e['Vecino_Siguiente'] != window(rows[j])):
                raise ValueError('Fuente, partición o ventana modificada')
        positions = {r['ID_Intervencion']:i for i,r in enumerate(rows)}
        if len(positions) != len(rows):
            raise ValueError('ID de intervención duplicado')
        covered = set()
        for left,(right,state) in CASES.items():
            e = package['Casos'][left]
            a,b = rows[positions[left]:positions[left]+2]
            groups = {side:[r for r in rows if r['ID_Turno'] == end['ID_Turno']]
                      for side,end in [('Izquierda',a),('Derecha',b)]}
            snapshots = {side:[{**endpoint(r),'SHA256_Fila':parent_signature([r])} for r in g]
                         for side,g in groups.items()}
            covered.update(r['ID_Padre'] for g in groups.values() for r in g)
            if (b['ID_Intervencion'] != right or e['Derecha'] != right or e['Decision'] != state
                    or not e['Justificacion'] or not e['Reservas'] or e['Grupos_Leidos'] != snapshots):
                raise ValueError('Extremos, miembros, decisión o justificación modificados')
            if state == 'RESERVA_TRAMO_MIXTO':
                if e.get('Limite_Funcional_No_Aplicado') != functional_boundary(b,raw[b['ID_Padre']]['Texto']):
                    raise ValueError('Propuesta funcional no coincide con el literal')
            elif 'Limite_Funcional_No_Aplicado' in e:
                raise ValueError('Propuesta fuera de alcance')
        if covered != PARENTS:
            raise ValueError('Padres de miembros no leídos')
    except (KeyError,TypeError,IndexError) as exc:
        raise ValueError('Lote incompleto') from exc


def exports(rows, package):
    validate(rows,package)
    prior = json.loads(PRIOR.read_text())['Casos']
    inv = [{**e,'Estado_Lote4':package['Casos'].get(e['Izquierda'],{}).get('Decision','FUERA_DE_ESTE_LOTE'),
            'Reserva_Lote3':prior.get(e['Izquierda'],{}).get('Decision','SIN_FICHA_EN_LOTE3')}
           for e in inventory(rows)]
    decisions = [dict(Izquierda=k,Derecha=e['Derecha'],Decision=e['Decision'],Justificacion=e['Justificacion'],
                      Aplicado='NO',Miembros_Leidos=';'.join(r['ID_Intervencion'] for g in e['Grupos_Leidos'].values() for r in g))
                 for k,e in package['Casos'].items()]
    proposals = [e['Limite_Funcional_No_Aplicado'] for e in package['Casos'].values() if 'Limite_Funcional_No_Aplicado' in e]
    summary = dict(Pares_Inventariados=len(inv),Casos_Leidos=len(decisions),Padres_Completos=len(package['Padres']),
                   Caracteres_Origen=sum(len(e['Texto_Padre']) for e in package['Padres'].values()),
                   Separaciones_Respaldadas=sum(e['Decision'].startswith('SEPARAR_') for e in decisions),
                   Reservas=sum(e['Decision'].startswith('RESERVA_') for e in decisions),
                   Limites_Funcionales_No_Aplicados=len(proposals),Enlaces_Aplicados=0,Cortes_Aplicados=0,Alertas_Cerradas=0,
                   Nota='El inventario sigue en77: revisión de un corte no elimina el par. No adjudica los58 pares fuera del lote4.')
    return inv,decisions,proposals,summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',type=Path,default=BASE)
    parser.add_argument('--lecturas',type=Path,default=READINGS)
    parser.add_argument('--salida',type=Path,required=True)
    args = parser.parse_args()
    dest = args.salida.resolve()
    allowed = (ROOT/'.cache', ROOT/'docs')
    if dest.exists() or not any(p.resolve() in dest.parents for p in allowed):
        raise ValueError('Usar un destino nuevo bajo .cache/ o docs/, nunca data/')
    if dest in (args.base.resolve(),args.lecturas.resolve()):
        raise ValueError('Destino coincide con entrada')
    if hashlib.sha256(args.base.read_bytes()).hexdigest() != BASE_SHA:
        raise ValueError('La base no es v3 inmutable')
    pkg = json.loads(args.lecturas.read_text())
    inv,decisions,proposals,summary = exports(read_rows(args.base),pkg)
    dest.mkdir(parents=True)
    for name,data in [('inventario.csv',inv),('decisiones.csv',decisions),('limites_no_aplicados.csv',proposals)]:
        with (dest/name).open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]),quoting=csv.QUOTE_ALL);w.writeheader();w.writerows(data)
    summary['SHA256_Base'] = BASE_SHA
    summary['SHA256_Lecturas'] = hashlib.sha256(args.lecturas.read_bytes()).hexdigest()
    (dest/'resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
