"""LOOP24: actos personales frente a metadatos, pasivas y cesiones acotadas."""
import copy,hashlib,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews,speaker_intervals,validate_speaker_reviews
from context_warnings import load_context_warnings,contextual_motives,validate_context_warnings
from mention_reviews import load_mention_reviews
from continuity import update_state
STRUCT=(2661,2680,2746,2788,2875,2958,3008,3288,5252)
class LoopTwentyFourTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw);cls.warnings=load_context_warnings(cls.raw)
    def parts(self,p,review=True):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p) if review else None)
    def entry(self,p,last=False):
        return copy.deepcopy([e for e in speaker_intervals(self.reviews[p]) if '-L24-' in e['Revision_ID']][-1 if last else 0])
    def variant(self,p,replace=None,prefix_quote=False,actor=None,last=False):
        e=self.entry(p,last);r=self.raw[p];t=r['Texto'];pre,body,tail=t[:e['Inicio']],t[e['Inicio']:e['Fin']],t[e['Fin']:]
        if replace:
            old,new=replace;pre=pre.replace(old,new);body=body.replace(old,new)
        if prefix_quote:pre='“'+pre
        e['Inicio']=len(pre);e['Fin']=len(pre)+len(body)
        if actor:e['Actor']=actor
        return b.segment_turns(pre+body+tail,r['Fecha'],r['Actor'],review=e)
    def test_ten_new_intervals_validate_and_no_global_anchors(self):
        self.assertEqual(sum('-L24-' in e['Revision_ID'] for p in STRUCT for e in speaker_intervals(self.reviews[p])),10)
        for p in STRUCT:
            rows=[dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p))]
            self.assertEqual(validate_speaker_reviews(rows,{p:self.reviews[p]}),[])
            for t,a,m in self.parts(p):
                if m=='CONTEXTO_REVISADO':
                    state={};update_state(state,a,m,t,self.raw[p]['Fecha'],b.TURN_DETECTOR,b.split_sentences,'reviewed')
                    self.assertFalse(state['anchor'])
    def test_three_new_boundaries_are_opt_in_only(self):
        for p in [2661,3288,2788,5252]:self.assertGreater(len(self.parts(p)),len(self.parts(p,False)))
        self.assertIn('haciendo presente que',self.parts(5252,False)[1][0])
        self.assertIn('El señor Gerente de División Estudios Subrogante recuerda',self.parts(2788,False)[-1][0])
    def test_passive_variants_reject_past_and_wrong_preposition(self):
        for p in [2661,3288]:
            for replace in [(' es ',' fue '),(' por el ',' para el ')]:
                with self.subTest(p=p,replace=replace),self.assertRaises(ValueError):self.variant(p,replace)
    def test_new_nominal_boundaries_reject_wrong_actor_and_open_quote(self):
        for p,last in [(2661,False),(3288,False),(5252,False),(2788,True)]:
            with self.subTest(p=p),self.assertRaises(ValueError):self.variant(p,actor='Rodrigo Vergara Montes',last=last)
            with self.subTest(p=p),self.assertRaises(ValueError):self.variant(p,prefix_quote=True,last=last)
    def test_passive_variants_do_not_expand_previous_opt_in(self):
        for p in [2661,3288]:
            e=self.entry(p);e['Tipo_Limite']='RESPUESTA_PASIVA_NOMINAL_REVISADA';r=self.raw[p]
            with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)
    def test_assumption_requires_contiguous_named_subject_and_declaration(self):
        for replace in [('pasa a presidir','había presidido'),('señor Manuel Marfán,','señor Desconocido,'),('haciendo presente que','habiendo estado presente'),('Manuel Marfán,','Manuel Marfán.')]:
            with self.subTest(replace=replace),self.assertRaises(ValueError):self.variant(5252,replace)
    def test_role_handoff_requires_actual_nominal_invitation_and_predicate(self):
        for replace in [('ofrece la palabra al','menciona la labor del'),('señor Claudio Soto, para','señor Desconocido, para'),('Subrogante recuerda que','Subrogante estuvo presente')]:
            with self.subTest(replace=replace),self.assertRaises(ValueError):self.variant(2788,replace,last=True)
        # La nómina no certifica el cargo subrogante: sólo el destinatario nominal.
        self.assertEqual(b.roster_role_for(self.raw[2788]['Fecha'],'Claudio Soto Gamboa'),'Gerente de Análisis Macroeconómico')
    def test_time_preface_does_not_make_welcomed_recipient_speak(self):
        for p,n in [(2875,1038),(2958,224),(3008,332)]:
            self.assertEqual(self.parts(p)[1][1:],('José De Gregorio Rebeco','CONTEXTO_REVISADO'))
            self.assertEqual(len(self.parts(p)[1][0]),n)
            self.assertEqual(self.parts(p,False)[1][1],b.CONSEJO)
        self.assertEqual(self.parts(3008)[2][1],'Felipe Larraín Bascuñán')
    def test_reopening_and_attendance_stay_institutional(self):
        for p,i,n in [(2680,1,75),(2746,3,287),(2788,2,74),(5252,1,158)]:
            t,a,m=self.parts(p)[i];self.assertEqual((a,m),(b.CONSEJO,'ACTA/META'));self.assertEqual(len(t),n)
        self.assertIn('excusó su asistencia',self.parts(2746)[-1][0])
        self.assertNotIn('Andrés Velasco Brañes',[a for t,a,m in self.parts(2746)])
    def test_long_presentations_and_two_posterior_anchors_preserved(self):
        for p,n in [(2661,1322),(2746,1094),(3288,3138),(5252,1712),(2680,489)]:self.assertTrue(any(len(t)==n and m in b.EXPLICIT for t,a,m in self.parts(p)))
        for p,n in [(2661,1322),(5252,223)]:
            pairs=[(x,y) for x,y in zip(self.parts(p),self.parts(p)[1:]) if x[2]=='CONTEXTO_REVISADO' and x[1]==y[1] and y[2] in b.EXPLICIT]
            self.assertEqual(len(pairs),1);self.assertEqual(len(pairs[0][1][0]),n)
    def test_retired_warning_and_original_coordination_are_preserved(self):
        self.assertNotIn(2661,self.warnings)
        archive=json.loads(Path('data/curation/alertas_contextuales_retiradas.json').read_text());self.assertEqual(len(archive),3)
        e=next(e for e in archive if e['Alerta_Original']['ID_Padre']==2661)
        self.assertEqual(e['Alerta_Original']['Texto_Intervalo'],' '.join(t for t,a,m in self.parts(2661)[4:6]))
        old=[e for e in speaker_intervals(self.reviews[2661]) if '-L24-' not in e['Revision_ID']]
        self.assertEqual(len(old),1);self.assertEqual(old[0]['Tipo_Limite'],'COORDINACION_Y_EXPLICITA')
    def test_five_exact_warnings_do_not_certify_or_rewrite(self):
        for p,n in [(2680,75),(2788,407),(2958,335),(3008,413),(4055,722)]:
            rows=[dict(ID=i,ID_Padre=p,Fecha=self.raw[p]['Fecha'],Texto=t,Actor_Final=a,Motivos_Revision='') for i,(t,a,m) in enumerate(self.parts(p))]
            hits=[r for r in rows if contextual_motives(r,self.warnings)];self.assertEqual(len(hits),1);self.assertEqual(len(hits[0]['Texto']),n)
            hits[0]['Motivos_Revision']=self.warnings[p]['Motivo'];self.assertEqual(validate_context_warnings(rows,{p:self.warnings[p]}),[])
            hits[0]['Texto']+=' añadido';self.assertTrue(validate_context_warnings(rows,{p:self.warnings[p]}))
    def test_reference_controls_and_joint_passage_are_not_invented_turns(self):
        ms=load_mention_reviews(self.raw)
        for p in [1549,2219,4055]:self.assertEqual(self.parts(p),self.parts(p,False));self.assertNotIn(p,self.reviews)
        self.assertEqual({e['ID_Padre'] for e in ms.values() if e['Decision']=='PENDIENTE_DELIMITAR_APORTE'},{6185,3775,4055,2510})
        self.assertEqual(sum(e['Decision']=='MENCION_LEGITIMA_REVISADA' for e in ms.values()),98)
        self.assertEqual(self.warnings[4055]['Motivo'],'PASAJES_CONJUNTOS_POR_DELIMITAR')
    def test_source_hash_mutation_fails_before_publication(self):
        raw=copy.deepcopy(self.raw);raw[2788]['Texto']+='X'
        with self.assertRaises(ValueError):load_speaker_reviews(raw)
    def test_parent_2661_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2661]['Texto'].encode()).hexdigest(),'ba871e522560a087da27e178ffbdc31badc52e41f09e7fa9b434fb31d9a632c4')
        ps=self.parts(2661)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Andrés Velasco Brañes', 98, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 219, 'SUJETO_NOMBRE'), ('Jorge Desormeaux Jiménez', 292, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 917, 'SUJETO_NOMBRE'), ('Jorge Desormeaux Jiménez', 193, 'SUJETO_NOMBRE'), ('Sergio Lehmann Beresi', 49, 'CONTEXTO_REVISADO'), ('Sergio Lehmann Beresi', 1322, 'SUJETO_ROL_SESION'), ('Andrés Velasco Brañes', 107, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 375, 'SUJETO_ROL_NOMBRE'), ('Andrés Velasco Brañes', 58, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 69, 'CONTEXTO_REVISADO'), ('Sebastián Claro Edwards', 208, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[2661]['Texto'].split()))
    def test_parent_2680_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2680]['Texto'].encode()).hexdigest(),'9f6dc581b25eb91f7662b1418656aea654f8d86f74b3e4c6c2d812c8108aeef0')
        ps=self.parts(2680)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('José De Gregorio Rebeco', 180, 'SUJETO_ROL_SESION'), ('Consejo del Banco Central de Chile', 75, 'ACTA/META'), ('José De Gregorio Rebeco', 164, 'CONTEXTO_REVISADO'), ('Pablo García Silva', 489, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[2680]['Texto'].split()))
    def test_parent_2746_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2746]['Texto'].encode()).hexdigest(),'6bbf874937a753e834e76198517edb90e1e36ad6e68988ca7f4f4fb0d40b27e6')
        ps=self.parts(2746)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('José De Gregorio Rebeco', 153, 'SUJETO_ROL_SESION'), ('Kevin Cowan Logan', 1094, 'SUJETO_NOMBRE'), ('José De Gregorio Rebeco', 181, 'CONTEXTO_REVISADO'), ('Consejo del Banco Central de Chile', 287, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[2746]['Texto'].split()))
    def test_parent_2788_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2788]['Texto'].encode()).hexdigest(),'01401cf1a5883b177d14025bb3c371eb389bada960e5c62511165ffeeee87131')
        ps=self.parts(2788)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('José De Gregorio Rebeco', 126, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 182, 'CONTEXTO_REVISADO'), ('Consejo del Banco Central de Chile', 74, 'ACTA/META'), ('José De Gregorio Rebeco', 191, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 407, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[2788]['Texto'].split()))
    def test_parent_2875_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2875]['Texto'].encode()).hexdigest(),'130cfe9812c54e581dfc4c2d8a9d46092a7a31da68109450c501a8304a3b2e37')
        ps=self.parts(2875)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('José De Gregorio Rebeco', 79, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 1038, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[2875]['Texto'].split()))
    def test_parent_2958_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2958]['Texto'].encode()).hexdigest(),'6e6dcaac4057416a10b9c9cb842a9f47d0e54a09ede2a94f8cf33a5a568cf34e')
        ps=self.parts(2958)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('José De Gregorio Rebeco', 335, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 224, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[2958]['Texto'].split()))
    def test_parent_3008_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3008]['Texto'].encode()).hexdigest(),'e06a08c6d205aadcc7918c9243c489cb14ee76fe353db9d8ec7e6684b525e9e8')
        ps=self.parts(3008)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('José De Gregorio Rebeco', 61, 'SUJETO_ROL_SESION'), ('José De Gregorio Rebeco', 332, 'CONTEXTO_REVISADO'), ('Felipe Larraín Bascuñán', 413, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[3008]['Texto'].split()))
    def test_parent_3288_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3288]['Texto'].encode()).hexdigest(),'d381eea1c036434cb1b3bf3658db833e511294c237958afc1f6fb5767a4a761e')
        ps=self.parts(3288)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Rodrigo Vergara Montes', 129, 'SUJETO_ROL_NOMBRE'), ('Beltrán de Ramón Acevedo', 96, 'CONTEXTO_REVISADO'), ('Sergio Lehmann Beresi', 3138, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[3288]['Texto'].split()))
    def test_parent_5252_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5252]['Texto'].encode()).hexdigest(),'5962e84de409e110e810754ab33a7799f9758ae3aeff1f12c2d97a86bb245686')
        ps=self.parts(5252)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Manuel Marfán Lewis', 1712, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 158, 'ACTA/META'), ('Manuel Marfán Lewis', 162, 'CONTEXTO_REVISADO'), ('Manuel Marfán Lewis', 223, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[5252]['Texto'].split()))
    def test_parent_1549_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1549]['Texto'].encode()).hexdigest(),'1a8e5a56c3eb0cd869b86884ac1dfd7d33fe9d6f1ad5099de4a7dbca881d860e')
        ps=self.parts(1549)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Manuel Marfán Lewis', 332, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[1549]['Texto'].split()))
    def test_parent_2219_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2219]['Texto'].encode()).hexdigest(),'7899c455442a19c92887e9ea500bf2a89ad56ff4ee98dddc91d43a4b3e17b0db')
        ps=self.parts(2219)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Manuel Marfán Lewis', 786, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 297, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[2219]['Texto'].split()))
    def test_parent_4055_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4055]['Texto'].encode()).hexdigest(),'d265a6d34f7613d664e750177bec1c8584e2da48ab9605e08966d73a7588aa24')
        ps=self.parts(4055)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('José De Gregorio Rebeco', 722, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 39, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[4055]['Texto'].split()))
