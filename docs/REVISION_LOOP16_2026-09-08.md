# LOOP16 — Diálogo recuperado, exposiciones completas y atribuciones locales

**2026-09-08 · [PR #3](https://github.com/joako0o/nlm_proyect/pull/3).**
Base: `8a55a3911d4eab15e6233c7cc1add113c315e226`, [LOOP15](REVISION_LOOP15_2026-09-08.md).
Lectura dirigida por agente del texto disponible; **sin nuevo cotejo PDF ni muestra independiente**. La selección dirigida no constituye una auditoría exhaustiva del corpus.

## Resultado

| Medida | Antes | Ahora |
|---|---:|---:|
| Filas físicas XLSX | 9.500 | **9.504** |
| Bloques de texto | 9.499 | 9.503 |
| Grupos de turno | 9.089 | 9.093 |
| Grupos multifila / máximo de filas | 315 / 11 | 315 / 11 |
| Filas con alertas / padres alertados | 321 / 288 | **322 / 288** |
| Pruebas | 1.100 | **1.129** |
| Intervalos revisados / padres con revisión | 223 / 216 | **234 / 225** |
| Advertencias contextuales registradas | 21 | 24 |
| Etiquetas nominales de actor | 51 | 50 |

**Diez padres afectados:** dos con separación de hablantes —780 sólo parcialmente—, uno con cambio de etiqueta local de actor y siete sólo con metadatos de atribución/advertencias. Los otros **7.209 padres** conservan sus campos semánticos, descontando identificadores secuenciales. El comparador agrupa las separaciones y el cambio de actor como tres padres estructurales; no son tres diálogos separados.

- [Comparación global antes/después](comparacion_loop16_2026-09-08.json)
- [Detalle de filas, texto y hashes](cambios_loop16_2026-09-08.csv)
- [Checkpoint y pendientes](estado_revision_loop16_2026-09-08.json)

## 1. Exposiciones largas: 506 y 1572

Se leyeron íntegramente las exposiciones disponibles de **Sergio Lehmann**, de **8.662 y 18.132 caracteres** respectivamente, con sus cesiones de palabra y retornos pertinentes. Se mantiene cada desarrollo completo; los párrafos sucesivos y las referencias a autoridades extranjeras no se convierten en turnos nuevos. La atribución pasa de `ANAFORA_LOCAL` a `CONTEXTO_REVISADO` mediante intervalos con hash y evidencia.

**506:** el daño sigue visible, incluidos «indicadores de El señor Lehmann» y el final «tanto en Estados Unidos». Una advertencia contextual nueva evita confundir identificación del expositor con reconstrucción del texto. La respuesta posterior de Lehmann de **206 caracteres**, revisada en LOOP13, se conserva idéntica por identificador, límites y evidencia, ahora como revisión secundaria del contenedor. No se certifica todo el padre 506 ni se reescribe el OCR.

## 2. 780: recuperación parcial de Corbo, no adjudicación del puente

Se leyó el padre completo. La salida anterior contenía 7.119 caracteres bajo De Gregorio, además del tramo presidencial explícito y del Consejo. Se recupera únicamente el inicio inequívoco:

> Lo que sí ha cambiado, indica el señor Corbo

La salida queda:

| Actor / alcance | Caracteres | Evidencia |
|---|---:|---|
| De Gregorio, etiqueta provisional del tramo anterior | 5.463 | Evidencia anterior conservada, **puente advertido** |
| Corbo, fragmento recuperado | 1.655 | `CONTEXTO_REVISADO` |
| Corbo, intervención explícita posterior | 1.763 | Ancla explícita conservada |
| Consejo | 2.546 | Acta institucional, sin cambio |

El puente «En la economía nacional…» continúa dentro del primer tramo, **sin adjudicación nueva de ese puente a De Gregorio ni a Corbo**. La advertencia de texto dañado conserva esta limitación. `Cita_Ancla_Posterior` mantiene separado el comienzo «Señala el Presidente, señor Corbo»; `Fin` solo no debe crear un corte ni una nueva ancla. No se obtuvo el acta desde el repositorio externo, que mostró verificación de acceso; no se usó evidencia PDF nueva.

## 3. 6009: diálogo antes fusionado y sin alerta

Al revisar contexto de Ricaurte se encontró este padre, que aparecía completo —**11.806 caracteres**— como Vergara y sin alerta automática. Se leyó íntegramente y se recuperaron:

1. **Vergara:** introducción, 1.451 caracteres.
2. **Ricaurte:** exposición internacional, 4.969 caracteres.
3. **Vergara:** intervención propia, 902 caracteres.
4. **Ricaurte:** continuación y retorno, 4.481 caracteres.

La nómina explícita del padre **6008** proporciona la etiqueta local **Miguel Ricaurte Bermúdez**. Ambos tramos conservan `VARIANTE_IDENTIDAD_POR_VERIFICAR`: el nombre de la sesión no prueba equivalencia global con Vintimilla. Las referencias a Obama, Yellen, autoridades europeas o a una opinión de Claro no generan intervenciones inventadas. Los desarrollos extensos se mantienen unidos.

Este hallazgo muestra por qué **ausencia de alertas no equivale a atribución correcta**. No sustituye una futura muestra independiente de filas con y sin alertas.

## 4. Ricaurte: atribución de sesión, no armonización de identidad

Se leyeron completas las intervenciones de **4575 / 4579 / 4582 / 4584**, de 4.584 / 873 / 1.220 / 3.010 caracteres. La nómina del padre **4573** sustenta la etiqueta local Bermúdez; las cuatro atribuciones pasan a revisión documentada y mantienen sus advertencias de variante. 4577 conserva su advertencia previa.

**6025:** los 415 caracteres se mantienen idénticos. La etiqueta final pasa de Vintimilla a Bermúdez según la nómina explícita de **6008**. El discurso sólo dice Miguel Ricaurte. El **actor original Vintimilla permanece registrado**, y el diccionario de alias no se modifica.

Como 6025 era la única fila que usaba Vintimilla como etiqueta final, la cardinalidad baja de **51 a 50 etiquetas nominales** —49 etiquetas personales y el Consejo—. **No es una demostración de que ambas variantes designen a la misma persona, ni un censo de identidades verificadas.** Las ocho filas actuales con advertencia de variante permanecen pendientes.

## 5. 6530: nombre literal discrepante

Se documenta el tramo de **Claudio Raddatz, 883 caracteres**, contrastándolo con la nómina de **6518**. El literal **«Claudia Raddatz»** se conserva. Se añade `NOMBRE_EN_DISCURSO_POR_VERIFICAR`, con decisión `PENDIENTE_CONTRASTE_NOMBRE`; no se corrige silenciosamente el texto. Los 239 caracteres posteriores de Vergara siguen separados e intactos.

El motivo nuevo usa la maquinaria común de advertencias contextuales y bloquea continuidad automática. No se amplían reglas de segmentación ni alias.

## 6. Cambios técnicos y trazabilidad

- **Once intervalos nuevos en diez padres**, nueve padres nuevos en el registro. Los **223 intervalos previos permanecen idénticos**, incluidos los secundarios.
- **Tres advertencias nuevas:** 506, 780 y 6530. Las 21 anteriores permanecen intactas.
- `scripts/context_warnings.py` incorpora el motivo de nombre discrepante.
- `scripts/review_queue.py` conserva la identidad pendiente como dimensión separada: columna **`Variante_Identidad_Pendiente`**, siguiente paso explícito y contador resumen. Un cambio de método o de etiqueta local no borra esa condición.
- La nueva columna corresponde a la **cola histórica**, no altera los esquemas de 37/24 columnas de las bases XLSX.
- **29 pruebas nuevas**: diez contratos exactos por padre y diecinueve controles de comportamiento, evidencia, advertencias y trazabilidad. Se actualizan expectativas históricas sin retirar guardas sobre lo que sigue pendiente.

## 7. Verificación integral

Ensayo aislado, suite completa y `python scripts/preparar_data.py` terminados correctamente. **1.129 pruebas; F0 y F1 sin errores bloqueantes.** La base publicada coincide campo por campo con el ensayo aislado. El ajuste posterior de la cola histórica sólo añade trazabilidad, no cambia esa base.

- **7.219 textos y 2.048.560 palabras conservados**; 132 sesiones y 310 contrastes TPM.
- **67 hashes de entradas/código y once hashes de salidas verificados**.
- Todos los enlaces preexistentes entre padres y grupos no afectados conservados; ningún enlace nuevo o retirado. Las dos exposiciones de García de once filas siguen intactas.
- `CONTEXTO_REVISADO` nunca se convierte en ancla global. Se conservan el ancla posterior de 780, las de 1092 y 2790, el enlace 2790 → 2791 y el retiro previo de 5402 → 5403.
- Sin cambios a 3110 institucional, la revisión de 797 caracteres de 3421, los retornos y advertencias anteriores, las once menciones actuales, las 21 fórmulas y los tres documentos leídos.
- 5212/5742/5802 mantienen **Larraín autor ≠ Vergara lector**, sin inferir asistencia o intervención oral del autor.
- Los datos de origen y todos los registros de curación distintos de hablantes/advertencias contextuales permanecen intactos.

## 8. Alertas y pendientes: no confundir contadores con cierres

Las filas alertadas pasan de **321 a 322**, en **288 padres**. Las alertas por anáfora pasan de **dos a cero** y las de atribución heurística legada de **ocho a dos**. Las dos legadas restantes son los pasajes conjuntos de **2126 y 3989**, no atribuidos arbitrariamente. El saldo total no pretende minimizar avisos: los nuevos tramos de 6009 hacen visible una incertidumbre de identidad antes oculta, mientras se conservan daño, puente ambiguo y nombre discrepante.

| Motivo actual | Filas |
|---|---:|
| Final sin puntuación | 258 |
| Posible otro hablante o mención | 20 |
| Texto dañado por cotejar | 11 |
| Fragmento breve | 10 |
| Variante de identidad por verificar | 8 |
| Pasajes conjuntos por delimitar | 6 |
| Cargo en discurso por verificar | 5 |
| Duplicado no fórmula | 3 |
| Texto escrito leído por tercero | 3 |
| Atribución heurística legada | 2 |
| Hablantes por identidad pendiente | 1 |
| Nombre en discurso por verificar | 1 |

Los motivos se superponen. No son 322 errores confirmados ni todas filas sin leer. Cero alertas por anáfora tampoco certifica toda atribución del corpus.

La cola histórica conserva **104 intervalos pendientes de lectura contextual**, antes 107. Clasifica 331 métodos actualizados, 170 cambios por comparación, 101 correcciones dirigidas, 58 fórmulas, siete breves, ocho menciones históricas, un estado principal de identidad, dos repeticiones y una continuidad. Son **501 comparaciones automáticas, 177 lecturas dirigidas y 105 triajes**. Estos contadores no equivalen a los once intervalos nuevos del registro.

**El estado principal `IDENTIDAD_PENDIENTE` baja de seis a uno sólo por precedencia de clasificación**, no por resolver cinco identidades: **seis intervalos históricos siguen marcados `Variante_Identidad_Pendiente=SI`** y sus alertas permanecen. La nueva dimensión evita ocultar este solapamiento. Los 104 históricos y las 322 alertas actuales no se suman; tampoco son intercambiables las ocho menciones históricas y las once actuales.

Siguen pendientes el puente de **780**, **6185**, **6443**, **2126/3989**, residuos conjuntos de **3191/5367**, identidad y daños de **4433**, todas las variantes de Ricaurte, el nombre de **6530** y las demás advertencias. No son una lista exhaustiva. En 6185 sólo se releyó una ventana del desarrollo de 20.118 caracteres: el aviso real corresponde a «conforme señala … Matías Bernier», no a la referencia previa a una pregunta de Claro. No se adjudica el intervalo ni se fuerza una intervención autónoma.

No se fuerzan los candidatos de continuidad 3887 → 3888, 4224 → 4225, 4745 → 4746, 4941 → 4942, 5910 → 5911 o 6561 → 6562. **Faltan cotejos documentales de casos ambiguos y una muestra independiente con y sin alertas.** F0/F1 no certifican pureza semántica exhaustiva.

## Publicación

Trabajo sobre la rama del PR #3. Verificaciones locales; `.github/workflows/data-quality.yml` sigue fuera del PR por falta de permiso `workflows`. No se afirma una ejecución remota de CI. El informe LOOP15 queda conservado como histórico. Sin proceso activo al cerrar la pasada.
