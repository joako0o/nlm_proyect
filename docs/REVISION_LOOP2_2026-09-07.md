# Segundo bloque de cuatro ciclos de revisión contextual

> **Informe histórico.** La publicación posterior a este bloque está en [revisión de residuos](REVISION_RESIDUOS_2026-09-07.md): 9.207 filas / 635 alertas / 222 pruebas. La respuesta en gerundio de 2981 ya se delimitó; en 780 se separó el acuerdo, pero sigue pendiente el comienzo de Corbo. Los IDs, métricas y pendientes de este documento y su checkpoint corresponden al bloque anterior. Los enlaces a `data/processed/` abren la versión vigente.

**Fecha:** 2026-09-07. **Inicio:** 9.186 filas / 650 alertas / 189 pruebas.
**Publicación:** **9.205 filas / 634 alertas / 209 pruebas; F0/F1 aprobados.**

## Alcance y entregables

Se encadenaron cuatro ciclos sin pedir confirmación entre lotes: prefijos de
pregunta/cesión, referencias al expositor, intervalos adjudicados y retornos tras
una presentación. Se leyeron los tramos afectados y su entorno; no se revisó
exhaustivamente el contenido de todas las actas ni de todos los padres. **Sin
cotejo PDF ni revisión humana independiente.**

- [Excel actualizado](../data/processed/revision_783.xlsx).
- [18 padres: hashes, IDs anteriores y 70 segmentos actuales completos](cambios_loop2_2026-09-07.csv).
- [Cambios de método y continuidad sin modificar texto/persona](metodos_continuidad_loop2_2026-09-07.csv).
- [Nuevo punto de reanudación, con pendientes identificados y candidatos](estado_revision_loop2_2026-09-07.json).
- Base final: `data/processed/consolidado_base_referencia_final.xlsx`.

El punto de reanudación es un registro, no un proceso que continúe ejecutándose
en segundo plano. Los ciclos de este bloque están terminados y publicados.

## 1. Primer ciclo: preguntas y cesiones de palabra

Se reconoció «En lo que dice relación con…» en la vista normalizada y se añadieron
los prefijos «Antes de continuar con la votación…» y «Complementando los comentarios
efectuados…». Siguen siendo necesarios sujeto y predicado de habla compatibles.

| Padre | Fecha | Corrección | Filas antes → ahora |
|---|---|---|---:|
| 298 | 2005-07-12 | Jadresic explica inventarios; Eyzaguirre formula la consulta sobre tasas forward. | 1 → 2 |
| 2167 | 2008-11-13 | Marshall termina su voto por 8,25%; el Presidente ofrece la palabra; Velasco aclara su postura. | 2 → 3 |
| 2408 | 2009-03-12 | Desormeaux comenta; Soto explica; De Ramón pregunta por el plan fiscal; Soto responde. | 2 → 4 |

La intervención de Marshall conserva más de 7.200 caracteres antes de la cesión.
La respuesta final de Soto en **2408** queda enlazada por `ID_Turno` con **2409**,
que continúa con el mismo hablante. No se considera que el cierre de un párrafo
termine necesariamente una exposición.

## 2. Segundo ciclo: el expositor mencionado no es quien pregunta

Se ajustaron dos guardas de referencia: **«del/al expositor»** y **«que ha
entregado»**. Evitan adjudicar una pregunta a la persona mencionada en el
antecedente por tomar el verbo de quien realmente pregunta.

| Padre | Fecha | Resultado final |
|---|---|---|
| 1873 | 2008-06-10 | Presidente → Marshall → Presidente → García. Soto es una referencia, no un turno. El comentario de Marshall necesitó además una adjudicación puntual del ciclo siguiente. |
| 1946 | 2008-07-10 | García → Velasco → Claro → Soto → Marfán. Claro pregunta sobre la exposición de Soto y Soto responde después. |
| 2206 | 2008-12-11 | Soto → Desormeaux → Soto. El Vicepresidente consulta sobre los datos entregados por Soto; la consulta no pertenece a Soto. |

En 2206 la exposición previa de Soto conserva más de 6.000 caracteres. En 1873
no se eliminó la restricción general sobre prefijos con otros verbos: el comentario
de Marshall se resolvió individualmente, sin abrir una regla que admita cualquier
mención de persona como hablante.

## 3. Tercer ciclo: intervalos acotados y respuestas enlazadas

Se añadieron seis entradas con fecha, hash, cita, inicio y fin:

| Padre | Fecha | Intervalo adjudicado y contexto |
|---|---|---|
| 753 | 2006-07-13 | Después de la oferta de Corbo, «Los mercados financieros nacionales, señala el señor Magendzo…» inicia la exposición de Magendzo. Se une a su continuación: **7.178 caracteres** en un tramo. |
| 1873 | 2008-06-10 | Marshall distingue transferencias de donaciones; el Presidente consulta después y García responde. Sólo se adjudica el comentario de Marshall. |
| 1718 | 2008-03-13 | Marshall menciona la fiscalización laboral; «a lo que el Consejero Marfán agrega…» abre la precisión de Marfán; luego interviene Velasco. |
| 2896 | 2010-02-11 | Vergara pregunta, Lehmann responde, García explica el precio del cobre y Lehmann retoma su exposición. |
| 2910 | 2010-02-11 | El Presidente pregunta, Soto responde 0% y García distingue anuncio, proyección y resultado fiscal. |
| 2983 | 2010-03-18 | Soto confirma los componentes; García explica las fuentes y la calibración del modelo. |

### Respuesta sin coma: excepción explícita, no regla global

Para 1718 se añadió **`RESPUESTA_A_LO_QUE_EXPLICITA`**. El constructor exige el
conector literal «a lo que el/la…», espacio previo, sujeto de habla compatible
y un límite fuera de comillas. El texto mantiene el conector y no se inventa
una coma. Estas comprobaciones se aplican incluso si el separador de oraciones
ya había propuesto el comienzo.

Sin la entrada revisada no se activa este corte. Las pruebas rechazan actor
incompatible, conector distinto, falta de espacio, cita y mención sin predicado
de habla. La referencia anterior de Magendzo a lo que dice Cowan sigue siendo
una referencia dentro del discurso de Magendzo.

Los tres comienzos con «en tanto que…» usan el límite revisado después de coma
que ya existía; no se introduce una división indiscriminada ante ese conector.

## 4. Cuarto ciclo: cierres, retornos y una sugerencia intercalada

Se reconocen «Antes de proseguir…», «Finalizada/Concluida la presentación…»,
«No habiendo más comentarios…» y «Refiriéndose ahora a…», siempre con sujeto y
verbo. Se admite la variante fuente «coméntanos» en ese prefijo concreto,
**sin reescribirla**.

| Padre | Fecha | Recuperación | Filas antes → ahora |
|---|---|---|---:|
| 2588 | 2009-06-16 | Tras Claro y la exposición de Soto, el Presidente ofrece la palabra a Cowan. Cowan empieza en 2589. | 2 → 3 |
| 2678 | 2009-08-13 | García explica; Desormeaux agrega su comentario antes de proseguir. | 1 → 2 |
| 2681 | 2009-08-13 | Se conservan más de 11.000 caracteres de García; el Presidente ofrece comentarios al final. | 1 → 2 |
| 2814 | 2009-12-15 | Claro comenta, el Presidente concede la palabra y Soto inicia la exposición nacional. | 2 → 3 |
| 2981 | 2010-03-18 | Después de García, Soto retoma inflación y escenario posterior al terremoto en **3.212 caracteres**. Véase la limitación sobre una respuesta posterior del Presidente. | 6 → 6 |
| 3007 | 2010-03-18 | Marfán → García → Marfán sugiere un escenario de riesgo → García responde. La sugerencia se adjudicó mediante una séptima entrada puntual. | 2 → 4 |
| 3147 | 2010-06-15 | Presidente → De Ramón → Presidente concede la palabra a Soto. | 2 → 3 |

No se atribuye una cesión de palabra al receptor ni se confunden las explicaciones
con los cierres. En 3007 se conserva el final dañado «No habiendo más comentarios,.»
sin inventar una voz institucional.

## 5. Comparación acumulada y validaciones

- Cambios de texto/actor sólo en **18 padres distintos**; 1873 participa en dos
  ciclos pero se cuenta una vez. Incremento neto de **19 filas**.
- **Siete intervalos nuevos** en `revisiones_hablantes.json`: 42 acumulados.
  Los cambios reconocidos por reglas se documentan en CSV y regresiones, sin
  convertir su evidencia explícita en asignaciones forzadas.
- Hashes fijos de las 18 fuentes y secuencias de atribución en
  `tests/test_loop2_review.py`. Se añadieron **20 pruebas**, para un total de **209**.
- Cero cambios de cargo para segmentos con texto y actor idénticos.
- En 2409 sólo cambia la relación a continuidad explícita. En **4596**, el texto
  y Vergara se mantienen; cambia el método de `ROL+NOMBRE` a `SUJETO_ROL_NOMBRE`
  y deja de advertirse como legado. No son nuevas correcciones de persona.
- Publicación igual por contenido al resultado preliminar comparado.
- Conservación de **7.219/7.219 padres** y **2.048.560 palabras**, ignorando sólo
  espacios en la comparación de caracteres. Excel de origen intacto frente a Git.
- Los once enlaces entre párrafos recuperados en el bloque anterior siguen
  vigentes. También las exposiciones de García de once filas en 60–70 y 142–152,
  y los negativos 3454, 3715 y 4266.
- Las seis anotaciones de menciones actuales siguen visibles; no se eliminan sus
  avisos automáticos. Las seis revisiones de cargo permanecen.
- Pipeline completo, **F0/F1 aprobados antes de publicar**, y **40 hashes de
  entradas/código más diez de salidas** verificados.

La validación comparte reconocedores con la construcción: no es auditoría
semántica independiente ni certifica todos los tramos de un padre modificado.

## 6. Métricas finales y seguimiento histórico

| Métrica | Antes | Ahora |
|---|---:|---:|
| Filas / bloques | 9.186 / 9.185 | 9.205 / 9.204 |
| Grupos de turno / multipárrafo | 8.799 / 296 | 8.817 / 297 |
| Máximo de filas por turno | 11 | 11 |
| Posible otro hablante o mención | 129 | 111 |
| Atribución anafórica | 43 | 42 |
| Atribución heurística legada | 260 | 259 |
| Final sin puntuación | 223 | 227 |
| **Filas con alguna alerta** | **650** | **634** |

Se mantienen ocho avisos de brevedad, seis de identidad y dos de duplicados no
formularios. Los duplicados exactos/formularios pasan de 557/555 a 559/557 por
la segmentación; no se elimina ninguna repetición. Siguen 132 sesiones, 37 columnas
de auditoría y 24 finales, máximo de 31.948 caracteres por celda y 310 fórmulas
TPM contrastadas.

Los motivos se superponen. **La reducción de 16 filas con alertas no equivale a
16 errores corregidos**: también intervienen cambios de método y nuevos finales
incompletos, que se mantienen sin rellenar.

| Estado de las 783 originales | Total |
|---|---:|
| Pendiente de lectura contextual | 471 |
| Fórmula procedimental reclasificada | 59 |
| Método actualizado | 71 |
| Segmentación o actor modificado por comparación | 118 |
| Corrección dirigida aplicada | 40 |
| Breve válido revisado | 7 |
| Mención legítima revisada | 8 |
| Identidad pendiente | 6 |
| Repetición sustantiva pendiente | 2 |
| Continuidad entre padres revisada | 1 |

Los 40 intervalos con corrección dirigida incluyen **ocho intervalos originales
adicionales**, no cuarenta correcciones nuevas. Se incorporaron siete decisiones:
una decisión puede afectar más de un intervalo de la instantánea. Las categorías
quedan en 117 lecturas dirigidas, 189 comparaciones y 477 triajes; 611 originales
se superponen con alguna alerta actual. Las seis lecturas actuales de menciones
se cuentan aparte. La instantánea original no se modificó.

## 7. Pendientes que no deben perderse en el siguiente ciclo

- **780:** después del voto de De Gregorio comienza «En la economía nacional…»
  sin encabezado; más adelante se nombra a Corbo. Falta delimitar el comienzo real
  de Corbo y separar su evaluación del acuerdo posterior. No se modificó el padre.
- **2981:** se recuperó el retorno de Soto, pero sigue sin separar la respuesta
  introducida por **«señalando el señor Presidente…»** dentro de la pregunta de
  Marshall. Ese residuo no queda certificado ni resuelto por el cambio anterior,
  aunque el detector no lo marque como otra voz.
- **2126 y 2661:** mantienen sus dificultades de atribución conjunta y de
  delimitación completa de voces. No se les asigna arbitrariamente un actor.

El nuevo estado guarda estos pendientes expresamente y los primeros veinte de
**97 candidatos** con aviso de otro hablante/mención sin anotación de lectura.
La lista es triaje, no revisión. No excluir un padre entero por tener una corrección
previa. Para enlazar versiones, usar padre, texto e intervalo: los IDs de fila
pueden desplazarse.
