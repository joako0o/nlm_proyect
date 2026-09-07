# -*- coding: utf-8 -*-
"""
Lista de cargos (roster) por sesión RPM, extraída del primer párrafo de cada
acta ("bajo la presidencia ... Asiste ... Asisten también ...").

Cada sesión queda como {nombre_normalizado: cargo_bruto}. La función
`canonical_role` normaliza variantes y aplica género (Consejero/a).
La función `match_role` resuelve con coincidencia estricta y, si la
coincidencia es única, la devuelve; en ambigüedad devuelve None.
"""
import re
import unicodedata

NAME_TOKEN = r"[A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñü']+(?:\s+[A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñü']+)*"
HONOR = r"(?:don|doña|señor|señora|sr\.|sra\.|srta\.|senor|senora)"

FEMALE_NAMES = {
    "María Elena Ovalle Molina",
    "María Eugenia Wagner Brizzi",
    "María Olivia Recart Herrera",
    "Gloria Peña Tapia",
    "Cecilia Feliú Carrizo",
    "Bernardita Piedrabuena Keymer",
    "Tatiana Vargas Manzo",
}

ROLE_PATTERNS = [
    ("Gerente de División Política Financiera Subrogante", None),
    ("Gerente de División Operaciones Financieras (S)", None),
    ("Gerente de División Mercados Financieros", None),
    ("Gerente de Mercados Financieros Nacionales", None),
    ("Gerente de División Política Financiera", None),
    ("Gerente de División Operaciones Financieras", None),
    ("Gerente de División Estadísticas", None),
    ("Gerente de División Estudios Subrogante", None),
    ("Gerente de División Estudios", None),
    ("Gerente de División Internacional", None),
    ("Gerente de Información e Investigación Estadística", None),
    ("Gerente de Investigación Económica (S)", None),
    ("Gerente de Investigación Económica", None),
    ("Gerente de Investigación Financiera", None),
    ("Gerente de Estabilidad Financiera Subrogante", None),
    ("Gerente de Estabilidad Financiera", None),
    ("Gerente de Análisis Macroeconómico Subrogante", None),
    ("Gerente de Análisis Macroeconómico Interino", None),
    ("Gerente de Análisis Macroeconómico", None),
    ("Gerente de Análisis Internacional Subrogante", None),
    ("Gerente de Análisis Internacional", None),
    ("Gerente de Estrategia y Comunicación de Política Monetaria", None),
    ("Gerente de Modelación y Análisis Económico", None),
    ("Gerente Asesor de Comunicaciones", None),
    ("Gerente de Mercados Nacionales", None),
    ("Gerente de Operaciones Monetarias", None),
    ("Gerente de Operaciones Financieras", None),
    ("Gerente General", None),
    ("Subgerente General", None),
    ("Ministro de Hacienda Subrogante", "Ministro de Hacienda (S)"),
    ("Ministra de Hacienda Subrogante", "Ministra de Hacienda (S)"),
    ("Ministro de Hacienda (S)", "Ministro de Hacienda (S)"),
    ("Ministra de Hacienda (S)", "Ministra de Hacienda (S)"),
    ("Ministro de Hacienda", "Ministro de Hacienda"),
    ("Ministra de Hacienda", "Ministra de Hacienda"),
    ("Subsecretario de Hacienda", "Subsecretario de Hacienda"),
    ("Secretario General", "Secretario General"),
    ("Secretaria Ejecutiva Gabinete de la Presidencia", "Secretaria Ejecutiva Gabinete de la Presidencia"),
    ("Secretaria Ejecutiva del Gabinete de la Presidencia", "Secretaria Ejecutiva Gabinete de la Presidencia"),
    ("Fiscal y Ministro de Fe Subrogante", "Fiscal y Ministro de Fe (S)"),
    ("Fiscal y Ministro de Fe", "Fiscal y Ministro de Fe"),
    ("Jefe del Departamento Análisis Internacional", "Jefe del Departamento Análisis Internacional"),
    ("Jefe de Departamento Análisis Internacional", "Jefe del Departamento Análisis Internacional"),
    ("Asesor del Ministro de Hacienda", "Asesor del Ministro de Hacienda"),
    ("Asesor del Ministerio de Hacienda", "Asesor del Ministerio de Hacienda"),
    ("Asesora Macroeconómica del Ministerio de Hacienda", "Asesora Macroeconómica del Ministerio de Hacienda"),
    ("Economista Senior de la Gerencia de Investigación Económica", "Economista Sénior de la Gerencia de Investigación Económica"),
    ("Economista Sénior de la Gerencia de Investigación Económica", "Economista Sénior de la Gerencia de Investigación Económica"),
]
ROLE_PATTERNS.sort(key=lambda x: -len(x[0]))

# variantes -> forma canónica
CANON = {
    "gerente de division de estudios": "Gerente de División Estudios",
    "gerente de division de operaciones financieras": "Gerente de División Operaciones Financieras",
    "jefe de departamento analisis internacional": "Jefe del Departamento Análisis Internacional",
    "gerente de mercados nacionales": "Gerente de Mercados Nacionales",
}


def nz(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s)).strip()


def canonical_role(role, name=None):
    r = re.sub(r"\s+", " ", str(role).replace("\u2013", "-")).strip().rstrip(".")
    r = r.replace("Ministro de Hacienda Subrogante", "Ministro de Hacienda (S)")
    r = r.replace("Ministra de Hacienda Subrogante", "Ministra de Hacienda (S)")
    r = re.sub(r"(?i)\bsubrogante\b", "(S)", r)
    if r.lower() == "consejero/a":
        if name and nz(name) in {nz(x) for x in FEMALE_NAMES}:
            return "Consejera"
        return "Consejero"
    return CANON.get(nz(r), r)


def parse_opening(text):
    t = re.sub(r"\s+", " ", str(text).replace("\n", " "))
    m = re.search(r"En\s+Santiago\s+de\s+Chile", t, re.I)
    if not m:
        return {}
    fm = re.search(r"(?:I\.|1\.)\s*Fecha\s+Sesi", t, re.I)
    block = t[m.start(): fm.start() if fm else m.start() + 12000]

    roster = {}
    pm = re.search(
        r"bajo\s+la\s+presidencia\s+del\s+titular\s+" + HONOR + r"\s+(" + NAME_TOKEN + r")",
        block, re.I,
    )
    if pm:
        roster[nz(pm.group(1))] = "Presidente del Banco Central"

    vm = re.search(
        r"con\s+la\s+asistencia\s+del\s+Vicepresidente\s+" + HONOR + r"\s+(" + NAME_TOKEN + r")",
        block, re.I,
    )
    if vm:
        roster[nz(vm.group(1))] = "Vicepresidente del Banco Central"

    cm = re.search(
        r"de\s+los\s+Consejeros\s+(?:señores\s+)?(.+?)(?:\.\s*(?:Asiste|Ministro|Gerente|Asisten)|\.\s*$)",
        block, re.I,
    )
    if cm:
        for nm in re.findall(HONOR + r"\s+(" + NAME_TOKEN + r")", cm.group(1), re.I):
            if nz(nm):
                roster[nz(nm)] = "Consejero/a"

    for pat, canon in ROLE_PATTERNS:
        cre = re.compile(re.escape(pat) + r"[\s,;.\-]*" + HONOR + r"\s+(" + NAME_TOKEN + r")", re.I)
        for mm in cre.finditer(block):
            name = mm.group(1).strip().rstrip(",").strip()
            key = nz(name)
            if not key or key in roster:
                continue
            roster[key] = canonical_role(canon or pat, name)
    return roster


def build_rosters(rows_by_date_openers):
    """rows_by_date_openers: {fecha: texto_apertura}"""
    return {date: parse_opening(text) for date, text in rows_by_date_openers.items()}


def _loose(actor_norm):
    """Tokens sueltos: quita guiones para poder comparar 'schmidt' con 'schmidt-hebbel'."""
    return set(re.sub(r"[-']", " ", actor_norm).split())


def match_role(roster, actor):
    an = nz(actor)
    if not an:
        return None
    toks = an.split()

    # exacto completo
    e = [k for k in roster if k == an]
    if len(e) == 1:
        return roster[e[0]]

    def one(keys):
        q = [roster[k] for k in keys if k in roster and roster[k]]
        return q[0] if len(q) == 1 else None

    # apellidos últimos / primero+último
    if len(toks) >= 2:
        v = one([k for k in roster if k == " ".join(toks[-2:])])
        if v:
            return v
        v = one([k for k in roster if k == toks[0] + " " + toks[-1]])
        if v:
            return v
    v = one([k for k in roster if toks and k == toks[-1]])
    if v:
        return v

    # coincidencia laxa sin guiones: primer nombre + algún otro token; única
    loose = _loose(an)
    cand = []
    for k, role in roster.items():
        kt = _loose(k)
        if an in k or k in an:
            cand.append((k, role))
        elif toks and an.split()[0] == k.split()[0] and len(loose & kt) >= 2:
            cand.append((k, role))
    if len(cand) == 1:
        return cand[0][1]
    return None
