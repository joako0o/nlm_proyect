# Revisión de comas — lote 3 (2026-09-08)

**Base:** `648e0ee4802a5dc204469fb141becf671f180987` (lote2).
**Entrega de datos:** LOOP32 (`1b02496`), sin cambios ni regeneración.

## Resultado

**40 límites adicionales revisados en29 padres leídos completos**, con45.575 caracteres
de origen. Los sujetos y predicados respaldan los cambios de hablante ya exportados en
los focos seleccionados. **No hicieron falta nuevos cortes en esos límites.** No son
40 errores corregidos ni40 voces nuevas recuperadas.

| Unidad | Tras lote2 | Tras lote3 |
|---|---:|---:|
| Límites del subgrupo | 167 | 167 |
| Con ficha bilateral | 80 | **120** |
| Sin ficha bilateral | 87 | **47** |
| Padres con fichas bilaterales | 75 | **104** |
| Filas físicas de la base | 9.691 | 9.691 |
| Filas alertadas / padres alertados | 465 /395 | 465 /395 |
| Alertas cerradas / nuevos cortes / nuevos enlaces | — | **0 /0 /0** |
| Pruebas locales | 1.815 | **1.829** |

El avance reduce **trabajo sin ficha**, no elimina alertas de puntuación. El estado
`LIMITE_REVISADO_SIN_CIERRE` no certifica integridad OCR, cifras, cargos o exclusividad
de todos los tramos del padre. Las120 fichas tampoco se suman a las102 fichas actuales
de menciones (98 legítimas y4 pendientes): son unidades distintas y pueden superponerse.

## Lectura del padre largo2765

Se leyeron completos sus **12.127 caracteres**. Se mantienen los seis tramos:

**Marfán869 → Lehmann1845 → Claro387 → Presidente139 → Desormeaux168 → Lehmann8714.**

La ficha corresponde al límite **Presidente139→Desormeaux168**. El Presidente comenta
la tasa de ahorro, refiriéndose al comentario anterior de Claro. «y el señor
Vicepresidente complementa» abre el aporte de Desormeaux. La referencia a Claro no
crea otra intervención suya dentro del tramo presidencial.

Después, Lehmann prosigue su exposición durante **8.714 caracteres**, pasando por
crecimiento, inflación, tasas, paridades y commodities. **No se recorta por cambios
de tema, países mencionados o longitud.** Tampoco se fusiona con sus1.845 caracteres
anteriores a través de las intervenciones de Claro, Presidente y Vicepresidente.
Leer ese desarrollo no certifica cada palabra o cifra; se conserva, por ejemplo,
«calda» en el aporte de Claro y los demás términos literales del padre.

## Agrupar los focos del mismo padre ahorra relecturas

Después de2765 se priorizó mayor número de límites personales sin ficha por padre;
a igualdad, menor longitud y luego menor ID. Se incluyeron juntos todos los focos
personales pendientes de cada padre elegido hasta completar40 límites. Esto permite
aprovechar una lectura completa, **no aprobar automáticamente otros límites**.

| Padre | Focos registrados en este lote | Control principal |
|---|---:|---|
| 2661 | 4 | Doce tramos conservados; respuesta de Lehmann49 y presentación nominal posterior1322 con su ancla propia. |
| 2696 | 3 | Respuestas de Soto a Desormeaux y al Presidente; pregunta final de Marfán. Soto2570 y continuidad2695→2696 intactos. |
| 2910 | 2 | Presidente96 → Soto55 → García269; no intervención conjunta inventada. |
| 3028 | 2 | Dos aportes presidenciales y dos respuestas nominales de Lehmann, sin fusionar retornos. |
| 2896 | 2 | Vergara118 → Lehmann49 → García492 → Lehmann1249. |
| 2608 | 2 | Velasco106 → Desormeaux169 → Lehmann2323, sin cortar la exposición final. |
| 2981 | 2 | Preguntas de Marshall y respuestas diferentes de Soto y Presidente; Soto3212 no se fragmenta por temas. |
| 2805 | 2 | Preguntas de Marfán y respuestas de Lehmann y García. Se conserva Lehmann4385 anterior y la acotación presidencial final. |

Estos ocho padres reúnen19 focos. Con el foco de2765 y20 padres con un foco cada uno,
se completan40 límites en29 padres. Los29 no se superponen con los75 padres de los
registros anteriores, aunque algunos ya habían sido leídos para otras revisiones.

La selección es dirigida, principalmente de2009–2010, con631 de2006. **No es muestra
representativa ni independiente.** La longitud orienta la carga de lectura, nunca el
segmentador. Se leyeron los padres completos, además de ventanas de hasta180 caracteres
al final/inicio de los vecinos externos; no se afirma lectura completa de todos éstos.

## Respuestas breves, retornos y referencias

- **2911:** confirmación de Soto43; mantiene `FRAGMENTO_BREVE` y su enlace revisado a2912.
- **3186:** confirmación de Soto47; mantiene `DUPLICADO_NO_FORMULA`.
- **2918:** confirmación y explicación de Soto215; enlace revisado a2919 intacto.
- **631:** Lehmann106 → Ministro59 → Lehmann182. Se vuelve a leer completo; no se
  adelanta la respuesta al destinatario ni se fusionan los aportes de Lehmann.
- **3044:** Marfán135 → Vergara141 → Marfán221. Réplica y retorno con ancla propia,
  preservando la corrección de LOOP29.
- **3353/2922:** el retorno al primer hablante no absorbe la respuesta intermedia.
- **2997:** pregunta presidencial, respuesta de Bernier y pregunta de García distintas.
  El comunicado anterior mencionado no se convierte en documento leído de tercero.
- **3041:** la noticia de un diario es referencia de Marshall; la respuesta actual es
  de García, no del diario ni una intervención conjunta.

Los focos631,2896 y3044 aparecieron en el diagnóstico inicial; se leyeron ahora completos
sus padres antes de registrar estas fichas. No se promovieron automáticamente desde
las ventanas. Todas las continuidades y particiones de la entrega siguen idénticas.
`CONTEXTO_REVISADO` no recibe nuevas anclas y Fin solo no corta ni ancla.

## Reservas que no se cierran

- **2661:** Lehmann219 tiene su propio `FINAL_SIN_PUNTUACION`, fuera de los cuatro
  focos con coma de este lote.
- **2696:** se conserva la barra antes de «Añade» dentro de Soto2570 y las comas
  interiores que mantienen al mismo hablante; no toda coma precede una voz distinta.
- **2805:** Lehmann4385 conserva su aviso de puntuación y la «A» aislada interior.
  Las dos fichas posteriores no sanean ese tramo ni su límite anterior a Marfán.
- **2981:** se conserva «V*» dentro de Soto3212, además de «1PCX1»; no se reconstruyen
  signos o palabras a partir del tema económico.
- **3186/2911:** permanecen los avisos de duplicación y brevedad de las respuestas.
- **3313:** se conservan «De Gregario» y **«100.000 Y 150.000 mil personas»**. La lectura
  de sujetos no corrige nombres/cantidades ni habilita alias globales.
- **2765:** se mantiene el texto literal, sin certificar OCR por haber identificado las voces.

Las reservas constan en las fichas, **sin nuevas advertencias ni retiros en la base**.
No se reparan los posibles desplazamientos de palabras de las pasadas anteriores.

## Registro, acumulación y validación

Se reutiliza la herramienta existente, **sin cambios de código de producción ni de
las herramientas de diagnóstico**. Cada nueva ficha exige ambos intervalos exactos,
actor/método/fecha, evidencia completa del padre y firma de su partición. La validación
rechaza modificaciones en partes no focales y evita duplicar límites entre lotes.

```bash
.venv/bin/python scripts/revisar_cola_comas.py \
  --revisiones docs/revision_comas_lote1_2026-09-08/revisiones.json \
  --revisiones docs/revision_comas_lote2_2026-09-08/revisiones.json \
  --revisiones docs/revision_comas_lote3_2026-09-08/revisiones.json \
  --salida .cache/cola_comas_acumulada
```

**1.829 pruebas pasan:1.815 anteriores +14 nuevas**, con subpruebas sobre los40 límites,
las exposiciones largas, los doce tramos de2661, alertas residuales, retornos y enlaces.

**Los27 archivos versionados de datos son idénticos byte a byte**, incluidas fuentes,
TPM externa, bases, QA, manifiesto, colas y curación. También permanecen idénticos los
**diez artefactos de los lotes1 y2**, no sólo sus fichas. La cola acumulada se publica
en una ruta nueva; las exportaciones históricas no se reescriben.

**No se regeneró el pipeline.** La entrega y su QA siguen siendo LOOP32, con9.691 filas
y465 alertadas en395 padres. Sin nuevo cotejo PDF, muestra independiente, cierre
semántico exhaustivo o afirmación de CI remota. Workflow preexistente fuera del PR.

## Archivos y siguiente tramo

- [40 fichas nuevas y29 padres completos](revision_comas_lote3_2026-09-08/revisiones.json)
- [Cola acumulada de167](revision_comas_lote3_2026-09-08/cola_comas.csv)
- [47 límites sin ficha](revision_comas_lote3_2026-09-08/comas_sin_ficha.csv)
- [Resumen reproducible](revision_comas_lote3_2026-09-08/resumen.json)
- [Verificación global y hashes](revision_comas_lote3_2026-09-08/verificacion.json)
- [Pruebas nuevas](../tests/test_revision_comas_lote3.py)
- [Lote anterior](REVISION_COMAS_LOTE2_2026-09-08.md)

Quedan **47 límites en47 padres:42 personales y5 institucionales**. Los institucionales
siguen siendo601,1901,2112,2803 y5252 y requieren su propia revisión de acta/discurso.
Por longitud de origen,22 están en padres de hasta2.400 caracteres y25 entre2.401 y6.000.
**Ya no quedan padres de más de6.000 caracteres sin ficha en este subgrupo**, lo que no
equivale a una revisión completa de todas las intervenciones largas del corpus.

El siguiente paso es continuar los42 personales y tratar los cinco institucionales
separadamente. Las posibles palabras desplazadas siguen en una tarea de cotejo de
fuente, no de limpieza automática o reasignación por proximidad.
