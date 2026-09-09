# LOOP21 — Consultas, respuesta del Fiscal y exposiciones absorbidas

**2026-09-08 · [PR #3](https://github.com/joako0o/nlm_proyect/pull/3)**

Base: `115ad489f20877c923fa2301d7f3079860769bc3`, [LOOP20](REVISION_LOOP20_2026-09-08.md).
Lectura dirigida por agente del texto disponible. **Sin nuevo cotejo PDF ni muestra independiente.**

## Resultado publicado

| Medida | LOOP20 | LOOP21 |
|---|---:|---:|
| Filas físicas / bloques | 9.571 / 9.570 | **9.584 / 9.583** |
| Grupos / grupos multifila | 9.155 / 320 | **9.168 / 320** |
| Máximo de filas por grupo | 11 | **11** |
| Filas advertidas / padres advertidos | 361 / 318 | **370 / 325** |
| Pruebas | 1.270 | **1.297** |
| Intervalos revisados / padres con revisión | 296 / 278 | **309 / 288** |
| Advertencias contextuales activas | 49 | **56** |
| Etiquetas nominales observadas | 54 | **55** |

**Ocho padres resegmentados y cuatro con cambios sólo de metadatos/advertencias.** Se añaden trece intervalos de hablante en diez padres: once intervalos estructurales y dos de documentación nominal/cargo. Los otros dos padres reciben advertencias sin adjudicación de hablante.

Siete de los ocho padres resegmentados estaban sin alertas. **6862 ya tenía un final sin puntuación**, pero no las separaciones recuperadas aquí. No se deduce pureza de hablante de la ausencia de alertas.

- [Comparación global, fuentes y hashes](comparacion_loop21_2026-09-08.json)
- [Detalle de filas antes/después](cambios_loop21_2026-09-08.csv)
- [Checkpoint y pendientes](estado_revision_loop21_2026-09-08.json)

## 1. Consultas y retornos separados

| Padre | Secuencia resultante; caracteres por tramo |
|---|---|
| **280, sólo el tramo final** | Herrera **846** → **Eyzaguirre 100 revisados** → Herrera **496** |
| **631** | Lehmann **106** → **Velasco 59 revisados** → **Lehmann 182 revisados** |
| **2141** | De Gregorio **181** → **Marfán 774 revisados** |
| **2646** | De Gregorio **149** → Cowan **1.781** → **De Gregorio 147 revisados** |
| **3012** | De Gregorio **109** → **De Ramón 375 revisados** → De Ramón **1.867 explícitos** |
| **5199** | Marshall **204** → **Soto 634 revisados** |

**280:** la pregunta «Consulta nuevamente el señor Ministro…» interrumpe la explicación de Herrera sobre liquidez y reserva técnica; Herrera responde después. Se leyó completo el intervalo final de **1.444 caracteres** y contexto breve. **No se leyó ni adjudicó nuevamente la exposición anterior de García de 30.150 caracteres**: se conserva exactamente y se verifica mecánicamente, junto con los otros cuatro segmentos previos.

**631:** se conserva la pregunta breve del Ministro y su coma final. «a lo cual … responde afirmativamente» delimita el retorno de Lehmann, no una referencia. La brevedad no justifica eliminar la pregunta.

**2141:** se recupera el comentario propio de Marfán sobre primas de riesgo. Se conserva y advierte **«Manual Marfán»**; la nómina 2128 sustenta el nombre local Manuel Marfán Lewis.

**2646:** la cesión final corresponde a De Gregorio, no a Cowan. Velasco es destinatario de la cesión y comienza su exposición en 2647; no se adelanta su turno por la mención.

**3012:** «quien hace presente…» introduce la exposición efectiva de De Ramón después de recibir la palabra. Se conserva la cesión presidencial en minúscula y la identificación posterior explícita de De Ramón con su ancla. La nómina 2969 sustenta su cargo/nombre.

**5199:** el cargo expreso Análisis Macroeconómico, su titular en la nómina 5161 y el cierre nominal de Soto en 5200, leído completo, sustentan su desarrollo después de Marshall. No se atribuye sólo por tema/proximidad.

Las nóminas de 280/631/2646 son 279/626/2604, respectivamente. Asistencia y cargo apoyan la identificación, pero no constituyen por sí solos evidencia de una intervención.

## 2. 518: exposición de opciones, no discurso del Presidente

Se conserva la secuencia previa de Corbo **101**, Eyzaguirre **221**, Corbo **128** y reanudación institucional **73**. El último segmento anterior, de **6.263 caracteres**, queda así:

**Corbo 252 → Valdés 5.935 revisados → Corbo 74**.

Se leyó completo el desarrollo de opciones y su contexto. «El señor Gerente de División mencionado informa…» retoma un referente incompleto en el propio párrafo: **517 nombra al Gerente de División Estudios Rodrigo Valdés** y **520 se refiere al análisis presentado por esa Gerencia**. Es una atribución contextual acotada, no un ancla general que atraviese suspensiones de sesión.

Se conserva la exposición completa, incluidas sus enumeraciones. El salto **7→9** no se repara inventando el numeral 8; tampoco se elimina la **H** del prefijo presidencial. Se añade advertencia de daño/integridad por cotejar, sin certificar su causa ni reconstruir contenido. El final donde Corbo ofrece la palabra permanece independiente.

## 3. 6862: Fiscal, cesión presidencial y exposición de Micco

La secuencia pasa de tres a seis segmentos:

**Vergara 213 → Araya 164 revisados → Vergara 155 revisados → Micco 1.302 revisados → Micco 642 explícitos → Vergara 2.292**.

La nómina **6810** identifica a **Juan Pablo Araya Marco, Fiscal y Ministro de Fe**. La solicitud nominal de Vergara seguida de «indicando el señor Fiscal que…» delimita su respuesta sobre el procedimiento. **La primera mención a Araya es el destinatario de la pregunta, no el inicio de su respuesta.**

Después, Vergara concede la palabra con el consentimiento de los consejeros. Micco se disculpa y desarrolla su evaluación económica: ese comienzo no pertenece a Vergara ni al Fiscal. Se conserva su segmento posterior explícito de **642 caracteres**, así como el retorno final de Vergara. El residuo **r** queda literal al final de los 1.302 caracteres recuperados y se advierte.

Se mantiene la etiqueta previa **Alejandro Micco**, sin realizar una armonización nominal nueva. La incorporación de Araya aumenta a **55 las etiquetas nominales observadas**, 54 personales y el Consejo: no es un censo independiente de identidades ni resuelve las variantes Ricaurte.

## 4. Tres excepciones acotadas, sin nuevas reglas generales de habla

1. **`RESPUESTA_A_LO_CUAL_EXPLICITA`**: variante de respuesta nominal; exige conector, separador previo y sujeto explícito compatible. No divide por cualquier «a lo cual».
2. **`CESION_HACE_PRESENTE_RELATIVA_EXPLICITA`**: exige cesión contigua, cedente y destinatario identificables y comienzo «quien hace presente que». El modo anterior de relativas no se amplía silenciosamente; cada variante requiere opt-in.
3. **`GERUNDIO_INDICANDO_FISCAL_EXPLICITO`**: exige una consulta nominal contigua «solicita al Fiscal señor … que precise…» y respuesta «indicando el señor Fiscal que…». El nombre se proyecta únicamente para validar el sujeto de esa respuesta, sin reescribir el texto. **Fiscal no se convierte en un alias global de Araya** ni basta un cargo aislado sin antecedente. Sus alias se restringen a Juan Pablo Araya / Juan Pablo Araya Marco: no se generan Marco ni sólo Juan Pablo.

Las revisiones llevan hashes, fecha, límites y citas. Hay rechazos por actor incompatible, falta de consulta contigua, cambio de predicado/conector, cita abierta o fuente modificada. **`CONTEXTO_REVISADO` no crea anclas globales**, y las anclas posteriores de 3012/6862 se conservan.

## 5. Cuatro padres sólo con metadatos o advertencias

- **632, Lehmann 587:** leído íntegro el intercambio y documentada su respuesta ya separada. Se advierte **Lehmman**, sin cambiar su actor, texto o límites y sin añadir alias generales.
- **4289, Lehmann 8.677:** leída íntegra su exposición internacional. El interior dice **«Gerente de Análisis Macroeconómico señor Lehmann»**, contradiciendo el cargo de nómina 4282 y otras identificaciones dentro del propio desarrollo. Se documenta la atribución y se advierte el cargo; **no se transfiere la exposición a Soto ni se corrige el literal**. Las preguntas referidas del Presidente/Claro no crean nuevos turnos.
- **520, Jadresic 2.821:** su tramo ya estaba separado de Herrera. Se leyeron ambos desarrollos y se advierte el final **«no se han»**, sin completar la conclusión ni modificar actor, método o límites.
- **4446, último tramo 484:** entre el agradecimiento y la cesión de De Gregorio aparece una **adhesión conjunta de Marshall, Claro y Vergara**. Se añade `PASAJES_CONJUNTOS_POR_DELIMITAR`; no se fabrican tres turnos ni se adjudica la adhesión a uno de ellos. La etiqueta de De Gregorio queda explícitamente provisional para esa fila compuesta. Las intervenciones previas de homenaje, suspensión y reanudación se conservan.

Siete advertencias nuevas en total: **518/520/632/2141/4289/4446/6862**, que se superponen con algunas alertas automáticas. **370 filas advertidas no equivalen a 370 errores confirmados.**

## 6. Verificación y preservación global

**1.297 pruebas**, 27 nuevas: **doce contratos exactos de fuente/segmentos y quince controles de comportamiento/evidencia**. Ensayo aislado y `python scripts/preparar_data.py` completos. **F0/F1 pasan**; publicación idéntica al ensayo campo por campo.

- **75 hashes de entradas/código y once de salidas verificados.** Fuentes raw/external intactas.
- **7.219 padres y 2.048.560 palabras conservados**, reconstruyendo contra fuentes disponibles e ignorando sólo espacios. 132 sesiones, 310 contrastes TPM.
- **296 revisiones anteriores y 49 advertencias anteriores idénticas**, igual que las veinte lecturas actuales, los cinco enlaces revisados y el archivo completo del retiro de la advertencia obsoleta de 6443. Ningún retiro en esta pasada.
- **Ningún enlace entre padres añadido ni perdido.** Composición de todos los grupos ajenos a los padres resegmentados conservada; 320 grupos multifila, máximo once. García, 224→225→226, 3454→3455, 2695→2696, 2754→2755, 2790→2791 y las cinco uniones revisadas intactos. No reaparece 5402→5403.
- Sólo los **doce padres indicados** cambian campos no secuenciales. Los otros **7.207** mantienen esos campos, excluyendo `ID` e `ID_Turno`. La incorporación nominal de Araya no altera otros padres.
- Esquemas XLSX **37/24**, 21 fórmulas y tres documentos leídos preservados. Se compararon los CSV: TPM sólo cambia IDs de evidencia; documentos, IDs físicos y un ordinal de `ID_Turno`. Contenido, autor y lector permanecen iguales: **Larraín autor escrito ≠ Vergara lector**, sin inferir presencia ni habla oral del autor.
- Recuperaciones previas intactas: 506/1572, 780, 6009/6025/6443, 4594, Nacrur/Mattar/Álvarez, 4054, 3110 y anclas 780/1092/2790/2778/2909. Siguen **21 filas actuales** con variante Ricaurte, sin cierre de equivalencia global.

### Cola histórica y unidades que no deben confundirse

El intervalo histórico **8653, padre 6862**, pasa de pendiente contextual a corrección dirigida aplicada. Conserva los motivos residuales de daño/final sin puntuación. La cola queda en **103 pendientes contextuales**, **500 comparaciones / 179 lecturas dirigidas / 104 triajes**, seis intervalos independientes con variante de identidad y 283 intervalos históricos con alertas actuales.

Las lecturas actuales siguen siendo **20 = 19 menciones legítimas + 1 pendiente (6185/Bernier)**; no se añadieron ni cerraron lecturas de esa clase en LOOP21. Son unidades distintas de las ocho menciones legítimas históricas. Los conteos no se suman y un estado principal no cierra todos sus motivos residuales.

## 7. Alcance pendiente

Los barridos de nombres, roles y predicados fueron **triaje dirigido**, no auditoría representativa. Se descartaron como cortes las asistencias, declaraciones de figuras extranjeras y referencias a economistas externos; las ventanas de triaje no equivalen a lecturas integrales.

Siguen 226/3454, 6185, el puente de 780, 4745→4746 y 6561→6562, los pasajes conjuntos —incluido ahora 4446—, nombres/cargos e identidades. Una presentación larga no es un párrafo dañado. **Sin nuevo cotejo PDF ni muestra independiente con/sin alertas; no se certifica pureza semántica total.**

Sin proceso activo. Validaciones locales; el workflow de GitHub Actions continúa fuera del PR.
