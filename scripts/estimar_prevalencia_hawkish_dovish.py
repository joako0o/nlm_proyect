"""Estima la prevalencia de posturas en el universo reponderando las 500 etiquetas oro.

La muestra NO es proporcional a la población: los deciles de puntaje léxico se
repartieron casi parejo para cubrir todo el espectro hawkish/dovish. Por eso el
informe dice que de las 500 no se puede leer prevalencia. Aquí se corrige eso con
post-estratificación por decil: cada etiqueta vale N_d/n_d, el tamaño del decil en
el universo sobre el tamaño del decil en la muestra.

Validez del peso. El sorteo reparte el cupo del decil entre las celdas
(año x grupo de actor) en proporción a su tamaño (`_reparto`, resto mayor) y
muestrea al azar dentro de la celda. La probabilidad de inclusión es entonces
aproximadamente constante dentro del decil, así que el decil es el nivel correcto
de ponderación: 10 celdas estables en vez de 155 con 3 casos de promedio.

Esa hipótesis no se asume: `representatividad_decil` compara la composición por
(año x grupo) de la muestra contra la del universo dentro de cada decil y reporta
la distancia de variación total. Si un decil estuviera sesgado, el peso no lo
arreglaría y habría que leerlo.

Qué NO corrige este cálculo:
  - el sesgo de una sola revisora y de leer el 35% de cada texto;
  - las 3 etiquetas marcadas `Duplicado_Exacto=SI`;
  - que los deciles se definan con el puntaje léxico, que es imperfecto.
El intervalo es sólo el error de muestreo.

Salida:
  data/releases/hawkish_dovish_v1/prevalencia_reponderada.json
  por pantalla: prevalencia con IC95, efecto de la ponderación, tamaño efectivo de
  muestra, representatividad por decil y contraste contra la predicción del modelo.

Uso:
  python3 scripts/estimar_prevalencia_hawkish_dovish.py
"""
import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from entrenar_hawkish_dovish import RELEASE  # noqa: E402
from hawkish_dovish import (MIN_PALABRAS_UNIVERSO, cargar_turnos, grupo_actor,
                            puntuar_lexico, universo)  # noqa: E402
from etiquetar_hawkish_dovish import ETIQUETAS  # noqa: E402

SALIDA = RELEASE / 'prevalencia_reponderada.json'
CLASES = ('HAWKISH', 'NEUTRAL', 'DOVISH')
Z = 1.959963984540054


def deciles_lexico(pool):
    """Asigna el decil de puntaje léxico por rango, igual que `muestra()`.

    Devuelve {ID_Turno: decil}. Los deciles salen de tamaño casi idéntico porque
    se definen por posición en el orden, no por cortes del puntaje.
    """
    orden = sorted(pool, key=lambda t: (t['Lex']['score'], t['ID_Turno']))
    k = len(orden)
    return {t['ID_Turno']: min(9, j * 10 // k) + 1 for j, t in enumerate(orden)}


def preparar(turnos, min_palabras=MIN_PALABRAS_UNIVERSO):
    """Universo con puntaje léxico, grupo de actor y decil asignado."""
    pool = universo(turnos, min_palabras)
    for t in pool:
        t['Lex'] = puntuar_lexico(t['Texto'])
        t['Grupo_Actor'] = grupo_actor(t['Rol_Final'])
    deciles = deciles_lexico(pool)
    for t in pool:
        t['Decile_Lex'] = deciles[t['ID_Turno']]
    return pool


def representatividad_decil(pool, muestra_ids):
    """Distancia de variación total entre muestra y universo, por decil.

    0.0 = composición idéntica por (año x grupo de actor); 1.0 = sin solape.
    Es la hipótesis que justifica ponderar a nivel de decil.
    """
    uni = defaultdict(Counter)
    for t in pool:
        uni[t['Decile_Lex']][(t['Anio'], t['Grupo_Actor'])] += 1
    mue = defaultdict(Counter)
    for t in pool:
        if t['ID_Turno'] in muestra_ids:
            mue[t['Decile_Lex']][(t['Anio'], t['Grupo_Actor'])] += 1
    salida = {}
    for d in sorted(uni):
        nu, nm = sum(uni[d].values()), sum(mue[d].values())
        if not nm:
            continue
        claves = set(uni[d]) | set(mue[d])
        tv = 0.5 * sum(abs(uni[d][k] / nu - mue[d][k] / nm) for k in claves)
        salida[str(d)] = {'universo': nu, 'muestra': nm,
                          'celdas_universo': len(uni[d]),
                          'variacion_total': round(tv, 4)}
    return salida


def prevalencia(pool, etiquetas):
    """Post-estratifica las etiquetas oro por decil y devuelve estimación e IC95."""
    muestra_ids = {e['ID_Turno'] for e in etiquetas}
    dentro = [e for e in etiquetas if e['ID_Turno'] in muestra_ids]
    N_decil, n_decil = Counter(), Counter()
    por_clase = defaultdict(Counter)
    clase_por_id = {e['ID_Turno']: e['HD_Clase'] for e in etiquetas}
    for t in pool:
        N_decil[t['Decile_Lex']] += 1
        if t['ID_Turno'] in clase_por_id:
            d = t['Decile_Lex']
            n_decil[d] += 1
            por_clase[d][clase_por_id[t['ID_Turno']]] += 1

    Ntot = sum(N_decil.values())
    ntot = sum(n_decil.values())
    if ntot != len(dentro):
        raise SystemExit(f'{len(dentro) - ntot} etiquetas fuera del universo: '
                         'no se puede ponderar lo que no está en el marco')

    est, var, pesos = {}, {}, []
    for c in CLASES:
        num, v = 0.0, 0.0
        for d in sorted(N_decil):
            if not n_decil[d]:
                continue
            W = N_decil[d] / Ntot
            p = por_clase[d][c] / n_decil[d]
            num += W * p
            s2 = p * (1 - p) * n_decil[d] / (n_decil[d] - 1) if n_decil[d] > 1 else 0.0
            v += W ** 2 * (1 - n_decil[d] / N_decil[d]) * s2 / n_decil[d]
        est[c], var[c] = num, v
    for d in sorted(N_decil):
        if n_decil[d]:
            pesos.extend([N_decil[d] / n_decil[d]] * n_decil[d])
    suma_w = sum(pesos)
    ess = suma_w ** 2 / sum(w * w for w in pesos)
    return {
        'universo': Ntot, 'etiquetas': ntot,
        'N_por_decil': dict(sorted(N_decil.items())),
        'n_por_decil': dict(sorted(n_decil.items())),
        'peso_por_decil': {str(d): round(N_decil[d] / n_decil[d], 4)
                           for d in sorted(N_decil) if n_decil[d]},
        'por_clase_y_decil': {str(d): dict(por_clase[d]) for d in sorted(por_clase)},
        'prevalencia': {c: round(est[c], 4) for c in CLASES},
        'error_estandar': {c: round(math.sqrt(var[c]), 4) for c in CLASES},
        'ic95': {c: [round(max(0.0, est[c] - Z * math.sqrt(var[c])), 4),
                     round(min(1.0, est[c] + Z * math.sqrt(var[c])), 4)] for c in CLASES},
        'intervenciones_estimadas': {c: round(est[c] * Ntot) for c in CLASES},
        'crudo_sin_ponderar': {c: sum(1 for e in etiquetas if e['HD_Clase'] == c)
                               for c in CLASES},
        'tamanio_efectivo_muestra': round(ess, 1),
        'efecto_de_disenio': round(ntot / ess, 3),
        'suma_pesos': round(suma_w, 1),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--etiquetas', default=str(ETIQUETAS))
    ap.add_argument('--salida', default=str(SALIDA))
    args = ap.parse_args()

    etiquetas = json.loads(Path(args.etiquetas).read_text(encoding='utf-8'))['Etiquetas']
    pool = preparar(cargar_turnos())
    res = prevalencia(pool, etiquetas)
    res['representatividad_por_decil'] = representatividad_decil(
        pool, {e['ID_Turno'] for e in etiquetas})

    Ntot, ntot = res['universo'], res['etiquetas']
    crudo = res['crudo_sin_ponderar']
    print(f'universo {Ntot} intervenciones · {ntot} etiquetas oro')
    print('\nPREVALENCIA EN EL UNIVERSO (post-estratificada por decil léxico)')
    for c in CLASES:
        lo, hi = res['ic95'][c]
        p = res['prevalencia'][c]
        print(f'  {c:<8} {p * 100:5.1f}%  IC95 {lo * 100:4.1f}-{hi * 100:4.1f}  '
              f'~{res["intervenciones_estimadas"][c]:4d} intervenciones')
    print(f'  suma {sum(res["prevalencia"].values()):.4f}')

    print('\nEFECTO DE PONDERAR (puntos porcentuales contra el conteo crudo)')
    for c in CLASES:
        print(f'  {c:<8} crudo {crudo[c] / ntot * 100:5.1f}%  ->  ponderado '
              f'{res["prevalencia"][c] * 100:5.1f}%  '
              f'({(res["prevalencia"][c] - crudo[c] / ntot) * 100:+.1f})')

    print(f'\ntamaño efectivo de muestra: {res["tamanio_efectivo_muestra"]} de {ntot} '
          f'(efecto de diseño {res["efecto_de_disenio"]}x)')

    print('\nREPRESENTATIVIDAD DENTRO DEL DECIL (variación total muestra vs universo)')
    tvs = []
    for d, v in res['representatividad_por_decil'].items():
        tvs.append(v['variacion_total'])
        print(f'  decil {d:>2}: {v["variacion_total"]:.3f}  '
              f'(muestra {v["muestra"]:>3} / universo {v["universo"]:>3}, '
              f'{v["celdas_universo"]} celdas año x grupo)')
    print(f'  media {sum(tvs) / len(tvs):.3f} · máxima {max(tvs):.3f}')

    modelo = RELEASE / 'resumen_entrenamiento.json'
    if modelo.exists():
        pred = json.loads(modelo.read_text(encoding='utf-8'))['distribucion_predicha_universo']
        print('\nCONTRASTE INDEPENDIENTE: oro reponderado vs modelo sobre el universo')
        print('  (el modelo fue entrenado con estas 500 y predice las 2.789; el oro')
        print('   reponderado no usa el modelo. Que coincidan es evidencia aparte.)')
        for c in CLASES:
            a = res['intervenciones_estimadas'][c]
            print(f'  {c:<8} oro {a:>5}   modelo {pred[c]:>5}   diferencia {a - pred[c]:>+5}')
        res['contraste_con_el_modelo'] = {
            c: {'oro_reponderado': res['intervenciones_estimadas'][c],
                'modelo_sobre_universo': pred[c],
                'diferencia': res['intervenciones_estimadas'][c] - pred[c]} for c in CLASES}

    Path(args.salida).write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\nescrito en {args.salida}')


if __name__ == '__main__':
    main()
