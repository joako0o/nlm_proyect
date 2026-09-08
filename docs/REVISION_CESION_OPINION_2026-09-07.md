# Cesión, agradecimiento y retorno del Presidente

**Fecha:** 2026-09-07. **Inicio:** 9.221 filas / 629 alertas / 285 pruebas.
**Publicación:** **9.226 filas / 627 alertas / 300 pruebas; F0/F1 aprobados.**

## Alcance y entregables

Se abordaron los dos límites pendientes de **3123** y el intercambio de **3187**.
La comparación detectó un tercer padre afectado por la fórmula de votación,
**3966**: se leyó su contenido y el entorno antes de aceptar el cambio.

Resultado: **tres padres modificados, ocho segmentos resultantes y cinco filas
adicionales**. En **3967** cambió sólo la relación de continuidad con Marshall,
sin modificar texto, actor, cargo ni método de atribución.

**Lectura dirigida del consolidado por el agente; sin cotejo PDF ni revisión
humana independiente.** No se revisó exhaustivamente la cola ni se certifica
la pureza semántica de todos los padres por haber corregido un intervalo.

- [Excel de seguimiento y cola vigente](../data/processed/revision_783.xlsx).
- Base final: `data/processed/consolidado_base_referencia_final.xlsx`.
- [Hashes, IDs y ocho segmentos completos](cambios_cesion_opinion_2026-09-07.csv).
- [Contenido antes/después, incluido 3967](comparacion_cesion_opinion_2026-09-07.json).
- [Evidencia de continuidad 3966 → 3967](continuidad_cesion_opinion_2026-09-07.csv).
- [Punto de reanudación y pendientes](estado_revision_cesion_opinion_2026-09-07.json).

Los números de padre son los del consolidado original; los IDs actuales de filas
pueden renumerarse. El checkpoint no representa un proceso activo en segundo plano.

## 1. Padre 3123 — 2010-05-13

Se conserva la exposición y el voto de Marshall, y se separan **ambos actos
posteriores**, no sólo la última cláusula:

| ID vigente | Actor | Alcance | Caracteres |
|---:|---|---|---:|
| 4557 | Marshall | Exposición y voto por mantener la TPM en 0,50% | 5.484 |
| 4558 | De Gregorio | Cesión de la palabra al Vicepresidente | 108 |
| 4559 | Marfán | Agradecimiento introducido por `quien` | 57 |

La cesión comienza en `Al continuar con la votación, el señor Presidente concede
la palabra…`. La revisión **HAB-20260907-3123** delimita literalmente:

> quien agradece, en primer término, el análisis del staff.

No se inventaron palabras pronunciadas por Marfán ni se atribuyó el
agradecimiento al Presidente o al staff. El texto describe un acto de Marfán.

### Salvaguardas

`CESION_AGRADECIMIENTO_RELATIVO_EXPLICITO` es una excepción individual con hash,
límites y citas. Exige la fórmula de agradecimiento constatada, la cesión
contigua en esa misma oración, coma previa, sujetos completos y no ambiguos
de cedente y destinatario, actor revisado compatible y ausencia de comillas.
No admite por defecto futuras acciones, invitaciones, destinatarios múltiples,
otros agradecimientos ni una cesión tomada de una oración anterior.

La variante existente de presentación en 2644 conserva su validación separada.
Las proyecciones para reconocer sujetos no alteran el texto exportado.

Se conserva la continuidad de Marshall **3122 → 3123**. En **3124**, Marfán
sigue identificado explícitamente como autor de la exposición siguiente. No se
fuerza un `ID_Turno` compartido desde el agradecimiento revisado: la política
vigente no convierte `CONTEXTO_REVISADO`, por sí solo, en un ancla explícita.
Esto no cambia el actor de la continuación ni une el discurso con el cedente.

## 2. Padre 3187 — 2010-06-15

Se recupera el intercambio completo:

| ID vigente | Actor | Inicio | Caracteres |
|---:|---|---|---:|
| 4634 | De Gregorio | `El señor Presidente indica…` | 183 |
| 4635 | Marfán | `Dado eso, el señor Vicepresidente manifiesta…` | 157 |
| 4636 | De Gregorio | `En opinión del señor Presidente…` | 476 |

El prefijo completo `Dado eso` permite reconocer al Vicepresidente cuando hay
un sujeto y predicado explícitos; no convierte referencias o menciones en turnos.
La revisión **HAB-20260907-3187** delimita el retorno del Presidente.
`Plantea…` y `Pregunta, entonces…` se conservan con este último.

No se añadió una regla global para atribuir cualquier frase `En opinión…` por
proximidad. Sin la revisión individual, el retorno seguiría sin delimitarse.

## 3. Padre 3966 — 2011-04-12

La misma fórmula explícita `Al continuar con la votación` permite separar el
voto de Claro del inicio de Marshall. Se verificó el contexto de este cambio
adicional; no se aceptó sólo porque lo propusiera el reconocimiento automático.

- **Claro: 4.029 caracteres**, conservando su exposición y voto por subir la TPM
  a 4,5%.
- **Marshall: 1.537 caracteres**, desde su inicio de intervención y agradecimiento,
  con sus comentarios sobre el entorno externo e interno y las continuaciones.

Se conserva literalmente `agradeciendo al staff eI apoyo`, sin reparar el OCR.
No se atribuye el voto de Claro a Marshall. El inicio de Marshall se reconoce
con `SUJETO_ROL_NOMBRE`, sin otra entrada de revisión contextual.

**3967** comienza explícitamente con Marshall y conserva su exposición y voto.
Ahora comparte turno con el final de 3966, pasando de `INICIO_EXPLICITO` a
`CONTINUIDAD_EXPLICITA`, sin modificación de su texto ni actor.

## 4. Validación global

- **300 pruebas aprobadas**, 15 nuevas: secuencias completas, conservación,
  hashes, agradecimiento efectivo frente a futuro/destinatario, ambigüedad,
  comillas, cesión no contigua, retorno de opinión, guardas de referencia,
  continuidad de Marshall y exactitud de intervalos.
- **56 revisiones de hablante**, dos más; las **54 anteriores son idénticas**.
- Ensayo aislado, comparación del alcance y ejecución completa de
  `scripts/preparar_data.py`: pruebas, construcción, exportación, **F0/F1**
  aprobados y publicación. La hoja principal coincide con el ensayo aislado.
- Comparación de **7.219 padres**: sólo 3123, 3187 y 3966 cambian texto segmentado
  o actor; 3967 cambia únicamente la relación de continuidad señalada, aparte de
  la renumeración de IDs. Los otros **7.215** conservan texto/actor, método,
  cargo/fuente, tipo de acta, motivos y relación de continuidad.
- Sin cambios de cargo en segmentos de texto y actor idénticos.
- Conservación ignorando sólo espacios: **2.048.560 palabras**, **9.225 bloques
  en 9.226 filas físicas**, máximo 31.948 caracteres por celda. El Excel de
  origen sigue idéntico al de `HEAD`.
- **8.835 grupos de turno; 300 multipárrafo; máximo 11 filas**. Se verificaron
  los grupos no afectados, los quince enlaces protegidos anteriores y el nuevo
  **3966 → 3967**. Permanecen las dos exposiciones de García de once filas,
  padres **60–70** y **142–152**.
- **46 hashes de entradas/código y 10 de salidas verificados** contra el manifiesto.
- 132 sesiones; 51 etiquetas de actor / 50 personas según F0; 310 contrastes TPM;
  559 duplicados exactos, 557 de fórmula. Las pruebas y controles compartidos no
  son una auditoría semántica independiente ni un cotejo de las actas originales.

## 5. Alertas y seguimiento histórico

**629 → 627 filas con alertas**. Los avisos de posible otro hablante/mención
pasan de **97 a 94**, y los finales sin puntuación de **236 a 237** por la coma
conservada al final de la cesión del Presidente en 3123. No se inventó un punto
ni se suprimió el aviso. Los demás motivos no cambian y se superponen.
**La variación no mide errores confirmados.**

En las **783 filas originales**: **457** pendientes de lectura contextual;
59 fórmulas; 71 métodos actualizados; **119** cambios por comparación;
**53** correcciones dirigidas; siete breves válidos; ocho menciones históricas;
seis identidades; dos repeticiones y una continuidad. Por tipo: **130 lecturas
dirigidas por agente, 190 comparaciones y 463 triajes**. **604 intervalos
originales** aún se solapan con alertas vigentes.

La corrección de 3966 está documentada aquí, pero se contabiliza como cambio
por comparación en ese seguimiento, no como otra entrada `CONTEXTO_REVISADO`.
Ninguna categoría equivale a certificación del padre completo.

Las seis menciones actuales documentadas siguen aparte y conservan sus avisos;
4574 conserva también la atribución legada. Quedan **80 candidatos de otro
hablante sin anotación de mención**, bajo el filtro anterior, no 80 errores
confirmados ni una lista exhaustiva de pendientes.

## 6. Continuación pendiente

3123 y 3187 dejan de estar pendientes por los límites concretos abordados.
Siguen pendientes, entre otros:

- **3191:** opiniones e intervención conjunta del Presidente y Soto; no asignar
  arbitrariamente esa coincidencia a una sola persona.
- **3421:** separar actos personales de suspensión/reanudación institucional.
- **780 y 2126:** comienzo ambiguo de Corbo e intervención conjunta, respectivamente.
- Confirmaciones pasivas de **2661/2704** y daño textual de **2667/3107**.
- La cola restante, las variantes de identidad, las repeticiones sustantivas y
  la revisión semántica independiente de una muestra con y sin alertas.

No se obtuvo un PDF nuevo en esta tanda. El checkpoint conserva las limitaciones
y los candidatos siguientes, sin excluir padres completos por una corrección parcial.
