# Revisión de comas — lote 1 (2026-09-08)

**Base de trabajo:** `ef9eba3397f384333227a54474681d4c996cc6eb`, diagnóstico posterior a
LOOP32. La entrega de datos sigue siendo LOOP32 (`1b02496`).

## Avance

**40 límites existentes revisados bilateralmente, en 36 padres leídos completos.**
En los límites seleccionados, los sujetos y predicados respaldan la separación ya
exportada. **No se encontraron nuevos cortes necesarios en esos límites.** No son
40 errores corregidos ni 40 voces nuevas recuperadas.

| Unidad de trabajo | Antes | Ahora |
|---|---:|---:|
| Comas del subgrupo, con distinto actor siguiente en el mismo padre | 167 | 167 |
| Límites con ficha bilateral de este registro | 0 | 40 |
| Límites del subgrupo sin ficha bilateral | 167 | **127** |
| Filas con alertas en la base | 465 | **465** |
| Filas físicas de la base | 9.691 | 9.691 |
| Alertas cerradas / nuevos cortes / nuevos enlaces | — | **0 / 0 / 0** |

**La reducción es de trabajo sin ficha, no de alertas mecánicas.** El estado
`LIMITE_REVISADO_SIN_CIERRE` significa que se leyó ese cambio de voz; no elimina la
coma, no valida OCR ni certifica todos los tramos del padre. La cola permite evitar
volver a empezar estos mismos límites sin saber que ya fueron leídos.

Las 127 sin ficha incluyen los doce focos de coma observados en el diagnóstico anterior.
Se excluyeron de este lote para ampliar la lectura; **no se promueven automáticamente**
a revisión bilateral por haber aparecido en una ventana. Tampoco se suman estas40
fichas a las102 fichas de menciones actuales: son registros distintos y superpuestos
con revisiones anteriores de otros tipos.

## Alcance y selección

Se eligieron los primeros40 candidatos por orden de la base que cumplían:

- único motivo en la fila izquierda: `FINAL_SIN_PUNTUACION`;
- coma antes de otro actor personal, dentro del mismo padre;
- foco no seleccionado en el diagnóstico anterior;
- padre de hasta2.400 caracteres en el origen.

Se leyeron completos los36 padres, **37.408 caracteres de origen**, además de ventanas
de hasta180 caracteres al final/inicio de los vecinos externos. La longitud limita
**la selección de lectura**, nunca la segmentación: no se acorta ninguna presentación.
La tanda se concentra entre2007 y2009; **no es muestra representativa ni independiente**.
No se estima precisión o cierre del corpus a partir de ella. Los padres largos y los
límites institucionales no cubiertos siguen pendientes en la cola.

Los cuatro padres con dos límites registrados son **2583, 2621, 2635 y2704**. El número
de padres es36, no40. Leer todo un padre no significa registrar todos sus límites.

## Hallazgos y controles

### Preguntas, respuestas y complementos

Predominan «a lo cual… responde/precisa/agrega», confirmaciones con sujeto nominal y
nuevos sujetos después de coma. La lectura conserva preguntas y contestaciones como
aportes diferentes, incluso cuando la respuesta es muy breve.

- **1713:** petición ministerial → respuesta presidencial; los aportes de Magendzo
  anteriores y posteriores quedan separados.
- **2583:** se conservan dos preguntas presidenciales con respuestas de Soto y Cowan,
  además de la complementación de García y la exposición posterior de Soto.
- **2621:** Presidente110 → García62 → Soto76. Las dos comas tienen sujetos distintos;
  no se adjudica el pasaje conjuntamente a los dos economistas.
- **2704:** consulta presidencial66 → De Ramón273; Marshall161 → confirmación de Soto48.
  No se absorbe la confirmación breve ni se borra el retorno por tener pocas palabras.
- **2743:** García «mencionaba la semana anterior» sigue siendo referencia dentro de
  Desormeaux. La respuesta actual es la del Ministro69. La ficha previa de mención
  permanece intacta.

### Presentaciones y continuidad

En **2198**, el agradecimiento/cesión presidencial empieza después del desarrollo de
Lehmann; no se devuelve al expositor por ser un cierre. En **2615**, Soto responde a
una pregunta referida de Claro, interviene el Ministro y Soto retoma su exposición:
la referencia inicial no constituye por sí sola un turno de Claro delimitable.

Se conservan las presentaciones dentro de **2535, 2619, 2673 y2785**. La lectura no
abre cortes por cambios de tema. Se comprueba la continuidad existente **2027→2028**,
**2673→2674** y **2785→2786**; los retornos tras otra persona no se fusionan. Todas las
demás continuidades de la entrega también quedan idénticas porque los datos no cambian.
`CONTEXTO_REVISADO` no recibe nuevas anclas y Fin solo no corta ni ancla.

### Reservas: un límite legible no sanea el texto o el cargo

- **2535:** Soto termina con **«/ ,»** antes de la intervención presidencial. El cambio
  de sujeto es legible, pero este residuo necesita cotejo. No se convierte el caso en
  «sólo una coma correcta» ni se borra la barra.
- **2667:** se identifica el comienzo de la respuesta de Lehmann a Velasco. Su tramo
  derecho conserva **«y el Gerente de»**, `TEXTO_DANADO_POR_COTEJAR` y su propio aviso
  de puntuación. **No se certifica la exclusividad de todo ese tramo**, ni se reconstruye
  el aporte faltante o se adjudica el residuo a Soto.
- **2576:** fuera del límite Marfán→Presidente, Cowan aparece con el cargo textual
  **«Gerente de División Política Monetaria»**. Queda anotado para cotejo, sin corregir
  el literal, certificar ese cargo o crear un alias global.
- **2723:** la confirmación de Lehmann43 conserva `DUPLICADO_NO_FORMULA`; reconocer su
  sujeto no cierra el aviso de repetición.
- **1809:** se conservan «De Gregario», «va a ener» y «yeso». Esta lectura no los corrige
  ni habilita nuevas variantes globales de nombre.

Estas reservas están documentadas en las fichas de lectura. **No se agregaron nuevas
advertencias a la base**, ni se retiraron las existentes. La fila izquierda puede tener
un único aviso mientras la derecha u otra parte del padre conserva otros problemas.

## Registro validado y cola para continuar

Cada ficha conserva ambos textos completos, actor, método, fecha y hash; se vincula a
la evidencia íntegra del padre y a una firma de toda su partición exportada. Cambiar
un texto, cargo, método, ancla, motivo o una parte no focal del padre invalida la ficha.
Se exigen adyacencia real, mismo padre, fechas compatibles y sujetos distintos. Las
fuentes originales se comprueban por hash. No basta el nombre o la proximidad.

La firma no depende del ID numérico global o del número global de grupo; sí de las
claves de intervención y de la evidencia de continuidad. Esto permite detectar cambios
materiales sin confundirlos con una renumeración puramente administrativa.

La herramienta es **independiente del pipeline** y sólo exporta seguimiento de lectura:

```bash
.venv/bin/python scripts/revisar_cola_comas.py \
  --revisiones docs/revision_comas_lote1_2026-09-08/revisiones.json \
  --salida .cache/cola_comas_actualizada
```

- [Registro de40 fichas y36 padres completos](revision_comas_lote1_2026-09-08/revisiones.json)
- [Cola completa de167 con estado de lectura](revision_comas_lote1_2026-09-08/cola_comas.csv)
- [127 límites sin ficha bilateral](revision_comas_lote1_2026-09-08/comas_sin_ficha.csv)
- [Resumen reproducible](revision_comas_lote1_2026-09-08/resumen.json)

## Validación y publicación

**1.795 pruebas pasan: 1.780 anteriores +15 nuevas**, con subpruebas de corrupción por
lado, fecha, actor, texto, cargo, método, anclas, inserciones y duplicados. Las pruebas
cubren las reservas de2667/2723, la conservación de «/ ,», continuidades y retornos.

**Los27 archivos versionados bajo `data/` son idénticos byte a byte** frente al commit
base, incluyendo la serie externa de TPM, fuentes, bases, colas, QA, manifiesto y todos
los registros de curación. Esta comparación amplía los26 hashes del diagnóstico previo
con la comprobación explícita de `data/external/tpm_oficial_bcch.csv`.

- **9.691 filas, 465 alertadas en395 padres**, mismos actores, textos, cargos, grupos e IDs.
- **102 fichas actuales de menciones (98 legítimas +4 pendientes)** sin cambios.
- **No pipeline regenerado**: el producto de datos y su QA siguen siendo LOOP32.
- Sin nuevo cotejo PDF, muestra independiente, cierre semántico exhaustivo o afirmación
  de CI remota. Workflow preexistente fuera del PR.

[Verificación global y hashes](revision_comas_lote1_2026-09-08/verificacion.json) ·
[Pruebas](../tests/test_revision_comas.py) ·
[Diagnóstico previo](DIAGNOSTICO_FINALES_2026-09-08.md) ·
[Entrega de datos LOOP32](REVISION_LOOP32_2026-09-08.md)

**Siguiente paso:** continuar con la cola de127 sin ficha, conservando en una tarea
separada los ocho candidatos a palabra desplazada detectados antes. No se usan esas
hipótesis para mover palabras, cerrar alertas o cambiar voces en este lote.
