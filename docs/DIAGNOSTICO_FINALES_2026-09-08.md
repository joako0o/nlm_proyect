# Diagnóstico de finales sin puntuación — 2026-09-08

**Base:** entrega LOOP32, commit `1b0249635bde7ce7ec177738c79bcf3a99fd486b`.
**Propósito:** encontrar patrones que permitan revisar por lotes antes de continuar
la corrección de hablantes. **No es una nueva entrega de datos ni cierre de alertas.**

## Resultado útil

De las **465 filas con alertas**, 317 incluyen `FINAL_SIN_PUNTUACION` y **302 tienen
únicamente ese motivo**, repartidas en 275 padres. Un padre puede tener además otros
segmentos con otros avisos: 275 no significa 275 padres libres de problemas de voz.

El patrón principal es claro: **167 de esas 302 filas (55%) terminan en coma justo
antes de otra fila del mismo padre con distinto actor exportado**. Es una propiedad
comprobable del archivo, no una certificación de que los 167 límites sean correctos.
En los ejemplos leídos aparecen preguntas/respuestas, réplicas y cambios ya separados;
no corresponde tratarlos inicialmente como 167 pérdidas de texto.

**No se borraron comas, pies, letras, palabras o alertas. No se cambiaron voces,
límites, grupos de turno, IDs o fichas de curación.** Se mantiene la entrega de
**9.691 filas y 465 alertadas en 395 padres**.

## Clasificación reproducible

Categorías excluyentes por prioridad del clasificador, sobre las **302 filas con
ese único aviso**. Son categorías de triaje, no causas certificadas.

| Patrón observable | Filas | Intervalos seleccionados leídos |
|---|---:|---:|
| Coma antes de otro actor dentro del mismo padre | 167 | 12 |
| Pie de página o rótulo institucional espaciado al final | 13 | 6 |
| Encabezado «Exposición Síntesis del mes» | 1 | 1 |
| Cola breve después de un signo de cierre | 42 | 5 |
| Final en término funcional: «para», «el», «las»… | 10 | 5 |
| Otros finales sin puntuación | 67 | 5 |
| Coma en otro contexto: aquí, mismo Presidente en dos modalidades | 2 | 2 |
| **Total** | **302** | **36** |

El CSV contiene las **317 filas**, incluyendo las 15 con motivos adicionales, que
se conservan explícitamente. No deben aplicarse los conteos de la tabla a las 317.
El rótulo del Banco exige letras espaciadas: la mera mención «Banco Central de Chile»
no se identifica como pie. La búsqueda sólo observa el final, no borra coincidencias
interiores. Las relaciones de continuidad se leen de los IDs/antecedentes ya
exportados y nunca se crean por coincidencia de actor.

## Lectura dirigida: qué se comprobó

Se leyeron **36 intervalos focales completos, en 36 padres**, con ventanas de hasta
240 caracteres de las filas colindantes. **Sólo cinco padres se leyeron completos en
esta pasada:** 301, 631, 1386, 1737 y 2555. No se debe convertir esta cifra en «36
padres completos». Los vecinos pueden ser partes del mismo padre o de padres distintos;
la herramienta conserva fechas y claves para distinguirlos.

Selección dirigida, no aleatoria: variedad de terminaciones, períodos, cargos,
intercambios breves y un desarrollo largo. Se incluyeron deliberadamente controles ya
revisados (como 3044, 4788 y 628). **No es una muestra independiente ni representativa**,
ni permite estimar precisión, errores restantes o horas ahorradas.

### A. Comas que acompañan límites ya exportados

- **301:** Eyzaguirre pregunta y Marfán responde después de «Al respecto».
- **631:** el Ministro consulta y Lehmann responde con «a lo cual».
- **1386:** Corbo consulta, Lehmann responde, Corbo cede la palabra y Valdés presenta.
  El enlace posterior 1386→1387 corresponde a **Valdés**, no a la pregunta con coma.
- **1737:** Desormeaux se suma a la mayoría; Claro mantiene otro voto. La conjunción
  no justifica adjudicar ambos votos al primero.
- **2555:** pregunta de Marshall, comentario de Marfán, agregado de Desormeaux,
  conclusión de García y reanudación de Lehmann. Hay también un límite sin coma en
  Marfán87: un cambio de voz no requiere que el origen termine en punto.
- **2697:** explicación de **Soto2739** antes del comentario explícito de Claro.
  Se conserva el desarrollo largo; su carácter interno «l» no queda certificado por
  estudiar la coma final.
- **2896/3044/4096/6415/7176:** consultas, réplicas o agregados con sujeto propio.
- **5252:** reanudación institucional seguida de un tramo exportado a Marfán.
  Aquí «distinto actor» incluye **Consejo**: no son necesariamente dos voces personales
  ni se certifica el límite institucional por esta clasificación.

**Ahorro posible:** comprobar estos límites en una vista que muestre ambos sujetos y
la coma literal, sin empezar cada caso como una supuesta pérdida de texto. No eliminar
el motivo globalmente: el mismo padre puede conservar otra duda o un límite incorrecto.

### B. Pies y encabezados

En **4753, 4784 y 4788**, el contenido anterior termina en punto y sigue
«Sesión N°184 Página… de26». En **5349, 6730 y 6733**, aparece el nombre espaciado del
Banco. En **6733** queda además una «i» antes del rótulo; reconocer éste no valida la letra.

En **628**, el anuncio de Corbo termina en punto y luego aparece
«Exposición Síntesis del mes». La exposición de Lehmann empieza después y permanece
íntegra. Su ficha previa de referencia no cierra el aviso de puntuación.

**Ahorro posible:** revisar estos finales como composición editorial, con el texto
anterior y el comienzo del siguiente tramo. No borrarlos ni moverlos para mejorar
estadísticas. En particular, el pie de **4788** no se arrastra a la llegada institucional.

### C. Un indicio especialmente útil: palabra posiblemente desplazada al anterior

La lectura encontró tres ejemplos:

| Foco | Final del tramo focal | Final literal de la fila anterior |
|---|---|---|
| 771 | «ofrece la palabra a los asistentes para» | «…política monetaria. comentarios.» |
| 1077 | «ofrece la palabra para comentarios sobre el escenario» | «…meses anteriores. interno.» |
| 2121 | «ofrece la palabra… para proceder a la» | «…hacia la neutralidad. votación.» |

La coincidencia sugiere un **posible problema de orden del texto extraído**, no
necesariamente una palabra ausente. No identifica el origen del problema ni prueba
a qué hablante pertenece la palabra.

Una búsqueda literal conservadora encuentra **ocho candidatos**:
**771, 1077, 1544, 1652, 2121, 2166, 2293 y 2434**. Tres pertenecen a la selección de36;
las otras cinco coincidencias se inspeccionaron sólo por sus finales, sin sumar lecturas
completas de sus padres. Son un **indicio adicional superpuesto** a las categorías de
la tabla, no ocho casos nuevos que deban sumarse al total302.

**Siguiente trabajo recomendado:** cotejar estos pares con la fuente documental para
resolver la posición literal. No mover «comentarios», «interno» o «votación» por una
regla global ni heredar actor por proximidad. Este diagnóstico no consultó nuevos PDFs.

### D. Finales que no deben tratarse como simples comas o pies

- **653:** «dado que el», antes de comenzar De Gregorio.
- **748:** «cuando los», antes de Jadresic.
- **3784:** «una caída importante en las», antes de Marshall.
- **514:** anuncia un hecho de «una agencia clasificadora de riesgos» sin desarrollarlo
  antes del siguiente tramo. Son finales aparentemente incompletos para cotejo;
  no se reconstruyen sustantivos o hechos.
- **210/1347/2312/5293/5770:** quedan «Y», «Lf» con barra invertida, «Y ■», «f» o una
  barra después de puntuación. Una letra puede ser conjunción real; ni siquiera esta
  categoría autoriza a borrarla o afirmar origen OCR.
- **1731:** se leyó el intervalo completo de **Marshall7456**, incluida su decisión y
  cierre sobre el comunicado. No se fragmenta por longitud. La falta de punto no
  demuestra pérdida ni certifica la integridad del resto del texto.
- **4233:** Herrera responde y después «el Gerente de Análisis Internacional agrega».
  Muestra que un final léxico sin coma también puede acompañar un límite entre sujetos.
- **6058:** anuncio y cesión de Vergara; Lehmann empieza después con sujeto explícito.

### E. Dos controles documentales

**3575 y 4109** tienen coma entre el agradecimiento presidencial y el anuncio de
lectura recibido del Ministro. Comparten actor exportado, pero sus modalidades están
separadas conforme a la revisión documental previa. **Mismo actor no implica fusionar**;
autor ≠ lector. No se convierten sus fórmulas en nuevos documentos ni se cierran avisos.

## Qué cambia en la manera de trabajar

1. **Cola de límites ya exportados:** 167 comas; ver inmediatamente ambos lados y
   distinguir persona/acta/documento. Confirmar individualmente antes de cualquier cierre.
2. **Cola editorial:** 13 pies y un encabezado; separar el motivo editorial del problema
   de voz sin alterar el literal.
3. **Cola de cotejo textual:** finales abiertos, letras sueltas y los ocho indicios de
   palabra desplazada. Priorizar documentación, no ajustes del detector de hablantes.
4. **Cola residual:** estudiar los otros finales y las modalidades documentales con
   contexto. No darles cierre por descarte del clasificador.

Esto organiza el trabajo; **no reduce todavía el número de pendientes**. Las 102
lecturas actuales registradas de LOOP32 (98 legítimas y4 pendientes) siguen iguales:
estas36 lecturas diagnósticas están en un registro separado, no son nuevas fichas de
menciones ni adjudicaciones de voz.

## Herramienta y validación

```bash
.venv/bin/python scripts/diagnosticar_finales.py \
  --salida .cache/diagnostico_finales_reproducido
```

Produce resumen JSON, CSV con finales/inicios y JSON con contexto completo. No está
integrada en el pipeline ni es llamada por él. Rechaza salidas dentro de `data/`,
`.git/`, `scripts/` o `tests/`, y no sobrescribe la entrada.

- **1.780 pruebas pasan: 1.757 previas +23 de diagnóstico.**
- **26 archivos de datos, fuentes y curación idénticos por SHA-256**, incluidas bases,
  colas, QA y manifiesto. Ningún cierre o cambio de grupos/actores/textos.
- Se verifican preservación de motivos adicionales, ausencia de mutaciones, protección
  de rutas, fechas, antecedentes de continuidad y ejemplos negativos de los patrones.
- **No se reejecutó el pipeline**, porque esta pasada sólo añade una herramienta
  independiente y documentación. La entrega de datos y su QA siguen siendo LOOP32.
  No se afirman nueva validación semántica exhaustiva ni CI remota.

## Evidencia y archivos

- [Resumen, alcance y hashes de conservación](diagnostico_finales_2026-09-08/resumen.json)
- [317 candidatos automáticos y sus motivos adicionales](diagnostico_finales_2026-09-08/candidatos.csv)
- [36 lecturas: texto focal completo, contexto acotado, hashes y observaciones](diagnostico_finales_2026-09-08/lecturas_36.json)
- [Herramienta](../scripts/diagnosticar_finales.py)
- [Pruebas](../tests/test_diagnosticar_finales.py)
- [Entrega de datos vigente: LOOP32](REVISION_LOOP32_2026-09-08.md)

El CSV automático sigue etiquetando candidatos, no cierres; para saber qué se leyó,
consultar el registro separado de36. Los textos de contexto guardados no significan
que todos esos padres hayan sido leídos completos.
