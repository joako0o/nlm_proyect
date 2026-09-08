# -*- coding: utf-8 -*-
"""
Base de referencia del consolidado RPM v2.
- Re-etiqueta hablante solo cuando el texto lo confirma.
- Corrige roles (Hacienda/subrogante y rol explicito).
- Fecha real + Id_Sesion + taxonomia canonica + flags.
"""
from procedural import is_formula, load_formula_reviews, FORMULA_REVIEWS
from curation import normalize_quote
import openpyxl, re, collections, datetime as dt
from pathlib import Path as _Path
from turns import TurnDetector, normalize as normalize_turn
from review_flags import review_reasons
from context_warnings import load_context_warnings, contextual_motives
from institutional_reviews import load_institutional_reviews, institutional_parts, institutional_type, NOTE as INSTITUTIONAL_NOTE
from curation import load_role_reviews, load_speaker_reviews, speaker_intervals, SPEAKER_REVIEW_SOURCE
from document_reviews import (load_document_reviews, document_parts, AUTHOR_SOURCE, READER_SOURCE,
                              ROLE_SOURCE as DOCUMENT_ROLE_SOURCE, DOCUMENT_TYPE)
from reviewed_continuity import load_reviewed_links
from continuity import continuation_start, annotate_turns, update_state, EXPLICIT, CONTINUED, boundary
from roster import ROLE_PATTERNS as ROSTER_ROLES
from roster import build_rosters as _build_rosters, match_role as _match_role, canonical_role as _canonical_role

# Rutas ancladas a la raíz del repositorio (el script vive en scripts/).
from paths import REPO, DATA_RAW, DATA_EXT, DATA_PROC
SRC=str(DATA_RAW/'consolidado_final.xlsx'); OUT=str(DATA_PROC/'consolidado_base_referencia.xlsx')
TEXTOS_COMPLETOS=DATA_PROC/'textos_completos.jsonl'
wb=openpyxl.load_workbook(SRC, data_only=True, read_only=True)
ws=wb['Consolidado']; data=list(ws.iter_rows(values_only=True))[1:]

CONSEJO='Consejo del Banco Central de Chile'
PSEUDO={'Gerente de División Internacional','Gerente de División Estudios Subrogante','Gerente de Investigación Económica','Gerente de Operaciones Financieras','Gerente de Área Técnica','Gerente de Estabilidad Financiera'}
EXTRA_ACTORS={'María Eugenia Wagner Brizzi','Rodrigo Alfaro','Rodrigo Álvarez Zenteno',
              'Alejandro Micco','Leonardo Hernández Tagle','Alfredo Pistelli',
              'Gloria Peña Tapia','Luis Alberto Álvarez Vallejos',
              'Miguel Ángel Nacrur Gazali','Pablo Mattar Oyarzún','Juan Pablo Araya Marco'}
ALL_ACTORS=sorted(set(str(r[2]).strip() for r in data)|EXTRA_ACTORS)
REAL=[a for a in ALL_ACTORS if a not in PSEUDO and a!=CONSEJO]

def norm(s):
    s=str(s).lower()
    for a,b in [('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('ñ','n'),('ü','u')]:
        s=s.replace(a,b)
    return re.sub(r'\s+',' ',s.strip())

def to_date_str(v):
    if isinstance(v,(dt.datetime,dt.date)):
        return v.strftime('%Y-%m-%d')
    return str(v).strip()[:10]

ROLE_PATS = [
 ('Ministra de Hacienda Subrogante','Ministra de Hacienda (S)'),
 ('Ministro de Hacienda Subrogante','Ministro de Hacienda (S)'),
 ('Ministra de Hacienda','Ministra de Hacienda'),
 ('Ministro de Hacienda','Ministro de Hacienda'),
 ('Subsecretario de Hacienda','Subsecretario de Hacienda'),
 ('Presidente del Banco Central','Presidente del Banco Central'),
 ('Vicepresidente del Banco Central','Vicepresidente del Banco Central'),
 ('Consejera','Consejera'),
 ('Consejero','Consejero'),
 ('Gerente de Análisis Macroeconómico Interino','Gerente de Análisis Macroeconómico Interino'),
 ('Gerente de Análisis Macroeconómico','Gerente de Análisis Macroeconómico'),
 ('Gerente de Análisis Internacional Subrogante','Gerente de Análisis Internacional Subrogante'),
 ('Gerente de Análisis Internacional','Gerente de Análisis Internacional'),
 ('Gerente de División Operaciones Financieras (S)','Gerente de División Operaciones Financieras (S)'),
 ('Gerente de División Operaciones Financieras','Gerente de División Operaciones Financieras'),
 ('Gerente de División Mercados Financieros','Gerente de División Mercados Financieros'),
 ('Gerente de División Estudios Subrogante','Gerente de División Estudios Subrogante'),
 ('Gerente de División Estudios','Gerente de División Estudios'),
 ('Gerente de División Política Financiera','Gerente de División Política Financiera'),
 ('Gerente de División Internacional','Gerente de División Internacional'),
 ('Gerente de División Estadísticas','Gerente de División Estadísticas'),
 ('Gerente de Investigación Económica (S)','Gerente de Investigación Económica (S)'),
 ('Gerente de Investigación Económica','Gerente de Investigación Económica'),
 ('Gerente de Investigación Financiera','Gerente de Investigación Financiera'),
 ('Gerente de Estabilidad Financiera Subrogante','Gerente de Estabilidad Financiera Subrogante'),
 ('Gerente de Estabilidad Financiera','Gerente de Estabilidad Financiera'),
 ('Gerente de Mercados Financieros Nacionales','Gerente de Mercados Financieros Nacionales'),
 ('Gerente de Mercados Financieros','Gerente de Mercados Financieros'),
 ('Gerente de Mercados Nacionales','Gerente de Mercados Nacionales'),
 ('Gerente de Estrategia y Comunicación de Política Monetaria','Gerente de Estrategia y Comunicación de Política Monetaria'),
 ('Gerente de Modelación y Análisis Económico','Gerente de Modelación y Análisis Económico'),
 ('Gerente de Área Técnica','Gerente de Área Técnica'),
 ('Economista Senior','Economista Senior'),
 ('Economista Sénior','Economista Sénior'),
 ('Gerente de Operaciones Monetarias','Gerente de Operaciones Monetarias'),
 ('Gerente de Operaciones Financieras','Gerente de Operaciones Financieras'),
 ('Gerente de Información e Investigación Estadística','Gerente de Información e Investigación Estadística'),
 ('Jefe del Departamento Análisis Internacional','Jefe del Departamento Análisis Internacional'),
 ('Jefe de Departamento Análisis Internacional','Jefe del Departamento Análisis Internacional'),
 ('Asesor del Ministerio de Hacienda','Asesor del Ministerio de Hacienda'),
 ('Asesor del Ministro de Hacienda','Asesor del Ministro de Hacienda'),
 ('Gerente General','Gerente General'),
 ('Presidente','Presidente del Banco Central'),
 ('Vicepresidente','Vicepresidente del Banco Central'),
 ('Ministro','Ministro de Hacienda'),
 ('Ministra','Ministra de Hacienda'),
]

VERBS=['señala','indica','manifiesta','expresa','dice','comenta','interviene','estima','consulta','afirma','responde','agrega','agregar','precisa','plantea','pregunta','informa','expone','menciona','hace presente','continúa','prosigue','solicita','opina','acota','destaca','recuerda','observa','concluye','inicia','apoya','coincide','agradece','aclara','considera','señalando','planteando','comentando','ofrece la palabra','concede la palabra','da la palabra','da comienzo','informa que','manifiesta estar','deja planteado','formula','señalando que','hace presente que','fija','da cuenta','explica','explica que','explicó','explicando','señaló','manifestó','indicó','expresó','comentó','preguntó','respondió','agregó','precisó','planteó','subrayó','recalcó','advirtió','destacó','da inicio','da inicio a','dio inicio','dio inicio a','piensa','piensa que','cree','considera','acepta','refiriéndose','refiere','se refiere','refiriéndose a','transmite','comienza','inicia su','inicia la']
VERBS += ['sostiene','confirma','apunta','argumenta','reconoce','describe','analiza','desarrolla',
 'expone','presenta','explicita','puntualiza','formula','contesta','propone','sugiere','señalando',
 'indicando','manifestando','expresando','acotando','precisando','destacando','comentando','hacen presente',
 'hizo presente','hace ver','presenta las opciones','tiene la impresion','se pregunta']
VNORM=[norm(v) for v in VERBS]

SURNAME={
 'Vittorio Corbo Lioi':'corbo','José De Gregorio Rebeco':'de gregorio','Manuel Marfán Lewis':'marfan',
 'Sebastián Claro Edwards':'claro','Claudio Soto Gamboa':'soto','Sergio Lehmann Beresi':'lehmann',
 'Enrique Marshall Rivera':'marshall','Pablo García Silva':'garcia','Rodrigo Vergara Montes':'vergara',
 'Luis Óscar Herrera Barriga':'herrera','Joaquín Vial Ruiz-Tagle':'vial','Miguel Fuentes Díaz':'fuentes',
 'Rodrigo Valdés Pulido':'valdes','Jorge Desormeaux Jiménez':'desormeaux','Andrés Velasco Brañes':'velasco',
 'Beltrán de Ramón Acevedo':'de ramon','Alberto Naudon Dell\'Oro':'naudon','Kevin Cowan Logan':'cowan',
 'Igal Magendzo Weinberger':'magendzo','Esteban Jadresic Marinovic':'jadresic','Nicolás Eyzaguirre Guzmán':'eyzaguirre',
 'Diego Gianelli Gómez':'gianelli','Matías Bernier Bórquez':'bernier','Felipe Larraín Bascuñán':'larrain',
 'Ricardo Vicuña Poblete':'vicuna','Klaus Schmidt-Hebbel Dunker':'schmidt-hebbel','Claudio Raddatz Kiefer':'raddatz',
 'Luis Felipe Céspedes Cifuentes':'cespedes','María Elena Ovalle Molina':'ovalle','Alberto Arenas de Mesa':'arenas',
 'María Olivia Recart Herrera':'recart','Luis Opazo Roco':'opazo','Rodrigo Cerda Norambuena':'cerda',
 'Mario Marcel Cullell':'marcel','Miguel Ricaurte Bermúdez':'ricaurte','Camilo Carrasco Alfonso':'carrasco',
 'Jorge Pérez Etchegaray':'perez','Enrique Orellana Cifuentes':'orellana','Elías Albagli Iruretagoyena':'albagli',
 'Ari Aisen':'aisen','Pablo Pincheira Brown':'pincheira','Felipe Jaque':'jaque','Julio Dittborn Cordua':'dittborn',
 'Miguel Ricaurte Vintimilla':'ricaurte','María Eugenia Wagner Brizzi':'wagner',
 'Rodrigo Alfaro':'alfaro','Rodrigo Álvarez Zenteno':'alvarez zenteno',
 'Alejandro Micco':'micco','Leonardo Hernández Tagle':'hernandez tagle','Alfredo Pistelli':'pistelli'
}
# extra surname aliases (second surname sometimes used)
EXTRA={('Rodrigo Vergara Montes','montes'),('Rodrigo Valdés Pulido','pulido'),('Manuel Marfán Lewis','lewis'),
       ('Sebastián Claro Edwards','edwards'),('Claudio Soto Gamboa','gamboa'),('Enrique Marshall Rivera','rivera'),
       ('Luis Óscar Herrera Barriga','barriga'),('Joaquín Vial Ruiz-Tagle','ruiz-tagle'),
       ('Alberto Arenas de Mesa','de mesa'),('Diego Gianelli Gómez','gomez'),('Felipe Larraín Bascuñán','bascunan'),
       ('Klaus Schmidt-Hebbel Dunker','dunker'),('Luis Felipe Céspedes Cifuentes','cifuentes'),
       ('María Elena Ovalle Molina','molina'),('María Olivia Recart Herrera','herrera'),('María Eugenia Wagner Brizzi','wagner'),('Rodrigo Alfaro','alfaro'),
       ('Mario Marcel Cullell','cullell'),('Camilo Carrasco Alfonso','alfonso'),('Miguel Ricaurte Bermúdez','bermudez')}

# Alta nominal acotada: no generar el alias común Marco ni sólo nombres de pila.
NARROW_NAME_ALIASES={'Juan Pablo Araya Marco': {'juan pablo araya marco','juan pablo araya'}}

# name resolution
def _nearest_actor(acts,date=None):
    if len(acts)==1: return next(iter(acts))
    if date:
        try:
            d=dt.date.fromisoformat(str(date))
        except Exception:
            d=None
        if d:
            best=None; bd=None
            for a in sorted(acts):
                ds=[dt.date.fromisoformat(to_date_str(x[1])) for x in data if str(x[2]).strip()==a]
                dist=min(abs((x-d).days) for x in ds) if ds else 10**9
                if bd is None or dist<bd:
                    bd=dist; best=a
            if best: return best
    return max(sorted(acts),key=lambda a:sum(1 for x in data if str(x[2]).strip()==a))

def resolve_name(name,date=None):
    n=norm(name).strip()
    if not n: return None
    exact=[a for a in REAL if norm(a)==n or norm(SURNAME.get(a,''))==n or n in [norm(x) for x in [SURNAME.get(a,''),a]]]
    if len(exact)==1: return exact[0]
    if len(exact)>1: return _nearest_actor(exact,date)
    cand=[]
    for a in REAL:
        if a in NARROW_NAME_ALIASES and n not in NARROW_NAME_ALIASES[a]:
            continue
        if n in norm(a): cand.append(a)
        elif n in norm(SURNAME.get(a,'')): cand.append(a)
    if len(cand)==1: return cand[0]
    if len(cand)>1:
        for a in cand:
            if n==norm(SURNAME.get(a,'')): return a
        return _nearest_actor(cand,date)
    # alias exacto (incluye variantes OCR)
    if n in alias_map:
        return _nearest_actor(alias_map[n],date)
    return None


# alias map from real actors
alias_map=collections.defaultdict(set)
for a in REAL:
    toks=norm(a).split()
    alts={norm(a)}
    for size in range(2, len(toks)):
        alts.add(" ".join(toks[:size]))
    if len(toks)>=2:
        alts.add(toks[0]+' '+toks[-1])
        alts.add(' '.join(toks[-2:]))
        alts.add(toks[-1])
        alts.add(' '.join(toks[:2]))
        if len(toks)>=3:
            alts.add(' '.join(toks[:2]+[toks[-1]]))
            alts.add(' '.join(toks[1:-1]+[toks[-1]]))
    sur=SURNAME.get(a)
    if sur: alts.add(norm(sur))
    for item in EXTRA:
        if item[0]==a: alts.add(norm(item[1]))
    # first + surname
    if sur:
        toks2=norm(a).split()
        alts.add(toks2[0]+' '+norm(sur))
    if a in NARROW_NAME_ALIASES:
        alts=NARROW_NAME_ALIASES[a]
    # full without accents already normalized
    for alt in alts:
        if len(alt)>3 and (len(alt.split())>1 or len(alt)>=4):
            alias_map[alt].add(a)

# alias extra: Maria Eugenia Wager (variante OCR del acta)
alias_map['wager'].add('María Eugenia Wagner Brizzi')
alias_map['maria wager'].add('María Eugenia Wagner Brizzi')
alias_map['maria eugenia wager'].add('María Eugenia Wagner Brizzi')
alias_map['maria eugenia wagner'].add('María Eugenia Wagner Brizzi')
for _lehm in ['lehmman','lehemann','lehamann','lehnann','lehmann b']:
    alias_map[_lehm].add('Sergio Lehmann Beresi')
alias_map['sergio lehmman'].add('Sergio Lehmann Beresi')
alias_map['sergio lehemann'].add('Sergio Lehmann Beresi')
alias_map['sergio lehmann b'].add('Sergio Lehmann Beresi')

# role -> actor per date
role_date=collections.defaultdict(collections.Counter)
for r in data:
    role_date[(to_date_str(r[1]),str(r[3]).strip())][str(r[2]).strip()]+=1

# nombres explicitos por rol (para role-only sin nombre)
ROLE_ACTOR_GLOBAL=collections.defaultdict(collections.Counter)
ROLE_DATE_ACTOR=collections.defaultdict(collections.Counter)
for r in data:
    _txt=str(r[5])[:500]
    for _pat,_canon in ROLE_PATS:
        for _m in re.finditer(r'(?<![A-Za-z0-9ÁÉÍÓÚÑáéíóúñ])'+re.escape(_pat),_txt,re.I):
            _after=_txt[_m.end():_m.end()+150]
            _nm=re.match(r'\s*[-,;]?\s*(?:(?:[Ss]ubrogante)|\([Ss]\)|\(s\)|en calidad de [Ss]ubrogante)?\s*(?:señor|señora|don|doña|sr\.|sra\.)?\s*([A-ZÁÉÍÓÚÑ][\wáéíóúñÁÉÍÓÚÑ]+(?:\s+[A-ZÁÉÍÓÚÑ][\wáéíóúñÁÉÍÓÚÑ]+){0,4})', _after)
            if _nm:
                _a=resolve_name(_nm.group(1).strip(),to_date_str(r[1]))
                if _a and _a in REAL:
                    ROLE_ACTOR_GLOBAL[_canon][_a]+=1
                    try:
                        ROLE_DATE_ACTOR[(dt.date.fromisoformat(to_date_str(r[1])),_canon)][_a]+=1
                    except Exception:
                        pass
MINISTER_BY_DATE=[
 (dt.date(2005,1,1),dt.date(2006,3,10),'Nicolás Eyzaguirre Guzmán'),
 (dt.date(2006,3,11),dt.date(2010,3,10),'Andrés Velasco Brañes'),
 (dt.date(2010,3,11),dt.date(2014,3,10),'Felipe Larraín Bascuñán'),
 (dt.date(2014,3,11),dt.date(2015,3,18),'Alberto Arenas de Mesa'),
 (dt.date(2015,3,19),dt.date(2030,1,1),'Rodrigo Valdés Pulido'),
]
SUBROGANTES={
 dt.date(2005,2,10):'Mario Marcel Cullell', dt.date(2005,4,7):'María Eugenia Wagner Brizzi',
 dt.date(2006,9,7):'Alberto Arenas de Mesa', dt.date(2007,7,12):'María Olivia Recart Herrera',
 dt.date(2007,11,13):'María Olivia Recart Herrera', dt.date(2008,2,7):'María Olivia Recart Herrera',
 dt.date(2008,5,8):'María Olivia Recart Herrera', dt.date(2009,2,12):'María Olivia Recart Herrera',
 dt.date(2009,12,15):'Alberto Arenas de Mesa',
 dt.date(2010,7,15):'Rodrigo Álvarez Zenteno',
}
def minister_for_date(date,sub=False):
    if sub and date in SUBROGANTES:
        return SUBROGANTES[date]
    d=date
    for a,b,n in MINISTER_BY_DATE:
        if a<=d<=b: return n
    return None
def role_variants(role):
    v=[role]
    if role=='Ministro de Hacienda (S)': v=['Ministro de Hacienda Subrogante','Ministra de Hacienda (S)',role]
    if role=='Ministro de Hacienda': v=[role,'Ministro de Hacienda Subrogante']
    if role=='Ministra de Hacienda': v=[role,'Ministra de Hacienda']
    if role=='Ministra de Hacienda (S)': v=['Ministra de Hacienda Subrogante',role]
    return v
def _roster_actor_for_role(date,role):
    """Si el rol aparece en la lista de asistencia de esa fecha con un único titular, lo prefiere."""
    rb=globals().get('ROSTER_BY_DATE')
    if not rb: return None
    r=rb.get(str(date)) if isinstance(rb.get(str(date)),dict) else rb.get(date)
    if not r: return None
    cands=[]
    for name,raw in r.items():
        cr=_canonical_role(raw,name)
        if cr==role:
            cands.append((name,cr))
    actors = {resolve_name(name,date) for name,_ in cands}
    actors.discard(None)
    if len(actors)==1:
        return next(iter(actors))
    return None

def actor_for_role(date,role):
    def _top(cnt):
        if not cnt: return None
        top=[x for x,n in cnt.most_common() if x in REAL]
        return top[0] if top else None
    if date:
        d=dt.date.fromisoformat(str(date))
        try:
            a=_roster_actor_for_role(date,role)
            if a: return a
        except Exception:
            pass
        if role in ('Ministro de Hacienda','Ministra de Hacienda'):
            m=minister_for_date(d,False)
            if m: return m
        if role in ('Ministro de Hacienda (S)','Ministra de Hacienda (S)'):
            m=minister_for_date(d,True)
            if m: return m
        # mapeo por rol/date construido con nombres explicitos en el texto
        for rv in role_variants(role):
            a=_top(ROLE_DATE_ACTOR.get((d,rv)))
            if a: return a
        # sesion mas cercana donde el rol aparece con nombre
        dates=sorted({dat for (dat,rv) in ROLE_DATE_ACTOR if rv in role_variants(role)})
        if dates:
            nd=min(dates,key=lambda x:abs((x-d).days))
            for rv in role_variants(role):
                a=_top(ROLE_DATE_ACTOR.get((nd,rv)))
                if a: return a
        for rv in role_variants(role):
            cnt=role_date.get((str(date),str(rv)))
            if cnt:
                top=[x for x,n in cnt.most_common() if x in REAL]
                if top: return top[0]
    for rv in role_variants(role):
        cnt=collections.Counter(str(r[2]).strip() for r in data if str(r[3]).strip()==rv)
        if cnt:
            top=[x for x,n in cnt.most_common() if x in REAL]
            if top: return top[0]
    g=ROLE_ACTOR_GLOBAL.get(role)
    if g:
        top=[x for x,n in g.most_common() if x in REAL]
        if top: return top[0]
    return None

def session_meta(text):
    t=norm(text).lstrip()
    starts=('siendo las','se retiran','se reanuda','se suspende','se levanta','comunicado','acuerdo n','se acuerda',
            'los consejeros manifiestan','en merito de lo anterior','a continuacion el consejo','a continuacion, el consejo',
            'acta correspondiente','en santiago de chile','a c t a')
    if t.startswith(starts): return True
    if t.startswith(('acta de la sesion','banco central de chile acta','el consejo aprueba','en su reunion mensual')): return True
    if (t[:35].find('el consejo')>=0 and ('aprueba' in t or 'acuerdo' in t)): return True
    t2=t.replace(' ','').replace("'",'')
    if t2[:12]=='bancocentral' and 'acta' in t2[:80]: return True
    if re.match(r'\d{1,2}-\d{2}-\d{4}',t) and 'se acuerda' in t: return True
    # inicio explicito con persona/cargo -> no tratar como acta colectiva
    if re.match(r'^(el|la|los|las)\s+(senor|señora|senores|presidente|ministro|ministra|gerente|consejero|consejera|vicepresidente|subsecretario|secretario)\b', t):
        return False
    # titular + hablante explicito en la misma fila -> no es acta colectiva
    if re.search(r'(?:\.|,|;|:)?\s*.*?\b(el|la)\s+(senor|señora|presidente|ministro|ministra|gerente|consejero|consejera|vicepresidente|subsecretario)\b.{0,90}\b('+'|'.join(v for v in sorted(VNORM,key=len,reverse=True))+r')\b', t[:220]):
        return False
    low=t
    if re.search(r'(\bel consejo\s+(adopt|aprob|acord|decid|resolv|acuerd)\w*)', low[:1000]): return True
    if re.search(r'((\bconforme a la votaci\w*)|(\ben virtud de lo anterior\b)|(\ben merito de lo anterior\b))', low[:1000]): return True
    if re.search(r'(\ben su reunion mensual de politica monetaria\b.+?\bel consejo\b)', low[:1000]): return True
    return False

def tipo_acta(text):
    """Subtipo de las filas institucionales/acta (Fuente_Rol=ACTA_INSTITUCIONAL)."""
    low=norm(text).lstrip()
    tl=str(text).lower()
    if low.startswith(('en santiago de chile','ac ta','a c t a','acta correspondiente',
                       'acta de la sesion','acta de la sesión')):
        return 'ACTA_CABECERA'
    if any(x in low for x in ['adopta el siguiente acuerdo','en merito de lo anterior',
                              'conforme a la votacion','por la unanimidad','por la mayoria',
                              'se acuerda','los consejeros manifiestan']):
        return 'ACUERDO_CONSEJO'
    if 'comunicado' in tl:
        return 'COMUNICADO'
    if any(x in low for x in ['siendo las','se reanuda','se suspende','se levanta','se retiran',
                              'se retira','se incorpora']):
        return 'META_SESION'
    return 'ACTA_INSTITUCIONAL'

# ---- decisión de TPM de la sesión (fórmula del acuerdo del Consejo) ----
# Tolerante a \s+ (el texto extraído del PDF trae saltos incrustados; la
# variante con espacios literales pierde ~18 sesiones) y a las variantes OCR:
# comas antes de "acordó", "del Banco Central" sin "de Chile", "resolvió, por
# unanimidad, mantener" (2005-06-09), "el Consejo acuerda bajar la Tasa"
# (2009-04-09), "el Consejo decidió mantener la tasa..." (comunicados 2005),
# y espacios OCR incrustados dentro de palabras clave ("monetari a",
# "anteri or"), que se curan con _fix_ocr.
from decision_rules import _soft, _fix_ocr, _is_current_decision


def detect(text,date):
    if session_meta(text) or is_header2(text):
        return (CONSEJO,'Consejo','ACTA/META',0)
    t=text[:1200]
    cands=[]
    for pat,canon in ROLE_PATS:
        for m in re.finditer(r'(?<![A-Za-z0-9ÁÉÍÓÚÑáéíóúñ])'+re.escape(pat), t, re.I):
            after=t[m.end():m.end()+150]
            nm=re.match(r'\s*[-,;]?\s*(?:(?:[Ss]ubrogante)|\([Ss]\)|\(s\)|en calidad de [Ss]ubrogante)?\s*(?:señor|señora|don|doña|sr\.|sra\.)?\s*([A-ZÁÉÍÓÚÑ][\wáéíóúñÁÉÍÓÚÑ]+(?:\s+[A-ZÁÉÍÓÚÑ][\wáéíóúñÁÉÍÓÚÑ]+){0,4})', after)
            if nm:
                actor=resolve_name(nm.group(1).strip(),date)
                if actor:
                    tail=after[nm.end():nm.end()+140]
                    verb=any(v in tail for v in VERBS)
                    beforen=norm(t[max(0,m.start()-34):m.start()])
                    mentioned=bool(re.search(r'(del|al|por el|por la|de la|presentacion del|presentación del|expuesto por el|agradece la presentacion de|agradece la presentación de|concede la palabra)\s+(senor|señor|ministro|ministra|gerente|consejero|consejera|presidente|vicepresidente|jefe|asesor)?\s*$', beforen))
                    cands.append({'pos':m.start(),'actor':actor,'role':canon,'verb':verb,'method':'ROL+NOMBRE','name':nm.group(1).strip(),'mention':mentioned})
            # role-only
            if not nm:
                # skip if role is en "del señor Ministro"/"al señor Ministro" etc (mention)
                before=t[max(0,m.start()-40):m.start()]
                bn=norm(before)
                if bn.endswith('del senor') or bn.endswith('al senor') or bn.endswith('del') or bn.endswith('al') or bn.endswith('comentario del senor') or bn.endswith('pregunta del senor'):
                    continue
                if re.search(r'(?:del|al|de los|de las|de la|los comentarios del|la solicitud del|solicitud del|respuesta a la|ante la solicitud del|a la solicitud del)\s*$', bn):
                    continue
                lo=max(0,m.start()-140); hi=min(len(t),m.end()+140)
                window=t[lo:hi]
                if any(v in window for v in VERBS):
                    actor=actor_for_role(date,canon)
                    if actor and actor in REAL:
                        cands.append({'pos':m.start(),'actor':actor,'role':canon,'verb':True,'method':'ROL+FECHA'})
    # name-only (hasta 1200 chars; contexto de título para apellidos ambiguos)
    tn=norm(text[:1200])
    seen=set()
    for alt,acts in alias_map.items():
        mult= ' ' in alt
        for m in re.finditer(r'(?<![a-z])'+re.escape(alt)+r'(?![a-z])', tn):
            if len(acts)>=1:
                actor=_nearest_actor(acts,date)
                if (m.start(),actor) in seen: continue
                seen.add((m.start(),actor))
                beforen=tn[max(0,m.start()-35):m.start()]
                if not mult:
                    # apellido suelto: exige título/honorifico antes (evita "fuentes" como fuentes de datos)
                    if not re.search(r'(senor|señor|don|doña|gerente|consejero|presidente|ministr|vicepresidente|subsecretario|jefe|asesor|sr|sra)\s+', beforen):
                        continue
                tailn=tn[m.end():m.end()+150]
                verb=any(v in tailn for v in VNORM) or any(v in beforen for v in VNORM)
                mentioned=bool(re.search(r'(al|del|a los|comentario del|pregunta del|consulta al|agradece al|concede la palabra al|invita al)\s+(senor|señor|sr|sra|don|doña)?\s*$', beforen))
                cands.append({'pos':m.start(),'actor':actor,'role':None,'verb':verb,'method':'NOMBRE+VERBO' if verb else 'NOMBRE','mention':mentioned})

    if not cands:
        return None
    has_trans=any(x in text[:800] for x in ['ofrece la palabra','da la palabra','concede la palabra','invita a','cede la palabra'])
    # candidatos "hablados": verbos, o role+nombre explicito reciente (aunque el verbo no este en la lista)
    strong=[c for c in cands if c.get('verb') or (c['method']=='ROL+NOMBRE' and c['pos']<1200)]
    if has_trans:
        trans_idx=min([i for x in ['ofrece la palabra','da la palabra','concede la palabra','invita a','cede la palabra'] for i in [text[:800].find(x)] if i>=0] or [0])
        def _speaks_after(c):
            if c.get('verb'): return True
            an=norm(c.get('actor') or c.get('name',''))
            toks=an.split()
            if not toks: return False
            low=text[c['pos']:c['pos']+1200]
            for token in [toks[0], toks[-1]]:
                for m in re.finditer(r'(?i)\b'+re.escape(token)+r'\w*', low):
                    if any(v in norm(low[m.start():m.start()+320]) for v in VNORM):
                        return True
            return False
        # Receptor explícito con cargo (rol+nombre) tras la transición.
        # No excluimos menciones: "concede la palabra al Ministro ... señor X"
        # es el destinatario de la palabra, no una mera mención.  Pero solo
        # lo tratamos como hablante si el texto muestra que realmente habla
        # más adelante en esa misma fila; si la fila es sólo "ofrece la palabra a X",
        # el hablante sigue siendo quien la concede.
        after_trans=[c for c in strong if c.get('role') and c['method']=='ROL+NOMBRE' and c['pos']>trans_idx]
        after_trans_name=[c for c in strong if c['pos']>trans_idx and c['method'] in ('NOMBRE+VERBO','ROL+NOMBRE')]
        after_all=[c for c in after_trans + [c for c in after_trans_name if c not in after_trans] if _speaks_after(c)]
        if after_all:
            after_all.sort(key=lambda c:(c['pos'],0 if c['method']=='ROL+NOMBRE' else 1,0 if c['actor'] not in PSEUDO else 1))
            c=after_all[0]; return (c['actor'],c['role'],c['method'],c['pos'])
        # Transición sin intervención del receptor en la misma fila: se queda
        # con quien está hablando antes de ceder la palabra.
        before_trans=[c for c in strong if c['pos']<trans_idx and not c.get('mention')]
        if before_trans:
            before_trans.sort(key=lambda c:(c['pos'],0 if c['method']=='ROL+NOMBRE' else 1,0 if c['actor'] not in PSEUDO else 1))
            c=before_trans[0]; return (c['actor'],c['role'],c['method'],c['pos'])
        best=[c for c in strong if c.get('role') and c['method']=='ROL+NOMBRE' and not c.get('mention')]
        if best:
            best.sort(key=lambda c:(c['pos'],0 if c['actor'] not in PSEUDO else 1))
            c=best[0]; return (c['actor'],c['role'],c['method'],c['pos'])
    if strong:
        # las menciones ("del Consejero señor X") no son hablantes; preferir candidatos no mencionados si existen
        no_mention=[c for c in strong if not (c.get('method')=='ROL+NOMBRE' and c.get('mention'))]
        if no_mention:
            strong=no_mention
        # role+nombre explicito al inicio es una señal muy fuerte (aunque el verbo no este en la lista).
        # Pero si antes hay un hablante explícito por nombre (p.ej. "Manifiesta el señor X que la
        # Gerencia ... señora Y"), el hablante es X, no el rol posterior.
        early_explicit=[c for c in strong if c['method']=='ROL+NOMBRE' and c['pos']<60]
        if early_explicit:
            earliest=min(strong,key=lambda c:(c['pos'],0 if c['method']=='ROL+NOMBRE' else 1,0 if c['actor'] not in PSEUDO else 1))
            if not (earliest['pos'] < early_explicit[0]['pos'] and earliest['method'] in ('ROL+NOMBRE','NOMBRE+VERBO')):
                early_explicit.sort(key=lambda c:(c['pos'],0 if c['actor'] not in PSEUDO else 1))
                c=early_explicit[0]; return (c['actor'],c['role'],c['method'],c['pos'])
        # cargo generico al inicio vs nombre explicito posterior en la misma intervencion
        generic=[c for c in strong if c['method']=='ROL+FECHA' and c['pos']<50 and c.get('role')]
        explicit=[c for c in strong if c['method'] in ('ROL+NOMBRE','NOMBRE+VERBO') and c['pos']<1200 and not c.get('mention')]
        if generic and explicit:
            g=min(generic,key=lambda c:c['pos']); e=min(explicit,key=lambda c:c['pos'])
            if e['actor']==g['actor']:
                return (g['actor'],g['role'],g['method'],g['pos'])
            between=norm(text[g['pos']:e['pos']+1])
            staff_generic=bool(g.get('role') and str(g.get('role')).split(' de ',1)[0] in ('Gerente','Jefe','Asesor','Subsecretario'))
            if staff_generic and not re.search(r'((ii|iii|iv|v)\.|iv\.|v\.|a continuaci\w+ el (senor )?presidente|ofrece la palabra|concede la palabra|da la palabra|se suspende|se reanuda|al respecto)', between):
                # conservar el rol explícito del texto; el nombre explícito corrige el hablante
                # solo si está inmediatamente ligado al cargo (evita menciones posteriores).
                if e['pos']-g['pos'] <= 120 and not e.get('mention'):
                    return (e['actor'],g['role'],e['method'],e['pos'])
                return (g['actor'],g['role'],g['method'],g['pos'])
        strong.sort(key=lambda c:(c['pos'],0 if c['method']=='ROL+NOMBRE' else 1 if c['verb'] else 2,0 if c['actor'] not in PSEUDO else 1))
        c=strong[0]; return (c['actor'],c['role'],c['method'],c['pos'])
    early=[c for c in cands if c['pos']<120 and c['role'] and c['method']=='ROL+NOMBRE']
    if early:
        early.sort(key=lambda c:c['pos'])
        c=early[0]; return (c['actor'],c['role'],c['method'],c['pos'])
    return None
    return None

# ---------------------------------------------------------------------------
# Segmentación de filas en intervenciones (una fila = una intervención real).
# ---------------------------------------------------------------------------
SPEECH_VERBS=[v for v in VERBS if v not in
 ('ofrece la palabra','concede la palabra','da la palabra','invita a','cede la palabra','invita',
  'agradece','agradece la presentacion de','agradece la presentación de','da inicio','da inicio a','dio inicio','dio inicio a')]
SPEECH_VERBS += ['confirma','confirma que','sostiene','sostiene que','apunta','apunta que',
 'argumenta','argumenta que','reconoce','reconoce que','describe','analiza','desarrolla',
 'expone','expone que','presenta','presenta que','explicita','explicita que','puntualiza','puntualiza que',
 'formula','contesta','propone','propone que','sugiere','sugiere que','se refiere','señalando','indicando',
 'manifestando','expresando','acotando','precisando','destacando','comentando','hace presente',
 'hacen presente','hizo presente','hace ver','fija','da cuenta','presenta las opciones','plantea que','indica que',
 'expresa que','comenta que','considera que','opina que','estima que','aclara que','responde que',
 'informa que','menciona que','recalca que','subraya que','advierte que','consulta que','pregunta que',
 'agrega que','observa que','destaca que','concluye que','precisa que','explica que','analiza que']
S_VERBS=sorted([norm(v) for v in SPEECH_VERBS],key=len,reverse=True)
S_VERB_RE=re.compile(r'\b(?:'+'|'.join(map(re.escape,S_VERBS))+r')\b')

INV_SUBJ_RE=re.compile(
 r'^(?:(?:al respecto|por su parte|a lo anterior|a este respecto|con respecto|en respuesta|a continuacion|asimismo|luego|despues|finalmente|por otra parte|en relacion|luego de|despues de),?\s*)?'
 r'(?:manifiesta|senala|sostiene|considera|plantea|indica|expresa|comenta|agrega|aclara|precisa|responde|informa|opina|acota|subraya|recalca|advierte|consulta|pregunta|concluye|estima|recuerda|reconoce|argumenta|confirma|explica|destaca|continua|prosigue|menciona|se refiere)'
 r'\s+(?:el|la|don|doña|senor|senora|presidente|vicepresidente|ministro|ministra|gerente|consejero|consejera)\s*$')
MENTION_RE=re.compile(
 r'(?:como\s+lo\s+(?:senala|indica|senalo|manifiesta|plantea)|como\s+senala|como\s+senalo|'
 r'lo\s+(?:senala|indica|senalo|manifiesta|plantea)|al\s+respecto\s+el\s+comentario|'
 r'comentario\s+(?:del|de)|presentacion\s+(?:del|de)|expuesto\s+por|de\s+acuerdo\s+a\s+lo\s+'
 r'(?:senalado|expuesto|indicado|planteado)\s+por|agradece\s+la\s+presentacion\s+(?:de|del)|'
 r'en\s+relacion\s+(?:al|con)\s+(?:lo\s+)?(?:senalado|expuesto|indicado|planteado)|'
 r'a\s+lo\s+(?:senalado|expuesto|indicado|planteado)\s+por|el\s+comentario\s+(?:del|de)|'
 r'segun\s+lo\s+expuesto\s+por|en\s+referencia\s+a\s+lo\s+(?:senalado|senalado)|'
 r'\bsenala\s+el\s+(?:senor|consejero|gerente|presidente|vicepresidente)|'
 r'\bsenalo\s+el\s+(?:senor|consejero|gerente|presidente|vicepresidente)|'
 r'\bindic[oa]\s+el\s+(?:senor|consejero|gerente|presidente|vicepresidente)|'
 r'\bmanifiesta\s+el\s+(?:senor|consejero|gerente|presidente|vicepresidente)|'
 r'\bconsidera)\s*$')
START_VERB=re.compile(r'^(?:agrega|agregar|senala|senalando|indica|manifest[oa]|expresa|dice|comenta|considera|plantea|opina|destaca|observa|aclara|continua|prosigue|recuerda|responde|informa|explica|menciona|se\s+refiere|refiere|cree|piensa|estima|consulta|pregunta|se\s+pregunta|se\s+senala|concluye|precisa|subraya|recalca|advierte)\b')
LEAD_OK=re.compile(r'^(?:el|la|a continuacion,?|luego,?|asimismo,?|por su parte,?|al respecto,?|despues,?|finalmente,?|con posterioridad,?|a su vez,?|de inmediato,?|enseguida,?|a continuacion\s+el|al\s+respecto\s+el|asistentes|a continuacion el senor|al respecto el senor|por su parte el senor)\s*$')

def seg_candidates(text,date):
    t=text; tn=norm(text); cands=[]
    for pat,canon in ROLE_PATS:
        for m in re.finditer(r'(?<![A-Za-z0-9ÁÉÍÓÚÑáéíóúñ])'+re.escape(pat),t,re.I):
            after=t[m.end():m.end()+150]
            nm=re.match(r'\s*[-,;]?\s*(?:(?:[Ss]ubrogante)|\([Ss]\)|\(s\)|en calidad de [Ss]ubrogante)?\s*(?:señor|señora|don|doña|sr\.|sra\.)?\s*([A-ZÁÉÍÓÚÑ][\wáéíóúñÁÉÍÓÚÑ]+(?:\s+[A-ZÁÉÍÓÚÑ][\wáéíóúñÁÉÍÓÚÑ]+){0,4})',after)
            if nm:
                actor=resolve_name(nm.group(1).strip(),date)
                if actor and actor in REAL:
                    tail=after[nm.end():nm.end()+140]
                    verb=bool(S_VERB_RE.search(norm(tail)))
                    beforen=norm(t[max(0,m.start()-60):m.start()])
                    inv=bool(INV_SUBJ_RE.search(norm(t[:m.start()])))
                    mentioned=(not inv) and (bool(MENTION_RE.search(beforen)) or bool(re.search(r'(del|al|por el|por la|de la|presentacion del|presentación del|expuesto por el|agradece la presentacion de|agradece la presentación de|concede la palabra)\s+(?:senor|ministro|ministra|gerente|consejero|consejera|presidente|vicepresidente|jefe|asesor)?\s*$',beforen)))
                    cands.append({'actor':actor,'pos':m.start(),'verb':verb,'mention':mentioned,'method':'ROL+NOMBRE','name':nm.group(1).strip()})
            else:
                before=t[max(0,m.start()-40):m.start()]
                bn=norm(before)
                if MENTION_RE.search(bn): continue
                # role-only que es referencia/posesión ("del Gerente...", "sobre los comentarios del...")
                # no es un hablante, se deja fuera.
                if re.search(r'(?:del|al|de los|de las|de la|los comentarios del|la solicitud del|solicitud del|respuesta a la|ante la solicitud del|a la solicitud del)\s*$', bn):
                    continue
                lo=max(0,m.start()-140); hi=min(len(t),m.end()+140)
                window=norm(t[lo:hi])
                if S_VERB_RE.search(window):
                    actor=actor_for_role(date,canon)
                    if actor and actor in REAL:
                        cands.append({'actor':actor,'pos':m.start(),'verb':True,'mention':False,'method':'ROL+FECHA','name':None})
    seen=set()
    for alt,acts in alias_map.items():
        mult=' ' in alt
        for m in re.finditer(r'(?<![a-z])'+re.escape(alt)+r'(?![a-z])',tn):
            if len(acts)>=1:
                actor=_nearest_actor(acts,date)
                if (m.start(),actor) in seen: continue
                seen.add((m.start(),actor))
                beforen=tn[max(0,m.start()-35):m.start()]
                if not mult and not re.search(r'(senor|don|doña|gerente|consejero|presidente|ministr|vicepresidente|subsecretario|jefe|asesor|sr|sra)\s+',beforen):
                    continue
                tailn=tn[m.end():m.end()+150]
                verb=bool(S_VERB_RE.search(tailn) or S_VERB_RE.search(beforen))
                inv=bool(INV_SUBJ_RE.search(tn[:m.start()]))
                mentioned=(not inv) and (bool(MENTION_RE.search(beforen)) or bool(re.search(r'(al|del|a los|comentario del|pregunta del|consulta al|agradece al|concede la palabra al|invita al)\s+(senor|sr|sra|don|doña)?\s*$',beforen)))
                cands.append({'actor':actor,'pos':m.start(),'verb':verb,'mention':mentioned,'method':'NOMBRE+VERBO' if verb else 'NOMBRE','name':None})
    return cands

# Reanudación dañada constatada en 4502. Sólo esta fórmula literal habilita
# el prefijo OCR; no se borra «i,-» ni se generaliza a basura entre oraciones.
_DAMAGED_REOPENING = 'i,- Siendo las 16:00 horas, se reanuda la Reunión de Política Monetaria N° 179.'


def split_sentences(text):
    # Conservar offsets originales. No usar saltos OCR como fin de oración.
    boundaries = {0, len(text)}
    pattern = r'(?<=[.!?;])\s*/*\s*(?=[A-ZÁÉÍÓÚÑ\"“‘«0-9])'
    for m in re.finditer(pattern, text):
        tail = text[max(0,m.start()-12):m.start()].rstrip()
        if re.search(r'\b(?:Sr|Sra|art|inc|num|pág|pag)\.$',tail,re.I):
            continue
        # La hora literal 13.05 en 5313 no inicia una oración en 05.
        if (re.search(r'\bsiendo las? (?:[01]?\d|2[0-3])\.$', text[:m.start()], re.I)
                and re.match(r'[0-5]\d horas\b', text[m.end():], re.I)):
            continue
        boundaries.add(m.end())
    # Marcadores inequívocos de turno aun cuando el OCR perdió el punto.
    for m in re.finditer(r'\s+(?=(?:A continuación,|Al respecto,|Por su parte,)\s+(?:el|la)\s+(?:señor|señora|Presidente|Vicepresidente|Consejero|Consejera|Gerente|Ministro))', text):
        boundaries.add(m.end())
    # OCR concatena párrafos sin punto ("...totalmente El Gerente...") o deja
    # basura entre el punto y el sujeto. Sólo sujeto con artículo MAYÚSCULO;
    # se excluyen subordinadas y citas. El detector valida el verbo después.
    for m in re.finditer(r'(?<!\w)(?:El|La|EL|LA)\s+(?:señor|señora|Presidente|Vicepresidente|Consejero|Consejera|Gerente|Ministro|Ministra|Subgerente)\b', text):
        if not m.start():
            continue
        before = text[:m.start()]
        if re.search(r'\b(?:Exposición|Intervención|Comentarios)\s+$', before):
            continue
        # OCR constatado: falta el sustantivo tras «proceder a la» y empieza
        # un nuevo sujeto explícito. No completar el texto ni atribuir el voto
        # al Presidente que acaba de ceder la palabra.
        broken_handoff = bool(re.search(
            r'ofrece la palabra a los señores Consejeros para proceder a la\s*$',
            before, re.I) and re.match(r'El Consejero\b',text[m.start():]))
        if not broken_handoff and re.search(r'\b(?:que|si|como|cuando|donde|del|al|de|por|segun|según|el|la)\s*$', before, re.I):
            continue
        if before.count('"') % 2 or before.count('“') > before.count('”') or before.count('«') > before.count('»'):
            continue
        # Una división en oración no implica cambio de actor: segment_turns
        # sólo crea fila si reconoce un nuevo sujeto de habla.
        boundaries.add(m.start())
    # Respuestas explícitas dentro de una oración, no nombres meramente citados.
    # Se conserva el conector en el segundo fragmento; el detector exige sujeto
    # y verbo. No abrir límites dentro de comillas ni extender esto a cualquier «y».
    for m in re.finditer(r'\ba lo (?:cual|que),?\s+(?:el|la)\s+(?:señor|señora|Presidente|Vicepresidente|Consejero|Consejera|Gerente|Ministro|Ministra)\b', text, re.I):
        before = text[:m.start()]
        if not re.search(r'[,;]\s*$', before):
            continue
        if before.count('"') % 2 or before.count('“') > before.count('”') or before.count('«') > before.count('»'):
            continue
        boundaries.add(m.start())
    for m in re.finditer(re.escape(_DAMAGED_REOPENING), text):
        before = text[:m.start()]
        quoted = (before.count('"') % 2 or before.count('“') > before.count('”')
                  or before.count('«') > before.count('»'))
        if re.search(r'\.\s+$', before) and not quoted:
            boundaries.add(m.start())
    positions = sorted(boundaries)
    return list(zip(positions, positions[1:]))


def sentence_speaker(sent,date):
    cs=seg_candidates(sent,date)
    strong=[c for c in cs if c['actor'] in REAL and not c.get('mention') and c.get('verb')]
    if not strong: return None,False
    strong.sort(key=lambda c:(c['pos'],0 if c['method']=='ROL+NOMBRE' else 1 if c['verb'] else 2))
    c=strong[0]
    prefix=norm(sent[:c['pos']])
    if not prefix: return c['actor'],True
    if START_VERB.search(prefix): return c['actor'],False
    if S_VERB_RE.search(prefix): return c['actor'],False
    ok = c['pos']<=35 or bool(LEAD_OK.match(prefix))
    if not ok: return c['actor'],False
    return c['actor'],True

def first_speaker_hint(text,date):
    """Prioriza el hablante explícito de la primera oración de la intervención."""
    if session_meta(text) or is_header2(text): return None
    for (s0,s1) in split_sentences(text):
        sent=text[s0:s1].strip()
        if not sent: continue
        spk,clear=sentence_speaker(sent,date)
        if clear and spk: return spk
        break
    return None

def _inst_transition(sent):
    """Oración que abre un bloque institucional del acta (transición al
    Consejo) — versión ESTRICTA para uso a nivel de oración dentro de
    segment_row. La heurística amplia de session_meta, aplicada por oración,
    dividía por error discursos que sólo mencionan al Consejo ("Hace presente
    que ... el Consejo adoptó ...", "En virtud de lo anterior, al Ministro...
    le parece ...", "Consigna que ... el Consejo decidió ...")."""
    # 5183: decisión institucional literal, no un turno de Vicuña o Nacrur.
    if sent.strip() == 'Se determinó, dada la importancia de este tema, que el Gerente de División Estadísticas efectúe una presentación sobre el tratamiento de las importaciones de aviones y barcos en una próxima Sesión de Pre Consejo.':
        return True
    t=_fix_ocr(norm(sent))
    # Registro horario de reanudación, no cualquier mención de una hora.
    if re.match(r'^a las (?:[01]?\d|2[0-3]):[0-5]\d horas, se reanuda la (?:reunion|sesion) de politica monetaria n[°º]\s*\d+\b', t):
        return True
    # Encabezado formal con código de acuerdo; espacios OCR sólo reconocidos.
    # No confundir una cifra ni una mención retrospectiva con un bloque del acta.
    if re.match(r'^\d{2,3}-\d{2}-\d{6}-\s*t\s*a\s*s\s*a de politica monetaria(?:\.|\s+el consejo\b)', t):
        return True
    if re.match(r'^luego de un intercambio de opiniones, se acuerda que\b', t):
        return True
    if sent.strip() in (_DAMAGED_REOPENING,
            # 2489: número de sesión desplazado por OCR. Fórmula literal,
            # no permiso general para anteponer números/basura a un relato.
            'N° 137, Siendo las 16:00 horas, se reanuda la Sesión de Política Monetaria'):
        return True
    if t.startswith(('siendo las','se levanta','se reanuda','se suspende','se retiran',
                     'se retira','se incorpora','se acuerda','comunicado','acuerdo n',
                     'se deja constancia','en su reunion mensual','a continuacion el consejo',
                     'a continuacion, el consejo','los consejeros manifiestan',
                     'acta correspondiente','en santiago de chile','a c t a')):
        return True
    # Fórmula formal constatada: no omitir la transición por la intercalación.
    # No aceptar aquí cualquier mención del Consejo dentro de un discurso.
    if re.match(r'^en merito de lo anterior,\s*el consejo,\s*por la unanimidad de sus miembros,\s*adopta el siguiente acuerdo\b', t):
        return True
    if re.match(r'^el\s+consejo\s+(adopta|adopto|aprueba|acuerda|acordo|resolvio|decidio|procede|procedio)\b', t):
        return True
    m=re.match(r'^(en\s+merito\s+de\s+lo\s+anterior|conforme\s+a\s+la\s+votacion[^,.;]{0,90}'
               r'|en\s+virtud\s+de\s+lo\s+anterior|en\s+consecuencia\s*,?\s*por\s+votacion\s+unanime'
               r'|por\s+(?:la\s+)?unanimidad\s+de\s+sus\s+miembros)\s*,?\s*', t)
    if m:
        return bool(re.search(r'\bel\s+consejo\s+(adopta|adopto|aprueba|acuerda|acordo|resolvio|decidio|procede|procedio)\b',
                              t[m.end():m.end()+160]))
    return False

def segment_row(text,date):
    sents=split_sentences(text)
    segs=[]; cur_start=0; prev=None
    for (s0,s1) in sents:
        if not text[s0:s1].strip(): continue
        sent=text[s0:s1]
        # Transición institucional: el Consejo/acta toma la palabra ("En
        # mérito de lo anterior, el Consejo ... adopta el siguiente Acuerdo",
        # "Conforme a la votación ...", "Se acuerda ...", "Siendo las ...").
        # Divide sólo si el tramo actual no es ya institucional, para no
        # fragmentar las filas de acta/meta propiamente tales.
        if prev!=CONSEJO and s0>cur_start and _inst_transition(sent):
            segs.append((cur_start,s0)); cur_start=s0; prev=CONSEJO
            continue
        spk,clear=sentence_speaker(sent,date)
        if clear and spk:
            if prev is not None and spk!=prev and s0>cur_start:
                segs.append((cur_start,s0)); cur_start=s0
            prev=spk
    segs.append((cur_start,len(text)))
    out=[]
    for a,b in segs:
        t=text[a:b].strip()
        if t: out.append(t)
    return out if out else [text.strip()]

def maybe_segments(text,date):
    if session_meta(text) or is_header2(text):
        return [text]
    return segment_row(text,date)

def is_header2(t):
    return norm(t).lstrip().startswith(('acta correspondiente','a c t a'))

# canonical role for actor/date
actor_role_by_date=collections.defaultdict(collections.Counter)
for r in data:
    actor_role_by_date[(to_date_str(r[1]),str(r[2]).strip())][str(r[3]).strip()]+=1
def canonical_role_by_actor(actor,date):
    cnt=actor_role_by_date.get((str(date),actor))
    if cnt: return cnt.most_common(1)[0][0]
    cnt=collections.Counter(str(r[3]).strip() for r in data if str(r[2]).strip()==actor)
    return cnt.most_common(1)[0][0] if cnt else None

KNOWN_MIN={'Nicolás Eyzaguirre Guzmán','Andrés Velasco Brañes','Felipe Larraín Bascuñán','Alberto Arenas de Mesa','Rodrigo Valdés Pulido','María Olivia Recart Herrera','Mario Marcel Cullell','María Eugenia Wagner Brizzi','Julio Dittborn Cordua','Rodrigo Álvarez Zenteno'}
FULL_MIN_START={'Andrés Velasco Brañes':dt.date(2006,3,11),'Felipe Larraín Bascuñán':dt.date(2010,3,11),'Alberto Arenas de Mesa':dt.date(2014,3,11),'Rodrigo Valdés Pulido':dt.date(2015,3,19)}
ALWAYS_SUBRO={'María Olivia Recart Herrera','Mario Marcel Cullell','María Eugenia Wagner Brizzi','Rodrigo Álvarez Zenteno'}
def ministry_role(text,actor,date):
    if actor=='Julio Dittborn Cordua': return 'Subsecretario de Hacienda'
    low=text.lower()
    fem=bool(re.search(r'(la ministra|ministra de hacienda|señora ministra)', low))
    male=bool(re.search(r'(el ministro|ministro de hacienda|señor ministro)', low))
    gen='Ministra' if (fem and not male) else 'Ministro'
    if actor in {'María Olivia Recart Herrera','María Eugenia Wagner Brizzi'}: gen='Ministra'
    subg=('subrogante' in low) or (actor in ALWAYS_SUBRO)
    if actor in FULL_MIN_START and date>=FULL_MIN_START[actor] and 'subrogante' not in low: subg=False
    return f'{gen} de Hacienda{" (S)" if subg else ""}'.strip()

# ---- roster de cargos por sesión (primer párrafo del acta) ----
_opening_by_date=collections.defaultdict(list)
for _r in data:
    _d=to_date_str(_r[1])
    if str(_r[4]).strip()=='1':
        _opening_by_date[_d].append(str(_r[5]))
ROSTER_BY_DATE=_build_rosters({_d:' '.join(_opening_by_date[_d]) for _d in _opening_by_date})
def roster_role_for(date,actor):
    r=ROSTER_BY_DATE.get(date)
    if not r: return None
    raw=_match_role(r,actor)
    if raw is None: return None
    return _canonical_role(raw,actor)

# ---- textos completos re-extraidos desde PDF (límite de celda Excel) ----
import json as _json
import os as _os
def load_full_texts(path=TEXTOS_COMPLETOS):
    result = {}
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            row = _json.loads(line)
            rid = int(row['ID'])
            if rid in result or not row.get('Texto_Completo'):
                raise ValueError(f'Texto completo duplicado o vacío: {rid}')
            if len(row['Texto_Completo']) != row['Longitud_Texto_Completo']:
                raise ValueError(f'Longitud de texto completo inconsistente: {rid}')
            result[rid] = row
    return result


def strict_alias(alias, date):
    actors = alias_map[alias]
    if len(actors) == 1:
        return next(iter(actors))
    present = [a for a in sorted(actors) if roster_role_for(date, a)]
    return present[0] if len(present) == 1 else None


def strict_role(date, role):
    # No inferir un turno nuevo por la frecuencia global de un cargo ambiguo.
    actor = _roster_actor_for_role(date, role)
    if actor:
        return actor
    base = re.sub(r'\s*(?:\(S\)|Subrogante)$', '', role)
    names = {resolve_name(name,date) for name,raw in ROSTER_BY_DATE.get(date,{}).items()
             if re.sub(r'\s*(?:\(S\)|Subrogante)$', '', _canonical_role(raw,name)) == base}
    names.discard(None)
    return next(iter(names)) if len(names)==1 else None


TURN_DETECTOR = TurnDetector(alias_map, ROLE_PATS + [(r, c or r) for r,c in ROSTER_ROLES] + [('Asesor Macroeconómico del Ministro de Hacienda', 'Asesor Macroeconómico del Ministro de Hacienda'), ('Gerente', 'Gerente'), ('Gerente de División', 'Gerente de División')],
                             strict_alias, strict_role, roster_role_for)


def segment_turns(text, date, initial_actor, state=None, review=None, document=None, institution=None):
    if state is not None and state.get('date') != date:
        state.clear()
        state['date'] = date
    if institution is not None:
        if review is not None or document is not None:
            raise ValueError('Continuación de acta solapada con revisión personal')
        if institution.get('Tipo_Alcance') == 'INTERRUPCION_Y_REANUDACION_REVISADA':
            if date != institution['Fecha'] or initial_actor != institution['Actor_Expositor']:
                raise ValueError('Acta: fecha/actor de reanudación incompatibles')
        parts = institutional_parts(text, institution, TURN_DETECTOR)
        if state is not None:
            state.update(roles={}, last_sentence='', anchor=None, pending=None, barrier=True)
        return parts
    if document is not None:
        if review is not None:
            raise ValueError('Documento y revisión de hablante se solapan')
        parts = document_parts(text, date, initial_actor, document, TURN_DETECTOR)
        if state is not None:
            state['roles'] = {}
            state['last_sentence'] = ''
        return parts
    spans = split_sentences(text)
    intervals = speaker_intervals(review)
    if any(e.get('Tipo_Limite')=='APERTURA_POST_NOMINA_REVISADA' for e in intervals) and not is_header2(text):
        raise ValueError('Apertura revisada fuera de cabecera')
    if is_header2(text) and intervals:
        # Excepción individual: sólo la cola presidencial revisada, nunca la nómina.
        if len(intervals)!=1 or intervals[0].get('Tipo_Limite')!='APERTURA_POST_NOMINA_REVISADA':
            raise ValueError('Apertura revisada sin alcance único')
        entry=intervals[0];a,z=entry['Inicio'],entry['Fin']
        prefix,fragment=text[:a],text[a:z]
        candidate=TURN_DETECTOR.speaker(fragment,date)
        if (not 0<a<z==len(text) or not fragment.startswith('El Presidente, señor ')
                or not re.search(r'Asisten? también',prefix)
                or prefix.count('"')%2 or prefix.count('“')>prefix.count('”')
                or prefix.count('«')>prefix.count('»')
                or not candidate or candidate['actor']!=entry['Actor']
                or candidate['method'] not in EXPLICIT
                or candidate['role']!='Presidente del Banco Central'):
            raise ValueError('Apertura revisada sin sujeto/límite presidencial válido')
        if state is not None:
            state.update(roles={},last_sentence='',anchor=None,pending=None,barrier=True)
        return bound_segments([(prefix.strip(),CONSEJO,'ACTA/META'),
                               (fragment.strip(),entry['Actor'],SPEAKER_REVIEW_SOURCE)])
    reviews_by_start = {r["Inicio"]:r for r in intervals}
    if len(reviews_by_start) != len(intervals):
        raise ValueError("Inicios revisados duplicados")
    for review in reviews_by_start.values():
        if review["Actor"] not in REAL:
            raise ValueError("Revisión de hablante sin actor/límite válido")
        if (review["Inicio"] not in {a for a,b in spans}
                or review.get("Tipo_Limite") in ("CONCATENACION_EXPLICITA_REVISADA", "INICIO_TRAS_ARTEFACTO_REVISADO", "RESPUESTA_A_LO_QUE_EXPLICITA", "RESPUESTA_POR_LO_QUE_EXPLICITA", "GERUNDIO_SENALANDO_EXPLICITO", "CESION_RELATIVA_EXPLICITA", "CESION_AGRADECIMIENTO_RELATIVO_EXPLICITO", "OPINION_TRAS_CITA_CERRADA_REVISADA", 'RETORNO_TRAS_CITA_CERRADA_REVISADA', 'RESPUESTA_A_LO_CUAL_MUESTRA_REVISADA', 'RESPUESTA_A_LO_CUAL_EXPLICITA', 'GERUNDIO_INDICANDO_FISCAL_EXPLICITO', 'CESION_HACE_PRESENTE_RELATIVA_EXPLICITA', 'GERUNDIO_NOMINAL_EXPLICITO_REVISADO', 'RESPUESTA_PASIVA_NOMINAL_REVISADA', 'RESPUESTA_LO_QUE_NOMINAL_REVISADA', 'CESION_AGRADECIMIENTO_ANALISIS_REVISADA', 'RESPUESTA_PASIVA_VARIANTE_REVISADA', 'DECLARACION_TRAS_ASUNCION_REVISADA', 'INICIO_CARGO_TRAS_CESION_NOMINAL_REVISADA', 'GERUNDIO_CONFIRMACION_NOMINAL_REVISADA', 'GERUNDIO_RESPUESTA_VARIANTE_REVISADA')):
            # Una decisión individual puede delimitar una cláusula interior:
            # exige separador previo o excepción documentada, sujeto explícito
            # compatible y fuera de cita.
            prefix = text[:review["Inicio"]]
            fragment = text[review["Inicio"]:review["Fin"]]
            passive_variant = review.get('Tipo_Limite') == 'RESPUESTA_PASIVA_VARIANTE_REVISADA'
            passive_reply = review.get('Tipo_Limite') == 'RESPUESTA_PASIVA_NOMINAL_REVISADA' or passive_variant
            assumption_declaration = review.get('Tipo_Limite') == 'DECLARACION_TRAS_ASUNCION_REVISADA'
            if assumption_declaration:
                subject=re.search(r'pasa a presidir la Sesión transitoriamente (el Vicepresidente señor [^,.;!?]+),\s*$',prefix)
                if not subject or not fragment.startswith('haciendo presente que '):
                    raise ValueError('Declaración sin asunción nominal contigua')
                fragment=subject[1]+' hace presente'+fragment[len('haciendo presente'):]
            role_handoff = review.get('Tipo_Limite') == 'INICIO_CARGO_TRAS_CESION_NOMINAL_REVISADA'
            if role_handoff:
                handoff=re.search(r'ofrece la palabra al (Gerente de División Estudios Subrogante), señor ([^,.;!?]+), para que presente las Opciones de Política Monetaria para esta Reunión\s+$',prefix)
                lead='El señor Gerente de División Estudios Subrogante recuerda que'
                if not handoff or not fragment.startswith(lead):
                    raise ValueError('Inicio por cargo sin cesión nominal contigua')
                fragment='El señor '+handoff[2]+' recuerda que'+fragment[len(lead):]
            relative_reply = review.get('Tipo_Limite') == 'RESPUESTA_LO_QUE_NOMINAL_REVISADA'
            if passive_reply:
                pattern=(r'^(acotación que es confirmada|lo cual es compartido) por (?=(?:el|la)\b)' if passive_variant else r'^(lo (?:que|cual)|Ello) es (confirmado|corroborado|rebatido) por (?=(?:el|la)\b)')
                head=re.match(pattern,fragment)
                if (not head or not prefix or not prefix[-1].isspace()
                        or not prefix.rstrip().endswith(('.', '!', '?') if head[1]=='Ello' else (',',))):
                    raise ValueError('Respuesta pasiva sin límite/conector válido')
                # Sólo proyección de sujeto nominal; el verbo/voz literal no se exporta cambiado.
                fragment='responde '+fragment[head.end():]
            if relative_reply:
                if not prefix.rstrip().endswith(',') or not re.match(r'^lo que (?:comparte|confirma) (?:el|la)\b',fragment):
                    raise ValueError('Respuesta relativa sin límite/predicado válido')
                fragment=fragment[len('lo que '):]
            fiscal_reply = review.get('Tipo_Limite') == 'GERUNDIO_INDICANDO_FISCAL_EXPLICITO'
            confirming_gerund = review.get('Tipo_Limite') == 'GERUNDIO_CONFIRMACION_NOMINAL_REVISADA'
            reply_gerund = review.get('Tipo_Limite') == 'GERUNDIO_RESPUESTA_VARIANTE_REVISADA'
            nominal_gerund = review.get('Tipo_Limite') == 'GERUNDIO_NOMINAL_EXPLICITO_REVISADO' or confirming_gerund or reply_gerund
            gerund = review.get('Tipo_Limite') == 'GERUNDIO_SENALANDO_EXPLICITO' or fiscal_reply or nominal_gerund
            if gerund:
                # Sólo esta decisión con hash/citas habilita el gerundio con
                # sujeto explícito pospuesto. Proyectar el predicado únicamente
                # para reconocer su sujeto; nunca modificar el texto guardado.
                if fiscal_reply:
                    # Referente nominal en la consulta contigua, no un Fiscal global.
                    antecedent=re.search(r'solicita al Fiscal señor ([^,.;!?]{1,100}) que precise [^.!?]+,\s*$',prefix)
                    lead='indicando el señor Fiscal'
                    if not antecedent or not fragment.startswith(lead+' que '):
                        raise ValueError('Respuesta fiscal sin consulta nominal contigua')
                    fragment='indica el señor '+antecedent[1]+fragment[len(lead):]
                elif nominal_gerund:
                    predicates={'respondiendo':'responde','acotando':'acota',
                                'comentando':'comenta','explicando':'explica',
                                'precisando':'precisa','agregando':'agrega'}
                    if confirming_gerund:
                        predicates={'confirmando':'confirma'}
                    if reply_gerund:
                        # Sólo fichas con hash y sujeto nominal: la réplica se
                        # proyecta para validación, no se reescribe ni se agrega
                        # un verbo al detector automático de turnos.
                        predicates={'afirmando':'afirma','replicando':'responde',
                                    'consignando':'consigna'}
                    head=re.match(r'^(\w+) (?=(?:el|la)\b)',fragment)
                    if not head or head[1] not in predicates or not prefix.rstrip().endswith((',', ';')):
                        raise ValueError('Gerundio nominal revisado sin predicado/separador válido')
                    fragment=predicates[head[1]]+fragment[len(head[1]):]
                else:
                    if not prefix.rstrip().endswith((',', ';')) or not re.match(r'^señalando\s+(?:el|la)\s+', fragment):
                        raise ValueError("Revisión de gerundio sin límite válido")
                    fragment = 'señala' + fragment[len('señalando'):]

            coordinated = review.get('Tipo_Limite') == 'COORDINACION_Y_EXPLICITA'
            artifact = review.get('Tipo_Limite') == 'INICIO_TRAS_ARTEFACTO_REVISADO'
            if artifact:
                noise = review.get('Cita_Artefacto')
                if (noise != "-4 . f . • \" ' A) " or not prefix.endswith(noise)
                        or not prefix[:-len(noise)].rstrip().endswith('.')
                        or not fragment.startswith('El señor Sergio Lehmann insiste en que ')):
                    raise ValueError('Artefacto revisado sin separador y sujeto exactos')
                prefix = prefix[:-len(noise)]
            concatenated = review.get('Tipo_Limite') == 'CONCATENACION_EXPLICITA_REVISADA' or artifact
            causal_reply = review.get('Tipo_Limite') == 'RESPUESTA_POR_LO_QUE_EXPLICITA'
            reply_muestra = review.get('Tipo_Limite') == 'RESPUESTA_A_LO_CUAL_MUESTRA_REVISADA'
            reply_cual = review.get('Tipo_Limite') == 'RESPUESTA_A_LO_CUAL_EXPLICITA'
            reply = review.get('Tipo_Limite') == 'RESPUESTA_A_LO_QUE_EXPLICITA' or causal_reply or reply_muestra or reply_cual
            if reply:
                # Excepción individual: conservar el conector, sin inventar coma.
                lead = 'a lo cual' if (reply_muestra or reply_cual) else ('por lo que' if causal_reply else 'a lo que')
                if (not re.match(r'^'+lead+r'\s+(?:el|la)\s+', fragment) or not prefix or not prefix[-1].isspace()
                        or ((causal_reply or reply_cual) and not prefix.rstrip().endswith(','))):
                    raise ValueError("Revisión de respuesta sin límite válido")
                if reply_muestra:
                    # Proyección exclusivamente para validar el sujeto nominal; no reescribir.
                    if not prefix.rstrip().endswith(',') or not re.match(r'^a lo cual el señor [^,.;!?]{1,100} muestra que\b',fragment):
                        raise ValueError('Respuesta muestra sin predicado/límite válido')
                    fragment=re.sub(r' muestra que\b',' señala que',fragment[len(lead):].lstrip(),count=1)
                if causal_reply:
                    # Proyección para reconocer el sujeto; el conector literal se conserva.
                    fragment = fragment[len(lead):].lstrip()
            if concatenated:
                # Texto dañado sin separador: sólo el intervalo con hash/citas.
                # No completar la frase anterior ni generalizar a mayúsculas.
                if not prefix or not prefix[-1].isspace() or not fragment[:1].isupper():
                    raise ValueError("Revisión de concatenación sin límite válido")
            if coordinated:
                # Sólo una entrada con hash/citas permite este corte. Nunca
                # interpretar automáticamente todas las coordinaciones con «y».
                if not re.match(r'^y,?\s+(?:(?:sobre este aspecto|en (?:este|ese) sentido),?\s+)?(?:el|la)\s+',fragment) or not prefix or not prefix[-1].isspace():
                    raise ValueError("Revisión de coordinación sin límite válido")
                fragment = re.sub(r'^y,?\s+', '', fragment)
            acknowledgement = review.get('Tipo_Limite') == 'CESION_AGRADECIMIENTO_RELATIVO_EXPLICITO'
            statement = review.get('Tipo_Limite') == 'CESION_HACE_PRESENTE_RELATIVA_EXPLICITA'
            analysis_ack = review.get('Tipo_Limite') == 'CESION_AGRADECIMIENTO_ANALISIS_REVISADA'
            relative = review.get('Tipo_Limite') == 'CESION_RELATIVA_EXPLICITA' or acknowledgement or statement or analysis_ack
            opinion_quote = review.get('Tipo_Limite') == 'OPINION_TRAS_CITA_CERRADA_REVISADA'
            return_quote = review.get('Tipo_Limite') == 'RETORNO_TRAS_CITA_CERRADA_REVISADA'
            if return_quote:
                # Retorno nominal después del comunicado cerrado; sólo por revisión con hash.
                if not re.match(r'^Antes de concluir la Reunión, (?:el|la) ', fragment) or not re.search(r'[.!?][”»"]$', prefix.rstrip()):
                    raise ValueError('Retorno revisado sin cita cerrada/límite válido')
                # Proyección sólo para validar el sujeto; el texto guardado no cambia.
                fragment = fragment[len('Antes de concluir la Reunión, '):]
            if opinion_quote:
                # Excepción sólo con revisión individual: cita cerrada antes de
                # una opinión nominal. No divide automáticamente por comillas.
                head = re.match(r'^(?:En opinión|A juicio) del ([^,.;!?“”«»"]{1,180}),', fragment)
                if not head or not re.search(r'[.!?][”»"]$', prefix.rstrip()):
                    raise ValueError("Opinión revisada sin cita cerrada/límite válido")
                candidate = TURN_DETECTOR.speaker('El '+head[1]+' señala.', date)
            elif relative:
                # Sólo el antecedente contiguo en esta oración, nunca otra cesión
                # anterior. La revisión y su hash delimitan la relativa adjudicada.
                sentence_start = max(a for a,b in spans if a <= review['Inicio'])
                candidate = TURN_DETECTOR.reviewed_relative_handoff(
                    text[sentence_start:review['Inicio']], fragment, date, acknowledgement=acknowledgement, statement=statement, analysis_ack=analysis_ack)
            else:
                candidate = TURN_DETECTOR.speaker(fragment,date)
            if (passive_reply or relative_reply or assumption_declaration or role_handoff) and (not candidate or candidate['method'] not in {'SUJETO_NOMBRE','SUJETO_ROL_NOMBRE'}):
                raise ValueError('Respuesta revisada sin sujeto nominal explícito')
            if nominal_gerund and (not candidate or candidate['method'] not in {'SUJETO_NOMBRE','SUJETO_ROL_NOMBRE'}):
                raise ValueError('Gerundio revisado sin sujeto nominal explícito')
            if gerund and (not candidate or not re.match(r'^\s*,?\s*que\b', normalize_turn(fragment)[candidate['end']:])):
                raise ValueError("Revisión de gerundio sin declaración válida")
            quoted = prefix.count('"') % 2 or prefix.count('“') > prefix.count('”') or prefix.count('«') > prefix.count('»')
            if ((not (coordinated or concatenated or reply or opinion_quote or return_quote or passive_reply or relative_reply or role_handoff) and not prefix.rstrip().endswith((',', ';'))) or quoted or not candidate
                    or candidate['actor'] != review['Actor'] or candidate['method'] not in EXPLICIT):
                raise ValueError("Revisión de hablante sin actor/límite válido")
            bounds = sorted({0,len(text),review["Inicio"]} | {a for a,b in spans} | {b for a,b in spans})
            spans = list(zip(bounds,bounds[1:]))
    # Opt-in con cita y hash: Fin solo NO crea cortes. Esta excepción conserva
    # una identificación explícita posterior del mismo expositor, sin convertir
    # CONTEXTO_REVISADO en ancla ni inventar un cambio de persona.
    explicit_review_ends = set()
    for entry in intervals:
        if 'Cita_Ancla_Posterior' not in entry:
            continue
        end = entry['Fin']
        tail = text[end:]
        anchor_quote = entry['Cita_Ancla_Posterior']
        prefix = text[:end]
        candidate = TURN_DETECTOR.speaker(tail, date)
        quoted = prefix.count('"') % 2 or prefix.count('“') > prefix.count('”') or prefix.count('«') > prefix.count('»')
        if (not isinstance(anchor_quote, str) or not anchor_quote or not tail.startswith(anchor_quote)
                or end not in {a for a,b in spans} or quoted or not candidate
                or candidate['actor'] != entry['Actor'] or candidate['method'] not in EXPLICIT):
            raise ValueError('Ancla posterior revisada sin sujeto explícito compatible')
        explicit_review_ends.add(end)
    author = TURN_DETECTOR.minute_author(text,date)
    if author:
        return bound_segments([(text,author,'ENCABEZADO_MINUTA')])
    if is_header2(text):
        return bound_segments([(text, CONSEJO, 'ACTA/META')])
    segments = []
    start, actor, method = 0, initial_actor, None
    context = dict((state or {}).get('roles', {})) if initial_actor in ((state or {}).get('actor'), (state or {}).get('pending')) else {}
    method = 'CONTINUIDAD_PARRAFO' if continuation_start(text, initial_actor, state, TURN_DETECTOR, split_sentences, date) else None
    def remember(who):
        role = roster_role_for(date, who) if who and who != CONSEJO else None
        if role:
            context[role] = who
            if role.startswith('Gerente'):
                context['Gerente'] = who
                if role.startswith('Gerente de División'):
                    context['Gerente de División'] = who
    if not context:
        remember(actor)
    previous_sentence = (state or {}).get('last_sentence', '')
    for a, b in spans:
        sent = text[a:b]
        if not sent.strip():
            continue
        local_context = {**context, **TURN_DETECTOR.referents(previous_sentence,date)}
        previous_sentence = sent
        candidate = TURN_DETECTOR.speaker(sent, date, actor, local_context)
        institutional = _inst_transition(sent)
        # La hora no vuelve institucional a un sujeto personal explícito que
        # abre/reanuda la sesión. «Se reanuda» sin tal sujeto sigue siendo acta.
        timed_personal = bool(candidate and candidate['method'] in EXPLICIT
                and re.match(r'^siendo las? (?:[01]?\d|2[0-3])[:.][0-5]\d horas,', normalize_turn(sent)))
        if timed_personal:
            institutional = False
        local_review = reviews_by_start.get(a)
        if local_review:
            if candidate and candidate["actor"] != local_review["Actor"]:
                raise ValueError("Revisión contradice sujeto explícito")
            who, source = local_review["Actor"], SPEAKER_REVIEW_SOURCE
        elif institutional:
            who, source = CONSEJO, 'ACTA/META'
        elif candidate:
            who, source = candidate['actor'], candidate['method']
            if (source == 'ANAFORA_LOCAL' and state and state.get('anchor')
                    and not state.get('barrier') and who == actor == state.get('actor')
                    and initial_actor == who):
                source = 'ANAFORA_CONTINUIDAD'
        else:
            continue
        if (who != actor or a in explicit_review_ends or local_review or timed_personal) and a > start:
            segments.append((text[start:a].strip(), actor, method))
            start, method = a, None
        actor = who
        method = method or source
        remember(actor)
        recipient = TURN_DETECTOR.handoff(sent, date)
        if recipient:
            remember(recipient)
    segments.append((text[start:].strip(), actor, method))
    if state is not None:
        state['roles'] = context
        state['last_sentence'] = previous_sentence
    if re.sub(r'\s+', '', ''.join(t for t, _, _ in segments)) != re.sub(r'\s+', '', text):
        raise ValueError('La segmentación perdió contenido')
    return bound_segments(segments)


def bound_segments(segments):
    # Fracciones físicas XLSX, no cambios de hablante. El bloque permite reunirlas.
    bounded = []
    for body, who, source in segments:
        while len(body) > 32767:
            ends = [b for a,b in split_sentences(body) if b <= 32000]
            cut = max(ends) if ends else body.rfind(' ', 0, 32000)
            if cut <= 0:
                raise ValueError('Texto largo sin límite seguro de fragmentación')
            bounded.append((body[:cut].strip(), who, source))
            body, source = body[cut:].strip(), 'CONTINUACION_XLSX'
        bounded.append((body, who, source))
    return bounded


# taxonomy
def cat(kw):
    k=norm(kw)
    if any(norm(x) in k for x in ['acuerdo','comunicado','adopción unánime','levantamiento']): return 'acuerdo_comunicado'
    if any(norm(x) in k for x in ['votación','voto','fundamentación de voto','llamado a votación','pase votación','apertura votación']): return 'decision_tpm'
    if any(norm(x) in k for x in ['opciones','minuta de opciones']): return 'opciones_tpm'
    if any(norm(x) in k for x in ['inflación','expectativas inflación','ipcx','subyacente','presiones de precios']): return 'inflacion'
    if any(norm(x) in k for x in ['mercado laboral','empleo','desempleo','participación laboral','salario','estrechez']): return 'mercado_laboral'
    if any(norm(x) in k for x in ['liquidez','curva','tasas','tipo de cambio','bonos','spread','interbancario','mercado monetario','renta fija','fondeo','financiero']): return 'mercados_financieros'
    if any(norm(x) in k for x in ['internacional','estados unidos','europa','china','brasil','ee.uu','weo','fed','commodities','petróleo','cobre','molibdeno','materias primas','mundial','global']): return 'escenario_internacional'
    if any(norm(x) in k for x in ['fiscal','hacienda','gasto público','superávit fiscal','deuda soberana','subsidio','regla fiscal']): return 'politica_fiscal'
    if any(norm(x) in k for x in ['actividad interna','actividad económica','demanda','inversión','consumo','imacec','pib','producto potencial','brecha del producto','industria','gasto']): return 'actividad_interna'
    if any(norm(x) in k for x in ['riesgo','balance','incertidumbre']): return 'riesgos'
    if any(norm(x) in k for x in ['apertura','asistencia','calendario','presidencia','inicio de sesión','invitaciones','orden','suspensión','reanudación','cierre','se levanta']): return 'apertura_cierre'
    if any(norm(x) in k for x in ['discusión','debate','deliberación','comentarios','traspaso','preguntas','ronda']): return 'debate'
    return 'otros'

def main():
    FULL_TEXTS = load_full_texts()
    reviewed_roles = load_role_reviews({int(r[0]): {"Fecha":to_date_str(r[1]),"Texto":str(r[5])} for r in data})
    reviewed_speakers = load_speaker_reviews({int(r[0]): {"Fecha":to_date_str(r[1]),"Texto":str(r[5])} for r in data})
    reviewed_institutions = load_institutional_reviews({int(r[0]): {'Fecha':to_date_str(r[1]),'Texto':str(r[5])} for r in data})
    DATA_PROC.mkdir(parents=True, exist_ok=True)
    # ---- process ----
    load_formula_reviews(raw_by_id={int(r[0]): {"Texto":str(r[5])} for r in data})
    reviewed_documents = load_document_reviews({int(r[0]): {'Fecha':to_date_str(r[1]),'Texto':str(r[5])} for r in data})
    context_alerts = load_context_warnings({int(r[0]): {'Fecha':to_date_str(r[1]),'Texto':str(r[5])} for r in data})
    _formula = is_formula
    _parent_meta={int(str(r[0])):str(r[5]) for r in data}
    _parent_texts=collections.Counter(_parent_meta.values())
    _parent_trunc=set(pid for pid,t in _parent_meta.items() if len(t)>=32767)
    _parent_near=set(pid for pid,t in _parent_meta.items() if 30000<=len(t)<32767)
    _parent_dup=set(pid for pid,t in _parent_meta.items() if _parent_texts[t]>1)
    _parent_dup_formula=set(pid for pid in _parent_dup if _formula(_parent_meta[pid]))

    records=[]; last_speaker={}; actor_corr=0; role_corr=0; method_counter=collections.Counter(); role_method_counter=collections.Counter()
    _seg_per_parent=collections.Counter(); _rid=0
    session_states = {}
    for r in data:
        parent_id=int(r[0]); date=to_date_str(r[1]); date_dt=dt.date.fromisoformat(date)
        actor_orig=str(r[2]).strip(); rol_orig=str(r[3]).strip()
        text=FULL_TEXTS.get(parent_id, {}).get('Texto_Completo', str(r[5]))
        if len(str(r[5])) >= 32767 and parent_id not in FULL_TEXTS:
            raise ValueError(f'Texto truncado sin recuperación: {parent_id}')
        state = session_states.setdefault(date, {'date': date})
        seg_texts=segment_turns(text,date,actor_orig,state,reviewed_speakers.get(parent_id),reviewed_documents.get(parent_id),reviewed_institutions.get(parent_id))
        _seg_per_parent[parent_id]+=len(seg_texts)
        block_number=0
        for segment_number, (text, segment_actor, segment_method) in enumerate(seg_texts, 1):
            if segment_method != "CONTINUACION_XLSX": block_number+=1
            _rid+=1; rid=_rid
            det=(segment_actor, None, segment_method, 0) if segment_method else detect(text,date)
            if det:
                spk,role,method,_=det
            else:
                spk=None; role=None; method='SIN_DETECTAR'
            # Si la primera oración de la intervención ya identifica un hablante explícito,
            # se prefiere ese hablante por sobre heurísticas posteriores del texto.
            hint=None if segment_method else first_speaker_hint(text,date)
            if hint and hint in REAL and hint!=spk:
                spk=hint; role=None; method='PRIMERA_ORACION'
            if spk and spk not in REAL and spk!=CONSEJO:
                method='PSEUDO'
                spk=None; role=None
            if spk in REAL:
                last_speaker[date]=spk
            # choose speaker
            if spk:
                pass
            elif session_meta(text):
                spk=CONSEJO; role='Consejo'; method='META'
            elif actor_orig in REAL:
                spk=actor_orig; role=None; method='ORIGINAL'
            else:
                prev=last_speaker.get(date)
                spk=prev if prev else actor_orig
                role=None
                method='HERENCIA' if prev else 'SIN_DETECTAR'
            if spk!=actor_orig and spk!=CONSEJO:
                actor_corr+=1
            # role
            rol=rol_orig if spk==actor_orig else (roster_role_for(date,spk) or canonical_role_by_actor(spk,date) or '')
            if method in ('ACTA/META','META') and spk==CONSEJO:
                rol='Consejo'
            # Política conservadora: Rol_Final = Rol_Fuente (cargo del PDF/source).
            # Solo se corrigen casos indudables:
            #   - actas/metadata del Consejo -> rol Consejo
            #   - Rodrigo Valdés antes de 2015 cuando el acta lo presenta como Gerente
            #   - género/subrogante de Hacienda confirmado por el texto
            if spk=='Rodrigo Valdés Pulido' and date_dt<FULL_MIN_START['Rodrigo Valdés Pulido'] and role and role.startswith('Gerente'):
                rol=role
            elif spk in KNOWN_MIN and ('Hacienda' in rol or 'Subsecretario' in rol) and not (spk=='Rodrigo Valdés Pulido' and date_dt<FULL_MIN_START['Rodrigo Valdés Pulido']):
                rol=ministry_role(text,spk,date_dt)
            # Fuente canónica de cargo: lista de asistencia del primer párrafo del acta.
            # Se aplica solo cuando la coincidencia nombre/cargo es única y exacta.
            rol_asistencia=None
            if spk and spk!=CONSEJO:
                rr=roster_role_for(date,spk)
                if rr:
                    rol_asistencia=rr
                    rol=rr
            metodo_rol='LISTA_ASISTENCIA' if rol_asistencia else ('ACTA_INSTITUCIONAL' if (method in ('ACTA/META','META') and spk==CONSEJO) else 'PENDIENTE_REVISION')
            review = reviewed_roles.get((parent_id,spk))
            if review:
                if rol_asistencia and rol != review['Rol']:
                    raise ValueError(f'Cargo de asistencia contradice {review["Revision_ID"]}')
                if not rol_asistencia:
                    rol = review['Rol']
                    metodo_rol = review['Fuente_Rol']
            if method == AUTHOR_SOURCE:
                # El cargo consta en el escrito recibido; no acredita asistencia.
                rol = reviewed_documents[parent_id]['Rol_Autor']
                rol_asistencia = None
                metodo_rol = DOCUMENT_ROLE_SOURCE
            tipo = (institutional_type(text, reviewed_institutions[parent_id]) if parent_id in reviewed_institutions
                    else tipo_acta(text) if metodo_rol=='ACTA_INSTITUCIONAL' else '')
            # La fila porta la decisión de TPM de la sesión -> ACUERDO_CONSEJO,
            # incluso si quedó tipificada como COMUNICADO (el texto del comunicado
            # repite la fórmula del acuerdo) o si es fila de persona que arrastra
            # el bloque del acuerdo.
            if method == AUTHOR_SOURCE:
                tipo = DOCUMENT_TYPE
            elif method == 'ENCABEZADO_MINUTA':
                tipo = 'MINUTA_PERSONAL'
            elif _is_current_decision(text):
                tipo = 'ACUERDO_CONSEJO'
            if rol!=rol_orig: role_corr+=1
            method_counter[method]+=1
            role_method_counter[metodo_rol]+=1
            records.append((rid,date,date_dt,actor_orig,spk,rol,rol_orig,role,method,int(r[4]),text,str(r[6]),str(r[7]),rol_asistencia,metodo_rol,tipo,parent_id,block_number))
            update_state(state, spk, method, text, date, TURN_DETECTOR,
                         split_sentences, rid, institutional=bool(tipo))
            if contextual_motives(dict(ID_Padre=parent_id,Fecha=date,Actor_Final=spk,Texto=text),context_alerts):
                state['barrier'] = True
                state['anchor'] = None

    print("Actors reasignados:",actor_corr)
    print("Roles cambiados:",role_corr)
    print("Métodos:",dict(method_counter))
    print("Fuente_Rol:",dict(role_method_counter))

    outwb=openpyxl.Workbook(); ows=outwb.active; ows.title='Consolidado'
    header=['ID','ID_Padre','Id_Sesion','Fecha','Actor_Original','Actor_Final','Actor_Corregido','Rol_Fuente','Rol_Final','Rol_Corregido','Rol_Detectado_Texto','Rol_Lista_Asistencia','Fuente_Rol','Tipo_Acta','Fuente_Actor','Página','Texto','Tema_Original','Tema_Categoria','Palabra_Clave_Original','Palabra_Clave_Categoria','Texto_Truncado','Duplicado_Exacto','Duplicado_Formula','Nota','ID_Intervencion','Numero_Segmento','Fuente_Texto','Duplicado_Exacto_Origen','Duplicado_Formula_Origen','ID_Bloque_Texto']
    ows.append(header)
    segment_counts=collections.Counter()
    clean_text=lambda t: re.sub(r'\s*\n\s*','\n',re.sub(r'[ \t]+',' ',t))
    exact_counts=collections.Counter(clean_text(rec[10]) for rec in records)
    for rec in records:
        rid,date,date_dt,actor_orig,spk,rol,rol_orig,role,method,page,text,tema,kw,rol_asistencia,metodo_rol,tipo,id_padre,block_number=rec
        clean=re.sub(r'[ \t]+',' ',text); clean=re.sub(r'\s*\n\s*','\n',clean)
        segment_counts[id_padre]+=1
        segment_number=segment_counts[id_padre]
        if len(clean)>32767:
            raise ValueError(f'Intervención {id_padre}/{segment_number} excede XLSX; no se truncará')
        note=[]
        if normalize_quote(clean) in FORMULA_REVIEWS:
            note.append("Fórmula procedimental revisada: " + FORMULA_REVIEWS[normalize_quote(clean)]["Revision_ID"])
        if id_padre in reviewed_institutions and method == 'ACTA/META':
            e = reviewed_institutions[id_padre]
            note.append(INSTITUTIONAL_NOTE+e['Revision_ID']+' (data/curation/revisiones_continuaciones_acta.json; no habla personal ni cotejo PDF)')
        if id_padre in reviewed_institutions and method != 'ACTA/META':
            e = reviewed_institutions[id_padre]
            note.append('Reanudación nominal revisada: '+e['Revision_ID']+' (data/curation/revisiones_continuaciones_acta.json; expositor nominal, sin cotejo PDF)')
        if method == SPEAKER_REVIEW_SOURCE:
            applicable = [r for r in speaker_intervals(reviewed_speakers[id_padre])
                          if r['Actor']==spk and normalize_quote(clean).startswith(normalize_quote(r['Cita_Inicio']))]
            if len(applicable) != 1:
                raise ValueError('Nota de hablante revisado sin intervalo único')
            note.append(f'Hablante por contexto documentado: {applicable[0]["Revision_ID"]} (data/curation/revisiones_hablantes.json; no cotejo PDF)')
        if method in (AUTHOR_SOURCE, READER_SOURCE):
            doc = reviewed_documents[id_padre]
            note.append(f"Lectura documental {doc['Revision_ID']}: autor={doc['Autor']}; lector={doc['Lector']}; asistencia del autor no inferida; data/curation/revisiones_documentos_leidos.json")
        review = reviewed_roles.get((id_padre,spk))
        if review:
            note.append(f'Revisión documental de cargo: {review["Revision_ID"]} (data/curation/revisiones_roles.json; no cotejo PDF)')
        if id_padre in _parent_trunc: note.append('Texto truncado en celda Excel (32,767)')
        if id_padre in _parent_near: note.append('Texto muy largo (>=30,000)')
        if id_padre in _parent_dup: note.append('Texto duplicado exacto'+(' (probable fórmula)' if id_padre in _parent_dup_formula else ''))
        if role: note.append('Rol detectado en texto: '+role)
        if rol_asistencia: note.append('Rol según lista de asistencia: '+rol_asistencia)
        if not rol_asistencia and metodo_rol=='PENDIENTE_REVISION':
            note.append('Sin cargo único en lista de asistencia; revisar manualmente')
        if method in ('HERENCIA','SIN_DETECTAR','ORIGINAL','PSEUDO'): note.append('Método: '+method)
        # estado de texto largo: completo en textos_completos.jsonl (por fila original)
        if id_padre in FULL_TEXTS:
            ft=FULL_TEXTS[id_padre]
            note.append(f'Texto completo ({ft.get("Longitud_Texto_Completo",len(str(ft.get("Texto_Completo",""))))} chars) en data/processed/textos_completos.jsonl')
            tc='NO'
        else:
            tc='SI' if id_padre in _parent_trunc else 'REV' if id_padre in _parent_near else 'NO'
        ows.append([rid,id_padre,'RPM-'+date,date_dt,actor_orig,spk,'SI' if spk!=actor_orig else 'NO',
                    rol_orig,rol,'SI' if rol!=rol_orig else 'NO',role if role else '',
                    rol_asistencia if rol_asistencia else '',metodo_rol,tipo,method,page,clean,
                    tema,cat(tema),kw,cat(kw),
                    tc,
                    'SI' if exact_counts[clean]>1 else 'NO','SI' if exact_counts[clean]>1 and _formula(clean) else 'NO','; '.join(note),
                    f'RPM-{date}:{id_padre}:{segment_number}',segment_number,
                    FULL_TEXTS.get(id_padre,{}).get('Fuente','XLSX_ORIGINAL'),
                    'SI' if id_padre in _parent_dup else 'NO','SI' if id_padre in _parent_dup_formula else 'NO',
                    f'RPM-{date}:{id_padre}:B{block_number}'])

    ows.cell(1, len(header)+1, 'Estado_Revision')
    ows.cell(1, len(header)+2, 'Motivos_Revision')
    review_count=0
    for row in ows.iter_rows(min_row=2):
        obj=dict(zip(header, [c.value for c in row[:len(header)]]))
        reasons=sorted(set(review_reasons(obj, TURN_DETECTOR, split_sentences)+contextual_motives(obj,context_alerts)))
        state='PENDIENTE_REVISION' if reasons else 'SIN_ALERTAS_AUTOMATICAS'
        ows.cell(row[0].row, len(header)+1, state)
        ows.cell(row[0].row, len(header)+2, ';'.join(reasons))
        review_count+=bool(reasons)
    context_header = header + ['Estado_Revision','Motivos_Revision']
    context_rows = [dict(zip(context_header, vals)) for vals in ows.iter_rows(min_row=2, values_only=True)]
    annotate_turns(context_rows, load_reviewed_links({int(r[0]): {"Fecha":to_date_str(r[1]),"Texto":str(r[5])} for r in data}))
    continuity_fields = ['ID_Turno','Relacion_Turno','ID_Antecedente_Continuidad','ID_Ancla_Actor']
    for j,key in enumerate(continuity_fields,len(context_header)+1):
        ows.cell(1,j,key)
        for i,obj in enumerate(context_rows,2):
            ows.cell(i,j,obj[key])
    md=outwb.create_sheet('Calidad'); md.append(['Indicador','Valor'])
    md.append(['Filas originales',len(data)])
    md.append(['Filas con alertas de revisión (no errores confirmados)',review_count])
    md.append(['Intervenciones (filas tras segmentar)',len(records)])
    md.append(['Filas divididas en intervenciones',sum(1 for n in _seg_per_parent.values() if n>1)])
    md.append(['Sesiones',len(set(x[1] for x in records))])
    md.append(['Fecha min',min(x[1] for x in records)]); md.append(['Fecha max',max(x[1] for x in records)])
    md.append(['Actores reasignados',actor_corr]); md.append(['Roles corregidos',role_corr])
    md.append(['Roles desde lista de asistencia',sum(1 for x in records if x[13])])
    md.append(['Filas sin cargo único en lista de asistencia (revisar)',sum(1 for x in records if x[14]=='PENDIENTE_REVISION')])
    md.append(['Fuente_Rol',str(dict(role_method_counter))])
    md.append(['Textos truncados sin resolver',len([i for i in _parent_trunc if i not in FULL_TEXTS])])
    md.append(['Textos largos sin revisar',len([i for i in _parent_near if i not in FULL_TEXTS])])
    md.append(['Textos con texto completo en JSONL',len(FULL_TEXTS)])
    md.append(['Duplicados exactos (intervenciones)',sum(n for n in exact_counts.values() if n>1)])
    md.append(['Duplicados fórmula (intervenciones)',sum(n for t,n in exact_counts.items() if n>1 and _formula(t))])
    md.append(['Duplicados exactos (origen)',len(_parent_dup)])
    md.append(['Duplicados fórmula (origen)',len(_parent_dup_formula)])
    md.append(['Métodos',str(dict(method_counter))])

    md2=outwb.create_sheet('Fuente_Actor'); md2.append(['Fuente_Actor','Registros'])
    for k,v in method_counter.most_common(): md2.append([k,v])
    md3=outwb.create_sheet('Fuente_Rol'); md3.append(['Fuente_Rol','Registros'])
    for k,v in role_method_counter.most_common(): md3.append([k,v])
    rc=collections.Counter(x[5] for x in records); cd=outwb.create_sheet('Diccionario_Rol'); cd.append(['Rol','Registros'])
    for k,v in rc.most_common(): cd.append([k,v])
    ac=collections.Counter(x[4] for x in records); ad=outwb.create_sheet('Diccionario_Actor'); ad.append(['Actor','Registros'])
    for k,v in ac.most_common(): ad.append([k,v])
    kc=collections.Counter(cat(x[12]) for x in records); catws=outwb.create_sheet('Diccionario_Categoria'); catws.append(['Categoria','Registros'])
    for k,v in kc.most_common(): catws.append([k,v])
    if FULL_TEXTS:
        ftws=outwb.create_sheet('Textos_Completos')
        _ft_headers=['ID','Id_Sesion','Fecha','Página','Paginas_PDF','Archivo_PDF','Actor','Rol','Tema','Palabra_Clave','Texto_Completo','Longitud_Excel','Longitud_Texto_Completo','Fuente','Ubicacion_Texto_Completo']
        ftws.append(_ft_headers)
        for k in sorted(FULL_TEXTS):
            ft=FULL_TEXTS[k]
            ftws.append([ft.get('ID',''),ft.get('Id_Sesion',''),ft.get('Fecha',''),ft.get('Página',''),
                         ft.get('Paginas_PDF',''),ft.get('Archivo_PDF',''),ft.get('Actor',''),ft.get('Rol',''),
                         ft.get('Tema',''),ft.get('Palabra_Clave',''),
                         'Ver texto completo en data/processed/textos_completos.jsonl (el XLSX limita la celda a 32,767 chars)',
                         ft.get('Longitud_Excel',''),ft.get('Longitud_Texto_Completo',''),ft.get('Fuente',''),'data/processed/textos_completos.jsonl'])

    for row in ows.iter_rows(min_row=2,max_row=ows.max_row,min_col=4,max_col=4):
        for c in row:
            if isinstance(c.value,dt.date): c.number_format='YYYY-MM-DD'
    for sheet in outwb.worksheets:
        for j,col in enumerate(sheet.iter_cols()):
            if not col: continue
            w=min(max(max((len(str(c.value)) for c in col[:300] if c.value is not None),default=8)+2,10),60)
            sheet.column_dimensions[col[0].column_letter].width=w
    ows.freeze_panes='A2'
    outwb.save(OUT); print("Saved",OUT)


if __name__ == "__main__":
    main()
