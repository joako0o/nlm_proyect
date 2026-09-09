# Refinamiento funcional v4 — 9 de septiembre de 2026

## Resultado

**Aplicados tres cortes funcionales y tres continuidades personales**, correspondientes a los padres **4788, 4849 y 4899**. El Presidente Rodrigo Vergara sigue siendo el hablante tanto de su aporte personal como de la declaración de unanimidad: **no hay reasignación de actor**.

La entrega nueva es [`data/releases/funcional_v4/`](../data/releases/funcional_v4/). No se sobrescriben LOOP32, v1, v2, v3 ni las fichas históricas.

- [Excel final, 24 columnas](../data/releases/funcional_v4/consolidado_base_referencia_final.xlsx).
- [Excel de auditoría, 37 columnas y hojas auxiliares](../data/releases/funcional_v4/consolidado_base_referencia.xlsx).
- [Tres decisiones y extremos](refinamiento_funcional_v4_2026-09-09/decisiones.csv).
- [Comparación global contra v3](../data/releases/funcional_v4/comparacion_funcional.json).
- [Linaje de todas las filas](../data/releases/funcional_v4/linaje_funcional.csv).
- [Verificación de pruebas, reproducción e históricos](refinamiento_funcional_v4_2026-09-09/verificacion.json).

| Métrica | v3 | Funcional v4 |
|---|---:|---:|
| Filas físicas | 9.691 | **9.694** |
| Bloques de texto | 9.690 | **9.693** |
| Grupos `ID_Turno` | 9.242 | **9.242** |
| Grupos de varias filas | 349 | **352** |
| Máximo de filas en un grupo | 11 | **11** |
| Filas con alertas | 465 | **467** |
| Padres con alertas | 395 | **397** |
| Pruebas intrapadre acumuladas | 15 | **15, conservadas** |
| Pruebas revisadas entre padres | 24 | **24, conservadas** |

Las tres continuidades nuevas se expresan como `CONTINUIDAD_EXPLICITA`, vinculadas a la evidencia funcional v4. No se añaden artificialmente a los registros históricos de 24 o 15 pruebas. El corpus mantiene 7.219 padres y 132 sesiones; no se modifica su número de palabras.

## Qué se separa y qué se enlaza

La aplicación utiliza la **lectura completa y los grupos documentados en el [lote4](CONTINUIDAD_LOTE4_2026-09-09.md)**. No se presenta como una segunda lectura semántica independiente ni como nuevo cotejo PDF.

El límite exacto empieza en:

> En consecuencia, el Presidente señor Rodrigo Vergara deja constancia que se acuerda por unanimidad

Esto es un **cambio de función del texto**, no una señal de que tomó la palabra otra persona. Sólo el aporte previo queda sin tipo institucional y continúa al Presidente del padre anterior. La constancia conserva `ACUERDO_CONSEJO`, no hereda continuidad personal ni genera un ancla de habla.

| Fecha / padre | Antecedente personal | Aporte separado | Constancia y residuo | Resultado |
|---|---|---:|---:|---|
| 17-04-2012 / **4788** | 4787:2, 1.423 caracteres | **1.946** | **185** | 4787:2 → 4788:1; constancia 4788:2 separada |
| 17-05-2012 / **4849** | 4848:1, 3.941 caracteres | **153** | **178** | 4848:1 → 4849:1; constancia 4849:2 separada |
| 14-06-2012 / **4899** | 4898:1, 2.802 caracteres | **219** | **178** | 4898:1 → 4899:1; constancia 4899:2 separada |

Cada prefijo literal contiene además **un espacio separador** al final. Se guarda explícitamente en el [registro v4](../data/curation/refinamiento_funcional_v4.json): las reconstrucciones son **1.946 + 1 + 185 = 2.132**, **153 + 1 + 178 = 332** y **219 + 1 + 178 = 398**. Las celdas conservan la política previa de quitar espacios exteriores; no se pierde ninguna palabra ni carácter no blanco. Los offsets del linaje son de base cero, con fin exclusivo, dentro de la fila anterior.

### Límites posteriores protegidos

- **4788** pasa de cuatro a cinco tramos: aporte personal **1.946** / constancia y pie **185** / llegada institucional **112** / intervención de Larraín **161** / retorno del Presidente **333**. La llegada no se atribuye como discurso del asistente. Ni Larraín ni el retorno quedan absorbidos por la continuidad inicial. La exposición posterior de **4789, 8.541 caracteres**, permanece intacta.
- **4849** conserva el acuerdo/comunicado del Consejo de **2.126 caracteres**, ahora segmento 3, separado de ambos segmentos del Presidente.
- **4899** conserva el acuerdo/comunicado del Consejo de **2.189 caracteres**, ahora segmento 3, también separado.
- Se mantienen el OCR literal, incluido `Pablo Garda`, la cifra `€100 billones`, los pies de página y los avisos existentes. No se corrigen identidades ni se amplían alias.

## Alertas: dos nuevas, ningún cierre

Las constancias de **4849:2 y 4899:2 son exactamente iguales**, de 178 caracteres, aunque pertenecen a sesiones distintas. Al separarlas, el cálculo global detecta dos duplicados nuevos. No están en el catálogo histórico de fórmulas procedimentales y reciben **`DUPLICADO_NO_FORMULA`**.

**No se borran, no se deduplican y no se añade una excepción para ocultar el aviso.** La repetición no demuestra un error de datos. El número de filas con ese motivo pasa de 19 a 21; los duplicados exactos pasan de 633 a 635.

En **4788**, `FINAL_SIN_PUNTUACION` queda asociado a la constancia que termina con `Sesión N° 184 Página 23 de 26`. El aviso se desplaza del antiguo segmento mixto al segmento 2, donde está el residuo; **no se cierra**. El total de finales sin puntuación sigue en 317.

Por eso la cola pasa de **465 filas / 395 padres** a **467 / 397**. No es una estimación de errores ni un recuento de lo que falta leer. `SIN_ALERTAS_AUTOMATICAS` tampoco acredita revisión humana de todo un texto.

## Protección de la prueba institucional de 4788

La revisión histórica `ACTA-20260908-L31-4788` exige cuatro tramos. **Su JSON y el validador institucional original no se modifican.**

1. El segmentador utiliza primero esa prueba histórica de cuatro tramos.
2. Un adaptador opcional y acotado exige coincidencia exacta del primer tramo, su actor y su fuente.
3. La prueba v4, ligada al hash de la revisión anterior y a la lectura del lote4, sustituye únicamente ese tramo por aporte + constancia.
4. La tipificación y F1 verifican **las cinco filas reales** con una copia refinada de la prueba. Los otros tres tramos y sus atributos permanecen iguales.

La prueba original **rechaza** las cinco filas si no se le aporta el refinamiento. Esto está probado: no se relaja su validador ni se reconstruyen ficticiamente cuatro filas para eludirlo.

## Comparación y regresiones

El gate v4 no reutiliza el comparador que presupone igual cardinalidad. Construye el esperado desde **v3 inmutable y los tres límites documentados**, sin tomar decisiones de la salida candidata.

Compara **cada campo de cada fila y todos los miembros de cada grupo**, con el renumerado explícito de filas, segmentos, bloques y referencias. Las únicas diferencias permitidas son las derivadas del refinamiento, las tres continuidades personales y las alertas descritas. No hay una lista abierta de campos que se ignoren globalmente.

Se conservan, entre otros:

- Los grupos extensos de García, de hasta once filas, y las presentaciones largas.
- Las 24 pruebas entre padres y las 15 intrapadre de v1/v2/v3, incluidas sus continuaciones posteriores.
- Las pausas y reanudaciones respaldadas en lote4, sin extender grupos a través de ellas.
- Las reservas de 780, 2661, 2863, 3646 y 5252 y los demás casos ambiguos; no se convierten en enlaces por falta de alertas.
- La prohibición de restaurar 600→601 o 5402→5403 y de convertir `CONTEXTO_REVISADO` en ancla global.
- Los documentos recibidos para lectura, la distinción autor/lector/asistencia, y los retornos personales.

**25 pruebas nuevas** cubren alcance, evidencia/hash, límites, segmentación real, conservación, tipificación, anclas, continuidad, duplicados, movimiento institucional, mutaciones de filas/grupos y aislamiento de perfiles.

### Verificación ejecutada

- Primera construcción aislada: **2.057 pruebas, PASS, 298,511 s**; F0, comparación global y F1 **PASS**.
- Segunda construcción y publicación: **2.057 pruebas, PASS, 299,852 s**; los mismos gates **PASS**.
- Las tres planillas reproducen **todas sus hojas y celdas**, no sólo la hoja principal.
- Los seis CSV, el JSONL y los JSON de QA/resumen son **idénticos byte a byte** entre ambas construcciones.
- La comparación sólo difiere en el SHA del XLSX candidato por metadatos binarios. Los manifiestos verifican **119 entradas/código y 13 salidas** por construcción; el manifiesto es el archivo número 14.
- Los **69 archivos de datos y 254 documentos/artefactos anteriores** conservan sus bytes. De los scripts anteriores se modifican sólo constructor, runner y QA; **31 quedan intactos**. Se añaden los dos módulos de refinamiento/comparación y su prueba.

SHA-256 de la base v4: `a8038f8c18933990a84a870fb607f2053e8daccc0dbea634dc612635fe41a5df`.

## Reproducir sin sobrescribir

```bash
.venv/bin/python scripts/preparar_data.py \
  --perfil funcional-v4 \
  --destino .cache/reproduccion_funcional_v4
```

El destino debe ser nuevo. `funcional-v4` es el perfil predeterminado y utiliza las quince pruebas intrapadre v3 más el registro funcional separado. Los perfiles `legacy`, `intrapadre-v1`, `intrapadre-v2` e `intrapadre-v3` eliminan la activación ambiental funcional; sus alcances no se amplían.

## Alcance pendiente

Esta entrega resuelve la aplicación de **los tres límites mixtos del lote4**, no toda la revisión semántica del corpus. Las otras seis reservas de ese lote y las reservas anteriores mantienen su estado. No hubo segundo revisor semántico, subagentes ni nuevo cotejo PDF; las pruebas técnicas no sustituyen esa revisión.
