# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1773**
- operaciones: **3047**
- filas marcadas para cotejo: **232**
- sha256 de la base: `eebaa728dc1d7ce14315caebd0c7516ff324b5d4acaefcf40cec2bf6d855945d`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 731 |
| `ESPACIO_INDEBIDO` | 510 |
| `PALABRA_PARTIDA` | 491 |
| `ACENTO_INDEBIDO` | 386 |
| `PUNTUACION` | 267 |
| `SIMBOLO_SUELTO` | 242 |
| `ACENTO_FALTANTE` | 220 |
| `FIRMA_TRUNCADA` | 55 |
| `ESPACIO_FALTANTE` | 34 |
| `PALABRA_ERRONEA` | 30 |
| `RESIDUO_PAGINACION` | 30 |
| `PALABRA_OMITIDA` | 22 |
| `PALABRA_DUPLICADA` | 16 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2015-04-16:6693:1` — Rodrigo Vergara Montes

1. **ESPACIO_INDEBIDO**
   - antes: `ington D C . A continu`
   - después: `ington D C. A continu`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2011-09-15:4302:1` — Claudio Soto Gamboa

1. **ACENTO_INDEBIDO**
   - antes: `a tasa de los bonos nomínales y reales del Ba`
   - después: `a tasa de los bonos nominales y reales del Ba`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 606 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2009-02-12:2358:1` — María Olivia Recart Herrera

1. **ESPACIO_INDEBIDO**
   - antes: `dit crunch .`
   - después: `dit crunch.`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2005-03-10:171:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `m antener`
   - después: `mantener`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 1788 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2009-11-12:2780:1` — Claudio Soto Gamboa

1. **LETRA_CONFUNDIDA**
   - antes: `IRC`
   - después: `IPC`
   - por qué: IRC por IPC. Medido en todo el corpus: 71 apariciones, ninguna en un contexto donde IRC sea una sigla legitima; 61 sueltas y 10 dentro de IRCX1, que tambien debe leerse IPCX1 porque la misma fila escribe IPCX e IPCX2. Regla de bloque revisada caso por caso.
2. **PUNTUACION**
   - antes: `PM.`
   - después: `PM,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.
3. **ACENTO_FALTANTE**
   - antes: `ril por la reincorporación del impuesto especifico. Con estos nuevos antecedentes, se lleg`
   - después: `ril por la reincorporación del impuesto específico. Con estos nuevos antecedentes, se lleg`
   - por qué: Adjetivo sin acento en «impuesto especifico». El corpus escribe «específico» 46 veces frente a 2, y las dos son esta misma expresión. El verbo «especifica», que aparece decenas de veces, es correcto y no se toca.

### `RPM-2006-06-15:708:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `l precio del cobre, índica que éste ha est`
   - después: `l precio del cobre, indica que éste ha est`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2012-11-13:5204:1` — Joaquín Vial Ruiz-Tagle

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2007-07-12:1335:4` — Igal Magendzo Weinberger

1. **SIMBOLO_SUELTO**
   - antes: `ocesamiento y otros que resultan mayores. fi`
   - después: `ocesamiento y otros que resultan mayores.`
   - por qué: Residuo "fi" al final de la fila, tras una oración que cierra completa en "mayores.". La fila ya viene con motivo FINAL_SIN_PUNTUACION. No es texto: no hay palabra española "fi" y la oración anterior no lo necesita.

### `RPM-2010-06-15:3146:2` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `de Beam Stearns, e`
   - después: `de Bear Stearns, e`
   - por qué: Nombre dañado por OCR: «Beam Stearns» por «Bear Stearns», el banco de inversión cuya quiebra en septiembre de 2008 abre la crisis financiera. Confusión de la erre por la eme, clásica en OCR. Medido en el corpus: «Beam Stearns» aparece 5 veces y «Bear Stearns» 1, de modo que la forma correcta está atestiguada por el propio corpus aunque sea minoritaria; los cinco contextos son inequívocos («cuando alrededor de julio del año 2008», «en el momento en que quebró», «la crisis de»). Se corrige y se deja constancia aquí de que es el primer caso en que la forma canónica es minoritaria: la decisión no descansa en la frecuencia sino en que la entidad es única y el corpus la atestigua.
2. **LETRA_CONFUNDIDA**
   - antes: `ró Beam Stearns. A`
   - después: `ró Bear Stearns. A`
   - por qué: Nombre dañado por OCR: «Beam Stearns» por «Bear Stearns», el banco de inversión cuya quiebra en septiembre de 2008 abre la crisis financiera. Confusión de la erre por la eme, clásica en OCR. Medido en el corpus: «Beam Stearns» aparece 5 veces y «Bear Stearns» 1, de modo que la forma correcta está atestiguada por el propio corpus aunque sea minoritaria; los cinco contextos son inequívocos («cuando alrededor de julio del año 2008», «en el momento en que quebró», «la crisis de»). Se corrige y se deja constancia aquí de que es el primer caso en que la forma canónica es minoritaria: la decisión no descansa en la frecuencia sino en que la entidad es única y el corpus la atestigua.

### `RPM-2015-05-14:6791:1` — Enrique Marshall Rivera

1. **ACENTO_INDEBIDO**
   - antes: `ensar que el efecto Índexación había desaparec`
   - después: `ensar que el efecto indexación había desaparec`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 149 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2009-07-09:2622:1` — Enrique Marshall Rivera

1. **ACENTO_FALTANTE**
   - antes: `la proyección de la economia, lo más probabl`
   - después: `la proyección de la economía, lo más probabl`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.
2. **ESPACIO_INDEBIDO**
   - antes: `va a tener .`
   - después: `va a tener.`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **LETRA_CONFUNDIDA**
   - antes: `Sanco`
   - después: `Banco`
   - por qué: El OCR escribio «S» donde va «B». «Sanco» no es palabra y aparece 7 veces en el corpus, siempre en contextos que solo admiten «Banco»: «el Sanco Central Europeo», «el Sanco Central», «por el Sanco». «Banco» aparece 2.418 veces. Las 7 se leyeron una por una.
4. **PALABRA_PARTIDA**
   - antes: `lo fundamen tal fue`
   - después: `lo fundamental fue`
   - por qué: Palabra partida por un espacio espurio, con la segunda mitad reducida a una letra: «fundamen tal» -> «fundamental». La evidencia es interna y doble: el primer trozo («fundamen») es marginal en el corpus (1 apariciones, y ésas son ésta) y la forma junta («fundamental») es la que el propio corpus usa 167 veces. La encontró detector_partida_letra, agregado en §31 porque detector_partida no puede verla: su guarda «segunda mitad con frecuencia < 50» bloquea justo las letras (a=37.528, o, e, s), que son frecuentes porque este mismo defecto las esparce. Precisión medida del detector: 40 candidatos en las 9.723 filas, 40 verdaderos; el único que no se corrige aquí es el de 147:1, que es la cola de una carrera letra por letra y se arregla entero en su pasada.

### `RPM-2008-11-13:2145:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.

### `RPM-2010-04-15:3049:2` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `nía en el escenario dellPoM.`
   - después: `nía en el escenario del IPoM.`
   - por qué: Sigla dañada por el glifo I/l. Medido en toda la salida: 26 apariciones de esta familia, y cada forma tiene su equivalente correcto ampliamente atestiguado en el corpus (el IPC 1.430, el IPoM 1.543, IPCX 649, IPCX1 469, el IPP 10). Se excluyeron de la pasada "ellPEC", "dellPEC" y "ellMCE" (fila 1719:4): aparecen junto a siglas que no se pueden corroborar en el corpus y no hay reconstruccion unica.

### `RPM-2008-04-10:1773:1` — José De Gregorio Rebeco

1. **PUNTUACION**
   - antes: `12;30 horas`
   - después: `12:30 horas`
   - por qué: Punto y coma donde va dos puntos en una hora. La forma «N:NN horas» aparece 544 veces en el corpus y «N;NN horas» 5, todas ellas este mismo dano.

### `RPM-2007-02-08:1090:4` — Rodrigo Valdés Pulido

1. **LETRA_CONFUNDIDA**
   - antes: `IRC`
   - después: `IPC`
   - por qué: IRC por IPC. Medido en todo el corpus: 71 apariciones, ninguna en un contexto donde IRC sea una sigla legitima; 61 sueltas y 10 dentro de IRCX1, que tambien debe leerse IPCX1 porque la misma fila escribe IPCX e IPCX2. Regla de bloque revisada caso por caso.
2. **ESPACIO_INDEBIDO**
   - antes: `monetaria— , continúa `
   - después: `monetaria—, continúa `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2011-01-13:3716:1` — Consejo del Banco Central de Chile

1. **PALABRA_PARTIDA**
   - antes: `110113-T a sa de Política Monetaria`
   - después: `110113-Tasa de Política Monetaria`
   - por qué: Pase transversal: «Tasa» sale deletreada como «T a sa» dentro del número del Acuerdo. Medido en todo el corpus: la fórmula correcta «Tasa de Política Monetaria» aparece 1.428 veces y la forma deletreada 6, siempre en el mismo lugar —pegada al número del acuerdo, «NN-NN-NNMMDD-T a sa de Política Monetaria»—. No hay ambigüedad: el formato del acuerdo es número-título y el título es siempre el mismo. Se corrige en Texto_Corregido; Texto queda intacto.

### `RPM-2014-06-12:6257:5` — Miguel Fuentes Díaz

1. **RESIDUO_PAGINACION**
   - antes: `uyendo a mantener el crecimiento del sector. 4`
   - después: `uyendo a mantener el crecimiento del sector.`
   - por qué: Residuo de paginación. La oración cierra con punto y después queda un número suelto: es el número de página del acta escaneada. Medido sobre la SALIDA corregida de las 9.724 filas, antes de este pase sólo 3 filas terminaban en « <número>» después de una oración completa, y las tres son iguales. Ojo con la cifra si se remide: en el Texto virgen el mismo patrón da 11, porque otras 8 filas —todas del acta de 2012-04-17— arrastran el pie de página explícito «Sesión N° 184 Página N de 26», que una tanda previa de 24 operaciones RESIDUO_PAGINACION ya retira; en la salida ese pie de página aparece 0 veces. Las dos cifras son ciertas, cada una en su columna. Se elimina el número; Texto queda intacto.

### `RPM-2008-06-10:1853:2` — Sergio Lehmann Beresi

1. **ACENTO_FALTANTE**
   - antes: `l señor Gerente que en linea con lo anterior, la`
   - después: `l señor Gerente que en línea con lo anterior, la`
   - por qué: Tilde faltante, grupo B3. Se leyeron las 53 apariciones de linea, continua, publica y lineas, y sólo 23 son defecto. «linea»: las 18 son la fórmula «en linea con», siempre el sustantivo, así que van con contexto. «lineas»: las 4 son sustantivo («otras lineas de financiamiento», «algunas lineas manufactureras», «de las lineas vinculadas»). «continua»: de 18 apariciones sólo 2 son el verbo («la actividad económica continua creciendo», «esta parte de la economía continua funcionando»); las otras 16 son el adjetivo continuo/continua y NO se tocan («la continua caída», «la mejora continua», «la convergencia continua y gradual», «la serie no es continua», «de continua colaboración», «de manera continua»). «publica»: las 13 son la tercera persona del verbo publicar («se publica anualmente», «la Reserva Federal no publica su propia», «el INE no los publica», «que publica el Fondo») y ninguna se corrige.

### `RPM-2014-04-17:6144:1` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: `a las proyecciones, índica que en línea co`
   - después: `a las proyecciones, indica que en línea co`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2010-06-15:3147:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `Beam Stearns`
   - después: `Bear Stearns`
   - por qué: Nombre dañado por OCR: «Beam Stearns» por «Bear Stearns», el banco de inversión cuya quiebra en septiembre de 2008 abre la crisis financiera. Confusión de la erre por la eme, clásica en OCR. Medido en el corpus: «Beam Stearns» aparece 5 veces y «Bear Stearns» 1, de modo que la forma correcta está atestiguada por el propio corpus aunque sea minoritaria; los cinco contextos son inequívocos («cuando alrededor de julio del año 2008», «en el momento en que quebró», «la crisis de»). Se corrige y se deja constancia aquí de que es el primer caso en que la forma canónica es minoritaria: la decisión no descansa en la frecuencia sino en que la entidad es única y el corpus la atestigua.

### `RPM-2006-05-11:671:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `IPOM`
   - después: `IPoM`
   - por qué: Sigla mal compuesta. Medido en el corpus: «IPoM» aparece 2473 veces y «IPOM» 58, siempre el mismo documento, el Informe de Política Monetaria del Banco Central de Chile, cuya sigla lleva la o minúscula. El OCR leyó la o minúscula como O mayúscula.

### `RPM-2009-10-13:2733:2` — Claudio Soto Gamboa

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2009-03-12:2438:1` — José De Gregorio Rebeco

1. **PUNTUACION**
   - antes: `"adelante de la curva"`
   - después: `“adelante de la curva”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.
2. **ESPACIO_INDEBIDO**
   - antes: `nominalizó , pero se p`
   - después: `nominalizó, pero se p`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **LETRA_CONFUNDIDA**
   - antes: `í\/lonetaria`
   - después: `Monetaria`
   - por qué: La OCR escribe la «M» como una secuencia de glifos con barra invertida. El corpus tiene «Monetaria» 3248 veces y no tiene ninguna forma legítima con esa secuencia.

### `RPM-2006-12-14:1003:6` — Igal Magendzo Weinberger

1. **LETRA_CONFUNDIDA**
   - antes: `ria de inversión, el Gerente señor ígal Madgenzo, señaló que las importaciones de bienes`
   - después: `ria de inversión, el Gerente señor Igal Magendzo, señaló que las importaciones de bienes`
   - por qué: Normalización de nombre propio dañado, autorizada por el usuario en esta ronda (el criterio anterior era marcar sin corregir). La forma canónica la acreditan el corpus y el roster de la sesión: «Magendzo» aparece 416 veces en la salida, contra 18 de la forma dañada. Se corrige en Texto_Corregido; Texto queda intacto. Lo que no tiene forma canónica atestiguada (por ejemplo «Miguel Angel Nacrur Gazali») sigue marcado NOMBRE_PROPIO_POR_COTEJAR. Extensión del §57: el mismo tramo llevaba también el nombre de pila dañado, «ígal» con í minúscula acentuada en vez de «Igal». Medido en el corpus: «Igal» aparece 131 veces y «ígal» 1, siempre el mismo Gerente de Análisis Macroeconómico, Igal Magendzo Weinberger.

### `RPM-2011-06-14:4114:1` — Enrique Marshall Rivera

1. **ACENTO_INDEBIDO**
   - antes: `perimentado ajustes margínales. Informa que pa`
   - después: `perimentado ajustes marginales. Informa que pa`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 113 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2010-08-12:3340:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2012-09-13:5085:1` — Joaquín Vial Ruiz-Tagle

1. **SIMBOLO_SUELTO**
   - antes: `as variables en los próximos meses. 4 / ■ En consideración a que aún no se`
   - después: `as variables en los próximos meses. En consideración a que aún no se`
   - por qué: Símbolo ■ con basura adyacente, residuo del escaneo. El tipo SIMBOLO_SUELTO fue creado justamente para estos casos («■V», «ry _<< ■» -> se elimina). Medido: 21 apariciones en 20 filas. Se trata cada una con su basura propia porque el ruido que la acompaña varía (■o J, ■,\y, ■', ■J, ■V, / ■ ' /, 4 / ■, i - /■, — f ■, ry _<< ■). En todos los casos las dos oraciones que rodean el residuo quedan completas sin él. Excepción: en 5802:2 se elimina solo el ■ y se deja el paréntesis abierto, porque esa fila ya está marcada RECONSTRUCCION_AMBIGUA_POR_COTEJAR con motivo FINAL_SIN_PUNTUACION.

### `RPM-2015-02-12:6618:3` — Miguel Fuentes Díaz

1. **ESPACIO_FALTANTE**
   - antes: `que sube a100%`
   - después: `que sube a 100%`
   - por qué: Falta el espacio entre la preposición y la cifra: «a100%» no es una palabra. Mismo caso ya registrado en el corpus («un13% en febrero» → «un 13%»).

### `RPM-2010-06-15:3155:1` — Claudio Soto Gamboa

1. **PUNTUACION**
   - antes: `rial.`
   - después: `rial,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.

### `RPM-2010-04-15:3023:1` — Consejo del Banco Central de Chile

1. **ESPACIO_FALTANTE**
   - antes: `celebrada el15 de abril de 2010`
   - después: `celebrada el 15 de abril de 2010`
   - por qué: Falta el espacio entre el artículo y la cifra en el encabezado formulaico del acta. Evidencia de fuente: el PDF de 2005-06-09, de la misma serie, escribe el mismo encabezado con espacio («Celebrada el 9 de junio de 2005»), mientras el de 2005-07-12 sale pegado («celebrada el12»); la diferencia es un artefacto de extracción, no una variante del acta. La fecha queda confirmada por el cuerpo de la misma oración y por el nombre del archivo.
