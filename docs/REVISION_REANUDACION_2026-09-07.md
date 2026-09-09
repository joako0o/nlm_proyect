# Reanudaciones, expositor mencionado y retornos con variantes de cargo

> Informe histórico de la versión de 9.165 filas / 672 alertas.
> El estado vigente está en [Fórmulas y menciones actuales](REVISION_FORMULAS_Y_MENCIONES_ACTUALES_2026-09-07.md).

**Fecha:** 2026-09-07. **Versión anterior:** 9.155 filas / 661 alertas.
**Publicación:** **9.165 filas / 672 alertas; 158 pruebas y F0/F1 aprobados.**

## Alcance y archivos

Se leyeron los siete padres con cambios de actor/límites y, para comprobar la
continuación de junio, el padre 728. Lectura del consolidado, **sin cotejo PDF ni
revisión humana independiente**. La comparación automática del resto del corpus
no equivale a lectura individual ni certifica pureza semántica.

- [Seguimiento de las 783 alertas originales](../data/processed/revision_783.xlsx).
- [Siete padres: hashes, IDs anteriores y 44 segmentos actuales completos](cambios_reanudacion_2026-09-07.csv).
- [Ocho cambios adicionales de método/alertas sin modificar texto ni actor](cambios_metodos_alertas_reanudacion_2026-09-07.csv).
- Base final: `data/processed/consolidado_base_referencia_final.xlsx`.
- Registro de intervalos: `data/curation/revisiones_hablantes.json`.

## 1. Decisiones y contexto

| Padre | Fecha | Resultado | Filas antes → ahora |
|---|---|---|---:|
| 644 | 2006-04-13 | Corbo suspende; se reanuda institucionalmente; Corbo solicita a Valdés presentar; Valdés expone; Corbo ofrece comentarios. Se conserva la exposición de Schmidt-Hebbel y se separa una pregunta de Marfán que estaba concatenada tras «Ello», seguida de su respuesta. | 8 → 12 |
| 664 | 2006-05-11 | Corbo → Velasco → Corbo suspende → reanudación institucional → Corbo presenta a Valdés → Valdés expone → Corbo ofrece comentarios. La suspensión deja de pertenecer a Velasco y la exposición deja de pertenecer a Corbo. | 4 → 7 |
| 727 | 2006-06-15 | Tras la reanudación y la solicitud de Corbo, «El señor Gerente de División mencionado informó lo siguiente» pertenece a Valdés. El padre 728 continúa con Valdés y mantiene su texto completo. | 3 → 4 |
| 770 | 2006-07-13 | Se adelanta el inicio de Valdés a «El señor Gerente de División mencionado informó…», uniéndolo a su continuación ya reconocida. No se divide la exposición por sus enumeraciones. | 4 → 4 |
| 1904 | 2008-06-10 | De Ramón recomienda 50 puntos base; Kevin Cowan inicia explícitamente su evaluación de tres noticias. Su referencia posterior al Gerente de División Operaciones Financieras no devuelve la palabra a De Ramón. | 1 → 2 |
| 2460 | 2009-04-09 | De Gregorio agradece a Lehmann y solicita la parte nacional a Soto; Soto presenta el IMACEC; García precisa el alcance de la explicación. Lehmann es mencionado, no un nuevo hablante. | 2 → 3 |
| 2462 | 2009-04-09 | Se recuperan dos retornos de Soto, sobre consumo e inversión, antes absorbidos parcialmente por García. Cada uno permanece unido al desarrollo que sigue: automóviles en el primero, viviendas en el segundo. Se conservan las intervenciones de Velasco, García y Marfán. | 12 → 12 |

El incremento neto es de **diez filas**, no un conteo de diez errores. Un mismo
padre puede contener más de un límite corregido.

### Exposiciones, interrupciones y texto dañado

- En mayo, Valdés conserva **8.397 caracteres** en un segmento; Corbo sólo
  recupera la palabra al final, cuando ofrece comentarios.
- En julio, Valdés conserva **7.648 caracteres** en un segmento, incluido el
  comienzo antes atribuido a Corbo. El «comentarios.» aislado final se mantiene:
  no se inventa un cierre ni un hablante para esa palabra.
- En junio, el comienzo de Valdés en 727 y su exposición en 728 conservan la misma
  persona. Esto no convierte automáticamente una anáfora en un ancla de continuidad
  ni fuerza la unión de sus `ID_Turno`; la atribución anafórica queda advertida.
- Se conservan «no solamente la» de Velasco, «Ello» de Schmidt-Hebbel y el
  marcador **■J** anterior a Cowan, sin completar ni eliminar texto.

## 2. Cambios de reconocimiento y decisiones ancladas

### Reconocimiento general, con controles de sujeto vigentes

En `scripts/turns.py` se añadieron:

1. **«informó»**, para reconocer la exposición del gerente nombrado en la oración
   anterior. La resolución contextual de «mencionado» ya existía; no se atribuye
   una presentación a cualquiera que haya sido mencionado.
2. **«le parece»**, como predicado del propio sujeto. Es necesario para conservar
   la intervención incompleta de Velasco al separarla de la suspensión posterior;
   no se toma prestado el verbo «suspende» de Corbo para reconocer a Velasco.
3. La variante exacta **«Gerente Análisis Macroeconómico»**, normalizada a
   «gerente de análisis macroeconómico» **sólo en la vista de reconocimiento**.
   El texto de salida sigue con su forma original. No se generaliza la omisión
   de «de» a cualquier cargo ni se modifica la asistencia.

Se mantienen las exclusiones de referencias, citas y sujetos sin predicado de
habla. Las solicitudes y agradecimientos no asignan por sí solos el texto al
receptor. Los tests incluyen discurso referido con «informó» y menciones del
cargo abreviado que no deben producir un turno.

### Cuatro intervalos nuevos en el registro

Los IDs `HAB-20260907-644`, `-664`, `-1904` y `-2462` incorporan hash del padre,
fecha, intervalo, citas, justificación y límites de la revisión. El registro
contiene ahora **25 intervalos de hablante** y mantiene las seis revisiones de cargo.

- **644:** sólo la pregunta de Marfán concatenada tras «Ello».
- **664:** sólo la suspensión explícita de Corbo.
- **1904:** el tramo de Cowan hasta el final.
- **2462:** el primer retorno de Soto, completo hasta la respuesta de García.

Los otros tramos corregidos por reconocimiento se documentan en este informe,
los tests y el CSV con hashes; **no se afirma que todos estén cubiertos por esos
cuatro intervalos**. En particular, el segundo retorno de Soto se comprueba por
regresión, no por un segundo intervalo en el registro.

En 1904 el título fuente dice **«Política l\/lonetaria»**, mientras la lista de
asistencia identifica a Cowan como **Gerente de División Política Financiera**.
Se adjudica el texto por el nombre explícito leído; no se reescribe ese título
ni se inventa un cargo de Política Monetaria. El método es `CONTEXTO_REVISADO`,
no una pretensión de reconocimiento automático correcto del título dañado.

## 3. Comparación global y garantías verificadas

- Cambios de texto/actor sólo en los **siete padres** de la tabla.
- En **615 y 817**, el actor y el texto permanecen; cambia el método a
  `ANAFORA_LOCAL`. En 817 también cambia la relación a continuidad no confirmada.
  No se presentan estos cambios de método como nuevas correcciones de persona.
- En **320, 1336, 1420, 2228, 4574 y 4656**, se agregan avisos de posible mención
  u otro hablante, sin cambiar texto ni actor. Son resultados del detector de
  alertas, no seis adjudicaciones dirigidas nuevas.
- Cero cambios de cargo para texto y actor idénticos.
- Conservación global entre versiones y **7.219/7.219 padres reconstruidos**,
  ignorando sólo espacios; **2.048.560 palabras**, sin cambios.
- Conservación de las exposiciones de García de 11 filas en los padres 60–70 y
  142–152, y de los negativos de menciones 3454, 3715 y 4266.
- Entrada original XLSX sin modificaciones frente a Git; publicación igual por
  contenido al resultado preliminar comparado.
- **158 pruebas aprobadas**, incluidas doce nuevas de reanudación, retornos,
  cargo abreviado, referencia contextual, negativos y conservación.
- Pipeline completo con F0/F1 antes de publicar. **35 hashes de entradas/código
  y diez de salidas** verificados contra el manifiesto.

La salida tiene **9.165 filas / 9.164 bloques**, 37 columnas de auditoría y 24
finales, 132 sesiones, **8.789 grupos de turno / 285 multipárrafo**, máximo de
11 filas por turno y 31.948 caracteres por celda. Se mantienen 310 fórmulas TPM
contrastadas. F0/F1 no son una auditoría semántica independiente del reconocedor.

## 4. Alertas: aumento visible, no ocultado

| Motivo | Antes | Ahora |
|---|---:|---:|
| Atribución anafórica | 37 | 43 |
| Atribución heurística legada | 265 | 264 |
| Final sin puntuación | 210 | 213 |
| Posible otro hablante o mención | 153 | 154 |
| Fragmento breve | 8 | 8 |
| Duplicado no reconocido como fórmula | 2 | 5 |
| Variante de identidad | 6 | 6 |
| **Filas con alguna alerta** | **661** | **672** |

Se eliminan cinco avisos de posible mezcla en los pasajes corregidos, pero se
agregan seis en textos sin cambios: por eso ese motivo aumenta en uno. No se
recorta el discurso referido para hacer desaparecer sus avisos.

Las tres nuevas repeticiones no reconocidas como fórmula son solicitudes de
Corbo a Valdés para presentar las opciones, ahora separadas en **644, 664 y 770**.
Su carácter procedimental está identificado en esta lectura, pero **no se amplió
el registro de fórmulas en esta ronda**: la advertencia automática sigue visible.
Los dos duplicados sustantivos de Herrera siguen sin eliminarse. Los duplicados
exactos son 557 y los reconocidos como fórmula, 552.

Las anáforas explícitas quedan advertidas aunque haya evidencia contextual;
los cortes también exponen los finales dañados. Los motivos se superponen:
**672 alertas no equivalen a 672 errores confirmados**.

## 5. Seguimiento histórico y pendientes

De los 783 intervalos originales:

| Estado | Total |
|---|---:|
| Pendiente de lectura contextual | 515 |
| Fórmula procedimental reclasificada | 59 |
| Método actualizado | 66 |
| Segmentación o actor modificado por comparación | 97 |
| Corrección dirigida aplicada | 22 |
| Breve válido revisado | 7 |
| Mención legítima revisada | 8 |
| Identidad pendiente | 6 |
| Repetición sustantiva pendiente | 2 |
| Continuidad entre padres revisada | 1 |

Los 22 intervalos con corrección dirigida incluyen **cuatro nuevos** sobre los
18 anteriores; no son 22 nuevas correcciones. El seguimiento clasifica los
intervalos originales según su evidencia: el segundo retorno de Soto no pasa a
corrección dirigida por estar fuera del primer intervalo documentado.
Hay 99 intervalos vinculados a lectura, 163 a comparación y 521 a triaje;
645 originales se superponen con alguna alerta actual. La instantánea de 783
permanece intacta. Estas cifras no son cierres semánticos exhaustivos.

Quedan las advertencias anafóricas, nuevas menciones detectadas, tres solicitudes
procedimentales por incorporar a la clasificación de fórmulas, las variantes de
identidad y las repeticiones sustantivas. El caso conjunto 2126 sigue sin asignarse
arbitrariamente a una sola persona. Se mantiene la necesidad de cotejar con las
actas originales los textos dañados y los casos que lo requieran.

Los IDs numéricos pueden desplazarse entre versiones: enlazar mediante padre,
texto y hashes, no sólo por número de fila.
