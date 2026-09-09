# LOOP17 — Diálogos sin alerta y recuperación de Gloria Peña

**2026-09-08 · [PR #3](https://github.com/joako0o/nlm_proyect/pull/3)**

Base: `af85daba1076177472ed510703edd9444f42cd09`, [LOOP16](REVISION_LOOP16_2026-09-08.md).
Lectura dirigida por agente del texto disponible y de las nóminas pertinentes. **Sin nuevo cotejo PDF ni muestra independiente.**

## Resultado publicado

| Medida | Antes | Ahora |
|---|---:|---:|
| Filas físicas | 9.504 | **9.525** |
| Bloques de texto | 9.503 | 9.524 |
| Grupos de turno | 9.093 | 9.114 |
| Grupos multifila / máximo de filas | 315 / 11 | 315 / 11 |
| Filas con alertas / padres alertados | 322 / 288 | **334 / 297** |
| Pruebas | 1.129 | **1.155** |
| Intervalos revisados / padres con revisión | 234 / 225 | **250 / 237** |
| Advertencias contextuales activas | 24 | 26 |
| Etiquetas nominales de actor | 50 | 51 |

**Doce padres con separación estructural, dieciséis intervalos nuevos y 21 filas adicionales.** Se leyó íntegro el texto disponible de los doce padres, sin cortar las exposiciones por países, indicadores o párrafos. Once de esos padres no tenían alerta antes de esta pasada; 6443 sí estaba advertido. No se interpreta cada mención como una intervención.

Los otros **7.207 padres** conservan todos sus campos semánticos, descontando identificadores secuenciales. No hay cambios adicionales de atribución, cargo o alertas fuera de los doce padres.

- [Comparación global antes/después](comparacion_loop17_2026-09-08.json)
- [Detalle de filas, texto y hashes](cambios_loop17_2026-09-08.csv)
- [Checkpoint y pendientes](estado_revision_loop17_2026-09-08.json)

## 1. Continuación del diálogo de Ricaurte, febrero de 2014

El hallazgo de 6009 en LOOP16 motivó revisar la continuación. La nómina del padre **6008** identifica a **Miguel Ricaurte Bermúdez**, Gerente de Análisis Internacional Subrogante. Se emplea esa etiqueta **sólo como atribución nominal local**, sin resolver la equivalencia global Bermúdez/Vintimilla.

| Padre | Secuencia resultante; caracteres por tramo |
|---|---|
| 6013 | Vergara **283** → Ricaurte **4.473** |
| 6014 | Pablo García **409** → Ricaurte **172** |
| 6015 | Vergara **112** → Ricaurte **562** → Vergara **170** → Ricaurte **8.218** |
| 6016 | Claro **536** → Ricaurte **785** → Claro **461** → Ricaurte **1.007** |
| 6019 | Beltrán de Ramón **373** → Ricaurte **4.364** |

Los turnos de Ricaurte habían quedado absorbidos bajo el participante inicial. Se conservan las exposiciones extensas y los comentarios o preguntas intercalados. En 6015, «Ello es confirmado por el señor Miguel Ricaurte» identifica una respuesta, no una mera mención. En 6016, el prefijo «En lo atinente a política monetaria» acompaña al sujeto explícito de Ricaurte y no se deja bajo Claro.

Se añaden advertencias de daño en **6013** —«Agrega que la proyección de En lo referente»— y en el primer tramo de Ricaurte de **6015** —«quien hace que»—. No se reconstruyen palabras faltantes ni se eliminan esos literales.

## 2. Octubre de 2014 y cierre estructural de 6443

La nómina del padre **6440** identifica a Ricaurte Bermúdez como Economista Senior. Se distinguen:

| Padre | Secuencia resultante; caracteres por tramo |
|---|---|
| 6441 | Vergara **455** → Ricaurte **5.897** |
| 6442 | Claro **276** → Ricaurte **550** |
| 6443 | Beltrán **734** → Pablo García **305** → Ricaurte **7.178** → Beltrán **480** → Ricaurte **6.399** |
| 6451 | Vergara **970** → Ricaurte **329** → Vergara **239** → Consejo **111** |

En **6443** se leyó todo el padre, de 15.100 caracteres. «En opinión del Consejero señor Pablo García» es una opinión actual intercalada, mientras que «Miguel Ricaurte retoma» y «Miguel Ricaurte confirma» permiten recuperar los dos desarrollos del expositor. Se conserva el retorno explícito de Beltrán sobre Alemania y los BRICS. Las autoridades extranjeras referidas no crean turnos adicionales.

No se corrigen datos o unidades por inferencia: se mantiene incluso el literal «US$3 el barril» referido al cobre, sin certificar su exactitud. En **6451**, el comentario final de Ricaurte no absorbe la cesión de Vergara a Fuentes ni la incorporación institucional de Soto.

### Advertencia anterior de 6443: retiro explícito, no desaparición silenciosa

La advertencia contextual que cubría todo 6443 bajo Beltrán ya no corresponde a la nueva segmentación. Se retira del registro activo y se conserva **íntegra**, junto con la justificación del retiro y las revisiones sustitutas, en:

`data/curation/alertas_contextuales_retiradas.json`

Las pruebas verifican la conservación del texto/hash original y las revisiones sustitutas. La identidad **no** queda resuelta: los dos tramos actuales de Ricaurte mantienen `VARIANTE_IDENTIDAD_POR_VERIFICAR`. Los controles históricos del motivo archivado siguen probando que una advertencia no registrada sea rechazada y que bloquee continuidad.

## 3. Claudio Soto entre dos intervenciones presidenciales

**4364:** De Gregorio **125** → Soto **154** → De Gregorio **346** caracteres.

El discurso dice «El señor **Claudios Soto** responde». La nómina **4334** y el contexto de **4363** respaldan a **Claudio Soto Gamboa**. Se recupera su respuesta y se mantiene el nombre literal con `NOMBRE_EN_DISCURSO_POR_VERIFICAR`; no se añade un alias general «Claudios» ni se reescribe el OCR.

## 4. Gloria Peña: participante omitida del registro de actores

| Padre | Secuencia resultante; caracteres por tramo |
|---|---|
| 6769 | Miguel Fuentes **1.122** → Gloria Peña **339** |
| 6770 | Vergara **94** → Gloria Peña **342** |

La nómina **6755** identifica a **Gloria Peña Tapia**, Gerente de División Estadísticas Subrogante. En 6769 precisa la publicación de series de actividad; en 6770 responde sobre qué cifras sorprenderían al mercado. La atribución se apoya en esos sujetos y verbos del discurso, **no sólo en la asistencia**.

Se incorpora su nombre completo al registro nominal de actores: antes no era elegible para una revisión de hablante. También se agrega el cargo explícito **Gerente de División Estadísticas Subrogante** al catálogo de nóminas, con salida **Gerente de División Estadísticas (S)**. Ambas filas quedan con `LISTA_ASISTENCIA`, no con un cargo inventado o pendiente pese a evidencia explícita.

Se comprobaron las tres apariciones de «Gloria» fuera de encabezados: la tercera, **6930**, es una referencia a coordinarse con ella, no una intervención suya; permanece como una sola intervención de Vergara. El comparador global confirma que la ampliación nominal y del cargo no altera otros padres.

La cardinalidad pasa de **50 a 51 etiquetas nominales**: 50 personales y el Consejo. La subida proviene de Gloria Peña; **no revierte ni armoniza las variantes Ricaurte**. El actor original Vintimilla de 6025 permanece registrado. No se trata de un censo de identidades independientemente verificadas.

## 5. Alcance técnico y conservación

- **16 intervalos nuevos**: doce de Ricaurte, uno de Pablo García, uno de Soto y dos de Gloria Peña. Total: **250 intervalos en 237 padres**.
- Los **234 intervalos anteriores permanecen idénticos**, incluidos los secundarios, la respuesta de 506 y los retornos revisados en las rondas anteriores.
- **Tres advertencias nuevas** (4364/6013/6015), **una retirada y archivada** (6443); las otras 23 anteriores permanecen idénticas. Total activo: **26**.
- Cambios de código limitados al registro nominal de Gloria Peña y al cargo explícito de Estadísticas Subrogante. Sin flexibilizar reglas de segmentación, alias de Ricaurte o tratamiento de menciones.
- **26 pruebas nuevas:** doce contratos exactos de fuente/segmentos y catorce controles de evidencia, conservación, continuidad, menciones, daño y archivo de advertencias. Se actualizan expectativas históricas, preservando las guardas de los pendientes reales.

## 6. Validación integral

Ensayo aislado y `python scripts/preparar_data.py` terminados correctamente. **1.155 pruebas; F0 y F1 aprobados sin errores bloqueantes.** La base publicada coincide campo por campo con el ensayo.

- **7.219 textos y 2.048.560 palabras conservados**, ignorando sólo espacios en la reconstrucción. 132 sesiones y 310 contrastes TPM.
- **69 hashes de entradas/código y once de salidas verificados**, incluido el nuevo archivo de advertencias retiradas.
- **Todos los enlaces previos entre padres y grupos no afectados conservados**, sin enlaces nuevos o retirados. Las dos exposiciones de García de once filas siguen intactas.
- `CONTEXTO_REVISADO` no crea anclas globales. Se conservan las anclas posteriores de 780/1092/2790, 2790 → 2791, el retiro previo de 5402 → 5403, 3110 institucional y la revisión de 797 caracteres de 3421.
- Esquemas de las bases XLSX **37/24** intactos. Once menciones actuales, 21 fórmulas y tres documentos leídos sin cambios de modelo.
- 5212/5742/5802 mantienen **Larraín autor ≠ Vergara lector**, sin inferir asistencia o habla oral del autor.

## 7. Alertas y pendientes

Las alertas pasan de **322 a 334 filas**, en **297 padres**, antes 288. El aumento no significa que se hayan introducido doce errores: doce intervalos de Ricaurte recién recuperados ahora exhiben la advertencia de identidad que antes quedaba oculta bajo otros actores; se agrega el aviso de nombre de Soto y se retira la antigua advertencia de mezcla de 6443. Las advertencias nuevas de daño se superponen con las de identidad.

Hay **20 filas actuales con variante Ricaurte**, antes ocho. Ninguna se certifica por el solo cambio de etiqueta local o de segmentación. Permanecen cero alertas por `ANAFORA_LOCAL` y dos por atribución heurística legada, correspondientes a pasajes conjuntos de 2126/3989. Esto no implica ausencia de otras atribuciones incorrectas.

La cola histórica mantiene **104 intervalos pendientes de lectura contextual**. Sus estados y tipos de revisión no cambian: **501 comparaciones automáticas, 177 lecturas dirigidas y 105 triajes**, con seis intervalos históricos marcados por variante de identidad. Las nuevas recuperaciones no pertenecen a los intervalos de esa cola histórica: **su contador no mide todo el avance ni todos los pendientes del corpus**. Los 104 históricos y las 334 alertas actuales se superponen; no se suman. Ocho menciones históricas tampoco equivalen a once actuales.

Siguen el puente ambiguo de 780, 6185, pasajes conjuntos de 2126/3989 y residuos de 3191/5367, 4433, discrepancias de nombre/cargo, daños y todas las variantes de Ricaurte. De 6185 no se hizo una lectura integral nueva: sigue el aviso asociado a Bernier, sin forzar un turno.

El barrido nominal dejó candidatos de nombres discrepantes en **226, 1003, 2990, 3476 y 3619**; se registran como **triaje**, no como lecturas integrales ni correcciones aplicadas. No se fuerzan los candidatos de continuidad pendientes de rondas anteriores.

**Faltan cotejos de fuentes primarias en los casos ambiguos y una muestra independiente con y sin alertas.** El barrido dirigido de esta ronda no es una muestra representativa. F0/F1 no certifican pureza semántica exhaustiva.

## Publicación

Rama del PR #3, sin proceso activo al cerrar. Verificaciones locales; `.github/workflows/data-quality.yml` sigue fuera del PR por falta de permiso `workflows`. No se informa CI remoto inexistente. Los informes anteriores se conservan como históricos.
