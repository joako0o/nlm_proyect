# LOOP20 — Cambios de hablante sin alerta, aperturas y menciones referidas

**2026-09-08 · [PR #3](https://github.com/joako0o/nlm_proyect/pull/3)**

Base: `34bacf35c9594e79f795c9f8685688c554f355f5`, [LOOP19](REVISION_LOOP19_2026-09-08.md).
Lectura dirigida por agente del texto disponible. **Sin nuevo cotejo PDF ni muestra independiente con/sin alertas.**

## Resultado publicado

| Medida | LOOP19 | LOOP20 |
|---|---:|---:|
| Filas físicas / bloques de texto | 9.551 / 9.550 | **9.571 / 9.570** |
| Grupos de turno | 9.136 | **9.155** |
| Grupos multifila / máximo | 319 / 11 | **320 / 11** |
| Filas con alertas / padres alertados | 349 / 309 | **361 / 318** |
| Pruebas | 1.230 | **1.270** |
| Intervalos revisados / padres con revisión | 279 / 262 | **296 / 278** |
| Advertencias contextuales activas | 39 | **49** |
| Lecturas actuales | 11 legítimas + 1 pendiente | **19 legítimas + 1 pendiente** |

Se separan intervenciones en **16 padres**, mediante **17 intervalos revisados nuevos**. Se añaden **ocho lecturas de menciones** sin cortar las exposiciones y **una advertencia sin reasignación en 1013**. Se documenta además la continuidad **2836→2837** de Marshall. Son clases de actuación diferentes, no un conteo único de errores corregidos.

**Quince de los dieciséis padres resegmentados no tenían ninguna alerta.** En 205, la fila que absorbía el cambio de hablante tampoco tenía alerta; sí existía otra fila de Marfán con final sin puntuación. El barrido fue dirigido, no una muestra representativa.

- [Comparación global y hashes](comparacion_loop20_2026-09-08.json)
- [Filas antes/después](cambios_loop20_2026-09-08.csv)
- [Checkpoint y pendientes](estado_revision_loop20_2026-09-08.json)

## 1. Intercambios recuperados sin dividir por meras referencias

Se leyeron los desarrollos completos de los padres de esta tabla y su contexto pertinente. Caracteres por tramo de salida; las palabras y signos de origen se conservan.

| Padre | Secuencia resultante |
|---|---|
| **205** | Desormeaux **549** → Marfán **310** → García **126** → **Marfán 1.047 revisados** → García **442** |
| **510** | Valdés **322** → García **1.165** → **Marfán 593 revisados** → Herrera **926** |
| **663** | Valdés **332** → **Magendzo 347 revisados** → Magendzo **370 explícitos** → Marfán **316** → Magendzo **661** → Desormeaux **304** → Valdés **660** |
| **1072** | Corbo **75** → **Velasco 245 revisados** |
| **2810** | Marshall **153** → **Lehmann 274 revisados** → Lehmann **932 explícitos** → Marfán **481** → Lehmann **1.812** |
| **4916** | Vergara **145** → **Herrera 341 revisados** → Vergara **237** |
| **5366** | Marfán **1.169** → **Marshall 468 revisados** |
| **6021** | **De Ramón 1.265 revisados** → Claro **496** → **Vial 2.048 revisados** → Claro **495** |
| **7182** | Fuentes **2.173** → **Marcel 214 revisados** |

- **205:** «desea agregar» introduce la objeción de Marfán a la Minuta; el regreso de García queda separado. No se atribuye a Marfán la respuesta previa de García sólo porque lo menciona.
- **510:** el comienzo de Marfán estaba concatenado tras «no cambios de». Se utiliza la excepción acotada de concatenación ya existente, sin completar la frase de García.
- **663:** «Señala también el señor Magendzo» introduce su comentario sobre minería, no una continuación de Valdés. El posterior desarrollo nominal de Magendzo sobre salarios mantiene sus límites y ancla.
- **1072:** «replica» introduce la contestación actual de Velasco a Corbo. Se mantiene el comentario presidencial breve: no se borra por su extensión.
- **2810:** «a lo cual el señor Lehmann muestra que» es una explicación en respuesta a Marshall. Se conserva el conector y la frase literal, así como la intervención posterior de Marfán.
- **4916:** Herrera comparte el planteamiento presidencial y anuncia una presentación futura de Soto. **«presentará» no se convierte en un turno de Soto.** La cesión final vuelve a Vergara.
- **5366:** se recupera a Marshall; el rótulo espaciado del Banco permanece al final del tramo previo de Marfán, sin inventar una voz institucional.
- **6021:** el comienzo «comienz» había permitido que Claro absorbiera la respuesta de De Ramón; «lo plantado» había ocultado el desarrollo de Vial. Se recuperan ambos, conservando literalmente esas formas y el retorno final de Claro.
- **7182:** Marcel pide precisar el tratamiento del reajuste público. Se conserva «solicite». La respuesta de **Naudon en 7183**, leída como contexto, no se atribuye a Fuentes ni a Marcel.

Las etiquetas se contrastan con nóminas de sesión y discurso, no con asistencia sola: 201, 505, 655, 1059, 2803, 4900, 5332, 6008 y 7157, respectivamente. No se añaden identidades ni alias globales.

## 2. Comienzos de exposiciones absorbidos por la voz anterior

| Padre | Resultado |
|---|---|
| **1728** | De Gregorio **75** → **Velasco 1.023 revisados** → Velasco **2.296 explícitos** |
| **2695** | De Gregorio **192** → **Soto 433 revisados** → Soto **1.020 explícitos** |
| **2754** | Claro **7.258** → **Marshall 732 revisados** → Marshall **2.603 explícitos** |
| **2836** | Claro **3.545** → **Marshall 142 revisados** |
| **6800** | Vergara **141** → **Vial 3.564 revisados** → Vial **151 explícitos** |

**1728:** la cesión presidencial termina en «señor Andrés» y el comienzo siguiente dice «señor a Andrés Velasco». Se identifican los turnos, pero no se reparan esos residuos.

**2695:** se conserva «X -» al final de la cesión, y la exposición de Soto continúa sin inventar pausas por sus indicadores sectoriales. La nómina 2689 sustenta su cargo/nombre.

**2754:** se mantiene completo el voto y desarrollo de Claro sobre la FLAP, de **7.258 caracteres**, incluida la referencia a Cowan. Sólo «toma la palabra … Marshall» introduce al siguiente expositor. También se conserva completo el desarrollo posterior de Marshall. La nómina 2713 identifica a los participantes.

**2836→2837:** la introducción/agradecimiento de Marshall y su exposición del padre siguiente se leyeron íntegramente y se agrupan por una nueva continuidad acotada. La nómina de la sesión es 2803. **No se fusionan textos:** el extremo revisado sigue sin ancla y el posterior conserva su propia ancla explícita.

**6800:** las felicitaciones dirigidas a Valdés y el desarrollo económico pertenecen a Vial, no a Vergara. Valdés es destinatario del saludo, no una voz intercalada. Se conserva la reiteración final explícita de Vial de **151 caracteres**. Nómina 6755.

En **663/1728/2695/2754/2810/6800** se utiliza `Cita_Ancla_Posterior` para conservar la evidencia explícita posterior. Dos segmentos contiguos del mismo expositor no implican otro hablante. **`Fin` solo no crea un corte y `CONTEXTO_REVISADO` no habilita herencia global.** Continúan intactos **2695→2696** y **2754→2755**.

## 3. Aperturas presidenciales mezcladas con las nóminas

- **2803:** Consejo/nómina **1.445** → De Gregorio/apertura **296**.
- **2969:** Consejo/nómina **1.661** → De Gregorio/apertura **301**.

Se separan únicamente la apertura y la fijación de calendario explícitas de De Gregorio. Los asistentes, invitados, cargos y residuos de la nómina siguen como texto institucional; no se infieren intervenciones de ellos. Se mantienen los finales **«A continuación,.»** y el residuo **«/ )»** de 2969.

### Dos nuevos tipos de límite, sólo por revisión acotada

- **`APERTURA_POST_NOMINA_REVISADA`:** un único intervalo al final de una cabecera, con sujeto presidencial explícito compatible. Exige nómina previa, límite final completo y ausencia de cita abierta; sin opt-in, la cabecera conserva su tratamiento anterior. Se rechaza en un párrafo ordinario, con otro actor o con un final parcial.
- **`RESPUESTA_A_LO_CUAL_MUESTRA_REVISADA`:** exige la cláusula nominal «a lo cual el señor … muestra que», separador previo y actor explícito compatible. Se proyecta «muestra que» como «señala que» **sólo para validar el sujeto**, nunca para modificar la salida. No se amplía globalmente el vocabulario de verbos ni se convierte una mención en un turno.

Ambos tipos dependen de hashes, fecha, límites y evidencia del registro. Construcción y pruebas rechazan alteraciones; los demás padres no reciben estas excepciones.

## 4. Ocho menciones leídas, sin cortes ni retirada de alertas

| Padre | Intervalo completo leído | Decisión acotada |
|---|---:|---|
| **571** | Desormeaux, **4.683** | Refiere lo señalado recientemente por el gerente como argumento de su propio voto. |
| **647** | Velasco, **3.785** | Recuerda argumentos de gerencias dentro de sus dudas y recomendación. |
| **1114** | Valdés, **471** | Alude a los riesgos expuestos antes por De Ramón; se comprobó el contexto 1113. |
| **1328** | Desormeaux, **204** | Recuerda expresamente la exposición que realizó Magendzo. |
| **1338** | Jadresic, **3.316** | Valdés es una presentación futura y Magendzo un comentario referido; no nuevos turnos. |
| **1574** | Lehmann, **1.617** | Responde a Marshall y refiere el gráfico comentado por Marfán en 1573. |
| **2397** | Claro, **1.537** | Cuestiona el escenario de Lehmann, quien responde recién en 2398. |
| **2430** | De Ramón, **4.002** | Desarrolla tres hechos y refiere el análisis previo de la Gerencia de Estudios. |

Los otros segmentos de 1338 y 1574 mantienen sus separaciones. Estas lecturas **no modifican textos, actores, límites, anclas ni alertas automáticas**. Tampoco certifican otros motivos, la integridad del OCR o el corpus.

Ahora hay **20 lecturas actuales = 19 menciones legítimas + 1 pendiente (6185/Bernier)**. Se preservan íntegros los doce registros anteriores. Las ocho nuevas decisiones no resuelven por analogía la atribución a Bernier. El campo heredado `menciones_actuales_documentadas` cuenta registros; `lecturas_actuales_por_estado` distingue los estados. No equivalen a las **ocho menciones legítimas históricas** de la cola de 783.

## 5. Daño visible, sin restauración inventada

Se añaden diez advertencias acotadas de daño/residuo: **205/510/1013/1728/2695/2803/2969/5366/6021/7182**. Las nueve asociadas a resegmentaciones no certifican la integridad de los otros tramos del padre.

**1013 es sólo advertencia:** se leyó su desarrollo de Valdés de **2.471 caracteres**. Los argumentos atribuidos a Jadresic y Schmidt-Hebbel son la comparación que efectúa Valdés; no se separan por aparecer sus nombres. Se advierte el final incompleto antes de «V Finalmente», sin cambiar actor, método o límites. Los otros tramos tampoco se certifican con este aviso.

Las **361 filas con alertas** no son 361 errores confirmados. El aumento incorpora nuevos intervalos de daño y finales que quedan visibles después de separar las voces. Los motivos se superponen: **24 avisos de daño**, **266 finales sin puntuación**, 20 posibles otras voces/menciones y 21 variantes de identidad, entre otros; no se suman como casos independientes.

## 6. Verificación global

**1.270 pruebas**, cuarenta nuevas: **26 contratos exactos de fuente/segmentos y 14 controles de comportamiento/evidencia**. Ensayo aislado y `python scripts/preparar_data.py` terminados correctamente. **F0/F1 sin errores bloqueantes**; publicación idéntica al ensayo campo por campo.

- **74 hashes de entradas/código y once de salidas verificados.** Fuentes raw/external intactas.
- **7.219 padres y 2.048.560 palabras conservados**, reconstruyendo contra fuentes disponibles e ignorando sólo espacios. 132 sesiones y 310 contrastes TPM.
- **279 intervalos revisados, 39 advertencias y doce lecturas anteriores idénticos**. Las cuatro continuidades revisadas previas también. Ningún retiro nuevo; archivo completo del retiro de la advertencia obsoleta de 6443 intacto.
- **Ningún enlace anterior perdido; sólo 2836→2837 añadido.** Miembros de todos los grupos ajenos a los padres resegmentados/nueva unión conservados. Incluye García de once filas, 224→225→226, 3454→3455, 2790→2791 y las cuatro uniones de LOOP19. No reaparece 5402→5403.
- **21 padres cambian campos no secuenciales:** 16 estructurales; 1013, advertencia; 2696/2755, actualización del identificador del antecedente sin cambiar su vínculo; 2837, nuevo enlace; 6857, recálculo de duplicado de una fórmula ahora recuperada en 6800. Los otros **7.198 padres** mantienen esos campos, excluyendo `ID` e `ID_Turno`.
- Esquemas XLSX **37/24**, **54 etiquetas nominales**, 21 fórmulas y tres documentos leídos intactos. **Larraín autor escrito ≠ Vergara lector**, sin inferir presencia ni habla oral del autor. Se compararon los CSV: TPM sólo cambia IDs de evidencia y documentos sólo su ID físico; el resto de sus campos es idéntico.
- Se conservan 506/1572, recuperación parcial de 780, 6009/6025/6443, 4594, Nacrur/Mattar/Álvarez, 4054 tras el comunicado, 3110 institucional y las anclas 780/1092/2790/2778/2909. Siguen **21 filas actuales** con variante Ricaurte, sin resolver equivalencia global.

La cola histórica mantiene **104 pendientes de lectura contextual**, **500 comparaciones / 178 lecturas dirigidas / 105 triajes**, seis intervalos con variante de identidad y 283 intervalos históricos con alertas actuales. Un estado principal no cierra motivos residuales. No se suman estas unidades con las filas actuales.

## 7. Alcance y siguientes pendientes

El barrido de sujetos/verbos produjo candidatos, incluidos encabezados, asistencias y referencias que no se convirtieron en voces. Las lecturas dirigidas y las correcciones se distinguen del triaje. **No se certifica exhaustivamente el corpus ni se ha realizado una muestra independiente.**

Siguen pendientes 226/3454, 6185, el puente de 780, 4745→4746 y 6561→6562, residuos conjuntos, nombres/cargos e identidades. El texto aparentemente incompleto no se repara con palabras inventadas y no se atribuye automáticamente a fallos del OCR sin cotejo de fuente. Una presentación larga no es un párrafo dañado.

Sin proceso activo. Verificaciones locales; el workflow de GitHub Actions continúa fuera del PR.
