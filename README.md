# nlm_proyect — Preparación de actas RPM del Banco Central de Chile

Corpus de **132 sesiones mensuales de 2005–2015**, preparado a partir de 7.219
filas originales. La salida tiene **9.504 filas físicas / 9.503 bloques de texto**,
con actor, cargo, trazabilidad y alertas. Una intervención extensa ocupa dos filas
por el límite de XLSX. **315 grupos comparten varias filas bajo un mismo
`ID_Turno`**, con hasta once filas consecutivas; no se fusionan registros de origen.

## Estado actual — 2026-09-08

**F0 y F1 pasan, con 1.129 pruebas. No certifican pureza semántica total.**
Quedan **322 filas con alertas en 288 padres**. Los motivos se superponen:
no son 322 errores confirmados ni filas todas sin leer.
`SIN_ALERTAS_AUTOMATICAS` tampoco equivale a revisión humana.

**Informe vigente:** [LOOP16: diálogo recuperado y atribuciones locales](docs/REVISION_LOOP16_2026-09-08.md).
**Diez padres afectados:** dos separaciones —780 sólo parcialmente—, un cambio
local de etiqueta de actor en 6025 y siete cambios sólo de metadatos de atribución.
Los otros **7.209 padres** conservan sus campos semánticos, descontando identificadores.
Ver [comparación global](docs/comparacion_loop16_2026-09-08.json),
[detalle CSV](docs/cambios_loop16_2026-09-08.csv) y
[checkpoint](docs/estado_revision_loop16_2026-09-08.json).

- **6009:** un padre sin alerta y fusionado bajo Vergara se separa en cuatro
  intervenciones: Vergara → Ricaurte → Vergara → Ricaurte. Se leyó íntegramente;
  las exposiciones extensas se conservan y las menciones no crean turnos nuevos.
- **780:** se recuperan 1.655 caracteres explícitos de Corbo. El puente anterior
  «En la economía nacional…» sigue provisional y advertido; se conserva el ancla
  posterior explícita de Corbo, sin extenderle la revisión.
- **506 / 1572:** se leen íntegramente las exposiciones disponibles de Lehmann
  de 8.662 / 18.132 caracteres. 506 conserva daño textual advertido y su respuesta
  previa de 206 caracteres, independiente e idéntica.
- **4575 / 4579 / 4582 / 4584 y 6025:** atribuciones documentadas por nóminas
  explícitas de sesión, con etiqueta local Bermúdez y advertencias de identidad
  intactas. **No se armonizan globalmente Bermúdez/Vintimilla.**
- **6530:** revisión acotada de Raddatz, manteniendo el literal «Claudia Raddatz»
  y añadiendo advertencia de nombre por verificar. Vergara sigue separado.

Son **once intervalos nuevos en diez padres**, nueve nuevos en el registro:
**234 intervalos en 225 padres**. Los 223 anteriores permanecen idénticos.
Tres advertencias nuevas (506/780/6530); las 21 anteriores se conservan.
No se amplían alias ni reglas de segmentación. `CONTEXTO_REVISADO` no crea anclas
globales y `Fin` por sí solo no crea cortes.

**Todos los enlaces previos entre padres y grupos no afectados se conservan**,
incluidas las dos exposiciones de García de once filas. Sin enlaces nuevos ni
retirados. Se mantienen 3110 institucional, 3421 y el modelo 5212/5742/5802:
**Larraín autor ≠ Vergara lector**, sin inferir asistencia ni habla oral del autor.
Los esquemas XLSX 37/24, once menciones actuales y 21 fórmulas permanecen intactos.
**67 hashes de entradas/código y once de salidas verificados**; la base publicada
coincide campo por campo con el ensayo aislado.

Alertas **321 → 322**; anáforas **2 → 0**, atribuciones legadas **8 → 2**.
El saldo no busca ocultar incertidumbre: los tramos nuevos de Ricaurte ahora
llevan advertencia de identidad. Cero alertas por anáfora no prueba exhaustividad.
La cola histórica conserva **104 intervalos pendientes de lectura contextual**, antes
107. Esta clasificación automática no equivale a tres cierres integrales.
La nueva columna histórica `Variante_Identidad_Pendiente` mantiene **seis intervalos**
pendientes de identidad aunque cambie su método o etiqueta local; no altera los
esquemas 37/24. Conteos históricos y actuales se superponen: **no se suman**.
Las once menciones actuales no son las ocho históricas.

Siguen el puente de 780, 6185, 6443, 2126/3989, residuos de 3191/5367, identidades,
nombres, daños y otras advertencias. Falta cotejo de originales en casos ambiguos
y una muestra independiente con y sin alertas. No hubo nuevo cotejo PDF ni lectura
exhaustiva del corpus.

Publicado en el [PR #3](https://github.com/joako0o/nlm_proyect/pull/3).
**No hay proceso activo.** El [informe anterior](docs/REVISION_LOOP15_2026-09-08.md)
conserva **9.500 filas / 321 alertas / 1.100 pruebas**. Verificaciones locales:
el workflow de GitHub Actions sigue fuera del PR por falta de permiso `workflows`.

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
    alertas_contextuales.json                # incertidumbre de cargo, sin adjudicación automática
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
- Lecturas de menciones actuales: hash, actor, texto y límites vigentes; alcance
  separado de las alertas automáticas y de los estados de las 783 originales.
- Alertas contextuales: fuente, fecha, hash e intervalo vigentes, actor provisional
  y aviso obligatorio; no desaparecen silenciosamente tras una resegmentación.
- Manifiesto de procedencia y cola de revisión explícita.
- Reconstrucción de los 783 intervalos históricos y decisiones de fórmulas con
  citas en los padres; comparación automática separada de lectura dirigida.

La reproducibilidad se verifica por contenido de hojas/estilos y texto, no por
igualdad binaria del ZIP XLSX: los metadatos del archivo incluyen timestamps.

## Límites y uso analítico

- Hay **50 etiquetas nominales de actor** (49 personales y el Consejo), no un censo
  de identidades verificadas. La bajada de 51 a 50 proviene sólo de la etiqueta local
  de 6025 según su nómina. El actor original Vintimilla permanece registrado.
  La variante `Miguel Ricaurte Vintimilla` / `Miguel Ricaurte Bermúdez` sigue advertida:
  no se certifica equivalencia ni se modifican alias globales.
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
