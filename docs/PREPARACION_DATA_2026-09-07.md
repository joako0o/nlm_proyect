# Preparación de la data — correcciones y revisiones iterativas

> **Informe de la ronda anterior (9.058 filas).** La revisión posterior incorporó
> continuidad entre párrafos y corrigió cortes por menciones. Consultar
> [la revisión vigente](CONTINUIDAD_PARRAFOS_2026-09-07.md). Los IDs y cifras
> siguientes corresponden a aquella ronda, no al Excel actual.

**Fecha:** 2026-09-07  
**Estado:** controles automáticos bloqueantes aprobados; revisión semántica dirigida pendiente.  
**Fuente de métricas:** `data/processed/qa_preparacion.json`.

Este informe sustituye, para la salida actual, las conclusiones de cierre de
`AUDITORIA_BASE_REFERENCIA.md` y
`informe_revision_base_referencia_2026-09-07.md`. Se conservan esos documentos
como antecedentes de la base de 8.493 filas. No se modificaron las entradas raw
ni la serie externa de TPM.

## 1. Diagnóstico confirmado

La base inicial pasaba F0, pero ese control sólo recuperaba una decisión por
sesión y aceptaba coincidencia de tasa **o** delta. Además:

- El JSONL de textos completos se leía para las notas, no para segmentar.
  `ID_Padre=297` seguía cortado aunque aparecía `Texto_Truncado=NO`.
- Las reglas temáticas normalizaban las tildes del texto, pero no de los patrones.
- Algunas menciones a otras personas se confundían con sujetos de habla.
- Permanecían diálogos entre varios participantes dentro de una misma fila.
- Las marcas de duplicados describían al padre, no necesariamente al nuevo segmento.
- La documentación exageraba la cobertura semántica de los controles.

La expresión regular de la revisión externa reproducía 1.274 alertas, pero
no distinguía continuación, mención y cambio de persona. Ese número no era un
conteo válido de errores. Tampoco era correcto tratar los cuatro casos finales
como simples sustituciones de actor: tres requerían dividir el texto.

## 2. Rondas realizadas

### A. Texto completo y conservación

Se incorpora `Texto_Completo` **antes** de segmentar. JSONL corrupto, duplicado
o inconsistente en longitud provoca error; no se continúa silenciosamente.

Durante la revisión del recuperador PDF se detectaron expresiones regulares que
podían borrar cifras en los bordes de línea y partes numéricas dentro del texto.
Se reemplazaron por firmas específicas de encabezados/pies, se comprobaron
los pies `12.07.2005 2.-` y la fecha aislada de la página 8, y se añadieron
pruebas para no borrar precios, años, porcentajes ni puntos base.

El texto recuperado final de `ID_Padre=297` tiene **35.906 caracteres**, frente
a 32.767 en el original XLSX. No se afirma que la diferencia de longitudes sea
una simple continuación: la recuperación es una nueva extracción PDF. La
comparación de conservación usa esa fuente recuperada íntegra.

Una intervención resultante excede el límite físico de Excel. Se fracciona
por oraciones, mantiene el actor y comparte `ID_Bloque_Texto`; la segunda
fracción lleva `Fuente_Actor=CONTINUACION_XLSX`. No es un nuevo turno conversacional.

### B. Sujetos y cambios de hablante

Se añadió un detector separado (`turns.py`) que vincula sujeto y verbo, en lugar
de buscar cualquier verbo dentro de una ventana alrededor del nombre.

Se revisaron y corrigieron, en sucesivas ejecuciones:

- Nombres completos/abreviados y cargos con saltos OCR.
- Sujetos invertidos: «consulta el señor Ministro…».
- Referencias nominales: «en respuesta a la consulta del Consejero…».
- Menciones frente a intervenciones: «comparte la apreciación de…».
- Transferencias de palabra: el receptor sólo toma el turno cuando hay discurso.
- Anáforas locales: «el Gerente mencionado…», después de una intervención identificada.
- Cargo `Subgerente General` y nombres como María Elena Ovalle.
- Duplicación de una misma persona en asistencia con nombre largo/corto.
- Párrafos concatenados por OCR sin punto y marcadores de turno.

Las primeras ejecuciones detectaron regresiones: omisión del Subgerente y
fusiones con nombres abreviados. Se inspeccionaron los padres afectados y se
corrigieron antes de la publicación. También se compararon límites con la base
anterior; no se mantuvieron ciegamente todos, porque algunos provenían de
atribuciones erróneas o de dos segmentos consecutivos del mismo hablante.

La resolución por cargo privilegia titulares únicos de la sesión. Las
coincidencias difusas de asistencia se abstienen cuando dos candidatos tienen
puntajes cercanos. Se corrigió una búsqueda temporal que ignoraba el cargo al
seleccionar fechas cercanas. Los métodos legados que aún se necesitan quedan
explícitamente señalados, no presentados como atribuciones verificadas.

### C. Taxonomía y duplicados

Los patrones y las etiquetas originales se normalizan de la misma manera.
Se conserva el orden de prioridad de la taxonomía; no se inventa un nuevo
etiquetado humano por turno ni se reescribe el discurso para clasificarlo.

`Duplicado_Exacto` y `Duplicado_Formula` se recalculan sobre el texto procesado.
Las marcas históricas del padre pasan a `Duplicado_Exacto_Origen` y
`Duplicado_Formula_Origen`. No se elimina ninguna repetición.

### D. F0, F1 y pruebas

F0 ahora valida cobertura mensual, todas las fórmulas vigentes detectadas
(incluso varias en una oración), su tipificación y todos los componentes
parseados: tasa, delta y signo verbal. Se corrigió el caso de delta expresado
en porcentaje («en 0,25% hasta 3,5%») para no tomar 0,25 como tasa objetivo.

F1 añade integridad, conservación contra la fuente completa, orden, cargos,
duplicados y correspondencia exacta entre ambos Excel.

Hay **38 pruebas**: casos reales positivos, casos que no deben dividirse,
conservación del texto largo, números PDF, JSONL corrupto/duplicado, ambigüedad
de nombres/cargos, decisiones contradictorias, cobertura ausente y mutaciones
que simulan pérdida de texto, marcas erróneas y divergencia de la proyección final.

### E. Publicación y reproducibilidad

El orquestador construye en staging y ejecuta pruebas, F0 y F1 antes de publicar.
Se realizó una reconstrucción adicional con `PYTHONHASHSEED=777`: los XML de
hojas, estilos y estructura de ambos Excel coincidieron con la publicación.
Se excluyó únicamente `docProps/core.xml`, que incluye timestamps de creación.

Se publica un manifiesto SHA-256 de entradas, scripts, pruebas, dependencias y
salidas. Los archivos raw y la referencia TPM permanecen intactos.

## 3. Resultados

| Indicador | Antes | Ahora |
|---|---:|---:|
| Filas de origen | 7.219 | 7.219 |
| Filas procesadas | 8.493 | **9.058** |
| Bloques actuales de texto | — | **9.057** |
| Padres divididos | 843 | **1.123** |
| Sesiones | 132 | **132** |
| Etiquetas de actor | 51 | **51** |
| Palabras en XLSX | 2.048.062 | **2.048.560** |
| Tema `otros` | 2.687 | **225** |
| Tema `inflacion` | 21 | **678** |
| Cargos pendientes de confirmación por asistencia | 6 | **6** |
| Padres reconstruidos contra fuente vigente completa | No incluía recuperación del 297 | **7.219 / 7.219** |
| Máxima longitud de celda de texto | 32.647 | **31.948** |
| Fórmulas TPM contrastadas | Una decisión seleccionada por sesión | **310 fórmulas / 132 sesiones** |
| Errores bloqueantes F0/F1 | F0 tenía menor alcance | **0** |

La diferencia de palabras incorpora la recuperación y su limpieza, no sólo
nuevas divisiones. Dividir por sí mismo no añade contenido. La reducción de
`otros` no es una medición de precisión temática: refleja la reparación de
reglas que antes no se activaban por las tildes.

Hay **533 filas con texto duplicado exacto**, de las cuales **480** cumplen
la heurística de fórmula. Estas cifras no son directamente comparables con los
391/362 anteriores: cambió la unidad del indicador (padre → texto procesado).

## 4. Casos testigo corregidos

Los números siguientes son **IDs de la versión actual**, no filas Excel
(la fila Excel añade uno por el encabezado). La referencia estable para
comparaciones entre versiones es el padre junto con el texto y el manifiesto.

| Padre | Caso | IDs / atribución actual |
|---|---|---|
| 611 | Corbo responde y Marfán replica | 769 Corbo; 770 Marfán |
| 2722 | García expone y Lehmann acota | 3831 García; 3832 Lehmann |
| 5403 | Lehmann comparte la apreciación de Claro | 7057 Lehmann; Claro es una mención |
| 7188 | Fuentes expone y Marcel interviene | 9018 Fuentes; 9019 Marcel |
| 7201 | Naudon expone y Marcel interviene | 9035 Naudon; 9036 Marcel |
| 506 | Exposiciones, pases de palabra, pregunta y respuesta | 596–605: Corbo, Lehmann, Corbo, García, Corbo, Lehmann, Eyzaguirre, Lehmann, Desormeaux, Corbo |

El padre 217 conserva correctamente a Desormeaux en la intervención que
menciona a Marfán y separa la intervención posterior de María Elena Ovalle.

## 5. Pendientes explícitos

**977 filas tienen al menos una alerta.** Hay **8.081 sin alertas automáticas**,
lo que no equivale a 8.081 filas revisadas por una persona.

| Motivo | Filas |
|---|---:|
| Atribución mediante heurística legada | 453 |
| Posible otro hablante **o mención** | 356 |
| Final sin puntuación reconocida | 106 |
| Duplicado no identificado como fórmula | 53 |
| Atribución por anáfora local | 26 |
| Fragmento menor a ocho palabras | 8 |
| Cargo sin confirmación suficiente en asistencia | 6 |
| Variante de identidad Ricaurte por verificar | 6 |

**Las categorías se superponen.** La cola incluye tanto posibles errores como
falsos positivos: por ejemplo, citas a otras intervenciones pueden activar el
detector sensible. No se han revisado manualmente todas esas filas ni se
certifica que el detector encuentre todos los errores restantes.

Los seis cargos pendientes corresponden a los padres 41, 234, 243, 246, 406 y
980. Se conservan los cargos propuestos con su incertidumbre, sin cambiar la
fuente a «verificada» a falta de evidencia suficiente.

La variante Miguel Ricaurte Vintimilla / Miguel Ricaurte Bermúdez ya estaba
presente en los nombres/reglas del proyecto. No se fusionaron identidades sin
una comprobación documental. La cardinalidad actual es de **etiquetas**, no
una validación independiente del número de personas reales.

## 6. Entregables y próxima revisión

- **Base de trabajo:** `data/processed/consolidado_base_referencia_final.xlsx`.
  Conserva las primeras 13 columnas y agrega 7 de trazabilidad/revisión.
- **Auditoría:** `consolidado_base_referencia.xlsx`, con 33 columnas y hojas de control.
- **Cola accionable:** `revision_pendientes.csv`, con padre, actor, motivo e inicio del texto.
- **Control de TPM:** `decisiones_tpm.csv`, una fila por sesión e IDs de evidencia.
- **Métricas/procedencia:** `qa_preparacion.json` y `manifiesto_preparacion.json`.

Prioridad recomendada: revisar combinaciones de alertas de hablante y método
legado, después fragmentos/cortes OCR y los seis cargos; documentar cualquier
corrección manual contra padre + texto, y volver a ejecutar el pipeline.

Para análisis hawk/dove no conviene excluir todas las alertas sin estudiar el
sesgo que produciría esa selección. Tampoco conviene usar sólo `Tipo_Acta` como
filtro de contenido económico: hay pasos de palabra atribuidos a personas y
hay decisiones dentro de discursos personales. Las actas contienen discurso
referido, no necesariamente palabras textuales de cada participante.

**Límite documental:** sólo hay dos PDFs fuente en el repositorio y la serie de
TPM tiene procedencia Datosmacro (aunque conserve el nombre histórico
`tpm_oficial_bcch.csv`). F0 usa la ventana temporal explícita de 10 días; no
sustituye la verificación primaria de todas las actas y fechas efectivas.
