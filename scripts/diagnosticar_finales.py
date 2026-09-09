"""Triaje de FINAL_SIN_PUNTUACION: sólo agrupa y exporta contexto, no adjudica.

Utilidad independiente del pipeline. No modifica la base ni registros de curación.
Las categorías describen indicios superficiales y relaciones YA exportadas, no
correcciones de puntuación, validaciones de OCR ni nuevos límites de voz.
"""
import argparse
import collections
import csv
import hashlib
import json
import re
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
MOTIVE = 'FINAL_SIN_PUNTUACION'
FOOTER = re.compile(r'(?:Sesión\s+N[°º]?\s*\d+\s+Página\s+\d+\s+de\s+\d+|'
                    r'B\s+A\s+N\s+C\s+O\s+C\s+E\s+N\s+T\s+R\s+A\s+L\s+D\s+E\s+C\s+H\s+I\s+L\s+E)\s*$', re.I)
HEADER = re.compile(r'Exposición\s+Síntesis\s+del\s+mes\s*$', re.I)
FUNCTION_WORD = re.compile(r'\b(?:para|el|la|los|las|un|una|de|del|al|con|que|ese|esa|estos|esas)\s*$', re.I)
FIELDS = ('ID', 'ID_Padre', 'ID_Intervencion', 'Fecha', 'Actor_Final', 'Texto',
          'Fuente_Actor', 'ID_Turno', 'ID_Antecedente_Continuidad', 'Motivos_Revision')


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def motives(row):
    return {m.strip() for m in (row.get('Motivos_Revision') or '').split(';') if m.strip()}


def same_session(a, b):
    return bool(a and b and str(a['Fecha'])[:10] == str(b['Fecha'])[:10])


def relation(row, following):
    if not following:
        return 'SIN_FILA_SIGUIENTE'
    if not same_session(row, following):
        return 'OTRA_SESION'
    if row['ID_Padre'] == following['ID_Padre']:
        return ('MISMO_PADRE_OTRO_ACTOR' if row['Actor_Final'] != following['Actor_Final']
                else 'MISMO_PADRE_MISMO_ACTOR')
    if row['Actor_Final'] != following['Actor_Final']:
        return 'OTRO_PADRE_OTRO_ACTOR'
    if (row.get('ID_Turno') and row['ID_Turno'] == following.get('ID_Turno')
            and following.get('ID_Antecedente_Continuidad') == row['ID_Intervencion']):
        return 'OTRO_PADRE_ENLACE_EXISTENTE'
    return 'OTRO_PADRE_MISMO_ACTOR_SIN_ENLACE'


def pattern(row, following):
    text = row['Texto'].rstrip()
    rel = relation(row, following)
    if FOOTER.search(text):
        return 'PIE_EDITORIAL_LITERAL'
    if HEADER.search(text):
        return 'ENCABEZADO_LITERAL'
    if text.endswith(','):
        if rel == 'MISMO_PADRE_OTRO_ACTOR':
            return 'COMA_ANTES_DE_OTRO_ACTOR_EN_PADRE'
        if rel == 'OTRO_PADRE_ENLACE_EXISTENTE':
            return 'COMA_CON_ENLACE_YA_EXISTENTE'
        if rel == 'OTRO_PADRE_MISMO_ACTOR_SIN_ENLACE':
            return 'COMA_MISMO_ACTOR_SIN_ENLACE'
        return 'COMA_OTRO_CONTEXTO'
    # Una letra suelta puede ser conjunción real: esto NO diagnostica un error OCR.
    tail = re.search(r'[.!?]\s+([^.!?\n]{1,12})$', text)
    if tail and (len(tail[1].strip()) <= 2 or not tail[1].replace(' ', '').isalnum()):
        return 'COLA_BREVE_TRAS_PUNTUACION'
    if FUNCTION_WORD.search(text):
        return 'TERMINO_FUNCIONAL_ABIERTO'
    return 'OTRO_FINAL_SIN_PUNTUACION'


def previous_tail_clue(row, previous):
    """Coincidencia literal orientativa; nunca mover/completar la palabra hallada."""
    if not same_session(row, previous) or row['ID_Padre'] == previous['ID_Padre']:
        return ''
    text = row['Texto'].rstrip()
    if not re.search(r'ofrece la palabra', text, re.I):
        return ''
    endings = (('para proceder a la', ('votación',)),
               ('a los asistentes para', ('comentarios',)),
               ('comentarios sobre el escenario', ('interno', 'internacional')))
    for ending, words in endings:
        if text.lower().endswith(ending):
            for word in words:
                if re.search(r'[.!?]\s+' + re.escape(word) + r'\.\s*$', previous['Texto'], re.I):
                    return word
    return ''


def context(row):
    if not row:
        return None
    return {k: str(row[k])[:10] if k == 'Fecha' else row[k] for k in FIELDS}


def diagnose(rows):
    seen = set()
    for row in rows:
        if any(k not in row for k in FIELDS) or not isinstance(row['Texto'], str) or not row['Texto'].strip():
            raise ValueError('Fila incompleta o sin texto')
        if not row['ID_Intervencion'] or row['ID_Intervencion'] in seen:
            raise ValueError('ID_Intervencion vacío o duplicado')
        seen.add(row['ID_Intervencion'])
    result = []
    for i, row in enumerate(rows):
        if MOTIVE not in motives(row):
            continue
        prev = rows[i - 1] if i else None
        nxt = rows[i + 1] if i + 1 < len(rows) else None
        result.append(dict(
            ID_Intervencion=row['ID_Intervencion'], ID_Padre=row['ID_Padre'],
            Fecha=str(row['Fecha'])[:10], Actor=row['Actor_Final'],
            SHA256_Texto_Exportado=sha(row['Texto']),
            Categoria=pattern(row, nxt), Relacion_Siguiente=relation(row, nxt),
            Indicio_Cola_Anterior=previous_tail_clue(row, prev),
            Solo_Este_Motivo=motives(row) == {MOTIVE},
            Motivos_Adicionales=sorted(motives(row) - {MOTIVE}),
            Estado='CANDIDATO_NO_ADJUDICADO', Texto=row['Texto'],
            Anterior=context(prev), Siguiente=context(nxt),
            Aviso='Triaje, no lectura completa ni cierre de alertas. Contexto puede pertenecer a otra sesión; comparar fechas.'
        ))
    return result


def summarize(cases):
    only = [c for c in cases if c['Solo_Este_Motivo']]
    return dict(Filas_Con_Motivo=len(cases), Filas_Solo_Este_Motivo=len(only),
                Padres_Solo_Este_Motivo=len({c['ID_Padre'] for c in only}),
                Indicios_Cola_Anterior=[c['ID_Intervencion'] for c in cases if c['Indicio_Cola_Anterior']],
                Categorias_Todos=dict(sorted(collections.Counter(c['Categoria'] for c in cases).items())),
                Categorias_Solo_Este_Motivo=dict(sorted(collections.Counter(c['Categoria'] for c in only).items())),
                Limite='Categorías de triaje mutuamente excluyentes por prioridad, no causas confirmadas. Sin cambios de datos, curación, enlaces o alertas.')


def read_rows(path):
    with path.open('rb') as source:
        wb = openpyxl.load_workbook(source, read_only=True, data_only=True)
        try:
            it = wb['Consolidado'].values
            header = next(it)
            return [dict(zip(header, row)) for row in it]
        finally:
            wb.close()


def safe_output(path, source):
    path = path.resolve()
    if path == source.resolve():
        raise ValueError('No se puede sobrescribir la entrada')
    for folder in ('data', '.git', 'scripts', 'tests'):
        protected = ROOT / folder
        if path == protected or protected in path.parents:
            raise ValueError('Salida de diagnóstico fuera de datos, código y Git')
    path.mkdir(parents=True, exist_ok=True)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=ROOT / 'data/processed/consolidado_base_referencia.xlsx')
    parser.add_argument('--salida', type=Path, required=True, help='Directorio de diagnóstico, fuera de data/')
    args = parser.parse_args()
    output = safe_output(args.salida, args.base)
    # Evitar también un fichero de entrada situado dentro del directorio de salida.
    names = ('finales_candidatos.json', 'finales_candidatos.csv', 'finales_resumen.json')
    if args.base.resolve() in {(output / name).resolve() for name in names}:
        raise ValueError('La entrada coincide con una salida')
    cases = diagnose(read_rows(args.base))
    summary = dict(SHA256_Base=hashlib.sha256(args.base.read_bytes()).hexdigest(), **summarize(cases))
    (output / names[0]).write_text(json.dumps(cases, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / names[2]).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    fields = ('ID_Intervencion', 'ID_Padre', 'Fecha', 'Actor', 'SHA256_Texto_Exportado',
              'Categoria', 'Relacion_Siguiente', 'Solo_Este_Motivo', 'Motivos_Adicionales', 'Estado', 'Indicio_Cola_Anterior', 'Final', 'Inicio_Siguiente')
    with (output / names[1]).open('w', newline='', encoding='utf-8-sig') as target:
        writer = csv.DictWriter(target, fieldnames=fields, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for c in cases:
            writer.writerow({**{k: ';'.join(c[k]) if isinstance(c[k], list) else c[k] for k in fields if k in c},
                             'Final': c['Texto'][-240:], 'Inicio_Siguiente': c['Siguiente']['Texto'][:240] if c['Siguiente'] else ''})
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
