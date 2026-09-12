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
| `nesgo` por `riesgo` | **29 veces en 29 filas**, y las 29 son hueco de `riesgo`, nunca de `sesgo` | **28 ocurrencias en 28 filas**. Corregida la de `2043:1` en la ronda 177. Ya estaba como ejemplo en la tabla de la sección 1 |
| oración de plantilla repetida con el mismo defecto | `de la mayoría las monedas frente al dólar` aparece **3 veces**: `6867:1` y `6876:1` (2015-07-14) y `6920:1` (2015-08-13) | **2 filas en 2015-07-14**, sin leer. Corregida la de `6920:1` en la ronda 178 |
| `en tomo a` por `en torno a` (erre perdida) | **24 veces** en el corpus; `en torno a` aparece **1.678** | **23 ocurrencias**. Corregida la de `6941:1` en la ronda 179 |
| punto como separador decimal | `0.9` aparece **3 veces**: `6937:1` y dos en `2088:1` (2008-09-04). El patrón dígito.dígito aparece 388 veces pero casi todas son miles (`US$ 2.969`) u horas (`17.10 hrs.`) | **2 ocurrencias en `2088:1`**, sin leer. Corregida la de `6937:1` en la ronda 179 |

El último caso merece atención porque parece un patrón legítimo y no lo es.
Que una cadena aparezca varias veces no la hace correcta: aquí el área repite
mes a mes la misma oración de presentación internacional, así que el defecto se
copió tres veces. La prueba es que `la mayoría de las` aparece 89 veces en el
corpus y `la mayoría las` sólo en esas 3, todas idénticas.

Del `IRC` se verificó caso por caso que las **71** son contexto de índice de
precios, incluidas las 18 donde la palabra «inflación» no aparece cerca: «un
par de IRC más bajos», «cuatro IRC cerca de 1%», «el IRC de octubre fue menor»,
«la publicación del IRC», «su convergencia hacia un 3% será más lenta que la
del IRC». Y el corte temporal es una pista: ninguna aparición es posterior a
2010-02-11, lo que apunta a un lote de escaneo concreto.

De `nesgo` se verificó una por una las **29**: «dicho nesgo es importante»,
«inclinación por nesgo», «escenario de nesgo», «premios por nesgo», «poner en
nesgo la recuperación», «primas de nesgo». Ninguna es hueco de `sesgo`, que
aparece 800 veces pero en marcos distintos («sesgo al alza», «sin sesgo»).

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

### 1 ter. Espacio dentro de una palabra: se reúne y se tipa `PALABRA_PARTIDA`

El OCR parte palabras con un espacio intrapalabra: `M arket`, `m ateria`,
`crecim iento`, `sim plem ente`, `efectivam ente`, `subirl a`. Se reúnen **sin
alterar una letra**, igual que la tilde de la sección 1: no hay lectura
alternativa que proteger, así que no se pide corroboración. Cuando la palabra
resultante no aparece en el corpus (`debido a la m ayor demanda`) se corrige
igual, porque lo único que se hizo fue quitar un espacio.

**El tipo importa y estuvo mal puesto.** Hay tres tipos distintos y se
confunden con facilidad:

| tipo | cuándo | ejemplo |
|---|---|---|
| `PALABRA_PARTIDA` | el espacio cae **entre dos letras** de una palabra | `m ateria` → `materia` |
| `ESPACIO_INDEBIDO` | el espacio cae **junto a un signo** | `simultánea , en cambio` → `simultánea, en cambio` |
| `ESPACIO_FALTANTE` | el espacio **falta** | `un13%` → `un 13%` |

En la ronda 179 se auditó el registro entero y **32 operaciones estaban tipadas
`ESPACIO_INDEBIDO` siendo `PALABRA_PARTIDA`**, más una (`un13%`) que era
`ESPACIO_FALTANTE`. Las 33 se reclasificaron. Un `Antes` y un `Despues` que
coinciden al quitarles todos los espacios no bastan para decidir: hay que mirar
**qué hay a cada lado del espacio**.

### 1 quáter. Una fila duplicada entera

`6926:2` (2015-08-13) medía 341 caracteres y era **exactamente** frase + espacio
+ frase, con la frase de 170 repetida dos veces. Verificado carácter por
carácter, no a ojo. Es la **única** fila de las 9.723 con una oración de más de
40 caracteres repetida dos veces seguidas, y la misma oración aparece
correctamente, una sola vez, en otras 8 filas de 2015. Con la forma buena
documentada ocho veces no hay lectura en que la repetición sea intencional: es
una fórmula de transición del acta, no un énfasis. Se eliminó la segunda copia
sin tocar una letra de la primera, tipo `PALABRA_DUPLICADA`.

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

**La prueba, en una línea: ¿la oración se puede leer con la palabra defectuosa?**
Si **sí**, existe una lectura alternativa que proteger y hace falta
corroboración en la fila o en la sesión. Si **no**, la reparación está forzada
y se corrige.

| forma defectuosa | ¿se puede leer? | decisión |
|---|---|---|
| `un alza en el control de endeudamiento` | **sí** («el control del endeudamiento» tiene sentido) | **marcar** |
| `implicancias cambiarlas de distinto ciclo` | no (un infinitivo no puede ser adjetivo) | corregir |
| `se ha tomado más sombrío` | no (`tomarse` no admite ese complemento) | corregir |
| `un retomo a prácticas habituales` | no (tras el artículo `un` sólo cabe sustantivo) | corregir |
| `no se cuenta que datos desagregados` | no, pero la sustitución cambia letras por completo (`que`→`con`) | **marcar** |

La última fila es el límite: cuando lo que falta **no es un glifo de la misma
palabra** sino otra palabra entera, la sección 2 manda aunque la oración no se
sostenga, porque ahí sí se está inventando vocabulario.

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

**Toda la familia `cambiar*` va en el primer grupo.** No es sólo `cambiaría`:
también `cambiarlas`, `cambiarlo`, `cambiarlos`. Las **8** ocurrencias de
`cambiarlas` del corpus están en posición de adjetivo — `paridades cambiarlas`
(4), `implicancias cambiarlas`, `expectativas cambiarlas`, `coberturas
cambiarlas`, `tensiones financieras y cambiarlas` — y `cambiarias` aparece
**19** veces en exactamente esos marcos: `paridades cambiarias`, `tensiones
cambiarias`, `expectativas cambiarias`, `primas cambiarias`, `licitaciones
cambiarias`. La diferencia es un solo glifo (ele o tilde por i) y el lugar
admite una sola categoría gramatical.

Esto costó una marca equivocada. En la ronda 175 se marcó `implicancias
cambiarlas` (`2044:1`) por falta de corroboración en la fila y en la sesión, y
en la 178 se corrigió `depreciación cambiaría` (`6920:1`) citando esta sección.
**Las dos decisiones no podían ser correctas a la vez.** La que estaba mal era
la marca: se corrigió en la ronda 180 y la marca de esa fila se achicó al único
caso que sigue en pie, `control de endeudamiento`.

**Regla de consistencia:** cuando el mismo defecto aparezca dos veces en
sesiones distintas, buscar la otra decisión antes de decidir. Un criterio que
se aplica de una forma en una fila y de otra en la siguiente no es un criterio.

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

### 5 bis. La única excepción: **reunir** un nombre que el corpus ya escribe bien

La regla de arriba prohíbe **resolver** (decidir que «Claudios Soto» es
«Claudio Soto») e **inventar** (poner una grafía que no consta en ninguna
parte). No prohíbe una tercera cosa, distinta: **reunir** un nombre que el
scanner partió, cuando el propio corpus trae la forma correcta referida a la
misma persona.

La prueba, y es la que autoriza o bloquea el caso:

> **¿La forma correcta aparece en el corpus, o en la lista de asistencia de la
> sesión, referida a la misma persona?** Si sí → se reúne. Si no → se marca.

| caso | forma correcta en el corpus | decisión |
|---|---|---|
| `Schmidt- Hebbel` (5) | `Schmidt-Hebbel` **122** + lista de asistencia «don Klaus Schmidt-Hebbel Dunker» | **reunir** |
| `Schmidt-⏎Hebbel` (1) | idem | **reunir** |
| `Marf án` (1) | `Marfán` **1.505** + «don Manuel Marfán Lewis» | **reunir** |
| `Claudios Soto` | `Claudio Soto` **no aparece en ninguna parte** | **marcar** |
| `don Kiaus Schmidt-Hebbei` | la forma correcta existe, pero aquí hay que **cambiar letras**, no quitar un espacio | **marcar** |

Las dos últimas filas son las que contienen la excepción. `Claudios Soto` no
pasa porque no hay testigo. `Kiaus Schmidt-Hebbei` no pasa porque reunir no
alcanza: habría que decidir que la `K` es `Kl` y la `ei` final es `el`, y eso
ya es reescribir la grafía.

La excepción sólo cubre **quitar un espacio o un salto de línea** dentro de un
nombre. Nunca cambiar una letra.

Dos datos que sostienen que el riesgo es bajo: las 7 ocurrencias totales, y
`Actor_Final` — la columna que de verdad consume la tarea de identificar
hablantes — ya estaba correcta en las 6 filas afectadas.

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

### 8 ter. Contar también antes de **eliminar**: la cadena puede ser legítima

El caso contrario existe y es más peligroso, porque eliminar texto bueno no
deja rastro. `U)` aparece **14 veces** en el corpus y a simple vista es basura,
pero **8 de esas 14 son el cierre legítimo de una sigla**: `(BCU)` 2 veces,
`(CLU)` 5 y `(NAIRU)` 1. Sólo 6 son residuos sueltos (`310:1`, `1379:1`,
`1484:1`, `1817:1`, `1847:1` que trae `U U)`, y `2024:1`). Una regla ciega de
borrar `U)` habría destruido ocho siglas reales.

**Regla:** antes de eliminar una cadena, contarla y mirar **todas** sus
ocurrencias con contexto. Se elimina la ocurrencia que no forma nada, no la
cadena.

El caso inverso confirma que es la medición la que manda, no una regla previa.
` V ` con espacios aparece **13 veces** y el reparto se invierte: **11 son
residuos sueltos** (`206:3`, `1004:1`, `1013:3`, `2041:1`, `3597:1`, `3914:1`,
`3939:1`, `4121:1`, `5066:1`, `5326:1`, `6009:4`) y sólo 2 son usos legítimos
de la letra como figura («descarta que sea una V porque no hay un rebote», «un
camino intermedio entre la V y la W»). Con `M)` era 1 residuo contra 77 siglas;
con ` V ` son 11 residuos contra 2 figuras. Dos cadenas de una letra, dos
respuestas opuestas, y en las dos gana el conteo.


---

## 9. Pase en bloque: sólo con precisión medida por regla

Un defecto sistemático es el que el scanner produce siempre igual, así que se
repite idéntico en decenas de filas. Corregirlo fila por fila al leer cuesta
~13 filas por turno; en bloque cuesta uno. Pero **la precisión no es del lote,
es de cada regla**, y hay que medirla antes:

| regla | ocurrencias | falsos positivos | precisión | decisión |
|---|---|---|---|---|
| `IRC`→`IPC` | 71 | 0 | 100 % | bloque |
| `nesgo`→`riesgo` | 29 | 0 | 100 % | bloque |
| `yeso`→`y eso` | 13 | 0 | 100 % | bloque |
| `en tomo a(l)`→`en torno a(l)` | 24 | 0 | 100 % | bloque |
| `Página N de N` | 26 | 0 | 100 % | bloque |
| `cambiaría`→`cambiaria` | 241 | **3** | 98,8 % | bloque **con exclusión** |
| `cambiarl[oa]s?`→`cambiari[oa]s?` | 89 | **6** | 93,3 % | bloque **con exclusión** |

Las 9 excluidas son formas verbales legítimas que una regla ciega habría
corrompido: «cuánto **cambiaría** la estimación», «no **cambiaría** el sesgo»,
«habría que **cambiarlos** por papeles», «no puede **cambiarlo**». El
discriminador mecánico es la palabra que precede (`no`, `cuánto`, `hay que`,
`para`, `puede`…) y se verificó que **ninguna fila mezcla** la forma verbal con
la adjetiva, lo que permite excluir por fila entera.

Tres reglas del procedimiento en bloque:

1. **Medir la forma suelta y la delimitada.** `cambiaría` suelto son 241 pero
   `\bcambiaría\b` son 188: la diferencia está dentro de `cambiarías`, y
   reemplazar la corta arregla también la larga. Lo mismo con `IRC`/`IRCX1` y
   `en tomo a`/`en tomo al`. Y al revés: `\bcambiar[íi]a\b` captura también la
   forma **correcta** `cambiaria`, así que ese patrón no sirve.
2. **Verificar de punta a punta contra la release**, no contra el registro:
   contar qué queda del defecto y qué creció en la forma buena, y comprobar que
   las formas legítimas excluidas **siguen intactas**.
3. **Cada nivel va en su propio commit**, con el conteo antes y después.

Lo que **no** se hizo en bloque, y por qué:

- `A continuación,.` — **76 filas**. Es decisión de bloque por tamaño, pero hay
  instrucción expresa de dejarlo intacto. Sigue pendiente.
- ~~66 comillas rectas que forman pares enteramente rectos o quedan huérfanas: sin
  desequilibrio no hay prueba de defecto. Convertirlas sería normalización
  tipográfica, no reparación.~~ **Corregido más abajo (§9 bis): el razonamiento
  era falso.**

## 9 bis. Las comillas rectas: el desequilibrio daba la dirección, no el defecto

Se había escrito aquí que un par enteramente recto no era defecto porque «sin
desequilibrio no hay prueba». Eso es un error y se revierte. El desequilibrio
entre `“` y `”` nunca probó que hubiera defecto: sólo permitió saber **cuál de
las dos rectas abría y cuál cerraba**. El defecto es el mismo en los dos casos
—el escáner produjo `"` donde el documento tenía comilla tipográfica—, y la
prueba no es el desequilibrio sino la norma del corpus: `“` aparece 323 veces
por 123 comillas rectas.

Lo que cambia es sólo qué se puede hacer con cada una:

| situación | filas | comillas | acción |
|---|---|---|---|
| par completo (cantidad par por fila) | 23 | 52 | convertir: la 1.ª de cada par abre, la 2.ª cierra |
| cierre de una cita que abre con `“` | 1 (`6438:3`) | 1 | convertir en `”` |
| cantidad impar por fila | 5 | 5 | **dejar y marcar** `RECONSTRUCCION_AMBIGUA_POR_COTEJAR` |

Las tres filas con 4 rectas son dos pares cada una (`"alerta inflacionaria"` +
`"emergencia inflacionaria"`, `"a la baja"` + `"neutral"`, `"El Niño"` ×2) y se
verificó una por una. Las dos `"El Niño"` idénticas van en una sola operación
con `Ocurrencias: 2`, porque exigir un fragmento distinto inventaría contexto.

**Resultado medido sobre la salida: 123 comillas rectas en la base → 5.** Las 5
que quedan son las filas impares, y las 5 están marcadas para cotejo.

Sigue abierta, sin regla, la población de **25 filas sin comillas rectas y con
`“` ≠ `”`**: ahí no hay recta que reparar y decidir si falta un cierre o sobra
una apertura no sale del texto.

## 10. Confusión de glifos parecidos (i / I / l / 1 / 0 / O)

Es una familia de defectos real y transversal, pero **no admite una regla ciega**: el mismo
patrón captura formas legítimas. Se corrigió caso por caso (23 ocurrencias en 20 filas,
ronda 186), con dos condiciones simultáneas: que la forma correcta esté atestiguada en el
corpus y que no haya más de un candidato.

Corregidos: `yieId`→`yield` (11:1), `cambIario`→`cambiario` (157:1), `i1iquidez`→`iliquidez`
(10:1), `f1exibilización`, `proxImos`→`próximos` (1.172:1), `opIrnon`→`opinión` (1.867:1),
`economIca`→`económica` (667:1), `opin1on` y `op1nion`→`opinión`, `1O`→`10` (10 apariciones,
tres de ellas dentro de años: `201O`→`2010`), `1nstitución`→`Institución`,
`1nstituto`→`Instituto` (75:1 para la fórmula completa), `7ay/or`→`Taylor` (33:1),
`í\/1onetaria`→`Monetaria` (1.411:1 para «Tasa de Política Monetaria»).

**Excluidos por ser legítimos, medido:** `3pp` (3) y `1pp` (1) son puntos porcentuales
(«0,3pp. mayor que el del Informe»), no dígitos mal leídos; y las mayúsculas internas de
nombres reales (`UniCredit` 6, `BancoEstado` 3, `McGuire` 2, `EuroCoin` 1) no son defectos.
Una regla sobre «mayúscula dentro de palabra» los habría roto.

**Cuando el arreglo mínimo y la forma atestiguada discrepan, se marca y no se elige.** Caso
`RPM-2007-07-12:1312:1`: «efectos `fIy` to quality». Corregir sólo el glifo da «fly to
quality», que no aparece ninguna vez en el corpus; la expresión financiera estándar es
«flight to quality», que aparece 21 veces, pero escribirla exige insertar cuatro letras, lo
que es reconstruir. Marcada `RECONSTRUCCION_AMBIGUA_POR_COTEJAR` y dejada intacta.

> **Actualización (§12): esta marca se retiró.** Al demostrar la regla `l`→`i` con 26 casos
> independientes de `ai` por `al`, la ambigüedad se resolvió a favor de `fly`: un escáner no
> convierte «flight» en «fiy» (sería borrar cuatro letras) y sí convierte «fly» en «fiy».
> Lección general: una marca por ambigüedad es provisional. Si después aparece una regla de
> glifo que explique la forma dañada, la ambigüedad desaparece y hay que volver sobre la marca.

## 11. El encabezado de página letra por letra

`B A N C O C E N T R A L D E C H I L E` —el encabezado del PDF, capturado letra
por letra— aparece **11 veces en 11 filas** y la forma normal `BANCO CENTRAL DE
CHILE` **ninguna**: cuando está presente, siempre viene así. Es residuo de la
fuente y se elimina (misma familia que números de página, marcas de hora y
firmas truncadas).

Tres cosas que salieron al aplicarlo, y que son la razón de verificar contra la
salida y no contra el registro:

1. **Una variante puede ser subcadena de otra.** Buscar el encabezado completo y
   el truncado `…D E C H` por separado dio 21 hallazgos sobre 11 reales: el
   truncado está dentro del completo. La validación lo acusó y hubo que
   emparejar por prefijo y dejar que la cola decida.
2. **El espaciado de la cola varía.** Una fila (`5367:1`) tiene `…D E C H IL E`,
   sin espacio entre `I` y `L`. Con una sola cola esperada, esa fila quedó con el
   residuo `IL E` colgando. Se cubren las cuatro combinaciones.
3. **El reemplazo debe decidir el espacio.** Si el encabezado está en medio del
   texto queda **un** espacio; si está en un borde, ninguno. También se absorbe
   un carácter de ruido pegado (`…nacional. i B A N C O…`): esas tres filas
   llevan una `i` suelta delante.

Verificado sobre la salida: encabezado **11 → 0**, residuo `IL E` **0**, y
ninguna de las 11 filas quedó con espacio doble ni con espacio inicial o final.

## 12. La regla `l`→`i` y las letras sueltas entre oraciones

**`ai` por `al`.** Medido en toda la salida: 26 apariciones de la palabra suelta `ai` en 26
filas. `ai` no es palabra del español; `al alza` aparece 1.405 veces contra 3 de `ai alza`. Se
revisaron las 26 y en todas el contexto exige `al` («asociadas ai sector exportador»,
«autorizó ai Banco Central», «Agrega que, ai respecto», «superior ai 9,5%»). Verificado sobre
la salida: palabra suelta `ai` **31 → 0** contando desde la base (son 31 y no 26 porque cinco
ya habían caído en pasadas anteriores).

Esta regla es la que resuelve el caso de §10: `fiy`/`fIy` → `fly`, 9 apariciones en 6 filas.
`flight to quality` (21 apariciones) es la otra grafía, correcta, y no se toca.

**Letra mayúscula suelta entre dos oraciones** («…últimos meses. V La colocación…»). Ruido de
escaneo: la oración anterior cierra en punto y la siguiente abre con mayúscula y sentido
completo, así que la letra no pertenece a ninguna de las dos. 17 casos en 17 filas, letras
V, H, L, U, A, M, Y, B, revisados uno por uno. Verificado: **27 → 0** desde la base. Dos
excepciones que una regla ciega habría estropeado:

- `RPM-2007-01-11:1055:1` «prolongado. **A SU** juicio»: la `A` abre la oración
  legítimamente; el defecto es `SU` en mayúscula. Se corrige la mayúscula, no se elimina.
- `RPM-2008-05-08:1847:1` «…u otra. **U U)** Menciona»: dos residuos contiguos. Eliminar sólo
  el primero dejaría «U) Menciona». Van en una sola operación.

Tres residuos puntuales más: el encabezado de página `Sesión N° 147 15.12.09 22.-` incrustado
entre dos oraciones (`2839:2`) y la basura `B A 'i` al final de `5821:1`.

**Sin decidir:** las corridas de guiones bajos `_____` (37 apariciones en 29 filas), línea de
formulario del acta. No medidas ni tratadas.

## 13. `!` por `l`, `ios` por `los`, y cómo se compone un fragmento

**`X!` → `Xl`.** 47 apariciones; todas dan palabra válida al reponer la ele: `de!` 31,
`coyuntura!` 2, `a!` 2, `e!` 2, `diferencia!`, `rea!`, `genera!`, `anua!`, `metano!`. Los cuatro
casos límite se leyeron en contexto («en algo a! alza», «precisa que e! planteamiento»,
«acceso a! financiamiento», «sobre e! Mecanismo»); ninguno es una exclamación.

**`ios` → `los`.** 94 apariciones contra 32.215 de `los`. Misma regla `l`→`i` de §12. Se
comprobó la palabra que precede a cada una: `de` 25, `en` 14, `que` 12, `a` 9, `para` 5,
`todos` 3, `con` 2, `y` 2, `por` 2, y el resto tras `cuando`, `durante`, `analizan`,
`septiembre,` o una comilla de apertura. En todas corresponde un artículo.

**`S` por `$`:** sólo 2 en todo el corpus (`S530`, `S610`), ambas montos en pesos.

**Sin regla posible:** el dígito suelto. «palabra + dígito + palabra» da **1.019** coincidencias
y son abrumadoramente legítimas («a 5 años», «en 1 punto», «de 5%»). Se corrigió a mano el único
caso real (`de 4 los ingresos`). Lo mismo con `-rla`: `mantenerla` 59, `dejarla` 30, `subirla` 26,
`llevarla` 25, `bajarla` 23 son todas formas válidas; sólo `llegarla` (1 contra 52 de `llegaría`)
es defecto.

### Dos reglas para componer `Antes`

1. **Se compone desde el texto virgen, no desde la salida.** El validador aplica las operaciones
   a la base, así que un fragmento que contenga algo ya corregido por otra operación no aparece.
   Pasó con un fragmento que llevaba `IPC`: en la base ese lugar dice `IRC`, y la operación
   `IRC`→`IPC` del nivel 1 lo reescribe antes.
2. **No basta con que los tramos no se solapen: hay que mirar si un `Antes` está contenido en
   otro.** `IRC`→`IPC` no tiene contexto, así que reescribe *todas* sus apariciones, incluidas
   las que caen dentro de mi fragmento. La comprobación correcta es de subcadena, no de posición.

Y cuando dos defectos caen en el mismo tramo, **se extiende la operación existente en vez de
crear otra**: en `1321:1` la operación `fiy`→`fly` empezaba justo en la `s` de `ios`, así que
las dos se pisaban en dos caracteres. Se amplió a `ios gráficos, el efecto fiy…` →
`los gráficos, el efecto fly…`.

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

---

## 14. Siglas con `I` leída como `l`, y los 21 residuos `■` (ronda 192)

Dos familias nuevas, medidas en toda la salida.

### La familia `I`→`l` en siglas

`IPCXI` 6, `dellPC` 5, `ellPoM` 5, `ÍPCX1` 2, `dellPoM` 2, `IPX1` 2, `IPCX 1` 1, `ellPP` 1, `ellPC` 7,
`ellPCX1` 1, `IPX` 3, `iPCX` 1, `deIIPCX` 2. Ninguna tiene forma correcta con `l`, y todas tienen su
equivalente ampliamente atestiguado: **`el IPC` 1.430, `el IPoM` 1.543, `IPCX` 649, `IPCX1` 469, `el IPP` 10**.
Todas se corrigieron. Resultado: **las 13 formas a 0**; `IPCX` 649→656 y `IPCX1` 469→480.

**Lo que se excluyó, deliberadamente.** `ellPEC`, `dellPEC` y `ellMCE` (fila `1719:4`) van juntas en la
misma oración —«la Encuesta de Expectativas que hace ellMCE y ellPEC»— y `PEC` y `MCE` no son siglas que
se puedan corroborar en el corpus. No hay reconstrucción única, así que **se dejan y se anotan**. Es la
misma regla de §5 bis al revés: cuando la forma dañada apunta a algo que no puedo verificar, no adivino.

**Dos trampas medidas.** (1) El **orden importa**: `deIIPCX` es prefijo de `deIIPCX1` y `IPX` es prefijo
de `IPX1`; si el patrón corto va primero, se come al largo y deja un `1` suelto. Hay que ir de más largo
a más corto. (2) **`IPCX` es legítimo**: aparece 180 veces suelto en contextos reales («el IPCX e IPCX1»,
«la inflación del IPCX y del IPCX1»), porque `IPCX` e `IPCX1` son dos medidas de inflación subyacente
distintas del Banco. Traté `IPCX` como defecto y casi destruyo 180 apariciones correctas. **Una sigla que
parece incompleta puede ser una segunda sigla real: hay que contar la forma suelta y leer sus contextos
antes de declararla dañada.**

### Los 21 residuos `■`

El tipo `SIMBOLO_SUELTO` existía justo para esto, y aun así quedaban 21 apariciones en 20 filas. La basura
adyacente varía (`■o J`, `■,\y`, `■'`, `■J`, `■V`, `/ ■ ' /`, `4 / ■`, `i - /■`, `— f ■`, `ry _<< ■`), así
que cada una se trató con su fragmento propio. **`■` pasó de 22 a 0.**

Dos casos pidieron criterio aparte:
- **`1352:1`**: el `■'` no es basura sino una **comilla de apertura**. Esa fila tiene `“`=0 y `”`=1, con la
  de cierre al final («…en 25 puntos base.»). Se repuso `Comunicado “En su reunión…`, el mismo patrón que
  se resolvió así en `6438:3`.
- **`5802:2`**: se eliminó **sólo** el `■` y se dejó el paréntesis abierto («…esta Sesión: («), porque la
  fila ya está marcada `RECONSTRUCCION_AMBIGUA_POR_COTEJAR` con motivo `FINAL_SIN_PUNTUACION`. Inventar el
  cierre habría tapado un final genuinamente incompleto.

También se quitó el `fi` que cerraba `1335:4` tras una oración completa («…que resultan mayores.»).

### Lo que enseñó esta ronda sobre el orden de aplicación

Tres defectos quedaron sin corregir en la primera vuelta porque caían a pocos caracteres de otro ya
corregido **en la misma fila** y las ventanas de `Antes` se pisaban. La solución no es forzar la
sustitución, es **componer un fragmento más estrecho o extender la operación existente**. En `3703:1` la
operación ya cubría `base en el caso del IPX e IPX1, respect` y había corregido `del IPX`→`del IPCX`; sólo
faltaba `IPX1`. **Cuando dos defectos caen dentro del mismo tramo, se extiende la operación, no se añade
otra** — la misma regla que resolvió `1321:1`.

En total: 49 operaciones en 31 filas.

---

## 15. Primera pasada transversal completa: palabras partidas (317 → 0)

Hasta aquí las pasadas salían de lo que iba apareciendo al leer. Esta es la primera
hecha sobre **las 9.723 filas de una vez**, y el motivo es una medición: de las filas
corregidas, **526 de 831 (63 %) caían en filas que todavía no se habían leído**. Lo que
encuentra los defectos es lo transversal, no la lectura secuencial.

**La regla.** Dos tokens vecinos separados por un solo espacio, cuya concatenación es una
palabra frecuente del corpus (>= 20 apariciones) y donde **ninguna de las dos mitades por
separado es una palabra corriente** (< 50). Si una mitad fuera común, el espacio sería
real. Medido: 317 pares en la base, 0 en la salida.

**Nombres propios.** Se corrigieron `Desorm eaux`→`Desormeaux` (444), `Zurbuc hen`→
`Zurbuchen` (100), `Claud io`→`Claudio` (1.350), `Am érica`→`América` (2.589),
`E lena`→`Elena` (32), `C onsejo`→`Consejo` (1.433). No es la resolución de alias que el
criterio prohíbe: la forma correcta está atestiguada y lo único que se elimina es un
espacio que el escaneo insertó **dentro** de la palabra. No se adivina ninguna grafía.

### Tres mediciones negativas que hay que registrar

1. **La rareza no discrimina.** Hay 5.917 hapax de largo >= 7 (5.435 en minúscula) y casi
   todos son palabras reales y raras (`abstuvo`, `ablandó`, `Abenomics`). Es el segundo
   generador automático que se mide y se descarta, después del pre-escáner (14/31, 45 %).
2. **El detector de acentos no es usable.** Encuentra 1.022 candidatos en 820 filas, pero
   la mayoría son pares mínimos legítimos del español que difieren sólo en acento
   (`terminó`/`término`, `cambió`/`cambio`, `dónde`/`donde`). Sin lexicón no hay forma
   barata de decidirlos. Reales entre ellos: `nomínales`, `anualízado`, `estimulo`,
   `Adicíonalmente`, `Adícionalmente` — quedan **pendientes**, no se aplican.
3. **`re.finditer` no solapa, y eso falsea cualquier detector de pares.** En «un crecim
   iento» empareja `un`+`crecim`, los consume, y la pareja real nunca se evalúa. Con el
   regex el detector llegó a reportar **«0 candidatos» cuando todavía quedaban 3 `crecim
   iento`, 5 `trim estre` y 3 `econom ías` en la salida**. Hay que recorrer posiciones de
   token. **Y el detector no es la prueba: la prueba es contar sobre el release.**

### Cuando dos defectos caen en el mismo tramo

Once casos no admitían operación nueva porque una ya registrada cubría el sitio. Dos
subcasos, y la diferencia importa:

* **Cobertura total** y la forma dañada ya no está en el `Despues` → ya resuelto, no tocar.
* **Cobertura parcial** — la operación corta a mitad de palabra (`…trim es`) → la división
  **sobrevive** aunque el fragmento no aparezca literal en el `Despues`. Hay que extender
  la operación: nuevo `Antes` = unión de tramos, nuevo `Despues` = trozo izquierdo +
  `Despues` viejo + trozo derecho, y sobre eso aplicar la unión.

Un tercer error, del mismo family: cuando una fila tiene **varias** apariciones del mismo
defecto y una operación previa ya resolvió la primera, `t.find()` mapea todas a esa y se
saltan las demás. Hay que enumerar todas las apariciones y quedarse con las vivas.

### Lo que esto cambió en el procedimiento

| | antes | ahora |
|---|---|---|
| filas corregidas | 831 | **921** |
| operaciones | 1.069 | **1.334** |
| auditoría | ninguna | `revision_operaciones.tsv` con las 1.334 |
| control del `Despues` | sólo «que algo cambie» | toda palabra introducida debe existir en el corpus |
| regresión | 3 tests mencionaban formas dañadas | 11 tests que fijan las basales |

Pendiente de esta sección: los candidatos de acento reales listados arriba, y los 5.917
hapax, que no son una lista de trabajo sino ruido hasta que haya lexicón.

---

## 16. Acentos: arbitrar los 1.094 candidatos del escáner

§15 dejó el detector de acentos como inutilizable «sin lexicón». El lexicón existe: es
conocimiento de ortografía española, y se aplicó caso por caso sobre los **190 pares
distintos (1.094 apariciones)** que produce el escáner. El rendimiento real:

| clase | apariciones | tratamiento |
|---|---:|---|
| acento espurio: con esa tilde la palabra no existe | **155** | corregido |
| falta la tilde y decide la oración | ~150 | pendiente, exige contexto |
| par mínimo legítimo del español | ~790 | **no se toca** |
| nombre propio con acento divergente | 51 filas | marcado, no corregido |

**Corregido (155 → 0).** `índica`→`indica` 42, `financíamiento`/`financiamíento`/
`fínanciamiento`→`financiamiento` 13, `nomínales` 6, `íncertidumbre`/`incertídumbre` 8,
`índexación`/`Índexación`/`indexacíón`→`indexación` 11, `Macroeconómíco`/`macroeconómíca` 6,
`maquinaría(s)` 3, `mayorítaria(mente)` 4, `desestacíonalizado(s)` 2, `desapalancamíento` 2,
`vísta` 3, `margínales`/`margínalmente` 4, `potencíales` 3, `salaríales` 2, `contrarío` 4,
`recesíón` 2, y 26 formas de una aparición (`medíante`, `claúsulas`, `trímestre`,
`comportamíento`, `dícha`, `tambíén`, `coíncídente`, `sosteníble`, `cambíario`,
`expansivídad`/`expansívidad`, `atríbuible`, `ínicialmente`, `monítoreo`, `perecíbles`,
`anualízado(s)`, `materialíce`, `comparacíón`, `noticías`, `tendencías`, `Bancaríos`,
`Adícionalmente`, `Adicíonalmente`).

**Lo que no se toca, y por qué.** `éstos`/`Éstos`/`Éstas`/`Aquéllas` (144): la tilde
diacrítica en demostrativos dejó de ser obligatoria en 2010, no es un error. `período`/
`periodo` (786/76): **ambas son válidas** según la RAE. `cuánto`, `dónde`, `cuándo`,
`quién`, `quiénes`: acentos interrogativos legítimos. Todos los pretéritos —`terminó`,
`cambió`, `inició`, `incrementó`, `previó`, `marcó`, `argumentó`, `motivó`, `trabajó`,
`promedió`, `retornó`, `impulsó`, `impactó`, `traspasó`, `retiró`, `desarrolló`, `estudió`,
`frenó`, `precisó`, `centró`, `contagió`, `completó`, `sesgó`, `gastó`, `costó`,
`deterioró`, `tornó`, `cursó`, `restó`, `sustentó`, `rebalanceó`— son formas verbales
correctas. Y cuatro que **sí existen como verbo o adjetivo** y por eso se excluyeron del
lote aun pareciendo dañadas: `solícita` (adjetivo), `varías`, `contraría`,
`complementarías` (verbos). `POLITICA`/`SESION`/`POLiTICA` (30) están en el encabezado en
mayúsculas del acta, donde la ausencia de tilde es aceptable.

**Nombres propios: marcados, no corregidos.** `Oscar`/`Óscar` 10, `America`/`América` 10,
`Angel`/`Ángel` 11, `Gíanelli`/`Gianellí`/`Gianelli` 7, `Marfan`/`Marfán` 2,
`Garcia`/`García` 2, `Larrain`/`Larraín` 2, `Beltran`/`Beltrán` 2, `Beresí`, `Váldés`,
`Sebastian`, `Arabía`, `Bascuñan`: **51 filas** con `NOMBRE_PROPIO_POR_COTEJAR`. La tilde
divergente en un nombre es un cambio de grafía, y el criterio prohíbe adivinar grafías de
nombres propios. Es distinto de §15, donde se eliminaba un espacio insertado *dentro* de
la palabra sin tocar ninguna letra. Las marcas subieron de 135 a **184**.

**Tres errores propios que corrigió la medición.** (1) El primer recuento de «sigue viva»
se hacía por fila y no por ocurrencia. (2) Un dedupe por forma suprimía las repeticiones
legítimas dentro de una misma fila: esas filas tienen de 2 a 4 apariciones y sólo se
corregía la primera — se detectó porque la salida daba 6 cuando el detector ya decía 0.
(3) `maquinaría` es substring de `maquinarías`, así que buscar la singular encontraba la
plural ya resuelta.

Estado: **1.025 filas corregidas, 1.476 operaciones, 184 marcadas, `Texto` intacto en las
9.723**. Queda pendiente el grupo de ~150 donde la tilde la decide la oración: no se
resuelve por frecuencia ni por escáner, hay que leer cada contexto.

### §16 segunda parte: los grupos A y B

El grupo de ~150 donde «decide la oración» se resolvió leyéndolo, y se dividió en tres.

**Grupo A — 68 → 0.** Sin la tilde la forma no existe en español en ninguna acepción, así
que no hay ambigüedad: `podria`/`podrian`/`serian`/`estaria`/`deberia`/`cabria`/
`aumentaria` (condicionales), `economia`, `indices`, `mayoria`, `paises`, `ciclicas`,
`geopoliticos`, `exposicion`, `todavia`, `habia`, `tenian`.

**Grupo B — se leyeron las 110 apariciones y sólo 61 eran defecto.**

| forma | leídas | defecto | legítimas, y por qué |
|---|---:|---:|---|
| `seria` | 40 | 33 | 7 son el adjetivo: «una seria amenaza», «no sólo es seria», «le parece muy seria», «gente extremadamente seria», «una cuantificación seria», «están en seria duda», «una seria advertencia» |
| `estimulo` | 18 | 18 | ninguna: todas son el sustantivo |
| `linea` | 19 | 19 | ninguna: todas son «en linea con» |
| `lineas` | 6 | 6 | ninguna |
| `continua` | 19 | **2** | 16 son el adjetivo: «la continua caída», «de manera continua», «la serie no es continua» |
| `publica` | 13 | **0** | 13 son el verbo: «el INE no los publica», «que publica el Fondo» |
| `tenia`, `limite`, `ultimo`, `titulo`, `diagnostico`, `domestica`, `llego`, `explicito`, `indice` | — | 29 | 2 subjuntivos de limitar («que limite las presiones») y 1 participio («década perdida») |

**El detector de acentos acertaba en un 55 % de lo que proponía.** `publica` era 100 %
falso positivo y `continua` un 89 %. Eso es lo que cuesta no leer: sin el paso humano,
esas 49 operaciones habrían entrado y habrían dañado texto correcto.

### Un error propio que la frontera de palabra destapó

El par `ultimo` → `último` emparejaba **por substring** y entró dentro de
`multimodal`, convirtiéndolo en `múltimodal` (el prefijo *multi-* no se acentúa). Fueron
4 operaciones en 3 filas, retiradas del registro; `multimodal` vuelve a dar 4 en la
salida, igual que en la base. La causa se corrigió en `scripts/aplicar_pares_ocr.py`:
ahora exige frontera de palabra en el builder y en el extensor.

Esa misma frontera destapó inmediatamente un segundo error, mío y no de la herramienta:
un par escrito como `economía continua funcionan`, truncado de `funcionando`, fue
rechazado porque la `d` final rompía la frontera. **El control nuevo funcionó: convirtió
un defecto que habría entrado en silencio en un rechazo visible.**

Estado tras §16 completo: **1.130 filas corregidas, 1.642 operaciones, 184 marcadas,
`Texto` intacto en las 9.723.**

## 17. El primer cotejo ejecutado contra el PDF original

Hasta aquí la columna `Cotejar_PDF` era una lista de preguntas sin respuesta posible: el
repositorio tiene 2 actas en PDF y las 184 marcas se reparten en 146 sesiones. **Yo venía
repitiendo que ninguna de las 184 caía en esas dos sesiones. Era falso.** Medido contra el
release, 4 filas sí caen: `2005-06-09:279:1`, `2005-06-09:280:6`, `2005-07-12:296:1` y
`2005-07-12:305:6`. El error venía de arrastrar un número de cuando el registro era más
chico, sin volver a medirlo.

### El método

Extracción con `pypdf` (20 páginas y 72.171 caracteres; 25 y 81.300), normalización de
espacios, y alineación de la fila contra el documento: se busca en el PDF una ancla tomada
de la propia fila y se recorta una ventana del mismo largo, para que el `difflib` no
compare contra el acta entera. Recortar la ventana importa: sin recorte, los segmentos
`delete` que devuelve son el desborde de la ventana, no defectos, y se confunden con
hallazgos.

| fila | ratio | diferencias internas |
|---|---|---|
| `2005-06-09:279:1` | 1,00000 | 0 |
| `2005-06-09:280:6` | 1,00000 | 0 |
| `2005-07-12:305:6` | 1,00000 | 0 |
| `2005-07-12:296:1` | 0,99862 | 1 defecto + 2 normalizaciones |

### El veredicto sobre el nombre

Las cuatro filas estaban marcadas por lo mismo: el corpus dice «Luis **Oscar** Herrera» y
la forma mayoritaria del corpus es «Óscar». El documento de referencia escribe
**«Luis Oscar Herrera» sin tilde**, dos veces en cada acta, y **«Óscar» aparece 0 veces**
en los dos PDFs. El corpus era fiel; la divergencia con la forma mayoritaria no era
evidencia de nada.

**Regla que queda: que el corpus discrepe de su propia forma mayoritaria no es prueba de
defecto. La única prueba es la fuente.** Las 4 marcas se cierran como
`NO_REQUIERE_COTEJO` con el veredicto en el `Motivo`; el texto no se toca. La entrada se
conserva en `Revisiones_Sin_Correccion`: cerrar una marca es registrar una respuesta, no
borrar una pregunta.

### Lo que la alineación destapó de rebote

La fila `2005-07-12:296:1` no daba ratio 1, y la causa no era el nombre: el PDF dice
«celebrada **el12** de julio de 2005» y el corpus «celebrada **e l1 2** de julio». El §15
no podía verlo porque trabaja sobre pares de **letras**; aquí hay dígitos de por medio. Un
detector con un alcance declarado sigue siendo ciego fuera de ese alcance, y el silencio no
se nota.

Y el PDF permitió decidir algo que de otro modo habría sido una conjetura: el acta de
**2005-06-09**, de la misma serie y con el mismo encabezado formulaico, escribe
«Celebrada **el 9** de junio de 2005» **con** espacio. Dos actas iguales, una con espacio y
otra sin él: el espacio faltante es un artefacto de la capa de texto, no una variante del
acta. Eso autoriza reponerlo.

### La familia de defectos con dígitos

Escaneada la salida efectiva con cuatro patrones (`letra suelta + dígito`, `el` pegado a
dígito, dígito-espacio-dígito, letra pegada a dígito):

| clase | n | tratamiento |
|---|---:|---|
| espacio faltante en el encabezado (`el10`, `el12`, `el15`, `el16`) | 5 | corregido, con la evidencia de 2005-06-09 |
| `e l1 2` → `el 12` | 1 | corregido, cotejado contra el PDF |
| `a100%` → `a 100%` | 1 | corregido; precedente registrado (`un13%` → `un 13%`) |
| `%%` → `%` | 6 en 5 filas | corregido; las 6 leídas, ninguna admite lectura válida |
| coma decimal convertida en espacio (`6 4%`, `0 6%`, `-8 3%`) | 8 | **marcadas**, no adivinadas |
| `5 1/4`, `i4>` | 2 | **marcadas** |

Las marcadas llevan `CIFRA_INCONSISTENTE_POR_COTEJAR`, salvo `i4>` que es
`RECONSTRUCCION_AMBIGUA_POR_COTEJAR`. El patrón de fondo es que el OCR volvió espacio la
coma decimal: «6 4%» es casi seguro «6,4%» porque la cifra paralela es «4,5%», pero *casi
seguro* no alcanza, y adivinarlo sería editar el discurso. Quedan para cuando estén los
PDFs de esas sesiones.

### El invariante que estaba mal formulado

`MIN_MARCADAS` era un piso sobre las marcas abiertas, con el comentario «nunca deben
bajar». **Cerrar un cotejo las baja, y ése es el resultado correcto.** El piso premiaba
dejar preguntas abiertas. Se reemplazó por dos: el total de casos adjudicados
(abiertos + cerrados, 187) y los cierres documentados (34), que ésos sí sólo pueden crecer.

Herramienta nueva: `scripts/cerrar_marcas_cotejadas.py`. `agregar_correcciones_ocr.py
--parche` añade y extiende correcciones y añade revisiones, pero no actualizaba la `Marca`
de una revisión ya registrada; sin esto el único camino era editar el registro a mano.
Valida vocabulario, motivo no vacío, ambigüedad por fragmento, y sin `--aplicar` sólo informa.

Estado tras §17: **1.140 filas corregidas, 1.654 operaciones, 189 filas en `Cotejar_PDF`,
`Texto` intacto en las 9.723.**

Las 189 no son lo mismo que las 187 revisiones del registro, y vale la pena dejar la
cuenta escrita porque a primera vista no cuadra: hay **153 revisiones abiertas que
corresponden a 133 filas distintas** (una fila puede cargar varias), más **7** marcas
adicionales y **51** filas cuya base ya traía `TEXTO_DANADO_POR_COTEJAR`; la unión de los
tres conjuntos da exactamente las 189 del release, verificadas como conjuntos idénticos y
no sólo como cardinal. Los **34** cierres `NO_REQUIERE_COTEJO` no entran en esa cuenta:
están excluidos de la columna a propósito.

Dos cosas que salieron de hacer esa cuenta. Una entrada del registro tiene por
`ID_Intervencion` dos filas separadas por `/`, y `construir()` las expande y marca ambas:
es una función, no un defecto, pero `cerrar_marcas_cotejadas.py` la heredaba como punto
ciego y ahora la detecta y se niega, porque cerrar una de esas entradas cerraría la otra
fila sin que nadie lo haya pedido.

Quedan 189 filas marcadas que necesitan los PDFs de sus sesiones.

## 18. Espacio antes del signo: la familia que estaba fuera del alcance

§17 dejó una regla: un detector con un alcance declarado sigue ciego fuera de él, y el
silencio no se nota. El §15 trabajaba sobre pares de letras y no vio los dígitos. La misma
pregunta aplicada a la puntuación destapó la familia más grande de todas.

### El barrido

| patrón | ocurrencias | filas |
|---|---:|---:|
| espacio antes de `,` | 344 | 218 |
| espacio antes de `.` | 150 | 124 |
| espacio antes de `;` | 21 | 19 |
| espacio antes de `%` | 31 | 27 |
| paréntesis sin par | 80 | 45 |
| sin espacio tras `.` | 45 | 36 |
| sin espacio tras `,` | 35 | 29 |
| punto duplicado `..` | 3 | 3 |
| `,,` / `;;` / `::` / `%%` | **0** | 0 |

Dos de esas líneas son trampa, y **sin espacio tras `.` lo es en las dos direcciones**. La
mayoría es legítima: domina `EE.UU.`, y también `S.E.`, `v.gr.` y `2005.IV` (la notación del
trimestre). Pero entre las 45 hay casos reales de espacio faltante —`mercados.En segundo
término`, `asiática.Hace presente`, `variación.Estas cifras`— y basura de OCR (`e.n Ií ~ea`,
`.LI I`). Un reemplazo global habría roto todas las abreviaturas del corpus; hay que leerlas
una por una. Queda pendiente. Y el punto duplicado son sólo 3 casos, otra familia.

### La evidencia, antes de tocar nada

El barrido no dice si el espacio viene del original o del OCR. Los dos PDFs del repositorio
sí lo dicen:

| patrón | PDF 2005-06-09 | PDF 2005-07-12 | filas del corpus de esas sesiones |
|---|---:|---:|---:|
| letra + `,` | 0 | 0 | 0 |
| letra + `.` | 0 | 0 | 0 |
| letra + `;` | 1 | 0 | 0 |
| `—` + `,` / `—` + `.` | 0 | 0 | 0 |
| dígito + `,` | 0 | 0 | 0 |
| dígito + `.` | 0 | 2 | 2 |
| espacio antes de `%` | 0 | 0 | 0 |

Los documentos no traen el espacio, y las 90 filas del corpus de esas dos sesiones
coinciden con su PDF casi exactamente. La familia no es una característica del acta.

### El pase

Herramienta nueva: `scripts/aplicar_espacios_puntuacion.py`. **546 ocurrencias en la base
→ 19 en la salida**, 510 operaciones `ESPACIO_INDEBIDO`, y `Texto` intacto en las 9.723.

Dos decisiones de diseño que importan:

- **Fusionar, no apilar.** Con ~510 ocurrencias en ~320 filas, muchas caen a pocos
  caracteres de distancia y una ventana de contexto fija las haría chocar entre sí y con
  operaciones ya registradas. La herramienta agrupa las cercanas en una sola operación.
- **El control de solape va sobre la ventana que se escribe.** La primera versión comparaba
  el tramo núcleo `(ini, fin)` pero escribía la ventana ensanchada `(x, y)`, y
  `revisar_parche` rechazó el lote con 7 choques. La red de seguridad funcionó: el lote no
  se escribió. El control se movió a la ventana real.

Verificación independiente sobre el release leído desde disco: de las 510 operaciones,
**0 alteran algo que no sea un espacio** (misma secuencia de caracteres no-blancos antes y
después), y **ningún blanco de los 517 era un salto de línea**, así que la operación es
homogénea y no puede unir dos palabras.

### Lo que quedó, y por qué

- **19 ocurrencias en 19 filas.** Caen dentro de la ventana de una operación ya registrada;
  resolverlas exige **extender** esa operación, no apilarle otra encima (§15). El conjunto
  está fijado en el test: resolver una obliga a bajar el techo, y que aparezca una nueva se
  ve enseguida.
- **`RPM-2006-04-13:653:1`** excluida a propósito: dice «e v ia m e n te ,», que es una
  palabra letra a letra (§11) además del espacio. Arreglar sólo la coma dejaría la fila
  medio corregida.
- **Punto duplicado (3), residuos `/ .` (7), paréntesis sin par (80):** familias distintas,
  no tocadas.

Un bug propio que apareció al escribir los tests: el filtro de signo duplicado miraba sólo
el carácter anterior, así que dejaba pasar `uno ,, dos`. Ahora mira los dos lados. No
cambió ninguna cifra del pase —el corpus no tiene signos duplicados— pero el filtro era
incorrecto y el test lo encontró.

Estado tras §18: **1.345 filas corregidas, 2.160 operaciones, 189 marcadas, `Texto` intacto
en las 9.723**, sha base `d0b64842…` sin cambio.

## 19. Punto pegado a letra: la familia que se arbitra leyendo, no con reglas

§18 la dejó señalada como trampa en las dos direcciones. Son 45 ocurrencias y se clasifican
por lo que precede al punto:

| lo que precede | n | veredicto |
|---|---:|---|
| `EE.` | 27 | `EE.UU.`, legítimo |
| ` S.` | 5 | `S.E.`, `S.A.`, legítimo |
| `05.` | 2 | `2005.IV`, la notación del trimestre |
| `(v.` | 1 | `v.gr.`, legítimo |
| ` U.` | 1 | `U.F.`, legítimo |
| **por leer** | **9** | se leyeron una por una |

36 legítimas, 9 por leer. Un reemplazo global habría roto las 36; ésa era la trampa.

### Las 9, una por una

**Corregidas (5):**

- `mercados.En segundo término` → espacio tras el punto. Lo confirma la mayúscula y la
  estructura paralela: el mismo párrafo abre con «En primer lugar».
- `asiática.Hace presente` y `variación.Estas cifras` → igual, mayúscula tras el punto.
- `internacionalestará` → `internacional estará`, aparecida en la misma fila que la primera.
- `crecimiento q.ue de acuerdo` → punto insertado dentro de la palabra.

**Marcadas (4):** `e.n Ií ~ea con` (probablemente «en línea con», pero son tres glifos y dos
saltos de línea a la vez), `todos lados. .LI I`, `3,7%. k ^l.y`, y `Financiera, ...don Luis
Opazo Roco` —en una lista de asistencia donde todas las entradas siguen «Cargo, don Nombre
Apellido;». Los puntos suspensivos son un cuerpo extraño, pero borrarlos supone saber que no
sustituían nada.

### El caso que cambia de sentido al leerlo

`RPM-2014-06-12:6282:1` aparecía como una falta de espacio más: «se producirán.las caídas».
El reflejo era reponer el espacio. **La oración no termina ahí**: sigue «las caídas de las
tasas de interés en el mercado de préstamos a que se hizo mención, así como la compresión de
spreads a plazos más largos», que es continuación, y «las» va en minúscula. El punto es
**espurio**. Reponer el espacio habría convertido un signo que sobraba en un punto y aparte
que no existe: un defecto de OCR reemplazado por un error de edición.

Y había un segundo pliegue. En la base el tramo es «producirán ** .**las», con espacio *y*
punto. El §18 quitó el espacio, que era lo que su regla veía, y dejó el punto al
descubierto. Dos defectos en el mismo tramo: la regla de §15 dice extender la operación, no
apilarle otra, porque dos tramos solapados sobre el mismo texto virgen no se pueden aplicar
en ningún orden.

### La herramienta que faltaba

Esa regla no tenía herramienta. `agregar_correcciones_ocr.py --parche` actualiza el
`Despues` cuando el `Antes` coincide, pero no puede cambiar el `Tipo`, y aquí cambia: quitar
un espacio indebido y descubrir después que el signo también sobraba ya no es
`ESPACIO_INDEBIDO`. Dejarla con ese tipo habría roto el invariante de §18 que exige que
esas operaciones no alteren nada que no sea un espacio.

`scripts/enmendar_operacion.py` (6 tests) enmienda `Tipo`, `Despues` y `Justificacion` de
una operación identificada por `(ID_Intervencion, Antes)`, sin tocar el `Antes` —que es lo
que la ancla al texto virgen— y sin crear una operación nueva.

### Dos errores propios que sólo la aserción vio

Dos de los fragmentos que iba a usar como `Antes` los había copiado de la **salida**, no del
texto virgen, y no existían en la base. La aserción `t.count(pat) == 1` los rechazó antes de
escribir nada; es la tercera vez que esa red salva el registro.

El segundo es más desagradable: al imprimir el contexto para leerlo había hecho
`.replace('\n', ' ')`, así que el tramo se veía como «creciendo e.n Ií ~ea con» cuando en la
base es `'creciendo\ne.n\nIí ~ea con'`. **El mismo formateo que hace legible un contexto
oculta los saltos de línea, y los saltos de línea son parte del defecto.** Para componer un
`Antes` hay que mirar el `repr`, no la impresión.

Estado tras §19: **1.346 filas corregidas, 2.165 operaciones, 193 marcadas (157 abiertas + 34
cierres), `Texto` intacto en las 9.723**, sha base `d0b64842…` sin cambio. La familia punto
pegado a letra queda en 40, todas abreviatura legítima o fila marcada, y el test exige que
cualquier punto pegado nuevo sea una de las dos cosas.

## 20. Cerrar el residuo del §18, y dos bugs que aparecieron al intentarlo

§18 dejó 19 ocurrencias con la promesa de que resolverlas exigía extender operaciones. Con
`enmendar_operacion.py` ya escrito, se pudo intentar. El residuo bajó de **19 a 4**, y la
familia completa de **551 a 4**. Aparecieron dos bugs, los dos míos, y los dos los encontró
una red que ya estaba puesta.

### Bug 1: `finditer` otra vez, en la herramienta nueva

`ocurrencias()` usaba grupos capturados, `(\S)(\s+)([,.;%])`. El signo queda **consumido** por
el match, y `re.finditer` no lo vuelve a ofrecer como carácter anterior del siguiente. En
«alcanza a 2 ,5 % . En cuanto» el detector veía `' ,'` y `' %'` y **se perdía el `' .'`**: el
`%` ya estaba gastado.

Es literalmente la lección de §15 —«nunca construyas un detector de candidatos con un regex
de varios grupos»— reaparecida en una herramienta escrita después de haberla documentado.
Saber la lección no inmuniza contra ella; lo que inmuniza es el test. Se corrigió con
lookahead y lookbehind, `(?<=\S)\s+(?=[,.;%])`, que no consume los bordes, y quedó un test
que fija las tres ocurrencias de esa cadena. La base pasó de 546 a **551** ocurrencias: el
detector viejo no las veía.

### Bug 2: `replace` quita el primer espacio, no el que uno quiere

Para las ocurrencias que caían dentro de una operación de otro tipo (palabra partida, tilde)
la enmienda consiste en quitar ese espacio del `Despues`. La primera versión localizaba un
contexto único y hacía `contexto.replace(' ', '', 1)`. En
`'ta financiera en el prim er mes del año— , '` el contexto era `'mes del año— , '` y el
primer espacio es el de **«mes del»**: el resultado fue `'mesdel'`.

Tres operaciones salieron así: `mesdel`, `preciodel`, `yelBrent`. **Ninguna llegó al
release**: `revisar_reemplazos()` las rechazó porque el reemplazo introducía una palabra que
no está en el corpus. La validación dio `FALLO` y el registro se restauró desde HEAD. El
arreglo es quitar el espacio **por posición** dentro del contexto, no por `replace`.

La moraleja no es «tuve cuidado», es al revés: no lo tuve, y lo que salvó el gold standard
fue un control escrito varios lotes antes para otro propósito. **Los controles que se
escriben pensando en un riesgo terminan cubriendo otros.**

### El residuo de 4

- `RPM-2006-04-13:653:1`: «p re v ia m e n te ,» es una palabra letra a letra (§11). Arreglar
  sólo la coma dejaría la fila medio corregida.
- `RPM-2015-08-13:6952:1`: cae en un tramo de basura (`servicios. , . . , Anaí ? ! £ , Ias
  medldas`) que necesita cotejo, no un arreglo de espacio.
- `RPM-2009-02-12:2319:1` y `RPM-2010-12-16:3619:1`: la ocurrencia está libre, pero **toda
  ventana lo bastante larga para ser única alcanza a una operación vecina**, y las dos
  restricciones chocan. Resolverlas exige modificar el `Antes` de la vecina, que es justo lo
  que la ancla al texto virgen.

También hizo falta bajar los márgenes de búsqueda de ventana: con las operaciones del §18 ya
puestas, el texto quedó denso y el margen mínimo de 10 caracteres chocaba casi siempre. Se
prueban 0, 2, 4, 7 y luego los de antes; eso solo resolvió 6, pero sin eso no se resolvía
ninguna.

## 21. La barra: una letra que la OCR escribe como «/»

Iba a cerrar los residuos `/ .`. Las notas del lote decían «7 casos en `RPM-2005-07-12:265:1`».
Medido: **36 en la base, 30 vivos en la salida, repartidos entre 2007 y 2015, y ninguno en esa
sesión**. Es el tercer número rancio que una nota arrastraba; los otros dos fueron «0 de 184» y
el «63 %». Una nota de progreso no es una medición.

Al clasificar las barras por lo que tienen a cada lado apareció otra cosa mucho más grande: la
OCR escribe **`v`, `l` e `I` como `/`**.

| forma dañada | n | correcta |
|---|---:|---|
| `obsen/ado`, `obsen/ada`, `obsen/ando`, `obsen/an`, `obsen/a`, `obsen/ó` | 10 | `observar` |
| `Resen/a`, `resen/as` | 4 | `Reserva` |
| `cun/a` | 2 | `curva` |
| `inten/ención` | 1 | `intervención` |
| `sw/aps` | 1 | `swaps` |
| `Financia/` | 2 | `Financial` |
| `se/ection` | 2 | `selection` |
| `Defau/t` | 1 | `Default` |
| `el /PoM`, `el /poM`, `el/PoM`, `del/PoM` | 6 | `IPoM` |

28 correcciones donde **una sola sustitución produce una palabra del corpus**, más 2 `el/PoM` y
`del/PoM` donde además se había perdido el espacio. La familia quedó en **0**.

### Lo que había que NO tocar

Junto al defecto conviven usos legítimos de la barra, y son mayoritarios: `y/o` 38,
`trimestre/trimestre` 27, `peso/dólar` 20, `yuan/dólar` 4, `t/t` 3, `a/a` 3, `sube/baja`,
`público/privado`, `WTI/Brent`, `AAA/Aaa`, `US$/libra`, `+/-`, `2008/2009`, `v/s`. Un reemplazo
global de la barra habría destruido todo eso. El test nuevo fija las dos puntas: cero formas
dañadas **y** los usos legítimos sin cambio.

### Dos rechazos del validador, con veredictos distintos

`revisar_reemplazos()` rechazó `Interest` y `selection` por foráneos. Se resolvieron distinto:

- **`selection` se añadió a `TERMINOS_FORANEOS`.** El corpus trae la forma dañada `se/ection
  bias` dos veces y nunca la correcta, así que el vocabulario no la tiene; la barra sustituye a
  la `l`, igual que en `Defau/t` → `Default`.
- **`Interest` NO se añadió.** Aparece **0 veces** en el corpus virgen, así que no hay forma
  interna de confirmar la grafía; además la misma palabra tiene un segundo defecto (`Poliey`) y
  el término completo es ambiguo (`Zero Interest Rate Policy` lleva un `Rate` que no está). Se
  marcó `RECONSTRUCCION_AMBIGUA_POR_COTEJAR` en vez de corregir.

La regla que separa los dos casos: **un término foráneo se acepta cuando el corpus contiene la
forma dañada y la sustitución es la misma que ya está probada en otra parte. No se acepta
cuando la única evidencia es que uno sabe cómo se escribe.**

### Dos vocabularios que confundí

Inventé `LETRA_ERRONEA` cuando el tipo correcto era `LETRA_CONFUNDIDA`, y marqué con
`TEXTO_DANADO_POR_COTEJAR`, que es un valor de `Motivos_Revision` y no del vocabulario de
`Cotejar_PDF`. Los dos los rechazó la validación antes de escribir. Hay **15 tipos** y **7
marcas**, cerrados; cuando uno no encaja, la respuesta es releer la lista, no agrandarla.

### El test nuevo encontró algo, y el equivocado era el test

Al primer intento falló: `«y/o» cambió: 39 -> 38`. Investigué antes de aflojarlo: el `y/o` que
faltaba estaba **dentro de `7ay/or`**, que es «Taylor» dañado (regla de Taylor) y se había
corregido antes. La baja es correcta; lo que estaba mal era mi expectativa. Ahora el test la
declara explícitamente como caída permitida, con la razón.

## 22. La «M» que la OCR escribe como `í\/l`

El escaneo del §21 mostró de rebote una secuencia con barra invertida (`í\/lanuel`,
`í\/1onetaria`) y no se siguió. Medida aparte: el corpus tiene **48 barras invertidas**, de las
cuales **15** forman la secuencia `\/` dentro de una palabra, en 11 formas distintas. Las otras 33
están sueltas y son otra familia, más sucia.

El patrón es una sola letra: **la `M` se vuelve `í\/l`, `l\/l`, `i\/l`, `Í\/1` o `Í\/I`**.

| dañada | n | correcta | veces en el corpus |
|---|---:|---|---:|
| `l\/lonetaria`, `í\/lonetaria`, `í\/1onetaria` | 5 | `Monetaria` | 3.248 |
| `TPÍ\/I` | 2 | `TPM` | 1.822 |
| `í\/larshall` | 2 | `Marshall` | 1.243 |
| `í\/lanuel` | 1 | `Manuel` | 1.184 |
| `i\/linistro`, `í\/línistro` | 2 | `Ministro` | 1.419 |
| `RPÍ\/1` | 1 | `RPM` | 591 |
| `í\/lacroeconómico` | 1 | `Macroeconómico` | 996 |
| **`lí\/IACEC`** | **1** | **¿?** | **`IACEC`: 1** |

14 corregidas. **`lí\/IACEC` se marcó**: «IACEC» aparece **una sola vez en todo el corpus, que es
esta misma ocurrencia**, y las candidatas son `IPCX1` (458) o `IPCSAE` (55). Dos lecturas
plausibles y sin PDF de la sesión → se marca, no se elige. La secuencia quedó en **1**, que es la
marcada, y el test exige exactamente eso.

### Nombres propios

`Marshall` y `Manuel` se corrigieron, y conviene decir por qué no choca con la regla de no
resolver alias de nombres. Esa regla prohíbe **elegir entre grafías alternativas** de una persona
(Bermúdez/Vintimilla, Ricaurte, «Claudia Raddatz»). Aquí no hay elección: `í\/larshall` no es una
grafía de nada, es un glifo dañado, y el destino es la forma que el propio corpus usa 1.243 veces.
Restaurar la forma mayoritaria del corpus no es resolver un alias.

### Un delta que no cuadraba, y por qué había que perseguirlo

Al verificar, `Ministro` pasó de 1.419 a 1.420: **+1, cuando mis dos correcciones daban +2**. Se
podía haber dicho «más o menos cuadra» y seguir. Se persiguió: la fila `RPM-2005-01-11:57:1` bajó
de 2 a 1 porque uno de los dos estaba dentro del bloque de firmas escaneadas que una decisión
anterior elimina como `FIRMA_TRUNCADA` (52 filas). El −1 es legítimo y documentado; el neto +1 es
correcto.

La regla operativa: **cuando un conteo no cuadra con lo que uno hizo, la diferencia es
información.** Casi siempre es una corrección anterior interactuando, y a veces es un daño.

Recuperación: el workspace se reseteó otra vez al inicio del turno (HEAD en el commit base, remoto
en `3ec89c9`). Se verificaron los 100 archivos contra el remoto —todos idénticos— antes de
restaurar, y el venv se recreó. Registro y release intactos, sha base sin cambio.

## 23. Leer una sesión encontró lo que siete pases transversales no vieron

Después de siete pases transversales seguidos se leyó una sesión, como pide el criterio. En la
fila `RPM-2007-07-12:1340:1` aparecieron palabras partidas a simple vista: `m aterializarse`,
`m antención`, `m ayores`, `M onetaria`, `m ediano`, `m ás`. El §15 había declarado esa familia
en cero.

El detector del proyecto, re-ejecutado, dijo **0 candidatos**. Tenía un punto ciego.

### La guarda que bloqueaba justo el caso más común

`detector_partida` exige que la palabra junta sea frecuente **y que ninguna de las dos mitades lo
sea**, para no juntar `de la`. Medido sobre la salida: el token `m` aparece **78 veces** y `a`
**37.528**. La regla `freq.get(a) >= 50` bloqueaba entonces **todo** `m ayor`, `m onetaria`,
`m eses`.

Y el razonamiento está al revés: una letra suelta es frecuente **precisamente porque la OCR parte
palabras**. La guarda tiene sentido para mitades que son palabras, no para letras. En español las
únicas letras que son palabra son `a`, `y`, `o`, `e`, `u` (y `A`); fuera de ésas, un token de una
letra es residuo.

Se añadió `LETRAS_PALABRA` y la excepción al detector. Con la guarda relajada sólo para letras
sueltas: **62 candidatas en 39 filas**, y las 62 inequívocas —todas `m`/`M` más una continuación
que forma una palabra de alta frecuencia (`mayor` 4.467, `monetaria` 4.277, `meses` 4.246,
`mercado` 4.420, `más` 11.942). Al generar el lote desde el texto virgen aparecieron además **328
ocurrencias ya cubiertas por una operación**: el §15 sí había corregido 328, y éstas 62 eran
exactamente las que la guarda escondía.

Más una que ningún detector de pares puede ver: `m ayoritariam ente`, **dos espacios dentro de la
misma palabra**. Juntar `m`+`ayoritariam` no da una palabra, así que el par no califica.
`mayoritariamente` aparece 126 veces y el fragmento `ayoritariam` aparece una sola vez, que es ésa.

### Por qué el punto ciego sobrevivió

`detector_partida` tenía la lección de `finditer` escrita en su docstring, con números y todo, y
**no tenía un solo test**. Una lección documentada no se ejecuta; un test sí. Se añadieron 5 que
fijan el caso roto (`m ayor` con `m` frecuente), el caso que la guarda debe seguir protegiendo
(`a yor`, `de la`) y el umbral de frecuencia.

Dos cosas más que dejó la lectura. Mi propio conteo con substring dio `se r` = 4 en una fila: falso
positivo, coincide dentro de «se recomienda» —el mismo error de substring que ya estaba
documentado. Y la comparación base/salida es obligatoria: el lector de rondas muestra el texto
virgen, así que leerlo sin comparar lleva a "descubrir" defectos ya corregidos.

La sesión `2007-07-12` quedó con las rondas 191-196 pendientes; se anota para no saltearlas.

## 24. Qué se mira para decidir que una fila tiene una sola voz

La sesión `2007-07-12` se cerró con las rondas 193-196 (16 filas). Todas de una sola voz. Como el
veredicto es negativo, conviene dejar escrito **qué se miró**, porque «no encontré nada» sin
método no se distingue de «no miré».

Para cada fila:

1. **Cómo termina.** En estas actas cada intervención cierra con la conclusión de su propio
   hablante —su voto («su voto es por subir la Tasa… en 25 puntos base») o su síntesis («En suma,
   el Consejero señor X indica que…»). Una fila con dos voces suele terminar en medio de una idea
   o con la voz equivocada.
2. **Nombres de otros consejeros.** Se cuentan. Que aparezcan no prueba nada: hay que leer cada
   aparición.
3. **Verbos de turno**: pregunta, responde, replica, interviene, consulta, toma la palabra.

Los tres casos que hubo que leer antes de firmar:

- `1347:2` tiene `responde` una vez, y es verbo común: «este cambio en el panorama inflacionario
  **responde** principalmente a choques de precios».
- `1347:2` menciona `Marshall` diez veces, y las diez son **el propio hablante en tercera
  persona** («Señala el Consejero señor Marshall que…»), que es el estilo de redacción del acta.
  Contar nombres sin leerlos habría dado un falso positivo de diez.
- `1349:1` menciona `Marshall` una vez: «como señalaba el Consejero señor Enrique Marshall, no
  sería coherente con el mensaje…». Es una **referencia** a algo dicho antes, no una
  intervención. El criterio ya lo decía —una mención, un pase de palabra, una llegada, una
  bienvenida no son intervención— y aquí se ve en la práctica.

De paso, la lectura produjo una corrección: `1347:1` terminaba en
`…para proceder a la votación. Lf \` —residuo de escaneo colgando después del punto final. Es la
misma familia de las 33 barras invertidas sueltas que §22 dejó sin tocar por ser más sucia; ésta se
pudo resolver porque el residuo está al final de la fila y la oración anterior está completa.

## 25. Una sesión de debate, y tres finales que piden tres veredictos distintos

La sesión `2005-04-07` (rondas 197-201, 59 filas) es lo contrario de la anterior: un debate con
turnos cortos alternados —`207:1` hasta `207:12` es una sola discusión partida en doce tramos—, o
sea el caso de muchos hablantes que motivó el eje. Los cortes ya estaban hechos; la lectura los
confirma. Veredicto: **una sola voz por fila en las 59**.

### Tres verbos que parecen cambio de turno y no lo son

- **«acota»**. En `202:2` y `204:3` es el verbo *limitar*: «acota el riesgo de que la expansión
  tome aun mayor fuerza», «el dólar… acota en parte el efecto inflacionario». No es «acota un
  comentario». Buscar el verbo sin leer la oración habría marcado dos falsos positivos.
- **«consulta»**. En `204:3`, «**En respuesta a la consulta de la señora Consejera**, el Gerente…
  señor García, indica que…»: la consulta es de Ovalle pero es una **referencia**, y todo lo que
  sigue es de García, que es el hablante de la fila.
- **«interviene»**. En `211:1`, «el señor García, **interviene** para señalar que…»: presenta el
  turno del propio García, que es a quien está atribuida la fila.

La regla que queda: un verbo de turno sólo delata una segunda voz **si introduce a alguien que no
es el hablante de la fila**.

### Tres finales rotos, tres decisiones distintas

Al revisar las filas que terminan mal aparecieron tres cosas que se parecen y no son lo mismo:

| fila | final | qué es | decisión |
|---|---|---|---|
| `203:2` | `…a considerar. '1^` | basura de escaneo después de un punto completo | **quitar** |
| `207:9` | `…asalariados. \` | barra invertida suelta después de un punto | **quitar** |
| `210:2` | `…hace un mes atrás. Y` | una conjunción que abría una cláusula perdida | **marcar** |
| `213:2` | `…evaluación posible. Perspectivas de inflación en el corto plazo` | un titular de sección pegado al final | **no tocar** |

La distinción que importa es la tercera fila contra las dos primeras. `'1^` y `\` no significan
nada; borrarlos no pierde información. **«Y» sí significa algo**: es la prueba de que se cortó
texto. Borrarla dejaría la fila con un final limpio y **ocultaría el corte**, que es justamente lo
que la columna `Cotejar_PDF` existe para señalar. Un residuo y una truncación se ven parecidos en
el byte y son opuestos en el significado.

La cuarta es de otro eje: el titular es texto real del acta, no un glifo dañado. Quitarlo sería
una decisión de segmentación, y el criterio pide evidencia y decisión acotada para eso, no una
limpieza de pasada.

Estado tras §25: **1.392 filas corregidas, 2.280 operaciones, 196 marcadas, `Texto` intacto en las
9.723**, sha base `d0b64842…` sin cambio. Sesiones cerradas: **31 de 131**; filas leídas **2.346 de
9.723**.

---

## §26. La palabra deletreada con espacios: una familia que el detector no podía ver

Sesión `2007-08-09` (rondas 202–209, 58 filas). Al leer `1357:1` apareció esto:

```
…en el margen las n o tic ia s han sido negativas.
```

No es el caso de §23. §23 trataba **una** letra suelta seguida de la continuación
(`m ayor` → `mayor`), y `detector_partida` busca justamente una partición en dos mitades.
Aquí el OCR esparció la palabra entera en varios trozos: `n o tic ia s`, `T a m b ié n`,
`c o rre g ir`, `C o m isió n`, `a lg u n o s`, `T a s a`. **El detector no las ve porque no
son una partición en dos, son una carrera de trozos cortos.** Igual que en §23, el defecto
estuvo invisible mientras sólo se miró con la herramienta que ya existía.

### Cómo se detecta sin regla automática

Una candidata es una carrera maximal de trozos de 1–4 letras separados por un espacio,
con frontera de palabra a ambos lados, dentro de la cual **alguna sub-ventana** se une en
una palabra establecida del corpus. Tres trampas medidas en el camino, todas con número:

1. **Sin frontera izquierda se detecta de más.** La primera pasada daba `ma de` → `made` y
   `pa y` → `pay`: son los finales de «panora**ma de**» y «Euro**pa y**». 96 candidatas, casi
   todas falsas. Con `(?<![letra])` y `(?![letra])` desaparecen.
2. **El regex greedioso entrega sólo la carrera completa.** En `n o tic ia s han sido` la
   carrera maximal se une en `noticiashansido`, que no es palabra, y `re.finditer` **no
   vuelve atrás por un filtro posterior**: la candidata buena se perdía entera. Hay que
   enumerar las sub-ventanas y quedarse, por posición de inicio, con la más larga que una en
   palabra real. Esto se vio con un conteo que no podía ser cero: `freq['noticias'] = 944` y
   el escáner devolvía 0.
3. **El umbral de frecuencia no sirve para letras sueltas.** Pedir «un trozo que no sea
   palabra» con `freq == 0` descartaba `n o tic ia s` porque `n` aparece 24 veces, `ia` 22 y
   `s` 90 — y aparecen justamente **porque este mismo defecto las esparce por el corpus**.
   La regla que funciona es doble: basta un trozo con `freq < 20`, **o** que la carrera sean
   3+ letras sueltas seguidas, que nunca son español legítimo. Fue esta segunda mitad la que
   hizo aparecer `T a s a` → `Tasa`, que la primera seguía perdiendo porque `T` tiene 38.

### Resultado

Corpus completo: **265 candidatas, 159 ya cubiertas** por operaciones anteriores, **106 sin
cubrir en 58 filas**. De ésas, **32 correcciones en 7 filas** de esta sesión, todas
`PALABRA_PARTIDA`:

| fila | ops | ejemplos |
|---|---:|---|
| `1357:1` | 15 | `n o tic ia s`→`noticias`, `T a m b ié n`→`También`, `c o rre g ir`→`corregir`, `C o m isió n`→`Comisión`, `q u e`→`que` (×3) |
| `1365:2` | 8 | `e fe c to`→`efecto`, `a lg u n o s`→`algunos`, `s im ila r`→`similar`, `cu rv a`→`curva`, `T a s a`→`Tasa` |
| `1385:1` | 5 | `C om enta`→`Comenta`, `A g reg a`→`Agrega`, `p o r`→`por` |
| `1363:1`, `1366:1`, `1390:1`, `1396:1` | 4 | `tem a`→`tema`, `Asim ism o`→`Asimismo`, `com o`→`como`, `cam b io s`→`cambios` |

Las 74 restantes están en sesiones todavía no leídas y quedan pendientes de su turno: la
política es curar fila por fila, no aplicar el escáner en bloque. Ninguna reconstrucción
introduce una palabra ajena al corpus — la menos frecuente, `Comisión`, aparece 26 veces.

Sobre el eje multihablante, las 58 filas son **de una sola voz**. Las cuatro banderas eran
referencias, no intervenciones: `1360:1` (Lehmann responde a una consulta de Desormeaux),
`1363:1` (García complementa un punto de Marfán), `1378:1` (Corbo alude a lo pedido por
Marfán), `1398:1` (Desormeaux cita a Schmidt-Hebbel). Es la misma regla de §25: el verbo de
turno sólo delata segunda voz si introduce a alguien que no es el hablante de la fila.

Estado tras §26: **1.393 filas corregidas, 2.312 operaciones, 196 marcadas, `Texto` intacto en
las 9.723**, sha base `d0b64842…` sin cambio. Sesiones cerradas: **32 de 131**; filas leídas
**2.404 de 9.723**.

