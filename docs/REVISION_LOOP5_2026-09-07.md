# Quinto bloque: lote posterior a la apertura del PR

**Fecha:** 2026-09-07. **PR:** [#3](https://github.com/joako0o/nlm_proyect/pull/3).
**Inicio:** 9.245 filas / 618 alertas / 339 pruebas.
**Publicación:** **9.251 filas / 615 alertas / 351 pruebas; F0/F1 aprobados.**

Se abrió primero el PR con el trabajo acumulado y después se completó este lote
en la misma rama. **Cuatro padres pasan de cinco a once segmentos**, con seis
filas adicionales. La publicación está terminada; no hay un proceso activo.

## Entregables

- [Excel final](../data/processed/consolidado_base_referencia_final.xlsx).
- [Seguimiento y cola vigente](../data/processed/revision_783.xlsx).
- [Cuatro padres y once segmentos completos, con hashes e IDs](cambios_loop5_2026-09-07.csv).
- [Comparación antes/después y comprobaciones globales](comparacion_loop5_2026-09-07.json).
- [Checkpoint de pendientes](estado_revision_loop5_2026-09-07.json).

El [informe anterior](REVISION_LOOP4_2026-09-07.md) conserva su estado histórico.
Los IDs de fila pueden cambiar; los padres se refieren al consolidado de origen.

## Decisiones de lectura

| Padre | Fecha | Secuencia resultante | Caracteres por segmento |
|---:|---|---|---|
| 4384 | 2011-10-13 | Marfán → Presidente → Consejo/acta | 477 / 134 / 143 |
| 4420 | 2011-11-15 | Lehmann → Claro → Lehmann | 706 / 214 / 559 |
| 4421 | 2011-11-15 | Herrera → Lehmann | 798 / 698 |
| 4502 | 2011-12-13 | Soto → Presidente → Consejo/acta | 2.418 / 127 / 79 |

- **4384:** la hipótesis de Marfán sobre demanda y tasas termina antes de
  `Al no haber consultas o comentarios adicionales…`. La suspensión corresponde
  al Presidente De Gregorio y la reanudación con incorporación del Ministro es
  institucional. Se leyeron también 4383 y 4385; no se convierte al Ministro,
  mencionado como incorporado, en un nuevo hablante.
- **4420:** al leer el contexto apareció la opinión de Claro sobre el petróleo
  y la recuperación de Estados Unidos, entre la exposición y la respuesta de
  Lehmann. Se delimitó `En opinión del Consejero señor Sebastián Claro…` hasta
  `El señor Lehmann manifiesta…`. **El pasaje no tenía aviso automático de otro
  hablante**: el caso muestra por qué la cola no equivale a una revisión exhaustiva.
- **4421:** Herrera explica WTI/Brent y cañerías; Lehmann retoma al exhibir la
  lámina 31. Su turno empieza en `A continuación… exhibe`, **no sólo en la última
  oración** `Al finalizar su presentación…`. Se mantienen juntos gráfico,
  comparación de commodities y curvas de futuros. 4422 agradece su presentación.
- **4502:** se conserva íntegra la extensa respuesta de Soto sobre colocaciones,
  empleo e IMACEC. Se separa la suspensión del Presidente Vergara y después el
  registro institucional. Se leyeron 4501 y 4503 para distinguir exposición,
  suspensión y posterior cesión de palabra a Herrera.

Se añadieron cuatro revisiones individuales con hash, citas y límites. No se
habilitó una atribución general por la frase `En opinión` ni por proximidad.
El fin de cada intervalo se verifica contra el contenido resultante: no se
supone que guardar un offset final cree por sí solo un corte.

### Reanudación dañada en 4502

Se conserva exactamente:

> i,- Siendo las 16:00 horas, se reanuda la Reunión de Política Monetaria N° 179.

El parser reconoce **sólo esta fórmula literal constatada**, sin borrar `i,-`.
Para abrir el límite exige punto y espacio previos, fuera de comillas. La
clasificación institucional exige la fórmula completa. Las pruebas rechazan
otras numeraciones, otros prefijos OCR, referencias y citas. No es una regla
que elimine cualquier basura OCR ni una reparación del original.

## Validación final

- **351 pruebas locales aprobadas**, doce nuevas. Incluyen secuencias completas,
  longitudes, hashes, conservación, límites revisados, retorno antes del cierre,
  citas y restricciones de la fórmula dañada.
- Construcción aislada y comparación global, seguida del pipeline completo con
  **F0/F1 aprobados**. El contenido publicado coincide con el ensayo.
- **7.219 padres conservados** ignorando sólo espacios; exactamente cuatro con
  cambios de segmentación/actor y **ningún cambio adicional de metadatos
  semánticos** en los restantes. Los segmentos idénticos en texto y actor
  mantienen cargo, fuentes, motivos, relación, categorías y duplicados.
- **18 enlaces de continuidad comprobados**, incluidos 3810 → 3811 y 3812 → 3813.
  La partición de grupos no afectados permanece igual. Se preservan las dos
  exposiciones de García de once filas (60–70 y 142–152).
- **74 revisiones de hablante**: las 70 anteriores son idénticas y se añaden cuatro.
  Las ocho anotaciones actuales de menciones permanecen idénticas y conservan
  sus avisos, incluida la atribución legada adicional de 4574.
- **49 hashes de entradas/código y diez hashes de salidas verificados**. El Excel
  de origen permanece idéntico al del commit inicial del PR.
- 9.250 bloques en 9.251 filas físicas, 2.048.560 palabras, máximo 31.948 caracteres
  por celda; 8.859 grupos de turno, **301 multipárrafo**, máximo once filas.
  132 sesiones y 310 contrastes TPM, sin errores bloqueantes.

Estos son controles locales, no checks remotos de GitHub ni una certificación
semántica independiente. La conexión rechazó el permiso `workflows`; el archivo
propuesto `.github/workflows/data-quality.yml` quedó guardado localmente, **fuera
del PR**. Para incluirlo habrá que revisar/reconectar GitHub en Arena con los
permisos necesarios. No se solicitaron credenciales ni se configuraron secretos.

## Alertas y pendientes

Las filas con alertas pasan de **618 a 615**; el motivo de posible otro hablante
pasa de 79 a 76. Los demás motivos permanecen iguales. Los tres avisos menos
corresponden a 4384, 4421 y 4502; 4420 se encontró por lectura contextual.
**Las alertas no son errores confirmados y su ausencia no certifica pureza.**

En las 783 originales hay 437 pendientes de lectura contextual, 59 fórmulas,
72 métodos actualizados, 123 cambios por comparación, 68 correcciones dirigidas,
siete breves, ocho menciones históricas, seis identidades, dos repeticiones y una
continuidad. Por tipo: 145 lecturas del agente, 195 comparaciones y 443 triajes;
590 intervalos originales se solapan con alertas actuales. Las ocho menciones
actuales se cuentan aparte; estos estados no cierran padres completos.

Quedan **60 candidatos** bajo el filtro de otro hablante sin anotación de mención.
Persisten 3191/2126 por intervenciones conjuntas, 780 por cotejo documental,
2661/2704 por confirmaciones pasivas, 2667/3107 por daños de origen y 5647 por el
compromiso de Lehmann y la continuidad posterior. No se forzaron los enlaces
contextuales 3887 → 3888 y 4224 → 4225. Faltan continuar la cola y la revisión
semántica independiente de una muestra con y sin alertas. **No hubo nuevo
cotejo PDF ni revisión humana independiente en este lote.**
