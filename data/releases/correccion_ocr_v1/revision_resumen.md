# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1069**
- operaciones: **1539**
- filas marcadas para cotejo: **184**
- sha256 de la base: `d0b64842cd756df4c50d2960d9bbf01c4c45e5df28609d7b612c5d666593da75`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 446 |
| `ACENTO_INDEBIDO` | 348 |
| `PALABRA_PARTIDA` | 319 |
| `PUNTUACION` | 106 |
| `ACENTO_FALTANTE` | 79 |
| `SIMBOLO_SUELTO` | 78 |
| `FIRMA_TRUNCADA` | 55 |
| `RESIDUO_PAGINACION` | 27 |
| `PALABRA_ERRONEA` | 26 |
| `PALABRA_OMITIDA` | 22 |
| `ESPACIO_FALTANTE` | 14 |
| `SALTOS_DE_LINEA` | 10 |
| `ESPACIO_INDEBIDO` | 4 |
| `PALABRA_DUPLICADA` | 3 |
| `PALABRA_SOBRANTE` | 2 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2012-09-13:5093:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` MANUEL MARFÁN LEWIS RODRIGO VERGARA MONTES Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2005-04-07:206:3` — Pablo García Silva

1. **SIMBOLO_SUELTO**
   - antes: `últimos meses. V La colocación`
   - después: `últimos meses. La colocación`
   - por qué: Letra mayúscula suelta entre dos oraciones. Es ruido de escaneo: la oración anterior termina en punto y la siguiente empieza con mayúscula y sentido completo, así que la letra no pertenece a ninguna de las dos. Medido: 17 casos en 17 filas, con las letras V, H, L, U, A, M, Y, B. Se revisaron uno por uno; el único que NO es residuo es RPM-2007-01-11:1055:1 ("prolongado. A SU juicio"), donde la A abre la oración legítimamente y el defecto es "SU" en mayúscula, que se trata aparte.

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

### `RPM-2007-05-10:1254:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2008-06-10:1895:1` — Claudio Soto Gamboa

1. **LETRA_CONFUNDIDA**
   - antes: `, porque en general ios ajustes son muy`
   - después: `, porque en general los ajustes son muy`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2015-08-13:6947:1` — Miguel Fuentes Díaz

1. **PALABRA_OMITIDA**
   - antes: `destaca que la caída del 25% de la producción minera anunciada para año fiscal tiene un impacto notorio`
   - después: `destaca que la caída del 25% de la producción minera anunciada para el año fiscal tiene un impacto notorio`
   - por qué: Falta el artículo: 'anunciada para año fiscal' no es gramatical y la reparación es única, porque el OCR omite y no agrega palabras. Corroborada donde el criterio exige: 'para el año fiscal' aparece 1 vez en esta misma sesión y 3 en el corpus. Mismo criterio que 'para año 2015' en 6920:1, ronda 178.

### `RPM-2013-09-12:5760:1` — Sergio Lehmann Beresi

1. **PALABRA_OMITIDA**
   - antes: `un porcentaje muy bajo del mercado esperaba en el mes enero pasado`
   - después: `un porcentaje muy bajo del mercado esperaba en el mes de enero pasado`
   - por qué: Preposición omitida. La forma completa está dos veces en la misma fila: 'en el mes de agosto se estimaba' y 'a contar del mes de enero de 2014'.

### `RPM-2011-05-12:4041:1` — Manuel Marfán Lewis

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.

### `RPM-2015-05-14:6802:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2009-09-08:2708:1` — Enrique Marshall Rivera

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.

### `RPM-2007-11-13:1562:1` — Beltrán de Ramón Acevedo

1. **LETRA_CONFUNDIDA**
   - antes: `IRC`
   - después: `IPC`
   - por qué: IRC por IPC. Medido en todo el corpus: 71 apariciones, ninguna en un contexto donde IRC sea una sigla legitima; 61 sueltas y 10 dentro de IRCX1, que tambien debe leerse IPCX1 porque la misma fila escribe IPCX e IPCX2. Regla de bloque revisada caso por caso.

### `RPM-2010-02-11:2891:4` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `ente en Europa, por ios motivos expuest`
   - después: `ente en Europa, por los motivos expuest`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2015-08-13:6952:1` — Miguel Fuentes Díaz

1. **SIMBOLO_SUELTO**
   - antes: `con la positiva en servicios. , . . , Anaí ? ! £ , Ias medldas de inflación subyacente permanecen elevadas`
   - después: `con la positiva en servicios. Las medidas de inflación subyacente permanecen elevadas`
   - por qué: RESIDUO Y DOS PALABRAS DAÑADAS EN EL MISMO TRAMO, corregidos juntos porque se pisarían si se separaran. Entre dos oraciones hay una cadena de glifos que no forma nada (coma, punto, punto, coma, 'Anaí', interrogación, exclamación, signo de libra, coma; verificados por codepoint: 0x2c 0x2e 0x2e 0x2c 0x41 0x6e 0x61 0xed 0x3f 0x21 0xa3 0x2c) y a continuación 'Ias medldas' por 'Las medidas', con i mayúscula por ele y ele por i. MEDIDO: 'Anaí' aparece 1 sola vez en todo el corpus, 'medldas' 1 e 'Ias ' 1, así que no hay otro uso que proteja la cadena; y 'Las medidas' aparece 54 veces. La oración siguiente ya empieza con mayúscula implícita y no se repone ningún signo.
2. **PALABRA_PARTIDA**
   - antes: `Resalta que su com portam iento ha mostrado bastante estabilidad en doce meses`
   - después: `Resalta que su comportamiento ha mostrado bastante estabilidad en doce meses`
   - por qué: Una sola palabra partida por DOS espacios: 'com portam iento' por 'comportamiento'. Se reúne sin alterar una letra, sección 1 ter.
3. **PALABRA_PARTIDA**
   - antes: `informa que se ha corregido en form a importante al alza, situándose en 4,5% a diciembre`
   - después: `informa que se ha corregido en forma importante al alza, situándose en 4,5% a diciembre`
   - por qué: Palabra partida: 'form a' por 'forma'. Sección 1 ter, se reúne sin alterar una letra.
4. **PALABRA_PARTIDA**
   - antes: `en enero de 2016, registraría una variación m ensual de 0,5%`
   - después: `en enero de 2016, registraría una variación mensual de 0,5%`
   - por qué: Palabra partida: 'm ensual' por 'mensual'. Sección 1 ter.
5. **PALABRA_PARTIDA**
   - antes: `por la entrada en vigencia de las modificaciones a la Ley sobre Im puesto de Timbres y Estampillas`
   - después: `por la entrada en vigencia de las modificaciones a la Ley sobre Impuesto de Timbres y Estampillas`
   - por qué: Palabra partida: 'Im puesto' por 'Impuesto'. Sección 1 ter. Es el nombre de una ley, pero la reparación no toca la identidad del nombre: sólo reúne las letras que ya están.
6. **PALABRA_PARTIDA**
   - antes: `si bien las brechas de actividad han sido menores, la evolución del tipo de cam bio plantea un riesgo`
   - después: `si bien las brechas de actividad han sido menores, la evolución del tipo de cambio plantea un riesgo`
   - por qué: Palabra partida: 'cam bio' por 'cambio'. Sección 1 ter.
7. **LETRA_CONFUNDIDA**
   - antes: `llevaría al IPC en doce meses a 4,9% y ai IPCSAE a 4,4%`
   - después: `llevaría al IPC en doce meses a 4,9% y al IPCSAE a 4,4%`
   - por qué: 'ai' no es palabra: es 'al' con la ele leída como i. La oración no admite otra lectura y el paralelo inmediato lo confirma, porque la misma frase acaba de decir 'llevaría al IPC'. Medido: 'al IPCSAE' aparece 2 veces en el corpus y 'ai IPCSAE' 1. Sección 2 bis: la forma defectuosa no es palabra, así que no hay lectura alternativa que proteger.
8. **ACENTO_FALTANTE**
   - antes: `las expectativas de inflación a uno y dos anos medidas por la Encuesta de Expectativas Económicas`
   - después: `las expectativas de inflación a uno y dos años medidas por la Encuesta de Expectativas Económicas`
   - por qué: Falta la tilde de la eñe: 'anos' por 'años'. Sección 1, la oración no admite otra lectura. Medido: 'años' aparece 1.543 veces en el corpus y ' anos ' con espacios 1 sola.
9. **LETRA_CONFUNDIDA**
   - antes: `señala que la depreciación cambiaría ha sido mayor que la sugerida por los fundamentos`
   - después: `señala que la depreciación cambiaria ha sido mayor que la sugerida por los fundamentos`
   - por qué: Tilde o ele por i en posición de adjetivo. La sección 3 ter manda corregir estas formas por muchas veces que se repitan, porque 'cambiaría'/'cambiarlas' son formas verbales y en este lugar sólo cabe el adjetivo. No se pide corroboración en la fila ni en la sesión para esta familia.
10. **LETRA_CONFUNDIDA**
   - antes: `que han coincidido con eventos de intervención cambiaría en particular el anuncio de intervención en el año 2011`
   - después: `que han coincidido con eventos de intervención cambiaria en particular el anuncio de intervención en el año 2011`
   - por qué: Tilde o ele por i en posición de adjetivo. La sección 3 ter manda corregir estas formas por muchas veces que se repitan, porque 'cambiaría'/'cambiarlas' son formas verbales y en este lugar sólo cabe el adjetivo. No se pide corroboración en la fila ni en la sesión para esta familia. Falta además una coma antes de 'en particular', pero la sección 7 prohíbe reponer un signo y queda documentada en la marca de esta misma fila.

### `RPM-2007-04-12:1216:1` — Enrique Marshall Rivera

1. **LETRA_CONFUNDIDA**
   - antes: `en tomo a`
   - después: `en torno a`
   - por qué: en tomo a por "en torno a". Medido: 24 apariciones (20 "en tomo a" y 4 "en tomo al"), la r leida como m. "tomo" es palabra real (volumen) pero ningun contexto lo admite. "en torno a" aparece 1.678 veces.

### `RPM-2014-03-13:6092:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2013-01-17:5316:1` — Luis Óscar Herrera Barriga

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2007-09-13:1444:1` — Vittorio Corbo Lioi

1. **ACENTO_FALTANTE**
   - antes: `cuando se trató de obtener las lineas de créditos correspondientes`
   - después: `cuando se trató de obtener las líneas de créditos correspondientes`
   - por qué: Tilde ausente. 'línea' es palabra llana terminada en vocal con hiato: siempre lleva tilde; 'lineas' no existe en español. Sección 1, no exige corroboración. Medido: 'lineas' sin tilde aparece 6 veces (1438:2, 1444:1, 2725:1, 2770:2, 2814:3, 3107:2) frente a 'líneas' 118.

### `RPM-2015-08-13:6953:2` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `la significativa magnitud de la depreciación ocurrida tras el episodio de intervención cambiaría podría estar dando cuenta`
   - después: `la significativa magnitud de la depreciación ocurrida tras el episodio de intervención cambiaria podría estar dando cuenta`
   - por qué: Tilde por i en posición de adjetivo: 'intervención cambiaria'. La sección 3 ter manda corregir la familia 'cambiar*' sin corroboración porque la forma verbal es imposible en este lugar y sólo cabe el adjetivo. Quinta ocurrencia corregida de esta familia desde la ronda 178.

### `RPM-2015-05-14:6786:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `de los alimentos no perecíbles son bastante pe`
   - después: `de los alimentos no perecibles son bastante pe`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 176 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2011-03-17:3849:1` — Claudio Soto Gamboa

1. **LETRA_CONFUNDIDA**
   - antes: `a de los precios de ios combustibles. P`
   - después: `a de los precios de los combustibles. P`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2014-07-15:6308:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: ` señor Pablo García índica que desde el pu`
   - después: ` señor Pablo García indica que desde el pu`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2006-09-07:858:1` — Rodrigo Valdés Pulido

1. **LETRA_CONFUNDIDA**
   - antes: `s que el INE autorizó ai Banco Central de Chil`
   - después: `s que el INE autorizó al Banco Central de Chil`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2013-09-12:5803:1` — Joaquín Vial Ruiz-Tagle

1. **ACENTO_INDEBIDO**
   - antes: `la balanza se inclina por medidas de política monetaria y cambiaría orientadas a frenar la depreciación`
   - después: `la balanza se inclina por medidas de política monetaria y cambiaria orientadas a frenar la depreciación`
   - por qué: El adjetivo 'cambiaria' no lleva tilde; con tilde es la primera persona del condicional de cambiar, que aquí no tiene sujeto. Es la errata sistemática más frecuente del corpus (204 apariciones en singular) y el contexto no admite la lectura verbal.

### `RPM-2008-03-13:1730:1` — Sebastián Claro Edwards

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.

### `RPM-2013-12-12:5911:1` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `En segundo término, índica que el precio d`
   - después: `En segundo término, indica que el precio d`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2007-12-13:1572:2` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2013-02-14:5334:1` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2005-07-12:299:7` — Pablo García Silva

1. **PALABRA_PARTIDA**
   - antes: `ión para el segundo trim estre que hace dos me`
   - después: `ión para el segundo trimestre que hace dos me`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2968 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2010-04-15:3070:1` — Pablo García Silva

1. **PALABRA_PARTIDA**
   - antes: `ativas un escenario macroeconóm ico de mediano plaz`
   - después: `ativas un escenario macroeconómico de mediano plaz`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 196 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2006-08-10:822:1` — Enrique Marshall Rivera

1. **LETRA_CONFUNDIDA**
   - antes: `mo contenido, similar
ai de los meses anterior`
   - después: `mo contenido, similar
al de los meses anterior`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.
2. **ACENTO_INDEBIDO**
   - antes: ` el ámbito interno, índica el Consejero se`
   - después: ` el ámbito interno, indica el Consejero se`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 5140 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).
