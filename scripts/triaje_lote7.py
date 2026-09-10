"""Triaje de los 53 pares sin adjudicación del inventario v6, con causa medida.

Publica una vista nueva bajo docs/ o .cache/; no modifica el inventario v6.
Cada registro lleva AMBOS extremos: la primera versión de este triaje guardaba el
extremo derecho en unas causas y el izquierdo en otras, y por eso no servía como
clave de par. Los conteos por causa no cambian.
"""
import argparse
import collections
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from diagnosticar_finales import read_rows
from qa_gate_f0 import extract_decision_rows
from context_warnings import has_context_warning
import functional_refinements_v5 as f5

V6 = ROOT / 'data/releases/continuidad_procedimental_v6/consolidado_base_referencia.xlsx'
V6_SHA = f5.BASE_SHA
INVENTARIO_V6 = ROOT / 'docs/procedimental_v6_2026-09-09/inventario_estado_v6.csv'
CONSTANCIA = re.compile(r'(?:deja constancia|se acuerda por unanimidad|se deja constancia)', re.I)
ESPERADOS = {'APORTE_PERSONAL_Y_CONSTANCIA_EN_UNA_FILA': 29,
             'DERECHA_ES_DOCUMENTO_LEIDO_POR_TERCERO': 8,
             'ALERTA_CONTEXTUAL_VIGENTE': 7,
             'DERECHA_SIN_FUENTE_PROPAGABLE': 4,
             'AMBOS_EXTREMOS_SIN_FUENTE_PROPAGABLE': 3,
             'POSIBLE_OTRA_VOZ': 1,
             'SIN_BARRERA_ESTRUCTURAL_IDENTIFICADA': 1}


def clasificar(rows, inventario):
    by = {r['ID_Intervencion']: r for r in rows}
    by_session = collections.defaultdict(list)
    for r in rows:
        by_session[str(r['Fecha'])[:10]].append(r)
    candidatas = {d['ID_Intervencion'] for g in by_session.values()
                  for d in extract_decision_rows(g)}
    registros = []
    for r in inventario:
        a, z = by[r['Izquierda']], by[r['Derecha']]
        t = z['Texto']
        m = CONSTANCIA.search(t)
        prefijo = len(t[:m.start()].strip()) if m else 0
        motivos = (a['Motivos_Revision'] or '') + '|' + (z['Motivos_Revision'] or '')
        if z['Tipo_Acta'] == 'ACUERDO_CONSEJO' and m and prefijo >= 250:
            causa = 'APORTE_PERSONAL_Y_CONSTANCIA_EN_UNA_FILA'
            detalle = {'Prefijo_Personal': prefijo, 'Es_Candidata_F0': z['ID_Intervencion'] in candidatas}
        elif z['Tipo_Acta'] == 'ACUERDO_CONSEJO':
            causa = 'CONSTANCIA_PURA_TIPIFICADA'
            detalle = {'Prefijo_Personal': prefijo}
        elif z['Tipo_Acta']:
            causa = 'OTRO_TIPO_ACTA:' + str(z['Tipo_Acta'])
            detalle = {}
        elif z['Fuente_Actor'] == 'LECTOR_DOCUMENTO_REVISADO':
            causa = 'DERECHA_ES_DOCUMENTO_LEIDO_POR_TERCERO'
            detalle = {}
        elif has_context_warning(a['Motivos_Revision']) or has_context_warning(z['Motivos_Revision']):
            causa = 'ALERTA_CONTEXTUAL_VIGENTE'
            detalle = {'Motivos': motivos}
        elif 'POSIBLE_OTRO_HABLANTE_O_MENCION' in motivos:
            causa = 'POSIBLE_OTRA_VOZ'
            detalle = {'Motivos': motivos}
        elif a['Fuente_Actor'] == 'CONTEXTO_REVISADO' and z['Fuente_Actor'] == 'CONTEXTO_REVISADO':
            causa = 'AMBOS_EXTREMOS_SIN_FUENTE_PROPAGABLE'
            detalle = {}
        elif z['Fuente_Actor'] == 'CONTEXTO_REVISADO':
            causa = 'DERECHA_SIN_FUENTE_PROPAGABLE'
            detalle = {}
        else:
            causa = 'SIN_BARRERA_ESTRUCTURAL_IDENTIFICADA'
            detalle = {'Motivos': motivos}
        registros.append({
            'Izquierda': r['Izquierda'], 'Derecha': r['Derecha'], 'Causa': causa,
            'Actor_Izquierda': a['Actor_Final'], 'Actor_Derecha': z['Actor_Final'],
            'Fuente_Izquierda': a['Fuente_Actor'], 'Fuente_Derecha': z['Fuente_Actor'],
            'Caracteres_Derecha': len(t), 'Tipo_Acta_Derecha': z['Tipo_Acta'] or '',
            **detalle})
    return registros


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', type=Path, required=True)
    out = parser.parse_args(argv).salida.resolve()
    if out.exists() or not any((ROOT / r).resolve() in out.parents for r in ('.cache', 'docs')):
        raise ValueError('Se requiere destino nuevo bajo .cache/ o docs/, nunca data/')
    import hashlib
    if hashlib.sha256(V6.read_bytes()).hexdigest() != V6_SHA:
        raise ValueError('La entrega v6 cambió')
    inventario = [r for r in csv.DictReader(INVENTARIO_V6.open(encoding='utf-8-sig'))
                  if r['Estado_Revision_Dirigida'] == 'SIN_ADJUDICACION_EN_ESTE_INVENTARIO']
    if len(inventario) != 53:
        raise ValueError(f'El inventario v6 debe tener 53 pares sin adjudicación, no {len(inventario)}')
    registros = clasificar(read_rows(V6), inventario)
    conteo = collections.Counter(r['Causa'] for r in registros)
    if dict(conteo) != ESPERADOS:
        raise ValueError(f'La clasificación cambió: {dict(conteo)}')
    if len({r['Izquierda'] for r in registros}) != 53:
        raise ValueError('Hay extremos izquierdos repetidos; no sirven como clave')
    out.mkdir(parents=True)
    paquete = {
        'Version': 2,
        'Alcance': 'TRIAJE_DE_CAUSAS_LOTE7_SIN_APLICAR',
        'Base': str(V6.relative_to(ROOT)),
        'SHA256_Base': V6_SHA,
        'Inventario': str(INVENTARIO_V6.relative_to(ROOT)),
        'Pares': 53,
        'Conteo_Por_Causa': dict(conteo.most_common()),
        'Nota': ('Cada registro lleva ambos extremos. La versión 1 guardaba el extremo derecho '
                 'en cuatro causas y el izquierdo en las otras tres, así que no servía como '
                 'clave de par; los conteos por causa son idénticos en ambas versiones.'),
        'Registros': sorted(registros, key=lambda r: r['Izquierda']),
    }
    (out / 'triaje_53.json').write_text(json.dumps(paquete, ensure_ascii=False, indent=1) + '\n')
    print(json.dumps({'pares': 53, 'conteo': dict(conteo.most_common())}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
