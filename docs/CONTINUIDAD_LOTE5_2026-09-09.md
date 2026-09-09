# Lote5 — continuidad de la conducción presidencial

**9 de septiembre de 2026 · Entrega `procedimental-v5`**

## Resultado

Se revisaron las **seis reservas restantes del lote4**, leyendo **12 padres completos / 23.450 caracteres**, incluidos todos los miembros de los grupos implicados. La lectura respalda **seis enlaces acotados**: cinco entre padres y uno dentro de 3421.

No se aplican nuevos cortes, reasignaciones de hablante, correcciones de OCR ni cierres de alertas. Las filas siguen separadas físicamente; cambia su agrupación discursiva.

**Entrega vigente:** [`data/releases/continuidad_procedimental_v5/`](../data/releases/continuidad_procedimental_v5/).

- [Excel final](../data/releases/continuidad_procedimental_v5/consolidado_base_referencia_final.xlsx).
- [Excel de auditoría](../data/releases/continuidad_procedimental_v5/consolidado_base_referencia.xlsx).
- [Comparación global contra v4](../data/releases/continuidad_procedimental_v5/comparacion_procedimental.json).
- [Lecturas completas y grupos](continuidad_lote5_2026-09-09/lecturas.json).
- [Seis decisiones](continuidad_lote5_2026-09-09/decisiones.csv).
- [Inventario v4](continuidad_lote5_2026-09-09/inventario_v4.csv) y [nuevo inventario v5](continuidad_lote5_2026-09-09/inventario_v5.csv).
- [Verificación de pruebas, reproducción e históricos](continuidad_lote5_2026-09-09/verificacion.json).

| Métrica | Funcional v4 | Procedimental v5 |
|---|---:|---:|
| Filas físicas | 9.694 | **9.694** |
| Bloques de texto | 9.693 | **9.693** |
| Grupos `ID_Turno` | 9.242 | **9.236** |
| Grupos de varias filas | 352 | **357** |
| Máximo de filas por grupo | 11 | **11** |
| Filas con alertas / padres | 467 / 397 | **467 / 397** |
| Pares inventariados | 77 | **71** |

## Revisión de las seis reservas

En los seis casos habla **José De Gregorio Rebeco**. No se usa la mera coincidencia de actor como evidencia suficiente: se examina la progresión de las frases, la aparición efectiva de otras voces y la delimitación temporal del episodio.

| Enlace aplicado | Evidencia de continuidad | Límite protegido |
|---|---|---|
| **1603:1 → 1604:1**, 13-12-2007 | La oferta general de comentarios de **176** caracteres se concreta en la cesión de **120** a Schmidt-Hebbel. | Su exposición de **6.220** caracteres empieza en1604:2 y permanece separada e íntegra. Magendzo sólo es mencionado en el agradecimiento. |
| **1630:1 → 1631:1**, 10-01-2008 | Agradecimiento/oferta general de **164** y cesión específica de **120**, antes de la respuesta del destinatario. | La exposición de Schmidt-Hebbel de **3.865** caracteres queda fuera. Su referencia a la RPM anterior pertenece a su discurso, no es una interrupción del Presidente. |
| **1840:1 → 1841:1**, 08-05-2008 | La oferta general de **164** se especifica con nombre y cargo de Recart en **134** caracteres. | La Ministra es destinataria de la cesión. La ventana de1842 muestra el inicio posterior de su respuesta; no se incorpora ni se afirma haber leído ese padre completo. |
| **2203:1 → 2204:1**, 11-12-2008 | Las dos cesiones de **150** y **179** designan a Soto para la misma exposición nacional/interna; la primera acaba con `A continuación,.`. | Se conserva la reiteración. El grupo previo **2202:2(134) → 2203:1** se extiende a2204:1. Marshall, **1.796** caracteres en2202:1, y el inicio de Soto en2205 quedan separados. |
| **3269:2 → 3270:1**, 15-07-2010 | La reapertura/bienvenida de **247** caracteres, a las16:00, termina en `A continuación,.`; sigue la cesión de **182** a García. | El cierre de **96** a las13:10 no se une a la tarde. Álvarez recibe la bienvenida, no toma la palabra aquí. La exposición de García de **7.111** empieza después de la cesión y se conserva completa. |
| **3421:5 → 3421:6**, 16-09-2010 | A la reapertura explícita de **108** caracteres sigue `Hace presente…`, reconocimiento de **797**, en nombre del Consejo y del propio Presidente. `Asimismo, el Presidente señor José De Gregorio…` explicita de nuevo el sujeto al dar la bienvenida a Herrera. | La suspensión previa de **201**, Marshall, Opazo y Soto siguen separados. García y Herrera son destinatarios/referentes, no voces intercaladas. El tramo6 conserva `CONTEXTO_REVISADO`, ancla nula y el residuo `Presidente.`. El fragmento de Larraín en3422 no se toca. |

Los doce padres son **1603, 1604, 1630, 1631, 1840, 1841, 2202, 2203, 2204, 3269, 3270 y 3421**. La lectura incluye sus 22 filas de la partición v4, no sólo los 13 miembros de grupos afectados.

### Alcance de la decisión

La agrupación representa **continuidad discursiva en el texto registrado**. No acredita ausencia de silencios o de actos no transcritos. La ausencia de otra voz no se toma por sí sola como prueba: la continuidad se respalda además en la concreción de la cesión, su reiteración con el mismo destinatario o la progresión del Presidente después de reabrir la sesión.

Tampoco se establece que cualquier cambio de función deba agruparse. Las constancias de unanimidad separadas en v4 continúan siendo institucionales y no se absorben. En este lote, la conducción de apertura/cesión/reconocimiento sigue atribuida a la persona que la realiza, sin una nueva decisión institucional en esos extremos.

## Inventario actualizado: mismo número no significaba mismos pares

Entre v3 y v4 había **77 pares en ambas bases, pero sólo 74 comunes**. Los tres pares antiguos que terminaban en filas mixtas fueron reemplazados por los límites internos aporte/constancia de4788,4849 y4899. El [resumen de lectura](continuidad_lote5_2026-09-09/resumen_lectura.json) enumera ambos conjuntos.

De v4 a v5 se retiran del inventario **exactamente los seis pares aplicados**; no aparece ningún par adicional. Quedan **71**, no71 errores ni71 casos nunca leídos. Entre ellos permanecen separaciones temporales respaldadas, las constancias v4 y las reservas complejas de revisiones anteriores.

Las dos alertas por constancias idénticas y el aviso del pie de página de4788 siguen visibles. No se usa esta revisión para deduplicar texto ni reducir artificialmente la cola.

## Implementación acotada y controles

El [registro v5](../data/curation/continuidades_procedimentales_v5.json) fija seis pares exactos y enlaza los hashes de la lectura, la base v4 y el registro funcional anterior.

- El motor histórico de segmentación y continuidad se ejecuta sin modificar sus reglas. Después, un adaptador exige los extremos y **todos los miembros anteriores** de cada grupo antes de aplicar los seis enlaces.
- La relación nueva es `CONTINUIDAD_PROCEDIMENTAL_REVISADA`. No cambia ninguna `Fuente_Actor` ni `ID_Ancla_Actor`; especialmente, **el contexto de3421:6 no se convierte en ancla ni en regla de propagación**.
- La expresión global que detecta `ofrece la palabra`, apertura y reanudación permanece intacta. F1 sólo exceptúa su barrera para la prueba exacta y la relación nueva correspondientes; continúa rechazando el resto de las barreras, tipos institucionales, advertencias, actores o sesiones incompatibles.
- **F1 sin las seis pruebas rechaza la salida v5**. Cambiar el texto, actor, cargo, fuente, ancla o alerta invalida la coincidencia. No basta declarar la relación nueva.
- El comparador independiente verifica la membresía de **todos los grupos**, el orden de todas las filas, todos los campos y la numeración determinista de `ID_Turno`.

La comparación da **seis uniones, 12 celdas relacionales modificadas, 147 etiquetas de turno renumeradas y 13 filas con compañeros de grupo distintos**. Las147 etiquetas no son147 enlaces; los IDs físicos, segmentos y bloques no se renumeran. No se divide ningún grupo anterior ni se modifica otro campo.

Se conservan las **24 pruebas revisadas entre padres**, las **15 intrapadre** y los **tres refinamientos con continuidad personal de v4**. Las seis pruebas nuevas se registran por separado: no se reescriben los archivos históricos. Quedan protegidas las presentaciones extensas y los grupos de García de hasta once filas, los casos ambiguos y los enlaces anteriores; no se restauran600→601 ni5402→5403.

## Validaciones ejecutadas

- **25 pruebas nuevas**: alcance, lectura completa, hashes, mutaciones, pertenencia global, tipos/avisos, anclas, cesiones, pausas, otras voces, perfiles históricos y rechazo de publicación anticipada. Prueba dirigida preliminar: PASS, **64,037 s**; las dos ejecuciones completas siguientes incluyen la comprobación de797 caracteres en3421:6.
- Primera construcción aislada: **2.082 pruebas PASS, 362,641 s**; F0, comparación global y F1 PASS.
- Segunda construcción y publicación: **2.082 pruebas PASS, 365,439 s**; los mismos controles PASS.
- Tres XLSX: **todas sus hojas y celdas idénticas** entre construcciones. Cinco CSV, JSONL y JSON de QA/resumen: **idénticos byte a byte**.
- La comparación difiere sólo en el SHA binario del XLSX candidato. Ambos manifiestos verifican **123 entradas/código y 12 salidas**; el manifiesto completa los13 archivos publicados.
- Tres exportaciones de lectura reproducidas. Se comprobó que el inventario final es exactamente el de v4 menos los seis pares.
- **84 archivos de datos y257 documentos/artefactos anteriores intactos byte a byte**. Sólo cambian tres scripts anteriores: constructor, runner y QA; otros33 se conservan. Se añaden el adaptador/lector, el comparador y su archivo de pruebas.

Antes de la entrega se corrigió una cifra descriptiva de la justificación de3421:6: **797 caracteres**, no773. Los textos, límites y enlaces de las construcciones preliminares ya eran íntegros. Se conservan esas salidas en staging y se repitieron las dos construcciones completas con la evidencia y su hash corregidos; los resultados anteriores corresponden a estas ejecuciones finales.

SHA-256 de la base de auditoría publicada:
`4da18c4e86f583fdf4d5d0cd9be49b9aac20fb40379cd391b5f4c7763cf9e168`.

## Reproducción

```bash
.venv/bin/python scripts/preparar_data.py \
  --perfil procedimental-v5 \
  --destino .cache/reproduccion_procedimental_v5
```

El destino debe ser nuevo, bajo `.cache/` o `data/releases/`. La publicación se hace sólo después de superar pruebas y controles. V5 requiere las pruebas intrapadre v3 y el refinamiento funcional v4. Los perfiles anteriores, incluido `funcional-v4`, eliminan la activación ambiental de v5.

Para reproducir únicamente la lectura/inventario **previos a la aplicación**, sin construir datos:

```bash
.venv/bin/python scripts/reviewed_procedural_v5.py \
  --salida .cache/reproduccion_lectura_lote5
```

## Qué sigue pendiente

Las nueve reservas originales del lote4 tienen ahora tratamiento: tres refinamientos en v4 y estas seis continuidades en v5. **Eso no termina la revisión del corpus.** Continúan abiertas las reservas complejas, incluidas780,2661,2863,3646 y5252, y las dudas textuales/de atribución que requieren otras lecturas o cotejo documental.

No hubo subagentes, segundo revisor semántico ni nuevo cotejo PDF. La recuperación técnica de los PDFs ya disponibles, realizada por el pipeline, no se presenta como nueva evidencia documental para estos seis enlaces.
