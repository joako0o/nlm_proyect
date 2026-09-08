"""Confirmaciones, réplicas y comienzos de exposición con opt-in y alcance."""
import copy,hashlib,json,sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews,speaker_intervals,validate_speaker_reviews
from context_warnings import load_context_warnings,contextual_motives,has_context_warning
from mention_reviews import load_mention_reviews
from reviewed_continuity import load_reviewed_links
from continuity import update_state,annotate_turns
STRUCT=(1871,2027,2685,2704,2707,2723,2796,2885,2963,3051,3186,3268,3439,3646,3843,4182,4470,5168,5639,5643)
P='RESPUESTA_PASIVA_NOMINAL_REVISADA';R='RESPUESTA_LO_QUE_NOMINAL_REVISADA'
class LoopTwentyThreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw);cls.warnings=load_context_warnings(cls.raw);cls.links=load_reviewed_links(cls.raw)
    def parts(self,p,review=True):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p) if review else None)
    def changed(self,p,e,text=None):
        r=self.raw[p];return b.segment_turns(text if text is not None else r['Texto'],r['Fecha'],r['Actor'],review=e)
    def test_twenty_one_new_intervals_and_previous_2704_preserved(self):
        count=0
        for p in STRUCT:
            count+=sum('-L23-' in e['Revision_ID'] for e in speaker_intervals(self.reviews[p]))
            rows=[dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p))]
            self.assertFalse(validate_speaker_reviews(rows,{p:self.reviews[p]}))
        self.assertEqual(count,21)
        old=copy.deepcopy(self.reviews[2704]);old.pop('Revisiones_Adicionales')
        self.assertEqual(self.parts(2704)[:3],self.changed(2704,old)[:3])
    def test_passive_variants_opt_in_only(self):
        for p in [2723,3186,3843,5168,5639]:self.assertGreater(len(self.parts(p)),len(self.parts(p,False)))
        self.assertIn('lo cual es rebatido',self.parts(3843)[1][0])
        self.assertIn('Ello es corroborado',self.parts(5168)[1][0])
    def test_passive_rejects_past_voice_wrong_agent_and_separator(self):
        e=copy.deepcopy(self.reviews[2723]);t=self.raw[2723]['Texto']
        for old,new in [('es confirmado','fue confirmado'),('por el señor','para el señor'),('crisis, lo cual','crisis. lo cual')]:
            with self.assertRaises(ValueError):self.changed(2723,e,t.replace(old,new))
    def test_passive_rejects_role_only_and_unknown_agent(self):
        for body in ['lo cual es confirmado por el señor Gerente.','lo cual es confirmado por el señor Desconocido.']:
            t='El Presidente pregunta, '+body;e=dict(Actor='Sergio Lehmann Beresi',Inicio=t.index(body),Fin=len(t),Tipo_Limite=P)
            with self.assertRaises(ValueError):b.segment_turns(t,self.raw[2723]['Fecha'],'José De Gregorio Rebeco',review=e)
    def test_nominal_reply_rejects_wrong_actor_and_open_quote(self):
        for p in [1871,2723]:
            e=copy.deepcopy(self.reviews[p]);e['Actor']='Rodrigo Vergara Montes'
            with self.assertRaises(ValueError):self.changed(p,e)
            e=copy.deepcopy(self.reviews[p]);t=self.raw[p]['Texto']
            with self.assertRaises(ValueError):self.changed(p,e,'“'+t[1:])
    def test_active_relative_only_compartir_or_confirmar(self):
        self.assertEqual(len(self.parts(2027)),2)
        e=copy.deepcopy(self.reviews[2027]);t=self.raw[2027]['Texto']
        with self.assertRaises(ValueError):self.changed(2027,e,t.replace('lo que confirma','lo que recuerda'))
        with self.assertRaises(ValueError):self.changed(2027,e,t.replace('desempleo, lo que','desempleo. lo que'))
    def test_acknowledgement_variant_does_not_expand_old_rules(self):
        e=copy.deepcopy(self.reviews[2885]);e['Tipo_Limite']='CESION_AGRADECIMIENTO_RELATIVO_EXPLICITO'
        with self.assertRaises(ValueError):self.changed(2885,e)
        e=copy.deepcopy(self.reviews[2885]);e['Actor']='José De Gregorio Rebeco'
        with self.assertRaises(ValueError):self.changed(2885,e)
    def test_six_posterior_explicit_anchors_preserved(self):
        for p,n in [(1871,401),(2685,6624),(2796,5287),(2885,2400),(3439,1955),(3646,1168)]:
            ps=self.parts(p);pairs=[(x,y) for x,y in zip(ps,ps[1:]) if x[2]=='CONTEXTO_REVISADO' and x[1]==y[1] and y[2] in b.EXPLICIT]
            self.assertEqual(len(pairs),1);self.assertEqual(len(pairs[0][1][0]),n)
            e=copy.deepcopy(self.reviews[p]);e['Cita_Ancla_Posterior']='bad'
            with self.assertRaises(ValueError):self.changed(p,e)
    def test_contextual_speakers_never_become_global_anchors(self):
        for p in STRUCT:
            for t,a,m in self.parts(p):
                if m=='CONTEXTO_REVISADO':
                    state={};update_state(state,a,m,t,self.raw[p]['Fecha'],b.TURN_DETECTOR,b.split_sentences,'reviewed')
                    self.assertFalse(state['anchor'])
    def test_two_bounded_links_preserve_physical_text_and_explicit_anchor(self):
        for key in [(2707,2708),(2963,2964)]:
            e=self.links[key];rows=[]
            for i,side in enumerate([e['Anterior'],e['Siguiente']],1):
                rows.append(dict(ID=i,ID_Padre=side['ID_Padre'],Fecha=e['Fecha'],Texto=side['Texto'],Actor_Final=e['Actor'],Fuente_Actor=side['Fuente_Actor'],ID_Intervencion=str(i),ID_Bloque_Texto=str(i),Tipo_Acta=None,Motivos_Revision=''))
            text=[r['Texto'] for r in rows];annotate_turns(rows,{key:e})
            self.assertEqual(rows[0]['ID_Turno'],rows[1]['ID_Turno']);self.assertEqual(text,[r['Texto'] for r in rows])
            self.assertFalse(rows[0]['ID_Ancla_Actor']);self.assertEqual(rows[1]['ID_Ancla_Actor'],'2')
    def test_old_2704_warning_archived_and_not_reactivated(self):
        self.assertNotIn(2704,self.warnings)
        archive=json.loads(Path('data/curation/alertas_contextuales_retiradas.json').read_text());self.assertEqual(len(archive),3)
        e=next(e for e in archive if e['Alerta_Original']['ID_Padre']==2704)
        self.assertEqual(e['Alerta_Original']['Revision_ID'],'ALERTA-20260908-L12-2704')
        self.assertEqual(e['Alerta_Original']['Texto_Intervalo'],' '.join(t for t,a,m in self.parts(2704)[-2:]))
        self.assertEqual(e['Revisiones_Sustitutas'],[self.reviews[2704]['Revisiones_Adicionales'][0]['Revision_ID']])
        self.assertNotIn(6443,self.warnings)
    def test_pending_cerda_is_not_legitimate_mention_or_ocr_damage(self):
        self.assertNotIn(3775,self.reviews);self.assertEqual(self.parts(3775),self.parts(3775,False))
        self.assertEqual(self.warnings[3775]['Motivo'],'HABLANTES_POR_DELIMITAR')
        self.assertTrue(has_context_warning('HABLANTES_POR_DELIMITAR'))
        ms=load_mention_reviews(self.raw)
        self.assertEqual({e['ID_Padre'] for e in ms.values() if e['Decision']=='PENDIENTE_DELIMITAR_APORTE'},{6185,3775,4055})
        self.assertEqual(len(ms),35)
    def test_past_reported_relatives_not_current_speakers(self):
        for p in [1926,4161]:
            self.assertNotIn(p,self.reviews);self.assertEqual(len(self.parts(p)),1)
            self.assertEqual(self.parts(p),self.parts(p,False));self.assertEqual(self.parts(p)[0][1],'José De Gregorio Rebeco')
    def test_four_warnings_match_only_their_rows(self):
        for p,n in [(2885,2400),(3268,688),(3775,440),(5643,162)]:
            hits=[t for t,a,m in self.parts(p) if contextual_motives(dict(ID_Padre=p,Fecha=self.raw[p]['Fecha'],Actor_Final=a,Texto=t),self.warnings)]
            self.assertEqual(len(hits),1);self.assertEqual(len(hits[0]),n)
    def test_long_expositions_and_literal_short_confirmations_retained(self):
        for p,n in [(2685,6624),(2796,5287),(2708,6092),(2964,6048)]:self.assertTrue(any(len(t)==n for t,a,m in self.parts(p)))
        for p,n in [(2704,48),(2723,43),(3051,40),(3186,47),(4470,43)]:self.assertTrue(any(len(t)==n and m=='CONTEXTO_REVISADO' for t,a,m in self.parts(p)))
        self.assertTrue(self.parts(3268)[-1][0].endswith('No habiendo más comentarios,.'))
    def test_source_mutation_rejected(self):
        raw=copy.deepcopy(self.raw);raw[2704]['Texto']+='X'
        with self.assertRaises(ValueError):load_speaker_reviews(raw)
    def test_parent_1871_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1871]['Texto'].encode()).hexdigest(),'90c9661e04af4f00dc1ec77663bf1f1b899069663a251bf79b603a34e596f147')
        parts=self.parts(1871)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 123, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 148, 'CONTEXTO_REVISADO'), ('Sergio Lehmann Beresi', 401, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 192, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1871]['Texto'].split()))
    def test_parent_2027_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2027]['Texto'].encode()).hexdigest(),'ec828c142ff8416a1ccabb28ecfaac6c9a2c30c3428472e17562e47b1ad618f2')
        parts=self.parts(2027)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Jorge Desormeaux Jiménez', 153, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 65, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2027]['Texto'].split()))
    def test_parent_2685_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2685]['Texto'].encode()).hexdigest(),'ed325da268fbcfefc2a16b5313ab78d759fb444086753baa93cba09b74d52d19')
        parts=self.parts(2685)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 3300, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 139, 'CONTEXTO_REVISADO'), ('Enrique Marshall Rivera', 6624, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2685]['Texto'].split()))
    def test_parent_2704_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2704]['Texto'].encode()).hexdigest(),'1b67ddf55051af63a23c5ac9d1b0bcdab007b6a164bd979c55e116b2ca631ff9')
        parts=self.parts(2704)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Beltrán de Ramón Acevedo', 658, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 66, 'CONTEXTO_REVISADO'), ('Beltrán de Ramón Acevedo', 273, 'SUJETO_NOMBRE'), ('Enrique Marshall Rivera', 161, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 48, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2704]['Texto'].split()))
    def test_parent_2707_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2707]['Texto'].encode()).hexdigest(),'bf565a96234d9becf62acfb1bc905c781e8bc86fbacf79e09dc7d5de2e98a3c4')
        parts=self.parts(2707)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 3973, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 139, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2707]['Texto'].split()))
    def test_parent_2723_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2723]['Texto'].encode()).hexdigest(),'6c1656ea79dfc8aadf22e55e2946240537ea41123a38381ac103d4c164474988')
        parts=self.parts(2723)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Jorge Desormeaux Jiménez', 284, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 43, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2723]['Texto'].split()))
    def test_parent_2796_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2796]['Texto'].encode()).hexdigest(),'d6eaa426df05adaf0e0c2ea82e392b02032cce05bc4fec86b388d2d0fcd311fa')
        parts=self.parts(2796)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 5097, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 343, 'CONTEXTO_REVISADO'), ('Enrique Marshall Rivera', 5287, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2796]['Texto'].split()))
    def test_parent_2885_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2885]['Texto'].encode()).hexdigest(),'6faf2896f7f4092243cdaaec6972b86807b1bcc205912dabe81816183624ab6f')
        parts=self.parts(2885)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 78, 'SUJETO_ROL_SESION'), ('Manuel Marfán Lewis', 165, 'CONTEXTO_REVISADO'), ('Manuel Marfán Lewis', 2400, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2885]['Texto'].split()))
    def test_parent_2963_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2963]['Texto'].encode()).hexdigest(),'5567715eb46c86e662055abeefb12a1ebca409436b0855cca660939b99647e8d')
        parts=self.parts(2963)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 4568, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 166, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2963]['Texto'].split()))
    def test_parent_3051_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3051]['Texto'].encode()).hexdigest(),'cd1706769a902c4ffc65b86187964e3a837deb0d81887164c950004e6775c149')
        parts=self.parts(3051)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 188, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 40, 'CONTEXTO_REVISADO'), ('Manuel Marfán Lewis', 291, 'SUJETO_NOMBRE'), ('Claudio Soto Gamboa', 1705, 'SUJETO_NOMBRE'), ('Pablo García Silva', 296, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3051]['Texto'].split()))
    def test_parent_3186_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3186]['Texto'].encode()).hexdigest(),'65a440f8ebabefcb64efd154c3e8bc226708372a0611c86f931a7f47e7e71a77')
        parts=self.parts(3186)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 108, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 47, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3186]['Texto'].split()))
    def test_parent_3268_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3268]['Texto'].encode()).hexdigest(),'ab4d4c2de94f94b06e0f718a60498c38f7f8b33a07f53fa751ae73338d5f974d')
        parts=self.parts(3268)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 388, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 47, 'CONTEXTO_REVISADO'), ('Manuel Marfán Lewis', 572, 'CONTEXTO_REVISADO'), ('Pablo García Silva', 688, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3268]['Texto'].split()))
    def test_parent_3439_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3439]['Texto'].encode()).hexdigest(),'af8af8bbb415f9946753f73e005344afa9b802348263a68a8868921bc9f8e1c9')
        parts=self.parts(3439)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Beltrán de Ramón Acevedo', 152, 'SUJETO_ROL_NOMBRE'), ('Felipe Jaque', 390, 'CONTEXTO_REVISADO'), ('Felipe Jaque', 1955, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3439]['Texto'].split()))
    def test_parent_3646_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3646]['Texto'].encode()).hexdigest(),'814cf096601a91a0820c3a5d75b7811bcd0847ef1ff182490537520175ba1866')
        parts=self.parts(3646)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 233, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 84, 'CONTEXTO_REVISADO'), ('Sergio Lehmann Beresi', 1168, 'SUJETO_NOMBRE'), ('Sebastián Claro Edwards', 98, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3646]['Texto'].split()))
    def test_parent_3843_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3843]['Texto'].encode()).hexdigest(),'836754415e1b53d602e81a5f4b72f762061731208aaf1f80bce8e096cfeaf38e')
        parts=self.parts(3843)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 293, 'SUJETO_ROL_NOMBRE'), ('Luis Óscar Herrera Barriga', 130, 'CONTEXTO_REVISADO'), ('Enrique Marshall Rivera', 244, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3843]['Texto'].split()))
    def test_parent_4182_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4182]['Texto'].encode()).hexdigest(),'41b0815e44cf335ab40fcb0b28d749a55be9c6b642a0063ed33b73ea0058780c')
        parts=self.parts(4182)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 114, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 182, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4182]['Texto'].split()))
    def test_parent_4470_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4470]['Texto'].encode()).hexdigest(),'f3126dd95e950b2596e2405c74085bdc3731fcc05842ec25c6acd700013550a1')
        parts=self.parts(4470)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 132, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 43, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4470]['Texto'].split()))
    def test_parent_5168_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5168]['Texto'].encode()).hexdigest(),'f60e1de9b4fde7a0e4e993f2528427b6c6d794c1a10e4942eb2cb6738898ac07')
        parts=self.parts(5168)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 187, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 178, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5168]['Texto'].split()))
    def test_parent_5639_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5639]['Texto'].encode()).hexdigest(),'5d084c290d4085c96a520ca38de79ec0b1e166079d6bb2be5c079a8bcb4cd896')
        parts=self.parts(5639)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 234, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 706, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5639]['Texto'].split()))
    def test_parent_5643_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5643]['Texto'].encode()).hexdigest(),'f8078bfaacc4be58cba84bad406feda84e9ef0876478d6d5bcaada03ee1b890a')
        parts=self.parts(5643)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 162, 'SUJETO_ROL_NOMBRE'), ('Joaquín Vial Ruiz-Tagle', 261, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 50, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5643]['Texto'].split()))
    def test_parent_2708_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2708]['Texto'].encode()).hexdigest(),'301b800fc275f537511e12bfb559984ce429a3cac175f04459298938d30b6e55')
        parts=self.parts(2708)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 6092, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2708]['Texto'].split()))
    def test_parent_2964_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2964]['Texto'].encode()).hexdigest(),'13a5691d5dda81a9fe178ed3b9c098ed7842a7a672ef2039eff8cce2a89615ee')
        parts=self.parts(2964)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 6048, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2964]['Texto'].split()))
    def test_parent_3775_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3775]['Texto'].encode()).hexdigest(),'efc7ea6aa75fa4b21ad023b66e2b2591557bc4266f130bd44428582b35cbcb9c')
        parts=self.parts(3775)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 440, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3775]['Texto'].split()))
    def test_parent_1926_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1926]['Texto'].encode()).hexdigest(),'d754ac7e0a06f23d332b3b73c0e784f1b673fdd0ecf938c39f8f23562f968429')
        parts=self.parts(1926)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 228, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1926]['Texto'].split()))
    def test_parent_4161_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4161]['Texto'].encode()).hexdigest(),'bec89b775709961c221443ac4c10ca0d18f9b603de85b2c77518ad29fc374a67')
        parts=self.parts(4161)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 226, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4161]['Texto'].split()))
