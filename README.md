# nlm_proyect

Dataset de las Actas y reuniones de Política Monetaria (RPM) del Banco Central de Chile:
132 sesiones entre el 11 de enero de 2005 y el 17 de diciembre de 2015.

## Archivos

- `consolidado_final.xlsx` — base consolidada de entrada (hoja `Consolidado`, 7,219 registros); `Fecha` en formato `datetime`.
- `consolidado_base_referencia.xlsx` — base de referencia generada y auditada.
- `build_base_referencia.py` — script reproducible que genera `consolidado_base_referencia.xlsx` a partir de `consolidado_final.xlsx`.
- `build_textos_completos.py` — re-extrae desde los PDFs el texto íntegro de las filas que alcanzan el límite de celda de Excel (32,767 caracteres) y escribe `textos_completos.jsonl`.
- `textos_completos.jsonl` — texto completo de las filas largas (por ID).
- `2005-06-09 - Actas.pdf` y `2005-07-12 - Actas.pdf` — documentos fuente utilizados para la re-extracción.
- `AUDITORIA_BASE_REFERENCIA.md` — informe de auditoría y criterios aplicados.
- `informe_revision_base_referencia_2026-09-07.md` — informe de la revisión más reciente (casos pendientes y validación de los parentes divididos).

## Estructura de `consolidado_base_referencia.xlsx`

Hoja `Consolidado` (25 columnas):

`ID, ID_Padre, Id_Sesion, Fecha, Actor_Original, Actor_Final, Actor_Corregido, Rol_Fuente, Rol_Final, Rol_Corregido, Rol_Detectado_Texto, Rol_Lista_Asistencia, Fuente_Rol, Tipo_Acta, Fuente_Actor, Página, Texto, Tema_Original, Tema_Categoria, Palabra_Clave_Original, Palabra_Clave_Categoria, Texto_Truncado, Duplicado_Exacto, Duplicado_Formula, Nota`

Hojas adicionales: `Calidad`, `Fuente_Actor`, `Fuente_Rol`, `Diccionario_Rol`, `Diccionario_Actor`, `Diccionario_Categoria`, `Textos_Completos`.

## Contenido principal

- **7,219 filas originales** que se segmentan en **8,302 intervenciones** (708 filas originales contienen más de una intervención).
- `ID` consecutivo de la intervención; `ID_Padre` conserva el identificador de la fila original.
- `Fecha` en formato `YYYY-MM-DD` y `Id_Sesion` con la forma `RPM-AAAA-MM-DD`.
- El hablante de cada intervención se reconstruye desde el texto y queda en `Actor_Final`.
- `Fuente_Actor` describe el método de atribución:
  `ROL+NOMBRE` (5,358), `NOMBRE+VERBO` (1,799), `ROL+FECHA` (698), `ACTA/META` (309), `PRIMERA_ORACION` (54), `ORIGINAL` (84).
- `Fuente_Rol` indica el origen del cargo:
  `LISTA_ASISTENCIA` (7,987), `ACTA_INSTITUCIONAL` (309), `PENDIENTE_REVISION` (6).
- `Tipo_Acta` clasifica las filas institucionales: `ACTA_CABECERA`, `ACUERDO_CONSEJO`, `COMUNICADO`, `META_SESION` o `ACTA_INSTITUCIONAL`.
- Las filas sin cargo único o exacto en la lista de asistencia quedan en `PENDIENTE_REVISION` y deben revisarse manualmente.
- `textos_completos.jsonl` es la fuente de verdad para las celdas que superan el límite de 32,767 caracteres del formato XLSX.
