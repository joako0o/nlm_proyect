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
