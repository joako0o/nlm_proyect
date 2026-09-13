#!/usr/bin/env python3
"""Enmienda una operación ya registrada en vez de apilarle otra encima.

    python scripts/enmendar_operacion.py <enmiendas.json> [--aplicar]

El archivo es una lista de objetos::

    {"ID_Intervencion": "...", "Antes": "...", "Tipo": "...",
     "Despues": "...", "Justificacion": "..."}

``Antes`` identifica la operación y no se modifica: es lo que la ancla al texto
virgen de la fila. Lo que se enmienda es ``Despues``, ``Tipo`` y
``Justificacion``.

Por qué existe: §15 dejó la regla de que cuando dos defectos caen en el mismo
tramo hay que **extender** la operación existente, no añadirle una segunda,
porque dos tramos solapados sobre el mismo texto virgen no se pueden aplicar en
ningún orden. ``agregar_correcciones_ocr.py --parche`` ya actualiza ``Despues``
cuando el ``Antes`` coincide, pero no puede cambiar el ``Tipo``, y hay enmiendas
que cambian la naturaleza del arreglo: quitar un espacio indebido y descubrir
después que el signo también sobraba ya no es ``ESPACIO_INDEBIDO``.

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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('enmiendas')
    ap.add_argument('--aplicar', action='store_true')
    a = ap.parse_args()

    reg = json.loads(REG.read_text(encoding='utf-8'))
    enmiendas = json.loads(Path(a.enmiendas).read_text(encoding='utf-8'))
    if isinstance(enmiendas, dict):
        enmiendas = enmiendas.get('Enmiendas', [])

    problemas: list[str] = []
    hechas = 0
    for e in enmiendas:
        rid, antes = e.get('ID_Intervencion'), e.get('Antes')
        tipo, despues = e.get('Tipo'), e.get('Despues')
        just = (e.get('Justificacion') or '').strip()

        if tipo not in core.TIPOS_VALIDOS:
            problemas.append(f'{rid}: Tipo fuera de vocabulario: {tipo!r}')
            continue
        if not despues or not just:
            problemas.append(f'{rid}: Despues y Justificacion son obligatorios')
            continue

        fila = next((c for c in reg['Correcciones'] if c['ID_Intervencion'] == rid), None)
        if fila is None:
            problemas.append(f'{rid}: no tiene correcciones registradas')
            continue
        ops = [o for o in fila['Operaciones'] if o['Antes'] == antes]
        if len(ops) != 1:
            problemas.append(f'{rid}: {len(ops)} operaciones con ese Antes (debe haber 1)')
            continue

        op = ops[0]
        if op['Despues'] == despues and op['Tipo'] == tipo:
            problemas.append(f'{rid}: la operación ya está como se pide')
            continue
        if antes == despues:
            problemas.append(f'{rid}: Despues igual a Antes, no corrige nada')
            continue

        print('  %s' % rid)
        print('      Antes    : %r' % antes[:64])
        print('      Tipo     : %s -> %s' % (op['Tipo'], tipo))
        print('      Despues  : %r -> %r' % (op['Despues'][:44], despues[:44]))
        op['Tipo'] = tipo
        op['Despues'] = despues
        op['Justificacion'] = just
        if e.get('Contexto'):
            op['Contexto'] = e['Contexto']
        hechas += 1

    if problemas:
        for p in problemas:
            print('ERROR:', p)
        print('no se escribe el registro')
        return 1
    if not hechas:
        print('nada que enmendar')
        return 0
    if not a.aplicar:
        print(f'\n{hechas} operaciones listas para enmendar (simulación; use --aplicar)')
        return 0

    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nregistro escrito: {hechas} operaciones enmendadas')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
