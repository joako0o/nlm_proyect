# LOOP26 — Documentos leídos, voces recuperadas y continuidad de exposiciones

**Base comparada:** `fa5c34c17bc4895ea290307772432d14024551db` (LOOP25).

**Resultado:** nueve padres resegmentados —tres de habla personal y seis de autor/lector documental—, dos continuidades antes pendientes resueltas mediante lectura completa de ambos extremos, dos referencias registradas y una advertencia textual nueva. **1.482 pruebas aprobadas**, F0/F1 sin bloqueos y publicación validada. Sin nuevo cotejo PDF ni muestra independiente.

## 1. Alcance real de lectura

Lectura íntegra de **dieciséis padres**: **3071, 3092, 3575, 4096, 4109, 4143, 4745, 4746, 4778, 5257, 5276, 5308, 5892, 5999, 6561 y 6562**. Se consultaron fechas, cabeceras/nóminas pertinentes y extremos de vecinos como contexto, sin contar esos extractos como lecturas completas adicionales.

El descubrimiento incluyó **49 ventanas de términos documentales**, **90 ventanas nominales con tratamiento** y un barrido de inicios dativos/de opinión que no produjo candidatos. Hay referencias, registros de asistencia, coincidencias nominales imperfectas y casos ya correctamente separados. **Ventanas no equivalen a padres leídos, errores, identidades confirmadas ni una muestra representativa.** El resultado cero de un barrido tampoco demuestra ausencia de mezclas.

**4096** se leyó íntegro como control: sus siete intervenciones ya estaban separadas. «Lectura» allí es interpretación económica, no prueba de un documento de otro autor. No se añade una ficha de mención ni se reasigna una voz por esa palabra.

## 2. Tres intervenciones personales recuperadas

Longitudes de las filas exportadas, incluidos espacios. No se reescribe el texto ni se inventan palabras para convertir la narración en citas directas.

| Padre | Antes → después | Evidencia y límites |
|---|---|---|
| **3092** | Marfán **1409** → Marfán **1272**, Vergara **136** | «Como antecedente, el Consejero señor Rodrigo Vergara cita una encuesta…» es un aporte propio sobre el rechazo de los españoles a los anuncios, no una referencia de Marfán a una intervención anterior. Conservar el **65%**. |
| **4143** | Herrera **715** → Herrera **562**, De Gregorio **152** | «Ajuicio del Presidente…» aporta la interpretación presidencial del QE3. Conservar **Ajuicio** literalmente. Bernanke sigue siendo referencia dentro de Herrera, no nueva voz. |
| **4778** | Marshall **531**, acta **75** → Marshall **312**, Vergara **218**, acta **75** | El Presidente cierra la parte de la reunión; no es Marshall quien lo hace. Se conserva el encabezado incrustado «Sesión N° 184 Página 15 de 26» dentro del intervalo textual, **no como palabras pronunciadas por el Presidente**. La reanudación a las 16:00 sigue siendo institucional. |

Se añaden **tres intervalos personales**, con total **374 en 345 padres**. Los **371 intervalos anteriores permanecen idénticos**. No hay nuevo tipo personal, alias ni expansión global de verbos o expresiones como «cita» o «Ajuicio». Se aplica el mecanismo individual de hash, límites y evidencia.

**CONTEXTO_REVISADO no crea anclas globales.** Una revisión personal no convierte todos los segmentos del padre en texto íntegro ni resuelve sus otros motivos.

## 3. Seis textos de Larraín leídos por el Presidente

Cada padre queda en cuatro partes completas y ordenadas. El primer tramo de **5257** es la excepción institucional explícitamente revisada, no habla presidencial.

| Padre | Primer tramo | Anuncio del lector | Texto de Larraín | Retorno del lector |
|---|---:|---:|---:|---:|
| **3071** | De Gregorio **71** | De Gregorio **217** | **2903** | De Gregorio **115** |
| **3575** | De Gregorio **120** | De Gregorio **181** | **4212** | De Gregorio **149** |
| **4109** | De Gregorio **124** | De Gregorio **181** | **5788** | De Gregorio **149** |
| **5257** | Acta institucional **79** | Vergara **266** | **6205** | Vergara **265** |
| **5892** | Vergara **123** | Vergara **387** | **3606** | Vergara **322** |
| **5999** | Vergara **132** | Vergara **392** | **3441** | Vergara **322** |

**Autor ≠ lector ≠ asistencia.** Se identifica a Larraín como autor del texto leído, no como hablante oral presente. Cerda, donde aparece, es intermediario. La cesión posterior a Vergara o Vial no les adjudica las palabras del lector. Las referencias dentro del documento no lo fragmentan en nuevas voces.

### Procedencia y variantes preservadas

- **3071:** comentarios enviados por intermedio de Cerda; el Presidente anuncia su lectura mediante una cláusula coordinada. **No dice literalmente «por escrito».** No se certifica el formato original del envío. Comilla inicial recta y final curva, ambas conservadas. Retorno «Finalizada la lectura…».
- **3575/4109:** «e informa…» introduce un planteamiento recibido para lectura. **Tampoco dice literalmente «por escrito».** El retorno comienza «Al proseguir con la Reunión…».
- **5257:** Vergara se integra y pasa a presidir la sesión; esta primera oración es acta, no intervención personal. A continuación anuncia el texto recibido **por escrito**. No se infiere presencia del autor.
- **5892:** procedencia **por escrito**, con comilla inicial curva y final recta. No se normalizan los signos para satisfacer el detector.
- **5999:** procedencia **por escrito**, con introducción que nombra explícitamente a Rodrigo Vergara como Presidente lector.

Las modalidades nuevas son **opt-in por ficha**, con hash, partición completa, cita de procedencia y lector compatible:

- `LECTURA_COMENTARIOS_RECIBIDOS_REVISADA` y `LECTURA_COORDINADA_RECIBIDA_REVISADA`: requieren las introducciones completas correspondientes y un antecedente presidencial compatible.
- `LECTURA_NOMINAL_POR_ESCRITO_REVISADA`: exige anuncio presidencial nominal compatible y procedencia escrita explícita.
- `RETORNO_LECTURA_VARIANTE_REVISADA`: cita de retorno exacta y validación del lector; las proyecciones verbales se usan sólo para validar, nunca para exportar palabras distintas.
- `PAR_MIXTO_REVISADO`: sólo los dos pares mixtos observados, con delimitación única y signos literales.
- `INCORPORACION_INSTITUCIONAL_REVISADA`: sólo la primera oración de incorporación documentada en 5257, con actor Consejo, fuente `ACTA/META`, sin ancla personal. **No habilita una conversión genérica de pasajes mixtos como 4055.**

Se rechazan opciones desconocidas, pérdida de opt-in, alteraciones de fuente/citas/límites, comillas incompatibles, lectores incorrectos y conversiones de la incorporación en voz personal. No se amplía la detección documental global por proximidad.

**Doce documentos registrados en total.** Las seis fichas anteriores —5212, 5742, 5802, 4453, 4507 y 4722— permanecen idénticas. Sus registros documentales exportados también, salvo IDs secuenciales. Los esquemas siguen siendo **37/24 columnas**.

## 4. Dos continuidades antes pendientes, ahora leídas completas

No se parte una exposición por cambiar de tema o de padre de origen. Tampoco se permite que cualquier `CONTEXTO_REVISADO` arrastre una voz globalmente.

| Enlace | Extremo anterior → siguiente | Alcance |
|---|---|---|
| **4745→4746** | Lehmann **597 → 1877** | Retoma proyecciones de crecimiento y continúa con el heat map de inflación, TPM y commodities. Soto **494** previo queda fuera del enlace. |
| **6561→6562** | Fuentes **4261 → 875** | Expone mercados emergentes, Rusia y Grecia y continúa con las medidas europeas que explican el menor riesgo griego. Vial **1669** previo queda fuera del enlace. |

Se leyeron íntegros los **cuatro padres**, sin interlocutor intermedio en estos extremos. Se registran ambos enlaces con fechas, hashes, intervalos y fuentes exactas. Las filas físicas y las intervenciones previas de Soto/Vial permanecen separadas. El extremo siguiente conserva su ancla explícita; el extremo revisado anterior **no** se convierte en ancla.

Se conservan «A continuación,.», el encabezado de página en 4746, «7 i» en 6561 y «Quantiative Easing» en 6562. **Resolver la continuidad de voz no certifica integridad del OCR ni permite completar el texto.** No se añade un aviso bloqueante nuevo a esos extremos que anule el enlace revisado. Los validadores siguen rechazando enlaces si aparecen barreras contextuales, cesiones o incompatibilidades.

Total **nueve pruebas de continuidad registradas = siete anteriores intactas + dos nuevas**. Ningún enlace anterior perdido. **5402→5403 no se restablece**. Las dos parejas ya no se presentan como pendientes de lectura en el checkpoint vigente.

## 5. Referencias, daño y pendientes

Dos nuevas lecturas de referencias, sin cambios de filas ni de alertas:

- **5276/441:** Vergara solicita a Lehmann confirmar la composición de la deuda y pide revisar cifras observadas por Claro. Son peticiones y referencias; no se inventan respuestas de los destinatarios.
- **5308/1034:** Vergara toma el análisis de Vial como antecedente y solicita seguimiento de la inversión. No abre un nuevo turno de Vial.

**35 lecturas actuales = 32 menciones legítimas + 3 pendientes: 6185, 3775 y 4055.** Las 33 fichas anteriores permanecen intactas. Los dos controles nuevos, sin alertas, están validados en el registro pero no aparecen en `revision_pendientes.csv`.

**71 advertencias contextuales = 70 anteriores + una nueva**, sin retiros. En el cuerpo documental de **3071/2903** permanecen «constituyó na», «0,1% ensual» y «escenario de onda», indicios de pérdidas de letras. Se advierte el daño sin reconstruirlo, cambiar de autor ni certificar su origen. La advertencia no se aplica al anuncio o al retorno del lector.

Siguen pendientes Bernier/6185, la conclusión posterior a Cerda/3775 y el pasaje conjunto/institucional de 4055. Los archivos de retiros de **6443, 2704 y 2661** no cambian. Tampoco se cierran los problemas de nombres, cargos, variantes de Ricaurte o daño por haber pasado pruebas estructurales.

## 6. Cola visible: +15 filas, no +15 errores

Las filas con alertas pasan de **433 a 448**, en **378 padres** frente a 372.

| Padre | Incremento de filas alertadas | Causa |
|---|---:|---|
| **3071** | +2 | Primer tramo sin puntuación final; documento con aviso de lectura por tercero y daño. Los dos motivos del documento cuentan como **una fila**. |
| **3575** | +4 | Coma del primer tramo, anuncio repetido, aviso documental y retorno repetido. |
| **4109** | +4 | Mismas clases de aviso que 3575. |
| **4507** | +1 | Su primer tramo de 132 caracteres resulta idéntico al nuevo primer tramo de 5999. |
| **5257** | +1 | Aviso documental. |
| **5892** | +1 | Aviso documental. |
| **5999** | +2 | Primer tramo repetido y aviso documental. |

Los anuncios de **3575/4109**, sus retornos y los primeros tramos de **4507/5999** se conservan con aviso de duplicado no fórmula. No se eliminan ni se promueven a fórmulas nuevas. Los retornos de 322 caracteres también se conservan, con la clasificación de fórmula ya existente; no originan un aviso nuevo de duplicado no fórmula.

**4507 sólo cambia indicadores de duplicado/revisión** en el primer tramo. No cambia su texto, atribución, límites o registro documental; no se cuenta como nueva lectura integral.

Las **448 filas alertadas no son 448 errores confirmados ni todo lo que falta leer**. Los motivos se superponen y las divisiones revisadas hacen visibles puntuación, repeticiones y autoría documental antes contenidas en una sola fila.

## 7. Verificación global

| Control | Resultado |
|---|---:|
| Pruebas | **1482**, todas pasan; **48 nuevas** |
| Filas físicas / bloques de texto | **9678 / 9677**, antes 9657 / 9656 |
| Grupos de turno / grupos multifila / máximo de filas | **9258 / 324 / 11**, antes 9239 / 322 / 11 |
| Padres / palabras / sesiones | **7219 / 2048560 / 132**, conservados |
| Intervalos personales anteriores / actuales | **371 / 374** |
| Padres con revisión personal | **345** |
| Advertencias anteriores conservadas / actuales | **70 / 71** |
| Lecturas anteriores conservadas / actuales | **33 / 35** |
| Documentos anteriores conservados / actuales | **6 / 12** |
| Pruebas de enlace anteriores conservadas / actuales | **7 / 9** |
| Nuevos enlaces / enlaces perdidos | **2 / 0** |
| Etiquetas de actor | **55**, sin nuevas identidades ni alias |
| Esquemas / fórmulas revisadas / contrastes TPM | **37/24 / 21 / 310** |
| Hashes de entradas/código y salidas comprobados | **80 / 11** |
| Ensayo aislado frente a publicación | **Idénticos** |

Los **nueve padres corregidos estaban antes sin alertas**. La comparación de todas las columnas salvo `ID` e `ID_Turno` detecta **doce padres con cambios**: nueve resegmentados, dos extremos siguientes con enlace nuevo (**4746/6562**) y **4507** por duplicado. **7207 padres conservan esas celdas**.

Esta última cifra no significa que los grupos de 4745 y 6561 no cambien: sus celdas no secuenciales permanecen iguales, pero ahora comparten grupo con su continuación. Hay **catorce padres alcanzados por correcciones, enlaces o duplicado**; los **7205 restantes** quedan fuera de ese alcance. Los dos controles de referencia y 4096 no cambian celdas ni grupos.

Se compararon también los grupos fuera de correcciones/enlaces, todas las aristas anteriores, las revisiones/advertencias/lecturas/fichas documentales previas, los archivos de retiro, las decisiones TPM y los documentos exportados anteriores salvo IDs. Se mantienen García de once filas, **224→225→226, 3454→3455, 2695→2696, 2754→2755, 2790→2791, 1386→1387, 2673→2674, 2863→2864, 2796→2797, 2707→2708, 2963→2964 y 2680→2681**, así como los siete enlaces revisados anteriores y el retorno explícito de Soto en 4926.

Las 48 pruebas nuevas incluyen dieciséis contratos de fuente/firma/conservación y treinta y dos pruebas de comportamiento: modos documentales individuales, comillas, incorporación institucional, lector, no asistencia, conservación del daño, enlaces exactos, barreras, referencias y pendientes. No se eliminaron controles anteriores para obtener el resultado.

## 8. Histórico y límites

La cola histórica de **783** mantiene sus estados y tipos: **102 pendientes contextuales**, **497 comparaciones**, **183 lecturas dirigidas** y **103 triajes**; **284 intervalos históricos** siguen vinculados a alertas actuales. La variante de identidad permanece en **seis intervalos históricos** y **21 filas actuales**. El estado principal de una ficha no cierra sus motivos independientes.

**Ocho menciones legítimas históricas no equivalen a 32 actuales**: son unidades distintas y superpuestas, no sumables. Las dos continuidades resueltas aquí no cambian por sí mismas los estados de esa cola histórica.

No se afirma revisión exhaustiva del corpus, pureza total de hablante, cotejo nuevo con PDF ni muestreo independiente con y sin alertas. Una exposición larga no está dañada por su extensión. No se confirma el origen de los daños de extracción/OCR sin cotejo.

## Entregables

- `data/processed/consolidado_base_referencia_final.xlsx`: entrega de **9678 filas**.
- `data/processed/consolidado_base_referencia.xlsx`: auditoría de 37 columnas.
- [Comparación global](comparacion_loop26_2026-09-08.json).
- [Cambios por padre y versión](cambios_loop26_2026-09-08.csv).
- [Checkpoint vigente](estado_revision_loop26_2026-09-08.json).
- [LOOP25 anterior](REVISION_LOOP25_2026-09-08.md), conservado como histórico.

Verificaciones locales. El workflow preexistente de GitHub Actions queda fuera del PR; no se afirma ejecución remota. No hay proceso activo.
