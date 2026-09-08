# Octavo bloque: exposiciones, respuestas y cargos provisionales

**Fecha:** 2026-09-08 · **PR:** [#3](https://github.com/joako0o/nlm_proyect/pull/3)

Pasada terminada y publicada tras cinco ciclos. **No queda un proceso activo en segundo plano.**

## Resultado

| Indicador | Loop7 | Loop8 |
|---|---:|---:|
| Filas físicas XLSX | 9.405 | **9.412** |
| Bloques de texto | 9.404 | **9.411** |
| Filas con alertas | 508 | **433** |
| Pruebas de regresión | 582 | **711** |
| Revisiones individuales de hablantes | 96 | **97** |
| Alertas contextuales documentadas | 0 | **1** |
| Grupos multipárrafo | 301 | **312** |
| Intervalos originales pendientes de lectura contextual | 305 | **232** |

Hay cambios en **110 padres**:

- **12 de segmentación o atribución:** 29 → 36 segmentos, **7 filas nuevas**. Algunos cambios adelantan un límite sin añadir filas; no debe medirse el trabajo sólo por el número de filas nuevas.
- **98 sólo de metadatos**, sin cambiar su texto, actor o partición. Predominan mejoras de evidencia del sujeto; también hay cambios de continuidad y una reclasificación conservadora en 14 que mantiene visible una atribución legada.
- **7.109 padres restantes sin cambios semánticos**, aparte del desplazamiento de IDs consecutivos de fila/turno.

La comparación global reconstruye los **7.219 textos**, omitiendo sólo espacios. Se conservan las **2.048.560 palabras**, las 132 sesiones, las 51 etiquetas de actor, los esquemas XLSX de 37/24 columnas y el máximo de 31.948 caracteres por celda. **F0 y F1 pasan sin errores bloqueantes**, con 310 fórmulas TPM contrastadas.

**Esto no es certificación semántica ni cotejo PDF/humano exhaustivo.** La lectura fue dirigida a sujetos, límites, retornos y contexto pertinente; no se certifica íntegramente cada uno de los 110 padres.

## Cinco ciclos y controles

| Ensayo aislado | Trabajo | Filas | Alertas |
|---|---|---:|---:|
| 1 | Inicios de exposición, respuestas, adhesión y valoración | 9.406 | 467 |
| 2 | Recomendaciones, gráficos, aperturas y variante de Corbo | 9.411 | 435 |
| 3 | Respuesta de Lehmann en 4469; cargo provisional en 4433; incisos acotados | 9.411 | 434 |
| 4 | Defensa contra verbos prestados por una subordinada | 9.411 | 435 |
| 5 | Dos variantes completas de retorno al expositor | **9.412** | **433** |

Estos son resultados intermedios de construcción, no cinco publicaciones certificadas. Los fallos de regresión y controles negativos se resolvieron antes de la publicación final. El cuarto ciclo aumenta deliberadamente una alerta: no se conserva una apariencia de evidencia explícita sólo para reducir el contador.

La publicación final ejecutó `python scripts/preparar_data.py`: recuperación disponible, **711 pruebas**, construcción, proyección final, F0 y F1. El contenido publicado coincide con el quinto ensayo aislado.

## Reconocimiento explícito, no atribución por proximidad

Se revisaron candidatos de atribuciones heredadas, leyendo comienzos/finales y los límites pertinentes; en los casos largos no se presenta esa lectura acotada como lectura integral. Entre las familias abordadas están:

- «da inicio a su presentación/intervención», «procede a responder» y «procede a dar respuesta»;
- variantes concretas de «se suma» ligadas a comentarios, planteamientos, preocupación o parabienes, **no una regla genérica para incorporarse a una reunión o grupo**;
- «discrepa», «adhiere», «califica», «acoge», «atribuye», «recomienda», «reafirma», «ratifica» y «hace alusión»;
- exhibición de un gráfico como parte de la exposición;
- inciso completo de apertura «junto con dar inicio a la Reunión de Política Monetaria N° …», con número acotado y verbo principal exigido;
- incisos «aludiendo» y «en referencia» con las mismas restricciones frente a otra cláusula;
- prefijos completos «Prosiguiendo con su exposición» y «Al proseguir con su presentación».

La variante **Vittoho Corbo** se reconoce sólo en la vista normalizada, como Vittorio Corbo. Se preserva el texto original: no se limpia el OCR ni se corrigen calendarios o números de sesión de las actas.

Las defensas siguen rechazando citas, destinatarios y referencias como «la opinión del…». La nueva prueba negativa detectó que un inciso podía terminar justo antes del verbo de una subordinada y tomarlo como verbo del sujeto principal. Ahora se evita ese préstamo cuando el prefijo termina en «que», «quien», «donde», «cuando» o «como».

### Consecuencia visible en 14

«El Gerente … Esteban Jadresic, en relación a lo que señala el señor Herrera, expresa…» conserva su texto y actor, pero deja de figurar como sujeto explícito por un reconocimiento que estaba tomando el «señala» de Herrera. Queda como atribución legada con aviso. **No se está afirmando que Jadresic sea incorrecto**, sino que la evidencia que usaba el detector no justificaba la categoría anterior.

Las regresiones históricas actualizadas conservan actores y longitudes esperadas: ciertas exhibiciones/retornos antes habilitados sólo por revisión individual ya se reconocen sin ella. Las revisiones anteriores no se borraron ni se sustituyeron por anclajes globales.

## Los 12 padres con cambios estructurales

| Padre | Corrección o delimitación | Conservación y límite |
|---|---|---|
| **263** | Corbo → reapertura institucional → Corbo | La solicitud a Valdés deja de estar absorbida por la fila institucional. Se preservan «Vittoho» y la constancia de ausencia de Cecilia Feliú. |
| **1869** | Se separa el retorno final de Sergio Lehmann | Sus 338 caracteres sobre futuros de petróleo/gasolina no quedan dentro de la intervención del Presidente. Los intercambios anteriores se conservan. |
| **2512** | De Gregorio → Lehmann | El retorno empieza cuando el Gerente de Análisis Internacional exhibe la gráfica, no en una mención posterior. Lehmann conserva 2.284 caracteres. |
| **2519** | Andrés Velasco → Lehmann | El retorno se adelanta a «Prosiguiendo con su exposición…». La exposición de Lehmann queda íntegra en 4.384 caracteres. |
| **2725** | Lehmann → Claro → Lehmann → Pablo García → Lehmann | Se recupera el comentario de Claro sobre el mecanismo de reservas de la FED, sin confundir las referencias con nuevos turnos. |
| **3422** | Felipe Larraín → De Gregorio | Se conservan los 80 caracteres incompletos de Larraín, que terminan en «por el señor». No se inventa el destinatario omitido. |
| **4360** | Rodrigo Vergara → Claudio Soto | Soto retoma al exhibir los gráficos de riesgo y conserva 2.740 caracteres de exposición, sin esperar a la siguiente sección. |
| **4433** | Se adelanta el retorno explícito de Soto | Quedan 4.022 caracteres de Soto, 705 atribuidos provisionalmente a Lehmann y 1.482 de Soto. **El tramo intermedio no se certifica: lleva la alerta contextual descrita abajo.** |
| **4469** | Manuel Marfán → Lehmann | La respuesta comienza en «En opinión del señor Sergio Lehmann», no en la posterior exhibición. Marfán ocupa 293 caracteres y Lehmann 2.353. |
| **4860** | Manuel Marfán → Lehmann | Se separan los 495 caracteres del expositor sobre los gráficos de Brasil y su continuación en 4861. |
| **5279** | Manuel Marfán → Lehmann | Retorno de 720 caracteres en «Al proseguir con su presentación», seguido por la exposición de 5280. |
| **6065** | Herrera → Pablo García → Lehmann | El heat map no queda atribuido a García. Se mantienen los 2.790 caracteres de Lehmann y el final sin puntuación de Herrera. |

La única revisión de hablante añadida es **HAB-20260908-4469**, con hash, límites, citas y justificación en [revisiones_hablantes.json](../data/curation/revisiones_hablantes.json). Sus 96 entradas anteriores permanecen intactas. No se generaliza «En opinión…» a toda mención ni `CONTEXTO_REVISADO` a ancla automática.

Además de estos retornos, se comprobaron por regresión exposiciones que permanecen completas: por ejemplo, **8.530 caracteres de Miguel Fuentes en 6767** y **6.081 de Sebastián Claro en 6802**. Mejorar la evidencia al comienzo no fragmenta el resto de la intervención.

## Alerta contextual nueva: cargo de la fuente por verificar

El padre **4433** contiene literalmente:

> El Gerente de Análisis Internacional prosigue con su presentación, indicando que el mercado laboral continúa bastante estrecho.

Ese cargo corresponde a Lehmann en la sesión, pero aparece entre dos partes expresamente atribuidas a Soto sobre el escenario interno. **El tema y la proximidad no permiten decidir por sí solos que el cargo del original está equivocado.**

Se conserva provisionalmente la atribución basada en el cargo, pero se añade **`CARGO_EN_DISCURSO_POR_VERIFICAR`** a los 705 caracteres delimitados. El registro [alertas_contextuales.json](../data/curation/alertas_contextuales.json) contiene fuente, fecha, hash del padre, límites, texto exacto, actor provisional y alcance. No modifica asistencia ni corrige al actor silenciosamente.

El módulo [context_warnings.py](../scripts/context_warnings.py):

- rechaza cambios de fuente, fecha, hash, límites o alcance;
- aplica el aviso sólo al intervalo/actor correspondiente;
- hace fallar F1 si el intervalo desaparece, cambia de actor, se duplica o pierde el aviso sin nueva revisión;
- mantiene una barrera de continuidad: el siguiente párrafo no hereda seguridad desde un tramo advertido.

Esta es una advertencia de incertidumbre, **no una adjudicación de error confirmado**. El original debe cotejarse antes de resolver ese tramo.

## Continuidad preservada y 14 enlaces comprobados

No se perdió ningún enlace previo entre padres, incluidos los 18 comprobados expresamente en los primeros bloques y los dos de Herrera 5994–5996 del loop7. Los grupos no alcanzados por cambios conservan su composición por padre/texto/actor, independientemente de la numeración del turno.

Nuevos enlaces, contrastados con ambos extremos:

- **Apertura del Presidente y su cesión siguiente:** 2553→2554, 2657→2658, 2690→2691, 2714→2715, 2842→2843, 2890→2891 y 3024→3025. El enlace alcanza sólo la cesión del Presidente; no atribuye a éste la presentación posterior de Lehmann.
- **Partes de la exposición de Soto:** 2863→2864.
- **Partes de exposiciones de Lehmann:** 3999→4000, 4230→4231, 4860→4861, 5102→5103, 5103→5104 y 5279→5280.

Hay **312 grupos multipárrafo**, con máximo de once filas. Las exposiciones de Pablo García en **60–70 y 142–152** permanecen intactas. No se agrupan todas las intervenciones de una persona durante una sesión: las vueltas después de otra persona siguen siendo vueltas distintas.

## Documentos, menciones y duplicados no se reinterpretaron

- Los **tres escritos** de Larraín leídos por Vergara siguen en cuatro tramos cada uno, con autor/lector distintos, tipo `OPINION_ESCRITA`, rol documental, asistencia no inferida y aviso obligatorio. Se verificó el vínculo con [documentos_leidos.csv](../data/processed/documentos_leidos.csv) y la naturaleza documental en [turnos_habla.csv](../data/processed/turnos_habla.csv).
- Las **diez anotaciones actuales de menciones** y las **21 fórmulas exactas** no cambiaron.
- Persisten **606 duplicados exactos**, de los que **603** son fórmula. Las tres filas sustantivas repetidas de 5212, 5256 y 5385 no se eliminan.
- El libro original permanece intacto. Se verificaron **57 hashes de entradas/código y 11 de salidas** contra la publicación.

## Alertas y las 783 originales

| Motivo actual, con solapamientos | Filas |
|---|---:|
| Atribución heurística legada | 104 |
| Final sin puntuación | 252 |
| Posible otro hablante o mención | 23 |
| Atribución por anáfora | 42 |
| Fragmento breve | 9 |
| Variante de identidad | 6 |
| Duplicado no fórmula | 3 |
| Texto escrito leído por tercero | 3 |
| Cargo en discurso por verificar | 1 |

El descenso **508 → 433** no se interpreta como 75 errores confirmados. Tampoco la reducción neta **182 → 104** de atribuciones legadas equivale a cambios de identidad: muchas ya tenían el actor correcto, pero carecían de evidencia reconocida por el detector.

En el seguimiento de las 783 originales quedan:

- **232** pendientes de lectura contextual;
- 59 fórmulas reclasificadas;
- **210** con método actualizado;
- **172** con segmentación/actor modificados por comparación;
- 86 correcciones dirigidas aplicadas;
- siete breves válidos, ocho menciones históricas, seis identidades, dos repeticiones históricas y una continuidad documentada.

Son **163 estados de lectura dirigida, 382 de comparación automática y 238 de triaje**. Cuatrocientos intervalos originales aún se solapan con alertas actuales. El descenso de pendientes **305 → 232** incluye **70 cambios de método y tres de comparación estructural**; **no son 73 nuevas lecturas humanas ni cierres semánticos**. La nueva revisión 4469 se cuenta en el registro de hablantes, sin inflar el contador histórico de correcciones dirigidas.

## Pendientes y límites

Permanecen sin adjudicar los cinco candidatos filtrados **780, 3191, 5367, 5647 y 6185**. No se afirma una nueva lectura exhaustiva de ellos en este bloque. Los límites y cautelas del checkpoint anterior siguen vigentes: frontera dañada De Gregorio/Corbo; intervenciones conjuntas; petición colectiva de los Consejeros; compromiso incrustado con continuación ambigua; y referencia/confirmación de Bernier dentro de la exposición de Lehmann.

**No son cinco pendientes totales:** quedan **433 filas con alertas, 232 intervalos originales pendientes**, la advertencia de cargo en 4433 y el método legado visible en 14, además de los otros residuos registrados. Sigue faltando cotejo de originales ambiguos/dañados y una muestra semántica independiente con y sin alertas. **No hubo nuevo cotejo PDF ni revisión humana independiente en esta pasada.**

## Entregables

- [Excel final](../data/processed/consolidado_base_referencia_final.xlsx) y [auditoría](../data/processed/consolidado_base_referencia.xlsx).
- [Cambios por padre y segmento](cambios_loop8_2026-09-08.csv).
- [Comparación completa antes/después](comparacion_loop8_2026-09-08.json).
- [Checkpoint](estado_revision_loop8_2026-09-08.json).
- [QA](../data/processed/qa_preparacion.json), [manifiesto](../data/processed/manifiesto_preparacion.json) y [cola actual](../data/processed/revision_pendientes.csv).
- [Regresiones del bloque](../tests/test_loop8_review.py): 110 fixtures de padres, límites, guardias negativas, conservación de exposiciones y validación de alertas contextuales.

```bash
python scripts/preparar_data.py
```

Las verificaciones son locales. El workflow de Actions continúa fuera del PR por falta del permiso `workflows` de la conexión; no se informa una ejecución remota inexistente.
