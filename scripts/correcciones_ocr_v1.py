#!/usr/bin/env python3
"""Aplica el registro curado de correcciones de OCR sobre la v7.

Política fijada por el usuario (2026-09-10):

* ``Texto`` queda **verbatim, intacto**. Es la fuente documental.
* Las correcciones viven en una columna paralela ``Texto_Corregido``.
* **Cero reglas automáticas.** Cada operación está curada a mano sobre una
  fila leída completa, con su contexto y su justificación.
* Los residuos del documento fuente (números de página, símbolos sueltos,
  firmas truncadas) **se eliminan** en ``Texto_Corregido``.
* Lo que no se pudo resolver a partir del texto va marcado en una tercera
  columna, ``Cotejar_PDF``, con vocabulario controlado: es la lista de trabajo
  para cuando se tenga el PDF original a la vista.

Contratos que valida antes de escribir:

1. ``Antes`` debe aparecer en el texto virgen de la fila exactamente las veces
   declaradas. Si no aparece, la corrida falla: no se adivina.
2. Dos operaciones de una misma entrada no pueden pisarse: el ``Antes`` de
   cada una se comprueba contra el texto virgen, no contra el intermedio.
3. Una fila sin operaciones no genera ``Texto_Corregido``.
4. Toda revisión descartada lleva ``Marca``, tomada del vocabulario.
5. Toda palabra que un ``Despues`` **introduce** debe existir en el corpus
   virgen (ignorando acentos y mayúsculas) o estar en ``TERMINOS_FORANEOS``.
   El ``Antes`` siempre estuvo controlado; el reemplazo no, y un ``Despues``
   mal escrito pasaba en silencio.

Uso::

    python scripts/correcciones_ocr_v1.py --base <v7.xlsx> --destino <dir>
    python scripts/correcciones_ocr_v1.py --validar
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

from openpyxl import load_workbook

sys.path.insert(0, str(Path(__file__).resolve().parent))
from diagnosticar_finales import read_rows  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
REGISTRO = RAIZ / 'data' / 'curation' / 'correcciones_ocr_v1.json'
# La base vigente es la entrega v8 (v7 + los cuatro cortes del lote10). v7 queda
# como referencia histórica y no se modifica; el registro se ancla a la base actual.
BASE = (RAIZ / 'data' / 'releases' / 'continuidad_procedimental_v11'
        / 'consolidado_base_referencia_final.xlsx')
COLUMNA = 'Texto_Corregido'
COLUMNA_COTEJO = 'Cotejar_PDF'

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
    'ESPACIO_FALTANTE',       # «caer yeso» -> «caer y eso», «individualmente,se» -> «individualmente, se»
    'PUNTUACION',             # puntuación ausente o duplicada
    'PALABRA_OMITIDA',        # «alta base comparación» -> «alta base de comparación»
    'SALTOS_DE_LINEA',        # una palabra por línea, artefacto de justificación del PDF
    'PALABRA_SOBRANTE',       # «renta de variable» -> «renta variable»
}

# Vocabulario de la columna Cotejar_PDF. Cada valor dice qué hay que mirar en
# el PDF original y por qué el texto no alcanza para resolverlo.
MARCAS_VALIDAS = {
    'NOMBRE_PROPIO_POR_COTEJAR',
    'CARGO_EN_DISCURSO_POR_COTEJAR',
    'CIFRA_INCONSISTENTE_POR_COTEJAR',
    'RECONSTRUCCION_AMBIGUA_POR_COTEJAR',
    'SIGNO_AUSENTE_POR_COTEJAR',
    'RESERVA_ABIERTA_POR_COTEJO',
    'NO_REQUIERE_COTEJO',
}

# La alerta del motor ya dice «por cotejar»: se arrastra sola a la columna.
MOTIVO_QUE_MARCA = 'TEXTO_DANADO_POR_COTEJAR'

# Términos foráneos que una corrección puede introducir legítimamente aunque no
# figuren en el corpus virgen. Cada uno está aquí por una razón verificada; si
# aparece otro, hay que justificarlo igual.
TERMINOS_FORANEOS = {
    'fly',   # «fly to quality»: el corpus sólo trae «flight to quality», y las
             # 9 correcciones «fiy»/«fIy» -> «fly» son justamente eso (§10).
    'selection',   # «selection bias»: el corpus virgen trae la forma dañada
                   # «se/ection bias» dos veces y nunca la correcta, así que el
                   # vocabulario no la contiene. La barra sustituye a la «l»,
                   # igual que en «Defau/t» -> «Default» (§21).
}

_TOKEN = None  # se compila en _vocabulario()
_PLEGADO: dict[str, set[str]] | None = None


def _vocabulario(textos) -> tuple[set[str], set[str]]:
    """Palabras del corpus virgen, en crudo y plegadas (sin acento ni caja).

    El plegado es lo que permite aceptar «exportó» o «Subsecretaria» cuando el
    corpus sólo trae «exporto» o «subsecretaria»: no son palabras inventadas,
    son la misma palabra con la ortografía repuesta.
    """
    global _TOKEN
    import re
    import unicodedata
    if _TOKEN is None:
        _TOKEN = re.compile(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{2,}')

    def plegar(s: str) -> str:
        s = unicodedata.normalize('NFD', s)
        s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
        return s.lower()

    crudo, plegado = set(), set()
    for t in textos:
        crudo.update(_TOKEN.findall(t))
    plegado = {plegar(w) for w in crudo}
    return crudo, plegado


def revisar_reemplazos(reg: dict, textos) -> list[str]:
    """Controla el lado ``Despues``, que hasta ahora nadie miraba.

    ``validar`` comprobaba el ``Antes`` con rigor (que exista, que sea único, que
    los tramos no se pisen) pero del reemplazo sólo exigía que algo cambiara: un
    ``Despues`` mal escrito pasaba en silencio. Aquí cada palabra que una
    operación **introduce** (presente en ``Despues`` y ausente en ``Antes``) debe
    existir en el corpus virgen, o coincidir con una palabra del corpus ignorando
    acentos y mayúsculas, o estar en ``TERMINOS_FORANEOS``.

    Medido sobre el registro curado: 1.057 de 1.069 operaciones pasan sin ayuda;
    las 12 restantes son «exportó», «etáreos», «Subsecretaria» y «fly» (×9), todas
    cubiertas por el plegado o por la lista explícita.
    """
    crudo, plegado = _vocabulario(textos)

    def plegar(s: str) -> str:
        import unicodedata
        s = unicodedata.normalize('NFD', s)
        return ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()

    problemas: list[str] = []
    for entrada in reg.get('Correcciones', []):
        rid = entrada['ID_Intervencion']
        for n, op in enumerate(entrada.get('Operaciones') or [], 1):
            antes = set(_TOKEN.findall(op['Antes']))
            for tok in _TOKEN.findall(op['Despues']):
                if tok in antes:
                    continue
                if tok in crudo or tok in TERMINOS_FORANEOS:
                    continue
                if plegar(tok) in plegado:
                    continue
                problemas.append(
                    f'{rid} op{n} ({op["Tipo"]}): el reemplazo introduce «{tok}», '
                    f'que no está en el corpus ni en TERMINOS_FORANEOS')
    return problemas


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


def validar(reg: dict | None = None, base: Path = BASE):
    reg = reg or cargar()
    filas = {r['ID_Intervencion']: r for r in read_rows(base)}
    problemas: list[str] = []
    corregidas: dict[str, str] = {}
    marcas: dict[str, list[str]] = defaultdict(list)

    pol = reg.get('Politica', {})
    if pol.get('Texto_Verbatim') != 'INTACTO':
        problemas.append('la política debe declarar Texto_Verbatim = INTACTO')
    if pol.get('Reglas_Automaticas') is not False:
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

    for rev in reg.get('Revisiones_Sin_Correccion', []):
        marca = rev.get('Marca')
        if marca not in MARCAS_VALIDAS:
            problemas.append(
                f"{rev.get('ID_Intervencion')}: Marca {marca!r} fuera del "
                f'vocabulario {sorted(MARCAS_VALIDAS)}')
            continue
        for rid in [x.strip() for x in rev['ID_Intervencion'].split('/')]:
            if rid and rid not in filas:
                problemas.append(f'{rid}: marcado para cotejo pero no existe en la base')
                continue
            if marca != 'NO_REQUIERE_COTEJO' and marca not in marcas[rid]:
                marcas[rid].append(marca)

    for extra in reg.get('Marcas_Adicionales', []):
        rid = extra['ID_Intervencion']
        if rid not in filas:
            problemas.append(f'{rid}: no existe en la base')
            continue
        if extra.get('Marca') not in MARCAS_VALIDAS:
            problemas.append(f"{rid}: Marca {extra.get('Marca')!r} fuera del vocabulario")
            continue
        if extra['Marca'] != 'NO_REQUIERE_COTEJO' and extra['Marca'] not in marcas[rid]:
            marcas[rid].append(extra['Marca'])

    for rid, fila in filas.items():
        if MOTIVO_QUE_MARCA in (fila.get('Motivos_Revision') or ''):
            if MOTIVO_QUE_MARCA not in marcas[rid]:
                marcas[rid].append(MOTIVO_QUE_MARCA)

    problemas.extend(revisar_reemplazos(reg, [f['Texto'] or '' for f in filas.values()]))

    return (not problemas), problemas, corregidas, dict(marcas)


def construir(base: Path, destino: Path) -> int:
    ok, problemas, corregidas, marcas = validar(base=base)
    if not ok:
        for p in problemas:
            print('ERROR:', p)
        return 1

    wb = load_workbook(base, data_only=True)
    ws = wb['Consolidado']
    cabecera = [c.value for c in ws[1]]
    idx_id = cabecera.index('ID_Intervencion') + 1
    col_txt, col_mar = len(cabecera) + 1, len(cabecera) + 2
    ws.cell(row=1, column=col_txt, value=COLUMNA)
    ws.cell(row=1, column=col_mar, value=COLUMNA_COTEJO)
    n_txt = n_mar = 0
    for r in range(2, ws.max_row + 1):
        rid = ws.cell(row=r, column=idx_id).value
        if rid in corregidas:
            ws.cell(row=r, column=col_txt, value=corregidas[rid])
            n_txt += 1
        if rid in marcas:
            ws.cell(row=r, column=col_mar, value=';'.join(sorted(marcas[rid])))
            n_mar += 1
    destino.mkdir(parents=True, exist_ok=True)
    wb.save(destino / 'consolidado_texto_corregido.xlsx')
    por_marca: dict[str, int] = defaultdict(int)
    for v in marcas.values():
        for m in v:
            por_marca[m] += 1
    (destino / 'correcciones_aplicadas.json').write_text(
        json.dumps({'Total_Filas_Corregidas': n_txt,
                    'Total_Operaciones': sum(len(e['Operaciones'])
                                             for e in cargar()['Correcciones']),
                    'Total_Filas_Marcadas_Para_Cotejo': n_mar,
                    'Marcas_Por_Tipo': dict(sorted(por_marca.items())),
                    'Filas_Corregidas': sorted(corregidas),
                    'Filas_Marcadas': sorted(marcas)},
                   ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'filas con {COLUMNA}: {n_txt}')
    print(f'filas con {COLUMNA_COTEJO}: {n_mar}')
    for m, c in sorted(por_marca.items()):
        print(f'  {c:5d}  {m}')
    print(f'escrito en {destino}')
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', type=Path, default=BASE)
    ap.add_argument('--destino', type=Path,
                    default=RAIZ / 'data' / 'releases' / 'correccion_ocr_v2')
    ap.add_argument('--validar', action='store_true')
    a = ap.parse_args()
    if a.validar:
        ok, problemas, corregidas, marcas = validar(base=a.base)
        for p in problemas:
            print('ERROR:', p)
        print(f'validacion: {"OK" if ok else "FALLO"} | filas corregibles: '
              f'{len(corregidas)} | filas marcadas para cotejo: {len(marcas)}')
        print('sha256 base:', hashlib.sha256(a.base.read_bytes()).hexdigest())
        return 0 if ok else 1
    return construir(a.base, a.destino)


if __name__ == '__main__':
    raise SystemExit(main())
