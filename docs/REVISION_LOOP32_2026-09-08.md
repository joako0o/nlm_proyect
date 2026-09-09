# LOOP32 — Referencias y continuidad pendiente, sin forzar cortes

**Fecha:** 2026-09-08. **PR:** [#3](https://github.com/joako0o/nlm_proyect/pull/3).
**Base congelada:** LOOP31, commit `d8797b9f722e2de80c87d4b1f72b3e0d6c5bec2f`.

## Resultado

**25 fichas nuevas de referencias legítimas y tres advertencias léxicas/sintácticas**,
superpuestas a esas lecturas. Además, cuatro pares candidatos a continuidad leídos
completos, sin forzar enlaces a través de sus advertencias pendientes.

**No se justificaron nuevos cortes o reasignaciones en los casos leídos.** Sus respuestas,
complementos y retornos ya estaban separados; se preservan. No se presentan las lecturas
negativas como correcciones de voz ni se alteran textos para disminuir alertas.

**1.757 pruebas pasan (+53)**. Pipeline completo, F0/F1 y comparación global pasan.
Ensayo aislado y publicación idénticos celda a celda. F0/F1 no certifican pureza semántica
exhaustiva ni integridad textual. **Todos los scripts de producción permanecen idénticos.**

| Unidad | LOOP31 | LOOP32 |
|---|---:|---:|
| Padres de origen | 7.219 | 7.219 |
| Filas físicas / bloques de texto | 9.691 / 9.690 | 9.691 / 9.690 |
| Grupos de turno | 9.257 | 9.257 |
| Grupos multifila / máximo de filas | 338 / 11 | 338 / 11 |
| Filas con alertas / padres alertados | 462 / 392 | 465 / 395 |
| Intervalos personales revisados / padres | 382 / 353 | 382 / 353 |
| Advertencias contextuales | 81 | 84 |
| Lecturas actuales legítimas / pendientes | 73 / 4 | 98 / 4 |
| Fichas de continuidad / documentos / fichas institucionales | 24 / 12 / 4 | 24 / 12 / 4 |
| Archivos de retiros | 3 | 3 |
| Intervalos históricos con alertas actuales | 285 | 285 |
| Pruebas | 1.704 | 1.757 |

## 1. Veinticinco referencias revisadas

Se leyeron los padres completos, no sólo las ventanas del barrido. Cada ficha tiene
fecha, hash, límites exactos y evidencia del padre. Las longitudes son caracteres de
la exportación, no offsets crudos. Ninguna ficha cambia actor, texto o segmentación.

| Padre | Intervalo | Decisión acotada |
|---|---|---|
| 79 | Jadresic 1011 | Responde al comentario de De Gregorio sobre petróleo. El inciso no transfiere la explicación al Vicepresidente. |
| 81 | Desormeaux 767 | Agrega información a la exposición de García sobre tasas. Se conserva «Desorm eaux» literal; no nueva voz de García. |
| 95 | Desormeaux 501 | Añade preocupación sobre empleo al comentario de De Gregorio, que es referencia. |
| 511 | De Gregorio 338 | Explica el comentario de Herrera: «consiste» tiene por sujeto el comentario, no otra intervención de Herrera. |
| 578 | Eyzaguirre 184 | Pregunta a García; el destinatario no es autor de la consulta. La respuesta explícita permanece separada. |
| 611 | Corbo 272 | Comenta lo expuesto por Marfán; la respuesta real de Marfán empieza después, con sujeto propio. |
| 628 | Corbo 283 | Anuncia que Lehmann presentará el informe. El desarrollo de Lehmann 3269 empieza después, con sujeto explícito. |
| 665 | Schmidt-Hebbel 1328 | Coincide con Marfán y refiere escenarios de Larraín Vial y Martín Walter; no participantes adicionales. Aviso textual concurrente abierto. |
| 666 | Jadresic 1608 | Concuerda con Valdés, pero argumenta su propia preferencia por mantener la tasa. |
| 681 | Desormeaux 378 | Consulta si Lehmann entregará información: referencia a una exposición futura, no habla actual del Gerente. |
| 689 | Schmidt-Hebbel 475 | Responde a la explicación de Lehmann sobre compensación inflacionaria. |
| 695 | Valdés 604 | Agrega elementos al análisis de De Gregorio; «agregaría» mantiene a Valdés. |
| 749 | Velasco 771 | Formula una conjetura a partir de la consulta de Desormeaux, sin transferirle su comparación cambiaria. |
| 3102 | Soto 279 | Retorno explícito de Soto después de De Ramón. Se mantienen tres tramos; no se fusionan los dos de Soto a través de la respuesta. |
| 3362 | Céspedes 291 | Confirma a Marshall; «agregando» corresponde a Céspedes. |
| 3473 | Marfán 767 | Se suma a Marshall y Cowan: dos referencias dentro de su argumento, no intervención conjunta de tres personas. |
| 3536 | Claro 710 | Pregunta a Lehmann por QE2 y alude a su interpretación; no respuesta actual de Lehmann dentro de la pregunta. |
| 3655 | Lehmann 218 | Responde a Claro sobre información no publicada por el ECB. La intervención de Claro anterior permanece separada. |
| 4153 | Lehmann 409 | Confirma precios y responde a una consulta de Vergara sobre azúcar; no nueva voz del Consejero. Marfán previo conserva su coma. |
| 5578 | Lehmann 271 | Concuerda con Claro y precisa el papel de Hong Kong; la observación anterior de Claro se mantiene aparte. |
| 6156 | Bernier 392 | Responde a Vergara sobre tipo de cambio. La pregunta presidencial posterior a Raddatz es otro tramo, no parte de Bernier. |
| 6250 | De Ramón 1479 | Coincide con Claro sobre calma financiera, dentro de su propia evaluación de riesgos. Aviso léxico pendiente. |
| 6456 | Vial 394 | Agrega un ejercicio multiplicador al pedido de García. García 828 y la opinión revisada de Vial siguen separados. |
| 6533 | García 399 | Concuerda con Marshall y distingue trayectorias inflacionarias; ambos aportes conservan sus voces. |
| 7096 | Raddatz 720 | Comparte el diagnóstico de Naudon sobre crédito. La aclaración real de Naudon sobre brechas y tasa neutral comienza después. |

**Cuatro fichas nuevas aparecen en la cola:** 628, que ya tenía
`FINAL_SIN_PUNTUACION`, y 665/6250/6456, que incorporan advertencia textual en esta pasada.
Las otras **21 fichas no corresponden a intervalos alertados**. La lectura legítima no
cierra los avisos concurrentes. El padre 4153 tiene puntuación pendiente en Marfán,
no en el intervalo de Lehmann que se revisa aquí.

### Anuncio, exposición y excusas: 627–629

Se leyeron los tres padres completos. 627 conserva el anuncio de una fecha de sesión;
628 separa el anuncio de Corbo y la presentación de **Lehmann 3269**, sin cortar esta
última por longitud. La variante «Sergio Lehmman» permanece literal.

629 conserva a **Velasco 248**, que se incorpora **y formula sus excusas** con sujeto
personal explícito. No se convierte toda llegada en acta institucional por analogía con
4788, ni se aplica el retiro de 6808 a cualquier mención de retirarse. La ficha personal
anterior de 629 sigue idéntica. No se revisan globalmente fechas, nombres o cargos.

## 2. Tres advertencias textuales

- **665 / Schmidt-Hebbel 1328:** «en lo cambiarlo» y «esta actitud cambiarla» en la
  discusión cambiaria. Dudas léxicas/sintácticas para cotejo, sin sustituir palabras.
- **6250 / De Ramón 1479:** «percepción de inexistencia de riego de mercado» en la
  discusión de volatilidad. Se conserva «riego»; no se inserta una palabra supuesta.
- **6456 / Vial 394:** «caída de la inversión se este sector». Se conserva la secuencia;
  no se reconstruye la preposición. El aviso no alcanza a **García 828** anterior.

Son tres avisos `TEXTO_DANADO_POR_COTEJAR` con intervalos y actores exactos. **No son
daños materiales u origen OCR confirmados**, ni cambios de voz. Su registro no certifica
los otros términos o tramos y las lecturas de referencias no los cierran.

**465 = 462 filas alertadas anteriores + tres filas nuevas**. No se elimina puntuación,
no se corrigen cifras o palabras y no se retira ninguna advertencia previa.

## 3. Cuatro pares de continuidad: lectura sin forzar el enlace

El barrido halló cuatro pares aún separados con el mismo actor, extremo previo
`CONTEXTO_REVISADO` y extremo siguiente explícito. Se leyeron completos ambos padres,
incluidas voces ajenas y partes institucionales. **No se agregan fichas de enlace**:
las advertencias actuales impiden aprobarlos bajo los controles vigentes.

| Par | Extremos | Decisión y límite |
|---|---|---|
| 1904→1905 | Cowan 1358→1295 | Desarrollo seguido de recomendación: continuidad plausible. El cargo del tramo previo sigue advertido. De Ramón anterior, su texto y el artefacto «■J» se preservan; no se certifican por leer a Cowan. |
| 2788→2789 | Soto 407→3081 | Recapitulación y noticias de Opciones: continuidad plausible. Sigue el aviso de «A continuación,.» y no se certifica el cargo subrogante. Cierre, reanudación e invitación anteriores quedan aparte. |
| 2803→2804 | De Gregorio 296→158 | Apertura y cesión posterior: no se fuerza a través del aviso textual. Cabecera mixta leída completa, sin promoverla a habla ni modificar su fecha de agenda. |
| 2969→2970 | De Gregorio 301→158 | Apertura y cesión posterior, con reserva textual previa. La exposición posterior de Lehmann en 2970 permanece separada y completa. |

Esto **no demuestra discontinuidad discursiva**: son candidatos plausibles que siguen
sin enlace confirmado. Tampoco justifica borrar advertencias para permitir la unión.
Las pruebas comprueban que proponer esos enlaces con sus motivos actuales provoca un
rechazo, sin cambiar el motor de continuidad. Los extremos revisados siguen sin ancla;
los siguientes conservan la suya y no reciben antecedente.

`CONTEXTO_REVISADO` nunca se convierte en ancla global. Fin solo no corta ni ancla.
No se restauran **5402→5403 ni 600→601**.

## 4. Comparación global

La comparación contra LOOP31 verifica todas las celdas, **sin excluir IDs o columnas**:

- **9.691 filas, 7.219 padres y 2.048.560 palabras conservados**. El cotejo del origen
  ignora sólo espacios; actor, cargo, texto, métodos, segmentos y numeración son idénticos.
- Sólo **tres padres** cambian celdas: `Motivos_Revision` y `Estado_Revision` por sus
  avisos. **7.216 padres son idénticos en todas sus celdas**, incluidos IDs y grupos.
- **Todos los enlaces, grupos y sus miembros son idénticos**. No nuevos cortes,
  reasignaciones, fusiones, anclas o renumeración.
- **382 intervalos personales, 81 advertencias, 77 lecturas, 24 enlaces revisados,
  12 documentos, 4 fichas institucionales y 3 archivos de retiros previos intactos**.
- **86 hashes de entradas/código y 11 de salidas verificados**. Fuentes, fórmulas y
  todos los scripts de producción conservan sus hashes. Sólo cambian registros de
  lectura/advertencia, pruebas, documentación y sus salidas derivadas.
- Esquemas **37/24**, **21 fórmulas**, **310 contrastes TPM**, **132 sesiones** y
  **55 etiquetas** preservados. CSV de **TPM, documentos e histórico783 idénticos byte a
  byte**, incluidos IDs. Autor documental ≠ lector ≠ asistencia; no documentos nuevos.
- Ensayo aislado/publicación idénticos celda a celda. Pipeline completo validado;
  no salidas parciales publicadas.
- Las **462 filas previas de la cola siguen presentes**: 461 completamente idénticas;
  628 añade únicamente los tres campos de anotación de lectura. No pierde su alerta.
  Se agregan 665/6250/6456 con sus avisos y lecturas legítimas concurrentes.

Se preservan García de once filas, los 24 enlaces documentados y también los no
registrados, como 224→225→226, 3454→3455, 2695→2696, 2754→2755, 2790→2791,
1386→1387, 2673→2674, 2863→2864, 2796→2797 y 2680→2681. Se conservan 5003→5004
y las 14 continuidades de LOOP28. **3572 reanudación 235 sigue separada**, al igual que
los movimientos de 4788/6808 frente a las intervenciones reales y al comunicado.
Las fichas 601/3110, la pausa archivada y los retornos 3044/4476/4926 permanecen intactos.
Se verifica su conservación, sin afirmar relectura de todos esos controles en esta pasada.

### Histórico 783, sin cambios de sus intervalos

El CSV es idéntico: no cambian IDs, actores, estados principales, motivos o siguientes
pasos de los 783 intervalos. Se mantiene el cambio de 6808 documentado en LOOP31,
sin revertirlo. Siguen **102 pendientes contextuales**, 497 comparaciones, 183 lecturas
dirigidas, 103 triajes y **285 intervalos con alertas actuales**. Los tres avisos nuevos
no recaen en los intervalos de esa cola histórica.

Continúan seis intervalos con variante y **21 filas actuales** de variantes. Las ocho
menciones históricas no son las 98 actuales. Sólo cambian en el resumen histórico los
contadores globales de la entrega actual: 465 alertas y 102 lecturas. Las unidades
superpuestas no se suman; un estado principal no cierra motivos residuales.

## 5. Alcance y pendientes

Se leyeron **35 padres completos**, incluidos los dos registros de cabecera mixta
2803/2969; no se cuentan como cabeceras adicionales. Padres: 79, 81, 95, 511, 578, 611,
627, 628, 629, 665, 666, 681, 689, 695, 749, 1904, 1905, 2788, 2789, 2803, 2804,
2969, 2970, 3102, 3362, 3473, 3536, 3655, 4153, 5578, 6156, 6250, 6456, 6533, 7096.
Hay fichas nuevas en **25 padres**: los tres avisos se superponen a las lecturas.

Descubrimiento: cuatro pares candidatos a continuidad; 147 coincidencias de términos
procedimentales en filas personales; y 594 ventanas de referencias en padres de hasta
4.000 caracteres sin ficha de mención previa. El barrido institucional fue también
orientativo y no aportó un cambio de voz demostrable. **Estos resultados se superponen,
no son errores confirmados ni lecturas completas de todas sus coincidencias.** El límite
de longitud se usa para seleccionar lecturas, nunca para segmentar las intervenciones.

Quedan **102 lecturas actuales = 98 legítimas + 4 pendientes**: 6185/Bernier,
3775/Cerda, 4055/conjunto-institucional y 2510/conjunto. Siguen pasajes conjuntos,
nombres/cargos, el puente de 780, la reserva de 6119 y demás pendientes anteriores.
No se reparten aportes conjuntos arbitrariamente ni se infiere exclusividad del hablante.

**Sin nuevo cotejo PDF ni muestra independiente con/sin alertas.** Identificar una voz
no certifica OCR; longitud no es daño. Verificaciones locales, sin afirmar CI remota.
Workflow preexistente fuera del PR; no queda proceso activo. Al recuperar el entorno,
todos los archivos se cotejaron con el commit publicado de LOOP31 antes de restaurar
únicamente el índice/rama de Git, sin sobrescribir archivos de trabajo.

## Archivos

- [Base final](../data/processed/consolidado_base_referencia_final.xlsx)
- [Auditoría](../data/processed/consolidado_base_referencia.xlsx)
- [Comparación global](comparacion_loop32_2026-09-08.json)
- [Detalle de los tres avisos](cambios_loop32_2026-09-08.csv)
- [Checkpoint](estado_revision_loop32_2026-09-08.json)
- [Pruebas LOOP32](../tests/test_loop32_review.py)
- [Informe anterior LOOP31](REVISION_LOOP31_2026-09-08.md)
