# Revisión de comas — lote 6: acta/discurso (2026-09-08)

**Base:** `84bdd565b969d6612b7e77e94b1d637028feed42` (lote 5).
**Datos:** LOOP32 (`1b02496`), sin cambios ni regeneración.

## Resultado: registro de la subcola completo, no alertas cerradas

Se revisaron los **cinco límites institucionales restantes**, leyendo sus **cinco padres completos (10.169 caracteres de origen)** y los **diez intervalos vecinos exportados completos (26.227 caracteres)**. Los límites examinados respaldan las separaciones existentes entre narración del acta e intervención personal.

| Unidad | Tras lote 5 | Tras lote 6 |
|---|---:|---:|
| Límites de esta subcola | 167 | 167 |
| Con ficha personal | 162 | **162** |
| Con ficha acta/discurso | 0 | **5** |
| Con ficha, total | 162 | **167** |
| Sin ficha | 5 | **0** |
| Padres con fichas | 146 | **151** |
| Filas / filas alertadas / padres alertados | 9.691 / 465 / 395 | Sin cambios |
| Nuevos cortes / enlaces / reasignaciones / cierres | — | **0 / 0 / 0 / 0** |
| Pruebas locales | 1.855 | **1.878** |

**Los 167 límites tienen ficha; no se han corregido 167 errores ni resuelto todo el corpus.** El alcance sigue siendo la subcola de finales en coma antes de otro actor dentro del padre, con `FINAL_SIN_PUNTUACION` como único motivo en el extremo izquierdo. Las cinco nuevas fichas usan `LIMITE_INSTITUCIONAL_REVISADO_SIN_CIERRE`; no eliminan puntuación ni certifican todas las voces, identidades, cargos, cifras o colas del padre.

Las fichas institucionales de este seguimiento no añaden ni sustituyen registros institucionales productivos. Tampoco se suman a las 102 fichas actuales de menciones: son unidades distintas y pueden superponerse.

## Lectura caso a caso

### 601: interrupción para fotografías y reinicio de García

Se conserva **acta 307 → García 3.688**. La primera parte describe la interrupción por diez minutos, el ingreso de reporteros y el reinicio con la exposición de García. Ni los reporteros ni Velasco, nombrado con motivo de las fotografías, pasan a ser hablantes.

«quien señala» abre el contenido económico de García. Se conservan sus párrafos internos sobre condiciones monetarias, demanda, actividad, precios y expectativas, sin recortarlos por tema. El método y ancla actuales de García permanecen; no se crea una regla general para «quien».

El vecino 600 contiene la exposición previa de García. **No se restaura 600→601 atravesando el acta.** El vecino 602 vuelve al Presidente, que ofrece comentarios. Tampoco se clasifica todo el padre 601 como institucional.

### 1901: suspensión, reanudación y cesión de palabra

Se mantiene **Presidente 130 → acta 74 → Presidente 178**. La suspensión e información del horario pertenecen al primer aporte presidencial; «Siendo las 16:00 horas» narra la reanudación. Después de la coma, el Presidente ofrece la palabra a García.

**Nombrar a García al ceder la palabra no inicia su exposición.** Esta comienza en el intervalo vecino 1902, leído completo, de **7.969 caracteres**. No se fusionan los aportes presidenciales a través de la reanudación. Se mantiene `N °124` literal y, en el vecino, `6,25 puntos base`, sin certificar ni corregir esa unidad.

### 2112: Jaque, reanudación y agenda presidencial

Se conserva **García 397 → Jaque 988 → acta 74 → Presidente 279**. El límite registrado es acta→Presidente. «Siendo las 16;00 horas» describe la reanudación; luego el Presidente fija una reunión futura y ofrece la palabra.

La mención de abril de 2009 no cambia la fecha de esta sesión, **2008-10-09**. García empieza la presentación en 2113, cuyo intervalo de **12.059 caracteres** se leyó completo: no se atribuye al Presidente por la cesión anterior ni se divide por temas. Se conservan `16;00` y el residuo `aumento Mí de 200 puntos base` del vecino, sin reconstrucción.

### 2803: lista de asistencia y apertura presidencial con daño pendiente

Se conserva **cabecera/asistencia 1.445 → Presidente 296**. Los nombres y cargos de la lista no son intervenciones de cada asistente. «El Presidente, señor José De Gregorio, junto con dar inicio…» abre el aporte que fija la reunión de junio de 2010.

La cabecera mantiene `9;00` y `Economista Señor`. El tramo presidencial conserva **`TEXTO_DANADO_POR_COTEJAR`**, su método `CONTEXTO_REVISADO`, ancla nula y la cola **`A continuación,.`**.

**2803→2804 continúa sin enlace**, aunque ambos tramos sean presidenciales. La lectura del comienzo no repara la cola. El vecino anterior 2802 pertenece al cierre de noviembre de 2009: no se lo arrastra hacia la sesión de diciembre por su cercanía física.

### 5252: presidencia transitoria de Marfán, no llegada de Vergara

Se mantienen **Marfán 1.712 → acta 158 → Marfán 162 → Marfán 223**. El acta registra reanudación y presidencia transitoria. «haciendo presente que…» introduce el comentario de **Marfán** sobre la futura incorporación de Vergara; no es una intervención ni una llegada actual de Vergara.

Es una lectura acotada por sujeto y contenido, **no una regla para promover gerundios a turnos**. La cesión nominal posterior de 223 caracteres conserva ancla propia y otro grupo; Herrera comienza su presentación en el vecino 5253. `CONTEXTO_REVISADO` del comentario de 162 caracteres conserva ancla nula.

Como control adicional se comprobó la llegada institucional de Vergara en **5257:1**. No se cuenta ese control como otro padre completo leído de origen ni se altera el tratamiento de los documentos leídos: autor, lector, asistencia y habla en vivo siguen siendo conceptos distintos.

## Seguimiento institucional separado y acotado

Se añade [`scripts/revisar_comas_institucionales.py`](../scripts/revisar_comas_institucionales.py), independiente del pipeline productivo. **`scripts/revisar_cola_comas.py` no cambia** y sigue rechazando los cinco extremos del Consejo. Su salida personal sigue siendo 162 con ficha y cinco fuera de su alcance; la nueva salida combinada incorpora las cinco fichas acta/discurso, sin reescribir las exportaciones anteriores.

El nuevo validador:

- sólo acepta el inventario **601:1, 1901:2, 2112:3, 2803:1 y 5252:2**, cada uno con criterio específico y tipo institucional esperado;
- exige extremo institucional a la izquierda, actor personal esperado a la derecha, adyacencia, fecha, texto, estado y evidencia completos;
- verifica fuente, texto íntegro de origen, partición del padre y ambos intervalos vecinos;
- comprueba las equivalencias de turno de **todos los pares locales**, no sólo los adyacentes: detecta también una fusión de García o del Presidente a través del acta, sin congelar la numeración global de los grupos;
- valida cada lote personal por separado, rechaza duplicados y no permite que una ficha aporte la evidencia omitida por otra;
- rechaza sobrescribir entradas o exportaciones ya existentes, y prohíbe salidas dentro de datos, código o Git.

No se amplía un detector genérico de actas, llegadas, cesiones, gerundios o menciones. No se convierte `CONTEXTO_REVISADO` en ancla global ni se utiliza `Fin` como criterio de corte o anclaje.

## Verificación

**1.878 pruebas locales pasan (+23), en 93,202 s.** Incluyen las cinco fichas, mutaciones de extremos y vecinos, cambios fuera del foco, fusiones a través del acta, paquetes parciales y duplicados, conservación de exposiciones y anclas, rechazo del validador personal y CLI reproducible que no sobrescribe resultados.

Los **27 archivos de datos versionados**, incluido TPM externo, y los **25 artefactos de los cinco lotes anteriores** son idénticos byte a byte a `84bdd56`. El validador personal también es idéntico. Las tres exportaciones combinadas se reprodujeron byte a byte; las huellas se guardan en `verificacion.json`.

No hubo nuevo cotejo PDF, revisión humana independiente, pipeline productivo, F0/F1 o CI remota. Base, QA y manifiesto siguen en LOOP32. Las reservas previas —daños, duplicados, identidades/cargos y enlaces advertidos o prohibidos— permanecen vigentes.

## Qué sigue fuera de este registro

El diagnóstico conserva **317 candidatos**: registrar estos 167 límites no significa que los otros 150 estén sin leer ni que estén resueltos. Hay revisiones previas y categorías que se superponen con otros seguimientos.

Para la próxima revisión dirigida conviene abordar los **tres límites de la misma categoría con motivos adicionales**, excluidos expresamente de esta subcola:

- **2680:2:** `TEXTO_DANADO_POR_COTEJAR`, junto al final sin puntuación de la reanudación;
- **2779:2:** `FRAGMENTO_BREVE`, en «El señor Soto asiente,»;
- **2957:2:** `NOMBRE_EN_DISCURSO_POR_VERIFICAR`, con «El señor Rabio García…» literal.

Aquí sólo se identifican como próximos focos a partir del diagnóstico, **no se registran como nuevas lecturas completas o correcciones**. Requieren relectura de sus padres y contraste con los controles anteriores; no se debe eliminar el motivo adicional para hacerlos entrar en un validador que no les corresponde. Las **465 filas alertadas / 395 padres alertados** tampoco equivalen al total sin leer.

## Artefactos y reproducción

- [Cinco fichas acta/discurso, padres y vecinos](revision_comas_lote6_2026-09-08/revisiones.json)
- [Cola combinada: 167 límites con clase de ficha](revision_comas_lote6_2026-09-08/cola_comas.csv)
- [Sin ficha: cero filas, encabezado conservado](revision_comas_lote6_2026-09-08/comas_sin_ficha.csv)
- [Resumen](revision_comas_lote6_2026-09-08/resumen.json) · [Verificación y huellas](revision_comas_lote6_2026-09-08/verificacion.json)

```bash
.venv/bin/python scripts/revisar_comas_institucionales.py \
  --personales docs/revision_comas_lote1_2026-09-08/revisiones.json \
  --personales docs/revision_comas_lote2_2026-09-08/revisiones.json \
  --personales docs/revision_comas_lote3_2026-09-08/revisiones.json \
  --personales docs/revision_comas_lote4_2026-09-08/revisiones.json \
  --personales docs/revision_comas_lote5_2026-09-08/revisiones.json \
  --institucionales docs/revision_comas_lote6_2026-09-08/revisiones.json \
  --salida .cache/revision_comas6_repro
.venv/bin/python -m unittest discover -s tests
```

La salida debe ser una carpeta sin esas exportaciones previas; para repetir la reproducción se elige otro destino, sin sobrescribir los lotes publicados.
