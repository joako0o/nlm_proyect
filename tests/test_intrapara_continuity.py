"""Implementación opt-in y publicación versionada, no simulación de etiquetas.

LOOP32 se lee explícitamente como baseline histórico. La salida se obtiene por
el motor real con las dos pruebas, manteniendo las pruebas entre padres aparte.
"""
import copy
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_base_referencia as builder
import preparar_data as pipeline
from continuity import annotate_turns
from qa_preparacion import validate_continuity
from reviewed_continuity import load_reviewed_links, validate_reviewed_links
from reviewed_intrapara_continuity import (PATH, ALLOWED, RELATION, load_intrapara_links,
                                         matching_intrapara, validate_intrapara_links)
from compare_intrapara_release import compare, groups, BASELINE_SHA
from diagnosticar_finales import read_rows


def exported(rows):
    # openpyxl exporta las cadenas vacías de estas dos columnas como celdas nulas.
    # El gate de publicación compara XLSX contra XLSX sin normalizar ninguna celda.
    for row in rows:
        for field in ('ID_Antecedente_Continuidad', 'ID_Ancla_Actor'):
            if row[field] == '':
                row[field] = None
    return rows


class IntraparaContinuityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {int(r[0]): {'Fecha': builder.to_date_str(r[1]), 'Texto': str(r[5])} for r in builder.data}
        cls.package = json.loads(PATH.read_text())
        cls.intra = load_intrapara_links(cls.raw)
        cls.inter = load_reviewed_links(cls.raw)
        cls.before = read_rows(ROOT / 'data/processed/consolidado_base_referencia.xlsx')
        cls.after = exported(annotate_turns(copy.deepcopy(cls.before), cls.inter, cls.intra))

    def load_package(self, package, raw=None):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'proof.json'
            path.write_text(json.dumps(package))
            return load_intrapara_links(self.raw if raw is None else raw, path)

    def test_baseline_is_explicitly_loop32_byte_identical(self):
        path = ROOT / 'data/processed/consolidado_base_referencia.xlsx'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), BASELINE_SHA)

    def test_registry_closed_to_two_pairs(self):
        self.assertEqual(set(self.intra), set(ALLOWED))
        self.assertEqual(len(self.inter), 24)

    def test_source_complete_and_literal_intervals(self):
        for e in self.intra.values():
            self.assertEqual(e['Texto_Padre'], self.raw[e['ID_Padre']]['Texto'])
            for side in ['Anterior', 'Siguiente']:
                s = e[side]
                self.assertEqual(e['Texto_Padre'][s['Inicio']:s['Fin']], s['Texto'])
            self.assertFalse(e['Texto_Padre'][e['Anterior']['Fin']:e['Siguiente']['Inicio']].strip())

    def test_legacy_default_reproduces_all_rows(self):
        self.assertEqual(exported(annotate_turns(copy.deepcopy(self.before), self.inter)), self.before)

    def test_two_actual_relations_with_direct_antecedents(self):
        index = {r['ID_Intervencion']: r for r in self.after}
        self.assertEqual(sum(r['Relacion_Turno'] == RELATION for r in self.after), 2)
        for left, right in ALLOWED:
            a, b = index[left], index[right]
            self.assertEqual(a['ID_Turno'], b['ID_Turno'])
            self.assertEqual(b['ID_Antecedente_Continuidad'], left)
            self.assertIsNone(a['ID_Ancla_Actor'])
            self.assertEqual(b['ID_Ancla_Actor'], right)

    def test_global_partition_and_all_noncontinuity_cells(self):
        report = compare(self.before, self.after)
        self.assertEqual((report['Grupos_Antes'], report['Grupos_Despues']), (9257, 9255))
        self.assertEqual(len(report['Celdas_Relacionales_Modificadas']), 4)
        self.assertEqual(len(report['Filas_Con_Conjunto_De_Companeros_Distinto']), 5)
        self.assertEqual(report['Otros_Campos_Modificados'], 0)

    def test_marshall_keeps_full_2797_and_excludes_claro(self):
        rows = [r for r in self.after if r['ID_Padre'] in (2796, 2797)]
        self.assertEqual([len(r['Texto']) for r in rows], [5097, 343, 5287, 2105])
        self.assertEqual(len({r['ID_Turno'] for r in rows[1:]}), 1)
        self.assertNotEqual(rows[0]['ID_Turno'], rows[1]['ID_Turno'])
        self.assertIn('ALAR', rows[-1]['Texto'])
        self.assertEqual(rows[-1]['ID_Antecedente_Continuidad'], rows[-2]['ID_Intervencion'])
        self.assertEqual(rows[-1]['ID_Ancla_Actor'], rows[-1]['ID_Intervencion'])

    def test_de_ramon_excludes_president(self):
        rows = [r for r in self.after if r['ID_Padre'] == 3012]
        self.assertEqual([len(r['Texto']) for r in rows], [109, 375, 1867])
        self.assertNotEqual(rows[0]['ID_Turno'], rows[1]['ID_Turno'])
        self.assertEqual(rows[1]['ID_Turno'], rows[2]['ID_Turno'])
        self.assertEqual(rows[0]['Motivos_Revision'], 'FINAL_SIN_PUNTUACION')

    def test_controls_and_all_other_memberships_preserved(self):
        old = {r: g for g in groups(self.before) for r in g}
        new = {r: g for g in groups(self.after) for r in g}
        changed = {r for pair in ALLOWED for r in pair} | {'RPM-2009-11-12:2797:1'}
        self.assertEqual({rid for rid in old if old[rid] != new[rid]}, changed)
        for parent in (2685, 2885, 1901, 2779, 600, 601, 5402, 5403, 780, 2705, 2706):
            for r in self.before:
                if r['ID_Padre'] == parent:
                    self.assertEqual(old[r['ID_Intervencion']], new[r['ID_Intervencion']])

    def test_24_old_proofs_and_f1_pass(self):
        self.assertEqual(validate_reviewed_links(self.after, self.inter), [])
        self.assertEqual(validate_intrapara_links(self.after, self.intra), [])
        self.assertEqual(validate_continuity(self.after), [])

    def test_no_unregistered_intra_relation(self):
        self.assertTrue(validate_intrapara_links(self.after, {}))

    def test_unapplied_declared_proofs_fail(self):
        self.assertTrue(validate_intrapara_links(self.before, self.intra))

    def test_empty_missing_or_duplicate_registry_fails(self):
        for reviews in ([], self.package['Revisiones'][:1], self.package['Revisiones'] * 2):
            with self.subTest(n=len(reviews)):
                p = copy.deepcopy(self.package)
                p['Revisiones'] = reviews
                with self.assertRaises(ValueError):
                    self.load_package(p)

    def test_wrong_scope_or_version_fails(self):
        for field, value in [('Alcance', 'SIMULACION_SIN_APLICAR'), ('Version', 2), ('Version', True)]:
            p = copy.deepcopy(self.package)
            p[field] = value
            with self.assertRaises(ValueError):
                self.load_package(p)

    def test_incomplete_package_fails(self):
        for field in self.package['Revisiones'][0]:
            p = copy.deepcopy(self.package)
            del p['Revisiones'][0][field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.load_package(p)

    def test_source_mutations_fail(self):
        for field, value in [('Texto_Padre', 'otro'), ('SHA256_Texto_Padre', '0'*64),
                             ('Fecha', '2000-01-01'), ('Actor', 'Otra persona'), ('ID_Padre', 2685),
                             ('Justificacion', ''), ('Limitacion', ''), ('Evidencia', [])]:
            p = copy.deepcopy(self.package)
            p['Revisiones'][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.load_package(p)

    def test_changed_raw_source_fails(self):
        raw = copy.deepcopy(self.raw)
        raw[2796]['Texto'] += ' '
        with self.assertRaises(ValueError):
            self.load_package(self.package, raw)

    def test_interval_mutations_fail(self):
        for side in ('Anterior', 'Siguiente'):
            for field, value in [('Inicio', -1), ('Fin', 999999), ('Inicio', True),
                                 ('Texto', 'otro'), ('Fuente_Actor', 'CONTINUIDAD_PARRAFO'),
                                 ('ID_Intervencion', 'RPM-2009-11-12:2685:3')]:
                p = copy.deepcopy(self.package)
                p['Revisiones'][0][side][field] = value
                with self.subTest(side=side, field=field), self.assertRaises(ValueError):
                    self.load_package(p)

    def test_intervals_cannot_expand_into_whitespace(self):
        p = copy.deepcopy(self.package)
        p['Revisiones'][0]['Siguiente']['Inicio'] -= 1
        with self.assertRaises(ValueError):
            self.load_package(p)

    def test_extra_actor_or_institutional_barrier_cannot_match(self):
        by_id = {r['ID_Intervencion']: r for r in self.before}
        left, right = next(iter(ALLOWED))
        for side in ('left', 'right'):
            for field, value in [('Actor_Final', builder.CONSEJO), ('Fecha', '2000-01-01'),
                                 ('ID_Padre', 2797), ('Tipo_Acta', 'ACTA'),
                                 ('Motivos_Revision', 'FINAL_SIN_PUNTUACION'), ('Texto', 'otro')]:
                a, b = copy.deepcopy(by_id[left]), copy.deepcopy(by_id[right])
                (a if side == 'left' else b)[field] = value
                with self.subTest(side=side, field=field):
                    self.assertIsNone(matching_intrapara(a, b, self.intra))

    def test_left_context_cannot_be_promoted_to_anchor(self):
        rows = copy.deepcopy(self.after)
        left, right = next(iter(ALLOWED))
        next(r for r in rows if r['ID_Intervencion'] == left)['ID_Ancla_Actor'] = left
        self.assertTrue(validate_intrapara_links(rows, self.intra))
        self.assertTrue(validate_continuity(rows))

    def test_wrong_relation_antecedent_or_right_anchor_fails(self):
        right = next(iter(ALLOWED))[1]
        for field in ('Relacion_Turno', 'ID_Antecedente_Continuidad', 'ID_Ancla_Actor', 'ID_Turno'):
            rows = copy.deepcopy(self.after)
            next(r for r in rows if r['ID_Intervencion'] == right)[field] = 'incorrecto'
            with self.subTest(field=field):
                self.assertTrue(validate_intrapara_links(rows, self.intra))

    def test_missing_or_nonadjacent_endpoint_fails(self):
        left, right = next(iter(ALLOWED))
        rows = [r for r in self.after if r['ID_Intervencion'] != left]
        self.assertTrue(validate_intrapara_links(rows, self.intra))
        rows = copy.deepcopy(self.after)
        pos = next(i for i, r in enumerate(rows) if r['ID_Intervencion'] == right)
        rows[pos], rows[pos+1] = rows[pos+1], rows[pos]
        self.assertTrue(validate_intrapara_links(rows, self.intra))

    def test_global_gate_rejects_any_text_or_warning_change(self):
        for field in ('Texto', 'Actor_Final', 'Rol_Final', 'Motivos_Revision', 'ID_Ancla_Actor'):
            rows = copy.deepcopy(self.after)
            rows[0][field] = 'alterado'
            with self.subTest(field=field), self.assertRaises(ValueError):
                compare(self.before, rows)

    def test_global_gate_rejects_extra_merge(self):
        rows = copy.deepcopy(self.after)
        rows[1]['ID_Turno'] = rows[0]['ID_Turno']
        with self.assertRaises(ValueError):
            compare(self.before, rows)

    def test_global_gate_rejects_lost_inherited_2797(self):
        rows = copy.deepcopy(self.after)
        next(r for r in rows if r['ID_Padre'] == 2797)['ID_Turno'] = 'nuevo'
        with self.assertRaises(ValueError):
            compare(self.before, rows)

    def test_global_gate_rejects_missing_rows_or_columns(self):
        with self.assertRaises(ValueError):
            compare(self.before, self.after[:-1])
        rows = copy.deepcopy(self.after)
        del rows[0]['Texto']
        with self.assertRaises(ValueError):
            compare(self.before, rows)


class VersionedPipelineTests(unittest.TestCase):
    def test_historical_or_source_destinations_rejected(self):
        for name in ('data/processed', 'data/raw/new', 'data/curation/new', '.git/new', 'docs/new', '.cache', 'data/releases'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                pipeline.release_target(ROOT / name)

    def test_existing_destination_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as temp:
            with self.assertRaises(ValueError):
                pipeline.release_target(Path(temp))

    def test_new_staging_destination_accepted(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as temp:
            path = Path(temp) / 'new'
            self.assertEqual(pipeline.release_target(path), path.resolve())

    def test_failed_gate_never_publishes(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as temp:
            dest = Path(temp) / 'release'
            with patch.object(pipeline.subprocess, 'run', side_effect=RuntimeError('gate falló')):
                with self.assertRaises(RuntimeError):
                    pipeline.main(['--perfil', 'intrapadre-v1', '--destino', str(dest)])
            self.assertFalse(dest.exists())

    def test_profile_is_explicit_and_legacy_ignores_ambient_intra(self):
        with patch.dict(os.environ, {'NLM_INTRAPARA_REVIEWS': 'no-autorizado'}):
            with patch.object(pipeline.subprocess, 'run', side_effect=RuntimeError('stop')) as run:
                with self.assertRaises(RuntimeError):
                    pipeline.main(['--perfil', 'legacy'])
                self.assertNotIn('NLM_INTRAPARA_REVIEWS', run.call_args.kwargs['env'])

    def test_default_profile_is_versioned_not_historical(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as temp:
            dest = Path(temp) / 'new'
            with patch.object(pipeline.subprocess, 'run', side_effect=RuntimeError('stop')) as run:
                with self.assertRaises(RuntimeError):
                    pipeline.main(['--destino', str(dest)])
                self.assertEqual(run.call_args.kwargs['env']['NLM_INTRAPARA_REVIEWS'], str(PATH))
                self.assertFalse(dest.exists())

    def test_versioned_profile_passes_registry_to_real_build(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as temp:
            dest = Path(temp) / 'new'
            with patch.object(pipeline.subprocess, 'run', side_effect=RuntimeError('stop')) as run:
                with self.assertRaises(RuntimeError):
                    pipeline.main(['--perfil', 'intrapadre-v1', '--destino', str(dest)])
                self.assertEqual(run.call_args.kwargs['env']['NLM_INTRAPARA_REVIEWS'], str(PATH))


if __name__ == '__main__':
    unittest.main()
