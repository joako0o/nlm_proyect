# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1742**
- operaciones: **2996**
- filas marcadas para cotejo: **218**
- sha256 de la base: `eebaa728dc1d7ce14315caebd0c7516ff324b5d4acaefcf40cec2bf6d855945d`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 702 |
| `ESPACIO_INDEBIDO` | 510 |
| `PALABRA_PARTIDA` | 491 |
| `ACENTO_INDEBIDO` | 385 |
| `PUNTUACION` | 267 |
| `SIMBOLO_SUELTO` | 241 |
| `ACENTO_FALTANTE` | 220 |
| `FIRMA_TRUNCADA` | 55 |
| `PALABRA_ERRONEA` | 30 |
| `RESIDUO_PAGINACION` | 30 |
| `ESPACIO_FALTANTE` | 27 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |
| `PALABRA_DUPLICADA` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2015-05-14:6808:1` — Rodrigo Valdés Pulido

1. **ACENTO_INDEBIDO**
   - antes: ` otros elementos no atríbuibles únicamente a l`
   - después: ` otros elementos no atribuibles únicamente a l`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 52 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2011-10-13:4388:1` — Felipe Larraín Bascuñán

1. **PUNTUACION**
   - antes: `el señor Felipe Larraín destaca, que el 30 de septiembre pasado`
   - después: `el señor Felipe Larraín destaca que el 30 de septiembre pasado`
   - por qué: Coma intrusa entre el verbo y la subordinada. Medido en todo el consolidado: 'destaca que' aparece 772 veces y 'destaca, que' una sola. La oración no admite otra lectura y la forma correcta es abrumadoramente mayoritaria.

### `RPM-2009-03-12:2389:1` — Pablo García Silva

1. **PALABRA_PARTIDA**
   - antes: `rcía comenta que ha soste nido conversaciones `
   - después: `rcía comenta que ha sostenido conversaciones `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 105 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
2. **PALABRA_PARTIDA**
   - antes: `en torn o a`
   - después: `en torno a`
   - por qué: Palabra partida por un espacio espurio, con la segunda mitad reducida a una letra: «torn o» -> «torno». La evidencia es interna y doble: el primer trozo («torn») es marginal en el corpus (1 apariciones, y ésas son ésta) y la forma junta («torno») es la que el propio corpus usa 1736 veces. La encontró detector_partida_letra, agregado en §31 porque detector_partida no puede verla: su guarda «segunda mitad con frecuencia < 50» bloquea justo las letras (a=37.528, o, e, s), que son frecuentes porque este mismo defecto las esparce. Precisión medida del detector: 40 candidatos en las 9.723 filas, 40 verdaderos; el único que no se corrige aquí es el de 147:1, que es la cola de una carrera letra por letra y se arregla entero en su pasada.

### `RPM-2005-03-10:171:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `m antener`
   - después: `mantener`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 1788 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2009-12-15:2803:1` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `9;00 horas`
   - después: `9:00 horas`
   - por qué: Idem: 544 contra 5.

### `RPM-2006-06-15:728:1` — Rodrigo Valdés Pulido

1. **LETRA_CONFUNDIDA**
   - antes: `IRC`
   - después: `IPC`
   - por qué: IRC por IPC. Medido en todo el corpus: 71 apariciones, ninguna en un contexto donde IRC sea una sigla legitima; 61 sueltas y 10 dentro de IRCX1, que tambien debe leerse IPCX1 porque la misma fila escribe IPCX e IPCX2. Regla de bloque revisada caso por caso.
2. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
3. **LETRA_CONFUNDIDA**
   - antes: ` inflacionaria y de ios salarios.
Señal`
   - después: ` inflacionaria y de los salarios.
Señal`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.
4. **ESPACIO_INDEBIDO**
   - antes: `lo avalan— , existe el`
   - después: `lo avalan—, existe el`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
5. **ESPACIO_INDEBIDO**
   - antes: `o
benigno— , y que la `
   - después: `o
benigno—, y que la `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

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

### `RPM-2007-07-12:1340:1` — Rodrigo Valdés Pulido

1. **LETRA_CONFUNDIDA**
   - antes: `rca del promedio de ios últimos cin co `
   - después: `rca del promedio de los últimos cinco `
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura. | Se extiende esta operación ya registrada en vez de añadir otra, porque la palabra partida cae dentro del mismo tramo: dos defectos en el mismo tramo se resuelven extendiendo, no apilando.
2. **PALABRA_PARTIDA**
   - antes: ` Rodrigo Valdés que tam bién hay motivos a f`
   - después: ` Rodrigo Valdés que también hay motivos a f`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 4812 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
3. **PALABRA_PARTIDA**
   - antes: ` han aumentado. Sin em bargo, detrás de este`
   - después: ` han aumentado. Sin embargo, detrás de este`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 1376 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
4. **PALABRA_PARTIDA**
   - antes: `ular, el Gerente de D ivisión Estudios señor `
   - después: `ular, el Gerente de División Estudios señor `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2999 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
5. **PALABRA_PARTIDA**
   - antes: `ck de precios, y un aum ento de 25 puntos ba`
   - después: `ck de precios, y un aumento de 25 puntos ba`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2682 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
6. **PALABRA_PARTIDA**
   - antes: `m aterializarse`
   - después: `materializarse`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 67 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
7. **PALABRA_PARTIDA**
   - antes: `m antención`
   - después: `mantención`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 510 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
8. **PALABRA_PARTIDA**
   - antes: `m ayores`
   - después: `mayores`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 1198 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
9. **PALABRA_PARTIDA**
   - antes: `M onetaria`
   - después: `Monetaria`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 3247 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
10. **PALABRA_PARTIDA**
   - antes: `m ediano`
   - después: `mediano`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 872 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
11. **PALABRA_PARTIDA**
   - antes: `m ás`
   - después: `más`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 11942 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2010-07-15:3211:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `Beam Stearns`
   - después: `Bear Stearns`
   - por qué: Nombre dañado por OCR: «Beam Stearns» por «Bear Stearns», el banco de inversión cuya quiebra en septiembre de 2008 abre la crisis financiera. Confusión de la erre por la eme, clásica en OCR. Medido en el corpus: «Beam Stearns» aparece 5 veces y «Bear Stearns» 1, de modo que la forma correcta está atestiguada por el propio corpus aunque sea minoritaria; los cinco contextos son inequívocos («cuando alrededor de julio del año 2008», «en el momento en que quebró», «la crisis de»). Se corrige y se deja constancia aquí de que es el primer caso en que la forma canónica es minoritaria: la decisión no descansa en la frecuencia sino en que la entidad es única y el corpus la atestigua.

### `RPM-2015-07-14:6906:1` — Alberto Naudon Dell'Oro

1. **LETRA_CONFUNDIDA**
   - antes: `tividad, señala que ios datos conocidos`
   - después: `tividad, señala que los datos conocidos`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2009-07-09:2649:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2008-12-11:2190:1` — José De Gregorio Rebeco

1. **ESPACIO_INDEBIDO**
   - antes: ` paridades , si se señ`
   - después: ` paridades, si se señ`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **ESPACIO_INDEBIDO**
   - antes: `ortalecido , ello tien`
   - después: `ortalecido, ello tien`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ACENTO_INDEBIDO**
   - antes: `él efectúo`
   - después: `él efectuó`
   - por qué: El sujeto es «él», así que hace falta la tercera persona del pretérito «efectuó»; «efectúo» es la primera persona del presente y no concuerda. Medido en el corpus: «efectúo» aparece 1 sola vez (ésta) y «efectuó» 51. En la misma fila el verbo se usa bien más adelante: «en el Ministerio de Hacienda se efectuó ese ejercicio».
4. **LETRA_CONFUNDIDA**
   - antes: `De Gregario`
   - después: `De Gregorio`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).

### `RPM-2010-05-13:3084:1` — Sebastián Claro Edwards

1. **SIMBOLO_SUELTO**
   - antes: ` \ `
   - después: ` `
   - por qué: Barra invertida suelta, residuo de salto de línea del PDF. Medido en el corpus: aparece 11 veces rodeada de espacios, siempre entre dos palabras que pertenecen a la misma oración.

### `RPM-2008-04-10:1785:1` — Consejo del Banco Central de Chile

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **PUNTUACION**
   - antes: `17,00 horas`
   - después: `17:00 horas`
   - por qué: Coma en vez de dos puntos en la hora. Medido en el corpus: «HH:MM horas» aparece 551 veces y «HH,MM horas» 18, siempre en contexto horario inequívoco («siendo las …», «suspende la Sesión a las …», «se reanudará a las …», «Se levanta la Sesión a las …»). No es un decimal: son horas y minutos. Es la misma familia que las 7 correcciones ya registradas del punto y coma («16;55 horas» -> «16:55 horas», tipo PUNTUACION). Los rangos con guion («46-50 horas», «0-45 horas») son otra cosa y no se tocan.

### `RPM-2007-02-08:1090:6` — Klaus Schmidt-Hebbel Dunker

1. **PALABRA_PARTIDA**
   - antes: `Schmidt- Hebbel`
   - después: `Schmidt-Hebbel`
   - por qué: Apellido partido por un espacio despues del guion. La seccion 5 prohibe RESOLVER o INVENTAR un nombre propio, y aqui no se hace ninguna de las dos cosas: se reune un nombre que el propio corpus escribe correctamente 122 veces contra 5 partidas, y que la lista de asistencia de las actas trae completo ("don Klaus Schmidt-Hebbel Dunker"). Prueba aplicada, que es la que autoriza la excepcion: la forma correcta existe en el corpus referida a la misma persona. Un caso como "Claudios Soto" no la pasaria, porque "Claudio Soto" no aparece en ninguna parte.

### `RPM-2011-03-17:3832:1` — Sergio Lehmann Beresi

1. **ACENTO_FALTANTE**
   - antes: `n en ese rango. Por ultimo, hace presente `
   - después: `n en ese rango. Por último, hace presente `
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2014-07-15:6332:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `opIrnon`
   - después: `opinión`
   - por qué: opIrnon por opinión. No es palabra y la formula "en su opinión" es de las mas frecuentes del corpus (1.867 apariciones de "opinión"); el contexto "Expresa que, en su opIrnon, la desaceleración" no admite otra lectura.
2. **LETRA_CONFUNDIDA**
   - antes: `1nstitución`
   - después: `Institución`
   - por qué: 1nstitución por Institución: la I mayuscula inicial se leyo como el digito 1. El contexto es "del staff de la 1nstitución".

### `RPM-2008-06-10:1865:1` — Pablo García Silva

1. **ESPACIO_INDEBIDO**
   - antes: `del precio , producto `
   - después: `del precio, producto `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **ESPACIO_INDEBIDO**
   - antes: `ena medida , los molin`
   - después: `ena medida, los molin`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: `o, y luego , en la med`
   - después: `o, y luego, en la med`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2014-06-12:6267:1` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **ACENTO_INDEBIDO**
   - antes: `nto de los salarios nomínales disminuye desde`
   - después: `nto de los salarios nominales disminuye desde`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 606 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2010-07-15:3213:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `que son similares a ios que considera l`
   - después: `que son similares a los que considera l`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2006-05-11:674:1` — Vittorio Corbo Lioi

1. **LETRA_CONFUNDIDA**
   - antes: `IPOM`
   - después: `IPoM`
   - por qué: Sigla mal compuesta. Medido en el corpus: «IPoM» aparece 2473 veces y «IPOM» 58, siempre el mismo documento, el Informe de Política Monetaria del Banco Central de Chile, cuya sigla lleva la o minúscula. El OCR leyó la o minúscula como O mayúscula.

### `RPM-2009-10-13:2758:1` — José De Gregorio Rebeco

1. **ESPACIO_INDEBIDO**
   - antes: `Presidente ,señor José`
   - después: `Presidente,señor José`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **PUNTUACION**
   - antes: `ad.`
   - después: `ad,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.

### `RPM-2009-04-09:2483:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `De Gregario`
   - después: `De Gregorio`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).
2. **LETRA_CONFUNDIDA**
   - antes: `Claudia Soto`
   - después: `Claudio Soto`
   - por qué: La «a» final ocupó el lugar de la «o» en el nombre de pila. El propio texto lo descarta: la fila lo trata en masculino («señor» o «don») y el corpus atestigua «Claudio Soto» 1.275 veces contra 1 «Claudia Soto». No es la Claudia legítima del corpus (doña Claudia Varela Lértora, doña Claudia Sotz Pantoja), que siempre va con «doña» o «Gerenta».

### `RPM-2006-12-14:1003:8` — Igal Magendzo Weinberger

1. **LETRA_CONFUNDIDA**
   - antes: `El señor Madgenzo comenta que el Transantiago representa `
   - después: `El señor Magendzo comenta que el Transantiago representa `
   - por qué: Normalización de nombre propio dañado, autorizada por el usuario en esta ronda (el criterio anterior era marcar sin corregir). La forma canónica la acreditan el corpus y el roster de la sesión: «Magendzo» aparece 416 veces en la salida, contra 18 de la forma dañada. Se corrige en Texto_Corregido; Texto queda intacto. Lo que no tiene forma canónica atestiguada (por ejemplo «Miguel Angel Nacrur Gazali») sigue marcado NOMBRE_PROPIO_POR_COTEJAR.
2. **LETRA_CONFUNDIDA**
   - antes: `o se trata de una cifra menor. El señor Madgenzo señala que en la RPM pasada se identifi`
   - después: `o se trata de una cifra menor. El señor Magendzo señala que en la RPM pasada se identifi`
   - por qué: Normalización de nombre propio dañado, autorizada por el usuario en esta ronda (el criterio anterior era marcar sin corregir). La forma canónica la acreditan el corpus y el roster de la sesión: «Magendzo» aparece 416 veces en la salida, contra 18 de la forma dañada. Se corrige en Texto_Corregido; Texto queda intacto. Lo que no tiene forma canónica atestiguada (por ejemplo «Miguel Angel Nacrur Gazali») sigue marcado NOMBRE_PROPIO_POR_COTEJAR.

### `RPM-2011-08-18:4238:1` — Luis Óscar Herrera Barriga

1. **SIMBOLO_SUELTO**
   - antes: `as del sur de Estados Unidos, asi como problemas de lluvia exce`
   - después: `as del sur de Estados Unidos, así como problemas de lluvia exce`
   - por qué: «asi» no es palabra del español y el corpus escribe «así» 1.199 veces frente a 19. Los 19 casos son la misma lesión (caída del acento) y se leyeron uno por uno: ninguno es una sigla ni parte de otra palabra.

### `RPM-2010-10-14:3437:1` — Felipe Jaque

1. **ACENTO_FALTANTE**
   - antes: `a que la tasa a dos años, en tanto, seria la única que no`
   - después: `a que la tasa a dos años, en tanto, sería la única que no`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.
2. **ESPACIO_INDEBIDO**
   - antes: ` del 2008— , muestra q`
   - después: ` del 2008—, muestra q`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2012-11-13:5207:1` — Claudio Soto Gamboa

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **ACENTO_FALTANTE**
   - antes: `a parte extrapresupuestaria, con tasas de c`
   - después: `a parte extrapresupuestaría, con tasas de c`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2015-05-14:6764:1` — Joaquín Vial Ruiz-Tagle

1. **SIMBOLO_SUELTO**
   - antes: `variable. ' En`
   - después: `variable. En`
   - por qué: Idem que 6067:1: apóstrofo suelto entre dos oraciones completas, sin basura alrededor y sin cita que abrir (§29).

### `RPM-2010-07-15:3216:1` — Sergio Lehmann Beresi

1. **ESPACIO_INDEBIDO**
   - antes: `007 y 2008 . Por regió`
   - después: `007 y 2008. Por regió`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **ESPACIO_INDEBIDO**
   - antes: ` paridades , el yuan y el franco suizo , que actua`
   - después: ` paridades, el yuan y el franco suizo, que actua`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: `o del yuan , indica qu`
   - después: `o del yuan, indica qu`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
4. **ESPACIO_INDEBIDO**
   - antes: `o del yuan .`
   - después: `o del yuan.`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2010-04-15:3070:1` — Pablo García Silva

1. **PALABRA_PARTIDA**
   - antes: `ativas un escenario macroeconóm ico de mediano plaz`
   - después: `ativas un escenario macroeconómico de mediano plaz`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 196 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
