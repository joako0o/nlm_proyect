"""Fusiona un lote de correcciones/revisiones dentro del registro curado.

Uso:  .venv/bin/python .cache/agregar_ocr.py <lote.json>

El lote tiene la forma {"Correcciones": [...], "Revisiones_Sin_Correccion": [...]}.
Rechaza una entrada cuyo ID_Intervencion ya esté registrado, para no pisar
trabajo previo por accidente.
"""
import json
import sys
from pathlib import Path

REG = Path('data/curation/correcciones_ocr_v1.json')
reg = json.loads(REG.read_text(encoding='utf-8'))
lote = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))

ids = {e['ID_Intervencion'] for e in reg['Correcciones']}
agregadas, repetidas = [], []
for e in lote.get('Correcciones', []):
    if e['ID_Intervencion'] in ids:
        repetidas.append(e['ID_Intervencion'])
        continue
    reg['Correcciones'].append(e)
    ids.add(e['ID_Intervencion'])
    agregadas.append(e['ID_Intervencion'])

ya = {(r['ID_Intervencion'], r['Texto_Original_Fragmento'])
      for r in reg['Revisiones_Sin_Correccion']}
nuevas = 0
for r in lote.get('Revisiones_Sin_Correccion', []):
    if 'Marca' not in r:
        print('RECHAZADA sin Marca:', r['ID_Intervencion'])
        raise SystemExit(1)
    clave = (r['ID_Intervencion'], r['Texto_Original_Fragmento'])
    if clave in ya:
        continue
    reg['Revisiones_Sin_Correccion'].append(r)
    ya.add(clave)
    nuevas += 1

REG.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('filas con correccion agregadas:', agregadas or 'ninguna')
print('revisiones agregadas:', nuevas)
if repetidas:
    print('RECHAZADAS por ya existir:', repetidas)
    raise SystemExit(1)
print('total filas con correccion:', len(reg['Correcciones']))
print('total operaciones:', sum(len(e['Operaciones']) for e in reg['Correcciones']))
print('total revisiones:', len(reg['Revisiones_Sin_Correccion']))
