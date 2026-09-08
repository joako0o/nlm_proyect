# Revisión de intervenciones coordinadas con «y»

> Informe histórico de la ronda de 9.153 filas; sus IDs corresponden a esa versión.
> El estado vigente está en [Revisión de concatenaciones](REVISION_CONCATENACIONES_2026-09-07.md).

**Fecha:** 2026-09-07. **Base anterior:** 9.142 filas / 661 alertas.
**Salida publicada:** 9.153 filas / 661 alertas; **136 pruebas y F0/F1 aprobados**.

## Alcance y entregables

Se revisaron doce pasajes del consolidado donde dos intervenciones explícitas
estaban unidas por «y el…». No se cotejaron con los PDFs ni se realizó una lectura
exhaustiva del corpus. Se conservaron las decisiones y exposiciones de las rondas
anteriores.

- [Seguimiento actualizado de las 783 alertas](../data/processed/revision_783.xlsx).
- [Comparación de los doce padres, con texto completo e IDs](cambios_coordinaciones_2026-09-07.csv).
- Base final actualizada: `data/processed/consolidado_base_referencia_final.xlsx`.

## 1. Doce decisiones dirigidas, no una regla de corte ante toda «y»

Cada decisión está en `data/curation/revisiones_hablantes.json`, con ID
`HAB-20260907-{padre}`, hash del texto original, intervalo, citas y justificación.
Se añadió el tipo de límite **`COORDINACION_Y_EXPLICITA`**. El conector «y» se
conserva al comienzo del segundo segmento.

El constructor exige una entrada documentada, un sujeto con verbo de habla
reconocido, actor compatible y un límite fuera de comillas. No se agregó una
regla que separe cualquier coordinación de nombres. Los nuevos intervalos llevan
`Fuente_Actor=CONTEXTO_REVISADO`, sin convertirse en anclas automáticas de herencia.

| Padre | Fecha | Intervención recuperada y contexto | Filas antes → ahora |
|---|---|---|---:|
| 1457 | 2007-09-13 | Velasco pregunta por el horizonte; García explica el efecto cambiario de los diferenciales a distintos plazos. | 1 → 2 |
| 1737 | 2008-03-13 | Desormeaux se suma a la mayoría; Claro mantiene su voto por 6,50%; después García comenta la minuta. | 2 → 3 |
| 2392 | 2009-03-12 | Desormeaux pregunta por cifras recientes; Lehmann informa la cifra formal; García comenta después. | 2 → 3 |
| 2443 | 2009-04-09 | De Gregorio menciona precios de mercado; Lehmann precisa PPP; De Gregorio vuelve a plantear dudas. | 11 → 13 |
| 2621 | 2009-07-09 | García informa la cifra trimestral; Soto agrega la revisión para el año. | 2 → 3 |
| 2765 | 2009-11-12 | De Gregorio comenta el ahorro; Desormeaux distingue riqueza inmobiliaria y accionaria; luego Lehmann retoma la presentación. | 5 → 6 |
| 2768 | 2009-11-12 | De Gregorio comparte una inquietud; Lehmann propone precios de commodities en otras monedas y continúa exponiendo. | 4 → 4 |
| 2826 | 2009-12-15 | Marshall comparte lo dicho por Marfán; De Gregorio agrega una comparación de inflación subyacente; después García desarrolla su respuesta. | 4 → 5 |
| 3449 | 2010-10-14 | De Gregorio comenta el Dow Jones; Herrera agrega las expectativas de relajamiento cuantitativo; Claro retoma su planteamiento. | 3 → 4 |
| 3871 | 2011-03-17 | Herrera propone «Indicador…» y De Gregorio propone «índice…». Son dos opiniones, no dos voces citadas dentro de una sola opinión. | 1 → 2 |
| 4233 | 2011-08-18 | Herrera explica una omisión; Lehmann complementa la comparación y continúa su exposición internacional. | 2 → 2 |
| 6407 | 2014-09-11 | Claro recuerda las marchas; De Ramón aporta el dato de los fondos de pensiones. | 1 → 2 |

La comparación global detecta cambios de actor/límites **solamente en esos doce
padres**, con incremento neto de **once filas**. No cambian los cargos de filas
con texto y actor idénticos.

### Votos que no deben confundirse — padre 1737

La frase inicial dice que Desormeaux se suma a la mayoría y luego que Claro
mantiene una votación por subir la TPM a **6,50%**. La intervención de Claro ya
no está bajo Desormeaux. Los IDs actuales son:

- **2347:** Desormeaux.
- **2348:** Claro, con su voto propio.
- **2349:** García, que comienza «Una vez adoptado el Acuerdo correspondiente…».

Se reconoció esa introducción específica para no trasladar el comentario
posterior de García al bloque de Claro. También se reconoció «Aún considerando
la explicación anterior…» en 2443 para recuperar el retorno de De Gregorio tras
la precisión de Lehmann.

### Respetar quién retoma la exposición

- **2768:** De Gregorio → Lehmann → Marshall → Lehmann. La propuesta breve de
  Lehmann se mantiene con su explicación posterior de dólar y commodities.
- **3449:** Claro → De Gregorio → Herrera → Claro. El comentario de Herrera no
  arrastra el planteamiento que Claro retoma explícitamente después.
- **4233:** Herrera → Lehmann. La precisión inicial de Lehmann y su exposición
  posterior de proyecciones de crecimiento forman un mismo segmento conservado.

Hay ahora **16 intervalos de hablante documentados**: los cuatro anteriores y
los doce de esta ronda. F1 exige que cada intervalo conserve íntegramente su
texto y actor; un límite o una cita inválidos bloquean la construcción.

## 2. Seguimiento más claro: corrección dirigida frente a cambio automático

Se añadió **`CORRECCION_DIRIGIDA_APLICADA`** para los intervalos originales que
se solapan con una corrección de hablante respaldada por el registro documental.
El estado enlaza su ID y justificación. No declara pureza semántica de todo el
intervalo original ni elimina sus alertas residuales.

Ahora hay **13 intervalos de la cola original** bajo ese estado: los doce de
esta ronda y el caso 6135 ya revisado antes. Esta reclasificación del seguimiento
no representa trece correcciones nuevas del contenido.

Balance acumulado de las **783 filas originales**:

| Estado | Filas |
|---|---:|
| Pendiente de lectura contextual | 526 |
| Fórmula procedimental reclasificada | 59 |
| Método actualizado | 65 |
| Segmentación o actor modificado por comparación | 96 |
| Corrección dirigida aplicada | 13 |
| Breve válido revisado | 7 |
| Mención legítima revisada | 8 |
| Identidad pendiente | 6 |
| Repetición sustantiva pendiente | 2 |
| Continuidad entre padres revisada | 1 |

Son 90 filas vinculadas a decisiones de lectura, 161 a comparación automática y
532 sólo a clasificación inicial. Las fórmulas continúan siendo 17 textos distintos
aplicados a sus repeticiones, no verificaciones PDF individuales. Hay 647 intervalos
originales que todavía se solapan con alguna alerta actual.

## 3. Por qué el total de alertas no bajó

El total permanece en **661 filas**. Los motivos se superponen y las filas cambian
de límites:

| Motivo | Antes | Ahora |
|---|---:|---:|
| Posible otro hablante o mención | 170 | 158 |
| Final sin puntuación de cierre | 194 | 205 |
| Atribución heurística legada | 265 | 265 |
| Anáfora local | 37 | 37 |
| Fragmento breve | 8 | 8 |
| Variante de identidad | 6 | 6 |
| Duplicado no fórmula | 2 | 2 |

Se resolvieron las mezclas documentadas, pero los límites nuevos pueden terminar
en una coma original o sin un punto antes de la conjunción. Esas advertencias
siguen visibles: no se añadió puntuación artificial para bajar el conteo. Por
ejemplo, la pregunta de Velasco termina en «ese horizonte» y la respuesta de
García comienza con «y el…».

El total de alertas no es una medida suficiente del número de errores ni del
progreso semántico. Tampoco una fila sin alertas queda automáticamente certificada.

## 4. Verificación publicada

- **136 pruebas aprobadas**, once nuevas; F0/F1 pasan sin errores bloqueantes.
- **7.219/7.219 padres** reconstruidos, ignorando sólo espacios.
- **9.153 filas físicas / 9.152 bloques**, 37 columnas de auditoría y 24 finales.
- **2.048.560 palabras**, sin variación; celda máxima **31.948 caracteres**.
- 132 sesiones, 51 etiquetas de actor y **310 fórmulas TPM contrastadas**.
- 8.777 grupos de turno, 285 de varias filas; máximo de once filas.
- Se comprobaron nuevamente las exposiciones de García **60–70** y **142–152**
  y las referencias sin cortes falsos de **3454, 3715 y 4266**.
- Hashes verificados de **33 entradas/archivos de código y diez salidas**.
- CSV de 783 filas de seguimiento, 661 pendientes, 8.777 turnos y 132 decisiones.
  `data/raw` sin cambios frente a Git; `git diff --check` sin errores.

Las pruebas incluyen coordinación sin revisión que no debe cortarse, citas que
no permiten un corte interior, menciones sin verbo de habla, sujeto incompatible,
votos separados y conservación exacta de los dieciséis intervalos documentados.

## Pendientes

Continúan los **526 intervalos sin lectura contextual adjudicada**, las seis
identidades, las dos repeticiones sustantivas y las advertencias residuales de
los intervalos modificados. Las voces conjuntas, como el padre 2126, no se han
dividido arbitrariamente: la nueva posibilidad de registrar coordinaciones no
resuelve por sí sola una declaración plural compartida.

La revisión fue del consolidado, sin cotejo PDF ni revisión humana independiente.
Se mantienen las limitaciones de la referencia TPM de Datosmacro y de los controles
que comparten reconocedores con el constructor. No se certifica la exactitud
semántica o histórica de todo el corpus.
