# Prioridades 2644/2661 y primer lote de candidatos

> **Informe histórico.** La publicación posterior a esta tanda está en [asentimiento y complementos](REVISION_ASENTIMIENTOS_2026-09-07.md): 9.218 filas / 632 alertas / 272 pruebas. El intercambio concreto de 2779 ya está delimitado. Los IDs, métricas y checkpoint de este documento son de la tanda anterior; los enlaces a `data/processed/` abren la versión vigente.

**Fecha:** 2026-09-07. **Inicio:** 9.211 filas / 635 alertas / 237 pruebas.
**Publicación final de esta tanda:** **9.215 filas / 633 alertas / 257 pruebas; F0/F1 aprobados.**

## Alcance y entregables

Se abordaron primero 2644 y 2661 y luego cuatro candidatos adicionales:
2779, 2785, 2805 y 2855. **Cinco padres cambian; 2779 queda pendiente**.
Se leyeron los intercambios y el entorno pertinente, sin cotejo PDF ni revisión
humana independiente. No se ejecutó una revisión exhaustiva de los 94 candidatos
anteriores ni del corpus completo.

- [Excel de seguimiento y cola vigente](../data/processed/revision_783.xlsx).
- Base final: `data/processed/consolidado_base_referencia_final.xlsx`.
- [Cinco padres, hashes y 24 segmentos resultantes](cambios_prioridades_2026-09-07.csv).
- [Contenido antes/después y hashes de las bases](comparacion_prioridades_2026-09-07.json).
- [Lectura de la respuesta explícita 2785](lectura_respuesta_2785_2026-09-07.json).
- [Punto de reanudación y pendientes del plan](estado_revision_prioridades_2026-09-07.json).

Los IDs del Excel son consecutivos de esta versión, no identificadores inmutables.
Los números de padre utilizados a continuación son los del consolidado original.

## 1. Presentación de Céspedes — 2644, 2009-07-09

El Presidente cede la palabra al Gerente de Investigación Económica, señor Luis
Felipe Céspedes. La cláusula `quien comienza su exposición señalando que…`
inicia su presentación, no prolonga el discurso del Presidente.

La revisión **HAB-20260907-2644** delimita:

1. Presidente: cesión inicial, **99 caracteres**.
2. Céspedes: **4.101 caracteres**, conservando toda la exposición y sus
   continuaciones —incluidas `Precisa…`, `Lo anterior, manifiesta el señor
   Céspedes…`, `El Gerente de Investigación Económica agrega…` y el cierre—.
3. Presidente: cesión final a De Ramón, **142 caracteres**.

Se mantienen tres segmentos: no se fragmenta la presentación por cada oración.
Se preserva el daño de la fuente, como `escenario de nesgo`.

### Salvaguardas de la cesión relativa

`CESION_RELATIVA_EXPLICITA` sólo opera con una revisión individual validada por
hash, límites y citas. No convierte cualquier `quien` ni cualquier invitación
en un turno. Se exige:

- La fórmula efectiva `quien comienza su exposición señalando que`.
- Una cesión contigua dentro de la misma oración, con coma previa.
- Sujetos completos y reconocibles de quien cede y quien recibe la palabra,
  sin nombres añadidos ni otras cláusulas incrustadas.
- Destinatario compatible con el actor revisado y posición fuera de comillas.

Las proyecciones utilizadas para validar sujetos no se exportan: el texto
conserva literalmente `quien…`. Sin la revisión, el inicio no se reatribuye.

## 2. Intercambio Ministro/Lehmann — 2661, 2009-08-13

Después de explicar el Presidente la relación de la inmigración con la PTF,
el texto introduce:

> El efecto debiera ser menor y al revés, acota el Ministro, y el señor Lehmann complementa que será necesario afinar el análisis.

Se recuperan **ambas voces**, no sólo la coordinación final:

**Presidente → Ministro (58 caracteres) → Lehmann (69 caracteres) → Claro.**

El Ministro se reconoce por su sujeto pospuesto y un prefijo estrictamente
acotado. El complemento de Lehmann queda documentado en
**HAB-20260907-2661**, de tipo `COORDINACION_Y_EXPLICITA`. La pregunta de Claro
sigue separada. El padre pasa de **9 a 11 segmentos**.

Los primeros siete segmentos y las exposiciones previas de Lehmann permanecen
idénticos. El comentario anterior de Desormeaux todavía contiene
`acotación que es confirmada por el señor Lehmann`. **Esa confirmación pasiva
sigue pendiente**: no se inventaron palabras de Lehmann ni se certificó el padre
completo por corregir el intercambio final.

## 3. Primer lote adicional

| Padre | Fecha | Corrección | Segmentos |
|---:|---|---|---:|
| 2785 | 2009-11-12 | Respuesta explícita de Soto tras `a lo cual,`, seguida de su presentación | 2 → 2 |
| 2805 | 2009-12-15 | Acotación final del Presidente después de García | 5 → 6 |
| 2855 | 2010-01-14 | Presentación de Soto separada de la solicitud del Presidente | 1 → 2 |

### 2785: respuesta y exposición de Soto, con continuidad hacia 2786

Claro conserva su planteamiento inicial, incluido `UF mayores Luego` sin
reparación. Soto empieza en `a lo cual, el señor Claudio Soto responde…` y
conserva **1.528 caracteres** de respuesta y exposición sobre colocaciones,
tipo de cambio e indicadores bursátiles.

Se admite la coma después de `a lo cual/que` en el detector existente de
respuestas, manteniendo el separador previo, las guardas de comillas y la
validación de sujeto/verbo. La búsqueda de esta variante en el consolidado
halló únicamente 2785; la comparación completa confirmó el alcance.

Durante la verificación se detectó que implementar este caso como un intervalo
`CONTEXTO_REVISADO` rompía el ancla hacia 2786. Se corrigió esa implementación:
**la salida definitiva usa `SUJETO_NOMBRE`**, y Soto conserva el mismo turno
entre ambos padres. No se relajó la política que impide usar una revisión
contextual, por sí sola, como ancla de continuidad.

La lectura está documentada aparte. **2785 no es una nueva entrada del registro
de intervalos de hablante**; su cambio se instrumenta como reconocimiento
explícito. Esto explica que su seguimiento histórico no se contabilice igual
que las cuatro revisiones individuales añadidas.

### 2805: cierre del Presidente

La revisión **HAB-20260907-2805** separa los **139 caracteres** de
`Esa es una decisión que han adoptado… acota el señor Presidente` del tramo
anterior de García. Se preservan los **4.385 caracteres** de la exposición
inicial de Lehmann y los intercambios posteriores con Marfán. No se corrigieron
cifras, redacción ni daños del original.

### 2855: inicio explícito de Soto

La revisión **HAB-20260907-2855** comienza en
`El Gerente de Análisis Macroeconómico, señor Claudio Soto, da inicio a su presentación`.
Se conservan **142 caracteres** de solicitud del Presidente y **1.026 caracteres**
de exposición de Soto. Las continuaciones sobre PIB y sectores no se distribuyen
entre hablantes por aparecer en distintas oraciones.

### 2779: leído, no modificado

Cowan interviene; luego `El señor Soto asiente, mientras que el Consejero señor
Enrique Marshall responde…`. Ambos actos siguen dentro del segmento de Cowan.
Debe delimitarse el asentimiento y la respuesta, conservando `En su opinión…`
como parte de esta última. Se dejó pendiente el conjunto, sin resolver únicamente
la última voz ni confundirlo con una mera referencia nominal.

## 4. Pruebas y comparación de toda la base

- **257 pruebas aprobadas**, 20 nuevas: conservación y hashes, cesión relativa,
  sujetos incompatibles o múltiples, futuro/invitación frente a exposición
  efectiva, comillas, separador y antecedente no contiguo; intercambio completo,
  respuestas, exposiciones largas y continuidad de Soto hacia 2786.
- **50 intervalos de hablante documentados**, cuatro más. Las **46 revisiones
  anteriores permanecen idénticas**. Hay 17 coordinaciones documentadas, sin
  convertir todas las conjunciones en cortes automáticos.
- Ensayos aislados y ejecución completa de `scripts/preparar_data.py`; **F0/F1
  aprobados**. La hoja principal publicada coincide con el ensayo final `iter2`.
- Comparación de **7.219 padres**: exactamente los cinco enumerados cambian
  segmentación o actor. Los otros **7.214** conservan texto, actor, método,
  cargo/fuente, tipo de acta, motivos y relación de continuidad, descontando la
  renumeración de IDs. No hay cambios de cargo en segmentos de texto/actor idénticos.
- **24 segmentos resultantes en los cinco padres; cuatro filas adicionales**.
  Conservación global ignorando sólo espacios: **2.048.560 palabras**,
  **9.214 bloques en 9.215 filas físicas**, máximo 31.948 caracteres por celda.
  El Excel de origen sigue idéntico al de `HEAD`.
- **8.826 grupos de turno; 298 multipárrafo; máximo 11 filas**. Partición de
  grupos no afectados verificada. Se protegieron los trece enlaces anteriores y
  el de Soto **2785 → 2786**, sin pérdida de continuidad. Conservadas las
  exposiciones de García de once filas, padres **60–70** y **142–152**.
- **43 hashes de entradas/código y 10 de salidas verificados** contra el manifiesto.
- 132 sesiones; 51 etiquetas de actor / 50 personas según F0; 310 contrastes TPM;
  559 duplicados exactos, 557 de fórmula. Estos controles comparten reconocedores
  y **no son una revisión semántica independiente**.

## 5. Alertas y seguimiento

**635 → 633 filas con alertas.** Los avisos de posible otro hablante/mención
pasan de **108 a 103**; los finales sin puntuación de **231 a 234**, por la
cesión inicial de 2644, la acotación del Ministro en 2661 y el planteamiento de
Claro en 2785, que conservan las comas originales. No se inventaron puntos ni
se suprimieron avisos para mejorar el contador. La diferencia no mide errores
confirmados. Los restantes motivos no cambian y se superponen.

En las **783 filas originales**: 466 pendientes de lectura contextual; 59 fórmulas;
71 métodos actualizados; 116 cambios por comparación; 47 correcciones dirigidas;
siete breves válidos; ocho menciones históricas; seis identidades; dos repeticiones
y una continuidad. Por tipo: **124 lecturas dirigidas por agente, 187 comparaciones
y 472 triajes**. Hay **610 intervalos originales** solapados con alertas vigentes.
Estos estados no equivalen a certificación de todo un padre.

Las seis menciones actuales documentadas siguen separadas del seguimiento
histórico y conservan sus avisos; 4574 conserva también la atribución legada.
Quedan **89 candidatos de otro hablante sin anotación de mención**, bajo el mismo
filtro anterior. No son 89 errores confirmados ni una lista exhaustiva de residuos.

## 6. Lo que no queda terminado del plan

- Continuar la cola contextual. Esta tanda no revisó todos los candidatos.
- Cotejar los comienzos ambiguos y enlaces dañados, especialmente **780 y 2667**.
  No se obtuvo un PDF nuevo ni se repitió aquí el acceso oficial previamente
  bloqueado por verificación humana.
- Resolver el tratamiento de la intervención conjunta de **2126**, las
  confirmaciones pasivas en **2661 y 2704**, y el intercambio de **2779**.
- Verificar las seis variantes de identidad y las dos repeticiones sustantivas.
- Realizar una revisión semántica **independiente** de una muestra con y sin
  alertas. Las lecturas y regresiones de esta tanda no cumplen esa función.

El checkpoint conserva estas limitaciones. No hay un proceso activo en segundo
plano y no se excluye un padre entero por tener una corrección parcial.
