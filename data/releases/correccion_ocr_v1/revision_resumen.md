# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1393**
- operaciones: **2312**
- filas marcadas para cotejo: **196**
- sha256 de la base: `d0b64842cd756df4c50d2960d9bbf01c4c45e5df28609d7b612c5d666593da75`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `ESPACIO_INDEBIDO` | 515 |
| `LETRA_CONFUNDIDA` | 487 |
| `PALABRA_PARTIDA` | 415 |
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

### `RPM-2014-08-14:6378:1` — Claudio Raddatz Kiefer

1. **ACENTO_INDEBIDO**
   - antes: `s últimos Informes. Adícionalmente, en cuanto a po`
   - después: `s últimos Informes. Adicionalmente, en cuanto a po`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 71 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2010-02-11:2941:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `IRC`
   - después: `IPC`
   - por qué: IRC por IPC. Medido en todo el corpus: 71 apariciones, ninguna en un contexto donde IRC sea una sigla legitima; 61 sueltas y 10 dentro de IRCX1, que tambien debe leerse IPCX1 porque la misma fila escribe IPCX e IPCX2. Regla de bloque revisada caso por caso.

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

### `RPM-2007-02-08:1074:1` — José De Gregorio Rebeco

1. **ACENTO_FALTANTE**
   - antes: `el escenario que se tenia hace uno y dos `
   - después: `el escenario que se tenía hace uno y dos `
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2015-08-13:6957:1` — Alberto Naudon Dell'Oro

1. **PALABRA_PARTIDA**
   - antes: `El Gerente de División Estudios señor Alberto Naudon aclara que el ejercicio en com ento no tuvo la intención`
   - después: `El Gerente de División Estudios señor Alberto Naudon aclara que el ejercicio en comento no tuvo la intención`
   - por qué: Palabra partida por un espacio intrapalabra. Sección 1 ter: se reúne sin alterar una letra, así que no hay lectura alternativa que proteger y no se pide corroboración.
2. **PALABRA_PARTIDA**
   - antes: `si bien la Minuta de Opciones no sugiere en caso alguno tom ar una acción inminente`
   - después: `si bien la Minuta de Opciones no sugiere en caso alguno tomar una acción inminente`
   - por qué: Palabra partida por un espacio intrapalabra. Sección 1 ter: se reúne sin alterar una letra, así que no hay lectura alternativa que proteger y no se pide corroboración.
3. **PALABRA_DUPLICADA**
   - antes: `que se situaría dentro del rango recién pasada la mitad del próximo año, con registros sobre sobre 5% en el intertanto`
   - después: `que se situaría dentro del rango recién pasada la mitad del próximo año, con registros sobre 5% en el intertanto`
   - por qué: Palabra duplicada: 'sobre sobre'. La reparación es única, porque quitar el segundo daría el mismo texto y 'sobre sobre' no es ninguna construcción. Medido: aparece 1 sola vez en todo el corpus, así que no es un uso de la fuente sino una duplicación de esta fila. Segundo caso de duplicación en el corpus tras la fila entera repetida de 6926:2 (ronda 179).

### `RPM-2008-02-07:1646:2` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `obsen/a`
   - después: `observa`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene observa y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.

### `RPM-2013-01-17:5268:1` — Consejo del Banco Central de Chile

1. **SIMBOLO_SUELTO**
   - antes: `B A N C O C E N T R A L D E C H I L E `
   - después: ``
   - por qué: Encabezado de pagina del PDF, "BANCO CENTRAL DE CHILE", capturado letra por letra y con espacios. Es un residuo de la fuente, no texto del acta: la forma normal "BANCO CENTRAL DE CHILE" no aparece ninguna vez en el corpus, o sea que cuando este encabezado esta presente siempre viene letra por letra. Medido: 10 apariciones en 10 filas, mas 1 truncado ("...D E C H"). La politica es eliminar los residuos de la fuente (numeros de pagina, marcas de hora, comillas huerfanas, firmas truncadas) y este es de la misma familia.

### `RPM-2010-10-14:3491:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarla`
   - después: `cambiaria`
   - por qué: cambiarla por cambiaria. Misma familia y mismo defecto. Medido: 8 apariciones (todas dentro de "cambiarlas"), todas adjetivas y revisadas una por una: "paridades cambiarlas" 4 veces, "implicancias cambiarlas" 2, "expectativas cambiarlas" 1, "coberturas cambiarlas" 1. "cambiarias" ya aparece 19 veces en el corpus.

### `RPM-2009-07-09:2653:1` — José De Gregorio Rebeco

1. **ACENTO_FALTANTE**
   - antes: `rca de lo que sería su limite inferior, el cual, a su `
   - después: `rca de lo que sería su límite inferior, el cual, a su `
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2012-09-13:5043:1` — Sergio Lehmann Beresi

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2008-12-11:2240:1` — Beltrán de Ramón Acevedo

1. **ACENTO_FALTANTE**
   - antes: `Señala también que, en linea con lo anterior y d`
   - después: `Señala también que, en línea con lo anterior y d`
   - por qué: Tilde faltante, grupo B3. Se leyeron las 53 apariciones de linea, continua, publica y lineas, y sólo 23 son defecto. «linea»: las 18 son la fórmula «en linea con», siempre el sustantivo, así que van con contexto. «lineas»: las 4 son sustantivo («otras lineas de financiamiento», «algunas lineas manufactureras», «de las lineas vinculadas»). «continua»: de 18 apariciones sólo 2 son el verbo («la actividad económica continua creciendo», «esta parte de la economía continua funcionando»); las otras 16 son el adjetivo continuo/continua y NO se tocan («la continua caída», «la mejora continua», «la convergencia continua y gradual», «la serie no es continua», «de continua colaboración», «de manera continua»). «publica»: las 13 son la tercera persona del verbo publicar («se publica anualmente», «la Reserva Federal no publica su propia», «el INE no los publica», «que publica el Fondo») y ninguna se corrige.

### `RPM-2007-08-09:1398:1` — Jorge Desormeaux Jiménez

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarla`
   - después: `cambiaria`
   - por qué: cambiarla por cambiaria. Misma familia y mismo defecto. Medido: 8 apariciones (todas dentro de "cambiarlas"), todas adjetivas y revisadas una por una: "paridades cambiarlas" 4 veces, "implicancias cambiarlas" 2, "expectativas cambiarlas" 1, "coberturas cambiarlas" 1. "cambiarias" ya aparece 19 veces en el corpus.

### `RPM-2014-02-18:6019:2` — Miguel Ricaurte Bermúdez

1. **ACENTO_INDEBIDO**
   - antes: `ñor Miguel Ricaurte índica que el alza del`
   - después: `ñor Miguel Ricaurte indica que el alza del`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2009-02-12:2320:1` — Sebastián Claro Edwards

1. **ESPACIO_INDEBIDO**
   - antes: `por riesgo , no deberí`
   - después: `por riesgo, no deberí`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **LETRA_CONFUNDIDA**
   - antes: `Defau/t`
   - después: `Default`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene Default y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.

### `RPM-2013-01-17:5277:1` — Sergio Lehmann Beresi

1. **SIMBOLO_SUELTO**
   - antes: `algo mayor en Europa. A Además`
   - después: `algo mayor en Europa. Además`
   - por qué: Letra mayúscula suelta entre dos oraciones. Es ruido de escaneo: la oración anterior termina en punto y la siguiente empieza con mayúscula y sentido completo, así que la letra no pertenece a ninguna de las dos. Medido: 17 casos en 17 filas, con las letras V, H, L, U, A, M, Y, B. Se revisaron uno por uno; el único que NO es residuo es RPM-2007-01-11:1055:1 ("prolongado. A SU juicio"), donde la A abre la oración legítimamente y el defecto es "SU" en mayúscula, que se trata aparte.

### `RPM-2007-01-11:1052:1` — Enrique Marshall Rivera

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.
2. **SIMBOLO_SUELTO**
   - antes: `una y otra dirección. U Sin embargo`
   - después: `una y otra dirección. Sin embargo`
   - por qué: Letra mayúscula suelta entre dos oraciones. Es ruido de escaneo: la oración anterior termina en punto y la siguiente empieza con mayúscula y sentido completo, así que la letra no pertenece a ninguna de las dos. Medido: 17 casos en 17 filas, con las letras V, H, L, U, A, M, Y, B. Se revisaron uno por uno; el único que NO es residuo es RPM-2007-01-11:1055:1 ("prolongado. A SU juicio"), donde la A abre la oración legítimamente y el defecto es "SU" en mayúscula, que se trata aparte.

### `RPM-2011-04-12:3968:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2010-05-13:3107:2` — Beltrán de Ramón Acevedo

1. **ACENTO_INDEBIDO**
   - antes: `íneas y que, por el contrarío, han tenido que`
   - después: `íneas y que, por el contrario, han tenido que`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 271 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
2. **ACENTO_FALTANTE**
   - antes: ` renunciar a lineas externas. Respe`
   - después: ` renunciar a líneas externas. Respe`
   - por qué: Tilde faltante, grupo B3. Se leyeron las 53 apariciones de linea, continua, publica y lineas, y sólo 23 son defecto. «linea»: las 18 son la fórmula «en linea con», siempre el sustantivo, así que van con contexto. «lineas»: las 4 son sustantivo («otras lineas de financiamiento», «algunas lineas manufactureras», «de las lineas vinculadas»). «continua»: de 18 apariciones sólo 2 son el verbo («la actividad económica continua creciendo», «esta parte de la economía continua funcionando»); las otras 16 son el adjetivo continuo/continua y NO se tocan («la continua caída», «la mejora continua», «la convergencia continua y gradual», «la serie no es continua», «de continua colaboración», «de manera continua»). «publica»: las 13 son la tercera persona del verbo publicar («se publica anualmente», «la Reserva Federal no publica su propia», «el INE no los publica», «que publica el Fondo») y ninguna se corrige.

### `RPM-2007-07-12:1321:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `ios gráficos, el efecto fiy to quality sobre Chile s`
   - después: `los gráficos, el efecto fly to quality sobre Chile s`
   - por qué: "fiy"/"fIy" por "fly": la l se leyo como i (o como I). Es el mismo glifo que produce "ai" por "al", demostrado con 26 casos independientes. Se retira la marca RECONSTRUCCION_AMBIGUA que se había puesto en esta fila: al aparecer la regla de glifo, la ambigüedad se resuelve. Un escáner no convierte "flight" en "fiy" (sería borrar cuatro letras); sí convierte "fly" en "fiy". Las 21 apariciones de "flight to quality" que hay en el corpus son la otra grafía, correcta, y no se tocan. La operación se extendió dos caracteres hacia la izquierda para cubrir además "ios" por "los" (§12): ambas caen en el mismo tramo y dos operaciones separadas se pisarían, porque el fragmento anterior empezaba justo en la s de "ios".

### `RPM-2014-06-12:6269:2` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: `eñor Miguel Fuentes índica que el reporte `
   - después: `eñor Miguel Fuentes indica que el reporte `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2013-06-13:5603:1` — Claudio Soto Gamboa

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2015-07-14:6916:1` — Consejo del Banco Central de Chile

1. **LETRA_CONFUNDIDA**
   - antes: `o la volatilidad de ios mercados financ`
   - después: `o la volatilidad de los mercados financ`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2013-01-17:5283:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2012-05-17:4849:3` — Consejo del Banco Central de Chile

1. **RESIDUO_PAGINACION**
   - antes: `En los últimos meses, los Página 31 de 31 indicadores económicos de Estados Unidos`
   - después: `En los últimos meses, los indicadores económicos de Estados Unidos`
   - por qué: Pie de página del PDF original incrustado a mitad de oración, entre 'los' e 'indicadores'. No pertenece al texto: la oración se lee completa sin él. La política de corrección autoriza explícitamente eliminar la numeración de páginas. Medido: el patrón 'Página N de N' aparece 26 veces en 22 filas del corpus, 20 de ellas en la sesión 2012-04-17 que aún está pendiente, 1 aquí y 1 en 5221:3.

### `RPM-2014-12-11:6548:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` \ ·----­ IQUE MARSHALL RIVERA RODRIGO VERGARA MONTES Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2013-09-12:5793:1` — Rodrigo Vergara Montes

1. **PALABRA_OMITIDA**
   - antes: `un grado de desintegración de la economía chilena respecto del resto mundo`
   - después: `un grado de desintegración de la economía chilena respecto del resto del mundo`
   - por qué: Artículo-contracto omitido. Corroborado en la sesión: 'resto del mundo' aparece 3 veces en 2013-09-12 (filas 5771, 5807 y 5811) y 129 veces en el corpus, contra 1 sola de 'resto mundo', que es ésta.

### `RPM-2014-09-11:6397:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `1O`
   - después: `10`
   - por qué: 1O por 10: el cero se leyo como la letra O mayuscula. Medido: 7 apariciones en 6 filas y todas son numeros donde solo cabe el diez ("tasas a 1O años plazo", "lámina Nº 1O", "US$ 3,1O la libra", "a 5 y 1O años", "a 2 y 1O años", "a 1O años", "de 1O o 20%"). Se verifico que no existen apariciones embebidas en otras palabras.

### `RPM-2009-07-09:2622:4` — José De Gregorio Rebeco

1. **ESPACIO_INDEBIDO**
   - antes: ` trimestre .`
   - después: ` trimestre.`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2011-10-13:4342:4` — Sebastián Claro Edwards

1. **ESPACIO_INDEBIDO**
   - antes: `sche Bank— , han decla`
   - después: `sche Bank—, han decla`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
