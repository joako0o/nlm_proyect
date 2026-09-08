"""Lecturas acotadas: consultas, Fiscal, continuaciones y advertencias residuales."""
import copy
import hashlib
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews,validate_speaker_reviews,speaker_intervals
from context_warnings import load_context_warnings,contextual_motives
from continuity import update_state
from mention_reviews import load_mention_reviews,PENDING_DECISION

STRUCT=(280,518,631,2141,2646,3012,5199,6862)
class LoopTwentyOneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw);cls.warnings=load_context_warnings(cls.raw)
    def parts(self,p,review=True):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p) if review else None)
    def with_entry(self,p,entry,text=None):
        r=self.raw[p];return b.segment_turns(text if text is not None else r['Texto'],r['Fecha'],r['Actor'],review=entry)
    def test_all_thirteen_intervals_match_output(self):
        ps=STRUCT+(632,4289)
        self.assertEqual(sum(len(speaker_intervals(self.reviews[p])) for p in ps),13)
        for p in ps:
            rs=[dict(ID=i,ID_Padre=p,Actor_Final=a,Fuente_Actor=m,Texto=t,Fecha=self.raw[p]['Fecha']) for i,(t,a,m) in enumerate(self.parts(p))]
            self.assertFalse(validate_speaker_reviews(rs,{p:self.reviews[p]}))
    def test_280_only_the_read_tail_is_resegmented(self):
        before=self.parts(280,False);after=self.parts(280)
        self.assertEqual(before[:5],after[:5]);self.assertEqual(len(after[1][0]),30150)
        self.assertEqual([a for t,a,m in after[-3:]],['Luis Óscar Herrera Barriga','Nicolás Eyzaguirre Guzmán','Luis Óscar Herrera Barriga'])
    def test_short_minister_question_not_deleted_or_merged(self):
        self.assertEqual([len(t) for t,a,m in self.parts(631)],[106,59,182])
        self.assertTrue(self.parts(631)[1][0].endswith(','))
    def test_cual_reply_requires_separator_and_compatible_actor(self):
        e=copy.deepcopy(speaker_intervals(self.reviews[631])[1]);r=self.raw[631]
        with self.assertRaises(ValueError):self.with_entry(631,e,r['Texto'].replace('caído, a lo cual','caído. a lo cual'))
        e['Actor']='Andrés Velasco Brañes'
        with self.assertRaises(ValueError):self.with_entry(631,e)
    def test_fiscal_is_not_the_question_recipient_until_the_response(self):
        parts=self.parts(6862)
        self.assertEqual(parts[0][1],'Rodrigo Vergara Montes');self.assertIn('Fiscal señor Juan Pablo Araya',parts[0][0])
        self.assertEqual(parts[1][1],'Juan Pablo Araya Marco');self.assertEqual(len(parts[1][0]),164)
        self.assertEqual(parts[2][1],'Rodrigo Vergara Montes')
        self.assertEqual(b.roster_role_for(self.raw[6862]['Fecha'],'Juan Pablo Araya Marco'),'Fiscal y Ministro de Fe')
    def test_fiscal_response_requires_contiguous_named_question_and_que(self):
        e=copy.deepcopy(speaker_intervals(self.reviews[6862])[0]);t=self.raw[6862]['Texto']
        for old,new in [('que precise','que precise.'),('indicando el señor Fiscal que','indicando el señor Fiscal si'),('solicita al Fiscal señor','recuerda al Fiscal señor')]:
            with self.assertRaises(ValueError):self.with_entry(6862,e,t.replace(old,new,1))
    def test_fiscal_response_rejects_wrong_actor_and_open_quote(self):
        e=copy.deepcopy(speaker_intervals(self.reviews[6862])[0]);e['Actor']='Rodrigo Vergara Montes'
        with self.assertRaises(ValueError):self.with_entry(6862,e)
        e=copy.deepcopy(speaker_intervals(self.reviews[6862])[0]);t=self.raw[6862]['Texto'];t='“'+t[1:]
        with self.assertRaises(ValueError):self.with_entry(6862,e,t)
    def test_fiscal_review_does_not_create_global_anchor(self):
        t,a,m=self.parts(6862)[1];state={}
        update_state(state,a,m,t,self.raw[6862]['Fecha'],b.TURN_DETECTOR,b.split_sentences,'reviewed')
        self.assertFalse(state['anchor'])
        for alias in ['marco','juan pablo']:
            self.assertNotIn(alias,b.alias_map)
            self.assertIsNone(b.resolve_name(alias))
        self.assertFalse(b.TURN_DETECTOR.speaker('El señor Marco responde que no.',self.raw[6862]['Fecha']))
        self.assertFalse(b.TURN_DETECTOR.speaker('El señor Fiscal que no hay inconveniente.',self.raw[6862]['Fecha']))
    def test_relative_statement_opt_in_not_generalized(self):
        self.assertEqual(len(self.parts(3012,False)),2);self.assertEqual(len(self.parts(3012)),3)
        e=copy.deepcopy(self.reviews[3012]);e['Tipo_Limite']='CESION_RELATIVA_EXPLICITA'
        with self.assertRaises(ValueError):self.with_entry(3012,e)
        e=copy.deepcopy(self.reviews[3012]);e['Actor']='José De Gregorio Rebeco'
        with self.assertRaises(ValueError):self.with_entry(3012,e)
    def test_long_valdes_exposition_and_missing_number_preserved(self):
        t,a,m=self.parts(518)[-2];self.assertEqual((a,len(t)),('Rodrigo Valdés Pulido',5935))
        self.assertIn('7. Con los antecedentes',t);self.assertIn('9. Por otro lado',t);self.assertNotIn('8. ',t)
        self.assertEqual(self.parts(518)[-1][1],'Vittorio Corbo Lioi')
    def test_post_review_explicit_segments_kept(self):
        for p in [3012,6862]:
            e=copy.deepcopy(self.reviews[p]);parts=self.parts(p)
            targets=[(x,y) for x,y in zip(parts,parts[1:]) if x[2]=='CONTEXTO_REVISADO' and y[1]==x[1] and y[2] in b.EXPLICIT]
            self.assertEqual(len(targets),1)
            anchor_entry=next(x for x in speaker_intervals(e) if 'Cita_Ancla_Posterior' in x)
            anchor_entry['Cita_Ancla_Posterior']='bad'
            # speaker_intervals returns copies; mutate the matching original entry.
            if 'Cita_Ancla_Posterior' in e:e['Cita_Ancla_Posterior']='bad'
            else:next(x for x in e['Revisiones_Adicionales'] if 'Cita_Ancla_Posterior' in x)['Cita_Ancla_Posterior']='bad'
            with self.assertRaises(ValueError):self.with_entry(p,e)
    def test_4289_role_conflict_does_not_split_or_reassign_to_soto(self):
        parts=self.parts(4289);self.assertEqual(len(parts),1)
        self.assertEqual((parts[0][1],len(parts[0][0])),('Sergio Lehmann Beresi',8677))
        self.assertIn('Gerente de Análisis Macroeconómico señor Lehmann',parts[0][0])
        self.assertEqual(self.warnings[4289]['Motivo'],'CARGO_EN_DISCURSO_POR_VERIFICAR')
    def test_joint_adhesion_not_assigned_to_one_of_three_councillors(self):
        self.assertNotIn(4446,self.reviews);self.assertEqual(self.parts(4446),self.parts(4446,False))
        self.assertEqual(self.warnings[4446]['Motivo'],'PASAJES_CONJUNTOS_POR_DELIMITAR')
        self.assertIn('Marshall, Sebastián Claro y Rodrigo Vergara',self.parts(4446)[-1][0])
    def test_warning_scopes_are_exact_and_old_mentions_remain(self):
        for p,n in [(518,5935),(520,2821),(632,587),(2141,774),(4289,8677),(4446,484),(6862,1302)]:
            hits=[t for t,a,m in self.parts(p) if contextual_motives(dict(ID_Padre=p,Fecha=self.raw[p]['Fecha'],Actor_Final=a,Texto=t),self.warnings)]
            self.assertEqual(len(hits),1);self.assertEqual(len(hits[0]),n)
        ms=load_mention_reviews(self.raw);self.assertEqual(len(ms),25)
        self.assertEqual([e['ID_Padre'] for e in ms.values() if e['Decision']==PENDING_DECISION],[6185,3775])
    def test_source_mutation_invalidates_registration(self):
        raw=copy.deepcopy(self.raw);raw[6862]['Texto']+='X'
        with self.assertRaises(ValueError):load_speaker_reviews(raw)
    def test_parent_280_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[280]['Texto'].encode()).hexdigest(),'4c38d3c35a0899a6b6bdbbdb2881827c9227d661a36e89c030da8e19eec97916')
        parts=self.parts(280)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 123, 'SUJETO_ROL_SESION'), ('Pablo García Silva', 30150, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 167, 'SUJETO_ROL_NOMBRE'), ('Vittorio Corbo Lioi', 409, 'SUJETO_ROL_SESION'), ('Nicolás Eyzaguirre Guzmán', 200, 'SUJETO_ROL_SESION'), ('Luis Óscar Herrera Barriga', 846, 'SUJETO_ROL_NOMBRE'), ('Nicolás Eyzaguirre Guzmán', 100, 'CONTEXTO_REVISADO'), ('Luis Óscar Herrera Barriga', 496, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[280]['Texto'].split()))
    def test_parent_518_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[518]['Texto'].encode()).hexdigest(),'338eb4cec2822fd5b72b5347bffce8dc7cc0249dad384d72bcc8517e4ac1b95b')
        parts=self.parts(518)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 101, 'SUJETO_ROL_NOMBRE'), ('Nicolás Eyzaguirre Guzmán', 221, 'SUJETO_ROL_SESION'), ('Vittorio Corbo Lioi', 128, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 73, 'ACTA/META'), ('Vittorio Corbo Lioi', 252, 'SUJETO_ROL_SESION'), ('Rodrigo Valdés Pulido', 5935, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 74, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[518]['Texto'].split()))
    def test_parent_520_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[520]['Texto'].encode()).hexdigest(),'86507f139d96c4e1832471dc0514926d662dd51b59d3ca5f9e7d3b0418f44b63')
        parts=self.parts(520)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Esteban Jadresic Marinovic', 2821, 'SUJETO_ROL_NOMBRE'), ('Luis Óscar Herrera Barriga', 2539, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[520]['Texto'].split()))
    def test_parent_631_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[631]['Texto'].encode()).hexdigest(),'4abeb0c7028c8cfa5b3437effbeb7eea57f4952f977cf87b31f4bda52b1dff9e')
        parts=self.parts(631)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sergio Lehmann Beresi', 106, 'SUJETO_ROL_SESION'), ('Andrés Velasco Brañes', 59, 'CONTEXTO_REVISADO'), ('Sergio Lehmann Beresi', 182, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[631]['Texto'].split()))
    def test_parent_632_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[632]['Texto'].encode()).hexdigest(),'8ad10eebc2786fd79b8dd29c7ba80943082aff1535f29d1935abb722c79128c0')
        parts=self.parts(632)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 262, 'SUJETO_ROL_NOMBRE'), ('Andrés Velasco Brañes', 122, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 587, 'CONTEXTO_REVISADO'), ('Manuel Marfán Lewis', 1259, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[632]['Texto'].split()))
    def test_parent_2141_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2141]['Texto'].encode()).hexdigest(),'e78e59949649ec149c607c32796f404fb07681ce6087b2642c4f82309aed538f')
        parts=self.parts(2141)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 181, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 774, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2141]['Texto'].split()))
    def test_parent_2646_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2646]['Texto'].encode()).hexdigest(),'a3bc594a2e243e4e850d9c632c9f0a9e40a4c7c69e97c8f5f247163428606901')
        parts=self.parts(2646)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 149, 'SUJETO_ROL_SESION'), ('Kevin Cowan Logan', 1781, 'SUJETO_NOMBRE'), ('José De Gregorio Rebeco', 147, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2646]['Texto'].split()))
    def test_parent_3012_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3012]['Texto'].encode()).hexdigest(),'43d700164e62a0195f0ca2b54a9cf3b35f2b2c806beb76f8dfa56694f13f661f')
        parts=self.parts(3012)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 109, 'SUJETO_ROL_SESION'), ('Beltrán de Ramón Acevedo', 375, 'CONTEXTO_REVISADO'), ('Beltrán de Ramón Acevedo', 1867, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3012]['Texto'].split()))
    def test_parent_4289_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4289]['Texto'].encode()).hexdigest(),'b3fa558f3810fbed4261fb728d3203b36ba9424fe26b2919029c497f99a93c3d')
        parts=self.parts(4289)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sergio Lehmann Beresi', 8677, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4289]['Texto'].split()))
    def test_parent_4446_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4446]['Texto'].encode()).hexdigest(),'f0dff58326025d43fd8e66d706493d3ed3aa2b7d0fddcc7fc34d034a98918a9d')
        parts=self.parts(4446)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 203, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 75, 'ACTA/META'), ('Manuel Marfán Lewis', 1637, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 484, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4446]['Texto'].split()))
    def test_parent_5199_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5199]['Texto'].encode()).hexdigest(),'1c9ada655a76fab8cd26c5a14bff63a190a68c437a589608543053a3f81f407f')
        parts=self.parts(5199)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 204, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 634, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5199]['Texto'].split()))
    def test_parent_6862_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[6862]['Texto'].encode()).hexdigest(),'d2ca34e001f4d59555e28431d2d79c34d6623b79cb2c0a7d49572eec9a6210cc')
        parts=self.parts(6862)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 213, 'SUJETO_ROL_NOMBRE'), ('Juan Pablo Araya Marco', 164, 'CONTEXTO_REVISADO'), ('Rodrigo Vergara Montes', 155, 'CONTEXTO_REVISADO'), ('Alejandro Micco', 1302, 'CONTEXTO_REVISADO'), ('Alejandro Micco', 642, 'SUJETO_NOMBRE'), ('Rodrigo Vergara Montes', 2292, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6862]['Texto'].split()))
