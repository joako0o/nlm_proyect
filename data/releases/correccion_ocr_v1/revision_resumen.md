# Revisión de las correcciones OCR aplicadas

Generado por `scripts/exportar_revision_ocr.py`. No es una fuente: es una
vista derivada de `data/curation/correcciones_ocr_v1.json` re-ejecutada
contra la base virgen. Si el registro cambia, hay que regenerarlo.

- filas corregidas: **1118**
- operaciones: **1618**
- filas marcadas para cotejo: **184**
- sha256 de la base: `d0b64842cd756df4c50d2960d9bbf01c4c45e5df28609d7b612c5d666593da75`

## Operaciones por tipo

| tipo | operaciones |
|---|---:|
| `LETRA_CONFUNDIDA` | 446 |
| `ACENTO_INDEBIDO` | 348 |
| `PALABRA_PARTIDA` | 319 |
| `ACENTO_FALTANTE` | 158 |
| `PUNTUACION` | 106 |
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

### `RPM-2012-04-17:4736:2` — Sergio Lehmann Beresi

1. **RESIDUO_PAGINACION**
   - antes: ` Sesión N° 184 Página 3 de 26 `
   - después: ` `
   - por qué: Residuo de paginacion del PDF incrustado en medio de la oracion. Medido: 26 apariciones, 24 con la cabecera "Sesion N° N" delante y 2 como pie de pagina del Comunicado ("Pagina 31 de 31"). "Sesion N° N" aparece 25 veces en el corpus y solo 24 van seguidas de Pagina, de modo que el patron exige ambos y no toca ninguna mencion legitima. Se elimina el residuo y se deja un solo espacio donde la oracion continua.

### `RPM-2005-04-07:202:2` — Pablo García Silva

1. **LETRA_CONFUNDIDA**
   - antes: `os de aceleración de! primer semestre`
   - después: `os de aceleración del primer semestre`
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.
2. **LETRA_CONFUNDIDA**
   - antes: `io internacional de ios combustibles. M`
   - después: `io internacional de los combustibles. M`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.
3. **LETRA_CONFUNDIDA**
   - antes: `e iniciaría antes de! cuarto trimestr`
   - después: `e iniciaría antes del cuarto trimestr`
   - por qué: Signo de exclamación en lugar de la ele final. Medido: 42 apariciones, y todas dan palabra válida al reponer la l: de! 31 (del), coyuntura! 2, a! 2 (al), e! 2 (el), diferencia!, rea!, genera!, anua!, metano!. Se revisaron las nueve formas una por una y los cuatro casos límite (a!, e!) en su contexto: "sorprendieron en algo a! alza", "precisa que e! planteamiento", "acceso a! financiamiento", "acuerdo sobre e! Mecanismo". Ninguna es una exclamación real.

### `RPM-2014-01-16:5999:3` — Felipe Larraín Bascuñán

1. **ACENTO_INDEBIDO**
   - antes: `a del componente de maquinarías y equipos, como`
   - después: `a del componente de maquinarias y equipos, como`
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 141 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2007-04-12:1218:1` — Jorge Desormeaux Jiménez

1. **LETRA_CONFUNDIDA**
   - antes: `entos de precios de ios alimentos y de `
   - después: `entos de precios de los alimentos y de `
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2008-05-08:1817:1` — Claudio Soto Gamboa

1. **LETRA_CONFUNDIDA**
   - antes: `IRC`
   - después: `IPC`
   - por qué: IRC por IPC. Medido en todo el corpus: 71 apariciones, ninguna en un contexto donde IRC sea una sigla legitima; 61 sueltas y 10 dentro de IRCX1, que tambien debe leerse IPCX1 porque la misma fila escribe IPCX e IPCX2. Regla de bloque revisada caso por caso.

### `RPM-2015-04-16:6725:1` — Miguel Fuentes Díaz

1. **ACENTO_FALTANTE**
   - antes: `de ejecución presupuestaria efectiva propor`
   - después: `de ejecución presupuestaría efectiva propor`
   - por qué: Tilde faltante. Sin ella la forma observada no es palabra española en ninguna acepción, así que no hay ambigüedad que resolver con el contexto: podria/podrian/serian/estaria/deberia/cabria/aumentaria no existen (son los condicionales podría, podrían, serían, estaría, debería, cabría, aumentaría), y lo mismo vale para economia, indices, mayoria, paises, ciclicas, geopoliticos, exposicion, todavia, habia y tenian. Grupo A del arbitraje de §16: se separó deliberadamente del grupo B, donde la forma sin tilde sí existe como verbo, adjetivo o participio (seria, continua, publica, linea, ultimo, titulo, diagnostico, grafica, perdida, desafio, explicito) y entonces decide la oración, no la palabra.

### `RPM-2013-03-14:5435:1` — Kevin Cowan Logan

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2010-12-16:3591:1` — Sergio Lehmann Beresi

1. **LETRA_CONFUNDIDA**
   - antes: `al. En relación con ios bonos periféric`
   - después: `al. En relación con los bonos periféric`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2014-09-11:6438:3` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: ` "`
   - después: ` “`
   - por qué: Comilla recta que abre la cita del Comunicado. Medido en todo el corpus: la formula "Comunicado" va seguida de “ 99 veces y de una recta solo 6. La apertura es inequivoca y la corroboracion es del propio corpus, no de la intuicion.
2. **PUNTUACION**
   - antes: `l horizonte de política."`
   - después: `l horizonte de política.”`
   - por qué: La fila abre con Comunicado “En su reunion mensual de politica (posicion 441, unica comilla de apertura) y TERMINA con una comilla recta en la posicion 2302, la ultima de la fila. Es el cierre de esa misma cita y no hay otro candidato. Es el patron ya resuelto en 5330:3 y 6547:3 (nivel 6): una cita del Comunicado abierta con tipografica y cerrada con recta.

### `RPM-2009-07-09:2641:1` — Pablo García Silva

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2007-10-11:1518:1` — José De Gregorio Rebeco

1. **LETRA_CONFUNDIDA**
   - antes: ` que se vienen para ios meses siguiente`
   - después: ` que se vienen para los meses siguiente`
   - por qué: "ios" por "los": la l se leyo como i, la misma regla que produce "ai" por "al" (§12). Medido: 90 apariciones en 88 filas contra 32.215 de "los". "ios" no es palabra del español. Se comprobo la palabra que precede a las 90 y en todas corresponde un articulo: de 25, en 14, que 12, a 9, para 5, todos 3, con 2, y 2, por 2, y el resto tras cuando, durante, analizan, septiembre, o una comilla de apertura.

### `RPM-2009-10-13:2757:1` — Jorge Desormeaux Jiménez

1. **ACENTO_FALTANTE**
   - antes: ` fiscal reducirá su estimulo en los próximos`
   - después: ` fiscal reducirá su estímulo en los próximos`
   - por qué: Tilde faltante, grupo B2. «seria»: se leyeron las 39 apariciones y 32 son el condicional («lo que seria interesante» -> sería); las 7 restantes son el adjetivo serio/seria y NO se tocan: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia». Por eso cada par lleva contexto. «estimulo»: las 18 apariciones son el sustantivo («el estimulo monetario», «el estimulo fiscal», «planes de estimulo», «el grado de estimulo») y ninguna es la primera persona del verbo estimular, así que todas llevan tilde.

### `RPM-2015-04-16:6730:2` — Claudio Soto Gamboa

1. **SIMBOLO_SUELTO**
   - antes: ` B A N C O C E N T R A L D E C H I L E`
   - después: ``
   - por qué: Encabezado de pagina del PDF, "BANCO CENTRAL DE CHILE", capturado letra por letra y con espacios. Es un residuo de la fuente, no texto del acta: la forma normal "BANCO CENTRAL DE CHILE" no aparece ninguna vez en el corpus, o sea que cuando este encabezado esta presente siempre viene letra por letra. Medido: 10 apariciones en 10 filas, mas 1 truncado ("...D E C H"). La politica es eliminar los residuos de la fuente (numeros de pagina, marcas de hora, comillas huerfanas, firmas truncadas) y este es de la misma familia.

### `RPM-2007-04-12:1171:2` — Sergio Lehmann Beresi

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.
2. **PALABRA_PARTIDA**
   - antes: ` aumento de riesgos geo políticos y también con s`
   - después: ` aumento de riesgos geopolíticos y también con s`
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 47 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2013-09-12:5803:1` — Joaquín Vial Ruiz-Tagle

1. **ACENTO_INDEBIDO**
   - antes: `la balanza se inclina por medidas de política monetaria y cambiaría orientadas a frenar la depreciación`
   - después: `la balanza se inclina por medidas de política monetaria y cambiaria orientadas a frenar la depreciación`
   - por qué: El adjetivo 'cambiaria' no lleva tilde; con tilde es la primera persona del condicional de cambiar, que aquí no tiene sujeto. Es la errata sistemática más frecuente del corpus (204 apariciones en singular) y el contexto no admite la lectura verbal.

### `RPM-2012-07-12:4909:1` — Manuel Marfán Lewis

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

### `RPM-2007-09-13:1423:1` — José De Gregorio Rebeco

1. **ACENTO_FALTANTE**
   - antes: `este gráfico que ha ocupado parte importante de la Reunión de Politica Monetaria`
   - después: `este gráfico que ha ocupado parte importante de la Reunión de Política Monetaria`
   - por qué: Tilde faltante. Medido: 'Politica Monetaria' sin tilde aparece 8 veces en el corpus y 'Política Monetaria' 3.205. La palabra no admite otra lectura.
2. **PALABRA_PARTIDA**
   - antes: `debiera estar claram ente contenido en la Minuta de esta Sesión`
   - después: `debiera estar claramente contenido en la Minuta de esta Sesión`
   - por qué: Espacio intrapalabra, artefacto del escaneo: la palabra está partida en dos. No es una reconstrucción, se reúne sin alterar una letra. Medido: 'claram ente' aparece 1 vez y 'claramente' 469.

### `RPM-2015-08-13:6979:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` E MARSHALL RIVERA RODRIGO VERGARA MONTES Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2015-04-16:6733:1` — Miguel Fuentes Díaz

1. **SIMBOLO_SUELTO**
   - antes: ` i B A N C O C E N T R A L D E C H I L E`
   - después: ``
   - por qué: Encabezado de pagina del PDF, "BANCO CENTRAL DE CHILE", capturado letra por letra y con espacios. Es un residuo de la fuente, no texto del acta: la forma normal "BANCO CENTRAL DE CHILE" no aparece ninguna vez en el corpus, o sea que cuando este encabezado esta presente siempre viene letra por letra. Medido: 10 apariciones en 10 filas, mas 1 truncado ("...D E C H"). La politica es eliminar los residuos de la fuente (numeros de pagina, marcas de hora, comillas huerfanas, firmas truncadas) y este es de la misma familia.

### `RPM-2014-09-11:6412:1` — Miguel Fuentes Díaz

1. **ACENTO_INDEBIDO**
   - antes: `cambiaría`
   - después: `cambiaria`
   - por qué: cambiaría por cambiaria. La tilde convierte el adjetivo en verbo condicional. Medido en todo el corpus: 241 apariciones con tilde (188 singulares y 53 dentro de "cambiarías", que esta regla tambien corrige porque la forma larga contiene a la corta). SOLO 3 son el condicional legitimo y sus filas quedan excluidas: "cuanto cambiaria la estimacion" (2005-12-13:515:1), "no cambiaria el sesgo" (2012-03-15:4723:1), "no cambiaria el comportamiento" (2014-09-11:6425:1). Las 238 restantes van siempre tras un sustantivo que exige adjetivo (apreciacion 65, depreciacion 55, intervencion 28, ...); los 46 con sustantivo ambiguo fueron muestreados y todos exigen adjetivo. Se verifico ademas que ninguna fila mezcla la forma verbal con la adjetiva.

### `RPM-2010-10-14:3488:1` — Sebastián Claro Edwards

1. **LETRA_CONFUNDIDA**
   - antes: `cambiarlo`
   - después: `cambiario`
   - por qué: cambiarlo por cambiario. Misma familia: el OCR puso una l donde va una i. Medido: 60 apariciones, de las cuales 16 son "cambiarlos" (la forma larga contiene a la corta, y esta regla las corrige tambien). 6 son el infinitivo legitimo y sus filas quedan excluidas: "habria que cambiarlos por papeles" (2006-08-10:812:1), "hay que cambiarlo" (2006-11-16:980:1), "haya que cambiarlo" (2007-03-15:1146:1), "no puede cambiarlo" (2008-08-14:2022:1), "no hay antecedentes para cambiarlo" (2010-08-12:3317:1), "razones para cambiarlo" (2012-05-17:4843:1). Las 54 restantes son adjetivas: "el lado cambiarlo", "en lo cambiarlo", "los mercados financieros y cambiarlos". Los 11 contextos con palabra funcion delante se revisaron uno por uno.
2. **LETRA_CONFUNDIDA**
   - antes: `entral delineada en ellPoM, manifestando q`
   - después: `entral delineada en el IPoM, manifestando q`
   - por qué: Sigla dañada por el glifo I/l. Medido en toda la salida: 26 apariciones de esta familia, y cada forma tiene su equivalente correcto ampliamente atestiguado en el corpus (el IPC 1.430, el IPoM 1.543, IPCX 649, IPCX1 469, el IPP 10). Se excluyeron de la pasada "ellPEC", "dellPEC" y "ellMCE" (fila 1719:4): aparecen junto a siglas que no se pueden corroborar en el corpus y no hay reconstruccion unica.

### `RPM-2014-02-18:6055:3` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `"`
   - después: `”`
   - por qué: Comilla recta que cierra una comilla curva: el par esta desbalanceado en el propio texto, de modo que el defecto queda demostrado sin recurrir al PDF. Medido en todo el corpus: 123 comillas rectas, de las cuales 57 forman par mixto con una curva (51 cierran una apertura “ y 6 abren donde el cierre es ”) y se corrigen; 57 forman pares enteramente rectos y no se tocan porque no hay desequilibrio que pruebe el defecto; 9 quedan huerfanas y se tratan aparte.

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

### `RPM-2013-04-11:5515:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` RODRIGO VERGARA MONTES Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2008-03-13:1687:1` — Consejo del Banco Central de Chile

1. **PUNTUACION**
   - antes: `lasco Brañes. Asisten también; Gerente General, `
   - después: `lasco Brañes. Asisten también: Gerente General, `
   - por qué: Punto y coma por dos puntos. Medido: "Asisten también:" aparece 93 veces y "Asisten también;" 7. La formula introduce una lista, así que corresponde dos puntos.

### `RPM-2013-05-16:5566:3` — Consejo del Banco Central de Chile

1. **ACENTO_INDEBIDO**
   - antes: `urozona continúa en recesíón y mantiene una `
   - después: `urozona continúa en recesión y mantiene una `
   - por qué: Acento espurio: con esa tilde la palabra no existe en español. Forma correcta atestiguada 222 veces en el corpus. Detectado por el escáner transversal de acentos y arbitrado uno por uno: se corrigieron sólo los casos en que la forma observada no es palabra en ninguna acepción. Se excluyeron los pares mínimos legítimos (terminó/término, cambió/cambio, dónde/donde, éstos/estos, período/periodo) y las formas que sí existen como verbo o adjetivo (solícita, varías, contraría, complementarías).

### `RPM-2007-11-13:1536:1` — Manuel Marfán Lewis

1. **PALABRA_ERRONEA**
   - antes: `ha sido más bien sensible a shocks de términos de intercambio que a s/70c/(s financieros`
   - después: `ha sido más bien sensible a shocks de términos de intercambio que a shocks financieros`
   - por qué: La cadena 's/70c/(' es basura de OCR que ocupa el lugar de la palabra 'shock': s por s, / por h, 70 por ho, /( por k. La lectura no es una suposición mía: la misma cadena aparece 3 veces en el corpus y en RPM-2007-11-13:1536:1 convive con la forma bien escrita en la misma frase y en posición paralela ('sensible a shocks de términos de intercambio que a s/70c/(s financieros'), lo que la prueba. Además 'shock' aparece 647 veces en el corpus, 12 en esta sesión y 1 en esta misma fila ('absorber adecuadamente dichos shocks'), así que la forma correcta está corroborada donde exige el criterio. Corrección tardía: esta fila pertenece a la sesión 2007-11-13, cerrada en las rondas 62-68. Se corrige ahora porque la medición del residuo 's/70c/(' en la ronda 168 mostró que es sistemático y que en esta misma fila la forma correcta está escrita literalmente a cuatro palabras de distancia. Queda una tercera ocurrencia en RPM-2008-08-14:2042:1, en una sesión aún no leída, que se corregirá en su ronda.

### `RPM-2012-08-16:5040:1` — Consejo del Banco Central de Chile

1. **FIRMA_TRUNCADA**
   - antes: ` MANUEL MARFAN LEWIS RODRIGO VERGARA MONTES Vicepresidente Presidente.`
   - después: ``
   - por qué: Bloque de firmas escaneadas al pie del acta, incrustado al final de la fila. Medido: 52 filas lo contienen y en las 52 cae despues de la formula de cierre "Se levanta la Sesion a las HH:MM horas", nunca en medio del discurso. No contiene intervencion de nadie: solo nombres, cargos y la constancia de firma. El dano optico lo hace irreparable: el corpus trae la misma firma como "ENRIQUE MARSHALL RIVERA" 4 veces, como "E MARSHALL RIVERA" 15 veces y como "EI)fRIQUE MARSHALL RIVERA"; otros bloques quedan como "rORTO CORBO LIOIV" o "J U A f ^ T E B ^ LAVÁL ZALDÍVAR li". Reponer el nombre estaria prohibido por la seccion 5 (nunca se reescribe un nombre propio) y en la mayoria de los casos seria imposible sin el PDF. Se elimina el bloque y se conserva integra la formula de cierre, que si es informacion: la hora de termino de la sesion. La eliminacion ocurre solo en Texto_Corregido; Texto queda intacto.

### `RPM-2005-07-12:299:5` — Pablo García Silva

1. **PALABRA_PARTIDA**
   - antes: ` con la información sem ana a semana puede `
   - después: ` con la información semana a semana puede `
   - por qué: Palabra partida en dos por un espacio espurio del OCR. Detectado por pasada transversal sobre las 9.723 filas: la palabra junta aparece 353 veces en el corpus y ninguna de las dos mitades por separado es una palabra corriente, así que el espacio no puede ser real. Tipo PALABRA_PARTIDA.

### `RPM-2009-12-15:2824:1` — Claudio Soto Gamboa

1. **ACENTO_FALTANTE**
   - antes: `plana que lo que se tenia en noviembre, p`
   - después: `plana que lo que se tenía en noviembre, p`
   - por qué: Tilde faltante, grupo B1: la forma sin tilde sí existe como verbo, adjetivo o participio, así que se leyó cada ocurrencia con su contexto y se decidió una por una. Donde la forma es mixta en el corpus se usa un par con contexto, para no tocar las apariciones legítimas. Casos leídos y NO corregidos porque son correctos: «un panorama benigno que limite las presiones» y «medidas que limite este accionar» (subjuntivo del verbo limitar, no el sustantivo), y «una eventual década perdida» (participio de perder, no el sustantivo pérdida). Los 29 que sí se corrigen son sustantivos, adjetivos, pretéritos o la fórmula «Por último» / «A título de».
