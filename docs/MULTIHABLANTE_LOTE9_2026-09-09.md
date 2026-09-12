# Lote 9 — filas con varios hablantes dentro de un mismo párrafo

## Por qué existe este lote

Todo el trabajo anterior parte del inventario de **límites entre filas**
(`auditar_continuidad_turnos`). Ese eje no cubre el caso de **una sola fila que contiene más
de un hablante**, que es el otro eje del encargo.

La única señal que el motor produce sobre ese eje es `POSIBLE_OTRO_HABLANTE_O_MENCION`, y
aparece en **22 filas** de 9.723. No se puede usar como si fuera el universo.

## Tres barridos independientes

| Barrido | Instrumento | Universo | Leídas | Dos voces |
|---|---|---:|---:|---:|
| A. Nombres del roster | personas de la asistencia presentes en la fila | 71 con ≥2 | **71** | 1 |
| B. Cola tras entrega | texto sustantivo después de «ofrece/concede la palabra» | 8 de 980 | **8** | 3 |
| C. Sujeto por cargo | sujeto con cargo ajeno + verbo de habla | 141 | — | **no válido** |

**Total: 78 filas leídas completas.** Los tres casos con dos voces salen del barrido B.

Un dato que justifica haber hecho el segundo barrido: de las 8 filas del barrido B, cinco no
aparecen en absoluto en el inventario por nombres (no mencionan a nadie de la asistencia), y
las otras dos —`2960:2` y `1564:1`, dos de los tres casos reales— sí aparecen pero con **una
sola** otra persona, así que quedaban fuera de las 71 priorizadas. El barrido por nombres,
solo, no las habría encontrado: en ambas la segunda voz entra por cargo («El Gerente de
División Política Financiera manifiesta…», «Menciona la señora Ministra…»), no por nombre.

El barrido C **no se usa como cobertura**. Encuentra 141 filas pero recupera sólo 1 de los 3
casos ya confirmados: no detecta `657:1` ni `1564:1`. Un instrumento que falla contra
positivos conocidos no prueba nada sobre el resto, así que se descarta en vez de presentarse
como revisado.

## Los tres casos con dos voces

Los tres tienen la misma estructura: **el inicio de la intervención del siguiente hablante
quedó pegado al final de la fila anterior**, y la fila siguiente ya está atribuida a ese
segundo hablante y continúa lo que empezó.

**`RPM-2006-05-11:657:1`** (Corbo, 684 caracteres). Anuncia quiénes expondrán, ofrece la
palabra a Lehmann «para que inicie la exposición», y la fila sigue:

> «Respecto al crecimiento mundial, la situación de China, que ha mostrado una dinámica mayor
> a la que se anticipaba, ha llevado a revisar el crecimiento mundial, en una décima…»

`657:2` ya es Sergio Lehmann y abre con «Hace presente el señor Lehmann, que respecto al
precio del cobre…». La primera oración de su exposición está en la fila de Corbo.

**`RPM-2007-11-13:1564:1`** (Corbo, 849 caracteres). Agradece a Jadresic, ofrece la palabra a
la Ministra Subrogante María Olivia Recart, y la fila sigue con 686 caracteres de exposición
de ella («Menciona la señora Ministra que va a destacar tres elementos centrales…»).
`1564:2` ya es Recart y abre con «En segundo lugar indica la señora Recart…».

**`RPM-2010-02-11:2960:2`** (De Gregorio, 1.275 caracteres). Agradece a Beltrán de Ramón,
concede la palabra a Kevin Cowan, y la fila sigue con 1.102 caracteres de exposición de Cowan
(«El Gerente de División Política Financiera manifiesta creer que…»). `2960:3` ya es Kevin
Cowan y abre con «Por otra parte, el señor Cowan señala estimar que…».

En los tres, el tramo final está atribuido al hablante equivocado. **No se aplicó ningún
corte**: es un cambio de atribución entre hablantes, no un refinamiento funcional, y
requiere su propio registro curado, validador y corrida.

### Un cuarto caso, con otra firma (ronda 171)

**`RPM-2008-08-14:1995:1`** (atribuida a Jorge Desormeaux, 2.791 caracteres). Los primeros
~500 caracteres sí son suyos («El Vicepresidente señor Jorge Desormeaux menciona que el
mensaje de algunos reportes de bancos de inversiones…»). El resto, unos 2.300 caracteres, es
exposición de Sergio Lehmann, y el propio texto lo dice cinco veces:

> «Señala el señor Gerente que en Japón y Europa las tasas han tendido a caer…»
> «Menciona el señor Gerente que respecto a mercados emergentes las bolsas han tendido a caer…»
> «Muestra en la gráfica los flujos netos acumulados en doce meses promedio por región…»
> «Respecto a precios de commodities, indica el señor Gerente que éstos han tendido a retroceder.»

Dos diferencias con los tres anteriores, y las dos importan:

1. **No continúa en una fila atribuida a Lehmann.** La prueba que validó a los otros tres
   («el bloque continúa en una fila atribuida a él») aquí no se cumple: la siguiente fila de
   Lehmann, `2001:1`, trata de trigo y maíz. La evidencia es interna: la fila nombra al otro
   hablante y describe acciones de quien presenta, no de quien comenta. No es discurso
   referido.
2. **El detector no la levantó.** La fila no traía ningún motivo de revisión. Los tres casos
   anteriores sí aparecían en algún barrido; este apareció leyendo.

Punto de corte propuesto: antes de «Señala el señor Gerente que en Japón y Europa las tasas
han tendido a caer». **Corte no aplicado**, igual que en los otros tres.


## Las otras 75

**70 de las 71 del barrido A son una sola voz.** Son aperturas de sesión: ausencias del
Ministro de Hacienda, bienvenidas a consejeros nuevos, fijación de la fecha siguiente,
anuncio de quién expondrá y entrega de la palabra. Los nombres presentes son menciones,
llegadas y traspasos; ninguno interviene en la fila. Es la regla ya vigente.

Una de ellas, `RPM-2012-02-14:4574:1`, lleva `POSIBLE_OTRO_HABLANTE_O_MENCION` y leída
completa es un **falso positivo**: bienvenida a Vial, renovación de Marfán, fecha de agosto,
constancia del mensaje de Larraín y paso a Ricaurte.

De las 8 del barrido B, 5 son falsos positivos medidos: en `3340:1` y `5584:1` «da paso a» no
es entrega de la palabra sino «da paso a una evolución/reacción»; en `747:1` y `1706:1` la
cola es del propio Presidente; en `1556:1` la cola es parte de la misma oración que enumera
lo que expondrá Magendzo.

## Las 339 filas con exactamente una otra persona

**Se leyeron las 339 en texto completo**, no se las cubrió por barrido. Son 134.189
caracteres; se leyeron en siete tramos de entre 8.000 y 16.000 caracteres por llamada.

| | |
|---|---:|
| Universo | 339 |
| Leídas en texto completo | **339** |
| Con dos voces | **2** |
| Con una sola voz | 337 |
| Con alerta del motor | 3 |
| Falsos positivos de esa alerta | **3** |

Las 2 con dos voces son `2960:2` y `1564:1`, ya confirmadas antes por el barrido de cola tras
entrega. **La lectura completa no encontró ninguna nueva.** Eso es lo importante: el barrido
validado y la lectura total coinciden, y el instrumento no estaba dejando pasar casos.

Con esto, **las 410 filas personales del inventario están leídas** (71 con ≥2 personas + 339
con 1). El resumen publicado reporta `Leidas_En_Este_Lote: 410`.

Las 3 alertas del motor dentro de las 339 son **falsos positivos**:

- `1338:3` — Jadresic pide la palabra y expone; Magendzo aparece citado («comentó que los datos apuntan a 3%»).
- `2397:1` — Claro comenta la exposición de Lehmann; no habla Lehmann.
- `4656:1` — Vergara abre la sesión, constata la ausencia de Larraín y ofrece la palabra.

### Dos casos límite que la lectura completa sí encontró

Ninguno es un corte, pero no estaban en ningún barrido y conviene dejarlos escritos:

- **`5109:1`** — narra un intercambio: «Kevin Cowan consulta si los bonos… **precisándose por parte del Gerente de Análisis Internacional señor Sergio Lehmann** que la Reserva Federal anunció la compra de US$ 40 billones de MBS». Es narración en tercera persona del acta, no palabras de Lehmann transcriptas. No hay segunda voz que recortar. Es lo más parecido a una segunda voz dentro de las 339.
- **`2332:1`** — el acta atribuye la intervención a dos personas a la vez: «el Presidente señor José De Gregorio **y el Vicepresidente señor Jorge Desormeaux** se refieren a la relevancia…». Es atribución conjunta del propio documento, no una segunda voz pegada al final. Se trata como caso documental.

## Dos detectores construidos y descartados

Intenté dos veces un detector por sujeto con cargo ajeno. El primero (C) marcaba 141 filas y
recuperaba 1 de 3 positivos. El segundo (D) corregía un defecto real de género —`ministra` no
contiene `ministro`, y por eso `1564:1` se escapaba— y aun así sigue sin recuperar `657:1` ni
`1564:1`. Ambos quedan **descartados**: un instrumento que no pasa por positivos conocidos no
prueba nada sobre el resto, aunque marque pocas filas.

## Cobertura final

**Cubierto por lectura completa:**

- Las 71 filas con ≥2 personas de la asistencia.
- Las 339 filas con exactamente 1 otra persona.
- Las 8 marcadas por el barrido de cola tras entrega (de 980 con fórmula de entrega).
- **415 filas con lectura completa registrada; las 410 personales del inventario, todas.**

**No cubierto:** el resto del corpus (las 233 filas institucionales de asistencia del Consejo y
las filas sin otra persona de la asistencia nombrada). Ahí podría haber una segunda voz que
entre sin nombre de la asistencia ni fórmula de entrega —el patrón de `657:1`, que no tiene
ninguna fórmula y se detectó sólo porque venía precedido de una entrega—. No tengo instrumento
validado para ese caso.

Lo que sí puedo afirmar sobre las 410 filas personales: **están leídas todas, una por una, y
sólo 3 tienen dos voces.**

## Siguiente paso

Registro curado, validador y corrida para los tres cortes de atribución
(`657:1`, `1564:1`, `2960:2`).

## Evidencia

`docs/continuidad_lote9_2026-09-09/lecturas.json` — 415 casos con lectura completa, hallazgo y
justificación, más el resultado de validación de cada barrido.
`docs/multihablante_v7_2026-09-09/inventario_multihablante_v7.csv` — las 643 filas con al
menos otra persona de la asistencia, con `Leidas_En_Este_Lote: 410`.

## Plan de rondas: reunión por reunión

**Revisión reunión por reunión.** Medido, no sale más caro:

| orden | rondas |
|---|---:|
| cronológico | 813 |
| por volumen de la sesión | 816 |
| **por riesgo, sesión por sesión** | **810** |
| por bandas de largo (plan anterior) | 826 |

O sea que la legibilidad no cuesta rondas. El plan anterior partía cada reunión en tres
pedazos repartidos a lo largo de 800 rondas, y eso impedía juzgar el flujo de hablantes —
que es justo lo que hace falta para ver si una voz quedó pegada.

Las **sesiones se ordenan por riesgo**: su fila más larga primero. Una segunda voz pegada
necesita espacio y los tres positivos conocidos miden 684, 849 y 1.275 caracteres. Dentro de
cada sesión las filas van en orden de acta.

**Plan v4: 856 rondas, ninguna cruza de reunión.** El empaquetado v3 llenaba las rondas
sin respetar el límite de sesión y **108 de 812 rondas mezclaban dos reuniones** — justo lo
que el orden por reunión venía a evitar. Cerrar la ronda al cambiar de sesión cuesta 44
rondas más (812 → 856) y vale la pena.

**132 sesiones en el corpus, 9.205 filas pendientes, 856 rondas.** Cada reunión
toma entre 2 y 10 rondas, mediana **6**. Verificado: 9.251 filas en el plan, 0 fuera.

| sesión | rondas | filas | chars |
|---|---|---:|---:|
| 2005-06-09 | 1–5 | 39 | 67.502 |
| 2013-11-19 | 6–13 | 54 | 107.001 |
| 2014-05-15 | 14–20 | 64 | 103.051 |
| 2007-12-13 | 21–29 | 72 | 123.992 |
| 2005-08-11 | 30–34 | 56 | 63.680 |
| 2007-10-11 | 35–43 | 67 | 117.394 |

`plan_rondas.csv` lista ronda por ronda la sesión, las bandas, los tramos, los caracteres y
los IDs.

```
.venv/bin/python scripts/rondas_lectura_lote9.py estado      # progreso y próximas sesiones
.venv/bin/python scripts/rondas_lectura_lote9.py leer 1      # una ronda del plan
.venv/bin/python scripts/rondas_lectura_lote9.py sesion AAAA-MM-DD   # una sesión entera
.venv/bin/python scripts/rondas_lectura_lote9.py registrar N UNA_SOLA_VOZ "justificacion"
.venv/bin/python scripts/rondas_lectura_lote9.py registrar_sesion AAAA-MM-DD UNA_SOLA_VOZ "justificacion"
```

Cada ronda cierra imprimiendo el índice de su última fila: el techo real de una llamada está
entre 19.267 y 20.501 caracteres emitidos y el recorte **vacía el medio conservando la cola**,
así que la salida se ve completa sin estarlo.

### Criterio de dos voces, corregido en la sesión 2007-11-13

El criterio que se venía aplicando —«dos voces requiere que las palabras del segundo
hablante estén literalmente en el texto»— **es incorrecto y se retira**. Medido sobre el
xlsx, los tres casos confirmados están todos en tercera persona narrada, ninguno con
palabras textuales:

| fila | total ch | entrega del turno | contenido del 2º hablante |
|---|---:|---:|---:|
| `RPM-2006-05-11:657:1` | 684 | 457 | **227** |
| `RPM-2007-11-13:1564:1` | 849 | 162 | **687** |
| `RPM-2010-02-11:2960:2` | 1.275 | 172 | **1.103** |

El criterio correcto es: **la fila contiene un bloque sustantivo de exposición del
segundo hablante que continúa en una fila atribuida a él**. En `1564:1` el bloque abre
con «Menciona la señora Ministra que va a destacar tres elementos centrales… En primer
lugar…» y la fila siguiente, atribuida a Recart, empieza con «**En segundo lugar**
indica la señora Recart». Esa continuidad es la prueba estructural.

Quedan fuera, por tanto, las filas donde el aporte ajeno solo se *refiere* o se responde
en una cláusula, sin desarrollarse:

- `RPM-2006-09-07:851:1` — «Ante un comentario del Gerente señor Magendzo…»: el
  comentario se menciona, su contenido no se reproduce.
- `RPM-2008-04-10:1764:1` — «El señor Gerente responde que efectivamente se refiere a
  dicho subsidio»: una cláusula, no exposición.

### Progreso

| ronda | sesión | filas | resultado |
|---|---|---:|---|
| 1 | 2005-01-11 | 4 | una sola voz |
| 2 | 2005-01-11 | 4 | una sola voz |
| 3 | 2005-01-11 | 5 | una sola voz |
| — | 2005-01-11 | 44 | una sola voz · **sesión cerrada 58/58** |
| 1–5 v3 | 2005-07-12 | 50 | una sola voz |
| — | 2005-07-12 | 5 | una sola voz · **sesión cerrada 52/52** |
| 1–5 v4 | 2005-06-09 | 38 | una sola voz · **sesión cerrada 38/38** |
| 6–13 | 2013-11-19 | 56 | una sola voz · **sesión cerrada 56/56** |
| 14–20 | 2014-05-15 | 65 | una sola voz · **sesión cerrada 65/65** |
| 21–29 | 2007-12-13 | 80 | una sola voz · **sesión cerrada 80/80** |
| 30–34 | 2005-08-11 | 56 | una sola voz · **sesión cerrada 56/56** |
| 35–43 | 2007-10-11 | 71 | una sola voz · **sesión cerrada 71/71** |
| 44–51 | 2014-01-16 | 53 | una sola voz · **sesión cerrada 53/53** |
| 52–57 | 2007-02-08 | 64 | una sola voz · **sesión cerrada 64/64** |
| 58–64 | 2008-11-13 | 60 | una sola voz · **sesión cerrada 60/60** |
| 65–69 | 2006-09-07 | 53 | una sola voz · **sesión cerrada 53/53** |
| 70–74 | 2006-11-16 | 45 | una sola voz · **sesión cerrada 45/45** |
| 75–79 | 2008-04-10 | 43 | una sola voz · **sesión cerrada 43/43** |
| 80–86 | 2014-09-11 | 61 | una sola voz · **sesión cerrada 61/61** |
| 87–91 | 2014-12-11 | 38 | una sola voz · **sesión cerrada 38/38** |
| 92–98 | 2008-02-07 | 68 | una sola voz · **sesión cerrada 68/68** |
| 99–106 | 2007-11-13 | 76 | una sola voz en las 70 filas del plan · **sesión cerrada 76/76** |
| 107–113 | 2012-11-13 | 76 | una sola voz · **sesión cerrada 76/76** |
| 114–120 | 2014-06-12 | 72 | una sola voz en las 72 filas del plan · **sesión cerrada 78/78** |
| 121–128 | 2012-09-13 | 59 | una sola voz en las 59 filas del plan · **sesión cerrada 65/65** |
| 129–134 | 2006-10-12 | 66 | una sola voz en las 66 filas del plan · **sesión cerrada 68/68** |
| 135–140 | 2006-01-12 | 47 | una sola voz en las 47 filas del plan · **sesión cerrada 50/50** |
| 141–147 | 2011-10-13 | 82 | una sola voz en las 82 filas del plan · **sesión cerrada 86/86** · 14 filas con 19 correcciones OCR, 11 marcas |
| 148–154 | 2013-09-12 | 69 | una sola voz en las 69 filas del plan · **sesión cerrada 72/72** · 12 filas con 18 correcciones OCR, 9 marcas |
| 155–161 | 2012-05-17 | 67 | una sola voz en las 67 filas del plan · **sesión cerrada 71/71** · 10 filas con 15 correcciones OCR, 1 marca |
| 162–169 | 2007-09-13 | 85 | una sola voz en las 85 filas del plan · **sesión cerrada 88/88** · 26 filas con 48 correcciones OCR (49 sustituciones), 11 marcas de cotejo y 6 revisiones descartadas |
| 170–177 | 2008-08-14 | 96 | una sola voz en las 96 filas del plan · **sesión cerrada 98/98** (2 filas ya estaban leídas) · **una fila nueva con dos voces: `1995:1`** · 20 filas con 35 correcciones OCR (40 sustituciones), 13 marcas de cotejo y 5 revisiones descartadas |
| 178–183 | 2015-08-13 | 66 | una sola voz en las 66 filas del plan · **sesión cerrada 69/69** (3 filas ya estaban leídas: `6919:1`, `6921:1`, `6966:1`) · 25 filas con 55 correcciones OCR, 9 marcas de cotejo · **una fila entera duplicada: `6926:2`** |
| 184–189 | 2007-05-10 | 49 | una sola voz en las 49 filas del plan · **sesión cerrada 52/52** (3 filas ya estaban leídas) · 9 filas con 11 correcciones OCR y 3 marcas de cotejo dentro de la sesión · su lectura destapó dos pasadas transversales: 23 ocurrencias de glifos confundidos (i/I/l/1/0/O) en 20 filas, y 53 comillas rectas en 24 filas donde el par es completo y la dirección deducible |
| 190 | 2007-07-12 | 7 | una sola voz · 67 correcciones OCR en 59 filas del corpus: `ai`→`al` 26, `Consesus`→`Consensus` 8, `fiy`/`fIy`→`fly` 9, `Asisten también;`→`:` 7, 15 letras sueltas, `A SU`→`A su` · se retira la marca de `1312:1` porque la `I` era una `l` · criterio §12 |
| 191 | 2007-07-12 | 11 | una sola voz · 141 correcciones OCR en 106 filas del corpus: `X!`→`Xl` 47→0, `ios`→`los` 94→0, `S`→`$` 2, `llegarla`→`llegaría`, `subpri me` 4→0 · se mide y se descarta una regla general para `-rla` y para palabra+dígito+palabra · criterio §13 |
| 192 | 2007-07-12 | 26 | una sola voz · 49 correcciones OCR en 31 filas: familia de siglas con `I` leída como `l` llevada a 0 (13 formas) y los 21 residuos `■` llevados a 0 · se preservan las 180 apariciones legítimas de `IPCX` (segunda medida de inflación subyacente) · se excluyen `ellPEC`/`dellPEC`/`ellMCE` por falta de reconstrucción única · criterio §14 |
| 193–196 | 2007-07-12 | 16 | una sola voz en las 16 filas del plan · **sesión cerrada 61/61** · cada fila cierra con la conclusión de su propio hablante (su voto o su síntesis); las menciones cruzadas son referencias, no intervenciones —`1349:1` dice «como señalaba el Consejero señor Enrique Marshall», y los 10 `Marshall` de `1347:2` son el propio hablante en tercera persona, que es el estilo del acta · 1 corrección OCR: residuo de escaneo `Lf \` al final de `1347:1` · la lectura destapó el punto ciego del detector de palabras partidas (criterio §23) |
| 197–201 | 2005-04-07 | 59 | una sola voz en las 59 filas del plan · **sesión cerrada 59/59** · sesión de debate con turnos cortos alternados (`207:1` a `207:12`), el caso de muchos hablantes: los cortes ya estaban hechos y la lectura los confirma · se leyeron las cuatro sospechosas y ninguna tiene segunda voz: «acota el riesgo» es el verbo limitar, la «consulta de la señora Consejera» de `204:3` es una referencia y el resto es la respuesta de García, y el «interviene» de `211:1` presenta el turno del propio García · 2 correcciones OCR de residuos finales (`'1^` y una barra invertida suelta) y 1 marca porque `210:2` termina en «Y» sola, o sea texto perdido, que borrar taparía · `213:2` termina con el titular «Perspectivas de inflación en el corto plazo»: es texto real del acta, problema de segmentación y no de OCR, no se toca (criterio §25) |

Ronda 1 (padres 30, 34, 36, 38): Corbo responde al Ministro, Valdés explica la revisión
del producto potencial y luego presenta las opciones numeradas 1 a 7, Marfán sugiere una
Minuta. El Ministro de Hacienda aparece citado en los tres primeros tramos —«lo expuesto
por el señor Ministro», «el Ministro en el fondo decía», «dudas parecidas a las del señor
Ministro»—, pero es discurso referido, no palabras suyas transcriptas. Ninguna segunda voz.

Ronda 2 (padres 3, 42, 4, 50): Pablo García expone el Informe de Política Monetaria en
`3:1` (8.224 ch) y **continúa en `4:1`** (4.184 ch) — es la misma exposición partida en dos
filas, no dos voces. Eyzaguirre habla en nombre propio en `42:1` y cita a Schmidt-Hebbel
(«al escuchar la intervención del señor Klaus Schmidt-Hebbel») y un artículo de Juan Andrés
Fontaine; ambos son discurso referido. Marfán fundamenta su voto en `50:1`.

Ronda 3 (padres 51, 52, 54, 57, 5) cierra la sesión. Ovalle, Desormeaux y Corbo
fundamentan cada uno su voto por 25 pb. `57:1` es una fila **institucional** —actor
«Consejo del Banco Central de Chile»—: registra el retiro del Ministro y de la Asesora,
el texto del Comunicado, su aprobación, el cierre y el bloque de firmas con sus residuos
de OCR, que se conservan tal cual. `5:1` es continuación de la exposición de Pablo García.

**La sesión 2005-01-11 quedó completa (58 filas).** Las 44 que faltaban estaban repartidas
en las bandas B, C y D del plan, así que se leyeron aparte por sesión. Es una discusión de
IPoM con intercambio rápido: el Ministro consulta y responden García, Valdés, Lehmann,
Vicuña, Herrera, Jadresic y Schmidt-Hebbel, **cada uno en su propia fila**; los Consejeros
comentan y luego votan uno por uno. Las filas `1:1`, `28:2`, `55:1` y `56:1` son
institucionales (actor «Consejo del Banco Central de Chile»): lista de asistencia,
reanudación, acuerdo y texto del acuerdo. Ninguna fila trae una segunda voz pegada.

**Caso particular en `5892:3` (sesión 2013-11-19).** El actor es Felipe Larraín Bascuñán
pero quien habla físicamente es el Presidente Vergara, que lee el planteamiento escrito del
Ministro — lo anuncia la fila anterior: «procederá a su lectura, de manera que quede inserto
en el Acta». El motor ya la trae marcada `TEXTO_ESCRITO_LEIDO_POR_TERCERO` y la atribución al
autor es la correcta. Es una fila con dos personas involucradas, pero **no es una segunda voz
pegada**: es un texto escrito, deliberadamente atribuido a su autor y ya alertado. No se
recorta. Conviene tenerla presente porque es el pariente estructural más cercano de los tres
casos de dos voces, y está bien resuelto.

**`TEXTO_ESCRITO_LEIDO_POR_TERCERO`: 12 filas en el corpus.** En una sola fila el autor
y el lector son personas distintas. Verificadas hasta ahora `5892:3` (Larraín, leído por
Vergara, sesión 2013-11-19) y `5999:3` (Larraín de nuevo, leído por Vergara, sesión
2014-01-16, texto entre comillas y anuncio previo en `5999:2`). Las dos están bien: el
motor las alerta y las atribuye al autor. **No son segundas voces pegadas y no se
recortan.** Son el pariente estructural más cercano de los tres casos de dos voces, y
conviene tenerlas presentes por si aparece una sin la alerta.

**El lector de rondas trunca por la cabeza, no por la cola.** `leer N` emite hasta
18.000 caracteres y la consola los corta por el principio, así que la primera fila de
una ronda larga puede registrarse sin haberse leído su comienzo. Por eso existe
`.cache/leer_seguro.py N [i | a:b]`: sin índice lista las filas de la ronda con su
largo, y con índice imprime una fila o un rango completos. Toda fila cuya cabeza no se
vio debe releerse por ese camino. Verificado en `1604:2`, `1611:1`, `314:1` y `361:1`.

Para leer una sesión entera al margen del plan:

```
.venv/bin/python scripts/rondas_lectura_lote9.py sesion AAAA-MM-DD [desde]
```

| 202–209 | 2007-08-09 | 58 | una sola voz en las 58 filas del plan · **sesión cerrada 58/58** · debate con turnos cortos alternados entre Consejeros y Gerentes · las cuatro banderas de segunda voz eran referencias: `1360:1` Lehmann responde a una consulta de Desormeaux, `1363:1` García complementa un punto planteado por Marfán, `1378:1` Corbo alude a lo solicitado por Marfán, `1398:1` Desormeaux cita lo informado por Schmidt-Hebbel · esta sesión destapó una familia de OCR que el detector no veía: la palabra **deletreada con espacios** (`n o tic ia s` → `noticias`, `T a m b ié n` → `También`), 32 correcciones en 7 filas y 106 casos sin cubrir en todo el corpus (criterio §26) |

| 210–215 | 2008-10-09 | 43 | una sola voz en las 43 filas del plan · **sesión cerrada 43/43** · sesión de la crisis financiera (Jaque, García, Cowan, debate y votación, mantención en 8,25 %) · las banderas eran un traspaso (`2105:1` De Gregorio anuncia que Jaque reemplaza a Lehmann; `2105:2` ya es la fila de Jaque), una aclaración en nombre propio (`2110:1`) y coincidencias de **substring**: `corresponden`/`corresponde` contienen «responde» y `acotada` contiene «acota» · 16 correcciones y 3 marcas, más dos familias transversales: `Sanco`→`Banco` (7 filas, leídas una por una) y la hora con punto y coma (6) · se confirmó que la guarda de `detector_partida` **no** debe abrirse: relajarla daría 23 candidatas con 5 falsos positivos graves (`con sumo cuidado`→`consumo`), y 4 pruebas nuevas fijan los contraejemplos (criterio §27) |

| 216–221 | 2009-01-08 | 65 | una sola voz en las 65 filas del plan · **sesión cerrada 65/65** · enero 2009 (Lehmann, Soto, Bernier, García; debate sobre reglas de Taylor e inercia; baja de 100 pb a 7,25 %) · las banderas eran referencias y traspasos (`2258:1`, `2289:2`, `2291:1`, `2291:3`, `2295:1`) · 2 correcciones y 5 marcas · se descubrió que una pasada anterior había dejado un par de comillas **invertido** (`”dilema del prisionero".`), resuelto enmendando la operación existente y añadiendo el cierre: comillas rectas 5→4, y el comentario del techo era inexacto · `yen` exigió ancla larga (75 veces como moneda, 312 coincidencias legítimas en `constituyen`/`excluyen`) · sin tocar: `2292:1` (titular pegado al final), `2262:2` (`Claudia Soto`, tratamiento documental) y `2289:2` (actor truncado: los actores se preservan) (criterio §28) |

| 222–229 | 2014-07-15 | 54 | una sola voz en las 54 filas del plan · **sesión cerrada 54/54** · julio 2014 (Lehmann, Fuentes, Vial, Claro, Vergara, Micco; recorte de 25 pb a 3,75 %) · las banderas eran los traspasos y agradecimientos protocolares del Presidente Vergara · **hallazgo: «tasa de instancia» (58 en 53 filas) NO es un defecto** —`instancia` es jerga nativa usada 89 veces fuera de esa colocución y `273:1` lo dice («como se llamaba entonces»); los dos PDF dan 0, pero son 2 de 131 sesiones y eso no es evidencia contra un término usado 147 veces · de los 16 apóstrofos sueltos del corpus, el de `674:2` **es una comilla de apertura**, no basura: se marcó · 10 correcciones (`Polítíca`→`Política` ×6, 4 apóstrofos limpios) y 1 marca (criterio §29) |

| 230–234 | 2014-11-18 | 42 | una sola voz en las 42 filas del plan · **sesión cerrada 42/42** · noviembre 2014 (Pistelli, Fuentes, Naudon, Micco; mantención en 3,0 %) · **sesión sin ninguna corrección OCR**: sobre la salida, `detector_partida` 0, `detector_deletreada` 0, espacio-antes-de-signo 0 y ninguna de las familias conocidas · con `\b` en la expresión regular, los verbos de turno que introducen a otro dan **cero** coincidencias: las menciones a García son los traspasos protocolares de Vergara · 1 sola marca: `6517:3` se corta en «Las proyecciones de.» con la cita del Comunicado sin cerrar — cuarta vez del mismo patrón (§25, §27, §28 dos veces), ya es una familia: las actas se truncan al final del Comunicado (criterio §30) |

| 235–241 | 2007-01-11 | 50 | una sola voz en las 50 filas del plan · **sesión cerrada 50/50** · enero 2007 (Lehmann, Magendzo, Valdés, Jadresic, De Ramón, Schmidt-Hebbel, Marshall, Desormeaux, Marfán, García, Velasco; baja de 25 pb a 5,0 %) · los 35 verbos de turno que «introducen a otro» son el estilo en tercera persona del acta o referencias · 8 correcciones y 2 marcas en la sesión · **dos familias se cerraron sin corregir nada**: la hora con punto (`17.15 horas`, 39 filas) es el estilo de la fuente —los dos PDF escriben `16.45` y `16.50` en «Se levanta la Sesión» y `13:10 horas` en el resto— y `A continuación,.` (76 filas) es el límite de segmentación: **las 76 ocurrencias terminan la fila** · `1054:1` tenía «profundizarl o» y `detector_partida` no podía verla: la guarda que la bloquea es `freq[segunda mitad] >= 50` y la segunda mitad es una letra · de ahí salió `detector_partida_letra` (8 pruebas), que mide **40 candidatos / 40 verdaderos** y destapó **58 palabras partidas en 44 filas** de 2005-2010, más 21 con segunda mitad de 2-4 letras; esa variante es 91 % precisa (`desorden en` es español correcto) y por eso se aplica leyendo, no como regla (criterio §31) |

| 242–250 | 2009-07-09 | 113 | una sola voz en las 113 filas del plan · **sesión cerrada 113/113**, la más grande leída hasta aquí (130.454 caracteres, 14 hablantes) · julio 2009 (De Gregorio, Marfán, Claro, De Ramón, Soto, Cowan, Céspedes, Velasco; baja de 50 pb a 1,75 %) · las 3 banderas del pre-cernido son referencias, no segundas voces · **la estructura dominante no es un defecto**: 40 y tantas filas vienen en pares pregunta/respuesta partidos por la segmentación («…consulta si X,» + «a lo cual el señor Y responde que…»); unirlas sería una decisión de segmentación, no de OCR · 2 correcciones, 2 marcas y 1 enmienda (la «r» suelta de `2633:1` cae dentro del tramo de una operación de §18) · los 6 candidatos de acento son variantes legítimas de §16 y los cuatro detectores dan 0 sobre la sesión, porque la pasada de §31 ya la había limpiado · **hallazgo transversal**: «staff e\\ apoyo» = «staff el apoyo», 9 filas repartidas en nueve sesiones que ninguna lectura había visto juntas (criterio §32, **aplicado**: 9 operaciones, la familia queda en 0 y las barras invertidas bajan de 29 a 20) |

| 248–253 | 2011-12-13 | 71 | una sola voz en las 71 filas · **sesión cerrada 71/71**, leída en dos tandas (25 + 42, más 4 ya anotadas) · diciembre 2011 (Vergara presidente, TPM a 4,0 %) · 2 banderas del pre-cernido, ambas referencia o anuncio de traspaso · **6 correcciones y 0 marcas**, todas residuos entre oraciones completas · el «4.» de `4489:2` **no** se borró: es el ítem 4 de la estructura del acta, presente en 21 filas; se fue sólo el apóstrofo huérfano, por enmienda · **hallazgo transversal**: la «i» suelta tras punto son **18 casos en 18 filas repartidos en 14 sesiones**, once ya cerradas sin haberla visto; quedan 16 (criterio §33) · apóstrofos censados: 41 en 38 filas, 11 legítimos · **trampa**: `plan` renumera las rondas y `registrar_sesion` marca la sesión entera |

| 1–6 | 2015-11-12 | 58 | una sola voz en las 58 filas · **sesión cerrada 56/56** (2 ya estaban anotadas) · noviembre 2015 · la única bandera es una referencia externa (Mario Draghi, presidente del BCE), no un asistente · 0 correcciones propias del acta: el único candidato de deletreada es falso positivo («con sumo cuidado») y los 2 acentos son legítimos · las 17 familias conocidas en 0 · **cambio de criterio (§34)**: los nombres propios dañados se normalizan cuando el corpus acredita la forma; pase transversal de nombres propios dañados: **41 operaciones en 35 filas**, cero formas dañadas restantes. Un undécimo caso, «Luis Oscar Herrera» sin tilde (10 apariciones, todas en 2005), **se revirtió**: no es daño de OCR sino la grafía del documento, y dos de esas actas ya estaban cotejadas contra el PDF (§34). El criterio de frecuencia solo resultó insuficiente y ahora exige además que la forma dañada no sea la grafía sistemática de un acta entera |

| — | **entrega v8** | 9.724 | publicada en `data/releases/continuidad_procedimental_v8` (9.723 → 9.724, una fila nueva: `RPM-2008-08-14:1995:2`) · gate propio `compare_procedural_v8.py`: todas las filas, todos los campos y todos los miembros de cada grupo · grupos 9.234 → 9.235 · alertas 484 → 484 · reservas 780/2661/5252 abiertas · 2.256 pruebas OK · **el `ID` de la base es posicional**: una fila nueva lo corre en +1 y eso invalidó las lecturas procedimentales v5; se refresca en memoria porque los cinco archivos implicados están fijados por hash (§35) |
| — | **corrección OCR v2** | 9.724 | reconstruida sobre v8 en `data/releases/correccion_ocr_v2` sin sobrescribir v1 · 1.462 filas con `Texto_Corregido` · `Texto` intacto en las 9.724 · **cero formas dañadas** de los 17 nombres · una sola operación re-anclada (`cambiarías`: 1995:1 → 1995:2) porque el corte la cambió de segmento |

| 7–16 | 2008-03-13 | 109 | **sesión cerrada 106/106** (3 ya estaban anotadas) · 15 actores · las 2 filas de la cola multihablante **ya estaban bien partidas en la base** (1718:10 Marshall / 1718:11 Marfán; 1737:1 Desormeaux / 1737:2 Claro) · 4 correcciones + pase transversal «T a sa»→«Tasa» en 6 actas · 2 marcas para cotejo PDF · 13 de 14 candidatos de acento eran falsos positivos |

| 17–25 | 2009-02-12 | 102 | **sesión cerrada 97/97** (5 ya estaban anotadas) · 14 actores · **cero correcciones**: 8 candidatos revisados y los 8 rechazados con la razón medida · el candidato multihablante (padre 2325) era una mención retrospectiva, no una segunda voz · los 4 de acento eran formas correctas («periodo» está en 36 actos) · los 3 de signo eran enumeración, cita del Acuerdo y la reserva 2661 |

| 26–31 | 2006-06-15 | 71 | **sesión cerrada 69/69** (2 ya estaban anotadas) · 14 actores · **cero correcciones**, segunda sesión seguida · ninguna fila en la cola multihablante · los 3 candidatos de acento eran tildes diacríticas legítimas («éstos» 2 filas, «cuánto» 1) · las 5 viñetas «•» son legítimas (141 en 31 actos): el hueco era del repertorio del auditor |

| 32–37 | 2009-08-13 | 79 | **sesión cerrada 78/78** (1 ya estaba anotada) · 15 actores · los **3** candidatos multihablante **ya estaban partidos en la base** (2661:10/11, 2667:1/2/3, 2680:2/3/4) · 3 correcciones + pase transversal «A continuación,.»→«A continuación,» en **76 filas** · 1 marca por residuo de lámina |

| 38–42 | 2008-01-10 | 49 | **sesión cerrada 45/45** (4 ya estaban anotadas) · 13 actores · el candidato multihablante (padre 1623) **ya estaba partido**: lo que la cola mostraba era el 7 suelto de 1623:1 pegado al inicio de 1623:2 · 9 de 10 candidatos de acento eran falsos · el décimo destapó la enumeración completa de «hacía»: **17 verbos y 15 preposiciones**, se corrigieron las 15 y el suelo de la guardia bajó de 32 a 17 medido · 3 residuos de paginación |

Para anotar una ronda leída:

```
.venv/bin/python scripts/rondas_lectura_lote9.py registrar N HALLAZGO "justificacion"
```
