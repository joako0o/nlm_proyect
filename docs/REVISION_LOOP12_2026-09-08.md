# Loop12 — Separaciones parciales, residuos visibles y continuidad preservada

Fecha: **2026-09-08**. Continúa [PR #3](https://github.com/joako0o/nlm_proyect/pull/3).
Base anterior: commit `e2858c5f53be123395ba102fedb9f5b44bcdf39a`,
[loop11](REVISION_LOOP11_2026-09-08.md). No hubo nuevo cotejo PDF ni revisión humana independiente.

## Resultado publicado

| Medida | Antes | Ahora |
|---|---:|---:|
| Filas físicas XLSX | 9.489 | **9.494** |
| Bloques de texto | 9.488 | 9.493 |
| Grupos de turno | 9.080 | 9.085 |
| Filas con alertas | 368 | **359** |
| Padres con alertas | 334 | 323 |
| Pruebas | 930 | **975** |
| Intervalos de hablante revisados | 160 | **177** |
| Padres con revisión de hablante | 158 | 174 |
| Advertencias contextuales registradas | 2 | 10 |

**22 padres afectados:** tres con separaciones nuevas (3 → 8 segmentos),
13 con atribución antigua documentada sin cambiar actor/texto y seis con nuevas
advertencias sin cambiar actor/texto. Son **tres cambios estructurales y 19 de
metadatos**, no 22 errores de separación corregidos. Los otros **7.197 padres**
conservan sus campos semánticos, descontando identificadores secuenciales.

Evidencia durable: [comparación global](comparacion_loop12_2026-09-08.json),
[detalle de filas](cambios_loop12_2026-09-08.csv) y
[checkpoint con pendientes](estado_revision_loop12_2026-09-08.json).

## 1. Separaciones recuperadas, sin adjudicar los residuos colectivos

### 3191: cierre de García, prefijo aún provisional

Se separa el cierre «Al finalizar esta discusión… Pablo García…»:
**520 caracteres provisionales bajo Marshall → 471 de García**. García se refiere
al planteamiento de Marfán: esa referencia no crea un turno de Marfán.

Los 520 caracteres iniciales incluyen a Marshall, una opinión de Claro y
«el señor Presidente y el señor Claudio Soto coinciden». **No se certifican como
habla exclusiva de Marshall** ni se adjudica la coincidencia conjunta a Claro.
Ahora tienen `PASAJES_CONJUNTOS_POR_DELIMITAR`, con alcance/hash exactos y bloqueo
de continuidad. La recuperación del cierre no equivale a cerrar todo el padre.

### 5367: Herrera responde, Fuentes vuelve, Claro opina

Antes: 3.944 caracteres bajo Fuentes. Ahora:

| Tramo | Actor/estado | Caracteres |
|---|---|---:|
| Presentación, solicitud colectiva y rótulo OCR | Fuentes provisional para el residuo | 2.995 |
| Ejemplo de crédito y consumo | Luis Óscar Herrera | 409 |
| Aclaración de colocaciones comerciales/PIB | Miguel Fuentes | 223 |
| Opinión sobre financiamiento exterior | Sebastián Claro | 314 |

Dos revisiones independientes delimitan Herrera y Claro; el retorno de Fuentes
se reconoce por su sujeto explícito. Se conserva literalmente
`B A N C O C E N T R A L D E C H IL E` en el prefijo. La solicitud de los Consejeros
queda advertida: **no se atribuye individualmente a Fuentes ni a Herrera**.

### 5647: observación de Vergara y respuesta de Lehmann

**Vergara 221 → Lehmann 675 caracteres.** El conector «por lo que» permanece
literalmente con la respuesta. Lehmann se compromete a revisar los datos y
continúa con intervenciones cambiarias en Perú, Brasil, Colombia y Corea.
Se leyó el desarrollo completo junto con 5646 (Lehmann expone monedas) y 5648
(Vial interviene). No se impone una regla general para todas las causales ni para
cualquier continuación temática. También se conserva la grafía `cambiarías`.

El límite `RESPUESTA_POR_LO_QUE_EXPLICITA` sólo opera con una revisión individual:
conector exacto, coma anterior, sujeto explícito compatible y fuera de cita.

## 2. Trece atribuciones antiguas documentadas

**392, 629, 790, 1092, 1128, 1758, 1842, 1899, 2790, 3189, 3385, 5207 y 7019.**
No cambian sus actores ni textos. Se reemplaza la evidencia heurística legada
por decisiones acotadas en el registro, conservando los límites ya válidos.

- Se preservan `Klauss Schmidt`, `Marfán Manuel` y `si posible`; no se crean alias
  globales ni se reescribe el OCR.
- En 1758, Soto es el autor del ejercicio mencionado; consulta el Ministro.
- En 1842, la nómina local identifica a Recart como Ministra Subrogante; no se
  usa la titularidad ordinaria de Velasco.
- En 1899 se conserva Marfán → Soto → Marfán; en 3189, Marshall → García → Marfán.
- En 5207, Soto termina antes de la suspensión de Vergara y del acta de reanudación.
- En 2790, el desarrollo nombra a Soto. La nómina no demuestra por sí sola la
  subrogancia de Estudios: la decisión se sustenta en el desarrollo nominal interno.

### Regresión detectada y rechazada antes de publicar

El primer ensayo produjo **9.492 filas / 356 alertas**, pero absorbía bajo
`CONTEXTO_REVISADO` las identificaciones nominales posteriores de 1092 y 2790.
Esto eliminaba el enlace correcto **2790 → 2791, Soto**. **No se publicó.**

Se acotaron ambos intervalos y se añadió el campo opcional
`Cita_Ancla_Posterior`. Exige cita literal en `Fin`, límite de oración, sujeto
explícito del mismo actor y ausencia de cita abierta. Conserva la separación
entre evidencias del mismo expositor; **no inventa un cambio de persona**.
`Fin` por sí solo sigue sin crear cortes. `CONTEXTO_REVISADO` sigue sin producir
anclas: la ancla pertenece al sujeto nominal posterior.

El segundo ensayo y la salida publicada conservan **todos los enlaces anteriores**,
sin añadir ni retirar ninguno. También se conservan los grupos no afectados,
los 313 grupos multipárrafo y las dos exposiciones de García de once filas.
No se restaura el enlace erróneo 5402 → 5403 retirado en loop10.

## 3. Advertir no es corregir

Ocho nuevas advertencias: las dos de 3191/5367 y otras seis en estos padres:

| Padre | Residuo advertido | Decisión |
|---|---|---|
| 2126 | Votación conjunta del Vicepresidente y Claro | Sin reparto individual |
| 3989 | Coincidencia conjunta de De Gregorio y Marshall | Sin adjudicación exclusiva |
| 2661 | Confirmación pasiva de Lehmann dentro del tramo de Desormeaux | Pendiente de delimitación |
| 2704 | Confirmación pasiva de Soto dentro del tramo de Marshall | Pendiente de delimitación |
| 2667 | `y el Gerente de`, cargo truncado | Cotejo textual pendiente |
| 3107 | Frases incompletas en el tramo de Bernier | Cotejo textual pendiente |

Las confirmaciones pasivas no se transforman en palabras inventadas de sus
participantes. En 3107 la atribución de Bernier sigue revisada, pero eso no
certifica la integridad del contenido. Los daños permanecen literalmente.

Se incorporan `PASAJES_CONJUNTOS_POR_DELIMITAR` y `TEXTO_DANADO_POR_COTEJAR`.
La barrera de continuidad y su validación comparten el catálogo de motivos
contextuales, evitando olvidar una categoría nueva. Las alertas requieren
fuente, fecha, hash, actor provisional y texto exacto; no son marcas globales.

Las dos advertencias previas permanecen intactas: cargo en **4433** y separación/
identidad en **6443**. No se escoge una identidad de Ricaurte ni se interpreta el
bloque completo de 6443 como una exposición validada de de Ramón.

## 4. Verificación

Se ejecutó `python scripts/preparar_data.py`: **975 pruebas, F0/F1 aprobados**,
sin errores bloqueantes. Se añadieron **45 pruebas**: 16 contratos de segmentación
por padre y 29 de comportamiento, límites, avisos y continuidad. Los contratos
históricos se actualizaron sólo para decisiones que ahora tienen evidencia;
se mantienen las comprobaciones sin revisión y contra adjudicación conjunta.

Comparación global posterior a la publicación:

- Los **7.219 textos** se conservan, ignorando sólo espacios; **2.048.560 palabras**.
- 132 sesiones, 51 etiquetas de actor/50 personas y 310 contrastes TPM.
- Contenido publicado equivalente al segundo ensayo; **61 hashes de entradas/
  código y 11 de salidas verificados**.
- Las 158 entradas anteriores de hablante (160 intervalos), las 11 menciones
  actuales, las 21 fórmulas y los registros documentales no cambian.
- Notas del Excel enlazadas al identificador correcto de cada uno de los 177
  intervalos, incluidos los secundarios de 2622, 4923 y 5367.
- Tres escritos de Larraín leídos por Vergara: **autor ≠ lector**, sin inferir
  asistencia ni habla oral de Larraín. CSV documental y esquemas XLSX **37/24** intactos.
- Se preservan las repeticiones sustantivas: no se deduplican opiniones.

### Alertas actuales — motivos superpuestos

| Motivo | Filas |
|---|---:|
| Atribución heurística legada | 16 |
| Anáfora | 43 |
| Final sin puntuación | 258 |
| Fragmento breve | 10 |
| Posible otro hablante o mención | 21 |
| Pasajes conjuntos por delimitar | 6 |
| Texto dañado por cotejar | 2 |
| Cargo en discurso por verificar | 1 |
| Variante de identidad por verificar | 6 |
| Duplicado no fórmula | 3 |
| Escrito leído por tercero | 3 |
| Hablantes por identidad pendiente | 1 |

**359 filas alertadas en 323 padres.** El descenso 368 → 359 no oculta los ocho
residuos advertidos. Las 13 atribuciones legadas documentadas no implican 13
separaciones nuevas; quedan 16 atribuciones legadas alertadas.

Cola histórica de 783: **150** pendientes de lectura contextual, **285** métodos
actualizados, **169** cambios por comparación, **97** correcciones dirigidas,
58 fórmulas, siete breves válidos, ocho menciones históricas, seis identidades,
dos repeticiones y una continuidad. Se distinguen **156 triajes automáticos,
454 comparaciones automáticas y 173 lecturas dirigidas por agente**.
La variación 163 → 150 no equivale a trece lecturas humanas ni cierres integrales.
Las **once menciones actuales** son un registro diferente de las ocho históricas.

## 5. Pendiente

El filtro anterior de cinco candidatos deja **780 y 6185** sin adjudicar. No es
el total pendiente: 3191 y 5367 se separaron parcialmente y sus residuos siguen
abiertos bajo otro motivo explícito. Continúan además las confirmaciones
pasivas, daños, identidades, cargo de 4433, ambigüedad de 6443 y repeticiones.

En 6185 esta ronda releyó la ventana de Bernier y el cierre de 6186, **no hizo una
nueva lectura integral de los 20.118 caracteres**. No se transfiere la exposición
de commodities a Bernier por «conforme señala». Tampoco se resuelve 6530 ni se
fusionan identidades por proximidad. No se incorporó evidencia externa a las
adjudicaciones de esta pasada.

Falta cotejo de originales en casos dañados/ambiguos y una muestra semántica
independiente con y sin alertas. **F0/F1 no certifican pureza exhaustiva.**
Verificaciones locales; el workflow de GitHub Actions sigue fuera del PR por
falta de permiso `workflows`. No hay proceso activo en segundo plano.
