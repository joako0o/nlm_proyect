# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1734**
- operaciones: **2980**
- filas marcadas para cotejo: **218**
- sha256 de la base: `eebaa728dc1d7ce14315caebd0c7516ff324b5d4acaefcf40cec2bf6d855945d`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 691 |
| `ESPACIO_INDEBIDO` | 510 |
| `PALABRA_PARTIDA` | 491 |
| `ACENTO_INDEBIDO` | 385 |
| `PUNTUACION` | 267 |
| `SIMBOLO_SUELTO` | 239 |
| `ACENTO_FALTANTE` | 217 |
| `FIRMA_TRUNCADA` | 55 |
| `PALABRA_ERRONEA` | 30 |
| `RESIDUO_PAGINACION` | 30 |
| `ESPACIO_FALTANTE` | 27 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |
| `PALABRA_DUPLICADA` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2015-06-11:6861:1` — Enrique Marshall Rivera

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2011-11-15:4455:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `prendieron en algo a! alza. Más allá `
   - después: `prendieron en algo al alza. Más allá `
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2009-03-12:2397:1` — Sebastián Claro Edwards

1. **PALABRA_PARTIDA**
   - antes: `si ese escenario de crecim iento mundial que pla`
   - después: `si ese escenario de crecimiento mundial que pla`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 5699 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2005-03-10:171:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `m antener`
   - después: `mantener`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 1788 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2009-12-15:2821:1` — Claudio Soto Gamboa

1. **ACENTO_INDEBIDO**
   - antes: `dose a los spreads, índica que se ha hecho`
   - después: `dose a los spreads, indica que se ha hecho`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2006-07-13:752:1` — Enrique Marshall Rivera

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2013-02-14:5335:1` — Rodrigo Vergara Montes

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2007-08-09:1357:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: ` Indica que el efecto fiy to quality, llevó a una `
   - después: ` Indica que el efecto fly to quality, llevó a una `
   - por qué: "fiy"/"fIy" por "fly": la l se leyo como i (o como I). Es el mismo glifo que produce "ai" por "al", demostrado con 26 casos independientes. Se retira la marca RECONSTRUCCION_AMBIGUA que se había puesto en esta fila: al aparecer la regla de glifo, la ambigüedad se resuelve. Un escáner no convierte "flight" en "fiy" (sería borrar cuatro letras); sí convierte "fly" en "fiy". Las 21 apariciones de "flight to quality" que hay en el corpus son la otra grafía, correcta, y no se tocan.
2. **LETRA_CONFUNDIDA**
   - antes: `e producto del efecto fiy to quality y turbulencia`
   - después: `e producto del efecto fly to quality y turbulencia`
   - por qué: "fiy"/"fIy" por "fly": la l se leyo como i (o como I). Es el mismo glifo que produce "ai" por "al", demostrado con 26 casos independientes. Se retira la marca RECONSTRUCCION_AMBIGUA que se había puesto en esta fila: al aparecer la regla de glifo, la ambigüedad se resuelve. Un escáner no convierte "flight" en "fiy" (sería borrar cuatro letras); sí convierte "fly" en "fiy". Las 21 apariciones de "flight to quality" que hay en el corpus son la otra grafía, correcta, y no se tocan.
3. **PALABRA_PARTIDA**
   - antes: `o, en la demanda de com bustible y eso lo ha lle`
   - después: `o, en la demanda de combustible y eso lo ha lle`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 51 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
4. **PALABRA_PARTIDA**
   - antes: `rve en las próximas sem anas, probablemente `
   - después: `rve en las próximas semanas, probablemente `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 609 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
5. **PALABRA_PARTIDA**
   - antes: ` Lehmann indica que é ste ha continuado p`
   - después: ` Lehmann indica que éste ha continuado p`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 224 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
6. **PALABRA_PARTIDA**
   - antes: `ia el alza, pero no so n cambios demasia`
   - después: `ia el alza, pero no son cambios demasia`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2973 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
7. **PALABRA_PARTIDA**
   - antes: ` hacia el próximo a U S $ 71. Agrega el`
   - después: ` hacia el próximo a US $ 71. Agrega el`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 685 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
8. **PALABRA_PARTIDA**
   - antes: `finación en Estados U nidos de América. Por`
   - después: `finación en Estados Unidos de América. Por`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2781 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
9. **ACENTO_INDEBIDO**
   - antes: `eferirse a precios, índica que la informac`
   - después: `eferirse a precios, indica que la informac`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
10. **ESPACIO_INDEBIDO**
   - antes: `m a rg e n , también m`
   - después: `m a rg e n, también m`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
11. **LETRA_CONFUNDIDA**
   - antes: `obsen/ó`
   - después: `observó`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene observó y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.
12. **PALABRA_PARTIDA**
   - antes: `m ostrando`
   - después: `mostrando`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 509 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
13. **PALABRA_PARTIDA**
   - antes: `m antención`
   - después: `mantención`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 510 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
14. **PALABRA_PARTIDA**
   - antes: `m ejorado`
   - después: `mejorado`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 101 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
15. **PALABRA_PARTIDA**
   - antes: `m aíz`
   - después: `maíz`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 130 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
16. **PALABRA_PARTIDA**
   - antes: `m anteniendo`
   - después: `manteniendo`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 84 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
17. **PALABRA_PARTIDA**
   - antes: `n o tic ia s`
   - después: `noticias`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 944 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
18. **PALABRA_PARTIDA**
   - antes: `s o b re`
   - después: `sobre`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 4493 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
19. **PALABRA_PARTIDA**
   - antes: `c a y e n d o`
   - después: `cayendo`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 239 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
20. **PALABRA_PARTIDA**
   - antes: `e sp e ra ría`
   - después: `esperaría`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 33 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
21. **PALABRA_PARTIDA**
   - antes: `T a m b ié n`
   - después: `También`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 4809 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
22. **PALABRA_PARTIDA**
   - antes: `c o rre g ir`
   - después: `corregir`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 121 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
23. **PALABRA_PARTIDA**
   - antes: `C o m isió n`
   - después: `Comisión`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 26 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
24. **PALABRA_PARTIDA**
   - antes: `q u e`
   - después: `que`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 100805 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
25. **PALABRA_PARTIDA**
   - antes: `a lz a`
   - después: `alza`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 2951 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
26. **PALABRA_PARTIDA**
   - antes: `v o lv ió`
   - después: `volvió`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 134 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
27. **PALABRA_PARTIDA**
   - antes: `d e riv a d o`
   - después: `derivado`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 55 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
28. **PALABRA_PARTIDA**
   - antes: `en to rn o`
   - después: `entorno`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 226 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
29. **PALABRA_PARTIDA**
   - antes: `d e m an da`
   - después: `demanda`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 2855 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
30. **PALABRA_PARTIDA**
   - antes: `e s te`
   - después: `este`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 5944 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
31. **PALABRA_PARTIDA**
   - antes: `ha sta`
   - después: `hasta`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 1512 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.
32. **ACENTO_INDEBIDO**
   - antes: `hacía`
   - después: `hacia`
   - por qué: Pase transversal, enumeración completa. De las 32 apariciones de «hacía» en el corpus, 17 son el verbo («hacía presente», «hacía referencia», «hacía mención», «hacía necesario», «lo hacía moderadamente»…) y 15 son la preposición «hacia» con tilde indebidamente puesta: siempre rigen un complemento de dirección o destino («hacía delante», «hacía adelante», «hacía la baja», «hacía América Latina», «hacía las economías emergentes», «hacía el tercer trimestre»). En esas 15 el verbo no tiene sujeto ni complemento posible. Se corrigieron las 15 y se dejaron las 17; el suelo de la guardia de regresión bajó de 32 a 17 con la enumeración documentada en el test, no en silencio. «hacia» aparece 2.183 veces.

### `RPM-2010-07-15:3227:2` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `do en períodos post recesíón.`
   - después: `do en períodos post recesión.`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 222 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
2. **ESPACIO_INDEBIDO**
   - antes: `ctivamente , a un crec`
   - después: `ctivamente, a un crec`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: `va Federal , sino que `
   - después: `va Federal, sino que `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
4. **SIMBOLO_SUELTO**
   - antes: `r crecimiento para el año 2010 Y algo menos para el 2011, así`
   - después: `r crecimiento para el año 2010 y algo menos para el 2011, así`
   - por qué: Conjunción «y» leída como mayúscula por el OCR. El corpus la escribe en minúscula; se excluyó el único caso legítimo, «el eje Y» (RPM-2012-09-13:5049:1), donde la mayúscula nombra el eje.

### `RPM-2015-08-13:6923:1` — Sebastián Claro Edwards

1. **PALABRA_OMITIDA**
   - antes: `en términos de los precios de commodities y de las condiciones financiera.`
   - después: `en términos de los precios de commodities y de las condiciones financieras.`
   - por qué: Falta la ese del plural: 'las condiciones financiera' no concuerda y no hay otra lectura. Corroborada donde el criterio exige: 'condiciones financieras' aparece 3 veces en esta misma sesión y 571 en el corpus.

### `RPM-2009-08-13:2666:3` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.
2. **ACENTO_INDEBIDO**
   - antes: `hacía`
   - después: `hacia`
   - por qué: Pase transversal, enumeración completa. De las 32 apariciones de «hacía» en el corpus, 17 son el verbo («hacía presente», «hacía referencia», «hacía mención», «hacía necesario», «lo hacía moderadamente»…) y 15 son la preposición «hacia» con tilde indebidamente puesta: siempre rigen un complemento de dirección o destino («hacía delante», «hacía adelante», «hacía la baja», «hacía América Latina», «hacía las economías emergentes», «hacía el tercer trimestre»). En esas 15 el verbo no tiene sujeto ni complemento posible. Se corrigieron las 15 y se dejaron las 17; el suelo de la guardia de regresión bajó de 32 a 17 con la enumeración documentada en el test, no en silencio. «hacia» aparece 2.183 veces.

### `RPM-2008-12-11:2203:1` — José De Gregorio Rebeco

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2010-05-13:3110:1` — Consejo del Banco Central de Chile

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2008-05-08:1793:3` — Jorge Desormeaux Jiménez

1. **PALABRA_PARTIDA**
   - antes: `relativizar un poco est os datos, el creci`
   - después: `relativizar un poco estos datos, el creci`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 1383 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
2. **PALABRA_PARTIDA**
   - antes: `El Vicepres idente señor Jorge Des`
   - después: `El Vicepresidente señor Jorge Des`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 1472 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2007-02-08:1102:2` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `siguiente Acuerdo;`
   - después: `siguiente Acuerdo:`
   - por qué: Pase transversal. La fórmula del Acuerdo es «el Consejo adopta/adoptó el siguiente Acuerdo: NNN-NN-NNMMDD - Tasa de Política Monetaria»: los dos puntos introducen el acuerdo enumerado, y un punto y coma no puede hacer eso. Medido en las 9.724 filas: la fórmula aparece 118 veces, 106 con dos puntos y 12 con punto y coma, y las 12 son estructuralmente idénticas a las otras —mismo número de acuerdo y mismo título a continuación—. El punto y coma es una lectura de OCR del dos puntos. Se corrigieron las 12 (2005-01-11, 2005-10-11, 2006-08-10, 2006-12-14, 2007-02-08, 2007-04-12, 2007-05-10, 2007-06-14, 2009-09-08, 2010-09-16, 2011-02-17, 2015-01-15). Es la misma evidencia que en §39 para «Siendo las 16; 15 horas» -> «16:15», donde también había 106 apariciones con dos puntos. Texto queda intacto.

### `RPM-2011-03-17:3889:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `"alerta inflacionaria"`
   - después: `“alerta inflacionaria”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.
2. **PUNTUACION**
   - antes: `"emergencia inflacionaria"`
   - después: `“emergencia inflacionaria”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.

### `RPM-2014-08-14:6389:4` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2008-06-10:1904:1` — Beltrán de Ramón Acevedo

1. **SIMBOLO_SUELTO**
   - antes: `n Estudios y de los seguros de inflación. ■J`
   - después: `n Estudios y de los seguros de inflación.`
   - por qué: Símbolo ■ con basura adyacente, residuo del escaneo. El tipo SIMBOLO_SUELTO fue creado justamente para estos casos («■V», «ry _<< ■» -> se elimina). Medido: 21 apariciones en 20 filas. Se trata cada una con su basura propia porque el ruido que la acompaña varía (■o J, ■,\y, ■', ■J, ■V, / ■ ' /, 4 / ■, i - /■, — f ■, ry _<< ■). En todos los casos las dos oraciones que rodean el residuo quedan completas sin él. Excepción: en 5802:2 se elimina solo el ■ y se deja el paréntesis abierto, porque esa fila ya está marcada RECONSTRUCCION_AMBIGUA_POR_COTEJAR con motivo FINAL_SIN_PUNTUACION.

### `RPM-2014-06-12:6282:1` — Beltrán de Ramón Acevedo

1. **SIMBOLO_SUELTO**
   - antes: `producirán .las caídas`
   - después: `producirán las caídas`
   - por qué: Enmienda de la operación del §18, que había quitado sólo el espacio y dejado «producirán.las». El punto es espurio, no un fin de oración: sigue «las caídas de las tasas de interés en el mercado de préstamos a que se hizo mención, así como la compresión de spreads a plazos más largos», que es continuación y no oración nueva, y «las» va en minúscula. Se quitan el espacio y el punto en la misma operación porque ambos caen dentro del mismo tramo del texto virgen; apilar una segunda operación habría dejado dos tramos solapados sin orden de aplicación posible (§15). Por eso cambia también el Tipo: ya no es sólo un espacio indebido.

### `RPM-2010-07-15:3228:1` — Sergio Lehmann Beresi

1. **ESPACIO_INDEBIDO**
   - antes: ` generales , de acuerd`
   - después: ` generales, de acuerd`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2006-06-15:693:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `recio del cobre tenía ai país bastante eufóric`
   - después: `recio del cobre tenía al país bastante eufóric`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2009-11-12:2776:7` — Andrés Velasco Brañes

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2009-04-09:2492:1` — Luis Felipe Céspedes Cifuentes

1. **ACENTO_FALTANTE**
   - antes: `ivo que el esperado anteriormente, seria dar una señal d`
   - después: `ivo que el esperado anteriormente, sería dar una señal d`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.

### `RPM-2006-12-14:1021:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` )RIO CORBO LIOI Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2011-10-13:4336:1` — Sergio Lehmann Beresi

1. **PALABRA_SOBRANTE**
   - antes: `salidas de bonos y de instrumentos de renta de variable`
   - después: `salidas de bonos y de instrumentos de renta variable`
   - por qué: Preposición intrusa. La misma fila trae la forma correcta párrafos antes: 'también se han registrado salidas de instrumentos de renta variable, en línea con los movimientos de las bolsas'.

### `RPM-2010-10-14:3465:1` — Claudio Soto Gamboa

1. **ACENTO_FALTANTE**
   - antes: `adamente, es decir, en el limite de los rangos de valores de e`
   - después: `adamente, es decir, en el límite de los rangos de valores de e`
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2012-12-13:5241:1` — Beltrán de Ramón Acevedo

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2015-05-14:6793:1` — Alberto Naudon Dell'Oro

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **ESPACIO_INDEBIDO**
   - antes: `e 4% real— , en especi`
   - después: `e 4% real—, en especi`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2010-07-15:3229:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `De Gregario`
   - después: `De Gregorio`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).

### `RPM-2010-05-13:3089:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `De Gregario`
   - después: `De Gregorio`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).
