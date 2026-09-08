# Continuación de revisión: menciones legítimas y pasos de palabra

> Antecedente de la ronda de 9.142 filas. La salida vigente se documenta en
> [Revisión de coordinaciones](REVISION_COORDINACIONES_2026-09-07.md).

**Fecha:** 2026-09-07. **Base anterior:** 9.134 filas / 723 alertas.
**Salida publicada:** 9.142 filas / 661 alertas; **125 pruebas y F0/F1 aprobados**.

## Alcance y entregables

Se continuó la revisión dirigida del consolidado, sin cotejar estos pasajes con
los PDFs. Se leyeron ocho intervalos señalados por posibles menciones y se
contrastaron los cambios de segmentación introducidos por las reglas nuevas.
No se declara revisión exhaustiva de las 783 alertas originales.

- [Seguimiento actualizado de las 783 alertas](../data/processed/revision_783.xlsx).
- [Cambios de esta ronda, con texto completo e IDs](cambios_menciones_cesiones_2026-09-07.csv).
- Base final: `data/processed/consolidado_base_referencia_final.xlsx`.

## 1. Ocho menciones legítimas documentadas, sin ocultar alertas

Se agregó el estado **`MENCION_LEGITIMA_REVISADA`** al seguimiento. Sus decisiones
están ancladas al hash del texto de la cola original y contienen una cita y una
justificación. **No reasignan actores ni suprimen el motivo automático**. La
revisión de una mención tampoco elimina una alerta independiente de método legado.

| ID de la cola original | Padre | Actor que continúa | Motivo de la decisión |
|---|---|---|---|
| 710 | 571 | Desormeaux | Fundamenta su voto y recuerda lo que «recientemente el Gerente… señaló». No comienza a hablar el Gerente. |
| 854 | 647 | Velasco | «Recuerda que el Gerente…» introduce un diagnóstico previo dentro de la argumentación del Ministro. |
| 1447 | 1114 | Valdés | De Ramón aparece en el inciso «como también lo menciona…», no en un nuevo turno. |
| 1721 | 1328 | Desormeaux | Remite a la exposición anterior de Magendzo al señalar un posible desfase en créditos. |
| 1741 | 1338 | Jadresic | Recoge el comentario previo de Magendzo y sigue desarrollando la diferencia entre promedios y escenarios modales de tasas. |
| 2061 | 1574 | Lehmann | Marshall y Marfán son destinatarios o referentes. El mercado, no Marfán, es sujeto de «da cuenta» en el pasaje que dispara la alerta. |
| 3259 | 2397 | Claro | Cuestiona el escenario de deflación «que planteaba el Gerente». Conserva además su advertencia de atribución legada. |
| 3301 | 2430 | De Ramón | «Las que ya comentó el Gerente…» remite a brechas mencionadas antes; continúa la propia evaluación de De Ramón. |

Las ocho mantienen `POSIBLE_OTRO_HABLANTE_O_MENCION` en la base automática y
muestran la adjudicación separada en `revision_783.xlsx`. No se introdujo una
regla global que silencie toda frase como «recuerda que».

## 2. El paso de palabra no pertenece al argumento de Claro

En cuatro padres, el texto original contiene esta unión defectuosa:

> El Presidente ofrece la palabra a los señores Consejeros para proceder a la El Consejero señor Sebastián Claro…

El filtro contra cortes tras artículos impedía separar el segundo sujeto. El
comienzo del argumento de Claro quedaba bajo el Presidente hasta otra identificación
posterior. Se agregó una excepción **sólo para esta secuencia comprobada**:

| Padre | Fecha | IDs actuales |
|---|---|---|
| 2121 | 2008-10-09 | 2898 Presidente / 2899 Claro |
| 2166 | 2008-11-13 | 2953 Presidente / 2954 Claro |
| 2293 | 2009-01-08 | 3130 Presidente / 3131 Claro |
| 2434 | 2009-03-12 | 3311 Presidente / 3312 Claro |

La frase del Presidente **sigue terminando en «proceder a la»**. No se inventa
el sustantivo que falta, ni se reescribe el OCR. La advertencia de final incompleto
queda visible. Los argumentos de Claro, incluidos sus votos, se conservan completos.
La excepción no actúa dentro de citas entrecomilladas.

## 3. Prefijos legítimos que no debían borrarse como OCR

La limpieza inicial podía interpretar «En» como basura OCR al comenzar una frase
con «En el…» o «En la…». Se protegieron esas preposiciones y otras palabras
funcionales. Se añadieron dos reconocimientos específicos:

- «Como es habitual» como introducción al sujeto que agradece o comenta.
- «Gerente de la División…» como variante gramatical para el reconocimiento,
  sin reescribir el texto ni modificar la lista de asistencia.

Esto recupera intervenciones como «En el mismo sentido, el señor Soto agrega…»
y evita atribuir los agradecimientos de Marshall o Desormeaux a quien habló antes.

También se reconoce **«hace referencia»** como locución de habla ligada al sujeto.
El caso más claro es el **padre 7032**, del 2015-09-15: el texto comienza «El señor
Beltrán de Ramón hace referencia…», pero la atribución anterior era García, citado
más adelante. Ahora queda bajo **De Ramón** (ID actual 8927), sin cambiar texto.

## 4. Se preserva el retorno del expositor

### Aeronaves: padre 6135, 2014-04-17

La primera corrección reconoció la consulta de Soto, pero dejó la explicación de
Vicuña dentro del bloque siguiente de Fuentes. La lectura completa permitió
separar la cláusula interior y la reanudación explícita:

**Fuentes → Soto → Fuentes → Vicuña → Fuentes** (IDs actuales 7920–7924).

La explicación de Vicuña empieza en «en tanto el Gerente de División Estadísticas
señor Ricardo Vicuña precisa…» y termina antes de «El señor Miguel Fuentes retoma
su presentación…».

La decisión **`HAB-20260907-6135`** en `revisiones_hablantes.json` tiene hash,
intervalo, citas y justificación. No se añadió un corte automático ante cualquier
«en tanto». Un límite interior revisado exige coma/punto y coma previo, estar
fuera de comillas y tener un sujeto explícito compatible. F1 comprueba que el
intervalo conserve texto y actor. Ya son cuatro decisiones de hablante documentadas.

### Otros cambios contrastados

La comparación con la versión anterior identifica **14 padres** con cambios de
actor o límites; no implica 14 correcciones independientes de todo su contenido:

| Padre | Filas antes → ahora | Cambio principal |
|---|---:|---|
| 300 | 9 → 10 | Valdés responde «En el mismo sentido…»; no queda bajo Vicuña. |
| 1461 | 3 → 2 | Se reconoce el inicio de Jadresic y desaparece un corte dentro de su propio discurso. No se elimina texto. |
| 1565 | 2 → 2 | El agradecimiento «Como es habitual…» inicia el bloque de Marshall, no el del Presidente. |
| 1566 | 2 → 2 | El agradecimiento de Desormeaux no queda dentro del bloque de Marfán. |
| 2121, 2166, 2293, 2434 | 2 → 2 cada uno | Separación correcta de cesión del Presidente e intervención de Claro. |
| 2213 | 1 → 2 | Marfán → García; el cargo «Gerente de la División Estudios» ya se reconoce. |
| 2534 | 2 → 3 | De Gregorio → García → Soto, que continúa con vestuario e inflación. |
| 2796 | 2 → 2 | «En el frente externo…» pasa al comienzo de la intervención de Marshall. |
| 6135 | 1 → 5 | Consulta y respuestas sobre aeronaves, con retorno explícito a Fuentes. |
| 7032 | 1 → 1 | García → De Ramón: una referencia a García no lo convierte en hablante. |
| 7058 | 3 → 5 | Vial → Naudon → Vial → Vergara → Raddatz; este último «hace referencia» a un informe laboral. |

Incremento neto: **8 filas**, sin añadir ni perder palabras. Los cambios de método
sin cambio de actor se distinguen de las correcciones de atribución en el seguimiento.

## 5. Balance acumulado de la cola original

Estas categorías son exclusivas y suman **783 intervalos originales**:

| Estado actual del seguimiento | Filas |
|---|---:|
| Pendiente de lectura contextual | 537 |
| Fórmula procedimental reclasificada | 59 |
| Método actualizado | 65 |
| Segmentación o actor modificado | 98 |
| Breve válido revisado | 7 |
| Mención legítima revisada | 8 |
| Identidad pendiente | 6 |
| Repetición sustantiva pendiente | 2 |
| Continuidad entre padres revisada | 1 |

Hay 77 filas vinculadas a decisiones de lectura, 163 a comparación automática y
543 sólo a clasificación inicial. Las decisiones sobre fórmulas siguen basadas
en 17 textos distintos aplicados a sus repeticiones; no son verificaciones PDF
independientes de cada fila. Los 98 intervalos modificados **no se declaran libres
de mezclas**. Hay 648 intervalos originales que aún se solapan con alertas actuales.

## 6. Controles y advertencias

- **125 pruebas aprobadas**, diez nuevas; F0/F1 pasan sin errores bloqueantes.
- **7.219/7.219 padres** reconstruidos ignorando sólo espacios.
- **9.142 filas físicas / 9.141 bloques**, 37 columnas de auditoría y 24 finales.
- **2.048.560 palabras**, sin variación; celda máxima **31.948 caracteres**.
- 132 sesiones, 51 etiquetas de actor, **310 fórmulas TPM contrastadas**.
- 8.766 grupos de turno, 285 de varias filas; máximo de once filas.
- Se conservaron las exposiciones de García de once filas en **60–70** y
  **142–152**, y las referencias sin cortes falsos de **3454, 3715 y 4266**.
- Verificados los hashes de **32 entradas/archivos de código y diez salidas**,
  CSV de seguimiento/pendientes/turnos/decisiones y `data/raw` sin cambios frente
  a Git. `git diff --check` no reportó problemas.

Quedan **661 filas con alertas automáticas**, frente a 723 antes. Motivos
superpuestos: 265 atribuciones legadas, 170 posibles otros hablantes/menciones,
194 finales sin cierre, 37 anáforas, ocho breves, seis identidades y dos duplicados
no fórmula. Las ocho menciones adjudicadas siguen incluidas en esos avisos.

La disminución de 62 alertas **no significa 62 errores confirmados corregidos**:
parte corresponde a métodos ahora reconocidos; otros casos cambian de límites.
Los finales incompletos aumentan al exponer las cesiones defectuosas del OCR.
No se completó artificialmente su texto.

Persisten 537 intervalos sin lectura contextual adjudicada, las seis identidades,
las dos repeticiones sustantivas y revisiones residuales de intervalos modificados.
No se ofrece certificación semántica ni histórica de todo el corpus. Las lecturas
fueron del consolidado, no de los PDFs; continúan las limitaciones de la referencia
TPM de Datosmacro y de los controles que comparten reconocedores con el constructor.
