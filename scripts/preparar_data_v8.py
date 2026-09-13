"""Construye la entrega v8 = v7 + los cuatro cortes del lote10, y publica sólo si pasa todo.

Uso: python scripts/preparar_data_v8.py --destino data/releases/continuidad_procedimental_v8

Es un driver nuevo a propósito. ``preparar_data.py`` está fijado por hash en el
manifiesto de la entrega v7 y su perfil ``procedimental-v7`` despacha a
``compare_functional_v7.py``, un gate que exige cardinalidad idéntica porque eso
es lo que v7 debía probar. Reescribirlo invalidaría la procedencia de v7; por eso
v8 tiene su propio driver y su propio gate.

La construcción es la de v7 (mismo refinamiento funcional v4+v5, mismas pruebas
intrapadre v4, mismas lecturas procedimentales v5); lo único que se agrega es el
registro ``revisiones_hablantes_lote10.json``, que ``build_base_referencia.py``
fusiona con el registro histórico sin tocarlo. Por eso ``NLM_PERFIL_CONSTRUCCION``
sigue siendo ``procedimental-v7``: ``intrapara_profiles.REQUIRED_INTRAPARA`` está
fijado y no conoce un perfil v8. La identidad de la entrega la declara
``comparacion_procedimental_v8.json``.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

GATE = 'scripts/compare_procedural_v8.py'
SALIDAS_EXTRAS = ('comparacion_procedimental_v8.json', 'linaje_cortes_lote10.csv')
SALIDAS = ('textos_completos.jsonl', 'consolidado_base_referencia.xlsx',
           'consolidado_base_referencia_final.xlsx', 'qa_preparacion.json',
           'revision_pendientes.csv', 'decisiones_tpm.csv', 'turnos_habla.csv',
           'manifiesto_preparacion.json', 'revision_783.csv', 'revision_783.xlsx',
           'resumen_revision_783.json', 'documentos_leidos.csv')


def destino_versionado(destino):
    objetivo = destino.resolve()
    raices = (ROOT / '.cache', ROOT / 'data/releases')
    if not any(r.resolve() in objetivo.parents for r in raices) or objetivo.exists():
        raise ValueError('La entrega versionada requiere un destino nuevo bajo .cache/ o data/releases/')
    return objetivo


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', type=Path,
                        default=ROOT / 'data/releases/continuidad_procedimental_v8')
    args = parser.parse_args(argv)
    objetivo = destino_versionado(args.destino)

    cache = ROOT / '.cache'
    cache.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='preparacion-v8-', dir=cache) as temp:
        stage = Path(temp)
        env = {**os.environ, 'NLM_PROCESSED_DIR': str(stage), 'PYTHONHASHSEED': '0',
               # La construcción es la de v7; v8 sólo agrega el registro lote10.
               'NLM_PERFIL_CONSTRUCCION': 'procedimental-v7',
               'NLM_PROCEDURAL_REVIEWS': str(ROOT / 'data/curation/continuidades_procedimentales_v5.json'),
               'NLM_FUNCTIONAL_REVIEWS': str(ROOT / 'data/curation/refinamiento_funcional_v4.json'),
               'NLM_FUNCTIONAL_V5_REVIEWS': str(ROOT / 'data/curation/refinamiento_funcional_v5.json'),
               'NLM_INTRAPARA_REVIEWS': str(ROOT / 'data/curation/continuidades_intrapadre_v4.json')}
        comandos = [
            ['scripts/build_textos_completos.py'],
            ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
            ['scripts/build_base_referencia.py'],
            ['scripts/crear_consolidado_final.py'],
            ['scripts/qa_gate_f0.py', str(stage / 'consolidado_base_referencia.xlsx')],
            [GATE, '--candidate', str(stage)],
            ['scripts/qa_preparacion_v8.py', '--processed', str(stage)],
        ]
        for comando in comandos:
            print('\n>>>', ' '.join(comando), flush=True)
            subprocess.run([sys.executable, *comando], cwd=ROOT, env=env, check=True)
        for nombre in SALIDAS + SALIDAS_EXTRAS:
            if not (stage / nombre).is_file():
                raise RuntimeError(f'Falta salida validada: {nombre}')
        # Nada se publica antes de pasar TODAS las verificaciones.
        destino_versionado(args.destino)
        objetivo.parent.mkdir(parents=True, exist_ok=True)
        os.replace(stage, objetivo)
    comparacion = json.loads((objetivo / 'comparacion_procedimental_v8.json')
                             .read_text(encoding='utf-8'))
    print(f'\nPublicación terminada en {objetivo}.')
    print('Perfil %s sobre %s: %d -> %d filas, %s'
          % (comparacion['Perfil'], comparacion['Baseline'], comparacion['Filas_Antes'],
             comparacion['Filas_Despues'], comparacion['Filas_Nuevas']))
    print('SHA256 del candidato: %s' % hashlib.sha256(
        (objetivo / 'consolidado_base_referencia_final.xlsx').read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
