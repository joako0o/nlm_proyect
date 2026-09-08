"""Alertas de revisión, NO etiquetas de error ni certificación de pureza."""
import re

LEGACY_METHODS = {'ORIGINAL', 'ROL+NOMBRE', 'NOMBRE+VERBO', 'ROL+FECHA',
                  'PRIMERA_ORACION', 'HERENCIA', 'SIN_DETECTAR', 'PSEUDO'}


def review_reasons(row, detector, sentence_spans):
    reasons = set()
    text = row['Texto'] or ''
    actor = row['Actor_Final']
    date = str(row['Fecha'])[:10]
    if row['Fuente_Rol'] == 'PENDIENTE_REVISION':
        reasons.add('CARGO_SIN_CONFIRMACION_ASISTENCIA')
    if row['Fuente_Actor'] in LEGACY_METHODS:
        reasons.add('ATRIBUCION_HEURISTICA_LEGADA')
    if row['Fuente_Actor'] == 'ANAFORA_LOCAL':
        reasons.add('ATRIBUCION_POR_ANAFORA')
    if actor != 'Consejo del Banco Central de Chile':
        for a, b in sentence_spans(text):
            # Más sensible que el segmentador: incluye citas y referencias.
            # Un candidato distinto requiere inspección; NO se divide a ciegas.
            candidates = detector.candidates(text[a:b], date, actor, allow_embedded=True)
            if any(c['actor'] != actor for c in candidates):
                reasons.add('POSIBLE_OTRO_HABLANTE_O_MENCION')
                break
    if '\ufffd' in text:
        reasons.add('CARACTER_REEMPLAZO_OCR')
    if text and not text.rstrip().endswith(('.', '!', '?', ':', ';', '"', "'", ')', ']', '}', '”', '»')):
        reasons.add('FINAL_SIN_PUNTUACION')
    if len(text.split()) < 8:
        reasons.add('FRAGMENTO_BREVE')
    if row['Duplicado_Exacto'] == 'SI' and row['Duplicado_Formula'] != 'SI':
        reasons.add('DUPLICADO_NO_FORMULA')
    if actor in ('Miguel Ricaurte Vintimilla', 'Miguel Ricaurte Bermúdez'):
        reasons.add('VARIANTE_IDENTIDAD_POR_VERIFICAR')
    return sorted(reasons)
