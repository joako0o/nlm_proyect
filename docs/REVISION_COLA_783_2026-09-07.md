# Revisión de la cola de 783 alertas

> Antecedente de la ronda de 9.134 filas. La salida y el balance vigentes están
> en [Menciones y cesiones](REVISION_MENCIONES_Y_CESIONES_2026-09-07.md).

**Fecha:** 2026-09-07. **Base de partida:** 9.053 filas / 783 alertas.
**Salida:** 9.134 filas / 723 filas con alertas automáticas.

## Resultado y alcance real

Se creó un seguimiento reproducible de **cada una de las 783 filas originales**.
Esto no equivale a haber leído exhaustivamente las 783 intervenciones. La hoja
separa decisiones de lectura dirigida, cambios detectados al regenerar la base
y pendientes que sólo han recibido una clasificación inicial de prioridad.

**Entregable:** [revision_783.xlsx](../data/processed/revision_783.xlsx), con:

1. **Resumen:** resultados y advertencia de alcance.
2. **Seguimiento_783:** los 783 IDs originales, actor y texto originales, motivos,
   estado de seguimiento, tipo de revisión, IDs/actores actuales, alertas
   residuales, justificación, siguiente paso y contexto contiguo actual.
3. **Alertas_actuales:** las 723 filas que siguen disparando controles automáticos.

También se publican `revision_783.csv` y `resumen_revision_783.json`.
No se borraron filas ni se borraron automáticamente alertas por el solo hecho
de haber creado esta hoja.

## 1. Balance de las 783 filas originales

Categorías exclusivas de seguimiento; suman exactamente **783**:

| Estado | Filas | Qué significa |
|---|---:|---|
| Fórmula procedimental reclasificada | 59 | Lectura de 17 textos distintos, aplicados por coincidencia exacta salvo espacios a sus repeticiones |
| Breve válido revisado | 7 | Seis pasos de palabra completos y una respuesta afirmativa completa |
| Continuidad entre padres revisada | 1 | El fragmento de Gianelli continúa en el padre siguiente |
| Segmentación o actor modificado | 83 | Comparación automática de intervalos originales con la nueva salida; **no cierre semántico de todo el intervalo** |
| Método actualizado | 11 | Cambia la evidencia reconocida sin cambiar actor ni límites |
| Identidad pendiente | 6 | Ricaurte: no fusionar identidades sin verificación |
| Repetición sustantiva pendiente | 2 | Recomendaciones de mantener la TPM, no meras fórmulas procedimentales |
| Pendiente de lectura contextual | 614 | No se adjudicaron: requieren lectura del discurso y contexto |

Hay **69 filas vinculadas a decisiones de lectura** (59 + 7 + 1 + 2),
**94 con comparación automática** (83 + 11) y **620 sólo clasificadas inicialmente**
(614 + 6). Las 59 fórmulas se revisaron por sus **17 textos distintos**; no se
presentan como 59 verificaciones independientes contra sus PDFs.

**710 de los 783 intervalos originales** todavía se solapan con alguna alerta
actual. No contradice las 723 filas actuales: la segmentación cambió y una fila
original puede corresponder a varias filas nuevas. No deben restarse estos
conteos como si fueran la misma unidad.

## 2. Duplicados: conservar, no eliminar

Se leyeron los 19 textos distintos que originaban 61 marcas de
`DUPLICADO_NO_FORMULA` en la versión de partida. Al normalizar sólo espacios,
las 59 repeticiones procedimentales corresponden a 17 textos distintos.

Las 59 filas son solicitudes de presentar las opciones, anuncios de apertura,
saludos o pasos de palabra/votación. Ejemplos:

- «A continuación el Presidente don Vittorio Corbo solicita al Gerente de
  División Estudios, don Rodrigo Valdés, que presente las Opciones de Política
  Monetaria.»
- «El Presidente señor José De Gregorio concede la palabra al Gerente de División
  Estudios señor Luis Óscar Herrera para que presente las Opciones de Política
  Monetaria para esta Reunión.»

Se mantienen `Duplicado_Exacto=SI` y **todas las ocurrencias**; cambia la
clasificación a `Duplicado_Formula=SI`. El registro
[`formulas_revisadas.json`](../data/curation/formulas_revisadas.json) conserva
textos, hashes, padres y justificaciones. Sólo se aplica a coincidencias completas
salvo espacios; una fórmula seguida por una recomendación sustantiva no queda
automáticamente cubierta por la decisión.

Las **dos recomendaciones de Herrera** (IDs originales 6903 y 7043) siguen
marcadas: «esa Gerencia propone al Consejo mantener la Tasa de Política Monetaria
en su nivel actual». Aunque se repitan, tienen contenido de política monetaria;
no se declaran fórmula procedimental ni se deduplican sin verificar cada sesión.

## 3. Preguntas y respuestas dentro de una misma oración

Un patrón frecuente era:

> El Presidente consulta…, **a lo cual el señor … responde…**

El segmentador reconocía sujetos de oración, pero omitía muchas respuestas
introducidas por esos conectores. Ahora reconoce límites de cláusula antes de
**«a lo cual» / «a lo que»**, siempre que:

- haya coma o punto y coma previo;
- siga un sujeto con tratamiento/cargo y un verbo de habla reconocido;
- el conector no esté dentro de comillas;
- no se trate simplemente de «se refiere a lo que…» sin límite de respuesta.

Se conserva el conector en la respuesta y toda la puntuación original. No se
extendió la regla a cualquier «y el…», ni a menciones sin un verbo de habla.

Al contrastar los cambios se comprobó también el retorno del expositor con
«Al concluir su presentación», una síntesis con «Para sintetizar» y una
intervención introducida por «A modo complementario». Se reconoce «repara en»
para no perder al primer sujeto cuando el actor original pertenece a quien
responde después.

### Ejemplos contrastados

| Padre | Antes | Ahora |
|---|---|---|
| 1857 | Marfán | Marfán pregunta → Lehmann responde afirmativamente |
| 1718 | Algunas respuestas y complementos quedaban dentro de otros hablantes | Se reconocen, entre otros, Magendzo → Cowan; no se absorbe el complemento de Cowan |
| 3189 | Marshall | Marshall → García → Marfán, que sintetiza |
| 3369 | Marfán | Marfán «repara en…» → Vergara «manifiesta…» |
| 6415 | Vergara | Vergara → Bernier → Fuentes, que retoma la exposición → Vergara |

La comparación global identifica **78 padres con cambios de actor/límites** y
un incremento neto de **81 filas**, sin aumentar palabras ni perder texto.
Los 83 intervalos de la cola original afectados no son 83 errores íntegramente
cerrados: algunos conservan otras menciones o turnos todavía no resueltos.
Los cambios mecánicos están identificados como `COMPARACION_AUTOMATICA` en la
hoja, no como revisión humana o certificación semántica.

En una construcción intermedia, el padre 3369 podía quedar entero bajo Vergara
porque el comienzo «Marfán repara en…» no se reconocía. Se detectó esa regresión,
se corrigió y se añadió una prueba antes de la publicación final.

## 4. Los ocho fragmentos breves

Se documentaron individualmente en
[`revisiones_cola_783.json`](../data/curation/revisiones_cola_783.json):

- **IDs originales 409, 465, 500, 551, 608 y 671:** «El Presidente ofrece la palabra
  para comentarios.» Es una intervención completa aunque breve.
- **ID original 5645, padre 4142:** «El señor Sergio Lehmann responde afirmativamente.»
  Responde a la pregunta de De Gregorio en 4141; Herrera comenta la cuestión en
  4143. No hay evidencia de pérdida de contenido por su brevedad.
- **ID original 8424, padre 6655:** «El señor Diego Gianellí anticipa que.» continúa
  en **6656**: «uno de los escenarios de riesgo del próximo IPoM…». Se preserva
  el punto OCR y ambos padres, sin completar ni inventar texto. Las filas actuales
  **8504–8505** comparten `RPM-2015-03-19:T19` bajo Gianelli.

Estas decisiones están en el registro separado. La alerta automática de
brevedad se conserva visible; no se modifica globalmente el umbral para ocultarla.
El seguimiento verifica que la continuación de Gianelli conserve el mismo turno.

## 5. Validación reproducible

- **115 pruebas aprobadas**, 13 nuevas; F0/F1 pasan.
- **7.219/7.219 padres reconstruidos**, ignorando sólo espacios en la comparación.
- **9.134 filas / 9.133 bloques**, 37 columnas de auditoría y 24 finales.
- **2.048.560 palabras**, sin variación; mayor celda: **31.948 caracteres**.
- **132 sesiones**, 51 etiquetas de actor; **310 fórmulas TPM contrastadas**.
- **8.759 grupos de turno**, 284 de varias filas; máximo de once filas.
- Las exposiciones de García **60–70** y **142–152** mantienen sus once filas.
  Las referencias en **3454, 3715 y 4266** siguen sin dividirse por meras menciones.
- Hashes comprobados de **31 entradas/archivos de código y 10 salidas**.
- `data/raw` sin cambios frente a Git; CSV y dimensiones del Excel de seguimiento
  comprobados; `git diff --check` sin errores.

`cola_783.json` conserva la instantánea original con textos, IDs, hash de la base,
hashes de texto y posiciones por padre. El seguimiento no empareja sólo por ID:
reconstruye los intervalos originales con las nuevas filas y falla si se pierde
contenido o cambia la sesión. Los tres artefactos nuevos se construyen en staging
antes de publicar, igual que la base y sus controles.

## 6. Qué sigue pendiente

La cola actual contiene **723 filas** con motivos superpuestos:

| Motivo | Antes | Ahora |
|---|---:|---:|
| Atribución heurística legada | 333 | 321 |
| Posible otro hablante o mención | 252 | 182 |
| Final sin puntuación de cierre | 110 | 189 |
| Anáfora local | 39 | 38 |
| Duplicado no fórmula | 61 | 2 |
| Fragmento breve | 8 | 8 |
| Variante de identidad | 6 | 6 |

Las alertas de final aumentan porque las preguntas separadas pueden terminar
en la **coma original anterior al conector**, no en punto. No se borró la coma
ni se añadió un punto artificial. Se mantiene la advertencia conservadora;
**ese incremento no prueba pérdida de texto**.

La disminución de 783 a 723 no representa 60 errores confirmados corregidos.
Hay decisiones de clasificación, nuevos límites y alertas residuales que pueden
solaparse. Debe continuarse con las **614 filas sin lectura contextual adjudicada**,
las seis identidades y las dos repeticiones sustantivas. También requieren
relectura los intervalos modificados que todavía contienen alertas de hablante.

Las lecturas se hicieron sobre el consolidado, **sin cotejo PDF de estos pasajes**.
F0/F1 y el seguimiento garantizan las comprobaciones implementadas, no pureza
semántica total, exactitud histórica independiente ni revisión exhaustiva de las
783 intervenciones. Permanecen las limitaciones de la referencia TPM de Datosmacro.
