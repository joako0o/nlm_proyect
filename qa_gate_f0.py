#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F0 QA gate — Base de referencia RPM (consolidado_base_referencia.xlsx)
======================================================================

F0(a) Cardinalidad de actores
     Actor_Final únicos y su frecuencia. El plan original decía 60–80;
     la cardinalidad real del consolidado es ~51 (verificar).

F0(b) Decisión de TPM por sesión
     Cada una de las 132 sesiones debe rendir exactamente UNA decisión
     (verbo + Δ pb y/o tasa objetivo). La fila que porta la decisión debe
     estar tipificada Tipo_Acta='ACUERDO_CONSEJO'; las que no lo están son
     "mis-tipificadas".

F0(c) Contraste contra la historia oficial de TPM del BCCh
     tpm_oficial_bcch.csv  (fecha_efectiva,tasa_pct,fuente).
     OJO: fecha_efectiva es la fecha en que la tasa COMIENZA A REGIR (por
     regla general, el día hábil siguiente a la reunión), no la fecha de la
     reunión. Por eso la sesión sólo adopta la siguiente tasa oficial si su
     fecha efectiva cae dentro de CHANGE_WINDOW_DAYS tras la reunión; en caso
     contrario mantiene la tasa vigente.

Uso:  python qa_gate_f0.py [base.xlsx] [tpm_oficial_bcch.csv]
"""

import sys
import re
import csv
import datetime as dt
from collections import Counter, defaultdict

try:
    import openpyxl
except ImportError:
    sys.exit("Se requiere openpyxl (pip install openpyxl)")

BASE = sys.argv[1] if len(sys.argv) > 1 else 'consolidado_base_referencia.xlsx'
TPM_CSV = sys.argv[2] if len(sys.argv) > 2 else 'tpm_oficial_bcch.csv'
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
    return _fix_ocr(_soft(t))

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
DECISION_VERB = r'(?:mantener|mantiene|aumentar|aumenta|aumentó|incrementar|incrementa|incrementó|elevar|eleva|elevó|reducir|reduce|redujo|bajar|baja|bajó)'
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
    'aumentar': 1, 'aumenta': 1, 'aumentó': 1,
    'incrementar': 1, 'incrementa': 1, 'incrementó': 1,
    'elevar': 1, 'eleva': 1, 'elevó': 1,
    'reducir': -1, 'reduce': -1, 'redujo': -1,
    'bajar': -1, 'baja': -1, 'bajó': -1,
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
        tg = TARGET_RE.search(tail)
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

def main():
    rows = load_base(BASE)
    tpm = load_tpm(TPM_CSV)
    print(f"Base: {BASE}  ({len(rows):,} filas)")
    print(f"TPM oficial: {TPM_CSV}  ({len(tpm)} cambios, "
          f"{tpm[0][0]} → {tpm[-1][0]})")
    print()

    # ---------------- F0(a) ----------------
    # Cardinalidad verificada: 51 valores de Actor_Final = 50 personas + el
    # Consejo (filas institucionales). El plan original decía 60–80: incorrecto.
    EXPECTED_PERSONS = 50
    counts = Counter(r['Actor_Final'] for r in rows)
    persons = {a: n for a, n in counts.items() if a != CONSEJO}
    print('== F0(a) Cardinalidad de actores ==')
    print(f"   Valores de Actor_Final: {len(counts)} "
          f"({len(persons)} personas + Consejo)")
    print(f"   Filas del Consejo (institucionales): {counts.get(CONSEJO, 0)}")
    n1 = sorted(a for a, n in persons.items() if n == 1)
    print(f"   Actores con n=1: {len(n1)} -> {', '.join(n1)}")
    print()

    by_sess = defaultdict(list)
    for r in rows:
        by_sess[r['Fecha_str']].append(r)
    sessions = sorted(by_sess)
    print(f"Sesiones: {len(sessions)}  ({sessions[0]} → {sessions[-1]})")

    # ---------------- F0(b) ----------------
    print()
    print('== F0(b) Decisión por sesión ==')
    missing, mistyped, parsed, no_parse = [], [], {}, []
    for s in sessions:
        cands = extract_decision_rows(by_sess[s])
        if not cands:
            missing.append(s)
            continue
        last = cands[-1]
        if (last.get('Tipo_Acta') or '') != 'ACUERDO_CONSEJO':
            mistyped.append((s, last['ID'], last.get('Tipo_Acta') or '',
                             last['Actor_Final']))
        dec = parse_decision(str(last['Texto']))
        if dec is None:                    # reintenta con las candidatas previas
            for c in reversed(cands[:-1]):
                dec = parse_decision(str(c['Texto']))
                if dec:
                    break
        if dec is None:
            no_parse.append((s, last['ID']))
        else:
            parsed[s] = dec
    print(f"   Sesiones sin fila de decisión detectable: {len(missing)}"
          + (f" -> {missing}" if missing else ''))
    print(f"   Sesiones con decisión parseada: {len(parsed)}/{len(sessions)}")
    print(f"   Filas de decisión mis-tipificadas (última candidata sin "
          f"ACUERDO_CONSEJO): {len(mistyped)}")
    for s, rid, t, act in mistyped:
        print(f"      {s}  ID {rid}  tipo='{t}'  actor={act}")
    if no_parse:
        print(f"   NO_PARSE: {no_parse}")
    print()

    # ---------------- F0(c) ----------------
    print('== F0(c) Contraste contra TPM oficial BCCh ==')
    print(f"   CHANGE_WINDOW_DAYS = {CHANGE_WINDOW_DAYS}")
    mism, ok, compared = [], 0, 0
    for s in sessions:
        if s not in parsed:
            continue
        meeting = dt.date.fromisoformat(s)
        before, after, odelta = expected_after(tpm, meeting)
        verb, bdelta, btarget = parsed[s]
        compared += 1
        ok_target = btarget is not None and abs(btarget - after) < 1e-9
        ok_delta = bdelta is not None and odelta is not None and bdelta == odelta
        if ok_target or ok_delta:
            ok += 1
        else:
            rid = extract_decision_rows(by_sess[s])[-1]['ID']
            mism.append((s, rid, verb, bdelta, btarget, before, after, odelta))
    print(f"   Sesiones contrastadas: {compared}   OK: {ok}   "
          f"Discrepancias: {len(mism)}")
    for (s, rid, verb, bd, bt, b, a, od) in mism:
        parts = [f"{s}  ID {rid}  '{verb}'"]
        if bd is not None or bt is not None:
            if bd is not None:
                parts.append(f"delta base={bd:+d}" if bd else "delta base=+0")
            if bt is not None:
                parts.append(f"tasa base={bt:.2f}")
        else:
            parts.append("base=NO_PARSE")
        parts.append(f"vs oficial: antes={b:.2f} despues={a:.2f} "
                     f"delta={od:+d}" if od is not None else "vs oficial: n/d")
        print('      ' + '  |  '.join(parts))
    print()

    # ---------------- veredicto ----------------
    fail = (len(persons) != EXPECTED_PERSONS or missing or no_parse
            or mistyped or mism)
    print('== VEREDICTO F0:', 'FALLA' if fail else 'PASA', '==')
    print(f"   F0(a) {'OK' if len(persons)==EXPECTED_PERSONS else 'FALLA'}: "
          f"{len(persons)} personas + Consejo = {len(counts)} valores de "
          f"Actor_Final (plan decía 60–80 -> corregir)")
    print(f"   F0(b) {'OK' if not (missing or no_parse or mistyped) else 'FALLA'}: "
          f"0 sin decisión, {len(mistyped)} mis-tipificadas, "
          f"{len(no_parse)} sin parsear")
    print(f"   F0(c) {'OK' if not mism else 'FALLA'}: {len(mism)} discrepancias "
          f"reales contra la historia oficial")
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
