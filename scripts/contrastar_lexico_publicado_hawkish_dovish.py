#!/usr/bin/env python3
"""Prioridad nº4 de la auditoría: validez convergente contra un léxico publicado.

El objetivo era contrastar el puntaje contra una fuente externa, como hace
Ornithologist con el Hawk-Dove Score de JP Morgan. El contraste pleno **no es
realizable con lo que hay en el repo**, y conviene decir por qué con precisión:

1. No hay serie de mercado en el repo (ningún archivo de tasas, spreads o
   expectativas), así que la vía JP Morgan está cerrada por datos.
2. Los léxicos hawk/dove publicados son **ingleses** —Apel & Grimaldi (2014),
   Bennani & Neuenkirch (2017), Loughran & McDonald (2011)— y este corpus es
   **español**. Traducirlos convertiría el "léxico publicado" en mi propia
   traducción, que es exactamente la circularidad que se quiere romper: el
   léxico propio y las 500 etiquetas ya son del mismo autor.

Lo que sí se puede medir sin traducir juicio alguno es la **cobertura de
dominios**. Apel & Grimaldi puntuan sobre 11 sustantivos temáticos ( inflation,
price, wage, oil price, cyclical position, growth, development, employment,
unemployment, recovery, cost ), citados en Quality & Quantity 58:5421-5444
(2024), nota 3. La correspondencia sustantivo->español no es discutible.

Resultado: 7 de 11 cubiertos. Los cuatro ausentes (wage, oil price, development,
recovery) son frecuentes en el corpus (23,7%-45,5% de los turnos), pero **no
producen un punto ciego**: entre los turnos que los mencionan, la fracción sin
señal léxica va de 17,9% a 29,4%, contra **41,8%** del universo completo. O sea
que esos turnos están mejor cubiertos que el promedio, porque la señal
direccional les llega por otro dominio (inflación, crecimiento, holguras).

La brecha de cobertura es real pero su impacto no es aislable con este método,
y no se traduce en una deficiencia medible. No se modifica el léxico.

Uso:
    python3 scripts/contrastar_lexico_publicado_hawkish_dovish.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import hawkish_dovish as hd  # noqa: E402

RELEASE = ROOT / 'data/releases/hawkish_dovish_v1'

# Los 11 sustantivos temáticos de Apel & Grimaldi (2014), vía Quality & Quantity
# 58:5421-5444 (2024), nota 3. Las equivalencias españolas son de dominio, no de
# criterio: son la única parte del contraste que no introduce juicio propio.
DOMINIOS = [
    ('inflation',         ['inflacion', 'inflacionari']),
    ('price',             ['precio']),
    ('wage',              ['salario', 'sueldo', 'remuneracion']),
    ('oil price',         ['petroleo', 'combustible', 'energia']),
    ('cyclical position', ['ciclo', 'ciclic', 'holgura', 'capacidad ociosa', 'brecha']),
    ('growth',            ['crecimiento', 'actividad', 'producto', 'pib', 'economia']),
    ('development',       ['evolucion', 'desempe', 'desarroll']),
    ('employment',        ['empleo', 'ocupacion', 'laboral', 'trabajo']),
    ('unemployment',      ['desempleo', 'desocupacion']),
    ('recovery',          ['recuperacion', 'repunte', 'revertir']),
    ('cost',              ['costo', 'coste']),
]

FUENTE = ('Apel & Grimaldi (2014), lista de 11 sustantivos temáticos citada en '
          'Quality & Quantity 58:5421-5444 (2024), nota 3')


def medir() -> dict:
    turnos = hd.cargar_turnos()
    universo = [t for t in turnos
                if t['Naturaleza_Turno'] == 'INTERVENCION' and t['Palabras'] >= 150]

    frases = [p for _, p in hd.HAWKISH] + [p for _, p in hd.DOVISH]
    # una sola pasada: la señal léxica de cada turno del universo
    con_senal = {t['ID_Turno']: hd.puntuar_lexico(t['Texto'])['score'] != 0.0
                 for t in universo}
    normalizado = {t['ID_Turno']: hd.normalizar(t['Texto']) for t in universo}

    sin_senal_universo = sum(1 for v in con_senal.values() if not v)
    base = {'turnos_universo': len(universo),
            'palabras_universo': sum(t['Palabras'] for t in universo),
            'sin_senal_lexica': sin_senal_universo,
            'fraccion_sin_senal_universo': round(sin_senal_universo / len(universo), 4)}

    dominios, ausentes = [], []
    for nombre, pats in DOMINIOS:
        en_lexico = sorted({p for p in frases if any(x in p for x in pats)})
        ids = [i for i in normalizado if any(p in normalizado[i] for p in pats)]
        n = len(ids)
        sin = sum(1 for i in ids if not con_senal[i])
        dominios.append({
            'dominio': nombre,
            'cubierto_por_lexico_propio': bool(en_lexico),
            'frases_propias': len(en_lexico),
            'ejemplo_frase_propia': en_lexico[0] if en_lexico else None,
            'turnos_que_lo_mencionan': n,
            'fraccion_del_universo': round(n / len(universo), 4),
            'de_esos_sin_senal': sin,
            'fraccion_de_esos_sin_senal': round(sin / n, 4) if n else None,
        })
        if not en_lexico:
            ausentes.append(dominios[-1])

    cubiertos = sum(1 for d in dominios if d['cubierto_por_lexico_propio'])
    # la brecha solo importa si los dominios ausentes dejan turnos mas a ciegas
    # que el promedio; si no, la señal les llega por otro dominio
    peor = max((d['fraccion_de_esos_sin_senal'] for d in ausentes), default=None)
    punto_ciego = peor is not None and peor > base['fraccion_sin_senal_universo']

    return {
        'objetivo': 'validez convergente contra un léxico hawk/dove publicado',
        'fuente_dominios': FUENTE,
        'dominios_publicados': len(DOMINIOS),
        'dominios_cubiertos': cubiertos,
        'dominios_ausentes': [d['dominio'] for d in ausentes],
        'detalle_dominios': dominios,
        'baseline_universo': base,
        'hay_punto_ciego_medible': punto_ciego,
        'veredicto': 'BRECHA REAL, IMPACTO NO MEDIBLE' if not punto_ciego
                     else 'PUNTO CIEGO DETECTADO',
        'contraste_pleno_posible': False,
        'por_que_no': [
            'No hay serie de mercado en el repo (tasas, spreads, expectativas), '
            'así que la vía de validez convergente tipo JP Morgan Hawk-Dove Score '
            'está cerrada por datos, no por método.',
            'Los léxicos hawk/dove publicados son ingleses (Apel & Grimaldi 2014, '
            'Bennani & Neuenkirch 2017, Loughran & McDonald 2011) y el corpus es '
            'español. Traducirlos convertiría la referencia externa en traducción '
            'propia, reintroduciendo la circularidad que se intenta romper: el '
            'léxico propio y las 500 etiquetas oro son del mismo autor.',
            'La correspondencia sustantivo temático -> español sí es verificable y '
            'es lo único de este contraste que no introduce criterio propio.',
        ],
        'limites': [
            'La equivalencia de los 11 dominios al español la hizo este agente; es '
            'de vocabulario y no de criterio, pero no deja de ser una decisión.',
            'Que un turno mencione el término no implica que el dominio cargue la '
            'postura: "han evolucionado por debajo de lo previsto" habla de '
            'inflación, que el léxico propio sí cubre.',
            'La comparación contra 41,8% es descriptiva. Aislar el efecto de cada '
            'dominio exigiría re-etiquetar, que es la prioridad nº1 y sigue abierta.',
            'No se modificó el léxico: cerrar la brecha sin medir su impacto sería '
            'agregar términos sin evidencia de que falten.',
        ],
    }


def main() -> None:
    res = medir()
    (RELEASE / 'contraste_lexico_publicado.json').write_text(
        json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')

    b = res['baseline_universo']
    print(f"CONTRASTE CONTRA LEXICO PUBLICADO ({res['fuente_dominios']})\n")
    print(f"  universo: {b['turnos_universo']} turnos, {b['palabras_universo']:,} palabras")
    print(f"  sin señal léxica: {b['sin_senal_lexica']} "
          f"({b['fraccion_sin_senal_universo']*100:.1f}%)\n")
    print(f"  dominios cubiertos: {res['dominios_cubiertos']}/{res['dominios_publicados']}"
          f"   ausentes: {', '.join(res['dominios_ausentes'])}\n")
    print(f"  {'dominio':<19}{'en léxico':>10}{'turnos':>9}{'% univ':>9}{'% sin señal':>13}")
    for d in res['detalle_dominios']:
        marca = 'sí' if d['cubierto_por_lexico_propio'] else 'NO'
        pct = f"{d['fraccion_de_esos_sin_senal']*100:.1f}%" \
            if d['fraccion_de_esos_sin_senal'] is not None else '—'
        print(f"  {d['dominio']:<19}{marca:>10}{d['turnos_que_lo_mencionan']:>9}"
              f"{d['fraccion_del_universo']*100:>8.1f}%{pct:>13}")
    print(f"\n  punto ciego medible: {res['hay_punto_ciego_medible']}")
    print(f"  veredicto: {res['veredicto']}")
    print(f"  contraste pleno posible: {res['contraste_pleno_posible']}")
    for r in res['por_que_no']:
        print(f'    - {r}')
    print(f"\nescrito {RELEASE / 'contraste_lexico_publicado.json'}")


if __name__ == '__main__':
    main()
