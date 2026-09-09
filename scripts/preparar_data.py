"""Construye en staging, ejecuta pruebas + F0/F1 y publica sólo si no hay fallos.

Uso actual: python scripts/preparar_data.py --perfil intrapadre-v3
El perfil predeterminado es intrapadre-v3 y nunca sobrescribe una entrega existente.
--perfil legacy conserva el constructor anterior; puede sobrescribir data/processed.
--destino admite una nueva salida bajo .cache/ o data/releases/.
Las alertas semánticas no se ocultan: se publican en revision_pendientes.csv.
"""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ('textos_completos.jsonl', 'consolidado_base_referencia.xlsx',
           'consolidado_base_referencia_final.xlsx', 'qa_preparacion.json',
           'revision_pendientes.csv', 'decisiones_tpm.csv', 'turnos_habla.csv', 'manifiesto_preparacion.json',
           'revision_783.csv', 'revision_783.xlsx', 'resumen_revision_783.json', 'documentos_leidos.csv')


def release_target(destination):
    target = destination.resolve()
    roots = (ROOT / '.cache', ROOT / 'data/releases')
    if not any(root.resolve() in target.parents for root in roots) or target.exists():
        raise ValueError('La entrega versionada requiere destino nuevo bajo .cache/ o data/releases/')
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--perfil', choices=('legacy', 'intrapadre-v1', 'intrapadre-v2', 'intrapadre-v3'), default='intrapadre-v3')
    parser.add_argument('--destino', type=Path)
    args = parser.parse_args(argv)
    versioned = args.perfil != 'legacy'
    version = args.perfil.removeprefix('intrapadre-v') if versioned else None
    if args.destino and not versioned:
        parser.error('--destino sólo se admite con perfiles versionados')
    target = release_target(args.destino or ROOT / f'data/releases/continuidad_intrapadre_v{version}') if versioned else ROOT / 'data/processed'

    cache = ROOT / '.cache'
    cache.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='preparacion-', dir=cache) as temp:
        stage = Path(temp)
        env = {**os.environ, 'NLM_PROCESSED_DIR': str(stage), 'PYTHONHASHSEED': '0'}
        # No permitir activación ambiental accidental en el perfil histórico.
        env.pop('NLM_INTRAPARA_REVIEWS', None)
        if versioned:
            env['NLM_INTRAPARA_REVIEWS'] = str(ROOT / f'data/curation/continuidades_intrapadre_v{version}.json')
        commands = [
            ['scripts/build_textos_completos.py'],
            ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
            ['scripts/build_base_referencia.py'],
            ['scripts/crear_consolidado_final.py'],
            ['scripts/qa_gate_f0.py', str(stage/'consolidado_base_referencia.xlsx')],
            *([[f'scripts/compare_intrapara_v{version}.py' if version in ('2','3') else 'scripts/compare_intrapara_release.py', '--candidate', str(stage)]] if versioned else []),
            ['scripts/qa_preparacion.py', '--processed', str(stage)],
        ]
        for args in commands:
            print('\n>>>', ' '.join(args), flush=True)
            subprocess.run([sys.executable, *args], cwd=ROOT, env=env, check=True)
        for name in OUTPUTS:
            if not (stage/name).is_file():
                raise RuntimeError(f'Falta salida validada: {name}')
        # Ninguna salida se publica antes de pasar TODAS las verificaciones.
        if versioned:
            release_target(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(stage, target)
        else:
            target.mkdir(parents=True, exist_ok=True)
            for name in OUTPUTS:
                os.replace(stage/name, target/name)
    print(f'\nPublicación terminada en {target}. Consultar qa_preparacion.json y revision_pendientes.csv.')


if __name__ == '__main__':
    main()
