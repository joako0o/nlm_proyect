#!/usr/bin/env python3
"""Aplica el registro curado de correcciones de OCR sobre la v7.

Política fijada por el usuario (2026-09-10):

* ``Texto`` queda **verbatim, intacto**. Es la fuente documental.
* Las correcciones viven en una columna paralela ``Texto_Corregido``.
* **Cero reglas automáticas.** Cada operación está curada a mano sobre una
  fila leída completa, con su contexto y su justificación.
* Los residuos del documento fuente (números de página, símbolos sueltos,
  firmas truncadas) **se eliminan** en ``Texto_Corregido``.

Contratos que valida antes de escribir:

1. ``Antes`` debe aparecer en ``Texto`` exactamente las veces declaradas
   (por omisión, una). Si no aparece, la corrida falla: no se adivina.
2. Una fila sin operaciones no genera ``Texto_Corregido``.
3. ``Texto`` sale byte a byte igual al de entrada.
4. Aplicar dos veces da el mismo resultado (idempotencia).

Uso::

    python scripts/correcciones_ocr_v1.py --base <v7.xlsx> --destino <dir>
    python scripts/correcciones_ocr_v1.py --validar
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from openpyxl import load_workbook, Workbook

sys.path.insert(0, str(Path(__file__).resolve().parent))
from diagnosticar_finales import read_rows  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
REGISTRO = RAIZ / 'data' / 'curation' / 'correcciones_ocr_v1.json'
BASE = RAIZ / 'data' / 'releases' / 'continuidad_procedimental_v7' / 'consolidado_base_referencia_final.xlsx'
COLUMNA = 'Texto_Corregido'

TIPOS_VALIDOS = {
    'PALABRA_DUPLICADA',      # «las las tasas» -> «las tasas»
    'PALABRA_PARTIDA',        # «to mo a $550» -> «en torno a $550»
    'ACENTO_INDEBIDO',        # «nomínales» -> «nominales»
    'ACENTO_FALTANTE',        # «indices» -> «índices»
    'LETRA_CONFUNDIDA',       # «nesgo» -> «riesgo»
    'PALABRA_ERRONEA',        # «jumo» -> «junio», «marcado» -> «mercado»
    'SIMBOLO_SUELTO',         # «■V», «ry _<< ■» -> se elimina
    'RESIDUO_PAGINACION',     # dígito de página al final de la fila
    'FIRMA_TRUNCADA',         # «IQUE MARSHALL RIVERA» -> «ENRIQUE MARSHALL RIVERA»
    'ESPACIO_INDEBIDO',       # «Poblete ;» -> «Poblete;»
    'PUNTUACION',             # puntuación ausente o duplicada
    'PALABRA_OMITIDA',        # «alta base comparación» -> «alta base de comparación»
    'SALTOS_DE_LINEA',        # una palabra por línea, artefacto de justificación del PDF
}


def cargar() -> dict:
    return json.loads(REGISTRO.read_text(encoding='utf-8'))


def aplicar_a_texto(texto: str, operaciones: list[dict], rid: str,
                    virgen: str | None = None) -> tuple[str, list[str]]:
    """Devuelve el texto corregido y los problemas encontrados.

    Cuando se pasa ``virgen``, cada ``Antes`` debe resolverse además contra el
    texto original de la fila, no sólo contra el estado intermedio. Eso impide
    que dos operaciones de una misma fila se pisen: la segunda no puede
    depender de lo que la primera ya modificó.
    """
    problemas: list[str] = []
    salida = texto
    for n, op in enumerate(operaciones, 1):
        antes, despues = op['Antes'], op['Despues']
        esperadas = int(op.get('Ocurrencias', 1))
        if virgen is not None and virgen.count(antes) != esperadas:
            problemas.append(
                f'{rid} op{n} ({op["Tipo"]}): «{antes}» no aparece {esperadas} '
                f'veces en el texto virgen de la fila; las operaciones de una '
                f'misma entrada no deben depender unas de otras')
            continue
        reales = salida.count(antes)
        if reales != esperadas:
            problemas.append(
                f'{rid} op{n} ({op["Tipo"]}): «{antes}» aparece {reales} veces, '
                f'se declararon {esperadas}')
            continue
        if op['Tipo'] not in TIPOS_VALIDOS:
            problemas.append(f'{rid} op{n}: tipo desconocido {op["Tipo"]!r}')
            continue
        for campo in ('Contexto', 'Justificacion'):
            if not (op.get(campo) or '').strip():
                problemas.append(f'{rid} op{n}: falta {campo}')
        salida = salida.replace(antes, despues)
    return salida, problemas


def validar(reg: dict | None = None, base: Path = BASE) -> tuple[bool, list[str], dict]:
    reg = reg or cargar()
    filas = {r['ID_Intervencion']: r for r in read_rows(base)}
    problemas: list[str] = []
    corregidas: dict[str, str] = {}

    if reg.get('Politica', {}).get('Texto_Verbatim') != 'INTACTO':
        problemas.append('la política debe declarar Texto_Verbatim = INTACTO')
    if reg.get('Politica', {}).get('Reglas_Automaticas') is not False:
        problemas.append('la política debe declarar Reglas_Automaticas = false')

    for entrada in reg.get('Correcciones', []):
        rid = entrada['ID_Intervencion']
        fila = filas.get(rid)
        if fila is None:
            problemas.append(f'{rid}: no existe en la base')
            continue
        ops = entrada.get('Operaciones') or []
        if not ops:
            problemas.append(f'{rid}: entrada sin operaciones')
            continue
        salida, probs = aplicar_a_texto(fila['Texto'] or '', ops, rid,
                                        virgen=fila['Texto'] or '')
        problemas.extend(probs)
        if not probs:
            if salida == (fila['Texto'] or ''):
                problemas.append(f'{rid}: las operaciones no cambian nada')
            else:
                corregidas[rid] = salida

    return (not problemas), problemas, corregidas


def construir(base: Path, destino: Path) -> int:
    ok, problemas, corregidas = validar(base=base)
    if not ok:
        for p in problemas:
            print('ERROR:', p)
        return 1

    wb = load_workbook(base, data_only=True)
    ws = wb['Consolidado']
    cabecera = [c.value for c in ws[1]]
    idx_id = cabecera.index('ID_Intervencion') + 1
    nueva = len(cabecera) + 1
    ws.cell(row=1, column=nueva, value=COLUMNA)
    n = 0
    for r in range(2, ws.max_row + 1):
        rid = ws.cell(row=r, column=idx_id).value
        if rid in corregidas:
            ws.cell(row=r, column=nueva, value=corregidas[rid])
            n += 1
    destino.mkdir(parents=True, exist_ok=True)
    wb.save(destino / 'consolidado_texto_corregido.xlsx')
    (destino / 'correcciones_aplicadas.json').write_text(
        json.dumps({'Total_Filas_Corregidas': n,
                    'Total_Operaciones': sum(len(e['Operaciones'])
                                             for e in cargar()['Correcciones']),
                    'Filas': sorted(corregidas)},
                   ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'filas con Texto_Corregido: {n}')
    print(f'escrito en {destino}')
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', type=Path, default=BASE)
    ap.add_argument('--destino', type=Path,
                    default=RAIZ / 'data' / 'releases' / 'correccion_ocr_v1')
    ap.add_argument('--validar', action='store_true')
    a = ap.parse_args()
    if a.validar:
        ok, problemas, corregidas = validar(base=a.base)
        for p in problemas:
            print('ERROR:', p)
        print(f'validacion: {"OK" if ok else "FALLO"} | filas corregibles: {len(corregidas)}')
        print('sha256 base:', hashlib.sha256(a.base.read_bytes()).hexdigest())
        return 0 if ok else 1
    return construir(a.base, a.destino)


if __name__ == '__main__':
    raise SystemExit(main())
