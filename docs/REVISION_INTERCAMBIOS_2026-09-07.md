# Intercambios acotados: complemento, exposición y pregunta

> **Informe histórico.** La publicación posterior a esta tanda está en [prioridades y primer lote](REVISION_PRIORIDADES_2026-09-07.md): 9.215 filas / 633 alertas / 257 pruebas. En 2644 ya se delimitó la presentación y en 2661 el intercambio final, con residuo pasivo pendiente. Los IDs, métricas y checkpoint de este documento corresponden a la tanda anterior; los enlaces a `data/processed/` abren la versión vigente.

**Fecha:** 2026-09-07. **Inicio:** 9.207 filas / 635 alertas / 222 pruebas.
**Publicación:** **9.211 filas / 635 alertas / 237 pruebas; F0/F1 aprobados.**

## Alcance y archivos

Continuación de la [revisión de residuos](REVISION_RESIDUOS_2026-09-07.md).
Se modificaron **tres padres**, con **12 segmentos resultantes y cuatro filas
adicionales**. En un cuarto padre, 2567, cambió sólo la relación de continuidad
con el turno anterior, sin modificar texto, actor, cargo ni método de atribución.

Se leyeron los intercambios de 2566, 2667 y 2704 y el entorno pertinente. También
se inspeccionaron 2644 y 2661, que permanecen pendientes y sin modificaciones.
**Lectura dirigida por agente del consolidado, sin cotejo PDF ni revisión humana
independiente. No se certifican completos los padres ni se revisó exhaustivamente
la cola de alertas.**

- [Excel de seguimiento y cola vigente](../data/processed/revision_783.xlsx).
- Base final: `data/processed/consolidado_base_referencia_final.xlsx`.
- [Cambios: tres padres y 12 segmentos completos](cambios_intercambios_2026-09-07.csv).
- [Continuidad de Lehmann en 2567](continuidad_intercambios_2026-09-07.csv).
- [Contenido anterior y posterior acotado, con hashes](comparacion_intercambios_2026-09-07.json).
- [Punto de reanudación y pendientes](estado_revision_intercambios_2026-09-07.json).

Los IDs actuales corresponden a esta publicación y pueden renumerarse en otra.
El checkpoint no es un proceso activo en segundo plano.

## 1. Padre 2566 — 2009-06-16

**Tres → cinco segmentos.** Marfán interviene, García explica los factores de las
tasas largas y Lehmann aclara cómo se miden las expectativas de inflación.
Dentro de esta última explicación aparece:

> planteamiento al cual el Vicepresidente señor Jorge Desormeaux complementa, señalando que cuando el mercado financiero se empieza a tranquilizar, los inversionistas tienden a abandonar los activos seguros en busca de activos más riesgosos y que esos activos corresponden esencialmente a inversiones con tasas nominales.

Se separa el complemento explícito de Desormeaux. La frase siguiente,
`Continuando con su exposición, el señor Lehmann indica…`, devuelve el turno a
Lehmann; no se le adjudica al Vicepresidente la exposición sobre paridades.

| ID actual | Actor | Caracteres |
|---:|---|---:|
| 3604 | Marfán | 396 |
| 3605 | García | 1.405 |
| 3606 | Lehmann | 639 |
| 3607 | Desormeaux | 319 |
| 3608 | Lehmann | 579 |

Revisión **HAB-20260907-2566**, con hash y citas. Los dos primeros segmentos
permanecen idénticos. La referencia `responde al Consejero señor Manuel Marfán`
no se transforma en un turno de Marfán.

El prefijo `planteamiento al cual` se admite en el reconocimiento de un sujeto
con verbo de habla. Se mantienen los filtros de menciones, comillas y otros
verbos finitos en el prefijo. **No se añade una regla general para cortar todas
las cláusulas de ese tipo**: el límite interno requiere la revisión individual,
con separador previo y sujeto compatible. La comparación aislada de toda la base
no produjo cambios estructurales fuera de los tres padres de esta tanda.

### Continuidad entre 2566 y 2567

El primer segmento de 2567, ahora ID 3609, comienza:

> El Gerente de Análisis Internacional prosigue con su presentación mencionando que persiste la recuperación de las bolsas

El retorno explícito de Lehmann al final de 2566 permite vincularlo con esa
continuación: **ambos comparten `RPM-2009-06-16:T32`**. La relación de 3609 pasa
de `INICIO_EXPLICITO` a `CONTINUIDAD_EXPLICITA`. Las intervenciones posteriores
de 2567 siguen separadas; no se fusionó todo el padre ni se ignoraron sus preguntas.

## 2. Padre 2667 — 2009-08-13

**Tres → tres segmentos**, adelantando el inicio de Soto:

| ID actual | Actor | Caracteres |
|---:|---|---:|
| 3810 | Velasco | 109 |
| 3811 | Lehmann | 150 |
| 3812 | Soto | 1.134 |

Después de la respuesta de Lehmann aparece el enlace dañado
`y el Gerente de Al continuar con la exposición sobre consumo…`.
La revisión **HAB-20260907-2667**, de tipo
`CONCATENACION_EXPLICITA_REVISADA`, comienza en:

> Al continuar con la exposición sobre consumo, el Gerente de Análisis Macroeconómico indica

El cargo de la sesión corresponde a Soto; el mismo tramo contiene
`el señor Gerente menciona…` y luego `el señor Soto manifiesta…`.
**Se mantiene toda esa presentación como una continuidad**, incluyendo
inventarios y catastro de inversión, sin partirla por cada nueva oración.

`y el Gerente de` queda literal al final del tramo anterior. No se reconstruyó
la frase perdida ni se adjudicó por conjetura a quién iba a nombrar. El nuevo
final truncado conserva un aviso de puntuación. La atribución del enlace dañado
no queda certificada por haber delimitado la presentación que sigue.

## 3. Padre 2704 — 2009-09-08

**Dos → cuatro segmentos.** La revisión **HAB-20260907-2704** separa:

> Es decir, no es problema de demanda, consulta el señor Presidente,

El sujeto pospuesto identifica al Presidente. La respuesta comienza
`a lo cual el señor de Ramón manifiesta…`, y De Ramón continúa con las restricciones
de oferta de los bancos. La pregunta no se deja dentro de su explicación ni se
traslada al Presidente la respuesta del expositor.

| ID actual | Actor | Caracteres |
|---:|---|---:|
| 3892 | De Ramón | 658 |
| 3893 | De Gregorio | 66 |
| 3894 | De Ramón | 273 |
| 3895 | Marshall | 210 |

Se conserva la coma final de la pregunta, con su aviso de puntuación. El último
segmento permanece idéntico y contiene `lo cual es confirmado por el señor
Claudio Soto`. **Esta confirmación pasiva no se adjudicó como un turno nuevo ni
se declaró resuelta**. Se registra como residuo aunque no dispare una alerta
automática; corregir la pregunta no certifica todo el padre.

## 4. Pruebas y comparación global

- **237 pruebas aprobadas**, 15 nuevas: secuencias de interlocutores, conservación,
  hashes de las tres fuentes, límites revisados, actor incompatible, comillas,
  separador, menciones negativas y conservación exacta de los intervalos.
- Se actualizó el inventario esperado de concatenaciones a **12** y el total de
  revisiones de hablante a **46**. Las **43 revisiones anteriores se conservan
  idénticas**; se añadieron tres, sin volver a registrar decisiones anteriores.
- Ensayo aislado, comparación y ejecución completa de `scripts/preparar_data.py`:
  pruebas, construcción, exportación, **F0/F1 aprobados** y publicación.
  El contenido de la hoja principal publicada coincide con el ensayo aislado.
- Comparación de **7.219 padres**: sólo 2566, 2667 y 2704 cambian texto segmentado
  o actor; 2567 cambia únicamente la relación de continuidad señalada, aparte de
  la renumeración de identificadores. No cambian cargos en segmentos de texto y
  actor idénticos. Los demás padres conservan métodos, roles, tipo de acta y avisos.
- Conservación global ignorando sólo espacios: **2.048.560 palabras**,
  **9.210 bloques / 9.211 filas físicas**, máximo 31.948 caracteres por celda.
  El Excel original sigue idéntico al de `HEAD`.
- **8.822 grupos de turno; 298 multipárrafo; máximo 11 filas**. Se verificó la
  partición de turnos no afectados descontando renumeraciones, los doce enlaces
  previamente protegidos —incluido Soto 2408 → 2409— y el nuevo 2566 → 2567.
  Las dos exposiciones de García de once filas, padres **60–70** y **142–152**,
  se conservan. Los padres 2981 y 780 siguen como en la publicación anterior.
- **42 hashes de entradas/código y 10 de salidas verificados** contra el manifiesto.
- 132 sesiones; 51 etiquetas de actor / 50 personas según F0; 310 contrastes TPM;
  559 duplicados exactos, 557 de fórmula. F0/F1 y la comparación automática no
  son lecturas semánticas independientes ni cotejos de las actas originales.

## 5. Alertas y seguimiento histórico

El total permanece en **635 filas con alertas**, pero cambia su composición:

| Motivo | Antes | Ahora |
|---|---:|---:|
| Posible otro hablante o mención | 111 | 108 |
| Final sin puntuación | 228 | 231 |
| Atribución legada | 259 | 259 |
| Anáfora | 42 | 42 |
| Fragmento breve | 8 | 8 |
| Variante de identidad | 6 | 6 |
| Duplicado no formulaico | 2 | 2 |

Los tres avisos nuevos de puntuación son el tramo de Lehmann antes del complemento
en 2566, el enlace truncado de 2667 y la pregunta del Presidente en 2704.
**No se reparó la fuente ni se suprimieron avisos para mejorar el contador.**
Los motivos se superponen; el cambio de alertas no mide errores confirmados.

El seguimiento de las **783 filas originales** arroja: **469** pendientes de
lectura contextual; 59 fórmulas; 71 métodos actualizados; **117** cambios por
comparación; **43** correcciones dirigidas; siete breves válidos; ocho menciones
históricas; seis identidades; dos repeticiones y una continuidad. Por tipo:
**120 lecturas dirigidas por agente, 188 comparaciones y 475 triajes**.
611 intervalos originales siguen solapándose con alertas actuales.
Una corrección dirigida aplicada no equivale a cierre semántico de todo el padre.

Las seis menciones actuales documentadas se cuentan aparte y conservan
`POSIBLE_OTRO_HABLANTE_O_MENCION`; 4574 conserva también el aviso de atribución
legada. Quedan **94 candidatos de otro hablante sin anotación de mención** bajo
el filtro anterior, no 94 errores certificados ni una lista exhaustiva de residuos.

## 6. Pendientes explícitos

- **780:** comienzo de Corbo anterior al límite reconocido; el acuerdo ya está
  delimitado. Se conserva la limitación documental de la tanda anterior.
- **2126:** intervención conjunta; no asignar un único actor arbitrariamente.
- **2661:** se releyó sin modificar. Sigue dentro del tramo del Presidente
  `El efecto debiera ser menor y al revés, acota el Ministro, y el señor Lehmann
  complementa…`; requiere delimitar ambas voces y revisar también la confirmación
  pasiva anterior de Lehmann. No basta separar sólo la última coordinación.
- **2644:** se releyó sin modificar. La cesión inicial a Céspedes contiene
  `quien comienza su exposición señalando…`; gran parte de su exposición sigue
  dentro del primer segmento del Presidente. Hace falta delimitar esa cláusula
  relativa manteniendo las continuaciones, hasta la cesión final a De Ramón.
- **2704:** confirmación pasiva de Soto en el último segmento, no adjudicada.
- **2667:** enlace truncado conservado, no reconstruido ni certificado.

Estos pendientes están en el checkpoint, incluso cuando el detector automático
no los señala. No se excluye un padre completo por tener una corrección previa.
