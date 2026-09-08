#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F0: cobertura mensual y consistencia de las decisiones de TPM.

Valida 132 sesiones 2005–2015, todas las fórmulas vigentes detectadas, su
etiqueta y TODOS los componentes parseados (tasa, delta y signo verbal).
La cardinalidad de actores se informa, no se fuerza a un número histórico.

La referencia CSV proviene de Datosmacro; su nombre histórico incluye BCCh,
pero no es una descarga directa del Banco Central. La asociación temporal
usa una ventana explícita de 10 días entre sesión y fecha efectiva.

Uso: python scripts/qa_gate_f0.py [base.xlsx] [tpm.csv] [--json reporte.json]
"""

import sys
import re
import csv
import datetime as dt
from pathlib import Path
from collections import Counter, defaultdict
from decision_rules import _is_current_decision

try:
    import openpyxl
except ImportError:
    sys.exit("Se requiere openpyxl (pip install openpyxl)")

_ROOT = Path(__file__).resolve().parent.parent
BASE = str(
    _ROOT / 'data' / 'processed' / 'consolidado_base_referencia.xlsx')
TPM_CSV = str(
    _ROOT / 'data' / 'external' / 'tpm_oficial_bcch.csv')
CONSEJO = 'Consejo del Banco Central de Chile'

# Ventana máxima (días) entre la reunión y la fecha efectiva de la nueva tasa
# para considerar que la sesión adoptó esa tasa.
CHANGE_WINDOW_DAYS = 10

# ---------------------------------------------------------------------------
# Normalización OCR: minúsculas sin acentos + colapso de espacios incrustados
# dentro de palabras clave ("monetari a" -> "monetaria", "anteri or" ->
# "anterior"; artefactos de la extracción del PDF).
# ---------------------------------------------------------------------------

def _soft(t):
    s = str(t).lower()
    for a, b in (('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('ñ','n'),('ü','u')):
        s = s.replace(a, b)
    return s

_OCR_WORDS = ('monetaria','anterior','politica','acuerdo','reunion','consejo','consejeros',
              'votacion','unanimidad','constancia','comunicado','interbancaria','mantener',
              'aumentar','reducir','puntos','siguiente','merito','virtud','hasta','anual')

def _fix_ocr(s):
    for w in _OCR_WORDS:
        s = re.sub(r'\s*'.join(w), w, s)
    return s

def _prep(t):
    return re.sub(r'\s+', ' ', _fix_ocr(_soft(t))).strip()

# ---------------------------------------------------------------------------
# Carga
# ---------------------------------------------------------------------------

def load_base(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb['Consolidado']
    it = ws.iter_rows(values_only=True)
    header = list(next(it))
    out = []
    for r in it:
        d = dict(zip(header, r))
        d['Fecha_dt'] = d['Fecha'].date() if isinstance(d['Fecha'], dt.datetime) else d['Fecha']
        d['Fecha_str'] = d['Fecha_dt'].isoformat()
        out.append(d)
    return out


def load_tpm(path):
    """[(fecha_efectiva date, tasa_pct float)] ordenado por fecha."""
    rows = []
    with open(path, newline='', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            y, m, d = r['fecha_efectiva'].split('-')
            rows.append((dt.date(int(y), int(m), int(d)), float(r['tasa_pct'])))
    import math
    if not rows or len({d for d,_ in rows}) != len(rows) or any(not math.isfinite(rate) or rate < 0 for _,rate in rows):
        raise ValueError('Referencia TPM vacía, duplicada o con tasas inválidas')
    rows.sort()
    return rows

# ---------------------------------------------------------------------------
# F0(b) — detección de la fila de decisión (patrones tolerantes a \s+,
# nunca con espacios literales: el texto extraído del PDF tiene saltos)
# ---------------------------------------------------------------------------

# Fórmula del acta/comunicado: "el Consejo ... acordó <verbo> la tasa ..." /
# "Se acuerda <verbo> la tasa ...". Variantes OCR: comas antes de "acordó",
# "del Banco Central" sin "de Chile", mayúsculas/minúsculas, la fórmula
# "resolvió, por unanimidad, mantener la tasa..." (2005-06-09), "el Consejo
# acuerda bajar la Tasa..." (2009) y "el Consejo decidió mantener la tasa..."
# (comunicados 2005), por lo que se toleran hasta 60 caracteres entre el
# verbo del acuerdo y la acción.
DECISION_VERB = r'(?:mantener|mantiene|aumentar|aumenta|aument[oó]|incrementar|incrementa|increment[oó]|elevar|eleva|elev[oó]|reducir|reduce|redujo|bajar|baja|baj[oó])'
DECISION_ROW_RE = re.compile(
    r'(?:se\s+acuerda|acuerda|acord[oó]|resolvi[oó]|decidi[oó])\s*[^.\n]{0,60}?' + DECISION_VERB +
    r'\s+(?:la\s+)?(?:tasa\s+de\s+(?:inter[eé]s\s+de\s+)?pol[íi]tica\s+monetaria|tpm)',
    re.I | re.S)
# Marcadores institucionales que suelen acompañar a la fila de decisión
DECISION_MARK_RE = re.compile(
    r'(adopta\s+el\s+siguiente\s+acuerdo|se\s+deja\s+constancia[^.]{0,120}acuerdo|'
    r'conforme\s+a\s+la\s+votaci[oó]n|en\s+m[ée]rito\s+de\s+lo\s+anterior|'
    r'en\s+virtud\s+de\s+lo\s+anterior|acuerdo\s+un[áa]nime)',
    re.I | re.S)


def extract_decision_rows(session_rows):
    """Filas candidatas a portar la decisión de TPM de la sesión.

    Se prefieren las filas con la fórmula de decisión ("el Consejo acordó/
    decidió/resolvió/acuerda <verbo> la tasa ...") sobre las que sólo traen
    marcadores de bloque de acuerdo (el marcador puede quedar en la fila del
    discurso del Presidente y la fórmula en la fila siguiente, p.ej.
    2007-06-14). La última candidata es, por regla general, la fila del
    acuerdo/constancia (el texto del COMUNICADO repite la fórmula al final).
    """
    formula, marks = [], []
    for d in session_rows:
        t = _prep(d.get('Texto') or '')
        if not _is_current_decision(t):
            continue
        if DECISION_ROW_RE.search(t):
            formula.append(d)
        elif DECISION_MARK_RE.search(t) and re.search(
                r'tasa\s+de\s+pol[íi]tica\s+monetaria|tpm', t):
            marks.append(d)
    return formula or marks

# ---------------------------------------------------------------------------
# F0(c) — parseo de la decisión (clause-aware)
# ---------------------------------------------------------------------------

NUM = r'(\d+(?:[.,]\d+)?)'
BP_RE = re.compile(r'\ben\s+' + NUM + r'\s*puntos\s+base', re.I)
# "en 0,25% hasta 3,5%": delta expresado en puntos porcentuales
PCT_DELTA_RE = re.compile(r'\ben\s+' + NUM + r'\s*%\s*(?=hasta|\ba\b)', re.I)
# "desde 5,25% a 5% anual"
DESDE_A_RE = re.compile(r'\bdesde\s+' + NUM + r'\s*%\s*a\s+' + NUM + r'\s*%', re.I)
TARGET_RE = re.compile(r'\b(?:hasta|a|en)\s+' + NUM + r'\s*%', re.I)

_VERB_SIGN = {
    'mantener': 0, 'mantiene': 0,
    'aumentar': 1, 'aumenta': 1, 'aumento': 1,
    'incrementar': 1, 'incrementa': 1, 'incremento': 1,
    'elevar': 1, 'eleva': 1, 'elevo': 1,
    'reducir': -1, 'reduce': -1, 'redujo': -1,
    'bajar': -1, 'baja': -1, 'bajo': -1,
}

_SENT_SPLIT = re.compile(r'(?<=[.!?\n])\s+')


def _decision_clauses(text):
    """Oraciones/bloques candidatos a contener la decisión (texto preparado
    con _prep: minúsculas, sin acentos, espacios OCR curados).

    Se prueban en orden inverso (el último bloque 'acuerdo'/COMUNICADO es el
    que contiene la fórmula vigente; los primeros suelen ser votaciones o
    menciones del mes anterior).
    """
    parts = [p.strip() for p in _SENT_SPLIT.split(_prep(text)) if p.strip()]
    return list(reversed(parts))


def _parse_clause(cl):
    """(verbo, delta_bps|None, target_pct|None) para una cláusula, o None."""
    m = DECISION_ROW_RE.search(cl)
    if not m:
        return None
    verb = None
    for tok in re.split(r'\s+', m.group(0)):
        t = tok.lower().strip(',;:("“')
        if t in _VERB_SIGN:
            verb = t
            break
    if verb is None:                      # p.ej. "acordó" + verbo separado por \n
        vm = re.search(DECISION_VERB, m.group(0), re.I)
        verb = vm.group(0).lower() if vm else None
    if verb is None:
        return None
    sign = _VERB_SIGN[verb]
    tail = cl[m.end():m.end() + 300]

    delta = None
    target = None
    dm = DESDE_A_RE.search(tail)
    if dm:
        old = float(dm.group(1).replace(',', '.'))
        new = float(dm.group(2).replace(',', '.'))
        target = new
        delta = round((new - old) * 100)
    else:
        bp = BP_RE.search(tail)
        pd = PCT_DELTA_RE.search(tail)
        if bp and sign != 0:
            delta = sign * int(float(bp.group(1).replace(',', '.')))
        elif pd and sign != 0:
            delta = sign * round(float(pd.group(1).replace(',', '.')) * 100)
        elif sign == 0:
            delta = 0                      # 'mantener': cualquier mención de pb es ruido
        tg = TARGET_RE.search(tail[pd.end():] if pd and sign != 0 else tail)
        if tg:
            target = float(tg.group(1).replace(',', '.'))
    return (verb, delta, target)


def parse_decision(text):
    """Parsea la decisión de TPM del texto de la fila.

    Recorre las cláusulas (último bloque 'acuerdo'/COMUNICADO primero) y
    retorna la primera que rinda un delta o una tasa objetivo.
    """
    for cl in _decision_clauses(text):
        got = _parse_clause(cl)
        if got and (got[1] is not None or got[2] is not None):
            return got
    return None

# ---------------------------------------------------------------------------
# F0(c) — expectativa oficial (fecha efectiva ≠ fecha de reunión)
# ---------------------------------------------------------------------------

def expected_after(tpm, meeting):
    """(antes_pct, despues_pct, delta_bps) según la historia oficial.

    La sesión adopta la siguiente tasa oficial sólo si su fecha efectiva es
    <= CHANGE_WINDOW_DAYS posterior a la reunión; si no, mantiene la tasa
    vigente en la fecha de la reunión.
    """
    before = None
    after = None
    for eff, rate in tpm:
        if eff <= meeting:
            before = rate
        elif meeting < eff <= meeting + dt.timedelta(days=CHANGE_WINDOW_DAYS):
            after = rate
            break
    if after is None:
        after = before
    delta = None if before is None else round((after - before) * 100)
    return before, after, delta

# ---------------------------------------------------------------------------
# Gate
# ---------------------------------------------------------------------------

def decision_matches_reference(decision, before, after, delta):
    """Todos los componentes disponibles deben concordar, incluido el signo verbal."""
    verb, parsed_delta, target = decision
    if before is None or after is None or delta is None:
        return False
    expected_sign = (delta > 0) - (delta < 0)
    if _VERB_SIGN[verb] != expected_sign:
        return False
    return ((parsed_delta is not None or target is not None)
            and (parsed_delta is None or parsed_delta == delta)
            and (target is None or abs(target - after) < 1e-8))


def audit(rows, tpm):
    errors = []
    counts = Counter(r['Actor_Final'] for r in rows)
    # La cardinalidad es descriptiva: no fuerza a mantener errores de nombres
    # para alcanzar un número prefijado. El registro canónico se valida en F1.
    if not counts.get(CONSEJO) or any(not a for a in counts):
        errors.append('Actor vacío o Consejo ausente')
    by_session = defaultdict(list)
    for r in rows:
        by_session[r['Fecha_str']].append(r)
    expected_months = {f'{y}-{m:02d}' for y in range(2005, 2016) for m in range(1,13)}
    if len(by_session) != 132 or {s[:7] for s in by_session} != expected_months:
        errors.append('Cobertura incompleta: se esperan 132 sesiones mensuales 2005–2015')
    decisions = []
    for session, group in sorted(by_session.items()):
        candidates = extract_decision_rows(group)
        if not candidates:
            errors.append(f'{session}: sin decisión vigente detectable')
            continue
        before, after, delta = expected_after(tpm, dt.date.fromisoformat(session))
        values = []
        for row in candidates:
            if row.get('Tipo_Acta') != 'ACUERDO_CONSEJO':
                errors.append(f'{session} ID {row["ID"]}: decisión sin tipificar')
            # Examinar todas las fórmulas en cada candidata, no sólo la última.
            clauses = _decision_clauses(row['Texto'])
            for clause in clauses:
                if not DECISION_ROW_RE.search(clause):
                    continue
                # Una recapitulación puede convivir con el acuerdo vigente.
                from decision_rules import RECAP_LEAD_RE
                matches = list(DECISION_ROW_RE.finditer(clause))
                for index, match in enumerate(matches):
                    if RECAP_LEAD_RE.search(clause[max(0, match.start()-240):match.start()]):
                        continue
                    end = matches[index+1].start() if index+1 < len(matches) else len(clause)
                    parsed = _parse_clause(clause[match.start():end])
                    if parsed and (parsed[1] is not None or parsed[2] is not None):
                        values.append((row['ID'], parsed))
                        if not decision_matches_reference(parsed, before, after, delta):
                            errors.append(f'{session} ID {row["ID"]}: {parsed} vs referencia {(before, after, delta)}')
                    else:
                        errors.append(f'{session} ID {row["ID"]}: fórmula no parseable')
            if not any(rid == row['ID'] for rid, _ in values):
                errors.append(f'{session} ID {row["ID"]}: candidata no parseable')
        if values:
            decisions.append({'Fecha': session, 'Tasa_Antes': before, 'Tasa_Despues': after,
                              'Delta_PB': delta, 'IDs_Evidencia': sorted({rid for rid,_ in values}),
                              'Formulas_Contrastadas': len(values)})
    return {'sesiones': len(by_session), 'actores': len(counts),
            'personas': len(counts)-int(CONSEJO in counts),
            'decisiones': decisions, 'errores': errors, 'pasa': not errors}


def main():
    import json
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('base', nargs='?', default=str(_ROOT/'data/processed/consolidado_base_referencia.xlsx'))
    parser.add_argument('tpm', nargs='?', default=str(_ROOT/'data/external/tpm_oficial_bcch.csv'))
    parser.add_argument('--json', dest='json_path')
    args = parser.parse_args()
    result = audit(load_base(args.base), load_tpm(args.tpm))
    print(f"Sesiones: {result['sesiones']} | Actores: {result['actores']}")
    print(f"Sesiones con evidencia parseada: {len(result['decisiones'])}")
    print(f"Fórmulas contrastadas: {sum(d['Formulas_Contrastadas'] for d in result['decisiones'])}")
    for error in result['errores']:
        print('ERROR:', error)
    print('== VEREDICTO F0:', 'PASA' if result['pasa'] else 'FALLA', '==')
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return 0 if result['pasa'] else 1


if __name__ == '__main__':
    sys.exit(main())
