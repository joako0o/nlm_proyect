# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1779**
- operaciones: **3055**
- filas marcadas para cotejo: **234**
- sha256 de la base: `eebaa728dc1d7ce14315caebd0c7516ff324b5d4acaefcf40cec2bf6d855945d`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 732 |
| `ESPACIO_INDEBIDO` | 507 |
| `PALABRA_PARTIDA` | 491 |
| `ACENTO_INDEBIDO` | 387 |
| `PUNTUACION` | 268 |
| `SIMBOLO_SUELTO` | 242 |
| `ACENTO_FALTANTE` | 220 |
| `FIRMA_TRUNCADA` | 55 |
| `RESIDUO_PAGINACION` | 36 |
| `ESPACIO_FALTANTE` | 34 |
| `PALABRA_ERRONEA` | 32 |
| `PALABRA_OMITIDA` | 22 |
| `PALABRA_DUPLICADA` | 16 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2015-03-19:6661:1` — Rodrigo Vergara Montes

1. **ESPACIO_INDEBIDO**
   - antes: `de cambio— , destaca t`
   - después: `de cambio—, destaca t`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **LETRA_CONFUNDIDA**
   - antes: `Resen/a`
   - después: `Reserva`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene Reserva y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.

### `RPM-2011-08-18:4274:1` — Rodrigo Vergara Montes

1. **ESPACIO_INDEBIDO**
   - antes: `descartar— , la probab`
   - después: `descartar—, la probab`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2009-02-12:2357:1` — Sebastián Claro Edwards

1. **ESPACIO_INDEBIDO**
   - antes: `los bancos , lo cual p`
   - después: `los bancos, lo cual p`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **LETRA_CONFUNDIDA**
   - antes: `se/ection`
   - después: `selection`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene selection y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.

### `RPM-2005-03-10:171:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `m antener`
   - después: `mantener`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 1788 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2009-11-12:2778:3` — Claudio Soto Gamboa

1. **PUNTUACION**
   - antes: `..`
   - después: `.`
   - por qué: Punto duplicado. Medido en el corpus: «..» aparece 4 veces en el texto virgen; una ya está cubierta por otra operación registrada (2006-01-12:562:1) y quedan estas 3, siempre al cierre de una oración seguida de otra que empieza en mayúscula.

### `RPM-2006-06-15:708:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `l precio del cobre, índica que éste ha est`
   - después: `l precio del cobre, indica que éste ha est`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2012-10-18:5157:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2007-07-12:1335:4` — Igal Magendzo Weinberger

1. **SIMBOLO_SUELTO**
   - antes: `ocesamiento y otros que resultan mayores. fi`
   - después: `ocesamiento y otros que resultan mayores.`
   - por qué: Residuo "fi" al final de la fila, tras una oración que cierra completa en "mayores.". La fila ya viene con motivo FINAL_SIN_PUNTUACION. No es texto: no hay palabra española "fi" y la oración anterior no lo necesita.

### `RPM-2010-06-15:3131:2` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `e alguna manera, en ios mercados americ`
   - después: `e alguna manera, en los mercados americ`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2015-05-14:6764:1` — Joaquín Vial Ruiz-Tagle

1. **SIMBOLO_SUELTO**
   - antes: `variable. ' En`
   - después: `variable. En`
   - por qué: Idem que 6067:1: apóstrofo suelto entre dos oraciones completas, sin basura alrededor y sin cita que abrir (§29).

### `RPM-2009-06-16:2602:1` — Consejo del Banco Central de Chile

1. **ACENTO_FALTANTE**
   - antes: `l impacto del mayor estimulo monetario. En m`
   - después: `l impacto del mayor estímulo monetario. En m`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.
2. **PUNTUACION**
   - antes: `Comunicado 'En su`
   - después: `Comunicado “En su`
   - por qué: La comilla de apertura de la cita del Comunicado está dañada. Medido en el corpus sobre las 113 filas de Acuerdo que tienen sección Comunicado: el signo que sigue inmediatamente a la palabra «Comunicado» es la comilla doble de apertura en 102 filas, y sólo 4 traen otra cosa (2 comilla recta, 1 comilla simple izquierda, 2 comillas simples izquierdas). La posición es fija —inmediatamente después de «Comunicado»— y en los 4 casos hay un signo, no una ausencia, así que no hay duda de que ahí va la comilla: sólo está mal leída. Corrobora que sea apertura dañada y no otra cosa que estas filas tienen la comilla de cierre intacta y sin pareja.

### `RPM-2008-11-13:2145:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.

### `RPM-2010-04-15:3033:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarla`
   - después: `cambiaria`
   - por qué: cambiarla por cambiaria. Misma familia y mismo defecto. Medido: 8 apariciones (todas dentro de "cambiarlas"), todas adjetivas y revisadas una por una: "paridades cambiarlas" 4 veces, "implicancias cambiarlas" 2, "expectativas cambiarlas" 1, "coberturas cambiarlas" 1. "cambiarias" ya aparece 19 veces en el corpus.
2. **ACENTO_FALTANTE**
   - antes: `lica que si bien es bastante marginal, seria de alrededor de`
   - después: `lica que si bien es bastante marginal, sería de alrededor de`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.

### `RPM-2008-04-10:1773:1` — José De Gregorio Rebeco

1. **PUNTUACION**
   - antes: `12;30 horas`
   - después: `12:30 horas`
   - por qué: Punto y coma donde va dos puntos en una hora. La forma «N:NN horas» aparece 544 veces en el corpus y «N;NN horas» 5, todas ellas este mismo dano.

### `RPM-2007-02-08:1090:4` — Rodrigo Valdés Pulido

1. **LETRA_CONFUNDIDA**
   - antes: `IRC`
   - después: `IPC`
   - por qué: IRC por IPC. Medido en todo el corpus: 71 apariciones, ninguna en un contexto donde IRC sea una sigla legitima; 61 sueltas y 10 dentro de IRCX1, que tambien debe leerse IPCX1 porque la misma fila escribe IPCX e IPCX2. Regla de bloque revisada caso por caso.
2. **ESPACIO_INDEBIDO**
   - antes: `monetaria— , continúa `
   - después: `monetaria—, continúa `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2011-01-13:3712:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.
2. **LETRA_CONFUNDIDA**
   - antes: `cambiarla`
   - después: `cambiaria`
   - por qué: cambiarla por cambiaria. Misma familia y mismo defecto. Medido: 8 apariciones (todas dentro de "cambiarlas"), todas adjetivas y revisadas una por una: "paridades cambiarlas" 4 veces, "implicancias cambiarlas" 2, "expectativas cambiarlas" 1, "coberturas cambiarlas" 1. "cambiarias" ya aparece 19 veces en el corpus.
3. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2014-06-12:6236:1` — Consejo del Banco Central de Chile

1. **ESPACIO_INDEBIDO**
   - antes: `ña Poblete ; Gerente d`
   - después: `ña Poblete; Gerente d`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2008-06-10:1853:2` — Sergio Lehmann Beresi

1. **ACENTO_FALTANTE**
   - antes: `l señor Gerente que en linea con lo anterior, la`
   - después: `l señor Gerente que en línea con lo anterior, la`
   - por qué: Tilde faltante, grupo B3. Se leyeron las 53 apariciones de linea, continua, publica y lineas, y sólo 23 son defecto. «linea»: las 18 son la fórmula «en linea con», siempre el sustantivo, así que van con contexto. «lineas»: las 4 son sustantivo («otras lineas de financiamiento», «algunas lineas manufactureras», «de las lineas vinculadas»). «continua»: de 18 apariciones sólo 2 son el verbo («la actividad económica continua creciendo», «esta parte de la economía continua funcionando»); las otras 16 son el adjetivo continuo/continua y NO se tocan («la continua caída», «la mejora continua», «la convergencia continua y gradual», «la serie no es continua», «de continua colaboración», «de manera continua»). «publica»: las 13 son la tercera persona del verbo publicar («se publica anualmente», «la Reserva Federal no publica su propia», «el INE no los publica», «que publica el Fondo») y ninguna se corrige.

### `RPM-2014-04-17:6117:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `ó un acuerdo sobre e! Mecanismo Único`
   - después: `ó un acuerdo sobre el Mecanismo Único`
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2010-06-15:3134:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.

### `RPM-2006-05-11:671:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `IPOM`
   - después: `IPoM`
   - por qué: Sigla mal compuesta. Medido en el corpus: «IPoM» aparece 2473 veces y «IPOM» 58, siempre el mismo documento, el Informe de Política Monetaria del Banco Central de Chile, cuya sigla lleva la o minúscula. El OCR leyó la o minúscula como O mayúscula.

### `RPM-2009-10-13:2730:1` — Pablo García Silva

1. **PUNTUACION**
   - antes: `No habiendo más comentarios,.`
   - después: `No habiendo más comentarios,`
   - por qué: Coma seguida de punto al final de la fila. Medido en el corpus: «<palabra>,.» aparece 98 veces en el texto virgen; el pase transversal del §45 corrigió 78 (76 «A continuación,.» más «década,.» y «Euro,.») y dejó estas 20, que son la misma familia con otras palabras: «Continuando con la votación,.» (6), «Para concluir con la votación,.» (3), «No habiendo más comentarios,.» (8), «No habiendo más comentarios y preguntas,.» (2) y «…señor Manuel Marfán,.» (1). En los 20 casos la fila siguiente empieza con «el Presidente…», «el Consejero…» o «el Vicepresidente…», de modo que la coma es la marca correcta y el punto es el signo sobrante. Se aplica el mismo criterio del §45.

### `RPM-2009-03-12:2437:1` — Jorge Desormeaux Jiménez

1. **ACENTO_FALTANTE**
   - antes: `, y que en adelante cabria esperar movimie`
   - después: `, y que en adelante cabría esperar movimie`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2006-12-14:1003:6` — Igal Magendzo Weinberger

1. **LETRA_CONFUNDIDA**
   - antes: `ria de inversión, el Gerente señor ígal Madgenzo, señaló que las importaciones de bienes`
   - después: `ria de inversión, el Gerente señor Igal Magendzo, señaló que las importaciones de bienes`
   - por qué: Normalización de nombre propio dañado, autorizada por el usuario en esta ronda (el criterio anterior era marcar sin corregir). La forma canónica la acreditan el corpus y el roster de la sesión: «Magendzo» aparece 416 veces en la salida, contra 18 de la forma dañada. Se corrige en Texto_Corregido; Texto queda intacto. Lo que no tiene forma canónica atestiguada (por ejemplo «Miguel Angel Nacrur Gazali») sigue marcado NOMBRE_PROPIO_POR_COTEJAR. Extensión del §57: el mismo tramo llevaba también el nombre de pila dañado, «ígal» con í minúscula acentuada en vez de «Igal». Medido en el corpus: «Igal» aparece 131 veces y «ígal» 1, siempre el mismo Gerente de Análisis Macroeconómico, Igal Magendzo Weinberger.

### `RPM-2011-06-14:4106:1` — Luis Óscar Herrera Barriga

1. **ACENTO_INDEBIDO**
   - antes: `y disponibilidad de financíamiento internacional. `
   - después: `y disponibilidad de financiamiento internacional. `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 440 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
2. **ACENTO_INDEBIDO**
   - antes: `. En este contexto, índica que el balance `
   - después: `. En este contexto, indica que el balance `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2010-08-12:3331:1` — Pablo García Silva

1. **ACENTO_FALTANTE**
   - antes: `s de forma aislada. podrian sugerir un incr`
   - después: `s de forma aislada, podrían sugerir un incr`
   - por qué: El punto en vez de coma quedó dentro del tramo de una operación ya registrada, que arreglaba otro defecto del mismo tramo (un acento, un espacio o una basura de OCR) y no tocaba el signo. Se enmienda el Despues en vez de apilar una segunda operación: dos tramos solapados sobre el mismo texto virgen no se pueden aplicar en ningún orden. La oración continúa en minúscula, de modo que el punto no puede ser de cierre y la marca correcta es la coma.
2. **ACENTO_FALTANTE**
   - antes: `la ejecución presupuestaria ha sido compara`
   - después: `la ejecución presupuestaría ha sido compara`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2012-09-13:5043:1` — Sergio Lehmann Beresi

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2015-01-15:6586:2` — Alberto Arenas de Mesa

1. **PUNTUACION**
   - antes: `"otros vehículos de transporte"`
   - después: `“otros vehículos de transporte”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.

### `RPM-2010-06-15:3143:1` — José De Gregorio Rebeco

1. **PUNTUACION**
   - antes: `rothers.,`
   - después: `rothers,`
   - por qué: Punto antes de una coma. Medido en el corpus: «.,» aparece 24 veces en el texto corregido, pero 20 son legítimas (abreviaturas «EE.UU.», «S.A.», «etc.», «v.gr.» e iniciales de nombre como «Velasco B.,»). Las 4 restantes tienen antes una palabra completa en minúscula o un signo de porcentaje, no una abreviatura, y el punto es sobrante.
2. **LETRA_CONFUNDIDA**
   - antes: `Beam Stearns`
   - después: `Bear Stearns`
   - por qué: Nombre dañado por OCR: «Beam Stearns» por «Bear Stearns», el banco de inversión cuya quiebra en septiembre de 2008 abre la crisis financiera. Confusión de la erre por la eme, clásica en OCR. Medido en el corpus: «Beam Stearns» aparece 5 veces y «Bear Stearns» 1, de modo que la forma correcta está atestiguada por el propio corpus aunque sea minoritaria; los cinco contextos son inequívocos («cuando alrededor de julio del año 2008», «en el momento en que quebró», «la crisis de»). Se corrige y se deja constancia aquí de que es el primer caso en que la forma canónica es minoritaria: la decisión no descansa en la frecuencia sino en que la entidad es única y el corpus la atestigua.

### `RPM-2010-03-18:3019:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `Para concluir con la votación,.`
   - después: `Para concluir con la votación,`
   - por qué: Coma seguida de punto al final de la fila. Medido en el corpus: «<palabra>,.» aparece 98 veces en el texto virgen; el pase transversal del §45 corrigió 78 (76 «A continuación,.» más «década,.» y «Euro,.») y dejó estas 20, que son la misma familia con otras palabras: «Continuando con la votación,.» (6), «Para concluir con la votación,.» (3), «No habiendo más comentarios,.» (8), «No habiendo más comentarios y preguntas,.» (2) y «…señor Manuel Marfán,.» (1). En los 20 casos la fila siguiente empieza con «el Presidente…», «el Consejero…» o «el Vicepresidente…», de modo que la coma es la marca correcta y el punto es el signo sobrante. Se aplica el mismo criterio del §45.
2. **PUNTUACION**
   - antes: `iste.`
   - después: `iste,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.
