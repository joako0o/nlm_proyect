# Revisión Gold RPM — 2026-09-07

**Archivo:** `consolidado_goldstandard.xlsx`
**Filas resultantes:** 8,302 intervenciones (7,219 filas originales; 708 divididas)
**Estado:** revisión de los 6 `PENDIENTE_REVISION` y auditoría de los 708 padres divididos.

---

## 1. Revisión de los casos `PENDIENTE_REVISION`

Solución aplicada: `actor_for_role()` ahora prefiere primero la lista de asistencia de la sesión
(vía `_roster_actor_for_role`) antes que el mapeo global por rol/fecha. Esto corrigió el caso que
era realmente un error de etiquetado.

| ID nuevo | Padre | Actor | Rol | Veredicto |
|---|---|---|---|---|
| 311 | 281 | ~~Kevin Cowan Logan~~ → **Luis Óscar Herrera Barriga** | Gerente de División Política Financiera | **Corregido** en esta revisión |
| 41 | 41 | Klaus Schmidt-Hebbel Dunker | Gerente de Investigación Económica | Legítimo: no aparece en la lista de asistencia de 2005-01-11 |
| 258/267/270 | 234/243/246 | Jorge Pérez Etchegaray | Gerente de Operaciones Monetarias | Legítimo: invitado a la sesión, no figura en el párrafo de asistencia |
| 456 | 406 | Sergio Lehmann Beresi | Gerente de Análisis Internacional | Legítimo: no figura en la lista de asistencia de 2005-10-11 |
| 1128 | 980 | Andrés Velasco Brañes | Ministro de Hacienda | Legítimo: el ministro envió excusas en la mañana; interviene más tarde |

**Conclusión:** quedan **6** `PENDIENTE_REVISION`, todos por no tener cargo único/exacto en la
lista de asistencia (invitados, ausentes que llegan tarde, o lista OCR incompleta). No son
errores de actor: el actor y el rol detectados son correctos. Deben quedar para revisión manual.

---

## 2. Auditoría de los 708 padres divididos

### 2.1 Controles automáticos

| Control | Resultado |
|---|---|
| Parentes divididos | 708 |
| Distribución | 2→500, 3→129, 4→42, 5→16, 6→7, 7→7, 8→3, 9→1, 10→2, 12→1 |
| Segmentos vacíos o solo espacios | 0 |
| Segmentos de <45 caracteres | 1 (`El señor Lehmann lo confirma.`, legítimo) |
| Segmentos consecutivos con el mismo actor | **5** |
| `LISTA_ASISTENCIA` | 7,987 |
| `ACTA_INSTITUCIONAL` | 309 |
| `PENDIENTE_REVISION` | 6 |

### 2.2 Mejoras aplicadas durante la revisión

1. **Preferir lista de asistencia para cargos sin nombre**
   - `_roster_actor_for_role` resuelve rol→actor por la sesión antes de usar el mapeo global.
   - Esto corrigió el caso `Gerente de División Política Financiera` que se asignaba a Kevin Cowan
     en vez de Luis Óscar Herrera.

2. **Reconocer subrogantes en rol + nombre**
   - "Gerente de División Política Financiera **subrogante señor Luis Opazo**" ahora resuelve a
     `Luis Opazo Roco` (antes caía a un cargo por fecha).

3. **Primer hablante explícito de cada intervención**
   - Nueva fuente `PRIMERA_ORACION` (54 filas): si la primera oración ya tiene hablante explícito
     claro, se prioriza sobre heurísticas posteriores.
   - Esto corrigió bloques tipo `El Presidente señala que... por el Gerente señor Lehmann...` que
     se atribuían a Lehmann.

4. **No tratar menciones como turnos**
   - `del Gerente de Análisis Macroeconómico...`, `ante la solicitud del señor Ministro...` ya no
     se consideran hablantes; se prefiere el sujeto explícito posterior (p. ej. el Consejero
     Marfán).

5. **Alias OCR del apellido Lehmann**
   - Se agregaron `lehmman`, `lehemann`, `lehamann`, `lehmann b.` → Sergio Lehmann Beresi,
     corrigiendo el OCR `Lehmman` en varias actas.

### 2.3 Puntos que quedan como observación (no errores críticos)

- **5 pares consecutivos con el mismo actor**: corresponden a dos intervenciones cortas del mismo
  hablante o a dos preguntas sucesivas (p. ej. dos turnos de Sebastián Claro o dos turnos de
  Manuel Marfán). No hay pérdida de texto; son revisables si se quiere una granularidad aún más fina.
- **93 intervenciones** arrancan con un conector/artefacto OCR (`y`, `d el`, `u) el`, `h el`)
  heredado de los separadores del acta. El contenido y el actor son correctos; es ruido de texto,
  no de clasificación.

---

## 3. Veredicto general

La base queda en **estado correcto para una siguiente fase**: cada intervención tiene un único
actor y rol, la trazabilidad está preservada por `ID_Padre`, y el único indicador de revisión
manual es el conjunto de 6 casos sin cargo único en la lista de asistencia.

**No se detectaron filas perdidas por la segmentación** y los 708 padres divididos mantienen
texto íntegro (la suma de los segmentos reproduce el texto original).

### Próximo paso sugerido
Revisar manualmente los 6 `PENDIENTE_REVISION` (decidir si se completa el cargo desde el texto o
si se deja como `PENDIENTE_REVISION` permanente) y, opcionalmente, unir los 5 pares consecutivos
de mismo actor que correspondan a una sola intervención.
