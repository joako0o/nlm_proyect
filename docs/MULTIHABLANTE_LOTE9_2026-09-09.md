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

Era el universo pendiente. No se leyeron las 339 en texto completo —son 134.189 caracteres—
sino que se cubrieron con el único instrumento que **valida contra los tres positivos
conocidos**: el barrido B. Ese barrido ya recorrió las 9.723 filas del corpus, así que las
339 están incluidas.

| | |
|---|---:|
| Universo | 339 |
| Cubiertas por el barrido B (validado) | **339** |
| Marcadas por el barrido B | **2** |
| Leídas completas además | 15 |
| Con alerta del motor | 3 |
| Falsos positivos de esa alerta | **3** |

Las 2 marcadas por el barrido B dentro de las 339 son `2960:2` y `1564:1`: las dos ya leídas
y confirmadas con dos voces. No apareció ninguna nueva.

Además se leyeron completas **las 14 más largas** (de 6.772 a 1.520 caracteres, que es donde
una segunda voz tendría más espacio) y **las 3 con alerta del motor**. Las 17 resultaron una
sola voz: el otro nombre siempre está citado, despedido, bienvenido o como fuente de la
información, nunca hablando.

Las 3 alertas del motor dentro de las 339 son **falsos positivos**:

- `1338:3` — Jadresic pide la palabra y expone; Magendzo aparece citado («comentó que los datos apuntan a 3%»).
- `2397:1` — Claro comenta la exposición de Lehmann; no habla Lehmann.
- `4656:1` — Vergara abre la sesión, constata la ausencia de Larraín y ofrece la palabra.

## Dos detectores construidos y descartados

Intenté dos veces un detector por sujeto con cargo ajeno. El primero (C) marcaba 141 filas y
recuperaba 1 de 3 positivos. El segundo (D) corregía un defecto real de género —`ministra` no
contiene `ministro`, y por eso `1564:1` se escapaba— y aun así sigue sin recuperar `657:1` ni
`1564:1`. Ambos quedan **descartados como cobertura**: un instrumento que no pasa por positivos
conocidos no prueba nada sobre el resto, aunque marque pocas filas.

El único instrumento validado es el barrido B, que recupera **3 de 3**.

## Cobertura final: lo que sí y lo que no

**Cubierto:**

- Las 71 filas con ≥2 personas de la asistencia — leídas todas.
- Las 9.723 filas del corpus bajo el barrido B — 980 tienen entrega de la palabra, 8 tienen texto sustantivo después, leídas las 8.
- Las 339 filas con exactamente 1 otra persona — barridas por B; leídas además las 14 más largas y las 3 con alerta del motor.
- **93 filas con lectura completa registrada.**

**No cubierto:** una segunda voz que entre sin fórmula de entrega de la palabra y sin sujeto
con cargo —el patrón de `657:1`, que allí se detectó sólo porque venía precedido de una
entrega. No tengo un instrumento validado para ese caso, así que no puedo afirmar que el eje
está cerrado.

Lo que sí puedo afirmar: **no queda ningún candidato de un instrumento validado sin leer.**

## Siguiente paso

Construir un detector que pase por los 3 positivos conocidos —incluido `657:1`, que no tiene
ninguna fórmula— antes de aplicarlo. El conjunto de prueba mínimo son esos 3; mientras un
detector no los recupere no sirve, como se vio dos veces.

Después: registro curado, validador y corrida para los tres cortes de atribución.

## Evidencia

`docs/continuidad_lote9_2026-09-09/lecturas.json` — 93 casos con lectura completa, hallazgo,
justificación y el resultado de validación de cada barrido.
`docs/multihablante_v7_2026-09-09/inventario_multihablante_v7.csv` — las 643 filas con al
menos otra persona de la asistencia.
