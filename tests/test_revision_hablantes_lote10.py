"""Lote10: separar por intervención sin tocar el registro histórico fijado por hash.

Las cuatro revisiones viven en ``revisiones_hablantes_lote10.json`` porque el
registro histórico está fijado por hash en veinte paquetes de procedencia;
agregarle entradas los invalida en cascada. Estas pruebas cubren lo que los
conteos ajenos ya no cubren: que las revisiones nuevas cargan, que no solapan el
registro, que cada corte produce el segmento esperado con su actor, y que el
registro histórico queda byte a byte como estaba.
"""
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import build_base_referencia as b  # noqa: E402
from curation import (SPEAKER_REVIEWS, load_speaker_reviews,  # noqa: E402
                      validate_speaker_reviews, text_hash)

LOTE10 = ROOT / 'data/curation/revisiones_hablantes_lote10.json'

# padre -> (actor del tramo revisado, inicio, fin, actor de la fila anterior)
ESPERADO = {
    657: ('Sergio Lehmann Beresi', 458, 4394, 'Vittorio Corbo Lioi'),
    1564: ('María Olivia Recart Herrera', 163, 2230, 'Vittorio Corbo Lioi'),
    1995: ('Sergio Lehmann Beresi', 740, 2791, 'Jorge Desormeaux Jiménez'),
    2960: ('Kevin Cowan Logan', 5729, 7785, 'José De Gregorio Rebeco'),
}


class Lote10Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wb = b.openpyxl.load_workbook(b.SRC, data_only=True, read_only=True)
        data = list(wb[b.SRC and 'Consolidado'].iter_rows(values_only=True))[1:]
        wb.close()
        cls.raw = {int(r[0]): {'Fecha': b.to_date_str(r[1]), 'Texto': str(r[5]),
                               'Actor': str(r[2])} for r in data}
        cls.entradas = json.loads(LOTE10.read_text(encoding='utf-8'))
        cls.historico = load_speaker_reviews(cls.raw)
        cls.completas = b.revisiones_hablantes_completas(cls.raw)

    def test_el_lote_carga_y_valida_contra_la_fuente(self):
        self.assertEqual(len(self.entradas), 4)
        sueltas = load_speaker_reviews(self.raw, LOTE10)
        self.assertEqual(set(sueltas), set(ESPERADO))
        for padre, entrada in sueltas.items():
            with self.subTest(padre=padre):
                self.assertEqual(entrada['SHA256_Texto_Padre'],
                                 text_hash(self.raw[padre]['Texto']))
                self.assertEqual(entrada['Tipo_Revision'], 'LECTURA_DIRIGIDA_POR_AGENTE')
                self.assertTrue(entrada['Justificacion'])
                self.assertTrue(entrada['Limitacion'])
                self.assertTrue(entrada['Evidencia'])

    def test_no_solapa_el_registro_historico(self):
        self.assertEqual(len(self.historico), 353)
        self.assertEqual(len(self.completas), 357)
        self.assertFalse(set(self.historico) & set(ESPERADO))
        # los mismos Revision_ID no pueden repetirse entre los dos archivos
        historicos = {e['Revision_ID'] for e in
                      json.loads(SPEAKER_REVIEWS.read_text(encoding='utf-8'))}
        self.assertFalse(historicos & {e['Revision_ID'] for e in self.entradas})

    def test_el_registro_historico_queda_intacto(self):
        """Los veinte paquetes que lo fijan por hash deben seguir vigentes."""
        self.assertEqual(len(json.loads(SPEAKER_REVIEWS.read_text(encoding='utf-8'))), 353)
        actual = hashlib.sha256(SPEAKER_REVIEWS.read_bytes()).hexdigest()
        fijados = {}
        for paquete in (ROOT / 'docs').rglob('*.json'):
            try:
                d = json.loads(paquete.read_text(encoding='utf-8'))
            except Exception:
                continue
            if not isinstance(d, dict):
                continue
            for campo, valor in d.items():
                if not campo.startswith('SHA256_') or not isinstance(valor, dict):
                    continue
                for ruta, h in valor.items():
                    if ruta.endswith('revisiones_hablantes.json'):
                        fijados[str(paquete)] = h
        self.assertGreaterEqual(len(fijados), 15)
        for paquete, h in fijados.items():
            with self.subTest(paquete=paquete):
                self.assertEqual(h, actual)

    def test_cada_corte_produce_su_segmento_con_el_actor_revisado(self):
        for padre, (actor, inicio, fin, anterior) in ESPERADO.items():
            with self.subTest(padre=padre):
                texto = self.raw[padre]['Texto']
                partes = b.segment_turns(texto, self.raw[padre]['Fecha'],
                                         self.raw[padre]['Actor'],
                                         review=self.completas.get(padre))
                # el contenido no se pierde ni se reescribe
                self.assertEqual(''.join(''.join(t.split()) for t, _, _ in partes),
                                 ''.join(texto.split()))
                actores = [a for _, a, _ in partes]
                fuentes = [m for _, _, m in partes]
                self.assertIn(actor, actores)
                self.assertEqual(fuentes[actores.index(actor)], 'CONTEXTO_REVISADO')
                # el tramo revisado empieza exactamente donde dice la revisión
                self.assertEqual(texto[inicio:fin].startswith(
                    self.completas[padre]['Cita_Inicio']), True)
                # y el hablante anterior conserva su tramo propio
                self.assertIn(anterior, actores)

    def test_los_intervalos_revisados_sobreviven_con_su_actor(self):
        filas = []
        for padre in ESPERADO:
            for texto, actor, fuente in b.segment_turns(
                    self.raw[padre]['Texto'], self.raw[padre]['Fecha'],
                    self.raw[padre]['Actor'], review=self.completas.get(padre)):
                filas.append(dict(ID=len(filas) + 1, ID_Padre=padre, Texto=texto,
                                  Actor_Final=actor, Fuente_Actor=fuente))
        revisadas = {p: r for p, r in self.completas.items() if p in ESPERADO}
        self.assertEqual(validate_speaker_reviews(filas, revisadas), [])

    def test_sin_el_lote_esos_padres_no_se_cortan(self):
        """Prueba de que el corte viene de la revisión y no del detector."""
        for padre, (actor, inicio, _, _) in ESPERADO.items():
            with self.subTest(padre=padre):
                texto = self.raw[padre]['Texto']
                sin = b.segment_turns(texto, self.raw[padre]['Fecha'],
                                      self.raw[padre]['Actor'])
                self.assertNotIn('CONTEXTO_REVISADO', [m for _, _, m in sin])


if __name__ == '__main__':
    unittest.main()
