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
| `los cambios en ios precios` | `en los precios` | la i por la ele; aparece 92 veces en el corpus contra 30.883 de `los` |
| `la del MI que se ubicó en 16,1%` | `la del M1` | el contexto dice «agregados monetarios»; la i mayúscula es el dígito 1 |
| `la inflación anual del IRC` | `del IPC` | medido: `IRC` 61 veces e `IRCX1` 10, siempre en contexto de índice de precios; `IPC` 1.867. Es una confusión sistemática P→R |
| `el precio promedio sería de LJS$ 2` | `de US$ 2` | la misma fila escribe `US$ 65`, `US$ 61` y `US$ 58` correctos |
| `factores estaciónales` | `estacionales` | «estacional» es grave terminada en l: no lleva tilde |
| `un crecimiento de entre 5%% y 6%%` | `5% y 6%` | símbolo duplicado; la misma fila escribe `6,3%` con uno |
| `tercer y cuatro trimestre` | `cuarto trimestre` | la misma fila trae «cuarto trimestre del año pasado» |
| `El / Consejero / señor / Marfán, / sobre / el…` | todo en una línea | artefacto de justificación del PDF; se reúne sin alterar una letra |
| `17.30 horas.` colgado entre el Comunicado y su aprobación | se elimina | marca horaria suelta sin sujeto ni verbo; el cierre ya consigna las 18:00 |

**Tareas pendientes medidas.** Tres defectos sistemáticos del corpus están
medidos y documentados, pero sólo se corrigen en las filas ya leídas; el resto
queda pendiente y hay que liquidarlo. Ninguno admite duda, y ninguno se aplica
en bloque porque la política es fila por fila, sin reglas automáticas.

| defecto | medición | pendiente |
|---|---|---|
| `Página N de N` al pie | 26 veces en 22 filas | **20 filas en 2012-04-17**, sin leer. Ya se limpiaron `4849:3` y `5221:3` |
| `IRC` por `IPC` (erre por pe) | **71 veces en 46 filas** de 32 sesiones, todas entre 2005-04-07 y 2010-02-11; 10 de ellas son `IRCX` por `IPCX` | **65 ocurrencias en 45 filas**. Corregidas las 6 de `1994:2` en la ronda 171 |
| `yeso` por `y eso` (espacio perdido) | **13 veces en 12 filas**, todas el mismo defecto | **12 ocurrencias en 11 filas**. Corregida la de `2001:1` en la ronda 171 |

Del `IRC` se verificó caso por caso que las **71** son contexto de índice de
precios, incluidas las 18 donde la palabra «inflación» no aparece cerca: «un
par de IRC más bajos», «cuatro IRC cerca de 1%», «el IRC de octubre fue menor»,
«la publicación del IRC», «su convergencia hacia un 3% será más lenta que la
del IRC». Y el corte temporal es una pista: ninguna aparición es posterior a
2010-02-11, lo que apunta a un lote de escaneo concreto.

La pérdida de espacio es una familia propia, con su tipo
`ESPACIO_FALTANTE`: `caer yeso` (13), coma pegada a la palabra siguiente
(35 en el corpus). Es el espejo de `ESPACIO_INDEBIDO`, que cubre la palabra
partida en dos. En los dos casos la reparación es única y no altera una letra.

### 1 bis. La tilde entra aquí, no en la sección 2

`estaciónales` → `estacionales` está arriba y no pidió corroboración: la
regla de la sección 1 es que **la oración no admita otra lectura**, no que la
forma correcta aparezca en otra parte. Un acento mal puesto o faltante
pertenece a esta sección cuando la gramática deja una sola opción:

| verbatim | corregido | por qué |
|---|---|---|
| `este aún esta en discusión` | `este aún está en discusión` | «este» es el sujeto; no hay otro verbo posible |
| `la demanda agregada prevista hacía fines de año` | `prevista hacia fines de año` | «prevista» es participio, no hay verbo finito al que sujetar «hacía» |
| `Asia, Oceania y Europa emergente` | `Oceanía` | el topónimo tiene una sola grafía; no es una reconstrucción |

Esto se aplicó mal una vez: `este aún esta en discusión` (`4342:2`, ronda
141) se marcó para cotejo argumentando que «está» no aparecía en la fila. Eso
es aplicar la regla de la sección 2 a un caso de la sección 1. La marca se
retiró en la ronda 144 y se corrigió.

**Límite:** si la tilde cambia el significado y ambas lecturas son
gramaticales, no es sección 1 — es duda, y se marca. Y si lo que falta es una
**letra** y caben dos palabras, tampoco: eso es sección 2.

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

### 2 bis. La corroboración sólo se pide si la forma defectuosa es una palabra real

La regla de arriba existe para no inventar: si lo que quedó en el texto
**puede leerse de otra manera**, hace falta que el documento respalde la
enmienda. Pero cuando la forma defectuosa **no es una palabra**, no hay lectura
alternativa que proteger y el caso vuelve a la sección 1, que no exige
corroboración:

| la forma defectuosa | ¿es palabra? | decisión |
|---|---|---|
| `ratando`, `fiy to safety`, `ios`, `ai`, `de!`, `ha ¡do`, `cambíanos` | **no** | **se corrige**, con la medición como respaldo |
| `cambiarlo`, `rotación`, `fusión`, `marco`, `cambiarlos`, `hora` | **sí** | se corrige **sólo** con corroboración en fila o sesión; si no, se marca |

Aplicado tres veces: `fiy to safety` → `flight to safety` (`1425:1`, ronda 163),
`fiy to safety` de nuevo (`1465:1`, ronda 168) y `está ratando de argumentar` →
`tratando` (`2003:1`, ronda 172). En los tres, la forma defectuosa no existe en
ningún idioma y el candidato es único.

Ojo con medir bien: `'ratando'` da 28 coincidencias en el corpus, pero 27 son el
**interior de `tratando`**. Contar una subcadena sin delimitarla infla el número
y puede hacer parecer mayoritario un defecto que aparece una vez.

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

### 3 bis. NO se corrige: el defecto es del corpus entero, no de la fila

Antes de corregir un patrón sospechoso, **contarlo en todo el consolidado**.
Si aparece decenas de veces de la misma forma, es una característica de la
fuente y corregirlo fila por fila sería reescribir el acta. Medido:

| patrón | cuenta | decisión |
|---|---|---|
| `,.` al final de fila tras la fórmula de cierre (`A continuación,.` / `No habiendo más comentarios,.` / `Continuando con la votación,.`) | 98 en total, 95 de esa forma | **NO se corrige.** Es el artefacto estructural con que el acta corta la fórmula de transición |
| `— ,` (raya de cierre seguida de espacio y coma) | 85, contra 31 de `—,` | **NO se corrige.** Es la convención tipográfica del acta para los incisos |
| `IMCE` | 74 | **NO se corrige.** Es el indicador real; `del IME` y `el IME` aparecen 0 veces |
| `la Secretario General, doña Marlys Pabst Cortés` | 77 contra 0 de `la Secretaria General` | **NO se corrige.** Es la fórmula uniforme del acta en todas las sesiones, no una errata de fila. Mismo tratamiento que `contractiva`. Y es un cargo ligado a un nombre propio, que nunca se reescribe |
| `IMACEC` en versalitas | 263, contra 224 de `Imacec` | **NO se corrige.** Conviven dos grafías de la misma sigla con peso parecido y ninguna es «la» forma del corpus. Elegir una sería normalizar por estilo unas 260 ocurrencias, y eso es una regla general. Marcado en `1469:1` (ronda 169) |

El contraste con las siglas que **sí** se corrigieron en la misma ronda es la
línea operativa: `IPom` (1 vez) e `IpoM` (5) contra `IPoM` (2.477) no son una
grafía alternativa sino casos sueltos de una errata, y por eso se corrigieron
en `1462:1`. `IPOM` (59) no se tocó: es una renderización coherente. **La
pregunta no es cuántas veces aparece la variante, sino si es una grafía
sistemática o una errata aislada.**

### 3 ter. El discriminador: ¿la forma defectuosa es ortográficamente imposible?

Contar no basta, porque `cambiaría` (241), `ios` (92) e `índica` (45) también
se repiten por todo el corpus y **sí** se corrigen. Lo que separa los dos
grupos no es la frecuencia:

| la forma defectuosa… | ejemplos | decisión |
|---|---|---|
| **es ortográficamente imposible** (no existe esa palabra, esa tilde o ese glifo) | `cambiaría` por el adjetivo, `ios`, `índica`, `de!`, `lineas`, `vísta`, `perecióles`, `IPCXI` | **se corrige**, sin importar cuántas veces se repita |
| **es una construcción legítima aunque minoritaria** | `la Secretario General` (77), `precio petróleo` (8 en 7 sesiones), `IMACEC`/`Imacec`, `Economista Sénior`, `tasa de instancia` | **no se corrige**: es el uso de quien transcribe |

Y hay una señal adicional que confirma el segundo grupo: **un defecto de
escaneo no se reproduce idéntico en documentos escaneados con años de
diferencia**. `el precio petróleo` aparece 8 veces en 7 sesiones entre 2006 y
2015 (`630:1`, `992:1`, `1572:2`, `1697:2`, `1982:1`, `4242:1`, `6872:1`).
Ningún escáner hace eso; los tipógrafos sí. Marcado en `1982:1` (ronda 170).

Lo mismo rige para la ortografía **vigente en la fecha del acta**: la tilde de
`ó` entre cifras (`3% ó 4%`) era obligatoria hasta 2010 y esta acta es de 2008.
`% ó ` aparece 12 veces, todas entre 2005 y 2011. No es defecto. Mismo caso que
`Economista Sénior` con tilde en las actas de 2007.

El mismo patrón en **una sola** fila y fuera de su forma habitual sí es
defecto: `la Zona Euro,. Al respecto` (`4390:1`) tiene la coma suelta a mitad
de fila, no tras la fórmula de cierre, y se corrigió. La diferencia no está en
el símbolo sino en si el corpus lo hace así siempre o sólo ahí.

Esto también se aplicó mal una vez, en sentido contrario a la sección 1 bis:
`la Secretario General` (`4334:1`, ronda 141) se marcó para cotejo con el
argumento de que «Secretaria General» no aparecía en la fila. Medido después
en todo el corpus, la forma del acta aparece **77 veces** y la «corregida»
**0 veces**: no hay errata que cotejar, es el uso uniforme de la fuente. La
marca se retiró en la ronda 148.

## 4. NO se corrige: es real

Los falsos positivos más peligrosos. Un detector automático los destruye.

| caso | qué es en realidad |
|---|---|
| `Bío Bío` | **topónimo**. Aparece como «palabra duplicada» |
| `TCM, TCM-5 y TCM-X` | **abreviatura** de Tipo de Cambio Multilateral. Son las 6 coincidencias de «tcm tcm» del escaneo |
| `IPCX`, `IPCX1`, `IPCSAE`, `BCP-2`, `BCU-5` | nombres de indicadores |
| `IMCE` | indicador real. Aparece 74 veces; `del IME` y `el IME` aparecen 0 |
| `M1A` | agregado monetario real, no un `MI` mal leído |
| `tasa de instancia` | **el caso más peligroso encontrado.** Parece errata de «tasa de interés», pero aparece **58 veces en 53 filas** entre 2005 y 2009 y era el nombre histórico de la tasa de política monetaria. La fila `273:1` lo dice sola: «decidió elevar la tasa de instancia monetaria, **como se llamaba**» |
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
`distintos recursos anuales`, `en el últimos dos días` (¿`el último` o
`los últimos`? la forma buena aparece 0 veces en la fila y en la sesión),
`En el caso del los IREM` (¿`de los` o `del`? ambas atestiguadas),
`mercado wall forward` (¿`mercado forward` o `swap forward`?),
`La rotación del tipo de cambio` (casi seguro `flotación`, pero `flotación`
aparece 0 veces en la fila y en la sesión y la reparación cambia tres letras).

### 8 bis. Antes de marcar un residuo, buscarlo en todo el corpus

Un residuo de glifos puede parecer irrecuperable y no serlo. `s/70c/(`
(`1467:1`, ronda 169) se leía como basura, pero aparece **3 veces** en el
consolidado y en `RPM-2007-11-13:1536:1` convive con la forma bien escrita en
la misma frase y en posición paralela: «sensible a **shocks** de términos de
intercambio que a **s/70c/(s** financieros». Eso prueba la lectura
(`s`→s, `/`→h, `70`→ho, `/(`→k) con evidencia del propio documento, no con
vocabulario mío. Se corrigió en `1467:1` y en `1536:1`; la tercera ocurrencia,
`RPM-2008-08-14:2042:1`, queda para su ronda.

**Regla:** un residuo que ocupa el lugar de una palabra no se elimina ni se
marca sin antes contar sus ocurrencias en el corpus. Si aparece más de una vez,
alguna puede estar al lado de la forma correcta y zanjar la lectura. Eliminar
en cambio sigue siendo lo correcto cuando el residuo no reemplaza a ninguna
palabra (`s - f '`, `^ / ■ -i`, `f ' '`, `/ '`, `H ^ .`, numeración de página).


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
