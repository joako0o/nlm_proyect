# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1368**
- operaciones: **2201**
- filas marcadas para cotejo: **194**
- sha256 de la base: `d0b64842cd756df4c50d2960d9bbf01c4c45e5df28609d7b612c5d666593da75`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `ESPACIO_INDEBIDO` | 515 |
| `LETRA_CONFUNDIDA` | 474 |
| `ACENTO_INDEBIDO` | 348 |
| `PALABRA_PARTIDA` | 320 |
| `ACENTO_FALTANTE` | 182 |
| `PUNTUACION` | 106 |
| `SIMBOLO_SUELTO` | 85 |
| `FIRMA_TRUNCADA` | 55 |
| `PALABRA_ERRONEA` | 28 |
| `RESIDUO_PAGINACION` | 27 |
| `ESPACIO_FALTANTE` | 24 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_DUPLICADA` | 3 |
| `PALABRA_SOBRANTE` | 2 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2014-11-18:6515:1` — Enrique Marshall Rivera

1. **LETRA_CONFUNDIDA**
   - antes: `opin1on`
   - después: `opinión`
   - por qué: opin1on por opinión: la i se leyo como el digito 1 y falta la tilde. Formula "en su opinión", 1.867 apariciones.

### `RPM-2010-04-15:3070:1` — Pablo García Silva

1. **PALABRA_PARTIDA**
   - antes: `ativas un escenario macroeconóm ico de mediano plaz`
   - después: `ativas un escenario macroeconómico de mediano plaz`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 196 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2005-03-10:192:1` — Jorge Desormeaux Jiménez

1. **PALABRA_PARTIDA**
   - antes: `esperan que la tasa norteam ericana se encuentre a `
   - después: `esperan que la tasa norteamericana se encuentre a `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 80 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
2. **PALABRA_PARTIDA**
   - antes: ` el Consejero señor Desorm eaux, señalando que `
   - después: ` el Consejero señor Desormeaux, señalando que `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 444 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA. Es un nombre propio, pero no se está adivinando nada: la forma correcta está atestiguada en el corpus y lo único que se elimina es un espacio que el escaneo insertó dentro de la palabra. No es resolución de alias, que es lo que el criterio prohíbe.
3. **PALABRA_PARTIDA**
   - antes: `e claro, pese a las incertidum bres, que las brecha`
   - después: `e claro, pese a las incertidumbres, que las brecha`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 78 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
4. **PALABRA_PARTIDA**
   - antes: `ijo tiene un efecto relativam ente reducido sobre `
   - después: `ijo tiene un efecto relativamente reducido sobre `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 771 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2011-10-13:4382:1` — Sebastián Claro Edwards

1. **ESPACIO_INDEBIDO**
   - antes: `BCP y BCU— , porque ha`
   - después: `BCP y BCU—, porque ha`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2007-03-15:1104:1` — Consejo del Banco Central de Chile

1. **PALABRA_PARTIDA**
   - antes: ` horas, se reúne el C onsejo del Banco Centr`
   - después: ` horas, se reúne el Consejo del Banco Centr`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 1433 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2015-11-12:7137:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `1O`
   - después: `10`
   - por qué: 1O por 10: el cero se leyo como la letra O mayuscula. Medido: 7 apariciones en 6 filas y todas son numeros donde solo cabe el diez ("tasas a 1O años plazo", "lámina Nº 1O", "US$ 3,1O la libra", "a 5 y 1O años", "a 2 y 1O años", "a 1O años", "de 1O o 20%"). Se verifico que no existen apariciones embebidas en otras palabras.

### `RPM-2008-02-07:1682:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **SALTOS_DE_LINEA**
   - antes: `ancieras de la crisis subpri me ya están deterior`
   - después: `ancieras de la crisis subprime ya están deterior`
   - por qué: Palabra partida por la justificación del PDF ("subpri me" por "subprime"). Medido: 4 apariciones en 4 filas en toda la base; una (1317:1) se corrigió con la ronda 191 y estas son las otras tres. La palabra es inequívoca y está atestiguada: "subprime" aparece 58 veces en el corpus. Es el mismo artefacto que "inmobiliari o" y que las 35 palabras en letras sueltas de §12.

### `RPM-2013-03-14:5402:1` — Sergio Lehmann Beresi

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.
2. **ACENTO_FALTANTE**
   - antes: `ar políticas presupuestarias expansivas y e`
   - después: `ar políticas presupuestarías expansivas y e`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2010-12-16:3641:1` — Consejo del Banco Central de Chile

1. **LETRA_CONFUNDIDA**
   - antes: `mías emergentes. En ios mercados financ`
   - después: `mías emergentes. En los mercados financ`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2009-09-08:2701:5` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2012-12-13:5233:1` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **ACENTO_INDEBIDO**
   - antes: `iaron el proceso de desapalancamíento antes de la cri`
   - después: `iaron el proceso de desapalancamiento antes de la cri`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 25 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
3. **ACENTO_INDEBIDO**
   - antes: `ncian un proceso de desapalancamíento que está en des`
   - después: `ncian un proceso de desapalancamiento que está en des`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 26 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2009-01-08:2286:1` — José De Gregorio Rebeco

1. **PALABRA_PARTIDA**
   - antes: ` caso, porque no se cons idera esto inmediatam`
   - después: ` caso, porque no se considera esto inmediatam`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 876 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2007-09-13:1429:1` — Jorge Desormeaux Jiménez

1. **PALABRA_PARTIDA**
   - antes: `de manera que sim plem ente quiere llamar la atención`
   - después: `de manera que simplemente quiere llamar la atención`
   - por qué: Espacio intrapalabra, artefacto del escaneo: la palabra está partida en dos. No es una reconstrucción, se reúne sin alterar una letra. Segunda ocurrencia de este artefacto en la sesión.

### `RPM-2014-04-17:6123:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `tubre o noviembre de! presente año, y`
   - después: `tubre o noviembre del presente año, y`
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2009-02-12:2362:1` — Pablo García Silva

1. **ESPACIO_INDEBIDO**
   - antes: `flación. r . Agrega el`
   - después: `flación. r. Agrega el`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2013-03-14:5405:1` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `icano, que registró ínicialmente una depreciació`
   - después: `icano, que registró inicialmente una depreciació`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 50 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2007-02-08:1068:1` — Jorge Desormeaux Jiménez

1. **LETRA_CONFUNDIDA**
   - antes: ` proyecciones del Consesus Forecast o JP Mor`
   - después: ` proyecciones del Consensus Forecast o JP Mor`
   - por qué: Consesus por Consensus: falta una n. Medido: "Consensus" aparece 127 veces en 99 filas y "Consesus" 8 veces en 6, siempre en el nombre propio "Consensus Forecast". No hay lectura alternativa.
2. **LETRA_CONFUNDIDA**
   - antes: `n de depreciación de! yuan en un 10% `
   - después: `n de depreciación del yuan en un 10% `
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2011-07-14:4205:1` — Rodrigo Vergara Montes

1. **ESPACIO_INDEBIDO**
   - antes: `entemente— , porque ha`
   - después: `entemente—, porque ha`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2010-07-15:3242:1` — Pablo García Silva

1. **ESPACIO_INDEBIDO**
   - antes: `ributarios .`
   - después: `ributarios.`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2007-08-09:1361:2` — Sergio Lehmann Beresi

1. **PALABRA_PARTIDA**
   - antes: `n Estados Unidos de Am érica, por tanto no e`
   - después: `n Estados Unidos de América, por tanto no e`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2587 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA. Es un nombre propio, pero no se está adivinando nada: la forma correcta está atestiguada en el corpus y lo único que se elimina es un espacio que el escaneo insertó dentro de la palabra. No es resolución de alias, que es lo que el criterio prohíbe.

### `RPM-2014-08-14:6389:4` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2013-09-12:5773:1` — Joaquín Vial Ruiz-Tagle

1. **ACENTO_INDEBIDO**
   - antes: `el contraste entre las políticas monetarias y cambiarías de los países emergentes`
   - después: `el contraste entre las políticas monetarias y cambiarias de los países emergentes`
   - por qué: El adjetivo 'cambiarias' no lleva tilde; con tilde sería la segunda persona del condicional de cambiar, que aquí no tiene sujeto posible. Medido en el corpus: 'cambiarías' aparece 53 veces y 'cambiarias' 19, o sea la forma mal acentuada es mayoritaria, pero el contexto de esta fila no admite la lectura verbal. Es la misma errata sistemática ya corregida 204 veces en singular.

### `RPM-2015-08-13:6974:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `que se han visto refrendadas con las modificaciones a la política cambiaría en ese país`
   - después: `que se han visto refrendadas con las modificaciones a la política cambiaria en ese país`
   - por qué: Tilde por i en posición de adjetivo, sección 3 ter.
2. **LETRA_CONFUNDIDA**
   - antes: `las perspectivas externas sugieren que la recuperación debiera der más lenta que lo anticipado`
   - después: `las perspectivas externas sugieren que la recuperación debiera ser más lenta que lo anticipado`
   - por qué: Ese por ese: 'debiera der' no es palabra y la oración no admite otra lectura. Corroborada dentro de la misma fila, que es lo mejor que puede pasar: 'debiera ser' aparece 1 vez en 6974:1, 1 en la sesión y 90 en el corpus. Medido: 'debiera der' aparece 1 sola vez en todo el corpus.

### `RPM-2013-03-14:5406:1` — Enrique Marshall Rivera

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2012-11-13:5186:1` — Claudio Soto Gamboa

1. **ACENTO_FALTANTE**
   - antes: `a parte extrapresupuestaria. Asimismo, resa`
   - después: `a parte extrapresupuestaría. Asimismo, resa`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2015-04-16:6733:1` — Miguel Fuentes Díaz

1. **SIMBOLO_SUELTO**
   - antes: ` i B A N C O C E N T R A L D E C H I L E`
   - después: ``
   - por qué: Encabezado de pagina del PDF, "BANCO CENTRAL DE CHILE", capturado letra por letra y con espacios. Es un residuo de la fuente, no texto del acta: la forma normal "BANCO CENTRAL DE CHILE" no aparece ninguna vez en el corpus, o sea que cuando este encabezado esta presente siempre viene letra por letra. Medido: 10 apariciones en 10 filas, mas 1 truncado ("...D E C H"). La politica es eliminar los residuos de la fuente (numeros de pagina, marcas de hora, comillas huerfanas, firmas truncadas) y este es de la misma familia.

### `RPM-2014-01-16:5964:1` — Consejo del Banco Central de Chile

1. **ESPACIO_INDEBIDO**
   - antes: `ña Poblete ; Gerente d`
   - después: `ña Poblete; Gerente d`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2014-12-11:6528:1` — Rodrigo Vergara Montes

1. **PUNTUACION**
   - antes: `"el alto precio del dólar alentará la inversión y el consumo"`
   - después: `“el alto precio del dólar alentará la inversión y el consumo”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.

### `RPM-2009-08-13:2679:1` — Matías Bernier Bórquez

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.
2. **ACENTO_FALTANTE**
   - antes: `e que relativiza el titulo, lo que no sign`
   - después: `e que relativiza el título, lo que no sign`
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2011-12-13:4513:1` — Rodrigo Vergara Montes

1. **ACENTO_FALTANTE**
   - antes: `ativas del mercado. Expresa que bajarla seria una medida de o`
   - después: `ativas del mercado. Expresa que bajarla sería una medida de o`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.
