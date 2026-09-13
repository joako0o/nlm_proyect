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

---

## §27. Una guarda que no se puede abrir, y una corrección que destapó otro defecto

Sesión `2008-10-09` (rondas 210–215, 43 filas). Sesión de la crisis financiera: presentaciones
de Jaque, García y Cowan, debate y votación (mantención en 8,25 %). Las 43 filas son de una
sola voz; las banderas eran `2105:1` (De Gregorio anunciando que Jaque reemplazará a Lehmann:
un traspaso, y `2105:2` ya es la fila de Jaque), `2110:1` (García aclarando en nombre propio) y
coincidencias de **substring** —`corresponden` y `corresponde` contienen «responde», `acotada`
contiene «acota». Sin `\b` en la expresión regular, el pre-cernido inventa segundas voces.

### El punto ciego de `detector_partida`, y por qué debe seguir ahí

En `2104:1` quedó `presenta ción`. `detector_partida` no la ve: su guarda descarta la pareja
cuando la primera mitad tiene frecuencia ≥ 50, y `presenta` aparece 513 veces. La tentación
obvia es relajar la guarda cuando la segunda mitad no es palabra. **Medido sobre las 9.723
filas: 23 candidatas, de las cuales 5 corromperían texto correcto.**

| texto real | unión tentadora | por qué está mal |
|---|---|---|
| `debe ser monitoreada con sumo cuidado` | `consumo cuidado` | «con sumo cuidado» es español correcto |
| `Después de terminada la cosecha` | `determinada la cosecha` | son dos palabras |
| `será sometida a prueba` | `aprueba` | otra palabra con otro significado |

La diferencia entre `presenta ción` y `con sumo` es **semántica, no estadística**: en los dos
casos la primera mitad es común, la segunda no es palabra y la unión sí lo es. Ningún umbral
los separa. La guarda se queda, `presenta ción` se corrigió a mano, y
`tests/test_escanear_corpus_partida.py` tiene ahora cuatro pruebas que fijan los
contraejemplos para que nadie la "arregle" más adelante.

### Dos familias transversales que salieron de esta sesión

**`Sanco` → `Banco`, 7 filas.** El OCR escribe `S` donde va `B`. `Sanco` no es palabra y
aparece 7 veces, siempre en contextos que sólo admiten `Banco`: «el Sanco Central Europeo»,
«el Sanco Central», «por el Sanco». `Banco` aparece 2.418. Se leyeron las 7 una por una y se
corrigieron las 7, aunque sólo una pertenezca a esta sesión: el eje OCR es transversal por
diseño (§18, §21, §22). En `2264:1` había que **extender** una operación existente
(`r el Sanco , ya que en`, §18) en vez de apilar otra: dos tramos solapados sobre el mismo
texto virgen no se pueden aplicar en ningún orden.

**La hora con punto y coma, 6 filas.** `N:NN horas` aparece 544 veces; `N;NN horas`, 5. Pero
al corregir quedaron **0**, no 1: la sexta era `RPM-2006-02-09:575:1`, y en la base dice
`11 ;30 horas`. La pasada de espacio-antes-de-signo (§18) la convirtió en `11;30 horas`.
**Una corrección propia destapó el defecto.** La lección general: **escanear la base
subcuenta; hay que escanear la salida.** También ésta se resolvió extendiendo la operación
existente, no apilando.

### Lo que no se tocó

- `2120:1` termina en `…hacia la neutralidad. votación.` — es el **titular** de la sección
  siguiente pegado al final, igual que el `213:2` de §25. Segmentación, no OCR.
- `2121:1` termina en `…para proceder a la` — **truncada**. Marcada, no borrada: borrarla
  dejaría un final limpio y ocultaría el corte, igual que el «Y» sola de §25.

### Lo que se marcó en vez de corregir

- `2106:1` `Sanco L1oyd's inglés` → el `Sanco`→`Banco` sí se corrigió, pero `L1oyd's` puede ser
  `Lloyd's` o `Lloyds` y **`Lloyd` aparece 0 veces en el corpus**, así que no hay forma
  mayoritaria propia a la que apelar. §21: una corrección que introduce una palabra ausente
  necesita prueba, no plausibilidad. El contexto sugiere Lloyds; no alcanza.
- `2101:1` `Economista Seníor` → el acento está mal, pero el corpus no tiene forma mayoritaria
  (`Sénior` 79, `Senior` 77) y la misma fila usa las dos grafías. §16 y §17.

Estado tras §27: **1.399 filas corregidas, 2.327 operaciones, 199 marcadas, `Texto` intacto en
las 9.723**, sha base `d0b64842…` sin cambio. Sesiones cerradas: **33 de 131**; filas leídas
**2.447 de 9.723**.

---

## §28. Una corrección anterior que dejó el par invertido, y `COALESCE` al verificar

Sesión `2009-01-08` (rondas 216–221, 65 filas). Enero de 2009: Lehmann, Soto, Bernier y García,
debate largo sobre reglas de Taylor e inercia, y votación por bajar 100 puntos base a 7,25 %.
Las 65 filas son de una sola voz; las banderas eran referencias y traspasos (`2258:1` Claro
consulta a Lehmann, `2289:2` Céspedes responde a Marfán, `2291:1`/`2291:3` De Gregorio cede y
agradece a García, `2295:1` Marfán alude a la quiebra de Lehmann Brothers).

### El par de comillas invertido

`6967:1` traía en la base `"dilema del prisionero".` — **las dos comillas rectas**. Una pasada
anterior (§6/§9 bis) registró la operación `" "` → `" ”"` y convirtió la **primera**, que es la de
apertura, en comilla de **cierre**. El resultado en la salida era `”dilema del prisionero".`:
invertido y sin cerrar. Se resolvió en dos piezas que no se podían apilar:

- **enmendar** la operación existente a `" "` → `" “"` (cambiar la dirección);
- **añadir** `prisionero".` → `prisionero”.` (cerrar el par).

No se apilaron las dos sobre la misma ancla porque ambas caen sobre el mismo par. Las comillas
rectas del corpus bajaron **5 → 4**, y el comentario de `COMILLAS_RECTAS_MAX` resultó inexacto:
decía que las restantes no tenían «dirección deducible», y dos sí la tienen —lo que les falta es
la otra mitad del par (`2417:1` `serrucho".` sin apertura, `2430:1` `aplicando "mecánicamente`
sin cierre). Convertir una comilla suelta sin su par no arregla nada y puede equivocarse, así que
se quedan. El techo bajó a 4.

### `yen` y el ancla larga

`2265:1`: `un modelo más acabado yen su opinión`. Falta el espacio entre conjunción y
preposición. El ancla tuvo que ser larga a propósito: **`yen` aparece 75 veces como moneda
japonesa** y el patrón `[a-z]yen` da **312 coincidencias legítimas** (`constituyen`, `excluyen`,
`atribuyen`). Un reemplazo corto habría destrozado el corpus. Aquí `acabado yen` no admite
lectura verbal, así que el espacio falta.

### Verificar con `COALESCE`, o el conteo miente

Al comprobar el resultado conté **1** comilla recta en la release y casi concluyo que habían
desaparecido cuatro. Era mi script: leía `Texto_Corregido`, que está **vacío en las 8.324 filas
sin corregir**. Con `COALESCE(Texto_Corregido, Texto)` el conteo correcto es **4**. La regla ya
estaba escrita y aun así cayó: cualquier verificación sobre la release tiene que hacer el
`COALESCE`, no leer la columna de corrección sola.

### Lo que no se tocó

- `2292:1` termina en `…durante el transcurso del último mes. votación.` — el **titular** de la
  sección siguiente pegado al final, igual que `2120:1` (§27) y `213:2` (§25). Segmentación.
- `2262:2` «El Gerente señor **Claudia Soto** hace presente…» — tratamiento documental. La
  instrucción es no resolver alias por intuición; se deja tal cual.
- `2289:2` tiene el actor truncado (`Luis Felipe Céspedes Cifue`) en el **campo de actor**, no en
  el texto. Los actores se preservan verbatim: no se tocan.

### Marcas nuevas

| fila | marca | por qué |
|---|---|---|
| `2293:1` | `RECONSTRUCCION_AMBIGUA_POR_COTEJAR` | «…para proceder a la», truncada; **la misma frase partida en el mismo punto** que `2121:1` (§27) |
| `2299:1` | `SIGNO_AUSENTE_POR_COTEJAR` | el Comunicado abre con `“` y nunca cierra (`“`=1, `”`=0); la fila siguiente ya es otra cosa, así que el texto no continúa |
| `2255:1`, `2803:1`, `2841:1` | `RECONSTRUCCION_AMBIGUA_POR_COTEJAR` | «Economista Señor» por «Senior»: el defecto es seguro (`Senior,` 73 + `Sénior,` 64 contra 4 dañadas) pero **el destino no** — las dos grafías correctas están 77 a 79 |

Estado tras §28: **1.399 filas corregidas, 2.329 operaciones, 204 marcadas, `Texto` intacto en
las 9.723**, sha base `d0b64842…` sin cambio. Sesiones cerradas: **34 de 131**; filas leídas
**2.512 de 9.723**.

---

## §29. Lo que parece un defecto y es vocabulario, y lo que parece basura y es un signo

Sesión `2014-07-15` (rondas 222–229, 54 filas). Julio 2014: Lehmann, Fuentes, Vial, Claro,
Vergara y el Subsecretario Micco; votación por recortar 25 pb a 3,75 %. Las 54 filas son de una
sola voz; las banderas eran los traspasos y agradecimientos protocolares del Presidente Vergara
(`6308:2`, `6327:1`, `6331:1`, `6331:3`, `6333:1`, `6335:1`, `6337:1`).

### «tasa de instancia» no es un defecto

Aparece **58 veces en 53 filas** y a primera vista parece una corrupción de «tasa de política»
(1.099 ocurrencias). No lo es, y tres cosas lo prueban:

1. **`instancia` es palabra nativa de estas actas.** Fuera de esa colocución aparece **89
   veces**: «la instancia monetaria de ese momento», «el ritmo de normalización de la instancia
   monetaria», «nos deja en una instancia algo más cómoda», «situación de última instancia»,
   «hacia una instancia más neutral de política monetaria». Es jerga del Banco: *instancia* =
   postura.
2. **El propio texto lo declara.** `273:1`: «el Banco Central decidió elevar la tasa de
   instancia monetaria, **como se llamaba entonces**».
3. **`instancia` → `política` no es una sustitución de OCR posible.** No comparten glifos.

Los dos PDF del repositorio dan **0** `instancia` y 57 `tasa de política`. Eso no contradice
nada: son 2 actas de 131 y simplemente no discuten la postura en esos términos. **La fuente es
evidencia para el texto que cubre, no para todo el corpus.** No se tocó ninguna de las 58.

### Lo que parece basura y es un signo

De los **16 apóstrofos sueltos** del corpus (`X ' Y`), sólo 4 son lo que parecen. El de `674:2`,
`Comunicado ' En su reunión mensual de política monetaria…`, **es la comilla de apertura**: la
estructura es idéntica a la de `2299:1` (§28), que sí trae `“`. Borrarlo habría eliminado un
signo real. Se marcó, y además la fila termina en «…en el horizonte habitual de.» sin cerrar la
frase ni la cita.

Las otras 11 ocurrencias vienen con basura pegada y forman una familia propia, todavía sin
pasar: `4. W '`, `i - J ' -`, `' í \ : Ai`, `¥ '`, `/ '`, `V '`, `i '`, `4 '`, `-4. f. • " ' A)`.
En varios hay que decidir sobre el grupo entero, no sobre el apóstrofo (`5087:1` «una
desaceleración más **4. W '** significativa en China», `5752:3` «continúan **i - J ' -**
anticipando»). Queda anotada para su pasada.

Se corrigieron los 4 limpios: `6331:2` (`debiese ' situarse`, en mitad de la cláusula) y tres en
frontera de párrafo sin basura alrededor (`6067:1`, `6255:1`, `6764:1`).

### `Polítíca` → `Política`, 6 filas

Acento espurio en la segunda «i». `Polítíca` aparece 6 veces, siempre dentro de «Tasa de
Polítíca Monetaria», «Opciones de Polítíca Monetaria», «División Polítíca Financiera» e
«Informe de Polítíca Monetaria». La forma del corpus es `Política`, **3.641** veces, y los dos
PDF dan 218 `Política` y 0 `Polítíca`.

Esto **no** contradice §16 ni §27, y la distinción importa:

| caso | ¿por qué no se corrigió / sí se corrigió |
|---|---|
| `éstos`, `período`, `cuánto` (§16) | las dos formas son español legítimo |
| `Seníor` (§27) | el destino está empatado: `Sénior` 79 contra `Senior` 77 |
| **`Polítíca` (§29)** | **no existe otra lectura: `Política` 3.641 contra 0** |

### Un bug de verificación, no de datos

Al comprobar el resultado conté los apóstrofos sobre `' '.join(filas)` y dio **14** cuando el
registro correcto es **12**: unir filas con un espacio **fabrica coincidencias en la frontera**.
Contando fila por fila da 12. Es la misma familia que «`se r` = 4 dentro de *se recomienda*»:
**los patrones que dependen del contexto no se cuentan sobre texto concatenado.**

Estado tras §29: **1.405 filas corregidas, 2.339 operaciones, 205 marcadas, `Texto` intacto en
las 9.723**, sha base `d0b64842…` sin cambio. Sesiones cerradas: **35 de 131**; filas leídas
**2.566 de 9.723**.

---

## §30. Una sesión sin correcciones, y por qué eso también es un resultado

Sesión `2014-11-18` (rondas 230–234, 42 filas). Noviembre 2014: Pistelli, Fuentes, Naudon, Micco
y los Consejeros; mantención de la TPM en 3,0 %. Las 42 filas son de una sola voz y **no hubo
ninguna corrección OCR que hacer**.

No es que no se haya buscado. Sobre la **salida** (no sobre la base, §27) se midió:

| detector / familia | resultado en estas 42 filas |
|---|---|
| `detector_partida` | 0 |
| `detector_deletreada` | 0 |
| espacio antes de `,` `.` `;` `%` | 0 |
| `A continuación,.` · doble punto · `_____` · hora con `;` · ` / ` · comilla recta · doble espacio | 0 cada una |

Y en el eje multihablante, el pre-cernido marcó verbos de turno (`acota` en `6498:1`, `6515:1`,
`6517:1`) y menciones a García (`6489:1`, `6508:3`, `6510:1`). Con `\b` en la expresión regular,
las coincidencias de *verbo que introduce a alguien que no es el hablante de la fila* son
**cero**: las menciones son los traspasos y agradecimientos protocolares del Presidente Vergara.
Es la regla de §25 aplicada con la frontera de palabra que §27 echó en falta.

### La única marca

`6517:3` abre la cita del Comunicado y **se corta a mitad de una frase**:

> «…nuevos brotes de volatilidad no son descartables. **Las proyecciones de.**»

Con la cita sin cerrar (`“`=1, `”`=0 en la salida). Es texto perdido, no un residuo: borrar el
fragmento dejaría un final limpio y **ocultaría el corte**. Es la cuarta vez que aparece exactamente
este patrón —`210:2` (§25), `2121:1` (§27), `2293:1` y `2299:1` (§28)— y las cuatro se marcaron en
vez de limpiarse. Ya es una familia: **las actas se truncan al final del Comunicado**, y conviene
revisarlo con los PDF como un solo asunto y no fila por fila.

### Por qué importa registrar una sesión vacía

Una sesión sin correcciones es información: dice que la densidad de defectos **no es uniforme** y
que los detectores ya cubren lo que hay. Si sólo se documentaran los hallazgos, el criterio daría
la impresión de que cada sesión tiene algo, y perdería valor como mapa de dónde queda trabajo.

Estado tras §30: **1.405 filas corregidas, 2.339 operaciones, 206 marcadas, `Texto` intacto en
las 9.723**, sha base `d0b64842…` sin cambio. Sesiones cerradas: **36 de 131**; filas leídas
**2.608 de 9.723**.

---

## §31. Dos familias que se cerraron sin tocarlas, y un punto ciego que resultó ser transversal

La sesión `2007-01-11` (rondas 235-241, 50 filas) es una reunión con IPoM: presentaciones largas
del staff, ronda de comentarios y votación. **Una sola voz en las 50 filas.** El pre-cernido marcó
35 verbos de turno que «introducen a otro» y los 35 son el estilo en tercera persona del acta
(«Señala el señor Ministro que…», «Indica el señor Consejero…», «Manifiesta el señor Presidente…»)
o referencias a algo dicho antes («la afirmación del Gerente de Estudios señor Valdés», «está de
acuerdo con la impresión del Consejero señor Manuel Marfán»). La regla de §25 funciona: un verbo
de turno sólo delata una segunda voz si introduce a alguien que no es el hablante de la fila, y
aquí el «otro» es siempre el propio hablante nombrado por su cargo.

### Dos familias que se cierran sin corregir nada

**La hora escrita con punto (`17.15 horas`) NO es un defecto.** En el corpus hay 39 filas con
`N.NN horas` contra 550 con `N:NN horas`, y 15 filas tienen **las dos formas**, 12 de ellas en la
misma plantilla: «suspende la Sesión a las 14.30 horas e informa que la misma se reanudará a las
16:00 horas». Eso parecía concluyente: la misma frase, dos puntuaciones. Pero los dos PDF del
repositorio zanjaron la pregunta, y la respuesta es la contraria de la que sugería el conteo:

| PDF | «Se levanta la Sesión a las…» | otras horas del mismo acta |
|---|---|---|
| `2005-06-09 - Actas.pdf` | **16.45** | `13:10 horas`, `16:00 horas`, `16.30 hrs` |
| `2005-07-12 - Actas.pdf` | **16.50** | `13:00 horas`, `16:00 horas` |

La fuente escribe con punto la hora del cierre y con dos puntos las demás; el corpus reproduce
fielmente esa inconsistencia (`RPM-2005-06-09:295:1` = `16.45`, `RPM-2005-07-12:311:1` = `16.50`).
Corregir las 39 filas habría sido fabricar una uniformidad que el acta no tiene. Es la regla de
§17 al revés: allí el PDF desmintió al corpus; aquí lo confirma. **No se toca.**

**`A continuación,.` tampoco.** Son 76 filas y la duda era si la coma antes del punto es un
defecto de puntuación o el resto de una frase cortada. Medido: **las 76 ocurrencias terminan la
fila**. No es una coma mal puesta: es el límite de segmentación, el punto donde el acta dice
«A continuación, [se da paso a…]» y el tramo siguiente quedó en la fila siguiente, atribuida a
otro hablante. Borrar la coma no arreglaría nada y taparía el corte. **No se toca**, y la familia
queda adjudicada: no es OCR.

### El punto ciego que resultó ser una familia de 40

`1054:1` tenía «sea necesario **profundizarl o**. En su opinión…». `detector_partida` daba 0
candidatos en las 50 filas, y no es un bug que se arregle abriendo su guarda: lo que bloquea el
caso es `freq[segunda mitad] >= 50`, y la segunda mitad es una letra (`a` aparece 37.528 veces,
`o`, `e`, `s`). Bajar `--min-frec` de 30 a 5 no cambia nada, porque el bloqueo no viene por ahí.
Y abrir la guarda de la primera mitad ya está medido y prohibido (§27: mete «con sumo
cuidado» → «consumo»).

La regla que sí discrimina va por el otro lado: **si la primera pieza es marginal en el corpus no
es una palabra, y si al pegarle la letra aparece una que sí lo es, el espacio sobra.** Marginal =
`freq <= 1` **o** `freq * 20 <= freq[junta]` (lo segundo cubre la pieza que el OCR partió varias
veces: `estim a` aparece 4 veces y `estima` 1.283). Se promovió a
`scripts/escanear_corpus.py::detector_partida_letra` con 8 pruebas, incluidas las cuatro de
`TestLaGuardaNoSePuedeAbrir`, que siguen fuera porque en ninguna la segunda mitad es una letra.

Medido sobre las 9.723 filas: **40 candidatos, 40 verdaderos** — `clim a`, `últim o`, `consum o`,
`form a`, `habrí a`, `hacerl o`, `darl e`, `aumentarl a`, `mantenerl a`, `subirl a`, `ocurri ó`,
`tem a`, `Inform e`, `monetari a`, `sistem a`, `próxim o`, `conjunt o`, `Análisi s`, `medi a`,
`coment a`, `posicione s`, `efectuad o`, `consecuenci a`, `IPo M`, `torn o`, `apreci a`, `com o`,
`cas i`, `Agreg a`, `acertad a`, `trayectori a`, `permitirí a`, `sugerí a`, `estim a`,
`profundizarl o`. Se corrigieron **58 palabras partidas en 44 filas** del corpus entero, no sólo
de esta sesión: la lectura de una sesión destapó defectos de 2005, 2006, 2008, 2009 y 2010.

Dos trampas al escribir el detector, las dos medidas:

1. **Pedir `freq[primera] == 0` no sirve.** La pieza dañada aparece **una** vez, que es ésa. Con
   `== 0` el detector devolvía 0 candidatos con `profundizarl o` todavía en la salida: la trampa 3
   de §26, otra vez.
2. **Pedir que la palabra junta sea frecuente pierde el caso que motivó el detector.**
   `profundizarlo` aparece 1 vez. Por eso este detector se llama con `min_frec=1`.

### La misma regla con la segunda mitad de 2-4 letras: 91 %, y por eso no es regla automática

Con la primera pieza marginal y la segunda de 2 a 4 letras aparecen 23 candidatos. **21 son
verdaderos** (`Estados Uni dos`, `tam poco`, `consecuentem ente`, `Dem anda`, `hídri ca`,
`prim era`, `sustantivam ente`, `sig no`, `seña la` ×2, `retroced ido`, `tranqui lo`, `tend ido`
×2, `vincu la`, `acumu lan`, `repli ca`, `fundamen tal`, `aliment icia`, `made ra`,
`eventua les`) y se corrigieron. Los dos que no:

- **`desorden en`** (`6797:1`): «se advierte un grado de **desorden en** lo que respecta a la
  forma como se está…». Es español correcto; juntarlo daría «desordenen», un verbo. Estadísticamente
  es idéntico a los 21 buenos: primera pieza marginal, unión atestiguada. **La diferencia es
  semántica**, exactamente la conclusión de §27.
- **`bail out`** (`3089:2`): variante legítima del inglés; el corpus usa `bailout` y `bail out`.
  No es ortográficamente imposible, así que no entra por §3 ter.

Con `desorden en` en la lista, la regla con segunda mitad larga es un **generador de candidatos al
91 %**, no una regla: se aplica leyendo, y por eso no se promovió a detector permanente. El de una
letra sí, porque ahí la precisión medida fue 40/40.

### Las dos enmiendas, y un bug del generador que las produjo

Tres candidatos caían dentro del tramo de una operación ya registrada, y ahí la regla de §15 es
extender, no apilar:

| fila | operación existente | qué se hizo |
|---|---|---|
| `144:1` | `LETRA_CONFUNDIDA` «r datos efectivos de! últim o trim estre» → «…del últim o trimestre» | se **enmendó** el `Despues` a «…del último trimestre»: la operación ya cubría el tramo y había conservado `últim o` |
| `2334:1` | `ESPACIO_INDEBIDO` «ión pasada , se acumu » | se **enmendó** el `Despues` quitándole también el espacio final: el espacio que parte `acumu lan` era el último carácter del tramo |
| `2253:2` | `ESPACIO_INDEBIDO` «o personal , queda mas» | **operación nueva** con ancla «tranqui lo por», sin «mas»: el espacio está fuera del tramo ajeno, así que no hay solapamiento |

El generador del lote tenía un bug que produjo el primer rechazo: componía el ancla buscando la
frase en la **BASE**, y como toma la primera ocurrencia, en `570:1` («mantenerl a» dos veces, la
primera ya corregida por §16-§17) apuntó al tramo ya arreglado y se solapó con la operación
existente. **El ancla se compone sobre la SALIDA**, que es donde el defecto sigue vivo, y se exige
que sea única en las dos versiones. Además el generador ahora pre-verifica el solapamiento con las
operaciones registradas y separa lo que va por `enmendar_operacion.py`, en vez de llegar al
rechazo de `agregar_correcciones_ocr.py`.

Otro bug propio, del mismo lote: con dos ocurrencias de la misma frase en una fila (`1308:2` tiene
«monetari a en 5% anual.» dos veces) el generador elegía **siempre la primera** y emitía dos anclas
idénticas. Se arregla llevando la cuenta de qué ocurrencia es cada candidata.

### Los residuos de la sesión, y la letra suelta que no se borra

| fila | qué había | veredicto |
|---|---|---|
| `1038:1` | `…referida Universidad. /D` | **quitar**: la familia «barra + letras al final» tiene 3 casos (`/D`, `/xD`, ` v\ /y` en `5497:1`) y el tercero muestra el racimo entero |
| `1046:2` | `…del Banco. /xD` | **quitar**, misma familia |
| `1056:1` | `…están balanceados. 1-^ Por lo anterior…` | **quitar**: marcador de nota al pie mal leído, 1 ocurrencia en el corpus, mismo caso que `'1^` de §25 |
| `1044:1` | `…producto potencial. k Respecto de inflación…` | **quitar**: « k » aparece 3 veces en el corpus y las 3 son residuo; a diferencia de la « V » de §8 ter, la «k» no tiene ningún uso legítimo atestiguado |
| `1034:1` y `1024:2` | `J)` y `kJ)` en un límite de párrafo | **quitar**, con tres mediciones: las 4 «LETRA)» del corpus son cierres de sigla o este par; los dos PDF (45 páginas) no tienen ninguna enumeración con letra; las enumeraciones reales del acta son minúsculas o romanas (`a)`, `i)`, `iv)`) y las presentaciones del staff usan viñetas «•» (141 en 33 filas) |
| `1024:2` | `(Purchasing Managers’Index)` | **reponer el espacio**: las otras 4 apariciones del corpus lo llevan, y un apóstrofo no pega dos palabras. El apóstrofo tipográfico no se toca: es estilo de la fuente |
| `1050:1` | `…de 25 puntos base. i` | **marcar**: es la figura de `210:2` (§25). Hay **20 filas** que terminan en letra suelta tras un punto completo; las letras sueltas de mitad de fila sí son residuo seguro (` k `, ` U `) porque el texto sigue, pero al final no hay forma de distinguir sin el acta. La familia de 20 se revisa de una vez con los PDF, como la del Comunicado (§30) |
| `1049:3` | `…reajuste tarifario eléctrico y por la l-P El Gerente…` | **marcar**: aquí el corte se ve, la cláusula queda a medias. «l-P» aparece 1 vez en 9.723 filas y no hay contraparte que fije la lectura; borrarlo dejaría «…y por la El Gerente…», que tapa el corte |
| `1032:1` | `A continuación,.` | **no tocar** (ver arriba) |
| `1058:1` | `17.15 horas` | **no tocar** (ver arriba) |
| `1049:2` | `…de tendencia; Si Richard Freedman…` | **no tocar**: mayúscula tras punto y coma es del fuente; cambiar el signo por punto sería una decisión de puntuación, no de lectura óptica |

La fila `147:1` (2005-03-10) quedó fuera del pase a propósito: su candidato (`id o`) es la cola de
`m e d id o`, una carrera letra por letra, y lo que hay que corregir es la carrera entera. Es un
recordatorio de que **el detector encuentra el par, pero el veredicto es sobre la fila**: cuando el
candidato cae dentro de una carrera más larga, arreglar sólo el par deja «m e d ido».

Estado tras §31: **1.418 filas corregidas, 2.405 operaciones, 208 marcadas, `Texto` intacto en las
9.723**, sha base `d0b64842…` sin cambio. Sesiones cerradas: **37 de 131**; filas leídas **2.658 de
9.723**. Suite local de OCR: **72 pruebas, OK**.

### Lo que hizo lenta esta ronda, y qué cambia

Esta ronda tardó mucho más que las anteriores y vale la pena dejar escrito por qué, porque las
causas son de procedimiento y se repiten:

1. **Hice tres rondas en una.** Cerrar la sesión eran 8 operaciones; el detector nuevo, las 58
   correcciones transversales y las 21 de segunda mitad larga fueron el resto. El corte natural
   era commitear el cierre de la sesión y seguir la pasada transversal después.
2. **Tres bugs propios que sólo aparecieron cuando algo se negó o un conteo no cuadró**: componer
   el ancla sobre la BASE en vez de la SALIDA, tomar siempre la primera ocurrencia de una frase
   repetida, y un parche cuyo `if` nunca matcheó y por lo tanto no hizo nada. El tercero es el
   grave: una operación que di por aplicada no lo estaba, y lo descubrí de rebote al reejecutar el
   detector. **Regla: el generador de un lote tiene que contabilizar todos sus candidatos**
   (aplicados / enmendados / excluidos / rechazados) y el turno no termina sin reejecutar el
   detector y comprobar que el residuo es el esperado.
3. **Costo fijo por script desechable: 4,27 s** (leer el xlsx 1,88 s + `core.validar()` 2,26 s),
   pagado unas 40 veces. Con un snapshot de `Texto` virgen y salida en `.cache/textos.json`
   (4,53 s una vez) cada script siguiente cuesta **0,47 s**.
4. **Explorar en seis pasadas lo que cabía en una**: medí la misma regla con `freq == 0`,
   `freq <= 1`, `freq * 20`, `>= 1`, `>= 2` y largos 2/3/4 en scripts separados, recargando el
   corpus cada vez. Las variantes de una regla se miden en un solo script.
5. **Un nombre de archivo mal escrito** (`escanar_corpus.py` por `escanear_corpus.py`) costó tres
   comandos fallidos y una teoría equivocada sobre caracteres invisibles. Cuando `ls` muestra el
   archivo y `open()` no lo encuentra, lo primero es comparar los bytes del nombre
   (`[hex(ord(c)) for c in nombre]`), no sospechar del sistema de archivos.

---

## §32. Una sesión de pregunta y respuesta partida en dos filas, y la «r» que sobra

`2009-07-09` (rondas 242-250) es la sesión más grande leída hasta aquí: **113 filas, 130.454
caracteres, 14 hablantes**. **Una sola voz en las 113.** El pre-cernido marcó tres verbos de turno
que introducen a otro y los tres son referencias: `2615:1` (Soto responde «a la pregunta del
Consejero señor Sebastián Claro»), `2620:5` (el Ministro «manifiesta concordar con lo planteado por
el Consejero señor Manuel Marfán»), `2628:1` («las razones ya mencionadas por el Presidente»).

### La estructura que domina esta sesión no es un defecto

Cuarenta y tantas filas vienen en pares: una termina **en coma** y la siguiente **empieza en
minúscula** con «a lo cual…»:

| fila | final | fila | apertura |
|---|---|---|---|
| `2609:1` | «…consulta si la tasa efectiva es mayor que la estimada**,**» | `2609:2` | «**a lo cual** el señor Lehmann responde que…» |
| `2620:3` | «…en el mismo sentido**,**» | `2620:4` | «**a lo cual** el señor Pablo García señala que…» |
| `2628:3` | «…consulta acerca de cómo se define una anomalía**,**» | `2628:4` | «**a lo cual** el Gerente de División Estudios…» |

Es el acta redactando «X consulta si…, a lo cual Y responde que…» como una sola oración, y la
segmentación la partió en dos filas atribuidas a hablantes distintos. **No es OCR y no se toca**:
unir esas filas sería una decisión de segmentación, y el criterio pide evidencia y decisión acotada
para eso, no una limpieza de pasada (§25, cuarto caso). Conviene dejarlo escrito porque es el
espejo de `A continuación,.` (§31): allí el corte escondía el traspaso de la palabra; aquí el
traspaso está dicho explícitamente en la fila siguiente.

### Lo que sí se corrigió

| fila | qué había | veredicto |
|---|---|---|
| `2628:2` | «para ver los **/** traspasos de tasas» | **quitar la barra**. La familia « / » tiene 31 ocurrencias en 29 filas y **no es uniforme**: hay usos legítimos («40 / 50 dólares», «tasa - euro / tasa - dólar») y residuos de salto de columna («no una tasa de / crecimiento», «front loaded. / Puntualiza»). Ésta no puede ser separador: separa un artículo de su sustantivo. Se elimina la ocurrencia, no la cadena (§8 ter) |
| `2633:1` | «…ese tipo de problemas. **r.** Sobre los indicadores…» | **quitar la «r»**, por **enmienda** de la operación de §18: el residuo cae dentro del tramo «oblemas. r . Sobre los», y dos tramos solapados no se aplican en ningún orden (§15). El Tipo pasó de `ESPACIO_INDEBIDO` a `SIMBOLO_SUELTO` porque lo que sobrevive del arreglo es un símbolo que sobra (§22) |
| `2620:3` | «consulta si el staff **Wer\\e** alguna percepción» | **marcar**. Falta el verbo y «Wer» aparece 1 vez en 9.723 filas, sin contraparte (§8 bis). Se consideró la familia «staff e\\ apoyo» = «staff el apoyo», pero aquí daría «si el staff Wer el alguna percepción», que no es español |
| `2623:3` | «…no una caída. **r**» al final | **marcar**: es la familia de 20 filas de §31, que se revisa de una vez con los PDF |

La «r» suelta entre oraciones aparece **6 veces en 6 filas** (`2362:1`, `2428:1` «r 4/», `2578:1`
«r -», `2633:1`, `3134:1`, `4510:1` «r "») y las 6 son residuo. A diferencia de la «V» de §8 ter
(11 residuos contra 2 figuras legítimas) y como la «k» de §31 (3 de 3), la «r» no tiene ningún uso
legítimo atestiguado: se elimina.

### Lo que se miró y no se tocó

Los **6 candidatos de acento** de la sesión se arbitraron uno por uno y son todos variantes
legítimas de §16: `hacía`/`hacia` (las dos son palabras), `cuánto` ×2 (124 apariciones), `tornó`
(verbo real), `periodo` ×2 (las dos grafías conviven, 661/60). Los cuatro detectores
(`partida`, `deletreada`, `partida_letra`, `acento`) dieron 0, 0, 0 y 6 sobre las 113 filas: la
pasada transversal de §31 ya había limpiado esta sesión, que tenía `cas i`, `Agreg a`,
`fundamen tal`, `aliment icia`, `made ra`, `acertad a` y `eventua les`.

### El hallazgo transversal: «staff e\\ apoyo» = «staff el apoyo»

Al enumerar las 29 barras invertidas que quedan en la salida apareció una familia repetida que
ninguna sesión había visto, porque está repartida en nueve:

| fila | texto | lectura |
|---|---|---|
| `777:1`, `1610:1`, `1635:1`, `1680:1` | «agradece al staff**e\\** material preparado» | «al staff **el** material» |
| `2754:2` | «agradeciendo al staff por **e\\** apoyo brindado» | «por **el** apoyo» |
| `3810:2`, `3887:2`, `4510:1` | «agradeciendo al staff **e\\** apoyo brindado» | «**el** apoyo» |
| `4513:1` | «agradeciendo al staff **e\\** excelente análisis» | «**el** excelente análisis» |

La lectura la prueba el propio corpus, que tiene 427 «staff» y escribe «agradece el análisis del
staff», «agradece al staff los Informes», «agradece al staff, por los informes»: el artículo es
obligatorio y la `l` leída como `\\` es el mismo glifo de §21-§22 al revés. Es la regla de §8 bis en
su forma útil: **un residuo que aparece varias veces suele tener al lado la forma correcta**.

Estado tras §32: **1.419 filas corregidas, 2.406 operaciones, 210 marcadas, `Texto` intacto en las
9.723**, sha base `d0b64842…` sin cambio. Sesiones cerradas: **38 de 131**; filas leídas **2.771 de
9.723**.

### Aplicado: las 9 filas de «staff e\\»

El pase se aplicó en el mismo turno y dejó **9 operaciones en 9 filas** (6 agregadas, 3 parcheadas
sobre filas que ya tenían correcciones de §16). Tras aplicarlo, la familia queda en **0** y las
barras invertidas del corpus bajan de 29 a 20.

La corroboración más fuerte no es la regla sino el propio corpus: la forma correcta ya aparecía
**20 veces** («agradece al staff el material preparado»), **25** («al staff por el apoyo
brindado»), **19** («al staff el apoyo brindado») y **3** («al staff el excelente análisis»). Las 9
filas corregidas se suman a esas 67, no inventan una forma nueva.

**El validador frenó la primera versión.** En las 4 filas donde el OCR pegó las dos palabras
(`staffe\\`, sin espacio) el reemplazo ingenuo produjo `staffel`, y `core.validar()` lo rechazó:
«el reemplazo introduce *staffel*, que no está en el corpus ni en TERMINOS_FORANEOS». La lectura
correcta es `staff el`, con el espacio restaurado por §16, igual que en `fundamen tal` o
`intervenci ón`. Se enmendó el `Despues` de esas 4 con `enmendar_operacion.py`. Queda como recordatorio
de por qué la guarda léxica existe: **una sustitución puede ser correcta en el símbolo y aun así
fabricar una palabra que no existe.**

---

## §33. La «i» suelta, el ítem «4.» que no era residuo, y las rondas que se renumeran

`2011-12-13` tiene **71 filas**, y se leyó en dos tandas: 25 primero y 42 después (más 4 que ya
estaban anotadas). **Una sola voz en todas**, 0 banderas del pre-cernido en la primera tanda y 2 en
la segunda, ambas referencia o anuncio («en relación con la pregunta del Consejero señor Sebastián
Claro…, el señor Sergio Lehmann señala que el Gerente… señor Claudio Soto **exhibirá** el perfil»:
una pregunta ajena citada y un traspaso de la palabra anunciado, que por criterio no son
intervenciones). Diciembre 2011, Vergara presidente, TPM a 4,0 %.

**Seis correcciones, cero marcas**, todas residuos entre oraciones completas:

| fila | qué había | veredicto |
|---|---|---|
| `4513:1` | «Aún **/** así, advierte que hay indicios» | **quitar la barra**: separa un adverbio de su conector |
| `4498:2` | «las líneas de crédito. **i/** pero sí una mayor disposición» | **quitar `i/`** |
| `4504:1` | «en la economía chilena. **i** El señor Luis Óscar Herrera plantea» | **quitar la `i`** |
| `4502:3` | «**i,-** Siendo las 16:00 horas, se reanuda la Reunión…» | **quitar `i,- `**: era lo único que impedía que la fila empezara en mayúscula |
| `4510:1` | «apuesta por un recorte. **r "** Sobre las opciones…» | **quitar los dos**: la «r» de §32 y una comilla recta huérfana (la fila tiene 1 recta y 0 curvas; lo que sigue es narración) |
| `4489:2` | «con el tipo de cambio. **4.'** El señor Claudio Soto hace presente» | **quitar sólo el apóstrofo**, por enmienda de la operación de §18 que ya cubría el tramo (`4 .'` → `4.'`) |

### El ítem «4.» no era residuo

La tentación era borrar `4.'` entero. No: `4.` es el **ítem 4 de la estructura habitual del acta**,
que aparece así en **21 filas** del corpus («4. Con estos antecedentes…», «4. Las condiciones
financieras internas…», «4. La inflación efectiva del IPC…»). Borrarlo habría destruido estructura
documental, que es justo lo que el criterio manda conservar. Se fue el apóstrofo, que ése sí es
huérfano: la fila tiene 1 apóstrofo y 0 comillas curvas.

El censo de apóstrofos queda en **41 en 38 filas**, y ya está clasificado: **11 son legítimos**
(`Moody's`, `Lloyd's`, `Standard & Poor's`, `Purchasing Managers' Index`, `Naudon Dell'Oro`) y el
resto viene pegado a basura de salto de página (`'V/`, `' ' v`, `' í \ : Ai`, `CENT'RAL`,
`reanclar1'`).

### La familia de la «i» suelta

`(?<=\.)\s+i[/,-]?(?=\s)` da **18 casos en 18 filas** repartidos en **14 sesiones**, once de ellas
ya cerradas cuando se midió. La lectura es la de la «r» de §32: tras un punto, una `i` minúscula
suelta no es palabra, no es número romano (no hay lista que numerar) y no es viñeta (el corpus usa
`•`, 141 veces en 33 filas). Tras este pase quedan 16.

**Por qué no se vio antes:** cada una de esas filas tenía **una sola** ocurrencia, sin compañía que
la hiciera sospechosa dentro de su sesión. Es la tercera vez que pasa (`staff e\` en §32, la letra
final en §31): **las pasadas por sesión encuentran filas; las familias se encuentran buscándolas en
la salida completa.**

### Trampa de procedimiento: las rondas se renumeran

`rondas_lectura_lote9.py plan` **reescribe** `plan_rondas.json` (línea 148) dejando fuera las filas
ya leídas, así que **la numeración de las rondas cambia cada vez que se corre**: el plan pasó de 856
a 605 rondas en esta sesión. Consecuencias prácticas, ambas sufridas aquí:

1. **Una etiqueta «rondas N-M» sólo vale contra la versión del plan que estaba vigente.** Las
   rondas 242-250 eran `2009-07-09` (113 filas) antes de regenerar el plan, y son `2012-01-12` +
   `2011-12-13` después. Para citar una ronda hay que decir contra qué plan.
2. **`registrar_sesion FECHA` marca la sesión entera, no las rondas que se leyeron.** Se registró
   `2011-12-13` habiendo leído 25 de sus 71 filas, y el registro quedó diciendo 71. Se corrigió
   leyendo las 42 que faltaban en el mismo turno, pero la regla queda: **antes de
   `registrar_sesion`, comprobar que las filas de la sesión en el corpus coinciden con las que se
   leyeron** (`len([k for k in corpus if k.startswith('RPM-FECHA:')])` contra las IDs analizadas).

Estado tras §33: **1.428 filas corregidas, 2.420 operaciones, 208 revisiones, 210 marcadas**,
`Texto` intacto en las 9.723, sha base `d0b64842…` sin cambio. Sesiones cerradas **39 de 131**,
filas leídas **2.838**.


---

## §34. Los nombres propios dañados se normalizan, con una excepción medida

Hasta esta ronda el criterio era: **un nombre propio nunca se corrige, sólo se marca
`NOMBRE_PROPIO_POR_COTEJAR`**. El usuario lo cambió: *«aprovecha de normalizar los nombres que
encontraste dañado»*.

La primera regla que probé fue de frecuencia: normalizar si el corpus acredita la forma canónica y
ésta es mayoritaria. **Esa regla es insuficiente y produjo un error que las pruebas detectaron.**
«Luis Oscar Herrera» tiene 490 apariciones con tilde contra 10 sin tilde; la frecuencia decía
corregir, y estaba mal. La regla que queda exige dos condiciones, no una:

> **Se normaliza un nombre propio sólo si (a) el corpus acredita la forma canónica *y* (b) la forma
> dañada es una desviación aislada, no la grafía sistemática de un acta entera.** Si (b) falla, no
> es daño de OCR: es cómo está escrito el documento, y se deja intacto.

### El caso que invalidó la regla de frecuencia

Las 10 apariciones de «Luis Oscar Herrera» sin tilde están todas en 2005, y en **cuatro de esas seis
actas es la única forma que existe** (2005-01-11 2/0, 2005-03-10 2/0, 2005-06-09 2/0, 2005-07-12 2/0;
sólo 2005-08-11 1/2 y 2005-11-10 1/3 tienen las dos). Además dos de esas actas están en `data/raw/`
y **ya habían sido cotejadas contra el PDF**: los documentos escriben «Luis Oscar Herrera» sin
tilde y «Óscar» aparece 0 veces. El corpus era fiel; la tilde que habría añadido era una invención.

**Las 10 operaciones se revirtieron.** Las cuatro filas cotejadas quedan `NO_REQUIERE_COTEJO` como
estaban; las otras seis conservan su marca `NOMBRE_PROPIO_POR_COTEJAR` abierta, porque el cotejo
real sólo existe para dos de esas actas y no se cierra una marca con una inferencia sobre
documentos que no se pueden leer. La base queda con dos grafías para esa persona (490 / 10) y eso
es **correcto**: reproduce la variación real de los documentos de 2005, y el registro dice por qué.

### Lo que sí se normalizó: 41 operaciones

Todos los casos restantes pasan (a) y (b) —desviaciones aisladas en actas donde la forma canónica
convive, a menudo muchas veces:

| forma dañada | canónica | dañadas | canónicas | por acta |
|---|---|---|---|---|
| `Madgenzo` | `Magendzo` | 18 | 416 | 6/18, 11/9, 1/8 |
| `Diego Gíanelli` / `Diego Gianellí` | `Diego Gianelli` | 4 / 3 | 117 | siempre con canónica |
| `Enrique Marshali` | `Enrique Marshall` | 2 | 1.011 | 1/2, 1/11 |
| `Marfan` | `Marfán` | 2 | 1.506 | 1/14, 1/5 |
| `Felipe Larrain` | `Felipe Larraín` | 2 | 266 | 1/7, 1/9 |
| `Beltran de Ramón` | `Beltrán de Ramón` | 2 | 249 | 1/2, 1/1 |
| `Kiaus Schmidt-Hebbei` | `Klaus Schmidt-Hebbel` | 1 | 94 | 1/1 |
| `Claudios Soto` | `Claudio Soto` | 1 | 1.274 | 1/27 |
| `Sebastian Claro` | `Sebastián Claro` | 1 | 1.103 | 1/11 |
| `Rodrigo Váldés` | `Rodrigo Valdés` | 1 | 227 | 1/5 |
| `Lehmann Beresí` | `Lehmann Beresi` | 1 | 148 | 1/1 |
| `Pablo Garcia Silva` / `Pablo Garcia` | `Pablo García Silva` / `Pablo García` | 1 / 1 | 90 / 737 | 1/0, 1/5 |
| `Larraín Bascuñan` | `Larraín Bascuñán` | 1 | 32 | 1/0 |
| `Naudon DeN’Oro` / `Naudon DellOro` / `Naudon Dell'Oro` | `Naudon Dell’Oro` | 1 / 1 / 3 | 12 | 1/0 cada una |

El `1/0` de las tres últimas no las invalida: en esas actas el nombre aparece **una sola vez**, así
que la forma canónica no puede convivir; la acreditan las otras actas. Ese es el límite de la
prueba (b): distingue «única forma de un acta que lo repite» de «única mención de un acta».

**Tras el pase no queda ninguna de las 17 formas dañadas**, y cada persona tiene una sola grafía:
`Magendzo` 434, `Marfán` 1.508, `Diego Gianelli` 124, `Claudio Soto` 1.275, `Sebastián Claro` 1.104,
`Enrique Marshall` 1.013, `Pablo García` 739, `Felipe Larraín` 268, `Beltrán de Ramón` 251,
`Rodrigo Valdés` 228, `Lehmann Beresi` 149, `Klaus Schmidt-Hebbel` 95, `Larraín Bascuñán` 33,
`Naudon Dell’Oro` 17. `Texto` intacto en las 9.723 y sha base sin cambio.

### Lo que sigue marcado

`Miguel Angel Nacrur Gazali` (2 filas): el corpus no tiene ninguna otra grafía, falla (a).
`Conference Support` (probablemente *The Conference Board*, sin fuente), `JP Morgan` / `JPMorgan`,
`Bank o f America`, las firmas truncadas y las seis filas de «Luis Oscar Herrera» sin PDF.
**La normalización no reemplaza el cotejo: lo usa como evidencia cuando existe, y cuando no existe
no lo suplanta.**

### Dos notas de implementación

1. **Se unificó también lo que no estaba dañado.** Las 3 filas con `Naudon Dell'Oro` (apóstrofo
   recto) no tenían daño: se unificaron a `Dell’Oro` porque el apóstrofo curvo es el mayoritario del
   corpus (59 contra 41) y una base gold no debe tener dos grafías para la misma persona. Reversible
   y no toca `Texto`.
2. **La operación se ciñe al tramo dañado.** En `RPM-2015-03-19:6655:2` la fila es tan corta
   («El señor Diego Gianellí anticipa que.», 37 caracteres) que la ventana de contexto del generador
   coincidió con la fila entera y `test_ninguna_operacion_reescribe_la_fila_completa` la rechazó.
   Tenía razón: una operación cuyo `Antes` es la fila completa es indistinguible de una reescritura.
   Se estrechó a `Gianellí` → `Gianelli`. **No se debilitó la prueba para que pasara.**
3. El tipo sigue el defecto: `LETRA_CONFUNDIDA` cuando cambian letras (`DeN’Oro`, `Kiaus`,
   `Madgenzo`), `ACENTO_FALTANTE`/`ACENTO_INDEBIDO` cuando sólo cambia el acento (`Marfan`,
   `Felipe Larrain`, `Sebastian Claro`).

**Lección para los pases transversales:** un pase automático sobre el corpus entero tiene que
correrse *antes* contra las pruebas del repo, no después. Las dos fallas que aparecieron aquí
(la tilde inventada y la fila reescrita) eran exactamente lo que esas pruebas están para atrapar.

---

## §35. La entrega v8 y el re-anclaje de una operación

Los cuatro cortes del lote10 se publicaron en `data/releases/continuidad_procedimental_v8`
(9.723 -> 9.724 filas; una fila nueva, `RPM-2008-08-14:1995:2`). La entrega anterior no se toca.

**El `ID` de la base es un contador posicional.** Una sola fila nueva corre en +1 el `ID` de todas
las siguientes, y las lecturas procedimentales v5 lo traen clavado. Eso tumbó el build con «Prueba
no coincide o ya aplicada». Los archivos que había que tocar (`reviewed_procedural_v5.py`,
`continuidades_procedimentales_v5.json`, `compare_functional_v7.py`, `preparar_data.py`,
`qa_preparacion.py`) están todos fijados por hash en manifiestos vigentes, así que no se cambió ni
un byte: se refresca el `ID` posicional en memoria, y sólo cuando todo lo demás coincide
exactamente. El gate nuevo es `scripts/compare_procedural_v8.py`.

**Consecuencia para el eje OCR.** Al partir el padre 1995 en el cambio de hablante, la palabra
`cambiarías` de la fila `RPM-2008-08-14:1995:1` pasó al segmento nuevo. La operación que la corrige
se re-ancló a `RPM-2008-08-14:1995:2` con su actor (`Sergio Lehmann Beresi`) y su contexto
actualizados, dejando constancia del motivo en la justificación. **Es la única de las 2.466 que se
movió**; las otras dos que tocan padres resegmentados (`RPM-2010-02-11:2960:1` ×2 y
`RPM-2006-05-11:657:2`) siguen calzando donde estaban.

La capa corregida se reconstruyó sobre v8 en `data/releases/correccion_ocr_v2`, sin sobrescribir
`correccion_ocr_v1`. Verificado: 9.724 filas, 1.462 con `Texto_Corregido`, `Texto` intacto en todas,
**cero formas dañadas** de los 17 nombres, y las 10 apariciones de «Luis Oscar Herrera» sin tilde
conservadas porque son la grafía del documento (§34).

**Regla que queda:** cuando un corte cambia la segmentación, hay que re-verificar las anclas del
registro OCR contra la nueva base. El validador las atrapa solo (`«cambiaría» no aparece 1 veces en
el texto virgen de la fila`), así que basta con correrlo; lo que no se puede hacer es publicarlo sin
correrlo.

---

## §36. Sesión 2008-03-13 y dos cosas que la cola no dice

**La cola multihablante está construida sobre los padres del consolidado, no sobre la base
construida.** Las dos filas de esta sesión que aparecían en la cola de 74 ya estaban bien partidas:
el padre 1718 tiene `1718:10` = Enrique Marshall Rivera y `1718:11` = Manuel Marfán Lewis; el padre
1737 tiene `1737:1` = Jorge Desormeaux Jiménez y `1737:2` = Sebastián Claro Edwards. Antes de
proponer un corte hay que mirar la base, no la cola. Es lo mismo que pasó con tres de los cuatro
cortes del lote10 (§35): el detector automático ya partía esos padres.

**Una sesión puede destapar una familia transversal.** La palabra deletreada `T a sa` apareció una
vez en el Acuerdo de esta sesión. Medida en todo el corpus: **6 apariciones contra 1.428 formas
correctas**, siempre pegada al número del acuerdo (`NN-NN-NNMMDD-T a sa de Política Monetaria`). Se
corrigieron las 6, en seis actas distintas. La fila leída dio la pista; la decisión la dio el conteo.

### Lo que se corrigió

| fila | antes | después | tipo |
|---|---|---|---|
| `2008-03-13:1705:1` | `(3,8®/o y 3,2%` | `(3,8% y 3,2%` | `LETRA_CONFUNDIDA` |
| `2008-03-13:1728:2` | `señor a Andrés Velasco` | `señor Andrés Velasco` | `PALABRA_SOBRANTE` |
| `2008-03-13:1735:1` | `con el sesgó eliminado` | `con el sesgo eliminado` | `ACENTO_INDEBIDO` |
| 6 actas | `…-T a sa de Política Monetaria` | `…-Tasa de Política Monetaria` | `PALABRA_PARTIDA` |

`señor a ` aparece **1 vez** en todo el corpus (`doña a ` 0, `don a ` 0). `sesgó` aparece **1 vez**
y la misma oración usa bien `sesgo` unos renglones antes. Ninguno de los dos es dudoso.

### Lo que se marcó en vez de corregirse

- **`4.3%` con punto** entre tres cifras con coma en el mismo enunciado. El corpus tiene 5.998
  decimales con coma y **60 con punto**: la coma es la convención, pero esos 60 prueban que la fuente
  a veces escribe punto. Cambiar el separador de una cifra financiera sin el PDF es falsear un dato,
  no corregir ortografía → `CIFRA_INCONSISTENTE_POR_COTEJAR`.
- **Una fila que termina en «señor Andrés»** sin apellido ni punto, seguida de otra que empieza
  «El Ministro de Hacienda señor a Andrés Velasco indica que…». Falta algo entre las dos, pero
  completarlo sería inventar texto → `RECONSTRUCCION_AMBIGUA_POR_COTEJAR`.

### El detector de acentos sigue siendo un generador de candidatos, no una regla

De 14 candidatos, 13 eran falsos positivos: `éstos`, `dónde`, `cuánto`, `quién`, `cuándo` y
`terminó` llevan tilde diacrítica o verbal legítima, y `publica` era el verbo («que publica la
Reserva Federal»), no el adjetivo. El único real fue `sesgó`. **Precisión 1/14 en esta sesión**: el
detector sirve para no dejar nada sin mirar, no para decidir.

También quedó medido que el chequeo de paréntesis desbalanceados da falsos positivos con las
enumeraciones `a) b) c)`, y que `Velasco B.` no es una firma truncada: es la abreviatura que el
corpus usa en otras tres actas.

---

## §37. Sesión 2009-02-12: ocho candidatos, cero correcciones

Cien filas leídas y ni una corrección. **Eso es un resultado, no una sesión perdida**: sin sesiones
que se cierran en cero no hay forma de saber si las correcciones de las otras las exige el texto o
las exige el proceso. Los ocho candidatos se rechazaron uno por uno, con la razón medida.

### El candidato multihablante era una mención, no una voz

El padre 2325, atribuido a Pablo García, dice:

> «En cuanto al tema del endeudamiento **a que se refirió la señora Ministra de Hacienda
> Subrogante**, estima que se encuentra vinculado al tipo de cambio…»

El detector permisivo vio un cargo + nombre y propuso a Recart como segunda voz. No lo es: García
viene hablando desde el inicio del párrafo y el sujeto de «estima que» sigue siendo él. Nombrar a
quien habló antes no es tomar la palabra. Que el detector **estricto** devolviera `Actor_Estricto
= None` ya era la señal.

### Los cuatro candidatos de acento eran formas correctas

| forma | filas | por qué no se toca |
|---|---|---|
| `éstos` | 5 | tilde diacrítica del pronombre demostrativo; `estos` (1.384) es el determinante |
| `dónde` | 1 | tilde diacrítica en «respecto a dónde se quiere llegar» |
| `continua` | 1 | es el adjetivo: «la debilidad **continua** de los sistemas financieros» |
| `periodo` | 2 | véase abajo |

**`periodo` merece el detalle.** Sin tilde aparece 60 veces y con tilde 661, una proporción que a
primera vista parece daño. Pero las 60 están **repartidas en 36 actos distintos**: no es un glifo
que se rompió en un escaneo, es cómo escribe la fuente en un tercio del corpus. La regla del §34
exige que la forma desviada sea una desviación **aislada**; ésta es sistemática, y además
`período`/`periodo` son las dos válidas. Corregirla sería imponer una preferencia ortográfica, no
reparar un defecto.

### Los tres candidatos de signo también

- **2362:1 «paréntesis desbalanceado»**: los tres cierres son `i) ii) iii)` de una enumeración.
  Mismo falso positivo que `a) b) c)` en 2008-03-13; el auditor ya los descuenta.
- **2381:1 «termina en comilla»**: las comillas están balanceadas (1 y 1) y cierran la cita del
  Acuerdo. Normal en las 132 actas.
- **2324:1 «termina sin punto»**: la oración está completa y la fila siguiente empieza con
  mayúscula y otro hablante, así que falta el punto de verdad. Pero la fila ya lleva
  `FINAL_SIN_PUNTUACION`, la alerta que sostiene la **reserva 2661**. Añadir el punto cerraría una
  reserva abierta, que es exactamente lo que no se hace.

### Lo que cambió en la herramienta

`scripts/analisis_sesion.py` descontaba mal los paréntesis de enumeración y daba el mismo falso
positivo en cada sesión. Ahora resta los cierres `a) / ii) / 1)` antes de contar, y separa las
filas sin puntuación final que **ya llevan** `FINAL_SIN_PUNTUACION` de las que no, para no volver a
proponer cerrar una reserva.

---

## §38. Dos cosas medidas: la precisión real del detector de acentos y el censo de caracteres

### El detector de acentos rinde 1 acierto en 27 candidatos

Tres sesiones leídas con el auditor, todos los candidatos adjudicados a mano:

| sesión | candidatos | reales | cuáles |
|---|---|---|---|
| 2008-03-13 | 14 | **1** | `sesgó` → `sesgo` |
| 2009-02-12 | 10 | 0 | — |
| 2006-06-15 | 3 | 0 | — |
| **total** | **27** | **1** | precisión ≈ 4 % |

No es un defecto del detector: está diseñado para proponer, no para decidir, y el §21 ya decía que
un detector de este tipo es un generador de candidatos. Lo que la medición agrega es **cuánto
cuesta**: hay que leer los 27. Conviene saberlo antes de correrlo sobre las 90 sesiones que faltan,
y conviene no convertirlo en regla — con 4 % de precisión una regla automática habría introducido
26 errores por cada acierto.

Los falsos positivos son siempre los mismos tres patrones: **tilde diacrítica** (`éste`, `dónde`,
`cuánto`, `quién`, `cuándo`), **par verbo/adjetivo** (`publica`/`pública`, `continua`/`continúa`) y
**variante ortográfica válida** (`periodo`/`período`, en 36 actos). En actas anteriores a 2010 la
tilde de los demostrativos ni siquiera era discutible: la Ortografía la recomendaba.

### Censo de caracteres fuera del repertorio (9.724 filas)

El auditor marcaba las viñetas como residuo y daba falso positivo en cada sesión con láminas. Se
midió el corpus entero en vez de parchar el síntoma:

| char | veces | actos | juicio |
|---|---|---|---|
| `•` | 141 | 31 | **legítimo** — marcador de lista de las presentaciones |
| `€` | 63 | 19 | **legítimo** — signo de moneda |
| `±` | 5 | 2 | por revisar cuando toque su sesión |
| `¥` | 5 | 5 | legítimo — moneda, un acto distinto cada vez |
| `►` | 2 | 2 | por revisar |
| `─` | 2 | 1 | por revisar |
| `®` | 2 | 1 | **daño** — `2015-03-19:6691:1`, «Particul^ m®n‘® Estados Unidos» |
| `£` | 1 | 1 | legítimo — moneda |
| `´` | 1 | 1 | por revisar |
| `\xad` | 1 | 1 | por revisar — guion blando |

Entraron al repertorio `•`, `€`, `¥` y `£`. Los demás quedan anotados aquí con su fila: no se
corrigen fuera de su sesión, que es donde se lee el contexto.

### Dos sesiones seguidas en cero

`2009-02-12` y `2006-06-15` se cerraron sin una sola corrección. Con `2008-03-13` (4 correcciones
más el pase transversal de 6 actas) eso deja la proporción en **una sesión de cada tres con algo
que corregir**. Si aparecieran correcciones en todas, habría que sospechar del proceso y no del
corpus.

---

## §39. Sesión 2009-08-13: la cola está 78 % resuelta y un punto espurio repetido 76 veces

### La cola de 74 casos hay que medirla contra la base, no contra el consolidado

Los tres candidatos multihablante de esta sesión ya estaban bien partidos: el padre 2661 tiene
`2661:10` = Velasco («El efecto debiera ser menor y al revés, acota el Ministro,») y `2661:11` =
Lehmann («y el señor Lehmann complementa que será necesario afinar el análisis»); el 2667 tiene
`2667:1/2/3` = Velasco / Lehmann / Soto; el 2680 tiene `2680:2/3/4` = Consejo / De Gregorio / García.

Eso motivó medir la cola entera:

| | |
|---|---|
| casos en la cola | 74 (73 padres distintos) |
| **cuyo padre ya está partido en la base construida** | **58 (78 %)** |
| que sí hay que mirar uno por uno | 16 |

**La cola se construyó sobre los padres del consolidado de origen, donde la segmentación automática
todavía no había corrido.** Contra la base construida, la mayoría ya está resuelta. Los 16 restantes
se reparten en 15 sesiones (`2009-03-12` tiene 2). Uno de ellos, el padre 2325 de `2009-02-12`, ya
se adjudicó en el §37: era una mención, no una voz.

### El pase transversal: un punto que no pertenece a la oración

`2680:4` terminaba en «A continuación,.» — coma y punto juntos. Medido sobre las 9.724 filas:

- **76 apariciones, las 76 al final de una fila**, cero en medio de una fila;
- las 76 con la fila siguiente **en minúscula y en la misma sesión**;
- las 76 seguidas de «el señor Presidente ofrece la palabra al…»;
- unidas dan «A continuación, el señor Presidente ofrece la palabra al…», que es la construcción
  normal del acta — «A continuación,» seguida de minúscula aparece **378 veces** sin el punto.

El punto es residuo del salto de párrafo de la fuente. Se quitaron los 76; después del pase
«A continuación,» + minúscula pasó de 378 a **454** (+76 exactos). `Texto` conserva las 76 formas
vírgenes.

### Las correcciones de la sesión

| fila | antes | después | tipo | evidencia |
|---|---|---|---|---|
| `2681:1` | `medidas complementarías posibles` | `complementarias` | `ACENTO_INDEBIDO` | 1 vez contra 47 |
| `2680:2` | `Siendo las 16; 15 horas` | `16:15` | `PUNTUACION` | 106 «Siendo las HH:MM horas» con dos puntos, y la fila anterior del mismo padre escribe `16:15` |

### La que no: `hacía` chocó con una guardia de regresión y perdió

`2666:3` dice «los flujos netos de inversión de cartera **hacía** economías emergentes». Ahí hace
falta la preposición: el verbo no tiene sujeto ni complemento posible. Se corrigió, y
`test_los_pares_minimos_legitimos_no_se_tocaron` falló:

> `AssertionError: 31 not greater than or equal to 32 : «hacía» bajó a 31 (< 32): es una forma
> legítima, no un defecto; una pasada la está corrigiendo de más`

Ese test existe porque una pasada anterior **sí** corrigió `hacía` de más, y el suelo de 32 es la
cicatriz. La regla del proyecto es no ensanchar una guardia para que pase un cambio, así que
**la corrección se revirtió** y la fila quedó marcada en `Marcas_Adicionales` con
`RECONSTRUCCION_AMBIGUA_POR_COTEJAR` y el razonamiento completo.

No es que la lectura esté mal: es que resolverlo exige el PDF o una decisión explícita sobre esa
guardia, y ninguna de las dos cosas se hace bajando un suelo en silencio. Queda visible para
quien tenga el acta a la vista.

### Lo que se marcó

`2681:1` tiene, entre dos oraciones que se leen bien, un `' ' v` que no es texto: residuo de una
viñeta o de un marcador de la lámina proyectada. El corpus usa `•` como viñeta (141 veces), así que
esto no es una viñeta reconocible. Borrarlo sería suponer qué era → `RECONSTRUCCION_AMBIGUA_POR_COTEJAR`.

### Los candidatos de acento, otra vez

Seis candidatos, dos reales (`hacía`, `complementarías`) y cuatro falsos: `cuánto` (interrogativo),
`periodo` (variante válida en 36 actos), `motivó` (verbo).

**Acumulado del detector en cuatro sesiones: 33 candidatos, 3 aciertos, precisión 9 %.**

| sesión | candidatos | reales |
|---|---|---|
| 2008-03-13 | 14 | 1 |
| 2009-02-12 | 10 | 0 |
| 2006-06-15 | 3 | 0 |
| 2009-08-13 | 6 | 2 * |
| **total** | **33** | **3** |

\* De los 2 de esta sesión, `hacía` se revirtió por la guardia de regresión (véase arriba) y sólo
`complementarías` quedó aplicado. El conteo mide **candidatos que el texto realmente pedía
corregir**, no correcciones publicadas: son dos cosas distintas y conviene no confundirlas.

---

## §40. `hacía`: la enumeración completa y por qué el suelo de la guardia bajó de 32 a 17

En el §39 una corrección de `hacía` → `hacia` chocó con `test_los_pares_minimos_legitimos_no_se_tocaron`
y **se revirtió**: el suelo de 32 existe porque una pasada anterior corrigió `hacía` de más, y la
regla es no ensanchar una guardia para que pase un cambio. Hasta ahí, correcto.

Pero en `2008-01-10` apareció el mismo fenómeno («una tendencia **hacía** la baja»), y en vez de
volver a revertir se hizo lo que faltaba: **enumerar las 32 apariciones una por una**.

### El resultado

| | | ejemplos |
|---|---|---|
| **el verbo** | **17** | «hacía presente», «hacía referencia», «hacía mención» (×5), «hacía necesario» (×3), «hacía que», «hacía prudente», «lo hacía moderadamente», «lo hacía conforme», «el mercado hacía del actuar» |
| **la preposición `hacia`** | **15** | «hacía delante» (×3), «hacía adelante» (×2), «hacía la baja», «hacía arriba», «hacía un riesgo al alza», «hacía América Latina», «hacía las economías emergentes» (×2), «hacía niveles neutrales», «hacía el término del año», «hacía el tercer trimestre», «cartera hacía economías emergentes» |

En las 15 el verbo no tiene sujeto ni complemento posible: siempre rigen un complemento de dirección
o destino. `hacia` aparece 2.183 veces en el corpus.

### Por qué esto no es ensanchar la guardia

Bajar el suelo de 32 a 17 **no debilita el test**: después del cambio la guardia sigue protegiendo
las 17 apariciones legítimas, y si una pasada futura se come cualquiera de ellas, vuelve a fallar.
Lo que cambió es que el número ahora **está medido** en vez de heredado. La enumeración completa
quedó escrita en el comentario del test, junto con la razón, para que el próximo que lo vea no tenga
que rehacerla.

La distinción que importa: *ensanchar una guardia para que pase un cambio* es bajar un umbral hasta
que el test deje de quejarse. *Corregir una guardia con evidencia* es enumerar el universo que
protege y mostrar que el umbral estaba mal. Lo primero esconde un problema; lo segundo lo documenta.

Las 15 se corrigieron, incluida `2009-08-13:2666:3`, cuya marca `RECONSTRUCCION_AMBIGUA_POR_COTEJAR`
se retiró porque ya no aplica. `hacia` pasó de 2.183 a **2.198** (+15 exactos).

### Tres residuos de paginación

`1623:1` terminaba en «…en dirección al alza**. 7**». Ese 7 suelto es el número de página del acta
escaneada — y era, además, lo que la cola multihablante mostraba como «**7** Menciona el señor
Magendzo…»: el final de `1623:1` pegado al comienzo de `1623:2`, que ya está bien partido.

Medido en la salida: sólo 3 filas del corpus terminan en número suelto tras una oración completa
(las otras dos son `2008-09-04:2064:1` y `2014-06-12:6257:5`, ambas en « 4»). **Ojo al remedir:** en
el Texto virgen el mismo patrón da 11, porque 8 filas del acta de `2012-04-17` arrastran el pie de
página explícito «Sesión N° 184 Página N de 26», que una tanda previa de 24 operaciones ya retira.
Las dos cifras son ciertas, cada una en su columna; la justificación de las operaciones lo dice.

### Nota sobre la herramienta

`enmendar_operacion.py` rechaza una enmienda que sólo cambia `Justificacion` (compara `Despues` y
`Tipo`). Las tres justificaciones se editaron directo en el registro y se reverificó con
`--validar` y la suite.

---

## §41. Sesión 2009-04-09: la más grande del corpus, cero correcciones — y qué significa eso

147 filas, 123.858 caracteres, la sesión con más filas pendientes. Se cerró sin una sola corrección.
Nueve candidatos de acento, los nueve formas correctas:

| término | filas | por qué es correcta |
|---|---|---|
| `previó` | 1 | verbo *prever*: «cuando se **previó** resultados positivos». La concordancia con «resultados» (debiera ser «se previeron») es de la fuente, no un glifo roto; y `previo` es adjetivo, no cabría ahí |
| `efectuara` | 1 | subjuntivo, que es lo que pide «el comentario que **efectuara** el señor Ministro» |
| `desarrolló` | 1 | verbo: «se **desarrolló** toda una discusión» |
| `dónde` | 1 | tilde diacrítica en interrogativa indirecta |
| `éstos` | 3 | tilde diacrítica del demostrativo |
| `periodo` | 2 | variante válida, presente en 36 actos (§37) |

El único candidato multihablante también estaba resuelto: el padre 2443 tiene **13 segmentos** y el
offset que la cola marcaba (1115) es exactamente el límite entre `2443:5` = De Gregorio («el señor
Presidente indica que Consensus considera precio de mercado») y `2443:6` = Lehmann («y el señor
Lehmann complementa que en la gráfica…»).

### Lo que seis sesiones ya dicen sobre dónde vive el daño que queda

| sesión | filas | correcciones | cómo aparecieron |
|---|---|---|---|
| 2008-03-13 | 109 | 4 + 6 | 3 locales; `T a sa` se volvió transversal al medirlo |
| 2009-02-12 | 102 | 0 | — |
| 2006-06-15 | 71 | 0 | — |
| 2009-08-13 | 79 | 2 + 76 | 2 locales; `A continuación,.` se volvió transversal |
| 2008-01-10 | 49 | 0 + 15 + 3 | `hacía` y la paginación, ambas transversales |
| 2009-04-09 | 147 | 0 | — |

**Tres de las seis sesiones no tienen nada que corregir, y las correcciones que sí aparecieron son
casi todas familias transversales que una fila suelta destapó.** El daño residual del corpus no está
repartido como erratas sesión por sesión: está concentrado en patrones que se repiten en decenas de
actas. La consecuencia práctica es que **medir cada candidato contra el corpus entero rinde mucho
más que leer buscando erratas** — los cuatro pases transversales de este tramo (`T a sa` 6 actas,
`A continuación,.` 76 filas, `hacía` 15 filas, paginación 3 filas) suman 100 filas corregidas, y
ninguno habría salido de una lectura fila por fila.

### Detector de acentos, acumulado

**42 candidatos, 3 que el texto pedía, 2 aplicados — precisión 7 %.** El tercero (`hacía` en
`2009-08-13`) se aplicó después, cuando la enumeración completa del §40 mostró que la guardia
protegía 15 defectos y no 32 formas legítimas.

---

## §42. Sesión 2010-02-11 y dos familias que quedan medidas y pendientes

134 filas, 117.420 caracteres. Una sola corrección, y dos familias grandes que conviene dejar
escritas con su número exacto antes de que se pierdan.

### Los tres candidatos multihablante, y el marcador que los delata

Los tres estaban ya partidos, y los tres con la misma construcción:

| padre | segmentos | el límite que la cola marcaba |
|---|---|---|
| 2896 | 4 | `2896:2` Lehmann («a lo cual el señor Lehmann responde que no lo es,») / `2896:3` García («**en tanto que** el señor Pablo García señala…») |
| 2910 | 3 | `2910:2` Soto («…responde que era de 0%,») / `2910:3` García («**en tanto que** el señor Pablo García agrega…») |
| 2915 | 4 | `2915:3` García / `2915:4` Soto |

**«en tanto que» seguido de un nombre es un marcador fiable de cambio de voz** en estas actas:
introduce al segundo hablante dentro de la misma oración. Vale como señal de lectura, no como regla
automática — pero cuando aparece, hay que mirar.

### El detector volvió a proponer `hacía`, y la respuesta sigue siendo no

`2960:1`: «su benchmark es el promedio de las mismas, **hacía** necesario que alguien las condujera a
ello». Es el verbo *hacer*, exactamente una de las 17 que la enumeración del §40 clasificó como
legítimas y dejó intactas. Que el detector la vuelva a proponer es esperado: su precisión es 7 %.

### La corrección

`2906:1` — «lo cual no lo hace inmune a los shocks**'**, por el contrario, estos provocan…». La
comilla no es posesivo inglés (no hay palabra en inglés) ni cierra ninguna cita: es la única comilla
recta de la fila y el corpus usa tipográficas (360 `“` y 347 `”`). → `SIMBOLO_SUELTO`.

### Familia 1: comillas rectas — 41 en 38 filas, y es **mixta**

No se puede resolver por regla, porque conviven dos cosas distintas:

| basura de OCR | posesivo inglés legítimo |
|---|---|
| `'’i^sgo geopolítico` → riesgo | `Purchasing Managers' Index` |
| `costos f' H- laborales` | `Lloyd's` |
| `'V/` · `'aquerida` → adquirida · `en'el caso` · `L' desanclaje` | |

Hay que leerlas una por una. Quedan pendientes.

### Familia 2: filas que terminan en letra suelta — **23**, no 20

El conteo que circulaba era 20; medido ahora son **23**. El patrón es nítido:

```
…el Informe de Política Monetaria de mayo. H
…se esta hablando. i          …respecto al Banco u
…seguirá monitoreando. y      …25 puntos base. i
```

Es **la primera letra de la palabra con que arranca el párrafo siguiente**, que el escaneo dejó
colgada al final de la página anterior. La fila siguiente siempre empieza con la palabra completa
(`2915:4` arranca «En cuanto a las tasas…»), así que la letra no le pertenece a ninguna de las dos.
Borrarla sería perder un carácter de la fuente si el corte cayó a mitad de palabra; confirmarlo
exige el PDF. **Pendientes, con el número corregido.**

---

## §43. Sesión 2010-09-16: la fórmula del Acuerdo, 12 actas, y cómo se extiende una operación

Ninguna fila en la cola multihablante y los cinco candidatos de acento eran formas correctas
(`dónde` ×2 y `cuánto` ×2 interrogativos, `motivó` verbo). El hallazgo salió de la sección de signos:
la fila del Acuerdo traía punto y coma donde la fórmula pide dos puntos.

### El pase transversal

«el Consejo adopta/adoptó el siguiente Acuerdo**X** NNN-NN-NNMMDD - Tasa de Política Monetaria»:

| | apariciones |
|---|---|
| con dos puntos | **106** |
| con punto y coma | **12** |
| con coma o punto | 0 |

Las 12 son **estructuralmente idénticas** a las otras: mismo número de acuerdo y mismo título a
continuación. Un punto y coma no puede introducir un acuerdo enumerado; es lectura de OCR del dos
puntos. Se corrigieron las 12, repartidas en 12 actas entre 2005 y 2015 — 2005-01-11, 2005-10-11,
2006-08-10, 2006-12-14, 2007-02-08, 2007-04-12, 2007-05-10, 2007-06-14, 2009-09-08, 2010-09-16,
2011-02-17, 2015-01-15.

Es exactamente la misma evidencia que en §39 para «Siendo las 16; 15 horas» → «16:15», donde también
había 106 apariciones con dos puntos. Después del pase: 118 con dos puntos, 0 con punto y coma en la
salida, y las 12 intactas en `Texto`.

### Cuando dos defectos caen en el mismo tramo

`2006-12-14:1020:2` ya tenía una operación en ese tramo, del pase de «T a sa» de §36:

```
Antes   : 'erdo; 101-01-061214-T asa de Política Mon'
Despues : 'erdo; 101-01-061214-Tasa de Política Mon'
```

El punto y coma está **dentro** del tramo ya registrado, así que no se puede añadir una segunda
operación: dos tramos solapados sobre el mismo texto virgen no se pueden aplicar en ningún orden. El
validador de `agregar_correcciones_ocr.py --parche` lo detecta y no escribe nada. Lo correcto es
**extender** la operación existente, que es lo que hace `enmendar_operacion.py`:

```
Despues : 'erdo: 101-01-061214-Tasa de Política Mon'   ← arregla las dos cosas
Tipo    : PUNTUACION
```

Queda documentado en la justificación que ahí caen dos defectos y por qué se arreglan juntos. Es la
regla del §15 aplicada: cuando dos defectos comparten tramo, se extiende, no se apila.

### Lo que se marcó y lo que se dejó

- **`3422:1`** termina en «se suma a lo expresado por el señor» **sin el nombre**, y la fila siguiente
  empieza una oración nueva, así que el nombre no está en ninguna parte. Ya llevaba
  `FINAL_SIN_PUNTUACION`, pero esa alerta dice sólo que falta el punto, no que falta un nombre: se
  marcó además con `RECONSTRUCCION_AMBIGUA_POR_COTEJAR`. Mismo caso que `2008-03-13:1728:1`.
- **`3431:2` tiene la comilla de cierre sin apertura** (0 `“`, 1 `”`). No se tocó: revisando las
  demás filas de Acuerdo el panorama es inconsistente — unas tienen el par completo, otras sólo la
  apertura, otras sólo el cierre. Reconstruir cuáles llevaban comilla de apertura exige el PDF.

---

## §44. Sesión 2008-12-11: 22 candidatos de acento, 2 reales — y un bug del propio auditor

La sesión con más candidatos hasta ahora: **22 en 16 filas**. Dos eran daño real:

| fila | antes | después | evidencia |
|---|---|---|---|
| `2190:1` | «alguna vez él **efectúo**» | `efectuó` | el sujeto es «él»: hace falta la 3.ª persona del pretérito. 1 aparición contra 51, y en la misma fila el verbo se usa bien («se efectuó ese ejercicio») |
| `2253:1` | «curso de acción en **politica** monetaria» | `política` | 1 aparición contra **5.573** — la forma correcta más frecuente de todo el corpus |

Los otros 20 eran formas legítimas: `costó`, `terminó`, `marcó`, `inició` son verbos; `publica` es el
verbo en «el índice se publica desde el 2003»; `continua` es el adjetivo; `efectuara` es subjuntivo;
`éstos`, `cuánto`, `cuándo` llevan tilde diacrítica.

### El candidato multihablante, rechazado leyendo el párrafo entero

Padre 2228, un solo segmento, atribuido a Andrés Velasco:

> «El señor Ministro de Hacienda señala que de los tres aspectos que **ha mencionado el señor
> Presidente**, le parece que hay uno de ellos que es fácil de confirmar…»

Es una referencia retrospectiva, no un cambio de voz, y todo el párrafo es del Ministro: «Agrega que
en el Ministerio de Hacienda se efectuó ese ejercicio», «Las otras dos interrogantes **le parecen**
más difíciles de medir», «si uno efectuara este ejercicio por plazo». Mismo patrón que el padre 2325
del §37. **Dos de dos** en candidatos con `Actor_Estricto` apuntando a un cargo: los dos eran
menciones.

### Un bug del auditor, encontrado porque dio un resultado imposible

`2206:1` salió marcada como «paréntesis desbalanceado», pero tiene **6 y 6**. El descuento de
enumeraciones que se añadió en el §37 incluía dígitos, y el `\d{1,2})` se comía el cierre de
paréntesis de verdad:

```
(más de 50)   →  contaba «50)» como enumeración
(1 en 1)      →  contaba «1)»  como enumeración
```

Medido en el corpus: los dígitos dan **4** apariciones y las cuatro son paréntesis reales, mientras
que las enumeraciones de letra y romanas son **48**. El patrón ahora sólo admite `[a-z]` y `[ivx]+`.
Verificado: `2206:1` pasa a 0 y las sesiones anteriores siguen en 0.

Vale la pena notar cómo se encontró: el auditor reportó un desbalance en una fila que, leída, estaba
balanceada. **Cuando una herramienta contradice lo que se está viendo, la equivocada suele ser la
herramienta.**

### Detector de acentos, acumulado

**64 candidatos, 5 que el texto pedía, precisión 8 %.**

---

## §45. Sesión 2011-02-17: el pase transversal que **no** era, y cómo se supo

Primera sesión con **cero candidatos en los cuatro detectores** —ni acento, ni palabra partida, ni
partida por letra, ni deletreada— y ninguna fila en la cola multihablante. Cero correcciones.

Lo valioso de la sesión es una medición que **cerró** un pase que parecía obvio.

### La tentación

Contando filas de Acuerdo: **103 tienen comilla de apertura y 15 no.** Con esa proporción, y con el
precedente de la fórmula del Acuerdo en §43 (106 contra 12), añadir las 15 comillas faltantes parecía
el mismo caso.

### Por qué no lo era

Se midió **dónde cae** la comilla en las 103 que la tienen:

```
distancia desde «Acuerdo:» hasta la «“»:  +148, +172, +202, +208, +209, +211,
                                          +224, +232, +233, +310, +313, +315,
                                          +333, +406, +434, … +2009 caracteres
```

No es una posición fija, y la razón se ve en el texto: la comilla **no abre el Acuerdo**, abre la
cita del **Comunicado**, que viene después y a distancia variable.

```
…Acuerdo: 76-01-050407-Tasa de Política Monetaria. Se acuerda aumentar la tasa…
   …Comunicado “ En su reunión mensual de política monetaria…
                ^ aquí, no después de «Acuerdo:»
```

Y al revisar las 15:

| | |
|---|---|
| **5** no tienen sección Comunicado | filas de 101 a 500 caracteres; no les falta nada, la cita está en otra fila |
| **10** tienen la sección pero sin `“` | y no de forma uniforme: unas traen una comilla recta o simple en su lugar (`Comunicado ' En su…`, `Comunicado ‘En su…`, `Comunicado ‘‘En su…`), otras no traen nada |

Medido en conjunto: **113 filas de Acuerdo tienen sección Comunicado y sólo 61 llevan la comilla de
apertura — 54 %.** Con esa dispersión no hay forma de saber cuáles la llevaban en el original.
**Se deja pendiente para el cotejo con PDF.**

### La diferencia con §43

| | fórmula del Acuerdo (§43) | comilla del Comunicado (§45) |
|---|---|---|
| proporción | 106 contra 12 | 61 contra 52 |
| posición | fija, inmediatamente después de «Acuerdo» | variable, 148 a 2.009 caracteres |
| forma alternativa | ninguna (0 con coma o punto) | cuatro: recta, simple, doble simple, ausencia |
| ¿unívoco? | **sí** | **no** |

Una proporción favorable no basta: hace falta que la posición sea fija y que no exista una forma
alternativa plausible. Aquí fallan las dos.

### Estado

Lectura: 3.899 filas. Cinco de las ocho sesiones leídas con el auditor se han cerrado sin
correcciones; las correcciones siguen viniendo de familias transversales, y ahora también sabemos
reconocer cuándo una familia **no** lo es.

---

## §46. Corrección de proceso: la cola del lote10 **no** es la red de multihablantes

Pregunta directa: *¿se están separando los párrafos de múltiples hablantes?* La respuesta medida
obligó a corregir el procedimiento.

### Lo que se venía haciendo, y por qué estaba mal planteado

En las diez sesiones cerradas con el auditor se revisó la **cola del lote10** (74 casos) y se
encontró que la mayoría ya estaba partida en la base. Eso se reportó como «los candidatos ya estaban
resueltos». Era cierto, pero incompleto: **la cola no es donde están los cortes.**

Medido:

| los 4 cortes curados publicados | ¿estaban en la cola de 74? |
|---|---|
| padre 657 (2006-05-11) | **NO** |
| padre 1564 (2007-11-13) | **NO** |
| padre 1995 (2008-08-14) | **NO** |
| padre 2960 (2010-02-11) | **NO** |

Los cuatro tienen `Tipo_Revision = LECTURA_DIRIGIDA_POR_AGENTE`. **La cola y la lectura encuentran
conjuntos disjuntos.** Revisar sólo la cola no es separar multihablantes: es revisar una lista que,
por construcción, no contiene lo que la lectura encuentra.

### La segunda red

`scripts/analisis_sesion.py` ahora tiene una sección **2b** que corre sobre la **base construida**
(no sobre los padres crudos) y con un método distinto: busca filas de **un solo segmento** donde
**otra persona** —no el actor de la fila— es sujeto de un verbo de habla en forma personal.

Resultado sobre las diez sesiones ya cerradas: **13 candidatos**. Leídos uno por uno:

- **7 son ruido de OCR sobre el propio actor**: «José De Gregario» por De Gregorio, «Manuel Mari»
  por Marfán. El apellido dañado no coincide con el del actor y el filtro lo deja pasar.
- **6 son menciones, no cambios de voz**, y caen exacto en las categorías que el criterio excluye:

| fila | qué dice | categoría |
|---|---|---|
| `2008-03-13:1738:1` | Magendzo «desea **apoyar la opinión** del Gerente… señor García», «**al igual que** el señor Pablo García, estima…» | adhesión |
| `2009-02-12:2302:1` | De Gregorio «informa que **asistirá** la Ministra… señora María Olivia Recart a quien **da la bienvenida**» | llegada / bienvenida |
| `2009-02-12:2328:1` | De Gregorio «**en relación con el planteamiento** de la Ministra… señora María Olivia Recart, estima…» | referencia retrospectiva |
| `2006-06-15:723:1` | Marfán «**sugiere incorporar** a la discusión… al Asesor… señor Luis Felipe Céspedes» | propuesta sobre un tercero |
| `2008-12-11:2209:1` | Desormeaux «**concuerda con lo que plantea** el Consejero señor Manuel Marfán **y agrega**…» | adhesión |
| `2008-12-11:2246:1` | Velasco «la pregunta… **la formuló muy bien el sindicalista señor Arturo Martínez** en un Seminario de Enade» | cita de un externo |

**Cero cortes.** Dos redes independientes, métodos distintos, las dos vacías en estas diez sesiones.

### Lo que sí queda pendiente de la cola

De los 74 casos, 58 ya están partidos en la base y 16 no. De esos 16 se adjudicaron 6 en esta
revisión (`2228`, `2325`, `2397`, `2430`, `6185`, `505`) y los 6 son menciones. El caso más
interesante fue `2430:1`: parecía un cambio de voz porque dice «el Gerente de División Operaciones
Financieras **se pregunta**… **Sobre este aspecto, comenta que**…», pero la fila abre con «El Gerente
de División Operaciones Financieras señor **Beltrán De Ramón** señala…»: en 2009 Beltrán *era* ese
Gerente, así que se pregunta y se responde él mismo. **El cargo no identifica a la persona si no se
verifica contra la propia acta.**

Quedan **10 casos** de la cola sin adjudicar, en sesiones todavía no leídas: `2005-08-11:320`,
`2005-12-13:505` (ya visto: es la sección formal del Acuerdo), `2006-01-12:571`, `2006-04-13:647`,
`2007-03-15:1114`, `2007-07-12:1328`, `2007-09-13:1420`, `2012-02-14:4574`, `2012-03-15:4656`,
`2013-07-11:5658`, `2015-01-15:6587`.

### Estado honesto

En las diez sesiones cerradas en este tramo **no se hizo ningún corte nuevo**. Ahora eso está
respaldado por dos redes independientes y por la lectura de los 19 candidatos reales que
produjeron, no sólo por la ausencia de avisos.

---

## §47. Adjudicación completa: los 16 casos de la cola y los 65 del corpus entero

Se pidió revisar los cortes pendientes **porque hay que hacerlos**. Se hizo, y el resultado es que
no queda ninguno — medido, no supuesto.

### Los 16 casos de la cola cuyo padre sigue sin partirse

Leídos uno por uno, los 16 son menciones. Las categorías:

| caso | qué dice | categoría |
|---|---|---|
| `2005-08-11:320` | Eyzaguirre «**en concordancia con lo que ha expresado** el Consejero señor Desormeaux» | adhesión |
| `2005-12-13:505` | «El señor Presidente **fija la sesión** de política monetaria…» | sección formal del Acuerdo |
| `2006-01-12:571` | Desormeaux «**recientemente** el Gerente de Mercados Financieros Nacionales **señaló**» | cita |
| `2006-04-13:647` | Velasco «**Recuerda que** el Gerente de División Estudios **señaló**…» | referencia retrospectiva |
| `2007-03-15:1114` | Valdés «**como también lo menciona** el Gerente… señor De Ramón» | adhesión citada |
| `2007-07-12:1328` | Desormeaux «**en la exposición que realizó** el señor Magendzo indicó» | cita |
| `2007-09-13:1420` | Jadresic «el punto **que ha planteado** el Gerente… **le parece interesante**» | adhesión |
| `2008-12-11:2228` | Velasco «los tres aspectos **que ha mencionado el señor Presidente**» | referencia (§44) |
| `2009-02-12:2325` | García «el tema **al que se refirió** la señora Ministra» | referencia (§37) |
| `2009-03-12:2397` | Claro «**la pregunta que le surge** es si ese escenario…» | es él mismo preguntándose |
| `2009-03-12:2430` | «el Gerente de División Operaciones Financieras **se pregunta**… **comenta que**» | es Beltrán, que en 2009 **era** ese Gerente |
| `2012-02-14:4574` | Vergara «**deja constancia que** el Ministro… **le informó** que solo asistirá» | discurso referido + traspaso propio |
| `2012-03-15:4656` | Vergara «**deja constancia que** el Ministro… **le informó** que no asistirá» | discurso referido + traspaso propio |
| `2013-07-11:5658` | Vial «**su Presidente le manifestó** que se comenzó a intervenir» | cita de un externo |
| `2014-05-15:6185` | Lehmann «**conforme señala** el Gerente… señor Matías Bernier» | cita |
| `2015-01-15:6587` | García «**Como mencionó el Ministro de Hacienda**, señala que…» | referencia retrospectiva |

### La red del §46 corrida sobre el corpus entero

5.823 filas de un solo segmento → **65 menciones reales** de otra persona como sujeto de un verbo de
habla (tras descartar el propio actor con el nombre dañado por OCR: «José De Gregario»,
«Manuel Mari^án», «María Eugenia Wager»).

| marcador que precede la mención | n | % |
|---|---|---|
| pregunta o consulta **resumida** | 19 | 29 % |
| respuesta a / ante / respecto de | 9 | 14 % |
| agradecimiento, saludo, bienvenida | 8 | 12 % |
| adhesión o acuerdo | 6 | 9 % |
| referencia retrospectiva | 2 | 3 % |
| sin marcador automático — **leídas las 21** | 21 | 32 % |

Las 21 leídas son: citas de externos (Janet Yellen, Mark Carney, Mitra Toossi, Marina Silva, Dilma
Rousseff, Arturo Martínez, un Luis Óscar Herrera de BTG Pactual que **no** es el del Banco),
adhesiones («coincidir con las aprensiones planteadas por», «compartir el planteamiento expuesto
por»), y menciones administrativas («acordó renovar la designación del señor Marfán»).

**Cero cortes en los 65.**

### Por qué hay tan pocos

Las actas de este corpus **resumen las intervenciones ajenas en vez de transcribirlas**:

```
…respondiendo a una consulta del Consejero señor Sebastián Claro, agrega que…
…ante una consulta del Consejero señor Sebastián Claro, agrega que…
…en relación a la consulta formulada por el Presidente señor Rodrigo Vergara, el señor Lehmann expresa que…
…respondiendo la consulta específica formulada por el Presidente señor Rodrigo Vergara, precisa que…
```

La pregunta nunca está en el texto: sólo su existencia y la respuesta. Por eso un nombre seguido de
un verbo de habla dentro de una fila de un solo hablante es casi siempre una consulta resumida, y no
un turno transcrito que haya que separar.

### Estado

**No quedan cortes pendientes.** Los 74 casos de la cola están todos resueltos (58 partidos por el
motor, 16 adjudicados como menciones) y la red independiente sobre el corpus entero dio 65
candidatos, todos menciones. Los cuatro cortes curados publicados siguen siendo los únicos, y todos
vinieron de lectura dirigida — que es exactamente lo que se hizo aquí, sólo que esta vez el resultado
fue negativo y ahora está medido en lugar de inferido.

---

## §48. Quinto corte aplicado: la firma correcta era «un tercero responde», no el traspaso

El §47 concluyó que no quedaban cortes. **Estaba mal.** Se pidió revisarlos de nuevo y la segunda
pasada encontró uno, porque se buscó otra cosa.

### Por qué las dos redes anteriores no podían encontrarlo

Se leyeron los cuatro cortes ya publicados para aprender su firma, y resultó que las redes del §46 y
del §47 eran **estructuralmente ciegas** a ella:

| corte | lo que precede | cómo abre la nueva voz |
|---|---|---|
| 657 | «**ofrece la palabra** a don Sergio Lehmann» | **sin sujeto**: «Respecto al crecimiento mundial…» |
| 1564 | «**ofrece la palabra** a la señora Ministra… Recart» | sujeto **pospuesto**: «**Menciona la señora Ministra** que…» |
| 1995 | «ha presentado el Gerente de Análisis Internacional» | sujeto **pospuesto**: «**Señala el señor Gerente** que…» |
| 2960 | «**concede la palabra** al Gerente… Kevin Cowan» | sujeto es un **cargo**, no un nombre |

Las redes buscaban `señor + Nombre propio` con el verbo **después**. Ninguno de los cuatro cumple:
o no hay nombre, o va pospuesto, o el sujeto es un cargo.

### El traspaso de palabra tampoco es la firma

Se midió: **989 fórmulas de traspaso** en el corpus, 671 en filas de un solo segmento. Pero **660
están al final de la fila** —el texto del siguiente hablante está en la fila siguiente, no hay nada
que cortar—. Con ≥1.500 caracteres después: **cero**. Los 4 cortes publicados agotaron ese patrón.

### La firma que sí funciona

**Un tercero responde dentro de una fila de un solo hablante.** 32 candidatos en el corpus;
filtrando los que son el propio actor con su cargo, quedan 2:

- `2005-02-10:103:1` — «El Ministro de Hacienda Subrogante responde…» con el actor registrado como
  Mario Marcel. **Falso**: la fila `100:1` dice «El Ministro de Hacienda Subrogante, **don Mario
  Marcel**» — en esa sesión Marcel *era* el Subrogante.
- **`2008-03-13:1706:1` — corte real.**

### El corte

> «El señor Presidente ofrece la palabra para comentarios sobre el escenario interno. En relación al
> aumento inesperado y generalizado del precio de los alimentos… **el Presidente consulta al señor
> Magendzo** si habría que esperar que este aumento continúe más aceleradamente que hace un mes.
> **El señor Gerente responde afirmativamente** en atención a que dicho aumento no se está viendo
> como un adelanto de una situación que se pensó que iba a ocurrir, sino que se está observando que
> el efecto de la sequía ha sido mayor de lo que se esperaba y que además es persistente en el
> tiempo.»

El hablante anterior **pregunta** y éste **responde con contenido propio**: no es el resumen de una
consulta («respondiendo a una consulta de X, agrega que…»), es la respuesta misma. El roster registra
a Igal Magendzo Weinberger con 13 filas en la sesión.

`HAB-20260912-1706-5` · `Inicio=313` · `Fin=603` · sha256 del padre `1de2586b…bea6`.

### Entrega v9

El gate de v8 está fijado en **exactamente una fila nueva**, así que —siguiendo la convención del
proprio proyecto, que da a cada entrega su driver y su gate— se crearon `preparar_data_v9.py`,
`compare_procedural_v9.py` y `qa_preparacion_v9.py`. Dos cosas hubo que resolver de verdad, no
copiar:

1. **`ID_Turno` se renumera tras un corte** y el gate lo capturó (`padre 1707: T33 -> T34`). Se
   añadió `RPM-2008-03-13` a `sesiones_corte`.
2. **Con dos filas nuevas el corrimiento del ID ya no es +1 fijo**: vale 0 antes del primer corte,
   +1 entre los dos y +2 después del segundo. En vez de fijarlo a mano, el gate ahora **calcula**
   cuántas filas nuevas preceden a cada fila y exige exactamente ese desplazamiento.

`comparacion_procedimental_v9.json`: **`Pasa: true`** · 9.723 → **9.725** · `Filas_Nuevas
['RPM-2008-03-13:1706:2', 'RPM-2008-08-14:1995:2']` · `Cortes: 5` · `IDs_Corridos 7.404` · grupos
9.234 → 9.236 · reservas `{780: 4, 2661: 12, 5252: 4}` intactas. Suite completa **2.256 OK**, F0
**PASA**, `qa_preparacion` **`pasa_controles_bloqueantes: true`**.

La capa OCR se reapuntó a v9 y se reconstruyó: 9.725 filas, 1.557 con `Texto_Corregido`, `Texto`
virgen en las 9.725 (0 diferencias), y **ninguna operación OCR toca el padre 1706**, así que ningún
ancla se invalidó. v8 y `data/processed/` quedaron intactas.

### Lección

Dos redes que dan cero no prueban que no haya nada: prueban que **esas dos redes** no lo ven. Los
cuatro cortes publicados estaban ahí, en el registro, con su evidencia — leerlos era la forma de
aprender qué buscar, y no se hizo hasta que se insistió.

---

## §49. Censo de firmas: ¿queda algún párrafo por cortar?

Pregunta: antes de seguir con la próxima acta, ¿falta algún párrafo que cortar? Se respondió
probando **todas las firmas que exhiben los cinco cortes aplicados**, más sus variantes. Las cuatro
redes del §46–§47 no bastaban porque sólo cubrían dos de ellas.

| # | firma | de dónde sale | candidatos | cortes |
|---|---|---|---|---|
| 1 | `señor + Nombre propio` + verbo de habla | cola lote10 (`TurnDetector`) | 74 | **0** (58 ya partidos, 16 menciones) |
| 2 | lo mismo, sobre la base construida | red §46 | 65 | **0** (todas menciones) |
| 3 | traspaso de palabra + texto largo después | cortes 657, 1564, 1995, 2960 | 989 → 3 con ≥400 ch | **0** pendientes (los 4 ya aplicados) |
| 4 | **un tercero responde** dentro de la fila | corte **1706** | 32 → 2 reales | **1** (aplicado) |
| 5 | **sujeto pospuesto**: «Menciona la señora Ministra que…» | cortes 1564, 1995 | **1** | **0** (es la propia Recart, que *es* la Ministra Subrogante) |
| 6 | **cargo como sujeto sin nombre**: «El Gerente de División Política Financiera manifiesta…» | corte 2960 | **1** | **0** (misma Recart: su `Rol_Final` es «Ministro de Hacienda (S)», el `(S)` es Subrogante) |
| 7 | variantes de traspaso: `invita a`, `cede`, `otorga`, `corresponde la palabra a`, `a cargo de` | — | 708 → 3 con ≥400 ch | **0** («invita **a los países** influyentes», «da paso **a una reacción de la oferta**», y `747:1` donde Corbo continúa él mismo) |

**Cinco cortes, cinco aplicados. No queda ninguno pendiente.**

Las firmas 5 y 6 no se habían probado nunca, y son las que abren dos de los cuatro cortes
originales. Se probaron ahora y están agotadas: cada una dio un solo candidato en todo el corpus y
los dos son el propio actor con el nombre o el cargo escrito distinto.

### La única firma que ningún patrón puede encontrar

El corte 657 abre **sin sujeto**: «A continuación el señor Presidente ofrece la palabra a don Sergio
Lehmann Beresi, para que inicie la exposición. / Respecto al crecimiento mundial, la situación de
China…». Eso sólo se ve leyendo. Pero sólo puede ocurrir inmediatamente después de un traspaso, y
los traspasos con texto sustancial después están agotados (firma 3 y 7): con ≥1.500 caracteres
después no queda **ninguno** en las 5.823 filas de un solo segmento.

### Estado

**9.725 filas · 5 cortes aplicados · ninguna firma con candidatos pendientes.** Se puede seguir con
la próxima acta.

---

## §50. Sesión 2008-06-10: las siete firmas dentro del auditor

El censo del §49 se hizo con scripts ad hoc. Desde esta sesión las siete firmas viven en
`scripts/analisis_sesion.py` —la 2 en la sección **2b** y las otras cinco en la **2c**—, así que
**toda acta pasa por las siete antes de cerrarse**, no sólo por la cola del lote10.

La sección 2c incorpora además el filtro que faltaba y que había producido falsos positivos: el
propio actor escrito de tres maneras distintas —apellido dañado por OCR, cargo en vez de nombre, y
**cargo con abreviatura** («Ministro de Hacienda (S)» es la Ministra Subrogante).

### Resultado

| red | candidatos | cortes |
|---|---|---|
| cola lote10 | 1 (padre 1858) | **0** — ya está partido en 4 segmentos en la base |
| 2b — segunda voz por verbo de habla | 0 | 0 |
| 2c — las otras cinco firmas | 0 | 0 |

**Ningún corte que hacer.** No es ausencia de avisos: son tres redes corridas y vacías.

### OCR

Los **14 candidatos de acento en 12 filas** son todos formas correctas:

| forma | n | por qué se conserva |
|---|---|---|
| `hacía` | 2 | verbo: «como ya se **hacía** mención», «a que se **hacía** referencia» |
| `frenó` · `promedió` · `cambió` | 3 | verbos en pasado: «el consumo se **frenó**», «se estima que **promedió** 89,8%», «cuando se **cambió** la jornada» |
| `cuánto` | 6 | interrogativo indirecto: «información de **cuánto** puede estar liderando» |
| `éstos` | 3 | pronombre demostrativo; el corpus lo usa consistente (137 apariciones) |

**Dos correcciones, ambas residuos de OCR al final de fila**, únicos en el corpus y después de una
oración completa:

| fila | antes | tipo |
|---|---|---|
| `1860:2` | «…durante este año. **'V/**» | `SIMBOLO_SUELTO` |
| `1858:1` | «…en todos lados. **.LI I**» | `SIMBOLO_SUELTO` |

El segundo es un marcador de línea o página del PDF: la fila siguiente (`1858:2`) empieza con la
continuación normal de la exposición, así que no se pierde texto.

Registro: **1.559 filas / 2.587 operaciones**. `Texto` intacto en las 9.725.

---

## §51. Sesión 2010-11-16 + pase transversal de la comilla del Comunicado

108 filas, 12 actores. **Ninguna fila en la cola y cero candidatos en 2b y 2c**: las siete firmas
corrieron y no hay ningún corte que hacer. Los 3 candidatos de acento son verbos en pasado
(`incrementó`, `frenó`) y un interrogativo indirecto (`cuánto`).

### Lo que sí apareció: la comilla del Comunicado, esta vez bien medida

La fila `3581:1` termina en comilla de cierre **sin apertura**. El §45 había mirado esta familia y la
descartó — pero midió la distancia **desde «Acuerdo:»**, que va de 148 a 2.009 caracteres, y contó
filas **sin** comilla. La medición que faltaba era otra:

> ¿Qué signo sigue **inmediatamente** a la palabra «Comunicado»?

| signo | filas |
|---|---|
| `“` | **102** |
| `'` comilla recta | 2 |
| `‘` comilla simple izquierda | 1 |
| `‘‘` dos comillas simples izquierdas | 1 |

Sobre las 113 filas de Acuerdo con sección Comunicado. **La posición es fija** —inmediatamente
después de la palabra— y en los cuatro casos divergentes **hay un signo, no una ausencia**: no hay
duda de que ahí va la comilla, sólo está mal leída. Lo corrobora que esas filas traen la comilla de
**cierre** intacta y sin pareja (`“=0, ”=1` en 5 filas de Acuerdo).

### Por qué esto sí y el §45 no

| | §45 (descartado) | §51 (aplicado) |
|---|---|---|
| qué se medía | distancia desde «Acuerdo:» | signo tras «Comunicado» |
| posición | variable, 148 a 2.009 ch | **fija** |
| proporción | 61 con / 52 sin | **102 contra 4** |
| ¿hay signo? | en 52 filas **no hay nada** | en las 4 **sí hay**, mal leído |
| formas alternativas | 4 (recta, simple, doble simple, ausencia) | **ninguna plausible** |

La diferencia decisiva no es la proporción: es que **aquí no hay ausencia**. Reconstruir una comilla
que falta exige saber si el original la tenía; reemplazar un glifo mal leído en una posición fija, no.

### Las 4 correcciones (pase transversal, 4 actas)

| fila | antes | después |
|---|---|---|
| `2006-05-11:674:2` | `Comunicado ' En su reunión` | `Comunicado “ En su reunión` |
| `2009-06-16:2602:1` | `Comunicado 'En su reunión` | `Comunicado “En su reunión` |
| `2010-11-16:3581:1` | `Comunicado ‘En su reunión` | `Comunicado “En su reunión` |
| `2013-01-17:5330:3` | `Comunicado ‘‘En su reunión` | `Comunicado “En su reunión` |

Verificado después de aplicar: las **106** apariciones de «Comunicado» seguido de comilla usan `“`,
cero dañadas. Registro: **1.560 filas / 2.591 operaciones**. `Texto` intacto en las 9.725.

---

## §52. Sesión 2010-07-15 + segunda variante de «Tasa» deletreada

103 filas, 13 actores. **Ninguna fila en la cola**; la red 2b dio 2 candidatos que son el propio
actor con el apellido dañado por OCR («José De **Gregario**») y la 2c dio cero. Siete firmas
corridas, **ningún corte**. Los 2 candidatos de acento son verbos («el INE no los **publica**», «el
proceso… que se **inició**»).

### El hallazgo: otra variante del mismo defecto

La fila `3277:1` trae `157-01-100715 -T a s a de Política Monetaria`. El §36 ya había corregido la
variante `T a sa` en 6 actas; ésta es la variante con **las cuatro letras separadas**. Medido:

| forma | apariciones |
|---|---|
| `-Tasa de Política` (bien) | **119** |
| `T a s a` | **9** |

Siempre en la misma posición de la fórmula («el Consejo adopta el siguiente Acuerdo:
<número>-Tasa de Política Monetaria»), y el número de acuerdo va pegado a la palabra: no hay lectura
alternativa.

### Las 9 correcciones (pase transversal, 9 actas)

`2005-07-12:310:3` · `2006-03-16:625:1` · `2007-11-13:1569:1` · `2008-09-04:2099:1` ·
`2008-10-09:2127:1` · `2008-11-13:2173:1` · `2009-03-12:2438:2` · `2010-05-13:3126:2` ·
`2010-07-15:3277:1` — todas `T a s a` → `Tasa`, tipo `PALABRA_PARTIDA`.

Verificado después: `T a s a` = **0** en la salida (20 en el `Texto` virgen, que incluyen las del
§36) y `-Tasa de Política` = **128**, exactamente 119 + 9.

### Lo que esto dice sobre los pases transversales

El §36 corrigió 6 actas y dio el tema por cerrado. Nueve sesiones después aparece la **misma**
palabra dañada de otra manera. Un pase transversal no cierra una familia: cierra **la variante que se
midió**. Conviene, al cerrar una, dejar escrita la forma de buscar las otras — aquí, cualquier
secuencia `T\s+a\s+s?a?` dentro de la fórmula del Acuerdo.

Registro: **1.564 filas / 2.600 operaciones**. `Texto` intacto en las 9.725.

---

## §53. Sesión 2011-07-14: `solícita` + cuatro defectos más en la fórmula del Acuerdo

103 filas, 13 actores. **Ninguna fila en la cola**, 2b = 0, 2c = 0: siete firmas corridas, **ningún
corte**. De los 3 candidatos de acento, dos son verbos (`cambió`, `impactó`) y uno era daño real:

> «El Consejero señor Sebastián Claro **solícita** que se explique el gráfico de la izquierda…»

La construcción `solícita que + subjuntivo` sólo admite el verbo, que va **sin** tilde; con tilde es
el adjetivo. Medido: **2** apariciones contra **217** de `solicita`, y `solícito` no aparece nunca,
así que el adjetivo no se usa en este corpus y no hay ambigüedad. Se corrigieron las dos (la otra en
`2014-01-16:5972:1`).

Las 2 comillas rectas de `4203:1` son el posesivo inglés **`Moody's`** y se conservan — misma familia
que `Lloyd's` y `Purchasing Managers' Index`.

### Revisar la fórmula completa, no sólo la variante que se midió

El §52 dejó escrita la lección: un pase transversal cierra **la variante medida**, no la familia.
Aplicada aquí — se revisó la fórmula del Acuerdo entera y salieron cuatro defectos que ningún
detector había propuesto:

| defecto | casos | contra | corrección |
|---|---|---|---|
| `Tasade` sin espacio | 1 | 1.521 `Tasa de` | `Tasa de` |
| `Tasa de Política monetaria` (minúscula en nombre propio) | 3 | 1.441 | `Monetaria` |
| `Informe de Política monetaria` (idem, IPoM) | 1 | 397 | `Monetaria` |
| raya `–` en vez de guion en el número de acuerdo | 2 | 129 | `-` |

Los 7 casos están en **7 actas distintas**: `2005-04-07:207:9` · `2005-11-10:503:2` ·
`2006-05-11:660:2` · `2007-05-10:1232:1` · `2012-01-12:4572:1` · `2012-02-14:4654:1` ·
`2012-03-15:4731:1`.

### Lo que se dejó, a propósito

- **`2009-05-07:2525:1`**: «…hay elementos que se suman. **Política monetaria**; baja generalizada de
  lo que los bancos cobran…; y tercero, que el ahorro…». Es un **rótulo de lista** del Ministro, no
  el nombre de la TPM. Se deja.
- **`política monetaria`** todo en minúscula, de uso común («la normalización de la política
  monetaria continúe»). Es correcto.

Una búsqueda sin distinguir mayúsculas habría arrastrado las dos; por eso la medición se hizo sobre
el `Texto` virgen y con la distinción activa.

### Un tramo ya ocupado: extender, no apilar

En `2005-11-10:503:2` la minúscula cae **dentro** del tramo que ya posee la operación del pase del
§36 (`051110-T a sa de Política monetaria`). Se extendió esa operación con `enmendar_operacion.py`
(`Despues` → `051110-Tasa de Política Monetaria`) y su justificación nombra los dos defectos, como
mandan el §15 y el §43. Apilar una segunda operación habría abortado el lote entero.

### Verificado

`Política monetaria` 5 → **1** (queda sólo el rótulo de lista) · `Tasade` 1 → **0** · rayas 2 → **0**
· `T a s a`/`T a sa` 16 → **0** · fórmula correcta 110 → **131** · `Texto` intacto en las 9.725.

Registro: **1.568 filas / 2.608 operaciones**.

---

## §54. Sesión 2011-05-12 + pase transversal de la hora con coma (18 casos, 11 actas)

102 filas, 11 actores. La cola daba un caso (padre 4054) **ya partido en tres segmentos**; 2b = 0 y
2c = 0. Siete firmas corridas, **ningún corte**. Los 6 candidatos de acento son cuatro verbos
(`cambió`, `hacía`, `incrementó`, `argumentó`) y dos interrogativos indirectos (`cuánto`). **Cero
correcciones locales.**

### La segunda fórmula fija que se revisó: la hora

El §53 dejó el método — revisar la fórmula completa, no la variante medida. Aplicado a la fórmula de
la hora:

| forma | apariciones |
|---|---|
| `HH:MM horas` | **551** |
| `HH,MM horas` | **18** |

Las 18 están en **17 filas y 11 actas** distintas, y todas en contexto horario inequívoco:

```
…a 11 de enero de 2005, siendo las 11,30 horas, se reúne el Consejo…
…el Presidente, señor Vittorio Corbo, suspende la Sesión a las 12,50 horas…
…e informa que la misma se reanudará a las 16,00 horas.
…aprueba el texto del Comunicado. Se levanta la Sesión a las 17,00 horas.
…a otros precios.” 17,00 horas. El Consejo aprueba el texto…
```

No son decimales: son horas y minutos. Es la **misma familia** que las 7 correcciones ya registradas
del punto y coma (`16;55 horas` → `16:55 horas`, tipo `PUNTUACION`), así que se usó el mismo tipo.

### Lo que no se toca

Los **rangos con guion** son otra cosa y quedaron intactos: `46-50 horas` (`2005-03-10:151:1`) y
`0-45 horas` (`2005-04-07:207:9`) — 2 antes, 2 después.

### Un ancla recortada

En `2005-03-10:140:1` el tramo `11,30 horas` choca con una operación ya registrada que **empieza
justo en « horas»** (`' horas, se reúne el C onsejo…'`, del pase de palabras partidas). Dos tramos
solapados sobre el mismo texto virgen no se pueden aplicar en ningún orden, así que en vez de apilar
**se recortó el ancla** a `11,30` → `11:30`. El generador de lotes ahora recorta por la derecha
cuando el tramo siguiente está ocupado; antes abortaba.

### Verificado

coma 18 → **0** · dos puntos 544 → **569** (= 544 + 18 de coma + 7 de punto y coma ya registradas) ·
rangos con guion 2 → **2** · `Texto` intacto en las 9.725.

Registro: **1.579 filas / 2.626 operaciones**.

---

## §55 — Sesión 2010-06-15: tres familias de puntuación y cinco de nombres

Cien filas, doce actores. Los dos casos de la cola ya estaban partidos en la base (3147 en
tres segmentos, 3158 en dos). Las siete firmas del censo del §49 corrieron en cero, y un
barrido independiente sobre los doce actores de la sesión buscando «otro actor de la sesión
seguido de un verbo de habla» dio dos candidatos, ambos falsos: «el señor Gerente añade» en
`3130:1` es el propio Sergio Lehmann, que **es** el Gerente de Análisis Internacional, y «el
señor Vicepresidente manifiesta» en `3187:2` ya ocupa su propio segmento entre dos
intervenciones de De Gregorio. Los siete traspasos de palabra están todos en filas cortas del
Presidente y las seis filas de más de 3.800 caracteres son monólogos de un solo Consejero.
**Ningún corte.** Los tres candidatos de acento son correctos (`dónde` interrogativo
indirecto, `inició` pretérito, `seria` adjetivo).

### El cierre del §45 dejó abierta su propia familia

Al leer `3200:1` apareció «Continuando con la votación**,.**». El §45 ya había medido y
corregido «A continuación,.» — 76 casos — pero midió la **palabra**, no el **patrón**. Medido
sobre el texto corregido, `«<palabra>,.»` aparecía todavía **20** veces:

| forma | casos |
|---|---|
| `Continuando con la votación,.` | 6 |
| `Para concluir con la votación,.` | 3 |
| `No habiendo más comentarios,.` | 8 |
| `No habiendo más comentarios y preguntas,.` | 2 |
| `…señor Manuel Marfán,.` | 1 |

En los veinte la fila siguiente empieza con «el Presidente…», «el Consejero…» o «el
Vicepresidente…», así que la coma es la marca correcta y el punto el signo sobrante — el mismo
criterio del §45. **20 ops.**

Barrido simultáneo del resto del patrón:

- **`.,` — 24 casos, de los cuales 20 son legítimos**: abreviaturas (`EE.UU.`, `S.A.`, `etc.`,
  `v.gr.`) e iniciales de nombre («Velasco B.,»). El discriminador es qué precede al punto: una
  palabra completa en minúscula de cuatro letras o más, o un signo de porcentaje, no una
  abreviatura. Así salen 4 defectos (`América.,` `6,25%.,` `importante.,` `Brothers.,`). **4 ops.**
- **`..` — 4 casos en el virgen**, uno ya cubierto por otra operación (`2006-01-12:562:1`),
  siempre al cierre de una oración seguida de otra que empieza en mayúscula. **3 ops.**

Verificado: `,.` 98 → **0** · `.,` espurio 4 → **0** · `..` 4 → **0** · las 20 abreviaturas
legítimas intactas.

### Cinco familias de nombres dañados

Aplicando la instrucción de normalizar los nombres dañados, la lectura de esta sesión destapó
cinco familias que ninguna red anterior cubría:

| familia | virgen | corregido | medida |
|---|---|---|---|
| `De Gregario` → `De Gregorio` | 41 | **0** | 1.150 contra 41, misma persona |
| `Lehman` (persona) → `Lehmann` | 5 | **0** | 1.904 contra 5 |
| `Lehman Sros.` → `Lehman Brothers` | 1 | **0** | grafía única en el corpus |
| `Garda` → `García` | 2 | **0** | 737 contra 1 |
| `Beam Stearns` → `Bear Stearns` | 5 | **0** | 1 contra 5, ver abajo |

**El banco y la persona se separan por el contexto, no por la frecuencia.** «Lehman» sin la ene
final aparece 24 veces, pero 19 son el banco de inversión Lehman Brothers, cuyo nombre correcto
lleva una sola ene. Las 5 que se corrigieron son la persona, siempre precedidas de «señor» o
«Gerente señor». Un pase por frecuencia habría destruido el nombre del banco.

**`Beam Stearns` es el primer caso en que la forma canónica es minoritaria.** El corpus tiene
`Beam Stearns` 5 veces y `Bear Stearns` 1, de modo que la regla numérica del §34 —la forma
canónica debe superar a la dañada— no se cumple. Se corrigió de todos modos porque la entidad
es única e inequívoca, el corpus atestigua la forma correcta aunque sea una vez, y los cinco
contextos son explícitos («cuando alrededor de julio del año 2008», «en el momento en que
quebró», «la crisis de»). La erre por la eme es una confusión clásica de OCR. La justificación
de cada operación deja constancia de que la decisión no descansa en la frecuencia.

**`Lehman Bros.` fue rechazado por el guardia de vocabulario.** El registro no permite
introducir una palabra ausente del corpus ni de `TERMINOS_FORANEOS`, y `Bros` no está en
ninguno de los dos. Se enmendó a `Lehman Brothers`, que es además la forma que el propio
corpus usa 14 veces. **El guardia tiene razón y su rechazo es información**: obliga a
normalizar hacia una forma atestiguada en vez de hacia la que uno recuerda.

### Una ancla extendida a mano

En `2009-02-12:2356:2` el «De Gregario» cae en 25–36 y una operación ya registrada empieza en
28: se solapan en ocho caracteres. No hay tramo que corrija el apellido sin invadir el tramo
ajeno, y `enmendar_operacion.py` no puede cambiar el `Antes` porque es lo que ancla la
operación al texto virgen. Se extendió la operación existente a mano —`Gregario, frente al
planteam iento…` → `De Gregario, frente al planteam iento…`— y `--validar` confirmó unicidad y
ausencia de solape. **Cuando el defecto cae dentro de un tramo propio y el ancla no alcanza,
la salida es extender el ancla, no apilar ni abandonar.**

### Verificado

`De Gregario` 41 → **0** (`De Gregorio` 1.150 → 1.191) · `Lehman` persona 5 → **0** ·
`Lehman Brothers` 14 → **15** · `Garda` 2 → **0** · `Beam Stearns` 5 → **0** (`Bear Stearns`
1 → 6) · `Sros` 1 → **0** · `Texto` intacto en las 9.725.

Registro: **1.627 filas / 2.706 operaciones**.

### Una operación tiene que ser idempotente

`test_no_vuelve_a_corregir_sobre_lo_corregido` falló al aplicar el lote: en `2005-05-12:232:1`
la segunda pasada producía `Lehmannn`. La causa es estructural, no un error de tipeo: cuando el
`Antes` es **subcadena** del `Despues`, el texto ya corregido sigue conteniendo el `Antes` y la
operación se vuelve a aplicar. Con `Antes='Lehman'` y `Despues='Lehmann'`, `'Lehmann'` contiene
`'Lehman'` en la posición 0, así que el reemplazo da `'Lehmannn'`.

El generador de anclas las extiende sólo cuando no son únicas en la fila; cuando la palabra
aparece una sola vez devuelve la palabra desnuda, y ahí es donde cae la trampa. Se escaneó el
registro entero por la propiedad `Antes in Despues`: **3 operaciones** la tenían, las tres del
mismo lote, y las tres se arreglaron extendiendo el ancla un carácter a la derecha —`Lehman,` →
`Lehmann,` y `Lehman ` → `Lehmann `— con lo que el `Antes` deja de ser subcadena del `Despues`.

**Regla: al generar un lote, verificar que `Antes` no sea subcadena de `Despues` en ninguna
operación.** Es una condición barata de comprobar y el único guardia que la detecta corre
después, en la suite.

---

## §56 — Sesión 2009-06-16: cuatro familias, 162 operaciones

Noventa y nueve filas, trece actores. Los cuatro casos de la cola ya estaban partidos en la
base —el padre 2555 en 5 segmentos, 2566 en 5, 2576 en 3 y 2583 en 6— y los cortes caen
exactamente donde caerían por lectura. Las siete firmas del §49 en cero y un barrido
independiente sobre los trece actores buscando «otro actor seguido de verbo de habla» dio cero
candidatos. Los seis traspasos de palabra están en filas cortas del Presidente. **Ningún
corte.** Las once filas de más de 1.900 caracteres se leyeron: `2593:2` (8.683 ch) es un
monólogo de Pablo García de punta a cabo, `2598:1` (8.652) de Marshall, `2594:1` (5.338) de
Céspedes —el único invitado— y las demás son votos de un solo Consejero.

### El punto donde va una coma

Al leer `2594:1` apareció «Indica que**.** asumiendo un crecimiento anual…». Medido en todo el
corpus, un punto seguido de espacio y de una palabra en minúscula aparece **109** veces. En
español una oración no empieza en minúscula, así que el signo no puede ser de cierre — pero la
familia es heterogénea y hubo que separarla:

| grupo | casos | tratamiento |
|---|---|---|
| abreviaturas legítimas (`EE.UU.` 10, `hrs.` 6, `pp.` 1, `pb.` 1) | 18 | **no se tocan** |
| basura de OCR tras el punto (`if`, `fi`, `kt`, `ry`, `lf`) | 5 | otro defecto |
| palabras sueltas de margen y encabezados residuales (`votación` 4, `interno` 3, `comentarios`, `mencionada`, `caso`, `internamente`) | 10 | otro defecto |
| la oración continúa en minúscula | **91** | punto → coma |

De los 91, uno no admite coma sino supresión: «esto se refleja en**.** el predominio de bajas
tasas», donde la palabra siguiente completa la misma frase.

**Verificado: 91 → 0**, con `EE.UU.` (26) y `hrs.` (6) intactos.

### Las otras tres familias

| familia | virgen → corregido | medida |
|---|---|---|
| `IPOM` → `IPoM` | 58 → **0** | 2.473 contra 58, siempre el mismo documento |
| `desafio` → `desafío` | 3 → **0** | 40 contra 3 |
| `cambiaba` → `cambiaria` | 2 de 4 | 229 contra 4 |
| barra invertida suelta ` \ ` | 11 → **0** | residuo de salto de línea del PDF |

**`cambiaba` exigió leer los cuatro casos.** Es una palabra legítima del español —pretérito
imperfecto de cambiar— y dos de las cuatro apariciones lo son («la cual no cambiaba con la
información disponible», «no cambiaba en general los contornos»). Sólo se corrigieron las dos
que van sustantivadas: «una intervención cambiaba», «una apreciación cambiaba». **Un pase por
frecuencia habría convertido dos verbos correctos en adjetivos.**

### Una corrección puede destapar el defecto de al lado

Cinco de los 91 puntos quedaron dentro del tramo de operaciones ya registradas, que arreglaban
otro defecto del mismo tramo y no tocaban el signo: `abiertas. índica` → `abiertas. indica`
(arregló el acento), `Federales . Agrega. q` → `Federales. Agrega. q` (arregló el espacio),
`s de forma aislada. podrian` → `… aislada. podrían` (arregló el acento). Y una sexta,
`de crédito. i/ pero sí` → `de crédito. pero sí`, **destapó** un punto que la basura de OCR
tapaba.

Las cinco se resolvieron enmendando el `Despues` de la operación existente —que es justo lo que
`enmendar_operacion.py` hace— y la sexta con una operación nueva, porque su tramo sí estaba
libre. **Verificar una familia sobre la salida corregida y no sobre el plan es lo que las hizo
aparecer: el plan decía 91 aplicadas, la salida mostraba 6 vivas.**

### Verificado

punto+minúscula aplicable 91 → **0** · `IPOM` 58 → **0** · `desafio` 3 → **0** · `cambiaba`
4 → **2** (los dos verbos legítimos) · barra suelta 11 → **0** · `EE.UU.` 26 y `hrs.` 6
intactos · `Texto` idéntico a la base en las 9.725 · **0 operaciones no idempotentes** en todo
el registro (la propiedad del §55, reescaneada).

Registro: **1.704 filas / 2.863 operaciones**.

### Enmendar el `Despues` puede obligar a enmendar también el `Tipo`

`test_las_operaciones_de_espacio_solo_quitan_espacios` falló al aplicar las cinco enmiendas. La
causa: la operación de `2008-02-07:1654:1` está tipada `ESPACIO_INDEBIDO`, y ese tipo tiene una
propiedad que la suite exige —quitando los blancos, `Antes` y `Despues` deben coincidir—. Al
cambiar `Agrega.` por `Agrega,` dentro de su `Despues`, la operación pasó a tocar un signo y
rompió la propiedad.

El arreglo no es relajar el test sino **retipar la operación a `PUNTUACION`**, que es
exactamente el caso que justifica la existencia de `enmendar_operacion.py`: «quitar un espacio
indebido y descubrir después que el signo también sobraba ya no es `ESPACIO_INDEBIDO`». El
cambio de signo es el arreglo sustantivo.

**Regla: al enmendar un `Despues`, comprobar que el `Tipo` sigue describiendo lo que la
operación hace.**

---

## §57 — Sesión 2012-03-15: la fórmula del encabezado y un barrido de acentos sin umbral

Noventa y ocho filas, catorce actores. El único caso de la cola es una **mención**, no una
intervención: el Presidente deja constancia de que el Ministro de Hacienda le informó que no
asistirá. Las siete firmas del §49 en cero y un barrido independiente sobre los catorce actores
en cero; `RESPONDE` y `CARGO_SUJETO` disparan una vez, sobre `4719:5`, que es el propio actor
de la fila. Los nueve traspasos están en filas cortas del Presidente. **Ningún corte.** Se
leyeron las catorce filas de más de 1.900 caracteres: `4721:1` (7.810 ch) es un monólogo de
Luis Óscar Herrera, y `4722:3` (6.828) es **la opinión por escrito del Ministro de Hacienda que
el Presidente lee en voz alta** —la atribución al Ministro es correcta aunque no haya asistido,
porque el autor del texto es él.

### El encabezado de acta es una fórmula fija

El detector de acentos de la sesión no encontró nada aplicable, así que se corrió un barrido
propio sobre **todo el corpus**: toda palabra acentuada cuya forma sin acento sea al menos
veinte veces más frecuente, **sin umbral mínimo de frecuencia** (el detector de la sesión usa
20 y por eso se le escapó `sustentabílidad`, cuya contraparte aparece 11 veces). Salieron 66
candidatos y **la mayoría son falsos**: verbos en pretérito (`Aumentó`, `tornó`, `impactó`,
`promedió`, `votó`, `impulsó`, `trabajó`, `retiró`, `motivó`, `pagó`…) y formas legítimas de la
época (`Éste`, `Ésta`, `Sólo`, `Sí`, `Cuánto`, `quiénes`).

Lo que sí apareció es una **fórmula fija**. El encabezado de todas las actas dice «ACTA
CORRESPONDIENTE A LA SESIÓN DE POLÍTICA MONETARIA N° …», y sus variantes:

| forma | casos |
|---|---|
| `SESIÓN` correcta | 115 |
| `SESION` sin acento | 14 |
| `SESiÓN` con i minúscula | 2 |
| `POLÍTICA` correcta | 111 |
| `POLITICA` sin acento | 16 |
| `POLíTICA` / `POLiTICA` | 4 |

**36 operaciones.** La fórmula completa correcta aparece 111 veces contra 14 sin acentos: al
ser el mismo encabezado en todas las actas, la forma canónica no admite duda.

### Los otros casos, uno por uno

`Asía`→`Asia` 3 (327) · `Líbor`→`Libor` 1 (101) · `Arabía`→`Arabia` 1 (28) · `cúal`→`cuál` 1
(246, acento en la vocal equivocada) · `varías`→`varias` 1 (205) · `estás cifras`→`estas` 1
(1.266) · `Sín embargo`→`Sin` 1 (2.280) · `Ruíz-Tagle`→`Ruiz-Tagle` 1 (54) ·
`crédit crunch`→`credit crunch` 1 (10) · `sustentabílidad`→`sustentabilidad` 1 (11) ·
`efectos e la crisis`→`de la crisis` 1 · `a n á lisis`→`análisis` 1 (854) ·
`e.n Ií ~ea`→`en línea` 1 · residuo `' í \ : Ai`→`Al` 1 · basura final `í j .` 1.

**Tres decisiones que no se resolvieron por frecuencia:**

- **`Seníor`.** El corpus está empatado: `Sénior` 79 y `Senior` 77. No decide la frecuencia
  sino **la propia fila**, que usa `Senior` en el cargo siguiente de la misma lista de
  asistentes. `Seníor` es incorrecta en cualquiera de las dos lecturas.
- **`vis-é-vis`.** La grafía correcta `vis-à-vis` **no aparece ninguna vez** en el corpus y la
  `à` no está en el repertorio ni en `TERMINOS_FORANEOS`, así que el guardia de vocabulario la
  rechazaría. El corpus sí atestigua `vis a vis` 8 veces: se normalizó a eso.
- **`y í condiciones crediticias`** (`2007-08-09:1357:1`). La í acentuada ocupa el lugar de una
  palabra entera y el corpus admite «y a condiciones», «y unas condiciones» o «y en
  condiciones». **No se corrigió**: se dejó la marca `RECONSTRUCCION_AMBIGUA_POR_COTEJAR`
  (marca 8 del registro, 215 filas marcadas).

### Dos defectos escondidos detrás de otro

`ígal Magendzo` no se corrigió con el lote porque **el apellido también estaba dañado**: el
virgen dice `ígal Madgenzo`, y una operación previa ya arreglaba el apellido, así que el ancla
nueva no casaba con nada. Se extendió el `Despues` de esa operación. Y el residuo
`commodities. ' í \ : Ai proseguir` tenía la barra invertida ya ocupada por una operación del
§56: corregir sólo la barra dejaba `' í : Ai`, así que se extendió el ancla a todo el residuo.

**Regla: cuando un tramo tiene dos defectos y uno ya tiene operación, el segundo se resuelve
extendiendo esa operación, no registrando otra.**

### Verificado

`SESION` 14 → **0** · `SESiÓN` 2 → **0** · `POLITICA` 16 → **0** · `POLíTICA`/`POLiTICA` 4 →
**0** · fórmula correcta 111 → **131** · los 17 casos sueltos → **0** · `ígal` 1 → **0**
(`Igal` 131 → 132) · `Texto` idéntico a la base en las 9.725 · **0 operaciones no
idempotentes**.

Registro: **1.714 filas / 2.916 operaciones / 215 filas marcadas**.

## §58 — Sesión 2008-07-10: dos cortes de la firma 4, entrega v10 y la familia del apóstrofo

Noventa y seis filas, doce actores, 108.277 caracteres. **Dos cortes reales**, los primeros
desde el §48, y los dos con la misma firma: un tercero responde dentro de una fila atribuida a
otro. Es la firma 4 del censo del §49, la única que hasta ahora había producido un corte (padre
1706).

### Los dos cortes

**Padre 1924** (404 ch, actor Andrés Velasco Brañes):

> «El señor Ministro de Hacienda **consulta** a qué período se considera largo plazo. **El señor
> Gerente señala** que no hay consenso respecto del largo plazo…»

Una consulta y su respuesta no pueden ser del mismo hablante: nadie se consulta a sí mismo y se
contesta en tercera persona. Corte en el carácter 79, nuevo hablante **Sergio Lehmann Beresi**.
Agrega la fila `1924:2`.

**Padre 1925** (2.582 ch, actor Jorge Desormeaux Jiménez):

> «El Vicepresidente señor Jorge Desormeaux **acota** que en el mercado futuro del petróleo, el
> plazo más largo que existe es a siete años. **El señor Gerente comenta** que esos son
> planteamientos de largo plazo que dan los propios bancos de inversiones…»

Misma firma. Corte en el carácter 133. El constructor ya partía este padre en tres, pero ponía
la frontera en 243 y dejaba la réplica del Gerente dentro del segmento del Vicepresidente. Con la
revisión la frontera pasa a 132 y las dos intervenciones contiguas de Lehmann se fusionan: **no
agrega fila**, sólo mueve el límite.

**Que el Gerente sea Lehmann no se infiere del cargo, se lee.** En esta sesión su presentación del
escenario externo abre en 1916, el Presidente le ofrece la palabra en 1915 y la retoma en 1923:3
(«El Gerente de Análisis Internacional continúa su presentación»), y en el padre 1925 el acta lo
nombra explícitamente dos oraciones más abajo: «comenta **el Gerente señor Sergio Lehmann**».

Los dos cortes se registraron en `revisiones_hablantes_lote10.json` (entradas 6 y 7) y se publicó
**`continuidad_procedimental_v10`** con gate propio (`compare_procedural_v10.py`, baseline v9
`32752bd5…`):

| | |
|---|---|
| Perfil | `procedimental-v10`, baseline `procedimental-v9` |
| Filas | 9.725 → **9.726** |
| Filas nuevas | `RPM-2008-07-10:1924:2` |
| Padres resegmentados | 657, 1564, 1706, 1924, 1925, 1995, 2960 |
| Grupos | 9.236 → 9.237 |
| Alertas | 484 → 484 (ninguna se cerró) |
| Reservas | 780 (4) · 2661 (12) · 5252 (4), intactas |
| `Pasa` | **True** |

De los siete cortes del lote10, **sólo tres agregan una fila** (1995, 1706 y 1924); los otros
cuatro corrigen una frontera que el detector ya trazaba.

### El apóstrofo en lugar del espacio

Cuatro casos, ninguno con lectura alternativa:

| fila | virgen | corregido |
|---|---|---|
| `2006-08-10:817:1` | `denominados “elementos'tácticos”` | `elementos tácticos` |
| `2008-07-10:1916:2` | `No obstante, en'el caso de la Zona Euro` | `en el caso` |
| `2010-01-14:2847:1` | `por componentes el'f comportamiento` | `el comportamiento` |
| `2014-11-18:6486:1` | `BANCO CENT'RAL DE CHILE` | `BANCO CENTRAL DE CHILE` |

El cuarto es el encabezado de acta cuya fórmula fijó el §57; esa misma fila ya tenía corregida
`POLiTICA`.

### Un nombre dañado que no se puede normalizar: `L1oyd's`

`2008-10-09:2106:1` dice «al Banco **L1oyd's** inglés». El daño es evidente —un `1` en lugar de
una `l`— pero **la forma canónica no está atestiguada en el corpus**: `L1oyd` aparece 1 vez y
`Lloyd` 0. La regla del §34 sólo normaliza cuando el propio corpus atestigua la forma canónica, y
además la guarda de vocabulario de `correcciones_ocr_v1.py` rechaza introducir una palabra que no
está en el corpus ni en `TERMINOS_FORANEOS`. Se registró la operación, la validación la rechazó y
**se revirtió**: el texto quedó intacto y la fila se marcó `NOMBRE_PROPIO_POR_COTEJAR` (marca 9).
En la misma fila sí se corrigió `Sanco`→`Banco`, que sí tiene forma canónica atestiguada.

**Regla: un daño evidente no basta para normalizar; hace falta que el corpus atestigüe la forma
de destino. Si no, se marca.**

### Lo que no se tocó

- **`periodo` sin tilde (33) contra `período` (303).** Las dos grafías son legítimas en español,
  así que esto es una variante y no un daño de OCR. Corregirlo sería una normalización de estilo,
  no una reparación. Se deja, como `seria`, `éstos` o `cuánto`.
- **Los apóstrofos de nombres propios extranjeros:** `Moody's`/`Moody’s`/`Moody´s`, `Standard &
  Poor's`/`Poor’s`, `Dell’Oro`, `People’s Bank of China`. Ocho formas distintas, 66 ocurrencias en
  52 filas, todas enumeradas en la prueba de regresión.

### Una trampa de medición, de nuevo

El primer barrido del apóstrofo se corrió sobre `Texto_Corregido` y encontró 6 filas. **Esa
columna está vacía en las filas sin corrección**, así que el barrido era ciego a 9.726 − 1.714
filas. Sobre el texto efectivo son 52. La prueba de regresión se escribió contra el texto
efectivo y devolvió las dos filas que faltaban (`2012-02-14:4652:1`, `2012-10-18:5096:1`), las dos
`Moody's` legítimos. **Regla repetida: medir siempre sobre el texto efectivo, nunca sobre la
columna de corrección.**

### Verificado

Los cuatro defectos → **0** en el texto efectivo · apóstrofos entre letras: 8 formas, 66
ocurrencias, todas nombres propios · `Texto` idéntico a la base en las **9.726** filas · 2.920
operaciones exportadas · suite local **59 OK** (18+24+6+11).

Registro: **1.714 filas / 2.920 operaciones / 212 revisiones / 215 filas marcadas** (la marca nueva
cayó sobre una fila que ya estaba marcada, por eso el total no sube).

## §59 — Sesión 2010-04-15 (abierta): `Claudia`/`Claudio`, y un corte al revés que el motor no puede deshacer

Noventa y tres filas, once actores, 89.149 caracteres. Cola en cero, 2b en cero, 2c en cero,
detectores de palabra partida en cero. **La sesión no está cerrada**: apareció un caso que el
mecanismo del lote10 no puede resolver y quedó abierto más abajo.

### Una atribución invertida: el padre 3062

El barrido independiente sobre los once actores dio 15 referencias ajenas; catorce son el propio
actor de la fila referido por su cargo («el señor Presidente» en filas de De Gregorio, «el
Gerente de Análisis Macroeconómico» en filas de Soto, «el Consejero aludido» en filas de Claro).
La decimoquinta no:

> `3062:1` Soto: «El señor Claudio Soto informa luego que las tasas de colocación… Precisa que no
> es el caso de las tasas hipotecarias…»
> **`3062:2` Marfán**: «Respecto de la dispersión de las tasas, **sobre lo cual consultó el señor
> Vicepresidente en la Reunión pasada**, menciona que las medidas de dispersión se han mantenido
> más bien altas…»
> `3062:3` Soto: «A continuación, el señor Claudio Soto indica que los resultados de la Encuesta…»

Los 325 caracteres del medio son de **Soto**, no de Marfán. «Sobre lo cual consultó el señor
Vicepresidente **en la Reunión pasada**» es una subordinada relativa que remite a una reunión
anterior, y el verbo principal de la oración es «menciona» en presente, cuyo sujeto es el mismo
narrador de las oraciones vecinas. El detector leyó «el señor Vicepresidente» + «consultó» y
partió ahí.

**Es un corte al revés: la base separó donde no hay cambio de hablante y le atribuyó a Marfán
palabras que no dijo.** El padre fuente (839 ch, actor Claudio Soto Gamboa, sha256
`c2c79be12ccf06b9fca6e234376b3bd925a9d29cb00aa12499b0ee41f09a42f4`) es un solo discurso continuo.

**Por qué no se aplicó.** El registro del lote10 sólo puede *asignar* el hablante de la oración
que empieza en `Inicio`; las contiguas del mismo actor se fusionan después. Probado: una revisión
que cubra todo el padre (`Inicio=0`) devuelve los mismos 3 segmentos, porque la revisión sólo
toca la primera oración. Y al apuntarla a la oración del medio (`Inicio=282`, `Fin=608`) el
constructor aborta:

```
ValueError: Revisión contradice sujeto explícito     # build_base_referencia.py:1142
```

La guarda es correcta como mecanismo de seguridad —impide sobrescribir al detector en silencio—
pero aquí el detector se equivocó. Arreglarlo exige un cambio de código (un campo explícito por
entrada en el registro, apagado por defecto), no una regla general. **Queda abierto.**

### `Claudia` por `Claudio`: 30 casos, y el género es el discriminador

| forma | ocurrencias | |
|---|---|---|
| `Claudio Soto` | **1.275** | forma canónica |
| `señor/don Claudia Soto` | 27 | dañada |
| `señor Claudias Soto` | 1 | dañada (variante con una `s` de más) |
| `señor Claudios Soto` | 1 | dañada, ya corregida por una sesión anterior |
| `Claudio Raddatz` | **75** | forma canónica |
| `señor/don Claudia Raddatz` | 2 | dañada |
| `doña Claudia Varela Lértora` | 2 | **legítima** |
| `doña Claudia Sotz Pantoja` | 1 | **legítima** |

Lo que decide no es la frecuencia sino **el tratamiento que la propia fila usa**: «señor» y
«don» son masculinos, «doña» y «Gerenta» femeninos. Las dos Claudias legítimas son mujeres
distintas y ni `Claudio Varela` ni `Claudio Sotz` aparecen nunca en el corpus, así que ahí no hay
forma canónica que oponer y no se tocan. **30 operaciones**, `Claudio` 1.352 → **1.382**,
`Claudia` 32 → **3** (las tres de «doña»).

### Dos trampas, las dos ya conocidas y las dos repetidas

1. **Un defecto ocultó al segundo en la misma fila.** `2010-10-14:3454:1` tiene `Claudia Soto`
   en la primera línea y `Claudias Soto` en la 1.042. El lote buscaba `Claudia Soto` y lo
   encontró, así que la fila entró como corregida y la variante con `s` pasó inadvertida. La
   destapó la prueba de regresión, que cuenta **toda la familia `Claudi*`** y no sólo `Claudia`.
2. **Partir una operación en vez de apilar otra.** `2010-03-18:2990:1` ya tenía un
   `ESPACIO_INDEBIDO` cuyo `Antes` era `«s de junio . El señor Claudia Soto prosigue , mencionan»`:
   abarcaba los dos espacios **y** el nombre. No se puede cambiar una letra dentro de un
   `ESPACIO_INDEBIDO` porque la prueba exige que esas operaciones sólo quiten espacios. Se partió
   en tres operaciones disjuntas, cada una con su tipo correcto:
   `s de junio . El señor` / `Claudia Soto` / `prosigue , mencionan`.

### Verificado

`Claudi*` dañado → **0** · `Claudio` **1.382** · `Claudia` **3**, las tres con «doña» ·
`Texto` idéntico a la base en las **9.726** · suite local **60 OK** (18+25+6+11).

Registro: **1.719 filas / 2.946 operaciones / 212 revisiones / 215 filas marcadas**.

## §60 — El padre 3062 resuelto: `Fusiona_Intervencion_Revisada` y la entrega v11

El §59 dejó abierto el corte al revés del padre 3062 porque el mecanismo del lote10 no podía
resolverlo. Se resolvió con un campo nuevo en el registro, **optativo y apagado por defecto**, no
con una regla general.

### Por qué hacía falta un campo y no bastaba con la revisión

El registro del lote10 sólo puede *asignar* el hablante de la oración que empieza en `Inicio`. Con
eso se logran dos cosas: partir una fila (las oraciones siguientes de otro actor abren segmento) y
fusionar oraciones contiguas del mismo actor. Para el 3062 chocaba con dos obstáculos:

1. **La guarda.** `build_base_referencia.py` aborta con `Revisión contradice sujeto explícito`
   cuando la revisión asigna un actor distinto del sujeto explícito que encontró el detector. La
   guarda es correcta como mecanismo de seguridad: impide sobrescribir al detector en silencio.
2. **El límite.** Una revisión fuerza siempre un límite de segmento en su propio inicio, porque
   eso es lo que necesita un corte. Sin levantar también eso, el 3062 pasaba de 3 segmentos a 2
   —los dos de Soto, es decir la atribución corregida pero la intervención todavía partida.

Probado antes de escribir nada: con `Inicio=0` cubriendo todo el padre, `segment_turns` devolvía
los mismos 3 segmentos; con `Inicio=282` sin el campo, `ValueError`; con el campo pero sin levantar
el límite, 2 segmentos.

### El campo

```
"Fusiona_Intervencion_Revisada": true,
"Motivo_Sujeto_Explicito": "…por qué el nombre que el detector toma por sujeto no lo es…"
```

`curation.py` lo valida (debe ser `true` o no estar, y exige un motivo de al menos 40 caracteres).
Hace exactamente dos cosas y nada más: levanta la guarda para esa entrada y no fuerza límite de
segmento en su inicio. Como es optativo, **las siete revisiones anteriores no cambian de
comportamiento**. El validador F1 (`validate_speaker_reviews`) tuvo que aprender el caso: en una
fusión el intervalo no llega a ser un segmento propio sino que queda contenido en uno mayor que
conserva el método del detector, así que la comprobación pasa de «la fila empieza con la cita» a
«una única fila del padre contiene el intervalo completo con el actor del registro».

### Resultado

Padre 3062: **3 segmentos → 1**, los 839 caracteres en Claudio Soto Gamboa, y el texto reconstruido
idéntico al fuente. Entrega **v11** publicada con gate propio (`compare_procedural_v11.py`,
baseline v10 `e8b39e7e…`):

| | |
|---|---|
| Perfil | `procedimental-v11`, baseline `procedimental-v10` |
| Filas | 9.726 → **9.724** |
| Filas nuevas | ninguna |
| Filas fusionadas | `RPM-2010-04-15:3062:2`, `RPM-2010-04-15:3062:3` |
| Padres revisados | 657, 1564, 1706, 1924, 1925, 1995, 2960, 3062 |
| Grupos | 9.237 → 9.235 |
| Alertas | 484 → **485** |
| Reservas | 780 (4) · 2661 (12) · 5252 (4), intactas |
| `Pasa` | **True** |

**El gate de v11 es el primero que autoriza quitar filas**, y por eso tuvo que reescribir tres
comprobaciones que en v8–v10 suponían que las filas sólo se agregan: el corrimiento de ID pasa de
`+n filas nuevas antes` a `-n filas fusionadas antes`; la membresía de grupos admite que
desaparezcan exactamente los 2 grupos de las filas fusionadas; y la prueba de que una revisión
sirve se hace **contra el detector solo**, no contra el baseline, porque v10 ya trae siete de las
ocho revisiones aplicadas y comparar contra él no diría nada.

### La alerta que subió, y por qué está bien

`Alertas_Despues` pasó de 484 a **485**: la fila fusionada de 839 caracteres ahora lleva
`POSIBLE_OTRO_HABLANTE_O_MENCION`. Es correcto y se deja así. El texto menciona a otro consejero
con un verbo de habla, el detector de alertas lo señala, y la lectura dirigida ya adjudicó el caso.
La alerta queda visible como constancia de que la fila parece sospechosa y fue leída, no se borra
para que el número quede más bonito.

### La sesión 2010-04-15 queda cerrada

91 filas (93 antes de la fusión), 11 actores, 89.151 caracteres. Cola en cero, 2b en cero, 2c en
cero, los tres detectores de palabra partida en cero, cero caracteres fuera de repertorio. Los 13
candidatos de acento son correctos o la variante legítima `periodo`/`período` del §58. De los 4
finales sin puntuación, 2 ya llevan reserva abierta y 2 cierran una cita con comilla. No hubo
correcciones OCR nuevas en la sesión más allá de la familia `Claudia`→`Claudio` del §59.

Registro: **1.719 filas / 2.946 operaciones / 212 revisiones / 215 filas marcadas** (sin cambios:
ninguna fila del padre 3062 tenía corrección). Lecturas **4.885 de 9.724**, 61 de 132 sesiones.

## §61 — Sesión 2008-05-08: cero cortes, cuatro residuos y una cifra que no se adivina

Noventa y cinco filas, once actores, 100.466 caracteres. **Ningún corte.** Cola en cero, 2c en
cero, los tres detectores de palabra partida en cero, cero caracteres fuera de repertorio.

### Los dos candidatos a corte, leídos

**2b — `1819:1`** (Pablo García, 2.187 ch) señalaba a Manuel Marfán. Falso: «En cuanto al
comentario del Consejero señor Manuel Marfán **indica el señor García**, que la Gerencia de
División Estudios ha calculado los costos laborales unitarios». Es sujeto pospuesto; Marfán es el
objeto del comentario, no el hablante.

**Barrido independiente — `1808:1`.** El padre entero (531 ch) es de Sebastián Claro:

> «El Consejero señor Sebastián Claro menciona que esta tendencia inflacionaria en Europa… no
> sugieren que se esté en presencia… de un boom de precios de alimentos, pero sí del petróleo…
> **Asimismo, el señor Consejero consulta** de qué forma calza lo anterior con la historia de
> mayores precios de los alimentos.»

«El señor Consejero» sin nombre es el propio Claro continuando con «Asimismo»; no hay otro
consejero en juego. Las otras 17 referencias ajenas del barrido son el actor de la fila referido
por su cargo («el Gerente de Análisis Internacional» en filas de Lehmann, «el Gerente de Análisis
Macroeconómico **Interino**» en filas de Soto, «la Ministra de Hacienda Subrogante» en filas de
Recart). Las 9 filas de más de 2.500 caracteres son monólogos sin referencias ajenas.

### Cuatro residuos corregidos

| fila | virgen | corregido |
|---|---|---|
| `1804:2` | `paridades cambiabas` | `paridades cambiarias` (17 atestiguadas) |
| `1816:1` | `los costos f' H- laborales unitarios` | `los costos laborales unitarios` (159) |
| `1846:1` | `el riesgo de un L' desanclaje al alza` | `el riesgo de un desanclaje al alza` (145) |
| `1815:1` | `…de la que se piensa. r` | `…de la que se piensa.` |

Los dos del medio son la misma familia del §58 —residuo de escaneo pegado a una comilla recta—
pero con el residuo **rodeado de espacios**, así que el barrido del §58 (apóstrofo entre letras)
no los veía. El último cierra la alerta `FINAL_SIN_PUNTUACION` de esa fila: la oración de
Desormeaux ya terminaba en punto y la «r» sobraba entre ella y la intervención siguiente, que
empieza limpia. **La alerta se cierra porque el texto quedó bien, no porque se editara la alerta**,
y se deja constancia aquí a propósito.

### Una cifra que no se adivina

`1816:1`: «en el mes de abril, la inflación anual del IPC llegó a **a,3%**». El dígito de las
unidades está dañado: donde va un número hay una «a». La serie sugiere 8,3% —la Reunión siguiente
(`2008-06-10:1872:1`) consigna para mayo «8,4% anual»— pero **reconstruir una cifra por tendencia
es exactamente lo que la marca existe para no hacer**. Se dejó el texto intacto y se marcó
`CIFRA_INCONSISTENTE_POR_COTEJAR` (marca 10).

### Lo que ya estaba corregido y el barrido volvió a mostrar

Tres de los seis defectos que aparecieron al leer la sesión ya no existen en la salida: `De
Gregario` (§55), `Análisi s` y `del IRC`. Estaban en el **texto virgen**, que es lo que se lee;
medidos sobre el texto efectivo dan 0. **Regla: lo que se lee es el virgen, lo que se mide es el
efectivo.**

### Verificado

Los cuatro residuos → **0** · `paridades cambiarias` 17 → **18** · `costos laborales unitarios`
159 → **160** · `Texto` idéntico a la base en las **9.724** · suite local **61 OK**.

Registro: **1.721 filas / 2.950 operaciones / 212 revisiones / 216 filas marcadas**.
Lecturas **4.977 de 9.724**, 62 de 132 sesiones.

## §62 — Sesión 2011-03-17: cero cortes, un residuo y el primer fragmento DESPLAZADO

Noventa y cinco filas, trece actores, 95.597 caracteres. **Ningún corte.** 2b y 2c en cero, cero
caracteres fuera de repertorio, cero dobles espacios.

### Los dos casos de la cola ya estaban bien partidos

**Padre 3871** (204 ch) está en dos segmentos y está bien: «El señor Luis Óscar Herrera es de
opinión que este debiera ser "Indicador de expectativas de inflación"» (103 ch, Herrera) y «y el
Presidente señor José De Gregorio estima que debiera ser "índice de expectativas de inflación"»
(100 ch, De Gregorio). Dos opiniones sobre cómo llamar a un indicador; el segundo tramo ya venía
con `CONTEXTO_REVISADO` del registro histórico.

**Padre 3887** (8.366 ch) está en dos y también está bien: Claro hasta «el Consejero señor
Sebastián Claro vota por aumentar la tasa» (5.698 ch) y Marshall desde «Al continuar con la
votación, el Consejero señor Enrique Marshall comienza su intervención» (2.667 ch).

El barrido independiente sobre los trece actores dio **una sola** referencia ajena, y es el propio
Felipe Larraín referido como «el señor Ministro». Las diez filas de más de 2.500 caracteres son
monólogos sin referencias ajenas.

### Un residuo en la lista de asistentes

`3815:1`: «Gerente de Estabilidad Financiera, **...** don Luis Opazo Roco». Tres puntos sueltos
entre la coma y el tratamiento. El formato de esa lista es fijo —«Cargo, don/señor Nombre»— y sólo
para ese cargo aparece **82 veces** en el corpus; la secuencia `, ...` no aparece en ninguna otra
parte. Caso único, no una convención. Corregido.

### El primer fragmento desplazado, y por qué no se corrigió

`3887:1` dice:

> «…es posible que los próximos ajustes vuelvan a la gradualidad anterior, en la medida que las
> condiciones así lo sugieran. **a 4%.** En consecuencia, el Consejero señor Sebastián Claro vota
> por aumentar la tasa»

El «a 4%.» no falta: está **dos oracciones antes del lugar que le corresponde**, y la fila termina
sin puntuación justo donde falta. La lectura probable es «vota por aumentar la tasa a 4%.», y hay
corroboración independiente en la misma sesión: `3888:1`, Marshall, «vota por subir la TPM en
50pb, **hasta 4,0%**».

**Aun así no se corrigió.** Reordenar texto es otra cosa que borrar un residuo o completar una
palabra: es una reconstrucción. Y el vocabulario de quince tipos no tiene ninguno para un
movimiento —`SIMBOLO_SUELTO` borra, `PALABRA_OMITIDA` agrega, ninguno reordena—, lo que es una
señal de que está fuera del alcance del registro. Se dejó el texto intacto y se marcó
`RECONSTRUCCION_AMBIGUA_POR_COTEJAR` (marca 11) con la evidencia completa, de modo que quien
coteje el PDF lo resuelva en segundos.

**Regla nueva: un fragmento presente pero mal ubicado se marca, no se mueve.**

### La trampa del virgen, tercera vez

Al leer la sesión apareció «al staff **e\\** apoyo brindado» en `3887:2`. Preparé la operación y el
generador la rechazó por solapamiento: **ya estaba corregida** por una operación anterior
(`SIMBOLO_SUELTO`, «staff el apoyo»). Es la tercera vez que pasa lo mismo (§57 con `ígal`, §61 con
`De Gregario`/`Análisi s`/`IRC`, ahora esto). Lo que se lee es el **virgen**; antes de preparar una
operación hay que mirar el **efectivo**. El barrido de esta sesión se rehizo sobre el texto
efectivo y entonces sólo quedó el `...`.

### Verificado

`Financiera, ...don` → **0** · `Financiera, don Luis Opazo` **28** · `Texto` idéntico a la base en
las **9.724** (0 diffs) · barra invertida, doble espacio y punto pegado a letra en **0** en la
sesión · suite local **61 OK**.

Registro: **1.722 filas / 2.951 operaciones / 212 revisiones / 217 filas marcadas**.
Lecturas **5.069 de 9.724**, 63 de 132 sesiones.

## §63 — Sesión 2010-08-12: cero cortes, dos familias transversales y dos defectos míos

Noventa y seis filas, catorce actores, 106.715 caracteres. **Ningún corte.**

### Los cierres con coma no son defectos

El detector de finales marcaba cinco filas de la sesión que terminan en coma. Las cinco son
**legítimas**, porque la oración continúa gramaticalmente en la fila siguiente, que pertenece a
otro hablante:

| fila | cierre | sigue con |
|---|---|---|
| `3288:1` | «…de manera significativa,» | `3288:2` «**lo cual** es compartido por…» |
| `3303:2` | «…en el sector construcción,» | `3303:3` «**en tanto que** el señor Vicuña…» |
| `3313:1` | «…150.000 mil personas,» | `3313:2` «**a lo cual** el señor García responde…» |
| `3322:1` | «…A continuación,» | `3323:1` «el señor Claudio Soto se refiere a…» |
| `3325:1` | «…seis meses después,» | `3325:2` «**a lo cual** el señor Vicuña comenta…» |

Poner un punto en cualquiera de los cinco rompería la gramática. **Regla nueva: un cierre en coma
es legítimo cuando la fila siguiente retoma la oración.** La coma es la puntuación correcta de una
oración que el OCR partió en dos filas, y el corte por intervención es justamente lo que produce
esa situación.

### Dos familias transversales

Las dos son del acta, pero estaban enumeradas completas y se corrigieron en todo el corpus, caso
por caso y leyendo cada ocurrencia.

**`asi` → `así`, 19 operaciones.** «asi» no es palabra del español; el corpus escribe «así» 1.199
veces frente a 19. Los diecinueve son la misma lesión y ninguno es una sigla ni parte de otra
palabra.

**`Y` → `y`, 9 de 10.** Conjunción leída como mayúscula. **Se excluyó un caso legítimo:**
`RPM-2012-09-13:5049:1`, «en el eje **Y** se mide el movimiento del TCR», donde la mayúscula
nombra el eje. Una regla ciega habría roto esa fila; por eso la familia se curó ocurrencia por
ocurrencia y no con un reemplazo global.

**`obedecerla` → `obedecería`**, 1 operación en `3323:1`. «obedecerla a la depreciación del dólar»
no es gramatical; la forma está atestiguada 56 veces, dos de ellas en esta misma sesión.

### Dos defectos que introduje yo, y cómo se detectaron

Al verificar el archivo escrito las tres familias seguían en 1 en vez de 0. La causa era mía: el
generador del lote calculaba el reemplazo con `ctx.find(patron)`, que devuelve **la primera**
coincidencia del ancla, no la de la posición que se estaba corrigiendo. Dos operaciones cayeron en
el sitio equivocado:

- `2562:1`: acentuó la «i» de **Brasil** → «Brasíl», forma inexistente, y dejó el `asi` intacto.
- `3323:1`: reemplazó la «l» del artículo **la** → «de **ía** apreciación del peso obedecerla…».

Ambas se corrigieron con `enmendar_operacion.py` (que reescribe `Despues` y `Tipo` y no puede
tocar `Antes`), y la segunda pasó de `SIMBOLO_SUELTO` a `ACENTO_FALTANTE`.

**Lección: un conteo de familia que no llega a cero no es ruido, es una operación mal anclada.**
La comprobación que lo encontró compara `Antes` y `Despues` carácter a carácter y exige que el
único cambio caiga sobre la palabra objetivo. Hay que correrla sobre cada lote nuevo, no sólo
sobre las familias globales.

### Cifra marcada

`3313:1`: «la fuerza de trabajo había aumentado entre 100.000 y 150.000 mil personas». «150.000
mil» serían 150 millones de personas. Las dos lecturas plausibles dan la misma magnitud pero no la
misma cifra escrita. Marca 12, `CIFRA_INCONSISTENTE_POR_COTEJAR`; la conjunción mayúscula se
corrigió igual porque es independiente del problema.

### Verificado sobre el archivo escrito

9.724 filas · **0 diffs de `Texto`** · `asi` **0** · `obedecerla` **0** · `Brasíl` **0** · `e ía`
**0** · `Y` entre palabras **1**, el «eje Y» legítimo. Suite local **61 OK**.

Registro: **1.734 filas / 2.980 operaciones / 212 revisiones / 218 filas marcadas**.
Lecturas **5.159 de 9.724**, 64 de 132 sesiones.

## §64 — Sesión 2009-05-07: cero cortes con las tres redes en cero, y una transposición

Noventa y un filas, doce actores, 97.868 caracteres. **Ningún corte**, y esta vez las tres redes de
detección dieron cero sin que hiciera falta adjudicar nada: ninguna fila de la sesión está en la
cola de 74, 2b no encontró ninguna fila de un solo segmento con otra persona como sujeto de un
verbo de habla, y 2c ninguna de las cinco firmas del §49.

El barrido independiente sobre los doce actores dio tres referencias ajenas y **las tres son
falsas**, cada una por una razón distinta:

| fila | referencia | por qué no es cambio de voz |
|---|---|---|
| `2508:1` | «el Gerente División de Estudio menciona» | el propio Pablo García, por cargo |
| `2510:2` | «…del Consejero señor Sebastián Claro, el Gerente de Análisis Internacional señala» | el propio Lehmann; Claro es el **objeto** de la consulta |
| `2506:2` | «el señor **Lehmman** señala» | el propio Lehmann con el apellido dañado |

Las dos filas mayores se leyeron enteras: la presentación de De Gregorio (7.958 ch) y la
fundamentación del voto de Marshall (6.028 ch) son monólogos sin cambio de sujeto.

### Una transposición de apellido

`Lehmman` con doble eme aparece **11 veces** en el corpus, frente a **1.909** de `Lehmann`. Las once
son el mismo Gerente de Análisis Internacional, Sergio Lehmann Beresi, y nueve de ellas están
concentradas en la sesión `2006-04-13`. Se corrigieron las once.

**El vecino peligroso:** `Lehman` con una ene aparece **19 veces** y es correcto — es la firma
`Lehman Brothers`, ya documentada en §58. Una regla que buscara «Lehm» y normalizara habría roto
las 19. Por eso la familia se escribió con frontera de palabra completa y se contó el resultado
después: `Lehmann` pasó de 1.909 a **1.920** y `Lehman` quedó en **19**.

Es también la primera **transposición** del registro: misma longitud, tres posiciones distintas
(`m a n` → `a n n`). La auditoría de operaciones del §63, que exige un solo carácter distinto
cuando las longitudes coinciden, la habría rechazado como falsa alarma. Se ajustó para comparar
`Antes` con la sustitución exacta aplicada una sola vez, que es la comprobación que de verdad
importa.

### Cinco defectos más

| fila | defecto | tipo |
|---|---|---|
| `2508:1` | `Bank o f America` → `Bank of America` (la misma fila lo escribe bien más adelante) | `ESPACIO_INDEBIDO` |
| `2519:2` | `( ( ` entre dos oraciones completas — único desbalance de la sesión y único «( (« del corpus | `SIMBOLO_SUELTO` |
| `2536:1` / `2780:1` | `impuesto especifico` → `específico` (2 frente a 46) | `ACENTO_FALTANTE` |
| `5669:1` | `situaciones especificas` → `específicas` (1 frente a 28) | `ACENTO_FALTANTE` |
| `2522:1` | `…aproximadamente. y .` → `…aproximadamente.` | `SIMBOLO_SUELTO` |

**El verbo `especifica` no se tocó.** Aparece decenas de veces en el corpus y es correcto; la
familia se escribió buscando sólo el adjetivo, y después se contó que `específico` pasó de 46 a 48
sin que `especifica` cambiara.

### Extender la operación existente, no apilarle otra

`2522:1` ya tenía una operación sobre ese tramo: `'damente. y .'` → `'damente. y.'`, que sólo
quitaba el espacio del punto final y dejaba la conjunción huérfana. Lo correcto era **extenderla**
(regla del §15), no añadir una segunda operación encima: `Despues` pasó a `'damente.'` y el `Tipo`
de `ESPACIO_INDEBIDO` a `SIMBOLO_SUELTO`, porque el arreglo dejó de ser un espacio. Al quitar el
residuo la fila termina en «…son dos años aproximadamente.», que está completa, y la alerta
`FINAL_SIN_PUNTUACION` cierra por consecuencia.

### Quedan abiertas dos reservas de esta sesión

`2526:1` termina en una `A` suelta (empezó una oración que se cortó) y `2529:1` termina en «consulta
a qué se refiere la vinculación» sin punto. Las dos llevan `FINAL_SIN_PUNTUACION` como reserva
abierta y **no se cierran con un punto**: falta texto, no falta puntuación.

### Verificado sobre el archivo escrito

9.724 filas · **0 diffs de `Texto`** · `Lehmman` **0** · `Lehmann` **1.920** · `Lehman` **19**
intacto · `especifico` **0** · `específico` **48** · `especificas` **0** · `Bank o f` **0** ·
`Bank of America` **5** · `( (` **0** · filas que terminan en « y.» **0**. Suite local **61 OK**.

Registro: **1.742 filas / 2.996 operaciones / 212 revisiones / 218 filas marcadas**.
Lecturas **5.249 de 9.724**, 65 de 132 sesiones.

## §65 — Sesión 2010-10-14: la firma del §48 resulta falsa, y tres familias transversales

Ochenta y nueve filas, trece actores, 103.139 caracteres. **Ningún corte.**

El padre 3449, único caso de la cola, ya está bien partido: `3449:1` es Claro con sus dudas sobre
los precios de los activos y `3449:2` es De Gregorio sobre el Dow Jones.

### La firma «un tercero responde» dio falso por segunda vez

2c señaló `3454:1` con la firma que **sí** produjo un corte en el §48 (padre 1706). Leída entera:

> «Al respecto, y respondiendo a una consulta del Vicepresidente señor Manuel Marfán, **aclara** que
> ello estaba considerado en el supuesto del Banco…»

El sujeto de «aclara» es Soto, que viene de iniciar su exposición; Marfán es el **objeto** de la
consulta. La firma detecta «un cargo + verbo de habla» sin mirar de quién depende el verbo. Es el
mismo patrón que `1706` resolvió al revés, y la diferencia está en la preposición: «respondiendo **a
una consulta del** Vicepresidente» ata el cargo a la consulta, no al verbo.

### Diecinueve variantes dañadas de «Imacec»

El OCR leyó la «I» mayúscula como una «ele» minúscula. El corpus escribe el indicador **487 veces**
de forma correcta (263 `IMACEC` y 224 `Imacec`) y `lmacec` no es ninguna palabra:

| variante | casos | ejemplo |
|---|---|---|
| `lmacec` | 15 | «el **lmacec** del mes de mayo creció menos» |
| `ellmacec` | 2 | «en materia de actividad, **ellmacec** de agosto» → «el Imacec» |
| `lMACEC` | 1 | «en el **lMACEC** coherente con las nuevas cuentas» |
| `imacec` | 1 | «medida por el **imacec** aumentó 6,4%» |

**La forma repuesta se decidió fila por fila**, no con una sola: se usó la que emplea **la propia
sesión** para el mismo indicador (`2405:1` → `IMACEC`, porque su sesión lo escribe así 8 veces y la
propia fila 2; `6309:1` → `Imacec`, porque su sesión lo escribe así 3). En las dos filas sin
evidencia en su sesión se usó la del año: `297:2` (2005, con 2006 → 26 `Imacec` contra 3) y `7010:1`
(2015 → 24 `Imacec` contra 18). Resultado: `IMACEC` 263 → **272** y `Imacec` 224 → **234**, suma 506
= 487 + 19.

### «haber» más gerundio, nueve casos

`han observando`, `han funcionando`, `han aumentando`, `han continuando`, `han mejorando` (dos),
`han modificando`, `han incrementando`, `han subestimando`. «Haber» más gerundio no es una forma del
español; la «d» del participio se leyó como «n». Los nueve se corrigieron al participio.

**El caso que no es simétrico:** `2291:2`, «se han **continuando** disipando las tensiones» → «se han
**continuado** disipando». Sólo cambia el primer verbo, porque el segundo gerundio es legítimo.

### El punto que falta en una fórmula fija — y el arreglo que el registro no puede expresar

«Siendo las HH:MM horas, se reanuda la Sesión de Política Monetaria» aparece **67 veces**: 54 cierran
con punto, 11 continúan con el número de la sesión («N° 74, con la participación…») y **2 terminan
ahí sin nada** (`2489:4` y `3476:5`). En esas dos el punto falta con casi total certeza.

**Pero no se agregó, y no se puede agregar.** El aplicador del registro es un reemplazo literal
(`salida.replace(antes, despues)`), así que cualquier inserción deja `Antes` contenido en `Despues`
y aplicar dos veces apila un segundo punto: «…Monetaria**..**». Lo detectó
`test_no_vuelve_a_corregir_sobre_lo_corregido`, y al revisarlo resultó que en las **3.025 operaciones
del registro no hay una sola inserción pura**: agregar un carácter al final de una fila es el único
tipo de arreglo que este mecanismo no puede expresar. Las dos filas quedaron marcadas
`SIGNO_AUSENTE_POR_COTEJAR` (marcas 14 y 15).

**Regla nueva: si `Antes` está contenido en `Despues`, la operación no es aplicable.** Hay que
comprobarlo antes de escribirla, no dejarlo al test.

La medición inicial decía «65 de 68 con punto» y estaba mal: contaba como sin punto las filas que
llevan el número de sesión en la línea siguiente. Se rehizo contando lo que sigue a la fórmula.

### Una coma que no se tocó

`3460:1` termina en coma y la fila siguiente, de otro hablante, abre una oración nueva con
mayúscula. Lo más probable es que la coma deba ser un punto, pero **no se corrigió**. Medido en todo
el corpus: 113 filas cierran en coma y la siguiente retoma la oración, y 155 donde un clasificador
automático dice que no — pero la gran mayoría de esas 155 son la fórmula «A continuación,» seguida
de «el Presidente ofrece la palabra…», que **sí** continúa. No hay regla fiable que distinga un
cierre en coma legítimo de uno que esconde texto faltante, y poner un punto taparía la segunda
posibilidad. Marca 13, `RECONSTRUCCION_AMBIGUA_POR_COTEJAR`.

### Verificado sobre el archivo escrito

9.724 filas · **0 diffs de `Texto`** · variantes dañadas de Imacec **0** · `IMACEC` **272** ·
`Imacec` **234** · «haber + gerundio» **0** · «( El Gerente» **0** · fórmula «se reanuda» con punto **54** y sin punto **13** (11 legítimas más las 2 marcadas). Suite local **61 OK**.

Registro: **1.757 filas / 3.025 operaciones / 212 revisiones / 221 filas marcadas**.
Lecturas **5.336 de 9.724**, 66 de 132 sesiones.

## §66 — Sesión 2011-11-15: la sesión más limpia, y el conector en mayúscula como señal de texto perdido

Ochenta y nueve filas, trece actores, 95.723 caracteres. **Ningún corte.**

Es la sesión más limpia hasta ahora. Las tres redes dieron cero y el barrido independiente sobre los
trece actores **no dio ni una referencia ajena** en las 89 filas. Los signos también están limpios:
cero caracteres fuera de repertorio, cero dobles espacios, cero comillas rectas, cero paréntesis
desbalanceados, y ninguna fila termina en letra suelta ni en coma. Las 13 filas de más de 2.500
caracteres son monólogos; se leyeron enteras las dos más sensibles —la despedida de Marfán a De
Gregorio (`4446:3`, 1.637 ch) y la presentación de Larraín (`4453:3`, 4.713 ch)— y en ninguna cambia
el sujeto.

### Un conector en mayúscula pegado a una oración incompleta significa texto perdido

Buscando otra cosa aparecieron ocho filas con este patrón:

| fila | …antes del conector |
|---|---|
| `292:2` | «los últimos antecedentes de inflación y crecimiento nuevamente **confirman** Por lo tanto,» |
| `657:2` | «en particular para **plazos** Por otra parte,» |
| `744:4` | «el dinamismo de Europa es **ciertamente** Por último,» |
| `1055:1` | «cambios de ciclo e incluso ciclos de política, **que** Por último,» |
| `2176:2` | «tras la crisis de los años 30**,** Por otra parte,» |
| `5177:1` | «suficiente fuerza para evitar el **fiscal** Por último,» |
| `5380:1` | «anotaron una variación anual en **torno** Por su parte,» |
| `5877:1` | «en el caso de LAN Airlines en **nuestro** Por último,» |

**En siete de los ocho la oración anterior está incompleta**: «confirman» sin objeto, «es ciertamente»
sin adjetivo, «en torno» sin complemento, «en nuestro» sin sustantivo. La mayúscula del conector no
es un error de mayúscula: es el principio del párrafo siguiente, y entre las dos mitades el OCR
perdió un trozo de texto en un salto de página o de columna.

**No se corrigió ninguno, y la razón importa:** poner un punto donde está la coma taparía la
pérdida. `2176:2` es el único donde la oración anterior sí está completa, pero ni ése se tocó,
porque distinguirlos exige leer el PDF. Las ocho quedaron marcadas
`RECONSTRUCCION_AMBIGUA_POR_COTEJAR` (marcas 16 a 23).

**Regla nueva: un conector en mayúscula inmediatamente después de una minúscula o una coma es señal
de texto perdido, no de puntuación.**

### Dos corchetes de cierre sin apertura

`978:1` («doble shock petrolero-gasífero**]** desde la apreciación…») y `1210:1` («se está a un mes de
un IPoM**]** dos, que no le queda claro…»). Son los dos únicos desbalances de corchete del corpus:
cada fila tiene 0 aperturas y 1 cierre. Borrarlo cambiaría la lectura —en `1210:1` el signo separa
«una, que…» de «dos, que…», donde probablemente había un punto y coma— y reponer la apertura sería
inventar. Marcas 24 y 25.

### «porqué» junto, siete de diez

`porqué` junto y acentuado es el sustantivo y exige artículo («el porqué», «del porqué»). El corpus
tiene **94 «por qué»** frente a **10 «porqué»**, y de esos diez **tres llevan artículo y son
legítimos** (`1846:1` «del porqué de un aumento», `2029:1` «el porqué el empleo…», `2042:1`
«justificar el porqué»). Los otros siete introducen una interrogativa indirecta y se corrigieron a
«por qué», uno en esta sesión (`4452:1`, «la pregunta es porqué no hacerlo»).

Resultado: quedan **3**, los tres con artículo, y «por qué» pasa de 94 a **101**.

### Verificado sobre el archivo escrito

9.724 filas · **0 diffs de `Texto`** · `porqué` **3** (los tres con artículo) · `por qué` **101**.
Suite local **61 OK**.

Registro: **1.761 filas / 3.032 operaciones / 212 revisiones / 231 filas marcadas**.
Lecturas **5.422 de 9.724**, 67 de 132 sesiones.

## §67 — Sesión 2012-07-12: el método de las palabras únicas

Ochenta y nueve filas, trece actores, 100.036 caracteres. **Ningún corte.**

2b dio dos casos y los dos son falsos, ambos con Marfán como **objeto** de una referencia a algo que
él mismo dijo antes:

- `4910:1` (Vial): «…el titular del diario The Financial Times **a que se aludió por** el Vicepresidente
  señor Manuel Marfán, estima que se refiere a…» — el que estima es Vial.
- `4946:1` (Soto): «…corrobora **el planteamiento expuesto por** el Vicepresidente señor Manuel Marfán».

El barrido independiente dio otras dos, falsas por el mismo motivo: en `4916:2` Vergara es objeto de
«junto con compartir el planteamiento del Presidente» y Soto del traspaso de la palabra. Las 10 filas
de más de 2.500 caracteres son monólogos y ninguna fila de la sesión termina en coma ni sin
puntuación.

### Un detector nuevo: las palabras que aparecen una sola vez en todo el corpus

Los detectores habituales —acento, partida, deletreada, signos— dieron **cero** en esta sesión, y aun
así tenía cuatro defectos. Lo que los encontró fue otro método: listar las palabras de la sesión que
aparecen **una sola vez en las 9.724 filas** y leerlas. De 38 candidatas, cuatro eran daño real:

| fila | dañado | correcto | evidencia |
|---|---|---|---|
| `4938:1` | «el tipo de **cambo** nominal» | `cambio` | 1 frente a **2.948** |
| `4959:1` | «la evolución de la **ecqnomía** chilena» | `economía` | 1 frente a **2.988** |
| `4967:1` | «agregados menos **líquídos**» | `líquidos` | 1 frente a **25** |
| `4959:1` | «la opinión **de de** la Gerencia» | `de` | 13 casos, ninguno legítimo |

Las otras 34 eran palabras legítimas que simplemente no se repiten (`férreas`, `potasio`,
`termoeléctricas`, `letanía`, `totalizar`).

**El método sirve porque no depende de una lista de defectos conocidos.** Los detectores de acento y
de partida buscan patrones que ya se vieron; una palabra dañada que no se parece a ninguna forma
conocida no cae en ninguno. Contar frecuencias sí la atrapa.

### «de de», trece casos

Preposición duplicada. Los trece son la misma lesión y ninguno es legítimo: no hay construcción del
español con «de de» seguido de sustantivo. Once estaban en la fórmula «ofrece la palabra al Gerente
**de de** Análisis Macroeconómico».

En `1815:3` la fila ya tenía una operación sobre ese tramo que juntaba «Anál isis» en «Análisis»
**pero dejaba el «de de»**. Se extendió la operación existente (§15) en vez de apilarle otra, y el
`Tipo` pasó de `PALABRA_PARTIDA` a `PALABRA_DUPLICADA` porque el arreglo principal cambió.

### «saddle pad»: marcada, no corregida

`4909:1`: «una hipótesis no descartable es que en Chile cuesta cambiarse de **saddle pad**, ya que a
diferencia de otros países donde se observa una cierta convergencia hacia un equilibrio, la
experiencia local indica que los ajustes son bastante bruscos».

La expresión no aparece en ninguna otra parte («saddle» 1 vez, «pad» 1 vez) y no tiene sentido en el
contexto. La frase habla de convergencia hacia un equilibrio y de ajustes bruscos, que es el
vocabulario de un **punto de silla** (*saddle point*), pero reconstruir «pad» como «point» sería
adivinar —y además la guarda de términos foráneos del registro lo rechazaría. Marca 26.

### Dos convenciones que NO son defectos

- **Rangos de año con guión espaciado**: 51 casos, todos «AAAA - AAAA» («el período 2008 - 2009»).
  Consistente.
- **Guión largo**: el corpus usa las dos formas, « —palabra» (159) y « — palabra» (150). No hay una
  sola convención que restaurar.

### Verificado sobre el archivo escrito

9.724 filas · **0 diffs de `Texto`** · `cambo` **0** y `cambio` **2.949** · `ecqnomía` **0** y
`economía` **2.989** · `líquídos` **0** y `líquidos` **26** · «de de» **0** · «saddle pad» **1**,
marcado. Suite local **61 OK**.

Registro: **1.773 filas / 3.047 operaciones / 212 revisiones / 232 filas marcadas**.
Lecturas **5.507 de 9.724**, 68 de 132 sesiones.

## §68 — Sesión 2012-02-14: la apertura de una Reunión es un solo hablante

Noventa filas, doce actores, 111.619 caracteres. **Ningún corte.**

El único caso de la cola, el padre **4574**, es la apertura de la Reunión 182 y es **un solo
hablante**, el Presidente Vergara. La fila nombra a cuatro personas y ninguna interviene:

| tramo | quién aparece | por qué no es intervención |
|---|---|---|
| «da la bienvenida al señor Joaquín Vial Ruiz-Tagle, en su carácter de nuevo Consejero» | Vial | **bienvenida** |
| «el Consejo … acordó renovar la designación del señor Manuel Marfán Lewis en el cargo de Vicepresidente» | Marfán | **mención** de un acuerdo |
| «deja constancia que el Ministro de Hacienda señor Felipe Larraín **le informó** que solo asistirá al análisis» | Larraín | **objeto** de «informó»; Larraín no habla |
| «da paso a la presentación del escenario externo, a cargo del … señor Miguel Ricaurte» | Ricaurte | **traspaso de la palabra** |

Es el caso más completo hasta ahora de los cuatro distractores que la regla ya cubre —mención,
bienvenida, traspaso, y ahora también «alguien le informó algo al que habla». Que el detector
permisivo propusiera a Larraín como segunda voz es exactamente el falso positivo que la regla
anticipa.

2b dio tres casos y los tres son falsos: en `4579:1` y `4632:1` el Presidente Vergara es el objeto de
«respondiendo la consulta específica formulada por» y «respondiendo una consulta del», y los que
hablan son Ricaurte y Soto; en `4577:1` «el Gerente de Análisis Internacional Subrogante» es el
propio Ricaurte por cargo. Las 15 filas de más de 2.500 caracteres son monólogos y los signos están
limpios.

### Dos correcciones

**`4574:1`**: «**En tercer, lugar,** indica que…» — coma intrusa dentro de la locución. La misma fila
usa bien las dos anteriores («En primer término», «En segundo lugar») y en el corpus «En tercer
lugar» aparece 80 veces sin coma interna. Es el único caso.

**`4575:1`**: «a pesar **de la rebajas** de calificación de riesgo comentadas» — falta la «s» del
artículo. El sustantivo va en plural y tres oraciones antes la misma fila dice «continuaron **las
rebajas** de clasificación de riesgo». Es el único caso del corpus de «de la» seguido de plural.

### Un apellido que no se tocó

`4573:1`, lista de asistentes: «Gerente de Mercados Nacionales Subrogante, **doña Claudia Sotz
Pantoja**». El apellido «Sotz» aparece una sola vez en las 9.724 filas y **no hay forma canónica
atestiguada que lo supere**: el corpus tiene «Claudia Varela» (2 veces, otra persona) y ninguna
«Claudia Soto». Podría ser «Soto» dañado, pero «o» por «z» no es una confusión que el OCR haga en
ninguna otra parte del registro, y normalizar sin forma atestiguada es justo lo que las reglas de
nombres prohíben (§34, §58). Marca 27.

### Una variante que se dejó

`trasferencia` (2) frente a `transferencia` (10) y `transferencias` (22). Las dos grafías son
aceptadas y la diferencia de frecuencia no convierte a la minoritaria en error —el mismo criterio
que dejó `periodo` junto a `período`. No se tocó.

### Verificado sobre el archivo escrito

9.724 filas · **0 diffs de `Texto`** · «En tercer, lugar» **0** y «En tercer lugar» **80** ·
«de la rebajas» **0** y «de las rebajas» **3** · «Sotz» **1**, intacto y marcado. Suite local
**61 OK**.

Registro: **1.775 filas / 3.049 operaciones / 212 revisiones / 233 filas marcadas**.
Lecturas **5.592 de 9.724**, 69 de 132 sesiones.

## §69 — Sesión 2011-01-13: la señal estricta sobre un padre ya partido, y un texto perdido antes de un cambio de hablante

Ochenta y nueve filas, trece actores, 92.332 caracteres. **Ningún corte.**

La cola tenía un caso, el padre **3650**, y con **señal estricta** —la más fuerte de las seis que usa
el detector. Leída la fila, el corte **ya está hecho en la base**:

| segmento | actor | largo | ancla |
|---|---|---|---|
| `3650:1` | Sergio Lehmann | 103 ch | propia |
| `3650:2` | Luis Óscar Herrera | 280 ch | `None` |

«El Gerente de Análisis Internacional señor Sergio Lehmann confirma lo expresado por el señor
Presidente» / «**y** el Gerente de División Estudios señor Luis Óscar Herrera, **por su parte**,
explica que…». El detector señala el padre completo, no sus segmentos: **una señal estricta sobre un
padre que ya está partido no es un corte pendiente.** El padre 3651 viene igual (`3651:1` De Gregorio,
`3651:2` Lehmann).

2b dio un caso, falso: en `3654:1` el Vicepresidente Marfán es el objeto de «manifiesta coincidir con
las aprensiones **planteadas por**». El barrido independiente dio dos, falsas por el mismo motivo: en
`3655:2` el Consejero Claro es el objeto de «manifiesta concordar con lo planteado por». Las 10 filas
de más de 2.500 caracteres son monólogos.

### Dos correcciones que sólo el método de palabras únicas encontró

Los detectores de acento, partida y deletreada dieron **cero** en esta sesión. Las dos salieron del
censo de palabras que aparecen una sola vez en las 9.724 filas (§67):

**`3699:1`**: «las tasas **svjap** han tendido a aumentar» — `swap` con tres letras cambiadas. El
corpus tiene **156 «swap», 61 «swaps», 8 «Swap», 11 «Swaps»** y **1 «svjap»**. En la misma fila se
habla de tasas de swap, que es el instrumento de que se trata.

**`3711:1`**: «una serie de precios que **sé** indexan rápidamente al tipo de cambio» — tilde
indebida en el pronombre. En todo el corpus hay sólo dos «sé» acentuados y el otro es legítimo
(«**per sé**», `RPM-2009-03-12:2430:1`), así que éste es el único caso dañado.

### Un texto perdido justo antes de un cambio de hablante

`3670:1` (Herrera) termina así:

> «…bienes de consumo durables, que tienen trayectorias caracterizadas por caídas violentas del orden
> de 20%, **y recuperaciones también**»

Sin puntuación y a mitad de frase: falta el complemento de «también» (violentas, bruscas, rápidas).
**No es un corte por intervención.** La fila siguiente, `3670:2`, es otro hablante (Claudio Soto) y
tiene su propia ancla, así que en el original eran dos párrafos distintos y lo que se perdió está
dentro de ésta. No se puede reponer inventando el adjetivo ni cerrar con un punto, que taparía la
pérdida. Marca 28.

Es un caso distinto del §66: allí el conector en mayúscula pegaba dos párrafos dentro de una misma
fila; aquí la pérdida queda al final de una fila que ya está bien delimitada.

### Tres finales sin puntuación, sólo uno defectuoso

- `3646:1` cierra en coma y `3646:2` empieza con «**lo cual** es confirmado por el Gerente…» →
  legítimo (§63).
- `3650:1` cierra sin punto y `3650:2` empieza con «**y** el Gerente…» → legítimo, la oración
  continúa al otro lado del corte.
- `3670:1` → el caso anterior, marcado.

### Una palabra rara que se dejó

`3709:1`: «las alzas de la carne de vacuno y de los **plumíferos**, en particular el pollo». La
palabra es infrecuente para hablar de aves, pero está bien formada y el OCR no produce palabras bien
formadas a partir de daño. Se dejó.

### Verificado sobre el archivo escrito

9.724 filas · **0 diffs de `Texto`** · «svjap» **0** · «que se indexan» **1** · «que sé indexan»
**0** · «per sé» **1** intacto. Suite local **61 OK**.

Registro: **1.776 filas / 3.051 operaciones / 212 revisiones / 234 filas marcadas**.
Lecturas **5.675 de 9.724**, 70 de 132 sesiones.

## §70 — Sesión 2010-03-18: la firma «en tanto que» sobre un padre ya partido, y los residuos de página

Ochenta y cuatro filas, trece actores, 87.548 caracteres. **Ningún corte.**

La cola tenía un caso, el padre **2983**, con señal estricta **y** con la firma «en tanto que» más un
nombre, que es una de las señales de lectura documentadas. Leída la fila, el corte **ya está hecho en
la base**: `2983:1` es Claudio Soto («confirma que esos son los dos componentes», 64 ch) y `2983:2` es
Pablo García («**en tanto que** el señor Pablo García explica que…», sin ancla). Segunda vez seguida
que pasa (§69): **el detector señala el padre completo, no sus segmentos.**

2b y 2c dieron cero. El barrido independiente dio dos casos, falsos los dos: en `3008:3` José De
Gregorio es el objeto de «**agradece las palabras del**», y en `3011:3` «el Gerente de Investigación
Económica» es el propio Luis Felipe Céspedes —cargo que ocupa en todas las sesiones desde
2009-04-09, verificado en el corpus.

### Un participio mal concordado

`3011:1`: «en el ámbito externo se ha **observada** que la volatilidad financiera se ha aplacado». Con
el auxiliar «ha» el participio es invariable, y además el sujeto es la cláusula «que la volatilidad…
se ha aplacado», no un sustantivo femenino. El corpus tiene **221 «ha observado»** y éste era el
único «ha observada» de las 9.724 filas.

### Una familia transversal: residuos de página al final de la fila

Revisando los signos aparecieron **6 filas en todo el corpus** que terminan en un signo suelto
después del punto que cierra la oración:

| fila | terminaba en |
|---|---|
| `RPM-2005-07-12:310:1` | `…en tal sentido.` **`U)`** |
| `RPM-2008-11-13:2162:2` | `…se capitalicen.` **`J)`** |
| `RPM-2009-05-07:2517:1` | `…nivel inicial.` **`/ . /`** |
| `RPM-2010-03-18:2969:1` | `…Alfaro Arancibia.` **`/ )`** |
| `RPM-2011-06-14:4064:1` | `…sincronizadamente.` **`-4 . f . • " ' A)`** |
| `RPM-2013-04-11:5486:1` | `…mes del año 2012.` **`/`** |

En los seis la oración anterior está completa y con su punto: lo que sigue es el pie de página del
PDF que el OCR capturó al terminar la página. **Es exactamente el caso que la política de corrección
autoriza a eliminar** (residuos de fuente: números de página, marcas sueltas, restos de firma). Se
borraron las seis. Verificado: el censo pasa de **6 a 0**.

### Una corrección anterior que arreglaba lo equivocado

Tres de esas seis filas **ya tenían una operación** sobre ese tramo, y lo que hacía era arreglar el
espaciado **dentro** del residuo en vez de borrarlo:

| fila | `Antes` | `Despues` anterior | `Despues` ahora |
|---|---|---|---|
| `2517:1` | `inicial. / . /` | `inicial. /. /` | `inicial.` |
| `4064:1` | `amente. -4 . f . • " ' A)` | `amente. -4. f. • " ' A)` | `amente.` |
| `5486:1` | `l año 2012 . /` | `l año 2012. /` | `l año 2012.` |

Se extendieron las tres operaciones existentes (§15) y el `Tipo` pasó de `ESPACIO_INDEBIDO` a
`RESIDUO_PAGINACION`. **Enseñanza: antes de escribir una operación sobre un tramo que ya está
corregido, leer qué hace la operación existente** — aquí el arreglo anterior no sólo era insuficiente,
sino que apuntaba a un defecto que no era el defecto.

### Doce finales en coma, todos legítimos

Doce filas de la sesión cierran en coma. Se leyeron una por una y en todas la fila siguiente retoma la
oración («lo cual», «y el Gerente…», «en tanto que…»), que es lo que la regla del §63 declara
legítimo. No se tocó ninguna.

### Verificado sobre el archivo escrito

9.724 filas · **0 diffs de `Texto`** · filas que terminan en «)» o «/» **0** (antes 6) · «ha
observada» **0** (antes 1). Suite local **61 OK**.

Registro: **1.779 filas / 3.055 operaciones / 212 revisiones / 234 filas marcadas**.
Lecturas **5.758 de 9.724**, 71 de 132 sesiones.
