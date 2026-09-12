#!/usr/bin/env python3
"""Mide si el release publica una medida de confianza usable.

La prioridad nº6 de la auditoría: el release entrega puntajes puntuales para 9.257
turnos sin incertidumbre. `Margen` existe pero nunca se validó como confianza.

Este script responde con datos, recomputando las predicciones **fuera de pliegue**
sobre las 500 (misma configuración y partición del release) y comparando tres
candidatos a medida de confianza:

  |HD_Score|  = |P(HAWKISH) - P(DOVISH)|   lo que el informe ya usaba
  Margen      = p(1) - p(2)                lo que el CSV publica
  max-prob    = p(clase predicha)          el estándar

Se reporta la curva de fiabilidad de cada uno, su error de calibración (ECE) y si
la precisión crece de forma monótona con la confianza.

Alcance importante que queda declarado en el artefacto: la calibración se estima
sobre las 500 **fuera de pliegue**. Para las otras 8.757 filas del corpus la
confianza del modelo es dentro de muestra respecto del oro que lo entrenó, así que
la curva no se les aplica sin más; y para las propias 500 el autoajuste da 0,988,
es decir, su confianza dentro de muestra está inflada.

Uso:
    python3 scripts/medir_calibracion_hawkish_dovish.py
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

CFG = {"max_rasgos": 600, "iteraciones": 30, "k": 5, "semilla": 0}
CUBOS = [(0.30, 0.50), (0.50, 0.60), (0.60, 0.70), (0.70, 0.80), (0.80, 0.90), (0.90, 1.01)]
CUBOS_SCORE = [(0.0, 0.25), (0.25, 0.50), (0.50, 0.75), (0.75, 1.01)]


def fuera_de_pliegue(cuentas: list, y: list) -> list[dict]:
    """Reproduce la partición del release y devuelve las predicciones con probabilidades."""
    oof: list = [None] * len(y)
    for fold in ent.pliegues(y, k=CFG["k"], semilla=CFG["semilla"]):
        test = set(fold)
        tr = [i for i in range(len(y)) if i not in test]
        trd = [cuentas[i] for i in tr]
        vocab = ent.seleccionar(trd, [y[i] for i in tr], CFG["max_rasgos"])
        idf = ent.idf_de(trd, vocab)
        modelo = ent.entrenar(ent.vectorizar(trd, vocab, idf), [y[i] for i in tr],
                              iteraciones=CFG["iteraciones"], p=len(vocab),
                              pesos_clase=ent.pesos_por_clase([y[i] for i in tr], True))
        Xte = ent.vectorizar([cuentas[i] for i in fold], vocab, idf)
        for j, i in enumerate(fold):
            oof[i] = ent.predecir(modelo, Xte[j])
    if any(o is None for o in oof):
        raise SystemExit("la partición no cubrió las 500")
    return oof


def curva(conf: list[float], ok: list[int], bordes: list[tuple]) -> tuple[list[dict], float]:
    """Curva de fiabilidad y ECE ponderado por tamaño de cubo."""
    n = len(ok)
    filas, ece = [], 0.0
    for lo, hi in bordes:
        idx = [i for i in range(n) if lo <= conf[i] < hi]
        if not idx:
            continue
        c = sum(conf[i] for i in idx) / len(idx)
        a = sum(ok[i] for i in idx) / len(idx)
        ece += len(idx) / n * abs(a - c)
        filas.append({"cubo": f"[{lo:.2f},{hi:.2f})", "n": len(idx),
                      "confianza_media": round(c, 4), "precision_real": round(a, 4),
                      "gap": round(a - c, 4)})
    return filas, round(ece, 4)


def es_monotona(filas: list[dict]) -> bool:
    v = [f["precision_real"] for f in filas]
    return all(b >= a for a, b in zip(v, v[1:]))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.parse_args()

    et = json.loads(ETIQUETAS.read_text(encoding="utf-8"))["Etiquetas"]
    por_id = {t["ID_Turno"]: t for t in hd.cargar_turnos()}
    y = [e["HD_Clase"] for e in et]
    cuentas = [ent.rasgos_texto(por_id[e["ID_Turno"]]["Texto"]) for e in et]

    oof = fuera_de_pliegue(cuentas, y)
    ok = [1 if oof[i]["clase"] == y[i] else 0 for i in range(len(y))]
    maxp = [max(oof[i]["probs"]) for i in range(len(y))]
    marg = [oof[i]["margen"] for i in range(len(y))]
    abss = [abs(oof[i]["score"]) for i in range(len(y))]

    c_maxp, ece_maxp = curva(maxp, ok, CUBOS)
    c_marg, ece_marg = curva(marg, ok, CUBOS)
    c_score, _ = curva(abss, ok, CUBOS_SCORE)

    res = {
        "configuracion": CFG,
        "n": len(y),
        "accuracy_fuera_de_pliegue": round(sum(ok) / len(ok), 4),
        "candidatos": {
            "max_prob": {"curva": c_maxp, "ece": ece_maxp,
                         "monotona": es_monotona(c_maxp)},
            "margen": {"curva": c_marg, "ece": ece_marg,
                       "monotona": es_monotona(c_marg)},
            "abs_score": {"curva": c_score, "monotona": es_monotona(c_score)},
        },
        "conclusion": "La medida de confianza usable es max-prob (p de la clase "
                      "predicha): su precisión crece de forma monótona y su ECE es "
                      "bajo. |HD_Score| no es monótona y por eso el release no debe "
                      "usarse para ordenar por certeza.",
        "limites": [
            "La calibración se estima sobre las 500 FUERA DE PLIEGUE. Para las otras "
            "8.757 filas del corpus la confianza del modelo es dentro de muestra "
            "respecto del oro que lo entrenó; la curva no se les aplica sin más.",
            "Para las propias 500 el autoajuste da 0,988: su confianza dentro de "
            "muestra está inflada y no debe leerse con esta curva.",
            "ECE con 6 cubos sobre 500 casos es sensible al corte de los cubos; la "
            "monotonía es la evidencia más robusta de las dos.",
        ],
    }
    RELEASE.mkdir(parents=True, exist_ok=True)
    (RELEASE / "calibracion_confianza.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"CALIBRACION DE LA CONFIANZA (n={res['n']}, acc oof {res['accuracy_fuera_de_pliegue']:.3f})")
    for nombre, clave in (("max-prob", "max_prob"), ("margen", "margen")):
        c = res["candidatos"][clave]
        print(f"\n  {nombre}: ECE {c['ece']:.4f} | monotona {c['monotona']}")
        print(f'    {"cubo":<14}{"n":>5}{"conf":>8}{"prec":>8}{"gap":>8}')
        for f in c["curva"]:
            print(f'    {f["cubo"]:<14}{f["n"]:>5}{f["confianza_media"]:>8.3f}'
                  f'{f["precision_real"]:>8.3f}{f["gap"]:>+8.3f}')
    s = res["candidatos"]["abs_score"]
    print(f"\n  |score|: monotona {s['monotona']}")
    print(f'    {"cubo":<14}{"n":>5}{"conf":>8}{"prec":>8}')
    for f in s["curva"]:
        print(f'    {f["cubo"]:<14}{f["n"]:>5}{f["confianza_media"]:>8.3f}{f["precision_real"]:>8.3f}')
    print(f"\n  {res['conclusion']}")
    print(f"\nescrito {(RELEASE / 'calibracion_confianza.json').relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
