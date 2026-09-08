# nlm_proyect — Preparación de actas RPM del Banco Central de Chile

Corpus de **132 sesiones mensuales de 2005–2015**, preparado a partir de un
consolidado de 7.219 filas. La salida actual tiene **9.353 filas físicas de
Excel / 9.352 bloques de texto**, con actor, cargo, trazabilidad y alertas de revisión.
Una intervención extensa ocupa dos filas por el límite de XLSX. Además,
**301 grupos comparten varias filas bajo un mismo `ID_Turno`**, con hasta
11 filas consecutivas en una exposición; no se fusionan los registros de origen.

## Estado actual — 2026-09-07

**F0 y F1 pasan, con 432 pruebas de regresión. Esto no certifica pureza semántica
total de cada intervención.** Quedan **580 filas con alertas** para revisión
dirigida. Los seis cargos antes pendientes tienen ahora evidencia documental
versionada (cuatro citas directas y dos de la misma sesión), no asistencia inventada.
Las alertas se superponen y pueden ser falsos positivos; no son 580 errores
confirmados. Tampoco `SIN_ALERTAS_AUTOMATICAS` equivale a revisión humana.

La revisión corrigió textos recuperados que no se estaban incorporando,
transiciones de hablantes, menciones confundidas con sujetos, categorías con
tildes, validación parcial de TPM y marcas de duplicados heredadas del padre.

**Informe vigente:** [sexto bloque: pasada amplia de suspensiones, retornos y votos](docs/REVISION_LOOP6_2026-09-07.md).
Se encadenaron tres ciclos: **59 padres corregidos**, de 74 a 176 segmentos,
con **102 filas nuevas**, y dos menciones legítimas documentadas sin suprimir
avisos. La familia de suspensión/reanudación permitió abordar 48 pasajes:
45 cambiaron y tres ya estaban correctos. Se conservaron las exposiciones,
las disidencias y los daños literales; no se inventó asistencia del Ministro.

Se comprobaron 18 enlaces de continuidad y las dos exposiciones de once filas.
Las revisiones contextuales no crean por sí solas anclas de agrupación. El
[punto de reanudación](docs/estado_revision_loop6_2026-09-07.json) registra
pendientes y alcance. La pasada está publicada y se incorpora al
[PR #3](https://github.com/joako0o/nlm_proyect/pull/3); **no hay un proceso activo
en segundo plano**.

De las 783 alertas originales, **388** están pendientes de lectura contextual,
59 son fórmulas reclasificadas, 71 tienen método actualizado, **157** presentan
cambios por comparación, **84** tienen una corrección dirigida aplicada, siete
son breves válidos, ocho menciones revisadas, seis identidades pendientes, dos
repeticiones sustantivas y una continuidad documentada. **No es una revisión
exhaustiva de las 783 filas.** Las **diez** anotaciones de menciones actuales se
cuentan aparte y conservan sus avisos.

Las filas con alertas pasan de **615 a 580**; el motivo de otro hablante/mención,
de 76 a 26. Hay cinco nuevos avisos de puntuación por límites que conservan
el daño original. Los motivos se solapan; su reducción no cuenta errores
confirmados. No hay cambios adicionales de metadatos semánticos fuera de los
59 padres; las anotaciones se añaden al seguimiento/cola.

Quedan **ocho candidatos prioritarios** sin anotación de mención: **780, 3191,
5212, 5367, 5647, 5742, 5802 y 6185**. **No son ocho pendientes totales:** siguen
580 filas con alertas y 388 intervalos originales pendientes de lectura contextual.
Los textos escritos del Ministro leídos por el Presidente se documentaron con
[propuestas de intervalos no aplicadas](docs/propuestas_documentales_loop6_2026-09-07.json),
distinguiendo autor y lector. Persisten casos conjuntos, daños de fuente,
identidades, repeticiones y necesidad de revisión independiente con y sin alertas.

El [informe anterior](docs/REVISION_LOOP5_2026-09-07.md) conserva el estado
histórico de **9.251 filas / 615 alertas / 351 pruebas**. Las verificaciones son
locales: el workflow propuesto de GitHub Actions sigue fuera del PR por falta
de permiso `workflows` en la conexión.

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
    formulas_revisadas.json                   # 18 fórmulas; 59 citas históricas + 4 actuales
    revisiones_menciones_actuales.json       # diez lecturas acotadas; no suprimen alertas
    revisiones_roles.json                    # seis cargos: citas, sesión, hash y justificación
    revisiones_hablantes.json                # 91 intervalos acotados con citas y hash
  processed/
    consolidado_base_referencia.xlsx          # 9.353 filas, 37 columnas + hojas de auditoría
    consolidado_base_referencia_final.xlsx    # 9.353 filas, 24 columnas
    textos_completos.jsonl                    # 2 textos de origen completos
    decisiones_tpm.csv                       # una fila por sesión, con IDs de evidencia
    revision_783.xlsx                        # seguimiento original + cola actual, tres hojas
    revision_783.csv                         # 783 intervalos con estado/evidencia/IDs actuales
    resumen_revision_783.json                # balance de estados; no cierres semánticos
    revision_pendientes.csv                  # alertas, contexto y alcance de lecturas dirigidas
    turnos_habla.csv                         # grupos de continuidad, sin duplicar texto completo
    qa_preparacion.json                      # métricas y errores bloqueantes
    manifiesto_preparacion.json              # SHA-256 de entradas, código y salidas
scripts/
  preparar_data.py                           # construcción + pruebas + QA + publicación
  build_textos_completos.py                  # recuperación PDF sin borrar cifras económicas
  build_base_referencia.py                   # construcción de la base de auditoría
  turns.py                                  # sujetos de habla y contexto local
  mention_reviews.py                        # valida lecturas actuales, sin cambiar actores/alertas
  continuity.py                             # continuidad entre párrafos con anclas de evidencia
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
| `Actor_Final` | Persona atribuida o Consejo del BCCh |
| `Rol_Final` | Cargo en la sesión; consultar su fuente y alertas |
| `Fuente_Actor` | Evidencia de atribución: sujeto explícito, cargo de sesión, anáfora, contexto revisado, encabezado de minuta o heurística legada |
| `Fuente_Rol` | `LISTA_ASISTENCIA`, `ACTA_INSTITUCIONAL`, `TEXTO_EXPLICITO_REVISADO`, `CONTEXTO_SESION_REVISADO` o `PENDIENTE_REVISION` |
| `Tipo_Acta` | Etiqueta institucional/decisión o `MINUTA_PERSONAL`; vacío en otras intervenciones, por diseño |
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
continuidad. Las minutas tienen relación `DOCUMENTO_PERSONAL` y tampoco se
heredan como turnos hablados. Las notas de auditoría enlazan las decisiones de
curación con sus IDs; la revisión fue del consolidado, no de los PDFs.

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
- Correspondencia exacta entre base de auditoría y proyección final.
- Cadenas de continuidad: anclas explícitas, antecedentes contiguos, misma
  persona/sesión, sin saltar barreras institucionales ni cesiones de palabra.
- Lecturas de menciones actuales: hash, actor, texto y límites vigentes; alcance
  separado de las alertas automáticas y de los estados de las 783 originales.
- Manifiesto de procedencia y cola de revisión explícita.
- Reconstrucción de los 783 intervalos históricos y decisiones de fórmulas con
  citas en los padres; comparación automática separada de lectura dirigida.

La reproducibilidad se verifica por contenido de hojas/estilos y texto, no por
igualdad binaria del ZIP XLSX: los metadatos del archivo incluyen timestamps.

## Límites y uso analítico

- Hay **51 etiquetas de actor**, no una certificación de 51 identidades distintas.
  Se señala la variante `Miguel Ricaurte Vintimilla` / `Miguel Ricaurte Bermúdez`
  para verificarla antes de fusionar o tratar ambos nombres como personas distintas.
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
