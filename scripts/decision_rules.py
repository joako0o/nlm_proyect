"""Reglas compartidas de decisión vigente; excluyen recapitulaciones históricas."""
import re

def _soft(t):
    """minúsculas sin acentos (mantiene saltos de línea)."""
    s=str(t).lower()
    for a,b in (('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('ñ','n'),('ü','u')):
        s=s.replace(a,b)
    return s

_OCR_WORDS=('monetaria','anterior','politica','acuerdo','reunion','consejo','consejeros',
            'votacion','unanimidad','constancia','comunicado','interbancaria','mantener',
            'aumentar','reducir','puntos','siguiente','merito','virtud')

def _fix_ocr(s):
    """Colapsa espacios OCR incrustados dentro de palabras clave (p.ej.
    'monetari a' -> 'monetaria', 'anteri or' -> 'anterior')."""
    for w in _OCR_WORDS:
        s=re.sub(r'\s*'.join(w), w, s)
    return s
_ACCORD_VERB = r'(?:acuerda|acord[oó]|resolvi[oó]|decidi[oó])'
_ACTION_VERB = (r'(?:mantener|mantiene|aumentar|aumenta|aumentó|incrementar|incrementa|incrementó|'
                r'elevar|eleva|elevó|reducir|reduce|redujo|bajar|baja|bajó)')
_TASA_RE = r'(?:la\s+)?(?:tasa\s+de\s+(?:inter[ée]s\s+de\s+)?pol[íi]tica\s+monetaria|tpm)'
# Fórmula canónica del acta/comunicado vigente: "En su reunión mensual de
# política monetaria, el Consejo (del Banco Central ...),? (acordó|decidió|
# resolvió|acuerda) <verbo> la tasa ..."
DECISION_FORMULA_RE = re.compile(
    r'en\s+su\s+reuni[oó]n\s+mensual\s+de\s+pol[íi]tica\s+monetaria\s*,?\s*el\s+consejo[^.\n]{0,80}?'
    + _ACCORD_VERB + r'\s*[^.\n]{0,60}?' + _ACTION_VERB + r'\s+' + _TASA_RE,
    re.I | re.S)
# Fórmula del acta 2005: "Se acuerda <verbo> la tasa de interés de política monetaria ..."
SE_ACUERDA_RE = re.compile(
    r'se\s+acuerda\s*[^.\n]{0,60}?' + _ACTION_VERB + r'\s+' + _TASA_RE, re.I | re.S)
# Verbo de acuerdo genérico, sin la fórmula completa (variantes de votación)
DECISION_ACTION_RE = re.compile(
    _ACCORD_VERB + r'\s*[^.\n]{0,60}?' + _ACTION_VERB + r'\s+' + _TASA_RE, re.I | re.S)
# Bloques de acuerdo del acta que acompañan a la decisión vigente
ACUERDO_BLOCK_RE = re.compile(
    r'(siguiente\s+acuerdo|en\s+m[ée]rito\s+de\s+lo\s+anterior|conforme\s+a\s+la\s+votaci[oó]n|'
    r'en\s+virtud\s+de\s+lo\s+anterior|se\s+deja\s+constancia|acuerdo\s+un[áa]nime|'
    r'por\s+votaci[oó]n\s+un[áa]nime|por\s+(?:la\s+)?unanimidad|unanimidad\s+de\s+sus\s+miembros)',
    re.I)
# Recapitulaciones de la decisión de un mes anterior: "En la última
# Reunión...", "En la reunión de política monetaria de <mes>...", "...desde
# la Reunión celebrada en el mes de <mes>..." (presentación de Opciones).
RECAP_LEAD_RE = re.compile(
    r'(?:[úu]ltima\s+reuni|reuni[oó]n\s+de\s+pol[íi]tica\s+monetaria\s+de\s+'
    r'(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre)'
    r'|reuni[oó]n\s+celebrada\s+en\s+el\s+mes\s+de|mes\s+(?:anterior|pasado))', re.I)

def _is_current_decision(text):
    """True si la fila porta la decisión de TPM de la SESIÓN (verbo de
    acuerdo sobre la tasa), no citas de decisiones de meses anteriores.
    Aplica a filas institucionales (ACUERDO/COMUNICADO) y a filas de persona
    que arrastran el bloque del acuerdo (típico 2013-2015, donde el acuerdo
    va pegado al discurso de cierre del Presidente)."""
    t=_fix_ocr(_soft(text))
    if DECISION_FORMULA_RE.search(t) or SE_ACUERDA_RE.search(t):
        return True
    for m in DECISION_ACTION_RE.finditer(t):
        pre=t[max(0,m.start()-240):m.start()]
        if RECAP_LEAD_RE.search(pre):
            continue
        ctx=t[max(0,m.start()-240):m.start()+240]
        if ACUERDO_BLOCK_RE.search(ctx):
            return True
    return False

