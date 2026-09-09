# Continuidad intrapadre v1 — dos enlaces aplicados

**Fecha:** 9 de septiembre de 2026. **Estado:** entrega versionada construida y validada.
No es otra simulación de etiquetas: el motor genera relaciones, antecedentes,
agrupaciones y los archivos finales correspondientes.

## Entrega y conservación del histórico

La entrega vigente está en **[`data/releases/continuidad_intrapadre_v1/`](../data/releases/continuidad_intrapadre_v1/)**:

- [Excel final — 24 columnas](../data/releases/continuidad_intrapadre_v1/consolidado_base_referencia_final.xlsx).
- [Excel de auditoría — 37 columnas](../data/releases/continuidad_intrapadre_v1/consolidado_base_referencia.xlsx).
- [Grupos de intervención](../data/releases/continuidad_intrapadre_v1/turnos_habla.csv),
  [alertas pendientes](../data/releases/continuidad_intrapadre_v1/revision_pendientes.csv),
  [QA](../data/releases/continuidad_intrapadre_v1/qa_preparacion.json) y
  [manifiesto](../data/releases/continuidad_intrapadre_v1/manifiesto_preparacion.json).

**`data/processed/` conserva LOOP32, no la nueva versión.** Sus 9.257 grupos son el
baseline explícito de las revisiones históricas. Los 27 archivos de datos previos
y los **233 documentos/artefactos previamente versionados en `docs/`** se comprobaron
idénticos byte a byte frente a `14484b9ed59060c5294ca2d61289e8bb50434cc7`.
No se reescribieron fichas fechadas ni se redirigieron silenciosamente sus validadores.
En particular, el lote5 describe correctamente la separación anterior de 3012;
la auditoría1 sigue siendo evidencia de una simulación, no de una aplicación realizada entonces.

## Qué se aplicó

| Caso | Agrupación de esta versión | Límites conservados |
|---|---|---|
| **2796 / Marshall** | 343 + 5.287 caracteres; conserva la continuación de **2.105** en 2797: **7.735** en total | Claro5.097 queda fuera; 2798 también. Se mantienen tres filas físicas y el literal `ALAR` de 2797, sin corrección OCR. |
| **3012 / De Ramón** | 375 + 1.867 caracteres: **2.242** en total | Presidente109 queda fuera, con su aviso de puntuación; tampoco se incorpora la intervención de 3013. |

En ambos casos, el primer tramo conserva `CONTEXTO_REVISADO` y **ancla nula**.
El tramo nominal siguiente conserva su **ancla propia**, pero ahora lleva
`Relacion_Turno=CONTINUIDAD_INTRAPADRE_REVISADA` y como antecedente el tramo previo.
El enlace existente **2796:3 → 2797:1** y el ancla propia de 2797 permanecen intactos.

Las pruebas de aplicación están en
[`continuidades_intrapadre_v1.json`](../data/curation/continuidades_intrapadre_v1.json):
texto íntegro del padre, SHA-256, fecha, actor, IDs de extremos, intervalos literales,
fuentes de atribución, evidencia y justificación. Proceden de la lectura completa
registrada en la [auditoría1](AUDITORIA_CONTINUIDAD1_2026-09-09.md), no de una nueva
lectura PDF ni de una regla de proximidad.

## Comparación global, no sólo de los dos padres

| Medida | LOOP32 | Intrapadre v1 |
|---|---:|---:|
| Filas físicas | 9.691 | **9.691** |
| Bloques de texto | 9.690 | **9.690** |
| Grupos de intervención | 9.257 | **9.255** |
| Grupos con varias filas | 338 | **339** |
| Máximo de filas por grupo | 11 | **11** |
| Filas alertadas / padres alertados | 465 / 395 | **465 / 395** |
| Pruebas revisadas entre padres | 24 | **24** |
| Pruebas revisadas intrapadre aplicadas | 0 | **2** |

Se verificó la **partición completa de las 9.691 filas**, ignorando únicamente los
nombres numéricos de los grupos para comparar su pertenencia. El resultado contiene
exactamente las dos uniones previstas: ningún grupo anterior se divide y no aparece
ningún enlace adicional, registrado o no.

- **Cuatro celdas relacionales cambian:** dos relaciones y dos antecedentes.
- **20 celdas `ID_Turno` cambian**, por las uniones y la renumeración posterior dentro
  de las dos sesiones. No son 20 correcciones ni 20 nuevas uniones.
- **Cinco filas tienen un conjunto de compañeros distinto:** 2796:2, 2796:3, 2797:1,
  3012:2 y 3012:3. La simulación anterior contaba tres sustituciones hacia la etiqueta
  izquierda; era otra medida, no un conteo de todas las filas afectadas por la unión.
- **Todos los demás campos son idénticos celda a celda**, incluidos textos, actores,
  cargos, fuentes, anclas, IDs físicos, fechas y alertas. No se cierran advertencias,
  no se recuperan palabras y no se recortan exposiciones.

[Comparación completa y las 20 etiquetas renumeradas](../data/releases/continuidad_intrapadre_v1/comparacion_intrapadre.json).

Permanecen separados los controles **2685** (duplicado), **2885** (daño), **1901**
(acta intermedia) y **2779** (tres personas). No se restauran **600→601** ni
**5402→5403**, ni se fuerzan los cuatro pares alertados de LOOP32. Se preservan
los grupos de García de once filas y todas las alternancias ya identificadas.
Esto se comprobó por equivalencia global, sin afirmar una relectura de cada caso.

## Implementación y controles

- Registro intrapadre separado y de alcance cerrado a los **dos pares exactos**.
  El cargador anterior sigue exigiendo padres consecutivos distintos y conserva sus 24 pruebas.
- El motor sólo usa el registro cuando se solicita expresamente el perfil nuevo.
  No convierte `CONTEXTO_REVISADO` en ancla propagable ni aplica una regla global de mismo actor.
- Extremos contiguos, literales, sin alertas ni intervalos institucionales;
  fuente o partición distinta provoca un fallo, no una aplicación aproximada.
- F1 comprueba las pruebas y rechaza relaciones intrapadre sin evidencia, antecedentes
  incorrectos, anclas alteradas o extremos ausentes. Conserva sus barreras existentes.
- El orquestador usa **`intrapadre-v1` por defecto**. Construye en staging; ejecuta
  pruebas, F0, la comparación global y F1; publica el directorio completo sólo tras pasar.
  Rechaza destinos existentes y rutas ajenas a `.cache/` o `data/releases/`.
  El modo `--perfil legacy` es explícito y conserva el comportamiento anterior;
  **no ejecutarlo sobre el histórico si se desea conservar sus hashes**.

## Validaciones ejecutadas

1. **Ensayo aislado:** 1.950 pruebas, 152,088s; reconstrucción completa, F0/F1 y
   comparación global satisfactorios.
2. Se añadió la prueba del perfil versionado predeterminado y se endureció el tipo
   del número de versión del registro.
3. **Publicación con el código final:** **1.951 pruebas, 151,952s**, incluidas
   **34 nuevas** respecto de la auditoría1; reconstrucción completa, F0/F1 y gate global pasan.
4. Ensayo/publicación: **todas las hojas y celdas de los tres XLSX idénticas**;
   seis auxiliares CSV/JSONL idénticos byte a byte y QA idéntico. Los hashes binarios
   de XLSX pueden diferir por metadatos del archivo; no se afirmó igualdad binaria.
5. **104 hashes de entradas/código y 12 de salidas** verificados en el manifiesto,
   junto con el hash del registro aplicado. Histórico completo conservado.

[Verificación independiente de los archivos generados](verificacion_continuidad_intrapadre_v1_2026-09-09.json).
Estas son verificaciones **locales**, no una certificación semántica total ni un
resultado de CI remoto. Siguen las 465 filas alertadas en 395 padres, las reservas
textuales/de identidad y las tres fichas abiertas del lote7. No hubo nuevo cotejo PDF.

## Reproducir sin sobrescribir ninguna entrega

Desde la raíz del repositorio, con las dependencias instaladas:

```bash
.venv/bin/python scripts/preparar_data.py --perfil intrapadre-v1 \
  --destino .cache/reproduccion_intrapadre_v1
```

El destino debe ser nuevo. Si ya existe, elegir otro. Para consumir datos, usar los
archivos de `data/releases/continuidad_intrapadre_v1/`, no los de `data/processed/`.

**Siguiente revisión:** continuar la lectura dirigida de candidatos restantes, sin
tratar los 92 pares inventariados como errores ni ampliar estas dos pruebas a
casos de duplicado, daño, acta o alternancia de personas.
