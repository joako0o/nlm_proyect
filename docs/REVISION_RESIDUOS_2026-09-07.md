# Revisión acotada de residuos: respuesta del Presidente y acuerdos del Consejo

> **Informe histórico.** La publicación posterior a esta tanda está en [intercambios acotados](REVISION_INTERCAMBIOS_2026-09-07.md): 9.211 filas / 635 alertas / 237 pruebas. Las métricas, IDs y el checkpoint de este documento corresponden a la tanda anterior. Los enlaces a `data/processed/` abren la versión vigente.

**Fecha:** 2026-09-07. **Inicio:** 9.205 filas / 634 alertas / 209 pruebas.
**Publicación:** **9.207 filas / 635 alertas / 222 pruebas; F0/F1 aprobados.**

## Alcance y entregables

Continuación del [segundo bloque contextual](REVISION_LOOP2_2026-09-07.md).
Se delimitó la respuesta del Presidente en 2981 y se separó el comienzo formal
del acuerdo institucional en diez padres. La comparación arroja **11 padres
modificados, 29 segmentos resultantes y dos filas adicionales**. No hubo cambios
de cargo en segmentos que conservaron texto y actor.

- [Excel de seguimiento y cola vigente](../data/processed/revision_783.xlsx).
- Base final: `data/processed/consolidado_base_referencia_final.xlsx`.
- [Evidencia de los 11 padres](cambios_residuos_2026-09-07.csv): hash de la fuente,
  fecha, IDs y actores anteriores, IDs/actores/métodos/alertas vigentes y texto
  completo de los 29 segmentos. Los IDs actuales son de esta publicación.
- [Punto de reanudación](estado_revision_residuos_2026-09-07.json): pendientes
  explícitos y candidatos de triaje; no es un proceso activo en segundo plano.

La lectura del agente se limita a los intervalos documentados y su entorno.
**No hubo cotejo PDF ni revisión humana independiente en esta tanda, ni lectura
exhaustiva de los padres completos.** Una corrección parcial no certifica todo
el padre, aunque algún segmento no tenga alertas automáticas.

## 1. Respuesta del Presidente, padre 2981 — 2010-03-18

La pregunta de Marshall termina con `el -1,1% y el - 0,7%,`. Le sigue:

> señalando el señor Presidente que es el cambio en la tasa de crecimiento respecto a un escenario pre terremoto. Agrega que como consecuencia del terremoto, el nivel del PIB podría disminuir 2% en el primer trimestre y 1,4% en el segundo.

El sujeto de la respuesta está explícito. `Agrega…` continúa con el Presidente;
`El señor Soto complementa…` devuelve la palabra a Soto. Se añadió la revisión
**HAB-20260907-2981**, con hash, límites y tres citas del mismo padre. El registro
suma **43 intervalos de hablante documentados**. No se duplicó la revisión.

| Segmento vigente | Actor | Caracteres |
|---|---|---:|
| 4333 | Marshall | 101 |
| 4334 | Soto | 1.089 |
| 4335 | García | 282 |
| 4336 | Soto | 3.212 |
| 4337 | Marshall | 85 |
| 4338 | De Gregorio | 237 |
| 4339 | Soto | 213 |

Se conservaron exactamente los primeros cuatro segmentos de la publicación
anterior, incluida la exposición larga de Soto, y el complemento final. La
respuesta no se distribuyó entre hablantes por proximidad.

### Salvaguardas del límite

`GERUNDIO_SENALANDO_EXPLICITO` es una excepción **individual con revisión
validada**, no un detector general de gerundios. Exige coma o punto y coma
previo, `señalando el/la…`, sujeto explícito compatible con el actor revisado,
complemento declarativo `que` después del sujeto y posición fuera de comillas.
Para validar el sujeto se proyecta temporalmente `señalando` a `señala`; **el
texto exportado conserva el gerundio y la puntuación originales**. Sin la
revisión, este padre mantiene seis segmentos; la excepción produce siete.

La pregunta separada termina en coma, por lo que ahora dispara
`FINAL_SIN_PUNTUACION`. Esto explica **634 → 635 filas con alertas** y
**227 → 228** avisos de ese motivo. No se inventó un punto ni se eliminó la alerta
para mejorar el contador. La variación de alertas no es un conteo de errores.

## 2. Acuerdo institucional: diez límites

Se reconoce de forma estrecha el comienzo:

> En mérito de lo anterior, el Consejo, por la unanimidad de sus miembros, adopta el siguiente Acuerdo

La intercalación `por la unanimidad de sus miembros` impedía detectar ese límite.
Ahora la declaración formal se atribuye al Consejo, no al votante precedente.
Se leyeron el cierre del voto y el comienzo del acuerdo en estos diez padres:

| Padre | Fecha | Segmentos antes → ahora |
|---:|---|---:|
| 219 | 2005-04-07 | 2 → 2 |
| 294 | 2005-06-09 | 2 → 2 |
| 310 | 2005-07-12 | 3 → 3 |
| 503 | 2005-11-10 | 1 → 2 |
| 526 | 2005-12-13 | 2 → 2 |
| 594 | 2006-02-09 | 2 → 2 |
| 654 | 2006-04-13 | 2 → 2 |
| 674 | 2006-05-11 | 2 → 2 |
| 780 | 2006-07-13 | 3 → 3 |
| 1020 | 2006-12-14 | 2 → 2 |

En nueve casos el acuerdo ya tenía una parte institucional: se adelantó su
inicio sin crear otra fila. En 503 se creó el segmento institucional separado.
El contenido personal del voto permanece con Corbo. La búsqueda mecánica del
patrón dio 23 padres; los otros 13 ya tenían ese tramo institucional y no
cambiaron. **23 coincidencias no equivalen a 23 lecturas contextuales completas.**

La regla no admite propuestas como `podría adoptar` ni menciones del Consejo
introducidas dentro de lo que dice un participante. Hay regresiones de estos
negativos y de una cita entre comillas. No se alteraron las anomalías de la
fuente, por ejemplo `89-01-0602109` en 594 ni la redacción de la TPM en 674.

### El comienzo de Corbo en 780 sigue pendiente

La separación cierta del Consejo **no resuelve** el texto anterior que comienza
`En la economía nacional…`, sin encabezado, después del voto de De Gregorio y
antes de menciones explícitas a Corbo. Se conservó íntegro el primer segmento
previo, incluida su alerta `POSIBLE_OTRO_HABLANTE_O_MENCION`. Corbo sigue
comenzando en el límite existente `Señala el Presidente, señor Corbo…`.
Esto no certifica que la atribución anterior sea correcta: falta evidencia
para adjudicar un comienzo más temprano sin inferirlo por proximidad.

Se intentó consultar la colección oficial de 2006 en
`https://repositoriodigital.bcentral.cl/xmlui/handle/20.500.12580/4530`.
La respuesta fue **“Verificación de acceso | Repositorio Digital”**, con
verificación de persona; no se obtuvo ni leyó el PDF. Las búsquedas adicionales
no aportaron evidencia útil y no sustentan ninguna adjudicación.

## 3. Verificación de la publicación

- **222 pruebas aprobadas**, 13 más que antes: límites positivos con coma/punto y
  coma, sujeto incorrecto, separador ausente incluso en límite de oración,
  gerundio de referencia/objeto sin sujeto declarativo, comillas, hash alterado,
  conservación, continuidad del expositor y transición formal del Consejo.
- `scripts/preparar_data.py` ejecutado completo: construcción aislada, exportación,
  **F0/F1 aprobados**, publicación. El contenido publicado coincide con el primer
  ensayo aislado; el refuerzo de validación no amplió su alcance.
- Conservación global de las **7.219 fuentes**, ignorando sólo espacios:
  **2.048.560 palabras**, 9.206 bloques en 9.207 filas físicas, máximo 31.948
  caracteres por celda. El Excel de origen sigue idéntico al de `HEAD`.
- Comparación de toda la base: exactamente los 11 padres enumerados; en los otros
  7.208 no cambian texto/actor, cargo/fuente, método, relación de continuidad,
  tipo de acta ni motivos de revisión.
- Partición de turnos no afectados idéntica, descontando renumeración de IDs.
  Conservados los once enlaces anteriores y Soto **2408 → 2409**; conservadas
  las dos exposiciones de García de once filas, padres **60–70** y **142–152**.
- **8.819 grupos de turno; 297 multipárrafo; máximo 11 filas**. No se fusionaron
  arbitrariamente párrafos ni se partieron presentaciones por su longitud.
- **41 hashes de entradas/código y 10 de salidas verificados** contra el manifiesto.
- 132 sesiones; 51 etiquetas de actor / 50 personas según F0; 310 contrastes TPM;
  559 duplicados exactos, 557 de fórmula. Los controles comparten reconocedores;
  no son una auditoría semántica independiente ni un cotejo documental completo.

## 4. Cola y continuación

El seguimiento de las **783 filas originales no cambia de estados**: 471
pendientes de lectura contextual; 59 fórmulas; 71 con método actualizado; 118
modificadas por comparación; 40 con corrección dirigida; siete breves válidos;
ocho menciones históricas revisadas; seis identidades; dos repeticiones y una
continuidad. Por tipo: 117 lecturas dirigidas por agente, 189 comparaciones y
477 triajes. **611 intervalos originales** aún se solapan con alertas actuales.
La nueva respuesta en 2981 no convierte automáticamente una fila histórica
adicional en cierre semántico.

Las **seis menciones actuales documentadas** siguen separadas de ese seguimiento
y conservan `POSIBLE_OTRO_HABLANTE_O_MENCION`; 4574 también conserva su aviso de
atribución legada. Las 635 alertas vigentes incluyen motivos superpuestos:
111 de otro hablante/mención, 42 anáforas, 259 atribuciones legadas, 228 finales
sin puntuación, ocho fragmentos breves, seis variantes de identidad y dos
duplicados no formulaicos.

El checkpoint conserva **97 candidatos de otro hablante sin anotación de
mención** bajo el mismo filtro anterior; no son 97 errores confirmados ni una
lista de cierres. Prioridades explícitas: comienzo de Corbo en **780**, intervención
conjunta en **2126** e intercambio complejo en **2661**. La respuesta concreta
por gerundio en 2981 ya está delimitada, sin certificar el padre completo.
