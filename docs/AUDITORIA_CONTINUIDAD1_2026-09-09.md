# Auditoría de continuidad y alternancias — 1 (2026-09-09)

**Base:** `b62ee7585c5cc94a74b670203dd0ceaf99c95112`.
**Estado:** **auditoría y simulación aislada; ningún enlace aplicado a los datos**.

## Resultado principal

La lectura respalda dos candidatos de continuidad dentro de un mismo padre:

1. **2796: Marshall 343 → 5.287 caracteres**, conservando además su continuación ya enlazada de **2.105 caracteres en 2797**.
2. **3012: De Ramón 375 → 1.867 caracteres**, sin incorporar la cesión presidencial previa.

La simulación agrupa sólo esos dos pares. Pasaría de **9.257 a 9.255 grupos** y cambiaría la pertenencia de **tres filas** en ese escenario, sin alterar textos, actores, roles, métodos, anclas o alertas. **La base publicada sigue con 9.257 grupos y todos sus datos intactos.** No se ha corregido aún la agrupación productiva.

## Inventario sistemático, no lista de errores

Se recorrieron las 9.691 filas actuales buscando pares **contiguos**, de la **misma persona y fecha**, que estuvieran en grupos distintos. Se excluyó al Consejo como actor de ambos extremos.

| Unidad | Cantidad |
|---|---:|
| Pares inventariados | **92** |
| Dentro del mismo padre | 43 |
| Entre padres distintos | 49 |
| Sólo indicador de fuente contextual izquierda no propagable, con derecha explícita | **21** |
| De esos 21, sin motivos de revisión en ninguno de los extremos | 20 |

Los indicadores no son excluyentes: 33 pares tienen tipo de acta/documento, 15 una barrera léxica izquierda, 8 una alerta contextual y 1 posible otra voz; también hay fuentes no propagables a izquierda o derecha. **Estos recuentos no equivalen a errores ni a propuestas aprobadas.** `Tipo_Acta` puede corresponder a un documento personal, no necesariamente a una narración del Consejo.

Los 21 pares del patrón contextual/nominal están dentro del mismo padre. Uno, 2685, conserva un aviso de duplicado aunque no active el indicador de alerta contextual. Por tanto, no se los denomina automáticamente «limpios» ni se eliminan sus reservas.

La auditoría de este lote leyó **cuatro pares de los 92** y añadió **dos controles negativos de alternancia/acta**, fuera de ese inventario de pares contiguos. Los otros 88 no se revisaron individualmente en este lote; algunos tienen controles anteriores y no deben contarse como 88 casos nunca leídos.

## Qué se leyó

Se leyeron completos **siete padres: 2796, 2797, 3012, 2685, 2885, 1901 y 2779**, con **28.893 caracteres de origen**. Se observaron además ventanas de hasta 250 caracteres de los vecinos externos, junto con la partición actual. Una ventana **no cuenta como lectura completa del vecino**, salvo cuando también se seleccionó ese padre: 2796 y 2797 sí se leyeron ambos completos.

Selección dirigida: un voto extenso y una intervención más breve para evaluar continuidad; un agradecimiento con duplicado y un voto con daño como contraste; y dos controles donde se debe mantener la separación. No es una muestra representativa.

## Lectura y decisión por caso

### 2796–2797: exposición y voto de Marshall

Se conservan físicamente **Claro 5.097 → Marshall 343 → Marshall 5.287**, seguidos de **Marshall 2.105** en 2797.

El tramo de 343 abre la exposición y resume el escenario; «En el frente externo, el señor Enrique Marshall…» desarrolla ese mismo argumento. No hay otra voz intercalada. El desarrollo termina planteando el retiro de la FLAP; 2797 retoma «las opciones para ello», precisa el calendario y concluye el voto.

La continuidad discursiva está respaldada por el contenido y la secuencia, no sólo por el nombre. El escenario une el inicio de 343 con el grupo que ya contiene 5.287 + 2.105, sin perder el enlace 2796→2797. **Claro permanece separado.** El texto `ALAR` al final de 2797 se conserva: agrupar el voto no certifica su OCR.

### 3012: De Ramón continúa después de la introducción anafórica

Se conservan **Presidente 109 → De Ramón 375 → De Ramón 1.867**.

«quien hace presente» inicia los comentarios de De Ramón sobre escenario y terremoto; «El señor de Ramón indica, asimismo» continúa el argumento de inflación, reconstrucción, tipo de cambio y brechas, sin otro participante entre ambos.

El escenario agrupa únicamente esos dos tramos de De Ramón. **No añade la cesión presidencial.** La ancla del tramo anafórico sigue nula y la del nominal sigue siendo propia. La ficha anterior del lote 5 dejó explícitamente los grupos separados y no registró un enlace; esa ficha histórica no se modifica.

### 2685: continuidad plausible, duplicado conservado

Se leyó todo el padre: **Claro 3.300 → Marshall 139 → Marshall 6.624**. El agradecimiento y el desarrollo nominal posterior son compatibles con la misma intervención de Marshall, pero el agradecimiento mantiene **`DUPLICADO_NO_FORMULA`**.

Este par queda **fuera de la simulación conservadora**, que exige extremos sin motivos de revisión. Es una reserva de selección, no una declaración de que el duplicado sea una barrera contextual del motor actual. No se deduplica la cláusula ni se agrega una nueva regla global. Se conservan también `opiruon`, `vahos`, `tempora l` y los demás residuos del texto.

### 2885: no levantar daño para agrupar el voto

Marfán agradece durante 165 caracteres y desarrolla el voto durante 2.400. Hay continuidad temática reconocible, pero el desarrollo conserva **`TEXTO_DANADO_POR_COTEJAR`** y termina **`Para concluir con la votación,.`**.

No se simula una unión que levante esa advertencia. No se traslada la cola a 2886 ni se convierte el agradecimiento contextual en ancla global.

### 1901: la reanudación impide unir ambos aportes presidenciales

**Presidente 130 → acta 74 → Presidente 178.** Hay un registro institucional entre suspensión/anuncio y cesión de palabra. Las dos intervenciones presidenciales no son contiguas y permanecen separadas; no se salta el acta porque coincida el actor.

### 2779: conservar las alternancias y la modalidad del asentimiento

**Cowan 222 → Soto 22 → Marshall 366.** Son aportes diferenciados. «El señor Soto asiente,» se mantiene sin inventarle palabras transcritas. La respuesta contrastiva de Marshall no pertenece a Soto ni a Cowan.

La presencia de Soto en las ventanas anterior y posterior no autoriza una fusión a través de las otras voces. Este es un control negativo de alternancias, no un par contiguo del mismo actor dentro de los 92.

## Por qué no se aplicó automáticamente

El motor actual mantiene `CONTEXTO_REVISADO` sin ancla global. El registro productivo de continuidad revisada admite **extremos de padres consecutivos**, pero no un enlace entre dos tramos del mismo padre. Las dos propuestas necesitan precisamente ese alcance intrapadre.

No se amplía el motor mediante una regla «mismo actor = mismo turno». Se añade un auditor independiente, [`scripts/auditar_continuidad_turnos.py`](../scripts/auditar_continuidad_turnos.py), que:

- inventaría sin aprobar los pares;
- exige evidencia de los siete padres y las decisiones de contraste;
- sólo simula los dos pares enumerados;
- verifica que los grupos afectados no contengan miembros adicionales sin leer;
- conserva el enlace existente de Marshall a 2797 y todas las otras agrupaciones;
- exporta una tabla **`SIMULADO_NO_APLICADO`**, sin escribir en `data/`.

La simulación cambia una **etiqueta de grupo de escenario**, no ejecuta todavía la nueva lógica productiva de `Relacion_Turno` o `ID_Antecedente_Continuidad`. Conserva las etiquetas actuales como referencia: una futura ejecución completa podría renumerar otros IDs de grupo sin cambiar sus miembros. **Tres filas del escenario no significa necesariamente tres celdas cambiadas en un pipeline regenerado.**

## Comparación verificable

| Indicador | Publicado | Sólo escenario |
|---|---:|---:|
| Grupos | **9.257** | **9.255** |
| Pares unidos en el escenario | 0 | 2 |
| Filas con distinta pertenencia de grupo | 0 | 3 |
| Filas físicas | 9.691 | 9.691 |
| Textos, actores, roles, métodos y anclas | Sin cambios | Sin cambios |
| Enlaces previos perdidos | 0 | 0 |
| Alertas cerradas | 0 | 0 |

**1.917 pruebas locales pasan (+20), en 130,628 s.** Se verifican inventario, evidencia, exclusión de reservas, controles de no fusión, pertenencia exacta de los grupos, conservación de miembros, rechazo de ampliaciones y CLI reproducible sin sobrescritura.

Los **27 archivos de datos**, los **34 artefactos de los siete lotes anteriores**, los dos módulos productivos de continuidad y los tres validadores de seguimiento previos permanecen idénticos byte a byte a `b62ee75`. Siguen vigentes las 24 pruebas productivas de continuidad registradas. Las cuatro exportaciones nuevas se reprodujeron byte a byte.

No hubo nuevo cotejo PDF, revisión humana independiente, pipeline productivo, F0/F1 o CI remota. Siguen **465 filas alertadas / 395 padres alertados**; la entrega de datos y QA permanece en LOOP32. La subcola de comas sigue en 167/167 y las tres reservas del lote 7 permanecen abiertas.

## Próximo paso concreto

Preparar una **aplicación productiva acotada sólo de los dos enlaces respaldados**, con un tipo de prueba intrapadre que preserve el comportamiento previo:

1. Registrar los extremos y sus evidencias, sin promover anclas contextuales.
2. Mantener el enlace de Marshall hacia 2797 y los controles negativos de acta, alternancia, duplicado y daño.
3. Tratar las fichas anteriores como evidencia histórica versionada, no reescribirlas o silenciar sus pruebas cuando cambie la agrupación vigente.
4. Ejecutar pipeline aislado, comparación global de pertenencias —no sólo numeración— y validaciones F0/F1 antes de reemplazar la entrega productiva.

No se propone aplicar en bloque los otros pares del inventario.

## Artefactos y reproducción

- [Padres leídos, decisiones y dos propuestas](auditoria_continuidad1_2026-09-09/revisiones.json)
- [Inventario de 92 pares, no aprobaciones](auditoria_continuidad1_2026-09-09/inventario.csv)
- [Seis decisiones y controles](auditoria_continuidad1_2026-09-09/decisiones.csv)
- [Tres cambios sólo de escenario](auditoria_continuidad1_2026-09-09/cambios_solo_escenario.csv)
- [Resumen](auditoria_continuidad1_2026-09-09/resumen.json) · [Verificación](auditoria_continuidad1_2026-09-09/verificacion.json)

```bash
.venv/bin/python scripts/auditar_continuidad_turnos.py \
  --revisiones docs/auditoria_continuidad1_2026-09-09/revisiones.json \
  --salida .cache/auditoria_continuidad1_repro
.venv/bin/python -m unittest discover -s tests
```

El destino debe ser nuevo; el auditor no permite sobrescribir entradas o exportaciones existentes.
