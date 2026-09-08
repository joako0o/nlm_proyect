# Loop14 — Exposiciones largas y separación de cierres personales del acta

**2026-09-08 · [PR #3](https://github.com/joako0o/nlm_proyect/pull/3).**
Base anterior: `ac374954be2e62d207e9467b8be50c07d3289226`,
[loop13](REVISION_LOOP13_2026-09-08.md). Lectura dirigida por agente del
consolidado, **sin nuevo cotejo PDF ni revisión humana independiente**.

## Resultado publicado

| Medida | Antes | Ahora |
|---|---:|---:|
| Filas físicas XLSX | 9.497 | **9.499** |
| Bloques de texto | 9.496 | 9.498 |
| Grupos de turno | 9.087 | 9.088 |
| Grupos de varias filas | 314 | 315 |
| Filas con alertas | 343 | **329** |
| Padres con alertas | 309 | **296** |
| Pruebas | 1.035 | **1.073** |
| Intervalos de hablante revisados | 192 | **208** |
| Padres con revisión de hablante | 188 | 204 |
| Advertencias contextuales | 13 | 15 |
| Continuaciones de acta revisadas | 1 | 1 |

**20 padres afectados:** tres estructurales (8 → 10 segmentos), 16 con revisión
de atribución y uno —2490— sólo con actualización de trazabilidad. No son 20
nuevos diálogos separados ni 20 padres completamente leídos. Los otros
**7.199 padres** conservan sus campos semánticos, descontando identificadores
secuenciales. Se conservan los **7.219 textos** originales.

- [Comparación global antes/después](comparacion_loop14_2026-09-08.json)
- [Detalle por fila y hash](cambios_loop14_2026-09-08.csv)
- [Checkpoint y pendientes](estado_revision_loop14_2026-09-08.json)

## 1. Dieciséis intervalos con lectura dirigida acotada

### Diez exposiciones completas de Valdés

**178, 214, 288, 305, 390, 438, 492, 557, 587 y 615.**
Se leyeron completos los intervalos de exposición, con las cesiones nominales
pertinentes y el retorno o apertura de comentarios posterior. Las enumeraciones,
los párrafos de desarrollo y los argumentos a favor de distintas opciones son
parte de la misma presentación. Los acuerdos de reuniones anteriores relatados
por el expositor **no se convierten en turnos nuevos del Consejo**.

En los padres que contienen otros participantes, la revisión se limita a Valdés:
no absorbe el regreso de Corbo ni las intervenciones posteriores. En particular,
288 y 305 mantienen separados los comentarios de otros gerentes después de la
apertura presidencial. Cada entrada registra fecha, hash, inicio, fin, citas,
justificación y limitación.

### Recomendaciones y respuesta

- **1605:** García desarrolla su recomendación preventiva de 25 puntos base y
  comunicación, después de la cesión nominal de la Presidencia. En 1606 recibe
  la palabra Beltrán de Ramón: no es continuidad de García.
- **1607:** Jadresic desarrolla su recomendación después de la cesión nominal.
  Las referencias a García y Schmidt-Hebbel comparan argumentos ajenos; no son
  cambios efectivos de hablante dentro de su exposición.
- **2036:** García desarrolla las opciones de 50 y 75 puntos base; la Presidencia
  agradece y abre comentarios en 2037. Se conserva la exposición completa.
- **836:** Lehmann responde a la consulta de De Gregorio por la trayectoria del
  petróleo. Desormeaux abre una consulta distinta en 837. El nombre permite
  revisar al hablante, pero el cargo textual queda pendiente, como se explica abajo.

### Dos introducciones, no dos series certificadas

**351 y 727:** sólo se revisan las frases introductorias de **61 caracteres** del
«Gerente de División mencionado», inmediatamente después de la cesión nominal a
Valdés. Se vio el inicio de las exposiciones siguientes, pero **no se declara
leída ni revisada íntegramente su continuación** con estas dos entradas.

Son **16 intervalos nuevos en 16 padres nuevos del registro**. Los 192 intervalos
anteriores y las 188 raíces permanecen idénticos; no se modifican las revisiones
secundarias de 1923/2622/4923/5367. `CONTEXTO_REVISADO` no crea anclas globales;
`Fin` por sí solo tampoco crea nuevos cortes.

## 2. Tres correcciones entre persona e institución

| Padre | Corrección |
|---|---|
| **2489** | Se separan los **200 caracteres** del cierre explícito de De Gregorio de los **74** de la reanudación institucional. |
| **2538** | Se aplica la misma distinción: **200** de cierre presidencial y **74** de reanudación impersonal. |
| **3269** | Los **247 caracteres** de apertura y bienvenida corresponden al Presidente explícito, no al Consejo institucional. |

Las locuciones «pone término a la sesión» y «abre la sesión» exigen sujeto y
predicado compatibles. Se mantienen las guardias de citas y subordinadas.
**«Se levanta la Sesión» impersonal sigue siendo acta**, no una voz presidencial
inferida. Ambas locuciones actúan como barreras a la herencia discursiva posterior.

En 2489 se conserva literalmente **«N° 137, Siendo las 16:00 horas, se reanuda la
Sesión de Política Monetaria»**. Sólo esa fórmula constatada reconoce el número
desplazado; no se generaliza a cualquier prefijo numérico o basura OCR.
No se completa su puntuación. En 3269 permanece **«A continuación,.»** y no se
atribuye la bienvenida al ministro que la recibe.

**2490 sólo cambia su referencia al antecedente:** de segmento 4 a segmento 5 de
2489. No hay nueva atribución ni lectura integral adjudicada de 2490. Su texto,
actores y continuidad entre padres permanecen iguales.

El nuevo grupo de varias filas está **dentro de 2489**: el comentario presidencial
y su cierre. No es una nueva unión entre padres. En 3269 la mañana y la apertura
de la tarde siguen en turnos distintos pese a compartir Presidente.

## 3. Dos advertencias que no se ocultan al revisar al hablante

- **587 — `TEXTO_DANADO_POR_COTEJAR`:** «apreciación del Agrega que» contiene una
  ruptura textual. La exposición se identifica como Valdés, pero no se reconstruye
  la parte ausente ni se considera resuelto el daño por reconocer al hablante.
- **836 — `CARGO_EN_DISCURSO_POR_VERIFICAR`:** el texto dice «Gerente de Análisis
  Financiero» y la nómina local vincula a Lehmann con Análisis Internacional.
  Nombre identificado no equivale a cargo textual confirmado. Se conserva el OCR.

Las trece advertencias anteriores quedan intactas, incluidas 4433, 6443, los
residuos colectivos, daños y discrepancias de cargo de 180/5573/6282.

## 4. Ensayo, pruebas y publicación

Se ejecutó un ensayo aislado, su comparación global y el pipeline integral.
La primera ejecución de pruebas señaló cinco expectativas anteriores pendientes
de actualización: conteos del registro/avisos y contratos de 178/3269. Se cambiaron
sólo esas expectativas verificadas, sin modificar fixtures ajenas a la pasada.

`python scripts/preparar_data.py`: **1.073 pruebas, F0 y F1 aprobados**.
Hay **38 pruebas nuevas**: 20 contratos exactos por padre y 18 de comportamiento,
alcance, conservación, advertencias y barreras. La publicación de la base de
auditoría coincide campo por campo con el ensayo aislado.

Verificación global posterior:

- **7.219 textos y 2.048.560 palabras conservados**, ignorando sólo espacios.
- **Todos los enlaces previos entre padres y los grupos no afectados intactos**;
  no hay enlaces nuevos ni retirados. Se mantiene 2790 → 2791; no se restaura
  el enlace erróneo 5402 → 5403.
- Las dos exposiciones de García de once filas se conservan.
- Los **192 intervalos anteriores**, 13 avisos, 11 menciones actuales, 21 fórmulas
  y registros documentales permanecen intactos.
- **65 hashes de entradas/código y 11 de salidas verificados**.
- 132 sesiones, 51 etiquetas/50 personas, 310 contrastes TPM y esquemas XLSX **37/24**.
- El modelo 5212/5742/5802 conserva Herrera → Vergara → escrito de Larraín leído
  por Vergara → Vergara. **Autor ≠ lector**, sin inferir asistencia ni habla oral.
- 3110 sigue como continuación de acta `ACTA_INSTITUCIONAL`, no Orellana ni
  comunicado monetario; la revisión previa de 797 caracteres de 3421 sigue intacta.

## 5. Pendientes y límites

**329 filas con alertas en 296 padres.** Motivos superpuestos:

| Motivo | Filas |
|---|---:|
| Anáfora | 16 |
| Atribución heurística legada | 8 |
| Cargo textual por verificar | 5 |
| Final sin puntuación | 258 |
| Fragmento breve | 10 |
| Posible otro hablante o mención | 21 |
| Pasajes conjuntos por delimitar | 6 |
| Texto dañado por cotejar | 3 |
| Variante de identidad | 6 |
| Duplicado no fórmula | 3 |
| Escrito leído por tercero | 3 |
| Hablantes por identidad pendiente | 1 |

Anáforas **32 → 16**; alertas totales **343 → 329**, manteniendo los dos nuevos
avisos. Esto no significa que las otras filas sean semánticamente perfectas ni
que las 329 estén todas sin leer. Persisten 780/6185, residuos de 3191/5367,
4433, identidades pendientes como 6443, daños y otras advertencias. Los candidatos
filtrados no representan el universo completo de pendientes.

Cola histórica de 783: **117** pendientes de lectura contextual, **315** métodos
actualizados, **171** cambios por comparación, **98** correcciones dirigidas,
58 fórmulas, siete breves, ocho menciones históricas, seis identidades, dos
repeticiones y una continuidad. Su clasificación da **486 comparaciones
automáticas, 174 lecturas dirigidas y 123 triajes**. Esta cola clasifica los cambios
de método como comparación automática; no sustituye el registro de las 16 nuevas
lecturas acotadas de esta pasada. La bajada **131 → 117 no equivale a 14 lecturas
humanas ni cierres integrales**. Las once menciones actuales se cuentan aparte.

Los conteos históricos y actuales usan unidades superpuestas: **no se suman**.
Faltan cotejo de originales en casos ambiguos/dañados y una muestra independiente
con y sin alertas. No hubo nuevo cotejo PDF ni lectura exhaustiva del corpus.
El workflow de GitHub Actions permanece fuera del PR por falta de permiso
`workflows`; las verificaciones descritas son locales. No queda proceso activo.
