# Lote7: triaje de los53 pares sin adjudicación

Fecha: 2026-09-09
Base leída: `data/releases/continuidad_procedimental_v6/` (SHA-256 `1dfce989aa1ded2fb4bc99557750c48bd3d01ee5a690708044a659065e45c7c4`)
**Este lote no aplica enlaces ni cortes. No modifica datos ni publica una entrega nueva.**

---

## 1. Alcance

El inventario de v6 deja **53 pares** como `SIN_ADJUDICACION_EN_ESTE_INVENTARIO`. La acción
pendiente registrada era: *«Localizar fichas previas y comprobar su alcance antes de decidir
una nueva lectura.»* Este lote ejecuta esa acción y además mide la causa estructural de cada
par.

## 2. Correcciones a afirmaciones anteriores

Dos afirmaciones de turnos previos no resisten la verificación y se corrigen aquí.

**(a)** Se dijo que «los 53 no equivalen a casos nunca leídos». Cruzando los 53 contra
`lecturas.json` de lote2–lote6, las 24 continuidades entre padres, `continuidades_intrapadre_v1–v4`,
los `CASES` de lote4, `refinamiento_funcional_v4.json` y `auditar_continuidad_turnos.DECISIONS`,
**sólo 2 tienen decisión previa registrada**:

| Par | Decisión previa | Fuente |
|---|---|---|
| `RPM-2009-08-13:2685:2 → 2685:3` | `CONTINUIDAD_PLAUSIBLE_CON_AVISO_DUPLICADO` | `auditar_continuidad_turnos.DECISIONS` + `docs/AUDITORIA_CONTINUIDAD1_2026-09-09.md` |
| `RPM-2010-01-14:2885:2 → 2885:3` | `NO_SIMULAR_POR_DANO` | idem |

Los otros **51 no tienen adjudicación en ningún registro**. Un muestreo de 22 de esos padres
en `docs/*.md` dio **1 mención**. La afirmación heredada sólo es cierta para 2 casos.

**(b)** Se dijo que «37 de los 53 tienen barrera estructural declarada y 16 no», contando
coincidencias exactas de la columna `Indicadores`. Ese conteo estaba mal delimitado: agrupaba
por cadena literal en vez de por causa. El triaje medido de la sección 4 reemplaza esa cifra.

## 3. Método

Para cada uno de los 53 pares se midió, sobre la entrega v6 y sin modificar nada:

- `Tipo_Acta` y `Fuente_Actor` de ambos extremos.
- Alertas vigentes de ambos extremos, y si son **contextuales** (`context_warnings.has_context_warning`).
- Posición de la fórmula de constancia de unanimidad dentro del texto del extremo derecho y
  cuántos caracteres de aporte personal la preceden.
- Si la fila es **candidata a decisión de F0**, calculado con `qa_gate_f0.extract_decision_rows`,
  la misma función que usa el gate.

## 4. Triaje medido de los53

| Causa | Pares | Naturaleza |
|---|---:|---|
| Aporte personal + constancia de unanimidad en **una sola fila** `ACUERDO_CONSEJO` | **29** | Patrón funcional-v4 sin cubrir |
| El extremo derecho es un documento leído por un tercero (`LECTOR_DOCUMENTO_REVISADO`) | 8 | Separación correcta por diseño |
| Alerta contextual vigente (`TEXTO_DANADO_POR_COTEJAR` ×6, `CARGO_EN_DISCURSO_POR_VERIFICAR` ×1) | 7 | Requiere resolver la alerta primero |
| Extremo derecho `CONTEXTO_REVISADO`, sin fuente propagable | 4 | Separación correcta por diseño |
| Ambos extremos `CONTEXTO_REVISADO` (Valdés, 2005) | 3 | Separación correcta por diseño |
| `POSIBLE_OTRO_HABLANTE_O_MENCION` | 1 | Requiere lectura |
| Sin barrera estructural identificada (`2685`) | 1 | Barrera de regla, ver abajo |
| **Total** | **53** | |

**15 pares son separaciones correctas por diseño** (documento leído por tercero + extremos sin
fuente propagable): el corpus ya prohíbe convertir `CONTEXTO_REVISADO` en ancla y distingue
autor ≠ lector ≠ hablante. **8 requieren resolver antes una alerta o una duda de otra voz.**
**30 tienen una causa concreta identificada** y son el trabajo real pendiente.

## 5. Hallazgo principal: el patrón funcional-v4 quedó cubierto sólo en3 padres

`funcional_v4` separó aporte personal + constancia de unanimidad en exactamente tres padres
(verificado: `functional_refinements.PARENTS == {4788, 4849, 4899}`). Comparación directa:

**`4788` — ya resuelto por funcional-v4:**

| Fila | Tipo | Car. | Contenido |
|---|---|---:|---|
| `4788:1` | nulo | 1.946 | Aporte personal de Vergara, `CONTINUIDAD_EXPLICITA` desde el padre anterior |
| `4788:2` | `ACUERDO_CONSEJO` | 185 | Sólo la constancia |

**`5330` — mismo patrón, sin resolver:**

| Fila | Tipo | Car. | Contenido |
|---|---|---:|---|
| `5330:1` | `ACUERDO_CONSEJO` | **2.197** | **2.073 car. de aporte personal de Vergara** + la constancia al final |
| `5330:2` | `ACUERDO_CONSEJO` | 1.966 | Acuerdo del Consejo |

Hay **29 filas así**, todas de Rodrigo Vergara Montes, entre `RPM-2012-07-12:4973:1` y
`RPM-2015-06-11:6863:1`, sin solape con `{4788, 4849, 4899}`. El aporte personal ocupa entre
**258 y 4.487 caracteres** (63–97% de la fila).

Consecuencia causal verificada: al llevar la fila completa `Tipo_Acta = ACUERDO_CONSEJO`,
`annotate_turns` la marca `institutional` y bloquea la continuidad con el padre anterior. Eso
es exactamente lo que mantiene el clúster Vergara en el inventario: **29 de los 53 pares (55%)
tienen esta única causa**.

**Restricción medida:** las **29 son candidatas a decisión de F0**. Por tanto el tipo
`ACUERDO_CONSEJO` no puede eliminarse: cualquier separación debe conservar la tipificación en
el tramo de constancia, tal como hizo funcional-v4, o F0 fallará con «decisión sin tipificar».

## 6. `2685`: la barrera es de regla, no de juicio

`RPM-2009-08-13:2685:2 → 2685:3` es el único par de los 53 con el mismo perfil de indicadores
que los dos enlaces aplicados en v6. Lectura completa del padre 2685:

- `2684:1` De Gregorio da paso a la votación (81 car.).
- `2685:1` Claro, su voto (3.300 car.).
- `2685:2` «A continuación, es el turno del Consejero señor Enrique Marshall, quien comienza su exposición agradeciendo al staff por el apoyo brindado.» — 139 car., `CONTEXTO_REVISADO`, alerta `DUPLICADO_NO_FORMULA`.
- `2685:3` Exposición completa de Marshall, 6.624 car., `SUJETO_NOMBRE`.
- `2686:1` Desormeaux (5.794 car.).

Mismo hablante, contiguo, sin otra voz intercalada. El caso aplicado en v1, `2796:2 → 2796:3`,
abre con **la misma frase literal**.

Se comprobó empíricamente cuál es la barrera:

```text
matching_intrapara(2685:2, 2685:3, prueba_declarada) -> None
matching_intrapara(2685:2 sin alerta, 2685:3, ...)   -> APLICA
```

`matching_intrapara` rechaza cualquier extremo que lleve **algún** `Motivos_Revision`, aunque
no sea alerta contextual: `has_context_warning('DUPLICADO_NO_FORMULA') == False` (verificado).

Es decir: la reserva de `2685` **no depende de una lectura**, depende de una regla general que
no distingue tipos de alerta. Cambiarla afectaría a las 17 pruebas intrapadre existentes y a
todas las futuras, y la salvaguarda «no introducir reglas globales para resolver un caso
particular» lo prohíbe. **Se mantiene la reserva** y se registra que lo que falta decidir es la
regla, no el caso.

## 7. Resultado del lote

| | |
|---|---:|
| Pares triados | 53 |
| Enlaces aplicados | **0** |
| Cortes aplicados | **0** |
| Alertas cerradas | **0** |
| Filas / grupos / alertas de la base | 9.694 / 9.234 / 467 (sin cambio) |
| Separaciones confirmadas como correctas por diseño | 15 |
| Causas concretas identificadas | 30 |
| Reservas que requieren trabajo previo | 8 |

Las tres reservas de lote6 (`780`, `2661`, `5252`) siguen abiertas y no fueron reexaminadas en
este lote.

## 8. Próximo trabajo, en orden

1. **Lote funcional-v5**: leer completos los 29 padres del clúster Vergara y separar aporte
   personal de constancia, conservando `ACUERDO_CONSEJO` en el tramo de constancia y la
   evidencia de decisión de F0. Requiere salida versionada nueva, pruebas completas, F0/F1 y
   comparación global. **No hacerlo por regla**: padre por padre, con intervalos exactos.
2. Decidir la regla de alertas no contextuales en `matching_intrapara` y, sólo entonces,
   reevaluar `2685`.
3. Resolver las 6 alertas `TEXTO_DANADO_POR_COTEJAR` y la de `CARGO_EN_DISCURSO_POR_VERIFICAR`
   por su propio mérito, sin usar el enlace como incentivo.
4. Leer `2430` (`POSIBLE_OTRO_HABLANTE_O_MENCION`).
5. Las tres reservas de lote6: `780` requiere el acta RPM95 del 13-07-2006; `2661` requiere el
   criterio de confirmaciones narradas; `5252` requiere la frontera acta/persona.

## 9. Límites de este lote

- Es un triaje estructural medido sobre v6, **no** una lectura semántica completa de los 53
  padres. Sólo `2685` fue leído completo en este lote.
- La clasificación «separación correcta por diseño» se apoya en las reglas vigentes del motor,
  no en una relectura de cada acta.
- No hay segundo revisor semántico ni cotejo PDF nuevo.
