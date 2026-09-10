# Criterio de corrección de OCR — casos ya decididos

Este archivo existe porque la regla abstracta no basta. Quien lea una fila
tiene que decidir en segundos si algo es un defecto de lectura óptica, un
error del hablante, una abreviatura real o un texto dañado sin reconstrucción
posible. Abajo están los casos reales ya resueltos, con el porqué. **Antes de
corregir algo nuevo, busca aquí el caso más parecido.**

Regla de fondo: **`Texto` nunca se toca.** Todo lo que se decide va en
`Texto_Corregido` (si se corrige) o en `Cotejar_PDF` (si no se puede resolver).
Nada se pierde y nada se adivina.

---

## 1. Se corrige: un glifo mal leído

El carácter equivocado está donde debería ir otro, y la oración no admite
otra lectura.

| verbatim | corregido | por qué |
|---|---|---|
| `bajo la presidencia de! titular` | `del titular` | el `!` ocupa el lugar de la ele; la fórmula de apertura de acta es fija en todo el corpus |
| `£1 peso se ha apreciado` | `El peso se ha apreciado` | `£` y `1` por `E` y `l`; «£1 peso» no es cifra posible antes de «se ha apreciado» |
| `indica ai señor Ministro` | `al señor Ministro` | la i por la ele en la contracción |
| `los cambios en ios precios` | `en los precios` | la i por la ele; aparece 91 veces en el corpus |
| `la del MI que se ubicó en 16,1%` | `la del M1` | el contexto dice «agregados monetarios»; la i mayúscula es el dígito 1 |
| `la inflación anual del IRC` | `del IPC` | medido: `IRC` 61 veces e `IRCX1` 10, siempre en contexto de índice de precios; `IPC` 1.867. Es una confusión sistemática P→R |
| `el precio promedio sería de LJS$ 2` | `de US$ 2` | la misma fila escribe `US$ 65`, `US$ 61` y `US$ 58` correctos |
| `factores estaciónales` | `estacionales` | «estacional» es grave terminada en l: no lleva tilde |
| `un crecimiento de entre 5%% y 6%%` | `5% y 6%` | símbolo duplicado; la misma fila escribe `6,3%` con uno |
| `tercer y cuatro trimestre` | `cuarto trimestre` | la misma fila trae «cuarto trimestre del año pasado» |
| `El / Consejero / señor / Marfán, / sobre / el…` | todo en una línea | artefacto de justificación del PDF; se reúne sin alterar una letra |
| `17.30 horas.` colgado entre el Comunicado y su aprobación | se elimina | marca horaria suelta sin sujeto ni verbo; el cierre ya consigna las 18:00 |

## 2. Se corrige: palabra omitida, **sólo con corroboración**

Falta una palabra. Se repone **únicamente si la forma correcta está en la
misma fila o en la misma sesión**. Si no está, se marca para cotejar.

| caso | decisión | evidencia |
|---|---|---|
| `la alta base comparación` | **se corrige** a `alta base de comparación` | la misma fila trae «la alta base de comparación de septiembre de 2005» |
| `Menciona los inventarios de petróleo` | **se corrige** a `Menciona que los inventarios` | la misma fila trae «Menciona además, que las presiones…» |
| `podría observase ya a partir del` | **se corrige** a `observarse` | después del condicional sólo cabe infinitivo |
| `habrá que ponderados en nuestras` | **se corrige** a `ponderarlos` | sustitución de un solo carácter, r por d |
| `El peso estuvo estable con respecto el dólar` | **NO se corrige**, se marca | medí la sesión completa: `con respecto al` aparece **0 veces**. No hay forma correcta en el documento que respalde la enmienda |
| `cuando se le cobra el consumidor` | **NO se corrige**, se marca | no hay otra ocurrencia de la fórmula en la fila |

## 3. NO se corrige: no es lectura óptica

| caso | por qué |
|---|---|
| `han habido salidas` | solecismo del hablante. Corregirlo sería editar el discurso |
| `el delta en dólares` | «delta» es la palabra que usó el Ministro |
| `un poco outlier` | anglicismo técnico, de uso normal en estas minutas |
| `resulta mejor que los precios` | discordancia de número: gramática del hablante |
| `contractiva` (por contractivo/restrictiva) | aparece igual en 887:1, 926:1 y 929:1: uso consistente del transcriptor |
| `pero si está vinculado a otro fenómeno` | `si` condicional **correcto**; ponerle tilde cambia el sentido |
| `solo` y `sólo` conviviendo en la misma fila | desde la Ortografía de 2010 el adverbio no exige tilde: es estilo, no OCR |

## 4. NO se corrige: es real

Los falsos positivos más peligrosos. Un detector automático los destruye.

| caso | qué es en realidad |
|---|---|
| `Bío Bío` | **topónimo**. Aparece como «palabra duplicada» |
| `TCM, TCM-5 y TCM-X` | **abreviatura** de Tipo de Cambio Multilateral. Son las 6 coincidencias de «tcm tcm» del escaneo |
| `IPCX`, `IPCX1`, `IPCSAE`, `BCP-2`, `BCU-5` | nombres de indicadores |
| `ACTA CORRESPONDIENTE A LA SESION DE POLITICA MONETARIA` | encabezado en versales sin tildes: convención tipográfica de la fuente |
| `Fecha Sesión de Política Monetaria del mes de julio de 2006.` | campo del formulario fuente, no residuo. Lleva información |

## 5. NO se corrige: nombre propio → **siempre se marca**

`don Kiaus Schmidt-Hebbei Dunker` en `RPM-2006-01-12:527:1`. El nombre real
es Klaus Schmidt-Hebbel y las dos desviaciones son **exactamente el glifo
i-por-l que sí se corrige** en `ios`→`los` y `MI`→`M1`.

Aun así **no se corrige**: la resolución de identidad vive en `Actor_Final` y
no se toca. Hay instrucción vigente de tratar las variantes de nombre como
tratamiento documental — es la regla que mantiene «Claudia Raddatz»,
«Claudios Soto», Bermúdez/Vintimilla y Ricaurte tal cual.

Se marca `NOMBRE_PROPIO_POR_COTEJAR` y se registra el motivo. Corregir la
grafía de un nombre es una decisión sobre identidad, no sobre un carácter.

## 6. NO se corrige: datos de la fuente

| caso | por qué |
|---|---|
| `US$ 58 el barril` (881:1) vs `US$ 66 el barril` (882:1), misma sesión | inconsistencia **del documento**. Se marca `CIFRA_INCONSISTENTE_POR_COTEJAR` |
| `la inflación entre 2 y 10 años… está anclada al 10%` | inverosímil frente a una meta de 3%, pero es un dato declarado. Tocar un número es falsear la fuente |
| `Gerente de Análisis Financiero señor Igal Magendzo` (906:1) | el acta y otras filas lo listan como Gerente de Análisis **Macroeconómico**. Es error del original, no OCR. Se marca `CARGO_EN_DISCURSO_POR_COTEJAR` |

## 7. NO se corrige: falta un signo

Falta un `%`, una coma, una tilde en un lugar donde no cambia el sentido.
Agregar un carácter ausente es editorializar. Se marca
`SIGNO_AUSENTE_POR_COTEJAR`.

| caso |
|---|
| `variaciones de -0,9%, -1,1 y -0,8%` |
| `habría sido un 9,8.` |
| `algún indicador por ejemplo, de tasa media` |

## 8. Se marca: texto dañado sin reconstrucción única

Más de una lectura posible ⇒ `RECONSTRUCCION_AMBIGUA_POR_COTEJAR`. Ejemplos
reales: `el pozo concentrado` (¿peso? ¿puesto? ¿plazo?), `Al antes comentando
incremento`, `lo de anticipábamos`, `de los cuales sería`, `un desarrollo es
muy largo` (probablemente «desfase», pero el cambio es demasiado grande),
`distintos recursos anuales`.

---

## El procedimiento que no se salta

1. Leer la fila **completa**. Nunca corregir desde el fragmento.
2. Verificar el `Antes` contra el texto fuente **antes** de escribirlo, con un
   conteo real. El validador lo exige y lo rechaza si no aparece.
3. Dos operaciones de una misma fila **no pueden pisarse**: el `Antes` de cada
   una debe existir en el texto virgen, no en el intermedio.
4. Buscar la forma correcta en la fila y en la sesión antes de reponer una
   palabra omitida. Si no está, se marca.
5. Si dudas entre corregir y marcar: **marcar**. Marcar de más cuesta una
   línea; corregir de más falsea la fuente.
