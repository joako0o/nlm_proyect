#!/usr/bin/env python3
"""Cierra marcas ``Cotejar_PDF`` cuyo cotejo contra el PDF original ya se hizo.

    python scripts/cerrar_marcas_cotejadas.py <cierres.json> [--aplicar]

El archivo de cierres es una lista de objetos::

    {"ID_Intervencion": "...", "Marca": "NO_REQUIERE_COTEJO", "Motivo": "..."}

``Texto_Original_Fragmento`` es opcional y sólo hace falta cuando una fila tiene
más de una revisión registrada: entonces desambigua cuál se cierra.

Por qué existe: ``agregar_correcciones_ocr.py --parche`` añade y extiende
correcciones, y añade revisiones nuevas, pero no actualiza la ``Marca`` de una
revisión ya registrada. Sin esta herramienta el único camino era editar el
registro a mano, que es justo lo que el pipeline intenta evitar.

Semántica de ``NO_REQUIERE_COTEJO``: la fila sale de la columna ``Cotejar_PDF``
(vedi ``correcciones_ocr_v1.construir``, que excluye esa marca), pero la entrada
se conserva en ``Revisiones_Sin_Correccion`` con el veredicto en ``Motivo``. Es
el mismo tratamiento que ya reciben los veredictos ``NO_ES_DEFECTO`` y
``NO_ES_OCR``. Nada se borra: cerrar una marca es registrar una respuesta, no
eliminar una pregunta.

Sin ``--aplicar`` sólo informa; no escribe.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import correcciones_ocr_v1 as core  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
REG = RAIZ / 'data' / 'curation' / 'correcciones_ocr_v1.json'

# Marcas que abren una pregunta; sólo ésas se pueden cerrar.
ABIERTAS = {m for m in core.MARCAS_VALIDAS if m.endswith('_POR_COTEJAR')} | {
    'RESERVA_ABIERTA_POR_COTEJO'}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('cierres')
    ap.add_argument('--aplicar', action='store_true')
    a = ap.parse_args()

    reg = json.loads(REG.read_text(encoding='utf-8'))
    revs = reg['Revisiones_Sin_Correccion']
    cierres = json.loads(Path(a.cierres).read_text(encoding='utf-8'))
    if isinstance(cierres, dict):
        cierres = cierres.get('Cierres', [])

    problemas: list[str] = []
    cerradas = 0
    for c in cierres:
        rid = c.get('ID_Intervencion')
        nueva = c.get('Marca')
        motivo = (c.get('Motivo') or '').strip()

        if nueva not in core.MARCAS_VALIDAS:
            problemas.append(f'{rid}: marca fuera de vocabulario: {nueva!r}')
            continue
        if not motivo:
            problemas.append(f'{rid}: Motivo vacío (el contrato de la columna lo exige)')
            continue

        # El registro admite un ID_Intervencion con varias filas separadas por '/'
        # (correcciones_ocr_v1.construir las expande y marca todas). Cerrar una de
        # esas entradas cerraría las demás sin que nadie lo pida, así que se
        # detecta el caso y se exige decidir explícitamente.
        frag = c.get('Texto_Original_Fragmento')
        cand = [r for r in revs
                if rid in [x.strip() for x in r['ID_Intervencion'].split('/')]]
        if frag:
            cand = [r for r in cand if r.get('Texto_Original_Fragmento') == frag]
        if not cand:
            problemas.append(f'{rid}: no hay revisión registrada que coincida')
            continue
        if len(cand) > 1:
            problemas.append(
                f'{rid}: {len(cand)} revisiones registradas; '
                'falta Texto_Original_Fragmento para desambiguar')
            continue

        r = cand[0]
        cubre = [x.strip() for x in r['ID_Intervencion'].split('/') if x.strip()]
        if len(cubre) > 1:
            problemas.append(
                f'{rid}: la revisión cubre {len(cubre)} filas ({r["ID_Intervencion"]!r}); '
                'cerrarla cerraría también las demás. Divídala en el registro primero')
            continue
        actual = r.get('Marca')
        if actual not in ABIERTAS:
            problemas.append(f'{rid}: la marca actual {actual!r} no está abierta')
            continue
        if actual == nueva:
            problemas.append(f'{rid}: ya tiene la marca {nueva!r}')
            continue

        print('  %-24s %-32s -> %s' % (rid, actual, nueva))
        print('      %s' % motivo[:150])
        r['Marca'] = nueva
        r['Motivo'] = motivo
        cerradas += 1

    if problemas:
        for p in problemas:
            print('ERROR:', p)
        print('no se escribe el registro')
        return 1
    if not cerradas:
        print('nada que cerrar')
        return 0
    if not a.aplicar:
        print(f'\n{cerradas} marcas listas para cerrar (simulación; use --aplicar)')
        return 0

    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nregistro escrito: {cerradas} marcas cerradas')
    print('total revisiones:', len(revs))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
