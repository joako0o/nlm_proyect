# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1704**
- operaciones: **2863**
- filas marcadas para cotejo: **214**
- sha256 de la base: `32752bd52ce5d3b50b0732780154aaef23482908f6671f92a327509e75edf452`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 655 |
| `ESPACIO_INDEBIDO` | 510 |
| `PALABRA_PARTIDA` | 490 |
| `ACENTO_INDEBIDO` | 374 |
| `PUNTUACION` | 267 |
| `SIMBOLO_SUELTO` | 203 |
| `ACENTO_FALTANTE` | 186 |
| `FIRMA_TRUNCADA` | 55 |
| `RESIDUO_PAGINACION` | 30 |
| `PALABRA_ERRONEA` | 28 |
| `ESPACIO_FALTANTE` | 27 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |
| `PALABRA_DUPLICADA` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2015-08-13:6944:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `El Consejero señor Pablo García consulta sí hay alguna razón objetiva para no divulgar`
   - después: `El Consejero señor Pablo García consulta si hay alguna razón objetiva para no divulgar`
   - por qué: Tilde indebida: aquí 'si' es conjunción que introduce una interrogativa indirecta, no el adverbio de afirmación, y la oración no admite otra lectura. Corroborado además: 'consulta si hay' aparece 15 veces en el corpus y 'consulta sí hay' 2.

### `RPM-2012-04-17:4746:1` — Sergio Lehmann Beresi

1. **RESIDUO_PAGINACION**
   - antes: ` Sesión N° 184 Página 7 de 26 `
   - después: ` `
   - por qué: Residuo de paginacion del PDF incrustado en medio de la oracion. Medido: 26 apariciones, 24 con la cabecera "Sesion N° N" delante y 2 como pie de pagina del Comunicado ("Pagina 31 de 31"). "Sesion N° N" aparece 25 veces en el corpus y solo 24 van seguidas de Pagina, de modo que el patron exige ambos y no toca ninguna mencion legitima. Se elimina el residuo y se deja un solo espacio donde la oracion continua.

### `RPM-2009-03-12:2438:2` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `“`
   - por qué: Comilla recta que abre una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.
2. **PALABRA_PARTIDA**
   - antes: `T a s a`
   - después: `Tasa`
   - por qué: La palabra «Tasa» de la fórmula del Acuerdo está deletreada con espacios internos. Medido en el corpus: «-Tasa de Política» aparece bien escrita 119 veces y «T a s a» 9, siempre en la misma posición de la fórmula («el Consejo adopta el siguiente Acuerdo: <número>-Tasa de Política Monetaria»). Es el mismo defecto que el pase del §36 corrigió en la variante «T a sa» de 6 actas; ésta es la variante con las cuatro letras separadas. La posición es fija y no hay lectura alternativa: el número de acuerdo va pegado a la palabra.

### `RPM-2005-03-10:171:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `m antener`
   - después: `mantener`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 1788 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2010-01-14:2876:1` — Andrés Velasco Brañes

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2006-07-13:764:2` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `croeconómico referido ai sector fiscal, en esp`
   - después: `croeconómico referido al sector fiscal, en esp`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2013-04-11:5464:2` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `Lehman `
   - después: `Lehmann `
   - por qué: Apellido dañado por OCR: falta la ene final. Medido en el corpus: «Lehmann» aparece 1904 veces y «Lehman» 24, pero 19 de esas 24 son el banco de inversión Lehman Brothers, cuyo nombre correcto lleva una sola ene y no se toca. Las 5 restantes son la persona, Sergio Lehmann Beresi, Gerente de Análisis Internacional, siempre precedidas de «señor» o «Gerente señor». El campo Actor_Final de esas filas dice «Sergio Lehmann Beresi».

### `RPM-2007-08-09:1370:1` — Jorge Desormeaux Jiménez

1. **LETRA_CONFUNDIDA**
   - antes: `tema, señala que en ios Estados Unidos `
   - después: `tema, señala que en los Estados Unidos `
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2010-07-15:3272:1` — Rodrigo Vergara Montes

1. **PUNTUACION**
   - antes: `de año.`
   - después: `de año,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.

### `RPM-2015-09-15:6999:1` — Diego Gianelli Gómez

1. **ACENTO_INDEBIDO**
   - antes: `Polítíca`
   - después: `Política`
   - por qué: Acento espurio en la segunda «i». «Polítíca» no es palabra y aparece 6 veces en el corpus, siempre dentro de «Tasa de Polítíca Monetaria», «Opciones de Polítíca Monetaria», «División Polítíca Financiera» e «Informe de Polítíca Monetaria»; la forma del propio corpus es «Política», con 3.641 apariciones, y los dos PDF del repositorio dan 218 «Política» y 0 «Polítíca». A diferencia de los acentos de §16 (éstos/período/cuánto, donde las dos formas son español legítimo) y del «Seníor» de §27 (donde Sénior 79 y Senior 77 están empatados), aquí el destino no es ambiguo: no existe otra lectura.

### `RPM-2009-09-08:2690:1` — José De Gregorio Rebeco

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2008-12-11:2253:1` — José De Gregorio Rebeco

1. **PALABRA_PARTIDA**
   - antes: `dad de una política moneta ria contracíclica. `
   - después: `dad de una política monetaria contracíclica. `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 4276 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
2. **ESPACIO_INDEBIDO**
   - antes: ` monetaria . Indica qu`
   - después: ` monetaria. Indica qu`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: ` el futuro , pero para`
   - después: ` el futuro, pero para`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
4. **ESPACIO_INDEBIDO**
   - antes: ` similares , es que pr`
   - después: ` similares, es que pr`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
5. **ESPACIO_INDEBIDO**
   - antes: ` expuestas , el Presid`
   - después: ` expuestas, el Presid`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
6. **PALABRA_PARTIDA**
   - antes: `Como consecuenci a del`
   - después: `Como consecuencia del`
   - por qué: Palabra partida por un espacio espurio, con la segunda mitad reducida a una letra: «consecuenci a» -> «consecuencia». La evidencia es interna y doble: el primer trozo («consecuenci») es marginal en el corpus (1 apariciones, y ésas son ésta) y la forma junta («consecuencia») es la que el propio corpus usa 869 veces. La encontró detector_partida_letra, agregado en §31 porque detector_partida no puede verla: su guarda «segunda mitad con frecuencia < 50» bloquea justo las letras (a=37.528, o, e, s), que son frecuentes porque este mismo defecto las esparce. Precisión medida del detector: 40 candidatos en las 9.723 filas, 40 verdaderos; el único que no se corrige aquí es el de 147:1, que es la cola de una carrera letra por letra y se arregla entero en su pasada.
7. **ACENTO_FALTANTE**
   - antes: `politica`
   - después: `política`
   - por qué: Falta la tilde. Medido en el corpus: «politica» sin tilde aparece 1 sola vez (ésta) y «política» 5.573 — es la forma correcta más frecuente de todo el corpus, así que no hay duda.
8. **LETRA_CONFUNDIDA**
   - antes: `sé De Gregario qu`
   - después: `sé De Gregorio qu`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).
9. **LETRA_CONFUNDIDA**
   - antes: `sé De Gregario vo`
   - después: `sé De Gregorio vo`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).

### `RPM-2010-06-15:3201:1` — Enrique Marshall Rivera

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.
2. **PUNTUACION**
   - antes: `ista.`
   - después: `ista,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.
3. **PUNTUACION**
   - antes: `PM.`
   - después: `PM,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.

### `RPM-2008-05-08:1809:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `De Gregario`
   - después: `De Gregorio`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).

### `RPM-2007-03-15:1117:1` — Rodrigo Valdés Pulido

1. **LETRA_CONFUNDIDA**
   - antes: `cun/a`
   - después: `curva`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene curva y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.

### `RPM-2011-06-14:4106:1` — Luis Óscar Herrera Barriga

1. **ACENTO_INDEBIDO**
   - antes: `y disponibilidad de financíamiento internacional. `
   - después: `y disponibilidad de financiamiento internacional. `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 440 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
2. **ACENTO_INDEBIDO**
   - antes: `. En este contexto, índica que el balance `
   - después: `. En este contexto, indica que el balance `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2014-12-11:6525:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `Financia/`
   - después: `Financial`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene Financial y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.

### `RPM-2008-07-10:1925:3` — Jorge Desormeaux Jiménez

1. **LETRA_CONFUNDIDA**
   - antes: `poco más rápido que ios del petróleo.`
   - después: `poco más rápido que los del petróleo.`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2014-09-11:6425:1` — Alberto Naudon Dell'Oro

1. **PUNTUACION**
   - antes: `"a la baja"`
   - después: `“a la baja”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.
2. **PUNTUACION**
   - antes: `"neutral"`
   - después: `“neutral”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.

### `RPM-2010-07-15:3276:1` — José De Gregorio Rebeco

1. **ACENTO_FALTANTE**
   - antes: `gos que enfrenta la economia chilena. Agrega`
   - después: `gos que enfrenta la economía chilena. Agrega`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.
2. **ESPACIO_INDEBIDO**
   - antes: `e responde , en parte,`
   - después: `e responde, en parte,`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: `s fiscales , en especi`
   - después: `s fiscales, en especi`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
4. **ESPACIO_INDEBIDO**
   - antes: ` delicadas , y al aumento de tensiones financieras . No obstan`
   - después: ` delicadas, y al aumento de tensiones financieras. No obstan`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
5. **ESPACIO_INDEBIDO**
   - antes: `en aumento , lo que ha`
   - después: `en aumento, lo que ha`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
6. **LETRA_CONFUNDIDA**
   - antes: `Sanco`
   - después: `Banco`
   - por qué: El OCR escribio «S» donde va «B». «Sanco» no es palabra y aparece 7 veces en el corpus, siempre en contextos que solo admiten «Banco»: «el Sanco Central Europeo», «el Sanco Central», «por el Sanco». «Banco» aparece 2.418 veces. Las 7 se leyeron una por una.
7. **LETRA_CONFUNDIDA**
   - antes: `sé De Gregario pl`
   - después: `sé De Gregorio pl`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).
8. **LETRA_CONFUNDIDA**
   - antes: `sé De Gregario me`
   - después: `sé De Gregorio me`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).

### `RPM-2006-06-15:731:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `Garda`
   - después: `García`
   - por qué: Apellido dañado por OCR: «Garda» por «García». Medido en el corpus: «Pablo García» aparece 737 veces y «Pablo Garda» 1. En 2006-06-15:731:1 el propio campo Actor_Final de la fila es «Pablo García Silva», de modo que «el señor Garda» es una autorreferencia con el apellido dañado.

### `RPM-2009-12-15:2809:3` — José De Gregorio Rebeco

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2009-05-07:2519:2` — Sergio Lehmann Beresi

1. **ESPACIO_FALTANTE**
   - antes: `yeso`
   - después: `y eso`
   - por qué: yeso por "y eso". Medido: 13 apariciones, en todas falta el espacio entre la conjuncion y el demostrativo ("alto yeso tiene que tener" = "alto, y eso tiene que tener"). Verificado que ninguna esta embebida en otra palabra. La coma no se inserta: la oracion queda gramatical sin ella y anadirla seria editar puntuacion.
2. **PALABRA_PARTIDA**
   - antes: ` ha centrado en las econom ías desarrolladas. `
   - después: ` ha centrado en las economías desarrolladas. `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2935 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
3. **PALABRA_PARTIDA**
   - antes: `as de las economías desarro lladas, éstas no se vi`
   - después: `as de las economías desarrolladas, éstas no se vi`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 650 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
4. **ACENTO_INDEBIDO**
   - antes: ` Continuando con la comparacíón entre ambas cri`
   - después: ` Continuando con la comparación entre ambas cri`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 234 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
5. **ESPACIO_INDEBIDO**
   - antes: `a indicaba , China cum`
   - después: `a indicaba, China cum`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
6. **ESPACIO_FALTANTE**
   - antes: `versus la crisis asiática.Hace presente`
   - después: `versus la crisis asiática. Hace presente`
   - por qué: Falta el espacio tras el punto. «Hace» va en mayúscula, así que es inicio de oración.
7. **PALABRA_PARTIDA**
   - antes: `se apreci a que`
   - después: `se aprecia que`
   - por qué: Palabra partida por un espacio espurio, con la segunda mitad reducida a una letra: «apreci a» -> «aprecia». La evidencia es interna y doble: el primer trozo («apreci») es marginal en el corpus (1 apariciones, y ésas son ésta) y la forma junta («aprecia») es la que el propio corpus usa 321 veces. La encontró detector_partida_letra, agregado en §31 porque detector_partida no puede verla: su guarda «segunda mitad con frecuencia < 50» bloquea justo las letras (a=37.528, o, e, s), que son frecuentes porque este mismo defecto las esparce. Precisión medida del detector: 40 candidatos en las 9.723 filas, 40 verdaderos; el único que no se corrige aquí es el de 147:1, que es la cola de una carrera letra por letra y se arregla entero en su pasada.
8. **PALABRA_PARTIDA**
   - antes: `alimenticios com o granos`
   - después: `alimenticios como granos`
   - por qué: Palabra partida por un espacio espurio, con la segunda mitad reducida a una letra: «com o» -> «como». La evidencia es interna y doble: el primer trozo («com») es marginal en el corpus (2 apariciones, y ésas son ésta) y la forma junta («como») es la que el propio corpus usa 5932 veces. La encontró detector_partida_letra, agregado en §31 porque detector_partida no puede verla: su guarda «segunda mitad con frecuencia < 50» bloquea justo las letras (a=37.528, o, e, s), que son frecuentes porque este mismo defecto las esparce. Precisión medida del detector: 40 candidatos en las 9.723 filas, 40 verdaderos; el único que no se corrige aquí es el de 147:1, que es la cola de una carrera letra por letra y se arregla entero en su pasada.

### `RPM-2007-01-11:1034:1` — Igal Magendzo Weinberger

1. **SIMBOLO_SUELTO**
   - antes: `ese año en 5%-6%%,`
   - después: `ese año en 5%-6%,`
   - por qué: El signo de porcentaje sale duplicado tras la cifra. No existe lectura en que «%%» sea correcto: en el mismo párrafo las cifras vecinas llevan un solo signo. Se deja uno.
2. **SIMBOLO_SUELTO**
   - antes: `origen importado. J) El Gerente`
   - después: `origen importado. El Gerente`
   - por qué: Marcador suelto en un límite de párrafo, dentro de una fila de 10.032 caracteres: «...bienes de origen importado. [J)] El Gerente de Análisis Macroeconómico señor Magendzo, indica que además...». Se leyó como posible enumeración de la fuente y se descartó con tres mediciones: (1) en las 9.723 filas hay 4 «LETRA)» y las otras 3 son cierres de sigla o paréntesis («M&E)», «(I)» dos veces), no enumeraciones; (2) los dos PDF del repositorio (2005-06-09 y 2005-07-12, 45 páginas) tienen CERO enumeraciones con letra; (3) la posición —límite de párrafo dentro de una fila— es la misma donde esta sesión tiene sus otros tres residuos de salto de página (« k » en 1044:1, « 1-^ » en 1056:1, « l-P » en 1049:3). No reemplaza ninguna palabra. Tipo SIMBOLO_SUELTO. Si el PDF de 2007-01-11 mostrara una enumeración real, el Texto original sigue intacto y la operación se puede revertir.

### `RPM-2011-11-15:4459:1` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2010-12-16:3598:1` — Manuel Marfán Lewis

1. **ESPACIO_INDEBIDO**
   - antes: `cial Times , Bélgica e`
   - después: `cial Times, Bélgica e`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2013-02-14:5387:1` — Felipe Larraín Bascuñán

1. **ACENTO_FALTANTE**
   - antes: `de Ejecución Presupuestaria entregado el 31`
   - después: `de Ejecución Presupuestaría entregado el 31`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.
2. **ESPACIO_INDEBIDO**
   - antes: `dio de 3,3 % en el año`
   - después: `dio de 3,3% en el año`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2015-07-14:6910:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2010-07-15:3277:1` — José De Gregorio Rebeco

1. **PALABRA_PARTIDA**
   - antes: `T a s a`
   - después: `Tasa`
   - por qué: La palabra «Tasa» de la fórmula del Acuerdo está deletreada con espacios internos. Medido en el corpus: «-Tasa de Política» aparece bien escrita 119 veces y «T a s a» 9, siempre en la misma posición de la fórmula («el Consejo adopta el siguiente Acuerdo: <número>-Tasa de Política Monetaria»). Es el mismo defecto que el pase del §36 corrigió en la variante «T a sa» de 6 actas; ésta es la variante con las cuatro letras separadas. La posición es fija y no hay lectura alternativa: el número de acuerdo va pegado a la palabra.

### `RPM-2010-06-15:3155:1` — Claudio Soto Gamboa

1. **PUNTUACION**
   - antes: `rial.`
   - después: `rial,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.
