"""Gate global de la entrega intrapadre v1, contra LOOP32 inmutable.

Compara la partición completa por pertenencia, no los números renumerados de
ID_Turno. Sólo permite dos uniones y cuatro celdas relacionales modificadas.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
from diagnosticar_finales import read_rows
from reviewed_intrapara_continuity import ALLOWED, RELATION

ROOT = Path(__file__).resolve().parents[1]
BASELINE_SHA = 'f9d76860d86500a8d3b928eb9e9f6849c74f9e4480df0fdaa381d090e69ddcd2'


def groups(rows):
    result = collections.defaultdict(set)
    for r in rows:
        result[r['ID_Turno']].add(r['ID_Intervencion'])
    return set(frozenset(v) for v in result.values())


def compare(before, after, *, pairs=ALLOWED, profile='intrapadre-v1', baseline='LOOP32'):
    ids = [r['ID_Intervencion'] for r in before]
    if len(set(ids)) != len(ids) or ids != [r['ID_Intervencion'] for r in after]:
        raise ValueError('Filas, identidad u orden alterados')
    expected = groups(before)
    for left, right in pairs:
        a = next(g for g in expected if left in g)
        b = next(g for g in expected if right in g)
        if a == b:
            raise ValueError('El baseline ya contiene el enlace intrapadre')
        expected.remove(a)
        expected.remove(b)
        expected.add(a | b)
    if expected != groups(after):
        raise ValueError('Partición global distinta: enlace extra, pérdida o división de grupo')
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
        'Nota': 'Los IDs numéricos se renumeran. La partición completa se compara por pertenencia, no por etiquetas.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    args = parser.parse_args()
    baseline = ROOT / 'data/processed/consolidado_base_referencia.xlsx'
    if hashlib.sha256(baseline.read_bytes()).hexdigest() != BASELINE_SHA:
        raise ValueError('LOOP32 histórico no coincide con el hash revisado')
    report = compare(read_rows(baseline), read_rows(args.candidate / baseline.name))
    report['SHA256_Baseline'] = BASELINE_SHA
    report['SHA256_Candidato'] = hashlib.sha256((args.candidate / baseline.name).read_bytes()).hexdigest()
    (args.candidate / 'comparacion_intrapadre.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'Celdas_ID_Turno_Modificadas'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
