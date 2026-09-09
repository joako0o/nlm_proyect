"""Lote6 aplicado: dos enlaces intrapadre; v1-v3, v4 funcional, v5 y reservas intactos."""
import collections
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
from continuity import annotate_turns
from reviewed_continuity import load_reviewed_links, validate_reviewed_links
from reviewed_intrapara_continuity import validate_intrapara_links, RELATION
from reviewed_intrapara_v3 import load_v3, selection
from reviewed_intrapara_v4 import (load_v4, validate_readings, BASE, BASE_SHA, PATH, READINGS,
                                   NEW_PAIRS, DECISIONES_LOTE6, RESERVAS_ABIERTAS, PARENTS,
                                   ALLOWED, check_sources)
from reviewed_procedural_v5 import (BASE as V4_BASE, PATH as V5_PATH, PAIRS as V5_PAIRS,
                                    load_reviews, apply_reviews)
from compare_intrapara_release import compare, groups
from compare_procedural_v6 import members, GRUPOS_V5, GRUPOS_V6, ALERTAS_V5
from diagnosticar_finales import read_rows
from intrapara_profiles import profile_name, load_intrapara_links, required_intrapara
from qa_preparacion import validate_continuity

V3_PATH = ROOT / 'data/curation/continuidades_intrapadre_v3.json'


def exported(rows):
    for r in rows:
        for f in ('ID_Ancla_Actor', 'ID_Antecedente_Continuidad'):
            if r[f] == '':
                r[f] = None
    return rows


class IntraparaV4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {int(r[0]): {'Fecha': b.to_date_str(r[1]), 'Texto': str(r[5])} for r in b.data}
        cls.v5 = read_rows(BASE)
        cls.v4 = read_rows(V4_BASE)
        cls.pkg = json.loads(PATH.read_text())
        cls.readings = json.loads(READINGS.read_text())
        cls.intra = load_v4(cls.raw)
        cls.prior = load_v3(cls.raw)
        cls.inter = load_reviewed_links(cls.raw)
        cls.procedural = load_reviews(cls.raw)
        cls.after = exported(apply_reviews(
            annotate_turns(copy.deepcopy(cls.v4), cls.inter, cls.intra), cls.procedural))
        cls.by_id = {r['ID_Intervencion']: r for r in cls.after}

    def load(self, pkg, loader=load_v4):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / 'proof.json'
            p.write_text(json.dumps(pkg))
            return loader(self.raw, p)

    def compare(self, rows):
        return compare(self.v5, rows, pairs=sorted(NEW_PAIRS),
                       profile='intrapadre-v4', baseline='procedimental-v5')

    # --- baseline y alcance -------------------------------------------------
    def test_v5_baseline_is_frozen(self):
        self.assertEqual(hashlib.sha256(BASE.read_bytes()).hexdigest(), BASE_SHA)
        self.assertEqual(len(self.v5), 9694)
        self.assertEqual(len(groups(self.v5)), GRUPOS_V5)

    def test_profile_and_accumulated_pairs(self):
        self.assertEqual(profile_name(PATH), 'intrapadre-v4')
        self.assertEqual(profile_name(V3_PATH), 'intrapadre-v3')
        self.assertEqual(len(self.intra), 17)
        self.assertEqual(set(ALLOWED), set(self.intra))
        self.assertEqual(required_intrapara('procedimental-v6'), 'intrapadre-v4')
        self.assertEqual(required_intrapara('procedimental-v5'), 'intrapadre-v3')
        self.assertEqual(required_intrapara('funcional-v4'), 'intrapadre-v3')
        with self.assertRaises(ValueError):
            required_intrapara('procedimental-v7')

    def test_selection_on_v5_is_exactly_the_lote6_cases(self):
        self.assertEqual(len(selection(self.v5)), 5)
        self.assertEqual({e['Izquierda'] for e in selection(self.v5)}, set(DECISIONES_LOTE6))

    def test_engine_still_reproduces_v4_with_v3_links(self):
        actual = exported(annotate_turns(copy.deepcopy(self.v4), self.inter, self.prior))
        self.assertEqual(actual, self.v4)

    def test_previous_fifteen_proofs_are_untouched(self):
        for key, evidence in self.prior.items():
            self.assertEqual(self.intra[key], evidence)

    def test_new_pairs_are_bounded_and_contiguous(self):
        for (left, right), (padre, fecha, actor) in NEW_PAIRS.items():
            e = self.intra[(left, right)]
            text = self.raw[padre]['Texto']
            self.assertEqual((e['ID_Padre'], e['Fecha'], e['Actor']), (padre, fecha, actor))
            self.assertEqual(text[e['Anterior']['Inicio']:e['Anterior']['Fin']], e['Anterior']['Texto'])
            self.assertEqual(text[e['Siguiente']['Inicio']:e['Siguiente']['Fin']], e['Siguiente']['Texto'])
            self.assertEqual(''.join(text[e['Anterior']['Fin']:e['Siguiente']['Inicio']].split()), '')
            self.assertEqual(e['Anterior']['Fuente_Actor'], 'CONTEXTO_REVISADO')
            self.assertEqual(e['Siguiente']['Fuente_Actor'], 'SUJETO_NOMBRE')
            self.assertEqual(e['Evidencia'], [e['Anterior']['Texto'], e['Siguiente']['Texto']])
            self.assertEqual(e['Justificacion'], self.readings['Casos'][left]['Justificacion'])

    # --- efecto productivo --------------------------------------------------
    def test_global_partition_admits_only_the_two_unions(self):
        report = self.compare(self.after)
        self.assertTrue(report['Pasa'])
        self.assertEqual(report['Grupos_Antes'], GRUPOS_V5)
        self.assertEqual(report['Grupos_Despues'], GRUPOS_V6)
        self.assertEqual(report['Alertas_Antes'], ALERTAS_V5)
        self.assertEqual(report['Alertas_Despues'], ALERTAS_V5)
        self.assertEqual(report['Otros_Campos_Modificados'], 0)
        self.assertEqual(report['Grupos_Previos_Divididos'], 0)
        self.assertEqual(len(report['Celdas_Relacionales_Modificadas']), 4)
        self.assertEqual(len(groups(self.after)), GRUPOS_V6)

    def test_soto_group_has_three_members_and_keeps_the_prior_continuity(self):
        grupo = members(self.after)['RPM-2010-01-14:2863:2']
        self.assertEqual(set(grupo), {'RPM-2010-01-14:2863:2', 'RPM-2010-01-14:2863:3',
                                      'RPM-2010-01-14:2864:1'})
        self.assertEqual(sum(len(self.by_id[r]['Texto']) for r in grupo), 1497)
        self.assertEqual(self.by_id['RPM-2010-01-14:2864:1']['Relacion_Turno'], 'CONTINUIDAD_EXPLICITA')
        self.assertEqual(self.by_id['RPM-2010-01-14:2864:1']['ID_Antecedente_Continuidad'],
                         'RPM-2010-01-14:2863:3')

    def test_lehmann_group_has_two_members(self):
        grupo = members(self.after)['RPM-2011-01-13:3646:2']
        self.assertEqual(set(grupo), {'RPM-2011-01-13:3646:2', 'RPM-2011-01-13:3646:3'})
        self.assertEqual(sum(len(self.by_id[r]['Texto']) for r in grupo), 1252)

    def test_applied_links_carry_the_reviewed_relation(self):
        for left, right in NEW_PAIRS:
            row = self.by_id[right]
            self.assertEqual(row['Relacion_Turno'], RELATION)
            self.assertEqual(row['ID_Antecedente_Continuidad'], left)
            self.assertEqual(row['ID_Turno'], self.by_id[left]['ID_Turno'])
            self.assertEqual(row['ID_Ancla_Actor'], right)
        self.assertEqual(sum(1 for r in self.after if r['Relacion_Turno'] == RELATION), 17)

    def test_left_endpoints_keep_null_anchor_and_contextual_source(self):
        """CONTEXTO_REVISADO no se convierte en ancla por agrupar."""
        for left, _ in NEW_PAIRS:
            row = self.by_id[left]
            self.assertIsNone(row['ID_Ancla_Actor'])
            self.assertEqual(row['Fuente_Actor'], 'CONTEXTO_REVISADO')
            self.assertIsNone(row['ID_Antecedente_Continuidad'])
        self.assertEqual(sum(1 for r in self.after if r['Fuente_Actor'] == 'CONTEXTO_REVISADO'),
                         sum(1 for r in self.v5 if r['Fuente_Actor'] == 'CONTEXTO_REVISADO'))

    def test_marfan_question_and_claro_interventions_stay_separate(self):
        for rid in ('RPM-2010-01-14:2863:1', 'RPM-2011-01-13:3646:1', 'RPM-2011-01-13:3646:4'):
            self.assertEqual(len(members(self.after)[rid]), 1)

    def test_three_reservations_remain_open(self):
        for left in RESERVAS_ABIERTAS:
            right = DECISIONES_LOTE6[left][0]
            self.assertNotEqual(members(self.after)[left], members(self.after)[right])
            self.assertEqual(self.by_id[right]['Relacion_Turno'], 'INICIO_EXPLICITO')
            self.assertIsNone(self.by_id[left]['ID_Ancla_Actor'])
        self.assertEqual(len(selection(self.after)), 3)
        self.assertEqual({e['Izquierda'] for e in selection(self.after)}, set(RESERVAS_ABIERTAS))

    def test_six_procedural_links_survive(self):
        for left, right in V5_PAIRS:
            self.assertEqual(members(self.after)[left], members(self.after)[right])
            self.assertEqual(self.by_id[right]['Relacion_Turno'], 'CONTINUIDAD_PROCEDIMENTAL_REVISADA')

    def test_no_text_actor_or_alert_was_touched(self):
        before = {r['ID_Intervencion']: r for r in self.v5}
        for rid, row in self.by_id.items():
            for field in row:
                if field in ('ID_Turno', 'Relacion_Turno', 'ID_Antecedente_Continuidad'):
                    continue
                self.assertEqual(row[field], before[rid][field], f'{rid}/{field}')
        self.assertEqual(sum(1 for r in self.after if r['Motivos_Revision']), ALERTAS_V5)

    def test_validators_accept_the_result(self):
        self.assertEqual(validate_reviewed_links(self.after, self.inter), [])
        self.assertEqual(validate_intrapara_links(self.after, self.intra), [])
        self.assertEqual(validate_continuity(self.after, self.procedural), [])

    # --- endurecimiento del registro ---------------------------------------
    def test_package_metadata_is_pinned(self):
        self.assertEqual(self.pkg['Version'], 4)
        self.assertEqual(self.pkg['Alcance'], 'CONTINUIDAD_INTRAPADRE_V4')
        self.assertEqual(len(self.pkg['Revisiones']), 17)
        old = json.loads(V3_PATH.read_text())
        for key in ('Lecturas_Lote2', 'SHA256_Lecturas_Lote2', 'Lecturas_Lote3',
                    'SHA256_Lecturas_Lote3', 'SHA256_Registro_V2'):
            self.assertEqual(self.pkg[key], old[key])
        self.assertEqual(self.pkg['SHA256_Registro_V3'], hashlib.sha256(V3_PATH.read_bytes()).hexdigest())
        self.assertEqual(self.pkg['Lecturas_Lote6'], 'docs/continuidad_lote6_2026-09-09/lecturas.json')
        self.assertEqual(self.pkg['SHA256_Lecturas_Lote6'],
                         hashlib.sha256(READINGS.read_bytes()).hexdigest())

    def test_rejects_metadata_tampering(self):
        for mutation in ({'Version': 3}, {'Alcance': 'CONTINUIDAD_INTRAPADRE_V3'},
                         {'SHA256_Registro_V3': '0'*64}, {'Lecturas_Lote6': 'docs/otro.json'},
                         {'SHA256_Lecturas_Lote6': '0'*64}, {'Lecturas_Lote3': 'docs/otro.json'}):
            pkg = {**self.pkg, **mutation}
            with self.subTest(mutation=list(mutation)[0]), self.assertRaises(ValueError):
                self.load(pkg)

    def test_rejects_missing_or_extra_proofs(self):
        pkg = copy.deepcopy(self.pkg)
        pkg['Revisiones'] = [e for e in pkg['Revisiones']
                             if e['Anterior']['ID_Intervencion'] != 'RPM-2010-01-14:2863:2']
        with self.assertRaises(ValueError):
            self.load(pkg)
        extra = copy.deepcopy(pkg['Revisiones'][-1])
        extra['Revision_ID'] = 'CONT-INTRA-EXTRA'
        extra['Anterior'] = {**extra['Anterior'], 'ID_Intervencion': 'RPM-2010-01-14:2864:1'}
        extra['Siguiente'] = {**extra['Siguiente'], 'ID_Intervencion': 'RPM-2010-01-14:2865:1'}
        pkg = {**self.pkg, 'Revisiones': [*self.pkg['Revisiones'], extra]}
        with self.assertRaises(ValueError):
            self.load(pkg)

    def test_rejects_modified_intervals_and_evidence(self):
        for field, side in [('Inicio', 'Anterior'), ('Fin', 'Anterior'), ('Texto', 'Siguiente'),
                            ('Fuente_Actor', 'Anterior')]:
            pkg = copy.deepcopy(self.pkg)
            for e in pkg['Revisiones']:
                if e['Anterior']['ID_Intervencion'] == 'RPM-2011-01-13:3646:2':
                    e[side][field] = (e[side][field] + 1) if field in ('Inicio', 'Fin') else 'otro'
            with self.subTest(campo=f'{side}.{field}'), self.assertRaises(ValueError):
                self.load(pkg)

    def test_rejects_justification_detached_from_the_reading(self):
        pkg = copy.deepcopy(self.pkg)
        for e in pkg['Revisiones']:
            if e['Anterior']['ID_Intervencion'] == 'RPM-2010-01-14:2863:2':
                e['Justificacion'] = 'Otra justificación.'
        with self.assertRaises(ValueError):
            self.load(pkg)

    def test_rejects_previous_proof_rewritten(self):
        pkg = copy.deepcopy(self.pkg)
        pkg['Revisiones'][0]['Limitacion'] = 'Límite ampliado retrospectivamente.'
        with self.assertRaises(ValueError):
            self.load(pkg)

    def test_rejects_reading_tampering(self):
        for key, value in [('Version', 2), ('Alcance', 'OTRO'), ('SHA256_Grupos', '0'*64)]:
            readings = {**self.readings, key: value}
            with self.subTest(campo=key), self.assertRaises(ValueError):
                validate_readings(self.v5, readings, self.raw)
        readings = copy.deepcopy(self.readings)
        readings['Casos']['RPM-2010-01-14:2863:2']['Aplicado'] = True
        with self.assertRaises(ValueError):
            validate_readings(self.v5, readings, self.raw)
        readings = copy.deepcopy(self.readings)
        readings['Padres']['2863']['Texto_Padre'] += ' agregado'
        with self.assertRaises(ValueError):
            validate_readings(self.v5, readings, self.raw)
        readings = copy.deepcopy(self.readings)
        del readings['Padres']['2864']
        with self.assertRaises(ValueError):
            validate_readings(self.v5, readings, self.raw)

    def test_source_hashes_are_checked_and_restricted(self):
        check_sources(self.readings)
        pkg = copy.deepcopy(self.readings)
        pkg['SHA256_Fuentes'] = dict(pkg['SHA256_Fuentes'])
        key = 'data/raw/consolidado_final.xlsx'
        pkg['SHA256_Fuentes'][key] = '0'*64
        with self.assertRaises(ValueError):
            check_sources(pkg)
        pkg['SHA256_Fuentes'][key] = self.readings['SHA256_Fuentes'][key]
        pkg['SHA256_Fuentes']['scripts/preparar_data.py'] = '0'*64
        with self.assertRaises(ValueError):
            check_sources(pkg)

    # --- pipeline -----------------------------------------------------------
    def test_v6_profile_passes_the_v4_registry(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as tmp:
            dest = Path(tmp) / 'new'
            with patch.object(pipeline.subprocess, 'run', side_effect=RuntimeError('stop')) as run:
                with self.assertRaises(RuntimeError):
                    pipeline.main(['--perfil', 'procedimental-v6', '--destino', str(dest)])
                env = run.call_args.kwargs['env']
                self.assertEqual(env['NLM_INTRAPARA_REVIEWS'], str(PATH))
                self.assertEqual(env['NLM_FUNCTIONAL_REVIEWS'],
                                 str(ROOT / 'data/curation/refinamiento_funcional_v4.json'))
                self.assertEqual(env['NLM_PROCEDURAL_REVIEWS'], str(V5_PATH))
                self.assertEqual(env['NLM_PERFIL_CONSTRUCCION'], 'procedimental-v6')
                self.assertFalse(dest.exists())

    def test_default_profile_still_uses_v3_and_v5(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as tmp:
            dest = Path(tmp) / 'new'
            with patch.object(pipeline.subprocess, 'run', side_effect=RuntimeError('stop')) as run:
                with self.assertRaises(RuntimeError):
                    pipeline.main(['--destino', str(dest)])
                self.assertEqual(run.call_args.kwargs['env']['NLM_INTRAPARA_REVIEWS'], str(V3_PATH))
                self.assertEqual(run.call_args.kwargs['env']['NLM_PERFIL_CONSTRUCCION'], 'procedimental-v5')

    def test_existing_releases_are_never_overwritten(self):
        for release in ('continuidad_procedimental_v5', 'funcional_v4', 'continuidad_intrapadre_v3'):
            with self.subTest(release=release), self.assertRaises(ValueError):
                pipeline.release_target(ROOT / 'data/releases' / release)
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as tmp:
            with self.assertRaises(ValueError):
                pipeline.release_target(Path(tmp))

    # --- comparador ---------------------------------------------------------
    def test_gate_rejects_a_third_union(self):
        rows = copy.deepcopy(self.after)
        target = next(i for i, r in enumerate(rows) if r['ID_Intervencion'] == 'RPM-2006-07-13:780:3')
        rows[target]['ID_Turno'] = rows[target-1]['ID_Turno']
        rows[target]['Relacion_Turno'] = RELATION
        rows[target]['ID_Antecedente_Continuidad'] = rows[target-1]['ID_Intervencion']
        with self.assertRaises(ValueError):
            self.compare(rows)

    def test_gate_rejects_any_other_field_change(self):
        for field in ('Texto', 'Actor_Final', 'Fuente_Actor', 'Motivos_Revision', 'ID_Ancla_Actor'):
            rows = copy.deepcopy(self.after)
            rows[0][field] = 'otro'
            with self.subTest(campo=field), self.assertRaises(ValueError):
                self.compare(rows)

    def test_gate_rejects_missing_union(self):
        with self.assertRaises(ValueError):
            self.compare(copy.deepcopy(self.v5))


if __name__ == '__main__':
    unittest.main()
