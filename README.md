# nlm_proyect

Dataset de las Actas y reuniones de Política Monetaria (RPM) del Banco Central de Chile:
132 sesiones entre el 11 de enero de 2005 y el 17 de diciembre de 2015.

## Archivos

- `consolidado_final.xlsx` — base consolidada de entrada (hoja `Consolidado`, 7,219 registros); `Fecha` en formato `datetime`.
- `consolidado_base_referencia.xlsx` — base de referencia generada y auditada (8,493 intervenciones; ver F0 más abajo).
- `consolidado_base_referencia_final.xlsx` — copia final de trabajo con las 13 columnas esenciales.
- `build_base_referencia.py` — script reproducible que genera `consolidado_base_referencia.xlsx` a partir de `consolidado_final.xlsx`.
- `crear_consolidado_final.py` — genera `consolidado_base_referencia_final.xlsx` a partir de `consolidado_base_referencia.xlsx`.
- `qa_gate_f0.py` — compuerta de calidad F0: cardinalidad de actores, decisión de TPM por sesión (una por sesión) y contraste contra la historia oficial de TPM del BCCh.
- `tpm_oficial_bcch.csv` — historia oficial de la Tasa de Política Monetaria (55 cambios, 2004-01-09 → 2015-12-18; `fecha_efectiva` = fecha en que la tasa rige, normalmente el día hábil siguiente a la reunión). Fuente: datosmacro.expansion.com/tipo-interes/chile.
- `build_textos_completos.py` — re-extrae desde los PDFs el texto íntegro de las filas que alcanzan el límite de celda de Excel (32,767 caracteres) y escribe `textos_completos.jsonl`.
- `textos_completos.jsonl` — texto completo de las filas largas (por ID).
- `2005-06-09 - Actas.pdf` y `2005-07-12 - Actas.pdf` — documentos fuente utilizados para la re-extracción.
- `AUDITORIA_BASE_REFERENCIA.md` — informe de auditoría y criterios aplicados.
- `informe_revision_base_referencia_2026-09-07.md` — informe de la revisión más reciente (F0, tipificación de decisiones y contraste con la TPM oficial).

## Estructura de `consolidado_base_referencia_final.xlsx`

Hoja `Consolidado` (13 columnas):

`ID, Fecha, Actor_Final, Rol_Final, Fuente_Actor, Fuente_Rol, Tipo_Acta, Página, Texto, Tema_Categoria, Palabra_Clave_Categoria, Duplicado_Exacto, Duplicado_Formula`

Esta versión contiene únicamente las columnas de consumo final. Se eliminan las columnas de control interno y de auditoría replicadas en la base de referencia: `ID_Padre`, `Id_Sesion`, `Actor_Original`, `Actor_Corregido`, `Rol_Fuente`, `Rol_Corregido`, `Rol_Detectado_Texto`, `Rol_Lista_Asistencia`, `Texto_Truncado` y `Nota`.

## Estructura de `consolidado_base_referencia.xlsx`

Hoja `Consolidado` (25 columnas):

`ID, ID_Padre, Id_Sesion, Fecha, Actor_Original, Actor_Final, Actor_Corregido, Rol_Fuente, Rol_Final, Rol_Corregido, Rol_Detectado_Texto, Rol_Lista_Asistencia, Fuente_Rol, Tipo_Acta, Fuente_Actor, Página, Texto, Tema_Original, Tema_Categoria, Palabra_Clave_Original, Palabra_Clave_Categoria, Texto_Truncado, Duplicado_Exacto, Duplicado_Formula, Nota`

Hojas adicionales: `Calidad`, `Fuente_Actor`, `Fuente_Rol`, `Diccionario_Rol`, `Diccionario_Actor`, `Diccionario_Categoria`, `Textos_Completos`.

## Contenido principal

- **7,219 filas originales** que se segmentan en **8,493 intervenciones** (843 filas originales contienen más de una intervención).
- `ID` consecutivo de la intervención; `ID_Padre` conserva el identificador de la fila original.
- `Fecha` en formato `YYYY-MM-DD` y `Id_Sesion` con la forma `RPM-AAAA-MM-DD`.
- El hablante de cada intervención se reconstruye desde el texto y queda en `Actor_Final`.
- `Fuente_Actor` describe el método de atribución:
  `ROL+NOMBRE` (5,384), `NOMBRE+VERBO` (1,800), `ROL+FECHA` (703), `ACTA/META` (466), `PRIMERA_ORACION` (55), `ORIGINAL` (85).
- `Fuente_Rol` indica el origen del cargo:
  `LISTA_ASISTENCIA` (8,021), `ACTA_INSTITUCIONAL` (466), `PENDIENTE_REVISION` (6).
- `Tipo_Acta` clasifica las filas institucionales: `ACTA_CABECERA` (130), `ACUERDO_CONSEJO` (197), `COMUNICADO` (93), `META_SESION` (101) o `ACTA_INSTITUCIONAL` (2).
- Las filas sin cargo único o exacto en la lista de asistencia quedan en `PENDIENTE_REVISION` y deben revisarse manualmente.
- `textos_completos.jsonl` es la fuente de verdad para las celdas que superan el límite de 32,767 caracteres del formato XLSX.

### Cardinalidad de actores

`Actor_Final` toma **51 valores: 50 personas + el Consejo del Banco Central de Chile** (466 filas institucionales).
El plan original estimaba 60–80 actores: esa cifra es incorrecta y fue corregida.
Seis personas aparecen una sola vez (n=1): Alfredo Pistelli, Ari Aisen, María Eugenia Wagner Brizzi, Pablo Pincheira Brown, Rodrigo Alfaro y Rodrigo Álvarez Zenteno.

## Compuerta de calidad F0 (`qa_gate_f0.py`)

Verificación reproducible de la base de referencia (ver `informe_revision_base_referencia_2026-09-07.md`):

- **F0(a) Cardinalidad:** 50 personas + Consejo = 51 valores de `Actor_Final`.
- **F0(b) Decisión por sesión:** las 132 sesiones rinden exactamente una decisión de TPM (Δ pb y/o tasa objetivo); la fila que la porta queda tipificada `ACUERDO_CONSEJO` (0 mis-tipificadas).
- **F0(c) Contraste contra la historia oficial:** cada decisión se valida contra `tpm_oficial_bcch.csv`. La sesión adopta la siguiente tasa oficial sólo si su fecha efectiva cae dentro de los 10 días posteriores a la reunión (`CHANGE_WINDOW_DAYS = 10`); en caso contrario mantiene la tasa vigente. Resultado actual: **132/132 OK, 0 discrepancias**.

Veredicto actual: **F0 PASA**.

## Segmentación (una intervención por fila)

- Cada fila tiene un único hablante; las filas originales con varias intervenciones se dividen.
- Las transiciones sin discurso quedan con quien entrega la palabra; no se divide una oración que sólo continúa al hablante anterior.
- Las filas de acta/metadatos (cabecera, suspensión/reanudación, acuerdo, comunicado) no se dividen, pero el bloque de acuerdo que llega pegado al discurso de cierre del Presidente (típico 2013–2015) se separa como fila institucional propia (`Actor_Final` = Consejo).
- Las filas de persona cuyo discurso porta la fórmula de la decisión vigente (p.ej. «…deja constancia que se acuerda por unanimidad mantener la tasa…») conservan al hablante y se marcan `Tipo_Acta = ACUERDO_CONSEJO`.

## Reproducibilidad

```bash
python build_base_referencia.py       # regenera consolidado_base_referencia.xlsx
python crear_consolidado_final.py     # regenera la copia final de 13 columnas
python qa_gate_f0.py                  # compuerta F0 (debe terminar en VEREDICTO F0: PASA)
```
