# Continuidad — lote3 y entrega intrapadre v3

**9 de septiembre de 2026. Nueve enlaces nuevos aplicados; cinco reservas conservadas.**

[Excel final](../data/releases/continuidad_intrapadre_v3/consolidado_base_referencia_final.xlsx) ·
[Excel de auditoría](../data/releases/continuidad_intrapadre_v3/consolidado_base_referencia.xlsx) ·
[QA](../data/releases/continuidad_intrapadre_v3/qa_preparacion.json) ·
[Comparación global](../data/releases/continuidad_intrapadre_v3/comparacion_intrapadre.json).

## Alcance: todos los casos restantes del subgrupo, no todo el corpus

Se revisaron los **14 candidatos restantes** de la selección utilizada en lote2:
`CONTEXTO_REVISADO → fuente explícita`, sin avisos en los extremos y con la falta
de fuente propagable a la izquierda como único indicador del inventario.
No se seleccionaron únicamente los más cortos esta vez.

Se leyeron **18 padres completos, 70.514 caracteres originales**, a través de sus
particiones literales completas, incluyendo todas las voces y todos los miembros
de los grupos afectados. Se comprobó que la concatenación conserva la totalidad
del original ignorando sólo espacios entre segmentos. Se guarda también el texto
íntegro original, su hash y la firma de la partición. Las ventanas externas son de
hasta250 caracteres; no constituyen lectura completa de otros padres vecinos.
El desarrollo2603 de2754 se volvió a leer completo tras truncarse su primera salida.

Además de los14 padres de candidatos, se leyeron completos **2696,2755,2791 y2864**,
porque sus filas pertenecen a grupos implicados. Esto permite conservar las
continuaciones largas sin unir respuestas a través de otra persona.

[Lecturas completas y evidencia](continuidad_lote3_2026-09-09/lecturas.json) ·
[Decisiones de los14 casos](continuidad_lote3_2026-09-09/decisiones.csv).

**Ausencia de alerta no significa ausencia de dudas.** Cinco candidatos quedan
reservados, incluidos casos sin palabras transcritas y con residuos textuales.
No hubo nuevo cotejo PDF, corrección de OCR ni cierre de advertencias.

## Nueve enlaces aplicados

| Padre / persona | Grupo completo resultante, caracteres | Separaciones conservadas |
|---|---|---|
| **1092 / Jadresic** | 276 +2821 = **3097** | El análisis atribuido al Gerente de Estudios es una referencia, no otra voz actual. |
| **2695 / Soto** | 433 +1020 +651 de2696 = **2104** | Presidente192 y sus avisos permanecen fuera. En2696 se separan Desormeaux107, los retornos de Soto, el Presidente y Marfán. |
| **2754 / Marshall** | 732 +2603 +4429 de2755 = **7764** | Claro7258 permanece fuera, al igual que Marfán2756. Se conservan literalmente `e\ apoyo` y `cambíanos`; el enlace no certifica esas grafías. |
| **2778 / Soto** | 803 +1810 = **2613** | Marfán519 queda fuera. No se incorpora el Soto de2779 atravesando a Cowan ni se inventan palabras del asentimiento de2779. |
| **2790 / Soto** | 594 +3179 +2819 de2791 = **6592** | No se añaden2789 ni el agradecimiento del Presidente2792. Se conserva toda la enumeración y desarrollo de las tres consideraciones sobre política/FLAP. |
| **2810 / Lehmann** | 274 +932 = **1206** | Marshall153 y Marfán481 quedan fuera. El retorno de Lehmann1812 sigue separado por Marfán. `Lehman Brothers` es la empresa mencionada, no un alias ni otra intervención. |
| **2909 / Soto** | 604 +2465 = **3069** | El Soto inicial1806 no se une atravesando a Marfán1244. El Presidente2910 queda fuera. |
| **3439 / Jaque** | 390 +1955 = **2345** | De Ramón152 permanece separado, con su aviso. Jaque aporta explicación sustantiva además de confirmar, a diferencia de las confirmaciones reservadas. |
| **6800 / Vial** | 3564 +151 = **3715** | Presidente141 queda fuera. La reiteración del voto se conserva literalmente, no se elimina como duplicación. Las felicitaciones a Valdés no crean otro turno. |

Cada extremo izquierdo sigue siendo contextual y **sin ancla**. Cada extremo
derecho conserva su **ancla explícita propia** y recibe una relación revisada con
antecedente inmediato. Las filas físicas no se fusionan. No se crea una regla
por «Agrega», «En cuanto», «Finalmente», gerundios o coincidencia de actor.

## Cinco reservas: no se fuerzan enlaces

| Padre | Reserva y alcance |
|---|---|
| **780** | Se mantiene pendiente el límite del puente `En la economía nacional` dentro de De Gregorio5463. No se desplaza ese texto ni se usa la compatibilidad de Corbo1655/1763 para resolverlo indirectamente. Se conservan cuatro grupos, incluido Consejo2546. |
| **2661** | La confirmación49 de Lehmann no transcribe palabras ni explicita modalidad. No se fusiona con su desarrollo1322. Se conservan las12 partes/grupos y todos los cambios de voz. No se afirma una discontinuidad absoluta entre ambos tramos. |
| **2863** | Se posterga el enlace adicional63→939 ante residuos como `ha caído algo r últimamente` y `A continuación,.`, aun sin aviso automático en esos extremos. **La continuidad existente2863:3→2864:1 se conserva**; no se elimina una relación previa ni se borra texto. |
| **3646** | La confirmación84 no transcribe palabras. Aunque el siguiente tramo dice que Lehmann continúa1168, se conserva la reserva sobre su agrupación/modalidad. Claro233 y su retorno98 permanecen separados. No se inventa una respuesta verbal. |
| **5252** | Relectura y conservación de la reserva anterior: comentario1712 / acta158 / aviso162 / cesión223 siguen separados. La llegada futura de Vergara no es habla; la cesión no adelanta a Herrera. |

Estas reservas son decisiones conservadoras de este lote, **no cinco errores
confirmados ni cinco pruebas de que intervino otra persona entre los extremos**.

## Resultado global y límites de las cifras

| Medida | v2 | v3 |
|---|---:|---:|
| Filas físicas / bloques de texto | 9691 /9690 | **9691 /9690** |
| Grupos | 9251 | **9242** |
| Grupos con varias filas | 343 | **349** |
| Máximo de filas por grupo | 11 | **11** |
| Filas alertadas / padres alertados | 465 /395 | **465 /395** |
| Pruebas intrapadre acumuladas | 6 | **15** |
| Pruebas revisadas entre padres | 24 | **24** |
| Pares del inventario | 86 | **77** |

El gate compara **toda la partición por pertenencia**, no sólo los padres del lote:
exactamente nueve uniones, ninguna otra fusión y ningún grupo previo dividido.
Cambia el conjunto de compañeros de **21 filas**. Hay **18 celdas relacionales**
modificadas —nueve relaciones y nueve antecedentes— y **358 etiquetas de grupo
renumeradas**. No son358 uniones ni358 correcciones semánticas.

**Todos los otros campos son idénticos celda a celda:** textos, actores, cargos,
fuentes, anclas, fechas, IDs físicos, clasificación y alertas. Se mantienen7.219
padres y2.048.560 palabras. Las seis pruebas intrapadre anteriores quedan idénticas,
incluidas Marshall2796→2797 y De Ramón3012. No se restauran600→601 ni5402→5403,
ni se fuerzan los pares alertados deLOOP32. Esta conservación global no afirma
que se hayan releído todos esos casos en el lote3.

[Inventario v2](continuidad_lote3_2026-09-09/inventario_v2.csv) ·
[Inventario v3](continuidad_lote3_2026-09-09/inventario_v3.csv).
Los77 pares restantes son **28 intrapadre y49 entre padres**: cinco reservas de
este lote y72 fuera de esta selección. Los CSV distinguen explícitamente
`FUERA_DE_ESTE_LOTE_NO_ADJUDICADO`; no equivale a «nunca leído» ni a aprobación.
La lectura del subgrupo está cubierta, **no la revisión total del corpus**.

## Verificación y entrega versionada

- **Ensayo aislado:**2.008 pruebas en217,300s; reconstrucción, F0/F1 y gate global pasan.
- **Publicación:**2.008 pruebas en222,612s; reconstrucción, F0/F1 y gate global pasan.
  Hay **28 pruebas nuevas**. El test del perfil predeterminado ahora espera v3;
  los perfiles explícitos v1/v2 siguen validados sin ampliar sus registros.
- Ensayo/publicación: **todas las hojas/celdas de tres XLSX idénticas**, seis
  auxiliares CSV/JSONL idénticos byte a byte y QA idéntico; mismo código en ambos.
  No se confunde igualdad de celdas con igualdad binaria de metadatos XLSX.
- **113 hashes de entradas/código y12 de salidas** verificados, más el hash de
  lecturas y el vínculo del registro acumulativo con v2.
- **55 archivos históricos de datos y241 documentos/artefactos anteriores**
  idénticos byte a byte frente a `f59210022688e36bcab112a3a4c588b1c6f0ed42`.
  LOOP32, v1, v2, sus manifiestos y las fichas fechadas no se sobrescribieron.

[Verificación](continuidad_lote3_2026-09-09/verificacion.json) ·
[Registro acumulativo](../data/curation/continuidades_intrapadre_v3.json) ·
[Manifiesto v3](../data/releases/continuidad_intrapadre_v3/manifiesto_preparacion.json).
Los manifiestos históricos remiten al código de sus commits. Las comprobaciones
son **locales**, no CI remoto ni certificación semántica total. Las465 filas
alertadas, dudas de identidad y pasajes conjuntos pendientes siguen abiertos.

```bash
.venv/bin/python scripts/preparar_data.py --perfil intrapadre-v3 \
  --destino .cache/reproduccion_intrapadre_v3
```

El destino debe ser nuevo. v3 es el perfil predeterminado; v1/v2 siguen disponibles
explícitamente para reproducir su semántica sin sobrescribir sus entregas.
**Siguiente frente:** los pares con indicadores adicionales —acta/documento,
barreras, alertas o atribuciones no propagables— requieren otra selección y lectura
completa. No se extienden estas nueve pruebas a esos72 casos automáticamente.
