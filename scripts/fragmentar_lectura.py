#!/usr/bin/env python3
"""Fragmenta la lectura pendiente en lotes disjuntos para sesiones paralelas.

Cuatro sesiones pueden leer a la vez **si y sólo si** no comparten archivos
mutables. Este script reparte las sesiones pendientes en N fragmentos
disjuntos y escribe, por fragmento:

* su lista de sesiones con filas y caracteres,
* un registro de OCR propio (``correcciones_ocr_<letra>.json``),
* un archivo de lecturas propio (``lecturas_<letra>.json``).

Cada sesión paralela trabaja sobre su rama y sus dos archivos; nadie escribe
el archivo canónico. Al final ``scripts/fusionar_fragmentos.py`` los reúne y
revalida.

Uso::

    python scripts/fragmentar_lectura.py --n 4
    python scripts/fragmentar_lectura.py --asignar A     # qué le toca a un fragmento
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from diagnosticar_finales import read_rows  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
BASE = (RAIZ / 'data' / 'releases' / 'continuidad_procedimental_v7'
        / 'consolidado_base_referencia_final.xlsx')
LECT = RAIZ / 'docs' / 'continuidad_lote9_2026-09-09' / 'lecturas.json'
REG = RAIZ / 'data' / 'curation' / 'correcciones_ocr_v1.json'
SALIDA = RAIZ / 'docs' / 'continuidad_lote9_2026-09-09' / 'fragmentos'


def fecha(v) -> str:
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.strftime('%Y-%m-%d')
    return str(v)[:10]


def pendientes():
    rows = read_rows(BASE)
    leidas = set(json.loads(LECT.read_text(encoding='utf-8'))['Casos'])
    por_sesion: dict[str, dict] = {}
    for r in rows:
        if r['ID_Intervencion'] in leidas:
            continue
        f = fecha(r['Fecha'])
        d = por_sesion.setdefault(f, {'filas': 0, 'chars': 0})
        d['filas'] += 1
        d['chars'] += len(r['Texto'] or '')
    return por_sesion


def repartir(por_sesion: dict, n: int) -> list[list[str]]:
    """Empaqueta por sesiones completas, de mayor a menor, al fragmento que
    vaya más liviano. Las sesiones nunca se parten: una sesión la cierra una
    sola persona, que es quien puede verificar su conteo contra el xlsx."""
    orden = sorted(por_sesion, key=lambda f: -por_sesion[f]['chars'])
    frags: list[list[str]] = [[] for _ in range(n)]
    carga = [0] * n
    for f in orden:
        i = carga.index(min(carga))
        frags[i].append(f)
        carga[i] += por_sesion[f]['chars']
    return frags


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=4)
    ap.add_argument('--asignar', type=str)
    a = ap.parse_args()
    por_sesion = pendientes()

    if a.asignar:
        letra = a.asignar.upper()
        doc = SALIDA / f'fragmento_{letra}.json'
        if not doc.exists():
            print(f'no existe {doc}; corre primero --n {a.n}')
            return 1
        d = json.loads(doc.read_text(encoding='utf-8'))
        print(f"fragmento {letra} | {d['Sesiones_Totales']} sesiones | "
              f"{d['Filas']} filas | {d['Caracteres']:,} chars")
        print(f"registro propio : data/curation/correcciones_ocr_{letra.lower()}.json")
        print(f"lecturas propias: docs/continuidad_lote9_2026-09-09/fragmentos/lecturas_{letra.lower()}.json")
        print('orden de trabajo:')
        for s in d['Orden']:
            print(f"  {s['Fecha']}  {s['Filas']:4d} filas  {s['Caracteres']:8,} ch")
        return 0

    frags = repartir(por_sesion, a.n)
    SALIDA.mkdir(parents=True, exist_ok=True)
    letras = 'ABCDEFGHIJ'[:a.n]
    print(f'{len(por_sesion)} sesiones pendientes repartidas en {a.n} fragmentos\n')
    for letra, fs in zip(letras, frags):
        filas = sum(por_sesion[f]['filas'] for f in fs)
        chars = sum(por_sesion[f]['chars'] for f in fs)
        orden = sorted(fs, key=lambda f: -por_sesion[f]['chars'])
        (SALIDA / f'fragmento_{letra}.json').write_text(json.dumps({
            'Fragmento': letra,
            'Generado': datetime.date.today().isoformat(),
            'Sesiones_Totales': len(fs),
            'Filas': filas,
            'Caracteres': chars,
            'Orden': [{'Fecha': f, **por_sesion[f]} for f in orden],
        }, ensure_ascii=False, indent=2), encoding='utf-8')
        (SALIDA / f'lecturas_{letra.lower()}.json').write_text(json.dumps({
            'Fragmento': letra, 'Casos': {}}, ensure_ascii=False, indent=2),
            encoding='utf-8')
        reg = json.loads(REG.read_text(encoding='utf-8'))
        reg['Fragmento'] = letra
        reg['Correcciones'] = []
        reg['Revisiones_Sin_Correccion'] = []
        (RAIZ / 'data' / 'curation' / f'correcciones_ocr_{letra.lower()}.json'
         ).write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'  {letra}: {len(fs):3d} sesiones | {filas:5d} filas | {chars:9,} chars')
        print(f'      primera: {orden[0]}   última: {orden[-1]}')
    print('\nCada fragmento escribe SOLO sus dos archivos. Nadie toca el canónico.')
    print('Al terminar: python scripts/fusionar_fragmentos.py')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
