# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1025**
- operaciones: **1476**
- filas marcadas para cotejo: **184**
- sha256 de la base: `d0b64842cd756df4c50d2960d9bbf01c4c45e5df28609d7b612c5d666593da75`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 446 |
| `ACENTO_INDEBIDO` | 348 |
| `PALABRA_PARTIDA` | 319 |
| `PUNTUACION` | 106 |
| `SIMBOLO_SUELTO` | 78 |
| `FIRMA_TRUNCADA` | 55 |
| `RESIDUO_PAGINACION` | 27 |
| `PALABRA_ERRONEA` | 26 |
| `PALABRA_OMITIDA` | 22 |
| `ACENTO_FALTANTE` | 16 |
| `ESPACIO_FALTANTE` | 14 |
| `SALTOS_DE_LINEA` | 10 |
| `ESPACIO_INDEBIDO` | 4 |
| `PALABRA_DUPLICADA` | 3 |
| `PALABRA_SOBRANTE` | 2 |

## Muestra aleatoria de 30 filas (semilla 20260911)

### `RPM-2013-01-17:5286:1` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2005-04-07:206:3` — Pablo García Silva

1. **SIMBOLO_SUELTO**
   - antes: `últimos meses. V La colocación`
   - después: `últimos meses. La colocación`
   - por qué: Letra mayúscula suelta entre dos oraciones. Es ruido de escaneo: la oración anterior termina en punto y la siguiente empieza con mayúscula y sentido completo, así que la letra no pertenece a ninguna de las dos. Medido: 17 casos en 17 filas, con las letras V, H, L, U, A, M, Y, B. Se revisaron uno por uno; el único que NO es residuo es RPM-2007-01-11:1055:1 ("prolongado. A SU juicio"), donde la A abre la oración legítimamente y el defecto es "SU" en mayúscula, que se trata aparte.

### `RPM-2014-09-11:6439:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` E MARSHALL RIVERA RODRIGO VERGARA MONTES Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2007-05-10:1254:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2008-07-10:1923:8` — Sergio Lehmann Beresi

1. **PALABRA_PARTIDA**
   - antes: `el Dólar ha tendido tamb ién en el margen a `
   - después: `el Dólar ha tendido también en el margen a `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 4820 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.
2. **PALABRA_PARTIDA**
   - antes: `s de activos en las econom ías emergentes resp`
   - después: `s de activos en las economías emergentes resp`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2940 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2014-01-16:5999:3` — Felipe Larraín Bascuñán

1. **ACENTO_INDEBIDO**
   - antes: `a del componente de maquinarías y equipos, como`
   - después: `a del componente de maquinarias y equipos, como`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 141 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2011-10-13:4390:1` — Rodrigo Vergara Montes

1. **SIMBOLO_SUELTO**
   - antes: `producto de acuerdos preliminares en la Zona Euro,. Al respecto`
   - después: `producto de acuerdos preliminares en la Zona Euro. Al respecto`
   - por qué: Coma suelta antes del punto de cierre. Medí el patrón ',.' en todo el corpus: aparece 98 veces y 95 de ellas son la fórmula de cierre de fila colgada ('A continuación,.', 'No habiendo más comentarios,.', 'Continuando con la votación,.'), que es un artefacto estructural del acta y no se toca. Este caso es distinto: la coma y el punto quedan a mitad de fila después de un sintagma común, así que es un símbolo suelto aislado, de la misma clase que el 'staff-,' y el apóstrofo-efe que ya se corrigieron.

### `RPM-2015-08-13:6967:1` — Rodrigo Valdés Pulido

1. **PALABRA_PARTIDA**
   - antes: `si se desancla la economía, será preciso reaccionar y determ inar las causas que llevaron a ello`
   - después: `si se desancla la economía, será preciso reaccionar y determinar las causas que llevaron a ello`
   - por qué: Palabra partida: 'determ inar' por 'determinar'. Sección 1 ter, se reúne sin alterar una letra.
2. **LETRA_CONFUNDIDA**
   - antes: `una función de reacción que lleve a subir la tasa de interés después de una depreciación cambiaría, por la configuración de parámetros`
   - después: `una función de reacción que lleve a subir la tasa de interés después de una depreciación cambiaria, por la configuración de parámetros`
   - por qué: Tilde por i en posición de adjetivo, sección 3 ter.
3. **LETRA_CONFUNDIDA**
   - antes: `dado que la combinación inflación y desempleo o inflación con breca no es aceptada como conveniente`
   - después: `dado que la combinación inflación y desempleo o inflación con brecha no es aceptada como conveniente`
   - por qué: Falta la hache: 'breca' por 'brecha'. La palabra 'breca' existe (un pez) pero aquí no tiene sentido y la oración no admite otra lectura. Corroborada de sobra: 'brecha' aparece 5 veces en esta misma sesión y 851 en el corpus. OJO CON LA MEDICION: 'breca' parece aparecer 28 veces, pero 27 de esas están DENTRO de 'sobrecalentamiento'/'sobrecalentada' (so-breca-lentamiento). La ocurrencia real es 1 sola. Es la misma trampa que 'ratando' dentro de 'tratando' y por eso la regla exige delimitar la palabra antes de contar.
4. **PALABRA_OMITIDA**
   - antes: `considerando además en este contexto el marco de aplicación de políticas contracíclicas y el hecho que el cambio de precios relativos puede llegar ser fuerte en dicho período`
   - después: `considerando además en este contexto el marco de aplicación de políticas contracíclicas y el hecho que el cambio de precios relativos puede llegar a ser fuerte en dicho período`
   - por qué: Falta la preposición: 'puede llegar ser fuerte' no es gramatical y la reparación es única, porque el OCR omite y no agrega palabras. 'llegar a ser' aparece 5 veces en el corpus. Mismo criterio que 'frente la decisión' (ronda 181), 'la proyección el PIB' (ronda 179) y 'la mayoría las monedas' (ronda 178).
5. **PUNTUACION**
   - antes: ` "`
   - después: ` ”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2009-11-12:2796:3` — Enrique Marshall Rivera

1. **ACENTO_INDEBIDO**
   - antes: `e dos temas agregan íncertidumbre al escenario gl`
   - después: `e dos temas agregan incertidumbre al escenario gl`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 861 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2007-11-13:1565:2` — Enrique Marshall Rivera

1. **LETRA_CONFUNDIDA**
   - antes: `en tomo a`
   - después: `en torno a`
   - por qué: en tomo a por "en torno a". Medido: 24 apariciones (20 "en tomo a" y 4 "en tomo al"), la r leida como m. "tomo" es palabra real (volumen) pero ningun contexto lo admite. "en torno a" aparece 1.678 veces.

### `RPM-2010-04-15:3049:2` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `nía en el escenario dellPoM.`
   - después: `nía en el escenario del IPoM.`
   - por qué: Sigla dañada por el glifo I/l. Medido en toda la salida: 26 apariciones de esta familia, y cada forma tiene su equivalente correcto ampliamente atestiguado en el corpus (el IPC 1.430, el IPoM 1.543, IPCX 649, IPCX1 469, el IPP 10). Se excluyeron de la pasada "ellPEC", "dellPEC" y "ellMCE" (fila 1719:4): aparecen junto a siglas que no se pueden corroborar en el corpus y no hay reconstruccion unica.

### `RPM-2007-04-12:1216:1` — Enrique Marshall Rivera

1. **LETRA_CONFUNDIDA**
   - antes: `en tomo a`
   - después: `en torno a`
   - por qué: en tomo a por "en torno a". Medido: 24 apariciones (20 "en tomo a" y 4 "en tomo al"), la r leida como m. "tomo" es palabra real (volumen) pero ningun contexto lo admite. "en torno a" aparece 1.678 veces.

### `RPM-2014-06-12:6295:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` IQUE MARSHALL RIVERA RODRIGO VERGARA MONTES Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2013-04-11:5496:1` — Luis Opazo Roco

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2007-09-13:1449:3` — Rodrigo Valdés Pulido

1. **ACENTO_FALTANTE**
   - antes: `Rodrigo Valdés señala que ello no ocurre asi, ya que llegan más permisos`
   - después: `Rodrigo Valdés señala que ello no ocurre así, ya que llegan más permisos`
   - por qué: Tilde ausente: 'asi' sin tilde no es una palabra del español. Sección 1, no exige corroboración. Medido: 'no ocurre asi' 1 vez frente a 'así' 1.200 en el corpus.

### `RPM-2015-08-13:6954:1` — Joaquín Vial Ruiz-Tagle

1. **PALABRA_PARTIDA**
   - antes: `materias que pudieron haber jugado un rol importante tam bién en el año 2008`
   - después: `materias que pudieron haber jugado un rol importante también en el año 2008`
   - por qué: Palabra partida por un espacio intrapalabra. Sección 1 ter: se reúne sin alterar una letra, así que no hay lectura alternativa que proteger y no se pide corroboración. Medido: 'también' aparece 4.809 veces en el corpus y 'tam bién' 9.

### `RPM-2011-08-18:4280:1` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2015-01-15:6569:1` — Rodrigo Vergara Montes

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2006-09-07:858:1` — Rodrigo Valdés Pulido

1. **LETRA_CONFUNDIDA**
   - antes: `s que el INE autorizó ai Banco Central de Chil`
   - después: `s que el INE autorizó al Banco Central de Chil`
   - por qué: "ai" por "al": la l se leyo como i. Medido en toda la salida: 26 apariciones de la palabra suelta "ai" en 26 filas, y "ai" no es una palabra del español. En cambio "al" aparece miles de veces y "al alza" 1.405 contra 3 de "ai alza". Se revisaron una por una las 26 apariciones y en todas el contexto exige "al" ("asociadas ai sector exportador", "converge ai mismo nivel", "autorizó ai Banco Central", "mayor ai previsto", "Agrega que, ai respecto", "superior ai 9,5%"). No hay ninguna fila en que "ai" sea otra cosa.

### `RPM-2014-02-18:6037:1` — Rodrigo Vergara Montes

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2008-03-13:1734:1` — Jorge Desormeaux Jiménez

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2014-03-13:6087:1` — Miguel Fuentes Díaz

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.

### `RPM-2007-12-13:1587:2` — Igal Magendzo Weinberger

1. **LETRA_CONFUNDIDA**
   - antes: `IRC`
   - después: `IPC`
   - por qué: IRC por IPC. Medido en todo el corpus: 71 apariciones, ninguna en un contexto donde IRC sea una sigla legitima; 61 sueltas y 10 dentro de IRCX1, que tambien debe leerse IPCX1 porque la misma fila escribe IPCX e IPCX2. Regla de bloque revisada caso por caso.

### `RPM-2013-04-11:5515:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` RODRIGO VERGARA MONTES Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2005-07-12:299:7` — Pablo García Silva

1. **PALABRA_PARTIDA**
   - antes: `ión para el segundo trim estre que hace dos me`
   - después: `ión para el segundo trimestre que hace dos me`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 2968 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2010-07-15:3227:2` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `do en períodos post recesíón.`
   - después: `do en períodos post recesión.`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 222 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

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

### `RPM-2009-07-09:2644:2` — Luis Felipe Céspedes Cifuentes

1. **LETRA_CONFUNDIDA**
   - antes: `nesgo`
   - después: `riesgo`
   - por qué: nesgo por riesgo. Medido: 29 apariciones en 29 filas, todas con la i leida como n. "nesgo" no es palabra del espanol, no existe lectura alternativa. "riesgo" aparece cientos de veces en el corpus.

### `RPM-2008-08-14:1978:1` — Consejo del Banco Central de Chile

1. **PALABRA_PARTIDA**
   - antes: `celebrada e l 4 de agosto de 2008`
   - después: `celebrada el 4 de agosto de 2008`
   - por qué: Espacio intrapalabra, artefacto del escaneo: 'el' está partido en dos. Se reúne sin alterar una letra. Medido: 'celebrada e l' aparece 2 veces en el corpus frente a 'celebrada el' 126.

### `RPM-2008-08-14:2033:1` — Andrés Velasco Brañes

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
