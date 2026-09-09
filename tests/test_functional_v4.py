"""Refinamiento funcional cerrado; los perfiles históricos siguen congelados."""
import collections
import copy
import hashlib
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
from functional_refinements import (PATH,BASE,BASE_SHA,PARENTS,PREVIOUS,load_refinements,
                                    refine_segments,refined_institutions,validate_refinements,active_refinements)
from compare_functional_v4 import compare,expected_rows,members
from diagnosticar_finales import read_rows
from institutional_reviews import load_institutional_reviews,validate_institutional_reviews,institutional_type
from continuity import annotate_turns
from review_flags import review_reasons
from procedural import is_formula
from reviewed_continuity import load_reviewed_links,validate_reviewed_links
from intrapara_profiles import load_intrapara_links
from reviewed_intrapara_continuity import validate_intrapara_links
from qa_preparacion import validate_continuity


class FunctionalV4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={int(r[0]):{'Fecha':b.to_date_str(r[1]),'Texto':str(r[5])} for r in b.data}
        cls.before=read_rows(BASE);cls.pkg=json.loads(PATH.read_text())
        cls.reviews=load_refinements(cls.raw)
        cls.institutions=load_institutional_reviews(cls.raw)
        cls.refined=refined_institutions(cls.institutions,cls.reviews)
        cls.inter=load_reviewed_links(cls.raw)
        cls.intra=load_intrapara_links(cls.raw,ROOT/'data/curation/continuidades_intrapadre_v3.json')
        cls.after,cls.lineage=expected_rows(cls.before,cls.reviews)
        # Ejercitar las reglas reales sobre el refinamiento: no conservar las
        # relaciones esperadas ni dar por verdaderas sus alertas calculadas.
        for r in cls.after:
            if r['ID_Padre'] in PARENTS and r['Numero_Segmento']<=2:
                r['Tipo_Acta']=('ACUERDO_CONSEJO' if b._is_current_decision(r['Texto']) else None)
                reasons=review_reasons(r,b.TURN_DETECTOR,b.split_sentences)
                r['Motivos_Revision']=';'.join(reasons) or None
                r['Estado_Revision']='PENDIENTE_REVISION' if reasons else 'SIN_ALERTAS_AUTOMATICAS'
            for key in ('ID_Turno','Relacion_Turno','ID_Ancla_Actor','ID_Antecedente_Continuidad'):r[key]=None
        annotate_turns(cls.after,cls.inter,cls.intra)
        for r in cls.after:
            for key in ('ID_Ancla_Actor','ID_Antecedente_Continuidad'):
                if r[key]=='':r[key]=None

    def load(self,pkg,raw=None):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'proof.json';p.write_text(json.dumps(pkg))
            return load_refinements(raw or self.raw,p)

    def parts(self,p,rows=None):return [r for r in (rows if rows is not None else self.after) if r['ID_Padre']==p]

    def test_frozen_v3_and_scope(self):
        self.assertEqual(hashlib.sha256(BASE.read_bytes()).hexdigest(),BASE_SHA)
        self.assertEqual(set(self.reviews),PARENTS)
        self.assertEqual((len(self.before),len(self.after)),(9691,9694))

    def test_global_full_comparison(self):
        report,lineage=compare(self.before,self.after,self.reviews)
        self.assertEqual((report['Grupos_Antes'],report['Grupos_Despues']),(9242,9242))
        self.assertEqual(len(lineage),9694)
        self.assertEqual(max(map(len,members(self.after).values())),11)

    def test_three_raw_separators_and_exact_reconstruction(self):
        for p,personal,constancia in [(4788,1946,185),(4849,153,178),(4899,219,178)]:
            e=self.reviews[p]
            self.assertEqual((len(e['Texto_Personal']),len(e['Texto_Constancia'])),(personal,constancia))
            self.assertEqual(e['Separador'],' ')
            self.assertEqual(e['Texto_Personal']+e['Separador']+e['Texto_Constancia'],e['Texto_Original'])

    def test_actual_segmentation_before_and_after_adapter(self):
        for p,e in self.reviews.items():
            old=self.parts(p,self.before)[0]
            legacy=b.segment_turns(self.raw[p]['Texto'],e['Fecha'],old['Actor_Original'],{'date':e['Fecha']},
                                   institution=self.institutions.get(p))
            parts=refine_segments(p,legacy,self.reviews)
            self.assertEqual(parts,[(r['Texto'],r['Actor_Final'],r['Fuente_Actor']) for r in self.parts(p)])

    def test_refinement_requires_original_segmentation(self):
        e=self.reviews[4788]
        for parts in [[],[(e['Texto_Original'],'Consejo','ACTA/META')],[(e['Texto_Personal'],e['Actor'],e['Fuente_Actor'])]]:
            with self.assertRaises(ValueError):refine_segments(4788,parts,self.reviews)

    def test_disabled_adapter_is_identity_and_not_a_marker_rule(self):
        e=self.reviews[4788];parts=[(e['Texto_Original'],e['Actor'],e['Fuente_Actor'])]
        self.assertIs(refine_segments(4788,parts,{}),parts)
        self.assertIs(refine_segments(4333,parts,self.reviews),parts)

    def test_personal_continuities_only_and_own_anchors(self):
        self.assertEqual(validate_refinements(self.after,self.reviews),[])
        for p in PARENTS:
            a,b=self.parts(p)[:2]
            self.assertIsNone(a['Tipo_Acta']);self.assertEqual(b['Tipo_Acta'],'ACUERDO_CONSEJO')
            self.assertEqual(a['Actor_Final'],b['Actor_Final'])
            self.assertEqual(a['ID_Ancla_Actor'],a['ID_Intervencion'])
            self.assertNotEqual(a['ID_Turno'],b['ID_Turno'])

    def test_original_movement_review_not_mutated(self):
        self.assertEqual(len(self.institutions[4788]['Tramos_Resultado']),4)
        self.assertEqual(len(self.refined[4788]['Tramos_Resultado']),5)
        self.assertEqual(self.institutions[4788]['Tramos_Resultado'][1:],self.refined[4788]['Tramos_Resultado'][2:])
        for p,e in self.institutions.items():
            if p!=4788:self.assertEqual(e,self.refined[p])

    def test_strict_historical_validator_rejects_unrefined_proof(self):
        self.assertTrue(validate_institutional_reviews(self.after,self.institutions))
        self.assertEqual(validate_institutional_reviews(self.after,self.refined),[])
        for r in self.parts(4788):
            self.assertEqual(institutional_type(r['Texto'],self.refined[4788]),r['Tipo_Acta'] or '')

    def test_all_prior_continuities_and_f1(self):
        self.assertEqual((len(self.inter),len(self.intra)),(24,15))
        self.assertEqual(validate_reviewed_links(self.after,self.inter),[])
        self.assertEqual(validate_intrapara_links(self.after,self.intra),[])
        self.assertEqual(validate_continuity(self.after),[])

    def test_duplicate_alerts_are_honest_not_suppressed(self):
        a=self.parts(4849)[1];c=self.parts(4899)[1]
        self.assertEqual(a['Texto'],c['Texto']);self.assertFalse(is_formula(a['Texto']))
        counts=collections.Counter(r['Texto'] for r in self.after)
        self.assertEqual(counts[a['Texto']],2)
        for r in self.after:self.assertEqual(r['Duplicado_Exacto'],'SI' if counts[r['Texto']]>1 else 'NO')
        for r in (a,c):self.assertEqual(r['Motivos_Revision'],'DUPLICADO_NO_FORMULA')
        self.assertEqual(sum(bool(r['Motivos_Revision']) for r in self.after),467)

    def test_footer_ocr_and_protected_arrival_and_speeches(self):
        parts=self.parts(4788)
        self.assertIn('Sesión N° 184 Página 23 de 26',parts[1]['Texto'])
        self.assertEqual(parts[1]['Motivos_Revision'],'FINAL_SIN_PUNTUACION')
        self.assertEqual([len(r['Texto']) for r in parts[2:]],[112,161,333])
        self.assertEqual(len({r['ID_Turno'] for r in parts}),5)
        self.assertIsNone(parts[2]['ID_Ancla_Actor'])
        for p in PARENTS:
            original=''.join(r['Texto'] for r in self.parts(p,self.before))
            current=''.join(r['Texto'] for r in self.parts(p))
            self.assertEqual(''.join(original.split()),''.join(current.split()))

    def test_earlier_groups_remain_frozen(self):
        for p in [600,601,780,1901,2779,2705,2706,2885,3268,5252,5402,5403,6808]:
            self.assertEqual([r['ID_Turno'] for r in self.parts(p)], [r['ID_Turno'] for r in self.parts(p,self.before)])

    def test_invalid_version_scope_and_evidence_fail(self):
        for field,value in [('Version',3),('Version',True),('Perfil','intrapadre-v4'),('SHA256_Lecturas_Lote4','otro')]:
            pkg=copy.deepcopy(self.pkg);pkg[field]=value
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):self.load(pkg)
        pkg=copy.deepcopy(self.pkg);del pkg['Revisiones']['4788']
        with self.assertRaises(ValueError):self.load(pkg)
        pkg=copy.deepcopy(self.pkg);pkg['Revisiones']['4333']=pkg['Revisiones']['4849']
        with self.assertRaises(ValueError):self.load(pkg)

    def test_interval_actor_predecessor_and_raw_mutations_fail(self):
        for field,value in [('Texto_Personal','otro'),('Separador',''),('Texto_Constancia','otro'),
                            ('Actor','Consejo del Banco Central de Chile'),('ID_Anterior',PREVIOUS[4849]),
                            ('Fuente_Actor','CONTEXTO_REVISADO'),('Tipo_Personal','ACUERDO_CONSEJO')]:
            pkg=copy.deepcopy(self.pkg);pkg['Revisiones']['4788'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.load(pkg)
        raw=copy.deepcopy(self.raw);raw[4899]['Texto']+=' '
        with self.assertRaises(ValueError):self.load(self.pkg,raw)

    def test_movement_proof_hash_cannot_change(self):
        pkg=copy.deepcopy(self.pkg);pkg['SHA256_Revision_Institucional_4788']='otro'
        with self.assertRaises(ValueError):self.load(pkg)

    def test_candidate_missing_row_column_or_extra_row_fails(self):
        for rows in [self.after[:-1],self.after+[self.after[-1]]]:
            with self.assertRaises(ValueError):compare(self.before,rows,self.reviews)
        rows=copy.deepcopy(self.after);del rows[0]['Texto']
        with self.assertRaises(ValueError):compare(self.before,rows,self.reviews)

    def test_global_unrelated_field_mutations_fail(self):
        for field in ['Texto','Actor_Final','Rol_Final','Nota','Motivos_Revision','ID_Ancla_Actor','Tipo_Acta','Duplicado_Exacto']:
            rows=copy.deepcopy(self.after);rows[0][field]='otro'
            with self.subTest(field=field),self.assertRaises(ValueError):compare(self.before,rows,self.reviews)

    def test_global_unregistered_merges_and_splits_fail(self):
        for p in [600,601,780,2696,2864,5403,6808]:
            rows=copy.deepcopy(self.after);self.parts(p,rows)[-1]['ID_Turno']='otro'
            with self.subTest(parent=p),self.assertRaises(ValueError):compare(self.before,rows,self.reviews)

    def test_no_absorption_of_declaration_event_or_following_intervention(self):
        for n in [1,2,3,4]:
            rows=copy.deepcopy(self.after);parts=self.parts(4788,rows);parts[n]['ID_Turno']=parts[0]['ID_Turno']
            with self.subTest(segment=n),self.assertRaises(ValueError):compare(self.before,rows,self.reviews)

    def test_new_alert_or_footer_cannot_be_hidden(self):
        for p in PARENTS:
            rows=copy.deepcopy(self.after);self.parts(p,rows)[1]['Motivos_Revision']=None
            with self.subTest(parent=p),self.assertRaises(ValueError):compare(self.before,rows,self.reviews)

    def test_movement_actual_five_rows_remain_strict(self):
        for field in ['Texto','Actor_Final','Fuente_Actor','Tipo_Acta','Nota','ID_Ancla_Actor']:
            rows=copy.deepcopy(self.after);self.parts(4788,rows)[2][field]='otro'
            with self.subTest(field=field):self.assertTrue(validate_institutional_reviews(rows,self.refined))

    def test_active_profile_requires_cumulative_v3(self):
        for intra in ['',str(ROOT/'data/curation/continuidades_intrapadre_v2.json')]:
            with patch.dict(os.environ,{'NLM_FUNCTIONAL_REVIEWS':str(PATH),'NLM_INTRAPARA_REVIEWS':intra}):
                with self.assertRaises(ValueError):active_refinements(self.raw)
        with patch.dict(os.environ,{'NLM_FUNCTIONAL_REVIEWS':''}):self.assertEqual(active_refinements(self.raw),{})

    def test_old_profiles_clear_ambient_functional(self):
        for profile in ['legacy','intrapadre-v1','intrapadre-v2','intrapadre-v3']:
            with tempfile.TemporaryDirectory(dir=ROOT/'.cache') as tmp:
                args=['--perfil',profile]+(['--destino',str(Path(tmp)/'new')] if profile!='legacy' else [])
                with patch.dict(os.environ,{'NLM_FUNCTIONAL_REVIEWS':'no-autorizado'}),patch.object(pipeline.subprocess,'run',side_effect=RuntimeError('stop')) as run:
                    with self.assertRaises(RuntimeError):pipeline.main(args)
                    self.assertNotIn('NLM_FUNCTIONAL_REVIEWS',run.call_args.kwargs['env'])

    def test_default_functional_pipeline_and_no_early_publication(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'.cache') as tmp:
            dest=Path(tmp)/'new'
            with patch.object(pipeline.subprocess,'run',side_effect=RuntimeError('stop')) as run:
                with self.assertRaises(RuntimeError):pipeline.main(['--destino',str(dest)])
                self.assertEqual(run.call_args.kwargs['env']['NLM_FUNCTIONAL_REVIEWS'],str(PATH))
                self.assertFalse(dest.exists())


if __name__=='__main__':unittest.main()
