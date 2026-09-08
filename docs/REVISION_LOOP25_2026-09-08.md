# LOOP25 — Intervenciones omitidas y opiniones leídas por terceros

**Base comparada:** `2344c3e3f2e365ebb917adfd60ee43210d4787d2` (LOOP24).

**Resultado:** once padres corregidos, todos previamente sin alertas: ocho con recuperación de habla personal y tres con separación de autor y lector. Además, cinco lecturas de referencias y dos advertencias textuales. **1.434 pruebas aprobadas**, F0/F1 sin bloqueos y publicación validada. Sin nuevo cotejo PDF ni muestra independiente.

## 1. Alcance de lectura

Lectura completa de dieciséis padres: **77, 586, 1004, 1042, 1456, 1627, 1680, 2167, 2698, 2918, 2948, 4453, 4507, 4722, 4926 y 6073**. Las nóminas pertinentes se utilizaron como evidencia de sesión. No se afirma nueva lectura completa de todos los controles históricos ni de los candidatos encontrados mediante barridos.

El descubrimiento combinó pasivas, gerundios, cesiones, cláusulas, predicados pospuestos e inicios de oración. Los resultados de los barridos contienen referencias, asistencia, nombres que coinciden con palabras comunes y casos ya resueltos. **No son una muestra representativa ni un recuento de errores.**

## 2. Ocho recuperaciones de habla personal

Siete resegmentaciones y una reasignación sin nuevas filas. Longitudes de las filas exportadas, incluidos espacios; los separadores entre filas se conservan sin reescribir el contenido.

| Padre | Cambio | Conservación y límites |
|---|---|---|
| **586** | Eyzaguirre 800 → Eyzaguirre **208**, Marfán **591** | «Al Consejero señor Marfán, le parece…» inicia su planteamiento sobre tasa neutral. García **553**, Marfán **916** y García **612** posteriores permanecen íntegros. |
| **1627** | De Ramón 581 → De Ramón **321**, Marshall **259** | Nuevo sujeto en oración autónoma: «hizo presente… e indica…». García responde después. Conservar García **609**, De Ramón **327** y Marfán **516**. No habilitar globalmente verbos pasados. |
| **1680** | Consejo 245 → Recart **245** | Recart informa al Presidente que debe retirarse; no es sólo registro de asistencia/salida. Nómina confirma identidad y subrogancia. Marshall **5991**, con su voto completo, intacto. |
| **2698** | Claro 2428 → Claro **823**, García **1604** | García analiza salarios nominales tras la consulta de Claro. De Gregorio **409** previo permanece independiente. |
| **2918** | De Gregorio 275 → De Gregorio **59**, Soto **215** | Confirmación y explicación nominal de Soto; conservar «confirmando» y la coma del planteamiento anterior. |
| **2948** | Marfán 1450 → Marfán **785**, De Ramón **664** | De Ramón detalla operaciones de divisas. Conservar US$5.000, US$2.000 y US$1.000 sin alterar cifras, y advertir el final incompleto. |
| **4926** | Soto 2114 → Soto **1751**, Vergara **148**, Soto **213** | Opinión presidencial entre exposición y respuesta de Soto. Conservar «A juicio de Presidente…» literalmente y el retorno explícito de Soto. |
| **6073** | Lehmann 1955 → Lehmann **92**, Claro **1862** | Claro cita hechos sobre China y desarrolla su evaluación. La referencia interna a Vial y a declaraciones chinas no abre nuevos turnos. |

Se incorporan **ocho intervalos personales**: total **371 en 342 padres**. Los **363 intervalos anteriores permanecen idénticos**, comparados de forma aplanada para no confundir raíces con intervalos adicionales.

Sólo se añade un tipo personal, `GERUNDIO_CONFIRMACION_NOMINAL_REVISADA`, para la forma nominal «confirmando». Requiere revisión individual, hash, coma/separador, sujeto compatible y declaración. El tipo anterior de gerundio no se amplía. Las demás decisiones usan el mecanismo de intervalos revisados ya existente, sin nuevos alias ni expansión global de «detalla», «cita» o «hizo presente».

El caso **1627** no se equipara a cualquier verbo pasado: hay una oración autónoma con Marshall como sujeto, un «e indica» presente y respuesta posterior de García. Las referencias retrospectivas de **1013** permanecen intactas.

## 3. Tres opiniones recibidas para lectura

Cada padre se conserva completo en cuatro partes: palabras propias del Presidente → anuncio de lectura → opinión de Larraín → retorno del Presidente a la votación.

| Padre | Palabras propias | Anuncio del lector | Texto de Larraín | Retorno del lector |
|---|---:|---:|---:|---:|
| **4453** | De Gregorio **448** | De Gregorio **227** | **4713** | De Gregorio **136** |
| **4507** | Vergara **132** | Vergara **227** | **6007** | Vergara **135** |
| **4722** | Vergara **119** | Vergara **239** | **6828** | Vergara **250** |

**Autor ≠ lector ≠ asistencia.** Larraín es autor del planteamiento leído; no se registra una intervención oral ni se deduce su presencia. Cerda es intermediario, no autor ni lector de la cita. El destinatario de la cesión final tampoco se convierte en hablante dentro de ella.

### Distinción de procedencia

- **4722** dice literalmente «por escrito» y utiliza la modalidad documental existente.
- **4453/4507** dicen que el Presidente recibió el planteamiento de Larraín por intermedio de Cerda y que dará lectura a continuación. **No dicen literalmente «por escrito».** La modalidad opt-in `PLANTEAMIENTO_RECIBIDO_PARA_LECTURA` valida esa introducción completa, la autoría anunciada y la cita delimitada. No certifica el formato original del envío.
- El retorno en 4453/4507 comienza «A continuación… da paso a la votación». La modalidad `CESION_TRAS_LECTURA_REVISADA` exige una cita de retorno exacta y un sujeto presidencial compatible. La proyección verbal sólo sirve para validar al lector; no modifica la frase exportada.

Las modalidades son individuales, con hash y límites. No hay detección documental global por proximidad. Se rechazan procedencias genéricas, modalidades desconocidas, cambios de cita, desplazamientos de comillas, actor/lector incompatible e inferencias de asistencia.

**Seis documentos registrados en total.** Las tres fichas anteriores de **5212/5742/5802** permanecen idénticas. Sus registros documentales exportados también, salvo IDs secuenciales. Los cuerpos citados no se dividen por personas mencionadas dentro de ellos. Las bases mantienen los esquemas **37/24**.

## 4. Referencias y daño textual

Cinco lecturas nuevas, sin reasignar voces:

- **77/256:** Corbo refiere lo señalado por Desormeaux.
- **1042/176:** Corbo evalúa elementos señalados por el Ministro.
- **1456/325:** la relativa «quien ha solicitado…» explica por qué Corbo cede la palabra; García habla después en su segmento de **974** caracteres.
- **2167/229:** «quien desea efectuar un alcance…» anuncia la intención del Ministro. Velasco interviene después en **558** caracteres; el voto previo de Marshall de **7298** queda completo.
- **1004/1422:** Marfán compara su hipótesis con la de Valdés; es referencia interna, no nuevo turno. La lectura no cierra el daño textual de esa fila.

**33 lecturas actuales = 30 menciones legítimas + 3 pendientes: 6185, 3775 y 4055.** Las 28 fichas anteriores permanecen intactas. Los cuatro controles sin alerta —77, 1042, 1456 y 2167— se validan en el registro pero no aparecen en `revision_pendientes.csv`. La referencia de 1004 sí es visible allí porque conserva una advertencia independiente.

**70 advertencias contextuales = 68 anteriores + 2 nuevas**, sin retiros:

- **1004/1422:** cláusula incompleta «Lo anterior, se observa menos porque V Por otra parte…». Se conserva sin reconstruir ni atribuir otra voz por el daño.
- **2948/664:** final «A continuación,.» de De Ramón. La separación de su intervención no permite completar ese final.

El residuo «se ha H agregado» de Marshall en 2167 también se conserva; no se certifica la integridad textual de esa exposición por haber adjudicado la cesión presidencial. Una exposición larga no es un párrafo roto por su longitud. Sin cotejo no se identifica con certeza el origen del daño.

Los tres retiros anteriores —6443, 2704 y 2661— permanecen exactamente iguales. **4055** sigue pendiente de una delimitación institucional/conjunta; no se modifica ni se inventan cuatro voces para cerrar su aviso. También siguen pendientes 6185/Bernier y 3775/Cerda.

## 5. Cola visible y duplicados

Las filas con alertas pasan de **423 a 433**, en **372 padres** frente a 366:

| Padre | Incremento de filas alertadas | Causa |
|---|---:|---|
| 1004 | +1 | Daño textual advertido. |
| 2918 | +1 | Coma final conservada al separar el planteamiento presidencial. |
| 2948 | +1 | Final incompleto advertido. |
| 4453 | +2 | Anuncio repetido y aviso de texto leído por tercero. |
| 4507 | +2 | Anuncio repetido y aviso documental. |
| 4722 | +2 | Anuncio repetido y aviso documental. |
| 5212 | +1 | Recalcular duplicado del anuncio de lectura de 239 caracteres, idéntico al de 4722. |

Los anuncios de **4453/4507** son idénticos entre sí, como los de **4722/5212**. Se mantienen las cuatro filas y sus avisos. **No se eliminan repeticiones ni se promueven automáticamente a las 21 fórmulas revisadas.** La fila de 5212 sólo cambia los indicadores de duplicado y revisión; su texto, atribución, límites y documento no cambian. No constituye una nueva lectura integral de 5212.

**433 alertas no son 433 errores confirmados ni un recuento de todo lo que falta leer.** Los motivos se superponen; autoría documental, puntuación y daño no son unidades intercambiables.

## 6. Validación global

| Control | Resultado |
|---|---:|
| Pruebas | **1434**, todas pasan; 31 nuevas |
| Filas físicas / bloques de texto | **9657 / 9656** |
| Grupos de turno / grupos multifila / máximo de filas | **9239 / 322 / 11** |
| Padres / palabras / sesiones | **7219 / 2048560 / 132**, conservados |
| Revisiones personales anteriores / actuales | **363 / 371** |
| Padres con revisión personal | **342** |
| Advertencias anteriores conservadas | **68**, todas |
| Lecturas anteriores conservadas / actuales | **28 / 33** |
| Documentos anteriores conservados / actuales | **3 / 6** |
| Enlaces revisados preservados | **7** |
| Nuevos enlaces / enlaces perdidos | **0 / 0** |
| Etiquetas de actor | **55**, ninguna nueva |
| Esquemas auditoría / final | **37 / 24** |
| Hashes de entradas/código / salidas | **79 / 11**, verificados |
| Otros padres con campos no secuenciales intactos | **7206** |

El ensayo aislado y la publicación son idénticos por filas y columnas. El pipeline publicó únicamente después de pasar pruebas, F0 y F1 en staging. Las **31 pruebas nuevas** comprenden dieciséis contratos de fuente/segmentación/conservación y quince controles de comportamiento.

La comparación cubre todos los campos salvo `ID` e `ID_Turno`, cuyos valores secuenciales cambian al insertar filas. Se verifican por separado sus agrupaciones y enlaces. Cambian otros campos en sólo **trece padres**: once corregidos, 1004 por advertencia y 5212 por duplicado. En los restantes **7206**, todos los campos no secuenciales permanecen iguales.

Ningún enlace previo se pierde. Se mantienen, entre otros, García de once filas, 224→225→226, 3454→3455, 2695→2696, 2754→2755, 2790→2791, 1386→1387, 2673→2674, 2863→2864, 2796→2797, 2707→2708, 2963→2964 y 2680→2681. No se restaura 5402→5403.

`CONTEXTO_REVISADO` no crea anclas globales. El retorno de Soto en **4926** conserva su fuente explícita y ancla. Los controles anteriores de 506/1572, 780, 6009/6025/6443, Ricaurte/4594, Nacrur/Mattar/Álvarez, 4054/3110, Araya, 2463, 2674, 2661 y 5252 quedan cubiertos por conservación y regresión, no por una nueva lectura completa de todos ellos.

El CSV de TPM no cambia salvo IDs de evidencia: **310 contrastes**. Las **21 fórmulas** se conservan. El CSV documental incorpora sólo las tres fichas nuevas y conserva las anteriores salvo IDs.

## 7. Histórico y continuidad del trabajo

Los estados y tipos de revisión del histórico783 permanecen iguales: **102 pendientes contextuales**, 497 comparaciones, 183 lecturas dirigidas y 103 triajes; 284 intervalos históricos tienen alertas actuales. Persisten seis intervalos históricos con variante de identidad y **21 filas actuales Ricaurte**. Las ocho menciones legítimas históricas no equivalen a las treinta actuales; no sumar unidades diferentes ni tomar el estado principal como cierre de los residuos.

Los barridos de esta pasada produjeron 68 ventanas amplias de relativas, 171 de gerundios, once de cesiones, catorce de predicados pospuestos y 201 de inicios nominales —135 con tratamiento cercano—. Muchos son falsos positivos y se solapan. El barrido de cláusulas con sujeto ya reconocible no produjo candidatos. **No sumar estos resultados como casos leídos ni afirmar lectura completa de todos ellos.** El alcance de lectura integral es el listado de dieciséis padres de la sección 1.

Seguir con delimitaciones conjuntas/institucionales, nombres/cargos y continuidad larga no alertada. En particular: 4055, 3775, 6185, discrepancias en 226/3454, puente de 780 y enlaces 4745→4746 y 6561→6562, sin forzarlos.

## Evidencia

- [Comparación global](comparacion_loop25_2026-09-08.json)
- [Detalle de filas antes/después](cambios_loop25_2026-09-08.csv)
- [Checkpoint](estado_revision_loop25_2026-09-08.json)
- [Informe LOOP24](REVISION_LOOP24_2026-09-08.md)
- [PR #3](https://github.com/joako0o/nlm_proyect/pull/3)

Sin nuevo cotejo PDF, sin muestra independiente con/sin alertas y sin afirmación de pureza exhaustiva. Verificaciones locales; el workflow preexistente de GitHub Actions queda fuera del PR.
