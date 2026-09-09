"""Gate v5 independiente: seis uniones exactas y todos los campos/grupos de v4."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
from diagnosticar_finales import read_rows
from reviewed_procedural_v5 import PAIRS, RELATION, BASE, BASE_SHA, load_reviews, ROOT, PATH, file_sha
from auditar_continuidad_turnos import inventory


def groups(rows):
    result = collections.defaultdict(set)
    for r in rows:
        result[r['ID_Turno']].add(r['ID_Intervencion'])
    return set(frozenset(v) for v in result.values())


def compare(before, after):
    pairs=PAIRS;profile='procedimental-v5';baseline='funcional-v4'
    ids = [r['ID_Intervencion'] for r in before]
    if len(set(ids)) != len(ids) or ids != [r['ID_Intervencion'] for r in after]:
        raise ValueError('Filas, identidad u orden alterados')
    expected = groups(before)
    for left, right in pairs:
        a = next(g for g in expected if left in g)
        b = next(g for g in expected if right in g)
        if a == b:
            raise ValueError('El baseline ya contiene el enlace procedimental')
        expected.remove(a)
        expected.remove(b)
        expected.add(a | b)
    if expected != groups(after):
        raise ValueError('Partición global distinta: enlace extra, pérdida o división de grupo')
    # Además de membresía, los rótulos deben conservar la secuencia por sesión.
    label_by_member={rid:g for g in expected for rid in g}
    seen={};counts=collections.Counter()
    for r in after:
        g=label_by_member[r['ID_Intervencion']];date=str(r['Fecha'])[:10]
        if g not in seen:
            counts[date]+=1;seen[g]=f'RPM-{date}:T{counts[date]}'
        if r['ID_Turno']!=seen[g]:raise ValueError('Numeración de grupos no determinista')
    rights = {right: left for left, right in pairs}
    changes, labels = [], []
    for a, b in zip(before, after):
        rid = a['ID_Intervencion']
        if a.keys() != b.keys():
            raise ValueError('Esquema de auditoría alterado')
        for field in a:
            if a[field] == b[field]:
                continue
            change = {'ID_Intervencion': rid, 'Campo': field, 'Antes': a[field], 'Despues': b[field]}
            if field == 'ID_Turno':
                labels.append(change)
            elif (rid in rights and field in ('Relacion_Turno', 'ID_Antecedente_Continuidad')
                    and b[field] == (RELATION if field == 'Relacion_Turno' else rights[rid])):
                changes.append(change)
            else:
                raise ValueError(f'Cambio no autorizado: {rid} / {field}')
    if len(changes) != 2 * len(pairs):
        raise ValueError('Se requieren las relaciones y antecedentes exactos de cada unión')
    old_members = {rid: g for g in groups(before) for rid in g}
    new_members = {rid: g for g in groups(after) for rid in g}
    affected = sorted(rid for rid in ids if old_members[rid] != new_members[rid])
    return {
        'Pasa': True, 'Perfil': profile, 'Baseline': baseline,
        'Filas': len(after), 'Grupos_Antes': len(groups(before)), 'Grupos_Despues': len(groups(after)),
        'Uniones_Exactas': [list(key) for key in pairs],
        'Celdas_Relacionales_Modificadas': changes, 'Celdas_ID_Turno_Modificadas': labels,
        'Filas_Con_Conjunto_De_Companeros_Distinto': affected,
        'Otros_Campos_Modificados': 0, 'Grupos_Previos_Divididos': 0,
        'Alertas_Antes': sum(bool(r['Motivos_Revision']) for r in before),
        'Alertas_Despues': sum(bool(r['Motivos_Revision']) for r in after),
        'Inventario_Antes':len(inventory(before)), 'Inventario_Despues':len(inventory(after)),
        'Nota': 'Sólo se renumeran etiquetas ID_Turno; IDs físicos, segmentos, anclas y todos los demás campos intactos.',
    }



def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate',type=Path,required=True);args=parser.parse_args()
    raw={r['ID']:r for r in read_rows(ROOT/'data/raw/consolidado_final.xlsx')}
    load_reviews(raw)
    target=args.candidate/BASE.name
    report=compare(read_rows(BASE),read_rows(target))
    report.update(SHA256_Baseline=BASE_SHA,SHA256_Candidato=file_sha(target),SHA256_Registro=file_sha(PATH))
    (args.candidate/'comparacion_procedimental.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='Celdas_ID_Turno_Modificadas'},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
