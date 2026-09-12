# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1391**
- operaciones: **2278**
- filas marcadas para cotejo: **195**
- sha256 de la base: `d0b64842cd756df4c50d2960d9bbf01c4c45e5df28609d7b612c5d666593da75`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `ESPACIO_INDEBIDO` | 515 |
| `LETRA_CONFUNDIDA` | 487 |
| `PALABRA_PARTIDA` | 383 |
| `ACENTO_INDEBIDO` | 348 |
| `ACENTO_FALTANTE` | 182 |
| `PUNTUACION` | 106 |
| `SIMBOLO_SUELTO` | 86 |
| `FIRMA_TRUNCADA` | 55 |
| `PALABRA_ERRONEA` | 28 |
| `RESIDUO_PAGINACION` | 27 |
| `ESPACIO_FALTANTE` | 24 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_DUPLICADA` | 3 |
| `PALABRA_SOBRANTE` | 2 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2014-08-14:6388:1` — Enrique Marshall Rivera

1. **ESPACIO_INDEBIDO**
   - antes: `nterior. i .`
   - después: `nterior. i.`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2010-02-11:2951:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `s chilenos que llevan ai movimiento del tipo d`
   - después: `s chilenos que llevan al movimiento del tipo d`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2005-03-10:185:1` — Nicolás Eyzaguirre Guzmán

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarla`
   - después: `cambiaria`
   - por qué: cambiarla por cambiaria. Misma familia y mismo defecto. Medido: 8 apariciones (todas dentro de "cambiarlas"), todas adjetivas y revisadas una por una: "paridades cambiarlas" 4 veces, "implicancias cambiarlas" 2, "expectativas cambiarlas" 1, "coberturas cambiarlas" 1. "cambiarias" ya aparece 19 veces en el corpus.
2. **LETRA_CONFUNDIDA**
   - antes: `ninguna duda cuando ios escucha de que `
   - después: `ninguna duda cuando los escucha de que `
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.
3. **PALABRA_PARTIDA**
   - antes: `íamos en esa época. Adem ás, no tendría nin`
   - después: `íamos en esa época. Además, no tendría nin`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 574 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
4. **PALABRA_PARTIDA**
   - antes: `as de lo que parece afirm ar el Banco y, por`
   - después: `as de lo que parece afirmar el Banco y, por`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 41 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
5. **PALABRA_PARTIDA**
   - antes: `ue han cambiado. En prim er lugar, hoy día `
   - después: `ue han cambiado. En primer lugar, hoy día `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 1739 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
6. **PALABRA_PARTIDA**
   - antes: ` durar, pero hay un am biente general en el m`
   - después: ` durar, pero hay un ambiente general en el m`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 87 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
7. **ACENTO_INDEBIDO**
   - antes: `nomías tienen tasas nomínales más bajas que C`
   - después: `nomías tienen tasas nominales más bajas que C`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 606 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
8. **ESPACIO_INDEBIDO**
   - antes: `otencial y ,por lo tan`
   - después: `otencial y,por lo tan`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
9. **PALABRA_PARTIDA**
   - antes: `m acroeconómica`
   - después: `macroeconómica`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 34 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2011-07-14:4211:1` — Manuel Marfán Lewis

1. **ACENTO_FALTANTE**
   - antes: `a la fecha del 2 de agosto, limite para que pueda eleva`
   - después: `a la fecha del 2 de agosto, límite para que pueda eleva`
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2007-02-08:1076:1` — Igal Magendzo Weinberger

1. **LETRA_CONFUNDIDA**
   - antes: ` cuarto trimestre de! año 2006 tuvo c`
   - después: ` cuarto trimestre del año 2006 tuvo c`
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2015-08-13:6959:1` — Sebastián Claro Edwards

1. **PALABRA_OMITIDA**
   - antes: `Expresa que frente la decisión de hacer explícita o no la preocupación sobre el riesgo de desanclaje`
   - después: `Expresa que frente a la decisión de hacer explícita o no la preocupación sobre el riesgo de desanclaje`
   - por qué: Falta la preposición: 'frente la decisión' no es gramatical y la reparación es única, porque el OCR omite y no agrega palabras. 'frente a la' aparece 110 veces en el corpus. Mismo criterio que 'la mayoría las monedas' (ronda 178) y 'la proyección el PIB' (ronda 179): preposición faltante, cadena agramatical, reparación única.

### `RPM-2008-02-07:1652:2` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.
2. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2013-01-17:5283:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2010-11-16:3494:1` — Consejo del Banco Central de Chile

1. **ESPACIO_FALTANTE**
   - antes: `celebrada el16 de noviembre de`
   - después: `celebrada el 16 de noviembre de`
   - por qué: Falta el espacio entre el artículo y la cifra en el encabezado formulaico del acta. Evidencia de fuente: el PDF de 2005-06-09, de la misma serie, escribe el mismo encabezado con espacio («Celebrada el 9 de junio de 2005»), mientras el de 2005-07-12 sale pegado («celebrada el12»); la diferencia es un artefacto de extracción, no una variante del acta. La fecha queda confirmada por el cuerpo de la misma oración y por el nombre del archivo.

### `RPM-2009-08-13:2659:1` — Sergio Lehmann Beresi

1. **ESPACIO_INDEBIDO**
   - antes: `jemplifica , la caída `
   - después: `jemplifica, la caída `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2012-09-13:5054:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2008-12-11:2252:1` — Jorge Desormeaux Jiménez

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2007-08-09:1402:1` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `“`
   - por qué: Comilla recta que abre una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.
2. **LETRA_CONFUNDIDA**
   - antes: `nflación subyacente IPCXI (que excluye co`
   - después: `nflación subyacente IPCX1 (que excluye co`
   - por qué: Sigla dañada por el glifo I/l. Medido en toda la salida: 26 apariciones de esta familia, y cada forma tiene su equivalente correcto ampliamente atestiguado en el corpus (el IPC 1.430, el IPoM 1.543, IPCX 649, IPCX1 469, el IPP 10). Se excluyeron de la pasada "ellPEC", "dellPEC" y "ellMCE" (fila 1719:4): aparecen junto a siglas que no se pueden corroborar en el corpus y no hay reconstruccion unica.

### `RPM-2014-02-18:6035:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2009-02-12:2334:1` — Claudio Soto Gamboa

1. **ESPACIO_INDEBIDO**
   - antes: `ión pasada , se acumu `
   - después: `ión pasada, se acumu `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **ESPACIO_INDEBIDO**
   - antes: `cipalmente , al deteri`
   - después: `cipalmente, al deteri`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: ` de fondos , el premio`
   - después: ` de fondos, el premio`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2013-01-17:5285:1` — Enrique Marshall Rivera

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2007-01-11:1053:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `erior. Sin embargo, índica el señor Marfán`
   - después: `erior. Sin embargo, indica el señor Marfán`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2011-05-12:3984:3` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2010-05-13:3126:1` — José De Gregorio Rebeco

1. **PALABRA_PARTIDA**
   - antes: `riendo espacio para em pezar el proceso de n`
   - después: `riendo espacio para empezar el proceso de n`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 33 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2007-07-12:1323:1` — Igal Magendzo Weinberger

1. **LETRA_CONFUNDIDA**
   - antes: `ivas de inflación de! sector privado `
   - después: `ivas de inflación del sector privado `
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.
2. **LETRA_CONFUNDIDA**
   - antes: ` un valor máximo de S530 a fines de juni`
   - después: ` un valor máximo de $530 a fines de juni`
   - por qué: S mayúscula en lugar del signo $. Medido: solo 2 apariciones en todo el corpus, "S5" y "S6", y ambas son montos en pesos donde solo cabe el signo: "la paridad peso/dólar alcanzó un valor máximo de S530" y "el dólar se cotizó en torno a S610". La misma fila 1323:1 usa "$520" unas lineas mas abajo.
3. **LETRA_CONFUNDIDA**
   - antes: `ento real del gasto llegarla a 9% anual resp`
   - después: `ento real del gasto llegaría a 9% anual resp`
   - por qué: llegarla por llegaría: la í se leyo como l, la dirección inversa del glifo anterior. Medido: "llegaría" aparece 52 veces y "llegarla" una sola, en "el crecimiento real del gasto llegarla a 9% anual", donde no cabe el infinitivo con pronombre. Se midio ademas que una regla general sobre palabras terminadas en -rla seria destructiva: mantenerla 59, dejarla 30, subirla 26, llevarla 25, bajarla 23 son todas formas legítimas.
4. **SIMBOLO_SUELTO**
   - antes: `recimiento anual de 4 los ingresos tri`
   - después: `recimiento anual de los ingresos tri`
   - por qué: Dígito 4 suelto entre "de" y "los" ("el crecimiento anual de 4 los ingresos tributarios"). No hay regla general posible: el patrón "palabra + dígito + palabra" da 1.019 coincidencias en el corpus y son abrumadoramente legítimas ("a 5 años", "en 1 punto", "de 5%"). Se trata solo este caso, donde el dígito no puede ser nada porque "los ingresos" ya cierra la frase.
5. **LETRA_CONFUNDIDA**
   - antes: `l salmón y el metano!. Por el lado de`
   - después: `l salmón y el metanol. Por el lado de`
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2014-06-12:6272:1` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2013-06-13:5608:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2015-08-13:6920:1` — Diego Gianelli Gómez

1. **PALABRA_PARTIDA**
   - antes: `de actividad de Estados Unidos de América conocidos desde la última reunión del Federal Open M arket Committee, FOMC`
   - después: `de actividad de Estados Unidos de América conocidos desde la última reunión del Federal Open Market Committee, FOMC`
   - por qué: Espacio intrapalabra: 'M arket' es 'Market' partido en dos. Se reúne sin alterar una letra, sección 1 bis. Medido: 'Market Committee' aparece 8 veces en el corpus y 'M arket' 1.
2. **PALABRA_PARTIDA**
   - antes: `su presentación informando que en m ateria de commodities se observan movimientos a la baja`
   - después: `su presentación informando que en materia de commodities se observan movimientos a la baja`
   - por qué: Espacio intrapalabra: 'm ateria' por 'materia'. Medido: 'en materia de commodities' aparece 26 veces en el corpus y la forma partida 1. Sección 1 bis: se reúne sin cambiar una letra.
3. **PALABRA_PARTIDA**
   - antes: `que estuvo rezagada debido a la m ayor demanda de gasolina en Estados Unidos de América`
   - después: `que estuvo rezagada debido a la mayor demanda de gasolina en Estados Unidos de América`
   - por qué: Espacio intrapalabra: 'm ayor' por 'mayor'. La frase exacta no aparece en el corpus, pero la sección 1 bis no pide corroboración porque lo único que se hace es quitar un espacio: no se toca ninguna letra y no hay otra lectura posible.
4. **PALABRA_ERRONEA**
   - antes: `se explica principalmente por el efecto del traspaso de la depreciación cambiaría a precios`
   - después: `se explica principalmente por el efecto del traspaso de la depreciación cambiaria a precios`
   - por qué: Tilde por i. 'cambiaría' es condicional del verbo cambiar y en posición de adjetivo es ortográficamente imposible: la sección 3 ter dice que esas formas se corrigen por muchas veces que se repitan. Es el defecto más numeroso del corpus (241 contra 72). 'cambiaria' aparece 0 veces en esta fila y 0 en la sesión, pero la sección 3 ter no pide corroboración cuando la forma defectuosa no puede existir en ese lugar; 'cambiario' sí aparece 2 veces en la sesión.
5. **PALABRA_ERRONEA**
   - antes: `Brasil y Colombia, en tanto, no han modificado sus políticas de intervención cambiaría.`
   - después: `Brasil y Colombia, en tanto, no han modificado sus políticas de intervención cambiaria.`
   - por qué: Segunda ocurrencia del mismo defecto en esta fila y por la misma razón: 'cambiaria' es adjetivo y 'cambiaría' condicional, imposible en este lugar. Se corrige por separado porque el fragmento anterior es distinto.
6. **PALABRA_OMITIDA**
   - antes: `las proyecciones de actividad para el mundo se han reducido en dos décimas para año 2015 y en una décima para 2016`
   - después: `las proyecciones de actividad para el mundo se han reducido en dos décimas para el año 2015 y en una décima para 2016`
   - por qué: Falta el artículo: 'para año 2015' no es gramatical. La reparación es única porque el OCR omite, no agrega palabras, así que lo que falta es 'el' y no sobra 'año'. Corroborada: 'para el año 2015' aparece 1 vez en esta misma sesión y 30 en el corpus, que es lo que la sección 2 exige.
7. **PALABRA_OMITIDA**
   - antes: `desde la Reunión previa se observó una depreciación generalizada de la mayoría las monedas frente al dólar`
   - después: `desde la Reunión previa se observó una depreciación generalizada de la mayoría de las monedas frente al dólar`
   - por qué: Falta la preposición 'de'. 'la mayoría las monedas' no es gramatical y la reparación es única; la construcción correcta 'la mayoría de las' aparece 89 veces en el corpus. MEDIDO CON CUIDADO: la frase defectuosa completa aparece 3 veces, y las 3 son la misma oración de plantilla que el área repite mes a mes (6867:1 y 6876:1 en 2015-07-14, y esta). No es un patrón legítimo de la fuente sino el mismo defecto copiado, y se corrige aquí por ser la fila leída; las otras dos quedan pendientes para la sesión 2015-07-14.
8. **ESPACIO_INDEBIDO**
   - antes: `y 3 meses— . El señor `
   - después: `y 3 meses—. El señor `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2013-01-17:5286:1` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2012-07-12:4911:1` — Enrique Marshall Rivera

1. **ACENTO_FALTANTE**
   - antes: `o el incremento del gasto publico, que se duplicó`
   - después: `o el incremento del gasto público, que se duplicó`
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2015-01-15:6569:1` — Rodrigo Vergara Montes

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2013-09-12:5802:2` — Rodrigo Vergara Montes

1. **SIMBOLO_SUELTO**
   - antes: `serto en el Acta de esta Sesión: ( ■`
   - después: `serto en el Acta de esta Sesión: (`
   - por qué: Símbolo ■ con basura adyacente, residuo del escaneo. El tipo SIMBOLO_SUELTO fue creado justamente para estos casos («■V», «ry _<< ■» -> se elimina). Medido: 21 apariciones en 20 filas. Se trata cada una con su basura propia porque el ruido que la acompaña varía (■o J, ■,\y, ■', ■J, ■V, / ■ ' /, 4 / ■, i - /■, — f ■, ry _<< ■). En todos los casos las dos oraciones que rodean el residuo quedan completas sin él. Excepción: en 5802:2 se elimina solo el ■ y se deja el paréntesis abierto, porque esa fila ya está marcada RECONSTRUCCION_AMBIGUA_POR_COTEJAR con motivo FINAL_SIN_PUNTUACION.

### `RPM-2014-09-11:6412:1` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2009-07-09:2623:1` — José De Gregorio Rebeco

1. **PALABRA_PARTIDA**
   - antes: `onsulta si acaso el segun do trimestre va a `
   - después: `onsulta si acaso el segundo trimestre va a `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 1770 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2011-10-13:4348:1` — Sergio Lehmann Beresi

1. **ESPACIO_INDEBIDO**
   - antes: `lámina 20— , y que, po`
   - después: `lámina 20—, y que, po`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
