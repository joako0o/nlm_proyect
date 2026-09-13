# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1808**
- operaciones: **3131**
- filas marcadas para cotejo: **241**
- sha256 de la base: `eebaa728dc1d7ce14315caebd0c7516ff324b5d4acaefcf40cec2bf6d855945d`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 819 |
| `ESPACIO_INDEBIDO` | 507 |
| `PALABRA_PARTIDA` | 496 |
| `ACENTO_INDEBIDO` | 390 |
| `PUNTUACION` | 268 |
| `SIMBOLO_SUELTO` | 244 |
| `ACENTO_FALTANTE` | 190 |
| `FIRMA_TRUNCADA` | 55 |
| `ESPACIO_FALTANTE` | 39 |
| `RESIDUO_PAGINACION` | 36 |
| `PALABRA_ERRONEA` | 34 |
| `PALABRA_OMITIDA` | 24 |
| `PALABRA_DUPLICADA` | 16 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2014-11-18:6517:3` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `“`
   - por qué: Comilla recta que abre la cita del Comunicado. Medido en todo el corpus: la formula "Comunicado" va seguida de “ 99 veces y de una recta solo 6. La apertura es inequivoca y la corroboracion es del propio corpus, no de la intuicion.

### `RPM-2011-08-18:4218:1` — Enrique Marshall Rivera

1. **PUNTUACION**
   - antes: `"Zona-Euro: Spread Libor-OIS"`
   - después: `“Zona-Euro: Spread Libor-OIS”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.

### `RPM-2009-02-12:2356:2` — José De Gregorio Rebeco

1. **PALABRA_PARTIDA**
   - antes: `De Gregario, frente al planteam iento del Consejero s`
   - después: `De Gregorio, frente al planteamiento del Consejero s`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 162 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA. Extensión del §55: el tramo original empezaba en «Gregario,» y dejaba fuera el «De » que lo precede, de modo que no había forma de corregir el apellido sin solaparse. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre la misma persona, José De Gregorio Rebeco.
2. **ESPACIO_INDEBIDO**
   - antes: `le prestan , en consec`
   - después: `le prestan, en consec`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **LETRA_CONFUNDIDA**
   - antes: `se/ection`
   - después: `selection`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene selection y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.

### `RPM-2005-03-10:161:1` — Luis Óscar Herrera Barriga

1. **PALABRA_PARTIDA**
   - antes: `os con la inversión exi stente. Al respecto, e`
   - después: `os con la inversión existente. Al respecto, e`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 40 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
2. **PALABRA_PARTIDA**
   - antes: `e lo anterior puede ten er algunos efectos`
   - después: `e lo anterior puede tener algunos efectos`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 1011 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
3. **PALABRA_PARTIDA**
   - antes: `m arginales`
   - después: `marginales`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 116 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
4. **PALABRA_PARTIDA**
   - antes: `m eses`
   - después: `meses`
   - por qué: Palabra partida por un espacio espurio: la forma junta aparece 4246 veces en el corpus y la segunda mitad por separado no es una palabra. La primera mitad es una letra suelta, que no es palabra española salvo a/y/o/e/u.
5. **PALABRA_PARTIDA**
   - antes: `Estados Uni dos están`
   - después: `Estados Unidos están`
   - por qué: Palabra partida por un espacio espurio, con la segunda mitad reducida a una letra: «Uni dos» -> «Unidos». La evidencia es interna y doble: el primer trozo («Uni») es marginal en el corpus (1 apariciones, y ésas son ésta) y la forma junta («Unidos») es la que el propio corpus usa 2782 veces. La encontró detector_partida_letra, agregado en §31 porque detector_partida no puede verla: su guarda «segunda mitad con frecuencia < 50» bloquea justo las letras (a=37.528, o, e, s), que son frecuentes porque este mismo defecto las esparce. Precisión medida del detector: 40 candidatos en las 9.723 filas, 40 verdaderos; el único que no se corrige aquí es el de 147:1, que es la cola de una carrera letra por letra y se arregla entero en su pasada.

### `RPM-2009-11-12:2770:2` — Claudio Soto Gamboa

1. **ACENTO_FALTANTE**
   - antes: `tores, como algunas lineas manufactureras,`
   - después: `tores, como algunas líneas manufactureras,`
   - por qué: Tilde faltante, grupo B3. Se leyeron las 53 apariciones de linea, continua, publica y lineas, y sólo 23 son defecto. «linea»: las 18 son la fórmula «en linea con», siempre el sustantivo, así que van con contexto. «lineas»: las 4 son sustantivo («otras lineas de financiamiento», «algunas lineas manufactureras», «de las lineas vinculadas»). «continua»: de 18 apariciones sólo 2 son el verbo («la actividad económica continua creciendo», «esta parte de la economía continua funcionando»); las otras 16 son el adjetivo continuo/continua y NO se tocan («la continua caída», «la mejora continua», «la convergencia continua y gradual», «la serie no es continua», «de continua colaboración», «de manera continua»). «publica»: las 13 son la tercera persona del verbo publicar («se publica anualmente», «la Reserva Federal no publica su propia», «el INE no los publica», «que publica el Fondo») y ninguna se corrige.

### `RPM-2006-06-15:688:1` — Vittorio Corbo Lioi

1. **LETRA_CONFUNDIDA**
   - antes: `rio Corbo en relación ai precio del cobre, que`
   - después: `rio Corbo en relación al precio del cobre, que`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2012-10-18:5100:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2007-07-12:1316:2` — Sergio Lehmann Beresi

1. **SALTOS_DE_LINEA**
   - antes: ` reales del mercado inmobiliari o. Estima que tod`
   - después: ` reales del mercado inmobiliario. Estima que tod`
   - por qué: Palabra partida por la justificación del PDF ("inmobiliari o"). La palabra es inequívoca y está atestiguada en el corpus; en la misma fila aparece varias veces completa.

### `RPM-2010-05-13:3124:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `e de las noticias de! Ministro respec`
   - después: `e de las noticias del Ministro respec`
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2015-02-12:6627:1` — Alberto Naudon Dell'Oro

1. **ACENTO_INDEBIDO**
   - antes: ` para aquellas cuyo financíamiento está más ligado`
   - después: ` para aquellas cuyo financiamiento está más ligado`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 440 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2009-06-16:2597:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: ` plazo que no sea compensado por movimientos cambíanos; o, simplemente, una recuperación más rápida`
   - después: ` plazo que no sea compensado por movimientos cambiarios; o, simplemente, una recuperación más rápida`
   - por qué: «cambíanos» no es palabra del español; el adjetivo de «cambio» es «cambiario». Los 18 casos del corpus están todos en el mismo contexto —«mercados financieros y cambíanos», «efectos cambíanos», «desalineamientos cambíanos», «ajustes cambíanos»— y en ninguno cabe otra lectura. El corpus tiene 55 «cambiarios» correctos. La «ri» se leyó como «n».

### `RPM-2008-11-13:2141:2` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarla`
   - después: `cambiaria`
   - por qué: cambiarla por cambiaria. Misma familia y mismo defecto. Medido: 8 apariciones (todas dentro de "cambiarlas"), todas adjetivas y revisadas una por una: "paridades cambiarlas" 4 veces, "implicancias cambiarlas" 2, "expectativas cambiarlas" 1, "coberturas cambiarlas" 1. "cambiarias" ya aparece 19 veces en el corpus.

### `RPM-2010-04-15:3023:1` — Consejo del Banco Central de Chile

1. **ESPACIO_FALTANTE**
   - antes: `celebrada el15 de abril de 2010`
   - después: `celebrada el 15 de abril de 2010`
   - por qué: Falta el espacio entre el artículo y la cifra en el encabezado formulaico del acta. Evidencia de fuente: el PDF de 2005-06-09, de la misma serie, escribe el mismo encabezado con espacio («Celebrada el 9 de junio de 2005»), mientras el de 2005-07-12 sale pegado («celebrada el12»); la diferencia es un artefacto de extracción, no una variante del acta. La fecha queda confirmada por el cuerpo de la misma oración y por el nombre del archivo.

### `RPM-2008-04-10:1747:1` — Sergio Lehmann Beresi

1. **ESPACIO_FALTANTE**
   - antes: `yeso`
   - después: `y eso`
   - por qué: yeso por "y eso". Medido: 13 apariciones, en todas falta el espacio entre la conjuncion y el demostrativo ("alto yeso tiene que tener" = "alto, y eso tiene que tener"). Verificado que ninguna esta embebida en otra palabra. La coma no se inserta: la oracion queda gramatical sin ella y anadirla seria editar puntuacion.
2. **PUNTUACION**
   - antes: `"Dificultad para encontrar empleo"`
   - después: `“Dificultad para encontrar empleo”`
   - por qué: Comilla recta en un par completo. En esta fila las comillas rectas son pares y su direccion es deducible sin ambiguedad: la primera de cada par abre y la segunda cierra. El corpus usa comillas tipograficas de forma abrumadora (“ aparece 323 veces), de modo que la recta es un residuo del escaneo y no una eleccion del texto. Medido: de las 58 comillas rectas que quedaban, 52 estan en 23 filas con cantidad par (20 filas con 2 y 3 filas con 4) y son estas; las otras 6 estan en filas de cantidad impar y se dejan marcadas para cotejo.
3. **PALABRA_PARTIDA**
   - antes: `alta demanda de las econom ías emergentes.
Asi`
   - después: `alta demanda de las economías emergentes.
Asi`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2935 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
4. **ACENTO_INDEBIDO**
   - antes: `ñor Gerente que las noticías son claramente `
   - después: `ñor Gerente que las noticias son claramente `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 944 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
5. **ACENTO_INDEBIDO**
   - antes: `n en lo que son las tendencías
inflacionarias.`
   - después: `n en lo que son las tendencias
inflacionarias.`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 225 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
6. **ESPACIO_INDEBIDO**
   - antes: `
del cobre ,
particula`
   - después: `
del cobre,
particula`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
7. **ESPACIO_INDEBIDO**
   - antes: ` del cobre , este
se h`
   - después: ` del cobre, este
se h`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
8. **ESPACIO_INDEBIDO**
   - antes: `imo
de 4,1 %. Destaca `
   - después: `imo
de 4,1%. Destaca `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
9. **ESPACIO_INDEBIDO**
   - antes: ` comercial , si bien
e`
   - después: ` comercial, si bien
e`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
10. **PALABRA_ERRONEA**
   - antes: `creciendo
e.n
Ií ~ea con el mayor`
   - después: `creciendo en línea con el mayor`
   - por qué: Tramo dañado por el OCR, con saltos de línea incluidos: «e.n Ií ~ea» por «en línea». La reconstrucción es única porque «en línea con» es una expresión fija del corpus y es lo único que encaja entre «las solicitudes de desempleo han ido creciendo» y «con el mayor desempleo».

### `RPM-2007-02-08:1068:1` — Jorge Desormeaux Jiménez

1. **LETRA_CONFUNDIDA**
   - antes: ` proyecciones del Consesus Forecast o JP Mor`
   - después: ` proyecciones del Consensus Forecast o JP Mor`
   - por qué: Consesus por Consensus: falta una n. Medido: "Consensus" aparece 127 veces en 99 filas y "Consesus" 8 veces en 6, siempre en el nombre propio "Consensus Forecast". No hay lectura alternativa.
2. **LETRA_CONFUNDIDA**
   - antes: `n de depreciación de! yuan en un 10% `
   - después: `n de depreciación del yuan en un 10% `
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2011-01-13:3709:1` — Felipe Larraín Bascuñán

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2014-03-13:6114:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` MARSHALL RIVERA RODRIGO VERGARA MONTES Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2008-05-08:1847:1` — Jorge Desormeaux Jiménez

1. **SIMBOLO_SUELTO**
   - antes: `una dirección u otra. U U) Menciona`
   - después: `una dirección u otra. Menciona`
   - por qué: Dos residuos seguidos, "U" y "U)": la regla general de letra suelta solo quitaria el primero y dejaria "U) Menciona". Se eliminan los dos en una sola operacion porque son adyacentes y forman un unico bloque de ruido entre las dos oraciones.

### `RPM-2014-02-18:6055:3` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2010-05-13:3126:1` — José De Gregorio Rebeco

1. **PALABRA_PARTIDA**
   - antes: `riendo espacio para em pezar el proceso de n`
   - después: `riendo espacio para empezar el proceso de n`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 33 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2006-05-11:659:1` — Esteban Jadresic Marinovic

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2009-10-13:2725:5` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.

### `RPM-2009-03-12:2436:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `/PoM`
   - después: `IPoM`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene IPoM y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.

### `RPM-2006-12-14:1001:1` — Rodrigo Valdés Pulido

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2011-05-12:4053:2` — Consejo del Banco Central de Chile

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2010-08-12:3314:1` — Enrique Marshall Rivera

1. **ESPACIO_INDEBIDO**
   - antes: ` dos temas . Señala qu`
   - después: ` dos temas. Señala qu`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **ESPACIO_INDEBIDO**
   - antes: ` un empleo . A título `
   - después: ` un empleo. A título `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
3. **ESPACIO_INDEBIDO**
   - antes: ` la semana , se consid`
   - después: ` la semana, se consid`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
4. **ESPACIO_INDEBIDO**
   - antes: `yor empleo , que la an`
   - después: `yor empleo, que la an`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
5. **ESPACIO_INDEBIDO**
   - antes: ` reflejado .`
   - después: ` reflejado.`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2012-07-12:4938:1` — Claudio Soto Gamboa

1. **PALABRA_PARTIDA**
   - antes: `dio Soto continúa, informando que el tipo de cambo nominal tendió a apreciarse, tanto en lo que`
   - después: `dio Soto continúa, informando que el tipo de cambio nominal tendió a apreciarse, tanto en lo que`
   - por qué: «el tipo de cambo nominal» — falta la «i». El corpus escribe «cambio» 2.948 veces y «cambo» aparece una sola vez en todo el corpus, aquí.

### `RPM-2014-09-11:6439:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` E MARSHALL RIVERA RODRIGO VERGARA MONTES Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2010-05-13:3126:2` — Consejo del Banco Central de Chile

1. **PALABRA_PARTIDA**
   - antes: `T a s a`
   - después: `Tasa`
   - por qué: La palabra «Tasa» de la fórmula del Acuerdo está deletreada con espacios internos. Medido en el corpus: «-Tasa de Política» aparece bien escrita 119 veces y «T a s a» 9, siempre en la misma posición de la fórmula («el Consejo adopta el siguiente Acuerdo: <número>-Tasa de Política Monetaria»). Es el mismo defecto que el pase del §36 corrigió en la variante «T a sa» de 6 actas; ésta es la variante con las cuatro letras separadas. La posición es fija y no hay lectura alternativa: el número de acuerdo va pegado a la palabra.

### `RPM-2010-03-18:3008:3` — Felipe Larraín Bascuñán

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.
