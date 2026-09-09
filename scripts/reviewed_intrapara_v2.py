"""Lote2: cuatro enlaces nuevos; v1 y la reserva5252 permanecen explícitos."""
import json
from pathlib import Path
from reviewed_intrapara_continuity import (_load_bounded_links, load_intrapara_links as load_v1,
                                         ALLOWED as V1_PAIRS)
from auditar_continuidad_turnos import window, group_signature
from revisar_cola_comas import parent_signature, endpoint, check_sources, compact, sha
from diagnosticar_finales import read_rows

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/curation/continuidades_intrapadre_v2.json'
BASE = ROOT / 'data/releases/continuidad_intrapadre_v1/consolidado_base_referencia.xlsx'
READINGS = ROOT / 'docs/continuidad_lote2_2026-09-09/lecturas.json'
NEW_PAIRS = {
    ('RPM-2006-05-11:663:2', 'RPM-2006-05-11:663:3'): (663, '2006-05-11', 'Igal Magendzo Weinberger'),
    ('RPM-2008-06-10:1871:2', 'RPM-2008-06-10:1871:3'): (1871, '2008-06-10', 'Sergio Lehmann Beresi'),
    ('RPM-2009-09-08:2692:2', 'RPM-2009-09-08:2692:3'): (2692, '2009-09-08', 'Sergio Lehmann Beresi'),
    ('RPM-2015-06-11:6813:2', 'RPM-2015-06-11:6813:3'): (6813, '2015-06-11', 'Diego Gianelli Gómez'),
}
ALLOWED = {**V1_PAIRS, **NEW_PAIRS}
PARENTS = {663, 1871, 2692, 5252, 6813}


def validate_readings(rows, package):
    """Contra v1 explícita: padres enteros, todos los miembros, ventanas y decisión."""
    try:
        if (type(package['Version']) is not int or package['Version'] != 1
                or package['Alcance'] != 'LECTURA_CONTINUIDAD_LOTE2'
                or set(package['Padres']) != {str(p) for p in PARENTS}
                or package['SHA256_Grupos'] != group_signature(rows)):
            raise ValueError('Lecturas incompatibles con el baseline v1')
        check_sources(package)
        for key, e in package['Padres'].items():
            p = int(key)
            indices = [i for i,r in enumerate(rows) if r['ID_Padre'] == p]
            if not indices or indices != list(range(indices[0], indices[-1]+1)):
                raise ValueError('Padre ausente o discontinuo')
            i, j = indices[0], indices[-1]+1
            pr = rows[i:j]
            a,b = pr[2:4] if p == 5252 else pr[1:3]
            groups = {side: [{**endpoint(r), 'SHA256_Fila': parent_signature([r])}
                             for r in rows if r['ID_Turno'] == end['ID_Turno']]
                      for side,end in [('Izquierda',a), ('Derecha',b)]}
            if (e['Lectura'] != 'PADRE_Y_GRUPOS_COMPLETOS'
                    or e['Fecha'] != str(a['Fecha'])[:10]
                    or e['SHA256_Texto_Padre'] != sha(e['Texto_Padre'])
                    or compact(e['Texto_Padre']) != compact(''.join(r['Texto'] for r in pr))
                    or e['SHA256_Particion'] != parent_signature(pr)
                    or e['Grupos_Leidos'] != groups
                    or e['Vecino_Anterior'] != window(rows[i-1],True)
                    or e['Vecino_Siguiente'] != window(rows[j])
                    or not e['Justificacion'] or not e['Reservas']
                    or e['Decision'] != ('RESERVA_FUNCIONES_DISTINTAS' if p == 5252 else 'ENLACE_RESPALDADO_POR_LECTURA')):
                raise ValueError('Lectura, partición, miembros o decisión modificados')
    except (KeyError, TypeError, IndexError) as exc:
        raise ValueError('Lecturas incompletas') from exc


def load_v2(raw, path=PATH):
    result = _load_bounded_links(raw, path, 2, 'CONTINUIDAD_INTRAPADRE_V2', ALLOWED)
    prior = load_v1(raw)
    if any(result[key] != value for key,value in prior.items()):
        raise ValueError('v2 no puede reescribir las pruebas de v1')
    package = json.loads(Path(path).read_text())
    if (package.get('Lecturas_Lote2') != str(READINGS.relative_to(ROOT))
            or package.get('SHA256_Lecturas_Lote2') != sha(READINGS.read_text())):
        raise ValueError('Falta vínculo íntegro con la lectura del lote2')
    readings = json.loads(READINGS.read_text())
    validate_readings(read_rows(BASE), readings)
    for p,e in readings['Padres'].items():
        if raw[int(p)]['Texto'] != e['Texto_Padre'] or str(raw[int(p)]['Fecha'])[:10] != e['Fecha']:
            raise ValueError('Lectura no coincide con la fuente literal actual')
    for key in NEW_PAIRS:
        e = result[key]
        evidence = readings['Padres'][str(e['ID_Padre'])]
        if e['Justificacion'] != evidence['Justificacion']:
            raise ValueError('Justificación distinta de la lectura')
    return result
