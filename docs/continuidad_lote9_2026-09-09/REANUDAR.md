# Punto de reanudación — lote 9 y correcciones de OCR

Este archivo existe para que un turno nuevo arranque sin rampa. Léelo primero.
Todo lo que dice está verificado contra el repositorio; si un número no cuadra,
manda el repositorio y hay que actualizar este archivo.

## Dónde estamos

Última actualización: 2026-09-10, commit `5210988`.

| | |
|---|---:|
| corpus | 9.723 filas |
| leídas | **1.665** |
| pendientes | **8.058** |
| sesiones cerradas | **23** de 132 |
| filas con `Texto_Corregido` | **14** |
| operaciones de OCR curadas | **23** |
| revisiones descartadas con motivo | **25** |

**Siguiente paso exacto:** sesión **`2006-01-12`**, rondas **135–140**, 47 filas
del plan, 85.020 caracteres.

Cola visible del plan: `2006-01-12` (135–140, 47) · `2011-10-13` (141–147, 82) ·
`2013-09-12` (148–154, 69) · `2012-05-17` (155–161, 67) · `2007-09-13`
(162–169, 85) · `2008-08-14` (170–177, 96) · `2015-08-13` (178–183, 66) ·
`2007-05-10` (184–189, 49) · `2007-07-12` (190–196, 61) · `2005-04-07`
(197–201, 59) · `2007-08-09` (202–209, 58) · `2008-10-09` (210–215, 43).

Ver el resto: `.venv/bin/python scripts/rondas_lectura_lote9.py estado`.

## Política vigente (fijada por el usuario, 2026-09-10)

Invierte la instrucción anterior de «no corrijas OCR». Ahora:

1. **`Texto` queda verbatim, intacto.** Es la fuente documental.
2. Las correcciones van en la columna paralela **`Texto_Corregido`**, en una
   salida versionada nueva. Nunca se sobrescribe `data/processed/` ni una
   versión publicada.
3. **Cero reglas automáticas.** Cada operación curada a mano sobre una fila
   leída completa, con `Contexto` y `Justificacion`.
4. **Residuos de fuente eliminados** en `Texto_Corregido`: números de página,
   marcas horarias sueltas, símbolos ilegibles, firmas truncadas.

### Criterio operativo

- **Carácter mal leído** (una letra por otra, un signo por una letra, tilde
  puesta o faltante): se corrige.
- **Palabra omitida**: se repone **sólo si la forma correcta está en la fila o
  en la sesión**. Medido: `alta base comparación` se corrigió porque la misma
  fila trae «alta base de comparación»; `con respecto el dólar` **no**, porque
  en toda la sesión `con respecto al` aparece 0 veces.
- **Ambiguo** (dos o más reconstrucciones posibles): se deja verbatim y se
  registra en `Revisiones_Sin_Correccion` con el motivo.
- **No es OCR**: solecismos del hablante (`han habido salidas`), abreviaturas
  y topónimos reales (`TCM`, `Bío Bío`), cifras inverosímiles (`anclada al
  10%`), inconsistencias entre filas de la misma sesión (`US$ 58` vs
  `US$ 66`). Se dejan y se anotan.
- **`Revisiones_Sin_Correccion` es parte del entregable**, no basura: es la
  prueba de que no se pasó una regla ciega.

## Flujo por sesión

```
.venv/bin/python .cache/leer_seguro.py N            # lista las filas de la ronda N
.venv/bin/python .cache/leer_seguro.py N a:b        # imprime a..b completas + chars emitidos
.venv/bin/python .cache/leer_seguro.py N k          # una fila completa
```

1. Listar la ronda, sumar los caracteres, **elegir un rango de modo que lo
   emitido no pase de 18.000**. Lo emitido es texto **+ ~106 caracteres de
   cabecera por fila**. Techo medido: completo a 19.267, truncado a 20.501, y
   la truncación se come el medio.
2. Leer el rango. Si la salida se trunca, **no registrar nada**: releer por
   separado.
3. Verificar los fragmentos que se van a corregir contra el texto fuente antes
   de escribirlos (un solo script que los cuente todos).
4. Escribir el lote en `.cache/lote_ocr_NNN.json` y fusionar:
   `.venv/bin/python .cache/agregar_ocr.py .cache/lote_ocr_NNN.json`
5. Validar: `.venv/bin/python scripts/correcciones_ocr_v1.py --validar`
6. Anotar la ronda:
   `.venv/bin/python scripts/rondas_lectura_lote9.py registrar N UNA_SOLA_VOZ "justificación"`
7. Al cerrar la sesión, **verificar el conteo contra el xlsx** — el conteo del
   plan casi nunca coincide (66 del plan vs 68 reales en 2006-10-12; 59 vs 65;
   72 vs 78).
8. Añadir la fila a `### Progreso` en `docs/MULTIHABLANTE_LOTE9_2026-09-09.md`.
9. Probar y publicar:

```
PYTHONPATH=scripts PYTHONHASHSEED=0 .venv/bin/python -m unittest \
    tests.test_inventario_v7 tests.test_correcciones_ocr_v1 -q
git add -A data/curation/correcciones_ocr_v1.json scripts/correcciones_ocr_v1.py \
    tests/test_correcciones_ocr_v1.py docs/continuidad_lote9_2026-09-09/lecturas.json \
    docs/MULTIHABLANTE_LOTE9_2026-09-09.md
git commit -m "..."
git push origin arena/01a08804-nlm-proyect
git ls-remote --heads origin arena/01a08804-nlm-proyect   # confirmar el SHA remoto
```

**Commit y push después de cada sesión cerrada.** El usuario lo pidió
explícitamente «por si acaso». El branch está fijo en
`arena/01a08804-nlm-proyect`; el PR es el **#5**.

## Trampas ya pagadas

- `registrar N` anota **toda la ronda**, leída o no. Si sólo se leyó parte de
  una ronda, hay que retirar las filas no leídas de `Casos` en
  `lecturas.json` antes de commitear. Pagado el 2026-09-10: se anotó la ronda
  136 completa habiendo leído una sola de sus 11 filas; se retiraron las 10.
  **Regla: nunca anotar una ronda que no se leyó entera.**
- La salida de bash se trunca por el **medio**, conservando cabeza y cola.
  Nunca encadenar una lectura grande con un listado en la misma llamada.
- Nunca pasar el lector por `head -c` / `tail -c`.
- `registrar` anota la ronda aunque la consola se haya cortado: confirmar que
  se vio la cabeza de cada fila antes de anotar.
- `Fecha` en el xlsx es `datetime`, no cadena. Comparar con
  `v.strftime('%Y-%m-%d')`.
- Las columnas que contienen `Texto` incluyen también `Rol_Detectado_Texto`,
  `Texto_Truncado`, `Fuente_Texto`, `ID_Bloque_Texto`. No hay columna `Actor`
  (usar `Actor_Final`) ni `Alerta` (usar `Motivos_Revision`).
- Los heredocs corren con el python del sistema, que no tiene openpyxl.
  Escribir a `.cache/` y correr con `.venv/bin/python`.
- `plan_rondas.json` es **estático**: su conteo de pendientes no es el vivo.
- Dos operaciones de una misma fila **no pueden pisarse**: el `Antes` de cada
  una debe existir en el texto virgen. Lo impone `aplicar_a_texto(virgen=...)`
  y lo cubre `test_operaciones_de_una_fila_no_pueden_pisarse`.

## Ritmo medido

- Turno de sólo lectura: ~130–145 filas.
- Turno con curaduría de OCR: ~66 filas.
- Restan 8.058 filas → **~120 turnos con curaduría**, ~45 sin ella.

No hay forma de autoconvocarse entre turnos: hace falta un mensaje del usuario
para arrancar cada uno.

## Lo que queda fuera del plan de lectura

- Corte de las **3 filas de dos voces** confirmadas (`657:1`, `1564:1`,
  `2960:2`): probado, sin materializar.
- Las **tres reservas** 780, 2661, 5252: requieren cotejo contra el acta
  fuente. Siguen abiertas y separadas.
- Salida versionada nueva con `Texto_Corregido` + comparación global + reporte.
