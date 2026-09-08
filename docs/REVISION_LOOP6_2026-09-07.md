# Sexto bloque: pasada amplia de suspensiones, retornos y votos

**Fecha:** 2026-09-07. **PR:** [#3](https://github.com/joako0o/nlm_proyect/pull/3).
**Inicio:** 9.251 filas / 615 alertas / 351 pruebas.
**Publicación:** **9.353 filas / 580 alertas / 432 pruebas; F0/F1 aprobados.**

Se encadenaron tres ciclos de corrección y una lectura/documentación de residuos.
**59 padres modificados, 102 filas adicionales y dos nuevas anotaciones de
menciones legítimas.** Los 59 padres pasan de 74 a 176 segmentos. La publicación
está terminada; no queda un proceso activo en segundo plano.

**Ocho candidatos prioritarios restantes no significan ocho pendientes totales:**
quedan 580 filas con alertas y 388 intervalos de la cola original pendientes de
lectura contextual. Las alertas no son errores confirmados.

## Entregables

- [Excel final](../data/processed/consolidado_base_referencia_final.xlsx).
- [Seguimiento de las 783 originales y cola actual](../data/processed/revision_783.xlsx).
- [59 padres y 176 segmentos completos, con hashes e IDs anteriores](cambios_loop6_2026-09-07.csv).
- [Comparación global y contenido antes/después](comparacion_loop6_2026-09-07.json).
- [Dos nuevas menciones documentadas](menciones_loop6_2026-09-07.csv).
- [Propuestas de intervalos documentales, NO aplicadas](propuestas_documentales_loop6_2026-09-07.json).
- [Checkpoint y candidatos restantes](estado_revision_loop6_2026-09-07.json).

Los IDs de fila pueden renumerarse. Los padres corresponden al consolidado de
origen. El [informe anterior](REVISION_LOOP5_2026-09-07.md) queda como histórico.

## Ciclos y alcance real de la lectura

| Ciclo | Trabajo | Filas del ensayo | Pruebas |
|---:|---|---:|---:|
| 1 | Suspensiones/reanudaciones; 45 padres modificados | 9.333 | 408 |
| 2 | Once intercambios, retornos y votos | 9.348 | 426 |
| 3 | Cuatro padres, uno ya abordado parcialmente en ciclo 1; dos menciones | 9.353 | 432 |

La lectura de la familia repetida fue **acotada al límite, su contexto inmediato
y el bloque de suspensión/reanudación**, no una certificación íntegra de cada
exposición anterior. En los intercambios se revisaron la secuencia y las
continuaciones pertinentes, usando también extractos de los padres vecinos.
No hubo cotejo PDF nuevo ni revisión humana/semántica independiente.

### Ciclo 1 — Familia de suspensión y reanudación

Se inspeccionaron 47 apariciones de `Al no haber…` / `Al no formularse…`, más
6373, cuya suspensión continúa una oración explícita del Presidente. **48
pasajes comprobados: 45 cambian y tres ya estaban correctamente segmentados
(4384, 4502 y 5252).**

Se reconocen prefijos completos de ausencia de comentarios, con hora válida
opcional, manteniendo las exigencias de sujeto y predicado de habla. También
se reconoce la fórmula institucional `A las HH:MM horas, se reanuda la Reunión
de Política Monetaria N°…`, no cualquier referencia a una hora.

El patrón predominante queda:

**Expositor → Presidente que suspende → Consejo/acta que registra la reanudación.**

Cuando el Presidente ya hablaba, no se inventa una voz nueva para la suspensión.
Cuando vuelve a hablar después del registro institucional, se conserva su
retorno. 5252 mantiene al Vicepresidente Marfán como quien suspende; no se fuerza
al Presidente por su cargo habitual.

Casos especiales comprobados:

- **5313:** `13.05 horas` se conserva literalmente y deja de cortarse como si
  `05` iniciara otra oración. La excepción exige contexto de hora y minutos válidos.
- **5548:** después de la reanudación, el Presidente cede la palabra a Lehmann.
  Se añadió una revisión individual para que esa cesión no quede dentro del acta
  ni se adjudique al destinatario; 5549 comienza la explicación de Lehmann.
- **6583:** además de la suspensión, se separó la opinión de Marshall entre el
  análisis de García y el Presidente. No se adjudica esa cautela a García.
- **5798:** se conserva `H ^ .`; **7145:** se conserva el número de reunión 227,
  sin corregir la numeración por intuición. 4502 conserva su prefijo `i,-`.

Las 48 citas de suspensión y reanudación tienen hashes y regresiones
parametrizadas. La comparación global confirmó sólo los 45 padres previstos,
sin cambios adicionales de metadatos.

### Ciclo 2 — No confundir retorno, disidencia y resultado del Consejo

| Padre | Secuencia corregida |
|---:|---|
| 4745 | Soto → Lehmann, retorno a las proyecciones internacionales |
| 4857 | Presidente → Vial → Lehmann; Putin es una referencia, no un hablante local |
| 4941 | Herrera → Soto, identificado por cargo de sesión y continuación en 4942 |
| 5910 | Vial → Lehmann, desde su complemento sobre Argentina hasta toda la exposición |
| 6050 | Presidente → Vial → Presidente, con toda la fundamentación y voto de Vial |
| 6293 | Presidente → García → Presidente, conservando la disidencia por bajar a 3,75% |
| 6389 | Presidente → García → Presidente → Consejo/acta |
| 6561 | Vial → Fuentes, con 4.261 caracteres de exposición internacional conservados juntos |
| 6730 | De Ramón → Soto → Naudon; Soto actúa como asesor de Hacienda |
| 7044 | Presidente → Vial → Presidente, conservando la disidencia por subir a 3,25% |
| 7092 | Naudon → Fuentes, cierre sobre expectativas de TPM |

En **6050**, Vial empieza en `En el plano internacional, indica…`, después de
la cesión explícita. No se corrigió solamente la reflexión final que vuelve a
nombrarlo. Su intervención de 4.119 caracteres conserva el final dañado
`economías`, antes del agradecimiento del Presidente.

Las coordinaciones revisadas admiten únicamente las variantes documentadas
`y sobre este aspecto…`, `y en este sentido…` y `y, en ese sentido…`, además de
las formas anteriores. **Requieren una entrada individual con hash, límites,
sujeto compatible y ausencia de comillas**: no se divide automáticamente cada
`y`. La proyección que reconoce el sujeto no reescribe los conectores exportados.

En 6293 y 7044, los votos individuales disidentes no se tipifican como acuerdos
del Consejo; las declaraciones de mayoría siguen con el Presidente. F0 mantiene
los 310 contrastes TPM.

### Ciclo 3 — Residuos internos y menciones legítimas

- **5368:** Herrera → Fuentes. La aclaración sobre gráficos no absorbe la
  exposición posterior sobre expectativas, salarios, consumo y demanda.
- **5417:** Marshall → Presidente. Se separa la cesión a Soto, encontrada al
  leer el contexto de 5418; el destinatario no se convierte en autor de la cesión.
- **5418:** Soto → Vicuña → Soto. Vicuña precisa el IMACEC de 6,7% a 6,5%; Soto
  mantiene 3.194 caracteres antes y 5.312 después de esa precisión. No se
  fragmentan sus continuaciones sobre minería, finanzas y empleo.
- **5615:** Herrera → Soto → Presidente → Consejo/acta. En el primer ciclo se
  había separado la suspensión, pero aún quedaba la precisión de Soto sobre
  importaciones dentro de Herrera. Este ciclo corrige ese límite adicional.

Se añadieron dos menciones actuales:

- **5658:** Vial recuerda una conversación con el Presidente del Banco Central
  de Reserva de Perú. No es una intervención del Presidente del BCCh.
- **6587:** García remite a lo mencionado previamente por el Ministro de
  Hacienda y continúa su fundamentación. No se crea un nuevo turno del Ministro.

**Ambas conservan sus alertas.** Las ocho anotaciones previas permanecen
idénticas; ahora hay diez. Se cuentan separadamente de las ocho menciones
históricas del seguimiento original.

## Continuidad y controles finales

- **432 pruebas locales aprobadas**, 81 más que al inicio, incluidas las 48
  comprobaciones parametrizadas de la familia. Hay negativos de citas,
  referencias, sujetos incompatibles, horarios inválidos y cortes no autorizados.
- Tres construcciones aisladas con comparación de alcance, seguidas del pipeline
  completo. El contenido publicado coincide con el tercer ensayo; **F0/F1 pasan**.
- Los **7.219 padres conservan el texto**, ignorando sólo espacios. Exactamente
  59 cambian segmentación/actor; los otros 7.160 mantienen texto, actor, cargo,
  fuentes, tipo, motivos, relación, categorías y duplicados, descontando IDs
  renumerados y notas que los contienen. No hay cambios adicionales de metadatos
  semánticos. Las anotaciones de mención se añaden en el seguimiento/cola.
- **18 enlaces protegidos** y la partición de grupos no afectados siguen
  intactos. Continúan los **301 grupos multipárrafo**, con máximo once filas;
  las exposiciones de García de 60–70 y 142–152 se comprobaron expresamente.
- Las revisiones contextuales no crean por sí solas anclas de agrupación. No se
  forzaron, entre otros, 4745 → 4746, 4941 → 4942, 5910 → 5911 o 6561 → 6562:
  se conserva su contenido/actor, sin fingir un `ID_Turno` común automático.
- **91 revisiones de hablante**, 17 nuevas; las 74 anteriores son idénticas.
  Hay 23 coordinaciones documentadas y diez menciones actuales con avisos intactos.
- **50 hashes de entradas/código y diez hashes de salidas verificados**. El Excel
  de origen no cambió. Se conservan 2.048.560 palabras; hay 9.352 bloques en
  9.353 filas físicas, máximo 31.948 caracteres por celda y 8.961 grupos de turno.
- Los duplicados exactos pasan a 576, de los que 574 son de fórmula; separar
  fórmulas repetidas modifica ese conteo, **no elimina textos**.

Los resultados son locales. El workflow de GitHub Actions sigue fuera del PR
por falta de permiso `workflows` en la conexión. Los controles automáticos no
sustituyen una revisión semántica independiente.

## Balance de alertas y seguimiento

| Indicador | Antes | Ahora |
|---|---:|---:|
| Filas con alguna alerta | 615 | **580** |
| Posible otro hablante/mención | 76 | **26** |
| Final sin puntuación | 244 | **249** |
| Candidatos de otro hablante sin anotación de mención | 60 | **8** |
| Originales pendientes de lectura contextual | 437 | **388** |

Los otros motivos se mantienen: 258 atribuciones legadas, 42 anáforas, nueve
breves, seis variantes de identidad y dos repeticiones no formulaicas.
Los cinco avisos nuevos de puntuación corresponden a límites conservados en
4857, 6050, 6293, 7044 y 5418. **Los motivos se solapan**: restar sus cantidades
no da directamente la variación de filas con alertas. La reducción no mide
un número de errores confirmados ni un porcentaje de pureza.

En las 783 originales: 388 pendientes de lectura contextual, 59 fórmulas,
71 métodos actualizados, 157 cambios por comparación, 84 correcciones dirigidas,
siete breves, ocho menciones históricas, seis identidades, dos repeticiones y una
continuidad. Por tipo: **161 lecturas del agente, 228 comparaciones y 394 triajes**.
555 intervalos originales siguen solapándose con alertas actuales. Estos estados
no certifican padres completos; las correcciones por reglas se mantienen
separadas de las lecturas dirigidas registradas en la cola.

## Ocho candidatos prioritarios y otros pendientes

| Padre | Estado al terminar |
|---:|---|
| 780 | Comienzo de Corbo pendiente de cotejo/delimitación; acuerdo ya abordado anteriormente |
| 3191 | Intercambio con coincidencia conjunta del Presidente y Soto; no adjudicar a uno solo |
| 5212 | Planteamiento escrito del Ministro leído por el Presidente |
| 5367 | Varios límites, rótulo OCR y petición colectiva de los Consejeros |
| 5647 | Compromiso de Lehmann y continuidad posterior sin adjudicar |
| 5742 | Planteamiento escrito del Ministro ausente, leído por el Presidente |
| 5802 | Otro planteamiento escrito leído por el Presidente, con daño OCR |
| 6185 | Referencia/confirmación de Bernier dentro de una exposición de 20.118 caracteres; lectura acotada, no cerrada |

Los textos completos de 5212, 5742 y 5802 se leyeron y se documentaron **propuestas
no aplicadas** de cuatro tramos: cierre de Herrera, introducción del Presidente,
texto escrito de Larraín y retorno del Presidente. Las propuestas distinguen
**autor y lector**; no inventan asistencia del Ministro ni presentan el escrito
como una intervención oral suya. Requieren una decisión de modelado y validación
antes de modificar la base. Los avisos permanecen.

5367 también se leyó: hay exposición de Fuentes, petición colectiva, respuesta
de Herrera tras el rótulo, aclaración de Fuentes y opinión de Claro. No se
adjudicó la petición colectiva arbitrariamente a una persona ni se corrigió
sólo el último límite para declarar resuelto el padre.

Persisten además 2126, las confirmaciones pasivas de 2661/2704, los daños de
2667/3107, las variantes de identidad, las repeticiones y la revisión de una
muestra independiente con y sin alertas. **El filtro de ocho no agota el trabajo.**
