# nlm_proyect — Preparación de actas RPM del Banco Central de Chile

Corpus de **132 sesiones mensuales de 2005–2015**, a partir de **7.219 filas originales**.
La entrega tiene **9.691 filas físicas / 9.690 bloques de texto**, con actor, cargo,
trazabilidad y alertas. Una intervención extensa ocupa dos filas por el límite de XLSX.
**338 grupos comparten varias filas bajo un mismo `ID_Turno`**, hasta once consecutivas;
no se fusionan registros de origen ni se recortan exposiciones por longitud.

## Estado actual — 2026-09-08

**Entrega de datos LOOP32: F0 y F1 pasan, con 1.757 pruebas en su publicación.**
No certifican pureza semántica total.
Quedan **465 filas con alertas en 395 padres**. No equivalen a errores confirmados
ni a todo lo que falta leer. `SIN_ALERTAS_AUTOMATICAS` tampoco significa revisión humana.

**Informe vigente:** [LOOP32: referencias y continuidad pendiente](docs/REVISION_LOOP32_2026-09-08.md).
**25 fichas nuevas de referencias legítimas y tres advertencias léxicas/sintácticas**.
Se leyeron **35 padres completos**, incluidos dos registros de cabecera mixta.
**No nuevos cortes, reasignaciones o enlaces**: las respuestas y retornos de los casos
leídos ya estaban separados. Ver [comparación global](docs/comparacion_loop32_2026-09-08.json),
[detalle CSV](docs/cambios_loop32_2026-09-08.csv) y
[checkpoint](docs/estado_revision_loop32_2026-09-08.json).

- **578/611:** las preguntas o referencias al destinatario no adelantan su respuesta;
  ésta conserva su inicio explícito. **3102** mantiene Soto → De Ramón → Soto.
- **628:** Corbo anuncia 283; Lehmann desarrolla **3269**, sin recorte por longitud.
  **629 / Velasco 248** formula excusas al incorporarse: habla personal, no evento genérico.
- **3473:** referencias a Marshall y Cowan dentro del argumento de Marfán, no tres voces
  conjuntas. **7096:** la referencia de Raddatz no adelanta la respuesta real de Naudon.
- **665/6250/6456:** reservas acotadas sobre «en lo cambiarlo», «riego de mercado» y
  «inversión se este sector», sin reconstruir palabras ni afirmar origen OCR confirmado.
- **1904→1905, 2788→2789, 2803→2804 y 2969→2970:** cuatro pares leídos completos;
  candidatos plausibles, pero no se fuerzan enlaces a través de sus avisos pendientes.
  Esto no prueba discontinuidad semántica ni justifica eliminar advertencias.

**Todos los scripts de producción siguen idénticos. CONTEXTO_REVISADO no crea anclas
globales** y Fin solo no corta ni ancla. Sin nuevas reglas de verbos o alias.
Autor documental ≠ lector ≠ asistencia: no nuevos documentos o eventos.

**382 intervalos personales en 353 padres, 24 enlaces revisados, 12 documentos,
4 fichas institucionales y 3 archivos de retiros, intactos**.
**84 advertencias = 81 anteriores + 3 nuevas**. Se conservan las separaciones de acta
**4788 llegada112 / 6808 retiro114**, junto con las excusas, respuestas, retornos y
presentaciones reales. La nota de movimiento sólo alcanza su intervalo individual.

**7.219 padres y 2.048.560 palabras conservados. Todos los enlaces, grupos e IDs idénticos.**
Sólo tres padres cambian celdas de alertas; **7.216 son idénticos en todas sus columnas**.
Ensayo aislado/publicación idénticos celda a celda. **86 hashes de entradas/código y 11
de salidas comprobados**; esquemas 37/24, 21 fórmulas, 310 contrastes TPM y 55 etiquetas
preservados. CSV de TPM, documentos e histórico783 idénticos byte a byte, incluidos IDs.

García de once filas; 224→225→226, 3454→3455, 2695→2696, 2754→2755, 2790→2791,
1386→1387, 2673→2674, 2863→2864, 2796→2797, 2707→2708, 2963→2964, 2680→2681,
4745→4746, 6561→6562, 5003→5004 y las 14 continuidades de LOOP28 se conservan.
**3572 reanudación235 sigue separada. 5402→5403 y 600→601 no se restauran.**
Pausa archivada, retornos 3044/4476/4926 y correcciones 2705/2706 intactos.

**102 lecturas actuales = 98 legítimas + 4 pendientes:** 6185/Bernier, 3775/Cerda,
4055/conjunto-institucional y 2510/conjunto. De las 25 nuevas, cuatro aparecen en la cola:
628 y 665/6250/6456. **No cierran sus avisos de puntuación/texto.** Las otras 21 lecturas
no corresponden a intervalos alertados. Las **462 filas previas de la cola siguen presentes**:
461 completamente idénticas y 628 sólo con anotación nueva. Tres filas añadidas por avisos.

Histórico **783**: CSV idéntico, **102 pendientes contextuales**, 497 comparaciones,
183 lecturas y 103 triajes. **285 intervalos con alertas actuales**: los tres avisos nuevos
no recaen en esa cola histórica. El cambio de estado de 6808 documentado en LOOP31
se conserva. Seis intervalos con variante y **21 filas actuales** de variantes.
Ocho menciones históricas no son las 98 actuales; unidades superpuestas, no sumables.

Los barridos son orientativos y superpuestos, no lecturas completas de todas sus
coincidencias ni muestra representativa. Siguen nombres/cargos, pasajes conjuntos,
puente de 780, reserva de 6119 y demás pendientes. **Sin nuevo cotejo PDF ni muestra
independiente con/sin alertas.** Identificar una voz no certifica OCR; longitud no es daño.
Controles previos preservados sin afirmar relectura de todos en esta pasada.

Publicado en el [PR #3](https://github.com/joako0o/nlm_proyect/pull/3).
**No hay proceso activo.** El [informe anterior](docs/REVISION_LOOP31_2026-09-08.md)
conserva 9.691 filas / 462 alertas / 1.704 pruebas. Verificaciones locales;
el workflow preexistente de GitHub Actions permanece fuera del PR.

## Diagnóstico posterior: patrones de puntuación

Se revisaron **36 intervalos completos con contexto acotado** para organizar los avisos,
sin modificar la entrega LOOP32. De las302 filas cuyo único aviso es el final sin
puntuación, **167 terminan en coma antes de otro actor ya separado en el mismo padre**.
También se distinguen pies/encabezados y ocho indicios de palabra posiblemente desplazada
al párrafo anterior. Son candidatos para cotejo, no reparaciones automáticas.

**En el diagnóstico inicial pasaron1.780 pruebas**, incluidas23 de su herramienta independiente.
Datos, curación, QA y manifiesto permanecen idénticos; **ninguna alerta cerrada**.
[Informe y evidencia de las36 lecturas](docs/DIAGNOSTICO_FINALES_2026-09-08.md).

### Seguimiento: primer lote de comas (histórico)

**El lote1 registró40 límites existentes en36 padres completos y dejó127 límites
sin ficha bilateral.** Los sujetos respaldan las separaciones examinadas; no
hicieron falta nuevos cortes. Las comas y reservas textuales/de cargo permanecen literales.

La nueva cola distingue **lectura realizada** de **alerta cerrada**: siguen465 filas
alertadas. Se conservan el daño de2667, el duplicado de2723, el residuo de2535 y los demás
pendientes. **En ese lote pasaron1.795 pruebas (+15); los27 archivos versionados de datos
permanecieron idénticos**, incluida TPM externa. El pipeline y su QA siguen siendo los de LOOP32.

[Informe del lote1](docs/REVISION_COMAS_LOTE1_2026-09-08.md) ·
[127 límites sin ficha](docs/revision_comas_lote1_2026-09-08/comas_sin_ficha.csv).

### Seguimiento: segundo lote de comas (histórico)

**El lote2 dejó80 límites con ficha bilateral y87 sin ficha**, después de leer40 límites adicionales
en39 padres completos. Se amplió la lectura a2010–2015 y al padre largo2738:
**Soto4743 → Presidente105 → Soto947 → Marfán401**, conservando la presentación y el retorno.
Los cinco límites institucionales siguen aparte; no se aprueban como dos voces personales.

La herramienta acumula lotes sin duplicar límites ni modificar las40 fichas anteriores.
**En ese lote pasaron1.815 pruebas (+20)** y los27 archivos de datos quedaron idénticos:
**465 filas alertadas**, sin nuevos cortes, reasignaciones o cierres. Permanecen las
reservas de nombres, residuos, duplicados y posibles palabras desplazadas.

[Informe del lote2 y plan para seguir](docs/REVISION_COMAS_LOTE2_2026-09-08.md) ·
[87 límites sin ficha](docs/revision_comas_lote2_2026-09-08/comas_sin_ficha.csv).

### Tercer lote de comas (histórico; continúa en el lote 4)

**120 límites con ficha bilateral y47 sin ficha**, tras revisar40 límites más en29
padres completos. Se leyó todo2765, de12.127 caracteres: sus seis tramos se conservan,
incluida la exposición final de **Lehmann8714**, sin cortes por temas o longitud.
Agrupar focos del mismo padre permitió revisar juntas las cuatro comas de2661 y otras
alternancias, sin aprobar automáticamente los límites no incluidos en las fichas.

**1.829 pruebas locales pasan (+14)**. Los27 archivos de datos y los diez artefactos
de los lotes1 y2 permanecen idénticos. **Ningún nuevo corte, reasignación o cierre de
alerta**: siguen465 filas alertadas. Quedan42 límites personales y5 institucionales;
las reservas de texto, cifras y nombres se conservan para cotejo.

[Informe del lote3](docs/REVISION_COMAS_LOTE3_2026-09-08.md) ·
[47 límites sin ficha](docs/revision_comas_lote3_2026-09-08/comas_sin_ficha.csv).

### Cuarto lote de comas (histórico; continúa en el lote 5)

**142 límites con ficha bilateral y 25 sin ficha**, tras revisar 22 límites más
leyendo 22 padres completos (57.607 caracteres). Se conservan el voto de
**Marshall de 5.484 caracteres**, la exposición de **Céspedes de 4.101** y las
quince intervenciones del padre 1718. No se corta por longitud o cambios de tema.

**1.841 pruebas locales pasan (+12)**. Los 27 archivos de datos y los 15 artefactos
de los tres lotes anteriores permanecen idénticos. **Ningún nuevo corte, enlace,
reasignación o cierre de alerta**: siguen 465 filas alertadas. La respuesta de
García en 2938 conserva su final dañado y ambas advertencias; identificar su inicio
no permite completar el texto. Quedan **20 límites personales y 5 institucionales**.

[Informe del lote 4](docs/REVISION_COMAS_LOTE4_2026-09-08.md) ·
[25 límites sin ficha](docs/revision_comas_lote4_2026-09-08/comas_sin_ficha.csv).

### Seguimiento vigente: quinto lote de comas

**162 límites con ficha bilateral y 5 sin ficha**, tras revisar los últimos
**20 límites personales de esta subcola**, leyendo 20 padres completos
(47.515 caracteres). Esto no completa la revisión de todos los hablantes del corpus.
Se conservan las exposiciones, los retornos y las confirmaciones breves de Soto;
en 2705 permanecen las siete partes, incluida la reanudación institucional separada.

**1.855 pruebas locales pasan (+14)**. Los 27 archivos de datos, los 20 artefactos
de los cuatro lotes previos y el helper siguen idénticos. **Ningún nuevo corte,
enlace, reasignación o cierre de alerta**: siguen 465 filas alertadas. El voto de
Marfán en 2885 y los tramos advertidos de 3268 conservan daño/duplicado y colas literales.

Quedan **5 límites institucionales** (601, 1901, 2112, 2803 y 5252), para revisión
con criterios acta/discurso, sin debilitar las restricciones del seguimiento personal.

[Informe del lote 5](docs/REVISION_COMAS_LOTE5_2026-09-08.md) ·
[5 límites institucionales sin ficha](docs/revision_comas_lote5_2026-09-08/comas_sin_ficha.csv).

## Ejecutar todo el pipeline

Python 3.10+ (entorno verificado: Python 3.11), sin servicios externos:

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/preparar_data.py
```

El comando:

1. Recupera los textos largos desde los dos PDFs disponibles.
2. Ejecuta las pruebas de regresión.
3. Segmenta, atribuye, clasifica y calcula alertas.
4. Genera la base final.
5. Ejecuta F0 (TPM/cobertura) y F1 (integridad/trazabilidad).
6. **Publica las salidas sólo después de pasar todas las verificaciones.**

La construcción se hace en un directorio temporal ignorado dentro de `.cache/`.
Un fallo de construcción, prueba o QA no sustituye los archivos publicados.
Las alertas semánticas no bloquean la publicación: quedan visibles en el Excel
y en `revision_pendientes.csv`.

Pruebas y validaciones por separado:

```bash
python -m unittest discover -s tests -v
python scripts/qa_gate_f0.py
python scripts/qa_preparacion.py
```

También existen los scripts individuales `build_textos_completos.py`,
`build_base_referencia.py` y `crear_consolidado_final.py`. Es preferible el
orquestador: ejecutarlos individualmente sí puede dejar salidas desactualizadas
entre sí. `NLM_PROCESSED_DIR` permite dirigir las salidas a un directorio alternativo.

## Archivos

```text
data/
  raw/
    consolidado_final.xlsx                    # entrada, no se modifica
    2005-06-09 - Actas.pdf
    2005-07-12 - Actas.pdf
  external/
    tpm_oficial_bcch.csv                      # referencia obtenida de Datosmacro
  curation/
    cola_783.json                            # instantánea de las 783 alertas originales
    revisiones_cola_783.json                  # 16 decisiones: brevedad, continuidad y menciones
    formulas_revisadas.json                   # 21 fórmulas exactas; no borrar repeticiones
    revisiones_menciones_actuales.json       # lecturas acotadas y pendientes; no suprimen alertas
    revisiones_roles.json                    # seis cargos: citas, sesión, hash y justificación
    revisiones_hablantes.json                # intervalos acotados con citas y hash
    revisiones_documentos_leidos.json        # autor, lector y límites con hash
    revisiones_continuidad_hablantes.json    # enlaces individuales; no anclas globales
    revisiones_continuaciones_acta.json      # acta, interrupción/reanudación o movimiento de asistentes acotado
    alertas_contextuales.json                # incertidumbre textual, de nombre, cargo o identidad
    alertas_contextuales_retiradas.json      # advertencia original, motivo del retiro y sustitutas
  processed/
    consolidado_base_referencia.xlsx          # base de 37 columnas + hojas de auditoría
    consolidado_base_referencia_final.xlsx    # entrega de 24 columnas
    textos_completos.jsonl                    # 2 textos de origen completos
    decisiones_tpm.csv                       # una fila por sesión, con IDs de evidencia
    revision_783.xlsx                        # seguimiento original + cola actual, tres hojas
    revision_783.csv                         # 783 intervalos con estado/evidencia/IDs actuales
    resumen_revision_783.json                # balance de estados; no cierres semánticos
    revision_pendientes.csv                  # alertas, contexto y alcance de lecturas dirigidas
    turnos_habla.csv                         # grupos, naturaleza y lector; no todos son habla oral
    documentos_leidos.csv                    # vínculo autor/lector, cargo, límites y no inferencia de asistencia
    qa_preparacion.json                      # métricas y errores bloqueantes
    manifiesto_preparacion.json              # SHA-256 de entradas, código y salidas
scripts/
  preparar_data.py                           # construcción + pruebas + QA + publicación
  build_textos_completos.py                  # recuperación PDF sin borrar cifras económicas
  build_base_referencia.py                   # construcción de la base de auditoría
  turns.py                                  # sujetos de habla y contexto local
  mention_reviews.py                        # valida lecturas actuales, sin cambiar actores/alertas
  continuity.py                             # continuidad entre párrafos con anclas de evidencia
  document_reviews.py                       # escritos leídos por terceros y validación autor/lector
  institutional_reviews.py                  # acta/reanudación acotadas y archivo de enlace retirado
  reviewed_continuity.py                     # valida extremos exactos de enlaces revisados
  context_warnings.py                        # valida advertencias contextuales ancladas a fuente
  curation.py                               # validación de decisiones documentadas
  roster.py                                 # asistencia, nombres y cargos
  decision_rules.py                         # identificación de decisiones vigentes
  procedural.py                             # fórmulas exactas revisadas + heurística anterior
  review_queue.py                            # seguimiento por intervalos de la cola original
  review_flags.py                           # alertas conservadoras
  crear_consolidado_final.py                 # proyección de columnas
  qa_gate_f0.py                              # cobertura y consistencia de TPM
  qa_preparacion.py                          # F1, reportes y manifiesto
  paths.py                                  # rutas comunes y staging
  descargar_actas_rpm.py                     # auxiliar local; requiere Playwright
```

El descargador no forma parte del pipeline reproducible; el repositorio BCCh
puede exigir verificación humana. No se necesitan nuevas descargas para
regenerar las salidas actuales.

## Esquema final

Las **primeras 13 columnas conservan su orden** para facilitar la migración:

| Columna | Significado |
|---|---|
| `ID` | Consecutivo de fila en esta versión, no un identificador inmutable |
| `Fecha` | Fecha de la sesión |
| `Actor_Final` | Persona atribuida, autor de documento escrito o Consejo del BCCh; consultar `Tipo_Acta` |
| `Rol_Final` | Cargo en la sesión; consultar su fuente y alertas |
| `Fuente_Actor` | Evidencia de atribución: sujeto explícito, cargo de sesión, anáfora, contexto revisado, encabezado de minuta, documento escrito/lector revisado o heurística legada |
| `Fuente_Rol` | `LISTA_ASISTENCIA`, `ACTA_INSTITUCIONAL`, `TEXTO_EXPLICITO_REVISADO`, `CONTEXTO_SESION_REVISADO`, `CARGO_DOCUMENTAL_REVISADO` o `PENDIENTE_REVISION` |
| `Tipo_Acta` | Etiqueta institucional/decisión, `MINUTA_PERSONAL` u `OPINION_ESCRITA`; vacío en otras intervenciones, por diseño |
| `Página` | Página del registro original; **no** localización recalculada de cada segmento |
| `Texto` | Texto preservado, con normalización de espacios |
| `Tema_Categoria` | Regla temática aplicada al tema del padre |
| `Palabra_Clave_Categoria` | Regla temática aplicada a la palabra clave del padre |
| `Duplicado_Exacto` | Repetición exacta del **texto procesado** en otra fila |
| `Duplicado_Formula` | Duplicado cuyo texto coincide con la heurística de fórmula procedimental |

Se conservan las **7 columnas de trazabilidad y revisión** de la preparación anterior:

| Columna | Significado |
|---|---|
| `ID_Padre` | ID del consolidado original |
| `Id_Sesion` | `RPM-AAAA-MM-DD` |
| `ID_Intervencion` | Sesión + padre + número de segmento, único dentro de una versión |
| `ID_Bloque_Texto` | Agrupa fracciones físicas de una misma intervención larga |
| `Fuente_Texto` | Excel original o texto recuperado/verificado con PDF |
| `Estado_Revision` | `PENDIENTE_REVISION` o `SIN_ALERTAS_AUTOMATICAS` |
| `Motivos_Revision` | Códigos de alertas separados por `;` |

La revisión de continuidad agrega **4 columnas más** (24 en el Excel final):

| Columna | Significado |
|---|---|
| `ID_Turno` | Grupo conservador de filas contiguas del mismo hablante y sesión |
| `Relacion_Turno` | Inicio explícito, continuidad explícita, párrafo/anáfora de continuidad, institucional, documento personal o sin continuidad confirmada |
| `ID_Antecedente_Continuidad` | Fila inmediatamente anterior que sustenta la continuidad |
| `ID_Ancla_Actor` | Fila con sujeto explícito que sustenta la atribución |

`CONTINUIDAD_PARRAFO` y `ANAFORA_CONTINUIDAD` no convierten menciones en nuevos
hablantes. Requieren un ancla vigente y compatibilidad con el actor de origen.
Un cambio de sesión, otro participante, una suspensión o cesión de palabra
interrumpe la cadena. Las anáforas sin esa evidencia siguen en revisión.

Para leer una exposición completa, ordenar por `ID` y agrupar por `ID_Turno`;
no agrupar todas las apariciones del actor en la sesión, porque puede intervenir
varias veces después de otros participantes. Los grupos incluyen unidades
institucionales aisladas; no constituyen un conteo certificado de turnos humanos.

`CONTEXTO_REVISADO` identifica una decisión dirigida con citas en
`data/curation/revisiones_hablantes.json`; no crea por sí sola un ancla de
continuidad. Las minutas y opiniones escritas tienen relación
`DOCUMENTO_PERSONAL` y tampoco se heredan como turnos hablados. Las notas de auditoría enlazan las decisiones de
curación con sus IDs; la revisión fue del consolidado, no de los PDFs.

En `OPINION_ESCRITA`, `Actor_Final` es el **autor** y `Fuente_Actor` es
`DOCUMENTO_ESCRITO_REVISADO`; la lectura y el cargo se documentan en
`documentos_leidos.csv`. El lector no sustituye la autoría. `Rol_Lista_Asistencia`
queda vacío: el cargo `CARGO_DOCUMENTAL_REVISADO` no es prueba de presencia.
Las introducciones y retornos del Presidente usan `LECTOR_DOCUMENTO_REVISADO`.
`turnos_habla.csv` agrega `Naturaleza_Turno` y `Lector_Documento` para que los
escritos no se interpreten como habla oral al usar ese archivo por separado.

La base de auditoría conserva además actor/cargo originales, temas originales,
notas, número de segmento y `Duplicado_Exacto_Origen` / `Duplicado_Formula_Origen`.
Los IDs basados en segmentos **pueden cambiar al modificar las reglas**; vincular
versiones mediante `ID_Padre`, texto y manifiesto, no sólo por número de fila.

## Controles

### F0 — cobertura y decisiones de TPM

- 132 sesiones, una por mes de 2005–2015.
- Identifica decisiones vigentes, excluyendo recapitulaciones históricas.
- Revisa todas las fórmulas candidatas detectadas y su tipificación.
- Comprueba **tasa objetivo, variación y signo verbal**, sin aceptar que un
  componente correcto oculte otro contradictorio.
- Resultado actual: **310 fórmulas contrastadas en 132 sesiones**, sin errores.
- La cardinalidad de actores se informa; no se fuerza un número histórico
  para mantener el veredicto. El registro de nombres se comprueba en F1.

### F1 — integridad y trazabilidad

- IDs, campos obligatorios, fechas, padres, orden de segmentos y bloques.
- **7.219/7.219 padres reconstruidos**, comparando caracteres y omitiendo sólo
  espacios, contra el texto original o su recuperación completa.
- Ninguna celda supera el límite XLSX; un texto largo se fracciona sin truncarlo.
- Cargos atribuidos por asistencia, categorías reproducibles y duplicados reales.
  Las regresiones de las aperturas de junio de 2008 y febrero de 2009 comprueban
  que la lista de consejeros no absorba gerentes u otros asistentes. La comparación
  con el propio parser de asistencia no es una verificación semántica independiente.
- Revisiones documentadas: hashes/citas vigentes, cargos aplicables e intervalos
  dirigidos íntegros con los actores revisados, sin sustituir asistencia.
- Escritos revisados: cuatro intervalos completos, autor/lector, cargo documental,
  no inferencia de asistencia, aviso obligatorio y barrera de continuidad.
- Correspondencia exacta entre base de auditoría y proyección final.
- Cadenas de continuidad: anclas explícitas, antecedentes contiguos, misma
  persona/sesión, sin saltar barreras institucionales ni cesiones de palabra.
- Enlaces revisados: extremos/hash exactos, opt-in, ancla posterior propia y
  rechazo de relaciones sin registro; no habilitan herencia global desde contexto.
- Lecturas actuales: hash, actor, texto y límites vigentes; distinguen menciones
  legítimas y aportes pendientes, sin retirar alertas ni adjudicar las 783 originales.
- Alertas contextuales: fuente, fecha, hash e intervalo vigentes, actor provisional
  y aviso obligatorio; no desaparecen silenciosamente tras una resegmentación.
- Manifiesto de procedencia y cola de revisión explícita.
- Reconstrucción de los 783 intervalos históricos y decisiones de fórmulas con
  citas en los padres; comparación automática separada de lectura dirigida.

La reproducibilidad se verifica por contenido de hojas/estilos y texto, no por
igualdad binaria del ZIP XLSX: los metadatos del archivo incluyen timestamps.

## Límites y uso analítico

- Hay **55 etiquetas nominales de actor** (54 personales y el Consejo), no un censo
  de identidades independientemente verificadas. Las altas desde LOOP18 incorporan
  intervenciones de Luis Alberto Álvarez Vallejos, Miguel Ángel Nacrur Gazali,
  Pablo Mattar Oyarzún y Juan Pablo Araya Marco, con discurso y nóminas explícitos.
  Gloria Peña se conserva.
  La variante `Miguel Ricaurte Vintimilla` / `Miguel Ricaurte Bermúdez` sigue advertida:
  no se certifica equivalencia ni se modifican sus alias. El actor original
  Vintimilla de 6025 permanece registrado aunque allí se use la etiqueta local Bermúdez.
- Las categorías son reglas de prioridad sobre etiquetas **heredadas del padre**,
  no anotaciones temáticas humanas de cada nuevo turno.
- Las repeticiones se marcan, **no se eliminan automáticamente**.
- Las actas contienen discurso referido, no necesariamente transcripción literal.
- Los dos PDFs permiten revisar la recuperación de textos largos, pero no
  reauditar la extracción completa de las 132 actas desde sus originales.
- `tpm_oficial_bcch.csv` conserva su nombre histórico, pero su columna `fuente`
  identifica a **Datosmacro**. No es una descarga primaria BCCh. La ventana de
  eficacia de 10 días es una hipótesis explícita de emparejamiento.
- Para análisis individual hawk/dove: revisar primero las alertas de hablante,
  distinguir contenido sustantivo de pasos de palabra/acuerdos y definir una
  política para las filas pendientes. No asumir que pasar F0/F1 resuelve esas decisiones.
