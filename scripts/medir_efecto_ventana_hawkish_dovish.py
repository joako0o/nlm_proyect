#!/usr/bin/env python3
"""Mide el efecto de la ventana de lectura sobre las etiquetas oro.

El límite nº2 del informe es que las 500 etiquetas se leyeron con una ventana
fija de 520 + 280 caracteres mientras el modelo entrena con el texto completo.
Hasta ahora esa asimetría estaba declarada pero **no medida**.

Este script la mide con una pasada adicional sobre las mismas 40 intervenciones
de la re-lectura ciega, leídas esta vez **completas**. Con tres pasadas sobre los
mismos textos se pueden separar dos cosas que de otro modo van mezcladas:

  ventana  vs oro   -> test-retest de la misma revisora (ya publicado: 0,825)
  completo vs oro   -> efecto de la ventana + ruido de re-lectura
  completo vs ventana -> **efecto puro de la ventana**, mismo lector

La tercera es la que responde la pregunta: si acuerdo es alto, la ventana no
cuesta mucho; si es bajo, las etiquetas dependen de cuánto texto se leyó.

Las etiquetas de la pasada completa son juicio humano y van en
``data/curation/lectura_completa_40.json``; este script sólo las compara.

Uso:
    python3 scripts/medir_efecto_ventana_hawkish_dovish.py
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

import hawkish_dovish as hd  # noqa: E402

ETIQUETAS = RAIZ / "data" / "curation" / "hawkish_dovish_etiquetas_v1.json"
CIEGO = RAIZ / "data" / "curation" / "relectura_ciega_40_textos.json"
VENTANA = RAIZ / "data" / "curation" / "relectura_ciega_40.json"
COMPLETA = RAIZ / "data" / "curation" / "lectura_completa_40.json"
RELEASE = RAIZ / "data" / "releases" / "hawkish_dovish_v1"

CLASES = ("HAWKISH", "NEUTRAL", "DOVISH")
BOOTSTRAP = 4000


def comparar(pares: list[dict], ka: str, kb: str, semilla: int = 20260911) -> dict:
    """Acuerdo, kappa y MAE entre dos pasadas, con intervalo por bootstrap."""
    n = len(pares)
    acuerdo = sum(1 for p in pares if p[f"{ka}_clase"] == p[f"{kb}_clase"]) / n
    se = math.sqrt(acuerdo * (1 - acuerdo) / n)
    mae = sum(abs(p[f"{ka}_score"] - p[f"{kb}_score"]) for p in pares) / n

    def kappa(muestra: list[dict]) -> float:
        po = sum(1 for p in muestra if p[f"{ka}_clase"] == p[f"{kb}_clase"]) / len(muestra)
        pe = sum(
            (sum(1 for p in muestra if p[f"{ka}_clase"] == c) / len(muestra))
            * (sum(1 for p in muestra if p[f"{kb}_clase"] == c) / len(muestra))
            for c in CLASES)
        return (po - pe) / (1 - pe) if pe != 1 else 0.0

    rng = random.Random(semilla)
    ks = []
    for _ in range(BOOTSTRAP):
        ks.append(kappa([pares[rng.randrange(n)] for _ in range(n)]))
    ks.sort()

    return {
        "n": n,
        "acuerdo": round(acuerdo, 4),
        "acuerdo_ic95": [round(acuerdo - 1.96 * se, 4), round(acuerdo + 1.96 * se, 4)],
        "kappa": round(kappa(pares), 4),
        "kappa_ic95": [round(ks[int(0.025 * (len(ks) - 1))], 4),
                       round(ks[int(0.975 * (len(ks) - 1))], 4)],
        "mae": round(mae, 4),
        "inversiones_de_signo": sum(1 for p in pares
                                    if {p[f"{ka}_clase"], p[f"{kb}_clase"]}
                                    == {"HAWKISH", "DOVISH"}),
        "cambios_de_clase": [
            {"ID_Turno": p["id"], f"{ka}": p[f"{ka}_clase"],
             f"{ka}_score": p[f"{ka}_score"], f"{kb}": p[f"{kb}_clase"],
             f"{kb}_score": p[f"{kb}_score"]}
            for p in pares if p[f"{ka}_clase"] != p[f"{kb}_clase"]],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.parse_args()

    for ruta in (CIEGO, VENTANA, COMPLETA, ETIQUETAS):
        if not ruta.exists():
            raise SystemExit(f"falta {ruta.relative_to(RAIZ)}")

    ids = [o["ID_Turno"] for o in json.loads(CIEGO.read_text(encoding="utf-8"))]
    vent = json.loads(VENTANA.read_text(encoding="utf-8"))["Relectura"]
    comp = json.loads(COMPLETA.read_text(encoding="utf-8"))["Lectura"]
    oro = {e["ID_Turno"]: e
           for e in json.loads(ETIQUETAS.read_text(encoding="utf-8"))["Etiquetas"]}
    for nombre, d in (("ventana", vent), ("completa", comp)):
        if set(d) != set(ids):
            raise SystemExit(f"la pasada {nombre} no cubre exactamente la submuestra")

    pares = [{"id": i,
              "co_score": float(comp[i]), "co_clase": hd.clase(float(comp[i])),
              "ve_score": float(vent[i]), "ve_clase": hd.clase(float(vent[i])),
              "or_score": float(oro[i]["HD_Score"]), "or_clase": oro[i]["HD_Clase"]}
             for i in ids]

    res = {
        "ventana_contra_oro": comparar(pares, "ve", "or"),
        "completo_contra_oro": comparar(pares, "co", "or"),
        "completo_contra_ventana": comparar(pares, "co", "ve"),
        "distribuciones": {
            "lectura_completa": {c: sum(1 for p in pares if p["co_clase"] == c) for c in CLASES},
            "relectura_ventana": {c: sum(1 for p in pares if p["ve_clase"] == c) for c in CLASES},
            "oro": {c: sum(1 for p in pares if p["or_clase"] == c) for c in CLASES},
        },
        "limites": [
            "n=40: las tres comparaciones tienen intervalos anchos y se solapan; ninguna "
            "diferencia entre ellas es significativa por sí sola.",
            "Las tres pasadas son de la misma revisora y las dos últimas se hicieron en la "
            "misma sesión, así que el efecto de la ventana está subestimado si hay memoria "
            "de la pasada anterior.",
            "Compara contra un oro que fue producido con la ventana; no dice cuál de las dos "
            "lecturas es más válida, sólo cuánto difieren.",
        ],
    }
    RELEASE.mkdir(parents=True, exist_ok=True)
    (RELEASE / "efecto_ventana.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"EFECTO DE LA VENTANA DE LECTURA (n={len(pares)})")
    print(f'{"comparacion":<34}{"acuerdo":>9}{"kappa":>8}{"MAE":>8}{"inv.signo":>11}')
    for clave, nom in (("ventana_contra_oro", "ventana vs oro (test-retest)"),
                       ("completo_contra_oro", "completo vs oro"),
                       ("completo_contra_ventana", "completo vs ventana (efecto puro)")):
        r = res[clave]
        print(f"{nom:<34}{r['acuerdo']:>9.3f}{r['kappa']:>8.3f}{r['mae']:>8.3f}"
              f"{r['inversiones_de_signo']:>11}")
    print("\nIC95 del acuerdo:")
    for clave, nom in (("ventana_contra_oro", "ventana vs oro"),
                       ("completo_contra_oro", "completo vs oro"),
                       ("completo_contra_ventana", "completo vs ventana")):
        lo, hi = res[clave]["acuerdo_ic95"]
        print(f"  {nom:<22} {lo:.3f} - {hi:.3f}")
    print("\ndistribuciones:", json.dumps(res["distribuciones"], ensure_ascii=False))
    print("\ncambios de clase al leer completo (vs oro):")
    for c in res["completo_contra_oro"]["cambios_de_clase"]:
        print(f"  {c['ID_Turno']:<22} oro {c['or']:<8}{c['or_score']:+.2f} -> "
              f"completo {c['co']:<8}{c['co_score']:+.2f}")
    print(f"\nescrito {(RELEASE / 'efecto_ventana.json').relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
