# Cuarto bloque: votos, complementos y retornos de exposición

**Fecha:** 2026-09-07. **Inicio:** 9.235 filas / 623 alertas / 318 pruebas.
**Publicación:** **9.245 filas / 618 alertas / 339 pruebas; F0/F1 aprobados.**

Se completaron **tres ciclos consecutivos**: nueve padres pasan de 12 a 22
segmentos en total, con **diez filas adicionales**. Hay además tres padres
con cambios sólo de metadatos, detallados abajo. No se modificó el Excel de
origen ni se reconstruyeron frases dañadas. El bloque terminó y está publicado;
**no hay un proceso activo en segundo plano**.

## Entregables

- [Excel final](../data/processed/consolidado_base_referencia_final.xlsx).
- [Seguimiento de las 783 originales y cola vigente](../data/processed/revision_783.xlsx).
- [Nueve padres: hashes, IDs anteriores y 22 segmentos completos](cambios_loop4_2026-09-07.csv).
- [Tres cambios sólo de metadatos](metadatos_loop4_2026-09-07.csv).
- [Comparación antes/después y verificaciones globales](comparacion_loop4_2026-09-07.json).
- [Punto de reanudación](estado_revision_loop4_2026-09-07.json).

Los padres son IDs de origen; los IDs de fila pueden renumerarse. El informe
[del bloque anterior](REVISION_LOOP3_2026-09-07.md) conserva su valor histórico,
no describe las cifras actuales.

## Ciclos y decisiones

| Ciclo | Padres estructurales | Filas del ensayo | Pruebas |
|---:|---|---:|---:|
| 1 | 3800, 3810, 3813 | 9.237 | 325 |
| 2 | 3887, 3906, 4220 | 9.241 | 334 |
| 3 | 4224, 4341, 4357 | 9.245 | 339 |

### Ciclo 1 — Votación y advertencia del Vicepresidente

- **3800, 2011-02-17: Soto → Marfán (141 / 710 caracteres).** Soto responde
  que se prepara una minuta. `Por último, el señor Vicepresidente comenta…`
  inicia la advertencia de Marfán sobre expectativas; `Indica…` y `En otras
  palabras…` siguen con él. La identificación del cargo se comprueba en la
  misma sesión, incluido el entorno 3799 y la votación 3812/3813.
- **3810, misma sesión: Claro → Marshall (6.479 / 153).** Se conserva completa
  la fundamentación y voto de Claro. `Al continuarse con la votación… Marshall
  comienza…` es el agradecimiento del siguiente votante, no de Claro. Se conserva
  el daño literal `staff e\ apoyo`. **3810 → 3811** queda enlazado como el mismo
  turno de Marshall, cuyo análisis y voto en el siguiente padre no se recortan.
- **3813, misma sesión: Marfán → Presidente → Consejo (1.131 / 2.571 / 1.806).**
  `Al concluir con la votación…` inicia el análisis del Presidente, antes
  absorbido por Marfán. Incluye su voto y declaración de unanimidad; el acuerdo
  y comunicado siguen siendo institucionales. El padre continúa teniendo tres
  segmentos: cambia el límite entre voces, no sólo el número de filas.
  Se conserva **3812 → 3813** para la intervención de Marfán.

Se añadió una revisión individual para 3800 y se reconocieron dos prefijos
completos de votación: `Al continuarse con la votación` y `Al concluir con la
votación`. El barrido del consolidado los encontró sólo en 3810 y 3813. Siguen
exigiendo sujeto y predicado válidos, fuera de citas y sin convertir referencias
en hablantes. 3810 y 3813 no requieren entradas de curación individual.

### Ciclo 2 — Texto concatenado y opiniones distintas

- **3887, 2011-03-17: Claro → Marshall (5.698 / 2.667).** La fuente conserva
  `a 4%.` antes de `En consecuencia…` y termina la frase de Claro en
  `vota por aumentar la tasa`, sin puntuación. Se delimita individualmente
  `Al continuar con la votación… Marshall comienza…`, conservando su
  agradecimiento y toda su exposición posterior. **No se movió `a 4%.` ni se
  completó la frase.** 3888 desarrolla la continuación explícita de Marshall.
- **3906, 2011-04-12: Presidente → Claro (135 / 122).** El Presidente plantea
  mayor inflación y mayor crecimiento; Claro contrapone mayor inflación y
  menor crecimiento. `en tanto que…` introduce una opinión distinta, no una cita.
- **4220, 2011-08-18: Presidente → Lehmann → Herrera (120 / 52 / 177).**
  El Presidente propone revisar las referencias de la Zona Euro; Lehmann
  se compromete a revisar el gráfico; Herrera señala que el spread alternativo
  arroja los mismos resultados. No se atribuyen los tres actos al Presidente.

Se añadieron tres revisiones acotadas, incluida una concatenación explícita
para 3887. Los cortes interiores requieren hash, límites y sujeto compatible;
no se generalizó el corte por mayúsculas o por cada `en tanto que`.

Se incorporó el predicado `se compromete a revisar`. Se leyeron sus cuatro
ocurrencias (4220, 4338, 5231 y 5647), con estos resultados adicionales:

- **5231:** conserva íntegros texto y actor Lehmann. El método pasa de
  `NOMBRE+VERBO` a `SUJETO_NOMBRE`; su relación pasa a `INICIO_EXPLICITO` y ya
  no genera aviso de atribución legada. Se mantiene su exposición completa.
- **5647:** aparece un aviso nuevo de posible otro hablante. El Presidente
  observa diferencias de paridades y Lehmann se compromete a revisar la
  información; sigue una exposición sobre intervenciones cambiarias. **Queda
  pendiente delimitar ese compromiso y la continuación.** No se cambió el actor
  ni se asignó automáticamente todo el resto a Lehmann.
- **4338:** no cambia: el compromiso sin nuevo sujeto continúa la exposición
  de Lehmann. No se repararon los daños literales que contiene el padre.

### Ciclo 3 — Retornos de Lehmann y complemento de Marfán

- **4224, 2011-08-18: Cowan → Lehmann (441 / 966).** Después de la explicación
  de Cowan sobre financiamiento en dólares, `Al proseguir con su presentación…`
  devuelve la voz a Lehmann. Se mantienen juntos CDS, Italia, España, bancos
  y el ejemplo de Société Générale. 4225 continúa con Lehmann.
- **4341, 2011-10-13: Presidente → Lehmann → Marfán → Lehmann
  (134 / 75 / 95 / 245).** Se separa el complemento de Marfán sobre las
  garantías; la precisión siguiente de Lehmann sobre países AAA no se atribuye
  a Marfán. La revisión termina antes de `El señor Lehmann precisa…` y se
  verifica el intervalo completo, no sólo una coincidencia con su comienzo.
- **4357, misma sesión: Marfán → Lehmann (654 / 580).** La alusión entre rayas
  a lo que Lehmann denomina especulativo sigue dentro del comentario de Marfán.
  El retorno real comienza en `Al finalizar su presentación…`; petróleo,
  convergencia y Libia permanecen con Lehmann. 4358 agradece su presentación
  antes de dar paso al escenario interno.

Son otras tres revisiones individuales. No se añadió una regla general que
atribuya todo cierre de presentación al expositor más próximo.

## Continuidad: texto y agrupación no son lo mismo

Se conservan las exposiciones completas y los cambios de persona efectivamente
identificados. Hay **301 grupos multipárrafo**, frente a 300: se recuperó el
ancla explícita de **3810 → 3811**.

**No se fuerza un `ID_Turno` compartido desde `CONTEXTO_REVISADO`.** En particular,
3887 → 3888 y 4224 → 4225 conservan el actor correcto y la continuidad textual
leída, pero siguen sin agruparse automáticamente desde esos límites revisados.
La agrupación exige evidencia admisible por su política de anclas; no se alteró
esa política ni se simuló que una decisión contextual fuera un ancla automática.

## Verificación de alcance y publicación

- **339 pruebas aprobadas**, 21 nuevas: secuencias, longitudes, conservación,
  hashes, límites, sujetos incompatibles, citas, daño literal, continuaciones,
  referencias y nueva alerta sin adjudicación en 5647.
- Tres construcciones aisladas comparadas con la base inicial; pipeline completo
  posterior con F0/F1 y publicación. El contenido publicado coincide con el
  tercer ensayo.
- Comparación de los **7.219 padres**: exactamente los nueve previstos cambian
  segmentación/actor; sólo **3811, 5231 y 5647** cambian los metadatos indicados.
  No hay otros cambios en texto, actor, cargo, fuente, tipo de acta, motivos,
  relación, categorías o duplicados de los padres restantes, descontando IDs
  renumerados y notas que los contienen. El estado de revisión acompaña el
  cambio de aviso en 5231/5647.
- **17 enlaces previos comprobados**: los 16 protegidos del bloque anterior y
  3812 → 3813; además del enlace nuevo 3810 → 3811. La partición de grupos no
  afectados sigue igual. Se mantienen las dos exposiciones de García de once
  filas, padres 60–70 y 142–152.
- **70 revisiones de hablante**, siete nuevas; las 63 anteriores siguen idénticas.
  Las ocho anotaciones actuales de menciones permanecen idénticas y conservan
  sus avisos, incluida la atribución legada adicional de 4574.
- **48 hashes de entradas/código y 10 de salidas verificados**. El Excel de origen
  sigue idéntico a `HEAD`. Se conserva el texto ignorando sólo espacios:
  **2.048.560 palabras**, 9.244 bloques en 9.245 filas físicas, máximo 31.948
  caracteres por celda, 8.853 grupos de turno y máximo once filas por grupo.
- 132 sesiones, 310 contrastes TPM y sin errores bloqueantes. Estos controles
  comparten reconocedores: **no son revisión semántica independiente**.

## Alertas y pendientes

**623 → 618 filas con alertas.** Los motivos cambian así:

| Motivo | Antes | Ahora |
|---|---:|---:|
| Posible otro hablante/mención | 87 | 79 |
| Final sin puntuación | 240 | 244 |
| Atribución heurística legada | 259 | 258 |

Nueve pasajes dejan de generar el aviso de otro hablante; aparece uno nuevo en
5647. Los cuatro avisos nuevos de puntuación son la frase truncada de Claro en
3887 y las comas conservadas antes de nuevos hablantes en 3906, 4220 y 4341.
Los motivos restantes no cambian. **Las alertas se superponen; no son errores
confirmados ni su disminución una medida de pureza semántica.**

En las 783 originales: **440** pendientes de lectura contextual, 59 fórmulas,
72 métodos actualizados, 123 cambios por comparación, 65 correcciones dirigidas,
siete breves, ocho menciones históricas, seis identidades, dos repeticiones y
una continuidad. Por tipo: 142 lecturas del agente, 195 comparaciones y 446
triajes; 593 intervalos originales siguen solapándose con alertas actuales.
Son estados de intervalos, no cierres completos de sus padres. Las ocho
anotaciones de menciones actuales se cuentan aparte.

Quedan **63 candidatos** bajo el filtro de otro hablante sin anotación de
mención, frente a 71: salen nueve y entra 5647. El filtro no agota los pendientes.
Siguen 3191 y 2126 por sujetos conjuntos, 780 por cotejo documental, 2661/2704
por confirmaciones pasivas y 2667/3107 por daños de fuente. Se añade 5647;
no se certifica su atribución heredada. Faltan la cola restante, las variantes
de identidad, repeticiones sustantivas y una muestra semántica independiente
con y sin alertas. **No hubo nuevo cotejo PDF ni revisión humana independiente.**
