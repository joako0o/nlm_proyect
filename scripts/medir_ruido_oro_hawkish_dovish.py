#!/usr/bin/env python3
"""Cuantifica el ruido del oro hawkish/dovish por re-lectura ciega.

El límite nº1 del informe es que las 500 etiquetas las produjo una sola revisora y
no se puede medir su fiabilidad sin una segunda. Este script aproxima la mitad de
esa medida: no hay segunda revisora, pero sí una **re-lectura** de la misma
revisora sobre una submuestra ciega, sin ver el oro original.

Protocolo:
  1. ``muestra_ciega()`` sortea ``N_RELECTURA`` intervenciones del oro y emite
     sólo ID y ventana de texto (cabeza 520 + cola 280, la misma del protocolo).
     Comprueba que el texto emitido no contenga ningún token de etiqueta.
  2. Una persona puntúa esas ventanas de -1 a +1 sin abrir el oro y guarda el
     resultado en ``data/curation/relectura_ciega_40.json``.
  3. Este script compara ambas pasadas: acuerdo, kappa, MAE, correlación,
     matriz de confusión y los intervalos correspondientes.

Límites que este script NO resuelve y declara en su salida:
  - Es test-retest de UNA revisora, no fiabilidad entre revisoras. Mide
    estabilidad de criterio, no validez.
  - Quien re-leyó ya había etiquetado las 500 antes. No se puede descartar
    memoria parcial, así que el acuerdo observado es un TECHO optimista.
  - Con n=40 los intervalos son anchos; se reportan siempre.

Uso:
    python3 scripts/medir_ruido_oro_hawkish_dovish.py            # emite ciego + compara
    python3 scripts/medir_ruido_oro_hawkish_dovish.py --emitir   # sólo emite la submuestra
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

import hawkish_dovish as hd  # noqa: E402
from etiquetar_hawkish_dovish import LECTURA_CABEZA, LECTURA_COLA  # noqa: E402

ETIQUETAS = RAIZ / "data" / "curation" / "hawkish_dovish_etiquetas_v1.json"
RELECTURA = RAIZ / "data" / "curation" / "relectura_ciega_40.json"
CIEGO = RAIZ / "data" / "curation" / "relectura_ciega_40_textos.json"
RELEASE = RAIZ / "data" / "releases" / "hawkish_dovish_v1"

N_RELECTURA = 40
SEMILLA_RELECTURA = 20260911
CLASES = ("HAWKISH", "NEUTRAL", "DOVISH")
BOOTSTRAP = 4000


SEPARADOR = "  [\u2026]  "  # dos espacios + [ + puntos suspensivos + ] + dos espacios = 7 chars


def ventana(texto: str) -> str:
    """La misma ventana de lectura del protocolo: cabeza 520 + cola 280.

    Los saltos de línea se convierten en espacios uno a uno (mismo largo) para que
    la ventana se lea como un solo párrafo, igual que en la pasada original.
    """
    texto = texto.replace("\n", " ")
    if len(texto) <= LECTURA_CABEZA + LECTURA_COLA:
        return texto
    return texto[:LECTURA_CABEZA] + SEPARADOR + texto[-LECTURA_COLA:]


TOKENS_PROHIBIDOS = ("HAWKISH", "DOVISH", "NEUTRAL", "HD_Clase", "HD_Score", "Evidencia")


def muestra_ciega(n: int = N_RELECTURA, semilla: int = SEMILLA_RELECTURA) -> list[dict]:
    """Sortea n intervenciones del oro y devuelve sólo ID y texto, sin etiquetas.

    La cita de ``Evidencia`` se extrae del propio discurso, así que puede aparecer
    legítimamente en la ventana: quien re-lee la vería de todos modos. Lo que sí se
    veta son los tokens de metadato que revelarían la etiqueta sin leer.
    """
    turnos = hd.cargar_turnos()
    rng = random.Random(semilla)
    etiquetas = json.loads(ETIQUETAS.read_text(encoding="utf-8"))["Etiquetas"]
    ids = [o["ID_Turno"] for o in etiquetas]
    elegidos = rng.sample(sorted(ids), n)
    por_id = {t["ID_Turno"]: t for t in turnos if t["ID_Turno"] in set(elegidos)}

    ciego = []
    for ident in elegidos:  # orden del sorteo, no del oro
        t = por_id[ident]
        texto = ventana(t["Texto"])
        for token in TOKENS_PROHIBIDOS:
            if token in texto:
                raise AssertionError(
                    f"fuga de metadato en {ident}: {token!r} aparece en la ventana")
        ciego.append({"ID_Turno": ident, "Fecha": t["Fecha"], "Actor_Final": t["Actor_Final"],
                      "Rol_Final": t["Rol_Final"], "Palabras": t["Palabras"],
                      "Ventana": texto})
    return ciego


def kappa(muestra: list[dict]) -> float:
    """Kappa de Cohen entre la clase re-leída y la clase del oro."""
    n = len(muestra)
    po = sum(1 for p in muestra if p["re_clase"] == p["oro_clase"]) / n
    pe = sum(
        (sum(1 for p in muestra if p["re_clase"] == c) / n)
        * (sum(1 for p in muestra if p["oro_clase"] == c) / n)
        for c in CLASES
    )
    return (po - pe) / (1 - pe) if pe != 1 else 0.0


def cuantiles(valores: list[float]) -> tuple[float, float]:
    ordenado = sorted(valores)
    return (ordenado[int(0.025 * (len(ordenado) - 1))],
            ordenado[int(0.975 * (len(ordenado) - 1))])


def comparar(pares: list[dict], semilla: int = SEMILLA_RELECTURA) -> dict:
    """Acuerdo, kappa, MAE, r y sus intervalos, más la matriz de confusión."""
    n = len(pares)
    acuerdo = sum(1 for p in pares if p["re_clase"] == p["oro_clase"]) / n
    se = math.sqrt(acuerdo * (1 - acuerdo) / n)
    mae = sum(abs(p["re_score"] - p["oro_score"]) for p in pares) / n

    mu_re = sum(p["re_score"] for p in pares) / n
    mu_oro = sum(p["oro_score"] for p in pares) / n
    cov = sum((p["re_score"] - mu_re) * (p["oro_score"] - mu_oro) for p in pares)
    den = (sum((p["re_score"] - mu_re) ** 2 for p in pares)
           * sum((p["oro_score"] - mu_oro) ** 2 for p in pares)) ** 0.5
    r = cov / den if den else 0.0

    rng = random.Random(semilla)
    ks, ms = [], []
    for _ in range(BOOTSTRAP):
        b = [pares[rng.randrange(n)] for _ in range(n)]
        ks.append(kappa(b))
        ms.append(sum(abs(p["re_score"] - p["oro_score"]) for p in b) / n)
    k_lo, k_hi = cuantiles(ks)
    m_lo, m_hi = cuantiles(ms)

    matriz = {a: {b: sum(1 for p in pares
                         if p["re_clase"] == a and p["oro_clase"] == b) for b in CLASES}
              for a in CLASES}

    return {
        "n": n,
        "acuerdo_clase": round(acuerdo, 4),
        "acuerdo_ic95": [round(acuerdo - 1.96 * se, 4), round(acuerdo + 1.96 * se, 4)],
        "kappa": round(kappa(pares), 4),
        "kappa_ic95": [round(k_lo, 4), round(k_hi, 4)],
        "mae_puntaje": round(mae, 4),
        "mae_ic95": [round(m_lo, 4), round(m_hi, 4)],
        "correlacion_puntaje": round(r, 4),
        "inversiones_de_signo": sum(1 for p in pares
                                    if {p["re_clase"], p["oro_clase"]} == {"HAWKISH", "DOVISH"}),
        "distribucion_relectura": {c: sum(1 for p in pares if p["re_clase"] == c) for c in CLASES},
        "distribucion_oro": {c: sum(1 for p in pares if p["oro_clase"] == c) for c in CLASES},
        "matriz_relectura_contra_oro": matriz,
        "discrepancias": [
            {"ID_Turno": p["id"], "relectura": p["re_clase"], "relectura_score": p["re_score"],
             "oro": p["oro_clase"], "oro_score": p["oro_score"]}
            for p in pares if p["re_clase"] != p["oro_clase"]
        ],
    }


def contraste_modelo(pares: list[dict]) -> dict:
    """Cómo le va al modelo fuera de pliegue en la misma submuestra re-leída.

    Sin esto el acuerdo 0,825 queda flotando: no se puede decir nada sobre si el
    clasificador alcanzó el techo que le impone el ruido de sus propias etiquetas
    si no se mide al modelo sobre los mismos casos.
    """
    fallos = RELEASE / "fallos_fuera_de_pliegue.csv"
    with fallos.open(newline="", encoding="utf-8") as fh:
        oof = {r["ID_Turno"]: r for r in csv.DictReader(fh)}
    faltan = [p["id"] for p in pares if p["id"] not in oof]
    if faltan:
        raise SystemExit(f"el CSV de fallos no cubre la submuestra: {faltan[:3]}")

    aciertos_sub = sum(1 for p in pares
                       if oof[p["id"]]["HD_Clase_Oro"] == oof[p["id"]]["Pred_Fuera_De_Pliegue"])
    aciertos_todas = sum(1 for r in oof.values()
                         if r["HD_Clase_Oro"] == r["Pred_Fuera_De_Pliegue"])
    return {
        "modelo_en_la_submuestra": round(aciertos_sub / len(pares), 4),
        "modelo_aciertos_en_la_submuestra": f"{aciertos_sub}/{len(pares)}",
        "modelo_en_las_500": round(aciertos_todas / len(oof), 4),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--emitir", action="store_true", help="sólo escribe la submuestra ciega")
    args = ap.parse_args()

    if not CIEGO.exists():
        CIEGO.write_text(json.dumps(muestra_ciega(), ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print(f"escrito {CIEGO.relative_to(RAIZ)} ({N_RELECTURA} ventanas, sin etiquetas)")
    if args.emitir:
        return

    ciego = json.loads(CIEGO.read_text(encoding="utf-8"))
    re = json.loads(RELECTURA.read_text(encoding="utf-8"))["Relectura"]
    oro = {e["ID_Turno"]: e
           for e in json.loads(ETIQUETAS.read_text(encoding="utf-8"))["Etiquetas"]}
    if {o["ID_Turno"] for o in ciego} != set(re):
        raise SystemExit("la relectura no cubre exactamente la submuestra ciega")

    pares = [{"id": o["ID_Turno"],
              "re_score": float(re[o["ID_Turno"]]),
              "re_clase": hd.clase(float(re[o["ID_Turno"]])),
              "oro_score": float(oro[o["ID_Turno"]]["HD_Score"]),
              "oro_clase": oro[o["ID_Turno"]]["HD_Clase"]} for o in ciego]

    res = comparar(pares)
    res['contraste_con_el_modelo'] = contraste_modelo(pares)
    res["protocolo"] = {
        "submuestra": N_RELECTURA,
        "semilla": SEMILLA_RELECTURA,
        "ventana_lectura": f"cabeza {LECTURA_CABEZA} + cola {LECTURA_COLA}",
        "umbral_clase": hd.UMBRAL_CLASE,
        "bootstrap": BOOTSTRAP,
    }
    res["limites"] = [
        "Es test-retest de UNA sola revisora: mide estabilidad de criterio, no "
        "fiabilidad entre revisoras ni validez de la etiqueta.",
        "Quien re-leyó ya había etiquetado las 500 originales; no se descarta memoria "
        "parcial, así que el acuerdo observado es un techo optimista del verdadero.",
        f"Con n={N_RELECTURA} los intervalos son anchos; el de kappa cruza el rango "
        "de acuerdo moderado a casi perfecto.",
    ]
    RELEASE.mkdir(parents=True, exist_ok=True)
    (RELEASE / "ruido_oro.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"RE-LECTURA CIEGA (n={res['n']}, semilla {SEMILLA_RELECTURA})")
    print(f"  acuerdo de clase : {res['acuerdo_clase']:.3f}  IC95 "
          f"{res['acuerdo_ic95'][0]:.3f}-{res['acuerdo_ic95'][1]:.3f}")
    print(f"  kappa de Cohen   : {res['kappa']:.3f}  IC95 "
          f"{res['kappa_ic95'][0]:.3f}-{res['kappa_ic95'][1]:.3f}")
    print(f"  MAE del puntaje  : {res['mae_puntaje']:.3f}  IC95 "
          f"{res['mae_ic95'][0]:.3f}-{res['mae_ic95'][1]:.3f}")
    print(f"  correlacion r    : {res['correlacion_puntaje']:.3f}")
    print(f"  inversiones signo: {res['inversiones_de_signo']}")
    cm = res["contraste_con_el_modelo"]
    print(f"  modelo fuera de pliegue en estas {res['n']}: "
          f"{cm['modelo_en_la_submuestra']:.3f} ({cm['modelo_aciertos_en_la_submuestra']})")
    print(f"  modelo fuera de pliegue en las 500    : "
          f"{cm['modelo_en_las_500']:.3f}")
    print("  matriz (filas=relectura, columnas=oro):")
    print("                 " + "".join(f"{c:>9}" for c in CLASES))
    for a in CLASES:
        print(f"    {a:<13}" + "".join(f"{res['matriz_relectura_contra_oro'][a][b]:>9}"
                                       for b in CLASES))
    print(f"\nescrito {(RELEASE / 'ruido_oro.json').relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
