# nlm_proyect — Actas RPM del Banco Central de Chile (2005–2015)

Dataset procesado de las Actas de las Reuniones de Política Monetaria (RPM)
del Banco Central de Chile: **132 sesiones mensuales** entre el 11-01-2005 y
el 17-12-2015, con hablante y cargo reconstruidos a partir del texto,
decisiones de TPM tipificadas (`ACUERDO_CONSEJO`) y verificadas contra la
historia oficial de la tasa (`data/external/tpm_oficial_bcch.csv`).

**Estado de calidad: compuerta F0 PASA** (cardinalidad de actores, una
decisión de TPM por sesión y contraste con la TPM oficial sin discrepancias).

## Estructura del repositorio

```
nlm_proyect/
├── README.md
├── data/
│   ├── raw/                          # entradas originales (no generadas)
│   │   ├── consolidado_final.xlsx    # consolidado de entrada (7,219 filas)
│   │   ├── 2005-06-09 - Actas.pdf    # PDFs fuente de la re-extracción
│   │   └── 2005-07-12 - Actas.pdf
│   ├── external/                     # datos oficiales de referencia
│   │   └── tpm_oficial_bcch.csv      # 55 cambios de TPM 2004-2015 (fecha efectiva)
│   └── processed/                    # salidas generadas (reproducibles con los scripts)
│       ├── consolidado_base_referencia.xlsx        # base de referencia (8,493 filas, auditoría)
│       ├── consolidado_base_referencia_final.xlsx  # copia final de trabajo (13 columnas)
│       └── textos_completos.jsonl                 # texto íntegro de filas largas (límite XLSX)
├── scripts/
│   ├── descargar_actas_rpm.py        # auxiliar (máquina local): descarga de actas BCCh
│   ├── build_textos_completos.py     # re-extracción de textos largos desde los PDFs
│   ├── build_base_referencia.py      # genera la base de referencia
│   ├── crear_consolidado_final.py    # genera la copia final de 13 columnas
│   ├── qa_gate_f0.py                 # compuerta de calidad F0
│   └── roster.py                     # utilidades de nombres/cargos (usado por el builder)
└── docs/
    ├── AUDITORIA_BASE_REFERENCIA.md                    # auditoría y criterios
    └── informe_revision_base_referencia_2026-09-07.md  # revisión + compuerta F0
```

## Pipeline

```
data/raw/consolidado_final.xlsx ──┬─> scripts/build_textos_completos.py ──> data/processed/textos_completos.jsonl
                                  │         (re-extrae desde data/raw/*.pdf los textos que
                                  │          alcanzan el límite de celda de Excel: 32,767 chars)
                                  │
                                  └─> scripts/build_base_referencia.py ───> data/processed/consolidado_base_referencia.xlsx
                                           (segmenta en intervenciones, atribuye hablante y cargo,
                                            tipifica filas institucionales; usa textos_completos.jsonl
                                            y scripts/roster.py)
                                                    │
                                                    └─> scripts/crear_consolidado_final.py
                                                            ──> data/processed/consolidado_base_referencia_final.xlsx

scripts/qa_gate_f0.py ── valida data/processed/consolidado_base_referencia.xlsx contra
                         data/external/tpm_oficial_bcch.csv  ──> VEREDICTO F0: PASA
```

## Reproducibilidad

Requisitos: Python 3.10+ con `openpyxl` y `pypdf` (`pip install openpyxl pypdf`).
`scripts/descargar_actas_rpm.py` además requiere Playwright y se ejecuta en la
máquina local (el repositorio digital del BCCh bloquea descargas automáticas).

Desde la raíz del repositorio:

```bash
python scripts/build_textos_completos.py    # opcional: regenera textos_completos.jsonl (byte-idéntico)
python scripts/build_base_referencia.py     # regenera la base de referencia (8,493 filas)
python scripts/crear_consolidado_final.py   # regenera la copia final de 13 columnas
python scripts/qa_gate_f0.py                # debe terminar en VEREDICTO F0: PASA
```

Los scripts resuelven sus rutas desde la raíz del repositorio, por lo que
pueden ejecutarse desde cualquier directorio.

## Datos de salida

### `data/processed/consolidado_base_referencia_final.xlsx` (copia final)

Hoja `Consolidado` con **8,493 filas** y 13 columnas:

| Columna | Descripción |
|---|---|
| `ID` | Identificador consecutivo de la intervención |
| `Fecha` | Fecha real de la sesión (`YYYY-MM-DD`) |
| `Actor_Final` | Hablante reconstruido desde el texto (50 personas + Consejo del BCCh) |
| `Rol_Final` | Cargo canónico del hablante en la sesión |
| `Fuente_Actor` | Método de atribución del hablante |
| `Fuente_Rol` | Origen del cargo |
| `Tipo_Acta` | Clasificación de filas institucionales |
| `Página` | Página del PDF original |
| `Texto` | Texto de la intervención |
| `Tema_Categoria` | Categoría temática del tema original |
| `Palabra_Clave_Categoria` | Categoría temática de la palabra clave original |
| `Duplicado_Exacto` | `SI` si el texto está duplicado exacto (fórmulas de sesión; no se eliminan) |
| `Duplicado_Formula` | `SI` si el duplicado corresponde a una fórmula de acta |

### `data/processed/consolidado_base_referencia.xlsx` (base de auditoría)

Hoja `Consolidado` con las mismas 8,493 filas y 25 columnas (las 13 anteriores
más las columnas de control: `ID_Padre`, `Id_Sesion`, `Actor_Original`,
`Actor_Corregido`, `Rol_Fuente`, `Rol_Corregido`, `Rol_Detectado_Texto`,
`Rol_Lista_Asistencia`, `Texto_Truncado`, `Nota`).
Hojas adicionales: `Calidad`, `Fuente_Actor`, `Fuente_Rol`, `Diccionario_Rol`,
`Diccionario_Actor`, `Diccionario_Categoria`, `Textos_Completos`.

`data/processed/textos_completos.jsonl` es la fuente de verdad para las celdas
que superan el límite de 32,767 caracteres del formato XLSX.

## Contenido y estadísticas

| Indicador | Valor |
|---|---|
| Sesiones | 132 (2005-01-11 → 2015-12-17) |
| Filas originales (`data/raw/consolidado_final.xlsx`) | 7,219 |
| Intervenciones tras segmentar | 8,493 |
| Filas originales divididas | 843 |
| `Actor_Final` | 51 valores = 50 personas + Consejo del BCCh (466 filas institucionales) |
| Actores con n=1 | 6: Alfredo Pistelli, Ari Aisen, María Eugenia Wagner Brizzi, Pablo Pincheira Brown, Rodrigo Alfaro, Rodrigo Álvarez Zenteno |
| `Fuente_Actor` | `ROL+NOMBRE` 5,384 · `NOMBRE+VERBO` 1,800 · `ROL+FECHA` 703 · `ACTA/META` 466 · `ORIGINAL` 85 · `PRIMERA_ORACION` 55 |
| `Fuente_Rol` | `LISTA_ASISTENCIA` 8,021 · `ACTA_INSTITUCIONAL` 466 · `PENDIENTE_REVISION` 6 |
| `Tipo_Acta` | `ACTA_CABECERA` 130 · `ACUERDO_CONSEJO` 197 · `COMUNICADO` 93 · `META_SESION` 101 · `ACTA_INSTITUCIONAL` 2 |
| Duplicados exactos | 391 (fórmulas de sesión; marcados, no eliminados) |
| Registros `PENDIENTE_REVISION` | 6 (ver `docs/informe_revision_base_referencia_2026-09-07.md` §1) |

### Cardinalidad de actores

El plan original estimaba 60–80 actores: esa cifra era incorrecta y fue
corregida. `Actor_Final` toma **50 personas + el Consejo del Banco Central de
Chile**.

## Compuerta de calidad F0 (`scripts/qa_gate_f0.py`)

| Control | Resultado |
|---|---|
| **F0(a)** Cardinalidad de actores | 50 personas + Consejo = 51 valores de `Actor_Final` |
| **F0(b)** Decisión de TPM por sesión | 132/132 sesiones con exactamente una decisión parseada; 0 filas mis-tipificadas |
| **F0(c)** Contraste contra TPM oficial | 132/132 OK contra `data/external/tpm_oficial_bcch.csv`; 0 discrepancias |

Detalles de la ventana de eficacia (`CHANGE_WINDOW_DAYS = 10`) y la resolución
de los 9 casos sospechosos: `docs/informe_revision_base_referencia_2026-09-07.md` §3.

## Criterios de segmentación

- Cada fila tiene un único hablante; las filas originales con varias
  intervenciones se dividen (verificación: la concatenación de segmentos
  reproduce el texto original en 7,219/7,219 filas).
- Las transiciones sin discurso quedan con quien entrega la palabra; no se
  divide una oración que sólo continúa al hablante anterior.
- Las filas de acta/metadatos (cabecera, suspensión/reanudación, acuerdo,
  comunicado) no se dividen; el bloque de acuerdo que llega pegado al discurso
  de cierre del Presidente (típico 2013–2015) se separa como fila
  institucional propia (`Actor_Final` = Consejo).
- Las filas de persona cuyo discurso porta la fórmula de la decisión vigente
  (p.ej. «…deja constancia que se acuerda por unanimidad mantener la tasa…»)
  conservan al hablante y se marcan `Tipo_Acta = ACUERDO_CONSEJO`.

## Documentación

- `docs/AUDITORIA_BASE_REFERENCIA.md` — auditoría completa de la base:
  cobertura, trazabilidad, métodos de atribución, tipificación, duplicados.
- `docs/informe_revision_base_referencia_2026-09-07.md` — revisión más
  reciente: casos `PENDIENTE_REVISION`, auditoría de filas divididas y
  compuerta F0 con la resolución de los 9 casos sospechosos.

## Datos externos

- `data/external/tpm_oficial_bcch.csv` — historia oficial de la Tasa de
  Política Monetaria: 55 cambios efectivos entre el 2004-01-09 (1,75%) y el
  2015-12-18 (3,50%). `fecha_efectiva` es la fecha en que la tasa comienza a
  regir (por regla general, el día hábil siguiente a la reunión), no la fecha
  de la reunión. Fuente: datosmacro.expansion.com/tipo-interes/chile; la
  sesión de febrero de 2008 se validó además contra la página oficial del BCCh.
