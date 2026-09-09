# Retornos de exposición, respuesta OCR y resumen

> **Informe histórico.** La publicación vigente está en [cesión y retorno de opinión](REVISION_CESION_OPINION_2026-09-07.md): 9.226 filas / 627 alertas / 300 pruebas. Los límites pendientes de 3123 y 3187 ya se abordaron. Los IDs, métricas y checkpoint de este documento son de la tanda anterior; los enlaces a `data/processed/` abren la versión vigente.

**Fecha:** 2026-09-07. **Inicio:** 9.218 filas / 632 alertas / 272 pruebas.
**Publicación:** **9.221 filas / 629 alertas / 285 pruebas; F0/F1 aprobados.**

## Alcance y entregables

Se corrigieron **3221, 3233 y 3468**, con **seis segmentos resultantes y tres
filas adicionales**. En **3222** cambió sólo la relación de continuidad, al
recuperarse el retorno de Lehmann en el padre anterior.

También se leyeron **3123, 3187, 3191 y 3421**. Sus intercambios requieren
varios límites o tratamiento de sujetos conjuntos/actos institucionales, por
lo que se dejaron sin modificar y con pendientes explícitos. No se corrigió
únicamente la última frase de esos padres para aparentar un cierre.

**Lectura dirigida por el agente del consolidado y entorno pertinente; sin
cotejo PDF ni revisión humana independiente. No es una revisión exhaustiva.**

- [Excel de seguimiento y cola vigente](../data/processed/revision_783.xlsx).
- Base final: `data/processed/consolidado_base_referencia_final.xlsx`.
- [Tres padres: hashes, IDs anteriores y seis segmentos completos](cambios_retornos_2026-09-07.csv).
- [Contenido anterior/posterior, incluido 3222](comparacion_retornos_2026-09-07.json).
- [Evidencia de continuidad 3221 → 3222](continuidad_retornos_2026-09-07.csv).
- [Punto de reanudación y pendientes](estado_revision_retornos_2026-09-07.json).

Los números de padre corresponden al consolidado original. Los IDs de filas
actuales pueden renumerarse. El checkpoint no es un proceso activo en segundo plano.

## 1. Padre 3221 — 2010-07-15

Antes, 2.514 caracteres estaban atribuidos al Presidente. Ahora:

- **Presidente: 296 caracteres**, comentario sobre la intervención suiza.
- **Lehmann: 2.217 caracteres**, desde `Al proseguir, el Gerente de Análisis
  Internacional señala…`, conservando toda la exposición sobre las proyecciones
  de crecimiento, China, Asia y Europa.

Se reconoce `Al proseguir` como prefijo completo del sujeto, sin extender este
cambio a cualquier frase larga que empiece igual. El detector sigue exigiendo
sujeto y predicado compatibles, y mantiene las guardas de referencias, cargos
ambiguos y comillas. La atribución usa `SUJETO_ROL_SESION`; no se necesita una
revisión contextual para sustituir una evidencia explícita.

Se conservan daños como `lo que está hoy está proyectando` y
`World Economic Out/ook`. No se repararon las palabras de la fuente.

### Continuidad con 3222

3222 comienza `El señor Sergio Lehmann continúa…`. El final de 3221 y el
comienzo de 3222 ahora comparten `ID_Turno`, con `CONTINUIDAD_EXPLICITA` en
3222. No se modificaron su texto, actor, cargo ni fuente de atribución.
La continuidad se apoya en sujetos explícitos, no en la mera proximidad ni en
convertir `CONTEXTO_REVISADO` en ancla.

## 2. Padre 3233 — 2010-07-15

Se separa la pregunta del Presidente sobre la brecha calculada por la OCDE
(**90 caracteres**) de la respuesta de García (**232 caracteres**).

La respuesta empieza literalmente `Ai respecto, el señor Pablo García responde…`.
Se normaliza esa variante inicial a `al respecto` **sólo en la vista de
reconocimiento**. El Excel conserva `Ai respecto`. La normalización es
idempotente, se limita al inicio del fragmento y no convierte menciones o citas
en sujetos. La salida usa `SUJETO_NOMBRE`.

El retorno posterior de Lehmann en 3234 no se fusiona con la respuesta de García.

## 3. Padre 3468 — 2010-10-14

Se separan:

- **Herrera: 502 caracteres**, comentario sobre flujos brutos/netos y referencia
  a la preocupación del Vicepresidente.
- **Marfán: 421 caracteres**, desde `Para resumir, el Vicepresidente señor Manuel
  Marfán plantea…`, incluidas las continuaciones `Por este motivo, estima…`
  y `Lo otro, indica…`.

La referencia anterior al Vicepresidente permanece con Herrera; no se confunde
una mención con una toma de palabra. La revisión **HAB-20260907-3468** delimita
el resumen con hash, citas y límites. Sin esa revisión, el límite no se aplica.
No se fragmenta el resumen por cada oración.

## 4. Validación

- **285 pruebas aprobadas**, 13 nuevas: hashes y conservación, retorno explícito,
  continuidad entre padres, cargos ambiguos, referencias, comillas, normalización
  OCR acotada, resumen y exactitud del intervalo revisado.
- **54 revisiones de hablante**, una más; las **53 anteriores son idénticas**.
  3221 y 3233 se corrigen por reconocimiento explícito y quedan documentados en
  la evidencia de esta tanda, no como nuevas entradas de `CONTEXTO_REVISADO`.
- Ensayo aislado y ejecución completa de `scripts/preparar_data.py`; **F0/F1
  aprobados**. La hoja principal publicada coincide con el ensayo aislado.
- Comparación global de **7.219 padres**: sólo tres cambian texto segmentado o
  actor; 3222 cambia únicamente la relación de continuidad indicada, aparte de
  IDs renumerados. Los restantes **7.215** conservan texto, actor, métodos,
  cargos/fuentes, tipo de acta, motivos y relaciones de continuidad.
- No hay cambios de cargo en segmentos de texto y actor idénticos.
- Conservación ignorando sólo espacios: **2.048.560 palabras**, **9.220 bloques
  en 9.221 filas físicas**, máximo 31.948 caracteres por celda. El Excel original
  sigue idéntico al de `HEAD`.
- **8.831 grupos de turno; 299 multipárrafo; máximo 11 filas**. Verificados la
  partición de grupos no afectados, los catorce enlaces anteriores y el nuevo
  **3221 → 3222**. Conservadas las exposiciones de García de once filas,
  padres **60–70** y **142–152**.
- **45 hashes de entradas/código y 10 de salidas verificados** contra el manifiesto.
- 132 sesiones; 51 etiquetas de actor / 50 personas según F0; 310 contrastes TPM;
  559 duplicados exactos, 557 de fórmula. Estos controles no son una auditoría
  semántica independiente ni cotejo completo de las actas originales.

## 5. Alertas y seguimiento histórico

**632 → 629 filas con alertas**. Los avisos de posible otro hablante/mención
pasan de **100 a 97**. No se modificaron los demás motivos: 236 finales sin
puntuación, nueve fragmentos breves, 259 atribuciones legadas, 42 anáforas,
seis variantes de identidad y dos duplicados no formulaicos. Los motivos se
superponen; la variación no es un conteo de errores confirmados.

En las **783 filas originales**: **460** pendientes de lectura contextual;
59 fórmulas; 71 métodos actualizados; **118** cambios por comparación;
**51** correcciones dirigidas; siete breves válidos; ocho menciones históricas;
seis identidades; dos repeticiones y una continuidad. Por tipo: **128 lecturas
dirigidas por agente, 189 comparaciones y 466 triajes**. **606 intervalos
originales** siguen solapándose con alertas actuales.

Las dos correcciones por reconocimiento se contabilizan como comparación en
ese seguimiento; su lectura está documentada aquí, sin inflar el registro de
intervalos revisados. Ninguno de esos estados certifica padres completos.

Las seis menciones actuales documentadas se cuentan aparte y conservan sus
avisos; 4574 mantiene también la atribución legada. Quedan **83 candidatos de
otro hablante sin anotación de mención**, bajo el filtro anterior. No constituyen
una lista exhaustiva de residuos ni 83 errores confirmados.

## 6. Pendientes identificados en esta lectura

- **3123:** después del voto de Marshall siguen en su segmento la cesión del
  Presidente y el agradecimiento de Marfán introducido por `quien agradece`.
  Faltan ambos límites, conservando la votación previa.
- **3187:** comentario del Vicepresidente en `Dado eso…` y retorno del Presidente
  en `En opinión del señor Presidente…`. No corregir uno absorbiendo el otro.
- **3191:** Marshall, opinión de Claro, coincidencia conjunta del Presidente y
  Soto, y cierre de García. No adjudicar el sujeto conjunto a una sola persona
  ni separar sólo el último cierre.
- **3421:** agradecimiento y suspensión del Presidente aún con Soto; reanudación
  institucional que engloba también agradecimientos personales y bienvenida.
  Es necesario delimitar el conjunto, no trasladarlo entero a otra etiqueta.

Se mantienen además los pendientes anteriores: 780, 2126, las confirmaciones
pasivas de 2661/2704, los daños de 2667/3107, la cola restante, variantes de
identidad, repeticiones sustantivas y revisión semántica independiente de una
muestra con y sin alertas. No se obtuvo un PDF nuevo en esta tanda.
