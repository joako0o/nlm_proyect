# LOOP27 — Interrupción institucional y cambios de voz entre referencias y artefactos

**Base comparada:** `d1656177b533a99444491b7d62b88197ccde219b` (LOOP26).

**Resultado:** cuatro padres resegmentados —tres con intervenciones personales recuperadas y uno con separación de acta y exposición—, dos referencias registradas y un pasaje conjunto advertido y pendiente. **1.514 pruebas aprobadas**, F0/F1 sin bloqueos y comparación global validada. Sin nuevo cotejo PDF ni muestra independiente.

## 1. Alcance y descubrimiento

Se leyeron íntegros **ocho padres: 600, 601, 870, 2510, 3120, 4064, 4476 y 6601**. Se consultaron además extremos de vecinos, fechas y evidencia de sesión, sin contarlos como nuevas lecturas completas.

Los barridos complementarios produjeron:

| Barrido | Resultados candidatos |
|---|---:|
| Inicios nominales con conectores excluidos por el barrido de LOOP26 | 131 ventanas |
| Proyección desde tratamientos interiores | 138 ventanas |
| Sujetos por cargo sin tratamiento nominal cercano | 16 ventanas |
| Palabra posterior al nombre, con filtros de predicado | 1086 ventanas |
| Cargos presidenciales/ministeriales con proyección de verbo | 34 ventanas |

No se suman estas cifras como casos únicos o lecturas completas: se superponen e incluyen puntuación, cesiones, asistencia, referencias retrospectivas y atribuciones sintéticas incorrectas. Las proyecciones son **instrumentos de búsqueda, no atribuciones adoptadas**. Por ejemplo, referencias a Bernanke, Obama o Putin no los convierten en presidentes del Banco ni crean alias.

No se afirma lectura integral de todas las ventanas, muestreo representativo ni ausencia de mezclas por haber agotado estos filtros. La menor cantidad de correcciones que en otras pasadas no se compensa con cortes sin evidencia.

## 2. Tres recuperaciones de habla personal

Longitudes de las filas **exportadas**, incluidos espacios; no son tamaños de fuente cruda antes de la normalización habitual de espacios/saltos.

| Padre | Antes → después | Evidencia y límites |
|---|---|---|
| **3120** | Presidente **161**, Larraín **6886** → Presidente **161**, Larraín **6723**, Presidente **162** | «Finalizada la intervención del señor Ministro…» devuelve la voz a De Gregorio, quien abre la votación. Vergara es destinatario, no hablante dentro de la cesión. La intervención de Larraín es **oral según el relato**, no uno de los documentos leídos por tercero. |
| **4064** | Herrera **685** → Herrera **462**, Lehmann **222** | Lehmann insiste en la distorsión de filtros después de la explicación de Herrera sobre el heat map. El artefacto intermedio se conserva y se advierte en la fila previa. |
| **4476** | Vergara **1297** → Vergara **395**, Lehmann **797**, Vergara **103** | «En cuanto a las consecuencias… el Gerente… percibe…» introduce la respuesta de Lehmann sobre Reino Unido/Europa. La pregunta presidencial posterior conserva su identificación explícita y su ancla propia. |

Se añaden **tres intervalos personales**: total **377 en 348 padres**. Los **374 intervalos anteriores permanecen idénticos**. El aporte completo de Larraín conserva «inflación vi* acotada» y sus cifras: la separación de la cesión no certifica integridad del OCR ni permite reconstruirlo.

No se amplía globalmente «percibe», «da paso» ni los alias. **CONTEXTO_REVISADO sigue sin crear anclas globales; Fin solo no corta ni crea anclas.**

### Excepción individual para el artefacto de 4064

`INICIO_TRAS_ARTEFACTO_REVISADO` exige el intervalo con hash y evidencia, el artefacto literal `-4 . f . • " ' A) `, una oración terminada antes de él y el sujeto/declaración nominal correspondiente de Lehmann.

Sólo para **validar ese límite** se separa el artefacto del prefijo examinado por el guardián de comillas. **No se elimina de la exportación.** La protección contra una cita realmente abierta antes del artefacto sigue vigente. Se rechazan cambios de actor, cita del artefacto, signos o modo; no hay una regla global que ignore comillas impares o separe cualquier mayúscula.

El artefacto no se certifica como palabras pronunciadas por Herrera ni se identifica su origen material sin cotejo. Permanece como residuo textual en el tramo anterior, con aviso independiente.

## 3. 600→601: exposición conservada, pausa respetada

Se leyeron íntegros ambos padres. **600** contiene la exposición de García de **1869 caracteres exportados**. **601** comienza con una interrupción de diez minutos para que reporteros fotografíen al Consejo con el nuevo Ministro. Luego se reinicia la sesión y se nombra a Pablo García como expositor.

Antes, los **3996 caracteres** de 601 figuraban bajo García y compartían turno con 600. Ahora:

1. **Acta institucional, 307 caracteres:** interrupción, fotografías y reanudación con expositor nominal. No se inventa una intervención oral de Corbo ni de Velasco.
2. **García, 3688 caracteres:** exposición económica completa, comenzando literalmente «quien señala que…». Se conservan sus desarrollos monetarios, de demanda, actividad, precios, salarios y expectativas.

La identidad del relativo se valida mediante la mención nominal contigua en el acta. La proyección «El señor Pablo García…» se utiliza sólo en la validación: **no sustituye «quien» en la salida**. La fuente nominal y su justificación revisada quedan trazadas; el cuerpo no se tipifica como acta.

### Alcance institucional acotado

El registro `revisiones_continuaciones_acta.json` admite ahora, además de su modalidad anterior de padre completo, `INTERRUPCION_Y_REANUDACION_REVISADA`. Para 601 exige:

- fuente, fecha, límite y dos textos completos;
- el registro exacto de interrupción/reanudación y nombre del expositor;
- antecedente inmediato 600 con hash y cita;
- notas y tipos distintos para acta y exposición;
- archivo de ambas filas que sostenían el enlace anterior.

La ficha anterior de **3110 permanece idéntica**, sigue aplicando al padre completo y mantiene su validación. No se introduce herencia institucional genérica ni una solución automática para 4055. No se permite solapamiento con una revisión personal o documental del mismo padre.

### Un enlace retirado con justificación, no una regresión silenciosa

**600→601 es el único enlace retirado.** El vínculo anterior atravesaba la interrupción institucional; García conserva su identidad y toda su exposición, pero comienza un turno nuevo tras la pausa. No se corta por longitud ni por un cambio temático.

Las dos filas completas de LOOP26 quedan archivadas en `Enlace_Retirado` de **ACTA-20260908-L27-601**, junto con la razón del retiro. La comparación global las coteja con la base anterior, no sólo con una descripción. No se elimina ninguna de las **nueve pruebas de continuidad revisadas**. En particular, **4745→4746** y **6561→6562**, resueltas en LOOP26, permanecen intactas.

## 4. Referencias que no abren voces y un pasaje que no se fuerza

### Dos lecturas legítimas nuevas

- **870/1854:** Jadresic suscribe la propuesta sobre el comunicado, «tal como lo ha manifestado… García». García es una referencia; no pasa a ser sujeto de «suscribe». El desarrollo completo de Jadresic se conserva.
- **6601/833:** Naudon comparte un planteamiento de Claro y cita el caso sueco. Claro no es autor del desarrollo de Naudon. Los tramos posteriores de **De Ramón 311** y **García 542** permanecen intactos, incluida la revisión previa de este último.

Ambas fichas están validadas en el registro actual y **no aparecen en `revision_pendientes.csv`**, pues sus filas no tienen alertas. No se cambian textos, atribuciones o agrupaciones para registrar estas lecturas.

### 2510: comentario conjunto pendiente

El primer tramo de **699** caracteres contiene palabras presidenciales y termina con «el Presidente y el Consejero señor Sebastián Claro comentan…». No es defendible atribuir esa proposición exclusivamente a uno, duplicarla como dos intervenciones o repartir sus palabras arbitrariamente. Velasco aparece como consultante referido, no como un turno delimitado allí.

Se registra **PASAJES_CONJUNTOS_POR_DELIMITAR** y una lectura **PENDIENTE_DELIMITAR_APORTE**, manteniendo provisionalmente la fila existente. Se conservan las cuatro filas del padre: **699 / 2071 / 243 / 503**. Las dos exposiciones de Lehmann y el comentario presidencial posterior no se absorben en el aviso.

**38 lecturas actuales = 34 menciones legítimas + 4 pendientes: 6185, 3775, 4055 y 2510.** Las 35 fichas anteriores permanecen intactas. Los tres pendientes previos no se convierten en menciones resueltas por esta pasada.

## 5. Advertencias y cola visible

**73 advertencias contextuales = 71 anteriores + 2 nuevas**, sin retirar ninguna:

- **4064/462:** residuo gráfico previo a Lehmann, conservado sin reconstrucción ni origen certificado.
- **2510/699:** proposición conjunta Presidente/Claro sin delimitación exclusiva.

Los tres archivos de retiro de advertencias —**6443, 2704 y 2661**— no cambian. Son una unidad distinta del **enlace** retirado en 600→601.

Las filas con alertas pasan de **448 a 451**, en **381 padres** frente a 378:

| Padre | Incremento | Motivo |
|---|---:|---|
| **601** | +1 fila | Coma final conservada en el tramo de acta al separar el relativo; `FINAL_SIN_PUNTUACION`. |
| **2510** | +1 fila | Advertencia de proposición conjunta. |
| **4064** | +1 fila | Advertencia de daño/artefacto textual. |

**451 filas con alertas no equivalen a 451 errores confirmados ni a todo lo que falta revisar.** No se suprime la coma ni se promueve la nueva fila a fórmula para ocultar el aviso. No hay nuevas fichas documentales ni nuevas fórmulas.

## 6. Verificación global

| Control | Resultado |
|---|---:|
| Pruebas | **1514**, todas pasan; **32 nuevas** |
| Filas físicas / bloques | **9683 / 9682**, antes 9678 / 9677 |
| Grupos de turno / multifila / máximo | **9264 / 323 / 11**, antes 9258 / 324 / 11 |
| Padres / palabras / sesiones | **7219 / 2048560 / 132**, conservados |
| Intervalos personales anteriores / actuales | **374 / 377** |
| Padres con revisión personal | **348** |
| Advertencias anteriores / actuales | **71 / 73** |
| Lecturas anteriores / actuales | **35 / 38** |
| Documentos anteriores / actuales | **12 / 12**, todos conservados |
| Pruebas de enlace revisado | **9**, todas intactas |
| Enlaces nuevos / retiros justificados / retiros no justificados | **0 / 1 / 0** |
| Registro institucional anterior / actual | **1 / 2**, 3110 intacto |
| Etiquetas de actor | **55**, sin nuevas identidades ni alias |
| Esquemas / fórmulas / contrastes TPM | **37/24 / 21 / 310** |
| Hashes de entradas/código / salidas comprobados | **81 / 11** |
| Ensayo aislado frente a publicación | **Idénticos** |

Los cuatro padres corregidos estaban antes sin alertas. **Cinco padres cambian celdas no secuenciales**: 601, 3120, 4064 y 4476 por resegmentación; 2510 sólo por aviso. **7214 conservan esas celdas**, excluidos `ID` e `ID_Turno`.

600 conserva sus celdas, pero su grupo deja de incluir 601. Por ello son **seis padres alcanzados por correcciones, retiro de enlace o aviso**, y **7213 fuera de ese alcance**. Los grupos fuera de correcciones y de la arista retirada permanecen iguales. La disminución de un grupo multifila es la consecuencia documentada de la pausa, no pérdida de texto.

Se verificaron todas las aristas anteriores: sólo se retira la archivada **600→601**. Permanecen García de once filas, **224→225→226, 3454→3455, 2695→2696, 2754→2755, 2790→2791, 1386→1387, 2673→2674, 2863→2864, 2796→2797, 2707→2708, 2963→2964 y 2680→2681**, y las nueve pruebas de enlace revisado. **5402→5403 no se restablece.**

También se compararon todos los intervalos, advertencias, lecturas y documentos previos, 3110, los archivos de retiro de advertencias, decisiones TPM y registros documentales salvo IDs. Los retornos explícitos de **Soto/4926** y **Vergara/4476** conservan sus anclas.

Las 32 pruebas nuevas comprenden **ocho contratos de fuente cruda/firma/conservación** y **24 pruebas de comportamiento**. Las longitudes crudas de 600, 601 y 870 difieren de las exportadas por la normalización de espacios/saltos ya existente, no por eliminación de contenido. La comparación global conserva todos los caracteres ignorando sólo espacios y todas las palabras.

## 7. Histórico y límites

La cola histórica de **783** conserva sus estados y tipos: **102 pendientes contextuales**, **497 comparaciones**, **183 lecturas dirigidas** y **103 triajes**; **284 intervalos históricos** siguen ligados a alertas actuales. Se mantienen **seis intervalos históricos** de variante de identidad y **21 filas actuales** correspondientes. El estado principal no cierra motivos independientes.

**Ocho menciones legítimas históricas no equivalen a 34 actuales**: las unidades se superponen y no se suman. Las nuevas lecturas no convierten estos barridos en una muestra independiente.

Siguen pendientes 6185/Bernier, la conclusión de 3775/Cerda, 4055/conjunto-institucional y ahora 2510/conjunto, además de los controles anteriores de nombres, cargos y daño. No se afirma nueva lectura integral de todos los controles preservados ni revisión exhaustiva o pureza total del corpus.

**Sin nuevo cotejo PDF ni muestra independiente con/sin alertas.** Una exposición larga no está dañada por su extensión. La extracción no se repara mediante conjeturas.

## Entregables

- `data/processed/consolidado_base_referencia_final.xlsx`: **9683 filas**.
- `data/processed/consolidado_base_referencia.xlsx`: auditoría de 37 columnas.
- [Comparación global y archivo de la arista](comparacion_loop27_2026-09-08.json).
- [Cambios por padre y versión](cambios_loop27_2026-09-08.csv).
- [Checkpoint vigente](estado_revision_loop27_2026-09-08.json).
- [LOOP26 anterior](REVISION_LOOP26_2026-09-08.md), conservado como histórico.

Verificaciones locales. El workflow preexistente de GitHub Actions queda fuera del PR; no se afirma ejecución remota. No hay proceso activo.
