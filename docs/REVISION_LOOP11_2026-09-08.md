# Undécimo bloque — varios intervalos, citas cerradas e identidades pendientes

**Publicado, 2026-09-08: 9.489 filas / 368 filas con alertas / 930 pruebas; F0 y F1 aprobados.** Sin proceso activo. Continúa el [PR #3](https://github.com/joako0o/nlm_proyect/pull/3).

Comparación contra [loop10](REVISION_LOOP10_2026-09-08.md), commit `d304becb929442e12250ccb16593664bdac76721`: 9.466 filas, 372 alertas, 871 pruebas y 138 intervalos revisados en 138 padres.

## Resultado y alcance

- **29 padres afectados:** **19 estructurales** (43 → 66 segmentos, **23 filas adicionales**) y **10 sólo metadatos**, sin cambiar sus textos ni actores.
- **22 intervalos de hablante nuevos en 20 padres.** Ahora hay **160 intervalos en 158 padres**: 2622 y 4923 contienen dos revisiones independientes cada uno. Las 138 entradas anteriores permanecen intactas.
- **7.190 padres restantes** sin cambios en las columnas semánticas comparadas; se excluyen los IDs globales renumerados.
- Todos los enlaces de continuidad anteriores y los grupos no afectados conservados; no se añadieron ni retiraron enlaces. **313 grupos multipárrafo**, máximo de once filas.
- Nueva advertencia acotada en **6443**: mezcla de intervenciones con identidad de Ricaurte pendiente. No se presenta su actor provisional como atribución validada de todo el bloque.

Se leyeron los intervalos intervenidos y contextos pertinentes, no íntegramente los 29 padres ni todo el corpus. En particular, la advertencia de 6443 procede de la lectura del inicio y de sus transiciones: **no certifica lectura completa de sus 15.100 caracteres**.

## Dos ciclos comparados

| Ciclo | Filas | Alertas | Padres estructurales | Sólo metadatos |
|---|---:|---:|---:|---:|
| Base loop10 | 9.466 | 372 | — | — |
| 1: revisiones múltiples, cita cerrada y variantes de cargo | 9.489 | 367 | 19 | 9 |
| 2: hacer visible y bloquear el caso 6443 | **9.489** | **368** | **19** | **10** |

Cada ciclo se compara con loop10. El aumento de una alerta en el segundo ciclo es deliberado: muestra un problema que antes quedaba oculto, no un empeoramiento de integridad ni una atribución forzada.

## Cambios principales

### Varios intervalos en el mismo padre

- **4923:** Soto presenta masa salarial → Vergara interpreta el crecimiento real → Marshall pide contrastar la variación nominal. Las dos opiniones tienen actores, límites, citas e identificadores propios.
- **2622:** se separa la opinión de De Gregorio dentro del tramo de Marshall y, más adelante, el agregado de Soto dentro de una respuesta de García. Se conserva el OCR `Anális is` y la coordinación sólo se divide por su revisión individual. Resultado: Marshall → De Gregorio → Soto → De Gregorio → García → Soto.

### Opinión después de una cita cerrada

**4954:** Marfán pregunta qué mide la encuesta → Soto cita «¿Qué va a hacer el Banco Central de Chile?» → Marfán explica qué debería reflejar esa encuesta. La cita se mantiene con Soto. La nueva excepción exige una revisión específica, cierre de cita y puntuación, y un sujeto nominal compatible con el actor revisado. **No se dividen automáticamente todas las citas ni todas las fórmulas de opinión.**

### Otras opiniones y retornos

| Padres | Límite revisado |
|---|---|
| 2635 | De Gregorio interpreta la respuesta de García sobre proyecciones y mercado. |
| 2776 | Desormeaux evalúa datos y riesgos después de Magendzo, antes de la intervención de Velasco. |
| 3173 | Marfán distingue el impacto único del impuesto y la estrategia de mediano plazo, después de Soto. |
| 3310 | García interpreta el perfil de la demanda; Soto retoma explícitamente el mercado laboral. |
| 4437 | Orellana explica ajustes de inventarios; Soto vuelve al supuesto de existencias. |
| 4665 | Herrera aporta el contrafactual de financiamiento después de Cowan. |
| 6060 | Lehmann responde a Vergara sobre la apreciación del euro. |
| 6308 | Vergara inicia su balance internacional antes de la cesión de palabra que ya se reconocía; no se prolonga sobre él la intervención de García. |
| 6447 | García aporta su análisis de inflación y demanda global después de Vial. |
| 7063 | Valdés, como Ministro, contrapone su interpretación de tasas largas al final de la exposición de Gianelli. |
| 7066 | De Ramón responde a García sobre CDS y contagio brasileño. |

### Cargo expreso y lectura contextual

La vista de reconocimiento admite `Gerente de División de Estudios`, `Interino`, el inicio OCR `A l respecto` y la variante `Gerente de Anális is Macroeconómico`. **No reescribe el texto exportado.** Sigue exigiendo sujeto/predicado y rechazando citas o presencia sin intervención.

Esto recupera cinco intercambios adicionales en **641, 2664, 2670, 2671 y 2674**, con respuestas de Valdés/García antes absorbidas por Marfán, el Presidente, Soto o Magendzo. En 2674 se conserva íntegra la revisión de Marshall del bloque anterior y los retornos de Soto.

Se documentaron también seis intervalos antes atribuidos por método legado: **14, 2220, 2703, 3262, 4297 y 6505**, sin cambiar sus actores/textos. En 14, la relativa sobre Herrera sigue sin poder prestar su verbo a Jadresic: la confianza adicional proviene de la lectura registrada, no de retirar la guardia general. En 6505 se mantiene literalmente `precede a responder`. En 178 el método pasa a anáfora local y **conserva una alerta de atribución**; no se presenta como sujeto resuelto sin incertidumbre.

## Evolución del registro y controles

[revisiones_hablantes.json](../data/curation/revisiones_hablantes.json) mantiene una entrada principal por padre. Opcionalmente admite `Revisiones_Adicionales`, una lista de entradas completas con el mismo padre/fecha/hash y **su propio** `Revision_ID`, actor, `Inicio`, `Fin`, cita, justificación y evidencia.

- Compatibilidad con las entradas individuales anteriores.
- Rechazo de IDs duplicados, intervalos solapados/desordenados, hash/fecha/padre distintos y anidación adicional.
- F1 comprueba por separado cada intervalo, su inicio en el texto reconstruido y su extensión exacta. Detecta omisiones, desplazamientos y atribución excesiva.
- El Excel anota el identificador **del intervalo aplicable**, no siempre el identificador principal del padre. Se comprobó también para los dos identificadores secundarios.
- El seguimiento histórico puede reconocer una revisión secundaria sin declarar puro todo el intervalo original.
- Ninguna revisión contextual crea por sí sola un ancla de continuidad.

El tipo `OPINION_TRAS_CITA_CERRADA_REVISADA` se usa en 4954 únicamente con decisión individual. No agrega un detector global de opiniones ni un corte general por comillas.

## 6443: advertencia, no solución ficticia

El bloque de **15.100 caracteres** comienza con de Ramón, incluye «En opinión del Consejero señor Pablo García» y después «El señor Miguel Ricaurte retoma su presentación». La atribución del bloque completo a de Ramón **no está validada**. El catálogo contiene dos identidades para el alias Ricaurte, y esta pasada no las fusiona ni elige una por proximidad o tema.

Se registra `HABLANTES_POR_IDENTIDAD_PENDIENTE` mediante [alertas_contextuales.json](../data/curation/alertas_contextuales.json), con texto, hash y alcance exactos. La alerta se exporta, no desaparece de la cola y bloquea la propagación de continuidad. Si cambian el actor o el intervalo, la validación exige revisar la advertencia de nuevo.

Se mantiene asimismo la advertencia de **cargo** en 4433, sin trasladar por tema a Soto los 705 caracteres provisionales de Lehmann. Son **dos advertencias contextuales distintas**, no dos identidades resueltas.

## Validación publicada

`python scripts/preparar_data.py` ejecutó reconstrucción, **930 pruebas**, construcción aislada, exportación, F0/F1 y publicación. **59 pruebas nuevas**: 29 fixtures de padres afectados y 30 pruebas de comportamiento/validación.

Las expectativas antiguas se ajustaron sólo donde había cambios comprobados: el método revisado de 14, la respuesta de García en 2674 y el inicio anterior de Vergara en 6308. Las pruebas de 4954/4923 ahora verifican sus revisiones aplicadas; las de pasajes conjuntos e identidades pendientes siguen exigiendo abstención.

Comparación global adicional:

- Los **7.219 textos** se reconstruyen ignorando sólo espacios; **2.048.560 palabras** conservadas.
- Actores/textos idénticos en los diez padres de metadatos; columnas estables iguales en los otros 7.190.
- Todos los enlaces y grupos no afectados conservados, incluidas las exposiciones de García de once filas.
- Original XLSX intacto; 132 sesiones, 51 etiquetas de actor/50 personas, 310 contrastes TPM y esquemas **37/24 columnas**.
- Tres escritos de Larraín leídos por Vergara conservan autor ≠ lector, naturaleza escrita y ausencia de inferencia de asistencia/habla oral. Continúa `documentos_leidos.csv`.
- Once menciones actuales y 21 fórmulas revisadas intactas; las tres repeticiones sustantivas no se deduplican.
- Base publicada equivalente por contenido al ensayo 2. **60 hashes de entradas/código y 11 de salidas verificados.**

Entregables de auditoría: [comparación global](comparacion_loop11_2026-09-08.json), [CSV de cambios](cambios_loop11_2026-09-08.csv) y [checkpoint](estado_revision_loop11_2026-09-08.json).

## Pendientes y límites

**368 filas alertadas en 334 padres**, frente a 372/339 en loop10. Motivos superpuestos: 29 atribuciones legadas, 43 anáforas, 256 finales sin puntuación, diez fragmentos breves, 24 posibles otros hablantes/menciones, seis variantes de identidad, tres duplicados no fórmula, tres escritos leídos, una advertencia de cargo y una de hablantes por identidad pendiente. Los nuevos límites pueden generar avisos de puntuación; no se agrega puntuación a la fuente para eliminarlos.

Cola histórica de 783: **163** pendientes de lectura contextual, 58 fórmulas, 274 métodos actualizados, 171 cambios por comparación, 93 correcciones dirigidas, siete breves válidos, ocho menciones históricas, seis identidades, dos repeticiones y una continuidad. **170→163 no equivale a siete lecturas humanas ni cierres semánticos.** Las once menciones actuales se cuentan aparte.

Los cinco candidatos filtrados **780, 3191, 5367, 5647 y 6185** continúan pendientes. 4923, 4954, 6308 y 6447, señalados antes fuera de alertas, tienen ahora revisiones aplicadas; 6443 pasó a advertencia visible, **no a resuelto**. No se adjudican pasajes conjuntos a una sola persona. Estos candidatos no son el total de trabajo restante.

**Sin nuevo cotejo PDF ni muestra humana independiente.** Las verificaciones de integridad no certifican pureza exhaustiva del corpus. GitHub Actions no se declara ejecutado: el workflow propuesto continúa fuera del PR por falta del permiso `workflows`.
