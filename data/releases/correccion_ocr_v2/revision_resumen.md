# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1568**
- operaciones: **2608**
- filas marcadas para cotejo: **214**
- sha256 de la base: `32752bd52ce5d3b50b0732780154aaef23482908f6671f92a327509e75edf452`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 542 |
| `ESPACIO_INDEBIDO` | 511 |
| `PALABRA_PARTIDA` | 490 |
| `ACENTO_INDEBIDO` | 374 |
| `SIMBOLO_SUELTO` | 194 |
| `ACENTO_FALTANTE` | 183 |
| `PUNTUACION` | 136 |
| `FIRMA_TRUNCADA` | 55 |
| `RESIDUO_PAGINACION` | 30 |
| `PALABRA_ERRONEA` | 28 |
| `ESPACIO_FALTANTE` | 27 |
| `PALABRA_OMITIDA` | 22 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |
| `PALABRA_DUPLICADA` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2013-05-16:5541:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2009-07-09:2641:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2005-03-10:184:1` — Nicolás Eyzaguirre Guzmán

1. **PALABRA_PARTIDA**
   - antes: `m uchas`
   - después: `muchas`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 116 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.

### `RPM-2010-07-15:3277:1` — José De Gregorio Rebeco

1. **PALABRA_PARTIDA**
   - antes: `T a s a`
   - después: `Tasa`
   - por qué: La palabra «Tasa» de la fórmula del Acuerdo está deletreada con espacios internos. Medido en el corpus: «-Tasa de Política» aparece bien escrita 119 veces y «T a s a» 9, siempre en la misma posición de la fórmula («el Consejo adopta el siguiente Acuerdo: <número>-Tasa de Política Monetaria»). Es el mismo defecto que el pase del §36 corrigió en la variante «T a sa» de 6 actas; ésta es la variante con las cuatro letras separadas. La posición es fija y no hay lectura alternativa: el número de acuerdo va pegado a la palabra.

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

### `RPM-2014-04-17:6179:1` — Rodrigo Vergara Montes

1. **ACENTO_INDEBIDO**
   - antes: `a una posible mayor expansívidad de la política `
   - después: `a una posible mayor expansividad de la política `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 129 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2007-09-13:1469:1` — Consejo del Banco Central de Chile

1. **LETRA_CONFUNDIDA**
   - antes: `perecióles`
   - después: `perecibles`
   - por qué: B por ó. 'Perecióles' no es palabra: el adjetivo es 'perecibles'. Aparece 2 veces en esta misma fila y las dos son el mismo defecto, por eso se declara Ocurrencias: 2. Medido: 'perecióles' aparece 10 veces en 9 filas del corpus frente a 'perecibles' 166, con 1 ocurrencia de la forma buena en esta misma fila ('excluye combustibles, perecibles y algunos servicios regulados') y 8 en la sesión. Es el mismo defecto ya corregido en RPM-2012-05-17:4827:1 en la ronda 158. Quedan 7 filas más con 'perecióles' en otras sesiones, que se corregirán en sus rondas.
2. **LETRA_CONFUNDIDA**
   - antes: `la inflación subyacente IPCXI (que excluye combustibles`
   - después: `la inflación subyacente IPCX1 (que excluye combustibles`
   - por qué: Letra I por el dígito 1: el indicador se llama 'IPCX1' y no existe un 'IPCXI' en numeración romana dentro de la nomenclatura del Banco. Medido: 'IPCXI' aparece 6 veces en 6 filas frente a 'IPCX1' 458, y la construcción exacta 'la inflación subyacente IPCX1' aparece 24 veces en el corpus; dentro de la sesión, 'IPCX1' aparece 3 veces. La reparación es única. Las otras 5 ocurrencias de 'IPCXI' están en 1352:1, 1402:1, 1520:1, 1569:1 y 1641:1, de sesiones distintas, y se corregirán en sus rondas.

### `RPM-2011-05-12:4053:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `en tomo a`
   - después: `en torno a`
   - por qué: en tomo a por "en torno a". Medido: 24 apariciones (20 "en tomo a" y 4 "en tomo al"), la r leida como m. "tomo" es palabra real (volumen) pero ningun contexto lo admite. "en torno a" aparece 1.678 veces.

### `RPM-2010-01-14:2888:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` JOSÉ DE GREGORIO REBECO Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.
2. **PUNTUACION**
   - antes: `16;55 horas`
   - después: `16:55 horas`
   - por qué: Idem: 544 contra 5.

### `RPM-2009-03-12:2396:2` — Sergio Lehmann Beresi

1. **ESPACIO_FALTANTE**
   - antes: `yeso`
   - después: `y eso`
   - por qué: yeso por "y eso". Medido: 13 apariciones, en todas falta el espacio entre la conjuncion y el demostrativo ("alto yeso tiene que tener" = "alto, y eso tiene que tener"). Verificado que ninguna esta embebida en otra palabra. La coma no se inserta: la oracion queda gramatical sin ella y anadirla seria editar puntuacion.

### `RPM-2011-02-17:3810:2` — Enrique Marshall Rivera

1. **SIMBOLO_SUELTO**
   - antes: ` intervención agradeciendo al staff e\ apoyo brindado en esta oportu`
   - después: ` intervención agradeciendo al staff el apoyo brindado en esta oportu`
   - por qué: «staff el <sustantivo>» es la formula del corpus, que tiene 427 «staff» y escribe «agradece el analisis del staff», «agradece al staff los Informes», «agradece al staff, por los informes»: el articulo es obligatorio y no existe la forma «staff e». La barra invertida es la «l» leida por el OCR, el mismo glifo de §21-§22 al reves, y se repite 9 veces en 9 sesiones distintas con la misma estructura, por lo que la lectura no es una intuicion: es una familia (§8 bis). §32.

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

### `RPM-2012-10-18:5160:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` MARFÁN LEWIS RODRIGO VENGARA MONTES Presidente Vicepresidente ENRIQUE MARSHALL RIVERA Consejero.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2015-11-12:7154:1` — Rodrigo Vergara Montes

1. **ESPACIO_INDEBIDO**
   - antes: `ha brecha— . Por últim`
   - después: `ha brecha—. Por últim`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2008-09-04:2099:1` — Consejo del Banco Central de Chile

1. **PALABRA_PARTIDA**
   - antes: `T a s a`
   - después: `Tasa`
   - por qué: La palabra «Tasa» de la fórmula del Acuerdo está deletreada con espacios internos. Medido en el corpus: «-Tasa de Política» aparece bien escrita 119 veces y «T a s a» 9, siempre en la misma posición de la fórmula («el Consejo adopta el siguiente Acuerdo: <número>-Tasa de Política Monetaria»). Es el mismo defecto que el pase del §36 corrigió en la variante «T a sa» de 6 actas; ésta es la variante con las cuatro letras separadas. La posición es fija y no hay lectura alternativa: el número de acuerdo va pegado a la palabra.

### `RPM-2015-09-15:6999:1` — Diego Gianelli Gómez

1. **ACENTO_INDEBIDO**
   - antes: `Polítíca`
   - después: `Política`
   - por qué: Acento espurio en la segunda «i». «Polítíca» no es palabra y aparece 6 veces en el corpus, siempre dentro de «Tasa de Polítíca Monetaria», «Opciones de Polítíca Monetaria», «División Polítíca Financiera» e «Informe de Polítíca Monetaria»; la forma del propio corpus es «Política», con 3.641 apariciones, y los dos PDF del repositorio dan 218 «Política» y 0 «Polítíca». A diferencia de los acentos de §16 (éstos/período/cuánto, donde las dos formas son español legítimo) y del «Seníor» de §27 (donde Sénior 79 y Senior 77 están empatados), aquí el destino no es ambiguo: no existe otra lectura.

### `RPM-2011-05-12:4053:2` — Consejo del Banco Central de Chile

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

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

### `RPM-2010-06-15:3202:1` — Manuel Marfán Lewis

1. **PALABRA_PARTIDA**
   - antes: `en matemáticamente. P or todo lo anterio`
   - después: `en matemáticamente. Por todo lo anterio`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 3613 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2009-09-08:2701:5` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2007-03-15:1167:1` — Vittorio Corbo Lioi

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2013-03-14:5429:1` — Claudio Soto Gamboa

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2012-02-14:4654:1` — Consejo del Banco Central de Chile

1. **ESPACIO_INDEBIDO**
   - antes: `taria en 5 % anual. En`
   - después: `taria en 5% anual. En`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **PUNTUACION**
   - antes: `120214 – Tasa`
   - después: `120214 - Tasa`
   - por qué: Raya en vez de guion como separador del número de acuerdo. Medido en el corpus: 129 filas usan el guion y 2 la raya, en la misma posición fija de la fórmula del Acuerdo.

### `RPM-2014-03-13:6105:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: ` con lo que esperan ios agentes privado`
   - después: ` con lo que esperan los agentes privado`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2011-06-14:4064:1` — Luis Óscar Herrera Barriga

1. **ESPACIO_INDEBIDO**
   - antes: `amente. -4 . f . • " ' A)`
   - después: `amente. -4. f. • " ' A)`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2011-01-13:3716:1` — Consejo del Banco Central de Chile

1. **PALABRA_PARTIDA**
   - antes: `110113-T a sa de Política Monetaria`
   - después: `110113-Tasa de Política Monetaria`
   - por qué: Pase transversal: «Tasa» sale deletreada como «T a sa» dentro del número del Acuerdo. Medido en todo el corpus: la fórmula correcta «Tasa de Política Monetaria» aparece 1.428 veces y la forma deletreada 6, siempre en el mismo lugar —pegada al número del acuerdo, «NN-NN-NNMMDD-T a sa de Política Monetaria»—. No hay ambigüedad: el formato del acuerdo es número-título y el título es siempre el mismo. Se corrige en Texto_Corregido; Texto queda intacto.

### `RPM-2014-09-11:6422:1` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2013-09-12:5760:1` — Sergio Lehmann Beresi

1. **PALABRA_OMITIDA**
   - antes: `un porcentaje muy bajo del mercado esperaba en el mes enero pasado`
   - después: `un porcentaje muy bajo del mercado esperaba en el mes de enero pasado`
   - por qué: Preposición omitida. La forma completa está dos veces en la misma fila: 'en el mes de agosto se estimaba' y 'a contar del mes de enero de 2014'.

### `RPM-2012-05-17:4798:1` — Sergio Lehmann Beresi

1. **PUNTUACION**
   - antes: `se encuentran en los máximos históricos: y que los de Italia`
   - después: `se encuentran en los máximos históricos; y que los de Italia`
   - por qué: Dos puntos en lugar de punto y coma dentro de una enumeración. La propia fila separa los cuatro miembros de la serie con punto y coma ('...y Alemania; que Australia... incrementos; que los de España...'); éste es el único dos puntos y corta la serie justo antes del último miembro. Mismo caso que el de 'Tatiana Vargas Manzo:' en 5754:1.
