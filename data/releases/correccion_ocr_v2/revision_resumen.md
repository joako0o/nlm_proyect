# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1757**
- operaciones: **3025**
- filas marcadas para cotejo: **221**
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
| `PALABRA_ERRONEA` | 30 |
| `RESIDUO_PAGINACION` | 30 |
| `ESPACIO_FALTANTE` | 27 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |
| `PALABRA_DUPLICADA` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2015-05-14:6778:1` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: `láusulas usuales de índexación, se observa que`
   - después: `láusulas usuales de indexación, se observa que`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 149 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2011-10-13:4364:2` — Claudio Soto Gamboa

1. **LETRA_CONFUNDIDA**
   - antes: `El señor Claudios Soto responde que hay un debate entre la Cám`
   - después: `El señor Claudio Soto responde que hay un debate entre la Cám`
   - por qué: Normalización de nombre propio dañado, autorizada por el usuario en esta ronda (el criterio anterior era marcar sin corregir). La forma canónica la acreditan el corpus y el roster de la sesión: «Claudio Soto» aparece 1274 veces en la salida, contra 1 de la forma dañada. Se corrige en Texto_Corregido; Texto queda intacto. Lo que no tiene forma canónica atestiguada (por ejemplo «Miguel Angel Nacrur Gazali») sigue marcado NOMBRE_PROPIO_POR_COTEJAR.

### `RPM-2009-03-12:2388:2` — Sergio Lehmann Beresi

1. **ESPACIO_INDEBIDO**
   - antes: `, pero que , obviament`
   - después: `, pero que, obviament`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **SIMBOLO_SUELTO**
   - antes: `ón intermedia para el año 2010 Y se supuso que se tendrá una `
   - después: `ón intermedia para el año 2010 y se supuso que se tendrá una `
   - por qué: Conjunción «y» leída como mayúscula por el OCR. El corpus la escribe en minúscula; se excluyó el único caso legítimo, «el eje Y» (RPM-2012-09-13:5049:1), donde la mayúscula nombra el eje.

### `RPM-2005-03-10:171:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `m antener`
   - después: `mantener`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 1788 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2009-11-12:2802:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` JORGE DESORMEAUX JIMÉNEZ JOSE DE GREGORIO REBECO Vicepresidente Presidente ENRIQUE MARSHALL RIVERA LEWIS Consejero Consejero.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

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

### `RPM-2013-01-17:5280:1` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `Asía`
   - después: `Asia`
   - por qué: Acento indebido. Medido en el corpus: «Asia» aparece 327 veces y «Asía» 3, siempre «Asia emergente» o «Asia y Oceanía». El topónimo no lleva acento.
2. **ACENTO_INDEBIDO**
   - antes: `Arabía`
   - después: `Arabia`
   - por qué: Acento indebido. Medido en el corpus: «Arabia» aparece 28 veces y «Arabía» 1, siempre «Arabia Saudita».

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

### `RPM-2010-06-15:3206:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` JOSE DE GREGORfO REBECO Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2015-06-11:6852:1` — Beltrán de Ramón Acevedo

1. **LETRA_CONFUNDIDA**
   - antes: `El señor Beltran de Ramón plantea que el comportamiento del tipo `
   - después: `El señor Beltrán de Ramón plantea que el comportamiento del tipo `
   - por qué: Normalización de nombre propio dañado, autorizada por el usuario en esta ronda (el criterio anterior era marcar sin corregir). La forma canónica la acreditan el corpus y el roster de la sesión: «Beltrán de Ramón» aparece 249 veces en la salida, contra 2 de la forma dañada. Se corrige en Texto_Corregido; Texto queda intacto. Lo que no tiene forma canónica atestiguada (por ejemplo «Miguel Angel Nacrur Gazali») sigue marcado NOMBRE_PROPIO_POR_COTEJAR.

### `RPM-2009-07-09:2644:2` — Luis Felipe Céspedes Cifuentes

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.

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

### `RPM-2010-05-13:3082:2` — Claudio Soto Gamboa

1. **LETRA_CONFUNDIDA**
   - antes: `de inversión y de Consesus Forecasts. Hace l`
   - después: `de inversión y de Consensus Forecasts. Hace l`
   - por qué: Consesus por Consensus: falta una n. Medido: "Consensus" aparece 127 veces en 99 filas y "Consesus" 8 veces en 6, siempre en el nombre propio "Consensus Forecast". No hay lectura alternativa.

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

### `RPM-2011-02-17:3813:3` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `siguiente Acuerdo;`
   - después: `siguiente Acuerdo:`
   - por qué: Pase transversal. La fórmula del Acuerdo es «el Consejo adopta/adoptó el siguiente Acuerdo: NNN-NN-NNMMDD - Tasa de Política Monetaria»: los dos puntos introducen el acuerdo enumerado, y un punto y coma no puede hacer eso. Medido en las 9.724 filas: la fórmula aparece 118 veces, 106 con dos puntos y 12 con punto y coma, y las 12 son estructuralmente idénticas a las otras —mismo número de acuerdo y mismo título a continuación—. El punto y coma es una lectura de OCR del dos puntos. Se corrigieron las 12 (2005-01-11, 2005-10-11, 2006-08-10, 2006-12-14, 2007-02-08, 2007-04-12, 2007-05-10, 2007-06-14, 2009-09-08, 2010-09-16, 2011-02-17, 2015-01-15). Es la misma evidencia que en §39 para «Siendo las 16; 15 horas» -> «16:15», donde también había 106 apariciones con dos puntos. Texto queda intacto.

### `RPM-2014-07-15:6308:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: ` señor Pablo García índica que desde el pu`
   - después: ` señor Pablo García indica que desde el pu`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

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

### `RPM-2014-06-12:6246:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `mes de mayo, superior ai 9,5% anotado el mes p`
   - después: `mes de mayo, superior al 9,5% anotado el mes p`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.
2. **LETRA_CONFUNDIDA**
   - antes: `smo, manifiesta que ios datos de PIB de`
   - después: `smo, manifiesta que los datos de PIB de`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.
3. **SIMBOLO_SUELTO**
   - antes: `ndustrial fue menor que lo anticipado. ry _<< ■ En Japón, el PIB fue may`
   - después: `ndustrial fue menor que lo anticipado. En Japón, el PIB fue may`
   - por qué: Símbolo ■ con basura adyacente, residuo del escaneo. El tipo SIMBOLO_SUELTO fue creado justamente para estos casos («■V», «ry _<< ■» -> se elimina). Medido: 21 apariciones en 20 filas. Se trata cada una con su basura propia porque el ruido que la acompaña varía (■o J, ■,\y, ■', ■J, ■V, / ■ ' /, 4 / ■, i - /■, — f ■, ry _<< ■). En todos los casos las dos oraciones que rodean el residuo quedan completas sin él. Excepción: en 5802:2 se elimina solo el ■ y se deja el paréntesis abierto, porque esa fila ya está marcada RECONSTRUCCION_AMBIGUA_POR_COTEJAR con motivo FINAL_SIN_PUNTUACION.

### `RPM-2010-07-15:3211:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `Beam Stearns`
   - después: `Bear Stearns`
   - por qué: Nombre dañado por OCR: «Beam Stearns» por «Bear Stearns», el banco de inversión cuya quiebra en septiembre de 2008 abre la crisis financiera. Confusión de la erre por la eme, clásica en OCR. Medido en el corpus: «Beam Stearns» aparece 5 veces y «Bear Stearns» 1, de modo que la forma correcta está atestiguada por el propio corpus aunque sea minoritaria; los cinco contextos son inequívocos («cuando alrededor de julio del año 2008», «en el momento en que quebró», «la crisis de»). Se corrige y se deja constancia aquí de que es el primer caso en que la forma canónica es minoritaria: la decisión no descansa en la frecuencia sino en que la entidad es única y el corpus la atestigua.

### `RPM-2006-05-11:674:1` — Vittorio Corbo Lioi

1. **LETRA_CONFUNDIDA**
   - antes: `IPOM`
   - después: `IPoM`
   - por qué: Sigla mal compuesta. Medido en el corpus: «IPoM» aparece 2473 veces y «IPOM» 58, siempre el mismo documento, el Informe de Política Monetaria del Banco Central de Chile, cuya sigla lleva la o minúscula. El OCR leyó la o minúscula como O mayúscula.

### `RPM-2009-10-13:2757:1` — Jorge Desormeaux Jiménez

1. **ACENTO_FALTANTE**
   - antes: ` fiscal reducirá su estimulo en los próximos`
   - después: ` fiscal reducirá su estímulo en los próximos`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.
2. **ESPACIO_INDEBIDO**
   - antes: `l año 2010 . En los me`
   - después: `l año 2010. En los me`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2009-04-09:2482:3` — Claudio Soto Gamboa

1. **ESPACIO_INDEBIDO**
   - antes: `ctualmente , está en -`
   - después: `ctualmente, está en -`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **ESPACIO_INDEBIDO**
   - antes: ` inflación , en genera`
   - después: ` inflación, en genera`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **LETRA_CONFUNDIDA**
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

### `RPM-2011-07-14:4214:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` MANUEL MARFAN LEWIS JOSÉ DE GREGORIO REBECO Vicepresidente Presidente 7 SEBASTIÁN CLARO EDWARDS ENRI0UE MARSHALL RIVERA Consejero Consejero.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2010-10-14:3435:1` — Sebastián Claro Edwards

1. **ESPACIO_INDEBIDO**
   - antes: ` Forecasts . Señala qu`
   - después: ` Forecasts. Señala qu`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2012-11-13:5164:1` — Sergio Lehmann Beresi

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2015-04-16:6716:1` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: `hacía`
   - después: `hacia`
   - por qué: Pase transversal, enumeración completa. De las 32 apariciones de «hacía» en el corpus, 17 son el verbo («hacía presente», «hacía referencia», «hacía mención», «hacía necesario», «lo hacía moderadamente»…) y 15 son la preposición «hacia» con tilde indebidamente puesta: siempre rigen un complemento de dirección o destino («hacía delante», «hacía adelante», «hacía la baja», «hacía América Latina», «hacía las economías emergentes», «hacía el tercer trimestre»). En esas 15 el verbo no tiene sujeto ni complemento posible. Se corrigieron las 15 y se dejaron las 17; el suelo de la guardia de regresión bajó de 32 a 17 con la enumeración documentada en el test, no en silencio. «hacia» aparece 2.183 veces.

### `RPM-2010-07-15:3213:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `que son similares a ios que considera l`
   - después: `que son similares a los que considera l`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2010-04-15:3069:1` — Pablo García Silva

1. **PUNTUACION**
   - antes: `oM.`
   - después: `oM,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.
