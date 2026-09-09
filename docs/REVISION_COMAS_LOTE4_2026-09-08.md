# Revisión de comas — lote 4 (2026-09-08)

**Base:** `c012c941685895270fcebfe2e84d6bad7e125d72` (lote 3).
**Datos:** LOOP32 (`1b02496`), sin cambios ni regeneración.

## Resultado

Se revisaron **22 límites más en 22 padres completos**, leyendo **57.607 caracteres de origen**. En los focos examinados, los sujetos y predicados respaldan la separación existente. No hicieron falta nuevos cortes: son **22 fichas de revisión, no 22 errores corregidos ni voces recuperadas**.

| Unidad | Tras lote 3 | Tras lote 4 |
|---|---:|---:|
| Límites del subgrupo | 167 | 167 |
| Con ficha bilateral | 120 | **142** |
| Sin ficha bilateral | 47 | **25** |
| Padres con fichas | 104 | **126** |
| Filas / filas alertadas / padres alertados | 9.691 / 465 / 395 | Sin cambios |
| Nuevos cortes / enlaces / reasignaciones / cierres | — | **0 / 0 / 0 / 0** |
| Pruebas locales | 1.829 | **1.841** |

`LIMITE_REVISADO_SIN_CIERRE` registra la lectura bilateral; no elimina las alertas de puntuación ni certifica integridad OCR, cifras, identidad/cargo global o exclusividad de todos los intervalos. Las 142 fichas no se suman a las 102 fichas actuales de menciones: son unidades distintas y pueden superponerse.

## Selección y alcance de lectura

Entre los 42 límites personales pendientes al comenzar, se alternaron los **11 padres más cortos y los 11 más largos**, ordenando por longitud e ID. Cada uno tenía un foco personal pendiente. Es una selección dirigida para balancear carga de lectura, **no una muestra representativa ni un umbral para cortar intervenciones**.

Se leyeron los 22 padres completos, sus particiones actuales y ventanas de 150 caracteres de los vecinos externos. Estas ventanas **no cuentan como lectura completa de los vecinos**. Los padres 301 y 1386 se releyeron íntegramente; su revisión previa en el diagnóstico no produjo una aprobación automática.

### Exposiciones largas y alternancias conservadas

- **3123:** Marshall **5.484** → Presidente 108 → Marfán 57. El voto completo de Marshall permanece unido. El foco es la cesión presidencial seguida de «quien agradece», no un corte dentro del voto. Se conserva el enlace revisado de Marfán **3123→3124**.
- **2644:** Presidente 99 → Céspedes **4.101** → Presidente 142. «quien comienza su exposición» abre el aporte de Céspedes. La Minuta de Opciones es una referencia dentro de su argumento; no se inventa otro lector. La oferta posterior a De Ramón pertenece al Presidente; De Ramón comienza en 2645.
- **1718:** se mantienen los **15 tramos**, de 690/89/181/139/705/644/266/187/266/119/132/323/283/171/948 caracteres. La ficha corresponde a Desormeaux→Magendzo al comienzo. Selaive y Rappaport son coautores mencionados, no dos intervenciones nuevas. El final sin puntuación de Marshall 119 es otro límite y permanece fuera de esta ficha.
- **2740, 2697, 2567, 2699, 2810, 3288 y 2566:** se mantienen desarrollos extensos y retornos explícitos, sin fusionar a un expositor a través de las intervenciones de otros ni cortar por cambios de tema. La exposición de Lehmann en 3288 conserva sus **3.138 caracteres**.

## Los 22 focos

Las fichas incluyen ambos extremos, huellas del padre y de toda su partición, justificación individual y reservas. Los números identifican padres de origen; las flechas describen **límites existentes**, no cambios aplicados.

| Padre | Foco y evidencia local |
|---|---|
| 301 | Eyzaguirre→Marfán: «Al respecto… señala», respuesta sobre shock de oferta. |
| 3123 | Presidente→Marfán: «quien agradece», después del voto de Marshall. |
| 2931 | Marshall→García: «afirmando…», confirmación metodológica; retorno de García conservado. |
| 1718 | Desormeaux→Magendzo: «a lo que… responde», áreas positivas y negativas. |
| 2956 | Presidente→Cowan: «a lo cual… señala», efectos transitorios pero prolongados. |
| 2740 | Soto→Velasco: «acotando…», interpretación del movimiento de AFP. |
| 2938 | Marshall→García: «señalando…», inicio identificable de respuesta con final dañado. |
| 2697 | Soto→Claro: «Al respecto… comenta», salarios reales; Soto responde después. |
| 2852 | Vergara→Lehmann: «a lo cual… responde», commodities agrícolas. |
| 2644 | Presidente→Céspedes: «quien comienza su exposición». |
| 3348 | Presidente→De Ramón: «a lo cual… responde», magnitud de intervención. |
| 2567 | Desormeaux→Lehmann: «a lo cual… responde», proyección de petróleo. |
| 3001 | Claro→Bernier: «a lo cual… responde», operaciones REPO anteriores. |
| 2699 | Marfán→Velasco: «a lo que el señor Ministro agrega», plazo de convergencia salarial. |
| 2863 | Marfán→Soto: «respondiendo…», reconstrucción del IPC. |
| 2591 | Marfán→Cowan: «a lo cual… responde», discusión de tasa mínima en Canadá. |
| 1386 | Corbo→Lehmann: «señalando…», cierre del cobre; Corbo vuelve y después comienza Valdés. |
| 2810 | Marshall→Lehmann: «a lo cual… muestra», índice de alimentos. |
| 3303 | Soto→Vicuña: «en tanto que… complementa», registro de albañiles. |
| 3288 | Vergara→De Ramón: «lo cual es compartido por…», confirmación; después continúa Lehmann. |
| 3189 | Marshall→García: «a lo cual… responde», M2/M3; Marfán sintetiza después. |
| 2566 | Lehmann→Desormeaux: «planteamiento al cual… complementa»; Lehmann retoma después. |

## Reservas que no se cierran

**2938 es el control principal:** Marshall 105 → García **51** → Marfán 634. Reconocer «señalando el señor García» no completa **«tendrá efectos en los»**. El tramo de García mantiene `FINAL_SIN_PUNTUACION;TEXTO_DANADO_POR_COTEJAR`. No se reconstruye la cola ni se afirma que todo ese intervalo esté resuelto.

También se conservan literalmente:

- **2956, 2567 y 2863:** `A continuación,.`; en 2863, además, `ha caído algo r últimamente`. No se añade una advertencia que invalide el enlace previamente revisado 2863→2864.
- **2697:** `l` aislada; **2644:** `nesgo`; **2699:** `/ .` y las magnitudes económicas tal como aparecen, sin corrección por plausibilidad.
- **2591:** `r .`, `soft` y `antología`; **3303:** `relaciones menores`; **1718:** `pipe Une` y `yeso`. La lectura de la voz no certifica estos términos.
- **2810:** Lehman Brothers se menciona como empresa, no como un turno de Sergio Lehmann. No se crean alias globales.

Los enlaces **3123→3124, 1386→1387, 2863→2864, 2566→2567 y 2956→2957** se mantienen. `CONTEXTO_REVISADO` no se convierte en ancla global y `Fin` sigue sin ser criterio de corte o anclaje. Las reservas y prohibiciones de los lotes anteriores siguen vigentes, incluidas las continuidades advertidas no enlazadas.

## Verificación

- **1.841 pruebas locales pasan (+12), en 73,349 s.** Incluyen las 22 fichas, mutaciones de ambos extremos, cambios fuera del foco en el voto de Marshall, conservación de texto, 15 tramos de 1718, daño de 2938, retornos y enlaces, y rechazo de duplicados.
- Los **27 archivos de datos versionados**, incluido TPM externo, son idénticos byte a byte a `c012c94`. Los **15 artefactos** de los tres lotes previos también permanecen idénticos; sus huellas constan en `verificacion.json`.
- El helper de seguimiento no cambia. Se validan las fuentes y cada lote por separado antes de acumular las fichas.
- Esto **no es una nueva ejecución del pipeline productivo, F0/F1 ni CI remota**. Base, QA y manifiesto siguen siendo LOOP32. No hubo nuevo cotejo PDF.

## Pendiente y próximo paso

Quedan **25 límites en 25 padres: 20 personales y 5 institucionales**.

Personales: **658, 1737, 2532, 2555, 2556, 2588, 2613, 2620, 2624, 2627, 2666, 2705, 2807, 2885, 2897, 2915, 3012, 3051, 3101 y 3268**. La siguiente lectura debe tomar cada padre completo y su continuidad, no aprobar sus límites por cercanía con fichas anteriores.

Institucionales: **601, 1901, 2112, 2803 y 5252**, reservados para criterios específicos de acta/discurso. No se relaja el rechazo del helper a extremos del Consejo para contarlos como respuestas personales.

Las **465 filas alertadas / 395 padres alertados** no equivalen al total sin leer. Este lote avanza una subcola concreta, sin declarar cerrados otros problemas de texto, identidad o continuidad.

## Artefactos y reproducción

- [22 fichas nuevas](revision_comas_lote4_2026-09-08/revisiones.json)
- [Cola acumulada: 167 límites](revision_comas_lote4_2026-09-08/cola_comas.csv)
- [25 límites sin ficha](revision_comas_lote4_2026-09-08/comas_sin_ficha.csv)
- [Resumen](revision_comas_lote4_2026-09-08/resumen.json) · [Verificación y huellas](revision_comas_lote4_2026-09-08/verificacion.json)

```bash
.venv/bin/python scripts/revisar_cola_comas.py \
  --revisiones docs/revision_comas_lote1_2026-09-08/revisiones.json \
  --revisiones docs/revision_comas_lote2_2026-09-08/revisiones.json \
  --revisiones docs/revision_comas_lote3_2026-09-08/revisiones.json \
  --revisiones docs/revision_comas_lote4_2026-09-08/revisiones.json \
  --salida .cache/revision_comas4_repro
.venv/bin/python -m unittest discover -s tests
```

La salida va a una carpeta nueva; no se sobrescriben los lotes anteriores.
