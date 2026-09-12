"""Puntaje hawkish/dovish de intervenciones y muestra estratificada para etiquetar.

Dos piezas independientes y auditables:

1. ``puntuar_lexico`` — baseline determinista por léxico ponderado de política
   monetaria en español. Sirve de referencia y de estratificador; no se usa como
   etiqueta oro.
2. ``muestra`` — sorteo estratificado (año x grupo de actor x tercio léxico) de
   las intervenciones que se leerán y puntarán a mano.

El texto de cada turno se reconstruye desde el consolidado uniendo las filas
``ID_Desde..ID_Hasta`` de ``turnos_habla.csv``. La reconstrucción se valida fila
por fila contra ``Numero_Filas`` y ``Palabras`` antes de puntuar nada.
"""
import argparse
import csv
import hashlib
import json
import random
import re
import unicodedata
from pathlib import Path

from openpyxl import load_workbook

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import DATA_PROC, REPO  # noqa: E402

XLSX_BASE = DATA_PROC / 'consolidado_base_referencia_final.xlsx'
TURNOS_CSV = DATA_PROC / 'turnos_habla.csv'
CURATION = REPO / 'data/curation'

MIN_PALABRAS_UNIVERSO = 150
# Los deciles extremos llevan mas cupo: es donde la postura hawkish/dovish es visible.
PESOS_DECIL = {1: 3.0, 2: 2.2, 3: 1.5, 4: 1.1, 5: 1.0, 6: 1.0, 7: 1.1, 8: 1.5, 9: 2.2, 10: 3.0}
SEMILLA = 20260911
UMBRAL_CLASE = 0.50

# Léxico ponderado. Sólo locuciones multitermino: las palabras sueltas
# ("subir", "inflacion") disparan falsos positivos en este corpus.
HAWKISH = [
    (3.0, 'subir la tasa'), (3.0, 'aumento de la tasa'), (3.0, 'incremento de la tasa'),
    (3.0, 'alza de la tasa'), (3.0, 'subida de la tasa'), (3.0, 'retirar el estimulo'),
    (3.0, 'retiro del estimulo'), (3.0, 'retiro gradual del estimulo'),
    (3.0, 'presiones inflacionarias'), (3.0, 'presion inflacionaria'),
    (3.0, 'sobrecalentamiento'), (3.0, 'sobrecalentada'),
    (3.0, 'expectativas desancladas'), (3.0, 'desanclaje de las expectativas'),
    (3.0, 'por encima de la meta'), (3.0, 'por sobre la meta'), (2.0, 'sobre la meta'),
    (3.0, 'por encima del 3'), (3.0, 'exceso de demanda'), (3.0, 'sobrepasar la meta'),
    (3.0, 'riesgo al alza de la inflacion'), (3.0, 'riesgos al alza de la inflacion'),
    (4.0, 'holguras se han reducido'), (4.0, 'holguras se reducen'),
    (4.0, 'holguras han disminuido'), (4.0, 'menores holguras'),
    (4.0, 'capacidad ociosa se ha reducido'), (4.0, 'capacidad ociosa se reduce'),
    (4.0, 'capacidad ociosa se ha ido reduciendo'),
    (3.0, 'crecimiento por encima del potencial'), (3.0, 'por sobre el potencial'),
    (3.0, 'brecha positiva'), (3.0, 'brecha de producto positiva'),
    (2.0, 'politica restrictiva'), (2.0, 'sesgo restrictivo'), (2.0, 'endurecer la politica'),
    (2.0, 'retirar el impulso'), (2.0, 'retiro del impulso'), (2.0, 'normalizacion de la politica'),
    (2.0, 'inflacion mas alta'), (2.0, 'inflacion elevada'), (2.0, 'alza de la inflacion'),
    (2.0, 'mayor inflacion'), (2.0, 'inflacion subyacente alta'),
    (2.0, 'expectativas al alza'), (2.0, 'expectativas por sobre la meta'),
    (2.0, 'anclaje de las expectativas'), (2.0, 'riesgo inflacionario'),
    (2.0, 'riesgos inflacionarios'), (2.0, 'presiones de costos'),
    (2.0, 'presiones de demanda'), (2.0, 'tipo de cambio real bajo'),
    (2.0, 'demanda interna robusta'), (2.0, 'demanda interna dinamica'),
    (2.0, 'mercado laboral estrecho'), (2.0, 'mercado del trabajo estrecho'),
    (2.0, 'costos laborales'), (2.0, 'costos unitarios del trabajo'),
    (2.0, 'menor holgura'), (2.0, 'holguras acotadas'), (2.0, 'capacidad ociosa reducida'),
    (2.0, 'restringir la demanda'), (2.0, 'enfriar la economia'),
    (1.0, 'inflacion subyacente'), (1.0, 'inflacion no transable'),
    (1.0, 'inflacion de costos'), (1.0, 'consumo dinamico'), (1.0, 'consumo robusto'),
    (1.0, 'segunda vuelta'), (1.0, 'efectos de segunda vuelta'),
    (1.0, 'traspaso a precios'), (1.0, 'pass through'),
]

DOVISH = [
    (3.0, 'bajar la tasa'), (3.0, 'reduccion de la tasa'), (3.0, 'recorte de la tasa'),
    (3.0, 'reducir la tasa'), (3.0, 'disminucion de la tasa'), (3.0, 'relajar la politica'),
    (3.0, 'estimulo monetario adicional'), (3.0, 'mas estimulo'), (3.0, 'mayor estimulo'),
    (3.0, 'inflacion bajo la meta'), (3.0, 'por debajo de la meta'),
    (3.0, 'por debajo del 3'), (3.0, 'inflacion contenida'), (3.0, 'inflacion baja'),
    (3.0, 'holguras de capacidad'), (3.0, 'holgura de capacidad'),
    (3.0, 'capacidad ociosa'), (3.0, 'capacidad instalada sin uso'),
    (3.0, 'brecha negativa'), (3.0, 'brecha de producto negativa'),
    (3.0, 'debilidad de la demanda'), (3.0, 'demanda debil'), (3.0, 'demanda deprimida'),
    (3.0, 'riesgo a la baja de la inflacion'), (3.0, 'riesgos a la baja de la inflacion'),
    (3.0, 'inflacion transitoria'), (3.0, 'caracter transitorio'), (3.0, 'shock transitorio'),
    (3.0, 'convergencia a la meta'), (3.0, 'convergencia hacia la meta'),
    (3.0, 'inflacion cedera'), (3.0, 'la inflacion ceda'), (3.0, 'cedera hacia la meta'),
    (2.0, 'politica expansiva adicional'), (2.0, 'sesgo expansivo'), (2.0, 'impulso expansivo adicional'),
    (2.0, 'flexibilizar'), (2.0, 'relajamiento'), (2.0, 'menor presion inflacionaria'),
    (2.0, 'sin presiones inflacionarias'), (2.0, 'presiones inflacionarias acotadas'),
    (2.0, 'crecimiento por debajo del potencial'), (2.0, 'por debajo del potencial'),
    (2.0, 'desaceleracion'), (2.0, 'desaceleramiento'), (2.0, 'menor crecimiento'),
    (2.0, 'menor dinamismo'), (2.0, 'debil dinamismo'), (2.0, 'recesion'),
    (2.0, 'desempleo al alza'), (2.0, 'aumento del desempleo'), (2.0, 'mercado laboral holgado'),
    (2.0, 'efectos de segunda vuelta acotados'), (2.0, 'ancladas en torno a la meta'),
    (2.0, 'expectativas ancladas'), (2.0, 'expectativas en torno a la meta'),
    (2.0, 'inflacion moderada'), (2.0, 'inflacion a la baja'), (2.0, 'inflacion convergera'),
    (2.0, 'tipo de cambio alto'), (1.0, 'crisis financiera'), (1.0, 'crisis internacional'),
    (1.0, 'holgura'), (1.0, 'crecimiento bajo'),
    (1.0, 'inflacion baja y estable'), (1.0, 'escenario benigno'), (1.0, 'riesgo deflacionario'),
]

NEGACIONES = ('no', 'sin', 'nunca', 'tampoco', 'poco', 'ningun', 'ninguna', 'jamás', 'jamas')


def normalizar(texto):
    """Minusculas y sin tildes; conserva el resto del texto intacto."""
    t = str(texto).lower()
    t = ''.join(c for c in unicodedata.normalize('NFD', t)
                if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', t).strip()


def _pesos_negados(texto_norm, frase, peso):
    """Descuenta la locucion si una negacion la precede en hasta 3 palabras."""
    total = 0.0
    inicio = 0
    while True:
        pos = texto_norm.find(frase, inicio)
        if pos < 0:
            return total
        previas = texto_norm[:pos].split()[-3:]
        if any(p in NEGACIONES for p in previas):
            total -= peso * 0.5
        else:
            total += peso
        inicio = pos + len(frase)


def puntuar_lexico(texto):
    """Devuelve puntaje hawkish/dovish en [-1, 1] y las locuciones que lo explican."""
    t = normalizar(texto)
    hawk = []
    dove = []
    for peso, frase in HAWKISH:
        w = _pesos_negados(t, frase, peso)
        if w:
            hawk.append((frase, round(w, 2)))
    for peso, frase in DOVISH:
        w = _pesos_negados(t, frase, peso)
        if w:
            dove.append((frase, round(w, 2)))
    ph = sum(w for _, w in hawk)
    pd = -sum(w for _, w in dove)
    # Direccion (balance hawkish/dovish) atenuada por la intensidad de la evidencia:
    # un solo acierto debil no debe saturar en +-1.
    denom = ph + abs(pd)
    balance = (ph + pd) / denom if denom else 0.0
    intensidad = denom / (denom + 4.0)
    score = balance * intensidad
    palabras = len(t.split()) or 1
    return {
        'score': round(score, 4),
        'peso_hawkish': round(ph, 2),
        'peso_dovish': round(abs(pd), 2),
        'hits_por_100_palabras': round((len(hawk) + len(dove)) / palabras * 100, 2),
        'hits_hawkish': hawk,
        'hits_dovish': dove,
    }


def clase(score):
    if score >= UMBRAL_CLASE:
        return 'HAWKISH'
    if score <= -UMBRAL_CLASE:
        return 'DOVISH'
    return 'NEUTRAL'


def grupo_actor(rol):
    """CONSEJO vota; STAFF expone; HACIENDA asiste sin voto.

    Presidente y Vicepresidente del Banco Central son miembros del Consejo: agruparlos
    con las gerencias mezclaría a quien decide con quien informa. Gerente General y
    Subgerente General no votan y quedan en STAFF.
    """
    r = str(rol or '')
    if ('Presidente del Banco Central' in r or 'Vicepresidente del Banco Central' in r
            or 'Consejo' in r or 'Consejero' in r or 'Consejera' in r):
        return 'CONSEJO'
    if 'Ministro' in r or 'Ministra' in r or 'Subsecretario' in r or 'Asesor del Minist' in r:
        return 'HACIENDA'
    return 'STAFF'


def cargar_turnos(xlsx=XLSX_BASE, turnos_csv=TURNOS_CSV):
    """Une cada turno con su texto y valida el join contra Numero_Filas y Palabras."""
    wb = load_workbook(str(xlsx), read_only=True)
    ws = wb['Consolidado']
    filas = ws.iter_rows(values_only=True)
    hdr = next(filas)
    ix = {h: k for k, h in enumerate(hdr)}
    por_id, rol_por_id = {}, {}
    for r in filas:
        por_id[int(r[ix['ID']])] = (str(r[ix['Texto']] or ''), r[ix['ID_Turno']])
        rol_por_id[int(r[ix['ID']])] = r[ix['Rol_Final']]
    wb.close()

    salida, errores = [], []
    with open(turnos_csv, newline='', encoding='utf-8-sig') as f:
        for t in csv.DictReader(f):
            a, b = int(t['ID_Desde']), int(t['ID_Hasta'])
            ids = [k for k in range(a, b + 1)
                   if k in por_id and por_id[k][1] == t['ID_Turno']]
            texto = ' '.join(por_id[k][0] for k in ids)
            if len(ids) != int(t['Numero_Filas']) or len(texto.split()) != int(t['Palabras']):
                errores.append(t['ID_Turno'])
                continue
            fecha = t['Fecha'][:10]
            salida.append({
                'ID_Turno': t['ID_Turno'],
                'Fecha': fecha,
                'Anio': fecha[:4],
                'Actor_Final': t['Actor_Final'],
                'Rol_Final': rol_por_id.get(ids[0], ''),
                'Naturaleza_Turno': t['Naturaleza_Turno'],
                'Palabras': int(t['Palabras']),
                'Numero_Filas': int(t['Numero_Filas']),
                'ID_Desde': a,
                'ID_Hasta': b,
                'Texto': texto,
                'SHA256_Texto': hashlib.sha256(texto.encode('utf-8')).hexdigest(),
            })
    if errores:
        raise RuntimeError(f'join turno/texto inconsistente en {len(errores)} turnos: {errores[:5]}')
    return salida


def universo(turnos, min_palabras=MIN_PALABRAS_UNIVERSO):
    return [t for t in turnos
            if t['Naturaleza_Turno'] == 'INTERVENCION' and t['Palabras'] >= min_palabras]


def _reparto(pesos, total):
    """Reparto proporcional por resto mayor; garantiza que sume exactamente `total`."""
    base = sum(pesos.values())
    crudo = {k: v / base * total for k, v in pesos.items()}
    entero = {k: int(v) for k, v in crudo.items()}
    resto = total - sum(entero.values())
    for k in sorted(crudo, key=lambda k: (-(crudo[k] - entero[k]), k)):
        if resto <= 0:
            break
        entero[k] += 1
        resto -= 1
    return {k: min(v, pesos[k]) for k, v in entero.items()}


def muestra(turnos, n=500, semilla=SEMILLA, min_palabras=MIN_PALABRAS_UNIVERSO,
            forzar=()):
    """Sorteo por decil de puntaje lexico y, dentro del decil, por año x grupo de actor.

    No es un muestreo proporcional a la poblacion: los deciles se reparten parejo para
    que las 500 etiquetas cubran todo el espectro hawkish/dovish. Consecuencia: las
    etiquetas sirven para entrenar un clasificador, no para estimar la prevalencia de
    cada postura en el corpus (para eso habria que reponderar por decil).
    """
    pool = universo(turnos, min_palabras)
    for t in pool:
        t['Lex'] = puntuar_lexico(t['Texto'])
        t['Grupo_Actor'] = grupo_actor(t['Rol_Final'])

    orden = sorted(pool, key=lambda t: (t['Lex']['score'], t['ID_Turno']))
    k = len(orden)
    deciles = {}
    for j, t in enumerate(orden):
        d = min(9, j * 10 // k) + 1
        t['Decile_Lex'] = d
        deciles.setdefault(d, []).append(t)

    forzar = {f for f in forzar if f in {t['ID_Turno'] for t in pool}}
    obligadas = [t for t in pool if t['ID_Turno'] in forzar]
    resto = [t for t in pool if t['ID_Turno'] not in forzar]
    deciles_resto = {}
    for t in resto:
        deciles_resto.setdefault(t['Decile_Lex'], []).append(t)
    cupos = _reparto({d: len(v) * PESOS_DECIL[d] for d, v in deciles_resto.items()},
                     max(min(n, len(pool)) - len(obligadas), 0))
    deciles = deciles_resto
    rng = random.Random(semilla)
    elegidos = list(obligadas)
    for d in sorted(deciles):
        sub = {}
        for t in deciles[d]:
            sub.setdefault((t['Anio'], t['Grupo_Actor']), []).append(t)
        reparto = _reparto({kk: len(vv) for kk, vv in sub.items()}, cupos[d])
        for kk in sorted(sub):
            if reparto.get(kk, 0):
                elegidos.extend(rng.sample(sorted(sub[kk], key=lambda t: t['ID_Turno']),
                                           reparto[kk]))
    elegidos.sort(key=lambda t: t['ID_Turno'])
    for i, t in enumerate(elegidos, start=1):
        t['Lote'] = i
        t['Forzada'] = t['ID_Turno'] in forzar
        t['Estrato'] = f"D{t['Decile_Lex']}|{t['Anio']}|{t['Grupo_Actor']}"
    return elegidos, pool


CAMPOS_MUESTRA = [
    'Lote', 'ID_Turno', 'Fecha', 'Anio', 'Actor_Final', 'Rol_Final', 'Grupo_Actor',
    'Estrato', 'Decile_Lex', 'Etiqueta_Previa', 'Palabras', 'Numero_Filas', 'ID_Desde', 'ID_Hasta',
    'Lex_Score', 'Lex_Clase', 'Lex_Peso_Hawkish', 'Lex_Peso_Dovish',
    'Lex_Hits_por_100', 'Lex_Evidencia', 'SHA256_Texto',
    'HD_Score_Oro', 'HD_Clase_Oro', 'Evidencia_Oro', 'Chars_Leidos', 'Texto',
]


def escribir_muestra(ruta, elegidos):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_MUESTRA)
        w.writeheader()
        for t in elegidos:
            lex = t['Lex']
            evidencia = '; '.join(
                [f'H:{frase}' for frase, _ in lex['hits_hawkish']] +
                [f'D:{frase}' for frase, _ in lex['hits_dovish']])
            w.writerow({
                'Lote': t['Lote'], 'ID_Turno': t['ID_Turno'], 'Fecha': t['Fecha'],
                'Anio': t['Anio'], 'Actor_Final': t['Actor_Final'], 'Rol_Final': t['Rol_Final'],
                'Grupo_Actor': t['Grupo_Actor'], 'Estrato': t['Estrato'],
                'Decile_Lex': t['Decile_Lex'],
                'Etiqueta_Previa': 'SI' if t.get('Forzada') else 'NO',
                'Palabras': t['Palabras'], 'Numero_Filas': t['Numero_Filas'],
                'ID_Desde': t['ID_Desde'], 'ID_Hasta': t['ID_Hasta'],
                'Lex_Score': lex['score'], 'Lex_Clase': clase(lex['score']),
                'Lex_Peso_Hawkish': lex['peso_hawkish'], 'Lex_Peso_Dovish': lex['peso_dovish'],
                'Lex_Hits_por_100': lex['hits_por_100_palabras'],
                'Lex_Evidencia': evidencia[:400], 'SHA256_Texto': t['SHA256_Texto'],
                'HD_Score_Oro': '', 'HD_Clase_Oro': '', 'Evidencia_Oro': '',
                'Chars_Leidos': '', 'Texto': t['Texto'],
            })
    return ruta


def resumen(pool, elegidos):
    from collections import Counter

    def cuenta(items):
        return dict(Counter(clase(t['Lex']['score']) for t in items))
    return {
        'turnos_totales_corpus': None,
        'universo_etiquetable': len(pool),
        'muestra': len(elegidos),
        'clases_lexico_universo': cuenta(pool),
        'clases_lexico_muestra': cuenta(elegidos),
        'estratos_muestra': len({t['Estrato'] for t in elegidos}),
        'deciles_lexico_muestra': dict(sorted(Counter(t['Decile_Lex'] for t in elegidos).items())),
        'incluidas_por_etiqueta_previa': sum(1 for t in elegidos if t.get('Forzada')),
        'palabras_min': min(t['Palabras'] for t in elegidos),
        'palabras_max': max(t['Palabras'] for t in elegidos),
        'palabras_media': round(sum(t['Palabras'] for t in elegidos) / len(elegidos), 1),
        'semilla': SEMILLA,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--etapa', choices=['muestra'], default='muestra')
    ap.add_argument('--n', type=int, default=500)
    ap.add_argument('--salida', default=str(CURATION / 'muestra_500_hawkish_dovish.csv'))
    ap.add_argument('--forzar-etiquetas',
                    default=str(CURATION / 'hawkish_dovish_etiquetas_v1.json'),
                    help='JSON de etiquetas cuyas intervenciones entran sí o sí en la muestra')
    ap.add_argument('--resumen', default=str(CURATION / 'muestra_500_hawkish_dovish_resumen.json'))
    args = ap.parse_args()

    turnos = cargar_turnos()
    if args.etapa == 'muestra':
        forzar = []
        ruta_forzar = Path(args.forzar_etiquetas)
        if ruta_forzar.exists():
            paquete = json.loads(ruta_forzar.read_text(encoding='utf-8'))
            forzar = [e['ID_Turno'] for e in paquete['Etiquetas']]
        elegidos, pool = muestra(turnos, n=args.n, forzar=forzar)
        escribir_muestra(args.salida, elegidos)
        r = resumen(pool, elegidos)
        r['turnos_totales_corpus'] = len(turnos)
        Path(args.resumen).write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(r, ensure_ascii=False, indent=2))
        print('escrito:', args.salida)


if __name__ == '__main__':
    main()
