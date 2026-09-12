# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1376**
- operaciones: **2214**
- filas marcadas para cotejo: **195**
- sha256 de la base: `d0b64842cd756df4c50d2960d9bbf01c4c45e5df28609d7b612c5d666593da75`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `ESPACIO_INDEBIDO` | 515 |
| `LETRA_CONFUNDIDA` | 487 |
| `ACENTO_INDEBIDO` | 348 |
| `PALABRA_PARTIDA` | 320 |
| `ACENTO_FALTANTE` | 182 |
| `PUNTUACION` | 106 |
| `SIMBOLO_SUELTO` | 85 |
| `FIRMA_TRUNCADA` | 55 |
| `PALABRA_ERRONEA` | 28 |
| `RESIDUO_PAGINACION` | 27 |
| `ESPACIO_FALTANTE` | 24 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_DUPLICADA` | 3 |
| `PALABRA_SOBRANTE` | 2 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2014-10-16:6447:1` — Joaquín Vial Ruiz-Tagle

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2010-03-18:3022:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` lANUEL MARFÁN LEWIS JOSÉ DE GREGORIO REBECO Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2005-03-10:192:1` — Jorge Desormeaux Jiménez

1. **PALABRA_PARTIDA**
   - antes: `esperan que la tasa norteam ericana se encuentre a `
   - después: `esperan que la tasa norteamericana se encuentre a `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 80 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
2. **PALABRA_PARTIDA**
   - antes: ` el Consejero señor Desorm eaux, señalando que `
   - después: ` el Consejero señor Desormeaux, señalando que `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 444 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA. Es un nombre propio, pero no se está adivinando nada: la forma correcta está atestiguada en el corpus y lo único que se elimina es un espacio que el escaneo insertó dentro de la palabra. No es resolución de alias, que es lo que el criterio prohíbe.
3. **PALABRA_PARTIDA**
   - antes: `e claro, pese a las incertidum bres, que las brecha`
   - después: `e claro, pese a las incertidumbres, que las brecha`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 78 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
4. **PALABRA_PARTIDA**
   - antes: `ijo tiene un efecto relativam ente reducido sobre `
   - después: `ijo tiene un efecto relativamente reducido sobre `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 771 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2011-10-13:4344:1` — Sergio Lehmann Beresi

1. **ACENTO_FALTANTE**
   - antes: `ajustes a la baja en América Latina, Asia, Oceania y Europa emergente`
   - después: `ajustes a la baja en América Latina, Asia, Oceanía y Europa emergente`
   - por qué: Falta la tilde en 'Oceanía'. No es una reconstrucción ambigua: el topónimo tiene una sola grafía en español y la serie es una enumeración de regiones, así que no hay otra lectura posible. Distinto de los casos que marco, donde faltaba una letra y cabían dos palabras.

### `RPM-2007-03-15:1104:1` — Consejo del Banco Central de Chile

1. **PALABRA_PARTIDA**
   - antes: ` horas, se reúne el C onsejo del Banco Centr`
   - después: ` horas, se reúne el Consejo del Banco Centr`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 1433 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2015-10-15:7058:5` — Claudio Raddatz Kiefer

1. **ESPACIO_INDEBIDO**
   - antes: `n chilena— , así como `
   - después: `n chilena—, así como `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2008-02-07:1680:1` — Enrique Marshall Rivera

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2013-02-14:5361:1` — Miguel Fuentes Díaz

1. **ACENTO_FALTANTE**
   - antes: `la ejecución presupuestaria del año 2012 fu`
   - después: `la ejecución presupuestaría del año 2012 fu`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2010-12-16:3619:1` — Claudio Soto Gamboa

1. **LETRA_CONFUNDIDA**
   - antes: `nes negativas y que ellPCX1 disminuyó por s`
   - después: `nes negativas y que el IPCX1 disminuyó por s`
   - por qué: Sigla dañada por el glifo I/l. Medido en toda la salida: 26 apariciones de esta familia, y cada forma tiene su equivalente correcto ampliamente atestiguado en el corpus (el IPC 1.430, el IPoM 1.543, IPCX 649, IPCX1 469, el IPP 10). Se excluyeron de la pasada "ellPEC", "dellPEC" y "ellMCE" (fila 1719:4): aparecen junto a siglas que no se pueden corroborar en el corpus y no hay reconstruccion unica.
2. **LETRA_CONFUNDIDA**
   - antes: `ue se está cerrando ellPoM de diciembre, y`
   - después: `ue se está cerrando el IPoM de diciembre, y`
   - por qué: Sigla dañada por el glifo I/l. Medido en toda la salida: 26 apariciones de esta familia, y cada forma tiene su equivalente correcto ampliamente atestiguado en el corpus (el IPC 1.430, el IPoM 1.543, IPCX 649, IPCX1 469, el IPP 10). Se excluyeron de la pasada "ellPEC", "dellPEC" y "ellMCE" (fila 1719:4): aparecen junto a siglas que no se pueden corroborar en el corpus y no hay reconstruccion unica.
3. **LETRA_CONFUNDIDA**
   - antes: `mbién la corrección dellPC y, en especial,`
   - después: `mbién la corrección del IPC y, en especial,`
   - por qué: Sigla dañada por el glifo I/l. Medido en toda la salida: 26 apariciones de esta familia, y cada forma tiene su equivalente correcto ampliamente atestiguado en el corpus (el IPC 1.430, el IPoM 1.543, IPCX 649, IPCX1 469, el IPP 10). Se excluyeron de la pasada "ellPEC", "dellPEC" y "ellMCE" (fila 1719:4): aparecen junto a siglas que no se pueden corroborar en el corpus y no hay reconstruccion unica.
4. **LETRA_CONFUNDIDA**
   - antes: ` deIIPCX1 `
   - después: ` del IPCX1 `
   - por qué: Sigla dañada por el glifo I/l. Medido en toda la salida: 26 apariciones de esta familia, y cada forma tiene su equivalente correcto ampliamente atestiguado en el corpus (el IPC 1.430, el IPoM 1.543, IPCX 649, IPCX1 469, el IPP 10). Se excluyeron de la pasada "ellPEC", "dellPEC" y "ellMCE" (fila 1719:4): aparecen junto a siglas que no se pueden corroborar en el corpus y no hay reconstruccion unica.
5. **ESPACIO_INDEBIDO**
   - antes: `onsecutivo . Con respe`
   - después: `onsecutivo. Con respe`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
6. **ESPACIO_INDEBIDO**
   - antes: `e la carne . Subraya q`
   - después: `e la carne. Subraya q`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
7. **ESPACIO_INDEBIDO**
   - antes: `Manifiesta , al respec`
   - después: `Manifiesta, al respec`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
8. **ESPACIO_INDEBIDO**
   - antes: `finalmente , en diciem`
   - después: `finalmente, en diciem`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
9. **ESPACIO_INDEBIDO**
   - antes: ` organismo . En consec`
   - después: ` organismo. En consec`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2009-08-13:2685:3` — Enrique Marshall Rivera

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.
2. **PALABRA_PARTIDA**
   - antes: ` cierta perspectiva tempora l. En opinión del`
   - después: ` cierta perspectiva temporal. En opinión del`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 26 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
3. **ACENTO_FALTANTE**
   - antes: ` y que en esa línea estaria, por ejemplo, l`
   - después: ` y que en esa línea estaría, por ejemplo, l`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.
4. **ACENTO_FALTANTE**
   - antes: `n de nuevas medidas deberia darse conjuntam`
   - después: `n de nuevas medidas debería darse conjuntam`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.
5. **ACENTO_FALTANTE**
   - antes: `ara ejercer todo el estimulo requerido en es`
   - después: `ara ejercer todo el estímulo requerido en es`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.
6. **ESPACIO_INDEBIDO**
   - antes: ` monetario . Agrega qu`
   - después: ` monetario. Agrega qu`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
7. **ESPACIO_INDEBIDO**
   - antes: `afirmarlas , lo que co`
   - después: `afirmarlas, lo que co`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
8. **ESPACIO_INDEBIDO**
   - antes: `e enfrenta , mucho ayu`
   - después: `e enfrenta, mucho ayu`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2012-10-18:5160:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` MARFÁN LEWIS RODRIGO VENGARA MONTES Presidente Vicepresidente ENRIQUE MARSHALL RIVERA Consejero.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2009-01-08:2281:2` — Claudio Soto Gamboa

1. **ESPACIO_INDEBIDO**
   - antes: `untos base , mientras `
   - después: `untos base, mientras `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **ESPACIO_INDEBIDO**
   - antes: `untos base , y la encu`
   - después: `untos base, y la encu`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2007-09-13:1429:1` — Jorge Desormeaux Jiménez

1. **PALABRA_PARTIDA**
   - antes: `de manera que sim plem ente quiere llamar la atención`
   - después: `de manera que simplemente quiere llamar la atención`
   - por qué: Espacio intrapalabra, artefacto del escaneo: la palabra está partida en dos. No es una reconstrucción, se reúne sin alterar una letra. Segunda ocurrencia de este artefacto en la sesión.

### `RPM-2014-03-13:6095:1` — Luis Óscar Herrera Barriga

1. **ACENTO_FALTANTE**
   - antes: `eserva Federal. Por ultimo, expresa que la`
   - después: `eserva Federal. Por último, expresa que la`
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2009-02-12:2357:1` — Sebastián Claro Edwards

1. **ESPACIO_INDEBIDO**
   - antes: `los bancos , lo cual p`
   - después: `los bancos, lo cual p`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **LETRA_CONFUNDIDA**
   - antes: `se/ection`
   - después: `selection`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene selection y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.

### `RPM-2013-02-14:5366:1` — Manuel Marfán Lewis

1. **SIMBOLO_SUELTO**
   - antes: ` i B A N C O C E N T R A L D E C H I L E`
   - después: ``
   - por qué: Encabezado de pagina del PDF, "BANCO CENTRAL DE CHILE", capturado letra por letra y con espacios. Es un residuo de la fuente, no texto del acta: la forma normal "BANCO CENTRAL DE CHILE" no aparece ninguna vez en el corpus, o sea que cuando este encabezado esta presente siempre viene letra por letra. Medido: 10 apariciones en 10 filas, mas 1 truncado ("...D E C H"). La politica es eliminar los residuos de la fuente (numeros de pagina, marcas de hora, comillas huerfanas, firmas truncadas) y este es de la misma familia.

### `RPM-2007-02-08:1068:1` — Jorge Desormeaux Jiménez

1. **LETRA_CONFUNDIDA**
   - antes: ` proyecciones del Consesus Forecast o JP Mor`
   - después: ` proyecciones del Consensus Forecast o JP Mor`
   - por qué: Consesus por Consensus: falta una n. Medido: "Consensus" aparece 127 veces en 99 filas y "Consesus" 8 veces en 6, siempre en el nombre propio "Consensus Forecast". No hay lectura alternativa.
2. **LETRA_CONFUNDIDA**
   - antes: `n de depreciación de! yuan en un 10% `
   - después: `n de depreciación del yuan en un 10% `
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2011-06-14:4116:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `sión crecientemente mayoritaría y que, en lo gr`
   - después: `sión crecientemente mayoritaria y que, en lo gr`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 195 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2010-07-15:3221:2` — Sergio Lehmann Beresi

1. **ESPACIO_INDEBIDO**
   - antes: ` efectuado , particula`
   - después: ` efectuado, particula`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **ESPACIO_INDEBIDO**
   - antes: `inancieras . Añade que`
   - después: `inancieras. Añade que`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2007-08-09:1361:2` — Sergio Lehmann Beresi

1. **PALABRA_PARTIDA**
   - antes: `n Estados Unidos de Am érica, por tanto no e`
   - después: `n Estados Unidos de América, por tanto no e`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2587 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA. Es un nombre propio, pero no se está adivinando nada: la forma correcta está atestiguada en el corpus y lo único que se elimina es un espacio que el escaneo insertó dentro de la palabra. No es resolución de alias, que es lo que el criterio prohíbe.

### `RPM-2014-07-15:6332:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `opIrnon`
   - después: `opinión`
   - por qué: opIrnon por opinión. No es palabra y la formula "en su opinión" es de las mas frecuentes del corpus (1.867 apariciones de "opinión"); el contexto "Expresa que, en su opIrnon, la desaceleración" no admite otra lectura.
2. **LETRA_CONFUNDIDA**
   - antes: `1nstitución`
   - después: `Institución`
   - por qué: 1nstitución por Institución: la I mayuscula inicial se leyo como el digito 1. El contexto es "del staff de la 1nstitución".

### `RPM-2013-08-13:5707:1` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

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

### `RPM-2013-02-14:5367:1` — Miguel Fuentes Díaz

1. **SIMBOLO_SUELTO**
   - antes: ` B A N C O C E N T R A L D E C H IL E`
   - después: ``
   - por qué: Encabezado de pagina del PDF, "BANCO CENTRAL DE CHILE", capturado letra por letra y con espacios. Es un residuo de la fuente, no texto del acta: la forma normal "BANCO CENTRAL DE CHILE" no aparece ninguna vez en el corpus, o sea que cuando este encabezado esta presente siempre viene letra por letra. Medido: 10 apariciones en 10 filas, mas 1 truncado ("...D E C H"). La politica es eliminar los residuos de la fuente (numeros de pagina, marcas de hora, comillas huerfanas, firmas truncadas) y este es de la misma familia.

### `RPM-2012-10-18:5116:1` — Joaquín Vial Ruiz-Tagle

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2015-03-19:6673:1` — Miguel Fuentes Díaz

1. **ESPACIO_INDEBIDO**
   - antes: `al — 2,9%— , sus varia`
   - después: `al — 2,9%—, sus varia`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2013-12-12:5905:1` — Consejo del Banco Central de Chile

1. **ESPACIO_INDEBIDO**
   - antes: `ña Poblete ; Gerente d`
   - después: `ña Poblete; Gerente d`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2014-11-18:6490:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `economIca`
   - después: `económica`
   - por qué: economIca por económica: la i se leyo como I mayuscula y falta la tilde. Medido: "económica" aparece 667 veces y "economIca" una sola, en "la creciente divergencia economIca entre Estados Unidos de América".

### `RPM-2009-08-13:2666:3` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.

### `RPM-2011-10-13:4399:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` MARFÁN LEWIS JOSÉ DE GREGORIO REBECO Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.
