"""QA de preparación para v9: el mismo módulo, con la comparación interna apuntando a v9.

``qa_preparacion.py`` está fijado por hash en varios manifiestos y, cuando el
refinamiento funcional v5 está activo, llama internamente a
``compare_functional_v7.compare``, que exige la cardinalidad de v7 (9.723 filas)
porque eso es lo que v7 debía probar. v9 agrega una fila legítimamente, así que
esa comparación interna se sustituye en memoria por la de v9.

No se toca ningún byte fijado: la sustitución vive en este archivo nuevo y el
módulo original se importa tal cual. La comparación que se ejecuta es la misma
que corre el gate, sobre los mismos archivos.
"""
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import build_base_referencia as builder  # noqa: E402
import compare_functional_v7 as v7  # noqa: E402
import compare_procedural_v9 as v9  # noqa: E402
import qa_preparacion  # noqa: E402


def compare_como_v9(antes, despues, refinamientos):
    """Reemplaza la comparación v7 por la v9 dentro de qa_preparacion.

    ``qa_preparacion`` pasa las filas del consolidado intermedio; se recarga el
    consolidado final del staging para comparar exactamente lo mismo que el gate.
    """
    stage = Path(os.environ['NLM_PROCESSED_DIR'])
    candidato = stage / v9.BASE.name
    report, _ = v9.compare(v9.read_rows(v9.BASE), v9.read_rows(candidato), v9.revisiones())
    if not report['Pasa']:
        raise ValueError('La comparación v9 no pasó')
    return report, []


# qa_preparacion importa compare_functional_v7.compare DENTRO de main(), así que
# parchar el atributo del módulo alcanza: se recoge en el momento de la llamada.
v7.compare = compare_como_v9

# Segunda causa: qa_preparacion carga las lecturas procedimentales del archivo fijado,
# que trae el ID posicional de antes del corte. matching_review compara ese ID, así que
# los tres pares posteriores al corte dejan de reconocerse y saltan «relación
# procedimental sin prueba exacta» y «continuidad atraviesa barrera». Se refresca el
# mismo campo posicional, con la misma función que usa el constructor.
_active_procedural_original = qa_preparacion.active_procedural


def active_procedural_con_ids(continuity_raw):
    lecturas = _active_procedural_original(continuity_raw)
    _, filas = qa_preparacion.read_rows(
        Path(os.environ['NLM_PROCESSED_DIR']) / 'consolidado_base_referencia.xlsx')
    builder.refrescar_ids_de_lectura(filas, lecturas)
    return lecturas


qa_preparacion.active_procedural = active_procedural_con_ids

# Tercera causa: qa_preparacion carga sólo el registro histórico de hablantes, así que
# los cuatro segmentos del lote10 quedan sin evidencia que los respalde. Se le pasa el
# registro completo —el histórico más el lote10—, que es exactamente lo que el
# constructor fusiona para producir esas filas.
qa_preparacion.load_speaker_reviews = builder.revisiones_hablantes_completas

if __name__ == '__main__':
    raise SystemExit(qa_preparacion.main())
