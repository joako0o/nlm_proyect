"""Refinamiento funcional v5: veintinueve constancias, mismo criterio que v4.

Verifica que el registro derive de la lectura lote8, que el corte conserve el
texto, que el antecedente sea la última fila del padre anterior y que el gate
produzca exactamente veintinueve filas nuevas sin cerrar ninguna alerta.
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
import build_base_referencia as b
import preparar_data as pipeline
import functional_refinements as f4
import functional_refinements_v5 as f5
from compare_functional_v7 import compare, expected_rows, members
from diagnosticar_finales import read_rows
from institutional_reviews import load_institutional_reviews
from intrapara_profiles import required_intrapara


class FunctionalV5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {int(r[0]): {'Fecha': b.to_date_str(r[1]), 'Texto': str(r[5])} for r in b.data}
        cls.readings = json.loads(f5.READINGS.read_text())
        cls.reviews = f5.load_refinements(cls.raw)
        cls.before = read_rows(f5.BASE)
        cls.after, cls.lineage = expected_rows(cls.before, cls.reviews, cls.raw)
        cls.by_id = {r['ID_Intervencion']: r for r in cls.before}

    # ---------- registro y evidencia ----------
    def test_registry_covers_exactly_the_29_and_pins_its_sources(self):
        self.assertEqual(len(self.reviews), 29)
        self.assertEqual(sorted(self.reviews), sorted(f5.PARENTS))
        pkg = json.loads(f5.PATH.read_text())
        self.assertEqual(pkg['Version'], 5)
        self.assertEqual(pkg['Perfil'], 'funcional-v5')
        self.assertEqual(pkg['SHA256_Lecturas_Lote8'], f5.file_sha(f5.READINGS))
        self.assertEqual(pkg['SHA256_Base'], f5.BASE_SHA)
        self.assertEqual(f5.file_sha(f5.BASE), f5.BASE_SHA)
        self.assertEqual(pkg['SHA256_Registro_Funcional_V4'], f5.file_sha(f5.V4_PATH))
        self.assertEqual(f5.file_sha(f5.V4_PATH), f5.V4_SHA)

    def test_v5_does_not_touch_the_v4_registry_or_its_parents(self):
        self.assertFalse(set(f5.PARENTS) & f4.PARENTS)
        self.assertEqual(f5.file_sha(f5.V4_PATH), f5.V4_SHA)
        self.assertEqual(len(f4.load_refinements(self.raw)), 3)

    def test_registry_rejects_a_changed_version_or_missing_parent(self):
        pkg = json.loads(f5.PATH.read_text())
        with tempfile.TemporaryDirectory() as tmp:
            for mutate in (lambda p: p.update(Version=4),
                           lambda p: p.update(Perfil='funcional-v4'),
                           lambda p: p['Revisiones'].pop('4973'),
                           lambda p: p.update(SHA256_Base='0' * 64),
                           lambda p: p.update(SHA256_Lecturas_Lote8='0' * 64),
                           lambda p: p.update(SHA256_Registro_Funcional_V4='0' * 64)):
                broken = copy.deepcopy(pkg)
                mutate(broken)
                path = Path(tmp) / 'roto.json'
                path.write_text(json.dumps(broken, ensure_ascii=False))
                with self.assertRaises(ValueError):
                    f5.load_refinements(self.raw, path)

    def test_a_modified_entry_is_rejected(self):
        pkg = json.loads(f5.PATH.read_text())
        with tempfile.TemporaryDirectory() as tmp:
            for key in ('Texto_Personal', 'Texto_Constancia', 'Separador', 'Actor',
                        'Fuente_Actor', 'Tipo_Constancia', 'ID_Anterior', 'Revision_ID',
                        'Justificacion', 'SHA256_Texto_Padre'):
                broken = copy.deepcopy(pkg)
                broken['Revisiones']['4973'][key] = 'alterado'
                path = Path(tmp) / f'roto_{key}.json'
                path.write_text(json.dumps(broken, ensure_ascii=False))
                with self.assertRaises(ValueError, msg=key):
                    f5.load_refinements(self.raw, path)

    # ---------- la lectura debe seguir siendo cierta ----------
    def test_cut_conserves_the_text_and_ends_a_sentence(self):
        for p, e in self.reviews.items():
            self.assertEqual(e['Texto_Personal'] + e['Separador'] + e['Texto_Constancia'],
                             e['Texto_Original'])
            self.assertTrue(e['Separador'].isspace())
            self.assertTrue(e['Texto_Personal'].rstrip().endswith('.'))
            self.assertEqual(e['Corte'], len(e['Texto_Personal']))
            self.assertEqual(self.by_id[e['ID_Fila_Original']]['Texto'], e['Texto_Original'])

    def test_antecedent_is_the_last_row_of_the_previous_parent(self):
        by_parent = {}
        for r in self.before:
            by_parent.setdefault(r['ID_Padre'], []).append(r)
        for p, e in self.reviews.items():
            ultimo = by_parent[p - 1][-1]
            self.assertEqual(ultimo['ID_Intervencion'], e['ID_Anterior'])
            self.assertEqual(ultimo['Actor_Final'], e['Actor'])
            self.assertFalse(ultimo['Tipo_Acta'])
            self.assertFalse(ultimo['Motivos_Revision'])
            self.assertEqual(ultimo['ID_Ancla_Actor'], ultimo['ID_Intervencion'])

    def test_reading_revalidation_rejects_a_corrupted_cut(self):
        roto = copy.deepcopy(self.readings)
        caso = roto['Casos'][self.reviews[4973]['ID_Fila_Original']]
        caso['Texto_Constancia'] = caso['Texto_Constancia'] + ' agregado'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'lecturas.json'
            path.write_text(json.dumps(roto, ensure_ascii=False))
            with patch.object(f5, 'READINGS', path):
                with self.assertRaises(ValueError):
                    f5.load_refinements(self.raw)

    def test_reading_revalidation_rejects_a_moved_antecedent(self):
        roto = copy.deepcopy(self.readings)
        caso = roto['Casos'][self.reviews[4973]['ID_Fila_Original']]
        caso['ID_Anterior'] = 'RPM-2012-07-12:4972:9'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'lecturas.json'
            path.write_text(json.dumps(roto, ensure_ascii=False))
            with patch.object(f5, 'READINGS', path):
                with self.assertRaises(ValueError):
                    f5.load_refinements(self.raw)

    # ---------- comportamiento del corte ----------
    def test_refine_segments_splits_and_guards_the_partition(self):
        for p, e in self.reviews.items():
            legacy = [(e['Texto_Original'], e['Actor'], e['Fuente_Actor'])]
            parts = f5.refine_segments(p, legacy, self.reviews)
            self.assertEqual([t for t, _, _ in parts],
                             [e['Texto_Personal'], e['Texto_Constancia']])
            self.assertTrue(all(a == e['Actor'] and f == e['Fuente_Actor'] for _, a, f in parts))
            with self.assertRaises(ValueError):
                f5.refine_segments(p, parts, self.reviews)
        self.assertIs(f5.refine_segments(4973, legacy, {}), legacy)
        self.assertIs(f5.refine_segments(4333, legacy, self.reviews), legacy)

    def test_the_29_have_no_institutional_revision_to_rebuild(self):
        antiguas = json.loads((ROOT / 'data/curation/revisiones_continuaciones_acta.json').read_text())
        self.assertFalse({e['ID_Padre'] for e in antiguas} & set(f5.PARENTS))
        self.assertEqual(load_institutional_reviews(self.raw).keys() & set(f5.PARENTS), set())

    def test_constancia_keeps_the_council_type_and_the_speaker(self):
        for p, e in self.reviews.items():
            self.assertEqual(e['Tipo_Personal'], '')
            self.assertEqual(e['Tipo_Constancia'], 'ACUERDO_CONSEJO')
            self.assertEqual(self.by_id[e['ID_Fila_Original']]['Tipo_Acta'], 'ACUERDO_CONSEJO')

    # ---------- gate ----------
    def test_gate_adds_exactly_29_rows_and_keeps_every_group(self):
        self.assertEqual(len(self.after), len(self.before) + 29)
        self.assertEqual(len(self.lineage), len(self.after))
        self.assertEqual(len(members(self.before)), len(members(self.after)))
        partes = [r for r in self.after if r['ID_Padre'] == 4973]
        self.assertEqual(len(partes), 3)

    def test_gate_validation_passes_and_catches_tampering(self):
        self.assertEqual(f5.validate_refinements(self.after, self.reviews), [])
        for campo, valor in [('Tipo_Acta', 'ACUERDO_CONSEJO'),
                             ('Relacion_Turno', 'INSTITUCIONAL'),
                             ('ID_Ancla_Actor', None)]:
            roto = copy.deepcopy(self.after)
            objetivo = next(r for r in roto
                            if r['ID_Intervencion'] == self.reviews[4973]['ID_Fila_Original'])
            objetivo[campo] = valor
            self.assertTrue(f5.validate_refinements(roto, self.reviews), campo)

    def test_gate_never_closes_an_alert_and_reports_the_new_duplicates(self):
        report, _ = compare(self.before, self.after, self.reviews)
        self.assertTrue(report['Pasa'])
        self.assertEqual(report['Alertas_Cerradas'], 0)
        self.assertEqual(report['Alertas_Antes'], 467)
        self.assertEqual(report['Alertas_Despues'], 484)
        self.assertEqual(len(report['Alertas_Nuevas']), 17)
        for rid in report['Alertas_Nuevas']:
            fila = next(r for r in self.after if r['ID_Intervencion'] == rid)
            self.assertEqual(fila['Motivos_Revision'], 'DUPLICADO_NO_FORMULA')
            self.assertEqual(fila['Duplicado_Exacto'], 'SI')

    def test_no_alert_disappears_from_the_baseline(self):
        antes = {r['ID_Intervencion']: r['Motivos_Revision'] for r in self.before
                 if r['Motivos_Revision']}
        despues = {r['ID_Intervencion']: r['Motivos_Revision'] for r in self.after
                   if r['Motivos_Revision']}
        for rid, motivo in antes.items():
            if rid in despues:
                self.assertEqual(despues[rid], motivo, rid)

    # ---------- activación ----------
    def test_active_refinements_requires_the_profile_and_the_v4_registry(self):
        # Entornos explícitos: este test no puede depender de variables heredadas.
        intra_v4 = str(ROOT / 'data/curation/continuidades_intrapadre_v4.json')
        intra_v3 = str(ROOT / 'data/curation/continuidades_intrapadre_v3.json')
        valido = {'NLM_FUNCTIONAL_V5_REVIEWS': str(f5.PATH), 'NLM_INTRAPARA_REVIEWS': intra_v4,
                  'NLM_FUNCTIONAL_REVIEWS': str(f4.PATH),
                  'NLM_PERFIL_CONSTRUCCION': 'procedimental-v7'}
        rotos = [
            dict(valido, NLM_FUNCTIONAL_V5_REVIEWS=''),
            dict(valido, NLM_PERFIL_CONSTRUCCION='procedimental-v5'),
            dict(valido, NLM_PERFIL_CONSTRUCCION='procedimental-v6',
                 NLM_INTRAPARA_REVIEWS=intra_v3),
            dict(valido, NLM_INTRAPARA_REVIEWS=intra_v3),
            dict(valido, NLM_INTRAPARA_REVIEWS=''),
            dict(valido, NLM_FUNCTIONAL_REVIEWS='no-autorizado'),
            dict(valido, NLM_FUNCTIONAL_REVIEWS=''),
        ]
        for env in rotos:
            with patch.dict(os.environ, env, clear=True):
                if env['NLM_FUNCTIONAL_V5_REVIEWS']:
                    with self.assertRaises(ValueError, msg=str(env)):
                        f5.active_refinements(self.raw)
                else:
                    self.assertEqual(f5.active_refinements(self.raw), {})
        with patch.dict(os.environ, valido, clear=True):
            self.assertEqual(len(f5.active_refinements(self.raw)), 29)

    def test_profile_v7_is_wired_without_changing_the_default(self):
        self.assertEqual(required_intrapara('procedimental-v7'), 'intrapadre-v4')
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as temp:
            dest = Path(temp) / 'nueva'
            with patch.object(pipeline.subprocess, 'run', side_effect=RuntimeError('stop')) as run:
                with self.assertRaises(RuntimeError):
                    pipeline.main(['--perfil', 'procedimental-v7', '--destino', str(dest)])
                env = run.call_args.kwargs['env']
                self.assertEqual(env['NLM_FUNCTIONAL_V5_REVIEWS'], str(f5.PATH))
                self.assertEqual(env['NLM_FUNCTIONAL_REVIEWS'], str(f4.PATH))
                self.assertEqual(env['NLM_PROCEDURAL_REVIEWS'],
                                 str(ROOT / 'data/curation/continuidades_procedimentales_v5.json'))
                self.assertEqual(env['NLM_INTRAPARA_REVIEWS'],
                                 str(ROOT / 'data/curation/continuidades_intrapadre_v4.json'))
                self.assertEqual(env['NLM_PERFIL_CONSTRUCCION'], 'procedimental-v7')
                self.assertFalse(dest.exists())
            # El perfil predeterminado sigue siendo v5 y no activa el registro v5.
            with patch.object(pipeline.subprocess, 'run', side_effect=RuntimeError('stop')) as run:
                with self.assertRaises(RuntimeError):
                    pipeline.main(['--destino', str(dest)])
                env = run.call_args.kwargs['env']
                self.assertEqual(env['NLM_PERFIL_CONSTRUCCION'], 'procedimental-v5')
                self.assertNotIn('NLM_FUNCTIONAL_V5_REVIEWS', env)


if __name__ == '__main__':
    unittest.main()
