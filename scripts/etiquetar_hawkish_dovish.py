"""Valida y fusiona las etiquetas oro hawkish/dovish con la muestra sorteada.

Cada etiqueta se verifica antes de aceptarse: el Lote existe, el SHA256 del texto
coincide con el de la muestra, la evidencia citada aparece literalmente en el
texto y la clase es coherente con el puntaje. ``Chars_Leidos`` y ``Cobertura``
no se declaran a mano: se recalculan con la regla de lectura de la rúbrica.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hawkish_dovish import (CURATION, clase, normalizar)  # noqa: E402

MUESTRA = CURATION / 'muestra_500_hawkish_dovish.csv'
ETIQUETAS = CURATION / 'hawkish_dovish_etiquetas_v1.json'

LECTURA_CABEZA = 520
LECTURA_COLA = 280


def chars_leidos(texto):
    """Caracteres efectivamente leidos con la ventana de la rúbrica."""
    t = ' '.join(str(texto).split())
    if len(t) <= LECTURA_CABEZA + LECTURA_COLA + 40:
        return len(t)
    return LECTURA_CABEZA + LECTURA_COLA


def cargar_muestra(ruta=MUESTRA):
    with open(ruta, newline='', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        return list(lector), lector.fieldnames


def validar(etiquetas, muestra):
    """Devuelve (validas, errores, fuera_de_muestra).

    Una etiqueta cuyo ID_Turno no está en el sorteo vigente no es un error: el sorteo
    es una selección reproducible y puede cambiar; la etiqueta sigue siendo válida para
    entrenar siempre que su texto se pueda recuperar del consolidado.
    """
    por_id = {r['ID_Turno']: r for r in muestra}
    vistos = Counter()
    validas, errores, fuera = [], [], []
    for e in etiquetas['Etiquetas']:
        clave = e.get('ID_Turno')
        vistos[clave] += 1
        if clave not in por_id:
            fuera.append(clave)
            continue
        fila = por_id[clave]
        lote = int(fila['Lote'])
        if hashlib.sha256(fila['Texto'].encode('utf-8')).hexdigest() != fila['SHA256_Texto']:
            errores.append(f'{clave}: SHA256 del texto no coincide con el declarado')
        score = float(e['HD_Score'])
        if not -1.0 <= score <= 1.0:
            errores.append(f'{clave}: puntaje {score} fuera de [-1, 1]')
        if clase(score) != e['HD_Clase']:
            errores.append(f"{clave}: clase {e['HD_Clase']} incoherente con puntaje {score} "
                           f'(la rúbrica da {clase(score)})')
        evidencia = ' '.join(str(e.get('Evidencia', '')).split())
        if not evidencia:
            errores.append(f'{clave}: sin evidencia citada')
        elif normalizar(evidencia) not in normalizar(fila['Texto']):
            errores.append(f'{clave}: la evidencia no aparece en el texto')
        leidos = chars_leidos(fila['Texto'])
        validas.append({
            'Lote': lote, 'ID_Turno': fila['ID_Turno'],
            'HD_Score_Oro': score, 'HD_Clase_Oro': e['HD_Clase'],
            'Evidencia_Oro': evidencia, 'Chars_Leidos': leidos,
            'Cobertura': round(leidos / max(len(' '.join(fila['Texto'].split())), 1), 3),
        })
    repetidos = [k for k, v in vistos.items() if v > 1]
    if repetidos:
        errores.append(f'ID_Turno duplicados: {sorted(repetidos)}')
    return validas, errores, sorted(fuera)


def fusionar(muestra, validas, fieldnames):
    por_id = {v['ID_Turno']: v for v in validas}
    for fila in muestra:
        v = por_id.get(fila['ID_Turno'])
        for k in ('HD_Score_Oro', 'HD_Clase_Oro', 'Evidencia_Oro', 'Chars_Leidos'):
            fila[k] = v[k] if v else ''
    if 'Cobertura' not in fieldnames:
        fieldnames = fieldnames + ['Cobertura']
    for fila in muestra:
        v = por_id.get(fila['ID_Turno'])
        fila['Cobertura'] = v['Cobertura'] if v else ''
    return muestra, fieldnames


def escribir(ruta, filas, fieldnames):
    with open(ruta, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(filas)
    return ruta


def acuerdo(validas, muestra):
    """Concordancia entre la etiqueta oro y el baseline léxico, y distribución."""
    por_id = {r['ID_Turno']: r for r in muestra}
    oro = [v['HD_Clase_Oro'] for v in validas]
    lex = [por_id[v['ID_Turno']]['Lex_Clase'] for v in validas]
    clases = ['HAWKISH', 'NEUTRAL', 'DOVISH']
    matriz = {a: {b: 0 for b in clases} for a in clases}
    for o, l in zip(oro, lex):
        matriz[o][l] += 1
    exactas = sum(1 for o, l in zip(oro, lex) if o == l)
    puntajes = [float(v['HD_Score_Oro']) for v in validas]
    lex_scores = [float(por_id[v['ID_Turno']]['Lex_Score']) for v in validas]
    mae = sum(abs(a - b) for a, b in zip(puntajes, lex_scores)) / len(puntajes)
    return {
        'etiquetadas': len(validas),
        'pendientes_en_muestra': len(muestra) - len(validas),
        'distribucion_oro': dict(Counter(oro)),
        'distribucion_lexico_sobre_etiquetadas': dict(Counter(lex)),
        'coincidencias_clase': exactas,
        'tasa_coincidencia': round(exactas / len(validas), 3),
        'mae_puntaje_oro_vs_lexico': round(mae, 3),
        'matriz_oro_filas_x_lexico_columnas': matriz,
        'puntaje_medio_oro': round(sum(puntajes) / len(puntajes), 3),
        'cobertura_media_lectura': round(
            sum(v['Cobertura'] for v in validas) / len(validas), 3),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--muestra', default=str(MUESTRA))
    ap.add_argument('--etiquetas', default=str(ETIQUETAS))
    ap.add_argument('--resumen', default=str(CURATION / 'hawkish_dovish_etiquetas_resumen.json'))
    ap.add_argument('--estricto', action='store_true',
                    help='falla con código 1 si alguna etiqueta no valida')
    args = ap.parse_args()

    etiquetas = json.loads(Path(args.etiquetas).read_text(encoding='utf-8'))
    muestra, fieldnames = cargar_muestra(args.muestra)
    validas, errores, fuera = validar(etiquetas, muestra)
    muestra, fieldnames = fusionar(muestra, validas, fieldnames)
    escribir(args.muestra, muestra, fieldnames)

    resumen = acuerdo(validas, muestra)
    resumen['fuera_de_muestra_actual'] = fuera
    resumen['errores'] = errores
    resumen['sha256_muestra'] = hashlib.sha256(
        Path(args.muestra).read_bytes()).hexdigest()
    Path(args.resumen).write_text(json.dumps(resumen, ensure_ascii=False, indent=2),
                                  encoding='utf-8')
    print(json.dumps({k: v for k, v in resumen.items() if k != 'matriz_oro_filas_x_lexico_columnas'},
                     ensure_ascii=False, indent=2))
    if errores and args.estricto:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
