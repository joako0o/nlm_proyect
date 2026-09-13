#!/usr/bin/env python3
"""Fusiona un lote de correcciones/revisiones dentro del registro curado.

Uso::

    python scripts/agregar_correcciones_ocr.py <lote.json>
    python scripts/agregar_correcciones_ocr.py <lote.json> --parche

El lote tiene la forma ``{"Correcciones": [...], "Revisiones_Sin_Correccion": [...]}``.

**Sin ``--parche``** (comportamiento histórico y predeterminado): una entrada
cuyo ``ID_Intervencion`` ya esté registrado se **rechaza** y el script termina
con código 1. Eso impide pisar trabajo previo por accidente, pero obligaba a
editar el JSON a mano cada vez que había que añadir una operación a una fila ya
corregida — el paso más frágil del pipeline, hecho sin red.

**Con ``--parche``**: las operaciones del lote se **añaden** a la entrada ya
existente en vez de rechazarse. Sigue sin pisar nada: se valida antes que el
``Antes`` de cada operación nueva no choque con las ya registradas (ni por
solape de tramos ni por contención de subcadenas), que sea único en el texto
virgen de la fila, y que el ``Antes`` no sea igual al ``Despues``. Si alguna
falla, no se escribe nada.

``--parche`` también permite reemplazar el ``Despues``/``Justificacion`` de una
operación existente cuando el ``Antes`` coincide exactamente: es el caso de
extender una corrección en vez de añadir otra, que ocurre cuando dos defectos
caen dentro del mismo tramo.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import correcciones_ocr_v1 as core  # noqa: E402
from diagnosticar_finales import read_rows  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
REG = RAIZ / 'data' / 'curation' / 'correcciones_ocr_v1.json'


def tramos(texto: str, ops: list[dict]) -> list[tuple[int, int, str]]:
    out = []
    for op in ops:
        i = texto.find(op['Antes'])
        if i >= 0:
            out.append((i, i + len(op['Antes']), op['Antes']))
    return out


def revisar_parche(rid: str, virgen: str, nuevas: list[dict],
                   existentes: list[dict]) -> list[str]:
    """Devuelve la lista de problemas; vacía si el parche es aplicable."""
    probs: list[str] = []
    ocupados = tramos(virgen, existentes)
    for op in nuevas:
        antes = op['Antes']
        if antes == op.get('Despues'):
            probs.append(f'{rid}: «{antes}» no cambia nada')
            continue
        if op.get('Tipo') not in core.TIPOS_VALIDOS:
            probs.append(f'{rid}: tipo desconocido {op.get("Tipo")!r}')
        for campo in ('Contexto', 'Justificacion'):
            if not (op.get(campo) or '').strip():
                probs.append(f'{rid}: falta {campo}')
        n = virgen.count(antes)
        if n != int(op.get('Ocurrencias', 1)):
            probs.append(f'{rid}: «{antes}» aparece {n} veces en el texto virgen, '
                         f'se declararon {op.get("Ocurrencias", 1)}')
        i = virgen.find(antes)
        if i >= 0:
            a, b = i, i + len(antes)
            for x, y, otro in ocupados:
                if a < y and x < b:
                    probs.append(f'{rid}: «{antes}» se solapa con «{otro}» ya registrada')
                elif otro in antes or antes in otro:
                    probs.append(f'{rid}: «{antes}» y «{otro}» se contienen mutuamente; '
                                 f'extienda la operación existente en vez de añadir otra')
        ocupados.append((i, i + len(antes), antes))
    return probs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('lote', type=Path)
    ap.add_argument('--parche', action='store_true',
                    help='añadir operaciones a filas ya registradas en vez de rechazarlas')
    a = ap.parse_args()

    reg = json.loads(REG.read_text(encoding='utf-8'))
    lote = json.loads(a.lote.read_text(encoding='utf-8'))
    base = {r['ID_Intervencion']: r for r in read_rows(core.BASE)}

    por_id = {e['ID_Intervencion']: e for e in reg['Correcciones']}
    agregadas, parcheadas, repetidas, ops_parche = [], [], [], 0
    problemas: list[str] = []

    for e in lote.get('Correcciones', []):
        rid = e['ID_Intervencion']
        if rid not in por_id:
            reg['Correcciones'].append(e)
            por_id[rid] = e
            agregadas.append(rid)
            continue
        if not a.parche:
            repetidas.append(rid)
            continue
        existentes = por_id[rid]['Operaciones']
        nuevas = []
        for op in e['Operaciones']:
            # misma «Antes» exacta => actualizar en vez de duplicar
            coincidencia = next((x for x in existentes if x['Antes'] == op['Antes']), None)
            if coincidencia is not None:
                coincidencia['Despues'] = op['Despues']
                coincidencia['Justificacion'] = op.get('Justificacion',
                                                      coincidencia.get('Justificacion', ''))
                coincidencia['Contexto'] = op.get('Contexto', coincidencia.get('Contexto', ''))
            else:
                nuevas.append(op)
        fila = base.get(rid)
        if fila is None:
            problemas.append(f'{rid}: no existe en la base')
            continue
        problemas.extend(revisar_parche(rid, fila['Texto'] or '', nuevas, existentes))
        if nuevas:
            existentes.extend(nuevas)
            ops_parche += len(nuevas)
            parcheadas.append(rid)

    ya = {(r['ID_Intervencion'], r['Texto_Original_Fragmento'])
          for r in reg['Revisiones_Sin_Correccion']}
    nuevas_rev = 0
    for r in lote.get('Revisiones_Sin_Correccion', []):
        # El contrato de tests/test_correcciones_ocr_v1.py exige Marca, Motivo y
        # Texto_Original_Fragmento no vacíos. Antes sólo se validaba Marca y eso
        # dejó pasar 51 revisiones sin Motivo: la suite completa falló.
        for campo in ('Marca', 'Motivo', 'Texto_Original_Fragmento'):
            if not (r.get(campo) or '').strip():
                print('RECHAZADA sin %s: %s' % (campo, r['ID_Intervencion']))
                return 1
        clave = (r['ID_Intervencion'], r['Texto_Original_Fragmento'])
        if clave in ya:
            continue
        reg['Revisiones_Sin_Correccion'].append(r)
        ya.add(clave)
        nuevas_rev += 1

    if problemas:
        for p in problemas:
            print('ERROR:', p)
        print('no se escribe el registro: corrija el lote y vuelva a intentar')
        return 1

    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('filas con correccion agregadas:', agregadas or 'ninguna')
    if a.parche:
        print('filas parcheadas:', parcheadas or 'ninguna', f'({ops_parche} operaciones añadidas)')
    print('revisiones agregadas:', nuevas_rev)
    if repetidas:
        print('RECHAZADAS por ya existir (use --parche para añadirles operaciones):', repetidas)
        return 1
    print('total filas con correccion:', len(reg['Correcciones']))
    print('total operaciones:', sum(len(e['Operaciones']) for e in reg['Correcciones']))
    print('total revisiones:', len(reg['Revisiones_Sin_Correccion']))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
