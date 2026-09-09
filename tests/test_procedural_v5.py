"""Lote5: sólo seis enlaces; no promover contexto ni atravesar pausas/voces."""
import collections
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_base_referencia as b
import preparar_data as pipeline
from reviewed_procedural_v5 import (BASE,BASE_SHA,PATH,READINGS,PAIRS,PARENTS,RELATION,
    load_reviews,validate_readings,apply_reviews,validate_reviews,matching_review,active_reviews,export_inventory,file_sha)
from compare_procedural_v5 import compare,groups
from diagnosticar_finales import read_rows
from auditar_continuidad_turnos import inventory
from qa_preparacion import validate_continuity
from continuity import annotate_turns,boundary
from reviewed_continuity import load_reviewed_links,validate_reviewed_links
from intrapara_profiles import load_intrapara_links
from reviewed_intrapara_continuity import validate_intrapara_links
from functional_refinements import load_refinements,validate_refinements,refined_institutions
from institutional_reviews import load_institutional_reviews,validate_institutional_reviews


class ProceduralV5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={int(r[0]):{'Fecha':b.to_date_str(r[1]),'Texto':str(r[5])} for r in b.data}
        cls.before=read_rows(BASE);cls.pkg=json.loads(PATH.read_text());cls.readings=json.loads(READINGS.read_text())
        cls.reviews=load_reviews(cls.raw)
        cls.inter=load_reviewed_links(cls.raw)
        cls.intra=load_intrapara_links(cls.raw,ROOT/'data/curation/continuidades_intrapadre_v3.json')
        cls.functional=load_refinements(cls.raw)
        # Ejercitar primero el motor de continuidad histórico, luego el adaptador.
        actual=annotate_turns(copy.deepcopy(cls.before),cls.inter,cls.intra)
        for r in actual:
            for k in ('ID_Antecedente_Continuidad','ID_Ancla_Actor'):
                if r[k]=='':r[k]=None
        if actual!=cls.before:raise AssertionError('El motor histórico dejó de reproducir v4')
        cls.after=apply_reviews(actual,cls.reviews)

    def load(self,pkg):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'proof.json';p.write_text(json.dumps(pkg));return load_reviews(self.raw,p)

    def row(self,rid,rows=None):return next(r for r in (self.after if rows is None else rows) if r['ID_Intervencion']==rid)

    def test_frozen_baseline_and_six_pairs(self):
        self.assertEqual(file_sha(BASE),BASE_SHA)
        self.assertEqual(set(self.reviews),set(PAIRS))
        self.assertEqual(len(self.before),9694)

    def test_full_parent_reading_and_all_group_members(self):
        validate_readings(self.before,self.readings,self.raw)
        self.assertEqual(len(PARENTS),12)
        self.assertEqual(sum(len(e['Texto_Padre']) for e in self.readings['Padres'].values()),23450)
        self.assertEqual([r['ID_Padre'] for r in self.readings['Casos'][PAIRS[3][0]]['Grupos_Leidos']['Izquierda']],[2202,2203])

    def test_exact_global_changes(self):
        r=compare(self.before,self.after)
        self.assertEqual((r['Grupos_Antes'],r['Grupos_Despues']),(9242,9236))
        self.assertEqual((len(r['Celdas_Relacionales_Modificadas']),len(r['Celdas_ID_Turno_Modificadas'])),(12,147))
        self.assertEqual(len(r['Filas_Con_Conjunto_De_Companeros_Distinto']),13)
        self.assertEqual((r['Alertas_Antes'],r['Alertas_Despues']),(467,467))

    def test_v4_inventory_replaces_three_pairs_not_six(self):
        prior=read_rows(ROOT/'data/releases/continuidad_intrapadre_v3'/BASE.name)
        a={(e['Izquierda'],e['Derecha']) for e in inventory(prior)}
        z={(e['Izquierda'],e['Derecha']) for e in inventory(self.before)}
        self.assertEqual((len(a),len(z),len(a&z)),(77,77,74))
        self.assertEqual(len(inventory(self.after)),71)

    def test_scoped_f1_accepts_and_unscoped_f1_rejects(self):
        self.assertEqual(validate_continuity(self.after,self.reviews),[])
        self.assertTrue(validate_continuity(self.after))
        self.assertTrue(validate_reviews(self.before,self.reviews))

    def test_prior_proofs_and_functional_splits_still_pass(self):
        self.assertEqual((len(self.inter),len(self.intra)),(24,15))
        self.assertEqual(validate_reviewed_links(self.after,self.inter),[])
        self.assertEqual(validate_intrapara_links(self.after,self.intra),[])
        self.assertEqual(validate_refinements(self.after,self.functional),[])
        inst=refined_institutions(load_institutional_reviews(self.raw),self.functional)
        self.assertEqual(validate_institutional_reviews(self.after,inst),[])

    def test_context_stays_without_anchor_or_new_source(self):
        r=self.row(PAIRS[-1][1]);self.assertEqual(r['Fuente_Actor'],'CONTEXTO_REVISADO')
        self.assertIsNone(r['ID_Ancla_Actor']);self.assertEqual(r['Relacion_Turno'],RELATION)
        self.assertEqual(len(r['Texto']),797)
        for a,z in zip(self.before,self.after):self.assertEqual(a['ID_Ancla_Actor'],z['ID_Ancla_Actor'])

    def test_pauses_before_reopening_remain_separate(self):
        for a,z in [('RPM-2010-07-15:3269:1','RPM-2010-07-15:3269:2'),('RPM-2010-09-16:3421:4','RPM-2010-09-16:3421:5')]:
            self.assertNotEqual(self.row(a)['ID_Turno'],self.row(z)['ID_Turno'])
            self.assertIsNone(self.row(z)['ID_Antecedente_Continuidad'])

    def test_presentations_and_responses_not_absorbed(self):
        for p,n in [(1604,6220),(1631,3865),(3270,7111)]:
            parts=[r for r in self.after if r['ID_Padre']==p]
            self.assertEqual(len(parts[1]['Texto']),n)
            self.assertNotEqual(parts[0]['ID_Turno'],parts[1]['ID_Turno'])
        for left,p in [(PAIRS[2][1],1842),(PAIRS[3][1],2205),(PAIRS[-1][1],3422)]:
            other=next(r for r in self.after if r['ID_Padre']==p)
            self.assertNotEqual(self.row(left)['ID_Turno'],other['ID_Turno'])

    def test_extended_three_member_group_and_marshall_separate(self):
        turn=self.row(PAIRS[3][1])['ID_Turno']
        self.assertEqual([r['ID_Intervencion'] for r in self.after if r['ID_Turno']==turn],
                         ['RPM-2008-12-11:2202:2',*PAIRS[3]])
        self.assertNotEqual(self.row('RPM-2008-12-11:2202:1')['ID_Turno'],turn)

    def test_literal_damage_and_duplicate_alerts_preserved(self):
        self.assertTrue(self.row(PAIRS[3][0])['Texto'].endswith('A continuación,.'))
        self.assertIn('de de',self.row(PAIRS[3][1])['Texto'])
        self.assertTrue(self.row(PAIRS[-1][1])['Texto'].endswith('Presidente.'))
        for a,z in zip(self.before,self.after):
            for k in ('Texto','Motivos_Revision','Duplicado_Exacto','Duplicado_Formula'):self.assertEqual(a[k],z[k])

    def test_garcia_and_reserved_cases_unchanged_membership(self):
        old={rid:g for g in groups(self.before) for rid in g};new={rid:g for g in groups(self.after) for rid in g}
        self.assertEqual(max(map(len,groups(self.after))),11)
        for r in self.before:
            if r['ID_Padre'] in {600,601,780,2661,2863,2864,3646,5252,5402,5403,4788,4849,4899,6808}:
                self.assertEqual(old[r['ID_Intervencion']],new[r['ID_Intervencion']])

    def test_no_global_boundary_change_or_default_application(self):
        for left,right in PAIRS:self.assertTrue(boundary(self.row(left)['Texto']))
        rows=copy.deepcopy(self.before);self.assertIs(apply_reviews(rows,{}),rows);self.assertEqual(rows,self.before)

    def test_only_full_registry_and_not_already_applied(self):
        with self.assertRaises(ValueError):apply_reviews(copy.deepcopy(self.before),dict(list(self.reviews.items())[:-1]))
        with self.assertRaises(ValueError):apply_reviews(copy.deepcopy(self.after),self.reviews)

    def test_invalid_versions_pairs_hashes(self):
        for field,v in [('Version',True),('Version',4),('Perfil','funcional-v4'),('Pares',[]),
                        ('SHA256_Base','otro'),('SHA256_Lecturas','otro'),('SHA256_Registro_Funcional_V4','otro')]:
            pkg=copy.deepcopy(self.pkg);pkg[field]=v
            with self.subTest(field=field),self.assertRaises(ValueError):self.load(pkg)

    def test_full_member_evidence_cannot_be_shortened(self):
        pkg=copy.deepcopy(self.readings);pkg['Casos'][PAIRS[3][0]]['Grupos_Leidos']['Izquierda']=pkg['Casos'][PAIRS[3][0]]['Grupos_Leidos']['Izquierda'][1:]
        with self.assertRaises(ValueError):validate_readings(self.before,pkg,self.raw)
        pkg=copy.deepcopy(self.readings);del pkg['Padres']['2202']
        with self.assertRaises(ValueError):validate_readings(self.before,pkg,self.raw)

    def test_raw_source_interval_window_and_decision_mutations_fail(self):
        for field,v in [('Texto_Padre','otro'),('SHA256_Particion','otro'),('Vecino_Anterior',{}),('Lectura','VENTANA')]:
            pkg=copy.deepcopy(self.readings);pkg['Padres']['3421'][field]=v
            with self.subTest(field=field),self.assertRaises(ValueError):validate_readings(self.before,pkg,self.raw)
        pkg=copy.deepcopy(self.readings);pkg['Casos'][PAIRS[0][0]]['Decision']='AGRUPAR_TODO'
        with self.assertRaises(ValueError):validate_readings(self.before,pkg,self.raw)
        raw=copy.deepcopy(self.raw);raw[1604]['Texto']+=' '
        with self.assertRaises(ValueError):validate_readings(self.before,self.readings,raw)

    def test_changed_actor_text_type_source_anchor_or_warning_not_exempt(self):
        for side in [0,1]:
            for field,v in [('Texto','otro'),('Actor_Final',b.CONSEJO),('Tipo_Acta','ACUERDO_CONSEJO'),
                            ('Fuente_Actor','CONTEXTO_REVISADO'),('ID_Ancla_Actor','otra'),('Motivos_Revision','DANO')]:
                rows=copy.deepcopy(self.after);self.row(PAIRS[0][side],rows)[field]=v
                with self.subTest(side=side,field=field):
                    self.assertTrue(validate_continuity(rows,self.reviews))
                    with self.assertRaises(ValueError):compare(self.before,rows)

    def test_global_other_columns_extra_split_merge_and_labels_fail(self):
        for field in ['Texto','Nota','Actor_Final','ID_Ancla_Actor','Motivos_Revision','Numero_Segmento','ID','ID_Turno']:
            rows=copy.deepcopy(self.after);rows[0][field]='otro'
            with self.subTest(field=field),self.assertRaises(ValueError):compare(self.before,rows)
        for p in [780,2696,2864,5252,5403]:
            rows=copy.deepcopy(self.after);next(r for r in rows if r['ID_Padre']==p)['ID_Turno']='otro'
            with self.subTest(parent=p),self.assertRaises(ValueError):compare(self.before,rows)

    def test_context_cannot_be_promoted_or_wrong_antecedent_accepted(self):
        for field,v in [('ID_Ancla_Actor',PAIRS[-1][0]),('ID_Antecedente_Continuidad','RPM-2010-09-16:3421:4'),('Relacion_Turno','CONTINUIDAD_EXPLICITA')]:
            rows=copy.deepcopy(self.after);self.row(PAIRS[-1][1],rows)[field]=v
            self.assertTrue(validate_continuity(rows,self.reviews))
            with self.assertRaises(ValueError):compare(self.before,rows)

    def test_missing_reordered_rows_and_schema_fail(self):
        rows=copy.deepcopy(self.after);rows[0],rows[1]=rows[1],rows[0]
        for r in [rows,self.after[:-1],self.after+[self.after[-1]]]:
            with self.assertRaises(ValueError):compare(self.before,r)
        rows=copy.deepcopy(self.after);del rows[0]['Nota']
        with self.assertRaises(ValueError):compare(self.before,rows)

    def test_export_reproducible_safe_and_not_productive(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'.cache') as t:
            a,z=Path(t)/'a',Path(t)/'z';export_inventory(a);export_inventory(z)
            self.assertEqual({p.name:p.read_bytes() for p in a.iterdir()},{p.name:p.read_bytes() for p in z.iterdir()})
            with self.assertRaises(ValueError):export_inventory(a)
        for p in ['data/new','data/releases/new','data/processed/new']:
            with self.assertRaises(ValueError):export_inventory(ROOT/p)

    def test_active_profile_requires_previous_layers(self):
        for env in [{'NLM_INTRAPARA_REVIEWS':''},{'NLM_FUNCTIONAL_REVIEWS':''}]:
            with patch.dict(os.environ,{'NLM_PROCEDURAL_REVIEWS':str(PATH),**env}):
                with self.assertRaises(ValueError):active_reviews(self.raw)
        with patch.dict(os.environ,{'NLM_PROCEDURAL_REVIEWS':''}):self.assertEqual(active_reviews(self.raw),{})

    def test_old_profiles_clear_ambient_v5(self):
        for profile in ['legacy','intrapadre-v1','intrapadre-v2','intrapadre-v3','funcional-v4']:
            with tempfile.TemporaryDirectory(dir=ROOT/'.cache') as t:
                args=['--perfil',profile]+(['--destino',str(Path(t)/'new')] if profile!='legacy' else [])
                with patch.dict(os.environ,{'NLM_PROCEDURAL_REVIEWS':'otro'}),patch.object(pipeline.subprocess,'run',side_effect=RuntimeError('stop')) as run:
                    with self.assertRaises(RuntimeError):pipeline.main(args)
                    self.assertNotIn('NLM_PROCEDURAL_REVIEWS',run.call_args.kwargs['env'])

    def test_default_v5_and_failed_gate_never_publish(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'.cache') as t:
            dest=Path(t)/'new'
            with patch.object(pipeline.subprocess,'run',side_effect=RuntimeError('stop')) as run:
                with self.assertRaises(RuntimeError):pipeline.main(['--destino',str(dest)])
                self.assertEqual(run.call_args.kwargs['env']['NLM_PROCEDURAL_REVIEWS'],str(PATH))
                self.assertFalse(dest.exists())


if __name__=='__main__':unittest.main()
