# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1771**
- operaciones: **3062**
- filas marcadas para cotejo: **237**
- sha256 de la base: `eebaa728dc1d7ce14315caebd0c7516ff324b5d4acaefcf40cec2bf6d855945d`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 757 |
| `ESPACIO_INDEBIDO` | 507 |
| `PALABRA_PARTIDA` | 496 |
| `ACENTO_INDEBIDO` | 390 |
| `PUNTUACION` | 268 |
| `SIMBOLO_SUELTO` | 242 |
| `ACENTO_FALTANTE` | 190 |
| `FIRMA_TRUNCADA` | 55 |
| `RESIDUO_PAGINACION` | 36 |
| `ESPACIO_FALTANTE` | 35 |
| `PALABRA_ERRONEA` | 33 |
| `PALABRA_OMITIDA` | 24 |
| `PALABRA_DUPLICADA` | 16 |
| `SALTOS_DE_LINEA` | 10 |
| `PALABRA_SOBRANTE` | 3 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2015-04-16:6693:1` — Rodrigo Vergara Montes

1. **ESPACIO_INDEBIDO**
   - antes: `ington D C . A continu`
   - después: `ington D C. A continu`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2011-08-18:4279:1` — José De Gregorio Rebeco

1. **ESPACIO_INDEBIDO**
   - antes: `a 5,75 o 6 %. Hace not`
   - después: `a 5,75 o 6%. Hace not`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2009-02-12:2358:1` — María Olivia Recart Herrera

1. **ESPACIO_INDEBIDO**
   - antes: `dit crunch .`
   - después: `dit crunch.`
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

### `RPM-2006-06-15:688:1` — Vittorio Corbo Lioi

1. **LETRA_CONFUNDIDA**
   - antes: `rio Corbo en relación ai precio del cobre, que`
   - después: `rio Corbo en relación al precio del cobre, que`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2012-10-18:5160:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` MARFÁN LEWIS RODRIGO VENGARA MONTES Presidente Vicepresidente ENRIQUE MARSHALL RIVERA Consejero.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2007-07-12:1321:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `ios gráficos, el efecto fiy to quality sobre Chile s`
   - después: `los gráficos, el efecto fly to quality sobre Chile s`
   - por qué: "fiy"/"fIy" por "fly": la l se leyo como i (o como I). Es el mismo glifo que produce "ai" por "al", demostrado con 26 casos independientes. Se retira la marca RECONSTRUCCION_AMBIGUA que se había puesto en esta fila: al aparecer la regla de glifo, la ambigüedad se resuelve. Un escáner no convierte "flight" en "fiy" (sería borrar cuatro letras); sí convierte "fly" en "fiy". Las 21 apariciones de "flight to quality" que hay en el corpus son la otra grafía, correcta, y no se tocan. La operación se extendió dos caracteres hacia la izquierda para cubrir además "ios" por "los" (§12): ambas caen en el mismo tramo y dos operaciones separadas se pisarían, porque el fragmento anterior empezaba justo en la s de "ios".

### `RPM-2010-06-15:3131:2` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `e alguna manera, en ios mercados americ`
   - después: `e alguna manera, en los mercados americ`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2015-05-14:6792:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `aro se refiere a la Índexación de los salarios`
   - después: `aro se refiere a la indexación de los salarios`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 149 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
2. **ACENTO_INDEBIDO**
   - antes: `, el coeficiente de Índexación implícito es ba`
   - después: `, el coeficiente de indexación implícito es ba`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 157 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
3. **ACENTO_INDEBIDO**
   - antes: `ce que con una alta Índexación y salarios real`
   - después: `ce que con una alta indexación y salarios real`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 157 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
4. **ACENTO_INDEBIDO**
   - antes: `an por efecto de la Índexación, ya que ello su`
   - después: `an por efecto de la indexación, ya que ello su`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 157 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

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

### `RPM-2008-11-13:2159:1` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.

### `RPM-2010-04-15:3033:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarla`
   - después: `cambiaria`
   - por qué: cambiarla por cambiaria. Misma familia y mismo defecto. Medido: 8 apariciones (todas dentro de "cambiarlas"), todas adjetivas y revisadas una por una: "paridades cambiarlas" 4 veces, "implicancias cambiarlas" 2, "expectativas cambiarlas" 1, "coberturas cambiarlas" 1. "cambiarias" ya aparece 19 veces en el corpus.
2. **ACENTO_FALTANTE**
   - antes: `lica que si bien es bastante marginal, seria de alrededor de`
   - después: `lica que si bien es bastante marginal, sería de alrededor de`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.

### `RPM-2008-04-10:1770:1` — Claudio Soto Gamboa

1. **ACENTO_INDEBIDO**
   - antes: `ero señor Marshall, índica que la estimaci`
   - después: `ero señor Marshall, indica que la estimaci`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2007-02-08:1074:1` — José De Gregorio Rebeco

1. **ACENTO_FALTANTE**
   - antes: `el escenario que se tenia hace uno y dos `
   - después: `el escenario que se tenía hace uno y dos `
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».

### `RPM-2011-01-13:3714:1` — Manuel Marfán Lewis

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2014-06-12:6257:1` — Miguel Fuentes Díaz

1. **ESPACIO_INDEBIDO**
   - antes: `isponible— , equivalen`
   - después: `isponible—, equivalen`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2008-06-10:1852:1` — José De Gregorio Rebeco

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2014-04-17:6144:1` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: `a las proyecciones, índica que en línea co`
   - después: `a las proyecciones, indica que en línea co`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
2. **ACENTO_INDEBIDO**
   - antes: `comercíalizadoras`
   - después: `comercializadoras`
   - por qué: «las empresas comercíalizadoras de automóviles» — el acento está corrido una sílaba y la forma resultante no es palabra española. El corpus tiene 15 «comercialización», 1 «Comercializadora», «comercializan», «comercializar» y «comercializarse», ninguna con ese acento. §73.
3. **PALABRA_PARTIDA**
   - antes: `exporta-ciones`
   - después: `exportaciones`
   - por qué: «el notorio aumento de las exporta-ciones mineras» — guion de salto de línea del original que dejó la palabra partida en dos. El corpus tiene 679 «exportaciones». §73.

### `RPM-2010-06-15:3134:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.

### `RPM-2006-05-11:659:1` — Esteban Jadresic Marinovic

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2009-10-13:2733:2` — Claudio Soto Gamboa

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2009-03-12:2438:2` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `“`
   - por qué: Comilla recta que abre una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.
2. **PALABRA_PARTIDA**
   - antes: `T a s a`
   - después: `Tasa`
   - por qué: La palabra «Tasa» de la fórmula del Acuerdo está deletreada con espacios internos. Medido en el corpus: «-Tasa de Política» aparece bien escrita 119 veces y «T a s a» 9, siempre en la misma posición de la fórmula («el Consejo adopta el siguiente Acuerdo: <número>-Tasa de Política Monetaria»). Es el mismo defecto que el pase del §36 corrigió en la variante «T a sa» de 6 actas; ésta es la variante con las cuatro letras separadas. La posición es fija y no hay lectura alternativa: el número de acuerdo va pegado a la palabra.

### `RPM-2006-12-14:1001:1` — Rodrigo Valdés Pulido

1. **SIMBOLO_SUELTO**
   - antes: `A continuación,.`
   - después: `A continuación,`
   - por qué: Pase transversal. La fila termina en «A continuación,.» y la fila siguiente empieza siempre en minúscula con «el señor Presidente ofrece la palabra al…»: unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción normal del acta. El punto que sigue a la coma no pertenece a la oración; es un residuo del salto de párrafo de la fuente. Medido sobre las 9.724 filas: 76 apariciones, las 76 al final de una fila, las 76 con la fila siguiente en minúscula y en la misma sesión, cero excepciones y ninguna aparición en medio de una fila. La forma correcta «A continuación,» seguida de minúscula aparece 378 veces. Se quita el punto y se conserva la coma; Texto queda intacto.

### `RPM-2011-06-14:4109:3` — Felipe Larraín Bascuñán

1. **ESPACIO_INDEBIDO**
   - antes: `creció 3,1 %. En los ú`
   - después: `creció 3,1%. En los ú`
   - por qué: Espacio insertado antes del signo. En español el signo va pegado a la palabra o a la cifra que lo precede: no hay lectura en que el espacio sea correcto. Evidencia de fuente (§18): los dos PDFs del repositorio dan 0 ocurrencias del patrón y las 90 filas del corpus de esas mismas sesiones también, así que no es una característica del acta. La operación sólo quita el blanco; no altera ninguna palabra ni ninguna cifra.

### `RPM-2010-08-12:3331:1` — Pablo García Silva

1. **ACENTO_FALTANTE**
   - antes: `s de forma aislada. podrian sugerir un incr`
   - después: `s de forma aislada, podrían sugerir un incr`
   - por qué: El punto en vez de coma quedó dentro del tramo de una operación ya registrada, que arreglaba otro defecto del mismo tramo (un acento, un espacio o una basura de OCR) y no tocaba el signo. Se enmienda el Despues en vez de apilar una segunda operación: dos tramos solapados sobre el mismo texto virgen no se pueden aplicar en ningún orden. La oración continúa en minúscula, de modo que el punto no puede ser de cierre y la marca correcta es la coma.

### `RPM-2012-09-13:5054:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2015-02-12:6618:3` — Miguel Fuentes Díaz

1. **ESPACIO_FALTANTE**
   - antes: `que sube a100%`
   - después: `que sube a 100%`
   - por qué: Falta el espacio entre la preposición y la cifra: «a100%» no es una palabra. Mismo caso ya registrado en el corpus («un13% en febrero» → «un 13%»).

### `RPM-2010-06-15:3143:1` — José De Gregorio Rebeco

1. **PUNTUACION**
   - antes: `rothers.,`
   - después: `rothers,`
   - por qué: Punto antes de una coma. Medido en el corpus: «.,» aparece 24 veces en el texto corregido, pero 20 son legítimas (abreviaturas «EE.UU.», «S.A.», «etc.», «v.gr.» e iniciales de nombre como «Velasco B.,»). Las 4 restantes tienen antes una palabra completa en minúscula o un signo de porcentaje, no una abreviatura, y el punto es sobrante.
2. **LETRA_CONFUNDIDA**
   - antes: `Beam Stearns`
   - después: `Bear Stearns`
   - por qué: Nombre dañado por OCR: «Beam Stearns» por «Bear Stearns», el banco de inversión cuya quiebra en septiembre de 2008 abre la crisis financiera. Confusión de la erre por la eme, clásica en OCR. Medido en el corpus: «Beam Stearns» aparece 5 veces y «Bear Stearns» 1, de modo que la forma correcta está atestiguada por el propio corpus aunque sea minoritaria; los cinco contextos son inequívocos («cuando alrededor de julio del año 2008», «en el momento en que quebró», «la crisis de»). Se corrige y se deja constancia aquí de que es el primer caso en que la forma canónica es minoritaria: la decisión no descansa en la frecuencia sino en que la entidad es única y el corpus la atestigua.

### `RPM-2010-03-18:3019:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `Para concluir con la votación,.`
   - después: `Para concluir con la votación,`
   - por qué: Coma seguida de punto al final de la fila. Medido en el corpus: «<palabra>,.» aparece 98 veces en el texto virgen; el pase transversal del §45 corrigió 78 (76 «A continuación,.» más «década,.» y «Euro,.») y dejó estas 20, que son la misma familia con otras palabras: «Continuando con la votación,.» (6), «Para concluir con la votación,.» (3), «No habiendo más comentarios,.» (8), «No habiendo más comentarios y preguntas,.» (2) y «…señor Manuel Marfán,.» (1). En los 20 casos la fila siguiente empieza con «el Presidente…», «el Consejero…» o «el Vicepresidente…», de modo que la coma es la marca correcta y el punto es el signo sobrante. Se aplica el mismo criterio del §45.
2. **PUNTUACION**
   - antes: `iste.`
   - después: `iste,`
   - por qué: Punto en vez de coma. Medido en el corpus: un punto seguido de espacio y de una palabra en minúscula aparece 109 veces; de esas, 18 son abreviaturas legítimas cuyo punto les pertenece («EE.UU.» 10, «hrs.» 6, «pp.» 1, «pb.» 1), 4 son basura de OCR tras el punto y 10 son palabras sueltas de margen o encabezados residuales («votación» 4, «interno» 3, «comentarios», «mencionada», «caso», «internamente»). Quedan 91 en que la oración continúa en minúscula y por tanto el punto no puede ser de cierre: la marca correcta es la coma. Cada caso se leyó uno por uno.
