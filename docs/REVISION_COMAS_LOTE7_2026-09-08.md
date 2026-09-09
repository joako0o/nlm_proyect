# Revisión por riesgo — lote 7: tres comas con reservas (2026-09-08)

**Base:** `302016680b5d43bc0dea7d157055b86661da1d7e` (lote 6).
**Datos:** LOOP32 (`1b02496`), sin cambios ni regeneración.

## Resultado

Se releyeron **2680, 2779 y 2957 completos (5.022 caracteres de origen)**, sus **seis intervalos vecinos exportados completos (18.783 caracteres)** y las **cabeceras completas 2656 y 2889 (3.053 caracteres de origen)**. Se contrastaron seis registros de curación anteriores, incluidas las advertencias vigentes y las decisiones de LOOP18/LOOP24.

Los tres límites están diferenciados en el texto y respaldan la separación existente. **Eso no resuelve por sí solo la integridad textual, la modalidad de un asentimiento o la identidad del nombre dañado.**

| Foco | Decisión sobre el límite | Reserva que sigue abierta |
|---|---|---|
| **2680:2** | Acta de reanudación → cesión presidencial, separadas. | Grafía horaria y numeración de sesión por cotejar. |
| **2779:2** | Asentimiento narrado de Soto → respuesta contrastiva de Marshall. | No hay palabras transcritas de Soto; no se determina si asintió verbalmente o mediante un gesto. |
| **2957:2** | Pregunta con «Rabio García» → respuesta presidencial, diferenciadas. | La atribución actual a Pablo García sigue siendo **local y provisional**; nombre literal pendiente de cotejo. |

Se registran **tres fichas con tres reservas abiertas**, no tres errores corregidos ni tres identidades confirmadas. No hay nuevos cortes, enlaces, reasignaciones o cierres. Los motivos originales permanecen, también cuando son dobles.

La subcola anterior **sigue siendo 167/167 con ficha y cero sin ficha**. Estos tres casos están fuera de ella por tener motivos adicionales; no se eliminan esos motivos para incorporarlos a los validadores anteriores. Sus estados no equivalen a certificación global del corpus.

## 2680: límite institucional claro, hora y número sin reparar

Se conserva:

**Presidente 180 → acta 75 → Presidente 164 → García 489 → continuación de García en 2681 de 11.085 caracteres.**

El Presidente anuncia el horario; el acta narra la reanudación; «y el señor Presidente ofrece la palabra…» constituye la cesión personal. García empieza después, en «El Gerente señor Pablo García, comienza a dar lectura…». Nombrarlo en la cesión no anticipa su intervención.

La lectura confirma dos reservas textuales:

- el pasaje de reanudación conserva **`16; 15`**, mientras el anuncio previo dice `16:15`;
- el pasaje dice **`N° 141`**, mientras la cabecera completa de la misma fecha, 2656, dice **`N° 142`**.

No se elige una versión como correcta sin cotejo. La advertencia `TEXTO_DANADO_POR_COTEJAR` ya documentada en LOOP24 sigue acotada al tramo institucional, junto con `FINAL_SIN_PUNTUACION`.

García 489 conserva `A continuación,.` y el enlace **2680→2681**. Se leyó todo el intervalo siguiente de **11.085 caracteres**, sin partirlo por noticias internacionales, actividad, precios, crédito o medidas de política. Sus residuos —por ejemplo, `nesgo`, `vanos` y la secuencia de comillas y `v`— no quedan certificados por la lectura. No se añade una alerta bloqueante que destruya la continuidad previamente respaldada.

**Acción pendiente:** cotejar hora y numeración en la fuente primaria, manteniendo las separaciones y la exposición actual mientras tanto.

## 2779: conservar el asentimiento sin inventar palabras

Se conserva **Cowan 222 → Soto 22 → Marshall 366**.

La cláusula literal es **«El señor Soto asiente,»**. Identifica un acto de Soto, pero no transcribe un «sí» ni otra respuesta verbal. Puede representar un asentimiento verbal o gestual: el texto no lo determina. Por eso no se elimina por breve, pero tampoco se presenta como una cita de palabras pronunciadas.

«mientras que el Consejero señor Enrique Marshall responde…» introduce la respuesta contrastiva de Marshall; «En su opinión» continúa ese aporte. No pertenece a Cowan ni a Soto. El registro anterior `HAB-20260907-2779` ya explicitaba que Soto asiente **sin palabras transcritas**; esta relectura conserva esa distinción.

Soto mantiene `FINAL_SIN_PUNTUACION;FRAGMENTO_BREVE`; Marshall mantiene `CONTEXTO_REVISADO` y ancla nula. El desarrollo previo de Soto en **2778:3 (1.810 caracteres)** y su retorno en **2780:1 (4.676)** se conservan, sin fusionarlos a través de Cowan o Marshall. Los términos literales del vecino —incluidos `IRC`, `IRCX1` y `senes`— no se corrigen.

**Acción analítica:** distinguir un asentimiento narrado de una cita verbal. La ficha no cambia todavía los campos productivos ni los recuentos de palabras del corpus.

## 2957: límite respaldado, atribución provisional

Se conserva **Cowan 772 → García provisional 73 → Presidente 117 → Marfán 907 → Soto 1.626**.

«El señor **Rabio García** consulta si este análisis se incluirá en la Minuta,» es una pregunta diferenciada de Cowan. «señalando el señor Presidente que no correspondería hacerlo…» abre una respuesta distinta. Marfán interviene después sobre qué debería publicarse; Soto retoma finalmente la exposición de expectativas.

LOOP18 ya delimitó la pregunta y la respuesta, asignó localmente la primera a Pablo García y conservó `NOMBRE_EN_DISCURSO_POR_VERIFICAR`. Se revisó esa justificación y la cabecera 2889 utilizada como antecedente. La nómina contiene a **Pablo García Silva**, pero también a **Mariana García Schmidt**: una lista de asistencia y un apellido **no certifican por sí solos** la identidad del pasaje dañado. Esto tampoco constituye evidencia para reasignarlo a Mariana.

Se mantiene la atribución actual a Pablo García **como provisional**, sin sustituir `Rabio`, crear un alias global o convertir `CONTEXTO_REVISADO` en ancla. Pregunta y respuesta conservan anclas nulas. La separación de los actos no se confunde con una nueva resolución de identidad.

El enlace de Cowan **2956→2957** permanece. El vecino 2958 mantiene su repetición y `TEXTO_DANADO_POR_COTEJAR`; no se repara ese cierre por proximidad.

**Acción pendiente:** cotejar el nombre en la fuente primaria antes de confirmar identidad o modificar el OCR. No se obtuvo nuevo cotejo PDF en este lote.

## Qué cambia en el seguimiento, no en los datos

Se añade [`scripts/revisar_comas_con_reservas.py`](../scripts/revisar_comas_con_reservas.py), con inventario cerrado de estos tres focos. Reutiliza las huellas de partición y las relaciones locales de los helpers anteriores, **sin modificarlos** ni ampliar sus criterios de admisión.

La tabla de riesgos separa:

1. **Estado del límite:** separación existente respaldada.
2. **Estado de identidad:** no hay nueva resolución; en 2957 se exige explícitamente atribución provisional.
3. **Naturaleza del pasaje:** acta/cesión, asentimiento sin palabras transcritas o pregunta/respuesta.
4. **Reserva abierta y siguiente acción.**

El validador exige los motivos adicionales originales, texto completo del padre, vecinos, cabeceras pertinentes y equivalencias de turno de todos los pares locales. Contrasta además los seis antecedentes por identificador, fuente, justificación y huella, incluyendo la respuesta presidencial anidada en el registro de 2957. Rechaza cerrar reservas o promover identidad/modalidad mediante un cambio de estado de la ficha, así como eliminar el motivo adicional para forzar una aprobación.

No es un detector general de asentimientos, gerundios o nombres dañados, ni una nueva capa de atribución aplicada al pipeline. Las reservas de otros lotes y las prohibiciones de enlaces o alias siguen vigentes.

## Validación

- **1.897 pruebas locales pasan (+19), en 105,255 s.** Cubren dimensiones separadas, conservación de motivos y textos, cambios en extremos/vecinos/cabeceras, antecedentes, anclas, fusiones indebidas, pérdida de continuidad, rechazos de los validadores anteriores y reproducción sin sobrescritura.
- Los **27 archivos de datos versionados**, incluido TPM externo, los **30 artefactos de los seis lotes anteriores** y ambos validadores anteriores son idénticos byte a byte a `3020166`.
- Las dos exportaciones nuevas se reprodujeron byte a byte. No se sobrescribieron los lotes previos.
- **9.691 filas; 465 filas alertadas / 395 padres alertados; cero cierres.** Sin nuevo pipeline productivo, F0/F1, CI remota, cotejo PDF o revisión humana independiente. Base, QA y manifiesto siguen en LOOP32.

## Siguiente paso recomendado

Continuar con la **auditoría cruzada de continuidad y alternancias**, priorizando casos donde una fusión o fragmentación pueda cambiar quién recibe el texto. Los nombres y colas que necesiten evidencia primaria deben conservar una ruta de cotejo aparte, sin bloquear ni dar por resuelto el resto del corpus.

No conviene seguir usando sólo el total de alertas como indicador: este lote muestra que una alerta de nombre, una cláusula breve sin palabras transcritas y una grafía horaria requieren decisiones distintas. Las nuevas fichas registran esa diferencia; no convierten las tres reservas en casos cerrados.

## Artefactos y reproducción

- [Tres fichas, padres, vecinos, cabeceras y antecedentes](revision_comas_lote7_2026-09-08/revisiones.json)
- [Tabla de riesgos abiertos y siguientes acciones](revision_comas_lote7_2026-09-08/riesgos_abiertos.csv)
- [Resumen](revision_comas_lote7_2026-09-08/resumen.json) · [Verificación y huellas](revision_comas_lote7_2026-09-08/verificacion.json)

```bash
.venv/bin/python scripts/revisar_comas_con_reservas.py \
  --revisiones docs/revision_comas_lote7_2026-09-08/revisiones.json \
  --salida .cache/revision_comas7_repro
.venv/bin/python -m unittest discover -s tests
```

La salida debe ser nueva: el CLI rechaza sobrescribir entradas o exportaciones existentes.
