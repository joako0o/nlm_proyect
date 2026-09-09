"""Lote6: dos enlaces intrapadre locales; v1-v3 y las tres reservas intactas.

Los dos enlaces provienen de la lectura completa del lote6 y sólo agrupan
respuesta→desarrollo dentro del mismo padre. No promueven CONTEXTO_REVISADO a
ancla (ambos extremos izquierdos conservan ancla nula), no reparan OCR, no
generalizan a otras confirmaciones narradas y no cierran ninguna alerta.
"""
import hashlib
import json
from pathlib import Path
from reviewed_intrapara_continuity import _load_bounded_links
from reviewed_intrapara_v3 import load_v3, ALLOWED as V3_PAIRS, PATH as V3_PATH, selection
from auditar_continuidad_turnos import window, group_signature
from revisar_cola_comas import parent_signature, compact, sha
from diagnosticar_finales import read_rows

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/curation/continuidades_intrapadre_v4.json'
BASE = ROOT / 'data/releases/continuidad_procedimental_v5/consolidado_base_referencia.xlsx'
BASE_SHA = '4da18c4e86f583fdf4d5d0cd9be49b9aac20fb40379cd391b5f4c7763cf9e168'
READINGS = ROOT / 'docs/continuidad_lote6_2026-09-09/lecturas.json'
SCOPE = 'LECTURA_RESERVAS_LOTE6_SIN_APLICAR'
NEW_PAIRS = {
    ('RPM-2010-01-14:2863:2', 'RPM-2010-01-14:2863:3'): (2863, '2010-01-14', 'Claudio Soto Gamboa'),
    ('RPM-2011-01-13:3646:2', 'RPM-2011-01-13:3646:3'): (3646, '2011-01-13', 'Sergio Lehmann Beresi'),
}
# Los cinco casos releídos en lote6: dos propuestas (ahora aplicadas) y tres
# reservas que permanecen abiertas y sin enlace.
DECISIONES_LOTE6 = {
    'RPM-2006-07-13:780:2': ('RPM-2006-07-13:780:3', 'RESERVA_COTEJO_INICIO'),
    'RPM-2009-08-13:2661:6': ('RPM-2009-08-13:2661:7', 'RESERVA_CONFIRMACION_NARRADA'),
    'RPM-2010-01-14:2863:2': ('RPM-2010-01-14:2863:3', 'PROPUESTA_LOCAL_NO_APLICADA'),
    'RPM-2011-01-13:3646:2': ('RPM-2011-01-13:3646:3', 'PROPUESTA_LOCAL_NO_APLICADA'),
    'RPM-2012-12-13:5252:3': ('RPM-2012-12-13:5252:4', 'RESERVA_LIMITE_ACTA_PERSONA'),
}
RESERVAS_ABIERTAS = frozenset(k for k, (_, s) in DECISIONES_LOTE6.items() if s.startswith('RESERVA_'))
PARENTS = {780, 2661, 2863, 2864, 3646, 5252}
ALLOWED = {**V3_PAIRS, **NEW_PAIRS}


def snapshot(row):
    return {k: (str(v)[:10] if k == 'Fecha' else v) for k, v in row.items()}


def check_sources(package):
    """Las fuentes del lote6 viven bajo data/ y docs/; todas deben seguir vigentes."""
    sources = package.get('SHA256_Fuentes')
    if not isinstance(sources, dict) or not sources:
        raise ValueError('Faltan hashes de fuentes')
    for name, expected in sources.items():
        path = (ROOT / name).resolve()
        if not any(root in path.parents for root in (ROOT / 'data', ROOT / 'docs')):
            raise ValueError('Fuente fuera de data/ o docs/: ' + name)
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Fuente original modificada: ' + name)


def validate_readings(rows, package, raw):
    """Baseline v5: seis padres enteros, cinco casos, grupos completos y reservas."""
    try:
        if (type(package['Version']) is not int or package['Version'] != 1
                or package['Alcance'] != SCOPE
                or set(package['Padres']) != {str(p) for p in PARENTS}
                or set(package['Casos']) != set(DECISIONES_LOTE6)
                or {e['Izquierda'] for e in selection(rows)} != set(DECISIONES_LOTE6)
                or package['SHA256_Grupos'] != group_signature(rows)):
            raise ValueError('Lecturas lote6 fuera de alcance o baseline distinto')
        check_sources(package)
        for key, e in package['Padres'].items():
            p = int(key)
            indices = [i for i, r in enumerate(rows) if r['ID_Padre'] == p]
            if not indices or indices != list(range(indices[0], indices[-1]+1)):
                raise ValueError('Padre ausente o discontinuo')
            i, j = indices[0], indices[-1]+1
            if i == 0 or j == len(rows):
                raise ValueError('Faltan ventanas de contexto')
            pr = rows[i:j]
            if (e['Lectura'] != 'PADRE_COMPLETO_EN_PARTICION_LITERAL'
                    or e['Fecha'] != str(raw[p]['Fecha'])[:10]
                    or e['Texto_Padre'] != raw[p]['Texto']
                    or e['SHA256_Texto_Padre'] != sha(e['Texto_Padre'])
                    or e['SHA256_Particion'] != parent_signature(pr)
                    or compact(e['Texto_Padre']) != compact(''.join(r['Texto'] for r in pr))
                    or e['Vecino_Anterior'] != window(rows[i-1], True)
                    or e['Vecino_Siguiente'] != window(rows[j])):
                raise ValueError('Padre, partición o ventanas modificados')
        index = {r['ID_Intervencion']: i for i, r in enumerate(rows)}
        if len(index) != len(rows):
            raise ValueError('IDs repetidos')
        covered = set()
        for left, (right, state) in DECISIONES_LOTE6.items():
            e = package['Casos'][left]
            a, b = rows[index[left]:index[left]+2]
            groups = {side: [snapshot(r) for r in rows if r['ID_Turno'] == end['ID_Turno']]
                      for side, end in [('Izquierda', a), ('Derecha', b)]}
            covered.update(r['ID_Padre'] for g in groups.values() for r in g)
            if (b['ID_Intervencion'] != right or e['Derecha'] != right
                    or a['ID_Padre'] != b['ID_Padre'] or e['Estado'] != state
                    or e['Aplicado'] is not False or not e['Justificacion']
                    or not e['Siguiente_Accion'] or not e['Limite']
                    or e['Grupos_Leidos'] != groups):
                raise ValueError('Par, decisión o miembros completos modificados')
        if covered != PARENTS:
            raise ValueError('Miembros sin lectura completa de sus padres')
    except (KeyError, TypeError, IndexError) as exc:
        raise ValueError('Lecturas lote6 incompletas') from exc


def load_v4(raw, path=PATH):
    result = _load_bounded_links(raw, path, 4, 'CONTINUIDAD_INTRAPADRE_V4', ALLOWED)
    prior = load_v3(raw)
    if any(result[k] != e for k, e in prior.items()):
        raise ValueError('v4 no puede modificar las quince pruebas anteriores')
    pkg = json.loads(Path(path).read_text())
    old = json.loads(V3_PATH.read_text())
    if (pkg.get('SHA256_Registro_V3') != sha(V3_PATH.read_text())
            or any(pkg.get(k) != old[k] for k in ('Lecturas_Lote2', 'SHA256_Lecturas_Lote2',
                                                  'Lecturas_Lote3', 'SHA256_Lecturas_Lote3',
                                                  'SHA256_Registro_V2'))
            or pkg.get('Lecturas_Lote6') != str(READINGS.relative_to(ROOT))
            or pkg.get('SHA256_Lecturas_Lote6') != sha(READINGS.read_text())):
        raise ValueError('Vínculo con registros/lecturas modificado')
    if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASE_SHA:
        raise ValueError('El histórico procedimental v5 cambió')
    readings = json.loads(READINGS.read_text())
    validate_readings(read_rows(BASE), readings, raw)
    for p, e in readings['Padres'].items():
        if raw[int(p)]['Texto'] != e['Texto_Padre'] or str(raw[int(p)]['Fecha'])[:10] != e['Fecha']:
            raise ValueError('Fuente literal de las lecturas cambió')
    for left, right in NEW_PAIRS:
        e = result[(left, right)]
        if (e['Justificacion'] != readings['Casos'][left]['Justificacion']
                or e['Limitacion'] == readings['Casos'][left]['Justificacion']):
            raise ValueError('Justificación o límite no coinciden con la lectura')
    return result
