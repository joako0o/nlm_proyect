# nlm_proyect

Actas y reuniones de Política Monetaria (RPM) del Banco Central de Chile, consolidadas en un dataset de 7.219 registros (132 sesiones, 2005-01-11 → 2015-12-17).

## Archivos

- `consolidado_final.xlsx` — base consolidada (hoja `Consolidado`), con `Fecha` como `datetime`.
- `consolidado_goldstandard.xlsx` — versión corregida/auditada.
- `build_gold_standard.py` — script reproducible que genera `consolidado_goldstandard.xlsx` a partir de `consolidado_final.xlsx` (`python3 build_gold_standard.py`).
- `build_textos_completos.py` — re-extrae desde los PDFs el texto íntegro de las filas que tocan/rozan el límite de celda Excel (32.767) y escribe `textos_completos.jsonl`.
- `textos_completos.jsonl` — texto completo (por ID) de las filas largas: ID 280 (2005-06-09) e ID 297 (2005-07-12). Para ID 297 el Excel no puede almacenar el texto completo (≈35.854 caracteres > 32.767), por eso la fuente de verdad es este JSONL.
- `2005-06-09 - Actas.pdf` y `2005-07-12 - Actas.pdf` — PDFs originales usados para la re-extracción (no son parte del dataset; están como fuente de verificación).
- `AUDITORIA_GOLD_STANDARD.md` — informe completo de auditoría y criterios aplicados.

## `consolidado_goldstandard.xlsx`

Hoja `Consolidado` (21 columnas):

`ID, Id_Sesion, Fecha, Actor_Original, Actor_Gold, Actor_Cambia, Rol_Original, Rol_Gold, Rol_Cambia, Rol_Texto, Metodo_Actor, Página, Texto, Tema_Original, Tema_Categoria, Palabra_Clave_Original, Palabra_Clave_Categoria, Texto_Truncado, Duplicado_Exacto, Duplicado_Formula, Nota`

Hojas adicionales: `Calidad`, `Metodo_Actor`, `Diccionario_Rol`, `Diccionario_Actor`, `Diccionario_Categoria`, `Textos_Completos`.

### Resumen de la versión gold

- `Fecha` convertida a **fecha real** con formato `YYYY-MM-DD`.
- `Id_Sesion` = `RPM-YYYY-MM-DD`.
- **Actor re-etiquetado** (quién habla realmente): 535 filas con cambio.
- **Rol corregido**: 181 filas. Política conservadora: `Rol_Gold = Rol_Original` (cargo tal como viene del PDF/source), salvo correcciones indudables (género/subrogante de Hacienda, Rodrigo Valdés como Gerente, actas/meta como `Consejo`).
- `Rol_Texto` conserva el rol reconstruido desde el texto para revisión diferencial.
- Métodos de atribución: `ROL+NOMBRE` (5.000), `NOMBRE+VERBO` (1.368), `ROL+FECHA` (437), `ACTA/META` (309), `ORIGINAL` (105).
- Textos largos resueltos con `textos_completos.jsonl` (ambos con `Texto_Truncado = NO`):
  - ID 280 (2005-06-09): 32.498 caracteres, ya completo en el Excel; verificado contra el PDF.
  - ID 297 (2005-07-12): celda Excel 32.767 (límite), texto íntegro 35.854 caracteres en `textos_completos.jsonl`.
  - La hoja `Textos_Completos` referencia el JSONL, porque el formato XLSX no puede guardar celdas > 32.767.
- Duplicados exactos: **391 registros**; **todos** quedan marcados como fórmula de sesión (`Duplicado_Formula = SI`), conforme a la instrucción de no eliminarlos.
- **Taxonomía canónica** de `Tema` y `Palabra Clave` (11 categorías):
  `acuerdo_comunicado`, `decision_tpm`, `opciones_tpm`, `inflacion`, `mercado_laboral`, `mercados_financieros`, `escenario_internacional`, `politica_fiscal`, `actividad_interna`, `riesgos`, `apertura_cierre`, `debate`, `otros`.
- La columna `Actor_Gold` ya no contiene pseudo-rolles (`Gerente de División Internacional`, etc.).
- No quedan filas `HERENCIA` ni `SIN_DETECTAR`.
