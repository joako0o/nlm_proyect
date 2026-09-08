# nlm_proyect — Preparación de actas RPM del Banco Central de Chile

Corpus de **132 sesiones mensuales de 2005–2015**, preparado a partir de 7.219
filas originales. La salida tiene **9.640 filas físicas / 9.639 bloques de texto**,
con actor, cargo, trazabilidad y alertas. Una intervención extensa ocupa dos filas
por el límite de XLSX. **322 grupos comparten varias filas bajo un mismo
`ID_Turno`**, con hasta once filas consecutivas; no se fusionan registros de origen.

## Estado actual — 2026-09-08

**F0 y F1 pasan, con 1.403 pruebas. No certifican pureza semántica total.**
Quedan **423 filas con alertas en 366 padres**. No son 423 errores confirmados
ni todas filas sin leer. `SIN_ALERTAS_AUTOMATICAS` tampoco significa revisión humana.

**Informe vigente:** [LOOP24: habla personal y registros de sesión](docs/REVISION_LOOP24_2026-09-08.md).
**Nueve padres corregidos, diez intervalos nuevos:** seis resegmentados y tres
reasignados sin nuevas filas. Además: un pendiente sin reasignación, dos referencias
legítimas y una actualización sólo de antecedente. Ver
[comparación global](docs/comparacion_loop24_2026-09-08.json),
[detalle CSV](docs/cambios_loop24_2026-09-08.csv) y
[checkpoint](docs/estado_revision_loop24_2026-09-08.json).

- **2661:** Desormeaux **193** → confirmación de Lehmann **49**. Archivar completa
  la advertencia conjunta anterior. Conservar Lehmann explícito **1322** y la
  coordinación previamente revisada de **69**.
- **3288:** Vergara **129** → conformidad de De Ramón **96**; exposición posterior
  de Lehmann **3138** intacta.
- **2680/2746/2788:** separar invitaciones y cierres presidenciales de reanudaciones
  y asistencia. Mantener Cowan **1094**, García **489** y su enlace **2680→2681**.
- **2788:** recuperar inicio y exposición de Soto **407** tras la cesión nominal.
  El destinatario identifica a Soto; la nómina no confirma el cargo subrogante.
  Conservar la concatenación y el final incompleto, sin alias global del cargo.
- **2875/2958/3008:** recuperar reconocimiento, apertura y bienvenida presidenciales
  que estaban bajo Consejo. No convertir homenajeados o destinatarios en hablantes.
  Respuesta de Larraín **413** independiente.
- **5252:** acta **158** → declaración de Marfán **162**, con antecedente nominal
  contiguo. Su exposición **1712** y cesión explícita posterior **223** intactas.
- **4055:** agradecimiento presidencial, aceptación conjunta y acuerdo institucional
  mezclados. Advertencia y lectura pendiente: no autor exclusivo certificado ni
  cuatro turnos individuales inventados.
- **1549/2219:** referencias a comentarios de Schmidt-Hebbel/Marfán, no nuevos turnos.

**Ocho de los nueve padres corregidos estaban sin alerta.** Total **363 intervalos
revisados en 334 padres**, con los **353 anteriores intactos**. **68 advertencias
activas = 64 anteriores − 1 archivada + 5 nuevas**. Tercer retiro: 2661. Los archivos
de 6443/2704 permanecen idénticos, sin resolver variantes Ricaurte.

Tres tipos nuevos requieren opt-in, hashes, límites y sujeto nominal compatible;
no reglas generales de corte ni nuevos alias. **CONTEXTO_REVISADO no crea anclas
globales**. Se conservan las posteriores de **2661/5252** y todas las anteriores
fuera del alcance modificado. Fin solo no corta.

**7.219 padres y 2.048.560 palabras conservados. Ningún enlace nuevo ni perdido.**
**322 grupos multifila**, máximo once. Preservados los siete enlaces revisados,
García de once filas, 224→225→226, 3454→3455, 2695→2696, 2754→2755, 2790→2791,
1386→1387, 2673→2674 y 2863→2864. En 2681 sólo cambia el antecedente; otros
**7.208 padres** mantienen todos los campos no secuenciales. **78 hashes de entradas/
código y once de salidas verificados**; publicación idéntica al ensayo aislado.

Esquemas **37/24**, 21 fórmulas y tres documentos intactos: **Larraín autor ≠ Vergara
lector**, sin inferir presencia ni habla oral. CSV TPM/documentos comparados salvo
IDs secuenciales. **28 lecturas actuales = 25 menciones legítimas + 3 pendientes:
6185/Bernier, 3775/Cerda y 4055/conjunto-institucional**. Las dos referencias nuevas
se validan en el registro, pero no aparecen en revision_pendientes.csv porque no
tienen alertas; no son avisos eliminados.

La cola visible aumenta en ocho filas por advertencias nuevas y puntuación
conservada en los límites; el informe detalla cada incremento. El retiro de 2661
no cierra otros motivos del padre. Los históricos mantienen **102 pendientes
contextuales**, 497 comparaciones, 183 lecturas dirigidas y 103 triajes; seis
intervalos con variante de identidad y 284 intervalos históricos con alertas
actuales. **21 filas actuales con variante Ricaurte**. Ocho menciones históricas
no equivalen a 25 actuales; **no sumar unidades distintas** ni interpretar el
estado principal como cierre de todos los motivos residuales.

Se conservan los controles de 506/1572, 780, 6009/6025/6443, 4594,
Nacrur/Mattar/Álvarez, 4054/3110, Araya/LOOP21 y la revisión anterior de 2674.
Siguen pendientes 4055, 3775, 6185, 2463, nombres en 226/3454, puente de 780,
4745→4746, 6561→6562, pasajes conjuntos, cargos e identidades. García489 en2680
conserva un final incompleto, sin aviso bloqueante que destruya su continuidad;
la advertencia nueva de ese padre sólo cubre el registro institucional.
**Sin nuevo cotejo PDF ni muestra independiente con/sin alertas.** Una exposición
larga no es un párrafo dañado; no se inventa texto.

Publicado en el [PR #3](https://github.com/joako0o/nlm_proyect/pull/3).
**No hay proceso activo.** El [informe anterior](docs/REVISION_LOOP23_2026-09-08.md)
conserva **9.633 filas / 415 alertas / 1.377 pruebas**. Verificaciones locales:
el workflow preexistente de GitHub Actions permanece fuera del PR.

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
    revisiones_menciones_actuales.json       # diez lecturas acotadas; no suprimen alertas
    revisiones_roles.json                    # seis cargos: citas, sesión, hash y justificación
    revisiones_hablantes.json                # 97 intervalos acotados con citas y hash
    revisiones_documentos_leidos.json        # 3 escritos: autor, lector y límites con hash
    alertas_contextuales.json                # incertidumbre textual, de nombre, cargo o identidad
    alertas_contextuales_retiradas.json      # advertencia original, motivo del retiro y sustitutas
  processed/
    consolidado_base_referencia.xlsx          # 9.412 filas, 37 columnas + hojas de auditoría
    consolidado_base_referencia_final.xlsx    # 9.412 filas, 24 columnas
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
