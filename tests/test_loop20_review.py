"""LOOP20: separaciones por evidencia local, exposiciones intactas y menciones acotadas."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews,validate_speaker_reviews,speaker_intervals
from context_warnings import load_context_warnings,contextual_motives
from mention_reviews import load_mention_reviews,validate_mention_reviews,DECISION,PENDING_DECISION
from reviewed_continuity import load_reviewed_links,validate_reviewed_links
from continuity import annotate_turns

STRUCTURAL=(205,510,663,1072,1728,2695,2754,2803,2810,2836,2969,4916,5366,6021,6800,7182)
MENTIONS=(571,647,1114,1328,1338,1574,2397,2430)
class LoopTwentyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw);cls.warnings=load_context_warnings(cls.raw)
        cls.mentions=load_mention_reviews(cls.raw);cls.links=load_reviewed_links(cls.raw)
    def parts(self,p,review=True):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p) if review else None)
    def rowset(self,p):
        return [dict(ID=i,ID_Padre=p,Fecha=self.raw[p]['Fecha'],Actor_Final=a,Fuente_Actor=m,Texto=t) for i,(t,a,m) in enumerate(self.parts(p),1)]
    def test_all_seventeen_new_speaker_intervals_match_exact_output(self):
        self.assertEqual(sum(len(speaker_intervals(self.reviews[p])) for p in STRUCTURAL),17)
        for p in STRUCTURAL:self.assertFalse(validate_speaker_reviews(self.rowset(p),{p:self.reviews[p]}))
    def test_headers_require_opt_in_and_preserve_attendance_as_institutional(self):
        for p in [2803,2969]:
            self.assertEqual(len(self.parts(p,False)),1)
            first,last=self.parts(p)
            self.assertEqual(first[1],b.CONSEJO);self.assertIn('Asisten también',first[0])
            self.assertEqual(last[1],'José De Gregorio Rebeco');self.assertTrue(last[0].endswith('A continuación,.'))
    def test_header_rejects_actor_without_presidential_subject(self):
        for p in [2803,2969]:
            r=self.raw[p];e=copy.deepcopy(self.reviews[p]);e['Actor']='Claudio Soto Gamboa'
            with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)
    def test_header_rejects_partial_end_and_wrong_type(self):
        p=2803;r=self.raw[p]
        for field,value in [('Fin',len(r['Texto'])-1),('Tipo_Limite','CONCATENACION_EXPLICITA_REVISADA')]:
            e=copy.deepcopy(self.reviews[p]);e[field]=value
            with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)
    def test_header_type_cannot_be_reused_in_an_ordinary_paragraph(self):
        r=self.raw[1072];e=copy.deepcopy(self.reviews[1072]);e['Tipo_Limite']='APERTURA_POST_NOMINA_REVISADA'
        with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)
    def test_muestra_reply_requires_opt_in_separator_and_exact_predicate(self):
        p=2810;r=self.raw[p];e=copy.deepcopy(self.reviews[p])
        self.assertEqual(len(self.parts(p,False)),4);self.assertEqual(len(self.parts(p)),5)
        self.assertIn('a lo cual el señor Lehmann muestra que',self.parts(p)[1][0])
        for old,new in [('cereales, a lo cual','cereales. a lo cual'),('Lehmann muestra que','Lehmann muestra si')]:
            with self.assertRaises(ValueError):b.segment_turns(r['Texto'].replace(old,new),r['Fecha'],r['Actor'],review=e)
        e['Actor']='Enrique Marshall Rivera'
        with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)
    def test_reviewed_ends_keep_posterior_explicit_anchors(self):
        for p in [663,1728,2695,2754,2810,6800]:
            parts=self.parts(p);indices=[i for i,s in enumerate(parts) if s[2]=='CONTEXTO_REVISADO']
            i=indices[0];self.assertEqual(parts[i][1],parts[i+1][1]);self.assertIn(parts[i+1][2],b.EXPLICIT)
            e=copy.deepcopy(self.reviews[p]);e['Cita_Ancla_Posterior']='cita inexistente'
            r=self.raw[p]
            with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)
    def test_claro_long_vote_not_split_by_cowan_reference(self):
        t,a,m=self.parts(2754)[0];self.assertEqual((a,len(t)),('Sebastián Claro Edwards',7258))
        self.assertIn('Kevin Cowan',t);self.assertIn('FLAP',t)
    def test_6021_recovers_two_speakers_and_claro_return(self):
        self.assertEqual([a for t,a,m in self.parts(6021)],['Beltrán de Ramón Acevedo','Sebastián Claro Edwards','Joaquín Vial Ruiz-Tagle','Sebastián Claro Edwards'])
        self.assertIn('comienz',self.parts(6021)[0][0]);self.assertIn('lo plantado',self.parts(6021)[2][0])
    def test_4916_future_soto_presentation_is_not_a_turn(self):
        self.assertEqual([a for t,a,m in self.parts(4916)],['Rodrigo Vergara Montes','Luis Óscar Herrera Barriga','Rodrigo Vergara Montes'])
        self.assertIn('presentará',self.parts(4916)[1][0])
    def test_ten_damage_warnings_have_exact_scope(self):
        for p,n in [(205,310),(510,1165),(1013,2471),(1728,1023),(2695,192),(2803,296),(2969,301),(5366,1169),(6021,1265),(7182,214)]:
            hits=[r for r in self.rowset(p) if contextual_motives(r,self.warnings)]
            self.assertEqual(len(hits),1);self.assertEqual(len(hits[0]['Texto']),n)
        self.assertNotIn(1013,self.reviews)
    def test_eight_readings_leave_alerts_and_source_rows_untouched(self):
        for p in MENTIONS:
            rs=self.rowset(p)
            for r in rs:r['Motivos_Revision']='POSIBLE_OTRO_HABLANTE_O_MENCION'
            original=copy.deepcopy(rs);rv={k:v for k,v in self.mentions.items() if v['ID_Padre']==p}
            errors,annotations=validate_mention_reviews(rs,rv)
            self.assertFalse(errors);self.assertEqual(rs,original);self.assertEqual(len(annotations),1)
            self.assertEqual(next(iter(annotations.values()))['Estado_Lectura_Dirigida'],DECISION)
        self.assertEqual(sum(e['Decision']==DECISION for e in self.mentions.values()),73)
        self.assertEqual([e['ID_Padre'] for e in self.mentions.values() if e['Decision']==PENDING_DECISION],[6185,3775,4055,2510])
    def test_marshall_intro_joins_only_its_reviewed_next_parent(self):
        e=self.links[(2836,2837)];rs=[]
        for i,s in enumerate([e['Anterior'],e['Siguiente']],1):
            rs.append(dict(ID=i,ID_Padre=s['ID_Padre'],Fecha=e['Fecha'],Texto=s['Texto'],Actor_Final=e['Actor'],Fuente_Actor=s['Fuente_Actor'],ID_Intervencion=str(i),ID_Bloque_Texto=str(i),Tipo_Acta=None,Motivos_Revision=''))
        annotate_turns(rs,{(2836,2837):e});self.assertEqual(rs[0]['ID_Turno'],rs[1]['ID_Turno'])
        self.assertFalse(rs[0]['ID_Ancla_Actor']);self.assertEqual(rs[1]['ID_Ancla_Actor'],'2')
        self.assertFalse(validate_reviewed_links(rs,{(2836,2837):e}))
    def test_mutated_source_hash_invalidates_new_reviews(self):
        raw=copy.deepcopy(self.raw);raw[1728]['Texto']+='X'
        with self.assertRaises(ValueError):load_speaker_reviews(raw)
    def test_parent_205_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[205]['Texto'].encode()).hexdigest(),'271e73f05b0e1c1ca51892414d8396fbb16402a5c5fd26814775f0c9bf04cd5b')
        parts=self.parts(205)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Jorge Desormeaux Jiménez', 549, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 310, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 126, 'SUJETO_ROL_SESION'), ('Manuel Marfán Lewis', 1047, 'CONTEXTO_REVISADO'), ('Pablo García Silva', 442, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[205]['Texto'].split()))
    def test_parent_510_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[510]['Texto'].encode()).hexdigest(),'775e1bf088f202500936de656c605b6c97ba5a0616cfcd8314cf75f8e3e1e905')
        parts=self.parts(510)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 322, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 1165, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 593, 'CONTEXTO_REVISADO'), ('Luis Óscar Herrera Barriga', 926, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[510]['Texto'].split()))
    def test_parent_663_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[663]['Texto'].encode()).hexdigest(),'ccc4338002d194441f73af2fafb0f8fe8c48e2e64630e6dd2de3dce0c8efd7a9')
        parts=self.parts(663)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 332, 'SUJETO_ROL_NOMBRE'), ('Igal Magendzo Weinberger', 347, 'CONTEXTO_REVISADO'), ('Igal Magendzo Weinberger', 370, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 316, 'SUJETO_ROL_NOMBRE'), ('Igal Magendzo Weinberger', 661, 'SUJETO_ROL_NOMBRE'), ('Jorge Desormeaux Jiménez', 304, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 660, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[663]['Texto'].split()))
    def test_parent_1072_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1072]['Texto'].encode()).hexdigest(),'da40ba4e9559f33fe2d7f70df826682c63d0ac960359b4707072c62d9b5295eb')
        parts=self.parts(1072)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 75, 'SUJETO_ROL_NOMBRE'), ('Andrés Velasco Brañes', 245, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1072]['Texto'].split()))
    def test_parent_1728_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1728]['Texto'].encode()).hexdigest(),'668ee9f5ab48a1d2c134983ef0c9d5ffb5e68cdc71a4f446849f27a1e1db2b92')
        parts=self.parts(1728)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 75, 'SUJETO_ROL_SESION'), ('Andrés Velasco Brañes', 1023, 'CONTEXTO_REVISADO'), ('Andrés Velasco Brañes', 2296, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1728]['Texto'].split()))
    def test_parent_2695_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2695]['Texto'].encode()).hexdigest(),'bfa81120967acbf8e9dbab07daa22431b7e757a06dd82de11b6e304ff435e9cb')
        parts=self.parts(2695)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 192, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 433, 'CONTEXTO_REVISADO'), ('Claudio Soto Gamboa', 1020, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2695]['Texto'].split()))
    def test_parent_2754_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2754]['Texto'].encode()).hexdigest(),'922d6de7cf0589f5435a7d9bb7c0951e2bb84bc8929564ca81c2685c4b731db8')
        parts=self.parts(2754)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 7258, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 732, 'CONTEXTO_REVISADO'), ('Enrique Marshall Rivera', 2603, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2754]['Texto'].split()))
    def test_parent_2803_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2803]['Texto'].encode()).hexdigest(),'1e76073f6c76c3c411daef28c7c3d02f86df4d8f0c48d7900ce77f2751103726')
        parts=self.parts(2803)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Consejo del Banco Central de Chile', 1445, 'ACTA/META'), ('José De Gregorio Rebeco', 296, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2803]['Texto'].split()))
    def test_parent_2810_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2810]['Texto'].encode()).hexdigest(),'95e8b8ad1b86ae8eb71ad384cb8bbf5a82c8c4aae9b9a1c2199b3795ed88a2e8')
        parts=self.parts(2810)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 153, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 274, 'CONTEXTO_REVISADO'), ('Sergio Lehmann Beresi', 932, 'SUJETO_NOMBRE'), ('Manuel Marfán Lewis', 481, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 1812, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2810]['Texto'].split()))
    def test_parent_2836_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2836]['Texto'].encode()).hexdigest(),'b8e1229d3fd88850a01d024f907865034fe6719ad86ec1e65a19819ffcbf72af')
        parts=self.parts(2836)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 3545, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 142, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2836]['Texto'].split()))
    def test_parent_2969_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2969]['Texto'].encode()).hexdigest(),'6d0bd0ba2c0a80ddb13a27821467c07df826c44561f618f3b0216cecdb79fd30')
        parts=self.parts(2969)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Consejo del Banco Central de Chile', 1661, 'ACTA/META'), ('José De Gregorio Rebeco', 301, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2969]['Texto'].split()))
    def test_parent_4916_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4916]['Texto'].encode()).hexdigest(),'0f7647d912645c7a3c23597d06e1296bebe558f5e06fb2b1615466bbd787d6a2')
        parts=self.parts(4916)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 145, 'SUJETO_ROL_NOMBRE'), ('Luis Óscar Herrera Barriga', 341, 'CONTEXTO_REVISADO'), ('Rodrigo Vergara Montes', 237, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4916]['Texto'].split()))
    def test_parent_5366_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5366]['Texto'].encode()).hexdigest(),'f34b1fffeace930c55f3928cb5bd6f4dedd17ca9a7e7cd080a2e34887ea534b1')
        parts=self.parts(5366)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 1169, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 468, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5366]['Texto'].split()))
    def test_parent_6021_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[6021]['Texto'].encode()).hexdigest(),'5f94bcbc52e7f4cfeeb21ad26a6c28f85efd009c40ef08760fdbb445d120e9af')
        parts=self.parts(6021)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Beltrán de Ramón Acevedo', 1265, 'CONTEXTO_REVISADO'), ('Sebastián Claro Edwards', 496, 'SUJETO_ROL_NOMBRE'), ('Joaquín Vial Ruiz-Tagle', 2048, 'CONTEXTO_REVISADO'), ('Sebastián Claro Edwards', 495, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6021]['Texto'].split()))
    def test_parent_6800_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[6800]['Texto'].encode()).hexdigest(),'bb99f596feb7f1eff5a48e6f65826a9716b186e8eba27474a4e501d600e05ac9')
        parts=self.parts(6800)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 141, 'SUJETO_ROL_SESION'), ('Joaquín Vial Ruiz-Tagle', 3564, 'CONTEXTO_REVISADO'), ('Joaquín Vial Ruiz-Tagle', 151, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6800]['Texto'].split()))
    def test_parent_7182_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[7182]['Texto'].encode()).hexdigest(),'3d0eaf64127d3c0c31ca5200b826ca5ac4e9ae572595ef8ce938646c556d9e53')
        parts=self.parts(7182)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Miguel Fuentes Díaz', 2173, 'SUJETO_NOMBRE'), ('Mario Marcel Cullell', 214, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[7182]['Texto'].split()))
    def test_parent_571_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[571]['Texto'].encode()).hexdigest(),'766ad0a170656731c03760231859c0bc002f3eafa9396497abfaa09355295b47')
        parts=self.parts(571)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Jorge Desormeaux Jiménez', 4683, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[571]['Texto'].split()))
    def test_parent_647_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[647]['Texto'].encode()).hexdigest(),'ee567cbbc796e3aace9ab3a23f98f76012d1c382c4b07aeeb50100211b9faea0')
        parts=self.parts(647)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Andrés Velasco Brañes', 3785, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[647]['Texto'].split()))
    def test_parent_1114_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1114]['Texto'].encode()).hexdigest(),'c70290e218f04b18c434872dd42f06244b19ce75a5c3f9fc27f252fc24a8aa44')
        parts=self.parts(1114)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 471, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1114]['Texto'].split()))
    def test_parent_1328_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1328]['Texto'].encode()).hexdigest(),'eff768d2d36fde341af252a27fc63b4c30ae96fb0d77b875a32dad513a943143')
        parts=self.parts(1328)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Jorge Desormeaux Jiménez', 204, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1328]['Texto'].split()))
    def test_parent_1338_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1338]['Texto'].encode()).hexdigest(),'b5671da33cc8aa975aab8b5677bfd45ae12fb11d727ea7284bed516af3d068a3')
        parts=self.parts(1338)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 470, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 74, 'ACTA/META'), ('Esteban Jadresic Marinovic', 3316, 'SUJETO_ROL_NOMBRE'), ('Vittorio Corbo Lioi', 139, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1338]['Texto'].split()))
    def test_parent_1574_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1574]['Texto'].encode()).hexdigest(),'096e66bc470ff980b0641e97dd6507b8cf871e48cdc66c5c5bde567fb3ba6e40')
        parts=self.parts(1574)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 719, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 1617, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1574]['Texto'].split()))
    def test_parent_2397_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2397]['Texto'].encode()).hexdigest(),'43039a562f42e9cadfef7c063187093f63e51a5ba091a71aba36a628e397eae2')
        parts=self.parts(2397)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 1537, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2397]['Texto'].split()))
    def test_parent_2430_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2430]['Texto'].encode()).hexdigest(),'7d7271b7a5d371399e18398d62625b9fc18498fea80f59a65d74eb105f39b3ae')
        parts=self.parts(2430)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Beltrán de Ramón Acevedo', 4002, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2430]['Texto'].split()))
    def test_parent_1013_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1013]['Texto'].encode()).hexdigest(),'d6f7c23182d45ebac141a198989c60a3c0ed44c67bcd1c9ce89834edba44b264')
        parts=self.parts(1013)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Esteban Jadresic Marinovic', 997, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 1691, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 2471, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1013]['Texto'].split()))
    def test_parent_2837_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2837]['Texto'].encode()).hexdigest(),'83eab9b80b33a458e9ab4df93e33b45c0040b5e4f2028ddd9fe84844d9cd8fec')
        parts=self.parts(2837)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 5300, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2837]['Texto'].split()))
