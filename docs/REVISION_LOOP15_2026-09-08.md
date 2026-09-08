# LOOP15 — Exposiciones largas, daño textual y retorno de Schmidt-Hebbel

**2026-09-08 · [PR #3](https://github.com/joako0o/nlm_proyect/pull/3).**
Base: `c470d106394f1d53ab6d1b13b66adf6d5a81bf78`, [LOOP14](REVISION_LOOP14_2026-09-08.md).
Lectura dirigida por agente del texto disponible; **sin nuevo cotejo PDF ni
revisión humana independiente**.

## Resultado publicado

| Medida | Antes | Ahora |
|---|---:|---:|
| Filas físicas XLSX | 9.499 | **9.500** |
| Bloques de texto | 9.498 | 9.499 |
| Grupos de turno | 9.088 | 9.089 |
| Grupos de varias filas | 315 | 315 |
| Filas con alertas | 329 | **321** |
| Padres con alertas | 296 | **288** |
| Pruebas | 1.073 | **1.100** |
| Intervalos revisados de hablante | 208 | **223** |
| Padres con revisión de hablante | 204 | 216 |
| Advertencias contextuales | 15 | 21 |

**15 padres afectados:** 1090 con separación estructural y revisión de atribución,
13 sólo con metadatos de atribución y 1091 sólo con trazabilidad. No son 15 nuevos
diálogos separados ni 15 padres íntegramente certificados. Los otros **7.204
padres** conservan sus campos semánticos, descontando identificadores secuenciales.

- [Comparación global antes/después](comparacion_loop15_2026-09-08.json)
- [Detalle de filas y hashes](cambios_loop15_2026-09-08.csv)
- [Checkpoint y pendientes](estado_revision_loop15_2026-09-08.json)

## 1. Catorce exposiciones leídas íntegramente en su texto disponible

**Valdés:** 644, 664, 770, 817, 867, 932, 976, 1012, 1047, 1090, 1155, 1209 y 1251.
**Magendzo:** 1297.

Se leyeron los intervalos completos, las cesiones nominales pertinentes y el
retorno o apertura de comentarios posterior. Son **111.314 caracteres en la
salida**, sin incluir el retorno adicional de Schmidt-Hebbel. Las enumeraciones,
viñetas y párrafos de análisis se mantienen unidos; comparar opciones opuestas
no significa que cambie quien habla. Tampoco las menciones a acuerdos anteriores,
votos de mayoría/minoría o citas de comunicados constituyen turnos nuevos.

En 1297 la cesión nombra a **Igal Magendzo**, Gerente de Análisis Macroeconómico,
y el desarrollo vuelve a nombrarlo. No se atribuye a Valdés por ser el expositor
habitual de las Opciones. En los padres con varias personas, la revisión termina
antes del retorno efectivo de la Presidencia o del siguiente participante.

«Lectura íntegra» significa aquí todo el intervalo **disponible en el consolidado**,
no que el OCR carezca de omisiones. Se registran por separado los daños detectados.
No se amplían las revisiones anteriores de las introducciones de 351/727 a sus
series posteriores.

## 2. Un cambio de hablante omitido en 1090

Al inspeccionar el retorno de la Presidencia después de Valdés, se encontró una
intervención de Schmidt-Hebbel absorbida en el segmento de Corbo:

| Antes | Después |
|---|---|
| Corbo: 1.382 caracteres | Corbo: **88**, apertura de comentarios |
| Dentro del mismo segmento | Schmidt-Hebbel: **1.293**, recomendación propia |
| García: 1.133 | García: **1.133**, sin alteración |

El sujeto invertido dice «Señala el Gerente de Investigación Económica, señor
Klaus Schmidt- Hebbel». Se leyó toda la recomendación; el nombre, cargo y nómina
local identifican a Schmidt-Hebbel. Se conserva **«Schmidt- Hebbel»** literalmente.
La revisión acotada permite el corte sin añadir una regla global de apellidos OCR.

En 1090 quedan siete segmentos en vez de seis. La exposición de Valdés, la
apertura de Corbo, la recomendación de Schmidt-Hebbel y la intervención de García
son independientes. **1091 sólo actualiza su antecedente del segmento 6 al 7 de
1090**; mantiene texto, actor y enlace de continuidad. No se adjudica una nueva
lectura integral a 1091 por ese cambio técnico.

## 3. Preservar las revisiones anteriores dentro de los mismos padres

Se añaden **15 intervalos en 14 padres**, 12 de ellos nuevos en el registro:
las 14 exposiciones y el retorno de Schmidt-Hebbel.

- **644:** la exposición nueva de Valdés precede a la pregunta de Marfán ya
  revisada. El contenedor se ordena cronológicamente; la pregunta pasa a intervalo
  secundario con **el mismo identificador, límites 6928–7093, actor y evidencia**.
  No se absorbe en Schmidt-Hebbel ni se reemplaza su revisión.
- **664:** la suspensión de Corbo, límites **433–562**, sigue intacta como primer
  intervalo. La exposición de Valdés se añade después, sin extender la suspensión.
- **1090:** exposición de Valdés y retorno de Schmidt-Hebbel se registran como
  dos intervalos independientes.

Los **208 intervalos previos permanecen idénticos por identificador**, incluidos
los secundarios de 1923/2622/4923/5367. Hay ahora siete padres con varios
intervalos: 644/664/1090/1923/2622/4923/5367. `CONTEXTO_REVISADO` no crea anclas
globales y `Fin` por sí solo no crea cortes.

## 4. Seis daños advertidos, no reconstruidos

| Padre | Evidencia de ruptura textual o sintáctica |
|---|---|
| **644** | «costos laborales U 5.» |
| **664** | «la persistencia que 8.» |
| **770** | «desde fines del • La inflación»; también queda «comentarios.» desplazado respecto de la apertura presidencial siguiente, cortada en «para» |
| **1012** | «inflacionaria efectiva y de los Señala» |
| **1047** | «más de medio punto por debajo • El IPC» |
| **1155** | «que en el último IPOM y que, aunque» |

Se registra `TEXTO_DANADO_POR_COTEJAR` en el intervalo de exposición correspondiente.
La identidad del expositor no resuelve el contenido ausente, desplazado o la
ruptura sintáctica. No se agregan palabras, no se reordena «comentarios» y no se
extiende el aviso a las otras voces de esos padres. Las quince advertencias
anteriores permanecen intactas, incluidas las discrepancias de cargo y las
identidades/residuos colectivos pendientes.

## 5. Controles y publicación

Un ensayo aislado y el pipeline integral `python scripts/preparar_data.py`
completaron **1.100 pruebas y controles F0/F1**, sin errores bloqueantes. La base
de auditoría publicada coincide campo por campo con el ensayo aislado.

**27 pruebas nuevas:** 14 contratos exactos por padre y 13 pruebas de alcance,
conservación, daños, anclas, intervalos secundarios y separación del retorno.
Se actualizaron los conteos previos y la prueba de concatenaciones para consultar
**todos los intervalos**, no sólo el primero de cada padre. Se corrigió un fixture
nuevo de continuidad al que le faltaban identificadores requeridos. No se
relajaron las validaciones del constructor.

Verificación posterior:

- **7.219 textos y 2.048.560 palabras conservados**, ignorando sólo espacios.
- **Todos los enlaces previos entre padres y los grupos no afectados intactos**;
  sin enlaces nuevos ni retirados. Se conservan las dos exposiciones de García
  de once filas, 2790 → 2791 y el retiro del enlace erróneo 5402 → 5403.
- Los **208 intervalos anteriores** y sus notas, quince avisos previos, once
  menciones actuales, 21 fórmulas y registros documentales permanecen intactos.
- **66 hashes de entradas/código y 11 de salidas verificados**.
- 132 sesiones, 51 etiquetas/50 personas, 310 contrastes TPM y esquemas XLSX **37/24**.
- Los tres escritos de Larraín leídos por Vergara mantienen **autor ≠ lector**,
  sin inferir asistencia ni habla oral. Se preserva el modelo 5212/5742/5802.
- 3110 continúa como `ACTA_INSTITUCIONAL`, no Orellana ni comunicado monetario;
  la revisión de 797 caracteres de 3421 se conserva.
- **Ningún archivo de `scripts/` cambia en esta pasada**: las correcciones usan
  revisiones acotadas, no reglas nuevas generalizadas al corpus.

## 6. Pendientes y límites

**321 filas con alertas en 288 padres.** Las anáforas bajan **16 → 2**, pero se
incorporan seis avisos de daño: el descenso neto de alertas es **329 → 321**.
Las dos anáforas restantes son las exposiciones de Lehmann de **506** (8.662
caracteres, distinta de la respuesta ya revisada) y **1572** (18.132 caracteres).
**No fueron leídas íntegramente ni adjudicadas en esta pasada.** No representan
el total pendiente del corpus.

Motivos superpuestos: 258 finales sin puntuación, 21 posibles otros hablantes o
menciones, diez breves, nueve daños documentados, ocho atribuciones legadas,
seis pasajes conjuntos, seis variantes de identidad, cinco cargos pendientes,
tres duplicados no fórmula, tres escritos leídos por tercero, dos anáforas y
un caso de hablantes por identidad pendiente.

Persisten 780/6185, los residuos de 3191/5367, 4433, 6443, variantes de Ricaurte,
6530 y otros casos ambiguos. No se asignan pasajes conjuntos ni identidades por
tema o proximidad. Las alertas no son todas errores confirmados ni filas sin leer.

La cola histórica de 783 conserva **107 intervalos pendientes de lectura
contextual**: 325 métodos actualizados, 171 cambios por comparación, 98 correcciones
dirigidas, 58 fórmulas, siete breves, ocho menciones históricas, seis identidades,
dos repeticiones y una continuidad. Clasifica 496 comparaciones automáticas,
174 lecturas dirigidas y 113 triajes. Las actualizaciones de método se clasifican
como comparación automática: no sustituyen el registro de las 15 lecturas acotadas
nuevas. **117 → 107 no significa diez lecturas humanas ni cierres integrales.**

Las unidades históricas y actuales se superponen y **no se suman**. Falta cotejo
de originales en casos ambiguos/dañados y una muestra independiente con y sin
alertas. No hubo lectura exhaustiva ni nuevo cotejo PDF. Las verificaciones son
locales; el workflow de GitHub Actions sigue fuera del PR por falta de permiso
`workflows`. No queda proceso activo.
