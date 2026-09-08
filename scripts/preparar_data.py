"""Construye en staging, ejecuta pruebas + F0/F1 y publica sólo si no hay fallos.

Uso: python scripts/preparar_data.py
Las alertas semánticas no se ocultan: se publican en revision_pendientes.csv.
"""
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


def main():
    cache = ROOT / '.cache'
    cache.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='preparacion-', dir=cache) as temp:
        stage = Path(temp)
        env = {**os.environ, 'NLM_PROCESSED_DIR': str(stage), 'PYTHONHASHSEED': '0'}
        commands = [
            ['scripts/build_textos_completos.py'],
            ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
            ['scripts/build_base_referencia.py'],
            ['scripts/crear_consolidado_final.py'],
            ['scripts/qa_gate_f0.py', str(stage/'consolidado_base_referencia.xlsx')],
            ['scripts/qa_preparacion.py', '--processed', str(stage)],
        ]
        for args in commands:
            print('\n>>>', ' '.join(args), flush=True)
            subprocess.run([sys.executable, *args], cwd=ROOT, env=env, check=True)
        target = ROOT / 'data/processed'
        target.mkdir(parents=True, exist_ok=True)
        for name in OUTPUTS:
            if not (stage/name).is_file():
                raise RuntimeError(f'Falta salida validada: {name}')
        # Ninguna salida se publica antes de pasar TODAS las verificaciones.
        for name in OUTPUTS:
            os.replace(stage/name, target/name)
    print('\nPublicación terminada. Consultar qa_preparacion.json y revision_pendientes.csv.')


if __name__ == '__main__':
    main()
