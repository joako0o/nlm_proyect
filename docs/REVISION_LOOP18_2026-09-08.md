# LOOP18 — Fiscales, Comunicaciones y cambios de hablante ocultos por OCR

**2026-09-08 · [PR #3](https://github.com/joako0o/nlm_proyect/pull/3)**

Base: `06155c9a3598d61890bbcca491c89aa977810d3c`, [LOOP17](REVISION_LOOP17_2026-09-08.md).
Lectura dirigida por agente del texto disponible y contexto de sesión. **Sin nuevo cotejo PDF ni muestra independiente.**

## Resultado publicado

| Medida | Antes | Ahora |
|---|---:|---:|
| Filas físicas | 9.525 | **9.551** |
| Bloques de texto | 9.524 | 9.550 |
| Grupos de turno | 9.114 | 9.140 |
| Grupos multifila / máximo de filas | 315 / 11 | 315 / 11 |
| Filas con alertas / padres alertados | 334 / 297 | **346 / 306** |
| Pruebas | 1.155 | **1.200** |
| Intervalos revisados / padres con revisión | 250 / 237 | **276 / 259** |
| Advertencias contextuales activas | 26 | 36 |
| Etiquetas nominales de actor | 51 | 54 |

**19 padres con separación estructural y cuatro sólo con metadatos de atribución/nombre.** Son **26 intervalos nuevos en 23 padres**, 22 nuevos en el registro; 3476 ya contenía una revisión independiente que se conserva. Los otros **7.196 padres** mantienen sus campos semánticos, descontando identificadores secuenciales.

Todos los padres con separación estaban antes sin alerta. De los cuatro padres con cambios sólo de metadatos, 1003 y 3476 ya tenían alertas en otros tramos. En total, **21 de los 23 padres afectados no tenían alerta**. El barrido nominal fue una búsqueda dirigida de candidatos, no una muestra representativa ni lectura exhaustiva del corpus.

- [Comparación global antes/después](comparacion_loop18_2026-09-08.json)
- [Detalle de filas, texto y hashes](cambios_loop18_2026-09-08.csv)
- [Checkpoint y pendientes](estado_revision_loop18_2026-09-08.json)

## 1. Respuestas jurídicas antes absorbidas bajo otros participantes

Se incorpora al registro nominal a **Miguel Ángel Nacrur Gazali**, sustentado en las nóminas de las sesiones y en sus intervenciones explícitas, no en la mera asistencia.

| Padre | Secuencia resultante; caracteres por tramo |
|---|---|
| 5105 | Marfán **168** → Nacrur **468** |
| 5106 | Vergara **106** → Nacrur **1.395** |
| 5107 | Marfán **169** → Nacrur **213** |
| 5108 | Marshall **289** → Nacrur **465** → Marshall **510** → Nacrur **613** |
| 5183 | Vicuña **401** → Nacrur **316** → Vicuña **656** → Consejo **212** |
| 6277 | Vergara **960** → Nacrur **95** → Vergara **373** |

**5105–5108:** se leyeron las preguntas, respuestas y retornos completos sobre operaciones financieras y facultades legales del Banco. La nómina **5094** identifica a Nacrur como Fiscal y Ministro de Fe, además de Gerente General Subrogante. La salida conserva **Fiscal y Ministro de Fe / LISTA_ASISTENCIA**; las citas legales no crean nuevas voces ni se presentan como asesoría jurídica actual.

**5183:** la nómina **5161** sustenta la aclaración jurídica sobre Latam entre las intervenciones de Vicuña. La frase final «Se determinó, dada la importancia de este tema…» se separa como **acta institucional**, no como opinión de Vicuña o Nacrur. La excepción usa esa oración literal completa; no convierte cualquier «Se determinó» en una transición.

**6277:** el homenaje inicial de Vergara contiene el nombre de Nacrur, pero no es habla de Nacrur. Se revisa también el homenaje como intervalo propio de Vergara y se recupera únicamente el agradecimiento efectivo, antes de su retorno presidencial.

### Mattar: confirmación jurídica, no voto propio

**6113:** Vergara **5.063** → **Pablo Mattar Oyarzún 229** → Consejo **2.334** caracteres.

La nómina **6057** identifica al Fiscal y Ministro de Fe Subrogante. Se registra su confirmación a solicitud de Vergara, conservando separado el acuerdo y el comunicado. No se le atribuye un voto ni se trasladan a él las declaraciones presidenciales. Su cargo final es **Fiscal y Ministro de Fe (S) / LISTA_ASISTENCIA**.

## 2. Comunicaciones: Luis Alberto Álvarez Vallejos

- **1742:** De Gregorio **893** → Álvarez **316** caracteres.
- **2354:** De Gregorio **112** → Álvarez **686** caracteres.

Las nóminas **1687 y 2301** dan el nombre completo local; el discurso dice Luis Álvarez. Se recuperan sus comentarios sobre la Minuta y su tratamiento por la prensa. Las referencias a ministros, analistas o consejeros no generan turnos adicionales.

Los nuevos nombres nominales —Álvarez, Nacrur y Mattar— elevan la cardinalidad de **51 a 54 etiquetas**, 53 personales y el Consejo. No constituyen un censo de identidades independientemente verificadas ni una armonización de variantes globales. Se comprobaron también las referencias a estos nombres fuera de sus intervenciones: no se divide el homenaje de 6277 por la primera mención a Nacrur, y se conserva 3110 institucional.

## 3. Cambios de hablante ocultos por nombres o construcciones defectuosas

| Padre | Secuencia resultante; caracteres por tramo |
|---|---|
| 1424 | Corbo **266** → Marshall **200** |
| 1663 | García **416** → Magendzo **452** → Marfán **1.662** |
| 1860 | De Gregorio **183** → Lehmann **1.716** → Desormeaux **692** → Lehmann **260** |
| 2473 | Marshall **644** → De Gregorio **158** |
| 2865 | Vergara **177** → García **335** |
| 2957 | Cowan **772** → García **73** → De Gregorio **117** → Marfán **907** → Soto **1.626** |

Se conservan los literales **Marshali, Manual Marfán, í\/lanuel, Oesormeaux y Rabio García**. Las nóminas pertinentes y los verbos del discurso sustentan las etiquetas locales, sin introducir alias generales de esos errores. Se agrega advertencia de nombre en los intervalos correspondientes.

**1860:** el residuo `'V/` permanece al final del tramo previo de Lehmann. Su final defectuoso queda visible como alerta automática; no se elimina ni se adjudica texto por tema. Se mantiene el retorno explícito de Lehmann.

**2473:** el literal «Al Presidente señor José De Gregorio comenta» se interpreta por nombre, cargo, verbo y contexto, pero no se reescribe «Al» como «El». Se registra advertencia de daño.

**2957:** la respuesta «señalando el señor Presidente…» se separa mediante el tipo de límite revisado en gerundio ya existente. Sólo el intervalo con hash/citas habilita ese corte; la coma final de la pregunta de García permanece literal.

## 4. Exposiciones de Soto: recuperar el retorno sin perder anclas posteriores

- **2778:** Marfán **519** → Soto **803 revisados** → Soto **1.810 explícitos**.
- **2909:** Soto **1.806** → Marfán **1.244** → Soto **604 revisados** → Soto **2.465 explícitos**.

Los dos comentarios de Soto habían quedado parcialmente atribuidos a Marfán. Se recuperan los comienzos y se preservan los tramos posteriores ya explícitos mediante **`Cita_Ancla_Posterior`**. Es una separación de evidencia/segmentos, no la invención de una interrupción entre los dos tramos contiguos de Soto. **`Fin` solo no crea un corte ni una ancla.** Las enumeraciones y desarrollos permanecen completos.

## 5. Marfán después del comunicado y Ricaurte después de Herrera

### 4054: declaración personal tras una cita cerrada

Marfán **191** → Consejo/comunicado **1.399** → Marfán **539** caracteres.

Después de cerrar el comunicado, Marfán manifiesta su decisión de sumarse al voto de mayoría y explica que reserva su disidencia para otras causas. Esta declaración estaba dentro del segmento institucional; ahora queda como intervención personal, sin alterar el comunicado ni el relato de su cambio de voto.

Se añade **`RETORNO_TRAS_CITA_CERRADA_REVISADA`**, exclusivamente por revisión acotada. Exige cierre de cita con puntuación, el inicio temporal documentado, sujeto explícito compatible y ausencia de cita abierta. La proyección del prefijo se utiliza sólo para validar al hablante, nunca para reescribir el texto. Hay pruebas de rechazo sin cierre de cita, sin opt-in y con actor incompatible. No es una regla automática para dividir citas o comunicados.

### 4594: respuesta de Ricaurte sobre inflación de alimentos

Herrera **1.149** → Ricaurte **1.567** caracteres.

La nómina **4573** sustenta la etiqueta local **Miguel Ricaurte Bermúdez**. Se mantiene la respuesta completa, sin convertir las referencias a organismos internacionales en intervenciones. Conserva `VARIANTE_IDENTIDAD_POR_VERIFICAR`: **no se resuelve la equivalencia global Bermúdez/Vintimilla**.

## 6. Cuatro revisiones sólo de atribución/nombre

Se leen completos y documentan estos intervalos, sin modificar su texto, actor ni límites:

| Padre | Intervalo revisado | Discrepancia preservada |
|---|---:|---|
| 1003 | Magendzo, **687** caracteres | Madgenzo |
| 2990 | Soto, **2.689** caracteres | Claudia Soto |
| 3476 | Soto, **2.853** caracteres | Claudia Soto |
| 3619 | Soto, **4.133** caracteres | Claudia Soto |

Se añaden avisos de nombre. En 1003 se revisa **sólo ese intervalo**, no los otros tramos de Magendzo ni todo el padre. En 3476, la revisión presidencial previa de **255 caracteres** queda idéntica e independiente, ahora secundaria. Identificar al expositor no certifica la integridad de todo el OCR.

**226** se leyó completo, pero no se registra adjudicación nueva ni se modifica la continuidad **224 → 225 → 226** de García. «Rabio García» sigue como discrepancia documental pendiente en el checkpoint; no se reescribe ni se introduce un aviso que corte automáticamente esa continuidad. Este pendiente no está resuelto por la pasada.

## 7. Verificación integral

**1.200 pruebas**, 45 nuevas —23 contratos exactos por padre y 22 controles de comportamiento/evidencia—. Ensayo aislado y `python scripts/preparar_data.py` completos; **F0 y F1 sin errores bloqueantes**. La base publicada coincide campo por campo con el ensayo.

- **7.219 textos y 2.048.560 palabras conservados**, ignorando sólo espacios en la reconstrucción. 132 sesiones y 310 contrastes TPM.
- **70 hashes de entradas/código y once de salidas verificados.**
- Los **250 intervalos previos y 26 advertencias previas permanecen idénticos**. Diez avisos contextuales nuevos: nueve de nombre y uno de daño; total activo **36**. No se retira ninguno en esta ronda y el archivo del retiro previo de 6443 queda intacto.
- Todos los enlaces entre padres y grupos no afectados conservados; **ningún enlace nuevo o retirado**. Las dos exposiciones de García de once filas permanecen intactas.
- `CONTEXTO_REVISADO` nunca crea anclas globales. Se preservan las anclas posteriores de 780/1092/2790 y las nuevas guardas de 2778/2909, 2790 → 2791, 3110 institucional, 3421 y el retiro previo de 5402 → 5403.
- Bases XLSX **37/24**, once menciones actuales, 21 fórmulas y tres documentos leídos sin cambios de modelo: **Larraín autor ≠ Vergara lector**, sin inferir asistencia o habla oral del autor.
- Cambios de código limitados al registro nominal de los tres participantes, la oración institucional literal de 5183 y el nuevo tipo de revisión posterior a cita cerrada. Sin flexibilizar alias de nombres dañados o de Ricaurte.

## 8. Alertas y trabajo pendiente

Las alertas pasan de **334 a 346 filas**, en **306 padres**, antes 297. Los motivos se superponen: nueve nombres nuevos, daño del inicio de 2473 y variante de Ricaurte de 4594; también quedan visibles los finales literales de 1860 y de la pregunta de 2957. No son doce errores nuevos introducidos por el procesamiento ni 346 errores confirmados.

Hay **21 filas actuales con variante Ricaurte**, antes veinte. Permanecen cero alertas por `ANAFORA_LOCAL` y dos por atribución heurística legada (2126/3989 conjuntos, no forzados). Esto no certifica todas las atribuciones del corpus.

La cola histórica conserva **104 intervalos pendientes de lectura contextual**. Una clasificación pasa de comparación estructural a corrección dirigida: ahora son **500 comparaciones automáticas, 178 lecturas dirigidas y 105 triajes**, con 102 correcciones dirigidas como estado principal. 3476 se reconoce como corrección dirigida; el intervalo histórico pendiente de 1003 no se declara resuelto por revisar otro tramo del mismo padre. Hay seis intervalos históricos con variante de identidad. Los conteos históricos y actuales se superponen y **no se suman**; ocho menciones históricas tampoco equivalen a once actuales.

Siguen 226, el puente de 780, 6185, 2126/3989, residuos de 3191/5367, 4433, variantes de identidad, nombres/cargos y daños. Se anotan nuevos candidatos nominales **2349/3050/3315/3454** sólo como triaje, sin lectura integral ni adjudicación en esta ronda. No se fuerzan las continuidades pendientes de rondas anteriores.

**Faltan cotejos de fuentes primarias para casos ambiguos y una muestra independiente con y sin alertas.** No hubo lectura exhaustiva del corpus ni cotejo PDF nuevo; F0/F1 no certifican pureza semántica total.

## Publicación

Rama del PR #3, sin proceso activo al cerrar. Verificaciones locales; `.github/workflows/data-quality.yml` sigue fuera del PR por falta de permiso `workflows`. No se informa CI remoto inexistente. Los informes anteriores permanecen como históricos.
