# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1560**
- operaciones: **2591**
- filas marcadas para cotejo: **214**
- sha256 de la base: `32752bd52ce5d3b50b0732780154aaef23482908f6671f92a327509e75edf452`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 539 |
| `ESPACIO_INDEBIDO` | 511 |
| `PALABRA_PARTIDA` | 481 |
| `ACENTO_INDEBIDO` | 372 |
| `SIMBOLO_SUELTO` | 194 |
| `ACENTO_FALTANTE` | 183 |
| `PUNTUACION` | 134 |
| `FIRMA_TRUNCADA` | 55 |
| `RESIDUO_PAGINACION` | 30 |
| `PALABRA_ERRONEA` | 28 |
| `ESPACIO_FALTANTE` | 26 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |
| `PALABRA_DUPLICADA` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2013-05-16:5567:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` RODRIGO VERGARA MONTES Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2009-07-09:2649:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2005-03-10:184:1` — Nicolás Eyzaguirre Guzmán

1. **PALABRA_PARTIDA**
   - antes: `m uchas`
   - después: `muchas`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 116 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2010-08-12:3291:1` — Enrique Marshall Rivera

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2006-11-16:955:1` — Igal Magendzo Weinberger

1. **LETRA_CONFUNDIDA**
   - antes: `bre. En septiembre, ios indicadores par`
   - después: `bre. En septiembre, los indicadores par`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.
2. **ESPACIO_INDEBIDO**
   - antes: `ltimo mes— .
Comenta e`
   - después: `ltimo mes—.
Comenta e`
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

### `RPM-2007-09-13:1469:1` — Consejo del Banco Central de Chile

1. **LETRA_CONFUNDIDA**
   - antes: `perecióles`
   - después: `perecibles`
   - por qué: B por ó. 'Perecióles' no es palabra: el adjetivo es 'perecibles'. Aparece 2 veces en esta misma fila y las dos son el mismo defecto, por eso se declara Ocurrencias: 2. Medido: 'perecióles' aparece 10 veces en 9 filas del corpus frente a 'perecibles' 166, con 1 ocurrencia de la forma buena en esta misma fila ('excluye combustibles, perecibles y algunos servicios regulados') y 8 en la sesión. Es el mismo defecto ya corregido en RPM-2012-05-17:4827:1 en la ronda 158. Quedan 7 filas más con 'perecióles' en otras sesiones, que se corregirán en sus rondas.
2. **LETRA_CONFUNDIDA**
   - antes: `la inflación subyacente IPCXI (que excluye combustibles`
   - después: `la inflación subyacente IPCX1 (que excluye combustibles`
   - por qué: Letra I por el dígito 1: el indicador se llama 'IPCX1' y no existe un 'IPCXI' en numeración romana dentro de la nomenclatura del Banco. Medido: 'IPCXI' aparece 6 veces en 6 filas frente a 'IPCX1' 458, y la construcción exacta 'la inflación subyacente IPCX1' aparece 24 veces en el corpus; dentro de la sesión, 'IPCX1' aparece 3 veces. La reparación es única. Las otras 5 ocurrencias de 'IPCXI' están en 1352:1, 1402:1, 1520:1, 1569:1 y 1641:1, de sesiones distintas, y se corregirán en sus rondas.

### `RPM-2011-06-14:4106:1` — Luis Óscar Herrera Barriga

1. **ACENTO_INDEBIDO**
   - antes: `y disponibilidad de financíamiento internacional. `
   - después: `y disponibilidad de financiamiento internacional. `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 440 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
2. **ACENTO_INDEBIDO**
   - antes: `. En este contexto, índica que el balance `
   - después: `. En este contexto, indica que el balance `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2010-02-11:2906:1` — Manuel Marfán Lewis

1. **SIMBOLO_SUELTO**
   - antes: `inmune a los shocks', por el contrario`
   - después: `inmune a los shocks, por el contrario`
   - por qué: Comilla recta suelta. La oración se lee completa y correcta sin ella: «se tiene mucha persistencia, lo cual no lo hace inmune a los shocks, por el contrario, estos provocan un significativo efecto por una vez». No es un posesivo inglés (no hay palabra en inglés) y no cierra ninguna cita: es la única comilla recta de la fila y el corpus usa comillas tipográficas (360 «“» y 347 «”»). Queda pendiente, para cuando toque cada sesión, la familia completa: 41 comillas rectas en 38 filas, y es mixta — la mayoría es basura de OCR («'’i^sgo», «costos f' H-», «'V/», «'aquerida») pero algunas son posesivos ingleses legítimos («Purchasing Managers' Index», «Lloyd's»), así que no se puede resolver por regla.

### `RPM-2009-03-12:2397:1` — Sebastián Claro Edwards

1. **PALABRA_PARTIDA**
   - antes: `si ese escenario de crecim iento mundial que pla`
   - después: `si ese escenario de crecimiento mundial que pla`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 5699 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2011-02-17:3813:2` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `umentando la TPM en ios próximos meses.`
   - después: `umentando la TPM en los próximos meses.`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2008-08-14:2002:1` — Sebastián Claro Edwards

1. **PALABRA_PARTIDA**
   - antes: `porque no sabe exactam ente cuál es la unidad, pero respecto del tamaño`
   - después: `porque no sabe exactamente cuál es la unidad, pero respecto del tamaño`
   - por qué: Espacio intrapalabra: 'exactam ente' está partida en dos. Se reúne sin alterar una letra. Medido: 'exactam ente' aparece 1 vez en el corpus y 'exactamente' 64.

### `RPM-2007-06-14:1297:4` — Igal Magendzo Weinberger

1. **LETRA_CONFUNDIDA**
   - antes: `IRC`
   - después: `IPC`
   - por qué: IRC por IPC. Medido en todo el corpus: 71 apariciones, ninguna en un contexto donde IRC sea una sigla legitima; 61 sueltas y 10 dentro de IRCX1, que tambien debe leerse IPCX1 porque la misma fila escribe IPCX e IPCX2. Regla de bloque revisada caso por caso.
2. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2012-11-13:5221:3` — Consejo del Banco Central de Chile

1. **RESIDUO_PAGINACION**
   - antes: `permanecen alineadas con la meta. Página 30 de 30 El Consejo reafirma`
   - después: `permanecen alineadas con la meta. El Consejo reafirma`
   - por qué: Pie de página del PDF original incrustado entre dos oraciones completas. Se me pasó al leer la sesión 2012-11-13 (rondas 107-113) porque en ese momento todavía no había medido el patrón; lo encontré ahora al contar las ocurrencias de 'Página N de N' en todo el corpus. Es un residuo de paginación, que la política de corrección autoriza eliminar.

### `RPM-2008-09-04:2100:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` JORGE DESORMEAUX JIMÉNEZ JOSE DE GREGORIO REBECO Vicepresidente Presidente EI)fRIQUE MARSHALL RIVERA Consejero.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2015-10-15:7063:1` — Diego Gianelli Gómez

1. **PUNTUACION**
   - antes: `"El Niño"`
   - después: `“El Niño”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.

### `RPM-2011-06-14:4109:3` — Felipe Larraín Bascuñán

1. **ESPACIO_INDEBIDO**
   - antes: `creció 3,1 %. En los ú`
   - después: `creció 3,1%. En los ú`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2006-10-12:934:1` — Pablo García Silva

1. **SALTOS_DE_LINEA**
   - antes: `prolongado
del
esperado.
Asimismo,
menciona
el
señor García,
que
todo
esto,
desgraciadamente,`
   - después: `prolongado del esperado. Asimismo, menciona el señor García, que todo esto, desgraciadamente,`
   - por qué: Artefacto de justificación del PDF: una palabra por línea. Segundo caso en esta sesión, después de 904:1. Se reúne el texto sin alterar una letra.

### `RPM-2010-07-15:3213:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `que son similares a ios que considera l`
   - después: `que son similares a los que considera l`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2009-09-08:2707:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.
2. **ACENTO_FALTANTE**
   - antes: `cesario mantener el estimulo monetario actua`
   - después: `cesario mantener el estímulo monetario actua`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.

### `RPM-2007-03-15:1167:1` — Vittorio Corbo Lioi

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2013-04-11:5461:1` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2012-04-17:4736:4` — Sergio Lehmann Beresi

1. **RESIDUO_PAGINACION**
   - antes: ` Sesión N° 184 Página 4 de 26 `
   - después: ` `
   - por qué: Residuo de paginacion del PDF incrustado en medio de la oracion. Medido: 26 apariciones, 24 con la cabecera "Sesion N° N" delante y 2 como pie de pagina del Comunicado ("Pagina 31 de 31"). "Sesion N° N" aparece 25 veces en el corpus y solo 24 van seguidas de Pagina, de modo que el patron exige ambos y no toca ninguna mencion legitima. Se elimina el residuo y se deja un solo espacio donde la oracion continua.

### `RPM-2014-04-17:6132:3` — Rodrigo Vergara Montes

1. **ACENTO_INDEBIDO**
   - antes: `Gerente de Análisis Macroeconómíco señor Miguel Fu`
   - después: `Gerente de Análisis Macroeconómico señor Miguel Fu`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 1000 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2011-06-14:4110:1` — Rodrigo Vergara Montes

1. **ESPACIO_INDEBIDO**
   - antes: `eríodo más . (1 pausad`
   - después: `eríodo más. (1 pausad`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2011-02-17:3788:1` — Claudio Soto Gamboa

1. **LETRA_CONFUNDIDA**
   - antes: ` consideraron todos ios otros fundament`
   - después: ` consideraron todos los otros fundament`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2014-10-16:6441:2` — Miguel Ricaurte Bermúdez

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2013-09-12:5793:1` — Rodrigo Vergara Montes

1. **PALABRA_OMITIDA**
   - antes: `un grado de desintegración de la economía chilena respecto del resto mundo`
   - después: `un grado de desintegración de la economía chilena respecto del resto del mundo`
   - por qué: Artículo-contracto omitido. Corroborado en la sesión: 'resto del mundo' aparece 3 veces en 2013-09-12 (filas 5771, 5807 y 5811) y 129 veces en el corpus, contra 1 sola de 'resto mundo', que es ésta.

### `RPM-2012-05-17:4839:1` — Felipe Larraín Bascuñán

1. **ACENTO_INDEBIDO**
   - antes: `De hecho, índica que en la Reunión del mes de abril`
   - después: `De hecho, indica que en la Reunión del mes de abril`
   - por qué: Tilde en la sílaba equivocada: 'índica' no es palabra. Medido: aparece 45 veces en el corpus contra 2.366 de 'indica que'. Es la misma errata ya corregida en 5762:1.
2. **ESPACIO_FALTANTE**
   - antes: `tras un 11,9% en marzo y un13% en febrero`
   - después: `tras un 11,9% en marzo y un 13% en febrero`
   - por qué: Falta el espacio entre el artículo y la cifra. La propia oración trae 'un 11,9%' con espacio inmediatamente antes, así que la forma correcta está en la misma fila. Medido: 'un13%' aparece una sola vez en el corpus.

### `RPM-2015-07-14:6915:3` — Rodrigo Vergara Montes

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
