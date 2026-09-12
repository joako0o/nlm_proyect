"""Gate v8: los cuatro cortes del lote10 sobre la entrega procedimental v7.

El esperado se deriva de la entrega v7 firmada y del registro lote10, NO del
constructor. Compara TODAS las filas, TODOS los campos y TODOS los miembros de
cada grupo; la única diferencia autorizada es la resegmentación de cuatro padres.

Este archivo es nuevo a propósito. ``compare_functional_v7.py`` está fijado por
hash en el manifiesto de la entrega v7 y exige cardinalidad idéntica (9.723),
porque eso era lo que v7 debía probar: que el refinamiento funcional no agregaba
filas. v8 agrega una, legítimamente, así que necesita su propio gate en vez de
reescribir el anterior.

Lo que se verifica, sin excepciones globales:

1. Cardinalidad: 9.723 -> 9.724, exactamente una fila nueva.
2. Todo padre ajeno a los cuatro revisados sale byte a byte igual en todos sus
   campos; sólo el ``ID`` posicional se corre en +1 después del punto de inserción.
3. En los cuatro padres revisados no se inventa ni se pierde texto: la
   concatenación de los segmentos es idéntica a la de v7.
4. El tramo revisado existe como segmento propio, con el actor del registro y el
   texto exacto del intervalo ``[Inicio, Fin]`` del padre.
5. Membresía de grupos idéntica fuera de las cuatro sesiones tocadas.
6. Las tres reservas (780, 2661, 5252) siguen abiertas y con los mismos motivos.
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_base_referencia as builder  # noqa: E402
from diagnosticar_finales import read_rows  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/releases/continuidad_procedimental_v7/consolidado_base_referencia_final.xlsx'
BASE_SHA = 'd0b64842cd756df4c50d2960d9bbf01c4c45e5df28609d7b612c5d666593da75'
LOTE10 = ROOT / 'data/curation/revisiones_hablantes_lote10.json'
PADRES = (657, 1564, 1995, 2960)
FILAS_V7 = 9723
RESERVAS = (780, 2661, 5252)
# El ID es un contador posicional: la fila nueva corre en +1 a todas las siguientes.
CAMPOS_POSICIONALES = ('ID',)
# Se renumeran dentro de una sesión con corte; la estructura se verifica aparte.
RENOMBRABLES = ('ID_Turno',)


def sin_posicionales(fila):
    return {k: v for k, v in fila.items() if k not in CAMPOS_POSICIONALES}


def por_padre(filas):
    grupos = collections.OrderedDict()
    for fila in filas:
        grupos.setdefault(int(fila['ID_Padre']), []).append(fila)
    return grupos


def miembros(filas):
    grupos = collections.defaultdict(list)
    for fila in filas:
        grupos[fila['ID_Turno']].append(fila['ID_Intervencion'])
    return dict(grupos)


SIN_ESPACIOS = lambda t: ''.join(t.split())


def textos_padre():
    """Texto fuente de cada padre, no la concatenación de segmentos ya cortados.

    Los segmentos de una entrega vienen recortados en la frontera, así que
    concatenarlos no devuelve el texto original y los offsets del registro no
    calzarían. Los offsets del lote10 son sobre el texto fuente.
    """
    wb = builder.openpyxl.load_workbook(builder.SRC, data_only=True, read_only=True)
    filas = list(wb['Consolidado'].iter_rows(values_only=True))[1:]
    wb.close()
    return {int(r[0]): str(r[5]) for r in filas}


def revisar_corte(padre, antes, despues, entrada, texto_padre):
    """Devuelve el linaje del padre y valida que el corte sea el del registro."""
    texto_antes = ''.join(f['Texto'] or '' for f in antes)
    texto_despues = ''.join(f['Texto'] or '' for f in despues)
    # Ni v7 ni v8 pueden inventar o perder texto respecto de la fuente. Se compara sin
    # espacios porque el constructor recorta el que separaba los tramos al partir.
    for etiqueta, texto in (('v7', texto_antes), ('v8', texto_despues)):
        if SIN_ESPACIOS(texto) != SIN_ESPACIOS(texto_padre):
            raise ValueError(f'padre {padre}: la entrega {etiqueta} no reproduce el texto fuente '
                             f'({len(texto)} caracteres contra {len(texto_padre)})')
    if not 1 <= entrada['Inicio'] <= len(texto_padre) or \
            not entrada['Inicio'] <= entrada['Fin'] <= len(texto_padre) + 1:
        raise ValueError(f'padre {padre}: el intervalo [{entrada["Inicio"]}, {entrada["Fin"]}] '
                         f'no cabe en un texto de {len(texto_padre)} caracteres')
    tramo = texto_padre[entrada['Inicio'] - 1:entrada['Fin']].strip()
    if not tramo:
        raise ValueError(f'padre {padre}: el intervalo revisado está vacío')
    dueno = [f for f in despues if (f['Texto'] or '').strip() == tramo]
    if len(dueno) != 1:
        raise ValueError(f'padre {padre}: el tramo revisado no aparece como un único segmento '
                         f'(aparece {len(dueno)} veces)')
    if dueno[0]['Actor_Final'] != entrada['Actor']:
        raise ValueError(f'padre {padre}: el tramo revisado quedó en '
                         f'{dueno[0]["Actor_Final"]!r}, el registro dice {entrada["Actor"]!r}')
    if dueno[0]['Texto'] == texto_despues:
        raise ValueError(f'padre {padre}: el corte no partió nada')
    return [dict(ID_Padre=padre, ID_Nuevo=f['ID_Intervencion'], Actor_Final=f['Actor_Final'],
                 Largo=len(f['Texto'] or ''),
                 Es_Tramo_Revisado='SI' if f is dueno[0] else 'NO',
                 Inicio_En_Padre=entrada['Inicio'] if f is dueno[0] else '',
                 Fin_En_Padre=entrada['Fin'] if f is dueno[0] else '',
                 SHA256_Texto=hashlib.sha256((f['Texto'] or '').encode()).hexdigest())
            for f in despues]


def compare(before, after, revisiones):
    if len(before) != FILAS_V7:
        raise ValueError(f'La entrega v7 tiene {len(before)} filas, se esperaban {FILAS_V7}')
    if len(after) != FILAS_V7 + 1:
        raise ValueError(f'v8 debe tener exactamente una fila más que v7: '
                         f'{len(after)} vs {FILAS_V7} + 1')

    antes, despues = por_padre(before), por_padre(after)
    if set(antes) != set(despues):
        raise ValueError('El conjunto de padres cambió')

    fuentes = textos_padre()
    sesiones_corte = {'RPM-2006-05-11', 'RPM-2007-11-13', 'RPM-2008-08-14', 'RPM-2010-02-11'}
    linaje = []
    tocadas = set()
    for padre in antes:
        if padre in PADRES:
            if padre not in revisiones:
                raise ValueError(f'El padre {padre} cambió sin revisión registrada')
            linaje += revisar_corte(padre, antes[padre], despues[padre],
                                    revisiones[padre], fuentes[padre])
            tocadas.update(f['ID_Intervencion'] for f in antes[padre] + despues[padre])
            continue
        if len(antes[padre]) != len(despues[padre]):
            raise ValueError(f'padre {padre}: cambió el número de segmentos sin revisión')
        for a, b in zip(antes[padre], despues[padre]):
            sesion = a['ID_Intervencion'].rsplit(':', 2)[0]
            for k in set(a) | set(b):
                if k in CAMPOS_POSICIONALES:
                    continue
                # Dentro de una sesión con corte el contador de turnos se renumera; la
                # estructura de grupos se verifica aparte, contra esa renumeración.
                if k in RENOMBRABLES and sesion in sesiones_corte:
                    continue
                if a.get(k) != b.get(k):
                    raise ValueError(f'padre {padre} ({a["ID_Intervencion"]}): '
                                     f'cambio no autorizado en {k}: '
                                     f'{a.get(k)!r} -> {b.get(k)!r}')
    if set(revisiones) - set(PADRES):
        raise ValueError(f'Revisiones sin padre cambiado: {sorted(set(revisiones) - set(PADRES))}')

    # El ID es posicional: o se conserva, o se corre exactamente en +1.
    id_v7 = {f['ID_Intervencion']: f['ID'] for f in before}
    corridas = []
    nuevas = []
    for fila in after:
        viejo = id_v7.get(fila['ID_Intervencion'])
        if viejo is None:
            nuevas.append(fila['ID_Intervencion'])
        elif fila['ID'] not in (viejo, viejo + 1):
            raise ValueError(f'{fila["ID_Intervencion"]}: ID pasó de {viejo} a {fila["ID"]}, '
                             'sólo se admite conservarlo o correrlo en +1')
        elif fila['ID'] == viejo + 1:
            corridas.append(fila['ID_Intervencion'])
    if len(nuevas) != 1:
        raise ValueError(f'Se esperaban 1 fila nueva y hay {len(nuevas)}: {nuevas}')
    if [f['ID'] for f in after] != list(range(1, len(after) + 1)):
        raise ValueError('El ID dejó de ser una secuencia contigua desde 1')
    if corridas and min(id_v7[i] for i in corridas) <= max(
            id_v7[i] for i in id_v7 if i not in corridas and i not in nuevas):
        raise ValueError('El corrimiento del ID no es un sufijo: se colaron filas del medio')

    # Membresía de grupos: la estructura tiene que conservarse exactamente, aunque el
    # número de turno se renumere dentro de la sesión cortada. Se reconstruye el mapa
    # viejo->nuevo y se exige que sea biyectivo y que cada grupo conserve sus miembros.
    por_iid = {f['ID_Intervencion']: f for f in after}
    mapa = {}
    for f in before:
        viejo, nuevo = f['ID_Turno'], por_iid[f['ID_Intervencion']]['ID_Turno']
        if viejo in mapa and mapa[viejo] != nuevo:
            raise ValueError(f'un grupo se partió: {viejo} va a {mapa[viejo]} y a {nuevo}')
        mapa[viejo] = nuevo
    if len(set(mapa.values())) != len(mapa):
        raise ValueError('dos grupos se fusionaron al renumerar los turnos')
    m_antes, m_despues = miembros(before), miembros(after)
    for viejo, miembros_viejos in m_antes.items():
        if m_despues.get(mapa[viejo]) != miembros_viejos:
            raise ValueError(f'grupo {viejo} -> {mapa[viejo]} cambió de miembros: '
                             f'{miembros_viejos} -> {m_despues.get(mapa[viejo])}')
    extras = sorted(set(m_despues) - set(mapa.values()))
    if len(extras) != 1:
        raise ValueError(f'se esperaban 1 grupo nuevo y hay {len(extras)}: {extras}')

    # Las tres reservas siguen abiertas y con los mismos motivos.
    def reserva(filas, padre):
        return sorted((f['ID_Intervencion'], f['Motivos_Revision'] or '')
                      for f in filas if int(f['ID_Padre']) == padre)

    reservas = {}
    for padre in RESERVAS:
        antes_r, despues_r = reserva(before, padre), reserva(after, padre)
        if antes_r != despues_r:
            raise ValueError(f'La reserva {padre} cambió: {antes_r} -> {despues_r}')
        if not despues_r:
            raise ValueError(f'La reserva {padre} desapareció')
        reservas[str(padre)] = len(despues_r)

    return dict(Perfil='procedimental-v8', Baseline='procedimental-v7', Pasa=True,
                Filas_Antes=len(before), Filas_Despues=len(after), Filas_Nuevas=nuevas,
                Padres_Resegmentados=sorted(PADRES),
                Cortes=len(revisiones),
                IDs_Corridos=len(corridas),
                Grupos_Antes=len(m_antes), Grupos_Despues=len(m_despues),
                Comparacion=('Todas las filas, todos los campos y todos los miembros de cada '
                             'grupo; la única diferencia autorizada es la resegmentación de '
                             'cuatro padres'),
                Alertas_Antes=sum(bool(f['Motivos_Revision']) for f in before),
                Alertas_Despues=sum(bool(f['Motivos_Revision']) for f in after),
                Filas_Alertadas_Antes=sum(bool(f['Motivos_Revision']) for f in before),
                Reservas_Abiertas=reservas,
                SHA256_Baseline=BASE_SHA,
                SHA256_Registro=hashlib.sha256(LOTE10.read_bytes()).hexdigest()), linaje


def revisiones():
    """Las cuatro revisiones del lote10, indexadas por padre."""
    entradas = json.loads(LOTE10.read_text(encoding='utf-8'))
    casos = entradas['Casos'] if isinstance(entradas, dict) and 'Casos' in entradas else entradas
    return {e['ID_Padre']: e for e in casos}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    args = parser.parse_args()
    if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASE_SHA:
        raise ValueError('La entrega procedimental v7 cambió')
    target = args.candidate / BASE.name
    report, linaje = compare(read_rows(BASE), read_rows(target), revisiones())
    report['SHA256_Candidato'] = hashlib.sha256(target.read_bytes()).hexdigest()
    with (args.candidate / 'linaje_cortes_lote10.csv').open('w', encoding='utf-8-sig',
                                                            newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(linaje[0]), quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(linaje)
    (args.candidate / 'comparacion_procedimental_v8.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
