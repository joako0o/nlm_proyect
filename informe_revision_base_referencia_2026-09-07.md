# Revisión de la base de referencia del consolidado RPM

**Fecha:** 2026-09-07
**Base de referencia:** `consolidado_base_referencia.xlsx`
**Contenido resultante:** 8,302 intervenciones, a partir de 7,219 filas originales; 708 filas fueron divididas.

## 1. Revisión de los registros `PENDIENTE_REVISION`

Se ajustó la resolución de cargos para preferir la lista de asistencia de la sesión antes que el mapeo global por cargo y fecha. Este cambio corrigió el siguiente caso:

| Identificador original | Actor asignado anteriormente | Actor corregido | Cargo |
|---|---|---|---|
| 281 | Kevin Cowan Logan | Luis Óscar Herrera Barriga | Gerente de División Política Financiera |

Los registros que permanecen en `PENDIENTE_REVISION` son los siguientes:

| Identificador | Actor | Cargo | Motivo |
|---|---|---|---|
| 41 | Klaus Schmidt-Hebbel Dunker | Gerente de Investigación Económica | No aparece en la lista de asistencia de la sesión |
| 234 | Jorge Pérez Etchegaray | Gerente de Operaciones Monetarias | Invitado a la sesión, no figura en la lista de asistencia |
| 243 | Jorge Pérez Etchegaray | Gerente de Operaciones Monetarias | Invitado a la sesión, no figura en la lista de asistencia |
| 246 | Jorge Pérez Etchegaray | Gerente de Operaciones Monetarias | Invitado a la sesión, no figura en la lista de asistencia |
| 406 | Sergio Lehmann Beresi | Gerente de Análisis Internacional | No figura en la lista de asistencia de la sesión |
| 980 | Andrés Velasco Brañes | Ministro de Hacienda | El ministro envió excusas por la mañana e intervino posteriormente |

**Conclusión:** la atribución de persona y cargo en los seis casos es correcta; la marca `PENDIENTE_REVISION` se mantiene porque la lista de asistencia no ofrece una coincidencia única y exacta. Estos registros quedan para verificación manual.

## 2. Auditoría de las filas divididas

### 2.1 Controles automáticos

| Control | Resultado |
|---|---|
| Filas originales divididas | 708 |
| Distribución de fragmentos | 2: 500; 3: 129; 4: 42; 5: 16; 6: 7; 7: 7; 8: 3; 9: 1; 10: 2; 12: 1 |
| Fragmentos vacíos | 0 |
| Fragmentos menores a 45 caracteres | 1 (corresponde a una intervención corta legítima) |
| Fragmentos consecutivos con el mismo hablante | 5 |
| Registros `LISTA_ASISTENCIA` | 7,987 |
| Registros `ACTA_INSTITUCIONAL` | 309 |
| Registros `PENDIENTE_REVISION` | 6 |

### 2.2 Mejoras aplicadas durante la revisión

1. **Preferencia de la lista de asistencia.** La resolución de cargos sin nombre explícito prioriza la lista de asistencia de la sesión antes del mapeo global. Esto corrigió la asignación errónea al cargo de División Política Financiera.
2. **Reconocimiento de subrogantes.** Grafías como `Gerente de División Política Financiera subrogante señor Luis Opazo` se resuelven al titular real (`Luis Opazo Roco`).
3. **Primer hablante explícito.** Cuando la primera oración de una intervención identifica al hablante, esa señal tiene prioridad sobre heurísticas posteriores del texto.
4. **Exclusión de menciones.** Construcciones como `del Gerente de Análisis Macroeconómico` o `ante la solicitud del señor Ministro` ya no se interpretan como nuevos turnos.
5. **Variantes del apellido Lehmann.** Se incorporaron las variantes OCR `Lehmman`, `Lehemann`, `Lehamann` y `Lehmann B.` para asociarlas a Sergio Lehmann Beresi.

### 2.3 Observaciones menores

- Existen **5 pares de fragmentos consecutivos con el mismo hablante**. Corresponden a dos turnos cortos o a dos preguntas sucesivas de la misma persona; no implican pérdida de texto.
- Algunas intervenciones conservan conectores o artefactos OCR al inicio del texto (por ejemplo, `y`, `h el`, `u) el`), heredados de los separadores del documento. No afectan la atribución.

## 3. Veredicto general

La base de referencia queda en condiciones de uso para la siguiente fase. Cada intervención tiene un único `Actor_Final` y un único `Rol_Final`, la trazabilidad está preservada mediante `ID_Padre`, y la segmentación conserva íntegro el texto original.

El único indicador de revisión manual pendiente es el conjunto de seis registros `PENDIENTE_REVISION`.
