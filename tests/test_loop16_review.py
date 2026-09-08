"""LOOP16: cierres anafóricos, atribuciones locales y residuos no certificados."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews,speaker_intervals,validate_speaker_reviews
from context_warnings import load_context_warnings,contextual_motives,has_context_warning,NAME_MOTIVE,DECISIONS
from review_flags import review_reasons
from continuity import annotate_turns

IDS=(506,780,1572,4575,4579,4582,4584,6009,6025,6530)
class LoopSixteenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw);cls.warnings=load_context_warnings(cls.raw)
    def parts(self,p,review=None):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews[p] if review is None else review)
    def rows(self,p):
        return [dict(ID=i,ID_Padre=p,ID_Intervencion=f'{p}:{i}',ID_Bloque_Texto=f'{p}:{i}',Fecha=self.raw[p]['Fecha'],Texto=t,Actor_Final=a,Fuente_Actor=m,Fuente_Rol='LISTA_ASISTENCIA',Duplicado_Exacto='NO',Duplicado_Formula='NO') for i,(t,a,m) in enumerate(self.parts(p))]
    def test_historical_identity_pending_is_independent_of_primary_change(self):
        from review_queue import track,compact
        for p,original,expected in [(4575,'Miguel Ricaurte Bermúdez','METODO_ACTUALIZADO'),(6025,'Miguel Ricaurte Vintimilla','CORRECCION_DIRIGIDA_APLICADA')]:
            r=self.rows(p)[0];r['Motivos_Revision']='VARIANTE_IDENTIDAD_POR_VERIFICAR'
            old=dict(r,Actor_Final=original,Fuente_Actor='NOMBRE+VERBO',Inicio_Compacto=0,Fin_Compacto=len(compact(r['Texto'])),SHA256_Texto=hashlib.sha256(r['Texto'].encode()).hexdigest())
            result=track([r],{'Filas':[old]},{},self.reviews)[0]
            self.assertEqual(result['Estado_Seguimiento'],expected)
            self.assertEqual(result['Variante_Identidad_Pendiente'],'SI')
            self.assertIn('VARIANTE_IDENTIDAD_POR_VERIFICAR',result['Alertas_Actuales'])
            self.assertIn('no fusionar variantes',result['Siguiente_Paso'])
    def test_identity_marker_uses_current_alert_not_only_historical_alert(self):
        from review_queue import track,compact
        r=self.rows(6025)[0];r['Motivos_Revision']=''
        old=dict(r,Motivos_Revision='VARIANTE_IDENTIDAD_POR_VERIFICAR',Fuente_Actor='NOMBRE+VERBO',Inicio_Compacto=0,Fin_Compacto=len(compact(r['Texto'])),SHA256_Texto=hashlib.sha256(r['Texto'].encode()).hexdigest())
        result=track([r],{'Filas':[old]},{})[0]
        self.assertEqual(result['Variante_Identidad_Pendiente'],'')
        self.assertEqual(result['Alertas_Actuales'],'')
    def test_all_new_intervals_survive_bounded(self):
        for p in IDS:self.assertFalse(validate_speaker_reviews(self.rows(p),{p:self.reviews[p]}))
    def test_lehmann_expositions_keep_full_available_development(self):
        for p,n in [(506,8662),(1572,18132)]:
            t,a,m=next(x for x in self.parts(p) if len(x[0])==n)
            self.assertEqual((a,m),('Sergio Lehmann Beresi','CONTEXTO_REVISADO'))
    def test_506_previous_answer_remains_independent(self):
        intervals=speaker_intervals(self.reviews[506]);self.assertEqual(len(intervals),2)
        self.assertEqual(intervals[1]['Revision_ID'],'HAB-20260908-L13-506')
        self.assertEqual((intervals[1]['Inicio'],intervals[1]['Fin']),(15634,15841))
        self.assertEqual(len([t for t,a,m in self.parts(506) if len(t)==206 and m=='CONTEXTO_REVISADO']),1)
    def test_780_partial_correction_does_not_assign_bridge_to_corbo(self):
        parts=self.parts(780)
        self.assertEqual([(a,len(t)) for t,a,m in parts[:3]],[('José De Gregorio Rebeco',5463),('Vittorio Corbo Lioi',1655),('Vittorio Corbo Lioi',1763)])
        self.assertIn('En la economía nacional',parts[0][0]);self.assertTrue(parts[1][0].startswith('Lo que sí ha cambiado, indica el señor Corbo'))
        self.assertIn('En la economía nacional',self.warnings[780]['Texto_Intervalo'])
        self.assertEqual(self.warnings[780]['Actor_Provisional'],'José De Gregorio Rebeco')
    def test_780_explicit_posterior_anchor_is_preserved(self):
        rows=self.rows(780);annotate_turns(rows)
        self.assertFalse(rows[1]['ID_Ancla_Actor']);self.assertTrue(rows[2]['ID_Ancla_Actor'])
        self.assertEqual(rows[2]['Fuente_Actor'],'SUJETO_ROL_NOMBRE')
    def test_fin_alone_cannot_manufacture_780_posterior_split(self):
        e=copy.deepcopy(self.reviews[780]);e.pop('Cita_Ancla_Posterior');parts=self.parts(780,e)
        self.assertEqual(len(parts),3)
        self.assertFalse(any(len(t)==1763 for t,a,m in parts))
    def test_6009_restores_both_ricaurte_interventions_and_presidential_return(self):
        parts=self.parts(6009)
        self.assertEqual([a for t,a,m in parts],['Rodrigo Vergara Montes','Miguel Ricaurte Bermúdez','Rodrigo Vergara Montes','Miguel Ricaurte Bermúdez'])
        self.assertIn('Mark Carney',parts[2][0])
        self.assertTrue(parts[3][0].startswith('A continuación el señor Miguel Ricaurte'))
        self.assertIn('planteamiento del Consejero señor Sebastián Claro',parts[3][0])
    def test_local_ricaurte_labels_require_recorded_full_name_evidence(self):
        for p in [4575,4579,4582,4584,6009,6025]:
            for e in speaker_intervals(self.reviews[p]):
                self.assertEqual(e['Actor'],'Miguel Ricaurte Bermúdez')
                self.assertTrue(any('don Miguel Ricaurte Bermúdez' in ev['Cita'] and ev['ID_Padre'] in [4573,6008] for ev in e['Evidencia']))
                self.assertIn('No resuelve la identidad real',e['Limitacion'])
    def test_ricaurte_identity_warning_is_not_removed(self):
        for p in [4575,4579,4582,4584,6009,6025]:
            for r in self.rows(p):
                if r['Actor_Final'].startswith('Miguel Ricaurte'):
                    self.assertIn('VARIANTE_IDENTIDAD_POR_VERIFICAR',review_reasons(r,b.TURN_DETECTOR,b.split_sentences))
    def test_6025_original_variant_is_not_rewritten(self):
        self.assertEqual(self.raw[6025]['Actor'],'Miguel Ricaurte Vintimilla')
        self.assertEqual(self.parts(6025)[0][1],'Miguel Ricaurte Bermúdez')
        self.assertNotIn('Bermúdez',self.parts(6025)[0][0])
    def test_6530_literal_name_remains_pending(self):
        t,a,m=self.parts(6530)[0]
        self.assertIn('señor Claudia Raddatz',t);self.assertEqual(a,'Claudio Raddatz Kiefer')
        self.assertEqual(self.warnings[6530]['Motivo'],NAME_MOTIVE)
        self.assertEqual(self.warnings[6530]['Decision'],'PENDIENTE_CONTRASTE_NOMBRE')
    def test_name_warning_blocks_continuity_like_other_pending_context(self):
        self.assertTrue(has_context_warning(NAME_MOTIVE))
        rows=self.rows(6530);rows[0]['Motivos_Revision']=NAME_MOTIVE;annotate_turns(rows)
        self.assertFalse(rows[0]['ID_Ancla_Actor'])
    def test_new_warnings_apply_only_to_exact_actor_and_interval(self):
        for p in [506,780,6530]:
            matches=[r for r in self.rows(p) if contextual_motives(r,self.warnings)]
            self.assertEqual(len(matches),1)
            r=copy.deepcopy(matches[0]);r['Texto']+=' X';self.assertFalse(contextual_motives(r,self.warnings))
    def test_source_damage_not_reconstructed(self):
        self.assertIn('indicadores de El señor Lehmann',self.parts(506)[1][0])
        self.assertTrue(self.parts(506)[1][0].endswith('tanto en Estados Unidos'))
    def test_6185_and_joint_identity_cases_remain_unadjudicated(self):
        self.assertFalse({6185,6443,2126,3989}&set(self.reviews))
    def test_changed_source_hash_rejects_local_review(self):
        raw=copy.deepcopy(self.raw);raw[6025]['Texto']+=' X'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'r.json';p.write_text(json.dumps([self.reviews[6025]]))
            with self.assertRaises(ValueError):load_speaker_reviews(raw,p)
    def test_invalid_name_warning_decision_is_rejected(self):
        e=copy.deepcopy(self.warnings[6530]);e['Decision']='IDENTIDAD_RESUELTA'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'w.json';p.write_text(json.dumps([e]))
            with self.assertRaises(ValueError):load_context_warnings(self.raw,p)
    def test_parent_506_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[506]['Texto'].encode()).hexdigest(),'aa7efe74ac2d46954631ae46ff00e6e104e89ba5ee2472c0278c735030ba48b0')
        parts=self.parts(506)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 547, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 8662, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 107, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 5743, 'SUJETO_ROL_NOMBRE'), ('Vittorio Corbo Lioi', 49, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 384, 'SUJETO_ROL_NOMBRE'), ('Nicolás Eyzaguirre Guzmán', 135, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 206, 'CONTEXTO_REVISADO'), ('Jorge Desormeaux Jiménez', 272, 'SUJETO_ROL_NOMBRE'), ('Vittorio Corbo Lioi', 533, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[506]['Texto'].split()))
    def test_parent_780_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[780]['Texto'].encode()).hexdigest(),'c9325d0aa5f9fa57bef82bb441e6a5ef228ee0db912c062c1c0fdc09d758cf13')
        parts=self.parts(780)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 5463, 'SUJETO_ROL_NOMBRE'), ('Vittorio Corbo Lioi', 1655, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 1763, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 2546, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[780]['Texto'].split()))
    def test_parent_1572_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1572]['Texto'].encode()).hexdigest(),'04437337337c05085053dd8af06c2f511eaaf4bce58ce84c23daa09359f8b65e')
        parts=self.parts(1572)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 764, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 18132, 'CONTEXTO_REVISADO'), ('José De Gregorio Rebeco', 98, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1572]['Texto'].split()))
    def test_parent_4575_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[4575]['Texto'].encode()).hexdigest(),'21057cd763854b3d0d2182dd7d28f4e865ad511e2377012e750572d03a6c81d0')
        parts=self.parts(4575)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Miguel Ricaurte Bermúdez', 4584, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4575]['Texto'].split()))
    def test_parent_4579_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[4579]['Texto'].encode()).hexdigest(),'5f50759fd1857d9d32d97142df0d2fd7b895818dbd37c5fa809075130bc5f6d2')
        parts=self.parts(4579)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Miguel Ricaurte Bermúdez', 873, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4579]['Texto'].split()))
    def test_parent_4582_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[4582]['Texto'].encode()).hexdigest(),'a84aada20e9c6c82793af566bfc4e09e4d34989ffa19363bd3bf2f67e8ca15e3')
        parts=self.parts(4582)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Miguel Ricaurte Bermúdez', 1220, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4582]['Texto'].split()))
    def test_parent_4584_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[4584]['Texto'].encode()).hexdigest(),'be4ec63a7ce1938bc3f352ff0013e809fa00a43e7bdd8fb9bb2a833c7889b24f')
        parts=self.parts(4584)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Miguel Ricaurte Bermúdez', 3010, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4584]['Texto'].split()))
    def test_parent_6009_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6009]['Texto'].encode()).hexdigest(),'16fd710baf80d00ceb56182997af5adcf43ead96cdc8e4d5b6428b3583599503')
        parts=self.parts(6009)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 1451, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 4969, 'CONTEXTO_REVISADO'), ('Rodrigo Vergara Montes', 902, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 4481, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6009]['Texto'].split()))
    def test_parent_6025_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6025]['Texto'].encode()).hexdigest(),'b7a023efdd8437efce3c271d74227e78887167054d2dbb69b0682b31b7518130')
        parts=self.parts(6025)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Miguel Ricaurte Bermúdez', 415, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6025]['Texto'].split()))
    def test_parent_6530_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6530]['Texto'].encode()).hexdigest(),'563bd75f4a960704d95076f464c81bcf11b388e19b38a1e7019e46d5899cc2e0')
        parts=self.parts(6530)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Raddatz Kiefer', 883, 'CONTEXTO_REVISADO'), ('Rodrigo Vergara Montes', 239, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6530]['Texto'].split()))
