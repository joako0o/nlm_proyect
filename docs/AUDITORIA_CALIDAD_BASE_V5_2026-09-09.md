# Auditoría de calidad de la base v5

**Fecha:** 9 de septiembre de 2026  
**Base auditada:** `data/releases/continuidad_procedimental_v5/`  
**Alcance:** controles estructurales, trazabilidad, atribución, continuidad y alertas. Esta auditoría identifica puntos de trabajo; no certifica pureza semántica total.

## 1. Resultado ejecutivo

Los controles bloqueantes de la base pasan y no se observan errores técnicos registrados. La base conserva los 7.219 padres originales y 2.048.560 palabras, sin pérdida de texto salvo la normalización explícita de espacios usada por el control de conservación.

El principal riesgo pendiente no es estructural sino semántico: todavía existen párrafos o grupos donde una mención, una narración de acta, una cesión o una constancia institucional podrían confundirse con una intervención efectiva. Por eso el QA mantiene el estado `REQUIERE_REVISION_DIRIGIDA`.

## 2. Métricas verificadas

| Control | Resultado |
|---|---:|
| Padres originales | 7.219 |
| Sesiones | 132 |
| Filas procesadas | 9.694 |
| Bloques de texto | 9.693 |
| Grupos `ID_Turno` | 9.236 |
| Grupos multipárrafo | 357 |
| Máximo de filas por grupo | 11 |
| Palabras | 2.048.560 |
| Padres con texto conservado | 7.219 |
| Filas con alertas | 467 |
| Padres con alertas | 397 |
| Actores | 55 |
| Columnas de auditoría / finales | 37 / 24 |
| Continuidades entre padres revisadas | 24 |
| Continuidades intrapadre revisadas | 15 |
| Continuidades procedimentales aplicadas | 6 |
| Refinamientos funcionales aplicados | 3 |
| Pruebas F0 | PASS |
| Controles bloqueantes | PASS |

## 3. Puntos de calidad positivos

- La cardinalidad de los padres originales se conserva.
- La comparación v5 limita los cambios a seis continuidades documentadas y sus campos derivados.
- Los tres refinamientos funcionales de v4 mantienen al Presidente como hablante y separan la constancia institucional sin reasignarla automáticamente al Consejo.
- Las alertas permanecen visibles; no se deduplican textos legítimos ni se cierran avisos por conveniencia.
- Se conservan las presentaciones largas y grupos de hasta once filas.
- Las fuentes contextuales y las anclas nulas se preservan en los casos revisados.
- El lote 6 mantiene abiertas las reservas de 780, 2661 y 5252.

## 4. Riesgos y puntos a trabajar

### Prioridad 1 — continuidad pendiente ya documentada

Implementar y validar, en una nueva salida basada en v5:

- `2863:2 → 2863:3`, conservando `2863:3 → 2864:1` y dejando separada la pregunta de Marfán.
- `3646:2 → 3646:3`, sin convertir la confirmación narrativa en cita hablada ni incorporar los retornos de Claro.

La expectativa es pasar de 9.236 a 9.234 grupos, pero debe confirmarse mediante comparación global, no asumirse.

### Prioridad 2 — reservas que no deben resolverse por inferencia

- **780:** comienzo ambiguo de Corbo; requiere cotejo de la transición en el acta.
- **2661:** confirmación narrada sin palabras ni modalidad explícita; mantener separada.
- **5252:** frontera abierta entre narración del acta y aporte personal; revisar función textual antes de unir.

### Prioridad 3 — revisión de atribución contextual

Hay 382 filas con fuente `CONTEXTO_REVISADO`. No son automáticamente errores, pero deben priorizarse cuando además exista:

- `POSIBLE_OTRO_HABLANTE_O_MENCION`;
- una cesión o reanudación;
- tipo `ACUERDO_CONSEJO`, `COMUNICADO` o `ACTA_INSTITUCIONAL`;
- cambio de función dentro del mismo padre;
- retorno de un hablante tras una intervención de otra persona.

`CONTEXTO_REVISADO` no debe convertirse en ancla global sólo por proximidad.

### Prioridad 4 — texto institucional y documental

La base contiene 199 segmentos `ACUERDO_CONSEJO`, 91 `COMUNICADO`, 8 `ACTA_INSTITUCIONAL`, 12 `OPINION_ESCRITA` y 3 `MINUTA_PERSONAL`. Debe revisarse la separación entre:

- voz personal;
- narración del acta;
- constancia del Consejo;
- documento leído o escrito;
- persona mencionada que no toma la palabra.

### Prioridad 5 — alertas

Las 467 filas alertadas no equivalen a 467 errores. Las alertas se superponen y deben desagregarse por padre y motivo. Los duplicados exactos y las fórmulas repetidas deben mantenerse visibles hasta demostrar que son errores de datos, no eliminarse automáticamente.

## 5. Orden de trabajo recomendado

1. Implementar las dos propuestas del lote 6 en una versión v6 aislada.
2. Ejecutar pruebas específicas de miembros, fuentes, anclas, barreras y reservas.
3. Ejecutar suite completa, F0, comparación global y F1.
4. Generar una cola de padres con señales combinadas de posible mezcla de voces.
5. Leer padres completos, no sólo ventanas, y clasificar cada caso como continuidad, separación, reserva o sin decisión.
6. Publicar sólo correcciones respaldadas y mantener v5 intacta.

## 6. Límites de esta auditoría

- No se realizó un nuevo cotejo sistemático con los PDF.
- Las pruebas técnicas no equivalen a un segundo revisor semántico.
- No es válido calcular un porcentaje de corpus semánticamente revisado a partir de alertas o fuentes.
- Una fila sin alerta no implica revisión humana completa.
- Una alerta no implica necesariamente un error.

**Conclusión:** la base v5 es técnicamente consistente y reproducible, pero requiere una nueva fase de revisión semántica dirigida para resolver mezclas de voces y funciones textuales. El trabajo inmediato son las dos continuidades aprobadas del lote 6; después debe abordarse una cola priorizada de párrafos mixtos.
