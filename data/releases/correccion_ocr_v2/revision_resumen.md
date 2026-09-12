# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1579**
- operaciones: **2626**
- filas marcadas para cotejo: **214**
- sha256 de la base: `32752bd52ce5d3b50b0732780154aaef23482908f6671f92a327509e75edf452`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 542 |
| `ESPACIO_INDEBIDO` | 511 |
| `PALABRA_PARTIDA` | 490 |
| `ACENTO_INDEBIDO` | 374 |
| `SIMBOLO_SUELTO` | 194 |
| `ACENTO_FALTANTE` | 183 |
| `PUNTUACION` | 154 |
| `FIRMA_TRUNCADA` | 55 |
| `RESIDUO_PAGINACION` | 30 |
| `PALABRA_ERRONEA` | 28 |
| `ESPACIO_FALTANTE` | 27 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |
| `PALABRA_DUPLICADA` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2013-04-11:5496:1` — Luis Opazo Roco

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2009-06-16:2602:1` — Consejo del Banco Central de Chile

1. **ACENTO_FALTANTE**
   - antes: `l impacto del mayor estimulo monetario. En m`
   - después: `l impacto del mayor estímulo monetario. En m`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.
2. **PUNTUACION**
   - antes: `Comunicado 'En su`
   - después: `Comunicado “En su`
   - por qué: La comilla de apertura de la cita del Comunicado está dañada. Medido en el corpus sobre las 113 filas de Acuerdo que tienen sección Comunicado: el signo que sigue inmediatamente a la palabra «Comunicado» es la comilla doble de apertura en 102 filas, y sólo 4 traen otra cosa (2 comilla recta, 1 comilla simple izquierda, 2 comillas simples izquierdas). La posición es fija —inmediatamente después de «Comunicado»— y en los 4 casos hay un signo, no una ausencia, así que no hay duda de que ahí va la comilla: sólo está mal leída. Corrobora que sea apertura dañada y no otra cosa que estas filas tienen la comilla de cierre intacta y sin pareja.

### `RPM-2005-03-10:184:1` — Nicolás Eyzaguirre Guzmán

1. **PALABRA_PARTIDA**
   - antes: `m uchas`
   - después: `muchas`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 116 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2010-07-15:3231:1` — Kevin Cowan Logan

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.

### `RPM-2006-10-12:904:1` — Manuel Marfán Lewis

1. **SALTOS_DE_LINEA**
   - antes: `El
Consejero
señor
Marfán,
sobre
el
mismo
tema,
señala
que
la
Superintendencia`
   - después: `El Consejero señor Marfán, sobre el mismo tema, señala que la Superintendencia`
   - por qué: Artefacto de justificacion del PDF: una palabra por linea durante doce palabras. El resto de la fila y de la sesion corta en el ancho normal. Se reune el texto sin alterar una sola letra.

### `RPM-2014-04-17:6132:3` — Rodrigo Vergara Montes

1. **ACENTO_INDEBIDO**
   - antes: `Gerente de Análisis Macroeconómíco señor Miguel Fu`
   - después: `Gerente de Análisis Macroeconómico señor Miguel Fu`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 1000 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2007-09-13:1450:2` — José De Gregorio Rebeco

1. **PALABRA_PARTIDA**
   - antes: `se consideró el d ía 17 como laboral para el efecto calendario`
   - después: `se consideró el día 17 como laboral para el efecto calendario`
   - por qué: Espacio intrapalabra, artefacto del escaneo: la palabra está partida en dos. No es una reconstrucción, se reúne sin alterar una letra. Medido: 'd ía' aparece 1 vez y 'el día 17' 8, una de ellas en esta misma sesión.

### `RPM-2011-04-12:3968:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2010-01-14:2850:2` — Enrique Marshall Rivera

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2009-02-12:2362:1` — Pablo García Silva

1. **ESPACIO_INDEBIDO**
   - antes: `flación. r . Agrega el`
   - después: `flación. r. Agrega el`
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

### `RPM-2008-07-10:1965:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: ` las discusiones de ios IPoM, van en la`
   - después: ` las discusiones de los IPoM, van en la`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2007-05-10:1232:1` — Igal Magendzo Weinberger

1. **LETRA_CONFUNDIDA**
   - antes: `perecióles`
   - después: `perecibles`
   - por qué: perecióles por perecibles. Defecto sistematico descubierto en la ronda 185 y medido en todo el corpus: 10 apariciones en 9 filas, todas con el mismo dano (la b leida como o con tilde). "perecióles" no es palabra del espanol; "perecibles" aparece 166 veces en 123 filas. Los 10 contextos se revisaron uno por uno y todos son "alimentos perecibles", "bienes perecibles", "los perecibles" o "tanto perecibles como no perecibles". Precision 100%, sin falsos positivos posibles.
2. **LETRA_CONFUNDIDA**
   - antes: `Tasa de Política monetaria, dentro`
   - después: `Tasa de Política Monetaria, dentro`
   - por qué: Mayúscula faltante en un nombre propio. Medido en el texto virgen del corpus: «Tasa de Política Monetaria» aparece 1.441 veces y «Tasa de Política monetaria» 3; «Informe de Política Monetaria» 397 veces y «Informe de Política monetaria» 1. Son nombres propios —de la tasa (TPM) y del documento (IPoM)—, no sintagmas comunes. Se deja en cambio «Política monetaria» en 2009-05-07:2525:1, que es un rótulo de lista del Ministro y no el nombre de la TPM, y la «política monetaria» en minúscula de uso común, que es correcta.

### `RPM-2012-09-13:5093:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` MANUEL MARFÁN LEWIS RODRIGO VERGARA MONTES Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2015-10-15:7065:1` — Diego Gianelli Gómez

1. **LETRA_CONFUNDIDA**
   - antes: `1O`
   - después: `10`
   - por qué: 1O por 10: el cero se leyo como la letra O mayuscula. Medido: 7 apariciones en 6 filas y todas son numeros donde solo cabe el diez ("tasas a 1O años plazo", "lámina Nº 1O", "US$ 3,1O la libra", "a 5 y 1O años", "a 2 y 1O años", "a 1O años", "de 1O o 20%"). Se verifico que no existen apariciones embebidas en otras palabras.

### `RPM-2008-09-04:2054:1` — Sergio Lehmann Beresi

1. **ESPACIO_FALTANTE**
   - antes: `yeso`
   - después: `y eso`
   - por qué: yeso por "y eso". Medido: 13 apariciones, en todas falta el espacio entre la conjuncion y el demostrativo ("alto yeso tiene que tener" = "alto, y eso tiene que tener"). Verificado que ninguna esta embebida en otra palabra. La coma no se inserta: la oracion queda gramatical sin ella y anadirla seria editar puntuacion.
2. **PALABRA_PARTIDA**
   - antes: ` debie ra `
   - después: ` debiera `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 488 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2015-08-13:6959:1` — Sebastián Claro Edwards

1. **PALABRA_OMITIDA**
   - antes: `Expresa que frente la decisión de hacer explícita o no la preocupación sobre el riesgo de desanclaje`
   - después: `Expresa que frente a la decisión de hacer explícita o no la preocupación sobre el riesgo de desanclaje`
   - por qué: Falta la preposición: 'frente la decisión' no es gramatical y la reparación es única, porque el OCR omite y no agrega palabras. 'frente a la' aparece 110 veces en el corpus. Mismo criterio que 'la mayoría las monedas' (ronda 178) y 'la proyección el PIB' (ronda 179): preposición faltante, cadena agramatical, reparación única.

### `RPM-2011-05-12:3973:1` — Sergio Lehmann Beresi

1. **ESPACIO_INDEBIDO**
   - antes: `te último— , y que más`
   - después: `te último—, y que más`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2006-09-07:841:1` — Esteban Jadresic Marinovic

1. **LETRA_CONFUNDIDA**
   - antes: `o sería el precio de! petróleo que
ha`
   - después: `o sería el precio del petróleo que
ha`
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2010-05-13:3124:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `e de las noticias de! Ministro respec`
   - después: `e de las noticias del Ministro respec`
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2009-08-13:2681:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.
2. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
3. **ACENTO_INDEBIDO**
   - antes: `medidas complementarías posibles`
   - después: `medidas complementarias posibles`
   - por qué: El adjetivo «complementarias» no lleva tilde; la forma esdrújula «complementarías» sería la segunda persona del condicional, que no cabe después de «medidas» y antes de «posibles». Medido: «complementarías» aparece 1 sola vez en todo el corpus y «complementarias» 47. En la misma fila, además, el sustantivo del que deriva se usa bien.

### `RPM-2007-03-15:1121:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `ne la impresión que ios impactos que pu`
   - después: `ne la impresión que los impactos que pu`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2013-02-14:5384:1` — Luis Óscar Herrera Barriga

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2011-11-15:4459:1` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2014-02-18:6055:3` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2011-05-12:3984:3` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2010-12-16:3642:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` JOSE DE GREGORIO REBECO Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2014-08-14:6362:1` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: ` materia de empleo, índica que la tasa de `
   - después: ` materia de empleo, indica que la tasa de `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2013-07-11:5671:1` — Claudio Soto Gamboa

1. **ACENTO_INDEBIDO**
   - antes: ` mercado se inclina mayoritaríamente a que se m`
   - después: ` mercado se inclina mayoritariamente a que se m`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 195 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2012-04-17:4771:2` — Claudio Soto Gamboa

1. **RESIDUO_PAGINACION**
   - antes: ` Sesión N° 184 Página 14 de 26`
   - después: ``
   - por qué: Residuo de paginacion del PDF incrustado en medio de la oracion. Medido: 26 apariciones, 24 con la cabecera "Sesion N° N" delante y 2 como pie de pagina del Comunicado ("Pagina 31 de 31"). "Sesion N° N" aparece 25 veces en el corpus y solo 24 van seguidas de Pagina, de modo que el patron exige ambos y no toca ninguna mencion legitima. Se elimina el residuo y se deja un solo espacio donde la oracion continua.
