# Lote 9 — filas con varios hablantes dentro de un mismo párrafo

## Por qué existe este lote

Todo el trabajo anterior parte del inventario de **límites entre filas**
(`auditar_continuidad_turnos`): pares de filas adyacentes que no están agrupadas. Ese eje
no cubre el caso de **una sola fila que contiene más de un hablante**, que es el otro eje
del encargo.

La única señal que el motor produce sobre ese eje es
`POSIBLE_OTRO_HABLANTE_O_MENCION`, y aparece en **22 filas** de 9.723. Un barrido
independiente sobre la lista de asistencia encuentra **410**. La diferencia es el motivo de
este lote: no se puede usar la alerta del motor como si fuera el universo.

## Medición

`scripts/inventario_multihablante_v7.py` →
`docs/multihablante_v7_2026-09-09/` (`inventario_multihablante_v7.csv`, `resumen.json`).

Para cada fila recorre la lista de asistencia de su sesión, canoniza cada nombre con
`resolve_name` y cuenta cuántas personas distintas del actor de la fila aparecen en el
texto. Canonizar es necesario: el roster trae variantes OCR de una misma persona
(`sergio lehmann beresi`, `sergio lehmann b`, `sergio lehmann`, `lehmann` son una sola), y
sin eso el conteo se infla.

| | |
|---|---:|
| Filas en v7 | 9.723 |
| Con al menos otra persona de la asistencia | 643 |
| — institucionales del Consejo (listas de asistencia) | 233 |
| — **hablantes personales** | **410** |
| Personales con ≥2 otras personas | **71** |
| Personales con ≥3 | 7 |
| Personales con alerta del motor | 4 |
| Personales sin ninguna alerta | 390 |
| Leídas en este lote | **3** |

Distribución de los 410 por cantidad de otras personas: 1 → 339, 2 → 64, 3 → 5, 4 → 1, 5 → 1.

## Qué muestran las tres lecturas

Leí completas las tres filas con más personas, que son también las más largas. **Las tres
son una sola voz.**

**`RPM-2006-06-15:676:1`** (Corbo, 5 personas, 1.308 caracteres). Informa la ausencia de
Velasco, fija la fecha de diciembre, da la bienvenida a Álvarez Vallejos, señala que García
fue invitado y anuncia que expondrán Lehmann y Magendzo. Los cinco nombres son menciones,
una llegada y una entrega de la palabra. Ninguno interviene.

**`RPM-2014-02-18:6009:1`** (Vergara, 4 personas, 1.451 caracteres). Bienvenida a García
Silva, felicitación a Marshall, despedida de Soto, fecha de agosto, palabra a Ricaurte.
Apertura de sesión completa en una sola voz.

**`RPM-2012-02-14:4574:1`** (Vergara, 3 personas, 1.228 caracteres). Bienvenida a Vial,
renovación de Marfán, fecha de agosto, constancia del mensaje de Larraín, paso a Ricaurte.
El motor la marcó con `POSIBLE_OTRO_HABLANTE_O_MENCION`; leída completa, no hay segunda voz.
Es un falso positivo de la alerta.

Las tres confirman la regla ya vigente: una mención, una bienvenida, una llegada o una
entrega de la palabra no son intervención. No se aplicó ningún corte.

## Lo que esto no dice

**No dice que las otras 407 estén bien.** Leí 3 de 410, y las 3 que leí son las más fáciles:
apertura de sesión, estructura repetida, nombres en serie. El resto incluye filas largas de
análisis económico donde un segundo consejero puede intervenir sin que el acta lo introduzca
con la fórmula habitual, que es justo lo que el detector no cubre.

Tampoco es un conjunto de errores. Contar nombres es deliberadamente sensible de más: un
párrafo que cita a cinco economistas extranjeros no tiene cinco hablantes.

## Siguiente paso acotado

Leer las **68 filas restantes con ≥2 personas** (71 menos las 3 leídas), priorizando las 7
con ≥3. Es un universo finito y medido, no una revisión del corpus completo. Cada una
requiere la lectura completa del padre, no de la fila suelta, porque la atribución depende
de quién tenía la palabra antes.

No se generalizó ninguna regla a partir de estas tres lecturas.
