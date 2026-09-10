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

Para anotar una ronda leída:

```
.venv/bin/python scripts/rondas_lectura_lote9.py registrar N HALLAZGO "justificacion"
```
