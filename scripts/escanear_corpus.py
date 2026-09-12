#!/usr/bin/env python3
"""Escáner transversal: busca familias de daño por OCR en las 9.723 filas.

**Por qué existe.** Medido en la ronda 192: de las 831 filas corregidas, 526
(63 %) caen en filas que aún no se habían leído. Es decir, lo que encuentra los
defectos son las pasadas transversales sobre el corpus completo, no la lectura
secuencial — y el plan estaba al revés. Este script permite hacer esas pasadas
sin leer fila por fila.

**Qué no es.** No es una regla automática y no corrige nada. Es un generador de
candidatos: imprime casos para que un humano los revise uno por uno, igual que
todo lo demás del criterio. La política del usuario sigue siendo «cero reglas
automáticas, curado fila por fila».

**Por qué no usa rareza.** Medido y descartado: hay 5.917 hapax de largo >= 7
(5.435 empezando en minúscula) y casi todos son palabras reales y raras
(``abstuvo``, ``ablandó``, ``Abenomics``). La rareza no discrimina. Tampoco un
pre-escáner genérico: medido antes, 14 de 31 aciertos (45 % de recall).

**Qué sí discrimina.** Exigir una **contraparte frecuente en el corpus**. Los dos
detectores de aquí funcionan así, y por eso son de alta precisión:

1. ``acento``  — una palabra que no existe en el corpus, cuya forma sin acentos
                 coincide con una palabra que sí existe y es frecuente, y que
                 difiere de ella sólo en la colocación del acento.
                 (``Adicíonalmente`` y ``Adícionalmente`` -> ``Adicionalmente``)
2. ``partida`` — dos tokens vecinos cuya concatenación sin espacio es una palabra
                 frecuente del corpus. (``Análisi s`` -> ``Análisis``,
                 ``subpri me`` -> ``subprime``)

Uso::

    python scripts/escanear_corpus.py --detector acento  --min-frec 20
    python scripts/escanear_corpus.py --detector partida --min-frec 30
    python scripts/escanear_corpus.py --todo --limite 20
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import correcciones_ocr_v1 as core  # noqa: E402
from diagnosticar_finales import read_rows  # noqa: E402

TOKEN = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")
VOCALES_ACENTUADAS = set('ÁÉÍÓÚáéíóú')
# Las únicas letras sueltas que son palabra en español. Fuera de éstas, un token
# de una letra es casi siempre el residuo de una palabra partida por el OCR.
LETRAS_PALABRA = {'a', 'y', 'o', 'e', 'u', 'A'}


def plegar(s: str) -> str:
    s = unicodedata.normalize('NFD', s)
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')


def construir_indices(salida: dict):
    freq: Counter[str] = Counter()
    for t in salida.values():
        freq.update(TOKEN.findall(t))
    # forma plegada -> forma canónica más frecuente del corpus
    por_plegada: dict[str, Counter[str]] = defaultdict(Counter)
    for w, c in freq.items():
        por_plegada[plegar(w).lower()][w] += c
    canon = {p: c.most_common(1)[0][0] for p, c in por_plegada.items()}
    return freq, canon


def detector_acento(salida: dict, freq: Counter, canon: dict, min_frec: int,
                    limite: int) -> None:
    """Acento en el sitio equivocado, o acento que sobra/falta.

    Se acepta el caso sólo si la forma correcta es frecuente en el corpus
    (``min_frec``) y la forma observada no aparece en ninguna otra parte: así no
    se propone «corregir» una palabra real poco usada.
    """
    print(f'--- detector acento (contraparte con frecuencia >= {min_frec}) ---')
    casos = []
    for rid in sorted(salida):
        t = salida[rid]
        for m in TOKEN.finditer(t):
            w = m.group()
            if len(w) < 5:
                continue
            correcta = canon.get(plegar(w).lower())
            # La forma observada no puede estar atestiguada en serio: si aparece
            # tanto como la canónica, es una variante real, no un daño. Ojo: un
            # hapax SÍ está en freq (con conteo 1), así que no basta con mirar
            # la pertenencia — hay que comparar magnitudes.
            if not correcta or correcta == w:
                continue
            if freq[correcta] < min_frec:
                continue
            if freq[w] * 10 > freq[correcta]:
                continue                      # magnitudes comparables: no es marginal
            if plegar(w) != plegar(correcta):
                continue
            if set(w.lower()) & VOCALES_ACENTUADAS == set(correcta.lower()) & VOCALES_ACENTUADAS:
                continue                      # mismo acento: diferencia de caja u otra
            casos.append((rid, m.start(), w, correcta, freq[correcta], t))
    vistos = defaultdict(int)
    for rid, i, w, correcta, f, t in casos:
        vistos[w] += 1
        if vistos[w] > 1:
            continue
        print('  %-22s -> %-22s (frec %5d)  %-22s ...%s...'
              % (w, correcta, f, rid, t[max(0, i - 35):i + len(w) + 25].replace('\n', '⏎')))
        if sum(vistos.values()) >= limite:
            break
    print(f'  total candidatos: {len(casos)} en {len({c[0] for c in casos})} filas')


def detector_partida(salida: dict, freq: Counter, min_frec: int, limite: int) -> None:
    """Palabra partida en dos por un espacio espurio.

    Se exige que la palabra junta sea frecuente y que las dos mitades por
    separado no lo sean: si una mitad es una palabra común, el espacio es real.

    **No se puede hacer con un regex de pares.** ``re.finditer`` no solapa: en
    «un crecim iento» empareja ``un``+``crecim``, consume ambos y la pareja
    ``crecim``+``iento`` nunca se evalúa. Medido: con el regex el detector daba
    «0 candidatos» cuando todavía quedaban 3 ``crecim iento``, 5 ``trim estre``
    y 3 ``econom ías`` en la salida. Hay que recorrer posiciones de token.
    """
    print(f'--- detector partida (palabra junta con frecuencia >= {min_frec}) ---')
    casos = []
    for rid in sorted(salida):
        t = salida[rid]
        toks = list(TOKEN.finditer(t))
        for k in range(len(toks) - 1):
            a, b = toks[k], toks[k + 1]
            if t[a.end():b.start()] != ' ':
                continue                      # no los separa un único espacio
            junta = a.group() + b.group()
            if junta not in freq or freq[junta] < min_frec:
                continue
            # si las dos mitades son palabras corrientes, el espacio es legítimo.
            # Excepción: una mitad de UNA letra que no sea palabra española. La
            # guarda se pensó para no juntar «de la», pero con letras sueltas se
            # vuelve al revés: el token «m» aparece 78 veces y «a» 37.528, así que
            # bloqueaba TODO «m ayor» o «m onetaria». Y una letra suelta es
            # frecuente precisamente porque la OCR parte palabras. Medido: con la
            # guarda sin excepción el detector daba 0 candidatos cuando quedaban
            # 62 en 39 filas (§23).
            es_letra_suelta = len(a.group()) == 1 and a.group() not in LETRAS_PALABRA
            if freq.get(a.group(), 0) >= 50 and not es_letra_suelta:
                continue
            if freq.get(b.group(), 0) >= 50:
                continue
            casos.append((rid, a.start(), a.group(), b.group(), junta, freq[junta], t))
    vistos = defaultdict(int)
    for rid, i, a, b, junta, f, t in casos:
        vistos[junta] += 1
        if vistos[junta] > 1:
            continue
        print('  %-12s %-12s -> %-20s (frec %5d)  %-22s ...%s...'
              % (a, b, junta, f, rid, t[max(0, i - 30):i + len(a) + len(b) + 22].replace('\n', '⏎')))
        if sum(vistos.values()) >= limite:
            break
    print(f'  total candidatos: {len(casos)} en {len({c[0] for c in casos})} filas')


CORTO = re.compile(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{1,4}')
CARRERA = re.compile(r'(?<![A-Za-zÁÉÍÓÚÜÑáéíóúüñ])'
                     r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{1,4}'
                     r'(?: [A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{1,4})+'
                     r'(?![A-Za-zÁÉÍÓÚÜÑáéíóúüñ])')


def detector_deletreada(salida: dict, freq: Counter, min_frec: int,
                        limite: int) -> None:
    """Palabra deletreada con espacios: «n o tic ia s» -> «noticias».

    Es otra familia que la de ``detector_partida``. Éste busca una partición en
    **dos** mitades; aquí el OCR esparce la palabra en una carrera de trozos
    cortos (``T a m b ié n``, ``c o rre g ir``, ``C o m isió n``, ``T a s a``).
    Medido en §26: el detector de partidas no las veía y había 265 candidatas.

    Tres trampas que ya costaron un conteo falso cada una:

    1. **Fronteras.** Sin ``(?<![letra])`` se detecta «panora**ma de**» como
       ``ma de`` -> ``made`` y «Euro**pa y**» como ``pa y`` -> ``pay``: 96
       candidatas, casi todas falsas.
    2. **El regex greedioso entrega sólo la carrera completa.** En
       ``n o tic ia s han sido`` la carrera maximal se une en
       ``noticiashansido``, que no es palabra, y ``re.finditer`` **no vuelve
       atrás por un filtro posterior**: la buena se perdía entera. Hay que
       enumerar sub-ventanas y tomar, por posición de inicio, la más larga que
       una en palabra real. Síntoma: ``freq['noticias'] = 944`` y el detector
       devolvía 0.
    3. **La frecuencia no sirve para letras sueltas.** Pedir «un trozo que no
       sea palabra» con ``freq == 0`` descartaba ``n o tic ia s`` porque ``n``
       aparece 24 veces, ``ia`` 22 y ``s`` 90 — y aparecen justamente porque
       este mismo defecto las esparce por el corpus. La regla es doble: basta un
       trozo con ``freq < min_frec``, **o** que sean 3+ letras sueltas seguidas,
       que nunca son español legítimo. La segunda mitad es la que hizo aparecer
       ``T a s a`` -> ``Tasa``, que la primera perdía porque ``T`` tiene 38.
    """
    print(f'--- detector deletreada (palabra unida con frecuencia >= {min_frec}) ---')
    casos = []
    for rid in sorted(salida):
        t = salida[rid]
        for m in CARRERA.finditer(t):
            trozos = [(x.group(), x.start() + m.start())
                      for x in CORTO.finditer(m.group())]
            usados = set()
            for i in range(len(trozos)):
                if i in usados:
                    continue
                for j in range(len(trozos), i + 1, -1):
                    pedazo = trozos[i:j]
                    unida = ''.join(x[0] for x in pedazo)
                    if len(unida) < 3 or freq[unida] < min_frec:
                        continue
                    sueltas = all(len(x[0]) == 1 for x in pedazo)
                    if not (sueltas and len(pedazo) >= 3):
                        if all(freq.get(x[0], 0) >= min_frec for x in pedazo):
                            continue
                    for k in range(i, i + len(pedazo)):
                        usados.add(k)
                    frag = t[pedazo[0][1]:pedazo[-1][1] + len(pedazo[-1][0])]
                    casos.append((rid, pedazo[0][1], frag, unida,
                                  freq[unida], t))
                    break
    vistos = defaultdict(int)
    for rid, i, frag, unida, f, t in casos:
        vistos[unida] += 1
        if vistos[unida] > 1:
            continue
        print('  %-22r -> %-14s (frec %6d)  %-22s ...%s...'
              % (frag, unida, f, rid,
                 t[max(0, i - 30):i + len(frag) + 22].replace('\n', '⏎')))
        if sum(vistos.values()) >= limite:
            break
    print(f'  total candidatos: {len(casos)} en {len({c[0] for c in casos})} filas')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', type=Path, default=core.BASE)
    ap.add_argument('--detector', choices=['acento', 'partida', 'deletreada'])
    ap.add_argument('--todo', action='store_true')
    ap.add_argument('--min-frec', type=int, default=20)
    ap.add_argument('--limite', type=int, default=20)
    a = ap.parse_args()

    reg = core.cargar()
    ok, problemas, corregidas, _ = core.validar(reg=reg, base=a.base)
    if not ok:
        for p in problemas[:10]:
            print('ERROR:', p)
        return 1
    virgen = {r['ID_Intervencion']: (r['Texto'] or '') for r in read_rows(a.base)}
    salida = {rid: corregidas.get(rid, t) for rid, t in virgen.items()}
    print(f'escaneando {len(salida)} filas corregidas\n')
    freq, canon = construir_indices(salida)

    if a.todo or a.detector == 'acento':
        detector_acento(salida, freq, canon, a.min_frec, a.limite)
        print()
    if a.todo or a.detector == 'partida':
        detector_partida(salida, freq, a.min_frec, a.limite)
        print()
    if a.todo or a.detector == 'deletreada':
        detector_deletreada(salida, freq, a.min_frec, a.limite)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
