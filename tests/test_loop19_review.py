"""Continuidades por lectura acotada: no fusionan textos ni habilitan herencia."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, validate_speaker_reviews
from reviewed_continuity import load_reviewed_links,validate_reviewed_links,RELATION
from mention_reviews import load_mention_reviews,validate_mention_reviews,PENDING_DECISION,DECISION
from context_warnings import load_context_warnings,contextual_motives
from continuity import annotate_turns,update_state
from qa_preparacion import validate_continuity

class LoopNineteenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw);cls.links=load_reviewed_links(cls.raw)
        cls.warnings=load_context_warnings(cls.raw);cls.mentions=load_mention_reviews(cls.raw)
    def parts(self,p):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p))
    def pair(self,key):
        e=self.links[key]
        return [dict(ID=i,ID_Padre=s['ID_Padre'],ID_Intervencion=f'proof:{i}',ID_Bloque_Texto=f'proof:{i}',Fecha=e['Fecha'],Texto=s['Texto'],Actor_Final=e['Actor'],Fuente_Actor=s['Fuente_Actor'],Tipo_Acta=None,Motivos_Revision='') for i,s in enumerate([e['Anterior'],e['Siguiente']],1)]
    def test_four_pairs_require_opt_in(self):
        for key in self.links:
            rs=self.pair(key);annotate_turns(rs)
            self.assertNotEqual(rs[0]['ID_Turno'],rs[1]['ID_Turno'])
    def test_four_pairs_join_without_changing_text_actor_or_source(self):
        for key in self.links:
            rs=self.pair(key);before=[(r['Texto'],r['Actor_Final'],r['Fuente_Actor']) for r in rs]
            annotate_turns(rs,{key:self.links[key]})
            self.assertEqual(before,[(r['Texto'],r['Actor_Final'],r['Fuente_Actor']) for r in rs])
            self.assertEqual(rs[0]['ID_Turno'],rs[1]['ID_Turno'])
            self.assertEqual(rs[1]['Relacion_Turno'],RELATION)
            self.assertFalse(rs[0]['ID_Ancla_Actor']);self.assertEqual(rs[1]['ID_Ancla_Actor'],rs[1]['ID_Intervencion'])
            self.assertFalse(validate_continuity(rs));self.assertFalse(validate_reviewed_links(rs,{key:self.links[key]}))
    def test_reviewed_left_still_does_not_create_actor_inheritance(self):
        for key,e in self.links.items():
            state={};left=self.pair(key)[0]
            update_state(state,e['Actor'],left['Fuente_Actor'],left['Texto'],e['Fecha'],b.TURN_DETECTOR,b.split_sentences,'old-reviewed')
            self.assertFalse(state['anchor'])
    def test_changed_endpoint_text_is_rejected(self):
        key=(4941,4942);rs=self.pair(key);rs[0]['Texto']+=' X'
        with self.assertRaises(ValueError):annotate_turns(rs,{key:self.links[key]})
    def test_changed_actor_date_or_source_rejected(self):
        key=(4941,4942)
        for field,value in [('Actor_Final','Manuel Marfán Lewis'),('Fecha','2000-01-01'),('Fuente_Actor','CONTEXTO_REVISADO')]:
            rs=self.pair(key);rs[1][field]=value
            with self.assertRaises(ValueError):annotate_turns(rs,{key:self.links[key]})
    def test_intervening_speaker_cannot_be_skipped(self):
        key=(4941,4942);rs=self.pair(key);middle=dict(rs[0],ID=99,ID_Padre=999,ID_Intervencion='middle',Actor_Final='Manuel Marfán Lewis')
        with self.assertRaises(ValueError):annotate_turns([rs[0],middle,rs[1]],{key:self.links[key]})
    def test_warnings_on_either_endpoint_block_reviewed_join(self):
        key=(4941,4942)
        for i in [0,1]:
            for motive in ['NOMBRE_EN_DISCURSO_POR_VERIFICAR','TEXTO_DANADO_POR_COTEJAR','POSIBLE_OTRO_HABLANTE_O_MENCION']:
                rs=self.pair(key);rs[i]['Motivos_Revision']=motive
                with self.assertRaises(ValueError):annotate_turns(rs,{key:self.links[key]})
                rs=self.pair(key);annotate_turns(rs,{key:self.links[key]})
                rs[i]['Motivos_Revision']=motive
                self.assertTrue(validate_continuity(rs))
    def test_handoff_and_institutional_barriers_not_overridden(self):
        key=(4941,4942);e=copy.deepcopy(self.links[key]);rs=self.pair(key)
        rs[0]['Texto']+=' Ofrece la palabra.';e['Anterior']['Texto']=rs[0]['Texto']
        with self.assertRaises(ValueError):annotate_turns(rs,{key:e})
        rs=self.pair(key);rs[0]['Tipo_Acta']='ACTA_INSTITUCIONAL'
        with self.assertRaises(ValueError):annotate_turns(rs,{key:self.links[key]})
    def test_unregistered_reviewed_relation_rejected_by_validator(self):
        rs=self.pair((4941,4942));annotate_turns(rs);rs[1]['Relacion_Turno']=RELATION
        self.assertTrue(validate_reviewed_links(rs,{}))
    def test_wrong_anchor_and_missing_antecedent_rejected(self):
        key=(4941,4942);rs=self.pair(key);annotate_turns(rs,{key:self.links[key]})
        rs[0]['ID_Ancla_Actor']=rs[0]['ID_Intervencion'];self.assertTrue(validate_reviewed_links(rs,{key:self.links[key]}))
        rs[0]['ID_Ancla_Actor']='';rs[1]['ID_Antecedente_Continuidad']='';self.assertTrue(validate_reviewed_links(rs,{key:self.links[key]}))
    def test_link_source_hash_bounds_and_duplicates_checked(self):
        e=copy.deepcopy(self.links[(4941,4942)])
        for kind in ['hash','bounds','duplicate']:
            x=copy.deepcopy(e)
            if kind=='hash':x['Anterior']['SHA256_Texto_Padre']='bad'
            if kind=='bounds':x['Anterior']['Inicio']+=1
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'e.json';p.write_text(json.dumps([x,x] if kind=='duplicate' else [x]))
                with self.assertRaises(ValueError):load_reviewed_links(self.raw,p)
    def test_registered_edges_include_loops19_20_23_26_28_and29(self):
        self.assertEqual(set(self.links),{(3887,3888),(4224,4225),(4941,4942),(5910,5911),(2836,2837),(2707,2708),(2963,2964),(4745,4746),(6561,6562),(121,122),(727,728),(2027,2028),(2838,2839),(2911,2912),(2918,2919),(3123,3124),(3571,3572),(4470,4471),(4903,4904),(5168,5169),(5872,5873),(6118,6119),(6394,6395),(5003,5004)})
        self.assertNotIn((5402,5403),self.links)
    def test_5911_long_presentation_remains_one_physical_segment(self):
        parts=self.parts(5911);self.assertEqual(len(parts),1);self.assertEqual(len(parts[0][0]),10080)
    def test_6185_long_presentation_not_split_or_reassigned(self):
        parts=self.parts(6185);self.assertEqual(len(parts),1)
        self.assertEqual((len(parts[0][0]),parts[0][1]),(20118,'Sergio Lehmann Beresi'))
        self.assertIn('conforme señala el Gerente de Mercados Nacionales señor Matías Bernier',parts[0][0])
        self.assertNotIn(6185,self.reviews)
    def test_pending_reading_never_becomes_legitimate_mention(self):
        e=next(e for e in self.mentions.values() if e['ID_Padre']==6185)
        self.assertEqual(e['Decision'],PENDING_DECISION)
        t,a,m=self.parts(6185)[0];rs=[dict(ID=1,ID_Padre=6185,Fecha=e['Fecha'],Actor_Final=a,Texto=t,Motivos_Revision='POSIBLE_OTRO_HABLANTE_O_MENCION')]
        errors,annotations=validate_mention_reviews(rs,{e['Revision_ID']:e})
        self.assertFalse(errors);self.assertEqual(annotations[1]['Estado_Lectura_Dirigida'],PENDING_DECISION)
        self.assertEqual(rs[0]['Motivos_Revision'],'POSIBLE_OTRO_HABLANTE_O_MENCION')
        self.assertEqual(sum(e['Decision']==DECISION for e in self.mentions.values()),98)
    def test_metadata_reviews_preserve_complete_developments(self):
        for p,n in [(2349,599),(3050,3025),(3315,1239)]:
            rows=[dict(ID=i,ID_Padre=p,Actor_Final=a,Fuente_Actor=m,Texto=t,Fecha=self.raw[p]['Fecha']) for i,(t,a,m) in enumerate(self.parts(p))]
            self.assertFalse(validate_speaker_reviews(rows,{p:self.reviews[p]}))
            hits=[r for r in rows if contextual_motives(r,self.warnings)]
            self.assertEqual(len(hits),1);self.assertEqual(len(hits[0]['Texto']),n);self.assertIn('Claudia Soto',hits[0]['Texto'])
    def test_existing_continuities_with_pending_name_not_forced_apart(self):
        for p in [226,3454]:
            self.assertNotIn(p,self.reviews);self.assertNotIn(p,self.warnings)
    def test_joint_passages_still_unadjudicated(self):
        self.assertFalse({2126,3989}&set(self.reviews))
        for p in [780,4433,3191,5367]:self.assertIn(p,self.warnings)
    def test_parent_2349_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2349]['Texto'].encode()).hexdigest(),'2b4e81f08c4a9883ba8e5d9b070424dea19edbc0bb9269f14e497f00783dc15d')
        parts=self.parts(2349)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Pablo García Silva', 1063, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 599, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2349]['Texto'].split()))
    def test_parent_3050_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3050]['Texto'].encode()).hexdigest(),'7287e9b8a419da34e8521c6ded3bf24b516ed39ea4da92d3a375fb9474e8c128')
        parts=self.parts(3050)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 302, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 181, 'SUJETO_NOMBRE'), ('Claudio Soto Gamboa', 3025, 'CONTEXTO_REVISADO'), ('Sebastián Claro Edwards', 433, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 384, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3050]['Texto'].split()))
    def test_parent_3315_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3315]['Texto'].encode()).hexdigest(),'f01ccc15a4a4e8729c22c1be73c903c44a151b872713a01b36c5a49508f1c4e3')
        parts=self.parts(3315)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Ricardo Vicuña Poblete', 165, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 1239, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3315]['Texto'].split()))
    def test_parent_3887_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3887]['Texto'].encode()).hexdigest(),'d8c21b38a94635b583aee621d4346374a9cb9226d2d1edb43800462c4a230453')
        parts=self.parts(3887)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 5698, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 2667, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3887]['Texto'].split()))
    def test_parent_3888_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3888]['Texto'].encode()).hexdigest(),'a7f3086e6c10fae71e8fd07e54381e0686b27afadd7ec00caa93058bf5dd6cab')
        parts=self.parts(3888)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 1627, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3888]['Texto'].split()))
    def test_parent_4224_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[4224]['Texto'].encode()).hexdigest(),'9aa4dcbac22b640a6a916b017e2225fdc46da85624ff836af69d724028d09530')
        parts=self.parts(4224)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Kevin Cowan Logan', 441, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 966, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4224]['Texto'].split()))
    def test_parent_4225_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[4225]['Texto'].encode()).hexdigest(),'2f42616bf276092f9929202420d430e54bb951c95a73784e2ec18785783969f7')
        parts=self.parts(4225)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sergio Lehmann Beresi', 2853, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4225]['Texto'].split()))
    def test_parent_4941_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[4941]['Texto'].encode()).hexdigest(),'daadfa2182aa9d4d37d5cc72237af3e914ca3862ca627468f93bcae57253e7af')
        parts=self.parts(4941)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Luis Óscar Herrera Barriga', 312, 'SUJETO_NOMBRE'), ('Claudio Soto Gamboa', 2079, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4941]['Texto'].split()))
    def test_parent_4942_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[4942]['Texto'].encode()).hexdigest(),'8ef3a1304cf754da6562f7b1c0d036250eef1be6f0d8c68bf4ee185b43bc9145')
        parts=self.parts(4942)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 291, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4942]['Texto'].split()))
    def test_parent_5910_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[5910]['Texto'].encode()).hexdigest(),'832b9d1155ccb16fe1e5d60f5758a23665c91f3f250cbf79f6cae618eb6b5507')
        parts=self.parts(5910)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Joaquín Vial Ruiz-Tagle', 365, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 1848, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5910]['Texto'].split()))
    def test_parent_5911_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[5911]['Texto'].encode()).hexdigest(),'bd1fea7a89cb68fa4345ced808e5ec141c22f2110863948d37a0a6e07c9ad00b')
        parts=self.parts(5911)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sergio Lehmann Beresi', 10080, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5911]['Texto'].split()))
    def test_parent_6185_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6185]['Texto'].encode()).hexdigest(),'9a9b1345ac739250ef4d70153ea9d737a7cb5d09795d79c9433f840dfa423792')
        parts=self.parts(6185)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sergio Lehmann Beresi', 20118, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6185]['Texto'].split()))
