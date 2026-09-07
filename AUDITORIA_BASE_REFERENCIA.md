# Auditoría de la base de referencia del consolidado RPM

**Fecha de auditoría:** 2026-09-07 (actualizada tras la compuerta F0)
**Base de entrada:** `consolidado_final.xlsx` (hoja `Consolidado`, 7,219 filas + encabezado)
**Base de referencia:** `consolidado_base_referencia.xlsx`

## 1. Cobertura

- 132 sesiones mensuales, entre el 11 de enero de 2005 y el 17 de diciembre de 2015.
- 7,219 filas originales, segmentadas en **8,493 intervenciones**.
- 843 filas originales contienen más de una intervención y fueron divididas.
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
| `ROL+NOMBRE` | 5,384 |
| `NOMBRE+VERBO` | 1,800 |
| `ROL+FECHA` | 703 |
| `ACTA/META` | 466 |
| `PRIMERA_ORACION` | 55 |
| `ORIGINAL` | 85 |

Diferencias con la atribución original: **1,347 cambios**.

### Cardinalidad de actores

`Actor_Final` toma **51 valores: 50 personas + el Consejo del Banco Central de Chile** (466 filas institucionales). El plan original (60–80 actores) era incorrecto y fue corregido. Seis personas aparecen una sola vez: Alfredo Pistelli, Ari Aisen, María Eugenia Wagner Brizzi, Pablo Pincheira Brown, Rodrigo Alfaro y Rodrigo Álvarez Zenteno.

## 4. Asignación de cargo

El cargo canónico proviene de la lista de asistencia del párrafo inicial de cada acta cuando la coincidencia entre nombre y cargo es única y exacta.

| Origen | Registros |
|---|---|
| `LISTA_ASISTENCIA` | 8,021 |
| `ACTA_INSTITUCIONAL` | 466 |
| `PENDIENTE_REVISION` | 6 |

Diferencias con el cargo original: **2,107 cambios**.

## 5. Clasificación de las filas institucionales

Las filas de acta se diferencian con `Tipo_Acta`:

| Tipo | Registros | Descripción |
|---|---|---|
| `ACTA_CABECERA` | 130 | Cabecera del acta de la sesión |
| `ACUERDO_CONSEJO` | 197 | Fila que porta la decisión de TPM de la sesión |
| `COMUNICADO` | 93 | Texto del comunicado oficial |
| `META_SESION` | 101 | Metadatos de sesión (suspensiones, reanudaciones, retiros, incorporaciones) |
| `ACTA_INSTITUCIONAL` | 2 | Otras filas institucionales del acta |

Criterios de tipificación de la decisión (`ACUERDO_CONSEJO`):

- La fila contiene la fórmula canónica del acta/comunicado («En su reunión mensual de política monetaria, el Consejo … acordó/decidió/resolvió/acuerda mantener|aumentar|reducir … la tasa …»), la fórmula 2005 («Se acuerda … la tasa …») o un verbo de acuerdo con bloque de votación próximo («Conforme a la votación …», «En mérito de lo anterior …», «por votación unánime»).
- Se excluyen las recapitulaciones de la decisión del mes anterior («En la última Reunión …», «En la reunión de política monetaria de <mes> …»), típicas de la presentación de Opciones.
- Los patrones toleran saltos de línea y espacios OCR incrustados («monetari a», «anteri or»).
- Las filas de persona cuyo discurso porta la fórmula de la decisión vigente conservan al hablante y quedan `ACUERDO_CONSEJO` (57 filas; p.ej. «…deja constancia que se acuerda por unanimidad mantener la tasa…»).

## 6. Compuerta de calidad F0

`qa_gate_f0.py` valida la base en tres frentes (ver `informe_revision_base_referencia_2026-09-07.md`):

| Control | Resultado |
|---|---|
| F0(a) Cardinalidad de actores | 50 personas + Consejo = 51 valores de `Actor_Final` |
| F0(b) Decisión por sesión | 132/132 sesiones con exactamente una decisión parseada; 0 filas de decisión mis-tipificadas |
| F0(c) Contraste contra TPM oficial | 132/132 OK contra `tpm_oficial_bcch.csv` (ventana de eficacia de 10 días); 0 discrepancias |

## 7. Textos largos

Se re-extrajo el contenido completo desde los PDFs originales para las celdas que alcanzan el límite de 32,767 caracteres del formato XLSX. La fuente de verdad se conserva en `textos_completos.jsonl`. La hoja `Textos_Completos` referencia esos registros.

## 8. Duplicados

Los 391 registros duplicados exactos corresponden a fórmulas de sesión repetidas entre actas. Conforme al criterio definido, **no se eliminan**; quedan marcados con `Duplicado_Exacto = SI` y `Duplicado_Formula = SI`.

## 9. Casos pendientes de revisión

Quedan **6 registros** en `PENDIENTE_REVISION` porque el párrafo inicial de la sesión no permite una coincidencia única y exacta entre nombre y cargo. Corresponden a invitados, ausentes que intervienen posteriormente o listas de asistencia incompletas en el OCR. Requieren verificación manual.
