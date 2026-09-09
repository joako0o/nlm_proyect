# Continuidad — lote2 y entrega intrapadre v2

**9 de septiembre de 2026. Estado: cuatro enlaces nuevos aplicados y validados.**
La entrega vigente está en [`data/releases/continuidad_intrapadre_v2/`](../data/releases/continuidad_intrapadre_v2/).

[Excel final](../data/releases/continuidad_intrapadre_v2/consolidado_base_referencia_final.xlsx) ·
[Excel de auditoría](../data/releases/continuidad_intrapadre_v2/consolidado_base_referencia.xlsx) ·
[QA](../data/releases/continuidad_intrapadre_v2/qa_preparacion.json) ·
[Comparación global](../data/releases/continuidad_intrapadre_v2/comparacion_intrapadre.json).

## Lectura realizada

Se actualizó el inventario sobre **v1**, no sobre LOOP32: **90 pares** de la misma
persona en grupos contiguos distintos, **41 intrapadre y 49 entre padres**.
No son 90 errores ni 90 casos nunca leídos.

Para un lote pequeño se seleccionaron los cinco pares de menor longitud combinada
entre los 18 candidatos `CONTEXTO_REVISADO → fuente explícita` cuyo único indicador
era la falta de fuente propagable a la izquierda y cuyos extremos no tenían avisos.
La selección facilita una lectura acotada; **no acredita menor incertidumbre semántica**.
5252 demuestra por qué no basta ese filtro para aprobar una unión.

Se leyeron **cinco padres completos, 8.314 caracteres de origen**, incluyendo todas
sus voces, y todos los miembros de los diez grupos de extremos, que en v1 tenían
una fila cada uno. El contexto externo se limitó a **ventanas de hasta250 caracteres**
a cada lado; no se afirma lectura completa de los padres vecinos ni nuevo cotejo PDF.

La evidencia íntegra y sus hashes están en
[`lecturas.json`](continuidad_lote2_2026-09-09/lecturas.json), con las particiones,
miembros completos, ventanas, justificaciones y reservas. La
[tabla de decisiones](continuidad_lote2_2026-09-09/decisiones.csv) resume el lote.

## Decisiones y límites de voz

| Padre | Decisión | Qué permanece separado |
|---|---|---|
| **663 / Magendzo** | Unir **347 +370 =717**: minería y luego costos de mano de obra, sin otra persona intercalada. | Valdés332; pregunta de Marfán316; respuesta posterior de Magendzo661; Desormeaux304 y Valdés660. **No se une Magendzo atravesando a Marfán.** Sebastián Edwards sigue siendo una referencia dentro del aporte de Valdés. |
| **1871 / Lehmann** | Unir **148 +401 =549**: respuesta sobre precios agrícolas y conclusión de las proyecciones. | Presidente123 y su retorno192. La oferta de palabra a Soto no se convierte en habla anticipada de Soto. El aviso de puntuación del Presidente permanece. |
| **2692 / Lehmann** | Unir **385 +416 =801**: respuesta sobre inventarios y cierre de proyecciones de commodities. | Pregunta del Presidente98 y posterior agradecimiento de2693. La fuente por cargo del segundo tramo no cambia de actor ni se convierte en alias nuevo. |
| **6813 / Gianelli** | Unir **141 +793 =934**: precisión sobre Grecia y continuación explícita de su presentación. | Vergara115/240. No se añade una voz de Draghi por la referencia a su discurso, ni se une el Gianelli de6814 atravesando el retorno de Vergara. |
| **5252 / Marfán** | **Reserva: no unir162→223.** Se conservan sus funciones diferenciadas de aviso sobre incorporación futura y cesión de palabra. | Siguen cuatro grupos: comentario1712 / acta158 / aviso162 / cesión223. No se convierte la futura llegada de Vergara en intervención, ni se adelanta la de Herrera. |

En 5252 **no se afirma otra voz intercalada ni imposibilidad absoluta de continuidad**:
se mantiene una separación conservadora, sin aprobación en este lote. Tampoco se
unen sus cuatro partes por aparecer repetidamente el nombre de Marfán. Esta revisión
de continuidad no repite ni sustituye las 167 fichas de comas ya documentadas.

## Aplicación real y conservación

Los cuatro pares se aplicaron mediante el motor y el registro acumulativo
[`continuidades_intrapadre_v2.json`](../data/curation/continuidades_intrapadre_v2.json).
Contiene **seis pruebas intrapadre: las dos de v1 idénticas y cuatro nuevas**.
Los 24 registros de continuidad entre padres mantienen su cargador separado y sus
exigencias. El cargador v1 continúa rechazando registros v2 o pares adicionales.

- La izquierda permanece `CONTEXTO_REVISADO`, **sin ancla**.
- La derecha conserva **su ancla explícita propia** y recibe la relación
  `CONTINUIDAD_INTRAPADRE_REVISADA` con antecedente inmediato a la izquierda.
- Se exigen fuente íntegra, fecha, actor, intervalos literales y pares exactos.
  v2 verifica además el hash del paquete de lecturas y sus grupos contra v1.
- No hay reglas globales por «Finalmente», «Por otra parte», gerundios, menciones
  o coincidencia de actor. No cambian aliases, atribuciones ni cortes físicos.

| Medida | v1 | v2 |
|---|---:|---:|
| Filas físicas / bloques | 9.691 /9.690 | **9.691 /9.690** |
| Grupos | 9.255 | **9.251** |
| Grupos con varias filas | 339 | **343** |
| Máximo de filas por grupo | 11 | **11** |
| Filas alertadas / padres alertados | 465 /395 | **465 /395** |
| Pruebas revisadas entre padres / intrapadre | 24 /2 | **24 /6** |
| Pares del inventario | 90 | **86** |

La comparación sobre **toda la partición** verifica exactamente las cuatro uniones:
ningún grupo previo se divide y no aparece otra unión. Se conservan Marshall2796→2797,
De Ramón3012, García de once filas y todas las demás continuidades, registradas o no.
Los controles2685/2885/1901/2779 y los enlaces prohibidos600→601/5402→5403 no cambian.
Esto es conservación comprobada, no una afirmación de relectura de esos casos aquí.

Cambian **ocho celdas relacionales** —cuatro relaciones y cuatro antecedentes— y
**215 etiquetas `ID_Turno`** por la renumeración en cuatro sesiones. No son215 nuevas
uniones. **Ocho filas cambian de compañeros de grupo.** Todos los demás campos son
idénticos celda a celda: textos, actores, cargos, fuentes, anclas, fechas, IDs físicos,
clasificaciones y alertas. Se conservan7.219 padres y2.048.560 palabras.

[Inventario sobre v1](continuidad_lote2_2026-09-09/inventario_v1.csv) ·
[Inventario sobre v2](continuidad_lote2_2026-09-09/inventario_v2.csv).
Quedan **86 pares inventariados:37 intrapadre y49 entre padres**, no86 errores ni86
pendientes de primera lectura. 5252 permanece en el inventario con su reserva documentada.

## Validación y versiones históricas

- **Ensayo aislado:** 1.980 pruebas,167,872s; reconstrucción, F0/F1 y comparación global pasan.
- **Publicación:** 1.980 pruebas,177,418s; reconstrucción, F0/F1 y comparación global pasan.
  Son **29 pruebas nuevas**. Se actualizó explícitamente la expectativa de un test
  del perfil predeterminado a v2; los tests del perfil explícito v1 siguen pasando.
- Ensayo/publicación: todas las hojas/celdas de **tres XLSX idénticas**, seis auxiliares
  CSV/JSONL idénticos byte a byte y QA idéntico. No se exige igualdad binaria de XLSX
  por sus metadatos. El código no cambió entre ambas construcciones.
- **109 hashes de entradas/código y12 de salidas** verificados, más el vínculo
  criptográfico entre el registro v2 y las lecturas. El manifiesto declara `intrapadre-v2`.
- **41 archivos históricos de datos y235 documentos/artefactos previos idénticos**
  byte a byte frente a `9daab5906aa913af88f31fb572e23c1ea613c519`.
  No se sobrescribieron LOOP32, v1, sus QA/manifiestos ni las fichas fechadas.

[Verificación de los archivos](continuidad_lote2_2026-09-09/verificacion.json) ·
[Manifiesto v2](../data/releases/continuidad_intrapadre_v2/manifiesto_preparacion.json).
Los manifiestos históricos describen el código de sus respectivos commits, no el
código actual. Estas verificaciones son locales: **no certifican exactitud semántica
total ni CI remoto**. Siguen465 filas alertadas, sin cierres ni nuevo cotejo PDF.

## Reproducir y continuar

```bash
.venv/bin/python scripts/preparar_data.py --perfil intrapadre-v2 \
  --destino .cache/reproduccion_intrapadre_v2
```

El destino debe ser nuevo; si existe, elegir otro. v2 es el perfil predeterminado.
El perfil explícito `intrapadre-v1` sigue disponible para reproducir su semántica en
un destino nuevo, sin sobrescribir la entrega histórica. Los componentes individuales
no deben ejecutarse sin las rutas de staging y el registro de perfil correspondientes.

**Próximo paso:** otro lote pequeño de continuidades, leyendo todos los miembros
antes de unir. Mantener aparte las reservas de duplicado/daño, las funciones
institucionales y las dudas de atribución; no usar la ausencia de alertas como aprobación.
