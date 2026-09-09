# Loop13 — Anáforas, exposición continua y límites entre discurso y acta

**2026-09-08 · [PR #3](https://github.com/joako0o/nlm_proyect/pull/3).**
Base anterior: `1ed3d5de44b37d4077a8d8a726447c5d754d2b29`,
[loop12](REVISION_LOOP12_2026-09-08.md). Lectura dirigida del consolidado;
**sin nuevo cotejo PDF ni revisión humana independiente**.

## Resultado

| Medida | Antes | Publicado |
|---|---:|---:|
| Filas físicas XLSX | 9.494 | **9.497** |
| Bloques de texto | 9.493 | 9.496 |
| Grupos de turno | 9.085 | 9.087 |
| Grupos de varias filas | 313 | 314 |
| Filas con alertas | 359 | **343** |
| Padres con alertas | 323 | **309** |
| Pruebas | 975 | **1.035** |
| Intervalos revisados de hablante | 177 | **192** |
| Padres con revisión de hablante | 174 | 188 |
| Advertencias contextuales | 10 | 13 |
| Continuaciones de acta revisadas | 0 | 1 |

**30 padres afectados:** 12 estructurales (31 → 34 segmentos), 17 con mejoras de
metadatos de atribución y uno —3068— sólo con actualización de trazabilidad.
No son 30 nuevos diálogos separados ni 30 padres íntegramente certificados.
Los otros **7.189 padres** conservan sus campos semánticos, descontando los
identificadores secuenciales. Se conservan los **7.219 textos** originales.

- [Comparación global antes/después](comparacion_loop13_2026-09-08.json)
- [Detalle de filas y hashes](cambios_loop13_2026-09-08.csv)
- [Checkpoint y pendientes](estado_revision_loop13_2026-09-08.json)

## 1. Exposiciones que continúan en varios párrafos

Se documentan seis intervalos de Valdés: **38–39, 120–121 y 264–265**.
Se leyeron completos junto con las cesiones de 37/119/263 y los cierres o
continuaciones de 40/122/266. Las series numeradas y el desarrollo táctico son
parte de las mismas exposiciones: **no se inventan nuevos hablantes por cambiar
de párrafo o de punto numerado**. Las referencias a acuerdos anteriores del
Consejo dentro de esas exposiciones siguen con el expositor.

Estas revisiones mejoran la evidencia de atribución; no habilitan por sí solas
anclas ni uniones automáticas entre registros. Se preservan los enlaces de turno
que ya estaban confirmados, sin añadir continuidad por mera proximidad.

## 2. Respuestas anafóricas acotadas

- **458:** García responde a la consulta de Eyzaguirre sobre inflación subyacente,
  entre su exposición de 456 y el comentario de Corbo en 459.
- **555:** el «citado Gerente» responde por petróleo/cobre y cuenta corriente.
  La introducción de 554 y la nómina local identifican a García; Valdés recibe la
  palabra recién después, en 556.
- **506:** se revisan sólo los **206 caracteres** de la respuesta de Lehmann sobre
  el bono de CODELCO, entre la consulta de Eyzaguirre y el comentario de Desormeaux.
  La primera exposición de 8.662 caracteres del mismo padre **no se certifica**
  con esa revisión y conserva su alerta por anáfora.
- **1923:** los **88 caracteres** sobre fechas spot son la respuesta de Lehmann
  a De Gregorio. Se añade un intervalo secundario sin modificar la revisión
  anterior de Velasco ni absorber el retorno posterior de De Gregorio.
- **2058:** Soto responde por los rubros no transables después de la pregunta
  de Marfán y antes de la siguiente consulta presidencial.

También se reconocen mejor los sujetos explícitos de **569, 570 y 752** mediante
«aprovecha de agradecer», «como siempre» y «hace una observación».
Se siguen exigiendo sujeto y predicado compatibles: ni asistencia ni mención
constituyen una intervención.

## 3. Nombre identificado no implica cargo textual confirmado

**180, 5573 y 6282** tienen nombre y predicado suficientes para revisar al hablante,
pero sus cargos literales difieren de la nómina local:

| Padre | Hablante | Cargo literal que queda pendiente |
|---|---|---|
| 180 | Sergio Lehmann | Gerente de Análisis Financiero |
| 5573 | Beltrán de Ramón | Gerente de División Operaciones Monetarias |
| 6282 | Beltrán de Ramón | Gerente de División Política Operaciones Financieras |

No se reescribe ninguno. Se conservan por separado los campos de texto y nómina,
y se añaden **tres avisos `CARGO_EN_DISCURSO_POR_VERIFICAR`**. Las diferencias
requieren cotejo; no prueban que exista un cargo nuevo ni que la nómina sea falsa.
La atribución nominal revisada no cierra esos avisos.

Con la revisión del tramo presidencial de **3126**, son **15 intervalos de
hablante nuevos en 15 padres**, 14 de ellos sin revisión previa. En 1923 se conserva
el intervalo anterior y se añade uno independiente. Los **177 intervalos previos
permanecen idénticos por identificador**, incluyendo límites, actor y evidencia.

## 4. Corregir los límites entre persona y acta

### Cuatro encabezados formales

En **2438, 2839, 3126 y 3205**, el encabezado con código de acuerdo y título
«Tasa de Política Monetaria» estaba pegado al discurso presidencial.
Ahora se conserva con el **bloque institucional** que le sigue.

El reconocimiento exige código formal y título, no basta una cifra, la palabra
«tasa» ni una mención retrospectiva. Se conservan `T a s a`, `T asa` y `T a sa`
literalmente. En 3126 la revisión del Presidente termina antes del código;
«se refirió» sólo se adjudica en ese intervalo, sin relajar la guardia general
contra referencias retrospectivas.

### Aperturas/cierres con sujeto personal explícito

En **3067, 3109, 3193, 3328, 3421, 3572 y 3881**, un prefijo horario no debe borrar
al Presidente que explícitamente abre, reanuda o suspende la sesión.
Se distingue de «se reanuda», sin sujeto personal, que sigue siendo acta.

- La hora debe ser válida y el sujeto/predicado reconocido. No se infiere habla
  por estar presente ni se asigna una bienvenida a su destinatario.
- Se mantienen límites entre la mañana y la reapertura de la tarde, aun cuando
  ambas correspondan al mismo Presidente.
- **3067** conserva la constancia institucional del retiro de Claro; la cesión
  presidencial y la exposición de García quedan separadas.
- **3421** conserva la revisión previa de los **797 caracteres** de agradecimiento.
  El reconocimiento de la reapertura no absorbe ese intervalo ni su identificador.
- **3881** conserva un bloque institucional de **177 caracteres** con la reanudación
  y la incorporación de Marfán/Larraín, entre suspensión y bienvenida presidencial.

### 3110 no es una intervención de Orellana

3109 termina «se acuerda que dicho horario será fijado por.»; 3110 continúa con
Orellana, la aprobación del Fiscal y la citación al Ministro. Son funciones del
acuerdo administrativo, **no palabras pronunciadas por Orellana ni Nacrur**.
3111 vuelve a identificar al Presidente al ceder la palabra a García.

Se registra 3110 como **continuación de acta**, en un registro separado:
[`revisiones_continuaciones_acta.json`](../data/curation/revisiones_continuaciones_acta.json).
Exige el texto completo, el antecedente inmediato, misma sesión, ambos hashes,
cita final del antecedente, justificación y límites de la decisión. La salida es
`Consejo / ACTA_INSTITUCIONAL / ACTA/META`, con nota de trazabilidad, sin ancla
personal. No se habilita herencia institucional global.

Se conserva el daño «por.» / «A continuación,.». **«Comunicado oportunamente»
es un participio del trámite, no el comunicado de política monetaria.**
Tampoco se infiere intervención de Larraín a partir del actor original de esta fila.

## 5. Ensayos, controles y publicación

Se hicieron dos ensayos aislados y luego el pipeline integral, con un reintento
tras una comprobación F1 fallida. No se publicaron las salidas rechazadas.

1. El ensayo exploratorio reveló que reconocer la reapertura podía absorber la
   revisión previa del mismo actor en 3421 y el bloque de asistencia en 3881.
   Se preservaron el inicio de revisión como límite de evidencia y la reanudación
   narrativa como acta. No se convierten revisiones contextuales en anclas.
2. El segundo ensayo conservó todos los enlaces previos y obtuvo **9.497 / 343**.
3. F1 rechazó el subtipo `COMUNICADO` de 3110. Se corrigió a
   `ACTA_INSTITUCIONAL` mediante su revisión específica, sin cambiar el texto.
   La comparación de la publicación con el segundo ensayo verifica que esa es
   la **única diferencia de campo** en la base de auditoría.

`python scripts/preparar_data.py`: **1.035 pruebas, F0 y F1 aprobados**, sin errores
bloqueantes. **60 pruebas nuevas:** 30 contratos por padre y 30 de comportamiento,
alcance, evidencia, barreras, errores de clasificación y conservación.
Los contratos anteriores se actualizan sólo para cambios verificados; las
fixtures no relacionadas permanecen intactas.

Verificación global posterior:

- **7.219 textos y 2.048.560 palabras conservados**, ignorando sólo espacios.
- **Todos los enlaces anteriores entre padres y los grupos no afectados intactos**.
  Sin enlaces nuevos ni retirados; se mantiene 2790 → 2791 y no se restaura
  el enlace erróneo 5402 → 5403.
- Las dos exposiciones de García de once filas permanecen intactas.
- 314 grupos de varias filas: el grupo adicional corresponde a dos tramos del
  mismo padre **3881**, no a una nueva unión entre padres.
- **64 hashes de entradas/código y 11 de salidas verificados**.
- 132 sesiones, 51 etiquetas/50 personas, 310 contrastes TPM, esquemas XLSX **37/24**.
- Los 177 intervalos previos, las diez advertencias previas, once menciones actuales,
  21 fórmulas y registros documentales se conservan.
- Los tres escritos de Larraín leídos por Vergara siguen con **autor ≠ lector**,
  sin inferir asistencia ni habla oral del autor. No se deduplican opiniones.

## 6. Qué sigue pendiente

**343 filas con alertas en 309 padres**. Motivos superpuestos:

| Motivo | Filas |
|---|---:|
| Anáfora | 32 |
| Atribución heurística legada | 8 |
| Cargo textual por verificar | 4 |
| Final sin puntuación | 258 |
| Fragmento breve | 10 |
| Posible otro hablante o mención | 21 |
| Pasajes conjuntos por delimitar | 6 |
| Texto dañado por cotejar | 2 |
| Variante de identidad | 6 |
| Duplicado no fórmula | 3 |
| Escrito leído por tercero | 3 |
| Hablantes por identidad pendiente | 1 |

El descenso **359 → 343** no oculta las tres discrepancias de cargo añadidas.
Las alertas no son un conteo de errores confirmados ni de filas completamente
sin leer. Persisten **780/6185**, los residuos colectivos de **3191/5367**,
las confirmaciones pasivas y daños señalados, **4433**, **6443**, las variantes
de Ricaurte, 6530 y las repeticiones. No se cerraron por proximidad o tema.

Cola histórica de 783: **131** pendientes de lectura contextual, **302** métodos
actualizados, **170** cambios por comparación, **98** correcciones dirigidas,
58 fórmulas, siete breves, ocho menciones históricas, seis identidades, dos
repeticiones y una continuidad. Son **137 triajes, 472 comparaciones automáticas
y 174 lecturas dirigidas por agente**. La bajada histórica **150 → 131** no equivale
a 19 lecturas humanas o cierres integrales. Las once menciones actuales se cuentan
aparte de las ocho históricas.

**Sin lectura exhaustiva del corpus ni muestra semántica independiente.**
Las lecturas de encabezados y ventanas locales no certifican todo el padre.
Verificaciones locales: el workflow de GitHub Actions sigue fuera del PR por
falta de permiso `workflows`. No hay proceso activo en segundo plano.
