"""Universo de filas con varias personas de la asistencia dentro de una misma fila.

Eje distinto al inventario de límites: allí se miran fronteras ENTRE filas; aquí se
buscan filas que por sí solas podrían contener más de un hablante.

Restringe los candidatos a la lista de asistencia de la sesión y los canoniza con
resolve_name, porque el roster trae variantes OCR de una misma persona (sergio
lehmann beresi / sergio lehmann b / lehmann) que inflarían el conteo.

Es deliberadamente sensible de más: contar nombres no decide nada. Una mención,
una bienvenida, una llegada o una entrega de la palabra no son intervención, así
que el resultado es un universo a leer, no un conjunto de errores.
"""
import argparse
import collections
import csv
import hashlib
import json
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_base_referencia as builder
from diagnosticar_finales import read_rows

V7 = ROOT / 'data/releases/continuidad_procedimental_v7/consolidado_base_referencia.xlsx'
V7_SHA = '84889a846ec0b3a2fce88d37f1d5a0a3676b33dcd962c428de7cdbb3c992d9a7'
CONSEJO = 'Consejo del Banco Central de Chile'
CAMPOS = ['ID_Intervencion', 'ID_Padre', 'Fecha', 'Actor_Final', 'Institucional',
          'Fuente_Actor', 'Caracteres', 'Otras_Personas_Roster', 'Nombres',
          'Motivos_Revision', 'Alerta_Motor', 'Leida_En_Lote9', 'Veredicto']


def norm(t):
    return ''.join(c for c in unicodedata.normalize('NFD', str(t).lower())
                   if unicodedata.category(c) != 'Mn')


def otras_personas(texto, actor, fecha):
    """Personas canónicas de la asistencia, distintas del actor, presentes en el texto."""
    texto_n = norm(texto)
    propios = set(norm(actor).split())
    personas = set()
    for clave in builder.ROSTER_BY_DATE.get(fecha, {}):
        canon = builder.resolve_name(clave, fecha)
        if not canon or canon in personas:
            continue
        partes = [p for p in norm(clave).split() if len(p) > 2]
        if not partes or set(partes) & propios:
            continue
        pos, presente = -1, True
        for p in partes[-2:]:
            pos = texto_n.find(p, pos + 1)
            if pos < 0:
                presente = False
                break
        if presente:
            personas.add(canon)
    return sorted(personas)


def scan(rows):
    out = []
    for r in rows:
        actor = r['Actor_Final'] or ''
        texto = r['Texto'] or ''
        nombres = otras_personas(texto, actor, str(r['Fecha'])[:10])
        if not nombres:
            continue
        out.append({
            'ID_Intervencion': r['ID_Intervencion'], 'ID_Padre': r['ID_Padre'],
            'Fecha': str(r['Fecha'])[:10], 'Actor_Final': actor,
            'Institucional': 'SI' if actor == CONSEJO else 'NO',
            'Fuente_Actor': r['Fuente_Actor'], 'Caracteres': len(texto),
            'Otras_Personas_Roster': len(nombres), 'Nombres': '; '.join(nombres),
            'Motivos_Revision': r['Motivos_Revision'] or '',
            'Alerta_Motor': ('SI' if 'POSIBLE_OTRO_HABLANTE_O_MENCION'
                             in (r['Motivos_Revision'] or '') else 'NO'),
            'Leida_En_Lote9': 'NO', 'Veredicto': '',
        })
    return out


LECTURAS = {
    'RPM-2006-06-15:676:1': (
        'UNA_SOLA_VOZ_MENCIONES_Y_TRASPASO',
        'Corbo informa la ausencia de Velasco, fija la fecha de diciembre, da la bienvenida a '
        'Álvarez Vallejos, señala que García fue invitado y anuncia quiénes expondrán. Los cinco '
        'nombres son menciones, llegadas y una entrega de la palabra; ninguno interviene.'),
    'RPM-2014-02-18:6009:1': (
        'UNA_SOLA_VOZ_MENCIONES_Y_TRASPASO',
        'Vergara da la bienvenida a García Silva, felicita a Marshall, se despide de Soto, fija '
        'la fecha de agosto y ofrece la palabra a Ricaurte. Cuatro nombres, ninguna intervención '
        'ajena: es apertura de sesión.'),
    'RPM-2012-02-14:4574:1': (
        'UNA_SOLA_VOZ_ALERTA_FALSO_POSITIVO',
        'Vergara da la bienvenida a Vial, registra la renovación de Marfán, fija la fecha de '
        'agosto, deja constancia del mensaje de Larraín y da paso a Ricaurte. El motor la marcó '
        'con POSIBLE_OTRO_HABLANTE_O_MENCION; leída completa, no hay segunda voz.'),
}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', type=Path, required=True)
    out = parser.parse_args(argv).salida.resolve()
    if out.exists() or not any((ROOT / r).resolve() in out.parents for r in ('.cache', 'docs')):
        raise ValueError('Se requiere destino nuevo bajo .cache/ o docs/, nunca data/')
    if hashlib.sha256(V7.read_bytes()).hexdigest() != V7_SHA:
        raise ValueError('La entrega v7 cambió')
    rows = read_rows(V7)
    vista = scan(rows)
    for r in vista:
        lectura = LECTURAS.get(r['ID_Intervencion'])
        if lectura:
            r['Leida_En_Lote9'] = 'SI'
            r['Veredicto'] = lectura[0]
    out.mkdir(parents=True)
    with (out / 'inventario_multihablante_v7.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(vista)
    personales = [r for r in vista if r['Institucional'] == 'NO']
    resumen = {
        'Filas_V7': len(rows),
        'Filas_Con_Alguna_Otra_Persona': len(vista),
        'Filas_Institucionales_Del_Consejo': len(vista) - len(personales),
        'Hablantes_Personales_Con_Otras_Personas': len(personales),
        'Personales_Por_Cantidad': dict(sorted(
            collections.Counter(r['Otras_Personas_Roster'] for r in personales).items())),
        'Personales_Con_Dos_O_Mas': sum(1 for r in personales if r['Otras_Personas_Roster'] >= 2),
        'Personales_Con_Tres_O_Mas': sum(1 for r in personales if r['Otras_Personas_Roster'] >= 3),
        'Con_Alerta_Del_Motor': sum(1 for r in personales if r['Alerta_Motor'] == 'SI'),
        'Sin_Ninguna_Alerta': sum(1 for r in personales if not r['Motivos_Revision']),
        'Leidas_En_Este_Lote': len(LECTURAS),
        'SHA256_V7': V7_SHA,
        'Nota': ('Universo a leer, no conjunto de errores: el motor sólo marca 22 filas en todo '
                 'el corpus y este barrido encuentra 410 hablantes personales con al menos otra '
                 'persona de la asistencia. Contar nombres no decide nada; una mención, una '
                 'bienvenida o una entrega de la palabra no son intervención.'),
    }
    (out / 'resumen.json').write_text(json.dumps(resumen, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(resumen, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
