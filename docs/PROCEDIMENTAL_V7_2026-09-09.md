# Entrega procedimental-v7 — separación funcional de 29 constancias de Vergara

## Estado

**Aplicado, validado y publicado.**

`data/releases/continuidad_procedimental_v7/` (14 archivos). Construido en staging,
publicado sólo después de pasar todos los controles. `data/processed/` y las entregas
v1–v6 no se tocaron.

| | |
|---|---|
| Perfil | `procedimental-v7` (explícito; el default sigue siendo `procedimental-v5`) |
| Base inmutable | `continuidad_procedimental_v6`, SHA `1dfce989…c7c4` |
| XLSX v7 | `84889a846ec0b3a2fce88d37f1d5a0a3676b33dcd962c428de7cdbb3c992d9a7` |
| XLSX final v7 | `d0b64842cd756df4c50d2960d9bbf01c4c45e5df28609d7b612c5d666593da75` |
| Registro | `data/curation/refinamiento_funcional_v5.json`, SHA `a0afd806…6901` |
| Lectura | `docs/continuidad_lote8_2026-09-09/lecturas.json`, SHA `5e1969a0…7b82` |
| Suite | **2155 tests OK** en 539,0 s |
| Controles bloqueantes | `pasa_controles_bloqueantes: True`, `errores: []` |
| Puerta F0 | `pasa: true` — 132 sesiones, 55 actores, 54 personas, 310 fórmulas |

## Qué cambió

Veintinueve filas mezclaban el aporte personal de Rodrigo Vergara con la constancia de
unanimidad, tipificadas `ACUERDO_CONSEJO` como un solo bloque. Cada una se dividió en dos.

Es el mismo criterio revisado en funcional-v4 para 4788, 4849 y 4899, extendido a los 29
casos estructuralmente idénticos que el triaje del lote7 aisló. No es una regla nueva.

| | v6 | v7 | Δ |
|---|---:|---:|---:|
| Filas | 9.694 | **9.723** | +29 |
| Grupos de turno | 9.234 | **9.234** | 0 |
| Grupos multifila | 358 | **387** | +29 |
| Máx. filas por turno | 11 | 11 | 0 |
| Filas alertadas | 467 | **484** | **+17** |
| Alertas cerradas | — | **0** | — |
| `CONTINUIDAD_EXPLICITA` | 379 | **408** | +29 |
| Refinamientos funcionales | 3 | **32** (3 v4 + 29 v5) | +29 |

Ninguna otra relación de turno cambió. `INSTITUCIONAL` se mantiene en 561: la constancia ya
era institucional dentro de la fila original y sigue siéndolo.

El linaje completo está en `linaje_funcional.csv`: 9.723 filas = 9.665 `INTEGRA` + 29
`PERSONAL` + 29 `CONSTANCIA`, con el intervalo exacto de cada tramo dentro de la fila
anterior y el SHA256 de cada texto.

## Las 17 alertas nuevas, y por qué no se evitaron

`DUPLICADO_NO_FORMULA` aparece en 17 de las 29 constancias porque **13 de ellas son
textualmente idénticas entre sí**, más dos pares adicionales:

> «En consecuencia, el Presidente señor Rodrigo Vergara deja constancia que se acuerda por
> unanimidad de los señores Consejeros mantener la Tasa de Política Monetaria en 5%…»

Eso no es un artefacto del corte: son 13 sesiones con la misma fórmula de cierre. El
constructor cuenta duplicados sobre los segmentos post-corte, así que al separar la
constancia del aporte personal la identidad quedó expuesta.

Se dejó la alerta. Eliminar texto para que no aparezca habría falsificado el corpus, y
cerrarla para mejorar una métrica está expresamente fuera de alcance. Es el mismo
tratamiento que funcional-v4 dio a 4849 y 4899.

Las otras 12 constancias son únicas y no generan alerta. Ninguna de las 29 filas personales
la genera: todas terminan en punto y ninguna se duplica.

## Comparación global

`comparacion_funcional.json`, `Pasa: true`. El esperado se deriva de la entrega v6 firmada y
de la lectura lote8, **no del constructor**; luego se compara fila por fila:

- 9.723 filas, todos los campos, sin excepciones globales.
- Membresía de los 9.234 grupos idéntica al esperado.
- `Alertas_Cerradas: 0`.
- `validate_refinements` sobre la salida real: sin errores.

Verificado además contra la entrega anterior:

| Invariante | Resultado |
|---|---|
| Reservas `780:2→780:3`, `2661:6→2661:7`, `5252:3→5252:4` | **separadas** |
| Enlaces v6 `2863:2→2863:3`, `3646:2→3646:3` | unidos |
| Las 6 continuidades procedimentales de v5 | unidas |
| `data/raw/consolidado_final.xlsx` | `c1cb7382…a512`, sin cambios |
| Entregas v4, v5, v6 | hashes sin cambios |

## Salvaguardas

`functional_refinements_v5.py` no confía en su propio JSON. Revalida la lectura contra la
entrega v6 y el origen antes de aplicar nada:

- las 29 filas siguen siendo `Numero_Segmento == 1`, `SUJETO_ROL_NOMBRE`, sin alerta previa;
- el texto del padre sigue coincidiendo con `data/raw` por SHA256;
- `personal + separador + constancia == original`, separador de sólo espacio, corte en
  límite de oración y aporte personal terminado en punto;
- **el antecedente es la última fila del padre anterior**, con ancla propia, sin `Tipo_Acta`
  y sin alerta — si otra voz se intercalara, el corte no aplicaría;
- `Revision_ID` debe coincidir con `FUNCIONAL_V5_{n:02d}_{padre}`: no es un campo libre.

`active_refinements` exige `intrapadre-v4` y el registro v4 intacto por hash; un perfil
menor no reproduce la base y se rechaza. Ninguno de los 29 padres tiene revisión
institucional, así que no se reconstruyó ninguna: verificado contra
`revisiones_continuaciones_acta.json`.

El hablante no cambia en ningún tramo. Vergara conserva la atribución del aporte personal y
de la constancia, aunque el contenido de ésta sea institucional — misma regla que v4.

## Dos correcciones hechas durante la implementación

**El contrato del antecedente.** La primera pasada del generador rechazó `6863` porque
exigía que el padre anterior tuviera una sola fila. El padre 6862 tiene seis (intervienen el
Fiscal y Alejandro Micco) y su última fila, `6862:6`, es la apertura de Vergara con ancla
propia. El antecedente correcto es la última fila, no el padre completo. Corregido el
contrato, los 29 pasan con 0 rechazos.

**Dos subreportes en el artefacto publicado.** El primer pase publicó un resumen que decía
`refinamientos_funcionales: 3` y un manifiesto que no registraba el registro v5, cuando se
habían aplicado 32 cortes. Ambos contadores se corrigieron en `qa_preparacion.py` y la
entrega se reconstruyó. Los datos de los tres pases son idénticos (verificado fila por
fila); sólo cambió el reporte. El hash de bytes del XLSX difiere entre pases por metadatos
de openpyxl, no por contenido.

## Reproducción

```
PYTHONPATH=scripts PYTHONHASHSEED=0 .venv/bin/python scripts/preparar_data.py \
    --perfil procedimental-v7 --destino <directorio nuevo>
```

El perfil predeterminado sigue siendo `procedimental-v5`; v7 es siempre explícito.

## Inventario actualizado

`docs/procedimental_v7_2026-09-09/` (`inventario_estado_v7.csv`, `resumen.json`), generado
por `scripts/inventario_procedimental_v7.py`. Rinde la cuenta completa de los 71 pares del
lote6 más los 29 límites internos que crea el corte: **100 filas**.

| Estado | Pares |
|---|---:|
| `SEPARACION_FUNCIONAL_APLICADA_V5` (agrupado en v7) | **29** |
| `SEPARACION_FUNCIONAL_V5_INTERNA` (límite nuevo del corte) | **29** |
| `SIN_ADJUDICACION_EN_ESTE_INVENTARIO` | **24** |
| `SEPARACION_RESPALDADA_PREVIAMENTE` | 10 |
| `SEPARACION_FUNCIONAL_V4` | 3 |
| `ENLACE_INTRAPADRE_APLICADO_V6` | 2 |
| Reservas (`780`, `2661`, `5252`) | 3 |
| **Total** | **100** |

Los 24 sin adjudicar llevan su causa medida, ninguno en blanco:

| Causa | Pares |
|---|---:|
| `DERECHA_ES_DOCUMENTO_LEIDO_POR_TERCERO` | 8 |
| `ALERTA_CONTEXTUAL_VIGENTE` | 7 |
| `DERECHA_SIN_FUENTE_PROPAGABLE` | 4 |
| `AMBOS_EXTREMOS_SIN_FUENTE_PROPAGABLE` | 3 |
| `POSIBLE_OTRA_VOZ` | 1 |
| `SIN_BARRERA_ESTRUCTURAL_IDENTIFICADA` (`2685`) | 1 |

Los 29 límites internos (`NNNN:1→NNNN:2`) son el propio corte y **deben seguir separados**:
la constancia es `INSTITUCIONAL` y no se une al aporte personal. El inventario lo declara
explícitamente para que no se lea como un enlace pendiente.

## Corrección al triaje del lote7

Al construir el inventario apareció un defecto en el triaje que había publicado: guardaba el
**extremo derecho** del par en cuatro causas y el **izquierdo** en las otras tres, así que su
primer campo no servía como clave de par. Los conteos por causa eran correctos — cada par
aparece una sola vez — pero no se podía cruzar con el inventario.

Se reescribió como `scripts/triaje_lote7.py`, que emite ambos extremos en cada registro y
falla cerrado si la clasificación cambia. Regenerado en
`docs/continuidad_lote7_2026-09-09/triaje_53.json` (versión 2): los conteos son **idénticos**
a la versión 1 (29/8/7/4/3/1/1), lo que confirma que sólo cambió la forma del registro.

## Suite

**2155 tests OK** en 539,0 s (2146 al publicar la entrega + 9 del inventario v7).

## Lo que queda abierto

Las 24 filas sin adjudicar conservan su causa medida. Ocho requieren resolver antes una
alerta de texto dañado, catorce son separaciones correctas por diseño o sin fuente
propagable, una (`2685`) es una barrera de regla medida y otra es una mención.

Las reservas `780`, `2661` y `5252` siguen abiertas y visibles.
