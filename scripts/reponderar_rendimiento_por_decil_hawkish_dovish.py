#!/usr/bin/env python3
"""Rendimiento reponderado por el diseño de muestreo.

Las 500 etiquetas oro se sortearon con muestreo ESTRATIFICADO: decil léxico x
anio x grupo de actor, con cuotas por decil (`PESOS_DECIL`) que no son
proporcionales a la población. El docstring de `muestra()` ya lo declara: las
etiquetas sirven para entrenar, no para estimar prevalencia. La prevalencia sí
se reponderó (`prevalencia_reponderada.json`). El RENDIMIENTO, no.

Este script mide lo que falta. Si el modelo rinde distinto según el decil
léxico, el macro-F1 0,702 publicado está calculado sobre una mezcla de deciles
que no es la del universo, y entonces no es la cifra que corresponde al corpus.

Método: pesos de diseño w_h = (N_h/N) / (n_h/n) por decil h. El macro-F1
ponderado usa precisión y recall ponderadas por clase, no un promedio de
subgrupos, porque es lo que responde "cómo le iría al modelo sobre el universo".

Salida: data/releases/hawkish_dovish_v1/rendimiento_reponderado.json

Uso:
    python3 scripts/reponderar_rendimiento_por_decil_hawkish_dovish.py
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import hawkish_dovish as hd  # noqa: E402

RELEASE = ROOT / 'data/releases/hawkish_dovish_v1'
MUESTRA = hd.CURATION / 'muestra_500_hawkish_dovish.csv'
CLASES = ['HAWKISH', 'NEUTRAL', 'DOVISH']


def deciles_universo(pool):
    """Decil léxico por turno, con la misma regla que usa `muestra()`."""
    orden = sorted(pool, key=lambda t: (t['Lex']['score'], t['ID_Turno']))
    k = len(orden)
    dec = {}
    for j, t in enumerate(orden):
        dec[t['ID_Turno']] = min(9, j * 10 // k) + 1
    return dec


def macro_f1_ponderado(filas, peso):
    """macro-F1 con precisión/recall ponderadas por `peso(i)`."""
    tp = defaultdict(float)
    fp = defaultdict(float)
    fn = defaultdict(float)
    for f in filas:
        w = peso(f)
        if f['oro'] == f['pred']:
            tp[f['oro']] += w
        else:
            fp[f['pred']] += w
            fn[f['oro']] += w
    f1s, detalle = [], {}
    for c in CLASES:
        p = tp[c] / (tp[c] + fp[c]) if (tp[c] + fp[c]) > 0 else 0.0
        r = tp[c] / (tp[c] + fn[c]) if (tp[c] + fn[c]) > 0 else 0.0
        f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
        f1s.append(f1)
        detalle[c] = {'precision': round(p, 4), 'recall': round(r, 4), 'f1': round(f1, 4)}
    return sum(f1s) / len(f1s), detalle


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--min-palabras', type=int, default=hd.MIN_PALABRAS_UNIVERSO)
    args = ap.parse_args()

    # --- universo y sus deciles -------------------------------------------------
    pool = hd.universo(hd.cargar_turnos(), args.min_palabras)
    for t in pool:
        t['Lex'] = hd.puntuar_lexico(t['Texto'])
    dec = deciles_universo(pool)
    N = Counter(dec.values())
    n_universo = sum(N.values())

    # --- muestra sorteada -------------------------------------------------------
    with open(MUESTRA, newline='', encoding='utf-8') as f:
        muestra = list(csv.DictReader(f))
    n_muestra = Counter(int(r['Decile_Lex']) for r in muestra)

    # Control: el decil declarado en la muestra debe coincidir con el recálculo.
    desacuerdos = [r['ID_Turno'] for r in muestra if dec.get(r['ID_Turno']) != int(r['Decile_Lex'])]

    # --- predicciones fuera de pliegue ------------------------------------------
    with open(RELEASE / 'fallos_fuera_de_pliegue.csv', newline='', encoding='utf-8') as f:
        oof = list(csv.DictReader(f))
    # La exactitud se recalcula comparando oro y predicción en vez de leer la
    # columna `Acierta`, que en este CSV vale 'SI'/'NO' y no 'true'/'false'.
    filas = []
    for r in oof:
        oro, pred = r['HD_Clase_Oro'], r['Pred_Fuera_De_Pliegue']
        declarada = r['Acierta'].strip().upper() == 'SI'
        filas.append({'id': r['ID_Turno'],
                      'decil': dec[r['ID_Turno']],
                      'oro': oro,
                      'pred': pred,
                      'acierta': oro == pred,
                      'acierta_declarada': declarada})

    # Control: el recálculo debe coincidir con la columna declarada del release.
    choque = [f['id'] for f in filas if f['acierta'] != f['acierta_declarada']]

    # --- pesos de diseño ---------------------------------------------------------
    total_w = 0.0
    pesos = {}
    for f in filas:
        h = f['decil']
        w = (N[h] / n_universo) / (n_muestra[h] / len(filas))
        pesos[f['id']] = w
        total_w += w

    # --- resultados ---------------------------------------------------------------
    macro_sin, detalle_sin = macro_f1_ponderado(filas, lambda f: 1.0)
    macro_pon, detalle_pon = macro_f1_ponderado(filas, lambda f: pesos[f['id']])
    acc_sin = sum(1 for f in filas if f['acierta']) / len(filas)
    acc_pon = sum(pesos[f['id']] for f in filas if f['acierta']) / total_w

    publicado = json.loads((RELEASE / 'resumen_entrenamiento.json').read_text(encoding='utf-8'))
    macro_pub = publicado['validacion_cruzada']['macro_f1']

    por_decil = []
    for h in sorted(N):
        sub = [f for f in filas if f['decil'] == h]
        por_decil.append({
            'decil': h,
            'universo': N[h],
            'fraccion_universo': round(N[h] / n_universo, 4),
            'muestra': n_muestra[h],
            'fraccion_muestra': round(n_muestra[h] / len(filas), 4),
            'peso_disenio': round((N[h] / n_universo) / (n_muestra[h] / len(filas)), 4),
            'etiquetadas': len(sub),
            'accuracy_sin_ponderar': round(sum(1 for f in sub if f['acierta']) / len(sub), 4),
        })

    res = {
        'que_mide': 'el rendimiento publicado reponderado por el diseño de muestreo',
        'por_que': ('las 500 etiquetas se sortearon por decil léxico x anio x grupo con cuotas no '
                    'proporcionales (PESOS_DECIL), así que el macro-F1 publicado está calculado '
                    'sobre una mezcla de deciles que no es la del universo'),
        'metodo': 'pesos de diseño w_h = (N_h/N)/(n_h/n); macro-F1 con precision y recall ponderadas',
        'universo': n_universo,
        'etiquetas': len(filas),
        'deciles_control_coinciden': not desacuerdos,
        'deciles_control_desacuerdos': desacuerdos[:10],
        'acierto_recalculado_coincide_con_el_csv': not choque,
        'acierto_recalculado_desacuerdos': choque[:10],
        'macro_f1_publicado': macro_pub,
        'macro_f1_recalculado_sin_ponderar': round(macro_sin, 4),
        'macro_f1_reponderado': round(macro_pon, 4),
        'diferencia_reponderado_menos_publicado': round(macro_pon - macro_pub, 4),
        'accuracy_sin_ponderar': round(acc_sin, 4),
        'accuracy_reponderada': round(acc_pon, 4),
        'por_clase_sin_ponderar': detalle_sin,
        'por_clase_reponderado': detalle_pon,
        'por_decil': por_decil,
        'suma_pesos': round(total_w, 4),
    }
    (RELEASE / 'rendimiento_reponderado.json').write_text(
        json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f'universo {n_universo} turnos · {len(filas)} etiquetas')
    print(f'  control de deciles : '
          f'{"OK" if res["deciles_control_coinciden"] else "DESACUERDOS"}')
    print(f'  control de acierto : '
          f'{"OK" if res["acierto_recalculado_coincide_con_el_csv"] else "DESACUERDOS"}')
    print(f'  accuracy publicada : {publicado["validacion_cruzada"]["accuracy"]:.4f} '
          f'| recalculada: {acc_sin:.4f}')
    print(f'\n{"":<24}{"sin ponderar":>14}{"reponderado":>14}')
    print(f'  {"macro-F1":<22}{macro_sin:>14.4f}{macro_pon:>14.4f}')
    print(f'  {"accuracy":<22}{acc_sin:>14.4f}{acc_pon:>14.4f}')
    for c in CLASES:
        print(f'  {"F1 " + c:<22}{detalle_sin[c]["f1"]:>14.4f}{detalle_pon[c]["f1"]:>14.4f}')
    print(f'\n  publicado en el release: {macro_pub:.4f}')
    print(f'  diferencia reponderado − publicado: {macro_pon - macro_pub:+.4f}')
    print(f'\n  decil  universo  frac_u  muestra  frac_m  peso   acc')
    for d in por_decil:
        print(f"  {d['decil']:>5}  {d['universo']:>8}  {d['fraccion_universo']:>6.3f}"
              f"  {d['muestra']:>7}  {d['fraccion_muestra']:>6.3f}"
              f"  {d['peso_disenio']:>5.2f}  {d['accuracy_sin_ponderar']:>5.3f}")
    print(f'\nescrito {RELEASE / "rendimiento_reponderado.json"}')


if __name__ == '__main__':
    main()
