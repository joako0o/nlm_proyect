"""Gate v6 independiente: dos uniones intrapadre exactas sobre la entrega v5.

Compara TODOS los campos y TODOS los grupos de la entrega v5, no sólo los dos
pares. Además exige que las seis continuidades procedimentales de v5 y las tres
reservas del lote6 sigan exactamente como estaban.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
from compare_intrapara_release import compare, groups
from reviewed_intrapara_v4 import BASE, BASE_SHA, NEW_PAIRS, RESERVAS_ABIERTAS, DECISIONES_LOTE6
from reviewed_procedural_v5 import PAIRS as V5_PAIRS, PATH, file_sha
from diagnosticar_finales import read_rows
from intrapara_profiles import required_intrapara

ROOT = Path(__file__).resolve().parents[1]
ALERTAS_V5 = 467
GRUPOS_V5 = 9236
GRUPOS_V6 = 9234


def members(rows):
    by_turn = collections.defaultdict(set)
    for r in rows:
        by_turn[r['ID_Turno']].add(r['ID_Intervencion'])
    return {rid: frozenset(g) for g in by_turn.values() for rid in g}


def verify(before, after):
    """Comparación global v5→v6; falla ante cualquier cambio no autorizado."""
    report = compare(before, after, pairs=sorted(NEW_PAIRS),
                     profile='procedimental-v6', baseline='procedimental-v5')

    # Las seis uniones procedimentales de v5 deben seguir vigentes en v6.
    after_members = members(after)
    by_id = {r['ID_Intervencion']: r for r in after}
    for left, right in V5_PAIRS:
        if after_members[left] != after_members[right]:
            raise ValueError(f'v6 perdió la continuidad procedimental {left}→{right}')
        if by_id[right]['Relacion_Turno'] != 'CONTINUIDAD_PROCEDIMENTAL_REVISADA':
            raise ValueError(f'{right}: relación procedimental ausente en v6')
    # Las tres reservas del lote6 permanecen separadas de su extremo izquierdo.
    for left in RESERVAS_ABIERTAS:
        right = DECISIONES_LOTE6[left][0]
        if after_members[left] == after_members[right]:
            raise ValueError(f'v6 cerró la reserva {left}→{right}')
    # Los extremos izquierdos aplicados conservan ancla nula y su fuente.
    for left, right in NEW_PAIRS:
        row = by_id[left]
        if row['ID_Ancla_Actor'] or row['Fuente_Actor'] != 'CONTEXTO_REVISADO':
            raise ValueError(f'{left}: ancla o fuente del extremo izquierdo alteradas')
        if by_id[right]['ID_Ancla_Actor'] != right:
            raise ValueError(f'{right}: el extremo nominal perdió su ancla propia')
    if (report['Grupos_Antes'] != GRUPOS_V5 or report['Grupos_Despues'] != GRUPOS_V6
            or report['Alertas_Antes'] != ALERTAS_V5 or report['Alertas_Despues'] != ALERTAS_V5):
        raise ValueError('Grupos o alertas fuera de la expectativa medida del lote6')
    report.update(Perfil_Intrapadre_Exigido=required_intrapara('procedimental-v6'),
                  Reserva='La revisión semántica del corpus no está terminada; 780, 2661 y 5252 siguen abiertos.')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    args = parser.parse_args()
    if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASE_SHA:
        raise ValueError('La entrega procedimental v5 cambió')
    target = args.candidate / BASE.name
    report = verify(read_rows(BASE), read_rows(target))
    report.update(SHA256_Baseline=BASE_SHA, SHA256_Candidato=file_sha(target),
                  SHA256_Registro_Intrapadre_V4=file_sha(ROOT / 'data/curation/continuidades_intrapadre_v4.json'),
                  SHA256_Registro_Procedimental_V5=file_sha(PATH))
    (args.candidate / 'comparacion_procedimental.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'Celdas_ID_Turno_Modificadas'},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
