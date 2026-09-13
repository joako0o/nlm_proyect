# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1761**
- operaciones: **3032**
- filas marcadas para cotejo: **231**
- sha256 de la base: `eebaa728dc1d7ce14315caebd0c7516ff324b5d4acaefcf40cec2bf6d855945d`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 730 |
| `ESPACIO_INDEBIDO` | 510 |
| `PALABRA_PARTIDA` | 491 |
| `ACENTO_INDEBIDO` | 385 |
| `PUNTUACION` | 267 |
| `SIMBOLO_SUELTO` | 242 |
| `ACENTO_FALTANTE` | 220 |
| `FIRMA_TRUNCADA` | 55 |
| `ESPACIO_FALTANTE` | 34 |
| `PALABRA_ERRONEA` | 30 |
| `RESIDUO_PAGINACION` | 30 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |
| `PALABRA_DUPLICADA` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2015-05-14:6755:1` — Consejo del Banco Central de Chile

1. **LETRA_CONFUNDIDA**
   - antes: `epartamento Análisis Internacional, don Diego Gianellí Gómez; Asesor del Ministerio de Haciend`
   - después: `epartamento Análisis Internacional, don Diego Gianelli Gómez; Asesor del Ministerio de Haciend`
   - por qué: Normalización de nombre propio dañado, autorizada por el usuario en esta ronda (el criterio anterior era marcar sin corregir). La forma canónica la acreditan el corpus y el roster de la sesión: «Diego Gianelli» aparece 117 veces en la salida, contra 7 de la forma dañada. Se corrige en Texto_Corregido; Texto queda intacto. Lo que no tiene forma canónica atestiguada (por ejemplo «Miguel Angel Nacrur Gazali») sigue marcado NOMBRE_PROPIO_POR_COTEJAR.

### `RPM-2011-10-13:4360:2` — Claudio Soto Gamboa

1. **LETRA_CONFUNDIDA**
   - antes: `una magnitud bastante más acotada que ei registrado en el año 2008`
   - después: `una magnitud bastante más acotada que el registrado en el año 2008`
   - por qué: I latina en lugar de ele: 'ei' no es palabra. El artículo es obligado porque el mismo enunciado trae 'en el año 2008' inmediatamente después.

### `RPM-2009-03-12:2386:2` — Sergio Lehmann Beresi

1. **ESPACIO_INDEBIDO**
   - antes: `s regiones , y que se `
   - después: `s regiones, y que se `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **ESPACIO_INDEBIDO**
   - antes: `importante , y que ya `
   - después: `importante, y que ya `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: ` Forecasts ,es decir,u`
   - después: ` Forecasts,es decir,u`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2005-03-10:171:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `m antener`
   - después: `mantener`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 1788 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2009-11-12:2798:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `Continuando con la votación,.`
   - después: `Continuando con la votación,`
   - por qué: Coma seguida de punto al final de la fila. Medido en el corpus: «<palabra>,.» aparece 98 veces en el texto virgen; el pase transversal del §45 corrigió 78 (76 «A continuación,.» más «década,.» y «Euro,.») y dejó estas 20, que son la misma familia con otras palabras: «Continuando con la votación,.» (6), «Para concluir con la votación,.» (3), «No habiendo más comentarios,.» (8), «No habiendo más comentarios y preguntas,.» (2) y «…señor Manuel Marfán,.» (1). En los 20 casos la fila siguiente empieza con «el Presidente…», «el Consejero…» o «el Vicepresidente…», de modo que la coma es la marca correcta y el punto es el signo sobrante. Se aplica el mismo criterio del §45.

### `RPM-2006-06-15:708:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `l precio del cobre, índica que éste ha est`
   - después: `l precio del cobre, indica que éste ha est`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2012-12-13:5261:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **ACENTO_INDEBIDO**
   - antes: `ses, por el tipo de financíamiento externo que se `
   - después: `ses, por el tipo de financiamiento externo que se `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 440 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2007-07-12:1335:4` — Igal Magendzo Weinberger

1. **SIMBOLO_SUELTO**
   - antes: `ocesamiento y otros que resultan mayores. fi`
   - después: `ocesamiento y otros que resultan mayores.`
   - por qué: Residuo "fi" al final de la fila, tras una oración que cierra completa en "mayores.". La fila ya viene con motivo FINAL_SIN_PUNTUACION. No es texto: no hay palabra española "fi" y la oración anterior no lo necesita.

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

### `RPM-2015-06-11:6814:1` — Diego Gianelli Gómez

1. **ESPACIO_INDEBIDO**
   - antes: `res meses— , los sprea`
   - después: `res meses—, los sprea`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **ESPACIO_INDEBIDO**
   - antes: ` y 5 años— , y los spr`
   - después: ` y 5 años—, y los spr`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: `y 10 años— . De acuerd`
   - después: `y 10 años—. De acuerd`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2009-07-09:2633:1` — Manuel Marfán Lewis

1. **SIMBOLO_SUELTO**
   - antes: `oblemas. r . Sobre los`
   - después: `oblemas. Sobre los`
   - por qué: Espacio insertado antes del signo (§18: en español el signo va pegado a la palabra que lo precede). AMPLIADA en §32: el tramo contiene además una «r» suelta entre dos oraciones completas («...la que puede resolver ese tipo de problemas. [r.] Sobre los indicadores bursátiles...»), y como cae DENTRO de este tramo no se le puede apilar una operación propia (§15). Se quita también. Medido: la «r» suelta entre oraciones aparece 6 veces en 6 filas (2362:1, 2428:1 «r 4/», 2578:1 «r -», ésta, 3134:1, 4510:1 «r "») y las 6 son residuo; a diferencia de la «V» de §8 ter (11 residuos contra 2 figuras legítimas), la «r» no tiene ningún uso legítimo atestiguado en el corpus. El Tipo pasa a SIMBOLO_SUELTO porque lo que sobrevive del arreglo es quitar un símbolo que sobra, no un espacio (§22).

### `RPM-2008-12-11:2185:2` — Sergio Lehmann Beresi

1. **ESPACIO_INDEBIDO**
   - antes: `l petróleo , se apreci`
   - después: `l petróleo, se apreci`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **PALABRA_PARTIDA**
   - antes: `ha efectuad o simplemente`
   - después: `ha efectuado simplemente`
   - por qué: Palabra partida por un espacio espurio, con la segunda mitad reducida a una letra: «efectuad o» -> «efectuado». La evidencia es interna y doble: el primer trozo («efectuad») es marginal en el corpus (1 apariciones, y ésas son ésta) y la forma junta («efectuado») es la que el propio corpus usa 134 veces. La encontró detector_partida_letra, agregado en §31 porque detector_partida no puede verla: su guarda «segunda mitad con frecuencia < 50» bloquea justo las letras (a=37.528, o, e, s), que son frecuentes porque este mismo defecto las esparce. Precisión medida del detector: 40 candidatos en las 9.723 filas, 40 verdaderos; el único que no se corrige aquí es el de 147:1, que es la cola de una carrera letra por letra y se arregla entero en su pasada.

### `RPM-2010-04-15:3075:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `Para concluir con la votación,.`
   - después: `Para concluir con la votación,`
   - por qué: Coma seguida de punto al final de la fila. Medido en el corpus: «<palabra>,.» aparece 98 veces en el texto virgen; el pase transversal del §45 corrigió 78 (76 «A continuación,.» más «década,.» y «Euro,.») y dejó estas 20, que son la misma familia con otras palabras: «Continuando con la votación,.» (6), «Para concluir con la votación,.» (3), «No habiendo más comentarios,.» (8), «No habiendo más comentarios y preguntas,.» (2) y «…señor Manuel Marfán,.» (1). En los 20 casos la fila siguiente empieza con «el Presidente…», «el Consejero…» o «el Vicepresidente…», de modo que la coma es la marca correcta y el punto es el signo sobrante. Se aplica el mismo criterio del §45.
2. **SIMBOLO_SUELTO**
   - antes: ` \ `
   - después: ` `
   - por qué: Barra invertida suelta, residuo de salto de línea del PDF. Medido en el corpus: aparece 11 veces rodeada de espacios, siempre entre dos palabras que pertenecen a la misma oración.

### `RPM-2008-04-10:1781:1` — Enrique Marshall Rivera

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarla`
   - después: `cambiaria`
   - por qué: cambiarla por cambiaria. Misma familia y mismo defecto. Medido: 8 apariciones (todas dentro de "cambiarlas"), todas adjetivas y revisadas una por una: "paridades cambiarlas" 4 veces, "implicancias cambiarlas" 2, "expectativas cambiarlas" 1, "coberturas cambiarlas" 1. "cambiarias" ya aparece 19 veces en el corpus.

### `RPM-2007-02-08:1090:4` — Rodrigo Valdés Pulido

1. **LETRA_CONFUNDIDA**
   - antes: `IRC`
   - después: `IPC`
   - por qué: IRC por IPC. Medido en todo el corpus: 71 apariciones, ninguna en un contexto donde IRC sea una sigla legitima; 61 sueltas y 10 dentro de IRCX1, que tambien debe leerse IPCX1 porque la misma fila escribe IPCX e IPCX2. Regla de bloque revisada caso por caso.
2. **ESPACIO_INDEBIDO**
   - antes: `monetaria— , continúa `
   - después: `monetaria—, continúa `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2011-02-17:3812:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.

### `RPM-2014-06-12:6293:1` — Rodrigo Vergara Montes

1. **ACENTO_INDEBIDO**
   - antes: `emás, los costos de fínanciamiento se encuentran e`
   - después: `emás, los costos de financiamiento se encuentran e`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 440 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2008-06-10:1860:3` — Jorge Desormeaux Jiménez

1. **ESPACIO_INDEBIDO**
   - antes: `de América . Habrá pre`
   - después: `de América. Habrá pre`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2014-05-15:6222:1` — Luis Óscar Herrera Barriga

1. **SIMBOLO_SUELTO**
   - antes: `precio del cobre. Y En el plano local`
   - después: `precio del cobre. En el plano local`
   - por qué: Letra mayúscula suelta entre dos oraciones. Es ruido de escaneo: la oración anterior termina en punto y la siguiente empieza con mayúscula y sentido completo, así que la letra no pertenece a ninguna de las dos. Medido: 17 casos en 17 filas, con las letras V, H, L, U, A, M, Y, B. Se revisaron uno por uno; el único que NO es residuo es RPM-2007-01-11:1055:1 ("prolongado. A SU juicio"), donde la A abre la oración legítimamente y el defecto es "SU" en mayúscula, que se trata aparte.

### `RPM-2010-06-15:3202:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `en matemáticamente. P or todo lo anterio`
   - después: `en matemáticamente. Por todo lo anterio`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 3613 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2006-05-11:671:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `IPOM`
   - después: `IPoM`
   - por qué: Sigla mal compuesta. Medido en el corpus: «IPoM» aparece 2473 veces y «IPOM» 58, siempre el mismo documento, el Informe de Política Monetaria del Banco Central de Chile, cuya sigla lleva la o minúscula. El OCR leyó la o minúscula como O mayúscula.

### `RPM-2009-10-13:2754:2` — Enrique Marshall Rivera

1. **SIMBOLO_SUELTO**
   - antes: `su exposición agradeciendo al staff por e\ apoyo brindado. El señor Cons`
   - después: `su exposición agradeciendo al staff por el apoyo brindado. El señor Cons`
   - por qué: «staff el <sustantivo>» es la formula del corpus, que tiene 427 «staff» y escribe «agradece el analisis del staff», «agradece al staff los Informes», «agradece al staff, por los informes»: el articulo es obligatorio y no existe la forma «staff e». La barra invertida es la «l» leida por el OCR, el mismo glifo de §21-§22 al reves, y se repite 9 veces en 9 sesiones distintas con la misma estructura, por lo que la lectura no es una intuicion: es una familia (§8 bis). §32.

### `RPM-2009-04-09:2463:2` — Andrés Velasco Brañes

1. **LETRA_CONFUNDIDA**
   - antes: `i\/linistro`
   - después: `Ministro`
   - por qué: La OCR escribe la «M» como una secuencia de glifos con barra invertida. El corpus tiene «Ministro» 1419 veces y no tiene ninguna forma legítima con esa secuencia.

### `RPM-2006-12-14:1003:6` — Igal Magendzo Weinberger

1. **LETRA_CONFUNDIDA**
   - antes: `ria de inversión, el Gerente señor ígal Madgenzo, señaló que las importaciones de bienes`
   - después: `ria de inversión, el Gerente señor Igal Magendzo, señaló que las importaciones de bienes`
   - por qué: Normalización de nombre propio dañado, autorizada por el usuario en esta ronda (el criterio anterior era marcar sin corregir). La forma canónica la acreditan el corpus y el roster de la sesión: «Magendzo» aparece 416 veces en la salida, contra 18 de la forma dañada. Se corrige en Texto_Corregido; Texto queda intacto. Lo que no tiene forma canónica atestiguada (por ejemplo «Miguel Angel Nacrur Gazali») sigue marcado NOMBRE_PROPIO_POR_COTEJAR. Extensión del §57: el mismo tramo llevaba también el nombre de pila dañado, «ígal» con í minúscula acentuada en vez de «Igal». Medido en el corpus: «Igal» aparece 131 veces y «ígal» 1, siempre el mismo Gerente de Análisis Macroeconómico, Igal Magendzo Weinberger.

### `RPM-2011-07-14:4205:1` — Rodrigo Vergara Montes

1. **ESPACIO_INDEBIDO**
   - antes: `entemente— , porque ha`
   - después: `entemente—, porque ha`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2010-10-14:3434:2` — Felipe Jaque

1. **ACENTO_FALTANTE**
   - antes: `ipe Jaque inicia su exposicion, revisando los `
   - después: `ipe Jaque inicia su exposición, revisando los `
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.
2. **ESPACIO_INDEBIDO**
   - antes: `s regiones . Señala qu`
   - después: `s regiones. Señala qu`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: `l respecto , hace nota`
   - después: `l respecto, hace nota`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
4. **ESPACIO_INDEBIDO**
   - antes: `es de12011 .`
   - después: `es de12011.`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2012-10-18:5149:1` — Felipe Larraín Bascuñán

1. **ACENTO_INDEBIDO**
   - antes: `gentes, así como la íncertidumbre que aún persist`
   - después: `gentes, así como la incertidumbre que aún persist`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 861 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2015-03-19:6679:1` — Alberto Naudon Dell'Oro

1. **ESPACIO_INDEBIDO**
   - antes: ` internas— . No obstan`
   - después: ` internas—. No obstan`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2010-06-15:3205:2` — Consejo del Banco Central de Chile

1. **PALABRA_PARTIDA**
   - antes: `100615-T a sa de Política Monetaria`
   - después: `100615-Tasa de Política Monetaria`
   - por qué: Pase transversal: «Tasa» sale deletreada como «T a sa» dentro del número del Acuerdo. Medido en todo el corpus: la fórmula correcta «Tasa de Política Monetaria» aparece 1.428 veces y la forma deletreada 6, siempre en el mismo lugar —pegada al número del acuerdo, «NN-NN-NNMMDD-T a sa de Política Monetaria»—. No hay ambigüedad: el formato del acuerdo es número-título y el título es siempre el mismo. Se corrige en Texto_Corregido; Texto queda intacto.

### `RPM-2010-04-15:3050:3` — Claudio Soto Gamboa

1. **LETRA_CONFUNDIDA**
   - antes: `Claudia Soto`
   - después: `Claudio Soto`
   - por qué: La «a» final ocupó el lugar de la «o» en el nombre de pila. El propio texto lo descarta: la fila lo trata en masculino («señor» o «don») y el corpus atestigua «Claudio Soto» 1.275 veces contra 2 «Claudia Soto». No es la Claudia legítima del corpus (doña Claudia Varela Lértora, doña Claudia Sotz Pantoja), que siempre va con «doña» o «Gerenta».
