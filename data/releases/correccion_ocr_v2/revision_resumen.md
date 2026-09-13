# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1827**
- operaciones: **3181**
- filas marcadas para cotejo: **251**
- sha256 de la base: `eebaa728dc1d7ce14315caebd0c7516ff324b5d4acaefcf40cec2bf6d855945d`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 826 |
| `ESPACIO_INDEBIDO` | 508 |
| `PALABRA_PARTIDA` | 496 |
| `ACENTO_INDEBIDO` | 391 |
| `PUNTUACION` | 283 |
| `SIMBOLO_SUELTO` | 262 |
| `ACENTO_FALTANTE` | 193 |
| `FIRMA_TRUNCADA` | 55 |
| `ESPACIO_FALTANTE` | 41 |
| `RESIDUO_PAGINACION` | 37 |
| `PALABRA_ERRONEA` | 34 |
| `PALABRA_OMITIDA` | 24 |
| `PALABRA_DUPLICADA` | 16 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 5 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2014-09-11:6430:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2011-06-14:4117:1` — José De Gregorio Rebeco

1. **ACENTO_INDEBIDO**
   - antes: `. Hace presente que potencíales aumentos en la `
   - después: `. Hace presente que potenciales aumentos en la `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 72 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
2. **ESPACIO_INDEBIDO**
   - antes: `o central— , las decis`
   - después: `o central—, las decis`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2009-02-12:2352:1` — Matías Bernier Bórquez

1. **ESPACIO_INDEBIDO**
   - antes: ` escenario . Agrega, q`
   - después: ` escenario. Agrega, q`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

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

### `RPM-2009-10-13:2755:1` — Enrique Marshall Rivera

1. **ACENTO_FALTANTE**
   - antes: `olucionado bastante en linea con lo anticipado, `
   - después: `olucionado bastante en línea con lo anticipado, `
   - por qué: Tilde faltante, grupo B3. Se leyeron las 53 apariciones de linea, continua, publica y lineas, y sólo 23 son defecto. «linea»: las 18 son la fórmula «en linea con», siempre el sustantivo, así que van con contexto. «lineas»: las 4 son sustantivo («otras lineas de financiamiento», «algunas lineas manufactureras», «de las lineas vinculadas»). «continua»: de 18 apariciones sólo 2 son el verbo («la actividad económica continua creciendo», «esta parte de la economía continua funcionando»); las otras 16 son el adjetivo continuo/continua y NO se tocan («la continua caída», «la mejora continua», «la convergencia continua y gradual», «la serie no es continua», «de continua colaboración», «de manera continua»). «publica»: las 13 son la tercera persona del verbo publicar («se publica anualmente», «la Reserva Federal no publica su propia», «el INE no los publica», «que publica el Fondo») y ninguna se corrige.

### `RPM-2006-06-15:675:1` — Consejo del Banco Central de Chile

1. **LETRA_CONFUNDIDA**
   - antes: `regorio Rebeco y de ios Consejeros don `
   - después: `regorio Rebeco y de los Consejeros don `
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2012-08-16:5012:1` — Manuel Marfán Lewis

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2007-07-12:1310:1` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `Olivia Recart Asisten también; Gerente General, `
   - después: `Olivia Recart Asisten también: Gerente General, `
   - por qué: Punto y coma por dos puntos. Medido: "Asisten también:" aparece 93 veces y "Asisten también;" 7. La formula introduce una lista, así que corresponde dos puntos.

### `RPM-2010-05-13:3089:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: `De Gregario`
   - después: `De Gregorio`
   - por qué: Apellido dañado por OCR. Medido en el corpus: «De Gregorio» aparece 1150 veces y «De Gregario» 41, siempre referido a la misma persona, José De Gregorio Rebeco, Presidente del Banco Central desde 2008. El campo Actor_Final de las filas afectadas dice «José De Gregorio Rebeco». Confusión de la o por la a en la penúltima sílaba. Mismo tratamiento que las 39 normalizaciones de nombre ya registradas (tipo LETRA_CONFUNDIDA).

### `RPM-2014-12-11:6518:1` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `o; Gerente de División Estudios, don Alberto Naudon Dell'Oro; Gerente de División Operaciones Financieras`
   - después: `o; Gerente de División Estudios, don Alberto Naudon Dell’Oro; Gerente de División Operaciones Financieras`
   - por qué: Normalización de nombre propio dañado, autorizada por el usuario en esta ronda (antes el criterio era marcar sin corregir). La forma correcta la acredita el propio corpus: «Alberto Naudon Dell’Oro» aparece 12 veces (RPM-2014-08-14:6342:1, RPM-2014-10-16:6440:1 y otras) y «Dell'Oro» 3; el apóstrofo curvo es además el mayoritario en el corpus (59 contra 41 rectos). Se unifica a una sola grafía para que la persona tenga un único nombre en la base. No es una conjetura: es la forma que el corpus ya usa para el mismo cargo y la misma persona (Gerente de División Estudios). Caso: «Dell'Oro» con apóstrofo recto. La fila NO estaba dañada: se unifica sólo la grafía del apóstrofo a la mayoritaria para que la persona tenga un único nombre en la base. Es reversible y no altera Texto.
2. **LETRA_CONFUNDIDA**
   - antes: `POLiTICA`
   - después: `POLÍTICA`
   - por qué: Fórmula fija del encabezado de acta. Medido en el corpus: «SESIÓN» aparece 115 veces y «SESION» 14 más «SESiÓN» 2; «POLÍTICA» 111 y «POLITICA» 16 más «POLíTICA» 1 y «POLiTICA» 3. La fórmula completa correcta «SESIÓN DE POLÍTICA MONETARIA» aparece 111 veces contra 14 sin acentos. Es el mismo encabezado en todas las actas, así que la forma canónica no admite duda; el OCR perdió el acento o leyó la Í mayúscula como i minúscula.

### `RPM-2009-06-16:2580:1` — José De Gregorio Rebeco

1. **ESPACIO_INDEBIDO**
   - antes: `n elevadas ,`
   - después: `n elevadas,`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2008-11-13:2137:1` — José De Gregorio Rebeco

1. **PALABRA_DUPLICADA**
   - antes: `osé De Gregorio ofrece la palabra al Gerente de de Análisis Macroeconómico señor Claudio Soto G`
   - después: `osé De Gregorio ofrece la palabra al Gerente de Análisis Macroeconómico señor Claudio Soto G`
   - por qué: Preposición duplicada. Los 13 casos del corpus son la misma lesión y ninguno es legítimo: no hay construcción del español con «de de» seguido de sustantivo. Se corrigieron uno por uno.

### `RPM-2010-03-18:2992:2` — Claudio Soto Gamboa

1. **ESPACIO_INDEBIDO**
   - antes: `es décimas , ya que se`
   - después: `es décimas, ya que se`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **LETRA_CONFUNDIDA**
   - antes: `Claudia Soto`
   - después: `Claudio Soto`
   - por qué: La «a» final ocupó el lugar de la «o» en el nombre de pila. El propio texto lo descarta: la fila lo trata en masculino («señor» o «don») y el corpus atestigua «Claudio Soto» 1.275 veces contra 1 «Claudia Soto». No es la Claudia legítima del corpus (doña Claudia Varela Lértora, doña Claudia Sotz Pantoja), que siempre va con «doña» o «Gerenta».

### `RPM-2008-03-13:1744:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` JORGE DESORMEAUX JIMÉNEZ JOSÉ DE GREGORIO REBECO Vicepresidente Presidente ENRIQUE MARSHALL RIVERA Consejero.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2007-02-08:1061:2` — Sergio Lehmann Beresi

1. **PALABRA_PARTIDA**
   - antes: ` que teníamos en el IP oM de enero, y par`
   - después: ` que teníamos en el IPoM de enero, y par`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2481 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2010-12-16:3632:1` — Luis Óscar Herrera Barriga

1. **ESPACIO_INDEBIDO**
   - antes: `mantuvo •4 .; rezagada`
   - después: `mantuvo •4.; rezagada`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2014-03-13:6057:1` — Consejo del Banco Central de Chile

1. **ESPACIO_INDEBIDO**
   - antes: `ña Poblete ; Gerente d`
   - después: `ña Poblete; Gerente d`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.
2. **LETRA_CONFUNDIDA**
   - antes: ` ei`
   - después: ` el`
   - por qué: «ei» en lugar del artículo «el»: el OCR confunde la «l» con la «i». Sigue un sustantivo masculino, así que no hay otra lectura. Familia de 14 ocurrencias en 13 filas del corpus. §75.

### `RPM-2008-05-08:1844:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `obsen/ada`
   - después: `observada`
   - por qué: La OCR escribe esta letra como «/»: el corpus tiene observada y no tiene la forma con barra fuera de estos casos. Sustitución única que produce una palabra existente.

### `RPM-2014-01-16:5989:2` — Enrique Orellana Cifuentes

1. **ACENTO_INDEBIDO**
   - antes: `observa un panorama coíncídente con el consigna`
   - después: `observa un panorama coincidente con el consigna`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 47 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2010-05-13:3089:2` — Kevin Cowan Logan

1. **ESPACIO_INDEBIDO**
   - antes: `a la banca , pero no s`
   - después: `a la banca, pero no s`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2006-04-13:654:1` — Vittorio Corbo Lioi

1. **LETRA_CONFUNDIDA**
   - antes: ` del último IPOM`
   - después: ` del último IPoM`
   - por qué: Sigla mal compuesta. Medido en el corpus: «IPoM» aparece 2473 veces y «IPOM» 58, siempre el mismo documento, el Informe de Política Monetaria del Banco Central de Chile, cuya sigla lleva la o minúscula. El OCR leyó la o minúscula como O mayúscula.
2. **LETRA_CONFUNDIDA**
   - antes: `n el último IPOM`
   - después: `n el último IPoM`
   - por qué: Sigla mal compuesta. Medido en el corpus: «IPoM» aparece 2473 veces y «IPOM» 58, siempre el mismo documento, el Informe de Política Monetaria del Banco Central de Chile, cuya sigla lleva la o minúscula. El OCR leyó la o minúscula como O mayúscula.

### `RPM-2009-09-08:2708:1` — Enrique Marshall Rivera

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.
2. **ACENTO_FALTANTE**
   - antes: ` mejoren, añade, el estimulo asociado al act`
   - después: ` mejoren, añade, el estímulo asociado al act`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.
3. **ACENTO_FALTANTE**
   - antes: `n general, bastante en linea con lo anticipado, `
   - después: `n general, bastante en línea con lo anticipado, `
   - por qué: Tilde faltante, grupo B3. Se leyeron las 53 apariciones de linea, continua, publica y lineas, y sólo 23 son defecto. «linea»: las 18 son la fórmula «en linea con», siempre el sustantivo, así que van con contexto. «lineas»: las 4 son sustantivo («otras lineas de financiamiento», «algunas lineas manufactureras», «de las lineas vinculadas»). «continua»: de 18 apariciones sólo 2 son el verbo («la actividad económica continua creciendo», «esta parte de la economía continua funcionando»); las otras 16 son el adjetivo continuo/continua y NO se tocan («la continua caída», «la mejora continua», «la convergencia continua y gradual», «la serie no es continua», «de continua colaboración», «de manera continua»). «publica»: las 13 son la tercera persona del verbo publicar («se publica anualmente», «la Reserva Federal no publica su propia», «el INE no los publica», «que publica el Fondo») y ninguna se corrige.
4. **ACENTO_FALTANTE**
   - antes: `desafio`
   - después: `desafío`
   - por qué: Falta el acento. Medido en el corpus: «desafío» aparece 40 veces y «desafio» 3.

### `RPM-2009-03-12:2412:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `e los años 90 se produjo un fenómeno similar Indica que l`
   - después: `e los años 90 se produjo un fenómeno similar. Indica que l`
   - por qué: «también a fines de los años 90 se produjo un fenómeno similar Indica que las estimaciones de crecimiento potencial…» — falta el punto antes del nuevo sujeto.

### `RPM-2006-11-16:978:1` — Klaus Schmidt-Hebbel Dunker

1. **PUNTUACION**
   - antes: `te.`
   - después: `te,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.

### `RPM-2011-04-12:3968:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2010-07-15:3277:2` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` JOSE DE GREGORIO REBECO Presidente IQUE MARSHALL RIVERA Consejero Consejero.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.
2. **ESPACIO_INDEBIDO**
   - antes: `política.” . - El Cons`
   - después: `política.”. - El Cons`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2012-05-17:4826:2` — Ricardo Vicuña Poblete

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2014-08-14:6378:1` — Claudio Raddatz Kiefer

1. **ACENTO_INDEBIDO**
   - antes: `s últimos Informes. Adícionalmente, en cuanto a po`
   - después: `s últimos Informes. Adicionalmente, en cuanto a po`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 71 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
2. **ACENTO_INDEBIDO**
   - antes: `Polítíca`
   - después: `Política`
   - por qué: Acento espurio en la segunda «i». «Polítíca» no es palabra y aparece 6 veces en el corpus, siempre dentro de «Tasa de Polítíca Monetaria», «Opciones de Polítíca Monetaria», «División Polítíca Financiera» e «Informe de Polítíca Monetaria»; la forma del propio corpus es «Política», con 3.641 apariciones, y los dos PDF del repositorio dan 218 «Política» y 0 «Polítíca». A diferencia de los acentos de §16 (éstos/período/cuánto, donde las dos formas son español legítimo) y del «Seníor» de §27 (donde Sénior 79 y Senior 77 están empatados), aquí el destino no es ambiguo: no existe otra lectura.
3. **LETRA_CONFUNDIDA**
   - antes: `n algo más próxima muestra que los descalces cambíanos se mantienen en niveles acotados. Finalmente`
   - después: `n algo más próxima muestra que los descalces cambiarios se mantienen en niveles acotados. Finalmente`
   - por qué: «cambíanos» no es palabra del español; el adjetivo de «cambio» es «cambiario». Los 18 casos del corpus están todos en el mismo contexto —«mercados financieros y cambíanos», «efectos cambíanos», «desalineamientos cambíanos», «ajustes cambíanos»— y en ninguno cabe otra lectura. El corpus tiene 55 «cambiarios» correctos. La «ri» se leyó como «n».
4. **LETRA_CONFUNDIDA**
   - antes: `tenciales riesgos asociados a movimientos cambíanos`
   - después: `tenciales riesgos asociados a movimientos cambiarios`
   - por qué: «cambíanos» no es palabra del español; el adjetivo de «cambio» es «cambiario». Los 18 casos del corpus están todos en el mismo contexto y en ninguno cabe otra lectura; el corpus tiene 55 «cambiarios» correctos. Ancla que empieza en «tenciales» porque la fila ya tiene otra corrección registrada que termina justo antes («Adícionalmente» -> «Adicionalmente»).

### `RPM-2010-05-13:3090:1` — Luis Opazo Roco

1. **ESPACIO_INDEBIDO**
   - antes: `a su cargo , como los `
   - después: `a su cargo, como los `
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2010-02-11:2965:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **PUNTUACION**
   - antes: `Para concluir con la votación,.`
   - después: `Para concluir con la votación,`
   - por qué: Coma seguida de punto al final de la fila. Medido en el corpus: «<palabra>,.» aparece 98 veces en el texto virgen; el pase transversal del §45 corrigió 78 (76 «A continuación,.» más «década,.» y «Euro,.») y dejó estas 20, que son la misma familia con otras palabras: «Continuando con la votación,.» (6), «Para concluir con la votación,.» (3), «No habiendo más comentarios,.» (8), «No habiendo más comentarios y preguntas,.» (2) y «…señor Manuel Marfán,.» (1). En los 20 casos la fila siguiente empieza con «el Presidente…», «el Consejero…» o «el Vicepresidente…», de modo que la coma es la marca correcta y el punto es el signo sobrante. Se aplica el mismo criterio del §45.
