# LOOP31 — Asistencia distinta de habla y revisión de referencias

**Fecha:** 2026-09-08. **PR:** [#3](https://github.com/joako0o/nlm_proyect/pull/3).
**Base congelada:** LOOP30, commit `550ed89f009baf8250d0567dbb715f119bccc203`.

## Resultado y unidades

**Dos padres resegmentados para separar hechos del acta de palabras personales**,
ambos antes sin alerta. No son dos voces personales nuevas. Se agregan **20 fichas de
referencias legítimas y cuatro advertencias textuales**; se releen otras tres fichas
sin duplicarlas. Se preservan las exposiciones largas y todos los enlaces anteriores.

**1.704 pruebas pasan (+52)**, además del pipeline completo, F0/F1 y la comparación
global. Ensayo aislado y publicación idénticos celda a celda. F0/F1 no certifican
pureza semántica exhaustiva ni integridad textual.

| Unidad | LOOP30 | LOOP31 |
|---|---:|---:|
| Padres de origen | 7.219 | 7.219 |
| Filas físicas / bloques de texto | 9.689 / 9.688 | 9.691 / 9.690 |
| Grupos de turno | 9.255 | 9.257 |
| Grupos multifila / máximo de filas | 338 / 11 | 338 / 11 |
| Filas con alertas / padres alertados | 459 / 389 | 462 / 392 |
| Intervalos personales revisados / padres | 382 / 353 | 382 / 353 |
| Registros institucionales | 2 | 4 |
| Advertencias contextuales | 77 | 81 |
| Lecturas actuales legítimas / pendientes | 53 / 4 | 73 / 4 |
| Fichas de continuidad / documentos / archivos de retiros | 24 / 12 / 3 | 24 / 12 / 3 |
| Intervalos históricos con alertas actuales | 285 | 285 |
| Pruebas | 1.652 | 1.704 |

## 1. Separaciones entre acta y discurso

Las longitudes siguientes son caracteres de la exportación, no offsets crudos.
Cada ficha congela padre, antecedente inmediato y evidencia por fecha/hash; incluye
la partición completa esperada. Se leyeron también los vecinos posteriores y nóminas.

### 4788 — Llegada de Larraín después de la votación

**Antes:** Vergara 2245 → Larraín 161 → Vergara 333.

**Ahora:** **Vergara 2132 → acta de llegada 112** → Larraín 161 → Vergara 333.

La oración **«A continuación, y siendo las 16:25 horas, se incorpora a la Sesión el
Ministro de Hacienda señor Felipe Larraín.»** describe un hecho de asistencia. No es
parte del voto presidencial ni una intervención del Ministro. Sus excusas reales,
introducidas por «El señor Ministro presenta sus excusas», ya estaban separadas y
siguen como habla de Larraín. El Presidente luego informa la decisión y le da la palabra.

Se conserva íntegro el voto previo de Vergara y la exposición posterior de **Larraín
8541 en 4789**. Se leyeron completos 4787–4789 y la cabecera 4733. La aparición de
Larraín en una nómina no se usa para inferir presencia durante toda la sesión.

El pie **«Sesión N° 184 Página 23 de 26»** queda al final de Vergara 2132. Ahora genera
`FINAL_SIN_PUNTUACION`: no se elimina, no se agrega un punto ni se traslada a la llegada
para ocultar el aviso. La decisión TPM de la sesión se conserva.

### 6808 — Retiro de Valdés y Soto, no intervención conjunta

**Antes:** Valdés 633 → acta/comunicado 1940.

**Ahora:** **Valdés 518 → acta de retiro 114** → acta/comunicado 1940.

Se separa **«El Ministro de Hacienda señor Rodrigo Valdés y su Asesor, el señor Claudio
Soto, se retiran de la Sala de Consejo.»**. No son palabras de Valdés ni de Soto, ni
una intervención conjunta que deba repartirse entre ambos.

La pregunta que Valdés deja planteada antes de retirarse conserva sus **518 caracteres**
y su sujeto explícito. El comunicado siguiente conserva sus **1940 caracteres**, su
tipo `ACUERDO_CONSEJO` y un grupo distinto del retiro. La bienvenida de Vergara en
6807 no se transforma en habla de Valdés. La aprobación y cierre en 6809 permanecen.
Se leyeron 6807–6809 y la nómina 6755.

### Implementación limitada a fichas individuales

El nuevo alcance **`MOVIMIENTO_ASISTENTES_REVISADO`** reside en el registro institucional,
no en el de hablantes. Sólo admite las dos formas literales constatadas, con límites,
conservación del padre y controles de cita abierta y separador anterior. La segmentación
nativa de los fragmentos anteriores/posteriores debe coincidir con las voces y límites
congelados; no se adjudican esas voces por una tabla sin comprobación.

La nota de revisión aparece **sólo en el movimiento**, no en todos los tramos del padre.
Llegada y retiro usan `ACTA/META` y `ACTA_INSTITUCIONAL`, sin ancla ni antecedente de habla.
El retorno de Vergara y las excusas de Larraín conservan anclas explícitas propias.

**No cambia el detector automático ni los motores de continuidad.** No regla global
para «se incorpora» o «se retiran», ni para «antes de retirarse», que en 6808 sigue
introduciendo una pregunta personal. No modifica las fichas 601/3110 ni generaliza el
tratamiento al pasaje ambiguo 4055. `CONTEXTO_REVISADO` no crea anclas globales; Fin solo
no corta ni ancla. Autor documental ≠ lector ≠ asistencia: no se agregan documentos.

## 2. Veinte fichas nuevas de referencias legítimas

Todos los padres fueron leídos completos. Cada ficha delimita un intervalo, sin cambiar
su actor, texto, segmentación o alertas. Los complementos y las respuestas ya separadas
se mantienen: el gerundio posterior a una mención no se presta al actor mencionado.

| Padre | Intervalo | Lectura documentada |
|---|---|---|
| 202 | Corbo 767 | Anuncio de incorporación futura de Wagner e invitación a Pérez; no habla de los invitados ni del Presidente de la República referido. García 11028 y Corbo 88 separados. |
| 410 | De Ramón 558 | García cerró información antes de la reunión: referencia temporal, no cierre de sesión ni habla actual de García. |
| 953 | Lehmann 1024 | Responde a Desormeaux; «señalando» sigue atribuido a Lehmann. |
| 1273 | Corbo 165 | Se evaluará el tema planteado por Marfán; no nuevo turno del Consejero. |
| 2499 | Desormeaux 6880 | «en opinión del señor Ministro» está subordinado al argumento sobre la Minuta, no abre una intervención ministerial. |
| 2564 | De Gregorio 311 | Coincide con Marfán y pide explicación a De Ramón. La respuesta 688 ya está separada. |
| 2608 | Lehmann 252 | Concuerda con Velasco; se preservan seis tramos y su retorno revisado 2323. |
| 2701 | Marshall 838 | Coincide con Claro. Soto, Claro, Cowan y Marfán conservan sus tramos; aviso textual sólo para Soto. |
| 2743 | Desormeaux 169 | García mencionaba algo la semana anterior. Respuesta ministerial 69 separada; coma final y alerta conservadas. |
| 3059 | Claro 754 | Comparte la inquietud de Marfán; «manifestando» corresponde a Claro. |
| 3286 | Céspedes 500 | Las perspectivas mencionadas por Claro «indican», no Claro como hablante. Marshall 284 y Lehmann 1547 separados. |
| 3615 | Vicuña 565 | Complementa a Soto; «señalando» corresponde a Vicuña. Soto 198 y retorno 946 conservados. |
| 5078 | Herrera 623 | Complementa a Lehmann sobre QE3. Anuncio 286 y exposición de Lehmann 1926 separados; no documento personal por distribuir información de la FED. |
| 6353 | Vial 1904 | Complementa a García y refiere análisis externos sobre China/cobre. No voces de analistas citados. |
| 6402 | Vergara 736 | Referencias a Claro/García y a Marina Silva/Dilma Rousseff. «la señora Silva» no es Pablo García Silva. Sin modificación global de alias. |
| 6669 | Claro 703 | Complementa a Marshall; «destacando» mantiene a Claro. |
| 6891 | Fuentes 275 | Complementa a Naudon; «precisando» mantiene a Fuentes. |
| 6935 | Naudon 413 | Complementa a Fuentes; «mencionando» mantiene a Naudon. |
| 7124 | Naudon 1348 | Complementa a Vergara; «haciendo notar» mantiene a Naudon. Vergara 1413 anterior y retorno 192 con sujeto propio. |
| 7175 | Naudon 776 | Se suma a Vergara sobre Brasil; Marcel 350 posterior permanece separado. |

**Sólo dos fichas nuevas aparecen en la cola:** 202, junto con su aviso textual, y
2743, junto con la coma final. Las otras 18 no corresponden a intervalos alertados.
2701/5078 sí tienen avisos en el padre, pero **en otros intervalos**, no en los de las
nuevas lecturas. No se confunden filas, padres ni motivos.

### Tres relecturas, sin duplicar fichas

- **1338 / Jadresic 3316:** relectura íntegra del padre y de la referencia a Magendzo.
  La pausa/reanudación y el retorno de Corbo siguen separados. Ficha anterior intacta.
- **3147 / De Ramón 900:** relectura íntegra del padre; la información considerada por
  Lehmann no lo convierte en autor de «piensa». La ficha de mención previa se conserva
  y se agrega sólo un aviso textual independiente.
- **5658 / Vial 477:** el Presidente referido es el del Banco Central de Reserva de
  Perú, según relata Vial. No se le adjudica una voz local ni se cierra un alias global.
  Ficha anterior intacta.

Por tanto, son **20 lecturas registradas nuevas + 3 relecturas**, no 23 fichas nuevas.

## 3. Cuatro advertencias textuales, sin reconstrucción

| Padre / intervalo | Motivo conservado para cotejo |
|---|---|
| 202 / Corbo 767 | Cabecera 201: 7 de abril de 2005; el tramo fija una sesión del 11 de octubre de 2005 y contiene un encabezado de octubre. Aparente discordancia de calendario/composición. No se decide cuál fecha corresponde ni se altera `Fecha`. |
| 2701 / Soto 3144 | «hace prensar» y «la calda en el consumo», entre otros términos dudosos. No sustituir palabras ni extender a los otros cuatro actores. |
| 3147 / De Ramón 900 | «AA Dado eso» sin puntuación intermedia aparente. No reconstruir el signo ni atribuir el resto a Lehmann. La lectura legítima previa no cierra este motivo. |
| 5078 / Herrera 286 | «V» al final del anuncio, antes del inicio nominal de Lehmann. No eliminarlo ni trasladarlo a la exposición siguiente. |

Los cuatro avisos usan `TEXTO_DANADO_POR_COTEJAR`, con intervalos exactos. En 202 el
problema señalado es una discordancia por cotejar, **no una fecha errónea demostrada ni
OCR como origen confirmado**. Las advertencias no certifican otros términos o tramos.

**462 = 459 filas alertadas anteriores + 3 nuevas:** 202 y 2701 por aviso; 4788 por el
pie sin puntuación conservado al separar la llegada. 3147 y 5078 **ya estaban alertados**:
se agrega un motivo, no una fila. Cuatro avisos no equivalen a cuatro filas nuevas ni a
cuatro errores confirmados. No se elimina puntuación o duplicados para reducir la cola.

## 4. Comparación global y controles

Contra la base LOOP30 congelada:

- **7.219 padres y 2.048.560 palabras conservados**, ignorando sólo espacios.
- **Seis padres con cambios de celdas no secuenciales**: 4788/6808 por separación de
  acta; 202/2701/3147/5078 por advertencia. **7.213 padres conservan esas celdas**.
  Sólo se excluyen `ID` e `ID_Turno` como numeración secuencial.
- **Todos los enlaces entre padres son idénticos**. Grupos fuera de esos seis padres
  también idénticos por sus miembros, no sólo por números de turno.
- **382 intervalos personales, 77 advertencias, 57 lecturas, 24 enlaces revisados,
  12 documentos, 2 fichas institucionales y 3 archivos de retiros previos intactos**.
  Nuevas fichas añadidas sin sobrescribir las anteriores.
- **85 hashes de entradas/código y 11 de salidas verificados**. Fuentes originales,
  fórmulas, detector automático y motores de continuidad conservan sus hashes.
- Esquemas **37/24**, **21 fórmulas**, **310 contrastes TPM**, **132 sesiones** y
  **55 etiquetas** preservados. TPM/documentos sólo cambian IDs de evidencia/documento/turno.
- Ensayo aislado/publicación idénticos celda a celda; publicación por pipeline completo,
  tras pruebas y controles, sin salidas parciales.
- Las **459 filas previas de la cola siguen presentes**. Salvo IDs secuenciales,
  **456 son idénticas**; 2743 añade anotación de lectura y 3147/5078 añaden motivo textual.
  Ninguna pierde sus alertas anteriores. Se agregan las tres filas descritas arriba.

Se preservan García de once filas, 224→225→226, 3454→3455, 2695→2696, 2754→2755,
2790→2791, 1386→1387, 2673→2674, 2863→2864, 2796→2797, 2680→2681, 2707→2708,
2963→2964, 4745→4746, 6561→6562, 5003→5004 y las 14 continuidades de LOOP28.
**3572 reanudación 235 sigue separada; 5402→5403 y 600→601 no se restauran.**
Las fichas 601/3110, el archivo de la pausa y los retornos 3044/4476/4926 siguen intactos.
No se afirma relectura de todos esos controles: se preservan por pruebas y comparación.

### Histórico 783: tres cambios no secuenciales

1. **Original 4467 / padre 3147:** se agrega `TEXTO_DANADO_POR_COTEJAR` al motivo previo.
2. **Original 6710 / padre 5078:** se agrega el mismo motivo a `FINAL_SIN_PUNTUACION`.
3. **Original 8592 / padre 6808:** `METODO_ACTUALIZADO` →
   `SEGMENTACION_O_ACTOR_MODIFICADO`, al separar el retiro. Cambian actores actuales,
   justificación y siguiente paso; no se certifica pureza completa del intervalo.

El resto de cambios del CSV son IDs secuenciales. **No todos los estados principales
son idénticos**: método actualizado baja de 330 a 329 y segmentación/actor modificado
sube de 167 a 168. Siguen **102 pendientes contextuales**, 497 comparaciones,
183 lecturas dirigidas y 103 triajes, con sus tipos de revisión intactos.

Los intervalos históricos con alertas actuales siguen siendo **285**, porque los dos
avisos históricos nuevos afectan intervalos que ya tenían motivos. Se mantienen seis
intervalos con variante y **21 filas actuales** de variantes. Las ocho menciones
históricas no son las 73 actuales. Los estados principales no cierran motivos residuales;
las unidades superpuestas no se suman.

## 5. Alcance, exploración y límites

Se leyeron **29 padres completos y tres cabeceras**. Padres: 202, 410, 953, 1273,
1338, 2499, 2564, 2608, 2701, 2743, 3059, 3147, 3286, 3615, 4787, 4788, 4789,
5078, 5658, 6353, 6402, 6669, 6807, 6808, 6809, 6891, 6935, 7124, 7175.
Cabeceras: **201, 4733, 6755**. Hay fichas nuevas en **23 padres**, por superposición
entre lecturas y advertencias; no son 29 resegmentaciones.

Los barridos fueron orientativos y superpuestos: 333 ventanas nominales/invertidas,
167 coincidencias de opinión, 9 candidatos de habla incrustada tras filtro, 20 relativas
con otro nombre, 1.946 combinaciones nominales con predicado no reconocido y 43
coincidencias de movimientos. **No son errores confirmados, lecturas íntegras de todos
los resultados ni una muestra representativa.** Se reutilizaron candidatos de LOOP30
como orientación, no como nuevas lecturas. El filtro de movimientos mezcla asistentes
con usos económicos —incorporar datos, ingresar bienes, abandonar una estrategia—;
no puede promoverse a regla de cambio de voz.

Quedan **77 lecturas actuales = 73 legítimas + 4 pendientes**: 6185/Bernier,
3775/Cerda, 4055/conjunto-institucional y 2510/conjunto. Siguen 3191/5367 y demás pasajes
conjuntos, conflictos de nombres/cargos, puente de 780, reserva de 6119 y otros pendientes
anteriores. No se adjudican arbitrariamente aportes conjuntos.

**Sin nuevo cotejo PDF ni muestra independiente con/sin alertas.** Identificar una voz
no certifica OCR; longitud no es daño. Verificaciones locales, sin afirmar CI remota.
Workflow preexistente fuera del PR; no queda proceso activo.

## Archivos

- [Base final](../data/processed/consolidado_base_referencia_final.xlsx)
- [Auditoría](../data/processed/consolidado_base_referencia.xlsx)
- [Comparación global y seis padres antes/después](comparacion_loop31_2026-09-08.json)
- [Detalle CSV](cambios_loop31_2026-09-08.csv)
- [Checkpoint](estado_revision_loop31_2026-09-08.json)
- [Pruebas LOOP31](../tests/test_loop31_review.py)
- [Informe anterior LOOP30](REVISION_LOOP30_2026-09-08.md)
