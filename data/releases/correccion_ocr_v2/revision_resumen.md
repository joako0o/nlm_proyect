# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1722**
- operaciones: **2951**
- filas marcadas para cotejo: **217**
- sha256 de la base: `eebaa728dc1d7ce14315caebd0c7516ff324b5d4acaefcf40cec2bf6d855945d`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 690 |
| `ESPACIO_INDEBIDO` | 510 |
| `PALABRA_PARTIDA` | 491 |
| `ACENTO_INDEBIDO` | 385 |
| `PUNTUACION` | 267 |
| `ACENTO_FALTANTE` | 216 |
| `SIMBOLO_SUELTO` | 212 |
| `FIRMA_TRUNCADA` | 55 |
| `PALABRA_ERRONEA` | 30 |
| `RESIDUO_PAGINACION` | 30 |
| `ESPACIO_FALTANTE` | 27 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |
| `PALABRA_DUPLICADA` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2015-07-14:6904:1` — Alberto Naudon Dell'Oro

1. **LETRA_CONFUNDIDA**
   - antes: `adosos en el uso de ios adjetivos. En m`
   - después: `adosos en el uso de los adjetivos. En m`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.
2. **LETRA_CONFUNDIDA**
   - antes: `ral cuestionarse si ios supuestos utili`
   - después: `ral cuestionarse si los supuestos utili`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2011-12-13:4514:1` — Consejo del Banco Central de Chile

1. **LETRA_CONFUNDIDA**
   - antes: `TPÍ\/I`
   - después: `TPM`
   - por qué: La OCR escribe la «M» como una secuencia de glifos con barra invertida. El corpus tiene «TPM» 1822 veces y no tiene ninguna forma legítima con esa secuencia.

### `RPM-2009-03-12:2402:1` — Claudio Soto Gamboa

1. **PUNTUACION**
   - antes: `"mucho"`
   - después: `“mucho”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.
2. **ESPACIO_INDEBIDO**
   - antes: `de febrero . De otro l`
   - después: `de febrero. De otro l`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: `de febrero . En cuanto`
   - después: `de febrero. En cuanto`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
4. **LETRA_CONFUNDIDA**
   - antes: `Claudia Soto`
   - después: `Claudio Soto`
   - por qué: La «a» final ocupó el lugar de la «o» en el nombre de pila. El propio texto lo descarta: la fila lo trata en masculino («señor» o «don») y el corpus atestigua «Claudio Soto» 1.275 veces contra 1 «Claudia Soto». No es la Claudia legítima del corpus (doña Claudia Varela Lértora, doña Claudia Sotz Pantoja), que siempre va con «doña» o «Gerenta».

### `RPM-2005-03-10:171:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `m antener`
   - después: `mantener`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 1788 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2010-01-14:2847:1` — Sergio Lehmann Beresi

1. **ESPACIO_INDEBIDO**
   - antes: `de dólares , luego exp`
   - después: `de dólares, luego exp`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **SIMBOLO_SUELTO**
   - antes: `por componentes el'f comportamiento ha sido`
   - después: `por componentes el comportamiento ha sido`
   - por qué: Un apóstrofo y una «f» suelta se intercalaron entre el artículo y el sustantivo: «el'f comportamiento» por «el comportamiento». La oración sigue con «ha sido algo más heterogéneo, con maíz y trigo subiendo», que sólo admite ese sujeto.

### `RPM-2006-07-13:752:1` — Enrique Marshall Rivera

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2013-02-14:5395:1` — Manuel Marfán Lewis

1. **SIMBOLO_SUELTO**
   - antes: `persiste un crecimiento q.ue de acuerdo con`
   - después: `persiste un crecimiento que de acuerdo con`
   - por qué: Punto insertado dentro de la palabra: «q.ue» no existe y la única lectura es «que», que además es lo que pide la construcción «un crecimiento que, de acuerdo con la información disponible, no es sostenible».

### `RPM-2007-08-09:1363:1` — Pablo García Silva

1. **PALABRA_PARTIDA**
   - antes: `tem a`
   - después: `tema`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 784 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.

### `RPM-2010-07-15:3243:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `De Gregario`
   - después: `De Gregorio`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).
2. **LETRA_CONFUNDIDA**
   - antes: `Claudia Soto`
   - después: `Claudio Soto`
   - por qué: La «a» final ocupó el lugar de la «o» en el nombre de pila. El propio texto lo descarta: la fila lo trata en masculino («señor» o «don») y el corpus atestigua «Claudio Soto» 1.275 veces contra 1 «Claudia Soto». No es la Claudia legítima del corpus (doña Claudia Varela Lértora, doña Claudia Sotz Pantoja), que siempre va con «doña» o «Gerenta».

### `RPM-2015-08-13:6952:1` — Miguel Fuentes Díaz

1. **SIMBOLO_SUELTO**
   - antes: `con la positiva en servicios. , . . , Anaí ? ! £ , Ias medldas de inflación subyacente permanecen elevadas`
   - después: `con la positiva en servicios. Las medidas de inflación subyacente permanecen elevadas`
   - por qué: RESIDUO Y DOS PALABRAS DAÑADAS EN EL MISMO TRAMO, corregidos juntos porque se pisarían si se separaran. Entre dos oraciones hay una cadena de glifos que no forma nada (coma, punto, punto, coma, 'Anaí', interrogación, exclamación, signo de libra, coma; verificados por codepoint: 0x2c 0x2e 0x2e 0x2c 0x41 0x6e 0x61 0xed 0x3f 0x21 0xa3 0x2c) y a continuación 'Ias medldas' por 'Las medidas', con i mayúscula por ele y ele por i. MEDIDO: 'Anaí' aparece 1 sola vez en todo el corpus, 'medldas' 1 e 'Ias ' 1, así que no hay otro uso que proteja la cadena; y 'Las medidas' aparece 54 veces. La oración siguiente ya empieza con mayúscula implícita y no se repone ningún signo.
2. **PALABRA_PARTIDA**
   - antes: `Resalta que su com portam iento ha mostrado bastante estabilidad en doce meses`
   - después: `Resalta que su comportamiento ha mostrado bastante estabilidad en doce meses`
   - por qué: Una sola palabra partida por DOS espacios: 'com portam iento' por 'comportamiento'. Se reúne sin alterar una letra, sección 1 ter.
3. **PALABRA_PARTIDA**
   - antes: `informa que se ha corregido en form a importante al alza, situándose en 4,5% a diciembre`
   - después: `informa que se ha corregido en forma importante al alza, situándose en 4,5% a diciembre`
   - por qué: Palabra partida: 'form a' por 'forma'. Sección 1 ter, se reúne sin alterar una letra.
4. **PALABRA_PARTIDA**
   - antes: `en enero de 2016, registraría una variación m ensual de 0,5%`
   - después: `en enero de 2016, registraría una variación mensual de 0,5%`
   - por qué: Palabra partida: 'm ensual' por 'mensual'. Sección 1 ter.
5. **PALABRA_PARTIDA**
   - antes: `por la entrada en vigencia de las modificaciones a la Ley sobre Im puesto de Timbres y Estampillas`
   - después: `por la entrada en vigencia de las modificaciones a la Ley sobre Impuesto de Timbres y Estampillas`
   - por qué: Palabra partida: 'Im puesto' por 'Impuesto'. Sección 1 ter. Es el nombre de una ley, pero la reparación no toca la identidad del nombre: sólo reúne las letras que ya están.
6. **PALABRA_PARTIDA**
   - antes: `si bien las brechas de actividad han sido menores, la evolución del tipo de cam bio plantea un riesgo`
   - después: `si bien las brechas de actividad han sido menores, la evolución del tipo de cambio plantea un riesgo`
   - por qué: Palabra partida: 'cam bio' por 'cambio'. Sección 1 ter.
7. **LETRA_CONFUNDIDA**
   - antes: `llevaría al IPC en doce meses a 4,9% y ai IPCSAE a 4,4%`
   - después: `llevaría al IPC en doce meses a 4,9% y al IPCSAE a 4,4%`
   - por qué: 'ai' no es palabra: es 'al' con la ele leída como i. La oración no admite otra lectura y el paralelo inmediato lo confirma, porque la misma frase acaba de decir 'llevaría al IPC'. Medido: 'al IPCSAE' aparece 2 veces en el corpus y 'ai IPCSAE' 1. Sección 2 bis: la forma defectuosa no es palabra, así que no hay lectura alternativa que proteger.
8. **ACENTO_FALTANTE**
   - antes: `las expectativas de inflación a uno y dos anos medidas por la Encuesta de Expectativas Económicas`
   - después: `las expectativas de inflación a uno y dos años medidas por la Encuesta de Expectativas Económicas`
   - por qué: Falta la tilde de la eñe: 'anos' por 'años'. Sección 1, la oración no admite otra lectura. Medido: 'años' aparece 1.543 veces en el corpus y ' anos ' con espacios 1 sola.
9. **LETRA_CONFUNDIDA**
   - antes: `señala que la depreciación cambiaría ha sido mayor que la sugerida por los fundamentos`
   - después: `señala que la depreciación cambiaria ha sido mayor que la sugerida por los fundamentos`
   - por qué: Tilde o ele por i en posición de adjetivo. La sección 3 ter manda corregir estas formas por muchas veces que se repitan, porque 'cambiaría'/'cambiarlas' son formas verbales y en este lugar sólo cabe el adjetivo. No se pide corroboración en la fila ni en la sesión para esta familia.
10. **LETRA_CONFUNDIDA**
   - antes: `que han coincidido con eventos de intervención cambiaría en particular el anuncio de intervención en el año 2011`
   - después: `que han coincidido con eventos de intervención cambiaria en particular el anuncio de intervención en el año 2011`
   - por qué: Tilde o ele por i en posición de adjetivo. La sección 3 ter manda corregir estas formas por muchas veces que se repitan, porque 'cambiaría'/'cambiarlas' son formas verbales y en este lugar sólo cabe el adjetivo. No se pide corroboración en la fila ni en la sesión para esta familia. Falta además una coma antes de 'en particular', pero la sección 7 prohíbe reponer un signo y queda documentada en la marca de esta misma fila.

### `RPM-2009-08-13:2678:1` — Pablo García Silva

1. **ACENTO_FALTANTE**
   - antes: `que la que el Banco tenia el mes pasado, `
   - después: `que la que el Banco tenía el mes pasado, `
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2008-12-11:2219:2` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `De Gregario`
   - después: `De Gregorio`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).

### `RPM-2010-06-15:3131:2` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `e alguna manera, en ios mercados americ`
   - después: `e alguna manera, en los mercados americ`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2008-05-08:1798:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `i1iquidez`
   - después: `iliquidez`
   - por qué: i1iquidez por iliquidez: la l se leyo como el digito 1. Medido: "iliquidez" aparece 10 veces y "i1iquidez" una sola.

### `RPM-2007-02-08:1102:2` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `siguiente Acuerdo;`
   - después: `siguiente Acuerdo:`
   - por qué: Pase transversal. La fórmula del Acuerdo es «el Consejo adopta/adoptó el siguiente Acuerdo: NNN-NN-NNMMDD - Tasa de Política Monetaria»: los dos puntos introducen el acuerdo enumerado, y un punto y coma no puede hacer eso. Medido en las 9.724 filas: la fórmula aparece 118 veces, 106 con dos puntos y 12 con punto y coma, y las 12 son estructuralmente idénticas a las otras —mismo número de acuerdo y mismo título a continuación—. El punto y coma es una lectura de OCR del dos puntos. Se corrigieron las 12 (2005-01-11, 2005-10-11, 2006-08-10, 2006-12-14, 2007-02-08, 2007-04-12, 2007-05-10, 2007-06-14, 2009-09-08, 2010-09-16, 2011-02-17, 2015-01-15). Es la misma evidencia que en §39 para «Siendo las 16; 15 horas» -> «16:15», donde también había 106 apariciones con dos puntos. Texto queda intacto.

### `RPM-2011-05-12:3986:1` — José De Gregorio Rebeco

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2014-09-11:6434:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2008-07-10:1915:1` — José De Gregorio Rebeco

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2014-07-15:6331:2` — Alejandro Micco

1. **SIMBOLO_SUELTO**
   - antes: `e año. í j .`
   - después: `e año.`
   - por qué: La operación quitaba sólo el espacio entre la jota y el punto, y dejaba «e año. í j.»: una í con acento y una jota sueltas tras el punto de cierre. No tienen lectura posible y no falta texto, la oración está completa, así que se elimina la basura y el tipo pasa de ESPACIO_INDEBIDO a SIMBOLO_SUELTO porque ahora la operación quita letras y no sólo un blanco.
2. **SIMBOLO_SUELTO**
   - antes: `debiese ' situarse`
   - después: `debiese situarse`
   - por qué: Apóstrofo suelto en mitad de la cláusula: «la tasa de política debiese situarse en torno a 75 puntos base». El apóstrofo no tiene lectura en español en esa posición y no separa dos oraciones, así que no puede ser marca de párrafo ni comilla. Tipo SIMBOLO_SUELTO, igual que los residuos de §25.

### `RPM-2010-07-15:3244:1` — Claudio Soto Gamboa

1. **ESPACIO_INDEBIDO**
   - antes: `ublicación , lo que so`
   - después: `ublicación, lo que so`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **ESPACIO_INDEBIDO**
   - antes: `se explica , fundament`
   - después: `se explica, fundament`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: ` y calzado , equipos d`
   - después: ` y calzado, equipos d`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
4. **ESPACIO_INDEBIDO**
   - antes: `s de tasas , llevando `
   - después: `s de tasas, llevando `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2006-06-15:693:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `recio del cobre tenía ai país bastante eufóric`
   - después: `recio del cobre tenía al país bastante eufóric`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2009-11-12:2794:2` — Andrés Velasco Brañes

1. **ACENTO_INDEBIDO**
   - antes: `ión con que hay tal íncertidumbre respecto de lo `
   - después: `ión con que hay tal incertidumbre respecto de lo `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 861 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
2. **ACENTO_FALTANTE**
   - antes: `distinto del que se tenia hace un mes, y `
   - después: `distinto del que se tenía hace un mes, y `
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2009-04-09:2500:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `s bajas de tasas de ios meses anteriore`
   - después: `s bajas de tasas de los meses anteriore`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.
2. **ACENTO_FALTANTE**
   - antes: `lo último que se le podria acusar al Banco`
   - después: `lo último que se le podría acusar al Banco`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2006-12-14:1021:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` )RIO CORBO LIOI Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2011-10-13:4364:2` — Claudio Soto Gamboa

1. **LETRA_CONFUNDIDA**
   - antes: `El señor Claudios Soto responde que hay un debate entre la Cám`
   - después: `El señor Claudio Soto responde que hay un debate entre la Cám`
   - por qué: Normalización de nombre propio dañado, autorizada por el usuario en esta ronda (el criterio anterior era marcar sin corregir). La forma canónica la acreditan el corpus y el roster de la sesión: «Claudio Soto» aparece 1274 veces en la salida, contra 1 de la forma dañada. Se corrige en Texto_Corregido; Texto queda intacto. Lo que no tiene forma canónica atestiguada (por ejemplo «Miguel Angel Nacrur Gazali») sigue marcado NOMBRE_PROPIO_POR_COTEJAR.

### `RPM-2010-10-14:3493:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` JOSÉ DE GREGORIO REBECO Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2013-01-17:5287:1` — Claudio Soto Gamboa

1. **ACENTO_INDEBIDO**
   - antes: `iciones de Créditos Bancaríos del Banco, las `
   - después: `iciones de Créditos bancarios del Banco, las `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 126 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
2. **ACENTO_INDEBIDO**
   - antes: `ones se corrigieran margínalmente a la baja. A tí`
   - después: `ones se corrigieran marginalmente a la baja. A tí`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 282 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
3. **ACENTO_INDEBIDO**
   - antes: `n el mercado espera mayorítariamente la mantenc`
   - después: `n el mercado espera mayoritariamente la mantenc`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 195 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
4. **ACENTO_INDEBIDO**
   - antes: `cimiento del IMACEC desestacíonalizado registró una te`
   - después: `cimiento del IMACEC desestacionalizado registró una te`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 108 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
5. **ACENTO_FALTANTE**
   - antes: `timo IPoM, y que la demanda interna seria algo menor por `
   - después: `timo IPoM, y que la demanda interna sería algo menor por `
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.

### `RPM-2015-06-11:6821:1` — Diego Gianelli Gómez

1. **LETRA_CONFUNDIDA**
   - antes: `esgo han presionado ios precios de acti`
   - después: `esgo han presionado los precios de acti`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2010-07-15:3249:2` — Claudio Soto Gamboa

1. **ESPACIO_INDEBIDO**
   - antes: `ra el 2010 . Con ello,`
   - después: `ra el 2010. Con ello,`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2010-05-13:3116:1` — Beltrán de Ramón Acevedo

1. **PUNTUACION**
   - antes: `ue.`
   - después: `ue,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.
