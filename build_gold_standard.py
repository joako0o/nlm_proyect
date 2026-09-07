# -*- coding: utf-8 -*-
"""
Gold Standard del consolidado RPM v2.
- Re-etiqueta hablante solo cuando el texto lo confirma.
- Corrige roles (Hacienda/subrogante y rol explicito).
- Fecha real + Id_Sesion + taxonomia canonica + flags.
"""
import openpyxl, re, collections, datetime as dt

SRC='consolidado_final.xlsx'; OUT='consolidado_goldstandard.xlsx'
wb=openpyxl.load_workbook(SRC, data_only=True, read_only=True)
ws=wb['Consolidado']; data=list(ws.iter_rows(values_only=True))[1:]

CONSEJO='Consejo del Banco Central de Chile'
PSEUDO={'Gerente de División Internacional','Gerente de División Estudios Subrogante','Gerente de Investigación Económica','Gerente de Operaciones Financieras','Gerente de Área Técnica','Gerente de Estabilidad Financiera'}
EXTRA_ACTORS={'María Eugenia Wagner Brizzi','Rodrigo Alfaro'}
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

VERBS=['señala','indica','manifiesta','expresa','dice','comenta','interviene','estima','consulta','afirma','responde','agrega','agregar','precisa','plantea','pregunta','informa','expone','menciona','hace presente','continúa','prosigue','solicita','opina','acota','destaca','recuerda','observa','concluye','inicia','apoya','coincide','agradece','aclara','considera','señalando','planteando','comentando','ofrece la palabra','concede la palabra','da la palabra','da comienzo','informa que','manifiesta estar','deja planteado','formula','señalando que','hace presente que','fija','da cuenta','explica','explica que','explicó','explicando','señaló','manifestó','indicó','expresó','comentó','preguntó','respondió','agregó','precisó','planteó','subrayó','recalcó','advirtió','destacó','da inicio','da inicio a','dio inicio','dio inicio a','piensa','piensa que','cree','considera','acepta','refiriéndose','refiere','se refiere','refiriéndose a']
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
 'Rodrigo Alfaro':'alfaro'
}
# extra surname aliases (second surname sometimes used)
EXTRA={('Rodrigo Vergara Montes','montes'),('Rodrigo Valdés Pulido','pulido'),('Manuel Marfán Lewis','lewis'),
       ('Sebastián Claro Edwards','edwards'),('Claudio Soto Gamboa','gamboa'),('Enrique Marshall Rivera','rivera'),
       ('Luis Óscar Herrera Barriga','barriga'),('Joaquín Vial Ruiz-Tagle','ruiz-tagle'),
       ('Alberto Arenas de Mesa','de mesa'),('Diego Gianelli Gómez','gomez'),('Felipe Larraín Bascuñán','bascunan'),
       ('Klaus Schmidt-Hebbel Dunker','dunker'),('Luis Felipe Céspedes Cifuentes','cifuentes'),
       ('María Elena Ovalle Molina','molina'),('María Olivia Recart Herrera','herrera'),('María Eugenia Wagner Brizzi','wagner'),('Rodrigo Alfaro','alfaro'),
       ('Mario Marcel Cullell','cullell'),('Camilo Carrasco Alfonso','alfonso'),('Miguel Ricaurte Bermúdez','bermudez')}

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
            for a in acts:
                ds=[dt.date.fromisoformat(to_date_str(x[1])) for x in data if str(x[2]).strip()==a]
                dist=min(abs((x-d).days) for x in ds) if ds else 10**9
                if bd is None or dist<bd:
                    bd=dist; best=a
            if best: return best
    return max(acts,key=lambda a:sum(1 for x in data if str(x[2]).strip()==a))

def resolve_name(name,date=None):
    n=norm(name).strip()
    if not n: return None
    exact=[a for a in REAL if norm(a)==n or norm(SURNAME.get(a,''))==n or n in [norm(x) for x in [SURNAME.get(a,''),a]]]
    if len(exact)==1: return exact[0]
    if len(exact)>1: return _nearest_actor(exact,date)
    cand=[]
    for a in REAL:
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
    # full without accents already normalized
    for alt in alts:
        if len(alt)>3 and (len(alt.split())>1 or len(alt)>=4):
            alias_map[alt].add(a)

# alias extra: Maria Eugenia Wager (variante OCR del acta)
alias_map['wager'].add('María Eugenia Wagner Brizzi')
alias_map['maria wager'].add('María Eugenia Wagner Brizzi')
alias_map['maria eugenia wager'].add('María Eugenia Wagner Brizzi')
alias_map['maria eugenia wagner'].add('María Eugenia Wagner Brizzi')

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
            _nm=re.match(r'\s*[-,;]?\s*(?:señor|señora|don|doña|sr\.|sra\.)?\s*([A-ZÁÉÍÓÚÑ][\wáéíóúñÁÉÍÓÚÑ]+(?:\s+[A-ZÁÉÍÓÚÑ][\wáéíóúñÁÉÍÓÚÑ]+){0,4})', _after)
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
def actor_for_role(date,role):
    def _top(cnt):
        if not cnt: return None
        top=[x for x,n in cnt.most_common() if x in REAL]
        return top[0] if top else None
    if date:
        d=dt.date.fromisoformat(str(date))
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
        dates=sorted({dat for (dat,rv) in ROLE_DATE_ACTOR for rv in role_variants(role) if rv in [role]+role_variants(role)})
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

def detect(text,date):
    if session_meta(text) or is_header2(text):
        return (CONSEJO,'Consejo','ACTA/META',0)
    t=text[:500]
    cands=[]
    for pat,canon in ROLE_PATS:
        for m in re.finditer(r'(?<![A-Za-z0-9ÁÉÍÓÚÑáéíóúñ])'+re.escape(pat), t, re.I):
            after=t[m.end():m.end()+150]
            nm=re.match(r'\s*[-,;]?\s*(?:señor|señora|don|doña|sr\.|sra\.)?\s*([A-ZÁÉÍÓÚÑ][\wáéíóúñÁÉÍÓÚÑ]+(?:\s+[A-ZÁÉÍÓÚÑ][\wáéíóúñÁÉÍÓÚÑ]+){0,4})', after)
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
                before=t[max(0,m.start()-25):m.start()]
                bn=norm(before)
                if bn.endswith('del senor') or bn.endswith('al senor') or bn.endswith('del') or bn.endswith('al') or bn.endswith('comentario del senor') or bn.endswith('pregunta del senor'):
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
    has_trans=any(x in text[:140] for x in ['ofrece la palabra','da la palabra','concede la palabra','invita a','cede la palabra'])
    # candidatos "hablados": verbos, o role+nombre explicito reciente (aunque el verbo no este en la lista)
    strong=[c for c in cands if c.get('verb') or (c['method']=='ROL+NOMBRE' and c['pos']<650)]
    if has_trans:
        trans_idx=min([i for x in ['ofrece la palabra','da la palabra','concede la palabra','invita a','cede la palabra'] for i in [text[:140].find(x)] if i>=0] or [0])
        after_trans=[c for c in strong if c.get('role') and c['method']=='ROL+NOMBRE' and c['pos']>trans_idx]
        if after_trans:
            after_trans.sort(key=lambda c:(c['pos'],0 if c['actor'] not in PSEUDO else 1))
            c=after_trans[0]; return (c['actor'],c['role'],c['method'],c['pos'])
        best=[c for c in strong if c.get('role') and c['method']=='ROL+NOMBRE']
        if best:
            best.sort(key=lambda c:(c['pos'],0 if c['actor'] not in PSEUDO else 1))
            c=best[0]; return (c['actor'],c['role'],c['method'],c['pos'])
    if strong:
        # las menciones ("del Consejero señor X") no son hablantes; preferir candidatos no mencionados si existen
        no_mention=[c for c in strong if not (c.get('method')=='ROL+NOMBRE' and c.get('mention'))]
        if no_mention:
            strong=no_mention
        # role+nombre explicito al inicio es una señal muy fuerte (aunque el verbo no este en la lista)
        early_explicit=[c for c in strong if c['method']=='ROL+NOMBRE' and c['pos']<60]
        if early_explicit:
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
                # conservar el rol explicito del texto y solo corregir el hablante
                return (e['actor'],g['role'],g['method'],e['pos'])
        strong.sort(key=lambda c:(c['pos'],0 if c['method']=='ROL+NOMBRE' else 1 if c['verb'] else 2,0 if c['actor'] not in PSEUDO else 1))
        c=strong[0]; return (c['actor'],c['role'],c['method'],c['pos'])
    early=[c for c in cands if c['pos']<120 and c['role'] and c['method']=='ROL+NOMBRE']
    if early:
        early.sort(key=lambda c:c['pos'])
        c=early[0]; return (c['actor'],c['role'],c['method'],c['pos'])
    return None
    return None

def is_header2(t):
    return norm(t).lstrip().startswith(('acta correspondiente','a c t a'))

# canonical role for actor/date
actor_role_by_date=collections.defaultdict(collections.Counter)
for r in data:
    actor_role_by_date[(to_date_str(r[1]),str(r[2]).strip())][str(r[3]).strip()]+=1
def canonical_role(actor,date):
    cnt=actor_role_by_date.get((str(date),actor))
    if cnt: return cnt.most_common(1)[0][0]
    cnt=collections.Counter(str(r[3]).strip() for r in data if str(r[2]).strip()==actor)
    return cnt.most_common(1)[0][0] if cnt else None

KNOWN_MIN={'Nicolás Eyzaguirre Guzmán','Andrés Velasco Brañes','Felipe Larraín Bascuñán','Alberto Arenas de Mesa','Rodrigo Valdés Pulido','María Olivia Recart Herrera','Mario Marcel Cullell','María Eugenia Wagner Brizzi','Julio Dittborn Cordua'}
FULL_MIN_START={'Andrés Velasco Brañes':dt.date(2006,3,11),'Felipe Larraín Bascuñán':dt.date(2010,3,11),'Alberto Arenas de Mesa':dt.date(2014,3,11),'Rodrigo Valdés Pulido':dt.date(2015,3,19)}
ALWAYS_SUBRO={'María Olivia Recart Herrera','Mario Marcel Cullell','María Eugenia Wagner Brizzi'}
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

# ---- textos completos re-extraidos desde PDF (límite de celda Excel) ----
import json as _json
import os as _os
FULL_TEXTS={}
if _os.path.exists('textos_completos.jsonl'):
    try:
        with open('textos_completos.jsonl',encoding='utf-8') as _fh:
            for _line in _fh:
                _r=_json.loads(_line)
                FULL_TEXTS[int(_r['ID'])]=_r
    except Exception as _e:
        print('No se pudo leer textos_completos.jsonl:',_e)

# ---- process ----
records=[]; last_speaker={}; actor_corr=0; role_corr=0; method_counter=collections.Counter()
for r in data:
    rid=int(r[0]); date=to_date_str(r[1]); date_dt=dt.date.fromisoformat(date)
    actor_orig=str(r[2]).strip(); rol_orig=str(r[3]).strip(); text=str(r[5])
    det=detect(text,date)
    if det:
        spk,role,method,_=det
        if spk in REAL or spk==CONSEJO:
            if spk in REAL: last_speaker[date]=spk
        else:
            # pseudo actor fallback: try inherit / keep
            method='PSEUDO'
            spk=None; role=None
    else:
        method='SIN_DETECTAR'
        spk=None; role=None
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
    rol=rol_orig
    if method in ('ACTA/META','META') and spk==CONSEJO:
        rol='Consejo'
    # Política conservadora: Rol_Gold = Rol_Original (cargo del PDF/source).
    # Solo se corrigen casos indudables:
    #   - actas/metadata del Consejo -> rol Consejo
    #   - Rodrigo Valdés antes de 2015 cuando el acta lo presenta como Gerente
    #   - género/subrogante de Hacienda confirmado por el texto
    if spk=='Rodrigo Valdés Pulido' and date_dt<FULL_MIN_START['Rodrigo Valdés Pulido'] and role and role.startswith('Gerente'):
        rol=role
    elif spk in KNOWN_MIN and ('Hacienda' in rol or 'Subsecretario' in rol) and not (spk=='Rodrigo Valdés Pulido' and date_dt<FULL_MIN_START['Rodrigo Valdés Pulido']):
        rol=ministry_role(text,spk,date_dt)
    if rol!=rol_orig: role_corr+=1
    method_counter[method]+=1
    records.append((rid,date,date_dt,actor_orig,spk,rol,rol_orig,role,method,int(r[4]),text,str(r[6]),str(r[7])))

print("Actors reasignados:",actor_corr)
print("Roles cambiados:",role_corr)
print("Métodos:",dict(method_counter))

# taxonomy
def cat(kw):
    k=norm(kw)
    if any(x in k for x in ['acuerdo','comunicado','adopción unánime','levantamiento']): return 'acuerdo_comunicado'
    if any(x in k for x in ['votación','voto','fundamentación de voto','llamado a votación','pase votación','apertura votación']): return 'decision_tpm'
    if any(x in k for x in ['opciones','minuta de opciones']): return 'opciones_tpm'
    if any(x in k for x in ['inflación','expectativas inflación','ipcx','subyacente','presiones de precios']): return 'inflacion'
    if any(x in k for x in ['mercado laboral','empleo','desempleo','participación laboral','salario','estrechez']): return 'mercado_laboral'
    if any(x in k for x in ['liquidez','curva','tasas','tipo de cambio','bonos','spread','interbancario','mercado monetario','renta fija','fondeo','financiero']): return 'mercados_financieros'
    if any(x in k for x in ['internacional','estados unidos','europa','china','brasil','ee.uu','weo','fed','commodities','petróleo','cobre','molibdeno','materias primas','mundial','global']): return 'escenario_internacional'
    if any(x in k for x in ['fiscal','hacienda','gasto público','superávit fiscal','deuda soberana','subsidio','regla fiscal']): return 'politica_fiscal'
    if any(x in k for x in ['actividad interna','actividad económica','demanda','inversión','consumo','imacec','pib','producto potencial','brecha del producto','industria','gasto']): return 'actividad_interna'
    if any(x in k for x in ['riesgo','balance','incertidumbre']): return 'riesgos'
    if any(x in k for x in ['apertura','asistencia','calendario','presidencia','inicio de sesión','invitaciones','orden','suspensión','reanudación','cierre','se levanta']): return 'apertura_cierre'
    if any(x in k for x in ['discusión','debate','deliberación','comentarios','traspaso','preguntas','ronda']): return 'debate'
    return 'otros'

texts=[rec[10] for rec in records]
tc=collections.Counter(texts)
trunc=set(i for i,t in enumerate(texts) if len(t)>=32767)
nearcut=set(i for i,t in enumerate(texts) if 30000<=len(t)<32767)
dup=set(i for i,t in enumerate(texts) if tc[t]>1)
def formula(t):
    low=t.lower()
    return any(x in low for x in ['suspende','levanta la sesión','aprueba el texto','ofrece la palabra','agradece la presentación','agradece la exposición','se levanta la sesión','a continuación, concede'])
dup_formula=set(dup)  # todos los duplicados exactos son formulas de sesion repetidas (criterio usuario)

outwb=openpyxl.Workbook(); ows=outwb.active; ows.title='Consolidado'
header=['ID','Id_Sesion','Fecha','Actor_Original','Actor_Gold','Actor_Cambia','Rol_Original','Rol_Gold','Rol_Cambia','Rol_Texto','Metodo_Actor','Página','Texto','Tema_Original','Tema_Categoria','Palabra_Clave_Original','Palabra_Clave_Categoria','Texto_Truncado','Duplicado_Exacto','Duplicado_Formula','Nota']
ows.append(header)
for idx,rec in enumerate(records):
    rid,date,date_dt,actor_orig,spk,rol,rol_orig,role,method,page,text,tema,kw=rec
    clean=re.sub(r'[ \t]+',' ',text); clean=re.sub(r'\s*\n\s*','\n',clean)
    note=[]
    if idx in trunc: note.append('Texto truncado en celda Excel (32,767)')
    if idx in nearcut: note.append('Texto muy largo (>=30,000)')
    if idx in dup: note.append('Texto duplicado exacto'+(' (probable fórmula)' if idx in dup_formula else ''))
    if role: note.append('Rol detectado en texto: '+role)
    if method in ('HERENCIA','SIN_DETECTAR','ORIGINAL','PSEUDO'): note.append('Método: '+method)
    # estado de texto largo: completo en textos_completos.jsonl
    if rid in FULL_TEXTS:
        ft=FULL_TEXTS[rid]
        note.append(f'Texto completo ({ft.get("Longitud_Texto_Completo",len(str(ft.get("Texto_Completo",""))))} chars) en textos_completos.jsonl')
        tc='NO'
    else:
        tc='SI' if idx in trunc else 'REV' if idx in nearcut else 'NO'
    ows.append([rid,'RPM-'+date,date_dt,actor_orig,spk,'SI' if spk!=actor_orig else 'NO',
                rol_orig,rol,'SI' if rol!=rol_orig else 'NO',role if role else '',method,page,clean,
                tema,cat(tema),kw,cat(kw),
                tc,
                'SI' if idx in dup else 'NO','SI' if idx in dup_formula else 'NO','; '.join(note)])

md=outwb.create_sheet('Calidad'); md.append(['Indicador','Valor'])
md.append(['Filas',len(records)]); md.append(['Sesiones',len(set(x[1] for x in records))])
md.append(['Fecha min',min(x[1] for x in records)]); md.append(['Fecha max',max(x[1] for x in records)])
md.append(['Actores reasignados',actor_corr]); md.append(['Roles corregidos',role_corr])
md.append(['Textos truncados sin resolver',len([i for i in trunc if int(records[i][0]) not in FULL_TEXTS])])
md.append(['Textos largos sin revisar',len([i for i in nearcut if int(records[i][0]) not in FULL_TEXTS])])
md.append(['Textos con texto completo en JSONL',len(FULL_TEXTS)])
md.append(['Duplicados exactos',len(dup)]); md.append(['Duplicados fórmula',len(dup_formula)])
md.append(['Métodos',str(dict(method_counter))])

md2=outwb.create_sheet('Metodo_Actor'); md2.append(['Metodo','Registros'])
for k,v in method_counter.most_common(): md2.append([k,v])
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
                     'Ver texto completo en textos_completos.jsonl (el XLSX limita la celda a 32,767 chars)',
                     ft.get('Longitud_Excel',''),ft.get('Longitud_Texto_Completo',''),ft.get('Fuente',''),'textos_completos.jsonl'])

for row in ows.iter_rows(min_row=2,max_row=ows.max_row,min_col=3,max_col=3):
    for c in row:
        if isinstance(c.value,dt.date): c.number_format='YYYY-MM-DD'
for sheet in outwb.worksheets:
    for j,col in enumerate(sheet.iter_cols()):
        if not col: continue
        w=min(max(max((len(str(c.value)) for c in col[:300] if c.value is not None),default=8)+2,10),60)
        sheet.column_dimensions[col[0].column_letter].width=w
ows.freeze_panes='A2'
outwb.save(OUT); print("Saved",OUT)
