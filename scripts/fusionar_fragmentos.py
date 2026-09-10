#!/usr/bin/env python3
"""Reúne los fragmentos paralelos en el registro y las lecturas canónicas.

Cada fragmento trabajó sobre sus propios archivos; este script los concatena
y **revalida todo junto contra la base**, que es la única prueba de que dos
sesiones paralelas no se contradicen (por ejemplo, marcando la misma fila con
motivos incompatibles o corrigiendo la misma fila de dos maneras).

No sobrescribe nada: escribe ``*.fusionado.json`` al lado y sólo reemplaza el
canónico con ``--aplicar``.

Uso::

    python scripts/fusionar_fragmentos.py             # valida y muestra
    python scripts/fusionar_fragmentos.py --aplicar   # además reemplaza el canónico
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import correcciones_ocr_v1 as m  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
FRAG = RAIZ / 'docs' / 'continuidad_lote9_2026-09-09' / 'fragmentos'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--aplicar', action='store_true')
    a = ap.parse_args()

    regs = sorted((RAIZ / 'data' / 'curation').glob('correcciones_ocr_?.json'))
    if not regs:
        print('no hay fragmentos; corre primero scripts/fragmentar_lectura.py')
        return 1

    can = json.loads(m.REGISTRO.read_text(encoding='utf-8'))
    base_ids = {e['ID_Intervencion'] for e in can['Correcciones']}
    base_rev = {(r['ID_Intervencion'], r['Texto_Original_Fragmento'])
                for r in can['Revisiones_Sin_Correccion']}
    conflicto: list[str] = []
    for p in regs:
        r = json.loads(p.read_text(encoding='utf-8'))
        for e in r.get('Correcciones', []):
            rid = e['ID_Intervencion']
            if rid in base_ids:
                conflicto.append(f'{rid} corregida en dos fragmentos ({p.name} y el canónico u otro)')
                continue
            base_ids.add(rid)
            can['Correcciones'].append(e)
        for rev in r.get('Revisiones_Sin_Correccion', []):
            if rev.get('Marca') not in m.MARCAS_VALIDAS:
                conflicto.append(f"{p.name}: marca inválida {rev.get('Marca')!r} en {rev.get('ID_Intervencion')}")
                continue
            clave = (rev['ID_Intervencion'], rev['Texto_Original_Fragmento'])
            if clave in base_rev:
                continue
            base_rev.add(clave)
            can['Revisiones_Sin_Correccion'].append(rev)

    lecturas = json.loads((RAIZ / 'docs' / 'continuidad_lote9_2026-09-09'
                           / 'lecturas.json').read_text(encoding='utf-8'))
    vistos = set(lecturas['Casos'])
    doble = []
    for p in sorted(FRAG.glob('lecturas_?.json')):
        d = json.loads(p.read_text(encoding='utf-8'))
        for k, v in d.get('Casos', {}).items():
            if k in vistos:
                doble.append(k)
                continue
            vistos.add(k)
            lecturas['Casos'][k] = v

    print(f'fragmentos de correcciones : {len(regs)}')
    print(f'filas con corrección       : {len(can["Correcciones"])}')
    print(f'operaciones                : {sum(len(e["Operaciones"]) for e in can["Correcciones"])}')
    print(f'revisiones                 : {len(can["Revisiones_Sin_Correccion"])}')
    print(f'lecturas totales           : {len(lecturas["Casos"])}')
    print('marcas por tipo            :',
          dict(Counter(r['Marca'] for r in can['Revisiones_Sin_Correccion'])))
    if doble:
        print(f'ALERTA: {len(doble)} filas leídas en dos fragmentos: {doble[:8]}')
    if conflicto:
        print('\nCONFLICTOS:')
        for c in conflicto:
            print(' -', c)
        return 1
    print('\nsin conflictos entre fragmentos')

    tmp = m.REGISTRO.with_suffix('.fusionado.json')
    tmp.write_text(json.dumps(can, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    ok, problemas, corregidas, marcas = m.validar(can, m.BASE)
    for p in problemas:
        print('ERROR:', p)
    print(f'revalidación del conjunto fusionado: {"OK" if ok else "FALLO"} | '
          f'{len(corregidas)} filas corregibles | {len(marcas)} marcadas')
    if not ok:
        return 1
    if a.aplicar:
        m.REGISTRO.write_text(json.dumps(can, ensure_ascii=False, indent=2) + '\n',
                              encoding='utf-8')
        (RAIZ / 'docs' / 'continuidad_lote9_2026-09-09' / 'lecturas.json').write_text(
            json.dumps(lecturas, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print('canónicos reemplazados')
    else:
        print(f'escrito sin tocar el canónico en {tmp.relative_to(RAIZ)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
