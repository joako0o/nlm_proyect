# LOOP22 — Respuestas nominales en gerundio y OCR dañado

**2026-09-08 · [PR #3](https://github.com/joako0o/nlm_proyect/pull/3)**

Base: `49db3458f322b88e9eb6b2d77d8637579569ef14`, [LOOP21](REVISION_LOOP21_2026-09-08.md).
Lectura dirigida por agente del texto disponible. **Sin nuevo cotejo PDF ni muestra independiente.**

## Resultado publicado

| Medida | LOOP21 | LOOP22 |
|---|---:|---:|
| Filas físicas / bloques | 9.584 / 9.583 | **9.610 / 9.609** |
| Grupos / grupos multifila | 9.168 / 320 | **9.194 / 320** |
| Máximo de filas por grupo | 11 | **11** |
| Filas advertidas / padres advertidos | 370 / 325 | **392 / 343** |
| Pruebas | 1.297 | **1.336** |
| Intervalos revisados / padres con revisión | 309 / 288 | **332 / 307** |
| Advertencias contextuales activas | 56 | **61** |
| Lecturas actuales documentadas | 20 | **22** |
| Etiquetas nominales observadas | 55 | **55** |

**Veinte padres resegmentados**, con **23 intervalos nuevos** en 19 padres nuevos y uno ya revisado (2674). **2463 es recuperación parcial con cierre ambiguo advertido**, no resolución de exclusividad de voz. Además: **1904 sólo advertencia de cargo**, **854/1621 dos lecturas negativas sin cambiar segmentación**, y **1387/2864 sólo actualización de la referencia al antecedente de continuidad**.

**Dieciocho de los veinte padres resegmentados estaban sin alertas.** Los otros dos, 2938 y 3028, tenían final sin puntuación; la corrección no elimina todos sus motivos residuales.

- [Comparación global, fuentes y hashes](comparacion_loop22_2026-09-08.json)
- [Filas antes/después](cambios_loop22_2026-09-08.csv)
- [Checkpoint y pendientes](estado_revision_loop22_2026-09-08.json)

## 1. Respuestas y acotaciones efectivas

Se leyeron íntegros los padres de la tabla, incluidos los desarrollos previos/posteriores. Cifras en caracteres; «revisado» identifica una atribución acotada y **no un ancla global**.

| Padre | Secuencia relevante después de la revisión |
|---|---|
| **1386** | Corbo **104** → Lehmann **69 revisados** → Corbo **139** → Valdés **833** |
| **2692** | De Gregorio **98** → Lehmann **385 revisados** → Lehmann **416 explícitos** |
| **2738** | Soto **4.743** → De Gregorio **105 revisados** → Soto **947 revisados** → Marfán **401** |
| **2740** | Soto **3.731** → Velasco **137** → Soto **207** → Velasco **267 revisados** → De Ramón **674** |
| **2863** | Marfán **106** → Soto **63 revisados** → Soto **939 explícitos** |
| **2911** | Vergara **121** → Soto **43 revisados** |
| **2922** | De Gregorio **97** → Soto **192 revisados** → De Gregorio **196** |
| **2938** | Marshall **105** → García **51 revisados, incompletos** → Marfán **634** |
| **3028** | Se mantienen De Gregorio **72** → Lehmann **86**; el final queda De Gregorio **114** → Lehmann **173 revisados** |
| **3054** | Marshall **147** → Soto **133 revisados** |
| **3160** | Vergara **90** → García **81 revisados** |
| **3543** | Vergara **72** → Soto **56 revisados** |
| **5061** | Vergara **97** → Cowan **117 revisados** |
| **5519** | Claro **146** → Lehmann **158 revisados** |
| **5872** | Marfán **127** → Soto **114 revisados** |
| **6813** | Vergara **115** → Gianelli **141 revisados** → Gianelli **793 explícitos** → Vergara **240** |
| **7176** | Naudon **148** → Vial **111 revisados** |

Las respuestas tienen sujetos nominales y predicados efectivos: cotización e inventarios de cobre, efectos del IPC, perfiles estacionales, bonos, existencias, Grecia y acotaciones sobre inversiones o sector público. **No se confunde al consultante con quien responde**, ni se eliminan respuestas de 43/51/56/63 caracteres por su brevedad.

**2738:** la acotación presidencial sobre el shock de septiembre no absorbe el retorno de Soto. El cargo anafórico «el señor Gerente» se resuelve localmente por su exposición nominal previa, no por una regla global de proximidad.

**2692/2863/6813:** los segmentos posteriores explícitos del mismo expositor se conservan con sus propias anclas. Dos filas consecutivas del mismo actor no implican una intervención de otra persona entre ellas.

**1386:** la cesión final vuelve a Corbo; Valdés no habla por ser destinatario de esa cesión, sino desde su presentación efectiva posterior. Sus 833 caracteres y el enlace **1386→1387** se preservan.

**2863→2864:** se leyó completo también 2864, que continúa el desarrollo de Soto sobre IPC transable/no transable. Los residuos **r** y **«A continuación,.»** de los 939 caracteres previos permanecen literales y pendientes de cotejo. No se añade una advertencia bloqueante que rompa esa continuidad; la revisión nueva adjudica sólo la respuesta de 63 caracteres, no certifica integridad de los 939 posteriores.

**2938:** la respuesta de García termina en **«tendrá efectos en los»**. Se recupera lo identificable, sin inventar un complemento ni unirlo al comentario de Marfán. Advertencia de daño acotada a los 51 caracteres.

## 2. Tres intercambios ocultos por texto dañado

### 2463: recuperación parcial

**Céspedes 437 → Velasco 512 revisados y advertidos.**

«El señor i\\/linistro señala…» introduce el planteamiento del Ministro sobre vivienda subsidiada. La nómina **2440** y el intercambio **2462**, leído íntegro, sustentan la interpretación local del cargo. También se leyó 2464, donde Marshall hace su propio comentario sobre aprobación de créditos.

**Las dos frases finales desde «Este dato corresponde…» podrían ser un retorno de Céspedes sin introductor identificable.** No se inventa una frontera ni una certeza de autoría: Velasco es provisional para ese cierre. La advertencia explicita esta limitación. No se modifica i\\/linistro.

### 2525: Ministro, Marshall y Soto

**Velasco 278 → Marshall 216 revisados → Soto 721 revisados → Velasco 98 revisados → Soto 329 explícitos.**

Marshall comenta las compras de departamentos por inversionistas; Soto desarrolla datos de Collect y permisos de edificación; Velasco puntualiza dónde operan los subsidios. No era una exposición única del Ministro.

La nómina **2503** y las identificaciones del propio intercambio sustentan los actores. Se conserva **í\\/larshall**, con advertencia en el tramo de Marshall. Se conserva también **í\\/lacroeconómico** en los 721 caracteres de Soto: esa interpretación local está documentada en su ficha, **sin alias global ni corrección del literal**. La advertencia de Marshall no certifica el cargo de Soto; éste queda por contrastar. El registro de advertencias mantiene un intervalo por padre, sin extender una advertencia fuera de su alcance.

### 2674: un segundo intervalo independiente, no sustitución de la revisión anterior

El primer tramo, antes atribuido enteramente a Soto, queda:

**Soto 2.116 → Marshall 470 revisados → Soto 1.507.**

Marshall objeta comparar tasas con un peak que incluía riesgos de fondeo ya desaparecidos. La nómina **2656** sustenta su identidad local; el apellido **í\\/larshall** queda literal y advertido.

**Los siete segmentos posteriores permanecen iguales en texto, actor y método**, incluidos Cowan, Magendzo, García, Soto, el comentario anterior de Marshall de **1.159**, el retorno de Soto y Velasco. El enlace **2673→2674** permanece.

La ficha **`HAB-20260908-2674`**, inicio **5745**, fin **6905**, no se retira ni se reescribe: se conserva idéntica como revisión adicional, después del nuevo intervalo en orden cronológico. Se verifican todos sus campos y evidencias, además del hash de su ficha. El contenedor JSON cambia, **no la decisión anterior**.

## 3. Un cargo advertido y dos controles negativos

**1904:** lectura completa de De Ramón **3.052** y Cowan **1.358**; ya estaban separados. Se advierte únicamente el cargo de Cowan: **Política l\\/lonetaria** en el discurso frente a **Política Financiera** en la nómina **1851**. No se cambia actor, método, límite ni texto. No se certifican otros residuos, incluidos los de De Ramón.

**854:** lectura completa de **355 caracteres** de Valdés. **1621:** lectura completa del padre, adjudicación de la referencia dentro de los **494 caracteres** finales de Lehmann. En ambos casos **«respondiendo al Consejero…» identifica al destinatario**, no otro hablante. Marfán no vuelve a hablar por aparecer mencionado en la respuesta.

Ambos controles estaban y siguen **sin alerta automática**. Se documentan en `revisiones_menciones_actuales.json` y se validan contra filas exactas, sin tocar texto, actores, límites, anclas o alertas. **No aparecen en `revision_pendientes.csv` precisamente porque no tienen alertas.** No se cuenta su lectura como eliminación de dos alertas.

Total de lecturas actuales: **22 = 21 menciones legítimas + 6185/Bernier pendiente**. Las veinte previas siguen intactas.

## 4. Código acotado y pruebas

Nuevo opt-in **`GERUNDIO_NOMINAL_EXPLICITO_REVISADO`**, sólo para seis predicados: **respondiendo, acotando, comentando, explicando, precisando, agregando**. Se exige separador previo, sujeto nominal explícito compatible y declaración con **que**. La proyección del verbo finito se usa únicamente para reconocer el sujeto, **nunca para reescribir la salida**.

- Rechaza «respondiendo **al**», cargo aislado sin nombre, predicado no autorizado, actor incompatible, cita abierta o ausencia de separador/que.
- No modifica el detector global de turnos ni los alias nominales. No incorpora personas nuevas.
- `GERUNDIO_SENALANDO_EXPLICITO`, ya existente, se usa en 1386/2938; no se amplía silenciosamente para aceptar los otros seis verbos.
- `CONTEXTO_REVISADO` continúa sin crear anclas globales. `Fin` solo no crea cortes. Se mantienen guardas de anclas posteriores y hashes de origen.
- **39 pruebas nuevas:** 23 contratos de fuente/segmentación/conservación y 16 controles de comportamiento. Suite completa **1.336 pruebas**; los contratos anteriores de 2674 se actualizan para añadir el nuevo intervalo sin perder el de 1.159 caracteres.

## 5. Verificación global

Ensayo aislado y `.venv/bin/python scripts/preparar_data.py` completos. **F0/F1 pasan; no certifican pureza total de hablante.**

- **7.219 padres y 2.048.560 palabras conservados**, contra fuentes disponibles y antes/después, ignorando sólo espacios. Raw/external intactos.
- **76 hashes de entradas/código y once de salidas verificados.** Publicación idéntica al ensayo en todos los campos.
- **309 intervalos anteriores conservados**, incluidas todas las evidencias del reordenamiento de 2674. Las **56 advertencias**, veinte lecturas, cinco enlaces revisados y archivo completo de retiro de 6443 anteriores permanecen intactos. Cinco advertencias nuevas; **ningún retiro nuevo**.
- **Ningún enlace entre padres añadido o perdido.** Composición de todos los grupos ajenos a los padres resegmentados conservada; 320 grupos multifila, máximo once. 1386→1387, 2673→2674 y 2863→2864 explícitamente comprobados.
- Veinte padres cambian segmentación y 1904 sólo advertencia. **1387/2864 sólo cambian `ID_Antecedente_Continuidad`**, además de IDs secuenciales: referencias actualizadas al segmento correcto, no nuevas adjudicaciones. Los otros **7.196 padres** conservan todos los campos no secuenciales.
- Esquemas **37/24**, 21 fórmulas, 132 sesiones, 310 contrastes TPM y tres documentos preservados. CSV TPM/documentos comparados salvo IDs secuenciales. **Larraín autor escrito ≠ Vergara lector**, sin inferir asistencia/habla oral del autor.
- Controles anteriores intactos: García de once filas y 224→225→226; 3454→3455; 2695→2696, 2754→2755, 2790→2791; cinco enlaces revisados; 506/1572, 780, 6009/6025/6443, 4594, Nacrur/Mattar/Álvarez, 4054, 3110 y anclas 780/1092/2790/2778/2909. No reaparece 5402→5403. LOOP21/Araya y sus alias estrechos siguen intactos.

**392 filas advertidas no son 392 errores confirmados.** El incremento incluye prefijos de consulta que ahora terminan en la coma conservada antes de la respuesta, además de advertencias de nombre/cargo/daño. No se borra puntuación para reducir métricas.

### Cola histórica: cambio principal no equivale a cierre residual

- **4179/2938:** pendiente contextual → corrección dirigida; conserva final sin puntuación y daño.
- **4302/3028:** segmentación/actor modificado → corrección dirigida; conserva final sin puntuación.

Quedan **102 pendientes contextuales**, **499 comparaciones / 181 lecturas dirigidas / 103 triajes**; 283 intervalos históricos con alertas actuales y seis intervalos independientes con variante de identidad. Hay **21 filas actuales** con variante Ricaurte, sin resolver equivalencias globales.

Las ocho menciones legítimas históricas no equivalen a las **21 actuales**. No se suman estas unidades ni se interpreta el estado principal como cierre de los motivos residuales.

## 6. Alcance y pendientes

El barrido dirigido de respuestas produjo **47 ventanas nominales discrepantes**: incluía respuestas efectivas, destinatarios de consultas, referencias pasadas, cesiones y metadatos. El barrido de signos dañados produjo otras **17 ventanas**, varias ya revisadas o simples residuos. **No son 64 lecturas integrales ni una muestra independiente**. También se leyeron 3348 y 4513, sin nueva adjudicación: el primero ya separaba el diálogo; el segundo mantiene el agradecimiento a Marfán y la exposición propia de Vergara.

Siguen 2463 (posible retorno final), nombre/cargo dañado de 2525/2674, restos de 2863/2938/1904; los pendientes anteriores 226/3454, 6185, puente de 780, 4745→4746, 6561→6562, pasajes conjuntos —incluido 4446— e identidades. Una presentación larga no es un párrafo roto. **No se reconstruye texto ni se certifica la causa de su daño.**

Sin nuevo cotejo PDF ni muestra independiente con/sin alertas; sin proceso activo al cerrar. Validaciones locales; workflow de GitHub Actions fuera del PR.
