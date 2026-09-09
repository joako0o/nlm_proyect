# Entrega procedimental-v6: dos enlaces intrapadre del lote6 aplicados

Fecha: 2026-09-09
Rama de trabajo: `arena/01a08804-nlm-proyect`
Entrega publicada: `data/releases/continuidad_procedimental_v6/`

---

## 1. Verificación previa del estado recuperado

Antes de editar se comprobó el estado real del repositorio, no el descrito de memoria.

| Comprobación | Resultado |
|---|---|
| HEAD de la rama | `fdb1e13 Merge pull request #3 from joako0o/arena/01a07d66-nlm-proyect` |
| PR #3 | **Incorporada en `main`**; su contenido está presente en esta rama |
| Árbol de trabajo al iniciar | Limpio |
| `data/releases/` | v1, v2, v3, funcional_v4 y **procedimental_v5 completos** |
| `docs/continuidad_lote6_2026-09-09/` | Presente con sus seis archivos |
| SHA-256 base v5 | `4da18c4e86f583fdf4d5d0cd9be49b9aac20fb40379cd391b5f4c7763cf9e168` — coincide con el traspaso |
| SHA-256 base funcional-v4 | `a8038f8c18933990a84a870fb607f2053e8daccc0dbea634dc612635fe41a5df` — coincide |
| SHA-256 `data/raw/consolidado_final.xlsx` | `c1cb73821242a7dcb20a75aef671598a9a6901201318a1beb3f9723c9aa4a512` — coincide |
| SHA-256 `refinamiento_funcional_v4.json` | `d636f4a6f33bdef932956ca13834f247daf6cafd5d54bcb50440283a701220b8` — coincide |
| SHA-256 lecturas lote5 | `81aa9bfb93060b00c0ba4847963e2f1e0d583dddbc36399de12083d9dbbb1768` — coincide |
| SHA-256 lecturas lote6 | `0b1affeef2473519d387275f4eb3bf4f8788216db9756634091cad8837bd2aec` |

La advertencia del traspaso sobre una copia local incompleta **no se reprodujo aquí**: no fue
necesario recuperar nada ni se borró ningún archivo.

Métricas de v5 medidas directamente desde su XLSX antes de tocar nada:

| Métrica | Medido | Traspaso |
|---|---:|---:|
| Padres originales | 7.219 | 7.219 |
| Sesiones | 132 | 132 |
| Filas físicas | 9.694 | 9.694 |
| Bloques de texto | 9.693 | 9.693 |
| Grupos `ID_Turno` | 9.236 | 9.236 |
| Grupos de varias filas | 357 | 357 |
| Máximo de filas por grupo | 11 | 11 |
| Filas alertadas | 467 | 467 |
| Padres con alertas | 397 | 397 |

La firma de grupos de la base v5 reproduce la del paquete de lectura del lote6
(`3cba8cae204199c24b25b551e08941b77f7cd956b59287eefd38a828a1cc52b4`), y la selección
intrapadre sobre v5 devuelve exactamente los cinco casos del lote6. La lectura del lote6 es
por tanto reproducible sobre la base vigente.

Suite completa antes de cualquier cambio: **2.099 pruebas, OK**.

---

## 2. Revisión semántica independiente de los dos casos

Se leyeron los padres completos y todos los miembros de sus grupos, más las ventanas vecinas.

### 2.1 `RPM-2010-01-14:2863:2 → 2863:3`

Secuencia literal del acta:

| Fila | Hablante | Fuente | Caracteres | Contenido |
|---|---|---|---:|---|
| `2862:2` | Pablo García Silva | `SUJETO_ROL_SESION` | 1.009 | Explica la reconstrucción del IPC de vestuario |
| `2863:1` | Manuel Marfán Lewis | `SUJETO_ROL_SESION` | 106 | «El señor Vicepresidente consulta si esa reconstrucción permitió ver si se le habían quitado puntos al IPC**,**» |
| `2863:2` | Claudio Soto Gamboa | `CONTEXTO_REVISADO` | 63 | «respondiendo el señor Soto que no, porque fue un suavizamiento.» |
| `2863:3` | Claudio Soto Gamboa | `SUJETO_NOMBRE` | 939 | «Respecto de las sorpresas inflacionarias del mes, el señor Claudio Soto informa que…» |
| `2864:1` | Claudio Soto Gamboa | `SUJETO_NOMBRE` | 495 | «el señor Claudio Soto hace alusión a una descomposición del IPC…» |
| `2865:1` | Rodrigo Vergara Montes | `SUJETO_ROL_NOMBRE` | 177 | Nueva voz |

Lectura propia:

- `2863:1` termina en coma y `2863:2` empieza en minúscula con un gerundio: son **una sola
  oración del acta con dos hablantes**. La partición existente que separa la pregunta de
  Marfán de la respuesta de Soto es correcta y se conserva.
- Entre `2863:2` y `2863:3` **no interviene ninguna otra voz**. Soto responde y a
  continuación desarrolla.
- Los residuos `ha caído algo r últimamente` y `A continuación,.` están **dentro y al final**
  de `2863:3`; el segundo queda en el límite `2863:3→2864:1`, que **ya estaba unido en v5**.
  Ninguno de los dos está en el límite `2863:2→2863:3`. No se corrigieron ni se desplazaron.
- Criterio de consistencia: `2863:3→2864:1` ya estaba agrupado en v5 pese a que `2864:1`
  también re-presenta nominalmente a Soto («el señor Claudio Soto hace alusión»). Rechazar
  `2863:2→2863:3` por re-introducción nominal sería inconsistente con la convención ya
  aplicada en el mismo grupo.

**Decisión: enlace respaldado.** Grupo resultante de tres filas y **1.497 caracteres**.

### 2.2 `RPM-2011-01-13:3646:2 → 3646:3`

| Fila | Hablante | Fuente | Caracteres | Contenido |
|---|---|---|---:|---|
| `3645:1` | Sergio Lehmann Beresi | `SUJETO_NOMBRE` | 5.138 | Presentación del escenario externo |
| `3646:1` | Sebastián Claro Edwards | `SUJETO_ROL_NOMBRE` | 233 | «El Consejero señor Sebastián Claro plantea que los vaivenes… en el margen**,**» |
| `3646:2` | Sergio Lehmann Beresi | `CONTEXTO_REVISADO` | 84 | «lo cual es confirmado por el Gerente de Análisis Internacional señor Sergio Lehmann.» |
| `3646:3` | Sergio Lehmann Beresi | `SUJETO_NOMBRE` | 1.168 | «**El señor Lehmann continúa**, indicando que en materia de monedas…» |
| `3646:4` | Sebastián Claro Edwards | `SUJETO_ROL_NOMBRE` | 98 | «El Consejero señor Sebastián Claro consulta si Turquía y Hungría…» |

Lectura propia:

- `3646:1` y `3646:2` forman una sola oración del acta con dos hablantes; la separación
  existente es correcta y se conserva.
- `3646:3` abre con el marcador explícito **«El señor Lehmann continúa»**: evidencia positiva
  de que lo precedente también era discurso de Lehmann.
- El corpus **ya** trata este marcador como continuidad: `3647:2 → 3648:1` está unido en v5 y
  `3648:1` dice «El señor Sergio Lehmann prosigue con su presentación».
- La confirmación de `3646:2` **no transcribe palabras ni declara modalidad**. El enlace
  afirma continuidad discursiva, **no** que la confirmación fuera verbal ni gestual.
- Las intervenciones anterior y posterior de Claro quedan separadas.

**Decisión: enlace respaldado.** Grupo resultante de dos filas y **1.252 caracteres**.

---

## 3. Implementación

Los dos enlaces son **intrapadre** y tienen exactamente la forma de las capas v1/v2/v3
(extremo izquierdo `CONTEXTO_REVISADO` con ancla nula → extremo derecho con fuente nominal
explícita, dentro del mismo padre). Se implementaron como una **capa nueva**, no ampliando
las existentes.

### Archivos nuevos

| Archivo | Función |
|---|---|
| `data/curation/continuidades_intrapadre_v4.json` | 17 pruebas: las 15 de v3 **byte a byte** + las 2 nuevas, con intervalos, hashes y límites |
| `scripts/reviewed_intrapara_v4.py` | Validador `load_v4`: re-deriva intervalos, fuentes, hashes y grupos completos desde `data/raw`, la base v5 y la lectura del lote6 |
| `scripts/compare_procedural_v6.py` | Gate global v5→v6: sólo las dos uniones, todos los campos y todos los grupos |
| `scripts/inventario_procedimental_v6.py` | Inventario de los71 pares del lote6 recalculado sobre v6 |
| `tests/test_intrapara_v4.py` | 30 pruebas nuevas |
| `docs/procedimental_v6_2026-09-09/` | Inventario actualizado y resumen |

### Archivos modificados (sólo despacho, sin relajar nada)

| Archivo | Cambio |
|---|---|
| `scripts/intrapara_profiles.py` | Añade `intrapadre-v4` al despacho y la tabla `REQUIRED_INTRAPARA` |
| `scripts/preparar_data.py` | Añade `--perfil procedimental-v6`; **el perfil predeterminado sigue siendo `procedimental-v5`** |
| `scripts/functional_refinements.py` | `active_refinements` acepta el perfil intrapadre exigido (por defecto `intrapadre-v3`, igual que antes) |
| `scripts/reviewed_procedural_v5.py` | `active_reviews` idem; mensaje y comportamiento por defecto sin cambio |
| `scripts/qa_preparacion.py` | F1 compara contra v5 cuando el perfil es v6; `perfil_entrega` refleja el perfil real |

**No se modificó** `scripts/revisar_reservas_complejas.py`: sigue apuntando a la base v5 y
sigue siendo sólo lectura/clasificación. La carpeta del lote6 quedó intacta.

---

## 4. Validación ejecutada

Todo se ejecutó en staging y se publicó sólo al final, sin fallos.

| Paso | Comando | Resultado |
|---|---|---|
| Pruebas completas | `python -m unittest discover -s tests` | **2.129 pruebas, OK** (2.099 previas + 30 nuevas) |
| F0 | `scripts/qa_gate_f0.py` | **PASA** — 132 sesiones, 310 fórmulas TPM contrastadas, 0 errores |
| Comparación global | `scripts/compare_procedural_v6.py` | **PASA** |
| F1 | `scripts/qa_preparacion.py` | `pasa_controles_bloqueantes: true`, `errores: []` |

### Comparación global v5 → v6 (todos los campos, todos los grupos)

| Indicador | Valor |
|---|---:|
| Filas | 9.694 (sin cambio) |
| Grupos antes / después | 9.236 → **9.234** |
| Uniones exactas admitidas | 2 |
| Celdas relacionales modificadas | 4 |
| Etiquetas `ID_Turno` renumeradas | 119 |
| Filas con conjunto de compañeros distinto | 5 |
| **Otros campos modificados** | **0** |
| **Grupos previos divididos** | **0** |
| Alertas antes / después | 467 → **467** |

Las cuatro celdas relacionales son exactamente:

| Fila | Campo | Antes | Después |
|---|---|---|---|
| `2863:3` | `Relacion_Turno` | `INICIO_EXPLICITO` | `CONTINUIDAD_INTRAPADRE_REVISADA` |
| `2863:3` | `ID_Antecedente_Continuidad` | nulo | `RPM-2010-01-14:2863:2` |
| `3646:3` | `Relacion_Turno` | `INICIO_EXPLICITO` | `CONTINUIDAD_INTRAPADRE_REVISADA` |
| `3646:3` | `ID_Antecedente_Continuidad` | nulo | `RPM-2011-01-13:3646:2` |

Las cinco filas con compañeros distintos son exactamente los miembros de los dos grupos:
`2863:2`, `2863:3`, `2864:1`, `3646:2`, `3646:3`.

Los 9.234 grupos **eran una expectativa aritmética y ahora son un resultado construido y
validado**.

---

## 5. Estado productivo vigente: procedimental-v6

| Métrica | v5 | **v6** |
|---|---:|---:|
| Padres originales | 7.219 | 7.219 |
| Sesiones | 132 | 132 |
| Filas físicas | 9.694 | 9.694 |
| Bloques de texto | 9.693 | 9.693 |
| Grupos `ID_Turno` | 9.236 | **9.234** |
| Grupos de varias filas | 357 | **358** |
| Máximo de filas por grupo | 11 | 11 |
| Filas alertadas | 467 | 467 |
| Pruebas intrapadre | 15 | **17** |
| Pruebas entre padres | 24 | 24 |
| Enlaces procedimentales v5 | 6 | 6 |
| Refinamientos funcionales v4 | 3 | 3 |

SHA-256 de la entrega:

```text
1dfce989aa1ded2fb4bc99557750c48bd3d01ee5a690708044a659065e45c7c4  consolidado_base_referencia.xlsx
7b1dc48e637bd913d4efa97fae240da19d5c8827c12e1f002062d74e9f968a57  consolidado_base_referencia_final.xlsx
f7ca0555ff02b56df8950a061cc689a0183ef29490379f95b9b04743df2d4889  data/curation/continuidades_intrapadre_v4.json
```

El manifiesto de la entrega registra 130 entradas de código y sus hashes **coinciden con los
archivos actualmente en disco** (verificado).

### Capas acumuladas que se conservan

- 24 pruebas revisadas entre padres.
- **17** pruebas intrapadre (2 v1 + 4 v2 + 9 v3 + **2 v6**).
- 3 refinamientos funcionales v4.
- 6 enlaces procedimentales v5, verificados uno por uno en v6.
- Los dos grupos de García de once filas (`RPM-2005-02-10:T3`, `RPM-2005-03-10:T3`) intactos.

---

## 6. Inventario actualizado

`docs/procedimental_v6_2026-09-09/inventario_estado_v6.csv` rinde la cuenta completa de los
71 pares del lote6 sobre v6:

| Estado | Pares |
|---|---:|
| Separaciones respaldadas previamente en lote4 | 10 |
| Separaciones funcionales v4 | 3 |
| **Enlaces intrapadre aplicados en v6** | **2** |
| Reservas específicas abiertas | 3 |
| Sin adjudicación en esta vista | 53 |
| **Total** | **71** |

Dos pares dejaron de ser límites al agruparse; por eso el inventario de límites tiene 69
entradas y las dos restantes se informan explícitamente como aplicadas.

**Los 53 sin adjudicación no son 53 errores ni 53 casos nunca leídos**, y no estiman la
cobertura semántica del corpus.

---

## 7. Reservas que siguen abiertas

Las tres reservas del lote6 **no se cerraron** y están verificadas como separadas en v6:

| Par | Estado | Siguiente acción |
|---|---|---|
| `RPM-2006-07-13:780:2 → 780:3` | `RESERVA_COTEJO_INICIO` | Cotejar la transición en el acta RPM95 del 13-07-2006 entre el voto de De Gregorio y el inicio de Corbo |
| `RPM-2009-08-13:2661:6 → 2661:7` | `RESERVA_CONFIRMACION_NARRADA` | Definir el criterio de agrupación de confirmaciones narradas; un PDF con la misma redacción no revelará la modalidad |
| `RPM-2012-12-13:5252:3 → 5252:4` | `RESERVA_LIMITE_ACTA_PERSONA` | Revisar primero la frontera acta/aviso; Vergara no habla aquí y Herrera empieza en `5253` |

Tras aplicar los dos enlaces, la selección intrapadre sobre v6 contiene **exactamente estas
tres reservas** (verificado en pruebas).

---

## 8. Salvaguardas respetadas

Verificadas por pruebas, no sólo declaradas:

- `CONTEXTO_REVISADO` **no** se convirtió en ancla: los dos extremos izquierdos conservan
  `ID_Ancla_Actor` nulo y su fuente. El total de filas `CONTEXTO_REVISADO` no cambió (382).
- No se modificó texto, OCR, actor, cargo, fuente, ancla ni alerta en ninguna fila
  (comparación campo por campo de las 9.694 filas).
- Los residuos OCR de `2863:3` no se repararon ni desplazaron.
- No se introdujo ninguna regla léxica global (gerundios, «continúa», «prosigue»,
  confirmaciones narradas, cesiones, «A juicio», relativos, pasado).
- No se restauraron `600→601` ni `5402→5403`.
- No se cerró ninguna alerta: 467 antes, 467 después.
- No se modificaron los registros históricos v1–v5 ni los comparadores congelados de v4/v5.
- `revisar_reservas_complejas.py` y la carpeta del lote6 quedaron intactos.
- Las presentaciones largas y los grupos de hasta once filas se conservan.
- No se atribuyó nada por mera mención.

---

## 9. Reproducción

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt

# Pruebas completas
.venv/bin/python -m unittest discover -s tests -v

# Reconstruir v6 en un destino nuevo (nunca sobrescribe una entrega existente)
.venv/bin/python scripts/preparar_data.py --perfil procedimental-v6 \
  --destino .cache/reproduccion_procedimental_v6

# Inventario actualizado sobre v6
.venv/bin/python scripts/inventario_procedimental_v6.py \
  --salida .cache/inventario_v6
```

El perfil predeterminado de `preparar_data.py` **sigue siendo `procedimental-v5`**; v6 es
aditivo y siempre explícito.

---

## 10. Próximo trabajo

La revisión semántica del corpus **no está terminada**. No hay un porcentaje fiable de
cobertura total.

1. Cotejar el acta RPM95 del 13-07-2006 para resolver la reserva de `780`.
2. Definir el criterio de confirmaciones narradas y reevaluar `2661` a la luz del marcador
   «continúa» que sí aparece en `3646` (sin generalizar retrospectivamente).
3. Revisar la frontera acta/persona en `5252` antes de evaluar aviso→cesión.
4. Localizar y comprobar las fichas previas de los 53 pares sin adjudicación antes de decidir
   nuevas lecturas: no equivalen a errores ni a casos nunca leídos.
5. Cualquier nuevo enlace requiere lectura completa del padre y de todos los miembros de sus
   grupos, prueba acotada, salida versionada nueva, pruebas completas, F0/F1 y comparación
   global de todos los campos y grupos.
