"""Lote3 cerrado: nueve enlaces y cinco reservas; todos los miembros leídos."""
import json
from pathlib import Path
from reviewed_intrapara_continuity import _load_bounded_links
from reviewed_intrapara_v2 import load_v2, ALLOWED as V2_PAIRS, PATH as V2_PATH
from auditar_continuidad_turnos import window, group_signature, inventory
from revisar_cola_comas import parent_signature, endpoint, check_sources, compact, sha
from diagnosticar_finales import read_rows

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/curation/continuidades_intrapadre_v3.json'
BASE = ROOT / 'data/releases/continuidad_intrapadre_v2/consolidado_base_referencia.xlsx'
READINGS = ROOT / 'docs/continuidad_lote3_2026-09-09/lecturas.json'
NEW_PAIRS = {('RPM-2007-02-08:1092:1', 'RPM-2007-02-08:1092:2'): (1092,
                                                      '2007-02-08',
                                                      'Esteban Jadresic '
                                                      'Marinovic'),
 ('RPM-2009-09-08:2695:2', 'RPM-2009-09-08:2695:3'): (2695,
                                                      '2009-09-08',
                                                      'Claudio Soto Gamboa'),
 ('RPM-2009-10-13:2754:2', 'RPM-2009-10-13:2754:3'): (2754,
                                                      '2009-10-13',
                                                      'Enrique Marshall '
                                                      'Rivera'),
 ('RPM-2009-11-12:2778:2', 'RPM-2009-11-12:2778:3'): (2778,
                                                      '2009-11-12',
                                                      'Claudio Soto Gamboa'),
 ('RPM-2009-11-12:2790:1', 'RPM-2009-11-12:2790:2'): (2790,
                                                      '2009-11-12',
                                                      'Claudio Soto Gamboa'),
 ('RPM-2009-12-15:2810:2', 'RPM-2009-12-15:2810:3'): (2810,
                                                      '2009-12-15',
                                                      'Sergio Lehmann Beresi'),
 ('RPM-2010-02-11:2909:3', 'RPM-2010-02-11:2909:4'): (2909,
                                                      '2010-02-11',
                                                      'Claudio Soto Gamboa'),
 ('RPM-2010-10-14:3439:2', 'RPM-2010-10-14:3439:3'): (3439,
                                                      '2010-10-14',
                                                      'Felipe Jaque'),
 ('RPM-2015-05-14:6800:2', 'RPM-2015-05-14:6800:3'): (6800,
                                                      '2015-05-14',
                                                      'Joaquín Vial '
                                                      'Ruiz-Tagle')}
CASES = {'RPM-2006-07-13:780:2': ('RPM-2006-07-13:780:3', 'RESERVA_LIMITE_PREVIO'),
 'RPM-2007-02-08:1092:1': ('RPM-2007-02-08:1092:2',
                           'ENLACE_RESPALDADO_POR_LECTURA'),
 'RPM-2009-08-13:2661:6': ('RPM-2009-08-13:2661:7',
                           'RESERVA_CONFIRMACION_NO_TRANSCRITA'),
 'RPM-2009-09-08:2695:2': ('RPM-2009-09-08:2695:3',
                           'ENLACE_RESPALDADO_POR_LECTURA'),
 'RPM-2009-10-13:2754:2': ('RPM-2009-10-13:2754:3',
                           'ENLACE_RESPALDADO_POR_LECTURA'),
 'RPM-2009-11-12:2778:2': ('RPM-2009-11-12:2778:3',
                           'ENLACE_RESPALDADO_POR_LECTURA'),
 'RPM-2009-11-12:2790:1': ('RPM-2009-11-12:2790:2',
                           'ENLACE_RESPALDADO_POR_LECTURA'),
 'RPM-2009-12-15:2810:2': ('RPM-2009-12-15:2810:3',
                           'ENLACE_RESPALDADO_POR_LECTURA'),
 'RPM-2010-01-14:2863:2': ('RPM-2010-01-14:2863:3',
                           'RESERVA_RESIDUOS_TEXTUALES'),
 'RPM-2010-02-11:2909:3': ('RPM-2010-02-11:2909:4',
                           'ENLACE_RESPALDADO_POR_LECTURA'),
 'RPM-2010-10-14:3439:2': ('RPM-2010-10-14:3439:3',
                           'ENLACE_RESPALDADO_POR_LECTURA'),
 'RPM-2011-01-13:3646:2': ('RPM-2011-01-13:3646:3',
                           'RESERVA_CONFIRMACION_NO_TRANSCRITA'),
 'RPM-2012-12-13:5252:3': ('RPM-2012-12-13:5252:4',
                           'RESERVA_FUNCIONES_DISTINTAS'),
 'RPM-2015-05-14:6800:2': ('RPM-2015-05-14:6800:3',
                           'ENLACE_RESPALDADO_POR_LECTURA')}
PARENTS = {2754, 2755, 1092, 2661, 2790, 2695, 2696, 2791, 2810, 5252, 780, 2863, 2864, 3439, 6800, 2778, 2909, 3646}
ALLOWED = {**V2_PAIRS, **NEW_PAIRS}


def selection(rows):
    return [e for e in inventory(rows) if e['Indicadores'] == 'IZQUIERDA_SIN_FUENTE_PROPAGABLE'
            and e['Fuente_Izquierda'] == 'CONTEXTO_REVISADO'
            and not e['Motivos_Izquierda'] and not e['Motivos_Derecha']]


def validate_readings(rows, package):
    """Baseline v2: particiones íntegras, pares exactos y grupos completos."""
    try:
        if (type(package['Version']) is not int or package['Version'] != 1
                or package['Alcance'] != 'LECTURA_CONTINUIDAD_LOTE3'
                or set(package['Padres']) != {str(p) for p in PARENTS}
                or set(package['Casos']) != set(CASES)
                or {e['Izquierda'] for e in selection(rows)} != set(CASES)
                or package['SHA256_Grupos'] != group_signature(rows)):
            raise ValueError('Lecturas fuera de alcance o baseline distinto')
        check_sources(package)
        for key,e in package['Padres'].items():
            indices = [i for i,r in enumerate(rows) if r['ID_Padre'] == int(key)]
            if not indices or indices != list(range(indices[0],indices[-1]+1)):
                raise ValueError('Padre ausente/discontinuo')
            i,j = indices[0],indices[-1]+1
            if i == 0 or j == len(rows):
                raise ValueError('Faltan ventanas')
            pr = rows[i:j]
            if (e['Lectura'] != 'PADRE_COMPLETO_EN_PARTICION_LITERAL'
                    or e['Fecha'] != str(pr[0]['Fecha'])[:10]
                    or e['SHA256_Texto_Padre'] != sha(e['Texto_Padre'])
                    or compact(e['Texto_Padre']) != compact(''.join(r['Texto'] for r in pr))
                    or e['SHA256_Particion'] != parent_signature(pr)
                    or e['Vecino_Anterior'] != window(rows[i-1],True)
                    or e['Vecino_Siguiente'] != window(rows[j])):
                raise ValueError('Padre, partición o ventanas modificados')
        index = {r['ID_Intervencion']:i for i,r in enumerate(rows)}
        covered = set()
        for left,(right,state) in CASES.items():
            e = package['Casos'][left]
            a,b = rows[index[left]:index[left]+2]
            groups = {side:[r for r in rows if r['ID_Turno'] == end['ID_Turno']]
                      for side,end in [('Izquierda',a),('Derecha',b)]}
            covered.update(r['ID_Padre'] for g in groups.values() for r in g)
            snapshots = {side:[{**endpoint(r),'SHA256_Fila':parent_signature([r])} for r in g]
                         for side,g in groups.items()}
            if (b['ID_Intervencion'] != right or e['Derecha'] != right
                    or a['ID_Padre'] != b['ID_Padre'] or e['ID_Padre'] != a['ID_Padre']
                    or e['Decision'] != state or not e['Justificacion'] or not e['Reservas']
                    or e['Grupos_Leidos'] != snapshots):
                raise ValueError('Par, decisión o miembros completos modificados')
        if covered != PARENTS:
            raise ValueError('Miembros sin lectura completa de sus padres')
    except (KeyError,TypeError,IndexError) as exc:
        raise ValueError('Lecturas incompletas') from exc


def load_v3(raw, path=PATH):
    result = _load_bounded_links(raw,path,3,'CONTINUIDAD_INTRAPADRE_V3',ALLOWED)
    prior = load_v2(raw)
    if any(result[k] != e for k,e in prior.items()):
        raise ValueError('v3 no puede modificar las seis pruebas anteriores')
    pkg = json.loads(Path(path).read_text())
    old = json.loads(V2_PATH.read_text())
    if (pkg.get('SHA256_Registro_V2') != sha(V2_PATH.read_text())
            or any(pkg.get(k) != old[k] for k in ('Lecturas_Lote2','SHA256_Lecturas_Lote2'))
            or pkg.get('Lecturas_Lote3') != str(READINGS.relative_to(ROOT))
            or pkg.get('SHA256_Lecturas_Lote3') != sha(READINGS.read_text())):
        raise ValueError('Vínculo con registros/lecturas modificado')
    readings = json.loads(READINGS.read_text())
    validate_readings(read_rows(BASE),readings)
    for p,e in readings['Padres'].items():
        if raw[int(p)]['Texto'] != e['Texto_Padre'] or str(raw[int(p)]['Fecha'])[:10] != e['Fecha']:
            raise ValueError('Fuente literal de las lecturas cambió')
    for left,right in NEW_PAIRS:
        if result[(left,right)]['Justificacion'] != readings['Casos'][left]['Justificacion']:
            raise ValueError('Justificación no coincide con la lectura')
    return result
