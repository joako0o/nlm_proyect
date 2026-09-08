"""Detección conservadora de sujetos de habla; nunca divide por una mera mención.

Trabaja sobre una vista normalizada sólo para reconocer al sujeto. Los cortes
se hacen sobre offsets del texto original, que se conserva sin reescrituras.
"""
import re


def normalize(text):
    t = re.sub(r'\s+', ' ', str(text).lower().translate(str.maketrans(
        'áéíóúñü', 'aeiounu'))).strip()
    for old,new in [('vicepres idente','vicepresidente'),('de gregario','de gregorio'),
                    ('claudia soto','claudio soto'),('macroeconom ico','macroeconomico'),('claud io soto','claudio soto')]:
        t = t.replace(old,new)
    # Variantes constatadas en el consolidado, sólo en la vista de reconocimiento.
    for pattern, replacement in [
        (r'\bgerente de analis is macroeconomico\b', 'gerente de analisis macroeconomico'),
        (r'^a l respecto\b', 'al respecto'),
        (r'\bgerente de division de estudios\b', 'gerente de division estudios'),
        (r'\btam bien\b', 'tambien'),
        (r'\bvittoho corbo\b', 'vittorio corbo'),
        (r'\bgerente de la division (?:de )?', 'gerente de division '),
        (r'\bmadgenzo\b', 'magendzo'),
        (r'\bgerente analisis macroeconomico\b', 'gerente de analisis macroeconomico'),
        (r'\bgerente de estudios\b(?!\s+de\b)', 'gerente de division estudios'),
        (r'\bgerente division politica financiera\b', 'gerente de division politica financiera'),
        (r'\b(presidente|ministro de hacienda) seno[s]? (?=[a-z])', r'\1 senor '),
        (r'\ba continua cion\b', 'a continuacion'),
        (r'^ai respecto\b', 'al respecto'),
        (r'\bmari\^an\b', 'marfan'), (r'\bdesorm eaux\b', 'desormeaux'),
        (r'\bluis osear herrera\b', 'luis oscar herrera'),
        (r'\bsergio lehman\b', 'sergio lehmann'),
        (r'\b(?:e1|ei) (?=presidente|vicepresidente|consejero|gerente|senor)', 'el '),
        (r'\ben lo que (?:se refiere|dice relacion) a[l]?\b', 'respecto a'),
        (r'\ben lo que dice relacion con\b', 'respecto a'),
    ]:
        t = re.sub(pattern, replacement, t)
    return t


# Verbos finitos / locuciones que vinculan directamente el sujeto a su discurso.
# No usar búsqueda en una ventana: podría capturar el verbo de otra persona.
VERBS = (
    'aprovecha de agradecer', 'hace una observacion', 'da inicio a la sesion',
    'esta en desacuerdo', 'visualiza', 'asigna una alta probabilidad',
    'llama a ser cuidadosos', 'deja planteada la pregunta',
    'admite', 'tiende a compartir', 'tiende a coincidir', 'suscribe plenamente', 'da la bienvenida',
    'proporciona un comentario', 'hace un comentario', 'efectua varias reflexiones',
    'da por finalizada la sesion', 'da por concluida la sesion',
    'pone termino a la sesion', 'abre la sesion',
    'da inicio a la reunion de politica monetaria',
    'hace enfasis', 'pone enfasis', 'hace la salvedad', 'clarifica', 'especifica',
    'colige', 'deduce', 'calcula', 'compara', 'disiente', 'no descarta', 'no advierte',
    'se compromete a informar', 'se compromete a actualizar', 'se compromete a analizar',
    'se compromete a presentar', 'se compromete a continuar monitoreando',
    'recomienda', 'reafirma', 'ratifica', 'hace alusion', 'exhibe',
    'quiere hacer un comentario', 'desea efectuar algunas observaciones', 'desea plantear',
    'da inicio a su presentacion', 'da inicio a su intervencion',
    'procede a responder', 'procede a dar respuesta',
    'se suma a lo expresado', 'se suma a lo planteado', 'se suma a lo senalado',
    'se suma al planteamiento', 'se suma a los planteamientos', 'se suma al comentario',
    'se suma a los comentarios', 'se suma a la preocupacion', 'se suma a todos los parabienes',
    'discrepa', 'adhiere', 'califica', 'acoge', 'atribuye',
    'da paso a la exposicion', 'alude', 'corrobora', 'resume', 'hace el alcance', 'llama la atencion',
    'se compromete a revisar', 'asiente', 'le parece', 'hace referencia', 'repara en', 'felicita', 'anade', 'consigna', 'hace mencion', 'comunica', 'efectua un comentario',
    'quiere hacer presente', 'quiere hacer una aclaracion', 'quiere plantear', 'quiere puntualizar',
    'desea manifestar', 'desea senalar', 'quisiera senalar', 'se manifiesta de acuerdo',
    'es de opinion', 'suspende', 'reanuda', 'compartio', 'declara', 'resalta', 'insiste', 'estima',
    'hace notar', 'hace presente', 'hace ver', 'da cuenta', 'da comienzo',
    'ofrece la palabra', 'concede la palabra', 'da la palabra', 'cede la palabra',
    'se refiere', 'se pregunta', 'se muestra', 'tiene la impresion',
    'retoma', 'comparte', 'concuerda', 'resalta', 'anticipa', 'advierte',
    'senala', 'senalo', 'indica', 'indico', 'manifiesta', 'manifesto',
    'expresa', 'expreso', 'dice', 'comenta', 'comento', 'interviene',
    'estima', 'consulta', 'consulto', 'afirma', 'responde', 'respondio',
    'agrega', 'agrego', 'precisa', 'preciso', 'plantea', 'planteo',
    'pregunta', 'pregunto', 'informa', 'informo', 'expone', 'menciona', 'continua',
    'prosigue', 'solicita', 'opina', 'acota', 'destaca', 'recuerda',
    'observa', 'concluye', 'inicia', 'apoya', 'coincide', 'agradece',
    'aclara', 'considera', 'fija', 'explica', 'explico', 'subraya',
    'recalca', 'piensa', 'cree', 'acepta', 'transmite', 'comienza',
    'sostiene', 'confirma', 'apunta', 'argumenta', 'reconoce', 'describe',
    'analiza', 'desarrolla', 'presenta', 'explicita', 'puntualiza',
    'formula', 'contesta', 'propone', 'sugiere', 'vota', 'reitera',
    'complementa', 'enfatiza', 'estima conveniente', 'deja constancia',
)
VERB = '(?:' + '|'.join(re.escape(v) for v in sorted(VERBS, key=len, reverse=True)) + r')\b'
DIRECT = re.compile(r'^\s*[,;]?\s*(?:(?:le|lo)\s+)?(?:(?:tambien|ademas|entonces|luego|por su parte|en tanto|si bien)\s*,?\s*)?' + VERB)
PARENTHETICAL = re.compile(r'^\s*,?\s*(?:acerca del?|a raiz del?|en razon del?|insistiendo sobre|ante comentarios de|haciendo referencia al?|continuando con su|continuando su|en referencia|aludiendo|en relacion|con respecto|respecto|sobre|en cuanto|por su parte|en respuesta|a proposito|refiriendose|complementando|contestando|frente|con motivo|para ilustrar|ante una consulta|respondiendo)\b[^.;:]{1,250}?(?=' + VERB + ')')
# Incisos constatados: locuciones completas y verbo principal aún exigido.
OPENING_ASIDE = re.compile(r'^\s*,?\s*(?:como siempre|junto con dar inicio a la reunion de politica monetaria n[°º]\s*\d{1,3}|tambien con respecto a demanda|atendido lo expuesto|haciendo un calculo preliminar|junto con agradecer las opiniones expuestas|en nombre suyo y del consejo|antes de retirarse de la reunion|pensado en los agricultores),\s*(?=' + VERB + ')')
INVERTED = re.compile(VERB + r'\s*$')
FINITE = re.compile(r'\b' + VERB)
HONOR = r'(?:senor|senora|don|dona|sr\.|sra\.)\s+'
# Cierres acotados: prefijo completo, hora válida opcional, sujeto/predicado aún exigidos.
CLOSURE_LEAD = (r'al no (?:haber (?:consultas o comentarios adicionales|mas comentarios)|'
                r'formularse (?:otros comentarios|comentarios adicionales))'
                r'(?:(?:,| y) siendo las? (?:[01]?\d|2[0-3])[:.][0-5]\d(?: horas)?)?$')
LEAD = re.compile(r'^(?:siendo las? (?:[01]?\d|2[0-3])[:.][0-5]\d horas$|al continuar con su presentacion$|prosiguiendo con su exposicion$|al proseguir con su presentacion$|no existiendo otras consultas o comentarios$|no habiendo mas consultas ni comentarios (?:en (?:lo|io) concerniente al|respecto del) escenario internacional$|' + CLOSURE_LEAD + r'|no habiendo comentarios$|dado eso$|al continuar(?:se)? con la votacion$|al concluir con la votacion$|al proseguir$|mientras que|el efecto debiera ser menor y al reves|planteamiento al cual|por su parte|al respecto|en relacion|con respecto|en cuanto|'
                  r'antes de proseguir|finalizada la presentacion|concluida la presentacion|no habiendo mas (?:comentarios|comentanos)|refiriendose ahora a|antes de continuar con la votacion|complementando los comentarios efectuados|prosiguiendo con la votacion|prosiguiendo con la presentacion|al continuar con (?:su|la) exposicion|una vez adoptado el acuerdo correspondiente|aun considerando la explicacion anterior|como es habitual|para sintetizar|al concluir su presentacion|a modo complementario|a lo cual|a lo que|a continuacion|sobre el particular|sobre este|en este|en ese|'
                  r'nuevamente|tambien|respondiendo|asimismo|a su vez|finalmente|luego|despues|por otra parte|'
                  r'por otro lado|en respuesta|ante |respecto |intervencion|'
                  r'exposicion|comentarios|opciones|sobre la|sobre el|'
                  r'en |sobre |respecto |ante |para concluir|para finalizar|a este respecto|a su analisis|por las razones expuestas|sin embargo|en consecuencia|por ello|con relacion|de inmediato|enseguida|en seguida|a lo anterior|a lo anteriormente|a proposito|en otra|en esta|en tal|en el mismo|adicionalmente|ademas|continuando|para enfatizar|por el lado|en consideracion)\b')
def has_finite(text):
    # Una referencia retrospectiva bloquea prestar el verbo al actor mencionado;
    # no basta por sí sola para abrir un turno actual (casos 1013 y 2325).
    if re.search(r'\bse refirio\b', text):
        return True
    # "la consulta del Ministro" es un sustantivo, no otro verbo de habla.
    for m in FINITE.finditer(text):
        if m.group() in ('consulta', 'pregunta') and re.search(r'\b(?:la|una|su|esta|esa|dicha)\s+$', text[:m.start()]):
            continue
        return True
    return False


MENTION_END = re.compile(r'\b(?:(?:del|al|de|por|para|segun|con|ante|a)|(?:del|al)\s+expositor)\s*$')


class TurnDetector:
    def __init__(self, aliases, roles, resolve_alias, resolve_role, role_for_actor):
        self.aliases = aliases
        self.resolve_alias = resolve_alias
        self.resolve_role = resolve_role
        self.role_for_actor = role_for_actor
        self.name = re.compile(r'(?:' + '|'.join(re.escape(a) for a in
                               sorted(aliases, key=lambda a: (-len(a), a))) + r')(?![a-z])')
        self.roles = {normalize(k): v for k, v in roles}
        self.role = re.compile(r'(?<![a-z])(?:' + '|'.join(re.escape(k) for k in
                               sorted(self.roles, key=lambda a: (-len(a), a))) + r')(?![a-z])')
        self.honor = re.compile(HONOR)

    def _subject_start(self, text, pos):
        m = re.search(r'\b(?:(?:el|la)\s+)?(?:senor|senora)?\s*$', text[:pos])
        return m.start() if m and m.group().strip() else pos

    def candidates(self, sentence, date, previous=None, context=None, allow_embedded=False):
        t = normalize(sentence)
        t = re.sub(r'^(?!(?:en|de|al|si|se|lo|la|el|un|no|ni|su)\b)(?:[a-z]{1,2}\)?[ \W]*)(?=el |la |al respecto|interviene )', '', t)
        t = re.sub(r'^el relacion\b', 'en relacion', t)
        subjects = []
        # Rol + nombre explícito, rol único por sesión, o anáfora local de cargo.
        for m in self.role.finditer(t):
            start = self._subject_start(t, m.start())
            end = m.end()
            tail = t[end:]
            gap = re.match(r'\s*[,;]?\s*(?:(?:subrogante|interino|\(s\))\s*)?(?:' + HONOR + r')?', tail)
            name_start = end + gap.end()
            nm = self.name.match(t, name_start)
            role = self.roles[m.group()]
            if nm:
                actor = self.resolve_alias(nm.group(), date)
                end = nm.end()
                method = 'SUJETO_ROL_NOMBRE'
            else:
                end = name_start
                anaphora = re.match(r'(?:mencionado|mencionada|referido|referida)\b\s*', t[end:])
                if anaphora:
                    end += anaphora.end()
                    actor = (context or {}).get('REFERENTE:'+role) or (context or {}).get(role) or self.resolve_role(date, role)
                    method = 'ANAFORA_LOCAL'
                elif role in ('Consejero', 'Consejera', 'Gerente de División') or m.group() == 'gerente':
                    actor = ((context or {}).get(role) or
                             (previous if previous and self._compatible(previous, role, date) else None))
                    method = 'ANAFORA_LOCAL'
                else:
                    actor = self.resolve_role(date, role)
                    method = 'SUJETO_ROL_SESION'
            subjects.append((start, end, actor, method, role))
        # Nombre con tratamiento, sin exigir un cargo ni un verbo del interlocutor.
        for h in self.honor.finditer(t):
            nm = self.name.match(t, h.end())
            if nm:
                actor = self.resolve_alias(nm.group(), date)
                if any(start <= h.start() and end >= nm.end() and who == actor for start,end,who,_,_ in subjects):
                    continue
                subjects.append((self._subject_start(t, h.start()), nm.end(), actor, 'SUJETO_NOMBRE', None))
        found = []
        for start, end, actor, method, role in subjects:
            if not actor:
                continue
            prefix = t[:start].strip(' ,;:')
            tail = t[end:]
            parenthetical = PARENTHETICAL.match(tail) or OPENING_ASIDE.match(tail)
            if (parenthetical and not has_finite(parenthetical.group())
                    and not re.search(r'\b(?:que|quien|donde|cuando|como)\s*$', parenthetical.group())):
                tail = tail[parenthetical.end():]
            direct = bool(DIRECT.match(tail))
            inv = INVERTED.search(prefix)
            lead = prefix[:inv.start()].strip(' ,;:') if inv else prefix
            # "comparte la apreciación del Consejero X" no convierte X en sujeto.
            reference = re.search(r'\b(?:al igual que|lo mismo que|segun|como|que ha entregado)\s*$', prefix)
            if inv:
                reference = reference or re.search(r'\b(?:como(?: bien)?(?: lo)?|lo que|a que|que)\s*$', prefix[:inv.start()].strip())
            if reference or MENTION_END.search(prefix) or (not direct and not inv):
                continue
            # Prefijos nominales/temáticos admisibles; nunca otra oración de habla.
            if not allow_embedded and lead and (not LEAD.match(lead) or has_finite(lead)):
                continue
            # No interpretar sujetos citados dentro de comillas como turnos nuevos.
            if (t[:start].count('"') % 2 or t[:start].count('«') > t[:start].count('»')
                    or t[:start].count('“') > t[:start].count('”')):
                continue
            found.append({'actor': actor, 'pos': start, 'end': end,
                          'method': method, 'role': role})
        # Prefiere el sujeto completo con cargo sobre su nombre interno.
        return sorted(found, key=lambda c: (c['pos'], -c['end'], c['actor']))

    def minute_author(self, text, date):
        """Autor de una minuta personal delimitada, no de una mera mención."""
        t = normalize(text)
        heading = re.match(r'^(?:[a-z]\)\s*)?minuta (?:del|de la)\s+', t)
        if not heading or not t.endswith(('”','»','"')):
            return None
        if len(re.findall(r'\bminuta (?:del|de la)\b',t)) != 1:
            return None
        role = self.role.match(t,heading.end())
        if not role:
            return None
        gap = re.match(r'\s*[,;]?\s*(?:' + HONOR + r')?',t[role.end():])
        name = self.name.match(t,role.end()+gap.end())
        opening = re.match(r'\s*:\s*([“«"])',t[name.end():]) if name else None
        if not opening:
            return None
        # La cita exterior debe terminar al final: no engullir diálogo posterior.
        # Admite comillas anidadas y el cierre OCR mixto observado en la minuta 198.
        body_start = name.end()+opening.end()
        stack = [opening.group(1)]
        for i in range(body_start,len(t)):
            ch = t[i]
            if ch in ('“','«'):
                stack.append(ch)
            elif ch in ('”','»'):
                if not stack or stack[-1] != {'”':'“','»':'«'}[ch]:
                    return None
                stack.pop()
            elif ch == '"':
                if stack and (stack[-1]=='"' or (i==len(t)-1 and len(stack)==1)):
                    stack.pop()
                else:
                    stack.append(ch)
            if not stack:
                return self.resolve_alias(name.group(),date) if i==len(t)-1 else None
        return None

    def referents(self, sentence, date):
        """Nombres asociados a cargos en la oración previa, sólo para 'mencionado'.

        Una mención no es un turno. Se usa únicamente cuando la oración siguiente
        identifica explícitamente al cargo mencionado como sujeto de un verbo.
        """
        from collections import defaultdict
        t = normalize(sentence)
        found = defaultdict(set)
        for m in self.role.finditer(t):
            gap = re.match(r'\s*[,;]?\s*(?:' + HONOR + r')?', t[m.end():])
            name = self.name.match(t, m.end()+gap.end())
            if not name:
                continue
            who = self.resolve_alias(name.group(),date)
            if not who:
                continue
            role = self.roles[m.group()]
            found[role].add(who)
            if role.startswith('Gerente'):
                found['Gerente'].add(who)
                if role.startswith('Gerente de División'):
                    found['Gerente de División'].add(who)
        return {'REFERENTE:'+role:next(iter(names)) for role,names in found.items() if len(names)==1}

    def handoff(self, sentence, date):
        t = normalize(sentence)
        m = re.search(r'(?:ofrece|concede|da|cede) la palabra (?:al|a la)\s+|solicita al\s+', t)
        if not m:
            return None
        target = t[m.end():]
        role = self.role.match(target)
        offset = role.end() if role else 0
        gap = re.match(r'\s*,?\s*(?:' + HONOR + r')?', target[offset:])
        name = self.name.match(target, offset + gap.end())
        if name:
            return self.resolve_alias(name.group(), date)
        if role:
            return self.resolve_role(date, self.roles[role.group()])
        return None

    def reviewed_relative_handoff(self, prefix, fragment, date, acknowledgement=False, statement=False, analysis_ack=False):
        """Valida una cesión contigua para una revisión, no detecta turnos sola.

        La relativa debe declarar el comienzo efectivo de la exposición. Los
        sujetos completos de cedente y destinatario se validan por separado;
        no basta encontrar una cesión o un nombre en una ventana de contexto.
        Las proyecciones sirven sólo para reconocer sujetos, nunca para exportar.
        """
        if sum((acknowledgement, statement, analysis_ack))>1:
            return None
        if acknowledgement:
            # Variante individual constatada: no habilitar relativas de agradecimiento
            # arbitrarias ni confundir al destinatario de unas gracias con su autor.
            if not re.fullmatch(r'quien agradece, en primer termino, el analisis del staff\.', normalize(fragment)):
                return None
            lead = 'al continuar con la votacion, '
            prefix = normalize(prefix)
            if not prefix.startswith(lead):
                return None
            prefix = prefix[len(lead):]
        elif analysis_ack:
            if not re.match(r'^quien agradece el analisis del staff y declara hacer suyo el listado de antecedentes\b', normalize(fragment)):
                return None
        elif statement:
            if not re.match(r'^quien hace presente que\b', normalize(fragment)):
                return None
        elif not re.match(r'^quien comienza su exposicion senalando que\b', normalize(fragment)):
            return None
        m = re.fullmatch(r'(.+?) (?:ofrece|concede|da|cede) la palabra (?:al|a la) (.+),',
                         normalize(prefix))
        if not m:
            return None
        candidates = []
        for subject in m.groups():
            projected = subject + ' comienza'
            candidate = self.speaker(projected, date)
            if (not candidate or candidate['pos'] != 0
                    or candidate['method'] not in {'SUJETO_ROL_NOMBRE', 'SUJETO_ROL_SESION', 'SUJETO_NOMBRE'}
                    or projected[:candidate['end']].strip() != subject):
                return None
            candidates.append(candidate)
        return candidates[1]

    def _compatible(self, actor, role, date):
        actual = self.role_for_actor(date, actor) or ''
        if role in ('Gerente','Gerente de División'):
            return actual.startswith(role)
        return actual == role

    def speaker(self, sentence, date, previous=None, context=None):
        c = self.candidates(sentence, date, previous, context)
        return c[0] if c else None
