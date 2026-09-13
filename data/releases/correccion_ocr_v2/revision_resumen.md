# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1791**
- operaciones: **3085**
- filas marcadas para cotejo: **237**
- sha256 de la base: `eebaa728dc1d7ce14315caebd0c7516ff324b5d4acaefcf40cec2bf6d855945d`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 756 |
| `ESPACIO_INDEBIDO` | 507 |
| `PALABRA_PARTIDA` | 495 |
| `ACENTO_INDEBIDO` | 387 |
| `PUNTUACION` | 268 |
| `SIMBOLO_SUELTO` | 242 |
| `ACENTO_FALTANTE` | 220 |
| `FIRMA_TRUNCADA` | 55 |
| `RESIDUO_PAGINACION` | 36 |
| `ESPACIO_FALTANTE` | 35 |
| `PALABRA_ERRONEA` | 33 |
| `PALABRA_OMITIDA` | 22 |
| `PALABRA_DUPLICADA` | 16 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2015-02-12:6618:3` — Miguel Fuentes Díaz

1. **ESPACIO_FALTANTE**
   - antes: `que sube a100%`
   - después: `que sube a 100%`
   - por qué: Falta el espacio entre la preposición y la cifra: «a100%» no es una palabra. Mismo caso ya registrado en el corpus («un13% en febrero» → «un 13%»).

### `RPM-2011-07-14:4214:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` MANUEL MARFAN LEWIS JOSÉ DE GREGORIO REBECO Vicepresidente Presidente 7 SEBASTIÁN CLARO EDWARDS ENRI0UE MARSHALL RIVERA Consejero Consejero.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

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

### `RPM-2009-11-12:2769:2` — Sergio Lehmann Beresi

1. **PUNTUACION**
   - antes: `No habiendo más comentarios,.`
   - después: `No habiendo más comentarios,`
   - por qué: Coma seguida de punto al final de la fila. Medido en el corpus: «<palabra>,.» aparece 98 veces en el texto virgen; el pase transversal del §45 corrigió 78 (76 «A continuación,.» más «década,.» y «Euro,.») y dejó estas 20, que son la misma familia con otras palabras: «Continuando con la votación,.» (6), «Para concluir con la votación,.» (3), «No habiendo más comentarios,.» (8), «No habiendo más comentarios y preguntas,.» (2) y «…señor Manuel Marfán,.» (1). En los 20 casos la fila siguiente empieza con «el Presidente…», «el Consejero…» o «el Vicepresidente…», de modo que la coma es la marca correcta y el punto es el signo sobrante. Se aplica el mismo criterio del §45.

### `RPM-2006-06-15:688:1` — Vittorio Corbo Lioi

1. **LETRA_CONFUNDIDA**
   - antes: `rio Corbo en relación ai precio del cobre, que`
   - después: `rio Corbo en relación al precio del cobre, que`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2012-10-18:5116:1` — Joaquín Vial Ruiz-Tagle

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2007-07-12:1321:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `ios gráficos, el efecto fiy to quality sobre Chile s`
   - después: `los gráficos, el efecto fly to quality sobre Chile s`
   - por qué: "fiy"/"fIy" por "fly": la l se leyo como i (o como I). Es el mismo glifo que produce "ai" por "al", demostrado con 26 casos independientes. Se retira la marca RECONSTRUCCION_AMBIGUA que se había puesto en esta fila: al aparecer la regla de glifo, la ambigüedad se resuelve. Un escáner no convierte "flight" en "fiy" (sería borrar cuatro letras); sí convierte "fly" en "fiy". Las 21 apariciones de "flight to quality" que hay en el corpus son la otra grafía, correcta, y no se tocan. La operación se extendió dos caracteres hacia la izquierda para cubrir además "ios" por "los" (§12): ambas caen en el mismo tramo y dos operaciones separadas se pisarían, porque el fragmento anterior empezaba justo en la s de "ios".

### `RPM-2010-05-13:3119:1` — Luis Felipe Céspedes Cifuentes

1. **PUNTUACION**
   - antes: `io.`
   - después: `io,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.

### `RPM-2015-04-16:6730:2` — Claudio Soto Gamboa

1. **SIMBOLO_SUELTO**
   - antes: ` B A N C O C E N T R A L D E C H I L E`
   - después: ``
   - por qué: Encabezado de pagina del PDF, "BANCO CENTRAL DE CHILE", capturado letra por letra y con espacios. Es un residuo de la fuente, no texto del acta: la forma normal "BANCO CENTRAL DE CHILE" no aparece ninguna vez en el corpus, o sea que cuando este encabezado esta presente siempre viene letra por letra. Medido: 10 apariciones en 10 filas, mas 1 truncado ("...D E C H"). La politica es eliminar los residuos de la fuente (numeros de pagina, marcas de hora, comillas huerfanas, firmas truncadas) y este es de la misma familia.

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

### `RPM-2010-03-18:3020:1` — José De Gregorio Rebeco

1. **PALABRA_PARTIDA**
   - antes: ` pero con tensiones cambiari as y la potencial `
   - después: ` pero con tensiones cambiarias y la potencial `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 80 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2008-04-10:1747:1` — Sergio Lehmann Beresi

1. **ESPACIO_FALTANTE**
   - antes: `yeso`
   - después: `y eso`
   - por qué: yeso por "y eso". Medido: 13 apariciones, en todas falta el espacio entre la conjuncion y el demostrativo ("alto yeso tiene que tener" = "alto, y eso tiene que tener"). Verificado que ninguna esta embebida en otra palabra. La coma no se inserta: la oracion queda gramatical sin ella y anadirla seria editar puntuacion.
2. **PUNTUACION**
   - antes: `"Dificultad para encontrar empleo"`
   - después: `“Dificultad para encontrar empleo”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.
3. **PALABRA_PARTIDA**
   - antes: `alta demanda de las econom ías emergentes.
Asi`
   - después: `alta demanda de las economías emergentes.
Asi`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2935 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
4. **ACENTO_INDEBIDO**
   - antes: `ñor Gerente que las noticías son claramente `
   - después: `ñor Gerente que las noticias son claramente `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 944 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
5. **ACENTO_INDEBIDO**
   - antes: `n en lo que son las tendencías
inflacionarias.`
   - después: `n en lo que son las tendencias
inflacionarias.`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 225 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
6. **ESPACIO_INDEBIDO**
   - antes: `
del cobre ,
particula`
   - después: `
del cobre,
particula`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
7. **ESPACIO_INDEBIDO**
   - antes: ` del cobre , este
se h`
   - después: ` del cobre, este
se h`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
8. **ESPACIO_INDEBIDO**
   - antes: `imo
de 4,1 %. Destaca `
   - después: `imo
de 4,1%. Destaca `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
9. **ESPACIO_INDEBIDO**
   - antes: ` comercial , si bien
e`
   - después: ` comercial, si bien
e`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
10. **PALABRA_ERRONEA**
   - antes: `creciendo
e.n
Ií ~ea con el mayor`
   - después: `creciendo en línea con el mayor`
   - por qué: Tramo dañado por el OCR, con saltos de línea incluidos: «e.n Ií ~ea» por «en línea». La reconstrucción es única porque «en línea con» es una expresión fija del corpus y es lo único que encaja entre «las solicitudes de desempleo han ido creciendo» y «con el mayor desempleo».

### `RPM-2007-02-08:1074:1` — José De Gregorio Rebeco

1. **ACENTO_FALTANTE**
   - antes: `el escenario que se tenia hace uno y dos `
   - después: `el escenario que se tenía hace uno y dos `
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2011-01-13:3678:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarla`
   - después: `cambiaria`
   - por qué: cambiarla por cambiaria. Misma familia y mismo defecto. Medido: 8 apariciones (todas dentro de "cambiarlas"), todas adjetivas y revisadas una por una: "paridades cambiarlas" 4 veces, "implicancias cambiarlas" 2, "expectativas cambiarlas" 1, "coberturas cambiarlas" 1. "cambiarias" ya aparece 19 veces en el corpus.

### `RPM-2014-04-17:6177:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `n observado ajustes margínales en el último ti`
   - después: `n observado ajustes marginales en el último ti`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 113 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2008-05-08:1847:1` — Jorge Desormeaux Jiménez

1. **SIMBOLO_SUELTO**
   - antes: `una dirección u otra. U U) Menciona`
   - después: `una dirección u otra. Menciona`
   - por qué: Dos residuos seguidos, "U" y "U)": la regla general de letra suelta solo quitaria el primero y dejaria "U) Menciona". Se eliminan los dos en una sola operacion porque son adyacentes y forman un unico bloque de ruido entre las dos oraciones.

### `RPM-2014-03-13:6092:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2010-05-13:3121:1` — Rodrigo Vergara Montes

1. **PUNTUACION**
   - antes: `Continuando con la votación,.`
   - después: `Continuando con la votación,`
   - por qué: Coma seguida de punto al final de la fila. Medido en el corpus: «<palabra>,.» aparece 98 veces en el texto virgen; el pase transversal del §45 corrigió 78 (76 «A continuación,.» más «década,.» y «Euro,.») y dejó estas 20, que son la misma familia con otras palabras: «Continuando con la votación,.» (6), «Para concluir con la votación,.» (3), «No habiendo más comentarios,.» (8), «No habiendo más comentarios y preguntas,.» (2) y «…señor Manuel Marfán,.» (1). En los 20 casos la fila siguiente empieza con «el Presidente…», «el Consejero…» o «el Vicepresidente…», de modo que la coma es la marca correcta y el punto es el signo sobrante. Se aplica el mismo criterio del §45.

### `RPM-2006-05-11:659:1` — Esteban Jadresic Marinovic

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

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

### `RPM-2006-12-14:1001:1` — Rodrigo Valdés Pulido

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2011-05-12:4052:2` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2010-08-12:3313:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `De Gregario`
   - después: `De Gregorio`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).
2. **SIMBOLO_SUELTO**
   - antes: ` había aumentado entre 100.000 Y 150.000 mil personas,`
   - después: ` había aumentado entre 100.000 y 150.000 mil personas,`
   - por qué: Conjunción «y» leída como mayúscula por el OCR. El corpus la escribe en minúscula; se excluyó el único caso legítimo, «el eje Y» (RPM-2012-09-13:5049:1), donde la mayúscula nombra el eje.

### `RPM-2012-07-12:4958:1` — Luis Óscar Herrera Barriga

1. **ACENTO_INDEBIDO**
   - antes: `o. En este sentido, índica que las cifras `
   - después: `o. En este sentido, indica que las cifras `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2014-12-11:6530:1` — Claudio Raddatz Kiefer

1. **LETRA_CONFUNDIDA**
   - antes: `Claudia Raddatz`
   - después: `Claudio Raddatz`
   - por qué: La «a» final ocupó el lugar de la «o» en el nombre de pila. El propio texto lo descarta: la fila lo trata en masculino («señor» o «don») y el corpus atestigua «Claudio Raddatz» 75 veces contra 1 «Claudia Raddatz». No es la Claudia legítima del corpus (doña Claudia Varela Lértora, doña Claudia Sotz Pantoja), que siempre va con «doña» o «Gerenta».

### `RPM-2010-05-13:3124:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `e de las noticias de! Ministro respec`
   - después: `e de las noticias del Ministro respec`
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2010-03-18:3000:1` — Matías Bernier Bórquez

1. **SIMBOLO_SUELTO**
   - antes: `una disminución del stock neto en la ■V última semana, en el d`
   - después: `una disminución del stock neto en la última semana, en el d`
   - por qué: Símbolo ■ con basura adyacente, residuo del escaneo. El tipo SIMBOLO_SUELTO fue creado justamente para estos casos («■V», «ry _<< ■» -> se elimina). Medido: 21 apariciones en 20 filas. Se trata cada una con su basura propia porque el ruido que la acompaña varía (■o J, ■,\y, ■', ■J, ■V, / ■ ' /, 4 / ■, i - /■, — f ■, ry _<< ■). En todos los casos las dos oraciones que rodean el residuo quedan completas sin él. Excepción: en 5802:2 se elimina solo el ■ y se deja el paréntesis abierto, porque esa fila ya está marcada RECONSTRUCCION_AMBIGUA_POR_COTEJAR con motivo FINAL_SIN_PUNTUACION.
