# Revisión de la base de referencia del consolidado RPM

**Fecha:** 2026-09-07
**Base de referencia:** `data/processed/consolidado_base_referencia.xlsx`
**Contenido resultante:** 8,493 intervenciones, a partir de 7,219 filas originales; 843 filas fueron divididas.

## 1. Revisión de los registros `PENDIENTE_REVISION`

Se ajustó la resolución de cargos para preferir la lista de asistencia de la sesión antes que el mapeo global por cargo y fecha. Este cambio corrigió el siguiente caso:

| Identificador original (`ID_Padre`) | Actor asignado anteriormente | Actor corregido | Cargo |
|---|---|---|---|
| 281 | Kevin Cowan Logan | Luis Óscar Herrera Barriga | Gerente de División Política Financiera |

Los registros que permanecen en `PENDIENTE_REVISION` son los siguientes:

| ID | ID_Padre | Actor | Cargo | Motivo |
|---|---|---|---|---|
| 42 | 41 | Klaus Schmidt-Hebbel Dunker | Gerente de Investigación Económica | No aparece en la lista de asistencia de la sesión |
| 262 | 234 | Jorge Pérez Etchegaray | Gerente de Operaciones Monetarias | Invitado a la sesión, no figura en la lista de asistencia |
| 271 | 243 | Jorge Pérez Etchegaray | Gerente de Operaciones Monetarias | Invitado a la sesión, no figura en la lista de asistencia |
| 274 | 246 | Jorge Pérez Etchegaray | Gerente de Operaciones Monetarias | Invitado a la sesión, no figura en la lista de asistencia |
| 467 | 406 | Sergio Lehmann Beresi | Gerente de Análisis Internacional | No figura en la lista de asistencia de la sesión |
| 1165 | 980 | Andrés Velasco Brañes | Ministro de Hacienda | El ministro envió excusas por la mañana e intervino posteriormente |

**Conclusión:** la atribución de persona y cargo en los seis casos es correcta; la marca `PENDIENTE_REVISION` se mantiene porque la lista de asistencia no ofrece una coincidencia única y exacta. Estos registros quedan para verificación manual.

## 2. Auditoría de las filas divididas

### 2.1 Controles automáticos

| Control | Resultado |
|---|---|
| Filas originales divididas | 843 |
| Distribución de fragmentos | 2: 594; 3: 161; 4: 49; 5: 16; 6: 8; 7: 7; 8: 4; 9: 1; 10: 2; 12: 1 |
| Fragmentos vacíos | 0 |
| Registros `LISTA_ASISTENCIA` | 8,021 |
| Registros `ACTA_INSTITUCIONAL` | 466 |
| Registros `PENDIENTE_REVISION` | 6 |

### 2.2 Mejoras aplicadas durante la revisión

1. **Preferencia de la lista de asistencia.** La resolución de cargos sin nombre explícito prioriza la lista de asistencia de la sesión antes del mapeo global. Esto corrigió la asignación errónea al cargo de División Política Financiera.
2. **Reconocimiento de subrogantes.** Grafías como `Gerente de División Política Financiera subrogante señor Luis Opazo` se resuelven al titular real (`Luis Opazo Roco`).
3. **Primer hablante explícito.** Cuando la primera oración de una intervención identifica al hablante, esa señal tiene prioridad sobre heurísticas posteriores del texto.
4. **Exclusión de menciones.** Construcciones como `del Gerente de Análisis Macroeconómico` o `ante la solicitud del señor Ministro` ya no se interpretan como nuevos turnos.
5. **Variantes del apellido Lehmann.** Se incorporaron las variantes OCR `Lehmman`, `Lehemann`, `Lehamann` y `Lehmann B.` para asociarlas a Sergio Lehmann Beresi.
6. **División de transiciones institucionales.** El bloque de acuerdo del Consejo que llegaba pegado al discurso de cierre del Presidente (típico 2013–2015: «Conforme a la votación unánime efectuada por los señores Consejeros, el Consejo adoptó el siguiente Acuerdo …») se separa ahora como fila institucional propia (`Actor_Final` = Consejo). Igual tratamiento reciben la reanudación de sesión («Siendo las 16:00 horas, se reanuda …») y la lectura del comunicado. Esto añadió 157 filas institucionales; ninguna fila perdió su hablante (verificación por `ID_Padre` y texto).

### 2.3 Observaciones menores

- Algunas intervenciones conservan conectores o artefactos OCR al inicio del texto (por ejemplo, `y`, `h el`, `u) el`), heredados de los separadores del documento. No afectan la atribución.

## 3. Compuerta de calidad F0

`scripts/qa_gate_f0.py` verifica tres controles sobre la base de referencia. Veredicto actual: **F0 PASA**.

### 3.1 F0(a) Cardinalidad de actores

`Actor_Final` toma **51 valores: 50 personas + el Consejo del Banco Central de Chile** (466 filas institucionales). El plan original estimaba 60–80 actores: cifra incorrecta, corregida en la documentación. Seis personas aparecen una sola vez (n=1): Alfredo Pistelli, Ari Aisen, María Eugenia Wagner Brizzi, Pablo Pincheira Brown, Rodrigo Alfaro y Rodrigo Álvarez Zenteno.

### 3.2 F0(b) Decisión de TPM por sesión

Cada una de las 132 sesiones debe rendir exactamente una decisión (verbo + Δ pb y/o tasa objetivo) y la fila que la porta debe estar tipificada `ACUERDO_CONSEJO`.

- Detección tolerante a `\s+` (saltos de línea incrustados del PDF) y a espacios OCR dentro de palabras clave («monetari a», «anteri or»), con las variantes «acordó / decidió / resolvió / acuerda / se acuerda» y hasta 60 caracteres entre el verbo del acuerdo y la acción.
- Resultado: **132/132 sesiones con decisión parseada, 0 mis-tipificadas** (antes de la corrección: 79 filas de decisión sin `ACUERDO_CONSEJO`, mezcladas con discursos del Presidente o tipificadas `COMUNICADO`).
- Se excluyen las recapitulaciones del mes anterior («En la última Reunión …», «En la reunión de política monetaria de <mes> …») presentes en la presentación de Opciones.
- Quedan 57 filas de persona marcadas `ACUERDO_CONSEJO`: su discurso porta la fórmula vigente («…deja constancia que se acuerda por unanimidad mantener la tasa … en X% anual»); conservan al hablante conforme al criterio de una intervención por fila.

### 3.3 F0(c) Contraste contra la historia oficial de TPM

Cada decisión se contrasta contra `data/external/tpm_oficial_bcch.csv` (55 cambios efectivos entre 2004-01-09 y 2015-12-18; `fecha_efectiva` = fecha en que la tasa rige, por regla general el día hábil siguiente a la reunión).

- Regla de eficacia: la sesión adopta la siguiente tasa oficial sólo si su fecha efectiva cae dentro de los **10 días** posteriores a la reunión (`CHANGE_WINDOW_DAYS = 10`); si no, mantiene la tasa vigente. Ejemplo: la reunión del 15-07-2014 acuerda bajar a 3,75%, efectiva el 17-07-2014 (2 días después) → adoptada.
- Resultado: **132/132 OK, 0 discrepancias reales.**

Resolución de los 9 casos sospechosos identificados en la iteración previa:

| Sesión | Situación | Resolución |
|---|---|---|
| 2008-02-07 | Acta: «mantener … en 6,25% anual» | **Correcta.** El propio BCCh (página RPM febrero 2008) confirma la mantención en 6,25%; no hubo cambio de tasa entre enero y junio de 2008. El «+25 oficial» anterior era un artefacto de la lógica de expectativa sin ventana de eficacia. |
| 2011-02-17 | Acta: «aumentar … en 0,25% hasta 3,5% anual» | **Correcta.** El delta se expresa en puntos porcentuales, no en puntos base; el parser ahora lo convierte (+25 pb → 3,50%). Efectiva el 18-02-2011. |
| 2009-04-09 | −50 pb → 1,75% | Correcta; efectiva el 13-04-2009 (4 días). |
| 2014-07-15 | −25 pb → 3,75% | Correcta; efectiva el 17-07-2014 (2 días). |
| 2006-04-13, 2008-08-14, 2010-07-15, 2010-09-16, 2014-08-14 | cambios con fecha efectiva 4–5 días después de la reunión | Correctas; la ventana de 10 días los adopta. |

## 4. Veredicto general

La base de referencia queda en condiciones de uso para la siguiente fase. Cada intervención tiene un único `Actor_Final` y un único `Rol_Final`, la trazabilidad está preservada mediante `ID_Padre`, la segmentación conserva íntegro el texto original y la compuerta F0 pasa en sus tres controles (cardinalidad 50 personas + Consejo; 132 decisiones únicas por sesión, 0 mis-tipificadas; 0 discrepancias contra la TPM oficial).

El único indicador de revisión manual pendiente es el conjunto de seis registros `PENDIENTE_REVISION`.
