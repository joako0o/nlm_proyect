"""Gate v11: los ocho registros del lote10 sobre la entrega procedimental v10.

El esperado se deriva de la entrega v10 firmada y del registro lote10, NO del
constructor. Compara TODAS las filas, TODOS los campos y TODOS los miembros de
cada grupo; la única diferencia autorizada es la resegmentación de cinco padres.

Este archivo es nuevo a propósito. ``compare_functional_v7.py`` está fijado por
hash en el manifiesto de la entrega v7 y exige cardinalidad idéntica (9.723),
porque eso era lo que v7 debía probar: que el refinamiento funcional no agregaba
filas. v9 agregó dos, v10 una más y v11 quita dos al fusionar una intervención que
estaba partida en tres, así que cada versión necesita su propio gate en vez de
reescribir el anterior, que está fijado por hash en la procedencia de su entrega.

Lo que se verifica, sin excepciones globales:

1. Cardinalidad: 9.723 -> 9.725, exactamente dos filas nuevas.
2. Todo padre ajeno a los cinco revisados sale byte a byte igual en todos sus
   campos; sólo el ``ID`` posicional se corre en +1 después del punto de inserción.
3. En los cinco padres revisados no se inventa ni se pierde texto: la
   concatenación de los segmentos es idéntica a la de v10.
4. El tramo revisado existe como segmento propio, con el actor del registro y el
   texto exacto del intervalo ``[Inicio, Fin]`` del padre.
5. Membresía de grupos idéntica fuera de las cinco sesiones tocadas.
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
BASE = ROOT / 'data/releases/continuidad_procedimental_v10/consolidado_base_referencia_final.xlsx'
BASE_SHA = 'e8b39e7ef4b021419eb4364fc8ed561446264bd3a81dba97e86af1506f08391f'
LOTE10 = ROOT / 'data/curation/revisiones_hablantes_lote10.json'
PADRES = (657, 1564, 1706, 1924, 1925, 1995, 2960, 3062)
# Segmentos que debe tener cada padre revisado. Siete de los ocho son cortes y
# conservan o aumentan el número; el 3062 es el único corte AL REVÉS: la base lo
# partía en tres atribuyendo el tramo del medio a quien no lo dijo, y la revisión
# lo deja en una sola intervención.
SEGMENTOS_ESPERADOS = {657: 2, 1564: 2, 1706: 2, 1924: 2, 1925: 3, 1995: 2,
                       2960: 3, 3062: 1}
FILAS_FUSIONADAS = ["RPM-2010-04-15:3062:2", "RPM-2010-04-15:3062:3"]
FILAS_BASE = 9726
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


def fuente_padre():
    """Texto, fecha y actor de origen de cada padre, para poder segmentar SIN revisión.

    Hace falta porque el baseline v10 ya trae aplicadas siete de las ocho revisiones:
    comparar v11 contra v10 no dice si una revisión hizo algo. Lo que prueba que una
    revisión sirve es compararla contra la segmentación que el detector haría solo.
    """
    wb = builder.openpyxl.load_workbook(builder.SRC, data_only=True, read_only=True)
    filas = list(wb['Consolidado'].iter_rows(values_only=True))[1:]
    wb.close()
    return {int(r[0]): (str(r[5]), builder.to_date_str(r[1]), str(r[2])) for r in filas}


def revisar_corte(padre, antes, despues, entrada, texto_padre, fuente):
    """Devuelve el linaje del padre y valida que el corte sea el del registro."""
    texto_antes = ''.join(f['Texto'] or '' for f in antes)
    texto_despues = ''.join(f['Texto'] or '' for f in despues)
    # Ni v10 ni v11 pueden inventar o perder texto respecto de la fuente. Se compara sin
    # espacios porque el constructor recorta el que separaba los tramos al partir.
    for etiqueta, texto in (('v10', texto_antes), ('v11', texto_despues)):
        if SIN_ESPACIOS(texto) != SIN_ESPACIOS(texto_padre):
            raise ValueError(f'padre {padre}: la entrega {etiqueta} no reproduce el texto fuente '
                             f'({len(texto)} caracteres contra {len(texto_padre)})')
    if not 1 <= entrada['Inicio'] <= len(texto_padre) or \
            not entrada['Inicio'] <= entrada['Fin'] <= len(texto_padre) + 1:
        raise ValueError(f'padre {padre}: el intervalo [{entrada["Inicio"]}, {entrada["Fin"]}] '
                         f'no cabe en un texto de {len(texto_padre)} caracteres')
    tramo = SIN_ESPACIOS(texto_padre[entrada['Inicio'] - 1:entrada['Fin']])
    if not tramo:
        raise ValueError(f'padre {padre}: el intervalo revisado está vacío')
    esperado = SEGMENTOS_ESPERADOS[padre]
    if len(despues) != esperado:
        raise ValueError(f'padre {padre}: {len(despues)} segmentos, se esperaban {esperado}')
    # Invariante que sirve igual para un corte y para una fusión: TODO segmento que se
    # solape con el tramo revisado quedó con el actor del registro. En un corte el tramo
    # es un segmento completo y la comparación es de igualdad; en una fusión el tramo
    # queda contenido en un segmento mayor que antes estaba partido en tres.
    tocados = [f for f in despues
               if SIN_ESPACIOS(f['Texto'] or '')
               and (SIN_ESPACIOS(f['Texto'] or '') in tramo or tramo in SIN_ESPACIOS(f['Texto'] or ''))]
    if not tocados:
        raise ValueError(f'padre {padre}: ningún segmento contiene el tramo revisado')
    for f in tocados:
        if f['Actor_Final'] != entrada['Actor']:
            raise ValueError(f'padre {padre}: el tramo revisado quedó en '
                             f'{f["Actor_Final"]!r}, el registro dice {entrada["Actor"]!r}')
    # Que la revisión sirva se prueba contra el detector solo, no contra v10: el
    # baseline ya trae siete de las ocho revisiones aplicadas.
    texto_fuente, fecha, actor_origen = fuente[padre]
    sin_revision = list(builder.segment_turns(texto_fuente, fecha, actor_origen, review=None))
    if [(t.strip(), a) for t, a, _ in sin_revision] == \
            [(f['Texto'] or '', f['Actor_Final']) for f in despues]:
        raise ValueError(f'padre {padre}: la revisión no cambia nada respecto del detector solo')
    return [dict(ID_Padre=padre, ID_Nuevo=f['ID_Intervencion'], Actor_Final=f['Actor_Final'],
                 Largo=len(f['Texto'] or ''),
                 Es_Tramo_Revisado='SI' if f in tocados else 'NO',
                 Inicio_En_Padre=entrada['Inicio'] if f in tocados else '',
                 Fin_En_Padre=entrada['Fin'] if f in tocados else '',
                 SHA256_Texto=hashlib.sha256((f['Texto'] or '').encode()).hexdigest())
            for f in despues]


def compare(before, after, revisiones):
    if len(before) != FILAS_BASE:
        raise ValueError(f'La entrega v9 tiene {len(before)} filas, se esperaban {FILAS_BASE}')
    if len(after) != FILAS_BASE - 2:
        raise ValueError(f'v11 debe tener exactamente dos filas menos que v10: '
                         f'{len(after)} vs {FILAS_BASE} - 2. La revisión del padre 3062 fusiona '
                         f'tres segmentos en uno: era un corte al revés, la base partía donde no '
                         f'cambia el hablante y atribuía el tramo del medio a otro consejero.')

    antes, despues = por_padre(before), por_padre(after)
    if set(antes) != set(despues):
        raise ValueError('El conjunto de padres cambió')

    fuentes = textos_padre()
    fuente = fuente_padre()
    sesiones_corte = {'RPM-2006-05-11', 'RPM-2007-11-13', 'RPM-2008-03-13',
                  'RPM-2008-07-10', 'RPM-2008-08-14', 'RPM-2010-02-11',
                  'RPM-2010-04-15'}
    linaje = []
    tocadas = set()
    for padre in antes:
        if padre in PADRES:
            if padre not in revisiones:
                raise ValueError(f'El padre {padre} cambió sin revisión registrada')
            linaje += revisar_corte(padre, antes[padre], despues[padre],
                                    revisiones[padre], fuentes[padre], fuente)
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

    # El ID es posicional. v11 no agrega filas: las QUITA. El corrimiento es -2 para
    # toda fila posterior al punto de fusión y 0 para las anteriores. No se fija a
    # mano: se calcula cuántas filas desaparecidas preceden a cada una y se exige
    # exactamente ese desplazamiento, ni uno más ni uno menos.
    id_base = {f['ID_Intervencion']: f['ID'] for f in before}
    presentes = {f['ID_Intervencion'] for f in after}
    nuevas = sorted(i for i in presentes if i not in id_base)
    if nuevas:
        raise ValueError(f'v11 no agrega filas y aparecieron {len(nuevas)} nuevas: {nuevas}')
    borradas = sorted(i for i in id_base if i not in presentes)
    if borradas != sorted(FILAS_FUSIONADAS):
        raise ValueError(f'las filas fusionadas debían ser {sorted(FILAS_FUSIONADAS)} '
                         f'y son {borradas}')
    if [f['ID'] for f in after] != list(range(1, len(after) + 1)):
        raise ValueError('El ID dejó de ser una secuencia contigua desde 1')
    ids_borrados = sorted(id_base[i] for i in borradas)
    corridas = []
    for fila in after:
        viejo = id_base[fila['ID_Intervencion']]
        esperado = viejo - sum(1 for i in ids_borrados if i < viejo)
        if fila['ID'] != esperado:
            raise ValueError(f'{fila["ID_Intervencion"]}: ID pasó de {viejo} a {fila["ID"]}, '
                             f'se esperaba {esperado} (viejo - {viejo - esperado} filas '
                             'fusionadas antes)')
        if fila['ID'] != viejo:
            corridas.append(fila['ID_Intervencion'])
    # El corrimiento tiene que ser un sufijo: ninguna fila anterior a la fusión
    # puede haberse corrido.
    for fila in after:
        viejo = id_base[fila['ID_Intervencion']]
        if fila['ID'] == viejo and viejo > min(ids_borrados):
            raise ValueError(f'{fila["ID_Intervencion"]} conserva su ID aunque hay filas '
                             'fusionadas antes: el corrimiento no es un sufijo')

    # Membresía de grupos: la estructura tiene que conservarse exactamente, aunque el
    # número de turno se renumere dentro de la sesión cortada. Se reconstruye el mapa
    # viejo->nuevo y se exige que sea biyectivo y que cada grupo conserve sus miembros.
    por_iid = {f['ID_Intervencion']: f for f in after}
    mapa = {}
    for f in before:
        if f['ID_Intervencion'] not in presentes:
            continue          # las filas fusionadas no tienen grupo propio en v11
        viejo, nuevo = f['ID_Turno'], por_iid[f['ID_Intervencion']]['ID_Turno']
        if viejo in mapa and mapa[viejo] != nuevo:
            raise ValueError(f'un grupo se partió: {viejo} va a {mapa[viejo]} y a {nuevo}')
        mapa[viejo] = nuevo
    if len(set(mapa.values())) != len(mapa):
        raise ValueError('dos grupos sobrevivientes se fusionaron al renumerar los turnos')
    m_antes, m_despues = miembros(before), miembros(after)
    # La única fusión autorizada es la del padre 3062: sus tres turnos de v10 pasan a
    # ser uno solo en v11, con un único miembro. Se verifica por separado y no se
    # deja a la comprobación general, que exigiría membresía idéntica.
    turnos_3062 = {f['ID_Turno'] for f in before if int(f['ID_Padre']) == 3062}
    if len(turnos_3062) != 3:
        raise ValueError(f'el padre 3062 tenía {len(turnos_3062)} turnos en v10, se esperaban 3')
    # El turno sobreviviente del 3062 conserva sus miembros y eso lo verifica el
    # bucle general de abajo: en v10 ya compartía grupo con 3061:1 porque los dos
    # son de Soto y van seguidos, así que la fusión no le cambia la membresía. Lo
    # que sí hay que exigir es que los grupos de las dos filas fusionadas
    # desaparezcan, y que el padre quede en un solo segmento (SEGMENTOS_ESPERADOS).
    destino = {por_iid[f['ID_Intervencion']]['ID_Turno'] for f in before
               if int(f['ID_Padre']) == 3062 and f['ID_Intervencion'] in presentes}
    if len(destino) != 1:
        raise ValueError(f'las filas sobrevivientes del padre 3062 no quedaron en un '
                         f'solo turno: {destino}')
    if 'RPM-2010-04-15:3062:1' not in m_despues.get(destino.pop(), []):
        raise ValueError('el turno fusionado del padre 3062 no contiene su fila sobreviviente')
    for viejo, miembros_viejos in m_antes.items():
        if viejo in turnos_3062:
            continue
        if m_despues.get(mapa[viejo]) != miembros_viejos:
            raise ValueError(f'grupo {viejo} -> {mapa[viejo]} cambió de miembros: '
                             f'{miembros_viejos} -> {m_despues.get(mapa[viejo])}')
    extras = sorted(set(m_despues) - set(mapa.values()))
    if extras:
        raise ValueError(f'v11 no crea grupos y hay {len(extras)} nuevos: {extras}')
    perdidos = sorted(set(m_antes) - set(mapa))
    if set(perdidos) - turnos_3062:
        raise ValueError(f'desaparecieron grupos ajenos al padre 3062: '
                         f'{sorted(set(perdidos) - turnos_3062)}')
    if len(perdidos) != 2:
        raise ValueError(f'debían desaparecer los 2 grupos de las filas fusionadas del '
                         f'padre 3062 y desaparecieron {perdidos}')

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

    return dict(Perfil='procedimental-v11', Baseline='procedimental-v10', Pasa=True,
                Filas_Antes=len(before), Filas_Despues=len(after), Filas_Nuevas=nuevas,
                Filas_Fusionadas=borradas,
                Padres_Resegmentados=sorted(PADRES),
                Cortes=len(revisiones),
                IDs_Corridos=len(corridas),
                Grupos_Antes=len(m_antes), Grupos_Despues=len(m_despues),
                Comparacion=('Todas las filas, todos los campos y todos los miembros de cada '
                             'grupo; la única diferencia autorizada es la resegmentación de '
                             'ocho padres'),
                Alertas_Antes=sum(bool(f['Motivos_Revision']) for f in before),
                Alertas_Despues=sum(bool(f['Motivos_Revision']) for f in after),
                Filas_Alertadas_Antes=sum(bool(f['Motivos_Revision']) for f in before),
                Reservas_Abiertas=reservas,
                SHA256_Baseline=BASE_SHA,
                SHA256_Registro=hashlib.sha256(LOTE10.read_bytes()).hexdigest()), linaje


def revisiones():
    """Las ocho revisiones del lote10, indexadas por padre."""
    entradas = json.loads(LOTE10.read_text(encoding='utf-8'))
    casos = entradas['Casos'] if isinstance(entradas, dict) and 'Casos' in entradas else entradas
    return {e['ID_Padre']: e for e in casos}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    args = parser.parse_args()
    if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASE_SHA:
        raise ValueError('La entrega procedimental v10 cambió')
    target = args.candidate / BASE.name
    report, linaje = compare(read_rows(BASE), read_rows(target), revisiones())
    report['SHA256_Candidato'] = hashlib.sha256(target.read_bytes()).hexdigest()
    with (args.candidate / 'linaje_cortes_lote10.csv').open('w', encoding='utf-8-sig',
                                                            newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(linaje[0]), quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(linaje)
    (args.candidate / 'comparacion_procedimental_v11.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
