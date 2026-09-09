# Cuatro ciclos encadenados de revisión contextual

> Informe histórico de la versión de 9.186 filas / 650 alertas.
> Estado vigente: [Segundo bloque de ciclos](REVISION_LOOP2_2026-09-07.md).

**Fecha:** 2026-09-07. **Punto inicial:** 9.165 filas / 669 alertas / 173 pruebas.
**Publicación final:** **9.186 filas / 650 alertas / 189 pruebas; F0/F1 aprobados.**

## Alcance y entregables

Se ejecutaron cuatro ciclos sin pedir confirmación entre lotes: selección de
pendientes, lectura del intervalo y su entorno, ajuste acotado y comparación.
Se leyeron los tramos recuperados y su contexto; **no se leyó exhaustivamente todo
el contenido de cada padre ni de las 783 alertas**. No hubo cotejo PDF ni revisión
humana independiente. Las comparaciones globales no equivalen a lectura individual.

- [Excel actualizado de seguimiento](../data/processed/revision_783.xlsx).
- [24 padres: hashes, IDs anteriores y 84 segmentos actuales completos](cambios_loop_2026-09-07.csv).
- [14 filas con cambios de método o relación, sin cambiar texto ni persona](metodos_continuidad_loop_2026-09-07.csv).
- [Punto de reanudación y siguientes candidatos no adjudicados](estado_revision_loop_2026-09-07.json).
- Base final: `data/processed/consolidado_base_referencia_final.xlsx`.

El punto de reanudación es un registro persistido, **no un proceso autónomo que
siga trabajando en segundo plano**. Los cuatro ciclos de este informe terminaron
y sus salidas están publicadas.

## 1. Ciclo de votaciones: diez comienzos y sus continuaciones

El reconocedor no admitía el prefijo **«Prosiguiendo con la votación»**. La
intervención siguiente quedaba bajo el consejero anterior aunque nombrara un
sujeto y un verbo de habla explícitos. Se añadió esa locución al reconocimiento,
sin convertir cualquier referencia a una votación en un corte.

| Padre | Fecha | Límite recuperado | Filas antes → ahora |
|---|---|---|---:|
| 2883 | 2010-01-14 | Claro → Marshall | 1 → 2 |
| 3017 | 2010-03-18 | Claro → Marshall | 1 → 2 |
| 3073 | 2010-04-15 | Claro → Marshall | 1 → 2 |
| 3122 | 2010-05-13 | Claro → Marshall | 1 → 2 |
| 3273 | 2010-07-15 | Claro → Marshall | 1 → 2 |
| 3340 | 2010-08-12 | Claro → Marshall | 1 → 2 |
| 3428 | 2010-09-16 | Claro → Marshall | 1 → 2 |
| 3429 | 2010-09-16 | Marshall → Marfán | 1 → 2 |
| 3488 | 2010-10-14 | Claro → Marshall | 1 → 2 |
| 3637 | 2010-12-16 | Claro → Marshall | 1 → 2 |

Se verificó que, en **los diez casos**, el hablante recuperado comparte ahora
`ID_Turno` con el inicio del padre siguiente, cuya relación es
`CONTINUIDAD_EXPLICITA`. No se corta el discurso al cambiar de párrafo.

En 3429 el voto de Marshall por 50 puntos base hasta 2,5% permanece con Marshall;
Marfán empieza después. En 3340 la entrada de Marshall conserva más de 2.600
caracteres sustantivos: el agradecimiento inicial no convierte toda su evaluación
en una fórmula procedimental.

## 2. Ciclo de cargos y retornos de expositores

Se reconocen las locuciones **«Prosiguiendo con la presentación»** y
**«Al continuar con su/la exposición»**, siempre con los controles de sujeto,
verbo, referencias y citas existentes. En la vista de reconocimiento se admiten
«Gerente de Estudios» y «Gerente División Política Financiera». No se reescribe
el texto ni se sustituye el cargo determinado por asistencia; tampoco se aplica
la primera variante al título distinto «gerente de estudios de mercado».

| Padre | Fecha | Recuperación | Filas antes → tras ciclo 2 |
|---|---|---|---:|
| 1335 | 2007-07-12 | Valdés inicia el anexo, antes parcialmente bajo Magendzo; se conserva su continuación. | 5 → 5 |
| 2514 | 2009-05-07 | Cowan interviene después de García. | 1 → 2 |
| 2624 | 2009-07-09 | Soto retoma el escenario interno después de Velasco; De Gregorio interviene al final. | 3 → 3 |
| 2818 | 2009-12-15 | Soto retoma la exposición después de Marshall, con más de 4.400 caracteres hasta el comentario final del Presidente. | 8 → 8 |
| 6564 | 2015-01-15 | Fuentes retoma después de Naudon y conserva más de 2.800 caracteres. | 1 → 2 |

La continuación de Fuentes en **6565** también comparte su `ID_Turno`. Es el
undécimo enlace entre padres recuperado, además de los diez de las votaciones.

En **1202, 1583, 1959 y 6739**, el actor y el texto no cambiaron: el método pasó
de `NOMBRE+VERBO` a `SUJETO_ROL_NOMBRE` y dejó de advertirse como legado. Son
mejoras de evidencia, **no cuatro personas corregidas**. Se comprobó que las
menciones a Valdés en 1037 y 1338 no generaran nuevos turnos.

## 3. Ciclo de cláusulas documentadas: seis intervalos

Se añadieron decisiones con hash, fecha, citas, inicio y fin al registro de
hablantes. Las cuatro coordinaciones usan el tipo optativo existente; no se
introdujo un corte general ante «y».

| Padre | Fecha | Decisión | Filas iniciales → finales |
|---|---|---|---:|
| 1923 | 2008-07-10 | De Gregorio comenta Brasil; Velasco compara México, Perú y Chile; Lehmann vuelve a presentar. | 7 → 8 |
| 2555 | 2009-06-16 | Marfán distingue rebote de aumento; Desormeaux precisa la caída interanual; García cierra y Lehmann retoma. | 4 → 5 |
| 2576 | 2009-06-16 | Se separa la pregunta del Presidente, introducida por «en tanto», de la pregunta de Marfán; Cowan comenta después. | 2 → 3 |
| 2583 | 2009-06-16 | Soto responde; García precisa el efecto en nivel y anualizado; luego vuelven el Presidente, Cowan y Soto. | 5 → 6 |
| 2608 | 2009-07-09 | Desormeaux comenta China; Lehmann complementa y sigue con inflación, liquidez y tasas en un tramo de más de 2.300 caracteres. | 6 → 6 |
| 2818 | 2009-12-15 | «Esa moderación… sostiene el señor Enrique Marshall» se separa de Marfán; Soto responde después. Se mantiene también el retorno extenso del ciclo 2. | 8 → 9 |

En **1923** se adjudica únicamente la comparación inicial del Ministro. Las
anáforas posteriores de «el señor Gerente», tras la intervención de García,
**no quedan certificadas** por esta revisión.

## 4. Ciclo de concatenaciones y marcas de extracción

Cuatro decisiones adicionales, también optativas y ancladas al texto:

| Padre | Fecha | Secuencia recuperada | Filas antes → ahora |
|---|---|---|---:|
| 754 | 2006-07-13 | Marfán pregunta; Magendzo responde sobre M1/M2/M3; Marfán vuelve a comentar y Valdés aclara. Se conserva la frase incompleta «dinero como todo». | 3 → 5 |
| 1858 | 2008-06-10 | Tras el Presidente y «.LI I», Lehmann retoma y responde una consulta; el Presidente interviene y Lehmann vuelve a responder. | 4 → 4 |
| 2838 | 2009-12-15 | Marfán formula su voto; «Para finalizar con la votación…» inicia la evaluación de De Gregorio. | 1 → 2 |
| 2915 | 2010-02-11 | García → Claro → García → Soto. Tras la marca «i», Soto expone salarios e IPC hasta el final, sin fragmentar su desarrollo. | 3 → 4 |

No se completan frases ni se eliminan las marcas «fi», «.LI I» o «i». La
conservación material no las certifica como contenido discursivo ni como números
de página. El registro de hablantes pasa de 25 a **35 intervalos**: diez nuevos,
con 16 coordinaciones y once concatenaciones en el conjunto acumulado. Las seis
revisiones de cargo y las seis lecturas de menciones actuales se mantienen.

## 5. Validación acumulada y diferencias de alcance

- **24 padres distintos** con cambios de actor o límites; 2818 aparece en dos
  ciclos, pero se cuenta una sola vez. Incremento neto de **21 filas**.
- Los diez intervalos optativos nuevos están en `revisiones_hablantes.json`.
  Los cambios por reconocimiento general se documentan en los CSV y en las
  regresiones, sin convertir su método explícito en una asignación forzada.
- `tests/test_loop_review.py` fija los hashes de las **24 fuentes** y verifica
  sus secuencias y conservación. Un cambio posterior de fuente exige revisión.
- Cero cambios de cargo para texto y actor idénticos; cuatro cambios adicionales
  de método y diez cambios de relación en filas cuyo texto y persona no varían.
  El enlace restante de continuidad está dentro del padre 3429, que también
  cambia estructuralmente y figura en el CSV principal.
- **7.219/7.219 padres conservados**, comparando caracteres e ignorando sólo
  espacios; 2.048.560 palabras, sin cambios.
- Conservación de las exposiciones de García de once filas en los padres 60–70
  y 142–152 y de los negativos 3454, 3715 y 4266.
- Publicación final igual por contenido al resultado preliminar comparado.
- **189 pruebas**, incluidas 16 nuevas; F0/F1 aprobados antes de publicar.
- **39 hashes de entradas/código y diez de salidas** verificados; Excel de
  origen sin cambios frente a Git.

F0/F1 comparten componentes de reconocimiento con el constructor: no son una
auditoría semántica independiente. Ni las regresiones ni los hashes prueban
por sí solos que todo un intervalo sea semánticamente limpio.

## 6. Métricas y advertencias pendientes

| Métrica | Antes | Ahora |
|---|---:|---:|
| Filas físicas / bloques | 9.165 / 9.164 | 9.186 / 9.185 |
| Grupos de turno | 8.789 | 8.799 |
| Grupos multipárrafo | 285 | 296 |
| Máximo de filas por turno | 11 | 11 |
| Posible otro hablante o mención | 154 | 129 |
| Atribución heurística legada | 264 | 260 |
| Final sin puntuación | 213 | 223 |
| **Filas con alguna alerta** | **669** | **650** |

Se mantienen 43 avisos anafóricos, ocho de brevedad, seis de identidad y dos de
repeticiones no formularias. Los duplicados exactos/formularios siguen en
557/555. Hay 132 sesiones, 37 columnas de auditoría y 24 finales, máximo de 31.948
caracteres por celda y 310 fórmulas TPM contrastadas.

La caída de 19 filas con alertas **no significa diecinueve errores corregidos**.
Los motivos se superponen y los cortes revelan diez finales incompletos, que no
se rellenan para disminuir el contador. En el cuarto ciclo bajaron cuatro avisos
de posible mezcla y aumentaron cuatro de puntuación: el total quedó en 650.

### Seguimiento de las 783 originales

| Estado | Total |
|---|---:|
| Pendiente de lectura contextual | 489 |
| Fórmula procedimental reclasificada | 59 |
| Método actualizado | 70 |
| Segmentación o actor modificado por comparación | 109 |
| Corrección dirigida aplicada | 32 |
| Breve válido revisado | 7 |
| Mención legítima revisada | 8 |
| Identidad pendiente | 6 |
| Repetición sustantiva pendiente | 2 |
| Continuidad entre padres revisada | 1 |

Los 32 intervalos con corrección dirigida incluyen diez nuevos sobre los 22
anteriores. Los cambios reconocidos por regla siguen distinguiéndose de las
asignaciones optativas en ese seguimiento; no se transforma toda comparación
en una lectura o cierre semántico. Quedan 109 intervalos vinculados a lectura,
179 a comparación y 495 a triaje; 627 originales se superponen con alguna alerta
actual. Las seis anotaciones actuales de menciones continúan visibles y se cuentan
separadamente. La instantánea original permanece intacta.

## 7. Punto de reanudación

El archivo de estado guarda los cuatro ciclos y los primeros veinte candidatos
restantes con hash del padre, actor y evidencia automática. Tras excluir las
menciones ya anotadas, quedan **115 filas candidatas** con aviso de otro hablante
o mención. Esa selección es triaje, no adjudicación ni revisión exhaustiva.

Entre los siguientes están 298, 753, 780, 1718, 1873 y 1946. Se mantienen los
pendientes complejos, incluido el caso conjunto 2126 y el intercambio 2661,
que requieren delimitar todas las voces antes de aplicar una corrección. Los
textos dañados y las identidades siguen requiriendo documentación adicional.

Para enlazar versiones, usar padre e intervalo de texto, no sólo IDs de fila.
