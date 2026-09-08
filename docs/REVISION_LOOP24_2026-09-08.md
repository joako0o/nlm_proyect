# LOOP24 — Habla personal, registros de sesión y confirmaciones

**Base comparada:** `084bf2825e757a1390de189aa4f369bc1b986054` (LOOP23).
**Resultado:** nueve padres corregidos, diez intervalos nuevos; 1.403 pruebas y publicación validada. Sin nuevo cotejo PDF ni muestra independiente.

## Alcance y resultado

Se leyeron completos los doce padres 1549, 2219, 2661, 2680, 2746, 2788, 2875, 2958, 3008, 3288, 4055 y 5252, correspondientes a 37 filas de la base anterior. Esto no equivale a doce padres certificados íntegramente ni a doce avisos cerrados.

- **Seis padres resegmentados:** 2661, 2680, 2746, 2788, 3288 y 5252. Siete filas adicionales.
- **Tres padres con reasignación sin nuevas filas:** 2875, 2958 y 3008. El habla presidencial estaba bajo la etiqueta institucional. En 3008 se conserva la respuesta separada de Larraín.
- **4055:** advertencia y lectura pendiente, sin reasignación ni cortes arbitrarios.
- **1549/2219:** dos referencias legítimas registradas, sin cambiar sus filas ni alertas.
- **2681:** cambia exclusivamente el identificador de antecedente por la resegmentación de 2680; no es una nueva adjudicación ni una nueva lectura integral de 2681.

Ocho de los nueve padres corregidos no tenían alertas. El caso restante, 2661, tenía una advertencia de mezcla que ahora se archiva completa. No se utilizó la presencia de alertas como requisito para buscar errores.

## Separaciones y reasignaciones

Longitudes en caracteres de las filas exportadas, incluidos espacios. Los separadores entre filas explican que las longitudes individuales no se sumen exactamente a la fila anterior.

| Padre | Antes | Después y alcance |
|---|---|---|
| 2661 | Desormeaux 243, con confirmación de Lehmann dentro | Desormeaux **193** → Lehmann **49**. Mantener Lehmann explícito **1322**, los demás turnos y la coordinación revisada anterior de **69**. |
| 2680 | Consejo 240, con invitación presidencial | Acta **75** → De Gregorio **164**. García **489** sigue separado y unido a 2681 como antes. |
| 2746 | Consejo 469: cierre presidencial más reanudación | De Gregorio **181** → acta **287**. Cowan **1094** intacto. La excusa de Velasco no es una intervención. |
| 2788 | Consejo 257; De Gregorio 599, incluida exposición de Soto | De Gregorio **182** → acta **74**; invitación de De Gregorio **191** → exposición de Soto **407**. También permanece el agradecimiento previo de **126**. |
| 2875 | Consejo 1038 | Reconocimiento presidencial completo a Velasco, **1038**. Velasco es homenajeado, no hablante. Cierre previo de **79** intacto. |
| 2958 | Consejo 224 | Apertura presidencial y cesión a García, **224**. No atribuir a García palabras todavía no pronunciadas. Cierre previo **335** conservado, incluida su repetición. |
| 3008 | Consejo 332 | Bienvenida de De Gregorio **332**, seguida de respuesta de Larraín **413**, sin fusionarlas. |
| 3288 | Vergara 226, incluida conformidad de De Ramón | Vergara **129** → De Ramón **96**. Lehmann **3138** completo después. |
| 5252 | Consejo 321, incluida declaración de Marfán | Acta **158** → Marfán **162**, quien informa de la incorporación posterior de Vergara. Exposición previa de Marfán **1712** y cesión explícita posterior **223** intactas. |

**2788: identidad y cargo no son lo mismo.** La cesión presidencial nombra a Claudio Soto como destinatario y el texto siguiente comienza efectivamente la presentación bajo el cargo subrogante. La nómina, en cambio, lo registra como Gerente de Análisis Macroeconómico. Se identifica localmente a Soto por el antecedente nominal; no se cambia la nómina, no se certifica el cargo subrogante y no se crea un alias global del cargo.

**5252:** asumir temporalmente la presidencia es metadato. La declaración comienza en «haciendo presente que», con Marfán como sujeto nominal contiguo. La mención de Vergara no acredita que ya esté presente ni que intervenga. No se convierte «Presidente» en alias global de Marfán.

## Límites técnicos

Tres tipos adicionales requieren una revisión individual con fecha, hash, evidencia y límites:

1. `RESPUESTA_PASIVA_VARIANTE_REVISADA`: sólo las formas «acotación que es confirmada» y «lo cual es compartido», con coma previa y agente nominal identificable.
2. `DECLARACION_TRAS_ASUNCION_REVISADA`: declaración con antecedente nominal contiguo en la asunción temporal de la presidencia.
3. `INICIO_CARGO_TRAS_CESION_NOMINAL_REVISADA`: comienzo efectivo de la exposición tras una cesión nominal concreta; resuelve localmente el cargo sin generalizarlo.

Las proyecciones sirven únicamente para validar el sujeto. No se exporta una frase reescrita. No se amplían verbos o alias del detector global. Se prueban negativos de pasado, preposición incorrecta, sujeto desconocido, cita abierta, actor incompatible, ausencia de cesión y ausencia de declaración.

`CONTEXTO_REVISADO` no crea anclas globales. `Fin` solo tampoco corta. Se conservan expresamente las anclas posteriores de **2661/1322** y **5252/223**, además de todas las anteriores fuera del alcance modificado.

## Advertencias y lecturas

**68 advertencias contextuales activas = 64 anteriores − 1 archivada + 5 nuevas.**

- **2661:** la advertencia original de Desormeaux 243 queda íntegra en `alertas_contextuales_retiradas.json`, vinculada a su revisión sustituta. Los dos retiros anteriores, 6443 y 2704, permanecen idénticos. La revisión anterior de coordinación en 2661 se conserva idéntica como intervalo adicional cronológico, no se reemplaza.
- **2680/75:** grafía horaria «16; 15» conservada; no corregir la hora ni certificar la numeración de sesión sin cotejo.
- **2788/407:** comienzo concatenado sin punto y final «A continuación,.». Identidad local de Soto no equivale a resolver la discrepancia de cargo.
- **2958/335:** repetición del cierre presidencial y concatenación «y recuerda El señor Presidente», sin reconstrucción.
- **3008/413:** final «A continuación,.» de Larraín, conservado.
- **4055/722:** agradecimiento presidencial, aceptación conjunta con Marshall/Claro/Vergara y acuerdo institucional literal dentro de una fila. La etiqueta De Gregorio es provisional, no autoría exclusiva certificada. Pendiente delimitar el componente institucional y el conjunto; no inventar cuatro turnos individuales.

**28 lecturas actuales = 25 menciones legítimas + 3 pendientes: 6185, 3775 y 4055.** Las nuevas referencias legítimas son 1549 —Marfán evalúa lo comentado por Schmidt-Hebbel— y 2219 —De Gregorio evalúa lo señalado por Marfán—. Ambas se validan contra filas exactas; no figuran en `revision_pendientes.csv` porque no tienen alertas. No se eliminó ningún aviso mediante estas dos lecturas.

García 489 en 2680 conserva también el final «A continuación,.». Se documenta este residuo sin añadirle una advertencia bloqueante que destruya su enlace existente con 2681. El nuevo aviso de ese padre tiene alcance únicamente institucional. No se afirma haber resuelto la integridad textual del desarrollo de García.

### Por qué sube la cola visible

Las filas alertadas pasan de **415 a 423**, en **366 padres** frente a 359. Los aumentos por padre son: 2680 +1; 2788 +2; 2958 +1; 3008 +1; 3288 +1; 4055 +1; 5252 +1. En 2661 se retira la advertencia conjunta, pero la fila de Desormeaux delimitada termina en coma y mantiene un motivo automático de puntuación: no disminuye allí el número de filas alertadas.

Las comas conservadas en los nuevos límites también generan avisos de puntuación; no implican por sí mismas un texto nuevo dañado. **423 alertas no son 423 errores ni un recuento exhaustivo de lo que falta leer.**

## Verificación global

| Control | Resultado |
|---|---:|
| Pruebas | **1403**, todas pasan; 26 nuevas |
| Filas físicas / bloques de texto | **9640 / 9639** |
| Grupos de turno / grupos multifila / máximo | **9222 / 322 / 11** |
| Padres / palabras / sesiones | **7219 / 2048560 / 132**, conservados |
| Intervalos revisados / padres registrados | **363 / 334** |
| Intervalos anteriores conservados | **353**, comparación de intervalos aplanados |
| Advertencias anteriores activas conservadas | **63** y copia completa de 2661 archivada |
| Lecturas anteriores / enlaces revisados anteriores | **25 / 7**, íntegros |
| Nuevos enlaces / enlaces perdidos | **0 / 0** |
| Etiquetas de actor | **55**, sin etiquetas nuevas |
| Esquemas de auditoría / final | **37 / 24** |
| Hashes de entradas/código / salidas verificados | **78 / 11** |
| Otros padres con todos los campos no secuenciales intactos | **7208** |

La comparación cubre todos los campos salvo `ID` e `ID_Turno`, cuya numeración cambia al insertar filas. Sus agrupaciones y enlaces se verifican por separado. Sólo once padres cambian otros campos: los nueve corregidos, 4055 por advertencia y 2681 por antecedente.

El ensayo aislado y la base publicada son idénticos por filas y columnas. F0/F1 pasan; los archivos se publicaron sólo después de superar pruebas y validación en staging. Los CSV de TPM y documentos se compararon salvo sus IDs secuenciales: **310 contrastes TPM**, **21 fórmulas** y **3 documentos** preservados. Larraín autor escrito sigue siendo distinto de Vergara lector, sin inferir asistencia ni intervención oral.

Se mantienen todos los enlaces, incluidos 2680→2681, 224→225→226, 3454→3455, 2695→2696, 2754→2755, 2790→2791, 1386→1387, 2673→2674, 2863→2864, 2796→2797, 2707→2708 y 2963→2964. No se restaura 5402→5403. Los grupos de García de once filas y las exposiciones largas permanecen intactos.

Los controles anteriores de 506/1572, 780, 6009/6025/6443, Ricaurte/4594, Nacrur/Mattar/Álvarez, 4054/3110, Araya/LOOP21, 2463 y 2674 permanecen dentro de las verificaciones de conservación y regresión. Esto no equivale a haberlos releído en esta pasada.

## Histórico y próximos frentes

La cola histórica de 783 conserva sus estados y tipos de revisión: **102 pendientes contextuales**, 497 comparaciones, 183 lecturas dirigidas y 103 triajes; 284 intervalos históricos tienen alertas actuales. Persisten seis intervalos históricos con variante de identidad y 21 filas actuales Ricaurte. Las ocho menciones legítimas históricas no equivalen a las 25 actuales. No sumar estas unidades ni interpretar el estado principal como cierre de todos los residuos.

El descubrimiento usó barridos de pasivas, gerundios y filas institucionales con nombres. La selección institucional produjo 161 filas candidatas, no 161 lecturas completas. El barrido de gerundios dio dos referencias, no dos nuevos turnos. Es búsqueda dirigida, no una muestra independiente con y sin alertas.

Continuar por 4055 —separación institucional/conjunta—, 3775 —conclusión sin sujeto—, 6185 —aporte de Bernier—, cargos y nombres pendientes, y las continuidades 4745→4746 y 6561→6562 sin forzarlas. Un párrafo extenso no está dañado por ser largo; el origen de los textos incompletos requiere cotejo.

## Evidencia publicada

- [Comparación global antes/después](comparacion_loop24_2026-09-08.json)
- [Detalle de filas modificadas](cambios_loop24_2026-09-08.csv)
- [Checkpoint](estado_revision_loop24_2026-09-08.json)
- [Informe anterior LOOP23](REVISION_LOOP23_2026-09-08.md)
- [PR #3](https://github.com/joako0o/nlm_proyect/pull/3)

Sin nuevo cotejo PDF, sin muestra independiente y sin afirmación de pureza exhaustiva. Verificaciones locales; el workflow preexistente no se incorpora al PR.
