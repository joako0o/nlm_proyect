# Auditoría de la base de referencia del consolidado RPM

**Fecha de auditoría:** 2026-09-07
**Base de entrada:** `consolidado_final.xlsx` (hoja `Consolidado`, 7,219 filas + encabezado)
**Base de referencia:** `consolidado_base_referencia.xlsx`

## 1. Cobertura

- 132 sesiones mensuales, entre el 11 de enero de 2005 y el 17 de diciembre de 2015.
- 7,219 filas originales, segmentadas en **8,302 intervenciones**.
- 708 filas originales contienen más de una intervención y fueron divididas.
- La suma de los segmentos de cada fila reproduce íntegramente el texto original; no hay registros vacíos ni pérdida de contenido.

## 2. Trazabilidad

- `ID`: identificador consecutivo de cada intervención.
- `ID_Padre`: identificador de la fila original en `consolidado_final.xlsx`.
- `Fecha`: fecha real de la sesión, formato `YYYY-MM-DD`.
- `Id_Sesion`: `RPM-AAAA-MM-DD`.

## 3. Atribución de hablante

El hablante se asigna a partir del texto de cada intervención:

| Método | Registros |
|---|---|
| `ROL+NOMBRE` | 5,358 |
| `NOMBRE+VERBO` | 1,799 |
| `ROL+FECHA` | 698 |
| `ACTA/META` | 309 |
| `PRIMERA_ORACION` | 54 |
| `ORIGINAL` | 84 |

Diferencias con la atribución original: **1,345 cambios**.

## 4. Asignación de cargo

El cargo canónico proviene de la lista de asistencia del párrafo inicial de cada acta cuando la coincidencia entre nombre y cargo es única y exacta.

| Origen | Registros |
|---|---|
| `LISTA_ASISTENCIA` | 7,987 |
| `ACTA_INSTITUCIONAL` | 309 |
| `PENDIENTE_REVISION` | 6 |

Diferencias con el cargo original: **1,987 cambios**.

## 5. Clasificación de las filas institucionales

Las filas de acta se diferencian con `Tipo_Acta`:

- `ACTA_CABECERA`
- `ACUERDO_CONSEJO`
- `COMUNICADO`
- `META_SESION`
- `ACTA_INSTITUCIONAL`

## 6. Textos largos

Se re-extrajo el contenido completo desde los PDFs originales para las celdas que alcanzan el límite de 32,767 caracteres del formato XLSX. La fuente de verdad se conserva en `textos_completos.jsonl`. La hoja `Textos_Completos` referencia esos registros.

## 7. Duplicados

Los 391 registros duplicados exactos corresponden a fórmulas de sesión repetidas entre actas. Conforme al criterio definido, **no se eliminan**; quedan marcados con `Duplicado_Exacto = SI` y `Duplicado_Formula = SI`.

## 8. Casos pendientes de revisión

Quedan **6 registros** en `PENDIENTE_REVISION` porque el párrafo inicial de la sesión no permite una coincidencia única y exacta entre nombre y cargo. Corresponden a invitados, ausentes que intervienen posteriormente o listas de asistencia incompletas en el OCR. Requieren verificación manual.
