"""Respuestas nominales acotadas: no gerundios globales ni reparación del OCR."""
import copy,hashlib,json,sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews,speaker_intervals,validate_speaker_reviews
from context_warnings import load_context_warnings,contextual_motives
from mention_reviews import load_mention_reviews
from continuity import update_state
STRUCT=(1386,2463,2525,2674,2692,2738,2740,2863,2911,2922,2938,3028,3054,3160,3543,5061,5519,5872,6813,7176)
G='GERUNDIO_NOMINAL_EXPLICITO_REVISADO'
class LoopTwentyTwoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw);cls.warnings=load_context_warnings(cls.raw)
    def parts(self,p,review=True):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p) if review else None)
    def changed(self,p,e,text=None):
        r=self.raw[p];return b.segment_turns(text if text is not None else r['Texto'],r['Fecha'],r['Actor'],review=e)
    def test_twenty_three_new_intervals_match_exact_output(self):
        count=0
        for p in STRUCT:
            count+=sum('-L22-' in e['Revision_ID'] for e in speaker_intervals(self.reviews[p]))
            rows=[dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p))]
            self.assertFalse(validate_speaker_reviews(rows,{p:self.reviews[p]}))
        self.assertEqual(count,23)
    def test_all_six_predicates_require_opt_in(self):
        ps=[2911,2740,2738,3160,5061,7176]
        for p in ps:self.assertGreater(len(self.parts(p)),len(self.parts(p,False)))
        self.assertEqual({self.raw[p]['Texto'][next(e['Inicio'] for e in speaker_intervals(self.reviews[p]) if e.get('Tipo_Limite')==G):].split()[0] for p in ps},{'respondiendo','acotando','comentando','explicando','precisando','agregando'})
    def test_invalid_predicate_preposition_and_missing_que_rejected(self):
        e=copy.deepcopy(self.reviews[2911]);t=self.raw[2911]['Texto']
        for old,new in [('respondiendo el','recordando el'),('respondiendo el','respondiendo al'),('Soto que','Soto si')]:
            with self.assertRaises(ValueError):self.changed(2911,e,t.replace(old,new))
    def test_gerund_requires_separator(self):
        e=copy.deepcopy(self.reviews[2911]);t=self.raw[2911]['Texto'];i=t.rfind(',',0,e['Inicio'])
        with self.assertRaises(ValueError):self.changed(2911,e,t[:i]+'.'+t[i+1:])
    def test_wrong_nominal_actor_and_quote_rejected(self):
        e=copy.deepcopy(self.reviews[2911]);e['Actor']='Rodrigo Vergara Montes'
        with self.assertRaises(ValueError):self.changed(2911,e)
        e=copy.deepcopy(self.reviews[2911]);t=self.raw[2911]['Texto']
        with self.assertRaises(ValueError):self.changed(2911,e,'“'+t[1:])
    def test_role_only_and_unregistered_predicate_do_not_qualify(self):
        date=self.raw[2911]['Fecha']
        for body in ['respondiendo el señor Gerente que no.','recordando el señor Soto que no.','respondiendo al señor Soto que no.']:
            t='El Consejero señor Rodrigo Vergara pregunta, '+body;a=t.index(body)
            e=dict(Actor='Claudio Soto Gamboa',Inicio=a,Fin=len(t),Tipo_Limite=G)
            with self.assertRaises(ValueError):b.segment_turns(t,date,'Rodrigo Vergara Montes',review=e)
    def test_old_gerund_variant_not_silently_widened(self):
        e=copy.deepcopy(self.reviews[2911]);e['Tipo_Limite']='GERUNDIO_SENALANDO_EXPLICITO'
        with self.assertRaises(ValueError):self.changed(2911,e)
    def test_reviewed_responses_never_create_global_anchors(self):
        for p in STRUCT:
            for t,a,m in self.parts(p):
                if m!='CONTEXTO_REVISADO':continue
                state={};update_state(state,a,m,t,self.raw[p]['Fecha'],b.TURN_DETECTOR,b.split_sentences,'reviewed')
                self.assertFalse(state['anchor'])
    def test_explicit_posterior_anchors_kept(self):
        for p,n in [(2692,416),(2863,939),(6813,793)]:
            parts=self.parts(p);matches=[(x,y) for x,y in zip(parts,parts[1:]) if x[2]=='CONTEXTO_REVISADO' and x[1]==y[1] and y[2] in b.EXPLICIT]
            self.assertEqual(len(matches),1);self.assertEqual(len(matches[0][1][0]),n)
            e=copy.deepcopy(self.reviews[p]);e['Cita_Ancla_Posterior']='bad'
            with self.assertRaises(ValueError):self.changed(p,e)
    def test_2463_is_partial_recovery_not_cespedes_return_invented(self):
        parts=self.parts(2463);self.assertEqual(len(parts),2)
        self.assertIn('Este dato corresponde',parts[1][0]);self.assertEqual(parts[1][1],'Andrés Velasco Brañes')
        self.assertIn('provisional',self.reviews[2463]['Justificacion'])
        self.assertIn('Céspedes',self.warnings[2463]['Justificacion'])
    def test_2674_old_later_intervention_and_other_turns_untouched(self):
        parts=self.parts(2674)
        self.assertEqual([(a,len(t)) for t,a,m in parts if a=='Enrique Marshall Rivera'],[('Enrique Marshall Rivera',470),('Enrique Marshall Rivera',1159)])
        old=speaker_intervals(self.reviews[2674])[1]
        self.assertEqual((old['Revision_ID'],old['Inicio'],old['Fin']),('HAB-20260908-2674',5745,6905))
        previous=self.changed(2674,self.reviews[2674]['Revisiones_Adicionales'][0])
        self.assertEqual(parts[3:],previous[1:])
        entries=json.loads(Path('data/curation/revisiones_hablantes.json').read_text())
        original=next(e for e in entries if e['ID_Padre']==2674)['Revisiones_Adicionales'][0]
        self.assertEqual(hashlib.sha256(json.dumps(original,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),'6b65fd3f3139b8e586be14b3d112d77c27bde1e5369306742befd0948a59c00e')
    def test_long_expositions_not_arbitrarily_fragmented(self):
        self.assertEqual(self.parts(2740)[0],self.parts(2740,False)[0])
        self.assertEqual(len(self.parts(2738)[0][0]),4743)
        self.assertEqual(len(self.parts(2738)[2][0]),947)
        self.assertEqual(self.parts(1386)[-1],self.parts(1386,False)[-1])
    def test_damage_and_short_replies_retained(self):
        for p,n in [(2911,43),(3543,56),(2938,51)]:
            t=next(t for t,a,m in self.parts(p) if m=='CONTEXTO_REVISADO');self.assertEqual(len(t),n)
        self.assertTrue(self.parts(2938)[1][0].endswith('tendrá efectos en los'))
        self.assertIn('í\\/larshall',self.parts(2674)[1][0])
        self.assertIn('í\\/lacroeconómico',self.parts(2525)[2][0])
    def test_warnings_have_exact_scope(self):
        for p,n in [(1904,1358),(2463,512),(2525,216),(2674,470),(2938,51)]:
            hits=[t for t,a,m in self.parts(p) if contextual_motives(dict(ID_Padre=p,Fecha=self.raw[p]['Fecha'],Actor_Final=a,Texto=t),self.warnings)]
            self.assertEqual(len(hits),1);self.assertEqual(len(hits[0]),n)
        self.assertNotIn(2863,self.warnings)
    def test_to_the_recipient_is_not_a_new_speaker(self):
        for p in [854,1621]:
            self.assertEqual(self.parts(p),self.parts(p,False))
        self.assertEqual(len(self.parts(854)),1);self.assertEqual(len(self.parts(1621)),5)
        ms=load_mention_reviews(self.raw);self.assertEqual(len(ms),102)
        self.assertEqual({e['ID_Padre'] for e in ms.values() if e['Decision']=='PENDIENTE_DELIMITAR_APORTE'},{6185,3775,4055,2510})
        self.assertEqual({e['ID_Padre'] for e in ms.values() if '-L22-' in e['Revision_ID']},{854,1621})
    def test_changed_source_rejected(self):
        raw=copy.deepcopy(self.raw);raw[2674]['Texto']+='X'
        with self.assertRaises(ValueError):load_speaker_reviews(raw)
    def test_parent_1386_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1386]['Texto'].encode()).hexdigest(),'e3444165d87d43ac1a872fea40b0041ade54d08005d67119304dd892a6927009')
        parts=self.parts(1386)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 104, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 69, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 139, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 833, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1386]['Texto'].split()))
    def test_parent_2463_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2463]['Texto'].encode()).hexdigest(),'932c8060a6d66359f3194a5e74c215400bf23fe71e9eb2a3fb3e34a94f278636')
        parts=self.parts(2463)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Luis Felipe Céspedes Cifuentes', 437, 'SUJETO_ROL_NOMBRE'), ('Andrés Velasco Brañes', 512, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2463]['Texto'].split()))
    def test_parent_2525_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2525]['Texto'].encode()).hexdigest(),'14b7732969ad5775c30a340f52eed5dc4156899f2e059af8e842d97c672da293')
        parts=self.parts(2525)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Andrés Velasco Brañes', 278, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 216, 'CONTEXTO_REVISADO'), ('Claudio Soto Gamboa', 721, 'CONTEXTO_REVISADO'), ('Andrés Velasco Brañes', 98, 'CONTEXTO_REVISADO'), ('Claudio Soto Gamboa', 329, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2525]['Texto'].split()))
    def test_parent_2674_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2674]['Texto'].encode()).hexdigest(),'d0bf1f145f07f3db3c185f7076213df875edad8f8c7939c209fd9dbbdae088aa')
        parts=self.parts(2674)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 2116, 'SUJETO_NOMBRE'), ('Enrique Marshall Rivera', 470, 'CONTEXTO_REVISADO'), ('Claudio Soto Gamboa', 1507, 'SUJETO_ROL_SESION'), ('Kevin Cowan Logan', 386, 'SUJETO_ROL_NOMBRE'), ('Igal Magendzo Weinberger', 237, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 387, 'SUJETO_ROL_SESION'), ('Claudio Soto Gamboa', 635, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 1159, 'CONTEXTO_REVISADO'), ('Claudio Soto Gamboa', 889, 'SUJETO_ROL_SESION'), ('Andrés Velasco Brañes', 447, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2674]['Texto'].split()))
    def test_parent_2692_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2692]['Texto'].encode()).hexdigest(),'4c9dc196f3424759e6ed3258f6dc711bf2d4ac014fdb9ab0e20d1f512cdc181d')
        parts=self.parts(2692)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 98, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 385, 'CONTEXTO_REVISADO'), ('Sergio Lehmann Beresi', 416, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2692]['Texto'].split()))
    def test_parent_2738_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2738]['Texto'].encode()).hexdigest(),'c77c6791f2de6357fc00e6dfe4b3a8efbcde89739d90c1b37c74e1836b48e85a')
        parts=self.parts(2738)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 4743, 'SUJETO_NOMBRE'), ('José De Gregorio Rebeco', 105, 'CONTEXTO_REVISADO'), ('Claudio Soto Gamboa', 947, 'CONTEXTO_REVISADO'), ('Manuel Marfán Lewis', 401, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2738]['Texto'].split()))
    def test_parent_2740_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2740]['Texto'].encode()).hexdigest(),'7d0cbd59577b3903a6a8d96ec66f199202cb60a1cbe330121632893cfbc8a451')
        parts=self.parts(2740)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 3731, 'SUJETO_NOMBRE'), ('Andrés Velasco Brañes', 137, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 207, 'SUJETO_NOMBRE'), ('Andrés Velasco Brañes', 267, 'CONTEXTO_REVISADO'), ('Beltrán de Ramón Acevedo', 674, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2740]['Texto'].split()))
    def test_parent_2863_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2863]['Texto'].encode()).hexdigest(),'3e900aa0430e18190910f0635adc6556d09341f5ff665405a78757542314489b')
        parts=self.parts(2863)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 106, 'SUJETO_ROL_SESION'), ('Claudio Soto Gamboa', 63, 'CONTEXTO_REVISADO'), ('Claudio Soto Gamboa', 939, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2863]['Texto'].split()))
    def test_parent_2911_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2911]['Texto'].encode()).hexdigest(),'757fea8bb62ce93702579737d1bcdf1fa3098d6355a72db4084310d9ee4c9755')
        parts=self.parts(2911)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 121, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 43, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2911]['Texto'].split()))
    def test_parent_2922_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2922]['Texto'].encode()).hexdigest(),'e6c6e858397dc65aa768d976feb47dcc08939128562c07e174485853ba3f8de8')
        parts=self.parts(2922)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 97, 'SUJETO_NOMBRE'), ('Claudio Soto Gamboa', 192, 'CONTEXTO_REVISADO'), ('José De Gregorio Rebeco', 196, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2922]['Texto'].split()))
    def test_parent_2938_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2938]['Texto'].encode()).hexdigest(),'c610b7fb81b3d20dbb15bd05877e5e6dfa512c7d3cf278bdd490e175b347da5c')
        parts=self.parts(2938)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 105, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 51, 'CONTEXTO_REVISADO'), ('Manuel Marfán Lewis', 634, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2938]['Texto'].split()))
    def test_parent_3028_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3028]['Texto'].encode()).hexdigest(),'dea83bfd06c62bbd74dbabf700eea4e5b95a74c58492ce6e853e916fd1d95c36')
        parts=self.parts(3028)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 72, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 86, 'SUJETO_NOMBRE'), ('José De Gregorio Rebeco', 114, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 173, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3028]['Texto'].split()))
    def test_parent_3054_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3054]['Texto'].encode()).hexdigest(),'1c7a9459194dcc212e5dc5bc1b0dfd9a7147133ae1587a141d5cd1e2f1c9fd8f')
        parts=self.parts(3054)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 147, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 133, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3054]['Texto'].split()))
    def test_parent_3160_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3160]['Texto'].encode()).hexdigest(),'dbf7ca2fb3db855f47511f8c6a8880091ba4e3ff878d7a73fe8dc26f9eb393c0')
        parts=self.parts(3160)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 90, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 81, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3160]['Texto'].split()))
    def test_parent_3543_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3543]['Texto'].encode()).hexdigest(),'70af36c1635ca68f3ad8000ba081c841671a239bc7faf68cd5a7ce47e7145938')
        parts=self.parts(3543)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 72, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 56, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3543]['Texto'].split()))
    def test_parent_5061_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5061]['Texto'].encode()).hexdigest(),'c1dd018b7749fd85c7fd4900d39e0beb0ff54cbe7d10dc18ecbfb4981cfdf693')
        parts=self.parts(5061)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 97, 'SUJETO_ROL_NOMBRE'), ('Kevin Cowan Logan', 117, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5061]['Texto'].split()))
    def test_parent_5519_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5519]['Texto'].encode()).hexdigest(),'0e1a264e2d635821c195362bc39dede8607e5d75195995becd8156722abfec71')
        parts=self.parts(5519)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 146, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 158, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5519]['Texto'].split()))
    def test_parent_5872_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5872]['Texto'].encode()).hexdigest(),'4a7f5819440fe8c2e3b2ee86e83c4c19be37baec8cf6d2c527341cd053d4c7b8')
        parts=self.parts(5872)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 127, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 114, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5872]['Texto'].split()))
    def test_parent_6813_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[6813]['Texto'].encode()).hexdigest(),'95bd9656b1c309956ba2978a9361ad024f6349403e0b002caccbdd9258adbc98')
        parts=self.parts(6813)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 115, 'SUJETO_ROL_NOMBRE'), ('Diego Gianelli Gómez', 141, 'CONTEXTO_REVISADO'), ('Diego Gianelli Gómez', 793, 'SUJETO_NOMBRE'), ('Rodrigo Vergara Montes', 240, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6813]['Texto'].split()))
    def test_parent_7176_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[7176]['Texto'].encode()).hexdigest(),'39ff1da54432c2116084b41ece9d7cff21b0b53beeed0c1525cae2f711a634c0')
        parts=self.parts(7176)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[("Alberto Naudon Dell'Oro", 148, 'SUJETO_NOMBRE'), ('Joaquín Vial Ruiz-Tagle', 111, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[7176]['Texto'].split()))
    def test_parent_1904_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1904]['Texto'].encode()).hexdigest(),'66478e0a23cc34e2501610e55e243605202fc7b4e5f43e778523e3c4c244a174')
        parts=self.parts(1904)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Beltrán de Ramón Acevedo', 3052, 'SUJETO_ROL_NOMBRE'), ('Kevin Cowan Logan', 1358, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1904]['Texto'].split()))
    def test_parent_854_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[854]['Texto'].encode()).hexdigest(),'34fd74f84c32a553a1eca1e0048064a37f5f5784d7277d0bd9f55e59960ad50b')
        parts=self.parts(854)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 359, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[854]['Texto'].split()))
    def test_parent_1621_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1621]['Texto'].encode()).hexdigest(),'6123e205bfd4a4ea9462bba2496290120d1b8479e15998e600a4ef0ac3b9134c')
        parts=self.parts(1621)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 160, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 329, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 424, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 494, 'SUJETO_ROL_NOMBRE'), ('Andrés Velasco Brañes', 366, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1621]['Texto'].split()))
