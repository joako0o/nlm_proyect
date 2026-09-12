# Auditoría metodológica — capa hawkish/dovish v1

**Fecha:** 2026-09-11 · **Artefactos:** `auditoria_metodologica.json`, `ruido_oro.json`, `efecto_ventana.json`, `deriva_temporal.json`, `calibracion_confianza.json`, `contraste_lexico_publicado.json`, `ensemble_por_sesion.json` y `rendimiento_reponderado.json`, todos en `data/releases/hawkish_dovish_v1/` · **Scripts:** `auditar_`, `medir_ruido_oro_`, `medir_efecto_ventana_`, `probar_deriva_temporal_`, `medir_calibracion_`, `contrastar_lexico_publicado_`, `probar_ensemble_por_sesion_` y `reponderar_rendimiento_por_decil_` + `hawkish_dovish.py`

Auditoría de lo entregado, contrastada contra cómo se mide el tono hawkish/dovish en la literatura de banca central. **Diez hallazgos**: cuatro son defectos que el informe publicado **no medía** (1, 2, 3 y 7); uno es una validación ausente que sí se pudo hacer con los datos del repo (4); uno documenta la distancia al estado del arte (5); uno es un remedio estándar que se probó y se **refutó** (6); uno es una validación que se midió y resultó **no realizable** con lo que hay (8); uno mide hasta dónde llega la fuga del hallazgo 2 sobre los veredictos publicados (9); y uno mide si el diseño de muestreo infla el rendimiento publicado (10). Todo lo que se afirma abajo sale de un artefacto reproducible, incluido lo que no se pudo cerrar.

---

## Hallazgo 1 — El modelo publicado no generaliza en el tiempo (severo)

`pliegues()` valida con una CV aleatoria que mezcla 2005 con 2015. Eso supone que las intervenciones son intercambiables. No lo son.

**Rolling-origin** (entrenar con todo lo anterior, probar con el año siguiente), misma configuración 600/30/bal:

| Año prueba | n | macro-F1 | accuracy |
|---|---|---|---|
| 2008 | 44 | 0,498 | 0,659 |
| 2009 | 44 | **0,301** | 0,523 |
| 2010 | 49 | 0,447 | 0,735 |
| 2011 | 44 | 0,591 | 0,727 |
| 2012 | 49 | 0,341 | 0,776 |
| 2013 | 54 | 0,407 | 0,778 |
| 2014 | 52 | 0,587 | 0,865 |
| 2015 | 45 | 0,475 | 0,756 |
| **media** | | **0,456** (sd 0,105) | **0,727** |

Contra **0,685 ± 0,015** publicado. Es decir: el número publicado describe *interpolar dentro del período*, no *predecir un período nuevo*. La accuracy se sostiene en 0,727 porque NEUTRAL domina; lo que colapsa son las clases minoritarias, que es justo lo que el macro-F1 está diseñado para exhibir.

**La causa no es el modelo: es desplazamiento de etiquetas.**

| Período | n | H | N | D |
|---|---|---|---|---|
| 2005-2007 | 119 | 25,2% | 66,4% | 8,4% |
| 2008-2009 | 88 | 12,5% | 56,8% | **30,7%** |
| 2010-2012 | 142 | 15,5% | 75,4% | 9,2% |
| 2013-2015 | 151 | 5,3% | 70,9% | **23,8%** |

Dovish va de 8,4% a 30,7% a 9,2% a 23,8%. Eso es historia monetaria real —ciclo de alzas, crisis, normalización, inflación baja—, no un artefacto de etiquetado. Pero rompe la intercambiabilidad, y ningún reentrenamiento la arregla.

**Qué cambia:** para el artefacto entregado (puntuar el corpus 2005-2015 con un modelo entrenado en ese mismo período) el 0,685 sigue siendo defendible. Para **cualquier** aplicación a reuniones nuevas el número honesto es ~0,46 de macro-F1. El informe y el README no distinguían los dos casos; ahora lo hacen.

---

## Hallazgo 2 — La validación cruzada filtra información entre sesiones (menor pero real)

`pliegues()` baraja por turno. Los turnos de una misma RPM comparten día, discusión y vocabulario.

- **90,7%** de las 130 sesiones del oro quedan repartidas en más de un pliegue.
- CV por turno **0,6848** vs CV agrupada por sesión **0,6724**; diferencia **−0,0124** (sd 0,0183), menor en **7 de 10** semillas.

El efecto es real pero chico: −0,012 contra una sd de CV de 0,015. No invalida nada, pero el 0,685 publicado es ligeramente optimista y la cifra limpia es ~0,672.

Su alcance sobre los veredictos publicados —selección de configuración y descarte del ensemble— está medido en el **hallazgo 9**: ninguno de los dos se sostiene gracias a la fuga.

---

## Hallazgo 3 — El oro está bajo el umbral de fiabilidad aceptable (severo)

La re-lectura ciega de 40 etiquetas da **κ = 0,582** (IC95 0,257–0,833), acuerdo 0,825.

El estándar citado en análisis de contenido es **α/κ ≥ 0,80 aceptable; 0,667–0,800 sólo para conclusiones tentativas; < 0,667 no fiable**. **0,582 cae bajo el umbral de tentativas.**

Y la advertencia que importa: esos coeficientes miden **reproducibilidad, no exactitud** — codificadores entrenados juntos pueden converger en una lectura equivocada y el coeficiente lo reportará como alta fiabilidad. Con una sola revisora no hay ni siquiera reproducibilidad entre jueces: el 0,582 es test-retest de la misma persona, con posible memoria parcial, así que es un techo optimista.

**Contexto externo:** Shapiro, Sudhof & Wilson (SF Fed) usaron **800 artículos** valorados por **un equipo** de asistentes con instrucciones explícitas; su mejor modelo alcanza correlación de rango ≈**0,5** con las notas humanas. Mi 0,758 es más alto, pero sobre 500 textos y un solo juez: no son comparables y el mío no es más confiable por ser más alto.

---

## Hallazgo 4 — Faltaba la validación de constructo, y los datos la permitían (subsanado)

En esta literatura el índice se valida contra **decisiones de tasa reales**, no sólo contra otra lectura humana. Eso no se había hecho. El corpus contiene el Acuerdo formal de cada reunión, así que se extrajo:

- **104 de 132** sesiones con decisión extraída; **0 incoherencias** verbo/nivel en 92 transiciones consecutivas.
- Extracción tolerante a dos defectos de OCR del corpus: espacios dentro de la palabra (`T a s a`, `T asa`) y niveles sin decimales (`hasta 3% anual`).

Tono medio del Consejo contra la decisión, en tres versiones de menor a mayor limpieza:

| Versión | n | Spearman | ALZA | SIN CAMBIO | RECORTE |
|---|---|---|---|---|---|
| Contemporánea (con anuncio) | 104 | +0,788 | +0,452 | −0,080 | −0,365 |
| Contemporánea (sin anuncio) | 104 | +0,705 | +0,321 | −0,065 | −0,289 |
| **Tono en t → decisión en t+1** | 104 | **+0,615** | +0,268 | −0,021 | −0,259 |

La primera está contaminada: el acta contiene el anuncio de la decisión, así que parte de la asociación es leer el anuncio. Excluyendo esos turnos cae a 0,705. La única prueba sin fuga posible es la tercera —tono de la reunión *t* contra la decisión de la *t+1*— y da **+0,615** con el orden correcto.

**Esto es lo más fuerte de toda la entrega y no estaba.** El puntaje tiene contenido económico real: no es sólo una lectura autoconsistente.

---

## Hallazgo 5 — El modelo está lejos del estado del arte en esta tarea (esperable, no documentado)

El clasificador es regresión logística en Python puro sobre unigramas y bigramas. Lo comparable en la literatura:

- **Ornithologist** (RBA, 2025): sistema débilmente supervisado que guía un LLM con **árboles de decisión escritos a mano sobre una taxonomía de 66 temas**, generación restringida por gramática, validación manual + validez convergente contra el Hawk-Dove Score de JP Morgan + poder informativo sobre la trayectoria futura de la tasa.
- Un esquema de puntaje delta-consistente reporta **71,1% de accuracy** en clasificación hawk-dove a nivel de oración — mi 0,780 por turno está en el mismo orden, pero sobre una unidad más gruesa y sin validación externa.

La diferencia de fondo no es el algoritmo: es que **Ornithologist codifica el razonamiento económico en reglas inspeccionables**, mientras que aquí el criterio vive implícito en 500 etiquetas de un solo juez. Con las dependencias disponibles en el repo no se puede replicar ese enfoque, y no se intentó.

---

## Hallazgo 6 — El remedio obvio contra la deriva se probó y no funciona

El hallazgo 1 deja una pregunta práctica: si el problema es que el pasado lejano enseña otra cosa, ¿no basta con quedarse con lo reciente? Es el remedio estándar para *concept drift*, así que se probó en vez de suponerlo.

`scripts/probar_deriva_temporal_hawkish_dovish.py` compara la ventana **expansiva** (todo el pasado anterior al año de prueba) contra **ventanas deslizantes** de 3, 4 y 5 años, con la misma configuración publicada y los mismos 8 cortes:

| Estrategia | macro-F1 | sd | n entrena medio | diff vs expansiva | gana en |
|---|---|---|---|---|---|
| **Expansiva (base)** | **0,456** | 0,105 | 282 | — | — |
| Deslizante 5 años | 0,413 | 0,113 | 207 | −0,043 | 1/8 |
| Deslizante 4 años | 0,385 | 0,129 | 175 | −0,071 | 1/8 |
| Deslizante 3 años | 0,385 | 0,113 | 138 | −0,071 | 1/8 |

**Refutada, y de forma consistente**: las tres pierden, cada una gana en 1 de 8 cortes, y cuanto más corta la ventana peor. El mecanismo no es que lo reciente sea menos relevante: es que **con 500 etiquetas en total, descartar años cuesta más en tamaño de muestra de lo que gana en pertinencia temporal**. El conjunto de entrenamiento cae de 282 a 138 casos.

Lo que esto sí implica: el cuello del rendimiento hacia adelante es el **tamaño del oro**, no la estrategia de ponderación. Etiquetar más —sobre todo de las épocas extremas (2008-2009 y 2013-2015, donde dovish se dispara)— vale más que cualquier ajuste sobre las 500 actuales.

**Alcance:** esto no prueba que ponderar por recencia no sirva en general; prueba que no sirve *con este tamaño de oro*. Con 2.000-3.000 etiquetas la conclusión podría invertirse, y el script queda para volver a correrlo. **No se publica ningún cambio al release.**

---

## Hallazgo 7 — Ninguna columna publicada sirve para ordenar por certeza

La prioridad nº6 pedía exponer la incertidumbre por turno. Al medirla apareció algo más útil: **las dos medidas de confianza que el release ya publicaba estaban mal calibradas**, y la que funciona no se publicaba. Ya está publicada.

`scripts/medir_calibracion_hawkish_dovish.py` recomputa las predicciones fuera de pliegue sobre las 500 (misma configuración y partición del release) y compara tres candidatas:

| Candidata | ¿Monótona? | ECE | Veredicto |
|---|---|---|---|
| **max-prob** (p de la clase predicha) | **sí** | **0,041** | usable |
| `Margen` (p₁ − p₂) — publicada | no | 0,091 | no usable |
| `\|HD_Score_Modelo\|` — publicada | no | — | no usable |

Curva de fiabilidad de max-prob, que es la única que se comporta:

| Cubo de confianza | n | Confianza | Precisión real | Gap |
|---|---|---|---|---|
| [0,30 · 0,50) | 22 | 0,462 | 0,500 | +0,038 |
| [0,50 · 0,60) | 68 | 0,549 | 0,588 | +0,039 |
| [0,60 · 0,70) | 74 | 0,655 | 0,703 | +0,048 |
| [0,70 · 0,80) | 70 | 0,746 | 0,786 | +0,040 |
| [0,80 · 0,90) | 100 | 0,852 | 0,810 | −0,042 |
| [0,90 · 1,01) | 166 | 0,949 | 0,910 | −0,039 |

La precisión sube de **0,500 a 0,910** sin invertir el orden en ningún tramo, y el error de calibración es 0,041: el modelo sub-confía un poco en los cubos bajos y sobre-confía un poco en los altos, ambos bajo 5 puntos.

`Margen`, en cambio, promete 0,402 en su cubo más bajo y entrega 0,691 —un gap de **+0,288**— y además rompe la monotonía. `|HD_Score|` reproduce exactamente el patrón no monótono que el informe ya había documentado (0,836 · 0,678 · 0,625 · 0,797): los textos con puntaje intermedio son los menos fiables, no los más.

**Consecuencia práctica:** quien quiera quedarse sólo con las predicciones más seguras debe ordenar por `HD_Confianza_Modelo` —la columna nueva— y no por `Margen` ni por `|HD_Score|`. Con max-prob ≥ 0,90 se obtiene precisión 0,910 sobre 166 de las 500.

**Alcance:** la calibración se estima sobre las 500 **fuera de pliegue**. Para las otras 8.757 filas del corpus la confianza del modelo es dentro de muestra respecto del oro que lo entrenó, así que la curva no se les aplica sin más; y para las propias 500 el autoajuste da 0,988, o sea que su confianza dentro de muestra está inflada. Con 6 cubos sobre 500 casos el ECE es sensible al corte; la monotonía es la evidencia más robusta de las dos.

---

## Hallazgo 8 — La validez convergente externa no es realizable, y la brecha que sí se pudo medir no muerde

La prioridad nº4 pedía contrastar el puntaje contra una fuente externa. **No se pudo cerrar**, y conviene separar las dos razones porque son de distinta naturaleza:

- **Por datos:** no hay ninguna serie de mercado en el repo (tasas, spreads, expectativas). La vía que usa Ornithologist contra el Hawk-Dove Score de JP Morgan está cerrada por falta de insumo, no por falta de método.
- **Por idioma:** los léxicos hawk/dove publicados son **ingleses** —Apel & Grimaldi (2014), Bennani & Neuenkirch (2017), Loughran & McDonald (2011)— y este corpus es **español**. Traducirlos habría convertido la referencia externa en traducción propia, que es exactamente la circularidad que se quería romper: el léxico propio y las 500 etiquetas oro ya son del mismo autor.

Lo que sí admite medición sin traducir criterio alguno es la **cobertura de dominios**. Apel & Grimaldi puntúan sobre 11 sustantivos temáticos, y la correspondencia sustantivo→español no es discutible (`inflation`→inflación, `unemployment`→desempleo).

`scripts/contrastar_lexico_publicado_hawkish_dovish.py` mide eso sobre el universo de 2.789 turnos:

| Dominio publicado | ¿En el léxico propio? | Turnos que lo mencionan | % del universo | % de esos sin señal |
|---|---|---|---|---|
| inflation | sí | 1.797 | 64,4% | 25,8% |
| price | sí | 1.660 | 59,5% | 31,2% |
| **wage** | **no** | 661 | 23,7% | **17,8%** |
| **oil price** | **no** | 987 | 35,4% | **29,1%** |
| cyclical position | sí | 880 | 31,6% | 17,8% |
| growth | sí | 2.273 | 81,5% | 34,4% |
| **development** | **no** | 1.270 | 45,5% | **29,4%** |
| employment | sí | 1.342 | 48,1% | 24,8% |
| unemployment | sí | 450 | 16,1% | 18,7% |
| **recovery** | **no** | 859 | 30,8% | **29,1%** |
| cost | sí | 568 | 20,4% | 17,6% |

**7 de 11 cubiertos.** Los cuatro ausentes son frecuentes —entre 23,7% y 45,5% de los turnos—, así que la brecha no es trivial sobre el papel.

**Pero no produce un punto ciego.** En el universo completo, **41,8%** de los turnos (1.166 de 2.789) no recibe ninguna señal léxica. Entre los turnos que mencionan los dominios ausentes, la fracción sin señal va de **17,8% a 29,4%**: los cuatro están **por debajo** del promedio. La señal direccional les llega por otro dominio —"han evolucionado por debajo de lo previsto" habla de inflación, que el léxico sí cubre—.

**Consecuencia:** la brecha de cobertura es real pero su impacto no es aislable con este método, y no se traduce en una deficiencia medible. **No se modificó el léxico**: agregar términos sin evidencia de que falten sería empeorar un artefacto publicado por una razón estética.

**Alcance:** la equivalencia de los 11 dominios al español la hizo este agente (es de vocabulario, no de criterio, pero sigue siendo una decisión); que un turno mencione el término no implica que ese dominio cargue la postura; y aislar el efecto de cada dominio exigiría re-etiquetar, que es la prioridad nº1 y sigue abierta.

---

## Hallazgo 9 — La fuga por sesión no sostiene ningún veredicto publicado, pero casi

El hallazgo 2 tiene una consecuencia que conviene explicitar: si la CV por turno filtra entre sesiones, **todo veredicto publicado que descanse en esa CV queda bajo sospecha**. Son dos: la selección de configuración y el descarte del ensemble.

**Selección de configuración: no cambia.** Sobre las cinco mejores de la rejilla y 5 semillas, la regla elige **600/30/bal con ambas particiones**. Las diferencias por configuración van de −0,009 a −0,031 y **no alteran el ranking de las tres primeras**. Por eso `sha256_modelo` no se mueve al publicar la CV por sesión.

**Descarte del ensemble: sobrevive, pero sólo con el comparador correcto.** `scripts/probar_ensemble_por_sesion_hawkish_dovish.py` repite la CV anidada cambiando **solo** la partición, en los dos niveles (el externo y el interno que elige `w`):

| | por turno (publicado) | por sesión | ¿cambia de signo? |
|---|---|---|---|
| **mezcla − umbral** (técnico) | −0,0040 | **+0,0030** | **sí** |
| **mezcla − argmax** (decisorio) | −0,0282 | **−0,0332** | no |

El comparador técnico **cambia de signo**, así que leído a la ligera el veredicto parecería invertirse. No es así, por dos razones:

1. **Es ruido.** La sd de la diferencia es 0,011 por turno y 0,008 por sesión; ambos valores están dentro de una desviación de cero.
2. **No es el comparador que decide.** La mezcla decide con `hd.clase()`, así que emparejarla con el umbral es lo metodológicamente limpio, pero la pregunta práctica es si conviene mezclar **frente a lo que el release publica**, y lo que publica es argmax. Contra argmax la mezcla pierde por 0,028 y por 0,033 — y la brecha **se agranda** al agrupar por sesión.

**Veredicto: se mantiene** ("la mezcla no mejora al modelo; no se publica"), y se refuerza. Pero el episodio es la razón por la que el artefacto publica los dos comparadores por separado: un veredicto que depende de cuál de los dos se mire no está bien establecido, y conviene que el lector lo vea.

**Alcance:** 5 semillas, como el harness publicado. La partición por sesión no es estratificada por clase, así que los pliegues quedan más desbalanceados (97/97/83/118/105) que los de la CV publicada; eso agrega varianza a ambas columnas por igual, no sólo a una.

---

## Hallazgo 10 — El diseño estratificado no infla el rendimiento publicado

Las 500 etiquetas no se sortearon al azar simple: `muestra()` las estratifica por **decil léxico × año × grupo de actor** y reparte cupos con `PESOS_DECIL`, que da peso 3,0 a los deciles extremos y 1,0 a los centrales. El docstring de la función ya lo advierte: *"las etiquetas sirven para entrenar un clasificador, no para estimar la prevalencia"*.

Esa advertencia se atendió a medias. La **prevalencia** sí se reponderó (`prevalencia_reponderada.json`, ESS 435,3). El **rendimiento**, no: el macro-F1 0,702 se calculó sobre la muestra tal cual, como si fuera aleatoria simple.

`scripts/reponderar_rendimiento_por_decil_hawkish_dovish.py` lo mide con pesos de diseño `w_h = (N_h/N)/(n_h/n)` y macro-F1 de precisión y recall ponderadas:

| | sin ponderar (publicado) | reponderado al universo |
|---|---|---|
| **macro-F1** | 0,7023 | **0,7078** |
| **accuracy** | 0,7800 | **0,8045** |
| F1 HAWKISH | 0,7324 | 0,7294 |
| F1 NEUTRAL | 0,8501 | 0,8736 |
| F1 DOVISH | 0,5244 | 0,5203 |

**La diferencia es +0,0058: existe, pero es chica y va en la dirección contraria a la que se temería.** El diseño no infla el 0,702; si acaso lo subestima ligeramente.

La razón es visible en la tabla por decil: la exactitud va de **0,677 en el decil 2** a **0,969 en el decil 7**, y el diseño **sobremuestrea los extremos** (peso 0,60 y 0,61 en D1 y D10) **y subremuestrea el centro** (peso 1,67 y 1,56 en D6 y D7). O sea: la muestra publicada está cargada hacia los turnos difíciles, que es donde el modelo falla. Reponderar hacia el universo le devuelve peso a los casos fáciles y la cifra sube.

**Consecuencia práctica:** el 0,702 publicado es defendible como cifra del universo, no sólo de la muestra. Pero es conservador: un lector que quiera la mejor estimación del rendimiento sobre el corpus debería citar **0,708**, no 0,702.

**Controles internos del script:** el decil recalculado desde el universo coincide con el declarado en `muestra_500_hawkish_dovish.csv` para las 500, y el acierto recalculado comparando oro y predicción coincide con la columna `Acierta` del CSV de fallos. La accuracy recalculada reproduce exactamente la publicada (0,7800).

**Alcance:** esto repondera el **error de muestreo del diseño**, no el resto. No corrige la fuga por sesión (H2), ni la falta de generalización temporal (H3), ni el ruido del oro (H1). Es una corrección adicional, no sustitutiva.

---

## Lo que la auditoría NO encontró roto

Para que conste qué sobrevive:

- La **extracción de decisiones** es internamente coherente (0 incoherencias en 92 transiciones).
- La **validez de constructo** es robusta a eliminar la contaminación por anuncio (0,788 → 0,705 → 0,615, siempre con el orden correcto).
- El **modelo sigue ganándole al léxico en todos los cortes temporales** (p. ej. corte 2013: 0,671 contra 0,493 del léxico). La conclusión comparativa aguanta; el nivel absoluto no.
- La **fuga por sesión** es chica (−0,012) y no invalida el ranking de configuraciones.
- La **prevalencia reponderada** no depende de ninguno de estos hallazgos: post-estratifica por decil sobre el oro, y el oro es el que es.

---

## Prioridades para cerrar

1. **Segunda revisora independiente** sobre una submuestra ≥100, con adjudicación de desacuerdos y α de Krippendorff reportado. Es lo único que convierte el 0,582 en una medida de fiabilidad y no de memoria. Sin esto, el oro no pasa el umbral de conclusiones tentativas.
2. **Reportar siempre el número temporal junto al aleatorio.** El 0,685 sólo aplica a interpolar en el período; para proyectar hacia adelante es ~0,46.
3. ~~**Re-etiquetar leyendo el texto completo**, no la ventana 520+280.~~ **HECHO** en esta misma auditoría sobre las 40 de la re-lectura ciega (`efecto_ventana.json`). Resultado contra lo esperado: el efecto directo es chico —acuerdo **0,925**, κ **0,806** entre la pasada completa y la pasada por ventana, sólo 3 cambios de clase en 40— y contra el oro la lectura completa acuerda *más*, no menos (0,850 vs 0,825). Lo que sí aparece es el mecanismo: la ventana **omite votos explícitos** que caen en el medio del discurso (`RPM-2010-06-15:T85`, voto de +50 pb registrado como NEUTRAL; `RPM-2013-10-17:T35`, recomendación de recortar 25 pb). Re-etiquetar las 500 completas sigue valiendo la pena, pero por esos casos puntuales, no por un sesgo sistemático de la ventana. El efecto *indirecto* sobre el modelo continúa sin medirse.
4. **Validación convergente externa**: contrastar contra una medida de mercado o contra el léxico publicado en la literatura, como hace Ornithologist con el Hawk-Dove Score de JP Morgan. **MEDIDO Y NO CERRABLE** (`contraste_lexico_publicado.json`, Hallazgo 8). El contraste pleno exige una serie de mercado que el repo no tiene, o traducir un léxico inglés, que reintroduciría la circularidad que se intenta romper. Lo medible —cobertura de los 11 dominios temáticos de Apel & Grimaldi— da **7/11**, y los cuatro ausentes **no producen punto ciego**: 17,8%-29,4% de sus turnos sin señal contra **41,8%** del universo. Cerrarla de verdad requiere la prioridad nº1.
5. **CV agrupada por sesión como predeterminada**, no la aleatoria por turno. **PARCIAL**: la cifra limpia ya se **publica en el release** como `validacion_cruzada_por_sesion` (macro-F1 **0,682**, acc 0,768, MAE 0,243) junto a la aleatoria por turno, que queda sin cambios. **No se hizo predeterminada** porque eso reescribiría los titulares de un release versionado y hasheado —sería publicar un v2, no parchear v1—. Lo que sí se verificó es que el cambio no mueve el modelo: la regla de selección elige **600/30/bal con ambas particiones** sobre las cinco mejores de la rejilla, así que `sha256_modelo` no cambia y los baselines son idénticos. La diferencia por configuración (5 semillas) va de −0,009 a −0,031 y **no altera el ranking de las tres primeras**. Convertirla en predeterminada queda para v2.
6. ~~**Incertidumbre publicada por turno**~~ **MEDIDO** en esta auditoría (`calibracion_confianza.json`), y el resultado cambia la recomendación: `Margen` y `|HD_Score|` **no** sirven como confianza (ECE 0,091 y no monótona la primera; no monótona la segunda). La que sirve es max-prob (ECE 0,041, precisión monótona de 0,500 a 0,910). **CERRADO**: se publicó como columna `HD_Confianza_Modelo` en `puntajes_hawkish_dovish.csv` (17 columnas), regenerando el release con `--diagnostico` y verificando que el modelo, el resumen y el diagnóstico salen con el mismo sha256 y que ninguna celda preexistente cambia.
7. ~~**Reponderar el rendimiento al diseño de muestreo**~~ **MEDIDO** en esta auditoría (`rendimiento_reponderado.json`, Hallazgo 10). La advertencia del docstring de `muestra()` se había atendido a medias: la prevalencia sí se reponderó, el rendimiento no. Al hacerlo con pesos de diseño `w_h = (N_h/N)/(n_h/n)` el macro-F1 pasa de 0,7023 a **0,7078** y la accuracy de 0,780 a 0,8045. **CERRADO con resultado negativo útil**: el diseño estratificado **no infla** la cifra publicada, la **subestima** en +0,0058, porque sobremuestrea los deciles difíciles (exactitud 0,677 en D2 frente a 0,969 en D7). No requiere rehacer nada; para v2 conviene publicar la cifra reponderada junto a la sin ponderar.

---

## Reproducir

```bash
python3 scripts/auditar_hawkish_dovish.py            # ~60 s, 10 semillas de CV
python3 scripts/probar_deriva_temporal_hawkish_dovish.py   # ~12 s
python3 scripts/medir_calibracion_hawkish_dovish.py         # ~5 s
python3 scripts/contrastar_lexico_publicado_hawkish_dovish.py  # ~5 s
python3 scripts/probar_ensemble_por_sesion_hawkish_dovish.py   # ~70 s
python3 scripts/reponderar_rendimiento_por_decil_hawkish_dovish.py  # ~4 s
python3 scripts/auditar_hawkish_dovish.py --rapido   # 3 semillas
python -m unittest tests.test_hawkish_dovish -v
```

Cada cifra de este documento sale de `auditoria_metodologica.json`. Las 11 pruebas de `AuditoriaMetodologicaTests` hacen tres cosas distintas, y conviene no exagerarlas: **recalculan desde las entradas** la extracción de decisiones (sobre el corpus, no sobre el artefacto), el Spearman de validez de constructo (desde el CSV de puntajes más las decisiones) y el invariante de la partición por sesión; **assertan invariantes** sobre el artefacto para el resto (que agrupar por sesión baje el número, que el rolling-origin caiga bajo el publicado, que el orden ALZA > SIN CAMBIO > RECORTE se mantenga en las tres versiones, que κ quede bajo 0,667); y **verifican que el informe y el README** adviertan sobre el número temporal. La CV de 10 semillas y el rolling-origin no se recomputan en las pruebas porque tardan ~60 s; se reproducen con el script.
