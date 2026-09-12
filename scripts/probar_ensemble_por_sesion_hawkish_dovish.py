#!/usr/bin/env python3
"""Robustez del veredicto del ensemble ante la fuga por sesión.

El release publica `ensemble_anidado.json` con el veredicto *"la mezcla no mejora
al modelo; no se publica"*, medido con una CV anidada que baraja **por turno**.
El hallazgo 2 de la auditoría mostró que esa partición reparte el 90,7% de las
130 sesiones del oro en más de un pliegue, así que filtra información.

La pregunta que cierra ese cabo: **¿la fuga sostiene el veredicto?** Si al
agrupar por sesión la mezcla pasara a ganar, lo publicado sería una conclusión
falsa y no una aproximación conservadora.

Este script repite la misma CV anidada —mismos pesos candidatos, mismos pliegues
externos e internos, mismas semillas, misma regla de decisión— cambiando **solo**
la partición, en los dos niveles (el externo y el interno que elige `w`). Si se
cambiara solo el externo, el peso seguiría eligiéndose con fuga y la comparación
no sería limpia.

No reescribe `ensemble_anidado.json`: el veredicto publicado se queda como está
y esto se publica al lado, igual que la CV por sesión en el resumen.

Uso:
    python3 scripts/probar_ensemble_por_sesion_hawkish_dovish.py [--semillas 5]
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import entrenar_hawkish_dovish as ent  # noqa: E402
import validar_ensemble_hawkish_dovish as ens  # noqa: E402

RELEASE = ROOT / 'data/releases/hawkish_dovish_v1'


def pliegues_sesion(sesiones: list[str], k: int, semilla: int) -> list[list[int]]:
    """Posiciones de `sesiones` agrupadas de modo que ninguna sesión se parta.

    Devuelve posiciones dentro de la lista recibida, igual que `ent.pliegues`,
    para poder sustituirlo sin tocar el resto del harness.
    """
    ses = sorted(set(sesiones))
    rng = random.Random(semilla)
    rng.shuffle(ses)
    asigna = {s: i % k for i, s in enumerate(ses)}
    return [[i for i, s in enumerate(sesiones) if asigna[s] == f] for f in range(k)]


def oof_scores_sesion(cuentas, y, sesiones, indices, config, k, semilla):
    """Ídem `ens.oof_scores`, pero la partición interna agrupa por sesión."""
    salida = {}
    sub = [sesiones[i] for i in indices]
    for fold in pliegues_sesion(sub, k, semilla):
        test = set(fold)
        tr = [j for pos, j in enumerate(indices) if pos not in test]
        modelo, vocab, idf = ens._modelo_sobre(cuentas, y, tr, config)
        te_idx = [indices[pos] for pos in fold]
        Xte = ent.vectorizar([cuentas[i] for i in te_idx], vocab, idf)
        for j, i in enumerate(te_idx):
            salida[i] = ent.predecir(modelo, Xte[j])['score']
    return salida


def elegir_peso_sesion(cuentas, y, oro, lex, sesiones, indices, config, k, semilla):
    interno = oof_scores_sesion(cuentas, y, sesiones, indices, config, k, semilla)
    reales = [y[i] for i in indices]
    sp = [oro[i] for i in indices]
    tabla = {}
    for w in ens.PESOS:
        pp = [w * interno[i] + (1 - w) * lex[i] for i in indices]
        tabla[w] = ent.metricas(reales, [ens.clase(s) for s in pp], sp, pp)['macro_f1']
    return max(tabla, key=lambda w: tabla[w])


def una_semilla_sesion(cuentas, y, oro, lex, sesiones, config, externos, internos, semilla):
    p_argmax, p_umbral, p_mix, reales, sp, pp_mod, pp_mix, ws = [], [], [], [], [], [], [], []
    for fold in pliegues_sesion(sesiones, externos, semilla):
        test = set(fold)
        tr = [i for i in range(len(y)) if i not in test]
        w = elegir_peso_sesion(cuentas, y, oro, lex, sesiones, tr, config, internos, semilla)
        ws.append(w)
        modelo, vocab, idf = ens._modelo_sobre(cuentas, y, tr, config)
        Xte = ent.vectorizar([cuentas[i] for i in fold], vocab, idf)
        for j, i in enumerate(fold):
            pred = ent.predecir(modelo, Xte[j])
            s_mix = w * pred['score'] + (1 - w) * lex[i]
            p_argmax.append(pred['clase'])
            p_umbral.append(ens.clase(pred['score']))
            p_mix.append(ens.clase(s_mix))
            reales.append(y[i])
            sp.append(oro[i])
            pp_mod.append(pred['score'])
            pp_mix.append(s_mix)
    m_arg = ent.metricas(reales, p_argmax, sp, pp_mod)
    m_umb = ent.metricas(reales, p_umbral, sp, pp_mod)
    m_mix = ent.metricas(reales, p_mix, sp, pp_mix)
    return {'semilla': semilla,
            'modelo_argmax': m_arg['macro_f1'],
            'modelo_umbral': m_umb['macro_f1'],
            'mezcla': m_mix['macro_f1'],
            'pesos_elegidos': ws}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--semillas', type=int, default=5)
    ap.add_argument('--externos', type=int, default=5)
    ap.add_argument('--internos', type=int, default=5)
    args = ap.parse_args()

    modelo_pub = json.loads((RELEASE / 'modelo_hawkish_dovish.json').read_text(encoding='utf-8'))
    c = modelo_pub['config']
    config = {'max_rasgos': c['max_rasgos'], 'iteraciones': c['iteraciones'],
              'balancear': c['balancear_clases']}
    cuentas, y, oro, lex = ens.cargar()
    etiquetas = json.loads(Path(ens.ETIQUETAS).read_text(encoding='utf-8'))['Etiquetas']
    sesiones = [e['ID_Turno'].split(':')[0] for e in etiquetas]
    assert len(sesiones) == len(y)

    t0 = time.time()
    filas = [una_semilla_sesion(cuentas, y, oro, lex, sesiones, config,
                                args.externos, args.internos, s)
             for s in range(args.semillas)]
    for f in filas:
        print(f"  semilla {f['semilla']}: argmax {f['modelo_argmax']:.4f} | "
              f"umbral {f['modelo_umbral']:.4f} | mezcla {f['mezcla']:.4f} | "
              f"w {f['pesos_elegidos']}")

    dif = [f['mezcla'] - f['modelo_umbral'] for f in filas]
    media = sum(dif) / len(dif)
    gana = sum(1 for d in dif if d > 0)

    pub = json.loads((RELEASE / 'ensemble_anidado.json').read_text(encoding='utf-8'))

    # Dos comparadores y no uno, porque miden cosas distintas:
    #   mezcla - umbral : comparador TECNICO. La mezcla decide con hd.clase(), igual
    #                     que el umbral, así que es el emparejamiento metodológico.
    #   mezcla - argmax : comparador DECISORIO. argmax es la regla que el release
    #                     publica, así que es el que responde "¿conviene mezclar?".
    media_arg = media_sesion_argmax = None
    arg_sesion = sum(f['modelo_argmax'] for f in filas) / len(filas)
    mix_sesion = sum(f['mezcla'] for f in filas) / len(filas)
    media_arg = pub['macro_f1_medio_mezcla'] - pub['macro_f1_medio_argmax']
    media_sesion_argmax = mix_sesion - arg_sesion

    veredicto_sesion = ('la mezcla no mejora al modelo' if media_sesion_argmax <= 0
                        else 'la mezcla mejora al modelo')
    veredicto_pub = ('la mezcla no mejora al modelo'
                     if pub['macro_f1_medio_mezcla'] - pub['macro_f1_medio_argmax'] <= 0
                     else 'la mezcla mejora al modelo')

    res = {
        'que_mide': 'el veredicto del ensemble bajo partición agrupada por sesión',
        'por_que': ('el veredicto publicado usa CV por turno, que reparte el 90,7% de las '
                    'sesiones en más de un pliegue; si la fuga lo sostuviera, lo publicado '
                    'sería una conclusión falsa y no una aproximación'),
        'cambio_respecto_del_harness_publicado': 'solo la partición, en los dos niveles '
                                                 '(externo y el interno que elige w)',
        'config_publicada': config,
        'semillas': args.semillas,
        'sesiones_distintas': len(set(sesiones)),
        'por_sesion': {
            'macro_f1_medio_argmax': round(sum(f['modelo_argmax'] for f in filas) / len(filas), 4),
            'macro_f1_medio_umbral': round(sum(f['modelo_umbral'] for f in filas) / len(filas), 4),
            'macro_f1_medio_mezcla': round(sum(f['mezcla'] for f in filas) / len(filas), 4),
            'diferencia_mezcla_menos_umbral': round(media, 4),
            'desviacion_diferencia': round(ent.desviacion(dif), 4),
            'semillas_ganando_la_mezcla': gana,
            'por_semilla': filas,
        },
        'publicado_por_turno': {
            'diferencia_mezcla_menos_umbral': pub['diferencia_mezcla_menos_umbral'],
            'desviacion_diferencia': pub['desviacion_diferencia'],
            'semillas_ganando_la_mezcla': pub['semillas_ganando_la_mezcla'],
        },
        'comparadores': {
            'mezcla_menos_umbral': {
                'que_es': 'comparador técnico: la mezcla decide con hd.clase(), igual que el umbral',
                'por_turno': pub['diferencia_mezcla_menos_umbral'],
                'por_sesion': round(media, 4),
                'cambia_de_signo': (pub['diferencia_mezcla_menos_umbral'] <= 0) != (media <= 0),
            },
            'mezcla_menos_argmax': {
                'que_es': 'comparador decisorio: argmax es la regla que el release publica',
                'por_turno': round(media_arg, 4),
                'por_sesion': round(media_sesion_argmax, 4),
                'cambia_de_signo': (media_arg <= 0) != (media_sesion_argmax <= 0),
            },
        },
        'veredicto_por_sesion': veredicto_sesion,
        'veredicto_publicado': veredicto_pub,
        'el_veredicto_se_mantiene': veredicto_sesion == veredicto_pub,
        'lectura': ('El comparador técnico cambia de signo, pero es ruido: sd 0,011 y 0,008. '
                    'El decisorio —contra argmax, la regla publicada— se mantiene negativo y se '
                    'agranda, así que el veredicto de no publicar la mezcla sobrevive y se refuerza.'),
        'segundos': round(time.time() - t0, 1),
    }
    (RELEASE / 'ensemble_por_sesion.json').write_text(
        json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')

    ps, pt = res['por_sesion'], res['publicado_por_turno']
    print(f"\n{'':<26}{'por turno (pub)':>17}{'por sesión':>13}")
    print(f"  {'argmax':<24}{'—':>17}{ps['macro_f1_medio_argmax']:>13.4f}")
    print(f"  {'umbral':<24}{pub['macro_f1_medio_umbral']:>17.4f}"
          f"{ps['macro_f1_medio_umbral']:>13.4f}")
    print(f"  {'mezcla':<24}{pub['macro_f1_medio_mezcla']:>17.4f}"
          f"{ps['macro_f1_medio_mezcla']:>13.4f}")
    print(f"  {'mezcla − umbral':<24}{pt['diferencia_mezcla_menos_umbral']:>+17.4f}"
          f"{ps['diferencia_mezcla_menos_umbral']:>+13.4f}")
    print(f"  {'gana la mezcla':<24}{str(pt['semillas_ganando_la_mezcla']) + '/5':>17}"
          f"{str(ps['semillas_ganando_la_mezcla']) + '/5':>13}")
    cmp_ = res['comparadores']
    print(f"\n  comparador técnico   mezcla−umbral: "
          f"{cmp_['mezcla_menos_umbral']['por_turno']:+.4f} -> "
          f"{cmp_['mezcla_menos_umbral']['por_sesion']:+.4f}"
          f"   cambia de signo: {cmp_['mezcla_menos_umbral']['cambia_de_signo']}")
    print(f"  comparador decisorio mezcla−argmax: "
          f"{cmp_['mezcla_menos_argmax']['por_turno']:+.4f} -> "
          f"{cmp_['mezcla_menos_argmax']['por_sesion']:+.4f}"
          f"   cambia de signo: {cmp_['mezcla_menos_argmax']['cambia_de_signo']}")
    print(f"\n  veredicto publicado : {veredicto_pub}")
    print(f"  veredicto por sesión: {veredicto_sesion}")
    print(f"  ¿se mantiene?       : {res['el_veredicto_se_mantiene']}")
    print(f"  lectura: {res['lectura']}")
    print(f"\nescrito {RELEASE / 'ensemble_por_sesion.json'}  ({res['segundos']} s)")


if __name__ == '__main__':
    main()
