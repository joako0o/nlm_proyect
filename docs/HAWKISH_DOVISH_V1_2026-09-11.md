# Hawkish/dovish v1 — 500 etiquetas oro, modelo entrenado y puntaje del corpus

**11 de septiembre de 2026 · Nueva capa de análisis sobre la entrega procedimental v5, sin tocar los datos**

## Resultado

Se cumplió el objetivo planteado: **las 500 intervenciones de la muestra sorteada están leídas y puntuadas a mano**, y con ellas se entrenó el clasificador que puntúa los **9.257 turnos** del corpus. Cero etiquetas pendientes, cero errores de validación.

**El modelo supera al baseline léxico en las tres clases.** Validación cruzada de 5 pliegues: macro-F1 **0,702** contra **0,550** del léxico y **0,271** de la clase mayoritaria; F1 por clase **0,732 HAWKISH / 0,850 NEUTRAL / 0,524 DOVISH**, contra **0,496 / 0,746 / 0,406** del léxico. Accuracy **0,780** contra 0,646 del léxico y 0,686 de responder siempre NEUTRAL. Sobre el puntaje continuo, MAE **0,239** contra 0,296 del léxico. En hawkish acierta **52 de 71**; en dovish, **43 de 86**.

Con **CV repetida** (10 semillas de partición) el macro-F1 del modelo publicado promedia **0,685** con desviación 0,015, y le gana al léxico en **10 de 10** semillas. Esa es la cifra robusta; el 0,702 es una partición favorable.

Los datos no cambiaron: **la entrega sigue siendo [procedimental v5](../data/releases/continuidad_procedimental_v5/)**, 9.694 filas / 9.236 grupos. Esta capa sólo lee el consolidado y publica una tabla nueva.

- [Muestra de 500](../data/curation/muestra_500_hawkish_dovish.csv) y [resumen del sorteo](../data/curation/muestra_500_hawkish_dovish_resumen.json).
- [500 etiquetas oro con evidencia](../data/curation/hawkish_dovish_etiquetas_v1.json) y [validación](../data/curation/hawkish_dovish_etiquetas_resumen.json).
- [Puntaje de los 9.257 turnos](../data/releases/hawkish_dovish_v1/puntajes_hawkish_dovish.csv), [modelo](../data/releases/hawkish_dovish_v1/modelo_hawkish_dovish.json), [métricas](../data/releases/hawkish_dovish_v1/resumen_entrenamiento.json) y [diagnóstico de capacidad](../data/releases/hawkish_dovish_v1/diagnostico_capacidad.json).

## Universo y muestra

El corpus tiene **132 sesiones entre 2005-01-11 y 2015-12-17**, **9.257 turnos** y **2.048.560 palabras**. El universo etiquetable son las intervenciones sustantivas: `Naturaleza_Turno = INTERVENCION` con **≥150 palabras**, **2.789 turnos** (1.100 Consejo, 1.540 staff, 149 Hacienda). Quedan fuera **6.468 turnos**: 561 institucionales, 12 escritos leídos por tercero, 3 documentos personales y **5.892 intervenciones breves** (menos de 150 palabras).

El sorteo (semilla **20260911**) reparte 500 cupos por decil de puntaje léxico con más peso en los extremos: objetivo **85/63/43/31/28/28/31/43/63/85**, realizado **83/62/35/38/31/30/32/50/57/82** (el reparto por año × grupo de actor dentro de cada decil no siempre alcanza el cupo). No es proporcional a la población, así que sirve para entrenar un clasificador pero **no para estimar la prevalencia** de cada postura sin reponderar por decil.

## Las 500 etiquetas

Se leyeron con ventana fija de **520 caracteres iniciales + 280 finales** (texto completo si es menor). Cobertura media de lectura: **0,348**. El puntaje va de −1 a +1 y la clase se deriva del puntaje, no al revés.

Distribución oro: **71 HAWKISH / 343 NEUTRAL / 86 DOVISH**, puntaje medio **−0,033**. Ocho tranches (63, 63, 63, 63, 62, 62, 62 y 62): la primera cada 8ª del sorteo original, después cada 7ª, 6ª, 5ª, 4ª, 3ª y 2ª de las pendientes, y la última con las 62 restantes, todas en orden cronológico 2005-2015.

El léxico, medido contra el oro, coincide en clase **64,6%** de las veces (MAE 0,296). Esa es la razón para entrenar y no para usar el léxico como etiqueta: **falla en más de un tercio de las intervenciones**.

Cada etiqueta se valida antes de aceptarse: `ID_Turno` existe, SHA256 del texto coincide, la clase es coherente con el puntaje y **la evidencia citada aparece literalmente en el acta**. El validador rechazó tres citas en todo el proceso: «se incorpore» en vez de «se incorpora» (tranche 1), «el escenario» en vez de «dicho escenario» (tranche 4) y «es importante» cortado a mitad de palabra (tranche 6). Las tres se corrigieron; las 500 quedaron validadas con **0 errores** y las tranches 2, 3, 5, 7 y 8 entraron limpias.

Se verificó además que no haya duplicados que contaminen la validación cruzada: **0 SHA256 de texto repetidos dentro de la muestra**, y ninguno de los 595 turnos del corpus que comparten SHA256 (141 textos distintos) cayó en ella. El consolidado sí marca 633 filas (630 `ID_Turno` distintos) como `Duplicado_Exacto = SI`; **3 de esos turnos están en la muestra** (`RPM-2007-11-13:T2`, `RPM-2009-09-08:T61`, `RPM-2014-09-11:T44`), en los tres casos por el bloque institucional de apertura que se repite entre actas, no por el contenido analizado.

## Modelo

Regresión logística multinomial en Python puro, sin dependencias nuevas (`requirements.txt` sigue en openpyxl + pypdf). Rasgos: unigramas y bigramas sobre texto normalizado, sin tildes, con stopwords del corpus; peso TF-IDF sublineal y normalización L2. La selección supervisada de rasgos se hace **dentro de cada pliegue**.

**Configuración publicada: 600 rasgos / 30 iteraciones / ponderación de clases por inverso de frecuencia.** La regla de selección está escrita en el código y no se aplica a mano: entre las tres mejores de la rejilla por macro-F1, se descarta la que no supere al léxico en el último punto de la curva y, entre las restantes, se toma la de mayor macro-F1 medio en **CV repetida sobre el conjunto completo** (10 semillas de partición).

### La regla de selección estaba mal y se corrigió

Hasta esta entrega el desempate usaba el macro-F1 medio de la **curva de aprendizaje**, que se mide con subconjuntos de 15-80% del oro. Eso optimizaba un régimen distinto al de uso: el modelo se despliega entrenado con las 500 completas. Con 500 etiquetas el criterio elegía 300 rasgos y publicaba macro-F1 0,662, renunciando a 0,040 frente a 600 rasgos.

Se midió si esa renuncia compraba algo. **CV repetida con 10 semillas de partición:**

| configuración | macro-F1 medio | sd | gana al léxico |
|---|---|---|---|
| **600/30 bal (publicada)** | **0,685** | 0,015 | 10/10 |
| 600/30 sin bal | 0,649 | 0,018 | 10/10 |
| 300/30 bal (publicada antes) | 0,648 | 0,009 | 10/10 |

600/30 balanceado gana en **10 de 10** semillas, con diferencia media **+0,037** y sd 0,018. No era ruido: el criterio viejo elegía sistemáticamente peor. Se cambió el desempate a CV repetida sobre el conjunto completo y la curva quedó como diagnóstico del cruce con el léxico, no como criterio. El defecto está cubierto por `test_diagnostico_desempata_por_cv_repetida_no_por_curva` y `test_release_publica_lo_que_elige_la_regla`.

Rejilla (macro-F1, top 5): **600/30 bal 0,702 (publicada)**; 600/30 sin bal 0,687; 300/30 bal 0,662; 300/120 sin bal 0,659; 900/200 sin bal 0,655.

### Curva de aprendizaje: el modelo gana desde ~175 etiquetas

| etiquetas | macro-F1 modelo | macro-F1 léxico | accuracy modelo |
|---|---|---|---|
| 75 | 0,504 | **0,517** | 0,720 |
| 125 | 0,524 | **0,528** | 0,704 |
| 175 | **0,592** | 0,513 | 0,749 |
| 250 | **0,579** | 0,540 | 0,728 |
| 325 | **0,613** | 0,532 | 0,726 |
| 400 | **0,661** | 0,535 | 0,760 |

Con 75 y 125 etiquetas gana el léxico; **de 175 en adelante gana el modelo en todos los puntos** con ventaja creciente. Como regla operativa: bajo ~150 etiquetas no vale la pena entrenar; sobre ~175, sí. Los puntos escalan con el tamaño del oro (15% a 80%).

Matriz de confusión del modelo publicado (filas = oro): HAWKISH **52** correctos / 15 a NEUTRAL / 4 a DOVISH; NEUTRAL 17 / **295** / 31; DOVISH 2 / 41 / **43**. El error casi nunca invierte el signo (6 casos de 500 entre hawkish y dovish): lo que hace el modelo es dudar hacia NEUTRAL.

El autoajuste sobre las 500 da accuracy **0,988**. Es sobreajuste, se publica como tal y no se usa como métrica.

## Evolución a lo largo de las ocho tranches

| etiquetas | config publicada | macro-F1 modelo | macro-F1 léxico | F1 dovish |
|---|---|---|---|---|
| 126 | 150/30 bal | 0,533 | 0,449 | 0,491 |
| 189 | 300/30 bal | 0,586 | 0,474 | 0,464 |
| 252 | 600/30 bal | 0,608 | 0,506 | 0,420 |
| 314 | 300/30 bal | 0,625 | 0,498 | 0,440 |
| 376 | 600/30 bal | 0,663 | 0,516 | 0,455 |
| 438 | 600/30 bal | 0,634 | 0,535 | 0,444 |
| 500 | 600/30 bal | **0,702** | 0,550 | **0,524** |

Las siete filas están **recomputadas hoy** con el código y el léxico actuales, sobre los primeros *n* etiquetas del JSON oro y la configuración que se publicó en cada etapa; así son comparables entre sí. No son las cifras que se imprimieron en su momento: el léxico se corrigió en el camino (saturaba en ±1), y con el léxico viejo las etapas de 126 y 189 daban 0,548 y 0,516. **Las filas de 126 a 438 reflejan la regla de selección vieja** (desempate por media de la curva); la de 500 ya usa la corregida. La etapa de 63 etiquetas no figura porque la configuración que publicó esa corrida no es recuperable de los artefactos actuales.

**No es una subida monótona.** De 376 a 438 el macro-F1 bajó de 0,663 a 0,634 mientras el léxico subía. Dos razones: la validación cruzada se recalcula sobre un conjunto distinto cada vez (no son las 376 anteriores más 62), y con este tamaño **±0,03 en macro-F1 está dentro del ruido**. Lo que sí se sostiene en las siete etapas es el signo: **con el léxico actual el modelo le gana en las siete**, desde las 126 etiquetas en adelante.

## Puntaje publicado

Los 9.257 turnos llevan `HD_Score_Modelo` en [−1, +1] (esperanza bajo la softmax), `HD_Clase_Modelo`, `Margen`, `En_Universo_Entrenado` y `En_Muestra_500`. En el universo entrenado: **321 HAWKISH / 410 DOVISH / 2.058 NEUTRAL**. Los 6.468 turnos fuera del universo también llevan puntaje, marcados como tales: es extrapolación.

**`HD_Clase_Modelo` no es el umbral de `HD_Score_Modelo`.** La clase publicada es el
**argmax de la softmax** (la clase más probable), mientras que el puntaje es la esperanza
P(H)−P(D). Las dos reglas discrepan en **531 de 9.257 filas (5,74%)**, siempre en el mismo
sentido: el argmax ve hawkish o dovish pero el puntaje cae dentro de la banda neutra. Aplicar
`|HD_Score_Modelo| >= 0,25` por cuenta propia daría **449 H / 888 D / 7.920 N** en vez de los
**614 H / 1.254 D / 7.389 N** publicados, y rinde menos: en validación anidada el argmax promedia **0,6838** de macro-F1 y el
umbral **0,6596**. Use la columna `HD_Clase_Modelo` tal como viene; el puntaje sirve para
ordenar, no para reclasificar.

**Un caso que antes era sólo consistencia de cara ahora está validado.** En versiones anteriores de este informe se destacaba que el 2014-10-16 el modelo y el léxico discrepaban frontalmente en una intervención de Pablo García, sin etiqueta que dirimiera. Esa intervención (`RPM-2014-10-16:T15`) se etiquetó **DOVISH (−0,50)** leyéndola, y el léxico la marca **+0,43**, es decir hawkish. Ese día el Consejo bajó la TPM de 3,25% a 3,00% (`decisiones_tpm.csv`, −25 pb). El mismo día hay otra intervención suya sin etiquetar (`RPM-2014-10-16:T51`) con la misma discrepancia, pero sin oro que la dirima, así que no cuenta como acierto. Un caso no valida nada por sí solo, pero es el tipo de error que el léxico comete y el modelo no.

### Dónde sigue flojo

El F1 dovish llegó a **0,524**, su mejor marca, pero sigue siendo el punto débil: **41 de los 86 dovish oro se clasifican NEUTRAL**. El recall dovish (0,500) quedó sobre el del léxico (0,465). Para un barrido exhaustivo conviene ordenar por `HD_Score_Modelo` y leer el extremo, no filtrar por `HD_Clase_Modelo`.

**Pero ojo: eso sirve para capturar posturas, no para medir certeza.** Son dos objetivos distintos y las columnas que sirven para cada uno no coinciden (`calibracion_confianza.json`). `|HD_Score_Modelo|` **no** es monótona en precisión —0,836 en [0,00·0,25) · 0,678 · 0,625 · 0,797 en el extremo—: los textos de puntaje intermedio son los menos fiables. `Margen` tampoco: su cubo más bajo promete 0,402 y entrega 0,691 (gap +0,288) y rompe la monotonía, con ECE 0,091.

La única medida bien calibrada es **max-prob**, la probabilidad de la clase predicha: precisión monótona de **0,500 a 0,910** y ECE **0,041**. Con max-prob ≥ 0,90 se obtiene precisión 0,910 sobre 166 de las 500. **Está publicada como columna `HD_Confianza_Modelo`** en el CSV de puntajes, junto a las otras dos para que se pueda comparar. Esa calibración se estima **fuera de pliegue**; para las otras 8.757 filas del corpus la confianza del modelo es dentro de muestra y la curva no se les aplica sin más.

## Defectos corregidos en el camino

1. **`grupo_actor` agrupaba Presidente y Vicepresidente del Banco Central con el staff.** Votan; las gerencias informan. **15 de las 63 primeras etiquetas estaban mal estratificadas.** Se corrigió (también `Asesor del Ministerio de Hacienda`, que caía en STAFF por comparar contra «Ministr») y las etiquetas pasaron a indexarse por `ID_Turno` para sobrevivir a un nuevo sorteo.
2. **El puntaje léxico saturaba en ±1** con un solo acierto y dejaba los deciles degenerados. Se separó dirección de intensidad y el umbral de clase subió a 0,50.
3. **Re-sortear la muestra borraba las etiquetas fusionadas** y el entrenamiento seguía corriendo igual. Ahora `entrenar_hawkish_dovish.py` se niega a arrancar si la muestra no lleva etiquetas fusionadas. El orden es `muestra → etiquetar → entrenar`.
4. **El diagnóstico elegía una configuración y `main()` publicaba otra.** Con 126 etiquetas la regla declaró 300/30 como mejor y el release salió con 150/30, el valor por omisión del CLI. Ahora la rejilla corre antes de entrenar, se publica lo que la regla elige salvo que el usuario fuerce un parámetro por CLI, y el origen de cada parámetro queda registrado.
5. **La curva de aprendizaje tenía los puntos fijos en 24-105 etiquetas.** Con 189 dejaba fuera el tramo final. Ahora escalan con el tamaño del oro.
6. **El desempate de configuración optimizaba el régimen equivocado.** Usaba el macro-F1 medio de la curva (subconjuntos de 15-80% del oro) para elegir un modelo que se entrena con el oro completo. Con 500 etiquetas eso costaba 0,040 de macro-F1 y la CV repetida mostró que la diferencia era real (10/10 semillas). Se cambió a CV repetida sobre el conjunto completo.

## Dónde falla el modelo, caso por caso

`python3 scripts/diagnosticar_fallos_hawkish_dovish.py` reproduce la misma validación cruzada
del release y escribe `fallos_fuera_de_pliegue.csv` (las 500 etiquetas con su predicción fuera
de pliegue). De ahí salen tres cosas que la matriz sola no muestra.

**Precisión por clase predicha, fuera de pliegue** (no confundir con la tabla anterior, que es
la matriz real×predicha): cuando el modelo dice HAWKISH acierta **52 de 71 (0,732)**; cuando dice
NEUTRAL acierta **295 de 351 (0,840)**; cuando dice DOVISH acierta **43 de 78 (0,551)**. O sea:
un turno marcado DOVISH por el release es el menos fiable de los tres y hay que leerlo.

**La confianza declarada no ordena la precisión.** Dividiendo las 500 por el valor absoluto del
puntaje fuera de pliegue:

| |score| | n | precisión |
|---|---|---|
| [0,00 · 0,25) | 298 | 0,836 |
| [0,25 · 0,50) | 87 | 0,678 |
| [0,50 · 0,75) | 56 | **0,625** |
| [0,75 · 1,01) | 59 | 0,797 |

No es monótona: el tramo intermedio-alto es el peor, y el extremo vuelve a subir. El margen medio
del modelo en sus **errores** es 0,356 y en sus **aciertos** 0,263; la cifra se explica por la
mezcla de clases (casi todos los aciertos son NEUTRAL de margen bajo), pero el mensaje práctico
sigue: **un |score| alto no garantiza acierto**.

**Dónde sí sirve ordenar por score: para barrer.** Hay 157 intervenciones no neutras en el oro
(base 31,4%). Tomando las N más extremas por |score|:

| leer las N más extremas | captura | precisión |
|---|---|---|
| 50 | 42 de 157 (26,8%) | 0,840 |
| 100 | 80 de 157 (51,0%) | 0,800 |
| 150 | 97 de 157 (61,8%) | 0,647 |
| 200 | 112 de 157 (71,3%) | 0,560 |

Con 100 lecturas se encuentra la mitad de todas las intervenciones con postura, con 8 de cada 10
ciertas, contra 3 de cada 10 si se leyeran 100 al azar. **Ese es el uso correcto del ranking.**
Lo que no se sostiene es leer el |score| como probabilidad: para eso hace falta una calibración
que con 500 casos no se puede estimar con solidez.

**Los errores son de matiz, no de signo.** De las 500, solo **6** invierten el signo (4 hawkish
→ dovish y 2 dovish → hawkish); los 104 restantes son casos que el modelo corrió hacia NEUTRAL o
desde NEUTRAL. El léxico, en cambio, acertaba la clase en **54 de esos 110 errores**: son turnos
donde dos métodos razonables discrepan y un segundo revisor decidiría mejor que cualquiera de los
dos.

## Una asimetría real: el efecto indirecto no se pudo medir, el directo sí

Las 500 etiquetas se tomaron leyendo una **ventana fija de 520 caracteres iniciales + 280
finales** (`LECTURA_CABEZA` / `LECTURA_COLA`, 800 en total, o el texto completo si es menor);
el clasificador entrena con el **texto completo**. El modelo ve, por tanto, información que la
revisora no vio. Eso puede cortar en dos sentidos: el modelo detecta matices del cuerpo que la
etiqueta no recogió, o aprende rasgos que no corresponden a lo que se juzgó.

**Intenté medirlo y no se puede con este diseño.** La idea era comparar el puntaje léxico de la
ventana leída contra el del texto completo y ver si el modelo falla más donde divergen. Aparece
un gradiente llamativo —error fuera de pliegue 13,6% · 20,0% · 24,8% · 29,6% por cuartil de
divergencia— pero es un artefacto: la divergencia correlaciona **0,716** con `|léxico del texto
completo|`, así que los cuartiles están ordenando los textos por cuánta señal léxica tienen, no
por desacuerdo entre lo leído y el resto. Controlando por banda de señal el patrón desaparece y
se da vuelta según la banda:

| |léxico completo| | n | divergencia baja | divergencia alta |
|---|---|---|---|
| [0,00 · 0,15) | 175 | 10,1% | 33,3% |
| [0,15 · 0,35) | 95 | 22,9% | 17,0% |
| [0,35 · 0,65) | 173 | 26,0% | 30,1% |
| [0,65 · 1,01) | 57 | 37,9% | 28,6% |

Sin patrón consistente no hay efecto que reportar. Un corte alternativo tampoco sostiene la
hipótesis: donde lo leído y el resto **coinciden** en dirección el error es 27,2% (n=136) y
donde difieren 20,1% (n=364), otra vez al revés de lo predicho.

Lo que sí queda es que **el oro concuerda más con la ventana leída que con el texto completo**
cuando se mide en clase: **338 de 500 contra 323 de 500**. Es coherente con que la etiqueta se
tomó leyendo esa ventana. En correlación de puntaje continuo sale al revés (0,301 contra 0,511),
pero eso no contradice nada: el léxico de 800 caracteres tiene poca señal propia, así que su
puntaje es ruidoso aunque su clase acierte más. Las dos medidas dicen cosas distintas y ninguna
de las dos mide el efecto de la asimetría.

**La medición directa sí se hizo después** (`efecto_ventana.json`): se re-leyeron las mismas
40 intervenciones de la re-lectura ciega, esta vez **completas** (148.563 caracteres en vez
de 800 por texto). Con tres pasadas sobre los mismos textos se separa lo que antes iba
mezclado:

| Comparación | Acuerdo | κ | MAE | IC95 del acuerdo |
|---|---|---|---|---|
| Ventana vs oro (test-retest) | 0,825 | 0,582 | 0,163 | 0,707 – 0,943 |
| Completo vs oro | **0,850** | 0,651 | 0,181 | 0,739 – 0,961 |
| Completo vs ventana (**efecto puro**) | **0,925** | 0,806 | 0,081 | 0,843 – 1,007 |

El resultado va contra lo que la sección anticipaba: **la ventana cuesta poco**. Leer el texto
completo cambia la clase en sólo **3 de 40** casos respecto de la propia pasada por ventana
(κ 0,806), y contra el oro la lectura completa acuerda *más*, no menos (0,850 contra 0,825).
Ninguna de las tres comparaciones invierte un signo.

Pero no es cero, y el mecanismo importa: en `RPM-2010-06-15:T85` el oro dice NEUTRAL +0,25 y la
lectura completa dice HAWKISH +1,00, porque el consejero vota **+50 puntos base** en el cuerpo
del texto —"es partidario de un aumento de la TPM de 50 puntos base, dado que el nivel
extremadamente expansivo de la política monetaria es, actualmente, difícil de justificar"— y esa
frase cae justo en el hueco entre la cabeza y la cola. En `RPM-2013-10-17:T35` pasa lo mismo con
la recomendación de recortar 25 pb. La ventana no distorsiona el tono promedio: **omite votos
explícitos cuando quedan en el medio del discurso**.

Con n=40 los tres intervalos se solapan, así que ninguna diferencia entre ellos es significativa
por sí sola; y las dos últimas pasadas las hizo la misma revisora en la misma sesión, lo que
subestima el efecto si hubo memoria de la pasada anterior.

*Nota de corrección: una versión anterior de esta sección comparaba contra los primeros 800
caracteres en vez de la ventana real 520+280, y concluía que el oro se apoyaba más en el texto
completo. Con la ventana correcta esa conclusión se invierte. Las cifras de arriba son las de la
ventana real.*

## Prevalencia en el universo, reponderada

La muestra no es proporcional: los deciles de puntaje léxico se repartieron casi parejo
para cubrir todo el espectro, así que **el conteo crudo de las 500 no es la prevalencia del
corpus**. Con post-estratificación por decil sí se puede estimar: cada etiqueta vale
`N_d/n_d` (279 intervenciones del decil en el universo sobre las 30-83 que cayeron en la
muestra), y los pesos suman exactamente 2.789.

`python3 scripts/estimar_prevalencia_hawkish_dovish.py` → `prevalencia_reponderada.json`.

| clase | crudo en las 500 | reponderado al universo | IC95 | intervenciones |
|---|---|---|---|---|
| HAWKISH | 14,2% | **10,8%** | 8,8-12,8 | ~301 |
| NEUTRAL | 68,6% | **73,5%** | 70,1-76,9 | ~2.051 |
| DOVISH | 17,2% | **15,7%** | 12,8-18,6 | ~438 |

El sorteo sobre-representó los extremos, como estaba diseñado: ponderar baja el hawkish
**3,4 puntos** y el dovish 1,5, y sube el neutral 4,9. El costo en precisión es chico —tamaño
efectivo de muestra **435 de 500**, efecto de diseño 1,15×— porque son sólo 10 celdas.

**La hipótesis que sostiene el peso está medida, no supuesta.** Ponderar a nivel de decil
(así y no a nivel de las 155 celdas año × grupo, que promedian 3 casos) exige que dentro de
cada decil la muestra sea aproximadamente representativa. El sorteo reparte el cupo del decil
entre esas celdas en proporción a su tamaño, así que debería serlo; el script lo comprueba
comparando composiciones y reporta la distancia de variación total por decil: **media 0,159,
máxima 0,277** (decil 3, con 35 casos sobre 28 celdas). No es cero, así que la estimación
arrastra algo de ese desbalance; está dentro de lo razonable para este tamaño, pero no es
exacta.

**Un contraste independiente.** El modelo predice sobre las 2.789 intervenciones
**321 H / 2.058 N / 410 D**; el oro reponderado, que no usa el modelo para nada, da
**301 H / 2.051 N / 438 D**. Difieren en 20, 7 y 28 intervenciones. Dos rutas distintas hacia
la misma cantidad que caen cerca: ninguna prueba la otra —ambas salen en parte de las mismas
500 etiquetas—, pero un desacuerdo grande habría sido una señal de alarma.

**Qué no corrige la ponderación:** el sesgo de una sola revisora, leer sólo la ventana
520+280 de cada texto, las 3 etiquetas marcadas `Duplicado_Exacto=SI`, y que los deciles se
definan con el puntaje léxico. El intervalo es sólo error de muestreo.

## Una hipótesis probada y descartada: mezclar el modelo con el léxico

Una exploración inicial sugirió que atenuar el modelo con el léxico
(`0,9·modelo + 0,1·léxico`) subía el macro-F1 a 0,709. **Esa cifra no era evidencia**: se
medía sobre las mismas 500 etiquetas que eligieron la configuración del release.

`scripts/validar_ensemble_hawkish_dovish.py` la prueba bien: el peso de la mezcla se elige
**dentro** de cada pliegue de entrenamiento con su propia CV interna, y sólo entonces se aplica
al pliegue retenido. Se mide el procedimiento completo, no un peso escogido a posteriori. El
script lleva un control obligatorio —en la semilla 0 debe reproducir el 0,702 publicado— y si
no lo reproduce aborta en vez de informar.

| regla de decisión | macro-F1 medio (5 semillas) |
|---|---|
| argmax (la publicada) | **0,6838** |
| umbral ±0,25 sobre el puntaje | 0,6596 |
| mezcla con el léxico, peso por CV interna | 0,6556 |

Diferencia mezcla − umbral: **−0,0040 (sd 0,0112)**; la mezcla gana en **2 de 5** semillas. Y la
CV interna eligió `w = 1,0` —es decir, *no mezclar*— en **9 de 25** pliegues, el valor más
frecuente. **La mezcla no mejora al modelo y no se publica.** El 0,709 exploratorio era sesgo de
selección, exactamente el riesgo que el defecto 6 ya había mostrado en la elección de
configuración. Artefacto: `ensemble_anidado.json`.

## El ruido del oro, medido por re-lectura ciega

El primer límite dice que una sola revisora produjo las 500 etiquetas. El **sesgo** de esa rúbrica no es medible desde adentro y sigue sin medirse. El **ruido**, en cambio, sí se puede acotar: re-leyendo.

**Protocolo.** Se sortearon 40 de las 500 (semilla 20260911) y se emitió sólo ID, fecha, actor, rol y la ventana de lectura —cabeza 520 + cola 280, la misma del protocolo—, sin la etiqueta. Se verificó que ninguna ventana contenga los tokens de metadato (`HAWKISH`, `DOVISH`, `NEUTRAL`, `HD_Clase`, `HD_Score`, `Evidencia`). La misma revisora puntuó de nuevo cada ventana de −1 a +1 sin abrir el oro; la clase sale de `UMBRAL_CLASE = 0,50`.

**Resultado** (`ruido_oro.json`; n=40, bootstrap de 4.000 con semilla fija):

| Medida | Valor | IC95 |
|---|---|---|
| Acuerdo de clase | **0,825** (33/40) | 0,707 – 0,943 |
| Kappa de Cohen | **0,582** | 0,257 – 0,833 |
| MAE del puntaje | **0,163** | 0,106 – 0,225 |
| Correlación de puntaje | **0,758** | — |
| Inversiones de signo | **0** | — |

Matriz (filas = re-lectura, columnas = oro):

| | HAWKISH | NEUTRAL | DOVISH |
|---|---|---|---|
| **HAWKISH** | 2 | 1 | 0 |
| **NEUTRAL** | 1 | 26 | 4 |
| **DOVISH** | 0 | 1 | 5 |

Las 7 discrepancias son **todas de clase vecina**: ninguna cruzó de hawkish a dovish ni al revés. La re-lectura fue más conservadora que el oro (31 neutrales vs 28), es decir, movió casos desde los extremos hacia el centro. Eso es lo que se espera de un ruido de umbral, no de un cambio de criterio: la frontera ±0,50 es donde se decide todo, y ahí los textos son genuinamente ambiguos.

**Qué implica para el modelo.** Fuera de pliegue el modelo acierta 0,780 en las 500; en estas mismas 40 acierta 0,625 (25/40), una fluctuación normal con n=40. El punto no es comparar 0,825 con 0,780: es que **el IC95 del acuerdo, 0,707–0,943, contiene al 0,780**. O sea, con estos datos no se puede afirmar que el modelo haya alcanzado el techo que le impone el ruido de sus propias etiquetas, ni tampoco que le falte mucho. Parte del 22% de error fuera de pliegue es inestabilidad de la etiqueta, no fracaso del clasificador, y esta medición no alcanza para separar las dos cosas.

**Qué NO resuelve.** Es test-retest de una sola revisora: mide estabilidad de criterio, no fiabilidad entre revisoras ni validez. Quien re-leyó ya había etiquetado las 500 antes, así que no se descarta memoria parcial y el 0,825 es un **techo optimista** del verdadero acuerdo. Y con n=40 el intervalo de kappa va de acuerdo moderado a casi perfecto: el número orienta, no cierra.

## Lo que encontró la auditoría metodológica

Una auditoría posterior ([documento completo](AUDITORIA_HAWKISH_DOVISH_V1_2026-09-11.md), **diez hallazgos** sobre ocho artefactos reproducibles) midió varias cosas que este informe no medía. Aquí van las tres que obligan a leer el macro-F1 con una distinción que antes no estaba; el documento completo añade la distancia al estado del arte (H5), el remedio por recencia que se probó y se refutó (H6), la calibración de la confianza (H7, más abajo) el contraste contra un léxico publicado, que resultó no realizable (H8), hasta dónde llega la fuga del H2 sobre los veredictos publicados (H9), y si el diseño de muestreo infla el rendimiento publicado (H10: no, lo subestima en 0,006).

**El modelo no generaliza en el tiempo.** La CV publicada mezcla 2005 con 2015, lo que supone intervenciones intercambiables. Bajo *rolling-origin* —entrenar con todo lo anterior, probar con el año siguiente, misma configuración— el macro-F1 medio cae a **0,456** (sd 0,105), con accuracy 0,727. Año por año va de 0,301 (2009) a 0,591 (2011).

La causa no es el modelo: es **desplazamiento real de etiquetas**. La proporción dovish pasa de 8,4% (2005-2007) a 30,7% (2008-2009) a 9,2% (2010-2012) a 23,8% (2013-2015). Eso es el ciclo monetario chileno, no un artefacto de etiquetado, y rompe la intercambiabilidad que la CV aleatoria necesita.

**Por tanto hay dos cifras y no una.** El **0,685** aplica a interpolar dentro del período 2005-2015 —que es lo que hace el release entregado—. El **0,456** es lo esperable al aplicar el modelo a reuniones nuevas. Este informe publicaba sólo la primera.

La CV aleatoria además filtra entre sesiones: el **90,7%** de las 130 sesiones del oro queda repartida en más de un pliegue, y agrupar por sesión baja el macro-F1 de 0,685 a **0,672** (diferencia −0,0124, sd 0,0183). Es menor y no invalida el ranking de configuraciones, pero el número limpio es 0,672.

Esa cifra limpia ya **se publica en el release** como `validacion_cruzada_por_sesion` en `resumen_entrenamiento.json`, calculada con la misma configuración y los mismos pliegues: macro-F1 **0,682**, accuracy 0,768, MAE 0,243, F1 por clase 0,690 / 0,844 / 0,512. La aleatoria por turno sigue publicada al lado, sin cambios (0,702 / 0,780 / 0,239), porque el release v1 está hasheado y reescribir sus titulares sería publicar un v2. **El modelo no se mueve**: la regla de selección elige 600/30/bal con ambas particiones —verificado sobre las cinco mejores de la rejilla—, así que `sha256_modelo` sigue siendo el mismo y los baselines (léxico 0,550, mayoría 0,271) son idénticos en las dos, como corresponde a predictores que no dependen de la partición.

**Lo que la auditoría sí encontró a favor:** el puntaje tiene validez de constructo. Extrayendo el Acuerdo formal de cada reunión (104 de 132 sesiones, cero incoherencias verbo/nivel en 92 transiciones), el tono medio del Consejo ordena correctamente las decisiones: +0,268 antes de alzas, −0,021 antes de mantener, −0,259 antes de recortes, con Spearman **+0,615** entre el tono de la reunión *t* y la decisión de la *t+1* —la única comparación sin fuga posible, porque el acta contiene el anuncio de la decisión y la versión contemporánea (0,788) está contaminada por leerlo—. Es la evidencia más fuerte de toda la entrega y faltaba.

Y el modelo **sigue ganándole al léxico en todos los cortes temporales** (p. ej. corte 2013: 0,671 contra 0,493). La conclusión comparativa aguanta; el nivel absoluto no.

## Límites

- **Una sola revisora** (este agente), sin segundo revisor semántico ni cotejo PDF. El **sesgo** de esa rúbrica no es medible desde adentro y sigue sin medirse. El **ruido** sí se acotó por re-lectura ciega de 40 etiquetas: acuerdo 0,825 (IC95 0,707–0,943), kappa 0,582 (IC95 0,257–0,833), cero inversiones de signo — pero es test-retest de la misma revisora y por posible memoria parcial es un techo optimista. Ver arriba.
- **Se leyó una ventana fija de 520 caracteres iniciales + 280 finales** (`LECTURA_CABEZA`/`LECTURA_COLA`; `Chars_Leidos` es 800 en las 500, cobertura media 34,8%), pero **el modelo entrena con el texto completo** (`rasgos_texto(r["Texto"])`). Medido sobre 40 textos re-leídos completos, el efecto directo es chico (acuerdo 0,925, κ 0,806 contra la pasada por ventana) pero no nulo: la ventana **omite votos explícitos** que caen en el medio del discurso. El efecto *indirecto* sobre el modelo sigue sin medirse.
- El puntaje describe **el texto**, no la intención del hablante; no se infiere voto donde el acta no lo dice.
- Las intervenciones de staff se puntúan por la dirección de los hechos que destacan; no se les atribuye preferencia de política.
- La muestra no es proporcional: el conteo crudo de las 500 **no** es la prevalencia del corpus. Reponderando por decil se estima (10,8% / 73,5% / 15,7%), pero la estimación arrastra el desbalance de composición dentro del decil (variación total media 0,159) y sólo corrige el diseño, no el sesgo de la rúbrica.
- La configuración se eligió mirando la misma validación cruzada que se reporta; con 500 casos ese sesgo de selección no es despreciable, y la diferencia entre las cinco mejores de la rejilla (0,655-0,702) es del orden de la desviación de la CV repetida (0,015).
- **La CV publicada es aleatoria por turno, no agrupada por sesión ni por tiempo.** Agrupar por sesión baja el macro-F1 a 0,672 —publicado como `validacion_cruzada_por_sesion`, 0,682 en la partición única—; validar hacia adelante lo baja a 0,456. El 0,685 sólo describe interpolación dentro de 2005-2015.
- No hay modelo de lenguaje natural preentrenado ni pesos externos.

## Reproducir

```bash
python scripts/hawkish_dovish.py --etapa muestra --n 500
python scripts/etiquetar_hawkish_dovish.py --estricto
python scripts/entrenar_hawkish_dovish.py --diagnostico
python3 scripts/diagnosticar_fallos_hawkish_dovish.py   # fallos_fuera_de_pliegue.csv
python3 scripts/validar_ensemble_hawkish_dovish.py      # ensemble_anidado.json
python3 scripts/estimar_prevalencia_hawkish_dovish.py   # prevalencia_reponderada.json
python3 scripts/medir_ruido_oro_hawkish_dovish.py       # ruido_oro.json (re-lectura ciega)
python3 scripts/auditar_hawkish_dovish.py               # auditoria_metodologica.json
python3 scripts/medir_efecto_ventana_hawkish_dovish.py # efecto_ventana.json
python3 scripts/medir_calibracion_hawkish_dovish.py    # calibracion_confianza.json
python -m unittest tests.test_hawkish_dovish -v
```

**134 pruebas: PASS.** Cubren:

- el **léxico** (dirección, negación, acotación) y el **tokenizador**;
- el **join turno/texto** sobre los 9.257 turnos;
- el **orden cronológico** (que la posición leída del `ID_Turno` coincida con el orden de las
  filas del acta en las 132 sesiones, que cada sesión arranque en `T1` sin huecos ni
  repetidos, y que ordenar la cadena dé un orden distinto —el gotcha de `T10` < `T9`);
- el **sorteo** (tamaño, deciles, determinismo, etiquetas forzadas);
- el **validador de etiquetas** (rechaza clase incoherente, evidencia falsa, duplicados y
  turnos ajenos a la muestra);
- el **clasificador** y la **reproducción de los 500 puntajes publicados desde el JSON**
  del modelo;
- la **regla de selección** (desviación estándar, reproducibilidad y estratificación de las
  particiones, desempate por CV repetida, y coherencia entre lo que la regla elige y lo que
  el release publica);
- el **diagnóstico de fallos fuera de pliegue** (cobertura de las 500, `Grupo_Actor` derivado
  del rol y no vacío, coherencia entre el CSV de fallos y la matriz publicada, y que
  recomputar la CV desde el modelo reproduce el macro-F1 del release);
- la **validación anidada de la mezcla** (que la rejilla incluya `w=1,0` para poder
  descartarla, que el control reproduzca el CV publicado, y que el veredicto cuadre con la
  diferencia medida);
- la **regla de decisión publicada** (la clase es argmax, no el umbral del puntaje, con los
  531 casos de discrepancia fijados);
- la **atribución de las cifras del propio informe** (cada distribución en el lado correcto
  de la frase; verificada por mutación: al invertir la frase la prueba falla);
- la **prevalencia reponderada** (que las prevalencias sumen 1, que los pesos reconstruyan
  exactamente las 2.789 intervenciones del universo, que ponderar mueva el resultado en el
  sentido esperado, que el IC95 sea coherente, que el efecto de diseño sea modesto, que los
  deciles estén balanceados por construcción, que la composición dentro del decil sea
  aproximadamente representativa y que el oro reponderado concuerde con la predicción del
  modelo);
- la **coherencia entre el README y el informe** (que el README no niegue la prevalencia que
  el informe publica, que ambos citen las mismas cifras del mismo artefacto y la misma
  cobertura de lectura; verificada por mutación: al reintroducir la frase contradictoria la
  prueba falla).
- el **ruido del oro por re-lectura ciega** (que la submuestra no filtre la etiqueta, que el
  sorteo se reproduzca con la semilla, que la re-lectura cubra exactamente la submuestra,
  que las cifras del artefacto se recalculen desde las entradas, que toda discrepancia sea
  de clase vecina, que los intervalos envuelvan la estimación y que los límites estén
  declarados, y que el contraste con el modelo se recalcule desde el CSV de fallos fuera
  de pliegue en vez de estar escrito a mano; verificada por mutación: al alterar una
  etiqueta de la re-lectura el acuerdo recalculado deja de cuadrar con el artefacto, y al
  falsear el contraste o el 0,625 del informe la prueba correspondiente falla).
- la **auditoría metodológica** (que la CV aleatoria filtre entre sesiones, que el
  *rolling-origin* caiga por debajo del número publicado mientras la accuracy se sostiene,
  que el desplazamiento de etiquetas sea el medido, que la extracción de decisiones no
  tenga incoherencias, que la validez de constructo sobreviva a quitar el anuncio y
  mantenga el orden ALZA > SIN CAMBIO > RECORTE, que el κ del oro quede bajo el umbral
  de 0,667 citado, y que el modelo le gane al léxico en los tres cortes temporales);
- que **el informe y el README adviertan** que el 0,685 es de interpolación y el 0,456 el
  esperable hacia adelante.
- el **efecto de la ventana de lectura** (que las tres pasadas cubran la misma submuestra,
  que las tres comparaciones se recalculen desde las entradas, que el efecto puro sea chico
  pero no nulo, que ninguna comparación invierta el signo, que leer completo no empeore el
  acuerdo con el oro y que los límites estén declarados).

## Siguiente paso

La muestra está cerrada, la regla de selección corregida y la prevalencia ya estimada con
pesos de diseño. Lo útil ahora es: (1) revisar la rúbrica de los **343 NEUTRAL (69% del oro)**,
que son los que más errores arrastran —41 dovish y 17 hawkish cayeron ahí—; (2) si se quiere
subir el F1 dovish sobre 0,60, el cuello es la rúbrica o los rasgos, no el tamaño del oro;
(3) un segundo revisor sobre una submuestra daría por fin una medida del acuerdo
inter-rúbrica, que con 500 etiquetas y una sola revisora sigue sin ser estimable.
