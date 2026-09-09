# Continuidad — lote4: pausas, cesiones y tramos mixtos

**9 de septiembre de 2026. Lectura documentada, sin aplicar enlaces ni cortes.**
La entrega de datos sigue siendo **intrapadre-v3**:9.691 filas,9.242 grupos y465
filas alertadas en395 padres. Este lote no genera una versión v4 de datos.

## Alcance de la lectura

Se revisaron **19 pares** del inventario vigente:

- Los **15 pares** con indicador `BARRERA_LEXICA_IZQUIERDA`.
- Los **primeros cuatro**, en orden de origen, cuyo único indicador era
  `TIPO_ACTA_O_DOCUMENTO`. Esa etiqueta se usó para seleccionar, no para decidir.

Se leyeron **29 padres completos /59.698 caracteres originales**, mediante sus
particiones literales completas, con conservación contrastada contra el original.
Esto incluye todas las voces de cada padre y todos los miembros de los grupos
implicados, no sólo los dos extremos de cada par. En particular, hubo que incluir
**2202,3108 y3571**, cuyos últimos tramos ya continúan hacia el extremo izquierdo.
Las exposiciones de Schmidt-Hebbel6220/3865 y García2764/7111 se leyeron completas
porque comparten padre con las cesiones examinadas; no se recortaron por longitud.

Se guardan textos íntegros, hashes, particiones, miembros y ventanas externas de
hasta250 caracteres. Las ventanas no son lectura completa de otros padres vecinos.
Los padres3193 y3269 se releen completos tras truncarse su primera salida de herramienta.

[Lecturas](continuidad_lote4_2026-09-09/lecturas.json) ·
[Decisiones de los19 pares](continuidad_lote4_2026-09-09/decisiones.csv) ·
[Inventario con estados del lote4 y reservas del lote3](continuidad_lote4_2026-09-09/inventario.csv).

## Diez separaciones respaldadas

**Nueve corresponden a pausas y reanudaciones.** La identidad del Presidente no
basta para unir intervenciones temporalmente distintas:

| Padre / extremos | Evidencia para mantener separación |
|---|---|
| **2875:1→:2** | Cierre de mañana79; reconocimiento a Velasco1038 antes de reanudar a las16:00. La respuesta posterior de Velasco no se adelanta. |
| **2958:1→:2** | Cierre335; inicio de tarde224 a las15:00. Se conserva la repetición dañada y su aviso, y García comienza aparte. |
| **3008:1→:2** | Cierre61; bienvenida332 antes de reanudar a las16:00. La respuesta413 de Larraín, su aviso y `A continuación,.` permanecen separados. |
| **3109:1→:2** | Cierre144 e inicio548 a las16:00. Se conserva3108:3(655)→3109:1, sin extenderlo a la tarde. La frase institucional83 terminada en `por.` no se reconstruye. |
| **3193:1→:2** | Cierre217 e inicio246 a las13:00. García2764 queda separado de la cesión; `Pablo Garda` se mantiene literal sin alias nuevo. |
| **3269:1→:2** | Cierre96 a las13:10; apertura y bienvenida247 a las16:00. No se borra el residuo final. |
| **3328:1→:2** | Cierre142; apertura245 a las16:00. La presentación449 de García tiene su propio inicio. |
| **3421:4→:5** | Suspensión201 a las13:20; reanudación108 a las16:00. Marshall90, Opazo243, Soto1143 y reconocimiento797 conservan sus límites. |
| **3572:1→:2** | Suspensión102; reanudación235 a las16:00. Se mantiene3571:2(390)→3572:1, no su prolongación hacia la reanudación. |

La décima es **4332:1→4333:1**: la argumentación y voto individual3732 preceden
a una declaración de acuerdo unánime145. Se distingue el voto individual de la
constancia del resultado y del acuerdo/comunicado1954 que sigue, atribuido al
Consejo. No se reasigna la declaración presidencial a otra persona.

Estas fichas respaldan las separaciones actuales; **no crean diez cortes nuevos**.

## Seis reservas de cesión o función presidencial

| Pares | Reserva |
|---|---|
| **1603→1604,1630→1631,1840→1841** | Oferta general de comentarios seguida de una cesión específica. No hay otra voz transcrita entre ambos extremos: se mantiene separación conservadora sin afirmar discontinuidad absoluta ni adelantar el habla del destinatario. |
| **2203→2204** | Cesión reiterada a Soto; se conservan `A continuación,.` y `de de`. No se elimina como duplicado ni se inventa una respuesta intercalada.2202:2(134)→2203:1 permanece enlazado. |
| **3269:2→3270:1** | Reanudación/bienvenida seguida de cesión a García. Álvarez es destinatario de bienvenida, no hablante aquí. La presentación7111 de García permanece aparte. |
| **3421:5→:6** | Reanudación seguida de reconocimiento a García y bienvenida a Herrera. No se mueve el posible residuo `Presidente.` hacia3422 ni se convierten sus menciones en turnos. |

La barrera léxica es una salvaguarda del motor, **no una prueba automática de que
se haya intercalado otra persona**. No se amplía ni desactiva globalmente por estas lecturas.

## Hallazgo prioritario: tres filas con mezcla funcional

En **4788:1,4849:1 y4899:1**, la etiqueta actual `ACUERDO_CONSEJO` abarca contenido
personal seguido de la declaración del acuerdo unánime. **No son filas puramente
institucionales**, y la etiqueta por sí sola no justifica cortar la continuidad
del contenido personal con el párrafo anterior.

| Par examinado | Fila mixta | Prefijo personal bruto | Constancia y residuo |
|---|---|---:|---:|
| **4787:2→4788:1** | Análisis, voto y constancia2132 | **1947** | **185** |
| **4848:1→4849:1** | Voto y constancia332 | **154** | **178** |
| **4898:1→4899:1** | Voto, sugerencia comunicacional y constancia398 | **220** | **178** |

Los conteos incluyen literalmente el espacio anterior a «En consecuencia» en el
prefijo; no son longitudes de nuevas filas ya publicadas. Los dos fragmentos se
recomponen exactamente, sin limpiar espacios ni corregir palabras.

[Posiciones y textos de los límites funcionales propuestos](continuidad_lote4_2026-09-09/limites_no_aplicados.csv).
El marcador acotado es la oración que comienza **«En consecuencia, el Presidente
señor Rodrigo Vergara deja constancia que se acuerda por unanimidad…»**.
Son propuestas **no aplicadas y no son cambios de hablante**: el Presidente sigue
siendo quien habla. Una corrección posterior debe distinguir sus funciones sin
atribuir toda la fila al Consejo, y evaluar la continuidad sólo de la porción personal.

En4788 siguen intactos **llegada112 institucional / excusa161 de Larraín /
retorno333 del Presidente**, junto con el aviso del pie editorial de la primera
fila. No se extiende la propuesta a toda la llegada ni a la exposición posterior
de Larraín. En4849/4899 se conservan aparte los acuerdos/comunicados2126/2189.
Se mantiene `€100 billones` de4898 sin validar ni reparar su escala.

**No se unieron las filas mixtas enteras ni se suprimió su etiqueta para forzar
un enlace.** El hallazgo requiere un tratamiento acotado de esa mezcla antes de
aplicar una continuidad; este lote sólo fija la evidencia y los límites exactos.

## Resultado, validaciones y pendientes

- **19 fichas:10 separaciones respaldadas +9 reservas**, incluidas las tres mezclas.
- **0 enlaces,0 cortes,0 reasignaciones y0 alertas cerradas.** Las9.691 filas,
  9.242 grupos,15 pruebas intrapadre y24 pruebas entre padres no cambian.
- El inventario sigue en **77 pares**: una separación leída y respaldada sigue
  apareciendo si el inventario sólo busca misma persona en grupos distintos.
  Hay58 pares fuera del lote4, incluidos los cinco reservados en lote3; por tanto,
  **53 quedan fuera de ambos lotes3/4 entre los pares aún inventariados**.
  No equivalen a53 casos nunca leídos ni a53 errores.
- **2.032 pruebas locales (+24),243,076s, pasan.** Se prueban la selección cerrada,
  padres/miembros completos, fuentes, reservas, límites exactos, conservación y
  rechazo de destinos protegidos o existentes.
- **F0 y F1 pasan sobre una copia aislada de v3.** No se reconstruyó ni publicó
  una base nueva. QA coincide con el publicado; tres XLSX coinciden en todas sus
  hojas/celdas y seis CSV/JSONL coinciden byte a byte.115 hashes de entradas/código
  y12 de salidas se verificaron en el manifiesto aislado, que no sustituye al histórico.
- **69 archivos históricos de datos,247 documentos/artefactos y33 scripts anteriores**
  se comprobaron idénticos byte a byte frente a `dcbcc7c2cb8279cf4e749c029cb0bdb39ecc2e08`.
  Los cuatro archivos exportados del lote se reprodujeron byte a byte.

[Verificación de archivos y pruebas](continuidad_lote4_2026-09-09/verificacion.json) ·
[Resumen](continuidad_lote4_2026-09-09/resumen.json).
La lectura y adjudicación las realizó el asistente; los controles técnicos
corrieron en paralelo. **No hubo subagentes ni segundo revisor semántico**, ni
nuevo cotejo PDF. F0/F1 no certifican la pureza semántica de cada `Tipo_Acta`;
las465 filas alertadas en395 padres y los demás pendientes siguen abiertos.

```bash
.venv/bin/python scripts/revisar_continuidad_barreras.py \
  --salida .cache/reproduccion_continuidad_lote4
```

El destino debe ser nuevo bajo `.cache/` o `docs/`; el comando no escribe en `data/`.
**Próximo paso prioritario:** tratar los tres límites funcionales documentados y
su relación con los párrafos anteriores, sin ampliar la regla a los otros casos
con etiqueta de acta/documento antes de leerlos completos.
