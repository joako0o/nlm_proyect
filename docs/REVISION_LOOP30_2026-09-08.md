# LOOP30 — Opinión presidencial, cierre de exposición y referencias

**Fecha:** 2026-09-08. **PR:** [#3](https://github.com/joako0o/nlm_proyect/pull/3).
**Base congelada:** LOOP29, commit `046deceebad01bf11b04c018f0509b957660e880`.

## Resultado

**Dos padres resegmentados**, ambos antes sin alerta, para separar intervenciones
presidenciales de los desarrollos de Soto y García. Además, **catorce intervalos de
menciones legítimas** y **tres advertencias textuales** documentadas. No se añade ni
se retira ningún enlace entre padres y no se fusionan filas físicas.

**1.652 pruebas pasan (+ 39)**. Pipeline completo, F0/F1 y comparación global pasan.
Ensayo aislado y publicación son idénticos celda a celda. F0/F1 no certifican pureza
semántica ni integridad textual exhaustivas.

| Unidad | LOOP29 | LOOP30 |
|---|---:|---:|
| Padres de origen | 7.219 | 7.219 |
| Filas físicas / bloques | 9.687 / 9.686 | 9.689 / 9.688 |
| Grupos de turno | 9.253 | 9.255 |
| Grupos multifila / máximo de filas | 338 / 11 | 338 / 11 |
| Filas con alertas / padres alertados | 455 / 385 | 459 / 389 |
| Intervalos personales / padres con revisión | 380 / 351 | 382 / 353 |
| Advertencias contextuales | 74 | 77 |
| Fichas de continuidad revisada | 24 | 24 |
| Lecturas actuales legítimas / pendientes | 39 / 4 | 53 / 4 |
| Documentos / registros institucionales | 12 / 2 | 12 / 2 |
| Archivos de advertencias retiradas | 3 | 3 |
| Intervalos históricos con alertas actuales | 284 | 285 |
| Pruebas | 1.613 | 1.652 |

## Separaciones de voz

Las longitudes son caracteres de la exportación, no offsets del texto crudo.
Las dos fichas incluyen hash, límites, cita inicial y evidencia completa de los
padres 2705–2707 y de la nómina2689, leídos íntegros.

### 2705: una opinión del Presidente dentro de Soto

**Antes:** Claro 430 → Cowan 194 → Soto 946 → Cowan 136 → Soto 1096 → acta 199.

**Ahora:** Claro 430 → Cowan 194 → Soto 664 → **Presidente 281** → Cowan 136 →
Soto 1096 → acta 199.

El texto atribuye expresamente al Presidente la valoración sobre las compensaciones
inflacionarias: **«lo cual, a juicio del señor Presidente, es muy curioso de analizar»**.
La cláusula completa281 se separa de la información expuesta por Soto. Cowan explica
a continuación la incertidumbre y Soto retoma su presentación; ambos retornos
conservan sus sujetos explícitos y anclas propias.

La relativa se conserva literal, incluido «lo cual». La coma queda al final de Soto 664
y genera `FINAL_SIN_PUNTUACION`; no se cambia por un punto ni se borra. La reanudación
final199 permanece como acta institucional, **no como habla del Presidente o de Recart**.

El nuevo tipo **`OPINION_RELATIVA_PRESIDENCIAL_REVISADA`** sólo se aplica con ficha
individual. Exige coma anterior y el inicio exacto «lo cual, a juicio del señor
Presidente, es». Proyecta temporalmente el sujeto presidencial para comprobarlo en
esa sesión y contra el actor de la ficha. La proyección no se exporta. Se mantienen
los controles de citas abiertas, fecha, hash y límites. No se crea una regla automática
para toda opinión relativa ni un alias presidencial independiente de la sesión.

### 2706: termina García y el Presidente da paso a la votación

**Antes:** Presidente 162 → García 7015.

**Ahora:** Presidente 162 → **García 6820** → **Presidente 194**.

La exposición completa de las Opciones termina antes de **«Concluida la presentación
de las Opciones»**. La oración siguiente nombra al Presidente De Gregorio y le atribuye
el paso a la votación. Se separa ese cierre, sin quitar contenido del informe de García.
La nómina2689 confirma quién preside y el cargo de García en esa sesión.

Es una revisión individual en un límite de oración; no se añade «da paso» al detector
automático. En 3340 y 5584 se leyó la misma expresión con sentido económico: no señala
un cambio de voz. Ambos desarrollos de Claro se mantienen completos. En 3340, Marshall
ya tiene su tramo posterior propio y conserva su continuidad.

La lectura de Opciones por García **no se transforma en un documento de otro autor**.
No se corta por longitud ni se unen las intervenciones presidenciales a ambos lados
de la exposición. Las dos nuevas atribuciones siguen como `CONTEXTO_REVISADO`,
sin anclas globales. Fin solo no crea cortes ni anclas.

## Catorce revisiones de referencias

Se leyeron todas las partes de cada padre, no sólo la frase detectada. Cada ficha
se limita a un intervalo exacto. Ninguna de estas lecturas cambia su voz o segmentación.

| Padre | Intervalo revisado | Referencia que no debe convertirse en otra intervención |
|---|---|---|
| 649 | Marfán 2174 | Reflexiones a propósito de lo expuesto por el Ministro. De Gregorio 550 y Velasco 341 anteriores permanecen separados. |
| 1298 | Schmidt-Hebbel 5985 | Minuta recién expuesta por el Gerente de Análisis Macroeconómico y evaluaciones previas de Consejeros. No cierra el aviso textual concurrente. |
| 1379 | De Gregorio 731 | Información entregada por el Gerente de Análisis Macroeconómico. La advertencia de De Ramón 1187 corresponde a otro intervalo. |
| 1930 | Desormeaux 340 | Información de Soto sobre Enap dentro de la pregunta. La respuesta real de Soto 414 permanece aparte. |
| 1941 | García 1071 | Información del Gerente de Análisis Macroeconómico. Soto 359 anterior y Velasco 867 posterior conservan sus voces. |
| 2058 | Marfán 242 | Datos de Soto dentro de la pregunta. Respuesta del Gerente265 y dos intervenciones presidenciales ya separadas. |
| 2201 | Desormeaux 1605 | Consultas de Claro, proyecciones del Gerente de Análisis Internacional y análisis de Marfán como antecedentes. |
| 2206 | Desormeaux 303 | Datos del IMACEC entregados por Soto. Se preservan la exposición6097 y la respuesta118 de Soto. |
| 2220 | Claro 356 | Información cambiaria del Gerente de Análisis Macroeconómico; no autoría de la consulta. García 433 queda aparte. |
| 2853 | Bernier 757 | Lo manifestado por el Vicepresidente sobre Libor OIS. Lehmann 462 posterior conserva su intervención. |
| 3570 | Céspedes 746 | Preocupación expresada por Marfán, dentro de la argumentación de Céspedes. |
| 4193 | Claro 385 | Lámina presentada por Lehmann; Claro es quien realiza la observación. |
| 4910 | Vial 2000 | Titular del Financial Times anteriormente aludido por Marfán. |
| 4989 | Herrera 2160 | Índices de transporte aludidos por Vial, dentro del diagnóstico de Herrera. |

**Trece de esos catorce intervalos no aparecen en la cola de pendientes**, pues no
están alertados. 1298 sí aparece: su lectura legítima convive con el aviso textual.
El padre1379 también aparece en la cola, pero por **De Ramón 1187**, no por el intervalo
revisado de De Gregorio 731. No se confunden filas, padres o motivos residuales.

## Tres advertencias textuales, sin reconstrucción

- **1298 / Schmidt-Hebbel 5985:** se conserva **«/aíer»** y la aparente discrepancia entre
  **«80 puntos base»** y **«4,5% a 6,2%»**. Se envía a cotejo, sin recalcular ni sustituir
  cifras ni afirmar que el origen del problema sea necesariamente OCR.
- **1379 / De Ramón 1187:** se conserva **«U) compensaciones»**. La advertencia sólo
  corresponde a ese tramo, no a la opinión posterior de De Gregorio.
- **3340 / Claro 7642:** se conserva **«rV- financieros»**. No se recorta el voto ni se
  extiende el aviso al tramo posterior de Marshall 2692. Otros términos dudosos de ese
  tramo posterior no se dan por certificados ni corregidos.

Son fichas con actor provisional, texto y límites exactos, bajo
`TEXTO_DANADO_POR_COTEJAR`. No adjudican nuevas voces ni certifican integridad de otros
tramos. El aviso de 1298 no queda cerrado por su revisión de mención legítima.

Las 459 filas alertadas son las 455 anteriores más estos tres avisos y la coma de Soto 664
en 2705. **Cuatro filas nuevas no equivalen a cuatro advertencias contextuales** ni a
cuatro errores nuevos confirmados. No se borran signos o duplicados para reducir la cola.

## Comparación global

La comparación abarca **9.689 filas actuales y 7.219 padres**, contra LOOP29 congelado:

- Todo el origen conservado, ignorando sólo espacios: **2.048.560 palabras**.
- Sólo dos padres cambian segmentación. **Cinco padres cambian celdas no secuenciales**:
  2705/2706 por separación y 1298/1379/3340 por advertencia. **7.214 padres conservan esas
  celdas**. Únicamente `ID` e `ID_Turno` se excluyen como numeración secuencial.
- **Todos los enlaces entre padres son idénticos**: ninguno añadido o retirado.
  También los grupos fuera de correcciones/advertencias, comparados por sus miembros.
- **380 intervalos personales, 74 advertencias, 43 lecturas, 24 enlaces revisados,
  12 documentos, 2 registros institucionales y 3 archivos de retiros previos idénticos**.
  Las nuevas fichas se agregan sin sobrescribir las anteriores.
- **84 hashes de entradas/código y 11 de salidas verificados**. Fuentes originales,
  fórmulas, detector automático y motores de continuidad conservan sus hashes.
  Esquemas37/24, 21 fórmulas, 310 contrastes TPM, 132 sesiones y 55 etiquetas se mantienen.
- TPM y documentos conservan todos sus campos sustantivos, salvo IDs de evidencia,
  documento o turno. Autor documental ≠ lector ≠ asistencia; no hay nuevos documentos.
- Las 455 filas previas de la cola conservan sus campos salvo IDs secuenciales.
- Ensayo aislado y publicación idénticos celda a celda. Publicación mediante pipeline
  sólo después de pruebas, F0 y F1; no se publican salidas parciales.

Se conservan García de once filas; 224→225→226, 3454→3455, 2695→2696, 2754→2755,
2790→2791, 1386→1387, 2673→2674, 2863→2864, 2796→2797, 2707→2708, 2963→2964,
2680→2681, 4745→4746, 6561→6562 y 5003→5004, además de las 14 continuidades de LOOP28.
**3572 reanudación 235 sigue separada; 5402→5403 y 600→601 no se restauran.**
Las fichas institucionales601/3110, el archivo de la pausa y los retornos 3044/4476/4926
siguen intactos. Los demás controles se preservan mediante pruebas y comparación,
sin afirmar relectura de todos en esta pasada.

### Histórico 783: un aviso residual adicional

Se mantienen todos los estados principales y tipos de revisión. Hay **un único cambio
no secuencial** en el CSV histórico: intervalo original **4715**, padre **3340**, incorpora
`TEXTO_DANADO_POR_COTEJAR` en `Alertas_Actuales`. Por eso los intervalos históricos con
alertas actuales aumentan de **284 a 285**, sin perder su corrección de hablante previa.
Los otros cambios del CSV son `IDs_Actuales` por la renumeración.

Siguen **102 pendientes contextuales**,497 comparaciones, 183 lecturas dirigidas y 103
triajes; seis intervalos con variante de identidad y **21 filas actuales** de variantes.
Las ocho menciones históricas no son las 53 actuales. El estado principal no cierra
los motivos residuales y las unidades superpuestas no se suman.

## Descubrimiento y límites

Dos barridos produjeron **25 ventanas nominales y 25 de predicados**; un filtro de
transiciones procedimentales produjo **3 candidatos**. Son resultados superpuestos,
no 53 lecturas ni una muestra representativa. El primero aportó referencias; el segundo
localizó el cierre 2706. La lectura completa de sus vecinos permitió identificar la
opinión presidencial2705. El último filtro distingue la transición de sesión de los
usos económicos de «da paso» en 3340/5584.

Se leyeron **19 padres completos y una cabecera**:649, 1298, 1379, 1930, 1941, 2058, 2201,
2206, 2220, 2705, 2706, 2707, 2853, 3340, 3570, 4193, 4910, 4989, 5584; cabecera 2689.
Se registraron fichas en **17 padres**, porque 1298/1379 se superponen entre lecturas y
avisos. 2707 y 5584 son controles completos sin nueva ficha. No son 19 resegmentaciones.

Quedan **57 lecturas actuales = 53 legítimas + 4 pendientes**: 6185/Bernier,
3775/Cerda, 4055/conjunto-institucional y 2510/conjunto. No se reparten arbitrariamente
pasajes conjuntos ni se convierten en problemas de OCR por defecto. Siguen nombres,
cargos, puente de 780, reserva textual de 6119 y los demás pendientes anteriores.

**Sin nuevo cotejo PDF ni muestra independiente con/sin alertas.** Identificar una voz
no certifica el OCR; la extensión de una exposición no es daño. Verificaciones locales,
sin afirmar CI remota. El workflow preexistente permanece fuera del PR. No queda proceso
activo. Al recuperar el entorno se comprobó que todos los archivos coincidían con el
commit publicado de LOOP29 antes de restaurar únicamente el seguimiento de Git; no se
sobrescribieron archivos para preparar la comparación.

## Archivos

- [Base final](../data/processed/consolidado_base_referencia_final.xlsx)
- [Auditoría](../data/processed/consolidado_base_referencia.xlsx)
- [Comparación global y cinco padres antes/después](comparacion_loop30_2026-09-08.json)
- [Detalle CSV](cambios_loop30_2026-09-08.csv)
- [Checkpoint](estado_revision_loop30_2026-09-08.json)
- [Pruebas LOOP30](../tests/test_loop30_review.py)
- [Informe anterior LOOP29](REVISION_LOOP29_2026-09-08.md)
