"""Despacho explícito; v1 y v2 conservan registros y alcances distintos."""
import json
from pathlib import Path
from reviewed_intrapara_continuity import load_intrapara_links as load_v1
from reviewed_intrapara_v2 import load_v2


def profile_name(path):
    package = json.loads(Path(path).read_text())
    if not isinstance(package, dict) or type(package.get('Version')) is not int:
        raise ValueError('Perfil intrapadre inválido')
    version = package['Version']
    if version not in (1,2) or package.get('Alcance') != f'CONTINUIDAD_INTRAPADRE_V{version}':
        raise ValueError('Perfil intrapadre desconocido')
    return f'intrapadre-v{version}'


def load_intrapara_links(raw, path):
    return (load_v1 if profile_name(path) == 'intrapadre-v1' else load_v2)(raw, path)
