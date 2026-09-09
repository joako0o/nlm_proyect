"""Lote 5: últimas comas personales de esta subcola, sin cerrar alertas."""
import copy
import csv
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import revisar_cola_comas as c

PATHS = [ROOT / f'docs/revision_comas_lote{n}_2026-09-08/revisiones.json'
         for n in range(1, 6)]


class CommaFifthBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = c.read_rows(ROOT / 'data/processed/consolidado_base_referencia.xlsx')
        cls.packages = [json.loads(p.read_text()) for p in PATHS]
        cls.new = cls.packages[-1]

    def parent(self, p):
        return [r for r in self.rows if r['ID_Padre'] == p]

    def one(self, e):
        p = e['ID_Padre']
        package = copy.deepcopy(self.new)
        package['Revisiones'] = [copy.deepcopy(e)]
        package['Padres'] = {str(p): package['Padres'][str(p)]}
        return copy.deepcopy(self.parent(p)), package

    def test_previous_four_packages_frozen(self):
        hashes = [
            'efd48b25aaa63ca591eb1bd2ca7923edff8bc2ede898c0635f73719b660b80fc',
            'bb343dc2fd538d47a701f9d80a82200d1d9b13088cd70789f79e77efa0b70a99',
            '28f16b295bb6d3502e39545ac3fcef19f9054817aa6b2f7765e9ca4faa94ca52',
            'f90d96e3580f815cced0516449c9dee9dddf3ffd5958b07e78df78a7a4bbbef9',
        ]
        for path, expected in zip(PATHS[:4], hashes):
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)

    def test_twenty_complete_parents(self):
        self.assertEqual(len(c.validate_reviews(self.rows, self.new)), 20)
        self.assertEqual(len(self.new['Padres']), 20)
        self.assertEqual(sum(len(p['Texto_Padre']) for p in self.new['Padres'].values()), 47515)
        previous = {p for pkg in self.packages[:4] for p in pkg['Padres']}
        self.assertFalse(previous & set(self.new['Padres']))

    def test_exact_remaining_personal_limits_from_lot4(self):
        with PATHS[3].with_name('comas_sin_ficha.csv').open(encoding='utf-8-sig') as f:
            remaining = list(csv.DictReader(f))
        expected = {q['ID_Intervencion'] for q in remaining
                    if 'Consejo del Banco' not in q['Actor_Izquierda'] + q['Actor_Derecha']}
        actual = {e['Izquierda']['ID_Intervencion'] for e in self.new['Revisiones']}
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 20)

    def test_cumulative_162_fiches_five_institutional_pending(self):
        before = copy.deepcopy(self.rows)
        package = c.combine_packages(self.packages)
        queue = c.build_queue(self.rows, package)
        self.assertEqual(len(queue), 167)
        self.assertEqual(len(package['Padres']), 146)
        self.assertEqual(sum(q['Estado_Lectura'] == c.STATE for q in queue), 162)
        pending = [q for q in queue if q['Estado_Lectura'] == c.PENDING]
        self.assertEqual({q['ID_Padre'] for q in pending}, {601, 1901, 2112, 2803, 5252})
        self.assertEqual(len(pending), 5)
        self.assertTrue(all('Consejo del Banco' in q['Actor_Izquierda'] + q['Actor_Derecha']
                            for q in pending))
        self.assertEqual(self.rows, before)
        self.assertEqual(sum(bool(r['Motivos_Revision']) for r in self.rows), 465)

    def test_whole_developments_and_returns(self):
        sizes = {
            658: [106, 215, 508, 71, 83, 1037, 496],
            1737: [90, 132, 1136],
            2532: [123, 523, 1059, 201, 737],
            2588: [163, 2331, 238],
            2666: [51, 108, 2743],
            3051: [188, 40, 291, 1705, 296],
        }
        for p, expected in sizes.items():
            rows = self.parent(p)
            self.assertEqual([len(r['Texto']) for r in rows], expected)
            for a, b in zip(rows, rows[1:]):
                if a['Actor_Final'] != b['Actor_Final']:
                    self.assertNotEqual(a['ID_Turno'], b['ID_Turno'])
        self.assertIn('Joaquín Vial', self.parent(658)[5]['Texto'])
        self.assertFalse(any('Vial' in r['Actor_Final'] for r in self.parent(658)))

    def test_multiparagraph_links_and_interrupted_lehmann(self):
        for p, q in [(2555, 2556), (2897, 2898), (3101, 3102)]:
            self.assertEqual(self.parent(p)[-1]['ID_Turno'], self.parent(q)[0]['ID_Turno'])
        rows = self.parent(2556)
        self.assertEqual([len(r['Texto']) for r in rows], [1434, 102, 910])
        self.assertEqual(rows[0]['Actor_Final'], rows[2]['Actor_Final'])
        self.assertNotEqual(rows[0]['ID_Turno'], rows[2]['ID_Turno'])
        self.assertEqual(self.parent(2555)[1]['Motivos_Revision'], 'FINAL_SIN_PUNTUACION')

    def test_2705_personal_focus_does_not_absorb_acta(self):
        rows = self.parent(2705)
        self.assertEqual([len(r['Texto']) for r in rows], [430, 194, 664, 281, 136, 1096, 199])
        self.assertEqual(rows[3]['Fuente_Actor'], 'CONTEXTO_REVISADO')
        self.assertIsNone(rows[3]['ID_Ancla_Actor'])
        self.assertEqual(rows[-1]['Fuente_Actor'], 'ACTA/META')
        self.assertEqual(rows[-1]['Actor_Final'], 'Consejo del Banco Central de Chile')
        self.assertIn('María Olivia Recart', rows[-1]['Texto'])
        self.assertNotEqual(rows[-1]['ID_Turno'], rows[-2]['ID_Turno'])
        e = next(e for e in self.new['Revisiones'] if e['ID_Padre'] == 2705)
        self.assertEqual(e['Derecha']['ID_Intervencion'], rows[3]['ID_Intervencion'])

    def test_2885_vote_damage_not_closed_by_focal_review(self):
        rows = self.parent(2885)
        self.assertEqual([len(r['Texto']) for r in rows], [78, 165, 2400])
        self.assertEqual(rows[-1]['Motivos_Revision'], 'TEXTO_DANADO_POR_COTEJAR')
        self.assertTrue(rows[-1]['Texto'].endswith('Para concluir con la votación,.'))
        self.assertEqual(rows[-1]['ID_Ancla_Actor'], rows[-1]['ID_Intervencion'])
        self.assertNotEqual(rows[1]['ID_Turno'], rows[2]['ID_Turno'])
        e = next(e for e in self.new['Revisiones'] if e['ID_Padre'] == 2885)
        for field in ['Texto', 'Motivos_Revision', 'ID_Ancla_Actor']:
            changed, package = self.one(e)
            changed[-1][field] = 'Cambio'
            with self.assertRaises(ValueError):
                c.validate_reviews(changed, package)

    def test_3268_short_confirmation_and_damaged_closure_preserved(self):
        rows = self.parent(3268)
        self.assertEqual([len(r['Texto']) for r in rows], [388, 47, 572, 688])
        self.assertEqual(rows[1]['Motivos_Revision'], 'DUPLICADO_NO_FORMULA')
        self.assertEqual(rows[-1]['Motivos_Revision'], 'TEXTO_DANADO_POR_COTEJAR')
        self.assertTrue(rows[-1]['Texto'].endswith('No habiendo más comentarios,.'))
        self.assertEqual(len({r['ID_Turno'] for r in rows}), 4)

    def test_3012_own_anchor_not_inherited_from_context(self):
        rows = self.parent(3012)
        self.assertEqual([len(r['Texto']) for r in rows], [109, 375, 1867])
        self.assertEqual(rows[1]['Fuente_Actor'], 'CONTEXTO_REVISADO')
        self.assertIsNone(rows[1]['ID_Ancla_Actor'])
        self.assertEqual(rows[2]['ID_Ancla_Actor'], rows[2]['ID_Intervencion'])
        self.assertNotEqual(rows[1]['ID_Turno'], rows[2]['ID_Turno'])

    def test_literal_residues_and_nonfocal_warning(self):
        parents = self.new['Padres']
        for p, literal in [('2620', r'staff Wer\e'), ('2624', '9,%'),
                           ('2666', 'tasas de nesgo'), ('3101', 'dan cuneta'),
                           ('2588', 'IRC')]:
            self.assertIn(literal, parents[p]['Texto_Padre'])
        rows = self.parent(2915)
        self.assertEqual([len(r['Texto']) for r in rows], [475, 241, 244, 1520])
        self.assertTrue(rows[2]['Texto'].endswith('sector público. i'))
        self.assertEqual(rows[2]['Motivos_Revision'], 'FINAL_SIN_PUNTUACION')
        self.assertIn('calda', rows[3]['Texto'])

    def test_each_endpoint_change_invalidates_its_fiche(self):
        for e in self.new['Revisiones']:
            for side in ['Izquierda', 'Derecha']:
                for field, value in [('Texto', 'Cambio,'), ('Actor_Final', 'Otra persona'),
                                     ('Fecha', '1900-01-01'), ('Fuente_Actor', 'ORIGINAL')]:
                    rows, package = self.one(e)
                    row = next(r for r in rows if r['ID_Intervencion'] == e[side]['ID_Intervencion'])
                    row[field] = value
                    with self.subTest(rid=e['Revision_ID'], side=side, field=field):
                        with self.assertRaises(ValueError):
                            c.validate_reviews(rows, package)

    def test_sources_parent_signatures_and_duplicate_rejection(self):
        c.check_sources(self.new)
        for p, e in self.new['Padres'].items():
            self.assertEqual(e['SHA256_Texto_Padre'], c.sha(e['Texto_Padre']))
            self.assertEqual(e['SHA256_Particion'], c.parent_signature(self.parent(int(p))))
            self.assertEqual(c.compact(e['Texto_Padre']),
                             ''.join(c.compact(r['Texto']) for r in self.parent(int(p))))
        with self.assertRaisesRegex(ValueError, 'duplicado'):
            c.combine_packages(self.packages + [self.new])

    def test_institutional_endpoints_still_rejected(self):
        # Synthetic negative fixtures, not registered reviews or claimed readings.
        queue = c.build_queue(self.rows, c.combine_packages(self.packages))
        by_id = {r['ID_Intervencion']: i for i, r in enumerate(self.rows)}
        for q in queue:
            if q['Estado_Lectura'] != c.PENDING:
                continue
            p = q['ID_Padre']
            rows = self.parent(p)
            pos = by_id[q['ID_Intervencion']]
            left, right = self.rows[pos:pos + 2]
            e = copy.deepcopy(self.new['Revisiones'][0])
            e.update(ID_Padre=p, Fecha=str(left['Fecha'])[:10],
                     Izquierda=c.endpoint(left), Derecha=c.endpoint(right))
            text = ' '.join(r['Texto'] for r in rows)
            package = copy.deepcopy(self.new)
            package['Revisiones'] = [e]
            package['Padres'] = {str(p): dict(
                Fecha=e['Fecha'], Lectura='PADRE_COMPLETO', Texto_Padre=text,
                SHA256_Texto_Padre=c.sha(text), SHA256_Particion=c.parent_signature(rows))}
            with self.subTest(parent=p):
                with self.assertRaisesRegex(ValueError, 'sólo revisa límites personales'):
                    c.validate_reviews(rows, package)


if __name__ == '__main__':
    unittest.main()
