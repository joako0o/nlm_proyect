# nlm_proyect — Preparación de actas RPM del Banco Central de Chile

Corpus de **132 sesiones mensuales de 2005–2015**, preparado a partir de un
consolidado de 7.219 filas. La salida actual tiene **9.245 filas físicas de
Excel / 9.244 bloques de texto**, con actor, cargo, trazabilidad y alertas de revisión.
Una intervención extensa ocupa dos filas por el límite de XLSX. Además,
**301 grupos comparten varias filas bajo un mismo `ID_Turno`**, con hasta
11 filas consecutivas en una exposición; no se fusionan los registros de origen.

## Estado actual — 2026-09-07

**F0 y F1 pasan, con 339 pruebas de regresión. Esto no certifica pureza semántica
total de cada intervención.** Quedan **618 filas con alertas** para revisión
dirigida. Los seis cargos antes pendientes tienen ahora evidencia documental
versionada (cuatro citas directas y dos de la misma sesión), no asistencia inventada.
Las alertas se superponen y pueden ser falsos positivos; no son 618 errores
confirmados. Tampoco `SIN_ALERTAS_AUTOMATICAS` equivale a revisión humana.

La revisión corrigió textos recuperados que no se estaban incorporando,
transiciones de hablantes, menciones confundidas con sujetos, categorías con
tildes, validación parcial de TPM y marcas de duplicados heredadas del padre.

**Informe vigente:** [cuarto bloque: votos, complementos y retornos de exposición](docs/REVISION_LOOP4_2026-09-07.md).
Se corrigieron **3800, 3810, 3813, 3887, 3906, 4220, 4224, 4341 y 4357**:
nueve padres pasan de 12 a 22 segmentos, con diez filas nuevas. Se separan
votos, complementos y retornos sin recortar exposiciones ni reconstruir frases
dañadas. Se recuperó **3810 → 3811**, la continuación de Marshall, y se
conservaron 17 enlaces previos comprobados y las dos exposiciones de once filas.
Las revisiones contextuales no crean por sí solas anclas de continuidad:
3887 → 3888 y 4224 → 4225 no se agrupan automáticamente bajo un mismo turno.
El [punto de reanudación](docs/estado_revision_loop4_2026-09-07.json) registra
pendientes y candidatos. Los tres ciclos están publicados; **no hay un proceso
activo en segundo plano**.

De las 783 alertas originales, **440** están pendientes de lectura contextual,
59 son fórmulas reclasificadas, 72 tienen método actualizado, **123** presentan
cambios por comparación, **65** tienen una corrección dirigida aplicada, siete
son breves válidos, ocho menciones revisadas, seis identidades pendientes, dos
repeticiones sustantivas y una continuidad documentada. **No es una revisión
exhaustiva de las 783 filas.** Las ocho lecturas de menciones actuales se cuentan
aparte, permanecen idénticas y conservan sus avisos.

En este bloque, las alertas pasan de **623 a 618**: ocho avisos netos menos de
posible otro hablante, cuatro más de puntuación y uno menos de atribución legada.
Los motivos se superponen; el contador no mide errores confirmados. Además de
los nueve padres estructurales, sólo cambian metadatos en 3811 (continuidad),
5231 (método explícito, mismo actor/texto) y **5647 (nuevo aviso, sin adjudicar)**.
Quedan **63 candidatos** bajo el filtro de otro hablante sin anotación de mención.
**3191 sigue pendiente por su coincidencia conjunta**, junto con los residuos
anteriores. Falta continuar la cola, el cotejo documental y la revisión semántica
independiente. Se separan cambios de voz con evidencia, no cada oración,
cada párrafo ni cada nombre mencionado.

El [informe anterior](docs/REVISION_LOOP3_2026-09-07.md) y sus evidencias se
conservan como registro histórico de la publicación de **9.235 filas / 623
alertas / 318 pruebas**.

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
    revisiones_menciones_actuales.json       # ocho lecturas acotadas; no suprimen alertas
    revisiones_roles.json                    # seis cargos: citas, sesión, hash y justificación
    revisiones_hablantes.json                # 70 intervalos acotados con citas y hash
  processed/
    consolidado_base_referencia.xlsx          # 9.245 filas, 37 columnas + hojas de auditoría
    consolidado_base_referencia_final.xlsx    # 9.245 filas, 24 columnas
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
