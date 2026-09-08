# Décimo bloque — opiniones intercaladas y discurso referido

**Publicado, 2026-09-08: 9.466 filas / 372 filas con alertas / 871 pruebas; F0 y F1 aprobados.** Sin proceso activo. Continúa el [PR #3](https://github.com/joako0o/nlm_proyect/pull/3).

Comparación contra [loop9](REVISION_LOOP9_2026-09-08.md), commit `3f02b97b557d2d8afc6b549ef3bfe387d435f0a9`: 9.427 filas, 391 alertas, 789 pruebas, 101 revisiones de hablante y diez menciones actuales.

## Resultado

- **60 padres afectados:** **39 estructurales**, de 66 a 105 segmentos (**39 filas adicionales**), y **21 sólo metadatos**, sin cambios de texto/actor.
- **37 revisiones individuales de hablante**, con hash, límites, citas y justificación. Total acumulado: **138**; las 101 anteriores intactas.
- **Una mención documentada nueva, 2325**: once actuales en total. Se conserva la alerta automática, sin volver a asignar una referencia a la Ministra como discurso suyo.
- Los **7.159 padres restantes** conservan sus columnas semánticas; se excluyen IDs globales renumerados.
- Todas las continuidades previas se conservan **excepto 5402→5403**, retirada justificadamente porque Claro interviene entre la exposición y la respuesta de Lehmann. No se añadieron enlaces. Permanecen 313 grupos multipárrafo y las exposiciones de once filas.

**La cola automática no era suficiente:** 36 de los 37 inicios revisados estaban dentro de segmentos sin ninguna alerta en loop9; el restante, 6257, sólo tenía un aviso de final sin puntuación. Es un resultado de esta búsqueda dirigida de fórmulas nominales, no una muestra aleatoria ni una estimación del error en todo el corpus.

## Ciclos y correcciones descartadas

| Ensayo aislado | Filas | Alertas | Padres estructurales | Sólo metadatos |
|---|---:|---:|---:|---:|
| Base loop9 | 9.427 | 391 | — | — |
| 1: incisos y predicados, provisional | 9.427 | 372 | 3 | 21 |
| 2: guardia retrospectiva, 33 revisiones y cargo de Soto | 9.460 | 373 | 35 | 19 |
| 3: cuatro opiniones adicionales | 9.466 | 373 | 39 | 20 |
| 4: contracciones `al`/`del` en incisos | **9.466** | **372** | **39** | **21** |

Cada fila se compara con loop9, no se suman los cambios. Después se documentó la mención de 2325 y se volvió a ejecutar el pipeline completo. La base publicada coincide por contenido con el ensayo 4; la anotación de mención se refleja en la cola y reportes de QA.

**El primer ensayo no se aceptó como resultado:** añadir «se refirió» como predicado de turno separaba indebidamente una referencia retrospectiva a Jadresic dentro de Valdés en 1013. Se retiró esa regla y también desapareció el enlace provisional 3125→3126. «Se refirió» ahora sólo bloquea prestar un verbo al sujeto mencionado en un prefijo; no abre por sí mismo un turno actual. 1013 permanece idéntico a loop9 y tiene una fixture adversarial propia.

## Cambios de atribución y límites

### Opiniones y respuestas acotadas

Los intervalos están registrados en [revisiones_hablantes.json](../data/curation/revisiones_hablantes.json). Se interpretó el pasaje y el contexto pertinente; **no se añadió una regla global de «En opinión»/«A juicio»**.

| Padres | Límite recuperado |
|---|---|
| 2674, 4634 | Opinión de Marshall entre partes de la presentación de Soto, con retorno explícito de Soto. |
| 3011 | Céspedes comienza en «El Gerente aludido menciona», tras la cesión nominal del Presidente, no sólo en la opinión posterior. Se mantienen los 8.431 caracteres anteriores de García y los 3.157 del desarrollo de Céspedes. |
| 3056 | La opinión de Marfán comienza antes de su advertencia ya reconocida; García responde después. |
| 3435, 4477 | Marshall aporta su evaluación propia después de Claro/Herrera, respectivamente. |
| 3442 | De Ramón opina entre el comentario de Marfán y el retorno de Jaque. |
| 3523, 4148, 4709 | Marfán opina después de De Gregorio, Lehmann y Vergara, respectivamente. |
| 4252, 7174 | Vergara aporta su propia evaluación, no atribuible a Herrera/García. |
| 4256 | Bernier precisa por qué el episodio no supone un mercado trabado persistentemente. |
| 4342, 4922, 5347, 5793, 6069, 6953, 6985 | Claro interpreta, objeta o responde después del hablante anterior. |
| 4589, 5470, 6305, 6456, 6791, 6839, 7142 | Vial desarrolla una evaluación propia; no se absorbe por el expositor anterior. |
| 4903, 6118 | Lehmann responde a la pregunta previa y continúa su presentación. En 6118 se conserva literalmente la `V` aislada anterior a «A juicio». |
| 6163, 6869, 6900, 6902 | García aporta una interpretación o pregunta propia; se preservan los cambios siguientes. |
| 6257, 7021 | Claro/Vial interrumpen a Fuentes; éste responde y retoma la exposición dentro del mismo padre. |
| 5402 | Claro cuestiona la interpretación del VIX tras una presentación larga de Lehmann; la respuesta de éste está en 5403. |
| 7079 | **Fuentes → Soto → Fuentes → Claro**. El cargo completo «Asesor Macroeconómico del Ministro de Hacienda» permite reconocer el reparo de Soto; no se atribuye ese reparo al Ministro ni a Fuentes. |

Las revisiones no deben extenderse hasta el final del padre por defecto: varios padres contienen otros hablantes después del segmento revisado. Se validaron sus límites exactos. Los tramos largos, retornos, daños y citas permanecen literales, incluidas las comillas OCR mixtas de calificaciones financieras en 5402.

### Dos reunificaciones correctas

- **2052:** una sola exposición de Lehmann. Reconocer «continuando su comentario» elimina una frontera de método entre dos tramos contiguos del mismo hablante.
- **2325:** García explica estrechez crediticia y endeudamiento. «A que se refirió la señora Ministra de Hacienda Subrogante» es referencia retrospectiva, no una intervención actual de Recart. Se reúne la explicación de García. El aviso de posible otro hablante queda visible y anotado como **mención legítima** mediante `MEN-20260908-2325`; no se elimina para mejorar cifras.

### Métodos sin cambio de actor/texto

Se reconocen incisos temáticos acotados y locuciones como desacuerdo, asignación de probabilidad y cautela. Siguen exigiendo predicado del sujeto y rechazando citas, presencia o verbos prestados por una relativa. Los 21 cambios sólo de metadatos incluyen **5403**, cuyo grupo cambia por la interrupción de Claro, y **2481**, con identificación más específica del sujeto. No representan 21 correcciones de identidad ni 21 lecturas integrales.

## Continuidad, conservación y pruebas

La comparación global comprueba:

1. Reconstrucción de los **7.219 textos**, ignorando sólo espacios; **2.048.560 palabras** conservadas.
2. Actores/textos iguales en los 21 padres de metadatos y columnas estables iguales en los otros 7.159.
3. Exactamente un enlace retirado: **5402→5403**. Todos los demás y los grupos no afectados se conservan. Las dos exposiciones de García de once filas permanecen intactas.
4. Original XLSX sin cambios; 132 sesiones, 51 etiquetas de actor/50 personas y 310 contrastes TPM.
5. Tres documentos de Larraín leídos por Vergara, autor ≠ lector, sin inferir asistencia ni habla oral del autor; `documentos_leidos.csv`, naturaleza escrita y esquemas XLSX **37/24** preservados.
6. Las 101 revisiones anteriores de hablante, diez menciones anteriores y 21 fórmulas revisadas intactas. La alerta de cargo de **4433** sigue visible y bloquea continuidad. Las revisiones contextuales no crean anclas por sí solas.

`python scripts/preparar_data.py` aprobó **871 pruebas**, F0 y F1, y publicó tras pasar todos los controles. Hay **82 pruebas nuevas**: 61 fixtures (60 padres afectados y 1013 como control adversarial) y 21 pruebas de comportamiento/contexto. La expectativa antigua de método en 7125 se actualizó explícitamente, manteniendo identidad, texto y longitud. Las pruebas de menciones ahora verifican once anotaciones exactas, sin alterar los avisos.

**59 hashes de entradas/código y 11 de salidas verificados** contra el manifiesto. Ver:

- [Comparación global antes/después](comparacion_loop10_2026-09-08.json).
- [CSV de cambios con textos y hashes](cambios_loop10_2026-09-08.csv).
- [Checkpoint de pendientes y alcance](estado_revision_loop10_2026-09-08.json).

Las verificaciones son locales. El workflow propuesto de GitHub Actions continúa fuera del PR por falta del permiso `workflows`.

## Pendientes y límites

**372 filas alertadas en 339 padres originales**, frente a 391/358 en loop9. Los motivos se superponen:

| Motivo | Filas |
|---|---:|
| Atribución heurística legada | 38 |
| Atribución por anáfora | 42 |
| Final sin puntuación | 253 |
| Fragmento breve | 10 |
| Posible otro hablante o mención | 24 |
| Cargo por verificar | 1 |
| Variante de identidad | 6 |
| Duplicado no fórmula | 3 |
| Escrito leído por tercero | 3 |

La atribución legada baja **58→38**. Aparece un aviso de posible mención adicional, precisamente el de 2325, que queda documentado y no borrado. Duplicados exactos: 608, de ellos 605 procedimentales; los tres no procedimentales permanecen sin deduplicar.

Cola histórica de 783: **170** pendientes de lectura contextual, 58 fórmulas, 267 métodos actualizados, 173 cambios de segmentación/actor por comparación, 91 correcciones dirigidas, siete breves válidos, ocho menciones históricas, seis identidades, dos repeticiones y una continuidad. **190→170 no equivale a 20 lecturas humanas ni cierres semánticos.** Las once menciones actuales se cuentan aparte.

Los cinco candidatos filtrados **780, 3191, 5367, 5647 y 6185** siguen sin adjudicación nueva. No son el total pendiente. El rastreo también dejó candidatos fuera de las alertas: **4954** (opinión después de una cita cerrada, sin límite compatible aún), **4923** (dos opiniones), **6308, 6443 y 6447**. Salvo el pasaje de 4954, estos últimos son triaje y no lectura completa; el checkpoint lo distingue. No se fuerza la segmentación ni se adjudican pasajes conjuntos a una sola persona.

**Sin nuevo cotejo PDF ni muestra humana independiente.** Se revisaron intervalos y contextos pertinentes, no íntegramente todos los padres afectados. Las pruebas, hashes y F0/F1 certifican contratos e integridad, no pureza exhaustiva del corpus. El hallazgo de opiniones sin alerta refuerza la necesidad de revisar también fuera de la cola automática.
