# Fórmulas de presentación y menciones de la cola actual

> Informe histórico de la versión de 9.165 filas / 669 alertas; sus IDs corresponden a esa versión.
> Estado vigente: [Cuatro ciclos de revisión](REVISION_LOOP_2026-09-07.md).

**Fecha:** 2026-09-07. **Anterior:** 9.165 filas / 672 alertas.
**Publicación:** **9.165 filas / 669 alertas; 173 pruebas y F0/F1 aprobados.**

## Alcance

Esta ronda **no modifica hablantes ni divide intervenciones**. Se revisó la
solicitud repetida de Corbo a Valdés y seis avisos nuevos de menciones de la ronda
anterior. Se leyeron los seis padres y extractos de contexto contiguo; no se
cotejaron PDFs ni hubo revisión humana independiente.

- [Excel de seguimiento](../data/processed/revision_783.xlsx): las seis lecturas
  están anotadas en **`Alertas_actuales`**.
- [Cuatro apariciones de la fórmula: antes y después](cambios_formulas_actuales_2026-09-07.csv).
- [Seis menciones: texto, decisión, intervalo y hash](menciones_actuales_revisadas_2026-09-07.csv).
- Registros: `data/curation/formulas_revisadas.json` y
  `data/curation/revisiones_menciones_actuales.json`.

## 1. Una fórmula exacta, sin absorber la exposición

Se incorporó `FORM-20260907-PRESENTACION-VALDES`:

> A continuación, el Presidente, don Vittorio Corbo, solicita al Gerente de División Estudios, don Rodrigo Valdés, que presente las Opciones de Política Monetaria.

Es una solicitud de presentación, no una opinión sobre la TPM. La coincidencia
requiere **la oración completa**, admitiendo sólo diferencias de espacios; no
basta que un discurso contenga «solicita». Añadir un desarrollo sustantivo impide
que esa coincidencia exacta lo clasifique como fórmula.

| Padre | ID actual | Cambio |
|---|---:|---|
| 644 | 848 | Duplicado no reconocido como fórmula → fórmula revisada. |
| 664 | 899 | Duplicado no reconocido como fórmula → fórmula revisada. |
| 727 | 968 | Se añade la nota de evidencia. Su variante con salto de línea no era un duplicado exacto; no se fuerza esa etiqueta. |
| 770 | 1037 | Duplicado no reconocido como fórmula → fórmula revisada. |

Las cuatro solicitudes siguen bajo **Corbo**; las exposiciones siguientes siguen
bajo **Valdés**, completas. Se conservan todas las repeticiones. El registro pasa
de 17 a **18 textos de fórmulas**: las 59 apariciones históricas documentadas más
estas cuatro citas actuales. Eso no equivale a 63 errores de atribución.

## 2. Seis menciones legítimas, no seis cambios de hablante

| Padre | ID actual | Hablante conservado | Lectura contextual |
|---|---:|---|---|
| 320 | 415 | Nicolás Eyzaguirre | Expone su evaluación del cobre y el petróleo en concordancia con Desormeaux. «Le parece» pertenece al Ministro, no a Desormeaux. |
| 1336 | 1747 | Pablo García | Responde al argumento previo de Marfán sobre el nerviosismo del modelo. Se conserva el cambio real Marfán → García; no hay retorno a Marfán dentro de la respuesta. |
| 1420 | 1851 | Esteban Jadresic | Desarrolla su argumento sobre liquidez y credit default swap, con referencias a García, De Ramón y Marfán, no nuevas intervenciones de ellos. |
| 2228 | 3052 | Andrés Velasco | Responde sobre los aspectos mencionados por el Presidente y desarrolla el cálculo y la distinción por plazo. El Presidente es referente del argumento. |
| 4574 | 6252 | Rodrigo Vergara | Comunica lo que Larraín le informó sobre asistencia parcial. Es discurso referido. La bienvenida a Vial y la designación de Marfán tampoco son turnos de ellos; Ricaurte inicia su exposición en 4575. |
| 4656 | 6337 | Rodrigo Vergara | Comunica que Larraín no asistirá y enviará comentarios por medio de Cerda. No se atribuye un turno a ninguno de ellos. Lehmann inicia la presentación en 4657. |

Cada entrada `MEN-20260907-{padre}` contiene hash del texto de origen, fecha,
actor, inicio y fin, citas y alcance. En 1336 se revisa **sólo el segmento de
García**, sin adjudicar el tramo anterior de Marfán a García.

Las seis advertencias `POSIBLE_OTRO_HABLANTE_O_MENCION` **permanecen visibles**.
No se debilita el detector para reducir el contador ni se marcan esas filas como
libres de alertas. En 4574 también se conserva la advertencia de atribución
heurística legada, que esta lectura de la mención no resuelve.

## 3. Una lectura visible y separada de las alertas

Se añadió `scripts/mention_reviews.py`, utilizado por F1 para validar el registro.
La lectura sólo se adjunta si siguen vigentes **texto, actor, fecha e intervalo
exacto de la fila**, ignorando sólo espacios en la comparación. Si cambia alguno,
la validación falla y exige revisar nuevamente; no reaplica una adjudicación a
un número de fila que ahora represente otro contenido.

El CSV `revision_pendientes.csv` y la hoja `Alertas_actuales` del Excel incluyen:

- `Estado_Lectura_Dirigida`: `MENCION_LEGITIMA_REVISADA` en estos seis casos.
- `Revision_Lectura_Dirigida`: ID de la entrada documental.
- `Alcance_Lectura_Dirigida`: motivo revisado, explicación y limitaciones.

Las demás filas dejan esas columnas vacías. **No son un nuevo `Fuente_Actor` ni
un ancla de continuidad**. No se modifican las 37 columnas de la base de auditoría
ni las 24 de la base final. La hoja de alertas pasa a diez columnas y el CSV de
pendientes a 24; ambos siguen mostrando sus motivos automáticos originales.

Cinco de estos padres no están en la instantánea original de 783 alertas. El
sexto, 4574, sí está, pero por el motivo legado que sigue pendiente. Por eso las
seis lecturas se informan **separadamente**, sin inflar las lecturas o cierres del
seguimiento histórico.

## 4. Comparación y pruebas

La comparación completa antes/después verificó:

- **Cero cambios de texto, actor, cargo, método de atribución, límites, IDs o turnos**.
- Sólo cuatro filas modificadas en la base: tres clasificaciones de fórmula con
  sus notas y estado de alerta, y la nota de evidencia de 727.
- Igualdad por contenido entre la construcción preliminar y la publicación.
- Seis anotaciones coincidentes en el CSV de pendientes y el Excel; sus seis
  avisos de mención y el aviso legado de 4574 siguen visibles.
- Entrada original XLSX intacta frente a Git.
- **173 pruebas aprobadas**, incluidas 15 nuevas: contexto, preservación de
  hablantes, hash, fecha, citas, límites, actor alterado, ID desplazado, alcance
  limitado, duplicación del registro, fórmula exacta y anotación del Excel.
- Pipeline completo y **F0/F1 aprobados antes de publicar**.
- **38 hashes de entradas/código y diez de salidas** verificados en el manifiesto.

La conservación de texto y turnos mantiene las exposiciones largas de las rondas
anteriores. F0/F1 y esta comparación no certifican pureza semántica del corpus.

## 5. Resultado y pendientes

| Métrica | Resultado |
|---|---:|
| Filas / bloques | 9.165 / 9.164 |
| Padres conservados | 7.219 / 7.219 |
| Palabras | 2.048.560 |
| Sesiones | 132 |
| Grupos de turno / multipárrafo | 8.789 / 285 |
| Máximo de filas por turno | 11 |
| Duplicados exactos | 557, sin cambios |
| Duplicados reconocidos como fórmula | 552 → 555 |
| Alertas de duplicado no formulario | 5 → 2 |
| **Filas con alguna alerta** | **672 → 669** |
| Menciones actuales documentadas en el registro nuevo | 6 |

La reducción de tres alertas es una **reclasificación procedimental**, no tres
hablantes corregidos. Los demás motivos permanecen: 43 anáforas, 264 atribuciones
legadas, 213 finales sin puntuación, 154 posibles menciones/mezclas, ocho breves y
seis variantes de identidad. Los motivos se superponen; no sumar sus cantidades
como si fueran filas distintas o errores confirmados.

La instantánea de 783 y sus estados **no cambian**: 515 pendientes contextuales,
59 fórmulas reclasificadas, 66 métodos actualizados, 97 intervalos modificados por
comparación, 22 correcciones dirigidas, siete breves válidos, ocho menciones
históricas revisadas, seis identidades pendientes, dos repeticiones sustantivas
y una continuidad documentada. Sus categorías siguen siendo 99 lecturas dirigidas,
163 comparaciones y 521 triajes; 645 intervalos originales se superponen con
alguna alerta actual. Las seis nuevas lecturas se muestran en un contador aparte.

Siguen pendientes las advertencias no adjudicadas, las anáforas contextuales,
el texto dañado, las variantes de identidad y los dos duplicados sustantivos de
Herrera, que no se eliminaron ni reclasificaron como fórmulas. El caso conjunto
2126 tampoco se asigna arbitrariamente a una sola persona. No se ha completado
la revisión exhaustiva de las 783 alertas ni el cotejo de las actas originales.
