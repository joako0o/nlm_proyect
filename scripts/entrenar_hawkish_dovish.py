"""Entrena un clasificador hawkish/dovish sobre las etiquetas oro y puntúa el resto.

Sin dependencias nuevas: tokenización propia, selección supervisada de rasgos y
regresión logística multinomial (softmax) en Python puro. La selección de rasgos
se hace dentro de cada pliegue para que la validación cruzada no se filtre.

Salida en data/releases/hawkish_dovish_v1/:
  puntajes_hawkish_dovish.csv   puntaje del modelo para cada turno del corpus
  modelo_hawkish_dovish.json    vocabulario y pesos (reproduce el puntaje sin reentrenar)
  resumen_entrenamiento.json    métricas, configuración y hashes
"""
import argparse
import csv
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hawkish_dovish import (CURATION, REPO, cargar_turnos, clase, grupo_actor,
                            normalizar, puntuar_lexico)  # noqa: E402
from etiquetar_hawkish_dovish import ETIQUETAS, MUESTRA, cargar_muestra

CLASES = ['HAWKISH', 'NEUTRAL', 'DOVISH']
RELEASE = REPO / 'data/releases/hawkish_dovish_v1'
# Semillas de particion para la CV repetida que desempata la configuracion.
SEMILLAS_CV = tuple(range(10))

STOPWORDS = {
    'que', 'por', 'para', 'con', 'una', 'uno', 'los', 'las', 'del', 'los', 'sus', 'al',
    'del', 'los', 'como', 'esta', 'este', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas',
    'fue', 'ser', 'son', 'era', 'han', 'hay', 'más', 'mas', 'pero', 'sin', 'sobre',
    'entre', 'cuando', 'muy', 'también', 'tambien', 'se', 'su', 'lo', 'le', 'les', 'nos',
    'por', 'ya', 'si', 'no', 'de', 'la', 'el', 'en', 'un', 'es', 'ha', 'he', 'hace',
    'desde', 'hasta', 'donde', 'cual', 'cuál', 'ser', 'está', 'esta', 'están', 'estan',
    'señor', 'senor', 'senora', 'señora', 'agrega', 'senal', 'señala', 'indica', 'dice',
    'respecto', 'materia', 'caso', 'vez', 'forma', 'parte', 'mayor', 'menor', 'nivel',
    'mes', 'meses', 'ano', 'año', 'anos', 'años', 'hacia', 'traves', 'través', 'ello',
    'ella', 'ellos', 'ellas', 'esto', 'eso', 'aquello', 'todo', 'toda', 'todos', 'todas',
    'otro', 'otra', 'otros', 'otras', 'mismo', 'misma', 'cada', 'dos', 'tres', 'puede',
    'debe', 'tiene', 'tener', 'hacer', 'hace', 'pues', 'asi', 'así', 'solo', 'sólo',
}


def tokens(texto):
    crudo = normalizar(texto)
    salida = []
    for tok in crudo.split():
        tok = ''.join(c for c in tok if c.isalnum())
        if len(tok) >= 3 and tok not in STOPWORDS and not tok.isdigit():
            salida.append(tok)
    return salida


def rasgos_texto(texto):
    """Unigramas y bigramas con frecuencia bruta."""
    toks = tokens(texto)
    cuenta = Counter(toks)
    for a, b in zip(toks, toks[1:]):
        cuenta[a + ' ' + b] += 1
    return cuenta


def seleccionar(X, y, max_rasgos, min_df=2):
    """Rasgos con df>=min_df y mayor dispersión de peso medio entre clases."""
    n = len(X)
    df, peso_total = Counter(), Counter()
    por_clase = defaultdict(Counter)
    cuenta_clase = Counter(y)
    for doc, etiqueta in zip(X, y):
        for k, v in doc.items():
            df[k] += 1
            peso_total[k] += v
            por_clase[etiqueta][k] += v
    puntaje = {}
    for k in df:
        if df[k] < min_df or df[k] > 0.9 * n:
            continue
        media = peso_total[k] / n
        var = sum((por_clase[c][k] / cuenta_clase[c] - media) ** 2
                  for c in CLASES if cuenta_clase[c])
        puntaje[k] = var
    orden = sorted(puntaje, key=lambda k: (-puntaje[k], k))[:max_rasgos]
    return orden


def vectorizar(docs, vocab, idf):
    indice = {t: i for i, t in enumerate(vocab)}
    X = []
    for cuenta in docs:
        v = {}
        for t, tf in cuenta.items():
            i = indice.get(t)
            if i is None:
                continue
            w = (1 + math.log(tf)) * idf[i]
            v[i] = w
        norma = math.sqrt(sum(w * w for w in v.values())) or 1.0
        X.append({i: w / norma for i, w in v.items()})
    return X


def idf_de(docs, vocab):
    n = len(docs)
    df = Counter()
    for cuenta in docs:
        for t in cuenta:
            df[t] += 1
    return [math.log((1 + n) / (1 + df[t])) + 1.0 for t in vocab]


def pesos_por_clase(y, balancear):
    # Peso inverso a la frecuencia: sin balancear, la clase mayoritaria domina el macro-F1.
    if not balancear:
        return None
    cuenta = Counter(y)
    n, K = len(y), len(CLASES)
    return {c: n / (K * cuenta[c]) for c in CLASES if cuenta[c]}


def entrenar(X, y, iteraciones=200, lr=0.5, l2=1e-3, p=0, pesos_clase=None):
    """Regresión logística multinomial por descenso de gradiente estocástico."""
    K = len(CLASES)
    p = p or (max((max(d) for d in X if d), default=-1) + 1)
    W = [[0.0] * p for _ in range(K)]
    b = [0.0] * K
    orden = list(range(len(X)))
    rng = random.Random(0)
    etiquetas = [CLASES.index(e) for e in y]
    w_doc = [pesos_clase[e] if pesos_clase else 1.0 for e in y]
    for _ in range(iteraciones):
        rng.shuffle(orden)
        for idx in orden:
            doc, real = X[idx], etiquetas[idx]
            scores = [sum(Wk[i] * v for i, v in doc.items()) + b[k]
                      for k, Wk in enumerate(W)]
            m = max(scores)
            exps = [math.exp(s - m) for s in scores]
            z = sum(exps)
            w = w_doc[idx]
            for k in range(K):
                g = w * (exps[k] / z - (1.0 if k == real else 0.0))
                if not g:
                    continue
                Wk = W[k]
                paso = lr * g
                for i, v in doc.items():
                    Wk[i] -= paso * v + lr * l2 * Wk[i]
                b[k] -= paso
    return {'W': W, 'b': b, 'p': p}


def predecir(modelo, doc):
    b = modelo['b']
    scores = [sum(Wk[i] * v for i, v in doc.items()) + b[k]
              for k, Wk in enumerate(modelo['W'])]
    m = max(scores)
    exps = [math.exp(s - m) for s in scores]
    z = sum(exps)
    probs = [e / z for e in exps]
    k = probs.index(max(probs))
    ordenadas = sorted(probs, reverse=True)
    return {
        'probs': probs,
        'clase': CLASES[k],
        'margen': round(ordenadas[0] - ordenadas[1], 4),
        'score': round(probs[0] * 1.0 + probs[1] * 0.0 + probs[2] * -1.0, 4),
    }


def metricas(reales, predichas, scores_reales=None, scores_predichos=None):
    clases = CLASES
    matriz = {a: {b: 0 for b in clases} for a in clases}
    for r, p in zip(reales, predichas):
        matriz[r][p] += 1
    f1s, detalle = [], {}
    for c in clases:
        tp = matriz[c][c]
        fp = sum(matriz[o][c] for o in clases) - tp
        fn = sum(matriz[c].values()) - tp
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        f1s.append(f1)
        detalle[c] = {'precision': round(prec, 3), 'recall': round(rec, 3), 'f1': round(f1, 3),
                      'soporte': tp + fn}
    out = {
        'accuracy': round(sum(1 for r, p in zip(reales, predichas) if r == p) / len(reales), 3),
        'macro_f1': round(sum(f1s) / len(f1s), 3),
        'por_clase': detalle,
        'matriz_real_x_predicha': matriz,
    }
    if scores_reales is not None:
        out['mae_puntaje'] = round(
            sum(abs(a - b) for a, b in zip(scores_reales, scores_predichos)) / len(scores_reales), 3)
    return out


def pliegues(y, k=5, semilla=0):
    """Partición estratificada por clase."""
    por_clase = defaultdict(list)
    for i, e in enumerate(y):
        por_clase[e].append(i)
    rng = random.Random(semilla)
    grupos = []
    for c in CLASES:
        idx = por_clase[c][:]
        rng.shuffle(idx)
        for j, i in enumerate(idx):
            grupos.append((j % k, i))
    salida = [[] for _ in range(k)]
    for f, i in grupos:
        salida[f].append(i)
    return salida


def desviacion(valores):
    """Desviación estándar muestral (n-1); 0.0 si hay un solo valor."""
    n = len(valores)
    if n < 2:
        return 0.0
    media = sum(valores) / n
    return math.sqrt(sum((v - media) ** 2 for v in valores) / (n - 1))


def pliegues_por_sesion(sesiones, k=5, semilla=0):
    """Partición por sesión: todos los turnos de una misma RPM caen en el mismo pliegue.

    `pliegues()` baraja por turno y reparte el 90,7% de las 130 sesiones del oro en
    más de un pliegue. Los turnos de una misma reunión comparten día, discusión y
    vocabulario, así que esa CV filtra información y es optimista. Ver
    `auditoria_metodologica.json` -> `fuga_por_sesion`.
    """
    ses = sorted(set(sesiones))
    rng = random.Random(semilla)
    rng.shuffle(ses)
    asigna = {s: i % k for i, s in enumerate(ses)}
    return [[i for i, s in enumerate(sesiones) if asigna[s] == f] for f in range(k)]


def validacion_cruzada(docs_cuenta, y, scores_oro, lex_scores, max_rasgos, iteraciones, k=5,
                       balancear=False, semilla=0, particion=None):
    resultados, oof = [], [None] * len(y)
    for fold in (particion if particion is not None
                 else pliegues(y, k=k, semilla=semilla)):
        test = set(fold)
        tr = [i for i in range(len(y)) if i not in test]
        if len({y[i] for i in fold}) == 0:
            continue
        tr_docs = [docs_cuenta[i] for i in tr]
        vocab = seleccionar(tr_docs, [y[i] for i in tr], max_rasgos)
        idf = idf_de(tr_docs, vocab)
        Xtr = vectorizar(tr_docs, vocab, idf)
        modelo = entrenar(Xtr, [y[i] for i in tr], iteraciones=iteraciones, p=len(vocab),
                          pesos_clase=pesos_por_clase([y[i] for i in tr], balancear))
        Xte = vectorizar([docs_cuenta[i] for i in fold], vocab, idf)
        for j, i in enumerate(fold):
            pred = predecir(modelo, Xte[j])
            oof[i] = pred
    idx = [i for i in range(len(y)) if oof[i] is not None]
    reales = [y[i] for i in idx]
    predichas = [oof[i]['clase'] for i in idx]
    sp = [float(scores_oro[i]) for i in idx]
    pp = [oof[i]['score'] for i in idx]
    m = metricas(reales, predichas, sp, pp)

    mayoria = Counter(reales).most_common(1)[0][0]
    m['baseline_mayoria'] = metricas(reales, [mayoria] * len(reales), sp, [0.0] * len(pp))
    lx = [float(lex_scores[i]) for i in idx]
    m['baseline_lexico'] = metricas(reales, [clase(s) for s in lx], sp, lx)
    m['predicciones_fuera_de_pliegue'] = len(idx)
    return m


def curva(cfg, cuentas, y, scores_oro, lex_scores, puntos, pliegues):
    """Curva de aprendizaje estratificada para una configuración dada."""
    por_clase = {c: [i for i, e in enumerate(y) if e == c] for c in CLASES}
    rng = random.Random(0)
    for c in por_clase:
        rng.shuffle(por_clase[c])
    salida = []
    for n in puntos:
        if n >= len(y):
            continue
        sub = []
        for c in CLASES:
            cuota = max(1, round(n * len(por_clase[c]) / len(y)))
            sub.extend(por_clase[c][:cuota])
        sub = sorted(sub[:n])
        m = validacion_cruzada([cuentas[i] for i in sub], [y[i] for i in sub],
                               [scores_oro[i] for i in sub], [lex_scores[i] for i in sub],
                               cfg['max_rasgos'], cfg['iteraciones'], k=pliegues,
                               balancear=cfg['balancear_clases'])
        salida.append({'etiquetas': len(sub), 'macro_f1': m['macro_f1'],
                       'accuracy': m['accuracy'], 'mae_puntaje': m.get('mae_puntaje'),
                       'macro_f1_lexico': m['baseline_lexico']['macro_f1']})
    return salida


def diagnostico(cuentas, y, scores_oro, lex_scores, rejilla, curva_puntos, pliegues,
                semillas_cv=SEMILLAS_CV):
    """Rejilla de capacidad, curva de aprendizaje y CV repetida.

    Regla de selección declarada: entre las tres mejores configuraciones de la rejilla
    por macro-F1 en el conjunto completo, se descarta la que no supere al léxico en el
    último punto de la curva y, entre las restantes, se toma la de mayor macro-F1 medio
    en **CV repetida sobre el conjunto completo** (varias semillas de partición).

    El desempate se hace sobre el conjunto completo porque ése es el régimen en que se
    despliega el modelo. Una versión anterior desempataba con el macro-F1 medio de la
    curva de aprendizaje, que mide con subconjuntos de 15-80% del oro: con 500
    etiquetas eso elegía 300 rasgos sobre 600 aunque 600 ganara en 10 de 10 semillas
    de partición (+0,037 de macro-F1). La curva se conserva como diagnóstico del
    cruce con el léxico, no como criterio de selección.
    """
    out = {'rejilla': [], 'curvas': {}, 'pliegues': pliegues, 'semillas_cv': list(semillas_cv)}
    for max_rasgos, iteraciones, balancear in rejilla:
        m = validacion_cruzada(cuentas, y, scores_oro, lex_scores,
                               max_rasgos, iteraciones, k=pliegues, balancear=balancear)
        out['rejilla'].append({'max_rasgos': max_rasgos, 'iteraciones': iteraciones,
                               'balancear_clases': balancear,
                               'macro_f1': m['macro_f1'], 'accuracy': m['accuracy'],
                               'mae_puntaje': m.get('mae_puntaje')})
    orden = sorted(out['rejilla'], key=lambda r: (-r['macro_f1'], r['max_rasgos']))
    candidatas = []
    for cfg in orden[:3]:
        clave = f"{cfg['max_rasgos']}/{cfg['iteraciones']}/bal={cfg['balancear_clases']}"
        out['curvas'][clave] = curva(cfg, cuentas, y, scores_oro, lex_scores,
                                     curva_puntos, pliegues)
        ultima = out['curvas'][clave][-1] if out['curvas'][clave] else None
        supera = bool(ultima and ultima['macro_f1'] > ultima['macro_f1_lexico'])
        candidatas.append((cfg, clave, supera))
        out['curvas'][clave + '_supera_lexico_en_curva'] = supera
    elegidas = [c for c in candidatas if c[2]]
    out['cv_repetida'] = {}
    if elegidas:
        # Desempate sobre el conjunto completo: varias semillas de particion.
        for cfg, clave_c, _ in elegidas:
            corridas = [validacion_cruzada(cuentas, y, scores_oro, lex_scores,
                                           cfg['max_rasgos'], cfg['iteraciones'], k=pliegues,
                                           balancear=cfg['balancear_clases'], semilla=sem)
                        for sem in semillas_cv]
            f1s = [m['macro_f1'] for m in corridas]
            # El baseline lexico no depende de la particion: predice igual en cada semilla.
            lex = corridas[0]['baseline_lexico']['macro_f1']
            out['cv_repetida'][clave_c] = {
                'macro_f1_por_semilla': [round(v, 4) for v in f1s],
                'macro_f1_medio': round(sum(f1s) / len(f1s), 4),
                'macro_f1_desviacion': round(desviacion(f1s), 4),
                'macro_f1_lexico': lex,
                'semillas_ganando_al_lexico': sum(1 for v in f1s if v > lex),
            }
        elegidas.sort(key=lambda c: -out['cv_repetida'][c[1]]['macro_f1_medio'])
        mejor, clave, _ = elegidas[0]
    else:
        # ninguna superó al léxico en el último punto: se publica la mejor del conjunto
        # completo y se deja constancia de que no pasó el filtro.
        mejor = orden[0]
        clave = f"{mejor['max_rasgos']}/{mejor['iteraciones']}/bal={mejor['balancear_clases']}"
        if clave not in out['curvas']:
            out['curvas'][clave] = curva(mejor, cuentas, y, scores_oro, lex_scores,
                                         curva_puntos, pliegues)
    out['mejor_configuracion'] = mejor
    out['clave_mejor_configuracion'] = clave
    out['macro_f1_medio_en_curva'] = {c[1]: round(sum(p['macro_f1'] for p in out['curvas'][c[1]])
                                                  / len(out['curvas'][c[1]]), 3)
                                      for c in candidatas}
    out['curva_aprendizaje'] = out['curvas'][clave]
    out['descartadas_por_curva'] = [c[1] for c in candidatas if not c[2]]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--muestra', default=str(MUESTRA))
    ap.add_argument('--etiquetas', default=str(ETIQUETAS))
    ap.add_argument('--salida', default=str(RELEASE))
    ap.add_argument('--max-rasgos', type=int, default=None,
                    help='por omisión lo decide la regla de --diagnostico; sin diagnóstico usa 150')
    ap.add_argument('--iteraciones', type=int, default=None,
                    help='por omisión lo decide la regla de --diagnostico; sin diagnóstico usa 30')
    ap.add_argument('--balancear-clases', action=argparse.BooleanOptionalAction, default=None,
                    help='pondera cada clase por el inverso de su frecuencia; por omisión lo '
                         'decide la regla de --diagnostico (sin diagnóstico: activo)')
    ap.add_argument('--pliegues', type=int, default=5)
    ap.add_argument('--diagnostico', action='store_true',
                    help='corre la rejilla de capacidad y la curva de aprendizaje')
    args = ap.parse_args()

    turnos = cargar_turnos()
    texto_por_id = {t['ID_Turno']: t for t in turnos}
    paquete = json.loads(Path(args.etiquetas).read_text(encoding='utf-8'))
    muestra_filas, _ = cargar_muestra(args.muestra)
    if paquete['Etiquetas'] and not any(r['HD_Clase_Oro'] for r in muestra_filas):
        raise SystemExit('la muestra no lleva etiquetas fusionadas: ejecute primero '
                         'scripts/etiquetar_hawkish_dovish.py (orden: muestra -> etiquetar -> entrenar)')
    oro, faltantes = [], []
    for e in paquete['Etiquetas']:
        t = texto_por_id.get(e['ID_Turno'])
        if not t:
            faltantes.append(e['ID_Turno'])
            continue
        lex = puntuar_lexico(t['Texto'])
        oro.append({'ID_Turno': e['ID_Turno'], 'Texto': t['Texto'],
                    'HD_Clase_Oro': e['HD_Clase'], 'HD_Score_Oro': float(e['HD_Score']),
                    'Lex_Score': lex['score'], 'Palabras': t['Palabras'],
                    'Naturaleza_Turno': t['Naturaleza_Turno'], 'Rol_Final': t['Rol_Final'],
                    'Fecha': t['Fecha']})
    if faltantes:
        raise SystemExit(f'{len(faltantes)} etiquetas sin texto en el consolidado: {faltantes[:3]}')
    if len(oro) < 30:
        raise SystemExit(f'sólo {len(oro)} etiquetas oro; se requieren al menos 30 para entrenar')

    cuentas = [rasgos_texto(r['Texto']) for r in oro]
    y = [r['HD_Clase_Oro'] for r in oro]
    scores_oro = [str(r['HD_Score_Oro']) for r in oro]
    lex_scores = [str(r['Lex_Score']) for r in oro]

    # La rejilla corre antes de entrenar: lo que se publica es la configuración que elige
    # la regla declarada en diagnostico(), salvo que el usuario la fuerce por CLI.
    diag = None
    if args.diagnostico:
        rejilla = [(150, 30, False), (150, 30, True), (150, 120, False), (150, 120, True),
                   (300, 30, False), (300, 30, True), (300, 120, False),
                   (600, 30, False), (600, 30, True), (900, 60, False), (900, 200, False)]
        puntos_curva = sorted({max(20, min(len(y) - 1, round(len(y) * f)))
                               for f in (0.15, 0.25, 0.35, 0.50, 0.65, 0.80)})
        diag = diagnostico(cuentas, y, scores_oro, lex_scores, rejilla,
                           puntos_curva, args.pliegues)

    por_omision = {'max_rasgos': 150, 'iteraciones': 30, 'balancear_clases': True}
    elegida = diag['mejor_configuracion'] if diag else None
    valores_cli = {'max_rasgos': args.max_rasgos,
                   'iteraciones': args.iteraciones,
                   'balancear_clases': args.balancear_clases}
    elegidos, origen = {}, {}
    for clave, por_defecto in por_omision.items():
        if valores_cli[clave] is not None:
            elegidos[clave], origen[clave] = valores_cli[clave], 'cli'
        elif elegida is not None:
            elegidos[clave], origen[clave] = elegida[clave], 'regla_diagnostico'
        else:
            elegidos[clave], origen[clave] = por_defecto, 'omision'
    max_rasgos = elegidos['max_rasgos']
    iteraciones = elegidos['iteraciones']
    balancear = elegidos['balancear_clases']
    print(f'configuracion publicada: {max_rasgos} rasgos / {iteraciones} iteraciones / '
          f'balancear={balancear}  (origen: {", ".join(f"{k}={v}" for k, v in origen.items())})')

    cv = validacion_cruzada(cuentas, y, scores_oro, lex_scores,
                            max_rasgos, iteraciones, k=args.pliegues,
                            balancear=balancear)
    # La CV publicada baraja por turno y filtra entre sesiones (90,7% de las sesiones
    # queda repartida en varios pliegues). La agrupada por sesión es la cifra limpia:
    # se publica junto a la otra, no en su lugar, porque el release v1 está hasheado.
    sesiones = [r['ID_Turno'].split(':')[0] for r in oro]
    cv_sesion = validacion_cruzada(cuentas, y, scores_oro, lex_scores,
                                   max_rasgos, iteraciones, k=args.pliegues,
                                   balancear=balancear,
                                   particion=pliegues_por_sesion(sesiones, args.pliegues))

    vocab = seleccionar(cuentas, y, max_rasgos)
    idf = idf_de(cuentas, vocab)
    X = vectorizar(cuentas, vocab, idf)
    modelo = entrenar(X, y, iteraciones=iteraciones, p=len(vocab),
                      pesos_clase=pesos_por_clase(y, balancear))
    # autoajuste sobre las mismas 63 etiquetas: se informa, no se usa como métrica
    auto = metricas(y, [predecir(modelo, d)['clase'] for d in X],
                    [float(s) for s in scores_oro], [predecir(modelo, d)['score'] for d in X])

    for t in turnos:
        t['Lex'] = puntuar_lexico(t['Texto'])
    indice = {tt: i for i, tt in enumerate(vocab)}
    filas = []
    for t in turnos:
        doc = rasgos_texto(t['Texto'])
        v = {}
        for tt, tf in doc.items():
            i = indice.get(tt)
            if i is not None:
                v[i] = (1 + math.log(tf)) * idf[i]
        norma = math.sqrt(sum(w * w for w in v.values())) or 1.0
        pred = predecir(modelo, {i: w / norma for i, w in v.items()})
        filas.append({
            'ID_Turno': t['ID_Turno'], 'Fecha': t['Fecha'], 'Anio': t['Anio'],
            'Actor_Final': t['Actor_Final'], 'Rol_Final': t['Rol_Final'],
            'Grupo_Actor': None, 'Naturaleza_Turno': t['Naturaleza_Turno'],
            'Palabras': t['Palabras'], 'Lex_Score': t['Lex']['score'],
            'HD_Score_Modelo': pred['score'], 'HD_Clase_Modelo': pred['clase'],
            'Margen': pred['margen'],
            # La unica medida de confianza calibrada (ECE 0,041, precision
            # monotona). Margen y |score| no lo son: ver calibracion_confianza.json
            'HD_Confianza_Modelo': round(max(pred['probs']), 4),
        })
    oro_por_turno = {r['ID_Turno']: r for r in oro}
    muestra_ids = {r['ID_Turno'] for r in muestra_filas}
    for f, t in zip(filas, turnos):
        f['Grupo_Actor'] = grupo_actor(t['Rol_Final'])
        f['En_Universo_Entrenado'] = 'true' if (t['Naturaleza_Turno'] == 'INTERVENCION'
                                                and t['Palabras'] >= 150) else 'false'
        m = oro_por_turno.get(t['ID_Turno'])
        f['HD_Score_Oro'] = m['HD_Score_Oro'] if m else ''
        f['HD_Clase_Oro'] = m['HD_Clase_Oro'] if m else ''
        f['En_Muestra_500'] = 'true' if t['ID_Turno'] in muestra_ids else 'false'

    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)
    if diag is not None:
        diag['baseline_lexico_macro_f1'] = cv['baseline_lexico']['macro_f1']
        diag['baseline_mayoria_macro_f1'] = cv['baseline_mayoria']['macro_f1']
        diag['configuracion_publicada'] = {'max_rasgos': max_rasgos,
                                           'iteraciones': iteraciones,
                                           'balancear_clases': balancear,
                                           'origen': origen}
        (salida / 'diagnostico_capacidad.json').write_text(
            json.dumps(diag, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'rejilla': diag['rejilla'],
                          'curva_aprendizaje': diag['curva_aprendizaje'],
                          'macro_f1_medio_en_curva': diag['macro_f1_medio_en_curva'],
                          'mejor_configuracion': diag['mejor_configuracion'],
                          'descartadas_por_curva': diag['descartadas_por_curva'],
                          'configuracion_publicada': diag['configuracion_publicada']},
                         ensure_ascii=False, indent=2))
    campos = ['ID_Turno', 'Fecha', 'Anio', 'Actor_Final', 'Rol_Final', 'Grupo_Actor',
              'Naturaleza_Turno', 'Palabras', 'Lex_Score', 'HD_Score_Modelo',
              'HD_Clase_Modelo', 'Margen', 'HD_Confianza_Modelo',
              'En_Universo_Entrenado', 'En_Muestra_500',
              'HD_Score_Oro', 'HD_Clase_Oro']
    with open(salida / 'puntajes_hawkish_dovish.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)

    modelo_json = {
        'version': 'hawkish_dovish_v1',
        'clases': CLASES, 'vocabulario': vocab, 'idf': idf,
        'pesos': modelo['W'], 'sesgo': modelo['b'],
        'config': {'max_rasgos': max_rasgos, 'iteraciones': iteraciones,
                   'stopwords': len(STOPWORDS), 'ngramas': 'unigrama+bigrama',
                   'balancear_clases': balancear, 'origen_configuracion': origen},
        'etiquetas_oro': len(oro),
    }
    (salida / 'modelo_hawkish_dovish.json').write_text(
        json.dumps(modelo_json, ensure_ascii=False), encoding='utf-8')

    resumen = {
        'etiquetas_oro': len(oro),
        'distribucion_oro': dict(Counter(y)),
        'configuracion_publicada': {'max_rasgos': max_rasgos, 'iteraciones': iteraciones,
                                    'balancear_clases': balancear, 'origen': origen},
        'validacion_cruzada': {k: v for k, v in cv.items()},
        'validacion_cruzada_por_sesion': {k: v for k, v in cv_sesion.items()},
        'autoajuste_sobre_oro': auto,
        'turnos_puntuados': len(filas),
        'turnos_en_universo_entrenado': sum(1 for f in filas if f['En_Universo_Entrenado'] == 'true'),
        'turnos_en_muestra_500': sum(1 for f in filas if f['En_Muestra_500'] == 'true'),
        'etiquetas_usadas': len(oro),
        'etiquetas_en_muestra_actual': sum(1 for f in filas if f['HD_Clase_Oro'] and f['En_Muestra_500'] == 'true'),
        'distribucion_predicha_todos': dict(Counter(f['HD_Clase_Modelo'] for f in filas)),
        'distribucion_predicha_universo': dict(Counter(
            f['HD_Clase_Modelo'] for f in filas if f['En_Universo_Entrenado'] == 'true')),
        'sha256_muestra': hashlib.sha256(Path(args.muestra).read_bytes()).hexdigest(),
        'sha256_etiquetas': hashlib.sha256(Path(args.etiquetas).read_bytes()).hexdigest(),
        'sha256_modelo': hashlib.sha256(
            (salida / 'modelo_hawkish_dovish.json').read_bytes()).hexdigest(),
    }
    (salida / 'resumen_entrenamiento.json').write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in resumen.items() if k != 'validacion_cruzada'},
                     ensure_ascii=False, indent=2))
    print('CV macro_f1=%.3f acc=%.3f mae=%.3f | lexico macro_f1=%.3f | mayoria macro_f1=%.3f'
          % (cv['macro_f1'], cv['accuracy'], cv.get('mae_puntaje', float('nan')),
             cv['baseline_lexico']['macro_f1'], cv['baseline_mayoria']['macro_f1']))
    print('CV agrupada por sesion macro_f1=%.3f acc=%.3f mae=%.3f (misma configuracion)'
          % (cv_sesion['macro_f1'], cv_sesion['accuracy'],
             cv_sesion.get('mae_puntaje', float('nan'))))
    print('escrito en', salida)


if __name__ == '__main__':
    main()
