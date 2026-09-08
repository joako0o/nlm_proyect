# Revisión de continuidad de párrafos y exposiciones

> Antecedente de la ronda de 9.033 filas. La salida vigente y los nuevos cambios
> están en [Revisión dirigida](REVISION_DIRIGIDA_2026-09-07.md).

**Fecha:** 2026-09-07.  
**Punto de partida:** base de 9.058 filas de la ronda anterior.  
**Salida de esta ronda:** 9.033 filas físicas; 132 sesiones; controles F0/F1 aprobados.

## Criterio central

**Un cambio de fila o párrafo no implica cambio de hablante.** Las presentaciones
pueden continuar durante muchos párrafos sin repetir el nombre del expositor.
Asimismo, «ante una consulta del Consejero…» puede introducir la respuesta del
expositor, no una nueva intervención del consejero.

La revisión conserva cada registro de origen y su trazabilidad. No junta todos
los textos de una persona ni elimina párrafos; documenta la continuidad y sólo
cambia la segmentación cuando hay evidencia de un turno real o de un corte
anterior provocado por una mención.

## 1. Qué se revisó y corrigió

### A. Continuidad entre padres/filas

Antes, el contexto del segmentador se reconstruía desde cero para cada padre.
Ahora se mantiene contexto por sesión y se exige:

1. Una atribución explícita previa que sirva de ancla.
2. Compatibilidad entre el actor original y el hablante vigente.
3. Ausencia de un nuevo sujeto de habla o de un sujeto no resuelto al comienzo.
4. Ausencia de cesión de palabra, interrupción institucional o cambio de sesión.

Un párrafo sin nombre compatible con esa evidencia lleva
`Fuente_Actor=CONTINUIDAD_PARRAFO`. Una repetición como «señala el señor Gerente»
que conserva el expositor anclado lleva `ANAFORA_CONTINUIDAD`.

No se reemplaza un actor original distinto por el hablante anterior sólo porque
esté cerca. Tampoco se asume que, después de una pregunta, vuelve automáticamente
el expositor: la reanudación necesita evidencia.

### B. Menciones que habían producido cortes falsos

El detector podía rechazar correctamente al sujeto completo de una mención
(«del Consejero señor X»), pero aceptar luego el nombre contenido dentro del
mismo sujeto como candidato independiente. Se evita ese doble reconocimiento.

Se distinguen referencias como «tal como lo señaló el Vicepresidente», «al igual
que el Consejero» y «ante la consulta del Presidente» de nuevos sujetos de habla.
Se inspeccionaron los tramos de texto que cambiaron de actor, junto a los
párrafos que los anteceden, y se incorporaron casos representativos a las pruebas.

Ejemplos corregidos:

| Padre de origen | Lectura contextual |
|---|---|
| 3454, 2010-10-14 | Claudio Soto sigue exponiendo y responde a una consulta de Marfán; la mención a Marfán no cambia el actor. |
| 3715, 2011-01-13 | José De Gregorio sigue argumentando y cita al Vicepresidente; no se atribuye esa continuación al Vicepresidente. |
| 4266, 2011-08-18 | Soto continúa respondiendo; «ante una consulta de Sebastián Claro» no convierte a Claro en expositor. |
| 4350, 2011-10-13 | Lehmann responde a una consulta de Vergara, pero después **sí** toma la palabra Claro («es de opinión…»); se conserva ese cambio real. |
| 2058, 2008-09-04 | Marfán pregunta y «el Gerente mencionado» responde: la mención previa a Claudio Soto permite resolver la anáfora sin convertir aquella mención en discurso. |

Se amplió específicamente la detección de «es de opinión» y del cargo genérico
«Gerente de División». Los casos «mencionado» pueden usar un cargo y nombre
únicos en la oración inmediatamente previa, **sólo cuando la oración actual
los presenta como sujeto de un verbo**. Una mención por sí sola no abre un turno.
Las anáforas locales sin cadena explícita de continuidad siguen marcadas para revisión.

## 2. Ejemplos de exposiciones largas conservadas

### Pablo García — 10 de febrero de 2005

Los padres **60–70**, once filas, corresponden a una misma exposición:

- El padre 60 identifica al Gerente de Análisis Macroeconómico Pablo García.
- El 61 continúa con «Señala el señor Gerente…».
- Los padres siguientes desarrollan actividad, precios, mercados y proyecciones
  sin volver a identificar al hablante.
- El padre 71 es la intervención del Presidente que ofrece la palabra para comentarios.

Las once filas comparten **`RPM-2005-02-10:T3`**. Se conserva cada `ID_Padre`;
no se crea una celda gigantesca ni se pierde la frontera del registro original.

### Pablo García — 10 de marzo de 2005

Los padres **142–152** forman otra exposición de once filas, alternando
referencias al Gerente y párrafos sin nombre. Comparten **`RPM-2005-03-10:T3`**.
La intervención posterior del Presidente interrumpe el turno.

Estos dos ejemplos, junto con una secuencia sintética de 16 párrafos,
están incluidos en las pruebas de regresión. El algoritmo no impone un máximo
arbitrario de párrafos a una presentación.

## 3. Nuevas columnas y archivos

El Excel final pasa de 20 a **24 columnas**, conservando el orden de las
primeras 20. La base de auditoría tiene **37 columnas**.

| Columna | Función |
|---|---|
| `ID_Turno` | Agrupa filas contiguas compatibles con un mismo turno. |
| `Relacion_Turno` | Explicita si la fila inicia, continúa, es institucional o no tiene continuidad confirmada. |
| `ID_Antecedente_Continuidad` | Identifica la fila inmediatamente anterior que sustenta la continuidad. |
| `ID_Ancla_Actor` | Identifica la fila con sujeto explícito que respalda al actor. |

Son identificadores de la versión generada; pueden cambiar al modificar reglas.
La comparación entre versiones debe usar padre, texto y manifiesto.

- **`turnos_habla.csv`** resume los grupos: actor, sesión, IDs inicial/final,
  número de filas, padres, palabras y cantidad de filas con alertas.
- **`revision_pendientes.csv`** ahora incluye el párrafo anterior y el siguiente
  de la misma sesión, sus actores/IDs y la oración que activa la alerta cuando
  corresponde. Así se puede revisar contexto, en vez de juzgar sólo el inicio
  de una celda aislada.

Los grupos son conservadores y también incluyen filas institucionales aisladas.
**No equivalen a un conteo certificado de intervenciones humanas.** Los grupos
con alertas siguen necesitando revisión antes de agregarse para análisis individual.

## 4. Resultados de la ronda

| Indicador | Ronda anterior | Actual |
|---|---:|---:|
| Filas físicas | 9.058 | **9.033** |
| Palabras | 2.048.560 | **2.048.560** |
| Sesiones | 132 | **132** |
| Padres reconstruidos contra fuente completa | 7.219/7.219 | **7.219/7.219** |
| Filas con alertas | 977 | **863** |
| Posible otro hablante o mención | 356 | **252** |
| Heurística legada | 453 | **411** |
| Cargos pendientes por asistencia | 6 | **6** |
| Pruebas automatizadas | 38 | **60** |
| Fórmulas de TPM contrastadas | 310 | **310** |
| Errores bloqueantes F0/F1 | 0 | **0** |

La reducción neta de 25 filas corresponde a cambios de segmentación; **no es
eliminación de texto**. Hay 55 padres con cambios de segmentación o actor
respecto de la ronda anterior. Algunos cortes falsos se quitaron y otros cambios
reales de hablante que no se detectaban se incorporaron.

Se identifican **274 grupos con varias filas**, con un máximo observado de 11.
Hay 31 filas atribuidas por continuidad de párrafo y 2 por anáfora de continuidad;
otras 328 filas con sujeto explícito continúan un grupo ya abierto. Una fila
adicional es la continuación física XLSX del texto largo recuperado.

Los conteos de alertas no miden precisión: sus categorías se superponen y aún
incluyen falsos positivos. Su disminución **no debe interpretarse como 114 errores
humanamente confirmados y corregidos**.

## 5. Validaciones nuevas

Además de conservación, proyección y TPM, F1 comprueba que:

- Todo enlace de continuidad apunta a la fila inmediatamente anterior.
- Actor, sesión y grupo coinciden en ambos extremos del enlace.
- El ancla existe, no está en el futuro, tiene sujeto explícito y pertenece al mismo grupo.
- No se atraviesan cesiones de palabra, marcas institucionales ni alertas internas de otro hablante.
- No se reabre un identificador de turno después de filas de otro grupo.

Las pruebas incluyen presentaciones largas reales y sintéticas, continuidad
explícita/implícita, anáforas, cambio de sesión, interrupción y retorno,
pases de palabra, identidad original discrepante, sujetos desconocidos,
referencias que no son discurso y mutaciones de enlaces/anclas que deben fallar.

## 6. Límites y siguiente trabajo

No se ha certificado manualmente toda la base. Permanecen **863 filas con
alertas**, incluidos los seis cargos y las variantes de identidad Ricaurte que
requieren comprobación documental. Continúan las limitaciones de extracción
OCR, disponibilidad de sólo dos PDFs y referencia externa de TPM descritas en
el README.

Para usar las exposiciones como unidad analítica: seleccionar un `ID_Turno`,
ordenar sus filas por `ID` y leer el conjunto. No agrupar indiscriminadamente
todas las apariciones de un actor en la sesión: entre ellas pueden haber hablado
otras personas. Para resolver las alertas restantes, usar los extractos de
contexto y acudir al texto completo de los padres cuando no basten.
