# Auditoría Gold Standard — `consolidado_goldstandard.xlsx`

Fecha de auditoría: 2026-09-06
Base original: `consolidado_final.xlsx` (hoja `Consolidado`, 7.219 filas + cabecera)
Resultado generado: `consolidado_goldstandard.xlsx`

---

## 1. Estructura y cobertura

- 7.219 registros, 8 columnas en la fuente: `ID, Fecha, Actor, Rol, Página, Texto, Tema, Palabra Clave`.
- 132 sesiones mensuales, 2005-01-11 → 2015-12-17.
- `ID` continua de 1 a 7.219, sin duplicados.
- `Fecha` está como **fecha real** (`datetime`) en el gold, con formato `YYYY-MM-DD`.
- Se agregó `Id_Sesion` (`RPM-YYYY-MM-DD`).

---

## 2. Truncamiento / textos largos

Se re-extrajo el texto desde los PDFs originales (`2005-06-09 - Actas.pdf`, `2005-07-12 - Actas.pdf`). El formato XLSX no permite celdas de más de **32.767 caracteres**, así que el texto íntegro se guarda en `textos_completos.jsonl` (misma `ID`):

| ID | Fecha | Excel | Texto completo | Fuente | Estado |
|---|---|---|---|---|---|
| 280 | 2005-06-09 | 32.498 | 32.498 | XLSX original (verificado contra PDF) | completo |
| 297 | 2005-07-12 | 32.767 | 35.854 | PDF re-extraído | completo en JSONL |

- En `consolidado_goldstandard.xlsx` ambas filas quedan con `Texto_Truncado = NO` y una nota que remite a `textos_completos.jsonl`.
- La hoja `Textos_Completos` del workbook hace el mismo enlace.

---

## 3. Duplicados

- **391 registros duplicados exactos** (88 textos distintos repetidos entre sesiones).
- Ninguno se repite dentro de la misma fecha.
- Todos son **fórmulas de acta** repetidas entre sesiones (“El Presidente… agradece…”, “ofrece la palabra…”, “El Consejo adoptó…”, etc.).
- Conforme a la instrucción: **no se eliminan**; quedan marcados con `Duplicado_Exacto = SI` y `Duplicado_Formula = SI` para **los 391 registros**.

---

## 4. Re-etiquetado de Actor (quién habla)

La columna original `Actor` era la mayor fuente de error. En el gold se reconstruye el hablante real a partir del texto, usando heurísticas verificadas:

1. **Rol + nombre** explícito en el texto (`El Gerente de División Estudios, señor Rodrigo Valdés…`).
2. **Nombre + verbo** (`El señor Luis Óscar Herrera manifiesta…`).
3. **Rol genérico + fecha** (`El señor Ministro de Hacienda señala…` / `El Gerente de División Estudios señala…`), con mapa de cargos por fecha.
4. **Acta / meta** (`I. Fecha…`, `En mérito de lo anterior…`, `Conforme a la votación…`, `BANCO CENTRAL DE CHILE ACTA…`).
5. **Original** cuando no hay otra señal y la fila ya era consistente.

### Correcciones destacadas verificadas

- `El Presidente fija la sesión…` → Vittorio Corbo (2005) / José De Gregorio (2007–2011) / Rodrigo Vergara (desde 2011-12).
- `La Ministra de Hacienda Subrogante, señora María Eugenia Wager…` → **María Eugenia Wagner Brizzi** (corrige la variante OCR “Wager”).
- `El señor Felipe Larraín…` → Felipe Larraín Bascuñán, rol `Ministro de Hacienda` (no `Ministra`).
- `El Gerente de División Estudios, señor Rodrigo Valdés…` → Rodrigo Valdés, `Gerente de División Estudios` (antes Ministro de Hacienda).
- `El Gerente de División Operaciones Financieras, señor Esteban Jadresic…` → Esteban Jadresic.
- `El señor Miguel Ricaurte…` se resuelve por fecha: Bermúdez (2012) / Vintimilla (2014).
- `El Gerente de División Estudios Subrogante…` → Igal Magendzo (2007), Claudio Soto (2009/2011).
- `El Gerente de Investigación Económica…` → Klaus Schmidt-Hebbel (2005–2007), Luis Felipe Céspedes (2009–2011), Claudio Raddatz (2012–2014).

### Métodos finales

| Método | Registros |
|---|---|
| `ROL+NOMBRE` | 5.000 |
| `NOMBRE+VERBO` | 1.368 |
| `ROL+FECHA` | 437 |
| `ACTA/META` | 309 |
| `ORIGINAL` | 105 |

**0 filas** con `HERENCIA` o `SIN_DETECTAR`: la atribución quedó completamente resuelta.

---

## 5. Rol canónico y género (política conservadora)

- **`Rol_Gold = Rol_Original`** (el cargo exacto del PDF/source) como regla general.
- Solo se aplican correcciones **indudables**:
  - `Ministra de Hacienda (S)` → `Ministro de Hacienda` cuando el texto habla de “El señor Ministro…” (136 cambios).
  - `Ministro de Hacienda Subrogante` → `Ministro de Hacienda (S)` (6 cambios).
  - Rodrigo Valdés Pulido (2005–2007) cuando el acta lo presenta como **Gerente de División Estudios** (31 cambios).
  - Filas de acta/metadata con `Actor_Gold = Consejo` → `Rol_Gold = Consejo`.
  - Un caso de `Ministra de Hacienda (S)` → `Ministro de Hacienda (S)` (subrogante masculino) y un caso de `Ministro de Hacienda` → `Ministra de Hacienda (S)` (subrogante femenina).
- `Rol_Texto` mantiene el rol reconstruido desde el texto para **revisión diferencial**; su uso no modifica `Rol_Gold`.
- No se reemplazan roles por inferencias textuales (p. ej. “El Consejero señor X” no cambia el rol si el source ya tiene otro cargo).

---

## 6. Taxonomía canónica

Se normalizaron `Tema_Original` y `Palabra_Clave_Original` a categorías canónicas:

`acuerdo_comunicado`, `decision_tpm`, `opciones_tpm`, `inflacion`, `mercado_laboral`, `mercados_financieros`, `escenario_internacional`, `politica_fiscal`, `actividad_interna`, `riesgos`, `apertura_cierre`, `debate`, `otros`.

Distribución de `Tema_Categoria` (top):

- `otros`: 2.446
- `escenario_internacional`: 1.169
- `acuerdo_comunicado`: 1.166
- `mercados_financieros`: 874
- `actividad_interna`: 441
- `mercado_laboral`: 380
- `opciones_tpm`: 221
- `apertura_cierre`: 197
- `riesgos`: 122
- `decision_tpm`: 97
- `politica_fiscal`: 69
- `inflacion`: 20
- `debate`: 17

---

## 7. Controles de consistencia

- **Actor**: sin hablantes pseudo-rol en `Actor_Gold` (p. ej. `Gerente de División Internacional`, `Gerente de Investigación Económica`, `Gerente de Área Técnica`).
- **Roles**: `Rol_Gold` conserva el cargo del PDF/source por política explícita, por lo que **no** se impone `Actor_Gold=Consejo ⇔ Rol_Gold=Consejo`; las diferencias se dejan visibles para comparar con `Rol_Texto`.
- **Género** validado:
  - `Ministra…` solo con subrogantes femeninas.
  - `Consejera` solo con María Elena Ovalle Molina.
- `Fecha` es `datetime` en las 7.219 filas.
- Métricas finales:
  - Filas: 7.219
  - Sesiones: 132
  - Actores reasignados: **530** (535 filas con `Actor_Cambia = SI` contando cambios a Consejo)
  - Roles corregidos: **181**
  - Textos truncados sin resolver: **0**
  - Textos largos sin revisar: **0**
  - Textos con texto completo en `textos_completos.jsonl`: **2** (ID 280, ID 297)
  - Duplicados exactos: **391** (todos marcados fórmula)

---

## 8. Limitaciones conocidas

1. El formato XLSX limita cada celda a 32.767 caracteres; el texto completo de ID 297 no cabe en una celda y reside en `textos_completos.jsonl`.
2. La taxonomía de `Tema`/`Palabra Clave` es **automática** y se basa en palabras clave; una revisión semántica humana puede reducir los casos `otros`.
3. La atribución de hablante usa reglas sobre el texto de las actas; los casos donde el acta no nombra al hablante se resuelven por cargo+mes. Verificar con el documento impreso sigue siendo recomendable para el 100% de “gold”.
4. `consolidado_final.xlsx` conserva el texto del ID 297 en 32.767 caracteres; el texto íntegro está en `textos_completos.jsonl`.
