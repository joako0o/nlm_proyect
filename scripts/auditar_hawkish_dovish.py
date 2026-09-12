#!/usr/bin/env python3
"""Auditoría metodológica de la capa hawkish/dovish v1.

Mide cuatro cosas que el informe publicado NO medía y que la literatura sobre
medición de tono de banca central sí exige:

1. **Fuga entre pliegues por sesión.** ``pliegues()`` baraja por turno, y los
   turnos de una misma RPM comparten día, discusión y vocabulario. Se compara la
   CV aleatoria por turno contra una CV agrupada por sesión.

2. **Generalización temporal.** El número publicado es una CV aleatoria que mezcla
   2005 con 2015. Aquí se hace *rolling-origin*: entrenar con todo lo anterior y
   probar con el año siguiente. Es lo relevante si el puntaje se aplica a reuniones
   nuevas.

3. **Desplazamiento de etiquetas.** La composición hawkish/neutral/dovish cambia
   por época; es historia monetaria real (ciclo de alzas, crisis, normalización,
   inflación baja), no un artefacto, y rompe la intercambiabilidad que supone la CV.

4. **Validez de constructo.** La literatura valida el índice contra decisiones de
   tasa reales. El corpus contiene el Acuerdo formal de cada reunión, así que se
   extrae la decisión y se contrasta con el tono. Se reportan tres versiones, de
   más contaminada a más limpia:
     - contemporánea (tono y decisión de la misma reunión);
     - contemporánea excluyendo los turnos que contienen el anuncio/comunicado;
     - **tono de la reunión t contra la decisión de la reunión t+1**, que es la
       única sin fuga posible.

Uso:
    python3 scripts/auditar_hawkish_dovish.py
    python3 scripts/auditar_hawkish_dovish.py --rapido   # 3 semillas en vez de 10
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

import hawkish_dovish as hd  # noqa: E402
import entrenar_hawkish_dovish as ent  # noqa: E402

ETIQUETAS = RAIZ / "data" / "curation" / "hawkish_dovish_etiquetas_v1.json"
PUNTAJES = RAIZ / "data" / "releases" / "hawkish_dovish_v1" / "puntajes_hawkish_dovish.csv"
RELEASE = RAIZ / "data" / "releases" / "hawkish_dovish_v1"

# configuración publicada en el release
CFG = {"max_rasgos": 600, "iteraciones": 30, "balancear": True, "k": 5}
CLASES = ("HAWKISH", "NEUTRAL", "DOVISH")
EPOCAS = ((2005, 2007), (2008, 2009), (2010, 2012), (2013, 2015))

ANCLA_ACUERDO = re.compile(r"Acuerdo[:\s].{0,60}T\s*a\s*s\s*a de Pol[ií]tica Monetaria",
                           re.I | re.S)
VERBO = re.compile(r"\b(mantener|mantuvo|elevar|elev[oó]|aumentar|aument[oó]|reducir|"
                   r"redujo|disminuir|disminuy[oó])\b", re.I)
NIVEL = re.compile(r"(?:hasta|a|en)\s*(\d+(?:[.,]\d{1,2})?)\s*%", re.I)
ANUNCIO = re.compile(r"(Acuerdo[:\s].{0,60}T\s*a\s*s\s*a de Pol[ií]tica Monetaria|Comunicado)",
                     re.I | re.S)


def direccion(verbo: str) -> int:
    if verbo.startswith(("aument", "elev")):
        return 1
    if verbo.startswith(("reduc", "dismin")):
        return -1
    return 0


def spearman(a: list[float], b: list[float]) -> float:
    """Correlación de rangos, con desempate por rango medio."""
    def rango(v: list[float]) -> list[float]:
        orden = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(orden):
            j = i
            while j + 1 < len(orden) and v[orden[j + 1]] == v[orden[i]]:
                j += 1
            for kk in range(i, j + 1):
                r[orden[kk]] = (i + j) / 2 + 1
            i = j + 1
        return r

    xs, ys = rango(a), rango(b)
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den if den else 0.0


def decidir(turnos: list[dict]) -> dict[str, dict]:
    """Extrae la decisión formal de TPM del Acuerdo de cada reunión.

    Tolera dos defectos del OCR presentes en el corpus: espacios dentro de la
    palabra ("T a s a", "T asa") y niveles sin decimales ("hasta 3% anual").
    """
    por_sesion: dict[str, dict] = {}
    for t in turnos:
        sid = t["ID_Turno"].split(":")[0]
        m = ANCLA_ACUERDO.search(t["Texto"])
        if not m:
            continue
        frag = t["Texto"][m.start():m.start() + 420].replace("\n", " ")
        v, n = VERBO.search(frag), NIVEL.search(frag)
        if not (v and n):
            continue
        por_sesion.setdefault(sid, {"ID_Turno": t["ID_Turno"], "verbo": v.group(1).lower(),
                                    "nivel": float(n.group(1).replace(",", "."))})
    return por_sesion


def cohorte(turnos: list[dict], decisiones: dict[str, dict]) -> dict:
    """Verifica que la serie extraída sea internamente coherente."""
    sesiones = sorted({t["ID_Turno"].split(":")[0] for t in turnos})
    pos = {s: i for i, s in enumerate(sesiones)}
    orden = [s for s in sesiones if s in decisiones]
    incoherencias = []
    for a, b in zip(orden, orden[1:]):
        if pos[b] - pos[a] != 1:
            continue  # hay reuniones intermedias sin extraer: el salto no es comparable
        delta = round(decisiones[b]["nivel"] - decisiones[a]["nivel"], 2)
        if (delta == 0) != decisiones[b]["verbo"].startswith(("mant",)):
            incoherencias.append({"sesion": b, "verbo": decisiones[b]["verbo"], "delta": delta})
    return {"sesiones_del_corpus": len(sesiones), "sesiones_con_decision": len(orden),
            "transiciones_consecutivas_comparadas":
                sum(1 for a, b in zip(orden, orden[1:]) if pos[b] - pos[a] == 1),
            "incoherencias_verbo_nivel": incoherencias}


def particion_sesion(y: list[str], sesiones: list[str], k: int, semilla: int) -> list[list[int]]:
    """Todos los turnos de una sesión caen en el mismo pliegue."""
    ses = sorted(set(sesiones))
    rng = random.Random(semilla)
    rng.shuffle(ses)
    asigna = {s: i % k for i, s in enumerate(ses)}
    return [[i for i, s in enumerate(sesiones) if asigna[s] == f] for f in range(k)]


def evaluar_particion(cuentas, y, scores, particion) -> float:
    """Macro-F1 fuera de pliegue con una partición arbitraria (mismo pipeline)."""
    oof = [None] * len(y)
    for fold in particion:
        test = set(fold)
        tr = [i for i in range(len(y)) if i not in test]
        trd = [cuentas[i] for i in tr]
        vocab = ent.seleccionar(trd, [y[i] for i in tr], CFG["max_rasgos"])
        idf = ent.idf_de(trd, vocab)
        modelo = ent.entrenar(ent.vectorizar(trd, vocab, idf), [y[i] for i in tr],
                              iteraciones=CFG["iteraciones"], p=len(vocab),
                              pesos_clase=ent.pesos_por_clase([y[i] for i in tr], CFG["balancear"]))
        Xte = ent.vectorizar([cuentas[i] for i in fold], vocab, idf)
        for j, i in enumerate(fold):
            oof[i] = ent.predecir(modelo, Xte[j])
    idx = [i for i in range(len(y)) if oof[i] is not None]
    return ent.metricas([y[i] for i in idx], [oof[i]["clase"] for i in idx],
                        [scores[i] for i in idx], [oof[i]["score"] for i in idx])["macro_f1"]


def entrenar_probar(cuentas, y, scores, tr: list[int], te: list[int]) -> dict:
    trd = [cuentas[i] for i in tr]
    vocab = ent.seleccionar(trd, [y[i] for i in tr], CFG["max_rasgos"])
    idf = ent.idf_de(trd, vocab)
    modelo = ent.entrenar(ent.vectorizar(trd, vocab, idf), [y[i] for i in tr],
                          iteraciones=CFG["iteraciones"], p=len(vocab),
                          pesos_clase=ent.pesos_por_clase([y[i] for i in tr], CFG["balancear"]))
    Xte = ent.vectorizar([cuentas[i] for i in te], vocab, idf)
    preds = [ent.predecir(modelo, Xte[j]) for j in range(len(te))]
    return ent.metricas([y[i] for i in te], [p["clase"] for p in preds],
                        [scores[i] for i in te], [p["score"] for p in preds])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rapido", action="store_true", help="3 semillas de CV en vez de 10")
    args = ap.parse_args()
    semillas = tuple(range(3)) if args.rapido else tuple(range(10))

    et = json.loads(ETIQUETAS.read_text(encoding="utf-8"))["Etiquetas"]
    turnos = hd.cargar_turnos()
    por_id = {t["ID_Turno"]: t for t in turnos}
    docs = [por_id[e["ID_Turno"]]["Texto"] for e in et]
    y = [e["HD_Clase"] for e in et]
    scores = [float(e["HD_Score"]) for e in et]
    cuentas = [ent.rasgos_texto(d) for d in docs]
    sesiones = [e["ID_Turno"].split(":")[0] for e in et]
    anios = [int(e["ID_Turno"].split("-")[1]) for e in et]

    # 1. fuga por sesión
    partidas = []
    for sem in semillas:
        en = defaultdict(set)
        for f, pl in enumerate(ent.pliegues(y, k=CFG["k"], semilla=sem)):
            for i in pl:
                en[sesiones[i]].add(f)
        partidas.append(sum(1 for v in en.values() if len(v) > 1) / len(en))
    por_turno, por_sesion = [], []
    for sem in semillas:
        por_turno.append(evaluar_particion(cuentas, y, scores,
                                           ent.pliegues(y, k=CFG["k"], semilla=sem)))
        por_sesion.append(evaluar_particion(cuentas, y, scores,
                                            particion_sesion(y, sesiones, CFG["k"], sem)))
    dif = [b - a for a, b in zip(por_turno, por_sesion)]

    # 2. generalización temporal
    rolling = []
    for an in sorted(set(anios)):
        tr = [i for i in range(len(y)) if anios[i] < an]
        te = [i for i in range(len(y)) if anios[i] == an]
        if len(tr) < 80 or len(te) < 15:
            continue
        m = entrenar_probar(cuentas, y, scores, tr, te)
        rolling.append({"anio_prueba": an, "n_entrena": len(tr), "n_prueba": len(te),
                        "macro_f1": m["macro_f1"], "accuracy": m["accuracy"]})

    # 2b. cortes temporales acumulativos, con el lexico como contraste
    cortes = []
    lex_scores = [hd.puntuar_lexico(d)["score"] for d in docs]
    for corte in (2011, 2012, 2013):
        tr = [i for i in range(len(y)) if anios[i] <= corte]
        te = [i for i in range(len(y)) if anios[i] > corte]
        m = entrenar_probar(cuentas, y, scores, tr, te)
        lx = [lex_scores[i] for i in te]
        base = ent.metricas([y[i] for i in te], [ent.clase(v) for v in lx],
                            [scores[i] for i in te], lx)
        cortes.append({"corte": corte, "n_entrena": len(tr), "n_prueba": len(te),
                       "macro_f1": m["macro_f1"], "macro_f1_lexico": base["macro_f1"]})

    # 3. desplazamiento de etiquetas
    epocas = []
    for lo, hi in EPOCAS:
        idx = [i for i in range(len(y)) if lo <= anios[i] <= hi]
        c = Counter(y[i] for i in idx)
        epocas.append({"periodo": f"{lo}-{hi}", "n": len(idx),
                       **{k: round(c[k] / len(idx), 4) for k in CLASES}})

    # 4. validez de constructo contra decisiones reales
    decisiones = decidir(turnos)
    cal = cohorte(turnos, decisiones)
    ses_corpus = sorted({t["ID_Turno"].split(":")[0] for t in turnos})
    siguiente = {s: ses_corpus[i + 1] for i, s in enumerate(ses_corpus[:-1])}
    anuncio = {r["ID_Turno"] for r in
               csv.DictReader(PUNTAJES.open(newline="", encoding="utf-8"))
               if r["En_Universo_Entrenado"] == "true"
               and ANUNCIO.search(por_id[r["ID_Turno"]]["Texto"])}

    tono = {True: defaultdict(list), False: defaultdict(list)}
    with PUNTAJES.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["Grupo_Actor"] != "CONSEJO" or r["En_Universo_Entrenado"] != "true":
                continue
            es_anuncio = r["ID_Turno"] in anuncio
            tono[False][r["ID_Turno"].split(":")[0]].append(float(r["HD_Score_Modelo"]))
            if not es_anuncio:
                tono[True][r["ID_Turno"].split(":")[0]].append(float(r["HD_Score_Modelo"]))

    def contraste(pares):
        rho = spearman([t for _, t in pares], [d for d, _ in pares])
        medias = {}
        for d, nom in ((1, "ALZA"), (0, "SIN_CAMBIO"), (-1, "RECORTE")):
            v = [t for dd, t in pares if dd == d]
            medias[nom] = {"n": len(v), "tono_medio": round(sum(v) / len(v), 4)} if v else None
        return {"n": len(pares), "spearman": round(rho, 4), "tono_medio_por_decision": medias}

    cont = [(direccion(decisiones[s]["verbo"]), sum(tono[False][s]) / len(tono[False][s]))
            for s in sorted(decisiones) if tono[False][s]]
    limpio = [(direccion(decisiones[s]["verbo"]), sum(tono[True][s]) / len(tono[True][s]))
              for s in sorted(decisiones) if tono[True][s]]
    futuro = [(direccion(decisiones[siguiente[s]]["verbo"]),
               sum(tono[True][s]) / len(tono[True][s]))
              for s in ses_corpus
              if tono[True][s] and siguiente.get(s) in decisiones]

    res = {
        "configuracion_auditada": CFG,
        "fuga_por_sesion": {
            "fraccion_sesiones_repartidas_en_varios_pliegues": round(sum(partidas) / len(partidas), 4),
            "macro_f1_cv_por_turno": round(sum(por_turno) / len(por_turno), 4),
            "macro_f1_cv_por_sesion": round(sum(por_sesion) / len(por_sesion), 4),
            "diferencia_media": round(sum(dif) / len(dif), 4),
            "diferencia_sd": round(ent.desviacion(dif), 4),
            "semillas_donde_por_sesion_es_menor": sum(1 for d in dif if d < 0),
            "semillas": list(semillas),
        },
        "generalizacion_temporal": {
            "rolling_origin": rolling,
            "macro_f1_medio": round(sum(r["macro_f1"] for r in rolling) / len(rolling), 4),
            "macro_f1_sd": round(ent.desviacion([r["macro_f1"] for r in rolling]), 4),
            "accuracy_media": round(sum(r["accuracy"] for r in rolling) / len(rolling), 4),
        },
        "cortes_temporales": cortes,
        "desplazamiento_de_etiquetas": epocas,
        "validez_de_constructo": {
            "extraccion_de_decisiones": cal,
            "contemporanea_con_anuncio": contraste(cont),
            "contemporanea_sin_anuncio": contraste(limpio),
            "tono_t_contra_decision_t1": contraste(futuro),
        },
    }
    RELEASE.mkdir(parents=True, exist_ok=True)
    (RELEASE / "auditoria_metodologica.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    f = res["fuga_por_sesion"]
    print("1. FUGA POR SESION")
    print(f"   {f['fraccion_sesiones_repartidas_en_varios_pliegues']:.1%} de las sesiones "
          f"quedan en mas de un pliegue")
    print(f"   macroF1 por turno {f['macro_f1_cv_por_turno']:.4f} | por sesion "
          f"{f['macro_f1_cv_por_sesion']:.4f} | diff {f['diferencia_media']:+.4f} "
          f"sd {f['diferencia_sd']:.4f}")
    g = res["generalizacion_temporal"]
    print("2. GENERALIZACION TEMPORAL (rolling-origin)")
    print(f"   macroF1 medio {g['macro_f1_medio']:.4f} sd {g['macro_f1_sd']:.4f} "
          f"| accuracy media {g['accuracy_media']:.4f}")
    for r in rolling:
        print(f"     prueba {r['anio_prueba']} n={r['n_prueba']:>3}: "
              f"macroF1 {r['macro_f1']:.4f} acc {r['accuracy']:.4f}")
    print("2b. CORTES TEMPORALES ACUMULATIVOS (entrena <= corte, prueba > corte)")
    for c in res["cortes_temporales"]:
        print(f"     corte {c['corte']}: macroF1 {c['macro_f1']:.4f} vs lexico "
              f"{c['macro_f1_lexico']:.4f} (n_prueba {c['n_prueba']})")
    print("3. DESPLAZAMIENTO DE ETIQUETAS")
    for e in epocas:
        print(f"   {e['periodo']} n={e['n']:>3}: " + " ".join(
            f"{k[:1]} {e[k]*100:>5.1f}%" for k in CLASES))
    v = res["validez_de_constructo"]
    print("4. VALIDEZ DE CONSTRUCTO (contra decisiones de tasa reales)")
    print(f"   decisiones extraidas: {v['extraccion_de_decisiones']['sesiones_con_decision']}"
          f"/{v['extraccion_de_decisiones']['sesiones_del_corpus']}; incoherencias "
          f"{len(v['extraccion_de_decisiones']['incoherencias_verbo_nivel'])}")
    for clave, nom in (("contemporanea_con_anuncio", "contemporanea (con anuncio)"),
                       ("contemporanea_sin_anuncio", "contemporanea (sin anuncio)"),
                       ("tono_t_contra_decision_t1", "tono_t -> decision_t+1")):
        c = v[clave]
        print(f"   {nom:<26} n={c['n']:>3} Spearman {c['spearman']:+.4f}")
    print(f"\nescrito {(RELEASE / 'auditoria_metodologica.json').relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
