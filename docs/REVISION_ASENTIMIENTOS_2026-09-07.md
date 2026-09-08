# Asentimiento expreso y complementos de exposición

> **Informe histórico.** La publicación posterior a esta tanda está en [retornos y respuestas](REVISION_RETORNOS_2026-09-07.md): 9.221 filas / 629 alertas / 285 pruebas. Los IDs, métricas y checkpoint de este documento corresponden a la tanda anterior; los enlaces a `data/processed/` abren la versión vigente.

**Fecha:** 2026-09-07. **Inicio:** 9.215 filas / 633 alertas / 257 pruebas.
**Publicación:** **9.218 filas / 632 alertas / 272 pruebas; F0/F1 aprobados.**

## Alcance y entregables

Se revisaron 2779, 3107 y 3158 y los comienzos/cierres pertinentes de sus padres
vecinos. **Tres padres modificados, ocho segmentos resultantes y tres filas
adicionales.** No hubo cambios de texto/actor ni de metadatos semánticos fuera
de esos tres padres, descontando renumeraciones de identificadores.

**Lectura dirigida del consolidado por el agente, sin cotejo PDF ni revisión
humana independiente.** No es una revisión exhaustiva de la cola ni una
certificación de todos los tramos de los padres afectados.

- [Excel de seguimiento y cola vigente](../data/processed/revision_783.xlsx).
- Base final: `data/processed/consolidado_base_referencia_final.xlsx`.
- [Tres padres: hashes, IDs anteriores y ocho segmentos actuales](cambios_asentimientos_2026-09-07.csv).
- [Contenido anterior/posterior y hashes de las bases](comparacion_asentimientos_2026-09-07.json).
- [Punto de reanudación y pendientes](estado_revision_asentimientos_2026-09-07.json).

Los números de padre son IDs del consolidado original; los IDs de filas actuales
pueden cambiar con una nueva publicación. El checkpoint no es un proceso activo
en segundo plano.

## 1. Padre 2779 — 2009-11-12

Antes, el segmento completo de 612 caracteres estaba atribuido a Cowan. Ahora
se conserva esta secuencia:

| Actor | Texto/alcance | Caracteres |
|---|---|---:|
| Kevin Cowan | Planteamiento sobre empleo asalariado y por cuenta propia | 222 |
| Claudio Soto | `El señor Soto asiente,` | 22 |
| Enrique Marshall | `mientras que… responde…`, incluida la continuación `En su opinión…` | 366 |

El asentimiento es **un acto expresamente narrado**, no una transcripción de
palabras pronunciadas. No se añadió «sí», una explicación, ni una interpretación
de cómo asintió Soto. La respuesta y su continuación pertenecen a Marshall,
no a Soto ni a Cowan.

La revisión **HAB-20260907-2779** delimita la respuesta de Marshall con hash,
citas y límites. El reconocimiento de `asiente` requiere sujeto válido; la
palabra por sí sola no identifica un hablante. La otra aparición en la fuente,
en 1054 —`un nuevo escenario se asiente`—, no cambió su segmentación.

Se admite el prefijo `mientras que` cuando hay sujeto y predicado explícitos,
con guardas de mención, comillas y verbos previos. **No se crea una regla global
que divida todas las cláusulas con ese conector**: el límite interno de Marshall
se habilita por la revisión individual y exige separador previo. Sin ella, el
asentimiento se reconoce, pero la respuesta contrastiva sigue sin separarse.

El breve segmento de Soto mantiene `FINAL_SIN_PUNTUACION;FRAGMENTO_BREVE`.
La coma y la brevedad son reales; no se cambió la fuente ni se suprimieron esos
avisos para mejorar el contador.

## 2. Padre 3107 — 2010-05-13

**Dos → tres segmentos**:

- Marfán: **2.900 caracteres**, exposición inicial intacta.
- De Ramón: **1.558 caracteres**, respuesta sobre la crisis griega y liquidez.
- Bernier: **336 caracteres**, desde `Para complementar, el Gerente de Mercados
  Financieros Nacionales, señor Matías Bernier, señala…` hasta el final.

La revisión **HAB-20260907-3107** devuelve a Bernier su complemento explícito.
`Agrega que el ha ido disminuyendo…` sigue con él, no se trata como otro turno.
Su cargo coincide con la lista de asistencia de la sesión según los controles.
Bernier aparece ahora entre las voces detectadas de esa fecha; no es un cambio
de cargo de una fila que conservara texto y actor.

Se mantienen expresiones dañadas como `han sido que no ha renovado en los Repos,
y últimamente` y `Agrega que el…`. **No se completaron nombres de bancos,
sujetos omitidos ni redacción**. Delimitar al autor del complemento no recupera
el contenido perdido; el daño queda explícito en el checkpoint para cotejo.

## 3. Padre 3158 — 2010-06-15

**Dos → dos segmentos**, adelantando el comienzo de Soto:

- García: **82 caracteres**, nivel de empleo de 6,5 millones de personas.
- Soto: **746 caracteres**, desde `y el señor Claudio Soto agrega…`, incluyendo
  la variación anual, `400.000 personas`, `El señor Soto prosigue…`, los sectores
  y la continuación final sobre volatilidad y terremoto.

La revisión **HAB-20260907-3158** usa `COORDINACION_Y_EXPLICITA`, sin generalizar
los cortes a toda conjunción. No se inventó una coma antes de `y`, no se partió
la cifra `400.000` y no se separaron las continuaciones de la exposición de Soto.
El nuevo final de García conserva el aviso de falta de puntuación.

## 4. Validación de la publicación

- **272 pruebas aprobadas**, 15 nuevas: conservación, hashes, secuencia de actos,
  ausencia de palabras inventadas, usos no personales de `asiente`, referencias,
  comillas, separador previo, actor incompatible, continuidad del expositor y
  exactitud de los intervalos revisados.
- **53 revisiones de hablante**, tres más. Las **50 anteriores siguen idénticas**.
  Hay 18 coordinaciones documentadas; no son un permiso para dividir cualquier `y`.
- Ensayo aislado, comparación de alcance y ejecución completa de
  `scripts/preparar_data.py`: pruebas, construcción, exportación, **F0/F1** y
  publicación. La hoja principal publicada coincide con el ensayo aislado.
- Comparación de **7.219 padres**: exactamente 2779, 3107 y 3158 cambian texto
  segmentado o actor. Los otros **7.216** conservan texto/actor, cargo/fuente,
  método, tipo de acta, motivos y relación de continuidad. No cambian cargos en
  segmentos de texto y actor idénticos.
- Conservación global ignorando sólo espacios: **2.048.560 palabras**,
  **9.217 bloques en 9.218 filas físicas**, máximo 31.948 caracteres por celda.
  El Excel de origen sigue idéntico al de `HEAD`.
- **8.829 grupos de turno; 298 multipárrafo; máximo 11 filas**. Verificada la
  partición de los grupos no afectados y los catorce enlaces protegidos,
  incluidos **2408 → 2409**, **2566 → 2567** y **2785 → 2786**. Conservadas las
  dos exposiciones de García de once filas, padres **60–70** y **142–152**.
- **44 hashes de entradas/código y 10 de salidas verificados** contra el manifiesto.
- 132 sesiones; 51 etiquetas de actor / 50 personas según F0; 310 contrastes TPM;
  559 duplicados exactos, 557 de fórmula. Estos controles no son una lectura
  semántica independiente ni un cotejo de las 132 actas originales.

## 5. Alertas y cola histórica

**633 → 632 filas con alertas**. Los motivos se superponen:

| Motivo | Antes | Ahora |
|---|---:|---:|
| Posible otro hablante/mención | 103 | 100 |
| Final sin puntuación | 234 | 236 |
| Fragmento breve | 8 | 9 |
| Atribución legada | 259 | 259 |
| Anáfora | 42 | 42 |
| Variante de identidad | 6 | 6 |
| Duplicado no formulaico | 2 | 2 |

Los avisos nuevos corresponden al asentimiento de Soto y al final de García en
3158. **La variación no mide errores confirmados**. No se eliminan alertas por
el mero hecho de haber leído un intervalo.

En las **783 filas originales**: **463** pendientes de lectura contextual; 59
fórmulas; 71 métodos actualizados; 116 cambios por comparación; **50** correcciones
dirigidas; siete breves válidos; ocho menciones históricas; seis identidades;
dos repeticiones y una continuidad. Por tipo: **127 lecturas dirigidas por agente,
187 comparaciones y 469 triajes**. **609 intervalos originales** todavía se
solapan con alertas actuales. Los estados no certifican padres completos.

Las seis menciones actuales documentadas se cuentan aparte y conservan sus
avisos; 4574 conserva también la atribución legada. Quedan **86 candidatos de
otro hablante sin anotación de mención**, bajo el filtro anterior, no 86 errores
confirmados ni una lista exhaustiva de residuos.

## 6. Continuación pendiente

2779 deja de estar pendiente por el intercambio concreto abordado, sin convertir
la tanda en una certificación semántica independiente. Se mantienen:

- Inicio de Corbo en **780** y enlace dañado de **2667**, pendientes de cotejo.
- Intervención conjunta de **2126**, sin asignación arbitraria a una sola persona.
- Confirmaciones pasivas en **2661 y 2704**, sin palabras inventadas.
- Daño textual de **3107**, aun con el complemento ya delimitado.
- La cola restante, las seis variantes de identidad, las dos repeticiones
  sustantivas y la revisión independiente de una muestra con y sin alertas.

No se obtuvo un PDF nuevo ni se realizó una auditoría semántica independiente
en esta tanda. El checkpoint mantiene esa limitación y los siguientes candidatos.
