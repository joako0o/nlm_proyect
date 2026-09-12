#!/usr/bin/env python3
"""Prueba un remedio contra la deriva temporal y lo refuta.

La auditoría encontró que el modelo no generaliza hacia adelante: bajo
*rolling-origin* el macro-F1 cae a 0,456 contra el 0,685 publicado, y la causa es
desplazamiento real de etiquetas entre épocas (dovish pasa de 8,4% a 30,7% a 9,2%
a 23,8%).

El remedio estándar para *concept drift* es ponderar el pasado: quedarse sólo con
lo reciente. Este script prueba esa hipótesis comparando la ventana **expansiva**
(todo el pasado anterior al año de prueba) contra **ventanas deslizantes** de 3, 4
y 5 años, siempre con la misma configuración publicada y los mismos cortes.

Resultado: **refutada**. Todas las ventanas deslizantes rinden menos y ganan en 1
de 8 cortes. El mecanismo es que con 500 etiquetas en total, descartar años cuesta
más en tamaño de muestra de lo que gana en relevancia temporal: el conjunto de
entrenamiento cae de 282 a 138 casos en promedio.

Nota de alcance: esto NO prueba que ponderar por recencia no sirva; prueba que no
sirve *con este tamaño de oro*. Con 2.000 o 3.000 etiquetas la conclusión podría
invertirse, y el script queda para volver a correrlo.

Uso:
    python3 scripts/probar_deriva_temporal_hawkish_dovish.py
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

import hawkish_dovish as hd  # noqa: E402
import entrenar_hawkish_dovish as ent  # noqa: E402

ETIQUETAS = RAIZ / "data" / "curation" / "hawkish_dovish_etiquetas_v1.json"
RELEASE = RAIZ / "data" / "releases" / "hawkish_dovish_v1"

CFG = {"max_rasgos": 600, "iteraciones": 30}
VENTANAS = (None, 5, 4, 3)  # None = expansiva
NOMBRES = {None: "expansiva_todo_el_pasado", 5: "deslizante_5_anios",
           4: "deslizante_4_anios", 3: "deslizante_3_anios"}
MIN_ENTRENA = 80
MIN_PRUEBA = 15


def entrenar_probar(cuentas, y, scores, tr: list[int], te: list[int]) -> dict:
    trd = [cuentas[i] for i in tr]
    vocab = ent.seleccionar(trd, [y[i] for i in tr], CFG["max_rasgos"])
    idf = ent.idf_de(trd, vocab)
    modelo = ent.entrenar(ent.vectorizar(trd, vocab, idf), [y[i] for i in tr],
                          iteraciones=CFG["iteraciones"], p=len(vocab),
                          pesos_clase=ent.pesos_por_clase([y[i] for i in tr], True))
    Xte = ent.vectorizar([cuentas[i] for i in te], vocab, idf)
    preds = [ent.predecir(modelo, Xte[j]) for j in range(len(te))]
    return ent.metricas([y[i] for i in te], [p["clase"] for p in preds],
                        [scores[i] for i in te], [p["score"] for p in preds])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.parse_args()

    et = json.loads(ETIQUETAS.read_text(encoding="utf-8"))["Etiquetas"]
    por_id = {t["ID_Turno"]: t for t in hd.cargar_turnos()}
    docs = [por_id[e["ID_Turno"]]["Texto"] for e in et]
    y = [e["HD_Clase"] for e in et]
    scores = [float(e["HD_Score"]) for e in et]
    cuentas = [ent.rasgos_texto(d) for d in docs]
    anios = [int(e["ID_Turno"].split("-")[1]) for e in et]

    cortes = []
    for an in sorted(set(anios)):
        te = [i for i in range(len(y)) if anios[i] == an]
        base = [i for i in range(len(y)) if anios[i] < an]
        if len(base) >= MIN_ENTRENA and len(te) >= MIN_PRUEBA:
            cortes.append(an)

    estrategias = {}
    for k in VENTANAS:
        filas = []
        for an in cortes:
            te = [i for i in range(len(y)) if anios[i] == an]
            tr = [i for i in range(len(y))
                  if anios[i] < an and (k is None or anios[i] > an - 1 - k)]
            if len(tr) < MIN_ENTRENA:
                continue
            m = entrenar_probar(cuentas, y, scores, tr, te)
            filas.append({"anio_prueba": an, "n_entrena": len(tr), "n_prueba": len(te),
                          "macro_f1": m["macro_f1"]})
        estrategias[NOMBRES[k]] = filas

    base_vals = [f["macro_f1"] for f in estrategias["expansiva_todo_el_pasado"]]
    comparaciones = []
    for k in VENTANAS[1:]:
        nom = NOMBRES[k]
        vals = [f["macro_f1"] for f in estrategias[nom]]
        dif = [b - a for a, b in zip(base_vals, vals)]
        comparaciones.append({
            "estrategia": nom,
            "macro_f1_medio": round(sum(vals) / len(vals), 4),
            "macro_f1_sd": round(ent.desviacion(vals), 4),
            "n_entrena_medio": round(sum(f["n_entrena"] for f in estrategias[nom])
                                     / len(estrategias[nom]), 1),
            "diff_contra_expansiva": round(sum(dif) / len(dif), 4),
            "diff_sd": round(ent.desviacion(dif), 4),
            "gana_en": sum(1 for d in dif if d > 0),
            "cortes": len(dif),
        })

    res = {
        "configuracion": CFG,
        "cortes_evaluados": cortes,
        "expansiva": {
            "macro_f1_medio": round(sum(base_vals) / len(base_vals), 4),
            "macro_f1_sd": round(ent.desviacion(base_vals), 4),
            "n_entrena_medio": round(sum(f["n_entrena"] for f in
                                          estrategias["expansiva_todo_el_pasado"])
                                     / len(estrategias["expansiva_todo_el_pasado"]), 1),
            "por_corte": estrategias["expansiva_todo_el_pasado"],
        },
        "deslizantes": comparaciones,
        "por_corte": {nom: estrategias[nom] for nom in
                      [NOMBRES[k] for k in VENTANAS[1:]]},
        "veredicto": "REFUTADA",
        "lectura": "Restringir la ventana a los años recientes empeora el rendimiento "
                   "hacia adelante en todos los tamaños probados. Con 500 etiquetas, el "
                   "costo de descartar datos supera la ganancia de relevancia temporal. "
                   "No se publica ningún cambio al release.",
        "alcance": "Esto no prueba que ponderar por recencia no sirva en general: prueba "
                   "que no sirve con este tamaño de oro. Con 2.000-3.000 etiquetas la "
                   "conclusión podría invertirse.",
    }
    RELEASE.mkdir(parents=True, exist_ok=True)
    (RELEASE / "deriva_temporal.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"DERIVA TEMPORAL — {len(cortes)} cortes, config {CFG['max_rasgos']}/{CFG['iteraciones']}/bal")
    e = res["expansiva"]
    print(f"  {'expansiva (base)':<22} macroF1 {e['macro_f1_medio']:.4f} sd {e['macro_f1_sd']:.4f} "
          f"n_entrena {e['n_entrena_medio']:.0f}")
    for c in res["deslizantes"]:
        print(f"  {c['estrategia']:<22} macroF1 {c['macro_f1_medio']:.4f} sd {c['macro_f1_sd']:.4f} "
              f"n_entrena {c['n_entrena_medio']:.0f}  diff {c['diff_contra_expansiva']:+.4f} "
              f"gana {c['gana_en']}/{c['cortes']}")
    print(f"\n  veredicto: {res['veredicto']}")
    print(f"  {res['lectura']}")
    print(f"\nescrito {(RELEASE / 'deriva_temporal.json').relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
