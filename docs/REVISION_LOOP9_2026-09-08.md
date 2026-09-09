# Noveno bloque — sujetos, opiniones intercaladas y continuidad

**Estado publicado, 2026-09-08:** 9.427 filas / 391 filas con alertas / **789 pruebas**, F0 y F1 aprobados. Sin proceso activo. Continúa el [PR #3](https://github.com/joako0o/nlm_proyect/pull/3).

Base de comparación: [loop8](REVISION_LOOP8_2026-09-08.md), commit `71947e2d57eead1fc94b72dafabc720c91bd9bd0`: 9.412 filas, 433 alertas, 711 pruebas y 97 revisiones de hablante. Las cifras siguientes son de esta pasada, no acumulaciones de todas las anteriores.

## Resultado y alcance

- **60 padres afectados:** 13 con cambios de segmentación/atribución (**28 → 43 segmentos**, 15 filas nuevas), 47 sólo con cambios de metadatos, conservando sus actores y textos.
- **7.159 padres restantes** sin cambios semánticos en las columnas comparadas; se excluyen los identificadores globales que se renumeran.
- Cuatro intervalos de opinión revisados individualmente, con hash, offsets, citas y justificación: **4706, 4719, 6600 y 6601**. Total: 101 revisiones; las 97 anteriores permanecen intactas.
- Todos los enlaces anteriores preservados; dos enlaces interpadre nuevos comprobados. **314 grupos multipárrafo**, máximo de once filas. No se fragmentan exposiciones porque cambie el párrafo físico.
- 58 hashes de entradas/código y 11 de salidas comprobados contra el manifiesto. La publicación coincide por contenido con el tercer ensayo aislado.

El alcance de lectura no es «60 padres certificados»: se examinaron sujetos/predicados, límites cambiados y contextos pertinentes; las cuatro revisiones acotadas documentan opiniones específicas. Las fixtures congelan resultados comparados, no sustituyen una lectura humana independiente.

## Tres ciclos ejecutados

| Ciclo | Filas | Alertas | Padres estructurales | Sólo metadatos |
|---|---:|---:|---:|---:|
| Base loop8 | 9.412 | 433 | — | — |
| 1: predicados inmediatos | 9.416 | 402 | 3 | 36 |
| 2: concesivas, confirmaciones, bienvenidas | 9.422 | 391 | 10 | 49 |
| 3: cuatro opiniones y retorno expreso | **9.427** | **391** | **13** | **47** |

Los cambios por ciclo se comparan siempre contra loop8, no se suman. En el tercero algunos padres dejan de ser sólo metadatos y pasan a tener cortes reales. **Separar hablantes puede no reducir las alertas:** la mejora del tercer ciclo no modifica el total de 391.

## Cambios de segmentación

### Ocho padres de intercambio/exposición

| Padre | Separación comprobada |
|---|---|
| 2626 | De Gregorio comenta las tasas; Cowan especifica a qué antecedentes corresponde la reducción. |
| 3395 | De Gregorio pregunta → Soto responde → De Gregorio colige → Soto confirma y desarrolla. Se mantiene la continuidad de Soto en 3396. |
| 3982 | De Gregorio estima probable un resultado; «El señor Lehmann lo confirma» es respuesta de Lehmann, no continuación del Presidente. |
| 4096 | Tras la solicitud del Presidente sobre exportaciones de cobre, Soto especifica la corrección y desarrolla la explicación. Se mantienen Cowan, Vergara y los retornos de Soto. |
| 4706 | Marfán plantea un reparo; «A juicio del Consejero señor Joaquín Vial» abre la interpretación de Vial. Su «En su opinión» sigue dentro de esa interpretación. |
| 4719 | Soto se compromete a informar → Marshall opina sobre inflación → Soto retoma su presentación → Cerda consulta → Herrera responde → Soto continúa. La opinión de Marshall no absorbe el retorno ni la exposición larga de Soto. |
| 6600 | Exposición de Fuentes → evaluación cambiaria propia de Claro. La respuesta nominal del padre siguiente y la vuelta de Fuentes en 6602 sostienen los límites. |
| 6601 | Naudon comparte parcialmente la idea de Claro → de Ramón coincide mayormente → García distingue el caso suizo. Claro es referente de las primeras opiniones, no su hablante. |

### Cinco padres procedimentales

**3631, 3702, 3801, 3881 y 4320:** se diferencia la intervención del Presidente, la narrativa institucional de suspensión/reanudación y su bienvenida/cesión de palabra posterior. Los ministros y expositores destinatarios **no** se convierten por ello en hablantes. En 3881 se conserva el bloque narrativo institucional que contiene la suspensión; no se presenta toda descripción de un acto presidencial como discurso oral.

## Reglas y límites

- Predicados finitos inmediatos: comentarios, reflexiones, énfasis, especificaciones, comparaciones y compromisos concretos de informar/analizar/presentar. No se busca indiscriminadamente un verbo de otro sujeto en una ventana de texto.
- «Si bien» admite una concesiva directamente ligada al mismo sujeto. Si sigue otro sujeto o sólo una referencia/presencia, no basta para atribuir habla.
- «Lo confirma», «tiende a compartir/coincidir», «suscribe plenamente» y «da la bienvenida» reconocen actos explícitos; una bienvenida no atribuye discurso al invitado.
- «Al continuar con su presentación» exige sujeto y predicado expreso para recuperar el retorno de Soto. No es una regla de herencia ciega.
- OCR `tam bién`: se normaliza únicamente en la vista de reconocimiento; el Excel conserva la grafía literal.
- Dar por finalizada/concluida la sesión impide propagar continuidad **hacia el párrafo siguiente**. Puede formar parte del cierre del turno anterior del mismo Presidente.
- **No se agregó una regla global de «En opinión» / «A juicio».** Las cuatro opiniones dependen de sus revisiones individuales y sus intervalos exactos.

Los 47 cambios sólo de metadatos incluyen el ajuste de antecedente en **3396**, el nuevo enlace en **3983** y la identificación más específica del método en **3434**. No son 47 cambios de identidad ni 47 lecturas completas certificadas.

## Continuidad y conservación

Nuevos enlaces: **3108 → 3109, De Gregorio**, y **3982 → 3983, Lehmann**. El primero enlaza el comentario previo con el cierre presidencial; la nueva barrera impide heredar después del cierre. El segundo enlaza la confirmación con la continuación explícita de Lehmann.

La comparación verifica:

1. Reconstrucción de los **7.219 textos**, ignorando exclusivamente espacios; **2.048.560 palabras** conservadas.
2. Actores/textos idénticos en los 47 padres de metadatos; columnas estables iguales en los otros 7.159.
3. Todos los enlaces interpadre previos y grupos no afectados conservados; exposiciones de García de once filas intactas.
4. Original XLSX intacto; 132 sesiones, 51 etiquetas de actor/50 personas y 310 contrastes TPM.
5. Tres documentos de Larraín leídos por Vergara intactos en su estructura: autor ≠ lector, naturaleza escrita, sin inferir asistencia ni habla oral del autor. Continúan los esquemas XLSX de **37/24 columnas** y `documentos_leidos.csv`.
6. Diez menciones actuales, 21 fórmulas revisadas y la advertencia acotada de cargo en 4433 preservadas. Las revisiones contextuales no crean anclas por sí solas.

## Pruebas y publicación

Se ejecutó `python scripts/preparar_data.py`: reconstrucción de textos, suite completa, construcción en staging, exportación, F0, F1 y publicación sólo tras aprobar todos los controles. **789 pruebas aprobadas**: 78 nuevas (60 fixtures y 18 pruebas de comportamiento/contexto).

Se actualizaron dos expectativas antiguas de forma explícita:

- 5243: misma identidad/texto de Marshall, método ahora de sujeto explícito gracias a «si bien admite».
- 3421/3476 sin curación: la bienvenida explícita ya se reconoce; eso no certifica el agradecimiento anafórico anterior de 3421. Su tramo completo sigue necesitando la revisión existente. Los resultados publicados de ambos padres permanecen iguales a loop8.

La comprobación global adicional verificó los 58 hashes de entradas/código y los 11 de salidas y produjo:

- [Comparación global antes/después](comparacion_loop9_2026-09-08.json).
- [CSV de los cambios con texto actual y hash del padre](cambios_loop9_2026-09-08.csv).
- [Checkpoint de alcance y pendientes](estado_revision_loop9_2026-09-08.json).

GitHub Actions no se declara ejecutado: el workflow local propuesto continúa fuera del PR por falta de permiso `workflows`.

## Lo que permanece abierto

**391 filas alertadas en 358 padres originales.** Motivos superpuestos:

| Motivo | Filas |
|---|---:|
| Atribución heurística legada | 58 |
| Atribución por anáfora | 42 |
| Final sin puntuación | 253 |
| Fragmento breve | 10 |
| Posible otro hablante o mención | 23 |
| Cargo en discurso por verificar | 1 |
| Variante de identidad | 6 |
| Duplicado no fórmula | 3 |
| Escrito leído por tercero | 3 |

Frente a loop8: **433 → 391** alertas; atribución legada **104 → 58**. Se conserva una alerta nueva de brevedad por la confirmación de Lehmann y una de final sin puntuación por un límite ahora separado. No se añade puntuación ni se ocultan los avisos para mejorar las cifras. Duplicados exactos 607, de ellos 604 procedimentales: una bienvenida recién separada coincide literalmente con otra; los tres no procedimentales siguen sin deduplicarse.

Cola histórica de 783 intervalos: **190** pendientes de lectura contextual, 58 fórmulas reclasificadas, 249 métodos actualizados, 173 cambios de segmentación/actor por comparación, 89 correcciones dirigidas, siete breves válidos, ocho menciones históricas, seis identidades, dos repeticiones y una continuidad. **232 → 190 no equivale a 42 lecturas humanas ni cierres semánticos.** La clasificación también cambia cuando un intervalo antes procedimental obtiene ahora una intervención personal explícita.

Siguen los cinco candidatos filtrados **780, 3191, 5367, 5647 y 6185**; no representan el total pendiente. En esta pasada se releyeron 3190–3192 y 5646–5648 sin adjudicar todo el pasaje: 3191 incluye una coincidencia conjunta del Presidente y Soto, y 5647 exige acotar el compromiso de Lehmann y las anáforas posteriores. No se asignan intervenciones conjuntas a una persona por conveniencia. Se conservan los demás residuos identificados en el checkpoint anterior, incluido 4433.

**Sin nuevo cotejo PDF y sin muestra semántica/humana independiente. F0/F1 verifican integridad y contratos, no pureza exhaustiva de hablante.**
