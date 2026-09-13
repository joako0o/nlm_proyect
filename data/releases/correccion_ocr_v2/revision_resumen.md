# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1719**
- operaciones: **2946**
- filas marcadas para cotejo: **215**
- sha256 de la base: `eebaa728dc1d7ce14315caebd0c7516ff324b5d4acaefcf40cec2bf6d855945d`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 689 |
| `ESPACIO_INDEBIDO` | 510 |
| `PALABRA_PARTIDA` | 491 |
| `ACENTO_INDEBIDO` | 385 |
| `PUNTUACION` | 267 |
| `ACENTO_FALTANTE` | 216 |
| `SIMBOLO_SUELTO` | 208 |
| `FIRMA_TRUNCADA` | 55 |
| `PALABRA_ERRONEA` | 30 |
| `RESIDUO_PAGINACION` | 30 |
| `ESPACIO_FALTANTE` | 27 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |
| `PALABRA_DUPLICADA` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2015-07-14:6910:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2012-02-14:4654:1` — Consejo del Banco Central de Chile

1. **ESPACIO_INDEBIDO**
   - antes: `taria en 5 % anual. En`
   - después: `taria en 5% anual. En`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **PUNTUACION**
   - antes: `120214 – Tasa`
   - después: `120214 - Tasa`
   - por qué: Raya en vez de guion como separador del número de acuerdo. Medido en el corpus: 129 filas usan el guion y 2 la raya, en la misma posición fija de la fórmula del Acuerdo.

### `RPM-2009-03-12:2405:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `De Gregario`
   - después: `De Gregorio`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).

### `RPM-2005-03-10:171:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `m antener`
   - después: `mantener`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 1788 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2010-01-14:2851:1` — Pablo García Silva

1. **PUNTUACION**
   - antes: `"respirador artificial"`
   - después: `“respirador artificial”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.

### `RPM-2006-07-13:752:1` — Enrique Marshall Rivera

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2013-03-14:5406:1` — Enrique Marshall Rivera

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2007-08-09:1363:1` — Pablo García Silva

1. **PALABRA_PARTIDA**
   - antes: `tem a`
   - después: `tema`
   - por qué: El OCR esparcio la palabra en trozos cortos separados por espacios. Detectado por pasada transversal sobre las 9.723 filas: la forma unida aparece 784 veces en el corpus y al menos un trozo por separado no es una palabra corriente, asi que los espacios no pueden ser reales. Tipo PALABRA_PARTIDA.

### `RPM-2010-07-15:3249:2` — Claudio Soto Gamboa

1. **ESPACIO_INDEBIDO**
   - antes: `ra el 2010 . Con ello,`
   - después: `ra el 2010. Con ello,`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2015-08-13:6955:1` — Beltrán de Ramón Acevedo

1. **PALABRA_PARTIDA**
   - antes: `El Gerente de División Operaciones Financieras señor Beltrán de Ramón tam bién expresa su preocupación`
   - después: `El Gerente de División Operaciones Financieras señor Beltrán de Ramón también expresa su preocupación`
   - por qué: Palabra partida por un espacio intrapalabra. Sección 1 ter: se reúne sin alterar una letra, así que no hay lectura alternativa que proteger y no se pide corroboración. Segunda ocurrencia de 'tam bién' en esta sesión.
2. **PALABRA_PARTIDA**
   - antes: `el dato de la EEE, en el año 2008 se elevó a 3,3%, retornó a 3% y term inó en 3,9%`
   - después: `el dato de la EEE, en el año 2008 se elevó a 3,3%, retornó a 3% y terminó en 3,9%`
   - por qué: Palabra partida por un espacio intrapalabra. Sección 1 ter: se reúne sin alterar una letra, así que no hay lectura alternativa que proteger y no se pide corroboración.
3. **PALABRA_PARTIDA**
   - antes: `y en el año 2011, se elevó levemente, pero previamente comenzó a aum entar su desviación respecto de la EOF`
   - después: `y en el año 2011, se elevó levemente, pero previamente comenzó a aumentar su desviación respecto de la EOF`
   - por qué: Palabra partida por un espacio intrapalabra. Sección 1 ter: se reúne sin alterar una letra, así que no hay lectura alternativa que proteger y no se pide corroboración.
4. **PALABRA_PARTIDA**
   - antes: `Hoy, en cambio, la EEE a dos años exhibe una desviación mínima, la menor en térm inos históricos`
   - después: `Hoy, en cambio, la EEE a dos años exhibe una desviación mínima, la menor en términos históricos`
   - por qué: Palabra partida por un espacio intrapalabra. Sección 1 ter: se reúne sin alterar una letra, así que no hay lectura alternativa que proteger y no se pide corroboración. Cuarta palabra partida en esta misma fila: el escaneo de esta página va partiendo palabras de a una.

### `RPM-2009-08-13:2680:2` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `Siendo las 16; 15 horas`
   - después: `Siendo las 16:15 horas`
   - por qué: Punto y coma en vez de los dos puntos de la hora. Medido en el corpus: el patrón «Siendo las HH:MM horas» aparece 106 veces y las 106 con dos puntos; «16; 15» aparece 1 sola vez. Y la fila anterior del mismo padre lo confirma sin dejar duda: «la sesión de la tarde comenzará a las 16:15 horas». Es la misma hora, escrita bien un renglón antes.

### `RPM-2008-12-11:2227:4` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `del crédit crunch`
   - después: `del credit crunch`
   - por qué: Acento indebido en un anglicismo. Medido en el corpus: «credit crunch» aparece 10 veces y «crédit crunch» 1.

### `RPM-2010-06-15:3143:1` — José De Gregorio Rebeco

1. **PUNTUACION**
   - antes: `rothers.,`
   - después: `rothers,`
   - por qué: Punto antes de una coma. Medido en el corpus: «.,» aparece 24 veces en el texto corregido, pero 20 son legítimas (abreviaturas «EE.UU.», «S.A.», «etc.», «v.gr.» e iniciales de nombre como «Velasco B.,»). Las 4 restantes tienen antes una palabra completa en minúscula o un signo de porcentaje, no una abreviatura, y el punto es sobrante.
2. **LETRA_CONFUNDIDA**
   - antes: `Beam Stearns`
   - después: `Bear Stearns`
   - por qué: Nombre dañado por OCR: «Beam Stearns» por «Bear Stearns», el banco de inversión cuya quiebra en septiembre de 2008 abre la crisis financiera. Confusión de la erre por la eme, clásica en OCR. Medido en el corpus: «Beam Stearns» aparece 5 veces y «Bear Stearns» 1, de modo que la forma correcta está atestiguada por el propio corpus aunque sea minoritaria; los cinco contextos son inequívocos («cuando alrededor de julio del año 2008», «en el momento en que quebró», «la crisis de»). Se corrige y se deja constancia aquí de que es el primer caso en que la forma canónica es minoritaria: la decisión no descansa en la frecuencia sino en que la entidad es única y el corpus la atestigua.

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

### `RPM-2011-05-12:4009:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `plicancias sobre el financiamíento de Chile y sobr`
   - después: `plicancias sobre el financiamiento de Chile y sobr`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 440 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
2. **ESPACIO_INDEBIDO**
   - antes: `o posible— , se observ`
   - después: `o posible—, se observ`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2014-10-16:6441:2` — Miguel Ricaurte Bermúdez

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2008-07-10:1917:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `idente, consulta si ellPP es mucho más in`
   - después: `idente, consulta si el IPP es mucho más in`
   - por qué: Sigla dañada por el glifo I/l. Medido en toda la salida: 26 apariciones de esta familia, y cada forma tiene su equivalente correcto ampliamente atestiguado en el corpus (el IPC 1.430, el IPoM 1.543, IPCX 649, IPCX1 469, el IPP 10). Se excluyeron de la pasada "ellPEC", "dellPEC" y "ellMCE" (fila 1719:4): aparecen junto a siglas que no se pueden corroborar en el corpus y no hay reconstruccion unica.
2. **LETRA_CONFUNDIDA**
   - antes: ` ellPC `
   - después: ` el IPC `
   - por qué: Sigla dañada por el glifo I/l. Medido en toda la salida: 26 apariciones de esta familia, y cada forma tiene su equivalente correcto ampliamente atestiguado en el corpus (el IPC 1.430, el IPoM 1.543, IPCX 649, IPCX1 469, el IPP 10). Se excluyeron de la pasada "ellPEC", "dellPEC" y "ellMCE" (fila 1719:4): aparecen junto a siglas que no se pueden corroborar en el corpus y no hay reconstruccion unica.

### `RPM-2014-07-15:6340:3` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2010-07-15:3250:2` — Claudio Soto Gamboa

1. **PUNTUACION**
   - antes: `ra.`
   - después: `ra,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.

### `RPM-2006-06-15:693:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `recio del cobre tenía ai país bastante eufóric`
   - después: `recio del cobre tenía al país bastante eufóric`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2009-11-12:2796:3` — Enrique Marshall Rivera

1. **ACENTO_INDEBIDO**
   - antes: `e dos temas agregan íncertidumbre al escenario gl`
   - después: `e dos temas agregan incertidumbre al escenario gl`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 861 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2009-05-07:2504:1` — José De Gregorio Rebeco

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2006-12-14:1021:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` )RIO CORBO LIOI Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2011-10-13:4388:1` — Felipe Larraín Bascuñán

1. **PUNTUACION**
   - antes: `el señor Felipe Larraín destaca, que el 30 de septiembre pasado`
   - después: `el señor Felipe Larraín destaca que el 30 de septiembre pasado`
   - por qué: Coma intrusa entre el verbo y la subordinada. Medido en todo el consolidado: 'destaca que' aparece 772 veces y 'destaca, que' una sola. La oración no admite otra lectura y la forma correcta es abrumadoramente mayoritaria.

### `RPM-2010-11-16:3508:1` — Sergio Lehmann Beresi

1. **ESPACIO_INDEBIDO**
   - antes: ` economías , y que sí `
   - después: ` economías, y que sí `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2013-01-17:5316:1` — Luis Óscar Herrera Barriga

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2015-06-11:6852:1` — Beltrán de Ramón Acevedo

1. **LETRA_CONFUNDIDA**
   - antes: `El señor Beltran de Ramón plantea que el comportamiento del tipo `
   - después: `El señor Beltrán de Ramón plantea que el comportamiento del tipo `
   - por qué: Normalización de nombre propio dañado, autorizada por el usuario en esta ronda (el criterio anterior era marcar sin corregir). La forma canónica la acreditan el corpus y el roster de la sesión: «Beltrán de Ramón» aparece 249 veces en la salida, contra 2 de la forma dañada. Se corrige en Texto_Corregido; Texto queda intacto. Lo que no tiene forma canónica atestiguada (por ejemplo «Miguel Angel Nacrur Gazali») sigue marcado NOMBRE_PROPIO_POR_COTEJAR.

### `RPM-2010-07-15:3258:2` — Claudio Soto Gamboa

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2010-05-13:3121:1` — Rodrigo Vergara Montes

1. **PUNTUACION**
   - antes: `Continuando con la votación,.`
   - después: `Continuando con la votación,`
   - por qué: Coma seguida de punto al final de la fila. Medido en el corpus: «<palabra>,.» aparece 98 veces en el texto virgen; el pase transversal del §45 corrigió 78 (76 «A continuación,.» más «década,.» y «Euro,.») y dejó estas 20, que son la misma familia con otras palabras: «Continuando con la votación,.» (6), «Para concluir con la votación,.» (3), «No habiendo más comentarios,.» (8), «No habiendo más comentarios y preguntas,.» (2) y «…señor Manuel Marfán,.» (1). En los 20 casos la fila siguiente empieza con «el Presidente…», «el Consejero…» o «el Vicepresidente…», de modo que la coma es la marca correcta y el punto es el signo sobrante. Se aplica el mismo criterio del §45.
