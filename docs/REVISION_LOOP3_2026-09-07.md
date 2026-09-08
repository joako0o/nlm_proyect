# Tercer bloque de cuatro ciclos: actos personales, retornos y menciones

**Fecha:** 2026-09-07. **Inicio:** 9.226 filas / 627 alertas / 300 pruebas.
**Publicación final:** **9.235 filas / 623 alertas / 318 pruebas; F0/F1 aprobados.**

## Alcance y estado de la reanudación

Se encadenaron cuatro ciclos sin solicitar confirmación entre lotes. La ejecución
final fue interrumpida durante la construcción y después se retomó comprobando
el estado real de los archivos. Se volvió a ejecutar el pipeline completo y se
verificó la publicación. **El bloque está terminado; no hay un proceso activo
en segundo plano.** No se volvieron a registrar las decisiones ya guardadas.

| Ciclo | Trabajo | Filas del ensayo | Pruebas aprobadas |
|---:|---|---:|---:|
| 1 | 3421 y 3476: actuaciones personales y reanudación institucional | 9.230 | 306 |
| 2 | 3303, 3650 y 3651: complementos y retornos de exposición | 9.233 | 311 |
| 3 | 3571 y 3737: cierre del Presidente y explicación de Lehmann | 9.235 | 314 |
| 4 | Menciones legítimas en 2768 y 3147, sin cambiar actores | 9.235 | 318 |

**Siete padres modificados, 23 segmentos resultantes, nueve filas adicionales
y dos nuevas lecturas de menciones actuales.** Se conservaron las exposiciones,
las referencias nominales y los daños de la fuente. 3191 fue releído y permanece
pendiente por su coincidencia conjunta del Presidente y Soto, sin asignarla
arbitrariamente a una sola persona ni corregir sólo su última frase.

La lectura es del agente sobre el consolidado y su entorno pertinente. **No hubo
cotejo PDF, revisión humana independiente ni revisión exhaustiva de la cola.**

### Archivos

- [Excel de seguimiento y cola vigente](../data/processed/revision_783.xlsx).
- Base final: `data/processed/consolidado_base_referencia_final.xlsx`.
- [Siete padres: ciclo, hash, IDs anteriores y 23 segmentos completos](cambios_loop3_2026-09-07.csv).
- [Dos menciones actuales documentadas](menciones_loop3_2026-09-07.csv).
- [Contenido antes/después y hashes de las bases](comparacion_loop3_2026-09-07.json).
- [Checkpoint con pendientes y siguientes candidatos](estado_revision_loop3_2026-09-07.json).

Los números de padre corresponden al consolidado original. Los IDs de las filas
actuales son de esta publicación y pueden renumerarse.

## Ciclo 1 — Separación personal/institucional

### 3421, 2010-09-16

Antes había cuatro segmentos; ahora hay seis:

**Marshall → Opazo → Soto → Presidente → Consejo/acta → Presidente.**

- Se conserva la presentación de Soto, **1.143 caracteres**, sin incluir en ella
  el agradecimiento y suspensión del Presidente.
- `No habiendo comentarios, el Presidente…` inicia su intervención de
  **201 caracteres**, con la suspensión a las 13:20 y anuncio de reanudación.
- `Siendo las 16:00 horas…` queda como registro institucional de reanudación,
  **108 caracteres**.
- **HAB-20260907-3421** delimita los **797 caracteres** desde `Hace presente que
  esta es la última Sesión…`: comentario personal del Presidente, agradecimiento
  a García y bienvenida a Herrera. Las menciones de ambos no se convierten en
  intervenciones suyas. Se conserva el final literal `Presidente.`.

No se trasladó todo el antiguo bloque institucional al Presidente: se mantuvo
la oración de reanudación como acta y se separó el discurso personal posterior.

### 3476, 2010-10-14

También pasa de cuatro a seis segmentos:

**Soto → Marfán → Soto → Presidente → Consejo/acta → Presidente.**

La exposición retomada de Soto mantiene **2.853 caracteres** y sus continuaciones.
La suspensión del Presidente ocupa **236 caracteres**; la reanudación institucional,
**66**. **HAB-20260907-3476** delimita los **255 caracteres** de bienvenida al
Ministro y cesión de palabra a Herrera: son destinatarios, no hablantes nuevos.

Se conservan `Claudia Soto`, `De Gregario` y el enlace sin punto
`Política Monetaria El Presidente…`. No se completó ni reparó el OCR.

El único ajuste de reconocimiento de este ciclo es el prefijo completo
`No habiendo comentarios`, exigiendo sujeto y predicado válidos y manteniendo
las guardas de comillas y referencias. La comparación global sólo detectó los
dos padres previstos. Los retornos personales posteriores al registro
institucional están adjudicados individualmente, con hash y citas.

## Ciclo 2 — Complementos sin fragmentar presentaciones

| Padre | Fecha | Secuencia resultante | Caracteres por segmento |
|---:|---|---|---|
| 3303 | 2010-08-12 | Vicuña → Soto → Vicuña | 949 / 147 / 114 |
| 3650 | 2011-01-13 | Lehmann → Herrera | 103 / 280 |
| 3651 | 2011-01-13 | Presidente → Lehmann | 165 / 1.283 |

- **HAB-20260907-3303:** el retorno `en tanto que el señor Vicuña complementa…`
  no pertenece a Soto. Se conserva completa la explicación inicial de Vicuña.
- **HAB-20260907-3650:** `y el Gerente de División Estudios… Herrera… explica…`
  inicia su intervención. La confirmación previa de Lehmann de lo dicho por el
  Presidente contiene una referencia, no un turno nuevo del Presidente.
- **HAB-20260907-3651:** Lehmann responde en `Para cerrar este tema…` y continúa
  con bolsas y premios soberanos. La respuesta y el resto de su exposición
  permanecen unidos, sin volver a atribuirlos al Presidente.

Los límites internos de 3303 y 3650 siguen requiriendo revisiones compatibles
con el sujeto y fuera de comillas. No se habilitó un corte general por cada
`en tanto que` ni por cada `y`.

## Ciclo 3 — Cierre y explicación del expositor

- **3571, 2010-11-16:** Marfán (**736 caracteres**) → Presidente (**390**).
  **HAB-20260907-3571** delimita `Para cerrar la discusión…`; `Al respecto,
  manifiesta…` continúa con el Presidente, no con Marfán.
- **3737, 2011-02-17:** De Ramón (**429 caracteres**) → Lehmann (**548**).
  **HAB-20260907-3737** delimita `Con el objeto de entender los movimientos
  en bolsa…`; `Agrega…` sigue con Lehmann. La coincidencia anterior de De Ramón
  con el Presidente no transforma a este último en un nuevo hablante.

Ambas son decisiones individuales; no se añadieron reglas globales para
atribuir cualquier frase de cierre o cualquier explicación por proximidad.

## Ciclo 4 — Menciones, no cambios de hablante

Se añadieron **MEN-20260907-2768** y **MEN-20260907-3147**, con hash, límites,
actor, citas y alcance. El contenido de la base de auditoría es idéntico al del
ciclo 3: este ciclo sólo añade anotaciones al seguimiento y la cola.

- **2768:** Marshall recuerda lo que García comentó en una reunión del FMI.
  García es objeto del recuerdo; no interviene de nuevo en ese tramo.
  `Señala desconocer…` sigue con Marshall y Lehmann responde después.
- **3147:** De Ramón responde a la pregunta de Claro y alude a la fuente de
  información que consideró Lehmann. No son turnos nuevos de Claro ni de Lehmann.
  `Para resumir…` sigue con De Ramón; luego el Presidente cede la palabra a Soto.

Las dos anotaciones conservan **`POSIBLE_OTRO_HABLANTE_O_MENCION`**. No modifican
actores, no crean anclas de continuidad ni cierran otros motivos o todo el padre.
Las seis anotaciones previas siguen idénticas; ahora son **ocho lecturas actuales**,
separadas de las ocho menciones históricas del seguimiento original de 783 filas.

## Verificación final de la publicación

- **318 pruebas aprobadas**, 18 nuevas respecto del inicio. Se probaron actos
  personales/institucionales, continuaciones, sujetos incompatibles, comillas,
  límites internos, conservación, hashes y anotaciones que no modifican filas
  ni avisos. Las pruebas de menciones incorporan las revisiones de hablante
  vigentes al construir sus fixtures.
- **63 revisiones de hablante**: las 56 anteriores son idénticas y se añadieron
  siete. Hay 19 coordinaciones documentadas. **Ocho menciones actuales**:
  las seis anteriores son idénticas y se añadieron dos.
- Cuatro ensayos aislados y comparaciones de alcance; pipeline completo retomado
  después de la interrupción, con **F0/F1 aprobados** y publicación terminada.
  La hoja principal publicada coincide con los ensayos de los ciclos 3 y 4.
- Comparación de **7.219 padres**: exactamente siete cambian segmentación o actor.
  Los otros **7.212** conservan texto/actor, cargo/fuente, método, tipo de acta,
  motivos y relación de continuidad, descontando renumeraciones. Las anotaciones
  de mención se añaden en la cola/seguimiento, no cambian esas columnas de la base.
- Sin cambios de cargo en segmentos de texto y actor idénticos.
- Conservación global ignorando sólo espacios: **2.048.560 palabras**, **9.234
  bloques en 9.235 filas físicas**, máximo 31.948 caracteres por celda. El Excel
  de origen sigue idéntico al de `HEAD`.
- **8.844 grupos de turno; 300 multipárrafo; máximo 11 filas**. Se verificaron
  la partición de grupos no afectados, los **16 enlaces protegidos** y las dos
  exposiciones de García de once filas, padres **60–70** y **142–152**.
- **47 hashes de entradas/código y 10 de salidas verificados** contra el manifiesto.
- 132 sesiones; 51 etiquetas de actor / 50 personas según F0; 310 contrastes TPM;
  559 duplicados exactos, 557 de fórmula. Los controles comparten reconocedores:
  no equivalen a una revisión semántica independiente ni a cotejo documental.

## Alertas y seguimiento histórico

**627 → 623 filas con alertas.** Los avisos de posible otro hablante/mención pasan
de **94 a 87**, mientras que los finales sin puntuación pasan de **237 a 240**.
Los tres nuevos avisos de puntuación corresponden al tramo de Soto antes del
complemento en 3303, al tramo institucional truncado de 3476 y al de Lehmann
antes de Herrera en 3650. Se conservan las comas y daños de la fuente.

Los restantes motivos no cambian: 42 anáforas, 259 atribuciones legadas, nueve
fragmentos breves, seis variantes de identidad y dos duplicados no formulaicos.
**Los motivos se superponen y la variación no mide errores confirmados.**

En las **783 filas originales**: **450** pendientes de lectura contextual;
59 fórmulas; 71 métodos actualizados; **121** cambios por comparación;
**58** correcciones dirigidas; siete breves válidos; ocho menciones históricas;
seis identidades; dos repeticiones y una continuidad. Por tipo: **135 lecturas
dirigidas por agente, 192 comparaciones y 456 triajes**. **599 intervalos
originales** siguen solapándose con alertas vigentes. Estos estados no certifican
padres completos, y las anotaciones actuales no se suman como cierres históricos.

Quedan **71 candidatos de otro hablante sin anotación de mención**, frente a
80 al inicio: siete pasajes salen del filtro por la segmentación y dos por su
anotación de mención, conservando estos últimos sus avisos. No son 71 errores
confirmados ni una lista exhaustiva de residuos. 4574 conserva también su alerta
de atribución legada.

## Pendientes y criterio de separación

**Se separan los cambios de hablante claros, no cada oración ni cada párrafo.**
Las exposiciones y retornos se mantienen; las menciones y los actos conjuntos
no se reparten entre personas por intuición.

3421 deja de estar pendiente por la separación personal/institucional abordada.
**3191 sigue pendiente**: contiene la opinión de Claro y una coincidencia conjunta
del Presidente y Soto, además del cierre de García. No se adjudicó esa coincidencia
a una sola persona ni se corrigió únicamente la última voz.

Persisten los pendientes documentales de 780, la intervención conjunta de 2126,
las confirmaciones pasivas de 2661/2704 y los daños de 2667/3107. También falta
continuar la cola, verificar variantes de identidad y repeticiones sustantivas,
y realizar una revisión semántica independiente de una muestra con y sin alertas.
No se obtuvo un PDF nuevo en este bloque.
