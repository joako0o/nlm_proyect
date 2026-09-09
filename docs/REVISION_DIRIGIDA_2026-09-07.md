# Revisión dirigida: locuciones, OCR, reanudaciones y cargos

> Antecedente de la ronda de 9.045 filas. La salida vigente y las correcciones
> posteriores están en [Revisión de cargos y contexto](REVISION_CARGOS_Y_CONTEXTO_2026-09-07.md).

**Fecha:** 2026-09-07. **Base anterior:** 9.033 filas / 863 filas con alertas.
**Salida publicada:** 9.045 filas / 792 filas con alertas; 90 pruebas y F0/F1 aprobados.

## Alcance y criterio

Ronda de lectura dirigida por el agente sobre el **consolidado original**, con
contexto anterior y posterior, no revisión humana independiente ni cotejo de
estos pasajes con los PDFs. Se examinaron atribuciones legadas, los seis cargos
pendientes y los cambios de segmentación producidos por las nuevas reglas.
No es una lectura exhaustiva de las 132 actas.

**Un párrafo nuevo no implica otro hablante.** Se conservan las exposiciones
largas, las referencias a terceros y la distinción entre ceder la palabra y
empezar efectivamente a hablar. La caída de alertas no cuenta errores corregidos.

## 1. Cambios de contenido atribuido o de límites

La comparación por `ID_Padre`, actor y texto identifica **14 padres con cambios**.
Otros **75 padres** sólo cambian método de atribución, fuente del cargo o tipo
de documento, sin cambiar actor ni límites del texto. Los cambios de IDs y de
grupos posteriores son consecuencia de la regeneración, no correcciones adicionales.

El [detalle CSV](cambios_revision_dirigida_2026-09-07.csv) conserva IDs/actores
anteriores y el texto completo de cada segmento actual de estos 14 padres.

| Padre | Fecha | Filas antes → ahora | Resolución y evidencia principal |
|---|---|---:|---|
| 702 | 2006-06-15 | 1 → 1 | **Jadresic → Marfán**. «el Consejero señor Mari^án, señala». El OCR se normaliza sólo para reconocer el nombre; el texto entregado conserva `Mari^án`. ID actual 931. |
| 1391 | 2007-08-09 | 2 → 1 | García sigue hablando. «se manifiesta de acuerdo» permite reconocer el comienzo y evita dividir el mismo discurso por una nueva referencia explícita al mismo actor. |
| 1450 | 2007-09-13 | 1 → 2 | Desormeaux → De Gregorio. «En lo que se refiere a actividad y demanda, el Vicepresidente señor De Gregorio consulta…». |
| 1456 | 2007-09-13 | 4 → 4 | Se separa la reanudación institucional del anuncio de Corbo: «el señor Presidente comunica…». Se mantiene la posterior cesión de palabra a García. |
| 1621 | 2008-01-10 | 4 → 5 | Se recupera la respuesta de Lehmann a Marfán: «El Gerente señor Lehmann, respondiendo al Consejero señor Marfán, señala…». Marfán es destinatario, no sujeto de esa respuesta. |
| 1815 | 2008-05-08 | 1 → 3 | Desormeaux → Lehmann → De Gregorio. Se reconoce «Sergio Lehman informa» y la cesión del Presidente tras «A continua ción». Soto es receptor, no hablante de la cesión. |
| 2110 | 2008-10-09 | 2 → 4 | García → Jaque → García → Jaque. Comentario breve sobre carry trade y reanudación de «el expositor», documentada abajo. |
| 2261 | 2009-01-08 | 2 → 3 | Soto → Claro → Soto. «El Gerente de Análisis Macroeconómico, respondiendo a la consulta… señala…» retoma la respuesta; no se asigna al consejero mencionado. |
| 2993 | 2010-03-18 | 1 → 2 | De Gregorio → Soto. Se reconoce «Ei señor Claudio Soto explica…». |
| 3308 | 2010-08-12 | 4 → 4 | «El señor Soto añade…» pasa al comienzo del bloque de Soto, sin quedar dentro de la intervención de Claro. |
| 3354 | 2010-09-16 | 2 → 3 | De Gregorio → García → De Gregorio. «El Presidente señor José De Gregorio añade…». |
| 5464 | 2013-04-11 | 1 → 2 | Vial → Lehmann. «el señor Sergio Lehman menciona…» retoma la exposición internacional. La atribución inicial de Vial conserva su alerta de método legado. |
| 6156 | 2014-04-17 | 1 → 2 | Bernier → Vergara. «Matías Bernier, respondiendo la consulta formulada por el Presidente… señala…» identifica al que responde, no al consultante. |
| 6733 | 2015-04-16 | 1 → 3 | Fuentes → Arenas → Fuentes. «El Ministro… consigna…» y «Miguel Fuentes continúa con su presentación…». |

Hay diez padres con más segmentos, uno con menos y tres con cambios sin variar
su número de filas: incremento neto de **12 filas**, sin sumar ni borrar texto.

### Reanudación documentada de Jaque — padre 2110

Una primera ejecución reconoció correctamente el comentario de García, pero
extendía indebidamente su bloque al tramo posterior de «el expositor». La
comparación contextual detectó esa consecuencia antes de la entrega final.

- Jaque expone sobre monedas: «Por el lado de las monedas, el señor Jaque indica…».
- García añade **una oración** sobre carry trade.
- «Refiriéndose a los mercados de commodities, el expositor menciona…» retoma
  el análisis de Jaque. La continuación vuelve a nombrarlo explícitamente:
  «Menciona el señor Jaque que si se observa el mercado de la gasolina…».

La resolución está en
[`revisiones_hablantes.json`](../data/curation/revisiones_hablantes.json),
`HAB-20260907-2110`, con hash del padre, intervalo de caracteres, citas y
justificación. Lleva `Fuente_Actor=CONTEXTO_REVISADO` y nota en la auditoría
(ID actual **2871**). No se generaliza a cualquier aparición de «expositor».
F1 exige que el intervalo sobreviva completo bajo Jaque y que exista la revisión
aplicable. **No se usa como ancla automática de continuidad posterior**; la
relación conservadora sigue siendo `SIN_CONTINUIDAD_CONFIRMADA`.

## 2. Seis cargos confirmados con evidencia documental

Los valores de los cargos **no cambian**: cambia su procedencia, antes pendiente.
Las celdas de asistencia permanecen vacías; no se inventan asistentes.

| Padre | Actor | Cargo | Evidencia |
|---|---|---|---|
| 41 | Klaus Schmidt-Hebbel Dunker | Gerente de Investigación Económica | Cargo y nombre explícitos en el propio padre |
| 234 | Jorge Pérez Etchegaray | Gerente de Operaciones Monetarias | Cita del padre 243, misma sesión del 2005-05-12 |
| 243 | Jorge Pérez Etchegaray | Gerente de Operaciones Monetarias | Cargo y nombre explícitos en el propio padre |
| 246 | Jorge Pérez Etchegaray | Gerente de Operaciones Monetarias | Cita del padre 243, misma sesión del 2005-05-12 |
| 406 | Sergio Lehmann Beresi | Gerente de Análisis Internacional | Cargo y nombre explícitos en el propio padre |
| 980 | Andrés Velasco Brañes | Ministro de Hacienda | Cargo y nombre explícitos en el propio padre |

Registro versionado:
[`revisiones_roles.json`](../data/curation/revisiones_roles.json).
Hay **4 `TEXTO_EXPLICITO_REVISADO` y 2 `CONTEXTO_SESION_REVISADO`**, con citas,
justificaciones y hash de cada padre. El cargador rechaza cambios de fuente,
citas inexistentes, evidencia de otra sesión, duplicados y fuentes no permitidas.
F1 comprueba su aplicación a la salida. No equivale a verificación histórica
externa del nombramiento o de la asistencia.

## 3. Minutas y continuidad preservada

- Padres **196–198**, del 2005-03-10: minutas personales de Corbo, De Gregorio y
  Ovalle. Se atribuyen por el encabezado (`ENCABEZADO_MINUTA`), no por menciones
  dentro de la cita. Tipo `MINUTA_PERSONAL`, relación `DOCUMENTO_PERSONAL`.
- El reconocedor exige encabezado y documento entrecomillado delimitado. Se
  abstiene ante varias minutas, cita sin cerrar o diálogo posterior. El cierre
  OCR mixto observado en la minuta de Ovalle se admite de forma delimitada.
- Las minutas largas también pasan por el fraccionamiento físico XLSX, sin
  truncar. Los tres casos actuales caben cada uno en una fila.
- Se conserva la exposición de García de **11 filas** en los padres **60–70**
  y otra de **11 filas** en **142–152**, bajo sus respectivos turnos.
- Las referencias en **3454, 3715 y 4266** siguen sin cortar artificialmente los
  discursos de Soto, De Gregorio y Soto. Las regresiones anteriores siguen pasando.
- Se reinicia el estado antes de segmentar otra sesión y se actualiza la última
  oración de contexto, evitando usar un antecedente ya superado.

## 4. Verificación publicada

| Control / métrica | Resultado |
|---|---:|
| Pruebas de regresión | **90 aprobadas**, 30 añadidas en esta ronda |
| F0 / F1 | **Pasan**, sin errores bloqueantes |
| Padres originales reconstruidos | **7.219 / 7.219** |
| Filas físicas / bloques de texto | **9.045 / 9.044** |
| Columnas auditoría / final | **37 / 24** |
| Sesiones / etiquetas de actor | **132 / 51** |
| Palabras conservadas | **2.048.560** |
| Mayor celda | **31.948 caracteres** |
| Padres divididos | **1.104** |
| Grupos de turno / grupos de varias filas | **8.677 / 278** |
| Máximo de filas por turno | **11** |
| Fórmulas TPM contrastadas | **310** |
| Filas con alertas | **792** |

Se verificaron los hashes de **24 entradas/archivos de código** y **7 salidas**
del manifiesto, la proyección final, los CSV (792 pendientes, 8.677 grupos y 132
decisiones), y que `data/raw` no tenga cambios frente a Git. Las pruebas incluyen
OCR idempotente, menciones que no son sujetos, reinicio de sesión, integridad de
las citas, reanudación contextual y minutas delimitadas/largas.

La conservación compara caracteres **ignorando sólo espacios**. El manifiesto
incluye ambos registros de curación. Los PDFs disponibles siguen usándose para
la recuperación automatizada de dos textos largos; esto no implica haber
cotejado esta ronda de atribuciones contra esos PDFs.

## 5. Cola pendiente y límites

| Motivo, con superposición | Filas |
|---|---:|
| Atribución heurística legada | 342 |
| Posible otro hablante o mención | 253 |
| Final sin puntuación | 110 |
| Duplicado no fórmula | 61 |
| Atribución por anáfora local | 39 |
| Fragmento breve | 8 |
| Variante de identidad | 6 |

No quedan filas con fuente de cargo `PENDIENTE_REVISION` en esta versión.
Eso no elimina las demás alertas ni certifica todos los cargos históricamente.
La cola pasa de **863 a 792**, pero cambian segmentación y métodos; **no son
71 errores confirmados corregidos**. Incluso aumentan algunos motivos, como
finales sin puntuación al exponer límites reales del OCR.

Persisten mezclas potenciales como el padre **2336**, las variantes de Ricaurte
sin fusionar y casos de herencia local que necesitan lectura. La revisión debe
seguir con ventanas de contexto y exposiciones completas, no tomando la fila
como unidad automática de hablante. `SIN_ALERTAS_AUTOMATICAS` no significa
revisión humana; F0 comparte el reconocedor de decisiones y no es una auditoría
semántica independiente. La referencia TPM sigue siendo Datosmacro, con las
limitaciones ya documentadas de la ventana de 10 días.
