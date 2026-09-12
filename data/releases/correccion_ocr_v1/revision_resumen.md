# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1392**
- operaciones: **2280**
- filas marcadas para cotejo: **196**
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
| `SIMBOLO_SUELTO` | 88 |
| `FIRMA_TRUNCADA` | 55 |
| `PALABRA_ERRONEA` | 28 |
| `RESIDUO_PAGINACION` | 27 |
| `ESPACIO_FALTANTE` | 24 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_DUPLICADA` | 3 |
| `PALABRA_SOBRANTE` | 2 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2014-08-14:6382:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `e desde el punto de vísta de los precios,`
   - después: `e desde el punto de vista de los precios,`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 501 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2010-02-11:2949:2` — Kevin Cowan Logan

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.

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

### `RPM-2011-07-14:4205:1` — Rodrigo Vergara Montes

1. **ESPACIO_INDEBIDO**
   - antes: `entemente— , porque ha`
   - después: `entemente—, porque ha`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2007-02-08:1074:1` — José De Gregorio Rebeco

1. **ACENTO_FALTANTE**
   - antes: `el escenario que se tenia hace uno y dos `
   - después: `el escenario que se tenía hace uno y dos `
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2015-08-13:6958:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `Por último, manifiesta que si hubiera un desanctaje de expectativas, un alza de tasas sería la señal correcta`
   - después: `Por último, manifiesta que si hubiera un desanclaje de expectativas, un alza de tasas sería la señal correcta`
   - por qué: 'desanctaje' no es palabra: la ele se leyó como te. La oración no admite otra lectura y la corroboración sobra: 'desanclaje' aparece 3 veces en esta misma fila, 40 en la sesión y 144 en el corpus. Sección 2 bis: la forma defectuosa no es palabra, así que no hay lectura alternativa que proteger.

### `RPM-2008-02-07:1651:1` — Igal Magendzo Weinberger

1. **ACENTO_INDEBIDO**
   - antes: `o del día anterior. índica que el tipo de `
   - después: `o del día anterior. indica que el tipo de `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2013-01-17:5277:1` — Sergio Lehmann Beresi

1. **SIMBOLO_SUELTO**
   - antes: `algo mayor en Europa. A Además`
   - después: `algo mayor en Europa. Además`
   - por qué: Letra mayúscula suelta entre dos oraciones. Es ruido de escaneo: la oración anterior termina en punto y la siguiente empieza con mayúscula y sentido completo, así que la letra no pertenece a ninguna de las dos. Medido: 17 casos en 17 filas, con las letras V, H, L, U, A, M, Y, B. Se revisaron uno por uno; el único que NO es residuo es RPM-2007-01-11:1055:1 ("prolongado. A SU juicio"), donde la A abre la oración legítimamente y el defecto es "SU" en mayúscula, que se trata aparte.

### `RPM-2010-10-14:3493:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` JOSÉ DE GREGORIO REBECO Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2009-07-09:2654:1` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.
2. **SIMBOLO_SUELTO**
   - antes: `días al nivel de la TPM vigente. ■ Ajustar el plan de emis`
   - después: `días al nivel de la TPM vigente. Ajustar el plan de emis`
   - por qué: Símbolo ■ con basura adyacente, residuo del escaneo. El tipo SIMBOLO_SUELTO fue creado justamente para estos casos («■V», «ry _<< ■» -> se elimina). Medido: 21 apariciones en 20 filas. Se trata cada una con su basura propia porque el ruido que la acompaña varía (■o J, ■,\y, ■', ■J, ■V, / ■ ' /, 4 / ■, i - /■, — f ■, ry _<< ■). En todos los casos las dos oraciones que rodean el residuo quedan completas sin él. Excepción: en 5802:2 se elimina solo el ■ y se deja el paréntesis abierto, porque esa fila ya está marcada RECONSTRUCCION_AMBIGUA_POR_COTEJAR con motivo FINAL_SIN_PUNTUACION.
3. **SIMBOLO_SUELTO**
   - antes: `ra coherente con la decisión anterior. ■ Suspender, por todo lo`
   - después: `ra coherente con la decisión anterior. Suspender, por todo lo`
   - por qué: Símbolo ■ con basura adyacente, residuo del escaneo. El tipo SIMBOLO_SUELTO fue creado justamente para estos casos («■V», «ry _<< ■» -> se elimina). Medido: 21 apariciones en 20 filas. Se trata cada una con su basura propia porque el ruido que la acompaña varía (■o J, ■,\y, ■', ■J, ■V, / ■ ' /, 4 / ■, i - /■, — f ■, ry _<< ■). En todos los casos las dos oraciones que rodean el residuo quedan completas sin él. Excepción: en 5802:2 se elimina solo el ■ y se deja el paréntesis abierto, porque esa fila ya está marcada RECONSTRUCCION_AMBIGUA_POR_COTEJAR con motivo FINAL_SIN_PUNTUACION.

### `RPM-2012-09-13:5049:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `en tomo a`
   - después: `en torno a`
   - por qué: en tomo a por "en torno a". Medido: 24 apariciones (20 "en tomo a" y 4 "en tomo al"), la r leida como m. "tomo" es palabra real (volumen) pero ningun contexto lo admite. "en torno a" aparece 1.678 veces.

### `RPM-2008-12-11:2251:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **ESPACIO_INDEBIDO**
   - antes: `r en China . En segund`
   - después: `r en China. En segund`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2007-08-09:1400:1` — José De Gregorio Rebeco

1. **ACENTO_INDEBIDO**
   - antes: `, podrían generarse potencíales presiones futur`
   - después: `, podrían generarse potenciales presiones futur`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 72 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2014-02-18:6027:1` — Claudio Soto Gamboa

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2009-02-12:2333:1` — Claudio Soto Gamboa

1. **ESPACIO_INDEBIDO**
   - antes: `gundo caso .`
   - después: `gundo caso.`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2013-01-17:5283:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2007-01-11:1052:1` — Enrique Marshall Rivera

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.
2. **SIMBOLO_SUELTO**
   - antes: `una y otra dirección. U Sin embargo`
   - después: `una y otra dirección. Sin embargo`
   - por qué: Letra mayúscula suelta entre dos oraciones. Es ruido de escaneo: la oración anterior termina en punto y la siguiente empieza con mayúscula y sentido completo, así que la letra no pertenece a ninguna de las dos. Medido: 17 casos en 17 filas, con las letras V, H, L, U, A, M, Y, B. Se revisaron uno por uno; el único que NO es residuo es RPM-2007-01-11:1055:1 ("prolongado. A SU juicio"), donde la A abre la oración legítimamente y el defecto es "SU" en mayúscula, que se trata aparte.

### `RPM-2011-05-12:3973:1` — Sergio Lehmann Beresi

1. **ESPACIO_INDEBIDO**
   - antes: `te último— , y que más`
   - después: `te último—, y que más`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2010-05-13:3124:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `e de las noticias de! Ministro respec`
   - después: `e de las noticias del Ministro respec`
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2007-07-12:1321:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `ios gráficos, el efecto fiy to quality sobre Chile s`
   - después: `los gráficos, el efecto fly to quality sobre Chile s`
   - por qué: "fiy"/"fIy" por "fly": la l se leyo como i (o como I). Es el mismo glifo que produce "ai" por "al", demostrado con 26 casos independientes. Se retira la marca RECONSTRUCCION_AMBIGUA que se había puesto en esta fila: al aparecer la regla de glifo, la ambigüedad se resuelve. Un escáner no convierte "flight" en "fiy" (sería borrar cuatro letras); sí convierte "fly" en "fiy". Las 21 apariciones de "flight to quality" que hay en el corpus son la otra grafía, correcta, y no se tocan. La operación se extendió dos caracteres hacia la izquierda para cubrir además "ios" por "los" (§12): ambas caen en el mismo tramo y dos operaciones separadas se pisarían, porque el fragmento anterior empezaba justo en la s de "ios".

### `RPM-2014-06-12:6270:1` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2013-06-13:5605:1` — Matías Bernier Bórquez

1. **ESPACIO_INDEBIDO**
   - antes: `n 0,48%. / .`
   - después: `n 0,48%. /.`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2015-07-14:6917:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` EMRIQUE MARSHALL RIVERA RODRIGO VERGARA MONTES Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2013-01-17:5285:1` — Enrique Marshall Rivera

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2012-07-12:4909:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2015-01-15:6561:2` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2013-09-12:5798:2` — Rodrigo Vergara Montes

1. **SIMBOLO_SUELTO**
   - antes: `las opciones de política monetaria. H ^ .`
   - después: `las opciones de política monetaria.`
   - por qué: Tres glifos sueltos después del punto de cierre: una hache, un acento circunflejo y un segundo punto. La oración ya está cerrada por su propio punto, así que el resto no aporta nada. Aparece una sola vez en el corpus.

### `RPM-2014-09-11:6399:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `1O`
   - después: `10`
   - por qué: 1O por 10: el cero se leyo como la letra O mayuscula. Medido: 7 apariciones en 6 filas y todas son numeros donde solo cabe el diez ("tasas a 1O años plazo", "lámina Nº 1O", "US$ 3,1O la libra", "a 5 y 1O años", "a 2 y 1O años", "a 1O años", "de 1O o 20%"). Se verifico que no existen apariciones embebidas en otras palabras.

### `RPM-2009-07-09:2622:6` — Claudio Soto Gamboa

1. **PALABRA_PARTIDA**
   - antes: `y el Gerente de Anális is Macroeconómico `
   - después: `y el Gerente de Análisis Macroeconómico `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 1784 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA. Es un nombre propio, pero no se está adivinando nada: la forma correcta está atestiguada en el corpus y lo único que se elimina es un espacio que el escaneo insertó dentro de la palabra. No es resolución de alias, que es lo que el criterio prohíbe.

### `RPM-2011-10-13:4344:1` — Sergio Lehmann Beresi

1. **ACENTO_FALTANTE**
   - antes: `ajustes a la baja en América Latina, Asia, Oceania y Europa emergente`
   - después: `ajustes a la baja en América Latina, Asia, Oceanía y Europa emergente`
   - por qué: Falta la tilde en 'Oceanía'. No es una reconstrucción ambigua: el topónimo tiene una sola grafía en español y la serie es una enumeración de regiones, así que no hay otra lectura posible. Distinto de los casos que marco, donde faltaba una letra y cabían dos palabras.
