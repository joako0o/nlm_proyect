# Revisión de cambios de hablante sin separador de puntuación

> Informe histórico de la ronda de 9.155 filas; sus pendientes e IDs corresponden a esa versión.
> El estado vigente está en [Reanudaciones y retornos](REVISION_REANUDACION_2026-09-07.md).

**Fecha:** 2026-09-07. **Base anterior:** 9.153 filas / 661 alertas.
**Salida publicada:** 9.155 filas / 661 alertas; **146 pruebas y F0/F1 aprobados**.

## Alcance

Cinco decisiones sobre pasajes del consolidado donde un cambio explícito de
hablante estaba concatenado con la frase anterior. Se leyeron los textos de los
cinco padres, incluidos sus desarrollos y retornos; no se cotejaron con PDFs.
La posible pérdida de puntuación o texto durante la extracción no se reconstruye.
Esto no constituye lectura exhaustiva del corpus ni revisión humana independiente.

- [Seguimiento de las 783 alertas originales](../data/processed/revision_783.xlsx).
- [Comparación: cinco padres y sus 18 segmentos actuales completos](cambios_concatenaciones_2026-09-07.csv).
- Base final: `data/processed/consolidado_base_referencia_final.xlsx`.
- Decisiones con hash, citas e intervalos: `data/curation/revisiones_hablantes.json`.

## 1. Decisiones y continuidad

| Padre | Fecha | Corrección dirigida | Filas antes → ahora |
|---|---|---|---:|
| 514 | 2005-12-13 | Corbo termina una frase incompleta sobre una clasificadora. «Con respecto al tipo de cambio, el Gerente de Mercados Financieros…» inicia la explicación de De Ramón, antes absorbida por Corbo. La referencia anterior a Marfán no es un turno. | 1 → 2 |
| 653 | 2006-04-13 | Desormeaux queda hasta «dado que el». «El Vicepresidente señor José De Gregorio indica…» abre la evaluación de De Gregorio; se une a su continuación ya reconocida y llega hasta su voto de 25 puntos base. | 2 → 2 |
| 1010 | 2006-12-14 | Se conservan Marfán → Magendzo → Valdés → Marfán y las menciones a Mario Marcel. Tras «ese es el», se recupera la intervención explícita de De Gregorio sobre actividad y costos laborales. | 4 → 5 |
| 1623 | 2008-01-10 | El comentario de Desormeaux termina antes de «Menciona el señor Magendzo…». Se adelanta el inicio de Magendzo y se conserva su exposición completa en un solo segmento de 11.058 caracteres. | 2 → 2 |
| 1652 | 2008-02-07 | La oferta de palabra del Presidente termina en «escenario». «En cuanto a mercados financieros, el Consejero señor Manuel Marfán señala…» y «Agrega el Consejero señor Marfán…» son una misma intervención. Se conservan los posteriores intercambios de García, Marfán y De Ramón. | 7 → 7 |

Los IDs de revisión son `HAB-20260907-{padre}`. Hay **cinco correcciones de
límites/atribución**, no cinco filas adicionales: el incremento neto es de dos.
En tres casos se recuperó el inicio del hablante y se unió a su continuación.
La exposición de Magendzo no se divide por cada «agrega», referencia al gerente
o cambio de tema. Su mención al Consejo tampoco transfiere al Consejo la autoría
del resto del análisis.

El dígito aislado **7** del padre 1623 permanece al final del tramo anterior,
en su posición original. Su conservación material no lo convierte en contenido
discursivo de Desormeaux ni certifica que sea un número de página. Tampoco se
completan las frases dañadas de Corbo, Desormeaux, Marfán o el Presidente.

## 2. Límite excepcional, no corte automático ante mayúsculas

El nuevo tipo `CONCATENACION_EXPLICITA_REVISADA` requiere:

- Una entrada individual con fecha, hash del padre, intervalo, citas y justificación.
- Espacio antes del inicio y una inicial mayúscula en el fragmento revisado.
- Sujeto explícito de habla reconocido y compatible con el actor documentado.
- Inicio fuera de comillas dobles rectas, curvas o angulares según el control existente.

La comprobación explícita también se aplica si el separador de oraciones ya
proponía ese inicio: una simple mención sin verbo de habla no autoriza la revisión.
No se añadieron verbos ni se relajaron globalmente las reglas de sujeto o de
continuidad. Sin la entrada revisada, el nuevo tipo de corte no se activa.
`CONTEXTO_REVISADO` sigue sin ser por sí solo un ancla para heredar hablantes.

## 3. Comparación y validaciones

La comparación automática de la publicación anterior con la nueva detectó
cambios de texto/actor **sólo en los cinco padres de la tabla**. Se comprobó:

- Igualdad por contenido entre la construcción preliminar y la publicación final.
- Conservación del texto de todos los padres entre versiones, ignorando sólo espacios.
- Cero cambios de cargo para segmentos con texto y actor idénticos.
- Entrada `data/raw/consolidado_final.xlsx` sin modificaciones frente a Git.
- Conservación de las exposiciones de García de 11 filas en los padres 60–70 y
  142–152, y de los casos negativos de menciones 3454, 3715 y 4266.
- Integridad de los **21 intervalos de hablante documentados** y seis revisiones de cargo.
- **146 pruebas aprobadas**, diez de ellas nuevas: secuencias, conservación,
  exposición larga, voto, ausencia de generalización, actor incompatible,
  comillas, límite sin espacio, mención sin habla y hash alterado.
- Pipeline completo `python scripts/preparar_data.py`: F0/F1 aprobados antes de publicar.
- **34 hashes de entradas/código y 10 de salidas** coincidentes con el manifiesto.

La comparación global no es lectura individual de los restantes padres ni una
auditoría semántica independiente del detector compartido por construcción y QA.

### Métricas publicadas

| Métrica | Resultado |
|---|---:|
| Padres conservados | 7.219 / 7.219 |
| Filas físicas / bloques | 9.155 / 9.154 |
| Sesiones | 132 |
| Palabras | 2.048.560, sin cambios |
| Máximo de caracteres por celda | 31.948 |
| Grupos de turno / multipárrafo | 8.779 / 285 |
| Máximo de filas por turno | 11 |
| Columnas de auditoría / finales | 37 / 24 |
| Fórmulas TPM contrastadas | 310 |
| Filas con alertas | 661 |

## 4. Por qué el total de alertas no baja

Las alertas de `POSIBLE_OTRO_HABLANTE_O_MENCION` pasan de **158 a 153**;
las de `FINAL_SIN_PUNTUACION`, de **205 a 210**. Los cortes exponen frases sin
cierre y el dígito aislado, que antes quedaban ocultos dentro de bloques mayores.
No se inventa puntuación para reducir el contador.

Se mantienen 265 avisos de atribución legada, 37 de anáfora, ocho de brevedad,
seis de identidad y dos de duplicados no formularios. Los motivos se superponen:
**661 alertas no equivalen a 661 errores confirmados ni a casos ya resueltos**.
Los duplicados exactos suben de 551 a 552 y los formularios de 549 a 550 por
la nueva segmentación; no se eliminó ningún texto repetido.

### Seguimiento de la instantánea original de 783

| Estado | Intervalos |
|---|---:|
| Pendiente de lectura contextual | 521 |
| Fórmula procedimental reclasificada | 59 |
| Método actualizado | 65 |
| Segmentación o actor modificado por comparación | 96 |
| Corrección dirigida aplicada | 18 |
| Breve válido revisado | 7 |
| Mención legítima revisada | 8 |
| Identidad pendiente | 6 |
| Repetición sustantiva pendiente | 2 |
| Continuidad entre padres revisada | 1 |

Cinco intervalos pasan de pendiente a corrección dirigida. Los **18** de ese
estado incluyen los trece anteriores: no son dieciocho correcciones nuevas.
Hay 95 intervalos vinculados a lectura dirigida, 161 a comparación automática y
527 a triaje; esas categorías no significan cierre semántico completo.
647 intervalos originales todavía se superponen con alguna alerta actual.
La instantánea original no se modificó.

## 5. Pendientes explícitos

- **Padre 664:** la inspección inicial detectó una posible mezcla en la suspensión
  y reanudación y una introducción de Valdés cuya exposición exige revisar el
  contexto de cargos y retornos. No se corrigió ni se considera revisado por completo;
  su texto y atribuciones permanecen como en la versión anterior.
- Los candidatos de cargos/variantes de extracción **1904 y 2462** siguen sin
  adjudicación en esta ronda.
- Se mantienen los pendientes de identidad, repeticiones sustantivas y otros
  avisos contextuales. No se asigna arbitrariamente un solo actor al caso conjunto 2126.

Para análisis individual, usar padre e intervalo de texto para enlazar versiones;
los IDs numéricos de fila pueden desplazarse. Pasar F0/F1 no certifica pureza de
hablante en cada intervalo ni sustituye el cotejo con las actas originales.
