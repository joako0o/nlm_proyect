# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1806**
- operaciones: **3127**
- filas marcadas para cotejo: **240**
- sha256 de la base: `eebaa728dc1d7ce14315caebd0c7516ff324b5d4acaefcf40cec2bf6d855945d`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 815 |
| `ESPACIO_INDEBIDO` | 507 |
| `PALABRA_PARTIDA` | 496 |
| `ACENTO_INDEBIDO` | 390 |
| `PUNTUACION` | 268 |
| `SIMBOLO_SUELTO` | 244 |
| `ACENTO_FALTANTE` | 190 |
| `FIRMA_TRUNCADA` | 55 |
| `ESPACIO_FALTANTE` | 39 |
| `RESIDUO_PAGINACION` | 36 |
| `PALABRA_ERRONEA` | 34 |
| `PALABRA_OMITIDA` | 24 |
| `PALABRA_DUPLICADA` | 16 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2014-12-11:6518:1` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `o; Gerente de División Estudios, don Alberto Naudon Dell'Oro; Gerente de División Operaciones Financieras`
   - después: `o; Gerente de División Estudios, don Alberto Naudon Dell’Oro; Gerente de División Operaciones Financieras`
   - por qué: Normalización de nombre propio dañado, autorizada por el usuario en esta ronda (antes el criterio era marcar sin corregir). La forma correcta la acredita el propio corpus: «Alberto Naudon Dell’Oro» aparece 12 veces (RPM-2014-08-14:6342:1, RPM-2014-10-16:6440:1 y otras) y «Dell'Oro» 3; el apóstrofo curvo es además el mayoritario en el corpus (59 contra 41 rectos). Se unifica a una sola grafía para que la persona tenga un único nombre en la base. No es una conjetura: es la forma que el corpus ya usa para el mismo cargo y la misma persona (Gerente de División Estudios). Caso: «Dell'Oro» con apóstrofo recto. La fila NO estaba dañada: se unifica sólo la grafía del apóstrofo a la mayoritaria para que la persona tenga un único nombre en la base. Es reversible y no altera Texto.
2. **LETRA_CONFUNDIDA**
   - antes: `POLiTICA`
   - después: `POLÍTICA`
   - por qué: Fórmula fija del encabezado de acta. Medido en el corpus: «SESIÓN» aparece 115 veces y «SESION» 14 más «SESiÓN» 2; «POLÍTICA» 111 y «POLITICA» 16 más «POLíTICA» 1 y «POLiTICA» 3. La fórmula completa correcta «SESIÓN DE POLÍTICA MONETARIA» aparece 111 veces contra 14 sin acentos. Es el mismo encabezado en todas las actas, así que la forma canónica no admite duda; el OCR perdió el acento o leyó la Í mayúscula como i minúscula.

### `RPM-2011-08-18:4222:1` — Luis Óscar Herrera Barriga

1. **LETRA_CONFUNDIDA**
   - antes: `¡guales`
   - después: `iguales`
   - por qué: El signo «¡» sustituye a la letra inicial: el OCR lee una «i» minúscula de inicio de palabra como el signo de exclamación de apertura. La palabra reparada es la única lectura posible en el contexto y está atestiguada 28 veces en el corpus. Familia de 44 ocurrencias en 40 filas, presente en el virgen; hallada en §75.

### `RPM-2009-02-12:2356:2` — José De Gregorio Rebeco

1. **PALABRA_PARTIDA**
   - antes: `De Gregario, frente al planteam iento del Consejero s`
   - después: `De Gregorio, frente al planteamiento del Consejero s`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 162 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA. Extensión del §55: el tramo original empezaba en «Gregario,» y dejaba fuera el «De » que lo precede, de modo que no había forma de corregir el apellido sin solaparse. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre la misma persona, José De Gregorio Rebeco.
2. **ESPACIO_INDEBIDO**
   - antes: `le prestan , en consec`
   - después: `le prestan, en consec`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **LETRA_CONFUNDIDA**
   - antes: `se/ection`
   - después: `selection`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene selection y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.

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

### `RPM-2009-11-12:2776:7` — Andrés Velasco Brañes

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2006-06-15:688:1` — Vittorio Corbo Lioi

1. **LETRA_CONFUNDIDA**
   - antes: `rio Corbo en relación ai precio del cobre, que`
   - después: `rio Corbo en relación al precio del cobre, que`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2012-10-18:5102:1` — Sergio Lehmann Beresi

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.
2. **ACENTO_INDEBIDO**
   - antes: `Asía`
   - después: `Asia`
   - por qué: Acento indebido. Medido en el corpus: «Asia» aparece 327 veces y «Asía» 3, siempre «Asia emergente» o «Asia y Oceanía». El topónimo no lleva acento.

### `RPM-2007-07-12:1316:2` — Sergio Lehmann Beresi

1. **SALTOS_DE_LINEA**
   - antes: ` reales del mercado inmobiliari o. Estima que tod`
   - después: ` reales del mercado inmobiliario. Estima que tod`
   - por qué: Palabra partida por la justificación del PDF ("inmobiliari o"). La palabra es inequívoca y está atestiguada en el corpus; en la misma fila aparece varias veces completa.

### `RPM-2010-05-13:3126:1` — José De Gregorio Rebeco

1. **PALABRA_PARTIDA**
   - antes: `riendo espacio para em pezar el proceso de n`
   - después: `riendo espacio para empezar el proceso de n`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 33 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2015-02-12:6629:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2009-06-16:2597:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: ` plazo que no sea compensado por movimientos cambíanos; o, simplemente, una recuperación más rápida`
   - después: ` plazo que no sea compensado por movimientos cambiarios; o, simplemente, una recuperación más rápida`
   - por qué: «cambíanos» no es palabra del español; el adjetivo de «cambio» es «cambiario». Los 18 casos del corpus están todos en el mismo contexto —«mercados financieros y cambíanos», «efectos cambíanos», «desalineamientos cambíanos», «ajustes cambíanos»— y en ninguno cabe otra lectura. El corpus tiene 55 «cambiarios» correctos. La «ri» se leyó como «n».

### `RPM-2008-11-13:2141:2` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarla`
   - después: `cambiaria`
   - por qué: cambiarla por cambiaria. Misma familia y mismo defecto. Medido: 8 apariciones (todas dentro de "cambiarlas"), todas adjetivas y revisadas una por una: "paridades cambiarlas" 4 veces, "implicancias cambiarlas" 2, "expectativas cambiarlas" 1, "coberturas cambiarlas" 1. "cambiarias" ya aparece 19 veces en el corpus.

### `RPM-2010-04-15:3024:1` — José De Gregorio Rebeco

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

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

### `RPM-2007-02-08:1068:1` — Jorge Desormeaux Jiménez

1. **LETRA_CONFUNDIDA**
   - antes: ` proyecciones del Consesus Forecast o JP Mor`
   - después: ` proyecciones del Consensus Forecast o JP Mor`
   - por qué: Consesus por Consensus: falta una n. Medido: "Consensus" aparece 127 veces en 99 filas y "Consesus" 8 veces en 6, siempre en el nombre propio "Consensus Forecast". No hay lectura alternativa.
2. **LETRA_CONFUNDIDA**
   - antes: `n de depreciación de! yuan en un 10% `
   - después: `n de depreciación del yuan en un 10% `
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2011-01-13:3711:1` — Rodrigo Vergara Montes

1. **ESPACIO_INDEBIDO**
   - antes: `oce meses— , así como `
   - después: `oce meses—, así como `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **ACENTO_INDEBIDO**
   - antes: `a como Chile, donde hay una serie de precios que sé indexan rápidamente al tipo de cambio, como es e`
   - después: `a como Chile, donde hay una serie de precios que se indexan rápidamente al tipo de cambio, como es e`
   - por qué: Tilde indebidamente agregada al pronombre: «una serie de precios que sé indexan rápidamente al tipo de cambio». «sé» acentuado es el verbo saber o el imperativo de ser; aquí es el pronombre reflexivo «se». En todo el corpus hay solo dos «sé» acentuados y el otro es legítimo («per sé», RPM-2009-03-12:2430:1), así que este es el único caso dañado.

### `RPM-2014-04-17:6115:1` — Consejo del Banco Central de Chile

1. **ESPACIO_INDEBIDO**
   - antes: `ña Poblete ; Gerente d`
   - después: `ña Poblete; Gerente d`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2008-05-08:1847:1` — Jorge Desormeaux Jiménez

1. **SIMBOLO_SUELTO**
   - antes: `una dirección u otra. U U) Menciona`
   - después: `una dirección u otra. Menciona`
   - por qué: Dos residuos seguidos, "U" y "U)": la regla general de letra suelta solo quitaria el primero y dejaria "U) Menciona". Se eliminan los dos en una sola operacion porque son adyacentes y forman un unico bloque de ruido entre las dos oraciones.

### `RPM-2014-03-13:6057:1` — Consejo del Banco Central de Chile

1. **ESPACIO_INDEBIDO**
   - antes: `ña Poblete ; Gerente d`
   - después: `ña Poblete; Gerente d`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **LETRA_CONFUNDIDA**
   - antes: ` ei`
   - después: ` el`
   - por qué: «ei» en lugar del artículo «el»: el OCR confunde la «l» con la «i». Sigue un sustantivo masculino, así que no hay otra lectura. Familia de 14 ocurrencias en 13 filas del corpus. §75.

### `RPM-2010-05-13:3126:2` — Consejo del Banco Central de Chile

1. **PALABRA_PARTIDA**
   - antes: `T a s a`
   - después: `Tasa`
   - por qué: La palabra «Tasa» de la fórmula del Acuerdo está deletreada con espacios internos. Medido en el corpus: «-Tasa de Política» aparece bien escrita 119 veces y «T a s a» 9, siempre en la misma posición de la fórmula («el Consejo adopta el siguiente Acuerdo: <número>-Tasa de Política Monetaria»). Es el mismo defecto que el pase del §36 corrigió en la variante «T a sa» de 6 actas; ésta es la variante con las cuatro letras separadas. La posición es fija y no hay lectura alternativa: el número de acuerdo va pegado a la palabra.

### `RPM-2006-05-11:659:1` — Esteban Jadresic Marinovic

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2009-10-13:2725:5` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.

### `RPM-2009-03-12:2436:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `/PoM`
   - después: `IPoM`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene IPoM y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.

### `RPM-2006-12-14:1001:1` — Rodrigo Valdés Pulido

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2011-06-14:4064:1` — Luis Óscar Herrera Barriga

1. **RESIDUO_PAGINACION**
   - antes: `amente. -4 . f . • " ' A)`
   - después: `amente.`
   - por qué: §70: se extiende la operación existente, que sólo había arreglado el espaciado DENTRO del residuo ('-4 . f . • " \' A)' -> '-4. f. • " \' A)') sin borrarlo. Lo que sigue al punto que cierra la oración no pertenece al texto: es el pie de página del PDF que el OCR capturó al terminar la página. La oración anterior está completa, así que borrarlo no quita nada del acta. El Tipo pasa a RESIDUO_PAGINACION porque ese es ahora el arreglo.

### `RPM-2010-08-12:3315:2` — Claudio Soto Gamboa

1. **ESPACIO_INDEBIDO**
   - antes: ` por tanto , permite c`
   - después: ` por tanto, permite c`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **ESPACIO_INDEBIDO**
   - antes: `ón pública . De acuerd`
   - después: `ón pública. De acuerd`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: `so extremo , se podría`
   - después: `so extremo, se podría`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
4. **LETRA_CONFUNDIDA**
   - antes: `Claudia Soto`
   - después: `Claudio Soto`
   - por qué: La «a» final ocupó el lugar de la «o» en el nombre de pila. El propio texto lo descarta: la fila lo trata en masculino («señor» o «don») y el corpus atestigua «Claudio Soto» 1.275 veces contra 2 «Claudia Soto». No es la Claudia legítima del corpus (doña Claudia Varela Lértora, doña Claudia Sotz Pantoja), que siempre va con «doña» o «Gerenta».

### `RPM-2012-07-12:4945:1` — Manuel Marfán Lewis

1. **ACENTO_FALTANTE**
   - antes: `ítica monetaria, la referida política seria ahora menos exp`
   - después: `ítica monetaria, la referida política sería ahora menos exp`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.

### `RPM-2014-10-16:6441:2` — Miguel Ricaurte Bermúdez

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2010-06-15:3131:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.

### `RPM-2010-03-18:3011:1` — Pablo García Silva

1. **PALABRA_ERRONEA**
   - antes: `s, hace presente que en el ámbito externo se ha observada que la volatilidad financiera se ha aplacado`
   - después: `s, hace presente que en el ámbito externo se ha observado que la volatilidad financiera se ha aplacado`
   - por qué: Participio mal concordado: «en el ámbito externo se ha observada que la volatilidad financiera se ha aplacado». Con el auxiliar «ha» el participio es invariable, y además el sujeto de la oración es la cláusula «que la volatilidad… se ha aplacado», no un sustantivo femenino. El corpus tiene 221 «ha observado» y este es el único «ha observada» de las 9.724 filas.
