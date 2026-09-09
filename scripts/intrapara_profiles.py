"""Despacho explícito; v1, v2, v3 y v4 conservan registros y alcances distintos."""
import json
from pathlib import Path
from reviewed_intrapara_continuity import load_intrapara_links as load_v1
from reviewed_intrapara_v2 import load_v2
from reviewed_intrapara_v3 import load_v3
from reviewed_intrapara_v4 import load_v4

VERSIONS = (1, 2, 3, 4)


def profile_name(path):
    package = json.loads(Path(path).read_text())
    if not isinstance(package, dict) or type(package.get('Version')) is not int:
        raise ValueError('Perfil intrapadre inválido')
    version = package['Version']
    if version not in VERSIONS or package.get('Alcance') != f'CONTINUIDAD_INTRAPADRE_V{version}':
        raise ValueError('Perfil intrapadre desconocido')
    return f'intrapadre-v{version}'


def load_intrapara_links(raw, path):
    loaders = {'intrapadre-v1':load_v1, 'intrapadre-v2':load_v2, 'intrapadre-v3':load_v3,
               'intrapadre-v4':load_v4}
    return loaders[profile_name(path)](raw,path)


# Perfil intrapadre acumulado que exige cada perfil de construcción. v6 usa v4
# (diecisiete pruebas); los perfiles históricos siguen exigiendo v3 (quince).
REQUIRED_INTRAPARA = {'funcional-v4': 'intrapadre-v3', 'procedimental-v5': 'intrapadre-v3',
                      'procedimental-v6': 'intrapadre-v4'}


def required_intrapara(perfil=None):
    """Perfil intrapadre exigido; admite el perfil de construcción o el intrapadre."""
    import os
    perfil = perfil or os.environ.get('NLM_PERFIL_CONSTRUCCION') or 'procedimental-v5'
    if perfil in REQUIRED_INTRAPARA:
        return REQUIRED_INTRAPARA[perfil]
    if perfil in {f'intrapadre-v{v}' for v in VERSIONS}:
        return perfil
    raise ValueError('Perfil de construcción desconocido: ' + str(perfil))
