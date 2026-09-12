# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1428**
- operaciones: **2420**
- filas marcadas para cotejo: **210**
- sha256 de la base: `d0b64842cd756df4c50d2960d9bbf01c4c45e5df28609d7b612c5d666593da75`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `ESPACIO_INDEBIDO` | 511 |
| `LETRA_CONFUNDIDA` | 496 |
| `PALABRA_PARTIDA` | 476 |
| `ACENTO_INDEBIDO` | 354 |
| `ACENTO_FALTANTE` | 182 |
| `SIMBOLO_SUELTO` | 115 |
| `PUNTUACION` | 113 |
| `FIRMA_TRUNCADA` | 55 |
| `PALABRA_ERRONEA` | 28 |
| `RESIDUO_PAGINACION` | 27 |
| `ESPACIO_FALTANTE` | 26 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_DUPLICADA` | 3 |
| `PALABRA_SOBRANTE` | 2 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2014-05-15:6228:1` — Joaquín Vial Ruiz-Tagle

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2009-12-15:2809:3` — José De Gregorio Rebeco

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

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
10. **PALABRA_PARTIDA**
   - antes: `que, com o se`
   - después: `que, como se`
   - por qué: Palabra partida por un espacio espurio, con la segunda mitad reducida a una letra: «com o» -> «como». La evidencia es interna y doble: el primer trozo («com») es marginal en el corpus (2 apariciones, y ésas son ésta) y la forma junta («como») es la que el propio corpus usa 5932 veces. La encontró detector_partida_letra, agregado en §31 porque detector_partida no puede verla: su guarda «segunda mitad con frecuencia < 50» bloquea justo las letras (a=37.528, o, e, s), que son frecuentes porque este mismo defecto las esparce. Precisión medida del detector: 40 candidatos en las 9.723 filas, 40 verdaderos; el único que no se corrige aquí es el de 147:1, que es la cola de una carrera letra por letra y se arregla entero en su pasada.
11. **PALABRA_PARTIDA**
   - antes: `reaccione consecuentem ente. La`
   - después: `reaccione consecuentemente. La`
   - por qué: Palabra partida por un espacio espurio, con la segunda mitad reducida a una letra: «consecuentem ente» -> «consecuentemente». La evidencia es interna y doble: el primer trozo («consecuentem») es marginal en el corpus (1 apariciones, y ésas son ésta) y la forma junta («consecuentemente») es la que el propio corpus usa 10 veces. La encontró detector_partida_letra, agregado en §31 porque detector_partida no puede verla: su guarda «segunda mitad con frecuencia < 50» bloquea justo las letras (a=37.528, o, e, s), que son frecuentes porque este mismo defecto las esparce. Precisión medida del detector: 40 candidatos en las 9.723 filas, 40 verdaderos; el único que no se corrige aquí es el de 147:1, que es la cola de una carrera letra por letra y se arregla entero en su pasada.

### `RPM-2011-04-12:3946:1` — Claudio Soto Gamboa

1. **ESPACIO_INDEBIDO**
   - antes: `tre otros— . Añade que`
   - después: `tre otros—. Añade que`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2007-01-11:1045:1` — José De Gregorio Rebeco

1. **ACENTO_FALTANTE**
   - antes: `e de acuerdo con el diagnostico que se ha hecho`
   - después: `e de acuerdo con el diagnóstico que se ha hecho`
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2015-07-14:6867:1` — Diego Gianelli Gómez

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **LETRA_CONFUNDIDA**
   - antes: ` climáticas asociadas ai fenómeno de El Niño. `
   - después: ` climáticas asociadas al fenómeno de El Niño. `
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2007-12-13:1611:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **SALTOS_DE_LINEA**
   - antes: `alcances de la crisis subpri me especialmente en `
   - después: `alcances de la crisis subprime especialmente en `
   - por qué: Palabra partida por la justificación del PDF ("subpri me" por "subprime"). Medido: 4 apariciones en 4 filas en toda la base; una (1317:1) se corrigió con la ronda 191 y estas son las otras tres. La palabra es inequívoca y está atestiguada: "subprime" aparece 58 veces en el corpus. Es el mismo artefacto que "inmobiliari o" y que las 35 palabras en letras sueltas de §12.

### `RPM-2012-09-13:5066:1` — Claudio Soto Gamboa

1. **LETRA_CONFUNDIDA**
   - antes: `en tomo a`
   - después: `en torno a`
   - por qué: en tomo a por "en torno a". Medido: 24 apariciones (20 "en tomo a" y 4 "en tomo al"), la r leida como m. "tomo" es palabra real (volumen) pero ningun contexto lo admite. "en torno a" aparece 1.678 veces.

### `RPM-2010-08-12:3341:1` — Enrique Marshall Rivera

1. **LETRA_CONFUNDIDA**
   - antes: `e se ubicará en torno ai límite superior del r`
   - después: `e se ubicará en torno al límite superior del r`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2009-06-16:2586:1` — Claudio Soto Gamboa

1. **LETRA_CONFUNDIDA**
   - antes: `IRC`
   - después: `IPC`
   - por qué: IRC por IPC. Medido en todo el corpus: 71 apariciones, ninguna en un contexto donde IRC sea una sigla legitima; 61 sueltas y 10 dentro de IRCX1, que tambien debe leerse IPCX1 porque la misma fila escribe IPCX e IPCX2. Regla de bloque revisada caso por caso.

### `RPM-2012-04-17:4766:1` — Sebastián Claro Edwards

1. **RESIDUO_PAGINACION**
   - antes: ` Sesión N° 184 Página 12 de 26`
   - después: ``
   - por qué: Residuo de paginacion del PDF incrustado en medio de la oracion. Medido: 26 apariciones, 24 con la cabecera "Sesion N° N" delante y 2 como pie de pagina del Comunicado ("Pagina 31 de 31"). "Sesion N° N" aparece 25 veces en el corpus y solo 24 van seguidas de Pagina, de modo que el patron exige ambos y no toca ninguna mencion legitima. Se elimina el residuo y se deja un solo espacio donde la oracion continua.

### `RPM-2008-11-13:2130:2` — Sergio Lehmann Beresi

1. **ACENTO_FALTANTE**
   - antes: `io de las viviendas todavia debe caer en to`
   - después: `io de las viviendas todavía debe caer en to`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.
2. **ESPACIO_INDEBIDO**
   - antes: `rticulares , el Gerent`
   - después: `rticulares, el Gerent`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2007-08-09:1371:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `te reales, sino que tam bién descontado el e`
   - después: `te reales, sino que también descontado el e`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 4812 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
2. **PALABRA_PARTIDA**
   - antes: `especto del tipo de cam bio y exportaciones`
   - después: `especto del tipo de cambio y exportaciones`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2947 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2013-11-19:5865:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2009-01-08:2285:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `Moneta ria que llevan al promed io del primer trim`
   - después: `Monetaria que llevan al promedio del primer trim`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 796 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA. | Se extiende esta operación ya registrada en vez de añadir otra, porque la palabra partida cae dentro del mismo tramo: dos defectos en el mismo tramo se resuelven extendiendo, no apilando.
2. **ESPACIO_INDEBIDO**
   - antes: ` trimestre . Para pone`
   - después: ` trimestre. Para pone`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: `a pregunta , ya que si`
   - después: `a pregunta, ya que si`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
4. **ESPACIO_INDEBIDO**
   - antes: `cia futuro , porque no`
   - después: `cia futuro, porque no`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2012-09-13:5072:1` — Manuel Marfán Lewis

1. **SIMBOLO_SUELTO**
   - antes: `cita la opinión del staff sobre el tema. ■V`
   - después: `cita la opinión del staff sobre el tema.`
   - por qué: Símbolo ■ con basura adyacente, residuo del escaneo. El tipo SIMBOLO_SUELTO fue creado justamente para estos casos («■V», «ry _<< ■» -> se elimina). Medido: 21 apariciones en 20 filas. Se trata cada una con su basura propia porque el ruido que la acompaña varía (■o J, ■,\y, ■', ■J, ■V, / ■ ' /, 4 / ■, i - /■, — f ■, ry _<< ■). En todos los casos las dos oraciones que rodean el residuo quedan completas sin él. Excepción: en 5802:2 se elimina solo el ■ y se deja el paréntesis abierto, porque esa fila ya está marcada RECONSTRUCCION_AMBIGUA_POR_COTEJAR con motivo FINAL_SIN_PUNTUACION.

### `RPM-2006-12-14:1017:1` — Enrique Marshall Rivera

1. **PALABRA_PARTIDA**
   - antes: `para hacerl o, tal`
   - después: `para hacerlo, tal`
   - por qué: Palabra partida por un espacio espurio, con la segunda mitad reducida a una letra: «hacerl o» -> «hacerlo». La evidencia es interna y doble: el primer trozo («hacerl») es marginal en el corpus (2 apariciones, y ésas son ésta) y la forma junta («hacerlo») es la que el propio corpus usa 89 veces. La encontró detector_partida_letra, agregado en §31 porque detector_partida no puede verla: su guarda «segunda mitad con frecuencia < 50» bloquea justo las letras (a=37.528, o, e, s), que son frecuentes porque este mismo defecto las esparce. Precisión medida del detector: 40 candidatos en las 9.723 filas, 40 verdaderos; el único que no se corrige aquí es el de 147:1, que es la cola de una carrera letra por letra y se arregla entero en su pasada.

### `RPM-2011-01-13:3713:1` — Enrique Marshall Rivera

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **LETRA_CONFUNDIDA**
   - antes: `imistas de parte de ios hogares, condic`
   - después: `imistas de parte de los hogares, condic`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2010-02-11:2968:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` JOSE DE GREGORIO REBECO Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2007-06-14:1267:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `mo se había planteado ai inicio de la exposici`
   - después: `mo se había planteado al inicio de la exposici`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.
2. **ACENTO_FALTANTE**
   - antes: `ro está más o menos en linea con el spread de lo`
   - después: `ro está más o menos en línea con el spread de lo`
   - por qué: Tilde faltante, grupo B3. Se leyeron las 53 apariciones de linea, continua, publica y lineas, y sólo 23 son defecto. «linea»: las 18 son la fórmula «en linea con», siempre el sustantivo, así que van con contexto. «lineas»: las 4 son sustantivo («otras lineas de financiamiento», «algunas lineas manufactureras», «de las lineas vinculadas»). «continua»: de 18 apariciones sólo 2 son el verbo («la actividad económica continua creciendo», «esta parte de la economía continua funcionando»); las otras 16 son el adjetivo continuo/continua y NO se tocan («la continua caída», «la mejora continua», «la convergencia continua y gradual», «la serie no es continua», «de continua colaboración», «de manera continua»). «publica»: las 13 son la tercera persona del verbo publicar («se publica anualmente», «la Reserva Federal no publica su propia», «el INE no los publica», «que publica el Fondo») y ninguna se corrige.

### `RPM-2014-03-13:6111:1` — Enrique Marshall Rivera

1. **LETRA_CONFUNDIDA**
   - antes: ` que se espera para ios próximos meses.`
   - después: ` que se espera para los próximos meses.`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.
2. **ACENTO_INDEBIDO**
   - antes: `magnitud del ajuste cambíario observado, esti`
   - después: `magnitud del ajuste cambiario observado, esti`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 213 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2013-03-14:5445:1` — Joaquín Vial Ruiz-Tagle

1. **SIMBOLO_SUELTO**
   - antes: `nergía. Por último, expresa que se ■ v acrecienta el riesgo polít`
   - después: `nergía. Por último, expresa que se acrecienta el riesgo polít`
   - por qué: Símbolo ■ con basura adyacente, residuo del escaneo. El tipo SIMBOLO_SUELTO fue creado justamente para estos casos («■V», «ry _<< ■» -> se elimina). Medido: 21 apariciones en 20 filas. Se trata cada una con su basura propia porque el ruido que la acompaña varía (■o J, ■,\y, ■', ■J, ■V, / ■ ' /, 4 / ■, i - /■, — f ■, ry _<< ■). En todos los casos las dos oraciones que rodean el residuo quedan completas sin él. Excepción: en 5802:2 se elimina solo el ■ y se deja el paréntesis abierto, porque esa fila ya está marcada RECONSTRUCCION_AMBIGUA_POR_COTEJAR con motivo FINAL_SIN_PUNTUACION.

### `RPM-2015-05-14:6782:1` — Miguel Fuentes Díaz

1. **ESPACIO_INDEBIDO**
   - antes: `e y queso— , que había`
   - después: `e y queso—, que había`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2012-09-13:5074:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2012-04-17:4736:4` — Sergio Lehmann Beresi

1. **RESIDUO_PAGINACION**
   - antes: ` Sesión N° 184 Página 4 de 26 `
   - después: ` `
   - por qué: Residuo de paginacion del PDF incrustado en medio de la oracion. Medido: 26 apariciones, 24 con la cabecera "Sesion N° N" delante y 2 como pie de pagina del Comunicado ("Pagina 31 de 31"). "Sesion N° N" aparece 25 veces en el corpus y solo 24 van seguidas de Pagina, de modo que el patron exige ambos y no toca ninguna mencion legitima. Se elimina el residuo y se deja un solo espacio donde la oracion continua.

### `RPM-2015-09-15:7030:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2014-08-14:6382:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `e desde el punto de vísta de los precios,`
   - después: `e desde el punto de vista de los precios,`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 501 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2013-06-13:5596:1` — Claudio Soto Gamboa

1. **ACENTO_FALTANTE**
   - antes: `subejecución presupuestaria, tanto por conc`
   - después: `subejecución presupuestaría, tanto por conc`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2014-06-12:6255:1` — Claudio Raddatz Kiefer

1. **SIMBOLO_SUELTO**
   - antes: `desarrollados. ' Sobre`
   - después: `desarrollados. Sobre`
   - por qué: Idem que 6067:1: apóstrofo suelto entre dos oraciones completas, sin basura alrededor y sin cita que abrir (§29).

### `RPM-2009-05-07:2544:1` — Sebastián Claro Edwards

1. **SIMBOLO_SUELTO**
   - antes: `ativas de inflación y actividad. / ■ Continuando con su exposici`
   - después: `ativas de inflación y actividad. Continuando con su exposici`
   - por qué: Símbolo ■ con basura adyacente, residuo del escaneo. El tipo SIMBOLO_SUELTO fue creado justamente para estos casos («■V», «ry _<< ■» -> se elimina). Medido: 21 apariciones en 20 filas. Se trata cada una con su basura propia porque el ruido que la acompaña varía (■o J, ■,\y, ■', ■J, ■V, / ■ ' /, 4 / ■, i - /■, — f ■, ry _<< ■). En todos los casos las dos oraciones que rodean el residuo quedan completas sin él. Excepción: en 5802:2 se elimina solo el ■ y se deja el paréntesis abierto, porque esa fila ya está marcada RECONSTRUCCION_AMBIGUA_POR_COTEJAR con motivo FINAL_SIN_PUNTUACION.
2. **ACENTO_FALTANTE**
   - antes: `e quiere comunicar, decisión que no seria fácil de interp`
   - después: `e quiere comunicar, decisión que no sería fácil de interp`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.
