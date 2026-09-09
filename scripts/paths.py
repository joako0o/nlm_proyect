"""Rutas comunes; NLM_PROCESSED_DIR permite construir y validar en staging."""
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA_RAW = REPO / 'data/raw'
DATA_EXT = REPO / 'data/external'
DATA_PROC = Path(os.environ.get('NLM_PROCESSED_DIR', REPO / 'data/processed')).resolve()
