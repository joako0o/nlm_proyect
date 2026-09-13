# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1714**
- operaciones: **2916**
- filas marcadas para cotejo: **215**
- sha256 de la base: `32752bd52ce5d3b50b0732780154aaef23482908f6671f92a327509e75edf452`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 664 |
| `ESPACIO_INDEBIDO` | 509 |
| `PALABRA_PARTIDA` | 491 |
| `ACENTO_INDEBIDO` | 385 |
| `PUNTUACION` | 267 |
| `ACENTO_FALTANTE` | 216 |
| `SIMBOLO_SUELTO` | 204 |
| `FIRMA_TRUNCADA` | 55 |
| `PALABRA_ERRONEA` | 30 |
| `RESIDUO_PAGINACION` | 30 |
| `ESPACIO_FALTANTE` | 27 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |
| `PALABRA_DUPLICADA` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

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

### `RPM-2012-03-15:4722:3` — Felipe Larraín Bascuñán

1. **ACENTO_INDEBIDO**
   - antes: ` enero, en términos nomínales, el índice de r`
   - después: ` enero, en términos nominales, el índice de r`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 606 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
2. **ESPACIO_INDEBIDO**
   - antes: `cieron 1,3 % interanua`
   - después: `cieron 1,3% interanua`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: `cieron 1,1 % mes a mes`
   - después: `cieron 1,1% mes a mes`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
4. **PALABRA_ERRONEA**
   - antes: `los efectos e la crisis externa`
   - después: `los efectos de la crisis externa`
   - por qué: Preposición truncada: falta la d de «de». Es el único caso de «e la» en el corpus que no es una palabra deletreada.

### `RPM-2009-03-12:2428:1` — Pablo García Silva

1. **ACENTO_FALTANTE**
   - antes: `de aquí en adelante cabria esperar movimie`
   - después: `de aquí en adelante cabría esperar movimie`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2005-03-10:171:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `m antener`
   - después: `mantener`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 1788 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2010-01-14:2854:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `No habiendo más comentarios,.`
   - después: `No habiendo más comentarios,`
   - por qué: Coma seguida de punto al final de la fila. Medido en el corpus: «<palabra>,.» aparece 98 veces en el texto virgen; el pase transversal del §45 corrigió 78 (76 «A continuación,.» más «década,.» y «Euro,.») y dejó estas 20, que son la misma familia con otras palabras: «Continuando con la votación,.» (6), «Para concluir con la votación,.» (3), «No habiendo más comentarios,.» (8), «No habiendo más comentarios y preguntas,.» (2) y «…señor Manuel Marfán,.» (1). En los 20 casos la fila siguiente empieza con «el Presidente…», «el Consejero…» o «el Vicepresidente…», de modo que la coma es la marca correcta y el punto es el signo sobrante. Se aplica el mismo criterio del §45.

### `RPM-2006-07-13:752:1` — Enrique Marshall Rivera

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2013-03-14:5422:1` — Claudio Soto Gamboa

1. **ACENTO_INDEBIDO**
   - antes: `ran los patrones de índexación habituales. En `
   - después: `ran los patrones de indexación habituales. En `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 149 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2007-08-09:1363:1` — Pablo García Silva

1. **PALABRA_PARTIDA**
   - antes: `tem a`
   - después: `tema`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 784 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.

### `RPM-2010-07-15:3261:1` — Claudio Soto Gamboa

1. **PUNTUACION**
   - antes: `ue.`
   - después: `ue,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.

### `RPM-2015-08-13:6965:1` — Beltrán de Ramón Acevedo

1. **LETRA_CONFUNDIDA**
   - antes: `el único factor importante de riesgo que queda, y que presiona los precios, es la depreciación cambiaría, pero que finalmente`
   - después: `el único factor importante de riesgo que queda, y que presiona los precios, es la depreciación cambiaria, pero que finalmente`
   - por qué: Tilde por i en posición de adjetivo. Sección 3 ter: la familia 'cambiar*' se corrige sin corroboración porque la forma verbal es imposible en este lugar.
2. **PUNTUACION**
   - antes: `que están “incómodos" con la inflación headline`
   - después: `que están “incómodos” con la inflación headline`
   - por qué: Comilla recta usada como cierre de una apertura curva. Es un PAR MIXTO y por eso es defecto sin ambigüedad: la fila tiene 1 apertura curva, 0 cierres curvos y 1 recta, así que esa recta sólo puede ser el cierre que falta. MEDIDO EN TODO EL CORPUS: de las 123 comillas rectas, 52 cierran una apertura curva (par mixto, defecto seguro) y 71 son otra cosa, entre ellas pares enteramente rectos como '"dilema del prisionero"' de esta misma sesión o '"commodities"' en 1257:1, que no se tocan porque ahí no hay desequilibrio que pruebe el defecto. Aperturas curvas 323, cierres curvos 267, rectas 123 en 91 filas, y 65 filas tienen más aperturas que cierres.

### `RPM-2009-08-13:2681:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.
2. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
3. **ACENTO_INDEBIDO**
   - antes: `medidas complementarías posibles`
   - después: `medidas complementarias posibles`
   - por qué: El adjetivo «complementarias» no lleva tilde; la forma esdrújula «complementarías» sería la segunda persona del condicional, que no cabe después de «medidas» y antes de «posibles». Medido: «complementarías» aparece 1 sola vez en todo el corpus y «complementarias» 47. En la misma fila, además, el sustantivo del que deriva se usa bien.

### `RPM-2008-12-11:2227:4` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `del crédit crunch`
   - después: `del credit crunch`
   - por qué: Acento indebido en un anglicismo. Medido en el corpus: «credit crunch» aparece 10 veces y «crédit crunch» 1.

### `RPM-2010-06-15:3164:1` — Claudio Soto Gamboa

1. **PALABRA_PARTIDA**
   - antes: `m ás`
   - después: `más`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 11942 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

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

### `RPM-2011-05-12:4052:2` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2014-10-16:6480:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2008-07-10:1917:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `idente, consulta si ellPP es mucho más in`
   - después: `idente, consulta si el IPP es mucho más in`
   - por qué: Sigla dañada por el glifo I/l. Medido en toda la salida: 26 apariciones de esta familia, y cada forma tiene su equivalente correcto ampliamente atestiguado en el corpus (el IPC 1.430, el IPoM 1.543, IPCX 649, IPCX1 469, el IPP 10). Se excluyeron de la pasada "ellPEC", "dellPEC" y "ellMCE" (fila 1719:4): aparecen junto a siglas que no se pueden corroborar en el corpus y no hay reconstruccion unica.
2. **LETRA_CONFUNDIDA**
   - antes: ` ellPC `
   - después: ` el IPC `
   - por qué: Sigla dañada por el glifo I/l. Medido en toda la salida: 26 apariciones de esta familia, y cada forma tiene su equivalente correcto ampliamente atestiguado en el corpus (el IPC 1.430, el IPoM 1.543, IPCX 649, IPCX1 469, el IPP 10). Se excluyeron de la pasada "ellPEC", "dellPEC" y "ellMCE" (fila 1719:4): aparecen junto a siglas que no se pueden corroborar en el corpus y no hay reconstruccion unica.

### `RPM-2014-08-14:6382:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `e desde el punto de vísta de los precios,`
   - después: `e desde el punto de vista de los precios,`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 501 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2010-07-15:3261:2` — José De Gregorio Rebeco

1. **ACENTO_FALTANTE**
   - antes: `dente señor José De Gregorio plantea que seria interesante rep`
   - después: `dente señor José De Gregorio plantea que sería interesante rep`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.

### `RPM-2006-06-15:693:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `recio del cobre tenía ai país bastante eufóric`
   - después: `recio del cobre tenía al país bastante eufóric`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2009-11-12:2799:1` — Jorge Desormeaux Jiménez

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.
2. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
3. **ACENTO_FALTANTE**
   - antes: `tido de mantener un estimulo monetario prolo`
   - después: `tido de mantener un estímulo monetario prolo`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.

### `RPM-2009-05-07:2510:2` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `ue han continuado / ios ajustes, partic`
   - después: `ue han continuado / los ajustes, partic`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.
2. **LETRA_CONFUNDIDA**
   - antes: `TPÍ\/I`
   - después: `TPM`
   - por qué: La OCR escribe la «M» como una secuencia de glifos con barra invertida. El corpus tiene «TPM» 1822 veces y no tiene ninguna forma legítima con esa secuencia.
3. **LETRA_CONFUNDIDA**
   - antes: `í\/línistro`
   - después: `Ministro`
   - por qué: La OCR escribe la «M» como una secuencia de glifos con barra invertida. El corpus tiene «Ministro» 1419 veces y no tiene ninguna forma legítima con esa secuencia.

### `RPM-2006-12-14:1021:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` )RIO CORBO LIOI Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2011-10-13:4396:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `una elevada volatilidad cambiaría`
   - después: `una elevada volatilidad cambiaria`
   - por qué: El adjetivo 'cambiaria' no lleva tilde; con tilde es el condicional del verbo cambiar y aquí modifica a 'volatilidad'. Es la confusión sistemática más frecuente del corpus: 'cambiaría' por 'cambiaria' aparece 204 veces y siempre se ha corregido cuando la fila lo permite. Esta fila no trae la forma correcta, pero el adjetivo es el único que cabe.

### `RPM-2010-11-16:3579:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarla`
   - después: `cambiaria`
   - por qué: cambiarla por cambiaria. Misma familia y mismo defecto. Medido: 8 apariciones (todas dentro de "cambiarlas"), todas adjetivas y revisadas una por una: "paridades cambiarlas" 4 veces, "implicancias cambiarlas" 2, "expectativas cambiarlas" 1, "coberturas cambiarlas" 1. "cambiarias" ya aparece 19 veces en el corpus.

### `RPM-2013-02-14:5334:1` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2015-07-14:6885:1` — Miguel Fuentes Díaz

1. **ESPACIO_INDEBIDO**
   - antes: ` anterior— ; y en adel`
   - después: ` anterior—; y en adel`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2010-07-15:3264:1` — Sebastián Claro Edwards

1. **PUNTUACION**
   - antes: `PM.`
   - después: `PM,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.

### `RPM-2010-06-15:3131:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.
