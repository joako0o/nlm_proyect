"""Diagnóstico de fallos del clasificador hawkish/dovish sobre predicciones fuera de pliegue.

El release publica el puntaje del modelo entrenado con las 500 etiquetas, así que
comparar ese puntaje con el oro mide autoajuste, no calidad. Este script rehace la
validación cruzada de la configuración publicada y guarda la predicción que el modelo
habría hecho sin ver cada etiqueta, que es la única comparación honesta.

Salida:
  data/releases/hawkish_dovish_v1/fallos_fuera_de_pliegue.csv   una fila por etiqueta oro
  por pantalla: reproducción del CV publicado, matriz de fallos y precisión por |score|

Uso:
  python scripts/diagnosticar_fallos_hawkish_dovish.py [--pliegues 5] [--semilla 0]
"""
import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from entrenar_hawkish_dovish import (RELEASE, cargar_turnos, idf_de, entrenar, metricas,
                                     pesos_por_clase, pliegues, predecir, rasgos_texto,
                                     seleccionar, vectorizar)  # noqa: E402
from hawkish_dovish import grupo_actor, puntuar_lexico  # noqa: E402
from etiquetar_hawkish_dovish import ETIQUETAS  # noqa: E402

SALIDA = RELEASE / 'fallos_fuera_de_pliegue.csv'
CUBOS = [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.01)]


def fuera_de_pliegue(paq, turnos, config, k=5, semilla=0):
    """Rehace la CV de la configuración publicada y devuelve las predicciones oof."""
    docs = [rasgos_texto(turnos[e['ID_Turno']]['Texto']) for e in paq]
    y = [e['HD_Clase'] for e in paq]
    oro = [float(e['HD_Score']) for e in paq]
    lex = [puntuar_lexico(turnos[e['ID_Turno']]['Texto'])['score'] for e in paq]
    oof = [None] * len(y)
    for fold in pliegues(y, k=k, semilla=semilla):
        test = set(fold)
        tr = [i for i in range(len(y)) if i not in test]
        vocab = seleccionar([docs[i] for i in tr], [y[i] for i in tr], config['max_rasgos'])
        idf = idf_de([docs[i] for i in tr], vocab)
        Xtr = vectorizar([docs[i] for i in tr], vocab, idf)
        mod = entrenar(Xtr, [y[i] for i in tr], iteraciones=config['iteraciones'],
                       p=len(vocab),
                       pesos_clase=pesos_por_clase([y[i] for i in tr],
                                                   config['balancear_clases']))
        Xte = vectorizar([docs[i] for i in fold], vocab, idf)
        for j, i in enumerate(fold):
            oof[i] = predecir(mod, Xte[j])
    return docs, y, oro, lex, oof


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--etiquetas', default=str(ETIQUETAS))
    ap.add_argument('--modelo', default=str(RELEASE / 'modelo_hawkish_dovish.json'))
    ap.add_argument('--salida', default=str(SALIDA))
    ap.add_argument('--pliegues', type=int, default=5)
    ap.add_argument('--semilla', type=int, default=0,
                    help='semilla de partición; la publicada es 0')
    args = ap.parse_args()

    config = json.loads(Path(args.modelo).read_text(encoding='utf-8'))['config']
    paq = json.loads(Path(args.etiquetas).read_text(encoding='utf-8'))['Etiquetas']
    turnos = {t['ID_Turno']: t for t in cargar_turnos()}
    faltan = [e['ID_Turno'] for e in paq if e['ID_Turno'] not in turnos]
    if faltan:
        raise SystemExit(f'{len(faltan)} etiquetas sin texto en el consolidado: {faltan[:3]}')

    _, y, oro, lex, oof = fuera_de_pliegue(paq, turnos, config, args.pliegues, args.semilla)
    m = metricas(y, [o['clase'] for o in oof], oro, [o['score'] for o in oof])
    print(f"configuración analizada: {config['max_rasgos']} rasgos / {config['iteraciones']} "
          f"iteraciones / balancear={config['balancear_clases']}")
    print(f"CV fuera de pliegue (semilla {args.semilla}): macro_f1={m['macro_f1']} "
          f"acc={m['accuracy']} mae={m['mae_puntaje']}")
    print('  (debe coincidir con validacion_cruzada del resumen_entrenamiento.json)')

    malos = [(i, o) for i, o in enumerate(oof) if o['clase'] != y[i]]
    print(f"\nerrores: {len(malos)} de {len(y)}")
    for par, n in Counter((y[i], o['clase']) for i, o in malos).most_common():
        print(f'   {par[0]:8s} -> {par[1]:8s} {n:3d}')
    inv = sum(1 for i, o in malos if {y[i], o['clase']} == {'HAWKISH', 'DOVISH'})
    print(f'inversiones de signo (hawkish<->dovish): {inv}')

    print('\nprecisión por cubo de |score| (fuera de pliegue):')
    print(f"{'cubo':>14} {'n':>4} {'acierta':>8} {'precisión':>10} {'oro mayoritario':>18}")
    for lo, hi in CUBOS:
        sel = [(i, o) for i, o in enumerate(oof) if lo <= abs(o['score']) < hi]
        if not sel:
            continue
        ok = sum(1 for i, o in sel if o['clase'] == y[i])
        may = Counter(y[i] for i, _ in sel).most_common(1)[0]
        print(f"  [{lo:.2f},{hi:.2f}) {len(sel):>4} {ok:>8} {ok / len(sel):>10.3f} "
              f"{may[0]:>10} ({may[1]})")

    print('\nprecisión por clase predicha:')
    for c in ('HAWKISH', 'NEUTRAL', 'DOVISH'):
        sel = [(i, o) for i, o in enumerate(oof) if o['clase'] == c]
        if not sel:
            continue
        ok = sum(1 for i, o in sel if y[i] == c)
        print(f"  predice {c:8s} n={len(sel):>3}  acierta {ok:>3}  precisión {ok / len(sel):.3f}")

    no_neutras = [i for i in range(len(y)) if y[i] != 'NEUTRAL']
    orden = sorted(range(len(y)), key=lambda i: -abs(oof[i]['score']))
    print('\nutilidad para barrido: leer los N turnos de |score| más alto')
    for n in (50, 100, 150, 200):
        top = orden[:n]
        cap = sum(1 for i in top if y[i] != 'NEUTRAL')
        print(f"  leyendo {n:>3} -> captura {cap:>3} de {len(no_neutras)} no neutras "
              f"({cap / len(no_neutras):.1%}), precisión {cap / n:.3f}")
    print(f"  tasa base (leer al azar): {len(no_neutras) / len(y):.1%}")

    with open(args.salida, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=[
            'ID_Turno', 'Fecha', 'Actor_Final', 'Rol_Final', 'Grupo_Actor',
            'HD_Score_Oro', 'HD_Clase_Oro', 'Evidencia_Oro', 'Lex_Score',
            'Score_Fuera_De_Pliegue', 'Pred_Fuera_De_Pliegue', 'Acierta'])
        w.writeheader()
        for i, e in enumerate(paq):
            t = turnos[e['ID_Turno']]
            w.writerow({
                'ID_Turno': e['ID_Turno'], 'Fecha': t['Fecha'],
                'Actor_Final': t['Actor_Final'], 'Rol_Final': t['Rol_Final'],
                'Grupo_Actor': grupo_actor(t['Rol_Final']),
                'HD_Score_Oro': e['HD_Score'], 'HD_Clase_Oro': e['HD_Clase'],
                'Evidencia_Oro': e['Evidencia'], 'Lex_Score': round(lex[i], 4),
                'Score_Fuera_De_Pliegue': round(oof[i]['score'], 4),
                'Pred_Fuera_De_Pliegue': oof[i]['clase'],
                'Acierta': 'SI' if oof[i]['clase'] == y[i] else 'NO'})
    print(f'\nescrito en {args.salida}')


if __name__ == '__main__':
    main()
