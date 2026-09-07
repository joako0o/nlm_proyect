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

## 2. Truncamiento

- **ID 297** (`2005-07-12`): `Texto` de **32.767 caracteres** (límite de celda Excel) y termina cortado → `Texto_Truncado = SI`.
- **ID 280** (`2005-06-09`): 32.498 caracteres; cerca del límite pero termina en punto → `Texto_Truncado = REV`.
- **No existe en el repositorio** ningún PDF/JSON fuente para re-extraer estos textos en esta sesión. Ambos quedan señalados en la columna `Nota`.

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

## 5. Rol canónico y género

- `Ministra de Hacienda (S)` → `Ministro de Hacienda` en los casos donde el texto habla de “El señor Ministro…” (136 cambios).
- Se mantiene `Ministra de Hacienda (S)` solo para las subrogantes femeninas (María Eugenia Wagner, María Olivia Recart).
- Formalización de subrogantes: `Ministro de Hacienda Subrogante` → `Ministro de Hacienda (S)`.
- El rol **detectado en el texto** prevalece sobre el rol del archivo fuente (incluidos `Consejero`, `Vicepresidente`, `Gerente…`).
- Se normalizaron también roles con errores OCR tipográficos cuando el texto lo permite.

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

- `Actor_Gold` = `Consejo del Banco Central de Chile` ⇔ `Rol_Gold` = `Consejo`: **0 discrepancias** (309 filas en cada lado).
- Sin hablantes pseudo-rol en `Actor_Gold` (p. ej. `Gerente de División Internacional`, `Gerente de Investigación Económica`, `Gerente de Área Técnica`).
- Sin `Rol_Gold` de género inconsistente:
  - `Ministra…` solo con subrogantes femeninas.
  - `Consejera` solo con María Elena Ovalle Molina.
- `Fecha` es `datetime` en las 7.219 filas.
- Métricas finales:
  - Filas: 7.219
  - Sesiones: 132
  - Actores reasignados: **530**
  - Roles corregidos: **1.032**
  - Truncados: **1 SI + 1 REV**
  - Duplicados exactos: **391** (todos marcados fórmula)
  - Textos largos revisar: 1

---

## 8. Limitaciones conocidas

1. **Textos truncados** (ID 297, ID 280) no pudieron re-extraerse porque no hay PDF/JSON en el repositorio.
2. La taxonomía de `Tema`/`Palabra Clave` es **automática** y se basa en palabras clave; una revisión semántica humana puede reducir los casos `otros`.
3. La atribución de hablante usa reglas sobre el texto de las actas; los casos donde el acta no nombra al hablante se resuelven por cargo+mes. Verificar con el documento impreso sigue siendo recomendable para el 100% de “gold”.
4. `consolidado_final.xlsx` permanece **sin modificar**; todo el trabajo está en `consolidado_goldstandard.xlsx`.
