# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1820**
- operaciones: **3166**
- filas marcadas para cotejo: **247**
- sha256 de la base: `eebaa728dc1d7ce14315caebd0c7516ff324b5d4acaefcf40cec2bf6d855945d`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 824 |
| `ESPACIO_INDEBIDO` | 508 |
| `PALABRA_PARTIDA` | 496 |
| `ACENTO_INDEBIDO` | 391 |
| `PUNTUACION` | 276 |
| `SIMBOLO_SUELTO` | 259 |
| `ACENTO_FALTANTE` | 193 |
| `FIRMA_TRUNCADA` | 55 |
| `ESPACIO_FALTANTE` | 39 |
| `RESIDUO_PAGINACION` | 36 |
| `PALABRA_ERRONEA` | 34 |
| `PALABRA_OMITIDA` | 24 |
| `PALABRA_DUPLICADA` | 16 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 5 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2014-10-16:6454:1` — Miguel Fuentes Díaz

1. **ESPACIO_INDEBIDO**
   - antes: `tomóviles— , y que las`
   - después: `tomóviles—, y que las`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2011-07-14:4203:1` — Felipe Larraín Bascuñán

1. **PUNTUACION**
   - antes: `"bono basura"`
   - después: `“bono basura”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.
2. **ACENTO_INDEBIDO**
   - antes: `ión de los salarios nomínales y reales, que c`
   - después: `ión de los salarios nominales y reales, que c`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 606 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
3. **ESPACIO_INDEBIDO**
   - antes: `o solo 3,1 % en mayo, `
   - después: `o solo 3,1% en mayo, `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2009-02-12:2352:1` — Matías Bernier Bórquez

1. **ESPACIO_INDEBIDO**
   - antes: ` escenario . Agrega, q`
   - después: ` escenario. Agrega, q`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2005-03-10:161:1` — Luis Óscar Herrera Barriga

1. **PALABRA_PARTIDA**
   - antes: `os con la inversión exi stente. Al respecto, e`
   - después: `os con la inversión existente. Al respecto, e`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 40 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
2. **PALABRA_PARTIDA**
   - antes: `e lo anterior puede ten er algunos efectos`
   - después: `e lo anterior puede tener algunos efectos`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 1011 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
3. **PALABRA_PARTIDA**
   - antes: `m arginales`
   - después: `marginales`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 116 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
4. **PALABRA_PARTIDA**
   - antes: `m eses`
   - después: `meses`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 4246 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
5. **PALABRA_PARTIDA**
   - antes: `Estados Uni dos están`
   - después: `Estados Unidos están`
   - por qué: Palabra partida por un espacio espurio, con la segunda mitad reducida a una letra: «Uni dos» -> «Unidos». La evidencia es interna y doble: el primer trozo («Uni») es marginal en el corpus (1 apariciones, y ésas son ésta) y la forma junta («Unidos») es la que el propio corpus usa 2782 veces. La encontró detector_partida_letra, agregado en §31 porque detector_partida no puede verla: su guarda «segunda mitad con frecuencia < 50» bloquea justo las letras (a=37.528, o, e, s), que son frecuentes porque este mismo defecto las esparce. Precisión medida del detector: 40 candidatos en las 9.723 filas, 40 verdaderos; el único que no se corrige aquí es el de 147:1, que es la cola de una carrera letra por letra y se arregla entero en su pasada.

### `RPM-2009-11-12:2768:2` — Sergio Lehmann Beresi

1. **ACENTO_FALTANTE**
   - antes: `especto a lo que se tenia en el último IP`
   - después: `especto a lo que se tenía en el último IP`
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».
2. **ACENTO_FALTANTE**
   - antes: `y el señor Sergio Lehmann agrega que seria útil contar con`
   - después: `y el señor Sergio Lehmann agrega que sería útil contar con`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.

### `RPM-2006-06-15:675:1` — Consejo del Banco Central de Chile

1. **LETRA_CONFUNDIDA**
   - antes: `regorio Rebeco y de ios Consejeros don `
   - después: `regorio Rebeco y de los Consejeros don `
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2012-09-13:5074:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2007-07-12:1310:1` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `Olivia Recart Asisten también; Gerente General, `
   - después: `Olivia Recart Asisten también: Gerente General, `
   - por qué: Punto y coma por dos puntos. Medido: "Asisten también:" aparece 93 veces y "Asisten también;" 7. La formula introduce una lista, así que corresponde dos puntos.

### `RPM-2010-05-13:3110:1` — Consejo del Banco Central de Chile

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2014-12-11:6538:1` — Rodrigo Vergara Montes

1. **LETRA_CONFUNDIDA**
   - antes: `op1nion`
   - después: `opinión`
   - por qué: op1nion por opinión: la i se leyo como el digito 1 y falta la tilde. Contexto "agradece la op1nion del Ministro", sin lectura alternativa.

### `RPM-2009-06-16:2593:2` — Pablo García Silva

1. **PUNTUACION**
   - antes: `ente año.`
   - después: `ente año,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.
2. **LETRA_CONFUNDIDA**
   - antes: `cambiaba`
   - después: `cambiaria`
   - por qué: «cambiaba» por «cambiaria»: es el adjetivo, no el verbo. Medido en el corpus: «cambiaria/o» aparece 229 veces y «cambiaba» 4, de las cuales 2 son el verbo en pretérito imperfecto y se dejan («la cual no cambiaba con la información disponible», «no cambiaba en general los contornos»). Las 2 que se corrigen van sustantivadas: «una intervención cambiaba», «una apreciación cambiaba».

### `RPM-2008-11-13:2137:1` — José De Gregorio Rebeco

1. **PALABRA_DUPLICADA**
   - antes: `osé De Gregorio ofrece la palabra al Gerente de de Análisis Macroeconómico señor Claudio Soto G`
   - después: `osé De Gregorio ofrece la palabra al Gerente de Análisis Macroeconómico señor Claudio Soto G`
   - por qué: Preposición duplicada. Los 13 casos del corpus son la misma lesión y ninguno es legítimo: no hay construcción del español con «de de» seguido de sustantivo. Se corrigieron uno por uno.

### `RPM-2010-03-18:3014:1` — Felipe Larraín Bascuñán

1. **PALABRA_PARTIDA**
   - antes: `que permitirí a retomar`
   - después: `que permitiría retomar`
   - por qué: Palabra partida por un espacio espurio, con la segunda mitad reducida a una letra: «permitirí a» -> «permitiría». La evidencia es interna y doble: el primer trozo («permitirí») es marginal en el corpus (1 apariciones, y ésas son ésta) y la forma junta («permitiría») es la que el propio corpus usa 54 veces. La encontró detector_partida_letra, agregado en §31 porque detector_partida no puede verla: su guarda «segunda mitad con frecuencia < 50» bloquea justo las letras (a=37.528, o, e, s), que son frecuentes porque este mismo defecto las esparce. Precisión medida del detector: 40 candidatos en las 9.723 filas, 40 verdaderos; el único que no se corrige aquí es el de 147:1, que es la cola de una carrera letra por letra y se arregla entero en su pasada.

### `RPM-2008-03-13:1744:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` JORGE DESORMEAUX JIMÉNEZ JOSÉ DE GREGORIO REBECO Vicepresidente Presidente ENRIQUE MARSHALL RIVERA Consejero.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2007-02-08:1061:2` — Sergio Lehmann Beresi

1. **PALABRA_PARTIDA**
   - antes: ` que teníamos en el IP oM de enero, y par`
   - después: ` que teníamos en el IPoM de enero, y par`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2481 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2011-01-13:3678:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarla`
   - después: `cambiaria`
   - por qué: cambiarla por cambiaria. Misma familia y mismo defecto. Medido: 8 apariciones (todas dentro de "cambiarlas"), todas adjetivas y revisadas una por una: "paridades cambiarlas" 4 veces, "implicancias cambiarlas" 2, "expectativas cambiarlas" 1, "coberturas cambiarlas" 1. "cambiarias" ya aparece 19 veces en el corpus.

### `RPM-2014-03-13:6074:2` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: ` ei`
   - después: ` el`
   - por qué: «ei» en lugar del artículo «el»: el OCR confunde la «l» con la «i». Sigue un sustantivo masculino, así que no hay otra lectura. Familia de 14 ocurrencias en 13 filas del corpus. §75.

### `RPM-2008-05-08:1844:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `obsen/ada`
   - después: `observada`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene observada y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.

### `RPM-2014-02-18:6009:4` — Miguel Ricaurte Bermúdez

1. **SIMBOLO_SUELTO**
   - antes: `registrado alzas mayores. V El señor`
   - después: `registrado alzas mayores. El señor`
   - por qué: Letra mayúscula suelta entre dos oraciones. Es ruido de escaneo: la oración anterior termina en punto y la siguiente empieza con mayúscula y sentido completo, así que la letra no pertenece a ninguna de las dos. Medido: 17 casos en 17 filas, con las letras V, H, L, U, A, M, Y, B. Se revisaron uno por uno; el único que NO es residuo es RPM-2007-01-11:1055:1 ("prolongado. A SU juicio"), donde la A abre la oración legítimamente y el defecto es "SU" en mayúscula, que se trata aparte.

### `RPM-2010-05-13:3116:1` — Beltrán de Ramón Acevedo

1. **PUNTUACION**
   - antes: `ue.`
   - después: `ue,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.

### `RPM-2006-04-13:654:1` — Vittorio Corbo Lioi

1. **LETRA_CONFUNDIDA**
   - antes: ` del último IPOM`
   - después: ` del último IPoM`
   - por qué: Sigla mal compuesta. Medido en el corpus: «IPoM» aparece 2473 veces y «IPOM» 58, siempre el mismo documento, el Informe de Política Monetaria del Banco Central de Chile, cuya sigla lleva la o minúscula. El OCR leyó la o minúscula como O mayúscula.
2. **LETRA_CONFUNDIDA**
   - antes: `n el último IPOM`
   - después: `n el último IPoM`
   - por qué: Sigla mal compuesta. Medido en el corpus: «IPoM» aparece 2473 veces y «IPOM» 58, siempre el mismo documento, el Informe de Política Monetaria del Banco Central de Chile, cuya sigla lleva la o minúscula. El OCR leyó la o minúscula como O mayúscula.

### `RPM-2009-10-13:2725:1` — Sergio Lehmann Beresi

1. **ACENTO_FALTANTE**
   - antes: ` embargo, que otras lineas de financiamien`
   - después: ` embargo, que otras líneas de financiamien`
   - por qué: Tilde faltante, grupo B3. Se leyeron las 53 apariciones de linea, continua, publica y lineas, y sólo 23 son defecto. «linea»: las 18 son la fórmula «en linea con», siempre el sustantivo, así que van con contexto. «lineas»: las 4 son sustantivo («otras lineas de financiamiento», «algunas lineas manufactureras», «de las lineas vinculadas»). «continua»: de 18 apariciones sólo 2 son el verbo («la actividad económica continua creciendo», «esta parte de la economía continua funcionando»); las otras 16 son el adjetivo continuo/continua y NO se tocan («la continua caída», «la mejora continua», «la convergencia continua y gradual», «la serie no es continua», «de continua colaboración», «de manera continua»). «publica»: las 13 son la tercera persona del verbo publicar («se publica anualmente», «la Reserva Federal no publica su propia», «el INE no los publica», «que publica el Fondo») y ninguna se corrige.

### `RPM-2009-03-12:2434:2` — Sebastián Claro Edwards

1. **ACENTO_FALTANTE**
   - antes: `cias internas están en linea con la tendencia de`
   - después: `cias internas están en línea con la tendencia de`
   - por qué: Tilde faltante, grupo B3. Se leyeron las 53 apariciones de linea, continua, publica y lineas, y sólo 23 son defecto. «linea»: las 18 son la fórmula «en linea con», siempre el sustantivo, así que van con contexto. «lineas»: las 4 son sustantivo («otras lineas de financiamiento», «algunas lineas manufactureras», «de las lineas vinculadas»). «continua»: de 18 apariciones sólo 2 son el verbo («la actividad económica continua creciendo», «esta parte de la economía continua funcionando»); las otras 16 son el adjetivo continuo/continua y NO se tocan («la continua caída», «la mejora continua», «la convergencia continua y gradual», «la serie no es continua», «de continua colaboración», «de manera continua»). «publica»: las 13 son la tercera persona del verbo publicar («se publica anualmente», «la Reserva Federal no publica su propia», «el INE no los publica», «que publica el Fondo») y ninguna se corrige.

### `RPM-2006-11-16:978:1` — Klaus Schmidt-Hebbel Dunker

1. **PUNTUACION**
   - antes: `te.`
   - después: `te,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.

### `RPM-2011-05-12:4012:2` — Beltrán de Ramón Acevedo

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2010-08-12:3310:7` — Claudio Soto Gamboa

1. **ESPACIO_INDEBIDO**
   - antes: `ctivamente , por un pe`
   - después: `ctivamente, por un pe`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2012-06-14:4889:1` — Felipe Larraín Bascuñán

1. **LETRA_CONFUNDIDA**
   - antes: ` se ha visto sacudido por temores que se han incrementando respecto a la situación de Europa. En efecto`
   - después: ` se ha visto sacudido por temores que se han incrementado respecto a la situación de Europa. En efecto`
   - por qué: «haber» más gerundio no es una forma del español: el participio es «haber» más participio. Los 9 casos del corpus son la misma lesión (la «d» del participio leída como «n») y se corrigieron uno por uno; en 2291:2 sólo cambia el primer verbo, porque «se han continuado disipando» lleva gerundio legítimo después.

### `RPM-2014-09-11:6399:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `1O`
   - después: `10`
   - por qué: 1O por 10: el cero se leyo como la letra O mayuscula. Medido: 7 apariciones en 6 filas y todas son numeros donde solo cabe el diez ("tasas a 1O años plazo", "lámina Nº 1O", "US$ 3,1O la libra", "a 5 y 1O años", "a 2 y 1O años", "a 1O años", "de 1O o 20%"). Se verifico que no existen apariciones embebidas en otras palabras.

### `RPM-2010-05-13:3119:1` — Luis Felipe Céspedes Cifuentes

1. **PUNTUACION**
   - antes: `io.`
   - después: `io,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.

### `RPM-2010-03-18:2992:2` — Claudio Soto Gamboa

1. **ESPACIO_INDEBIDO**
   - antes: `es décimas , ya que se`
   - después: `es décimas, ya que se`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **LETRA_CONFUNDIDA**
   - antes: `Claudia Soto`
   - después: `Claudio Soto`
   - por qué: La «a» final ocupó el lugar de la «o» en el nombre de pila. El propio texto lo descarta: la fila lo trata en masculino («señor» o «don») y el corpus atestigua «Claudio Soto» 1.275 veces contra 1 «Claudia Soto». No es la Claudia legítima del corpus (doña Claudia Varela Lértora, doña Claudia Sotz Pantoja), que siempre va con «doña» o «Gerenta».
