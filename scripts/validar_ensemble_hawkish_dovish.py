"""Prueba anidada de la mezcla modelo + léxico para el puntaje hawkish/dovish.

La comparación exploratoria medía la mezcla sobre las mismas 500 etiquetas que
eligieron la configuración del release, así que estaba sesgada al alza. Aquí el
peso de la mezcla se elige DENTRO de cada pliegue de entrenamiento, con su propia
validación cruzada interna, y sólo entonces se aplica al pliegue retenido. Lo que
se mide es el procedimiento completo, no un peso fijo escogido a posteriori.

Incluye un control obligatorio: en la semilla 0 el harness debe reproducir el
macro-F1 que publica el release (misma regla de decisión, argmax). Si no lo
reproduce, la comparación no vale y el script lo dice en vez de callarlo.

Se reportan tres reglas de decisión sobre las mismas particiones:
  argmax  -> la clase más probable; es la que usa el release publicado
  umbral  -> hd.clase(score), la banda neutra |score| < 0.25
  mezcla  -> hd.clase(w*score + (1-w)*lex), con w elegido por CV interna
El umbral y la mezcla se comparan entre sí; el argmax es el punto de referencia
publicado y se reporta para mostrar que las dos reglas no coinciden.

Salida:
  data/releases/hawkish_dovish_v1/ensemble_anidado.json
  por pantalla: control de reproducción y comparación por semilla

Uso:
  python3 scripts/validar_ensemble_hawkish_dovish.py [--semillas 5] [--externos 5] [--internos 5]
"""
import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from entrenar_hawkish_dovish import (RELEASE, cargar_turnos, desviacion, entrenar, idf_de,
                                     metricas, pesos_por_clase, pliegues, predecir,
                                     rasgos_texto, seleccionar, vectorizar)  # noqa: E402
from hawkish_dovish import clase, puntuar_lexico  # noqa: E402
from etiquetar_hawkish_dovish import ETIQUETAS  # noqa: E402

SALIDA = RELEASE / 'ensemble_anidado.json'
# w = peso del modelo; w = 1.0 equivale a no mezclar y está a propósito en la rejilla,
# para que la CV interna pueda descartar la mezcla si no le sirve.
PESOS = [1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.6, 0.5]


def cargar(etiquetas=ETIQUETAS):
    """Devuelve cuentas de rasgos, clases oro, puntajes oro y puntajes léxicos."""
    turnos = {t['ID_Turno']: t for t in cargar_turnos()}
    paquete = json.loads(Path(etiquetas).read_text(encoding='utf-8'))
    cuentas, y, oro, lex = [], [], [], []
    for e in paquete['Etiquetas']:
        t = turnos[e['ID_Turno']]
        cuentas.append(rasgos_texto(t['Texto']))
        y.append(e['HD_Clase'])
        oro.append(float(e['HD_Score']))
        lex.append(puntuar_lexico(t['Texto'])['score'])
    return cuentas, y, oro, lex


def _modelo_sobre(cuentas, y, indices, config):
    """Entrena con los índices dados y devuelve (modelo, vocab, idf)."""
    docs = [cuentas[i] for i in indices]
    yy = [y[i] for i in indices]
    vocab = seleccionar(docs, yy, config['max_rasgos'])
    idf = idf_de(docs, vocab)
    X = vectorizar(docs, vocab, idf)
    return (entrenar(X, yy, iteraciones=config['iteraciones'], p=len(vocab),
                     pesos_clase=pesos_por_clase(yy, config['balancear'])), vocab, idf)


def oof_scores(cuentas, y, indices, config, k, semilla):
    """Puntaje del modelo para cada índice, entrenando sólo con `indices`."""
    salida = {}
    for fold in pliegues([y[i] for i in indices], k=k, semilla=semilla):
        test = set(fold)
        tr = [j for pos, j in enumerate(indices) if pos not in test]
        modelo, vocab, idf = _modelo_sobre(cuentas, y, tr, config)
        te_idx = [indices[pos] for pos in fold]
        Xte = vectorizar([cuentas[i] for i in te_idx], vocab, idf)
        for j, i in enumerate(te_idx):
            salida[i] = predecir(modelo, Xte[j])['score']
    return salida


def elegir_peso(cuentas, y, oro, lex, indices, config, k, semilla, pesos=PESOS):
    """CV interna sobre el pliegue de entrenamiento; devuelve (w, tabla macro-F1)."""
    interno = oof_scores(cuentas, y, indices, config, k, semilla)
    reales = [y[i] for i in indices]
    sp = [oro[i] for i in indices]
    tabla = {}
    for w in pesos:
        pp = [w * interno[i] + (1 - w) * lex[i] for i in indices]
        tabla[w] = metricas(reales, [clase(s) for s in pp], sp, pp)['macro_f1']
    return max(tabla, key=lambda w: tabla[w]), tabla


def una_semilla(cuentas, y, oro, lex, config, externos, internos, semilla):
    """Una partición externa completa con las tres reglas de decisión."""
    p_argmax, p_umbral, p_mix = [], [], []
    reales, sp, pp_mod, pp_mix, pesos_elegidos = [], [], [], [], []
    for fold in pliegues(y, k=externos, semilla=semilla):
        test = set(fold)
        tr = [i for i in range(len(y)) if i not in test]
        w, _ = elegir_peso(cuentas, y, oro, lex, tr, config, internos, semilla)
        pesos_elegidos.append(w)
        modelo, vocab, idf = _modelo_sobre(cuentas, y, tr, config)
        Xte = vectorizar([cuentas[i] for i in fold], vocab, idf)
        for j, i in enumerate(fold):
            pred = predecir(modelo, Xte[j])
            s_mix = w * pred['score'] + (1 - w) * lex[i]
            p_argmax.append(pred['clase'])
            p_umbral.append(clase(pred['score']))
            p_mix.append(clase(s_mix))
            reales.append(y[i])
            sp.append(oro[i])
            pp_mod.append(pred['score'])
            pp_mix.append(s_mix)
    m_arg = metricas(reales, p_argmax, sp, pp_mod)
    m_umb = metricas(reales, p_umbral, sp, pp_mod)
    m_mix = metricas(reales, p_mix, sp, pp_mix)
    return {'semilla': semilla,
            'modelo_argmax': m_arg['macro_f1'],
            'modelo_umbral': m_umb['macro_f1'],
            'mezcla': m_mix['macro_f1'],
            'accuracy_argmax': m_arg['accuracy'],
            'accuracy_mezcla': m_mix['accuracy'],
            'mae_argmax': m_arg['mae_puntaje'],
            'mae_mezcla': m_mix['mae_puntaje'],
            'f1_dovish_argmax': m_arg['por_clase']['DOVISH']['f1'],
            'f1_dovish_mezcla': m_mix['por_clase']['DOVISH']['f1'],
            'pesos_elegidos': pesos_elegidos}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--etiquetas', default=str(ETIQUETAS))
    ap.add_argument('--salida', default=str(SALIDA))
    ap.add_argument('--semillas', type=int, default=5, help='particiones externas a promediar')
    ap.add_argument('--externos', type=int, default=5)
    ap.add_argument('--internos', type=int, default=5)
    args = ap.parse_args()

    modelo_pub = json.loads((RELEASE / 'modelo_hawkish_dovish.json').read_text(encoding='utf-8'))
    # el JSON del modelo guarda 'balancear_clases'; el entrenador usa 'balancear'
    c = modelo_pub['config']
    config = {'max_rasgos': c['max_rasgos'], 'iteraciones': c['iteraciones'],
              'balancear': c['balancear_clases']}
    cuentas, y, oro, lex = cargar(args.etiquetas)
    t0 = time.time()
    print(f'{len(y)} etiquetas · config publicada {config["max_rasgos"]}/'
          f'{config["iteraciones"]}/bal={config["balancear"]} · {len(PESOS)} pesos candidatos')
    print('(config del release: max_rasgos/iteraciones/balancear_clases)')

    filas = [una_semilla(cuentas, y, oro, lex, config, args.externos, args.internos, s)
             for s in range(args.semillas)]
    for f in filas:
        print(f'  semilla {f["semilla"]}: argmax {f["modelo_argmax"]:.4f} | '
              f'umbral {f["modelo_umbral"]:.4f} | mezcla {f["mezcla"]:.4f} | '
              f'w {f["pesos_elegidos"]}')

    # Control: la semilla 0 debe reproducir el macro-F1 publicado (regla argmax).
    publicado = json.loads((RELEASE / 'resumen_entrenamiento.json').read_text(encoding='utf-8'))
    cv_pub = publicado['validacion_cruzada']['macro_f1']
    reproduce = filas[0]['modelo_argmax'] == cv_pub
    print(f'\n[control] harness semilla 0 (argmax) = {filas[0]["modelo_argmax"]:.4f} | '
          f'release = {cv_pub:.4f} -> {"REPRODUCE" if reproduce else "NO REPRODUCE"}')
    if not reproduce:
        raise SystemExit('el harness no reproduce el CV publicado: la comparación no es válida')

    dif = [f['mezcla'] - f['modelo_umbral'] for f in filas]
    todos_w = [w for f in filas for w in f['pesos_elegidos']]
    resumen = {
        'config_publicada': config,
        'pesos_candidatos': PESOS,
        'pliegues_externos': args.externos,
        'pliegues_internos': args.internos,
        'semillas': args.semillas,
        'control_reproduce_cv_publicado': reproduce,
        'macro_f1_por_semilla': filas,
        'macro_f1_medio_argmax': round(sum(f['modelo_argmax'] for f in filas) / len(filas), 4),
        'macro_f1_medio_umbral': round(sum(f['modelo_umbral'] for f in filas) / len(filas), 4),
        'macro_f1_medio_mezcla': round(sum(f['mezcla'] for f in filas) / len(filas), 4),
        'diferencia_mezcla_menos_umbral': round(sum(dif) / len(dif), 4),
        'desviacion_diferencia': round(desviacion(dif), 4),
        'semillas_ganando_la_mezcla': sum(1 for d in dif if d > 0),
        'pesos_elegidos_por_la_cv_interna': dict(Counter(todos_w)),
        'veredicto': ('la mezcla no mejora al modelo; no se publica'
                      if sum(dif) / len(dif) <= 0 else
                      'la mezcla mejora al modelo bajo validación anidada'),
        'segundos': round(time.time() - t0, 1),
    }
    print(f'\nmacro-F1 medio argmax (regla publicada): {resumen["macro_f1_medio_argmax"]:.4f}')
    print(f'macro-F1 medio umbral : {resumen["macro_f1_medio_umbral"]:.4f}')
    print(f'macro-F1 medio mezcla : {resumen["macro_f1_medio_mezcla"]:.4f}')
    print(f'diferencia mezcla - umbral: {resumen["diferencia_mezcla_menos_umbral"]:+.4f} '
          f'sd {resumen["desviacion_diferencia"]:.4f}')
    print(f'gana la mezcla: {resumen["semillas_ganando_la_mezcla"]}/{args.semillas} semillas')
    print(f'pesos elegidos por la CV interna: {resumen["pesos_elegidos_por_la_cv_interna"]}')
    print(f'veredicto: {resumen["veredicto"]}')

    Path(args.salida).write_text(json.dumps(resumen, ensure_ascii=False, indent=2),
                                 encoding='utf-8')
    print(f'\nescrito en {args.salida} ({resumen["segundos"]}s)')


if __name__ == '__main__':
    main()
