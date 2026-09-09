# Lote 8 — clúster de constancias de Vergara (2026-09-09)

## Estado

**Lectura y decisión completas. Nada aplicado.**

`docs/continuidad_lote8_2026-09-09/lecturas.json` registra el texto completo de los 29
padres del clúster, sus hashes de fuente, el intervalo exacto de corte, la constancia y el
contexto del padre anterior. No se ejecutó ningún perfil nuevo: `data/releases/` sigue en
`continuidad_procedimental_v6`, sin sobreescritura de `data/processed/`.

| | |
|---|---|
| Lectura | `docs/continuidad_lote8_2026-09-09/lecturas.json` (801.724 bytes) |
| Padres leídos | 29 |
| Caracteres de origen leídos | 127.050 |
| Conservación del texto | verificada en los 29 |
| Corte aplicado | 0 |
| Enlace aplicado | 0 |
| Alertas cerradas | 0 |
| Base inmutable | `continuidad_procedimental_v6`, SHA `1dfce989…c7c4` |

## El hallazgo

El triaje del lote7 mostró que **29 de los 53 pares sin adjudicar comparten una sola
causa**: no es una duda de continuidad entre dos filas, es una fila que mezcla dos
segmentos.

Cada una de esas filas tiene la forma:

```
<aporte personal de Vergara>            205–4.434 caracteres
<espacio>
<En consecuencia|Con todo|Así|...> deja constancia que se acuerda por unanimidad…
                                       176–1.315 caracteres
Tipo_Acta = ACUERDO_CONSEJO
```

Es **exactamente el patrón que funcional-v4 ya resolvió** en los padres 4788, 4849 y 4899.
Allí la decisión fue: separar, conservar la atribución a Vergara como hablante de ambos
tramos, y no convertir el aporte personal en institucional por más que el resultado
pertenezca al Consejo.

El criterio existe, fue revisado y está curado. Estos 29 casos son instancias adicionales
del mismo criterio, no una regla nueva.

## Verificación de las precondiciones del criterio v4

Las 29 filas satisfacen **todas** las precondiciones que funcional-v4 exige; la verificación
es mecánica y reproducible:

| Precondición | Resultado |
|---|---|
| `Numero_Segmento == 1` | 29/29 |
| `Actor_Final == 'Rodrigo Vergara Montes'` | 29/29 |
| `Fuente_Actor == 'SUJETO_ROL_NOMBRE'` (explícita) | 29/29 |
| Texto presente literalmente en `data/raw` | 29/29 |
| Padre tiene exactamente 2 filas | 29/29 |
| `Tipo_Acta == 'ACUERDO_CONSEJO'` | 29/29 |
| Sin revisión institucional previa | 29/29 |
| El corte cae en un límite de oración | 29/29 |
| El tramo personal termina en `.` | 29/29 |
| Separador = sólo espacio | 29/29 |
| Tramo personal + separador + constancia == original | 29/29 |
| **Antecedente = última fila del padre anterior** | **29/29** |
| Antecedente: mismo actor, ancla propia, sin `Tipo_Acta`, sin alerta | 29/29 |

Rechazos: **ninguno**.

La última línea es la que da sentido al lote. En los 29 casos la intervención anterior de
Vergara es la **última** fila del padre anterior — ninguna voz se intercala — y empieza con
la fórmula de apertura:

> «El Presidente señor Rodrigo Vergara agradece el planteamiento del Vicepresidente señor
> Manuel Marfán e inicia su intervención expresando su reconocimiento al staff por el
> excelente análisis consignado precedentemente.»

Es decir: el tramo personal de estas filas **continúa una intervención ya empezada**, igual
que en 4788. No es una interpretación; es la misma estructura.

## Un caso que corrigió el contrato

La primera pasada del generador rechazó `RPM-2015-06-11:6863:1` con "padre anterior fuera
del contrato". La causa no era la fuente: era mi chequeo, que exigía que el padre anterior
tuviera **una sola** fila.

El padre 6862 tiene seis filas (intervienen el Fiscal, Alejandro Micco, Vergara). Su
**última** fila, `6862:6`, es la intervención de apertura de Vergara con ancla propia. El
antecedente correcto es esa fila, no el padre completo.

Corregido el contrato a "la última fila del padre anterior", los 29 pasan. Queda registrado
porque es el tipo de chequeo que, escrito apurado, habría descartado un caso legítimo.

## Qué falta

La lectura y la decisión están cerradas. Falta implementar, y no es poco:

1. `data/curation/refinamiento_funcional_v5.json` con los 29 intervalos y el hash de esta
   lectura.
2. Un módulo de refinamiento funcional que generalice `functional_refinements.py` a un
   conjunto no hardcodeado, con su propio hash de lecturas y de base.
3. Un perfil `procedimental-v7` en `preparar_data.py`, sin tocar el default `procedimental-v5`.
4. Validadores que exijan: conservación literal del texto, `ACUERDO_CONSEJO` conservado en
   la constancia, `CONTINUIDAD_EXPLICITA` del tramo personal hacia el anterior, `INSTITUCIONAL`
   en la constancia, y **ningún** cambio de hablante.
5. `auditar_continuidad_turnos` actualizado para que las 29 filas dejen de ser "candidatas a
   decisión" sin perder la tipificación.
6. Tests aislados + suite completa (la referencia es 2.129 OK).
7. Corrida real del perfil v7 en staging (~25 min) y entrega con comparación global de todos
   los campos y todos los grupos.

No lo aplico a medias en el mismo lote en que lo leí: la corrida es larga y los validadores
son los que impiden que un corte mal calculado se cuele como cambio correcto.

## Reservas

`780`, `2661` y `5252` siguen abiertas y visibles.

Las otras 24 filas sin adjudicar del lote7 conservan su causa registrada en
`docs/CONTINUIDAD_LOTE7_2026-09-09.md`; ocho requieren resolver antes una alerta de texto
dañado, catorce son separaciones correctas por diseño, una (`2685`) es una barrera de regla
y otra es una mención.
