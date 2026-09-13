#!/usr/bin/env python3
"""Mide formas en el corpus: en la base virgen y en la salida corregida.

Este script existe porque el harness de medición vivía en ``.cache/`` y el
workspace se ha reiniciado nueve veces, borrándolo cada una. Cada vez hubo que
reescribir los probes de memoria. Ahora está versionado.

Reglas de uso que este script aplica y que conviene no olvidar:

* **Nunca mida sobre filas unidas.** ``' '.join(...)`` inventa fronteras y hace
  aparecer pares de palabras que no existen (medido: letras sueltas 38/10 unidas
  frente a 27/0 reales).
* **Los conteos de base y de salida no son iguales.** ``ai`` dio 31 en base y 26
  en salida; ``X!`` dio 47 y 42. Declare siempre de qué lado mide.
* **Un substring no delimitado infla.** ``ratando`` cabe dentro de ``tratando``.
  Use ``--palabra`` para exigir frontera.

Uso::

    python scripts/medir_corpus.py IPCXI dellPC "IPCX 1"
    python scripts/medir_corpus.py --palabra IPCX --contexto 60
    python scripts/medir_corpus.py --hapax --min-largo 6 --limite 40
    python scripts/medir_corpus.py --vocabulario --top 30
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import correcciones_ocr_v1 as core  # noqa: E402
from diagnosticar_finales import read_rows  # noqa: E402

TOKEN = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{2,}")


def cargar_lados(base: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Devuelve (base virgen, salida corregida) como dict id -> texto."""
    reg = core.cargar()
    ok, problemas, corregidas, _ = core.validar(reg=reg, base=base)
    if not ok:
        for p in problemas[:10]:
            print('ERROR:', p)
        raise SystemExit(1)
    virgen = {r['ID_Intervencion']: (r['Texto'] or '') for r in read_rows(base)}
    salida = {rid: corregidas.get(rid, t) for rid, t in virgen.items()}
    return virgen, salida


def contar(formas: list[str], virgen: dict, salida: dict, palabra: bool,
           contexto: int, limite: int) -> None:
    print('%-24s %8s %8s' % ('forma', 'base', 'salida'))
    for f in formas:
        if palabra:
            pat = re.compile(r'(?<![A-Za-zÁÉÍÓÚÜÑáéíóúüñ])' + re.escape(f)
                             + r'(?![A-Za-zÁÉÍÓÚÜÑáéíóúüñ])')
            nb = sum(len(pat.findall(t)) for t in virgen.values())
            ns = sum(len(pat.findall(t)) for t in salida.values())
        else:
            nb = sum(t.count(f) for t in virgen.values())
            ns = sum(t.count(f) for t in salida.values())
        aviso = ''
        if nb and not ns:
            aviso = '  <- resuelta'
        elif not nb and ns:
            aviso = '  <- introducida'
        elif ns > nb:
            aviso = f'  <- sube (+{ns - nb})'
        print('%-24s %8d %8d%s' % (f, nb, ns, aviso))
        if contexto:
            vistos = 0
            for rid in sorted(salida):
                t = salida[rid]
                i = t.find(f)
                if i < 0:
                    continue
                print('      %-22s ...%s...'
                      % (rid, t[max(0, i - contexto):i + len(f) + contexto].replace('\n', '⏎')))
                vistos += 1
                if vistos >= limite:
                    break


def hapax(virgen: dict, salida: dict, min_largo: int, limite: int,
          minuscula: bool = False) -> None:
    """Palabras que aparecen una sola vez en las 9.723 filas.

    Es la mejor señal barata de daño por OCR que se puede obtener sin leer: una
    palabra real de este dominio aparece muchas veces; una palabra dañada suele
    aparecer una. No es una regla automática — es un generador de candidatos que
    un humano tiene que revisar caso por caso, igual que todo lo demás.

    Medido: sin filtro hay 5.917 hapax de largo >= 7, y casi todos son legítimos
    (palabras que inician oración, nombres propios, términos foráneos como
    ``Abenomics`` o ``Agricole``). Con ``minuscula=True`` el ruido cae fuerte,
    porque una palabra dañada rara vez abre una oración.
    """
    freq_base: Counter[str] = Counter()
    freq_sal: Counter[str] = Counter()
    donde: dict[str, tuple[str, int]] = {}
    for rid, t in virgen.items():
        for w in TOKEN.findall(t):
            freq_base[w] += 1
    for rid, t in salida.items():
        for m in TOKEN.finditer(t):
            w = m.group()
            freq_sal[w] += 1
            if freq_sal[w] == 1:
                donde[w] = (rid, m.start())
    h = sorted(w for w, c in freq_sal.items() if c == 1 and len(w) >= min_largo)
    if minuscula:
        h = [w for w in h if w[0].islower()]
    print(f'palabras distintas en la salida: {len(freq_sal)}')
    print(f'hapax (aparecen 1 vez) de largo >= {min_largo}'
          f'{" en minúscula" if minuscula else ""}: {len(h)}')
    print()
    for w in h[:limite]:
        rid, i = donde[w]
        t = salida[rid]
        print('  %-22s %-22s ...%s...' % (w, rid, t[max(0, i - 40):i + len(w) + 25].replace('\n', '⏎')))
    if len(h) > limite:
        print(f'  ... y {len(h) - limite} más')


def vocabulario(salida: dict, top: int) -> None:
    freq: Counter[str] = Counter()
    for t in salida.values():
        freq.update(TOKEN.findall(t))
    print(f'palabras distintas: {len(freq)}')
    for w, c in freq.most_common(top):
        print('  %-24s %6d' % (w, c))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('formas', nargs='*')
    ap.add_argument('--base', type=Path, default=core.BASE)
    ap.add_argument('--palabra', action='store_true', help='exigir frontera de palabra')
    ap.add_argument('--contexto', type=int, default=0, help='caracteres de contexto por lado')
    ap.add_argument('--limite', type=int, default=8)
    ap.add_argument('--hapax', action='store_true')
    ap.add_argument('--min-largo', type=int, default=6)
    ap.add_argument('--minuscula', action='store_true',
                    help='sólo hapax que empiezan en minúscula: quita el ruido de '
                         'palabras que abren oración y de nombres propios')
    ap.add_argument('--vocabulario', action='store_true')
    ap.add_argument('--top', type=int, default=30)
    a = ap.parse_args()
    virgen, salida = cargar_lados(a.base)
    print(f'filas: {len(virgen)} | filas con Texto_Corregido: '
          f'{sum(1 for r, t in virgen.items() if salida[r] != t)}')
    print()
    if a.hapax:
        hapax(virgen, salida, a.min_largo, a.limite, a.minuscula)
    if a.vocabulario:
        vocabulario(salida, a.top)
    if a.formas:
        contar(a.formas, virgen, salida, a.palabra, a.contexto, a.limite)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
