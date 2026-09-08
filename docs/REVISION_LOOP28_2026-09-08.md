# LOOP28 — Continuidades acotadas sin fragmentar exposiciones

**Fecha:** 2026-09-08. **PR:** [#3](https://github.com/joako0o/nlm_proyect/pull/3).
**Base congelada:** LOOP27, commit `becd417800dd42ca86c70d9770334ad600b1c2bc`.

## Resultado

**14 enlaces de continuidad documentados entre 28 padres leídos completos**, incluidas
las otras voces y partes institucionales de esos padres. Además, **tres revisiones de
menciones legítimas**, superpuestas a ese mismo conjunto de padres.

Esta pasada **no añade cortes ni adjudicaciones de voz**: corrige la trazabilidad de
intervenciones ya separadas que continúan inmediatamente. No fusiona filas físicas,
no reescribe OCR y no transforma `CONTEXTO_REVISADO` en ancla general. El parser,
el motor de continuidad y los demás scripts de producción permanecen idénticos.

**1.575 pruebas pasan**, 61 más que LOOP27. Pipeline completo, F0/F1 y comparación
global pasan. Ensayo aislado y publicación tienen las mismas filas y celdas.
F0/F1 no certifican pureza semántica ni integridad textual exhaustivas.

| Unidad | LOOP27 | LOOP28 |
|---|---:|---:|
| Padres de origen | 7.219 | 7.219 |
| Filas físicas / bloques de texto | 9.683 / 9.682 | 9.683 / 9.682 |
| Grupos de turno | 9.264 | 9.250 |
| Grupos con varias filas | 323 | 337 |
| Máximo de filas en un grupo | 11 | 11 |
| Filas con alertas / padres alertados | 451 / 381 | 451 / 381 |
| Intervalos personales / padres con revisión | 377 / 348 | 377 / 348 |
| Pruebas de enlace revisado | 9 | 23 |
| Lecturas actuales legítimas / pendientes | 34 / 4 | 37 / 4 |
| Advertencias contextuales | 73 | 73 |
| Documentos / registros institucionales | 12 / 2 | 12 / 2 |
| Archivos de advertencias retiradas | 3 | 3 |
| Pruebas de regresión | 1.514 | 1.575 |

## Los catorce enlaces

Las longitudes siguientes corresponden a **cada extremo en la exportación**, no al
padre completo ni a los límites en el texto crudo. Las fichas conservan offsets,
hashes de ambos padres y citas completas de ambos. Sólo enlazan el último tramo
del padre anterior con el primero del siguiente.

| Enlace | Actor | Caracteres de extremos | Evidencia y límites |
|---|---|---:|---|
| 121→122 | Rodrigo Valdés | 3940→1146 | Puntos 5–9 de opciones de política seguidos de 10 «Lo anterior» y 11 «Finalmente». Misma enumeración y exposición. |
| 727→728 | Rodrigo Valdés | 61→9505 | Anuncio de lo que informa el Gerente, tras invitación nominal, seguido del informe completo. Corbo, la reanudación institucional y la invitación permanecen aparte. |
| 2027→2028 | Claudio Soto | 65→700 | Confirmación y desarrollo de la composición del empleo. Desormeaux153 queda fuera. |
| 2838→2839 | José De Gregorio | 1702→746 | Argumentación presidencial sobre política no convencional y voto. Marfán2324 anterior y Consejo1698 posterior quedan separados. |
| 2911→2912 | Claudio Soto | 43→1895 | Respuesta y retorno explícito a la presentación. Vergara121 no se incorpora; la respuesta conserva `FRAGMENTO_BREVE`. |
| 2918→2919 | Claudio Soto | 215→1195 | Confirmación del cálculo y «un segundo punto» de la exposición. Presidente59 queda aparte, con su coma final y alerta; no se traslada esa coma a Soto. |
| 3123→3124 | Manuel Marfán | 57→6514 | Agradecimiento al equipo y desarrollo completo de su voto. Marshall5484, Presidente108 y el siguiente Presidente861 quedan fuera. |
| 3571→3572 | José De Gregorio | 390→102 | Cierre de discusión seguido del anuncio de suspensión. **La reanudación235 posterior NO pertenece al enlace**, aunque sea el mismo Presidente. |
| 4470→4471 | Sergio Lehmann | 43→2763 | Confirmación y continuación con el Heat Map. Vergara132 queda fuera; la confirmación conserva `DUPLICADO_NO_FORMULA`. |
| 4903→4904 | Sergio Lehmann | 462→1799 | Respuesta sobre expectativas de la Reserva Federal y retorno a la presentación. Vergara166 queda separado. |
| 5168→5169 | Sergio Lehmann | 178→422 | Corroboración del trimestre presentado y continuación con inflación. Marfán187 permanece separado. |
| 5872→5873 | Claudio Soto | 114→3346 | Respuesta sobre existencias y continuación con sectores, demanda y empleo. Marfán127 no se incorpora. |
| 6118→6119 | Sergio Lehmann | 839→10817 | Respuesta sobre capitalización bancaria, cierre bursátil y continuación explícita de la exposición. Claro490 queda separado. Reserva textual descrita abajo. |
| 6394→6395 | Sergio Lehmann | 2286→14541 | Noticias internacionales y continuación explícita con mercados financieros. Los mandatarios y políticos extranjeros referidos no toman la palabra en la sesión. |

En todos los casos el extremo anterior sigue **sin ancla propia**; el siguiente
conserva su **ancla explícita propia** y registra como antecedente el tramo inmediato.
Sin la ficha exacta no se establece el nuevo enlace. Las barreras por cambios de
sesión, voz, texto, fuente o alertas pendientes siguen funcionando.

### Suspensión y reanudación: 3571/3572

No se une toda la fila de origen 3572 al discurso previo. El cierre390 y el anuncio
de suspensión102 comparten grupo hasta la suspensión. La reanudación235 abre otro
grupo, conserva ancla propia y no hereda antecedente a través de la pausa. Es una
prueba explícita contra la inferencia «misma persona = mismo turno».

### Menciones, no voces nuevas

Se añaden tres lecturas exactas al registro de menciones:

- **2839, Presidente746:** referencia a lo indicado por el Ministro de Hacienda
  Subrogante dentro del voto presidencial. El acuerdo posterior pertenece al Consejo.
- **3124, Marfán6514:** noticias del Ministro de Hacienda y referencias a las opiniones
  de las autoridades fiscales dentro del desarrollo de Marfán. No se inventa una
  intervención ministerial intermedia ni se recorta la exposición.
- **6394, Lehmann2286:** Mario Draghi, Emmanuel Macron y Marina Silva aparecen como
  personas de las noticias internacionales, no como participantes actuales ni alias
  del Presidente del Banco Central de Chile.

Esas tres filas no tenían alertas y siguen sin ellas. Las lecturas se validan contra
texto, actor y límites en el registro; **no aparecen en `revision_pendientes.csv`**.
No cambian voces, cargos ni la segmentación y no cierran otros motivos.

## OCR literal y reservas abiertas

Se conserva **«V A juicio»** en 6118. En 6119 queda literalmente el empalme
**«procesos equivalentes en Al continuar»**, que aparenta falta de texto. Se documenta
como reserva pendiente de cotejo dentro de la ficha de continuidad: **no se crea
una nueva alerta contextual, no se resuelve el daño y no se inventan palabras**.
La identificación de Lehmann y la continuidad inmediata se sostienen en la respuesta
y el retorno nominal, no en una reconstrucción de ese pasaje interior.

En 6394/6395 se mantienen **«PIS», «1O» y «mo erada»**. Tampoco se corrigen la coma
presidencial de 2918, los fragmentos breves o las repeticiones de 4470 para reducir la
cola. Voz identificada y texto íntegro son cuestiones distintas. No se conoce el
origen del aparente daño sin cotejar la fuente. **La extensión no es daño.**

## Comparación global y preservación

La comparación abarca las **9.683 filas y los 7.219 padres**, no sólo los candidatos:

- **Texto literal de cada fila idéntico a LOOP27.** También son idénticos los actores,
  cargos, métodos/fuentes, alertas, duplicados, anclas, IDs físicos, bloques y límites.
  Se conserva todo el origen ignorando sólo espacios: **2.048.560 palabras**.
- Sólo cambian `Relacion_Turno` e `ID_Antecedente_Continuidad` en **14 extremos
  siguientes**, además de la numeración `ID_Turno` que se deriva de los nuevos grupos.
  **7.205 padres conservan todas sus celdas no secuenciales.**
- Los **14 extremos anteriores** sólo cambian su membresía lógica y, en algunos casos,
  la numeración del turno. Son **28 padres alcanzados por enlaces**, no14 padres
  resegmentados. **7.191 padres quedan fuera de los enlaces** y sus grupos se conservan.
- Se añaden exactamente los **14 enlaces declarados**. **No se retira ningún enlace
  preexistente**, revisado o automático. Los grupos fuera del alcance son idénticos
  por sus miembros, sin confundir renumeración con cambios de continuidad.
- Las **9 fichas previas de continuidad, 377 intervalos personales, 73 advertencias,
  38 lecturas, 12 documentos, 2 registros institucionales y 3 archivos de retiros**
  permanecen íntegros. Las nuevas entradas se agregan sin sobrescribir las anteriores.
- Se verifican **82 hashes de entradas/código y 11 de salidas**. Todos los scripts de
  producción, fuentes de origen y fórmulas revisadas conservan sus hashes de LOOP27.
  Esquemas **37/24**, **55 etiquetas de actor**, **132 sesiones**, **21 fórmulas** y
  **310 contrastes TPM** se mantienen.
- `decisiones_tpm.csv` es idéntico. Los doce documentos y la cola de 451 filas conservan
  todos sus campos salvo `ID_Turno`. Ninguna alerta desaparece por registrar una lectura.
- Ensayo aislado y publicación son idénticos celda a celda. La publicación se ejecutó
  mediante el pipeline, después de pruebas, F0 y F1; no se publicaron salidas parciales.

Persisten García de once filas y los enlaces224→225→226, 3454→3455, 2695→2696,
2754→2755, 2790→2791, 1386→1387, 2673→2674, 2863→2864, 2796→2797, 2707→2708,
2963→2964, 2680→2681, 4745→4746 y 6561→6562. **5402→5403 y 600→601 no se restauran**.
El archivo de la interrupción de 601, las revisiones de 3110 y los retornos explícitos
4926/4476 permanecen intactos. Autor documental ≠ lector ≠ asistencia; no hay documentos
nuevos ni reatribución de las opiniones leídas. Todos los demás controles anteriores
siguen cubiertos por sus pruebas y la comparación global, sin afirmar que se releían.

## Alcance de la revisión y pendientes

El descubrimiento buscó extremos contiguos, de igual actor/fecha, con atribución
revisada a la izquierda y explícita a la derecha, grupos distintos y sin barreras
incompatibles. Produjo **14 parejas candidatas**; se leyeron todas las partes de sus
**28 padres**. La decisión de registrar cada enlace fue posterior a esa lectura,
no una promoción automática del filtro. Es un barrido dirigido, **no una muestra
representativa ni una revisión integral del corpus**.

No se suman las tres lecturas de menciones a los 28 padres como si fueran31 casos.
Tampoco se cuentan las catorce fichas nuevas como catorce voces recuperadas.

Quedan **41 lecturas actuales: 37 legítimas y 4 pendientes**: 6185/Bernier,
3775/Cerda, 4055/conjunto-institucional y 2510/conjunto. No se reparten arbitrariamente
sus intervenciones ni se convierten en problemas de OCR por defecto. Siguen los
pendientes de nombres/cargos, el puente ambiguo de 780 y las demás reservas anteriores.

Histórico783 sin cambios de estado: **102 pendientes contextuales**, 497 comparaciones,
183 lecturas dirigidas y 103 triajes; **284 intervalos históricos con alertas actuales**,
seis intervalos con variante de identidad y **21 filas actuales** de variantes.
Las ocho menciones legítimas históricas no son las 37 actuales; las unidades se
superponen y el estado principal no cierra los motivos residuales.

**Sin nuevo cotejo PDF ni muestra independiente con/sin alertas.**
Verificaciones locales; no se afirma ejecución remota de CI. El workflow preexistente
permanece fuera del PR. No queda proceso activo.

## Archivos

- [Base final](../data/processed/consolidado_base_referencia_final.xlsx)
- [Base de auditoría](../data/processed/consolidado_base_referencia.xlsx)
- [Comparación global, extremos antes/después y nuevas fichas](comparacion_loop28_2026-09-08.json)
- [CSV de los 28 padres, con todas sus partes antes/después](cambios_loop28_2026-09-08.csv)
- [Checkpoint actualizado](estado_revision_loop28_2026-09-08.json)
- [Pruebas específicas](../tests/test_loop28_review.py)
- [Informe previo LOOP27](REVISION_LOOP27_2026-09-08.md)
