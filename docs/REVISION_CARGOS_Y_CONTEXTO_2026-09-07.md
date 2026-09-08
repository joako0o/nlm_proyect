# Revisión adicional: listas de asistentes y continuidad contextual

> Antecedente de la ronda de 9.053 filas. La salida vigente se describe en
> [Revisión de la cola de 783 alertas](REVISION_COLA_783_2026-09-07.md).

**Fecha:** 2026-09-07. **Punto de partida:** 9.045 filas, 792 filas con alertas.
**Salida publicada:** 9.053 filas, 783 filas con alertas; **102 pruebas y F0/F1 aprobados**.

## Alcance

Lectura dirigida por el agente del consolidado y de sus párrafos de contexto.
No se cotejaron estos casos con los PDFs ni se realizó una revisión humana
independiente. Se priorizaron atribuciones `ORIGINAL`/`ROL+FECHA`, el padre 2336
pendiente de la ronda anterior y los efectos de las correcciones sobre toda la
salida. No es una auditoría exhaustiva de todas las actas.

Se conservaron las correcciones anteriores, las minutas y las exposiciones
largas. Un cambio de párrafo sigue sin ser evidencia suficiente de cambio de
hablante; tampoco una mención a un presidente extranjero identifica al Presidente
del Banco Central de Chile.

## 1. Error de extracción de cargos en dos sesiones

Al investigar el padre 2336 se encontró que el cargo de Soto en la lista parseada
era `Consejero`, pese a que la apertura identifica su gerencia. El error afectaba
las sesiones **2008-06-10** y **2009-02-12**.

### Evidencia de las aperturas

- **Padre 1851, 2008-06-10:** la lista termina «don Sebastián Claro Edwards,
  Asisten también: Gerente General…». La coma, en lugar de punto, impedía que
  el parser terminara la lista de consejeros.
- **Padre 2301, 2009-02-12:** «don Sebastián Claro Edwards. Ministra de Hacienda
  Subrogante, doña María Olivia Recart Herrera Gerente General…». El patrón
  anterior reconocía `Ministro`, pero no `Ministra`, como límite.

En ambos casos se absorbía a gerentes y otros asistentes dentro de la categoría
`Consejero/a`. La asignación posterior del cargo específico no reemplazaba la
primera entrada errónea. Las listas resultantes tenían **21 claves** bajo esa
categoría; eran claves del parser, no 21 consejeros reales.

Ahora la lista se detiene antes de otra categoría de asistentes, admitiendo
punto, coma o punto y coma. El recorte de nombres tampoco absorbe el siguiente
cargo. Las listas corregidas contienen únicamente **Marfán, Marshall y Claro**
como consejeros en esas dos sesiones. Esto se verifica con casos de regresión
sobre las aperturas reales y variantes de puntuación.

### Impacto comprobado

Hay **72 filas con el mismo texto y actor antes/después cuyo cargo cambia**:
39 de junio de 2008 y 33 de febrero de 2009. El
[CSV de cargos](correcciones_cargos_2026-09-07.csv) detalla los IDs anteriores y
actuales, actor, cargo y fuente.

| Actor | Cargo anterior incorrecto | Cargo corregido | Filas con texto y actor idénticos |
|---|---|---|---:|
| Sergio Lehmann Beresi | Consejero | Gerente de Análisis Internacional | 23 |
| Claudio Soto Gamboa | Consejero | Gerente de Análisis Macroeconómico | 20 |
| Pablo García Silva | Consejero | Gerente de División Estudios | 19 |
| Kevin Cowan Logan | Consejero | Gerente de División Política Financiera | 4 |
| Beltrán de Ramón Acevedo | Consejero | Gerente de División Operaciones Financieras | 3 |
| Matías Bernier Bórquez | Consejero | Gerente de Mercados Financieros Nacionales | 3 |

La fuente sigue siendo `LISTA_ASISTENCIA`: esta vez se corrigió su extracción,
no se añadió evidencia externa ni se inventaron asistentes. Los padres 1879 y
2336 también cambian sus límites; sus segmentos modificados no están incluidos
en el conteo de 72 filas comparables por igualdad exacta de texto y actor.

**Limitación importante:** F1 comparaba las salidas con el mismo parser de
asistencia, por lo que no detectaba este error semántico. Las nuevas regresiones
lo cubren expresamente; pasar F0/F1 nunca certificó la corrección histórica de
todos los cargos. No se afirma que ya no existan otros problemas de extracción.

## 2. Siete padres con cambios de atribución o segmentación

[Comparación con texto completo de los segmentos actuales](cambios_contexto_adicional_2026-09-07.csv).
Los IDs de fila son propios de esta versión; usar también `ID_Padre` y texto.

| Padre | Fecha | Filas antes → ahora | Corrección |
|---|---|---:|---|
| 1003 | 2006-12-14 | 6 → 10 | Se reconocen las respuestas de Igal Magendzo escritas como «Madgenzo». Secuencia: Corbo → De Gregorio → Magendzo → De Gregorio → Valdés → Magendzo → Velasco → Magendzo → Corbo → Valdés. |
| 1008 | 2006-12-14 | 1 → 2 | De Gregorio → Magendzo: «Por otra parte, indica el señor Madgenzo…». |
| 1010 | 2006-12-14 | 3 → 4 | Marfán → Magendzo → Valdés → Marfán. La respuesta de Magendzo no queda dentro del discurso de Marfán. |
| 1600 | 2007-12-13 | 1 → 1 | **Claro → Velasco**. «El señor Ministro de Hacienda felicita…» identifica al sujeto; Claro es uno de los destinatarios. ID actual 2111. |
| 1879 | 2008-06-10 | 2 → 3 | Desormeaux → Soto → García. Corregir la asistencia permite resolver «El Gerente de División Estudios… comenta». La posterior mención de Soto sigue dentro de la intervención de García. |
| 2336 | 2009-02-12 | 1 → 2 | Soto → Marfán. Se conserva la exposición inicial de Soto y se separa la pregunta final de Marfán. IDs actuales 3177–3178. |
| 6394 | 2014-09-11 | 1 → 1 | **Vergara → Lehmann** por continuación contextual documentada de la exposición internacional. ID actual 8133. |

La vista de reconocimiento corrige `Madgenzo` a `Magendzo` y los honoríficos
`Presidente seño` / `Ministro de Hacienda seños`, sin reescribir el texto. Se añade
la locución explícita `felicita`. Los tests comprueban idempotencia y que un uso
normal como «en el seno del Consejo» permanezca intacto.

### Padre 2336: mención y pregunta no son el mismo sujeto

La última oración comienza:

> En relación a un comentario efectuado por el Gerente señor Claudio Soto respecto al gráfico que se refiere al PIB resto socios comerciales, el Consejero señor Manuel Marfán consulta por el significado de esa expresión.

Soto es el autor del comentario mencionado; **Marfán formula la consulta**. En
2337, Soto responde: «ello se refiere a la velocidad del PIB resto de los socios
comerciales». El parser general se abstiene por la relativa «que se refiere» en
el prefijo. Se resuelve este intervalo mediante `HAB-20260907-2336`, sin relajar
la salvaguarda general contra verbos de otras cláusulas.

### Padre 6394: Lehmann continúa hablando de autoridades extranjeras

- **6393:** «El señor Sergio Lehmann inicia su intervención…» sobre noticias
  políticas; en primer término, se refiere a Janet Yellen.
- **6394:** «El Presidente del Banco Central Europeo señor Mario Draghi, en
  tanto, dio señales…» continúa el tema; luego enumera «En segundo lugar…» y
  desarrolla Escocia, Francia y economías emergentes.
- **6395:** «El señor Sergio Lehmann prosigue con su presentación…» y pasa a
  mercados financieros.

No aparece una intervención de Vergara ni una cesión de palabra. La presencia
original de Vergara se corrige mediante `HAB-20260907-6394`, **no por herencia
automática que ignore el actor original**.

Ambas decisiones se suman a la reanudación ya documentada de Jaque en
[`revisiones_hablantes.json`](../data/curation/revisiones_hablantes.json).
Hay tres intervalos con `Fuente_Actor=CONTEXTO_REVISADO`: hashes, posiciones,
citas, justificación y notas de auditoría. F1 exige que los tres sobrevivan
completos bajo el actor revisado. No se convierten en anclas automáticas para
propagar atribuciones a otros párrafos. Las revisiones documentales de los seis
cargos de la ronda anterior siguen aplicándose sin cambios.

## 3. Validación y conservación

| Métrica | Resultado |
|---|---:|
| Pruebas | **102 aprobadas**, 12 nuevas en esta ronda |
| F0 / F1 | **Pasan**, sin errores bloqueantes |
| Padres originales reconstruidos | **7.219 / 7.219** |
| Filas físicas / bloques | **9.053 / 9.052** |
| Columnas auditoría / final | **37 / 24** |
| Sesiones / etiquetas de actor | **132 / 51** |
| Palabras | **2.048.560**, sin variación |
| Máxima longitud de celda | **31.948 caracteres** |
| Padres divididos | **1.106** |
| Grupos / grupos de varias filas | **8.684 / 278** |
| Máximo de filas por grupo | **11** |
| Fórmulas TPM contrastadas | **310** |
| Filas con alertas | **783** |

Se verificaron los hashes de **25 entradas/archivos de código y 7 salidas** del
manifiesto publicado; CSV de 783 pendientes, 8.684 grupos y 132 decisiones;
`data/raw` sin cambios frente a Git; y ausencia de errores de whitespace en
`git diff --check`. La conservación compara caracteres ignorando sólo espacios.

Las exposiciones de García en **60–70** y **142–152** continúan agrupando once
filas cada una. Las referencias a terceros de **3454, 3715 y 4266** siguen sin
provocar cortes falsos. Los tres documentos personales siguen identificados
como minutas y los textos largos permanecen completos.

## 4. Pendientes y siguiente foco

Las alertas pasan de 792 a **783**, pero esa diferencia **no mide los errores
corregidos**: las 72 correcciones de cargo no necesariamente tenían alertas.
Motivos actuales, superpuestos:

- 333 atribuciones heurísticas legadas.
- 252 posibles otros hablantes o menciones.
- 110 finales sin puntuación.
- 61 duplicados no fórmula.
- 39 anáforas locales.
- 8 fragmentos breves.
- 6 variantes de identidad.

El padre **2126** mantiene una atribución legada pendiente: «El señor
Vicepresidente y el Consejero señor Claro señalan…» es una expresión conjunta.
No se ha desagregado ni se ha asignado arbitrariamente al Consejo completo.
También siguen pendientes las variantes de Ricaurte, sin fusionarlas.

El padre **2336 ya no es la mezcla sin resolver de la ronda anterior**; su pregunta
final tiene resolución dirigida. Esto no garantiza pureza semántica de todo el
corpus. Conviene continuar revisando cargos contra las aperturas y leer las
atribuciones legadas con sus exposiciones completas. `SIN_ALERTAS_AUTOMATICAS`
no implica revisión humana. Las limitaciones de la referencia TPM de Datosmacro
y de su ventana de 10 días tampoco cambian.
