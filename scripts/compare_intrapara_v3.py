"""Gate v3 contra v2: exactamente nueve uniones nuevas; no tocar el histórico."""
import argparse
import hashlib
import json
from pathlib import Path
from compare_intrapara_release import compare
from reviewed_intrapara_v3 import BASE, NEW_PAIRS
from diagnosticar_finales import read_rows

BASELINE_SHA = '5ac6b4c788dafd9f1201e3774c3c3fdff88cd046d28d057f776b00e3a71b5f36'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    args = parser.parse_args()
    if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASELINE_SHA:
        raise ValueError('El histórico intrapadre v2 cambió')
    target = args.candidate / BASE.name
    report = compare(read_rows(BASE), read_rows(target), pairs=NEW_PAIRS,
                     profile='intrapadre-v3', baseline='intrapadre-v2')
    report['SHA256_Baseline'] = BASELINE_SHA
    report['SHA256_Candidato'] = hashlib.sha256(target.read_bytes()).hexdigest()
    (args.candidate / 'comparacion_intrapadre.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'Celdas_ID_Turno_Modificadas'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
