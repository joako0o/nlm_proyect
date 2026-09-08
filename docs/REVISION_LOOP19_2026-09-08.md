# LOOP19 — Continuidades acotadas y exposiciones largas, sin cortes artificiales

**2026-09-08 · [PR #3](https://github.com/joako0o/nlm_proyect/pull/3)**

Base: `09834ae6a6d6a5604b6ba40af1709a78b37adb47`, [LOOP18](REVISION_LOOP18_2026-09-08.md).
Lecturas dirigidas por agente del texto disponible. **Sin nuevo cotejo PDF ni muestra independiente con/sin alertas.**

## Resultado validado y publicado

| Medida | LOOP18 | LOOP19 |
|---|---:|---:|
| Filas físicas / bloques de texto | 9.551 / 9.550 | **9.551 / 9.550** |
| Grupos de turno | 9.140 | **9.136** |
| Grupos multifila / máximo de filas | 315 / 11 | **319 / 11** |
| Filas con alertas / padres alertados | 346 / 306 | **349 / 309** |
| Pruebas | 1.200 | **1.230** |
| Intervalos de hablante revisados / padres | 276 / 259 | **279 / 262** |
| Advertencias contextuales activas | 36 | **39** |
| Lecturas actuales exactas | 11 legítimas | **11 legítimas + 1 pendiente** |

**No se añadieron separaciones ni se reasignaron actores en esta pasada.** Se aplican cuatro enlaces discursivos por lectura acotada y tres revisiones de metadatos/nombre. Se registra además la lectura pendiente de 6185. No se equipara una lectura con un caso resuelto.

Los textos, límites, orden y actores de **las 9.551 filas** son exactamente los anteriores. Siete padres presentan diferencias de campos no secuenciales: los tres de metadatos y los cuatro extremos posteriores donde se escribe el enlace. Los **otros 7.212 padres** mantienen esos campos, excluyendo `ID_Turno`; las cuatro uniones cambian la pertenencia al grupo de sus ocho extremos. Ningún grupo ajeno a esas uniones cambia sus miembros.

- [Comparación global antes/después y hashes](comparacion_loop19_2026-09-08.json)
- [Detalle de las siete filas modificadas, antes/después](cambios_loop19_2026-09-08.csv)
- [Checkpoint y pendientes vigentes](estado_revision_loop19_2026-09-08.json)

## 1. Cuatro exposiciones continúan en el padre siguiente

Se leyeron **completos los ocho intervalos extremos**. Esto no equivale a leer todos los demás segmentos de los padres izquierdos.

| Enlace | Hablante | Caracteres de los extremos | Evidencia discursiva |
|---|---|---:|---|
| **3887 → 3888** | Enrique Marshall | 2.667 + 1.627 | La evaluación económica y de riesgos concluye con «con estos antecedentes» y su opción de voto. |
| **4224 → 4225** | Sergio Lehmann | 966 + 2.853 | CDS, expectativas, tasas y paridades; «en este contexto» enlaza la exposición financiera. |
| **4941 → 4942** | Claudio Soto | 2.079 + 291 | La explicación de las sorpresas de inflación concluye con la proyección, «en razón de lo expuesto precedentemente». |
| **5910 → 5911** | Sergio Lehmann | 1.848 + 10.080 | Desarrollo de actividad y precios; la presentación continúa con cuadros, empleo, brechas, inflación y commodities. |

En 5911 se conserva el desarrollo de **10.080 caracteres** completo: los cambios de indicador no se convierten en turnos de otras personas.

### Mecanismo y límites

El nuevo [registro de continuidades de hablante](../data/curation/revisiones_continuidad_hablantes.json) exige fecha, actor, texto y límites exactos de ambos extremos, hashes de ambos padres, fuentes de atribución y evidencia local. Se aplica **después** de determinar los hablantes.

- Sólo habilita esos cuatro enlaces entre filas consecutivas: `Relacion_Turno=CONTINUIDAD_REVISADA` y un mismo `ID_Turno`.
- **No fusiona textos físicos, no cambia actores ni crea alias.**
- El extremo anterior `CONTEXTO_REVISADO` **sigue sin ancla**. El posterior conserva **su propia ancla explícita**. La revisión contextual no se convierte en una regla global de herencia.
- No atraviesa otra voz, sesión, cesión de palabra, sección institucional ni advertencias bloqueantes. Cambios de texto, actor, método o límites invalidan la aplicación.
- La construcción y el QA vuelven a comprobar que aparecen los cuatro extremos exactos, con antecedente, grupo y anclas correctos. Una relación revisada sin registro se rechaza.

**4745 → 4746 y 6561 → 6562 permanecen pendientes.** Sus finales «A continuación,.» no justifican forzar una continuidad ni completar texto ausente.

## 2. Tres advertencias de nombre, sin cambiar la segmentación

| Padre | Intervalo completo leído | Resultado |
|---|---:|---|
| **2349** | Soto, 599 caracteres | Conserva «Claudia Soto»; el tramo de García no se modifica. |
| **3050** | Soto, 3.025 caracteres | Conserva el desarrollo y las menciones a Claudia; la pregunta de Claro y la respuesta posterior de Soto de 384 caracteres siguen separadas. |
| **3315** | Soto, 1.239 caracteres | Conserva «Claudia Soto» y el tramo previo de Vicuña de 165 caracteres. |

Las nóminas **2301, 3023 y 3278** identifican localmente a **Claudio Soto Gamboa**. Cada revisión tiene hash y límites, y añade una advertencia independiente `NOMBRE_EN_DISCURSO_POR_VERIFICAR`. No se reescribe el OCR ni se generaliza Claudia como alias.

Las tres filas estaban antes sin alerta: el aumento **346 → 349** corresponde a hacer visibles estas discrepancias, no a tres separaciones nuevas. La atribución se documenta como `CONTEXTO_REVISADO`; se retiran únicamente sus anclas anteriores, sin perder ningún enlace entre padres.

### 3454: lectura hecha, cambio aplazado para no romper continuidad

Se leyó su intervalo de **2.548 caracteres**. La referencia a una pregunta de Marfán forma parte del desarrollo de Soto y no delimita un turno autónomo. Permanecen los literales **Claudia/Claudias Soto**; la nómina **3433** identifica a Claudio Soto Gamboa.

La comprobación global previa detectó que 3454 ya está unido a **3455**. Convertirlo en revisión/advertencia bloqueante con el mecanismo actual rompería esa exposición. Por ello **no se añade una revisión de hablante ni una alerta activa en 3454**: texto, método, ancla y continuidad quedan intactos, y el pendiente nominal se registra en el checkpoint. No se presenta como nombre resuelto ni como uno de los tres cambios aplicados. El control previo de **224 → 225 → 226** y «Rabio García» se conserva por la misma cautela.

## 3. 6185: lectura íntegra, aporte de Bernier todavía sin delimitar

Se leyó la exposición disponible de Lehmann de **20.118 caracteres**, con el contexto anterior y el agradecimiento presidencial de **6186**. La pregunta referida de Claro no se convierte en un turno intercalado.

El pasaje sobre Colombia y su programa de compras de divisas termina con **«conforme señala el Gerente de Mercados Nacionales señor Matías Bernier»**. Atribuye información, pero no permite resolver con seguridad si se trata de una referencia o de un aporte oral autónomo ni dónde comenzaría éste. No se transfiere a Bernier la exposición de commodities ni se fabrica un segmento.

Se incorpora una lectura exacta, con hash, evidencia y decisión **`PENDIENTE_DELIMITAR_APORTE`**. Su alerta **`POSIBLE_OTRO_HABLANTE_O_MENCION` permanece activa** y su texto, actor y segmentación quedan sin cambios.

Hay ahora **12 lecturas actuales = 11 menciones legítimas previas + 1 lectura pendiente**, no doce menciones resueltas. El campo heredado `menciones_actuales_documentadas` cuenta los doce registros; el nuevo `lecturas_actuales_por_estado` los distingue en ambos resúmenes. La cola CSV muestra explícitamente el estado pendiente de 6185. Son unidades distintas de las **ocho menciones legítimas históricas** de la cola de 783.

## 4. Verificación y preservación global

**1.230 pruebas**, treinta nuevas: doce contratos exactos de fuente/segmentos y dieciocho controles de comportamiento, evidencia, barreras y pendientes. Se actualizaron los conteos acumulados y el contrato de método de 3315, sin debilitar sus controles de actor/texto/límites.

- Ensayo aislado y `python scripts/preparar_data.py` terminados correctamente; **F0/F1 sin errores bloqueantes**. Publicación idéntica al ensayo campo por campo.
- **73 hashes de entradas/código y once de salidas verificados.** Fuentes raw/external intactas.
- Reconstrucción de los **7.219 padres** comprobada contra las fuentes disponibles, ignorando sólo espacios; además, cada fila mantiene **exactamente su texto anterior**, no sólo el texto normalizado. **2.048.560 palabras**, 132 sesiones, 310 contrastes TPM.
- **276 revisiones anteriores y 36 advertencias activas anteriores idénticas**, al igual que las once lecturas previas y el archivo completo del retiro de la advertencia obsoleta de 6443. No se retira ninguna advertencia en LOOP19.
- **Ningún enlace previo perdido; sólo cuatro nuevos.** Comparación exacta de la composición de todos los grupos salvo esas uniones. Incluye las exposiciones de García de once filas, 224→225→226, 3454→3455 y 2790→2791. No reaparece 5402→5403.
- Al permanecer iguales todos los límites y actores, quedan conservados 506/1572, la recuperación parcial de 780, 6009/6025/6443, el retorno de Ricaurte de 4594, las anclas posteriores 1092/2790/780/2778/2909, las recuperaciones de Nacrur/Mattar/Álvarez, 4054 después del comunicado y los demás controles previos.
- Esquemas XLSX **37/24**; 21 fórmulas y tres documentos leídos intactos. **Larraín autor escrito ≠ Vergara lector**; no se infiere presencia ni intervención oral del autor.
- **54 etiquetas nominales**, sin altas ni armonización global de identidades. Siguen **21 filas actuales** con variante Ricaurte.

La cola histórica mantiene sus estados y tipos de revisión: **104 pendientes de lectura contextual**, **500 comparaciones / 178 lecturas dirigidas / 105 triajes**, seis intervalos independientes con variante de identidad y **283 intervalos históricos con alertas actuales**. Un estado principal no cierra sus motivos residuales. Estas unidades no se suman con las 349 filas actuales ni con las 21 advertencias actuales de identidad.

## 5. Qué significa daño o «párrafo roto» aquí

No significa «párrafo largo» ni «presentación de muchos párrafos». Se refiere a texto aparentemente incompleto o mal unido, por ejemplo «A continuación,.» o una frase interrumpida. **Sin cotejo de la fuente no se afirma si el defecto proviene del acta, del OCR, de una tabla o de la extracción.** No se inventan palabras para repararlo y no se deduce otro hablante sólo por ese daño.

El barrido de nombres, cargos y verbos fue **triaje dirigido**, no muestreo representativo ni auditoría exhaustiva. Las referencias a declaraciones de terceros o extranjeros no se convierten en participantes de la sesión.

Siguen abiertos 3454/226, 6185, el puente de 780, las dos continuidades dañadas, los residuos conjuntos de 3191/5367/2126/2661/2704/3989, discrepancias de nombres/cargos y las variantes de identidad. Se requiere cotejo documental y una muestra independiente con y sin alertas. **F0/F1 no certifican pureza total de hablante.**

Sin proceso activo. Verificaciones locales; no se incorpora el workflow de GitHub Actions fuera de alcance del PR.
