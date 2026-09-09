# Lote6 — reservas complejas y estado del inventario

**9 de septiembre de 2026 · Revisión de lectura, sin aplicar enlaces**

## Resultado

Se releyeron los cinco casos prioritarios **780, 2661, 2863, 3646 y 5252**, incluyendo **2864**, que forma parte del grupo de Soto. Son **6 padres completos, 28 filas de la partición y20.797 caracteres de origen**; los grupos directamente implicados tienen11 miembros.

La revisión distingue **dos propuestas locales de continuidad, todavía no aplicadas**, y **tres reservas con acciones diferentes**. Además, ordena los71 pares del inventario para no confundir una separación ya respaldada con una continuidad pendiente.

**La entrega de datos sigue siendo [procedimental v5](../data/releases/continuidad_procedimental_v5/): 9.694 filas, 9.236 grupos y467 filas alertadas en397 padres.** No se reconstruyeron ni publicaron datos nuevos, no se aplicaron cortes o enlaces y no se cerraron alertas.

- [Inventario por estado](continuidad_lote6_2026-09-09/inventario_estado.csv).
- [Cinco decisiones de lectura](continuidad_lote6_2026-09-09/decisiones.csv).
- [Tres reservas y siguiente acción](continuidad_lote6_2026-09-09/reservas_y_siguiente_accion.csv).
- [Lecturas completas, fuentes y miembros](continuidad_lote6_2026-09-09/lecturas.json).
- [Resumen](continuidad_lote6_2026-09-09/resumen.json) y [verificación técnica](continuidad_lote6_2026-09-09/verificacion.json).

## Decisiones

### 780 — reserva por el inicio de Corbo

El padre completo tiene **11.430 caracteres**. La partición conserva De Gregorio **5.463**, Corbo **1.655**, Corbo **1.763** y Consejo **2.546**, con los separadores originales entre tramos.

Tras el voto de De Gregorio aparece `En la economía nacional…`, sin atribución nominal propia. Ese puente permanece dentro del primer segmento. Más adelante, `Lo que sí ha cambiado, indica el señor Corbo…` identifica a Corbo. Sus dos tramos son compatibles, pero **esa compatibilidad no resuelve dónde comenzó su intervención**.

Se conserva la reserva y el aviso `TEXTO_DANADO_POR_COTEJAR`. La acción concreta es cotejar la transición en el acta RPM95 del13-07-2006; no desplazar el puente por afinidad temática ni resolverlo con búsquedas generales de nombres. El acuerdo del Consejo sigue separado.

### 2661 — reserva por confirmación narrada

Se leyó todo el intercambio de **3.918 caracteres y12 segmentos**. La acotación de **49 caracteres** dice que la observación de Desormeaux «es confirmada por el señor Lehmann». No transcribe palabras ni especifica modalidad. El desarrollo de Lehmann de **1.322 caracteres** comienza después, sobre producto potencial.

Aquí no aparece un marcador explícito de continuación como en3646. **Se mantiene la reserva**, sin deducir gesto, silencio, interrupción o respuesta verbal. Tampoco se unen los retornos de Lehmann a través de Desormeaux, Velasco, De Gregorio o Claro.

La acción pendiente es precisar el tratamiento de una confirmación narrada sin desarrollo. Si el PDF contiene la misma redacción, por sí solo no permitirá inferir su modalidad.

### 2863→2864 — propuesta local, no aplicada

Se leyeron **1.110 +495 caracteres**. Marfán pregunta sobre la reconstrucción del IPC (**106**); Soto responde que fue un suavizamiento (**63**) y el texto identifica nominalmente al mismo Soto al desarrollar las sorpresas inflacionarias (**939**). Ese desarrollo ya continúa a2864 (**495**).

La relectura distingue el problema de OCR del problema de continuidad: `ha caído algo r últimamente` está dentro del desarrollo y `A continuación,.` al final, **no en el límite entre la respuesta y el desarrollo**. Esos residuos no bastan para demostrar una discontinuidad en2863:2→3. Cambiar de aspecto del análisis tampoco constituye por sí solo un corte.

**Se propone evaluar la implementación de2863:2→3**, manteniendo el enlace existente2863:3→2864:1: un grupo de tres miembros y1.497 caracteres de texto, sin contar separadores entre filas. No se incorpora la pregunta de Marfán, no se corrige el OCR y el tramo contextual conserva su ancla nula. La propuesta no se ha incorporado al motor ni al registro productivo.

### 3646 — propuesta respaldada por «continúa», no aplicada

El padre tiene **1.586 caracteres**: Claro **233**, confirmación de Lehmann **84**, desarrollo de Lehmann **1.168** y retorno de Claro **98**.

La confirmación sigue sin palabras transcritas ni modalidad explícita. Sin embargo, el siguiente enunciado dice **«El señor Lehmann continúa»**. Es una señal positiva de continuidad discursiva, distinta de la mera adyacencia de2661.

**Se propone evaluar la implementación de3646:2→3**, conservando ambas filas, la fuente `CONTEXTO_REVISADO` y el ancla nula de la confirmación, y dejando fuera ambas intervenciones de Claro. Agrupar la secuencia no autoriza a convertir la confirmación en una cita verbal ni a afirmar que fue gestual. No se generaliza a otras confirmaciones y no hay enlace aplicado aún.

### 5252 — reserva por la frontera acta/persona

Se leyó el padre de **2.258 caracteres**. Se conservan los cuatro segmentos: comentario/cierre de Marfán **1.712**, reanudación institucional **158**, aviso **162** y cesión a Herrera **223**.

El gerundio `haciendo presente…` depende sintácticamente de la narración de reanudación y presidencia transitoria. El aviso puede acompañar la conducción de Marfán, pero **su frontera con la voz narrativa del acta sigue abierta**. Unir aviso y cesión no resuelve ese problema previo.

Se debe revisar primero esa frontera con el criterio de función textual y, cuando esté disponible, la fuente original. Vergara **se incorporará posteriormente**: no toma la palabra aquí. Herrera empieza en5253; sólo se leyó una ventana externa de ese inicio, no su exposición completa en este lote.

## Inventario organizado

| Estado en esta vista | Pares | Qué significa |
|---|---:|---|
| Separación respaldada previamente | **10** | Nueve pausas/reanudaciones y la distinción voto/constancia de4332→4333, documentadas en lote4. |
| Separación funcional v4 | **3** | Aporte personal frente a constancia en4788,4849 y4899; conservarlas. |
| Propuesta local no aplicada | **2** | 2863 y3646: preparar implementación acotada y controles antes de cambiar datos. |
| Reserva por inicio / confirmación / frontera acta-persona | **3** | 780,2661 y5252, con acciones específicas; no son tres pedidos equivalentes de PDF. |
| Sin adjudicación en este inventario | **53** | Localizar y comprobar fichas previas antes de programar nuevas lecturas. No significa nunca leído. |
| **Total** | **71** | El inventario no disminuye porque este lote no aplica enlaces. |

Las13 separaciones tienen **respaldo anterior verificado**, no una nueva lectura completa en lote6. Se comprueban sus extremos y fuentes; no se recicla esa evidencia como si se hubieran releído ahora todos sus padres y grupos.

Esta vista no calcula un porcentaje de revisión semántica del corpus. Las467 alertas no son un total de errores ni de trabajo pendiente, y se superponen con el inventario. Una fila sin alertas tampoco acredita lectura humana completa.

## Implementación y validación

Se añade únicamente un exportador de lectura/triage y sus pruebas. **No se modifican el constructor, las reglas de continuidad, los validadores productivos ni los registros de curación existentes.**

El paquete exige un alcance cerrado de cinco pares/seis padres, hash de la base v5, fuentes y fichas previas, texto íntegro de cada padre, particiones, ventanas externas y todos los miembros de los grupos. Las decisiones deben conservar `Aplicado=false`. El exportador sólo admite directorios nuevos bajo `.cache/` o `docs/`, nunca `data/`.

- **17 pruebas nuevas: PASS, 17,050 s**. Incluyen miembros omitidos, cambios de fuente/ancla, promoción indebida de propuestas, estados, ventanas, herencia de separaciones y protección de destinos.
- **2.099 pruebas completas: PASS, 320,771 s**.
- **F0 y F1: PASS sobre una copia aislada de v5**, incluida su comparación global contra v4. No hubo nueva construcción de datos.
- Las tres planillas mantienen todas sus hojas y celdas frente a v5. Los demás archivos de salida, salvo el manifiesto de la copia, son idénticos byte a byte; el informe QA también es idéntico.
- El manifiesto de la copia verifica **125 entradas/código y12 salidas**. Se preserva el manifiesto histórico de v5, que registra sus123 entradas originales.
- **98 archivos de datos,264 documentos/artefactos y38 scripts anteriores permanecen idénticos byte a byte**. Cuatro exportaciones del lote se reprodujeron exactamente.

Al iniciar el turno, el entorno local había reaparecido en un estado v2. Se verificó la rama publicada `a1445c9` en GitHub:384 archivos locales ya coincidían con v5,6 coincidían exactamente con v2 y77 faltaban; no se encontraron archivos divergentes en el conjunto versionado. Se respaldaron los6 antiguos y se recuperó la versión publicada en la misma rama, conservando `.github/` ajeno a esta tarea. La recuperación no se presenta como una nueva revisión de datos.

## Reproducir y continuar

```bash
.venv/bin/python scripts/revisar_reservas_complejas.py \
  --salida .cache/reproduccion_lectura_lote6
```

El siguiente trabajo productivo es **implementar y probar las dos propuestas locales en una salida versionada aislada**, sin cambiar sus fuentes/anclas ni afectar otras voces o las continuidades existentes. Las tres reservas se mantienen abiertas y no deben desaparecer del seguimiento al aplicar esas dos propuestas.

No se consultó un nuevo PDF ni hubo subagentes o segundo revisor semántico. Las pruebas y la copia de QA son verificaciones técnicas, no revisiones semánticas independientes.
