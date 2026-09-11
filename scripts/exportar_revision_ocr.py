#!/usr/bin/env python3
"""Exporta las correcciones OCR curadas en un formato que un humano puede revisar.

Motivo: el registro vive en JSON y el resumen del release
(``correcciones_aplicadas.json``) trae totales y listas de IDs solamente. Las
operaciones con su antes/después no estaban escritas en ningún sitio revisable,
y un *gold standard* que nadie puede auditar no lo es.

Este script no inventa nada: re-ejecuta ``correcciones_ocr_v1.validar()`` sobre
la base virgen y vuelca **lo que realmente se aplicó**, operación por operación.
Si la validación falla, no escribe y devuelve 1.

Salidas (en ``--destino``, por defecto junto al release):

* ``revision_operaciones.tsv`` — una fila por operación, con antes/después.
* ``revision_resumen.md``      — totales por tipo y una muestra aleatoria
                                 estratificada para revisión rápida.

Uso::

    python scripts/exportar_revision_ocr.py
    python scripts/exportar_revision_ocr.py --muestra 40 --destino /tmp/rev
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import correcciones_ocr_v1 as core  # noqa: E402
from diagnosticar_finales import read_rows  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DESTINO_DEFECTO = RAIZ / 'data' / 'releases' / 'correccion_ocr_v1'


def exportar(destino: Path, muestra: int, semilla: int) -> int:
    reg = core.cargar()
    ok, problemas, corregidas, marcas = core.validar(base=core.BASE)
    if not ok:
        for p in problemas:
            print('ERROR:', p)
        print('no se exporta: la validación falla')
        return 1

    filas = {r['ID_Intervencion']: r for r in read_rows(core.BASE)}
    destino.mkdir(parents=True, exist_ok=True)
    tsv = destino / 'revision_operaciones.tsv'

    por_tipo: Counter[str] = Counter()
    por_fila: dict[str, list[dict]] = defaultdict(list)
    n_ops = 0
    with tsv.open('w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, delimiter='\t', lineterminator='\n')
        w.writerow(['ID_Intervencion', 'Fecha', 'Actor', 'N_Op', 'Tipo',
                    'Antes', 'Despues', 'Justificacion'])
        for entrada in reg['Correcciones']:
            rid = entrada['ID_Intervencion']
            fila = filas.get(rid)
            fecha = fila['Fecha'].strftime('%Y-%m-%d') if fila else ''
            actor = (fila.get('Actor_Final') or '') if fila else ''
            for n, op in enumerate(entrada['Operaciones'], 1):
                antes, despues = op['Antes'], op['Despues']
                # mostrar los saltos de línea como visibles: en un TSV romperían la fila
                lim = lambda s: s.replace('\t', ' ').replace('\n', '⏎')
                w.writerow([rid, fecha, actor, n, op['Tipo'],
                            lim(antes), lim(despues), lim(op.get('Justificacion', ''))])
                por_tipo[op['Tipo']] += 1
                por_fila[rid].append(op)
                n_ops += 1

    rng = random.Random(semilla)
    ids = sorted(por_fila)
    k = min(muestra, len(ids))
    elegidas = rng.sample(ids, k)
    md = destino / 'revision_resumen.md'
    lineas = [
        '# Revisión de las correcciones OCR aplicadas',
        '',
        'Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una',
        'vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada',
        'contra la base virgen. Si el registro cambia, hay que regenerarlo.',
        '',
        f'- filas corregidas: **{len(corregidas)}**',
        f'- operaciones: **{n_ops}**',
        f'- filas marcadas para cotejo: **{len(marcas)}**',
        f'- sha256 de la base: `{core.hashlib.sha256(core.BASE.read_bytes()).hexdigest()}`',
        '',
        '## Operaciones por tipo',
        '',
        '| tipo | operaciones |',
        '|---|---:|',
    ]
    for t, c in por_tipo.most_common():
        lineas.append(f'| `{t}` | {c} |')
    lineas += ['', f'## Muestra aleatoria de {k} filas (semilla {semilla})', '']
    for rid in elegidas:
        fila = filas.get(rid)
        lineas.append(f'### `{rid}` — {(fila.get("Actor_Final") or "") if fila else ""}')
        lineas.append('')
        for n, op in enumerate(por_fila[rid], 1):
            lineas.append(f'{n}. **{op["Tipo"]}**')
            lineas.append(f'   - antes: `{op["Antes"]}`')
            lineas.append(f'   - después: `{op["Despues"]}`')
            just = op.get('Justificacion', '').strip()
            if just:
                lineas.append(f'   - por qué: {just}')
        lineas.append('')
    md.write_text('\n'.join(lineas), encoding='utf-8')

    print(f'operaciones exportadas: {n_ops}')
    print(f'filas: {len(por_fila)} | tipos: {len(por_tipo)}')
    print(f'escrito: {tsv}')
    print(f'escrito: {md}')
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--destino', type=Path, default=DESTINO_DEFECTO)
    ap.add_argument('--muestra', type=int, default=30)
    ap.add_argument('--semilla', type=int, default=20260911)
    a = ap.parse_args()
    return exportar(a.destino, a.muestra, a.semilla)


if __name__ == '__main__':
    raise SystemExit(main())
