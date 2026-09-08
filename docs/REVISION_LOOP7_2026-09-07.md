# Séptimo bloque: autor/lector, atribuciones heredadas y retornos

**Fecha:** 2026-09-07 · **PR:** [#3](https://github.com/joako0o/nlm_proyect/pull/3)

Pasada terminada y publicada. Se encadenaron cuatro ciclos, pruebas y comparación global. **No queda un proceso de revisión ejecutándose en segundo plano.**

## Resultado y alcance

| Indicador | Loop6 | Loop7 |
|---|---:|---:|
| Filas físicas de Excel | 9.353 | **9.405** |
| Bloques de texto | 9.352 | **9.404** |
| Filas con alertas | 580 | **508** |
| Pruebas de regresión | 432 | **582** |
| Revisiones de hablantes con citas/hash | 91 | **96** |
| Revisiones de documentos leídos por tercero | 0 | **3** |
| Fórmulas exactas revisadas | 18 | **21** |
| Anotaciones de menciones actuales | 10 | **10** |
| Intervalos originales pendientes de lectura contextual | 388 | **305** |
| Candidatos prioritarios sin anotación de mención | 8 | **5** |

**118 padres presentan cambios:**

- **45 con cambios de segmentación o atribución:** 53 → 105 segmentos, **52 filas adicionales**. Incluyen tres documentos escritos, nueve intercambios y 33 padres con cesiones al escenario interno.
- **73 sólo con cambios de metadatos:** conservan texto, actor y límites. Principalmente se sustituye una atribución heurística por reconocimiento del sujeto expreso; también se actualiza una fórmula repetida y la continuidad de una presentación. No son 73 errores de identidad corregidos.
- **7.101 padres restantes sin cambios semánticos**, salvo desplazamiento de los IDs consecutivos de fila/turno provocado por la nueva segmentación.

Se conservaron los caracteres de los **7.219 padres** —omitiendo sólo espacios en la comparación—, las **2.048.560 palabras**, las 132 sesiones y las 51 etiquetas de actor. Los esquemas principales siguen siendo de **37 columnas de auditoría y 24 finales**. La celda mayor tiene 31.948 caracteres y la fracción física de una intervención larga permanece intacta.

Los controles **F0 y F1 pasan sin errores bloqueantes**. Esto **no certifica pureza semántica, cotejo PDF ni revisión humana independiente**. Una mejora de método o una reducción de alertas no equivale a cerrar la revisión contextual del texto completo.

## Cuatro ciclos encadenados

| Ciclo aislado | Trabajo | Filas | Alertas |
|---|---|---:|---:|
| 1 | Modelo explícito de autor y lector en tres escritos | 9.362 | 582 |
| 2 | Predicados directos omitidos por el detector; retornos e intercambios | 9.368 | 517 |
| 3 | Cesión al escenario interno y sujeto con «en tanto» | 9.397 | 536 |
| 4 | Cinco revisiones acotadas, variantes de cesión y tres fórmulas exactas | **9.405** | **508** |

Los valores intermedios no son versiones finales ni certificados: por ejemplo, la tercera tanda hizo visibles repeticiones de cesiones y límites aún no adjudicados. La cuarta revisó esos textos exactos, sin declarar fórmula cualquier discurso que contenga una cesión. La publicación final se hizo con `python scripts/preparar_data.py`, que ejecutó las 582 pruebas y F0/F1 antes de sustituir las salidas.

## 1. Tres opiniones escritas: autor, lector y asistencia son cosas distintas

Se aplicaron las propuestas documentadas en el [loop6](propuestas_documentales_loop6_2026-09-07.json), ahora con un modelo y validación explícitos. El archivo anterior conserva su condición de propuesta histórica; las instrucciones vigentes están en [revisiones_documentos_leidos.json](../data/curation/revisiones_documentos_leidos.json).

Cada padre se divide en cuatro tramos:

1. Luis Óscar Herrera concluye su exposición.
2. Rodrigo Vergara informa que recibió un escrito y anuncia su lectura.
3. **Felipe Larraín es el autor del escrito; Rodrigo Vergara es quien lo lee.**
4. Vergara termina la lectura y retoma la conducción, ofreciendo la palabra a Joaquín Vial. Esa cesión no se atribuye a Vial.

| Padre | Fecha | Límites completos sobre el texto original | Longitud del escrito |
|---|---|---|---:|
| 5212 | 2012-11-13 | 0, 230, 470, 6509, 6760 | 6.039 |
| 5742 | 2013-08-13 | 0, 499, 866, 5774, 6097 | 4.908 |
| 5802 | 2013-09-12 | 0, 546, 928, 6022, 6345 | 5.094 |

Los límites usan offsets de Python, con fin exclusivo. El escrito conserva las comillas exteriores y su texto íntegro; no se divide por nombres citados dentro de él. También se conserva el daño `( ■` en la introducción de 5802.

La fila escrita tiene:

- `Actor_Final = Felipe Larraín Bascuñán` y `Fuente_Actor = DOCUMENTO_ESCRITO_REVISADO`.
- `Tipo_Acta = OPINION_ESCRITA`, no acuerdo institucional ni turno oral del Ministro.
- Cargo `Ministro de Hacienda` con `Fuente_Rol = CARGO_DOCUMENTAL_REVISADO`.
- **`Rol_Lista_Asistencia` vacío**: recibir o leer un escrito no acredita presencia del autor.
- Relación `DOCUMENTO_PERSONAL`, sin ancla ni antecedente que propague ese escrito como habla oral.
- Aviso obligatorio `TEXTO_ESCRITO_LEIDO_POR_TERCERO`.

Las introducciones y retornos usan `LECTOR_DOCUMENTO_REVISADO`. El nuevo [documentos_leidos.csv](../data/processed/documentos_leidos.csv) enlaza autor, lector, cargos, IDs, límites, hash y no inferencia de asistencia. Además, [turnos_habla.csv](../data/processed/turnos_habla.csv) añade `Naturaleza_Turno` y `Lector_Documento`: **sus grupos no son todos habla oral**, incluso al consultar ese archivo sin el Excel.

La carga rechaza cambios de texto/hash, fecha, partición, comillas, evidencia de autoría o lector incompatible. F1 exige que sobrevivan los cuatro tramos, su semántica documental y el aviso. No se reemplaza silenciosamente la autoría por la identidad de quien lee.

## 2. Predicados explícitos y exposiciones que continúan

Se leyeron los 64 tramos candidatos de la familia «alude», «corrobora», «resume», «hace el alcance» y «llama la atención», además de los nuevos cambios que mostró el ensayo global, como 3930. Estos verbos requieren un sujeto directamente vinculado al predicado: no se buscan a distancia para justificar cualquier nombre cercano.

También se admite el inciso acotado «en tanto» entre sujeto y verbo, sin convertirlo en una autorización para atravesar otra cláusula. Se conservaron las defensas frente a citas, destinatarios, sustantivos como «la opinión del…» y referencias a terceros.

### Nueve intercambios corregidos

| Padre | Secuencia resultante | Protección relevante |
|---|---|---|
| 2668 | De Gregorio → Pablo García → Claudio Soto | García comenta el patrón histórico como Gerente de División Estudios; su cargo/nombre constan en 2656 y 2680. Soto conserva 2.239 caracteres. |
| 3298 | Manuel Marfán → Claudio Soto | La llamada de atención del Gerente de Análisis Macroeconómico no pertenece al Vicepresidente. |
| 3315 | Ricardo Vicuña → Claudio Soto | Soto comienza en «El señor Claudia Soto, en tanto, agrega…», no en su posterior «alude». Se preserva «Claudia» literalmente y su tramo de 1.239 caracteres. |
| 4415 | Sebastián Claro → Sergio Lehmann | Opinión de Lehmann delimitada y revisada; no regla global sobre toda aparición de «En opinión de…». |
| 4801 | Enrique Marshall → Rodrigo Vergara → Marshall | Se separan los datos del BIS que introduce Vergara y la respuesta de Marshall. |
| 5079 | Manuel Marfán → Sergio Lehmann | Lehmann corrobora el compromiso de la Reserva Federal. La mención a Marfán no es un nuevo turno. |
| 5113 | Sergio Lehmann → Rodrigo Cerda → Lehmann | El retorno de Lehmann conserva 2.772 caracteres de la exposición de commodities. |
| 5412 | Sebastián Claro → Enrique Marshall | La evaluación de Marshall y su enumeración quedan en un tramo de 509 caracteres. |
| 6607 | Miguel Fuentes → Joaquín Vial → Fuentes | Vial ocupa 278 caracteres; el retorno de Fuentes comienza en «alude también» y conserva 4.103 caracteres, sin esperar a la siguiente sección temática. |

Las cinco entradas nuevas de [revisiones_hablantes.json](../data/curation/revisiones_hablantes.json) son **2668, 4415, 5286, 5360 y 5412**. Las dos últimas resuelven daños que impedían reconocer la cesión; las otras tres delimitan los intercambios indicados. Las 91 entradas anteriores permanecen intactas. `CONTEXTO_REVISADO` sigue sin crear un ancla de continuidad por sí solo.

## 3. Cesiones al escenario interno y repeticiones

La familia literal principal aparece en **40 padres, con 41 ocurrencias**: «No habiendo más consultas ni comentarios en lo concerniente al escenario internacional…». Se revisaron sus límites y variantes, no se certificó íntegramente cada exposición larga anterior.

Se incorporó la locución «da paso a la exposición» con prefijos completos y acotados. El Presidente sigue siendo quien cede el paso; Soto/Fuentes son destinatarios hasta que su exposición comienza efectivamente.

Los **33 padres con cambios estructurales de esta familia y sus variantes** son:

`4820, 4990, 5065, 5122, 5178, 5243, 5286, 5360, 5534, 5589, 5662, 5717, 5777, 5827, 5870, 5976, 6026, 6080, 6132, 6192, 6308, 6355, 6404, 6491, 6530, 6715, 6829, 6884, 6926, 7003, 7071, 7125, 7179`.

Casos especialmente protegidos:

- **5717:** Soto → Vergara → Soto, de 895 / 237 / 2.954 caracteres. La cesión intercalada no absorbe la presentación efectiva posterior.
- **5286:** se conservan `/y` y la `i` final del tramo de Lehmann; sólo la revisión con hash permite el corte tras el daño.
- **5360:** se conserva el rótulo espaciado `B A N C O C E N T R A L D E C H I L E` antes de la cesión. No se limpia el OCR.
- **5976:** se conserva `en io concerniente`; sólo la vista de reconocimiento acepta esa variante acotada.
- **6926:** las dos repeticiones consecutivas de la cesión permanecen en los 341 caracteres del tramo del Presidente. No se elimina ninguna.
- **7179:** Claro → Mario Marcel → Vergara; la cesión no queda dentro del comentario de Marcel.

Se añadieron **tres fórmulas completas y exactas** en [formulas_revisadas.json](../data/curation/formulas_revisadas.json), correspondientes a cesiones hacia Soto, hacia Fuentes y sin destinatario nominal. Su coincidencia permite sólo diferencias de espacios. Añadir una recomendación de tasa o un discurso anterior impide la coincidencia revisada del texto entero; no se suprimen alertas por una mera subcadena.

La heurística procedimental histórica continúa existiendo y no se declara resuelta su revisión general en este bloque.

## 4. Continuidad y comparación global

Se conservaron **todos los enlaces entre padres preexistentes**, incluidos los 18 comprobados expresamente en bloques anteriores:

`3966→3967, 3221→3222, 2785→2786, 2566→2567, 2408→2409, 2883→2884, 3017→3018, 3073→3074, 3122→3123, 3273→3274, 3340→3341, 3428→3429, 3429→3430, 3488→3489, 3637→3638, 6564→6565, 3812→3813, 3810→3811`.

Sólo se añadieron **5994→5995 y 5995→5996**, después de leer la presentación de opciones de Herrera y su conclusión. El reconocimiento de «alude» permite mantener ese desarrollo como una exposición continua. No se generalizó el anclaje de las revisiones contextuales.

En los documentos escritos, **5211→5212, 5741→5742 y 5801→5802** siguen enlazando la exposición de Herrera con su conclusión inicial; ya no arrastran el escrito de Larraín dentro de esa conclusión. Los cuatro tramos de cada padre pertenecen a cuatro grupos distintos.

Permanecen **301 grupos multipárrafo**, con un máximo de once filas, incluidas las exposiciones de Pablo García en 60–70 y 142–152. La composición de los grupos no alcanzados por cambios se comparó por padre/texto/actor, no por el ID de turno desplazado.

La validación final comprobó:

- Igualdad del contenido de la hoja consolidada publicada con el cuarto ensayo aislado.
- Conservación de texto, campos semánticos fuera de los 118 padres y todos los enlaces anteriores.
- Integridad de las diez anotaciones actuales de menciones y de las revisiones anteriores.
- Correspondencia del CSV documental con la naturaleza y lector de sus grupos.
- **54 hashes de entradas/código y 11 de salidas**, contra los archivos publicados.
- Libro original sin cambios y 310 fórmulas TPM contrastadas sin errores.

## Alertas y seguimiento: sin cierre masivo

| Motivo actual, con solapamientos | Filas |
|---|---:|
| Atribución heurística legada | 182 |
| Final sin puntuación | 252 |
| Posible otro hablante o mención | 23 |
| Atribución por anáfora | 42 |
| Fragmento breve | 9 |
| Variante de identidad | 6 |
| Duplicado no fórmula | 3 |
| Texto escrito leído por tercero | 3 |

Los duplicados exactos pasan de 576 a **606**, de los que **603** son fórmula. Los otros tres corresponden a **5212, 5256 y 5385**: se conservan las recomendaciones sustantivas repetidas. El corte documental hizo visible la coincidencia de la conclusión de Herrera en 5212; no se ocultó para mejorar el contador.

En el seguimiento de las 783 originales quedan **305 pendientes**, 59 fórmulas, 140 métodos actualizados, 169 intervalos con modificación detectada por comparación, 86 correcciones dirigidas, siete breves válidos, ocho menciones históricas, seis identidades, dos repeticiones sustantivas históricas y una continuidad. **163** estados se clasifican como lectura dirigida, **309** como comparación automática y **311** como triaje. **479 intervalos originales** aún se solapan con alertas actuales.

El paso de 388 a 305 pendientes de ese seguimiento incluye cambios automáticos de método; **no representa 83 lecturas humanas ni 83 casos certificados**. Las diez anotaciones de menciones actuales se cuentan aparte y mantienen sus advertencias.

## Pendientes que no se adjudicaron

Los cinco candidatos prioritarios filtrados son **780, 3191, 5367, 5647 y 6185**, no el total del trabajo pendiente:

- **780:** frontera entre De Gregorio y Corbo dañada/incompleta. El acceso al original había quedado bloqueado por verificación del repositorio; no se obtuvo un nuevo PDF en esta pasada.
- **3191:** Marshall, Claro, coincidencia conjunta del Presidente/Soto y García. No se asigna la intervención conjunta a una sola persona.
- **5367:** exposición de Fuentes, petición de los Consejeros, Herrera, Fuentes y opinión de Claro. Necesita varios límites y representación adecuada de la petición colectiva.
- **5647:** compromiso de Lehmann incrustado en la intervención del Presidente, seguido de una continuación sin sujeto explícito. No se adjudica todo el resto por proximidad.
- **6185:** se leyó el texto completo de **20.118 caracteres**, junto al cierre de 6184 y la cesión de 6186. «Conforme señala… Matías Bernier» puede ser referencia o confirmación intercalada; no permite trasladar la exposición posterior de commodities a Bernier ni cerrar la alerta como mención segura. Se conserva la exposición de Lehmann sin cortes nuevos.

Continúan los otros casos conjuntos/pasivos, daños, variantes de identidad y repeticiones del checkpoint anterior. No se hizo revisión independiente de una muestra con y sin alertas. **No hubo nuevo cotejo PDF ni certificación exhaustiva.**

## Archivos y reproducción

- [Excel final](../data/processed/consolidado_base_referencia_final.xlsx) y [auditoría](../data/processed/consolidado_base_referencia.xlsx).
- [Autor/lector de documentos](../data/processed/documentos_leidos.csv).
- [Cambios por padre y segmento](cambios_loop7_2026-09-07.csv).
- [Comparación completa antes/después](comparacion_loop7_2026-09-07.json).
- [Checkpoint y pendientes](estado_revision_loop7_2026-09-07.json).
- [QA](../data/processed/qa_preparacion.json), [manifiesto](../data/processed/manifiesto_preparacion.json) y [cola actual](../data/processed/revision_pendientes.csv).
- [Pruebas documentales](../tests/test_document_reviews.py) y [regresiones del bloque](../tests/test_loop7_review.py), con 115 fixtures de padres además de los documentos y controles negativos.

```bash
python scripts/preparar_data.py
```

Las verificaciones son locales. El workflow de Actions continúa excluido del PR por falta del permiso `workflows` en la conexión; no se informa una ejecución remota inexistente.
