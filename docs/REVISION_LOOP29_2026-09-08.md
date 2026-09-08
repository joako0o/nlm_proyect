# LOOP29 — Respuestas nominales dentro de párrafos y retorno al expositor

**Fecha:** 2026-09-08. **PR:** [#3](https://github.com/joako0o/nlm_proyect/pull/3).
**Base congelada:** LOOP28, commit `f4a258046816b8cd54db1e954dc5d9e71b01636d`.

## Resultado

Se separan **tres respuestas identificables dentro de tres padres antes sin alerta**:
García en 2931, Vergara en 3044 y Soto en 5003. Se conserva el retorno explícito de Marfán
en 3044 y se documenta **un enlace 5003→5004** para no fragmentar la exposición de Soto.
Además, se registran **dos menciones legítimas** y **una advertencia textual en 3045**.

**1.613 pruebas pasan (+38)**. Pipeline completo, F0/F1 y comparación global pasan;
ensayo aislado y publicación son idénticos celda a celda. No se retira ningún enlace
preexistente ni se pierde texto. Los controles no certifican pureza semántica exhaustiva.

| Unidad | LOOP28 | LOOP29 |
|---|---:|---:|
| Padres de origen | 7.219 | 7.219 |
| Filas físicas / bloques | 9.683 / 9.682 | 9.687 / 9.686 |
| Grupos de turno | 9.250 | 9.253 |
| Grupos multifila / máximo de filas | 337 / 11 | 338 / 11 |
| Filas alertadas / padres alertados | 451 / 381 | 455 / 385 |
| Intervalos personales / padres con revisión | 377 / 348 | 380 / 351 |
| Advertencias contextuales | 73 | 74 |
| Fichas de continuidad revisada | 23 | 24 |
| Lecturas actuales legítimas / pendientes | 37 / 4 | 39 / 4 |
| Documentos / registros institucionales | 12 / 2 | 12 / 2 |
| Archivos de advertencias retiradas | 3 | 3 |
| Pruebas de regresión | 1.575 | 1.613 |

## Separaciones aplicadas

Las longitudes corresponden a la exportación. Cada registro incluye hash del padre,
offsets del texto crudo, cita inicial, justificación y evidencia del padre, vecinos y
nómina de esa sesión. No se calculan offsets a partir de las longitudes normalizadas.

### 2931 — García responde a Marshall

**Antes:** García 310 → Marshall 415.

**Ahora:** García 310 → Marshall 172 → García 242.

Marshall consulta por los cambios metodológicos del IPC. **«afirmando el señor Pablo
García que»** introduce la respuesta afirmativa y la explicación sobre la similitud de
los documentos del INE. La consulta no se atribuye a García y la respuesta no se deja
dentro de Marshall. El primer aporte de García permanece separado de su respuesta:
no se salta la intervención intermedia por coincidir el nombre.

Se leyeron completos 2930–2932 y la cabecera2889. La nómina identifica a Pablo García
como Gerente de División de Estudios. No se introduce un alias ni se reescribe el texto.

### 3044 — Réplica de Vergara y retorno de Marfán

**Antes:** Marfán 499.

**Ahora:** Marfán 135 → Vergara141 → Marfán 221.

**«replicando el señor Vergara que»** delimita la precisión de Rodrigo Vergara sobre
la política transitoria de PPM del año anterior. En esta sesión Vergara es Consejero,
no Presidente. La frase **«El señor Marfán agrega»** inicia el retorno explícito del
Vicepresidente Marfán sobre ingresos estructurales y compensación en la operación renta.

El intervalo revisado termina antes de ese retorno. Marfán 221 conserva fuente
`SUJETO_NOMBRE`, ancla propia y grupo distinto, no heredado de la réplica de Vergara.
Se leyeron completos 3043–3045 y la cabecera3023.

### 5003 — Respuesta de Soto al Presidente

**Antes:** Vergara411.

**Ahora:** Vergara130 → Soto 280.

El Presidente comenta la baja del gas. **«consignando el señor Claudio Soto que»**
introduce la explicación sobre el perfil de la gasolina y el alcance de la baja de
precios de Metrogas. La respuesta deja de atribuirse al Presidente.

Se mantiene literalmente **«A continuación,.»** al final del tramo de Soto: no se
elimina ni se completa. Es una reserva textual pendiente de cotejo, sin nuevo aviso
bloqueante y sin certificar integridad del OCR.

### 5003→5004 — Misma exposición, sin incluir al Presidente

Se enlaza únicamente **Soto 280 → Soto 2849**. El comentario presidencial130 queda fuera.
El siguiente padre comienza nominalmente con Soto y continúa con alimentos, inflación,
expectativas y tasas. **5002/5703 y 5004/2849 permanecen completos**, sin cortes por extensión.
Se leyeron íntegros 5002–5004 y la cabecera4974.

La respuesta revisada280 permanece **sin ancla global**. 5004 conserva su ancla explícita
propia y registra como antecedente la respuesta inmediata. La continuidad requiere
una ficha exacta con hashes; sin ella no se establece el enlace. No se fusionan filas.

## Implementación acotada, no ampliación automática

Se agrega el tipo de revisión **`GERUNDIO_RESPUESTA_VARIANTE_REVISADA`**, exclusivamente
para fichas individuales con hash y evidencia. Admite estos tres predicados:

- `afirmando` → proyección `afirma`;
- `replicando` → proyección `responde`;
- `consignando` → proyección `consigna`.

Las proyecciones sólo permiten validar el sujeto nominal. **El texto exportado sigue
diciendo afirmando, replicando y consignando.** Se exige separador anterior, sujeto
nominal compatible, declaración con «que» y ausencia de cita abierta. Un cargo sin
nombre no basta para este tipo. Los modos antiguos no se amplían a estos predicados.

No cambia `turns.py`, no se añade «replica» al detector automático, no se alteran los
motores de continuidad ni se convierte `CONTEXTO_REVISADO` en ancla. Sin ficha no hay
nuevo corte. Se mantienen los bloqueos por texto, fecha, actor, fuente, citas y alertas.

## Menciones y daño: unidades distintas

### Dos nuevas lecturas legítimas

- **1142, Marfán 424:** compara su pregunta con lo que está preguntando el Vicepresidente.
  La relativa pertenece a su explicación; no es una intervención nueva del Vicepresidente.
- **1370, Desormeaux509:** compara la discusión estadounidense con la que está anticipando
  Magendzo. Es una referencia, no una toma de palabra intercalada. Se conserva «ios».

Ambos padres se leyeron completos. No cambian texto, actor, cargo, segmentación ni
alertas. Las fichas se validan contra sus intervalos exactos; al no haber alerta,
**no aparecen en `revision_pendientes.csv`**.

Se releyó además **2219 completo**: Marfán 786 → Presidente 297, con referencia a lo que
«está señalando» Marfán. Su lectura legítima previa permanece idéntica; no se duplica
la ficha ni se cuenta como una tercera lectura nueva.

### 3045: una nueva advertencia textual

Se conserva el desarrollo completo de **Claro 461**, sin reasignación ni corte.
**«bottom fine», «ser- 1,2%», «Yque» y «Oy -1,2%»** son aparentes confusiones o empalmes
que quedan señalados para cotejo como `TEXTO_DANADO_POR_COTEJAR`.

No se reconstruyen letras, signos ni cifras ni se atribuye un origen confirmado al
daño. El sujeto nominal identifica a Claro; la advertencia no inventa otra voz ni
resuelve la integridad del texto. No se pierde una continuidad previa por este aviso.

### Por qué aumenta la cola

Se conservan las 451 filas previamente alertadas, salvo la renumeración de IDs.
Se agregan **cuatro filas**, no cuatro advertencias contextuales:

1. Marshall 172 de 2931: coma final conservada, `FINAL_SIN_PUNTUACION`.
2. Marfán 135 de 3044: coma final conservada, `FINAL_SIN_PUNTUACION`.
3. Presidente 130 de 5003: coma final conservada, `FINAL_SIN_PUNTUACION`.
4. Claro 461 de 3045: la nueva advertencia contextual de daño.

Los intervalos de respuesta identificados no convierten las comas anteriores en puntos.
Tampoco se borran duplicados o restos de página para reducir la cola. Las alertas no
son un conteo de errores confirmados; su ausencia no certifica revisión humana.

## Verificación global

La comparación se realizó sobre las **9.687 filas actuales y los 7.219 padres**, contra
la entrega LOOP28 congelada, no sólo sobre los tres casos corregidos.

- **Todo el texto de origen conservado**, ignorando sólo espacios:2.048.560 palabras.
  Tres padres cambian segmentación; ningún padre pierde contenido.
- **Cinco padres cambian celdas no secuenciales:**2931, 3044, 5003 por segmentación;
  3045 sólo por advertencia;5004 sólo por relación/antecedente de continuidad.
  **7.214 padres conservan esas celdas.** Se excluyen sólo `ID` e `ID_Turno` secuenciales.
- El único enlace nuevo es5003→5004. **Todos los enlaces preexistentes se conservan**,
  incluidos los 23 revisados. Grupos fuera de correcciones/enlace/advertencia idénticos
  por sus miembros, sin confundir renumeración con cambio discursivo.
- Permanecen íntegros los **377 intervalos personales, 73 advertencias, 41 lecturas,
  23 fichas de enlace, 12 documentos, 2 registros institucionales y 3 archivos de retiros**
  anteriores. No se sobrescribe ninguna ficha previa.
- **83 hashes de entradas/código y 11 de salidas verificados**. Fuentes originales,
  fórmulas revisadas y detector automático conservan sus hashes. Esquemas37/24,
  21 fórmulas, 310 contrastes TPM, 132 sesiones y 55 etiquetas de actor conservados.
- TPM y documentos comparados salvo IDs de evidencia/documento/turno. No cambia el
  contenido sustantivo ni se agrega un documento. Autor ≠ lector ≠ asistencia.
- Las 451 filas anteriores de la cola conservan todos sus campos salvo IDs secuenciales.
  El histórico783 conserva estados y tipos de revisión;284 intervalos siguen con alertas.
- Ensayo aislado y publicación idénticos celda a celda. Publicación ejecutada mediante
  `scripts/preparar_data.py` después de pasar pruebas y ambos controles.

Siguen García de once filas;224→225→226, 3454→3455, 2695→2696, 2754→2755, 2790→2791,
1386→1387, 2673→2674, 2863→2864, 2796→2797, 2707→2708, 2963→2964, 2680→2681,
4745→4746 y 6561→6562. También las 14 continuidades de LOOP28, incluida3571→3572
**sin cruzar a la reanudación 235**. **5402→5403 y 600→601 no se restauran.**
Las fichas de 601/3110, la pausa archivada, los documentos y los retornos 4926/4476
siguen intactos. Los demás controles se preservan mediante pruebas y comparación,
sin afirmar relectura de todos ellos en esta pasada.

## Descubrimiento, alcance y pendientes

Se reutilizaron resultados exploratorios de LOOP27 como orientación, sin contarlos
como nuevas lecturas. El barrido actual produjo **261 ventanas nominales**, un filtro
específico de gerundios con nombre produjo **5 coincidencias** y otro de gerundios con
cargo produjo **4**. Son unidades superpuestas, con referencias y registros de
asistencia: **no se suman como 270 casos revisados**. En los filtros específicos,
los tres cambios nominales se distinguen de referencias como «está anticipando» y
«está señalando». Los candidatos no se adjudicaron automáticamente.

Se leyeron **12 padres completos**, además de **tres cabeceras completas**:
1142, 1370, 2219, 2930, 2931, 2932, 3043, 3044, 3045, 5002, 5003, 5004;
cabeceras 2889, 3023, 4974. No se afirma lectura íntegra de todas las ventanas del barrido.

Quedan **43 lecturas actuales = 39 legítimas + 4 pendientes**: 6185/Bernier,
3775/Cerda, 4055/conjunto-institucional y 2510/conjunto. No se reparten arbitrariamente
pasajes conjuntos ni se confunde delimitación de voz con identidad desconocida o daño.
Siguen las reservas anteriores, incluidos los nombres/cargos, el puente de 780 y
el empalme interior de 6119 documentado en LOOP28.

Histórico783: **102 pendientes contextuales**, 497 comparaciones, 183 lecturas dirigidas
y 103 triajes; seis intervalos con variante de identidad y **21 filas actuales** de
variantes pendientes. Las ocho menciones históricas no son las 39 actuales. Las unidades
se superponen; el estado principal no cierra los motivos residuales.

**Sin nuevo cotejo PDF ni muestra independiente con/sin alertas.** F0/F1 no establecen
pureza total y una exposición larga no está dañada por su extensión. Verificaciones
locales, sin afirmar CI remota. El workflow preexistente queda fuera del PR.
No queda proceso activo.

## Archivos

- [Base final](../data/processed/consolidado_base_referencia_final.xlsx)
- [Auditoría](../data/processed/consolidado_base_referencia.xlsx)
- [Comparación global y cinco padres antes/después](comparacion_loop29_2026-09-08.json)
- [Detalle CSV](cambios_loop29_2026-09-08.csv)
- [Checkpoint actualizado](estado_revision_loop29_2026-09-08.json)
- [Pruebas LOOP29](../tests/test_loop29_review.py)
- [Informe anterior LOOP28](REVISION_LOOP28_2026-09-08.md)
