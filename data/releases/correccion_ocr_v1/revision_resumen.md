# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1130**
- operaciones: **1642**
- filas marcadas para cotejo: **184**
- sha256 de la base: `d0b64842cd756df4c50d2960d9bbf01c4c45e5df28609d7b612c5d666593da75`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 446 |
| `ACENTO_INDEBIDO` | 348 |
| `PALABRA_PARTIDA` | 319 |
| `ACENTO_FALTANTE` | 182 |
| `PUNTUACION` | 106 |
| `SIMBOLO_SUELTO` | 78 |
| `FIRMA_TRUNCADA` | 55 |
| `RESIDUO_PAGINACION` | 27 |
| `PALABRA_ERRONEA` | 26 |
| `PALABRA_OMITIDA` | 22 |
| `ESPACIO_FALTANTE` | 14 |
| `SALTOS_DE_LINEA` | 10 |
| `ESPACIO_INDEBIDO` | 4 |
| `PALABRA_DUPLICADA` | 3 |
| `PALABRA_SOBRANTE` | 2 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2011-10-13:4397:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `ya que sigue en tomo a su meta`
   - después: `ya que sigue en torno a su meta`
   - por qué: Eme en lugar de ene. Medido en el consolidado: 'en tomo a' aparece 24 veces y 'en torno a' 1.678. Es una confusión sistemática de glifo, de la misma clase que 'ios' por 'los' (91 veces), que el criterio manda corregir.
2. **PALABRA_ERRONEA**
   - antes: `sería muy raro también justificar porqué no se baja la tasa hoy`
   - después: `sería muy raro también justificar por qué no se baja la tasa hoy`
   - por qué: 'Porqué' sustantivo exigiría artículo ('el porqué'); sin él la única lectura es el interrogativo 'por qué'. Medido: 'por qué' 90 veces y 'porqué' 13 en el corpus, así que no es un patrón sistemático del transcriptor sino un caso aislado, y la oración no admite otra lectura.

### `RPM-2005-04-07:202:2` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `os de aceleración de! primer semestre`
   - después: `os de aceleración del primer semestre`
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.
2. **LETRA_CONFUNDIDA**
   - antes: `io internacional de ios combustibles. M`
   - después: `io internacional de los combustibles. M`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.
3. **LETRA_CONFUNDIDA**
   - antes: `e iniciaría antes de! cuarto trimestr`
   - después: `e iniciaría antes del cuarto trimestr`
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2013-12-12:5911:1` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `En segundo término, índica que el precio d`
   - después: `En segundo término, indica que el precio d`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2007-04-12:1213:1` — Beltrán de Ramón Acevedo

1. **LETRA_CONFUNDIDA**
   - antes: `í\/1onetaria`
   - después: `Monetaria`
   - por qué: í\/1onetaria por Monetaria. La formula "Tasa de Política Monetaria" aparece 1.411 veces en el corpus, incluida esta misma fila en otras partes; aqui la M se leyo como "í\/1". No hay lectura alternativa.

### `RPM-2008-05-08:1815:2` — Sergio Lehmann Beresi

1. **PALABRA_PARTIDA**
   - antes: `da importante en el prec io del trigo , el `
   - después: `da importante en el precio del trigo , el `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 3328 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
2. **PALABRA_PARTIDA**
   - antes: ` la apreciación del dóla r. Informa tambié`
   - después: ` la apreciación del dólar. Informa tambié`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 933 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
3. **PALABRA_PARTIDA**
   - antes: ` respe cto `
   - después: ` respecto `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 5404 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2015-01-15:6587:1` — Pablo García Silva

1. **ACENTO_FALTANTE**
   - antes: ` restricción presupuestaria de los agentes `
   - después: ` restricción presupuestaría de los agentes `
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2013-02-14:5376:1` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2010-10-14:3488:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.
2. **LETRA_CONFUNDIDA**
   - antes: `entral delineada en ellPoM, manifestando q`
   - después: `entral delineada en el IPoM, manifestando q`
   - por qué: Sigla dañada por el glifo I/l. Medido en toda la salida: 26 apariciones de esta familia, y cada forma tiene su equivalente correcto ampliamente atestiguado en el corpus (el IPC 1.430, el IPoM 1.543, IPCX 649, IPCX1 469, el IPP 10). Se excluyeron de la pasada "ellPEC", "dellPEC" y "ellMCE" (fila 1719:4): aparecen junto a siglas que no se pueden corroborar en el corpus y no hay reconstruccion unica.

### `RPM-2014-08-14:6382:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `e desde el punto de vísta de los precios,`
   - después: `e desde el punto de vista de los precios,`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 501 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2009-07-09:2622:1` — Enrique Marshall Rivera

1. **ACENTO_FALTANTE**
   - antes: `la proyección de la economia, lo más probabl`
   - después: `la proyección de la economía, lo más probabl`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2007-10-11:1515:1` — Enrique Marshall Rivera

1. **LETRA_CONFUNDIDA**
   - antes: `financiamiento para ios bancos. Comenta`
   - después: `financiamiento para los bancos. Comenta`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2009-09-08:2712:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` JORGE DESORMEAUX JIMÉNEZ Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2015-01-15:6591:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2007-03-15:1160:1` — Beltrán de Ramón Acevedo

1. **PALABRA_PARTIDA**
   - antes: `ve aumento del IPC, IP C X y el IPCX1. M`
   - después: `ve aumento del IPC, IPC X y el IPCX1. M`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 1217 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2013-09-12:5760:1` — Sergio Lehmann Beresi

1. **PALABRA_OMITIDA**
   - antes: `un porcentaje muy bajo del mercado esperaba en el mes enero pasado`
   - después: `un porcentaje muy bajo del mercado esperaba en el mes de enero pasado`
   - por qué: Preposición omitida. La forma completa está dos veces en la misma fila: 'en el mes de agosto se estimaba' y 'a contar del mes de enero de 2014'.

### `RPM-2012-05-17:4794:1` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `la aplicación de planes de ajuste fiscal, tensíonando los mercados`
   - después: `la aplicación de planes de ajuste fiscal, tensionando los mercados`
   - por qué: Tilde en la sílaba equivocada: 'tensíonando' no es palabra. El gerundio de 'tensionar' es llano y no lleva tilde. La oración no admite otra lectura (sección 1 del criterio) y la forma correcta aparece 2 veces en el corpus.

### `RPM-2007-09-13:1420:1` — Esteban Jadresic Marinovic

1. **PALABRA_PARTIDA**
   - antes: `lo que le preocupa tiene que ver con un tem a de liquidez`
   - después: `lo que le preocupa tiene que ver con un tema de liquidez`
   - por qué: Espacio intrapalabra, artefacto del escaneo: la palabra está partida en dos. No es una reconstrucción, se reúne sin alterar una letra. Medido: 'tem a' aparece 1 vez en el corpus y 'tema' 1.258.
2. **PALABRA_PARTIDA**
   - antes: `No es lo que habitualm ente se utiliza`
   - después: `No es lo que habitualmente se utiliza`
   - por qué: Espacio intrapalabra, artefacto del escaneo: la palabra está partida en dos. No es una reconstrucción, se reúne sin alterar una letra. Medido: 'habitualm ente' aparece 1 vez y 'habitualmente' 84.

### `RPM-2015-08-13:6954:1` — Joaquín Vial Ruiz-Tagle

1. **PALABRA_PARTIDA**
   - antes: `materias que pudieron haber jugado un rol importante tam bién en el año 2008`
   - después: `materias que pudieron haber jugado un rol importante también en el año 2008`
   - por qué: Palabra partida por un espacio intrapalabra. Sección 1 ter: se reúne sin alterar una letra, así que no hay lectura alternativa que proteger y no se pide corroboración. Medido: 'también' aparece 4.809 veces en el corpus y 'tam bién' 9.

### `RPM-2015-01-15:6594:2` — Consejo del Banco Central de Chile

1. **ACENTO_INDEBIDO**
   - antes: ` Las condiciones de financiamíento local reflejan `
   - después: ` Las condiciones de financiamiento local reflejan `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 440 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2014-07-15:6308:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: ` señor Pablo García índica que desde el pu`
   - después: ` señor Pablo García indica que desde el pu`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2015-11-12:7148:4` — Mario Marcel Cullell

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2010-09-16:3390:2` — Rodrigo Cerda Norambuena

1. **ACENTO_FALTANTE**
   - antes: `la ejecución presupuestaria no ha sido tan `
   - después: `la ejecución presupuestaría no ha sido tan `
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2014-02-18:6009:4` — Miguel Ricaurte Bermúdez

1. **SIMBOLO_SUELTO**
   - antes: `registrado alzas mayores. V El señor`
   - después: `registrado alzas mayores. El señor`
   - por qué: Letra mayúscula suelta entre dos oraciones. Es ruido de escaneo: la oración anterior termina en punto y la siguiente empieza con mayúscula y sentido completo, así que la letra no pertenece a ninguna de las dos. Medido: 17 casos en 17 filas, con las letras V, H, L, U, A, M, Y, B. Se revisaron uno por uno; el único que NO es residuo es RPM-2007-01-11:1055:1 ("prolongado. A SU juicio"), donde la A abre la oración legítimamente y el defecto es "SU" en mayúscula, que se trata aparte.

### `RPM-2006-08-10:817:1` — Rodrigo Valdés Pulido

1. **ACENTO_FALTANTE**
   - antes: `miento de un dígito para el gasto,
seria marginalmente i`
   - después: `miento de un dígito para el gasto,
sería marginalmente i`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.

### `RPM-2013-03-14:5435:1` — Kevin Cowan Logan

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2008-02-07:1684:1` — José De Gregorio Rebeco

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2013-04-11:5515:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` RODRIGO VERGARA MONTES Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2007-11-13:1521:1` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `cart Herrera. Asisten también; Gerente General, `
   - después: `cart Herrera. Asisten también: Gerente General, `
   - por qué: Punto y coma por dos puntos. Medido: "Asisten también:" aparece 93 veces y "Asisten también;" 7. La formula introduce una lista, así que corresponde dos puntos.

### `RPM-2012-05-17:4825:1` — Claudio Soto Gamboa

1. **ACENTO_FALTANTE**
   - antes: `a parte extrapresupuestaria, cuya disminuci`
   - después: `a parte extrapresupuestaría, cuya disminuci`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2005-07-12:299:4` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: ` exportaciones. Sin em bargo, al ver las cif`
   - después: ` exportaciones. Sin embargo, al ver las cif`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 1376 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
