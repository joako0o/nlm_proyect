"""LOOP32: referencias no son turnos; advertencias no se cierran por proximidad."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, text_hash
from mention_reviews import load_mention_reviews, validate_mention_reviews
from context_warnings import load_context_warnings, contextual_motives
from reviewed_continuity import load_reviewed_links
from continuity import annotate_turns, update_state

ROOT=Path(__file__).resolve().parents[1]
MENTIONS=(79,81,95,511,578,611,628,665,666,681,689,695,749,3102,3362,3473,3536,3655,4153,5578,6156,6250,6456,6533,7096)
PAIRS=((1904,1905),(2788,2789),(2803,2804),(2969,2970))
def compact(t):return ''.join(t.split())
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

class LoopThirtyTwoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.speakers=load_speaker_reviews(cls.raw)
        cls.mentions=load_mention_reviews(cls.raw)
        cls.warnings=load_context_warnings(cls.raw)
        cls.links=load_reviewed_links(cls.raw)

    def parts(self,p):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.speakers.get(p))

    def rows(self,parents):
        result=[]
        for p in parents:
            for i,(text,actor,source) in enumerate(self.parts(p),1):
                row=dict(ID=len(result)+1,ID_Padre=p,Fecha=self.raw[p]['Fecha'],Texto=text,Actor_Final=actor,
                    Fuente_Actor=source,Tipo_Acta='ACTA_INSTITUCIONAL' if actor==b.CONSEJO else '',
                    ID_Intervencion=f'{p}:{i}',ID_Bloque_Texto=f'{p}:{i}',Motivos_Revision='')
                row['Motivos_Revision']=';'.join(contextual_motives(row,self.warnings));result.append(row)
        return result

    def test_twenty_five_exact_readings_never_modify_rows(self):
        for p in MENTIONS:
            rows=self.rows([p]);before=copy.deepcopy(rows)
            rv={k:e for k,e in self.mentions.items() if e['ID_Padre']==p and '-L32-' in k}
            self.assertEqual(len(rv),1)
            errors,annotations=validate_mention_reviews(rows,rv)
            self.assertFalse(errors);self.assertEqual(len(annotations),1);self.assertEqual(rows,before)
            self.assertEqual(next(iter(annotations.values()))['Estado_Lectura_Dirigida'],'MENCION_LEGITIMA_REVISADA')

    def test_reading_invalidated_by_actor_text_or_date_change(self):
        for p in MENTIONS:
            rv={k:e for k,e in self.mentions.items() if e['ID_Padre']==p and '-L32-' in k}
            rows=self.rows([p]);_,annotations=validate_mention_reviews(rows,rv);rid=next(iter(annotations))
            for key,value in [('Actor_Final',b.CONSEJO),('Texto','otra cosa'),('Fecha','1900-01-01')]:
                altered=copy.deepcopy(rows);next(r for r in altered if r['ID']==rid)[key]=value
                self.assertTrue(validate_mention_reviews(altered,rv)[0])

    def test_new_source_hash_and_limit_guards(self):
        for p in MENTIONS:
            e=next(e for e in self.mentions.values() if e['ID_Padre']==p)
            for field,value in [('SHA256_Texto_Padre','0'*64),('Inicio',-1),('Fin',0),('Cita_Inicio','inventada')]:
                changed=copy.deepcopy(e);changed[field]=value
                with tempfile.TemporaryDirectory() as d:
                    path=Path(d)/'m.json';path.write_text(json.dumps([changed]))
                    with self.assertRaises(ValueError):load_mention_reviews(self.raw,path)

    def test_questions_do_not_give_the_floor_to_the_addressee(self):
        self.assertEqual([a for t,a,m in self.parts(578)],['Nicolás Eyzaguirre Guzmán','Pablo García Silva'])
        self.assertEqual([a for t,a,m in self.parts(611)],['Vittorio Corbo Lioi','Manuel Marfán Lewis'])
        self.assertEqual([a for t,a,m in self.parts(6156)],['Matías Bernier Bórquez','Rodrigo Vergara Montes'])
        self.assertNotIn('Claudio Raddatz Kiefer',[a for t,a,m in self.parts(6156)])

    def test_soto_return_is_not_fused_across_de_ramon(self):
        rows=annotate_turns(self.rows([3102]))
        self.assertEqual([r['Actor_Final'] for r in rows],['Claudio Soto Gamboa','Beltrán de Ramón Acevedo','Claudio Soto Gamboa'])
        self.assertEqual(len({r['ID_Turno'] for r in rows}),3)
        self.assertEqual(rows[-1]['ID_Ancla_Actor'],rows[-1]['ID_Intervencion'])

    def test_complements_are_not_joint_or_previous_speaker(self):
        expected={3362:'Luis Felipe Céspedes Cifuentes',3655:'Sergio Lehmann Beresi',
                  4153:'Sergio Lehmann Beresi',5578:'Sergio Lehmann Beresi',
                  6456:'Joaquín Vial Ruiz-Tagle',6533:'Pablo García Silva',7096:"Alberto Naudon Dell'Oro"}
        for p,actor in expected.items():
            self.assertEqual(len(self.parts(p)),2);self.assertEqual(self.parts(p)[1][1],actor)
        self.assertEqual(len(self.parts(3473)),1);self.assertEqual(self.parts(3473)[0][1],'Manuel Marfán Lewis')

    def test_announcement_presentation_and_arrival_with_apology_are_distinct(self):
        self.assertEqual([len(t) for t,a,m in self.parts(628)],[283,3269])
        self.assertEqual(self.parts(628)[0][1],'Vittorio Corbo Lioi')
        self.assertEqual(self.parts(628)[1][1],'Sergio Lehmann Beresi')
        self.assertIn('estará a cargo',self.parts(628)[0][0])
        self.assertIn('Sergio Lehmman',self.parts(628)[1][0])
        self.assertEqual(self.parts(629)[0][1:],('Andrés Velasco Brañes','CONTEXTO_REVISADO'))
        self.assertIn('formula sus excusas',self.parts(629)[0][0])
        self.assertIn('octubre de 2006',self.raw[627]['Texto'])

    def test_three_lexical_warnings_preserve_exact_source_and_other_speakers(self):
        for p,index,quote in [(665,0,'en lo cambiarlo'),(6250,0,'riego de mercado'),(6456,1,'inversión se este sector')]:
            rows=self.rows([p]);self.assertIn(quote,rows[index]['Texto'])
            self.assertEqual([i for i,r in enumerate(rows) if r['Motivos_Revision']],[index])
            rv={k:e for k,e in self.mentions.items() if e['ID_Padre']==p}
            errors,annotations=validate_mention_reviews(rows,rv)
            self.assertFalse(errors);self.assertIn(rows[index]['ID'],annotations)
            self.assertEqual(rows[index]['Motivos_Revision'],'TEXTO_DANADO_POR_COTEJAR')
            altered=copy.deepcopy(rows[index]);altered['Texto']+='!'
            self.assertFalse(contextual_motives(altered,self.warnings))
        self.assertEqual(self.parts(6456)[0][1],'Pablo García Silva')
        self.assertEqual(len(self.parts(6456)[0][0]),828)

    def test_pending_readings_not_closed(self):
        for p in [6185,3775,4055,2510]:
            e=next(e for e in self.mentions.values() if e['ID_Padre']==p)
            self.assertEqual(e['Decision'],'PENDIENTE_DELIMITAR_APORTE')

    def test_four_candidate_links_are_not_forced(self):
        for pair in PAIRS:
            self.assertNotIn(pair,self.links)
            rows=annotate_turns(self.rows(pair));left=[r for r in rows if r['ID_Padre']==pair[0]][-1];right=next(r for r in rows if r['ID_Padre']==pair[1])
            self.assertEqual(left['Actor_Final'],right['Actor_Final'])
            self.assertNotEqual(left['ID_Turno'],right['ID_Turno'])
            self.assertTrue(left['Motivos_Revision'])
            self.assertFalse(left['ID_Ancla_Actor']);self.assertFalse(right['ID_Antecedente_Continuidad'])
            self.assertEqual(right['ID_Ancla_Actor'],right['ID_Intervencion'])
            state={};update_state(state,left['Actor_Final'],left['Fuente_Actor'],left['Texto'],left['Fecha'],b.TURN_DETECTOR,b.split_sentences,'review')
            self.assertFalse(state['anchor'])
            proposal=dict(Revision_ID='NO_REGISTRADA',Fecha=left['Fecha'],Actor=left['Actor_Final'],
                Anterior={k:left[k] for k in ['ID_Padre','Texto','Fuente_Actor']},
                Siguiente={k:right[k] for k in ['ID_Padre','Texto','Fuente_Actor']})
            with self.assertRaisesRegex(ValueError,'barrera'):annotate_turns(self.rows(pair),{pair:proposal})

    def test_warning_scope_does_not_absorb_whole_mixed_parent(self):
        for p in [1904,2788,2803,2969]:
            rows=self.rows([p]);self.assertEqual(sum(bool(r['Motivos_Revision']) for r in rows),1)
        self.assertEqual(self.parts(1904)[0][1],'Beltrán de Ramón Acevedo')
        self.assertEqual(self.parts(1904)[-1][1],'Kevin Cowan Logan')
        self.assertIn('■J',self.parts(1904)[0][0])

# Frozen source/signature and registry tests follow.

    def test_parent_79_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[79]['Texto']),'4bf402e18d2abd46a28fdb9dfaa8e75048709846a62c0cd3c50888640962d635')
        parts=self.parts(79)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Esteban Jadresic Marinovic', 1011, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[79]['Texto']))

    def test_parent_81_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[81]['Texto']),'f90369e73f9c615d024061e1f00d851e9f6c5badf8d839df77fda14d16d05dce')
        parts=self.parts(81)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Jorge Desormeaux Jiménez', 767, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[81]['Texto']))

    def test_parent_95_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[95]['Texto']),'ba3292ee22df2c45a1cb7e0752e1882a90f6e9d249b4f585b1853cf1e98d07bc')
        parts=self.parts(95)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Jorge Desormeaux Jiménez', 501, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[95]['Texto']))

    def test_parent_511_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[511]['Texto']),'0a1a01de3948b47ebeda900a41debcc38c59778b83f6a216ca1b1963b66c2ff4')
        parts=self.parts(511)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 338, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[511]['Texto']))

    def test_parent_578_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[578]['Texto']),'bb2360d12308663e70a44a986f876bf06f171e6947b6f351204010e567b82de6')
        parts=self.parts(578)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Nicolás Eyzaguirre Guzmán', 184, 'SUJETO_ROL_SESION'), ('Pablo García Silva', 820, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[578]['Texto']))

    def test_parent_611_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[611]['Texto']),'506808126aad889a3203d3bdcf86c2d5a5485cd256a6eb98f6086b447ae3a062')
        parts=self.parts(611)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 275, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 484, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[611]['Texto']))

    def test_parent_627_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[627]['Texto']),'56ab7ca55941c1723308f735ded7b4d69dd91bf2abe6d5cf9f07996b0eaddd43')
        parts=self.parts(627)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 123, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[627]['Texto']))

    def test_parent_628_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[628]['Texto']),'ef34b9076d7d07320631637be15569ddafefe950a3e089089c95df1f26499710')
        parts=self.parts(628)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 283, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 3269, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[628]['Texto']))

    def test_parent_629_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[629]['Texto']),'6b058534cb3ae325d2a27064d126abbb68b569db67b451d88b655f5c3c09e6ce')
        parts=self.parts(629)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Andrés Velasco Brañes', 248, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[629]['Texto']))

    def test_parent_665_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[665]['Texto']),'613c0ca3af23b863525c95d84f22a7ed7853b352a84fce0b80e119b26841b8cb')
        parts=self.parts(665)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Klaus Schmidt-Hebbel Dunker', 1328, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[665]['Texto']))

    def test_parent_666_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[666]['Texto']),'a1f13f9dcbc9fcffe0782e74a6e8b225393389e919a31bfd974295abe38421e8')
        parts=self.parts(666)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Esteban Jadresic Marinovic', 1608, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[666]['Texto']))

    def test_parent_681_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[681]['Texto']),'3a98d28dc0aa362933f77f67a5f4cc9b956ddebeaad2ef6db53c9cdb1be79cf1')
        parts=self.parts(681)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Jorge Desormeaux Jiménez', 383, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[681]['Texto']))

    def test_parent_689_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[689]['Texto']),'184379ffc702c36a9025a821f7d880f5bbc64ff516db36ea6cb6f7e860a69feb')
        parts=self.parts(689)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Klaus Schmidt-Hebbel Dunker', 480, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[689]['Texto']))

    def test_parent_695_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[695]['Texto']),'e0f6d7ac86f60bdce7fd1acb8fea133adfad56a1442e8e40f594961f651e16d5')
        parts=self.parts(695)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 611, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[695]['Texto']))

    def test_parent_749_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[749]['Texto']),'e3895e632f14c1e75c11fce3fa4dabffdbbfa11e86170e3ad4650728cc7944e6')
        parts=self.parts(749)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Andrés Velasco Brañes', 771, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[749]['Texto']))

    def test_parent_1904_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[1904]['Texto']),'66478e0a23cc34e2501610e55e243605202fc7b4e5f43e778523e3c4c244a174')
        parts=self.parts(1904)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Beltrán de Ramón Acevedo', 3052, 'SUJETO_ROL_NOMBRE'), ('Kevin Cowan Logan', 1358, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[1904]['Texto']))

    def test_parent_1905_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[1905]['Texto']),'6994287186d6bcbbcd598a3b95b9ec3ab2a80c78f9b1768fe068cd96aee8033e')
        parts=self.parts(1905)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Kevin Cowan Logan', 1295, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[1905]['Texto']))

    def test_parent_2788_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[2788]['Texto']),'01401cf1a5883b177d14025bb3c371eb389bada960e5c62511165ffeeee87131')
        parts=self.parts(2788)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 126, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 182, 'CONTEXTO_REVISADO'), ('Consejo del Banco Central de Chile', 74, 'ACTA/META'), ('José De Gregorio Rebeco', 191, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 407, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2788]['Texto']))

    def test_parent_2789_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[2789]['Texto']),'84f2529bfcb40874474af6878f210ba1a6010bef4c251b30230ef773c90f8dc5')
        parts=self.parts(2789)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 3081, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2789]['Texto']))

    def test_parent_2803_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[2803]['Texto']),'1e76073f6c76c3c411daef28c7c3d02f86df4d8f0c48d7900ce77f2751103726')
        parts=self.parts(2803)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Consejo del Banco Central de Chile', 1445, 'ACTA/META'), ('José De Gregorio Rebeco', 296, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2803]['Texto']))

    def test_parent_2804_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[2804]['Texto']),'cddc49a5deac614ded108f169e1f298b2989a52994dc063205eb82989a1643eb')
        parts=self.parts(2804)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 158, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2804]['Texto']))

    def test_parent_2969_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[2969]['Texto']),'6d0bd0ba2c0a80ddb13a27821467c07df826c44561f618f3b0216cecdb79fd30')
        parts=self.parts(2969)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Consejo del Banco Central de Chile', 1661, 'ACTA/META'), ('José De Gregorio Rebeco', 301, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2969]['Texto']))

    def test_parent_2970_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[2970]['Texto']),'843b97726ac25352348068b2bbebd306a45576eeb51a25d4cf02024205aa7a1f')
        parts=self.parts(2970)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 158, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 1318, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2970]['Texto']))

    def test_parent_3102_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[3102]['Texto']),'193195672819a3269f7a68255cf0837aa3b11a430f57a53582dbcad07b8ec680')
        parts=self.parts(3102)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 851, 'SUJETO_NOMBRE'), ('Beltrán de Ramón Acevedo', 443, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 279, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3102]['Texto']))

    def test_parent_3362_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[3362]['Texto']),'939dcfd23ff4a651fe061898349e508c6433d063b38b1f0cb6d034762cbf8fac')
        parts=self.parts(3362)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 150, 'SUJETO_ROL_NOMBRE'), ('Luis Felipe Céspedes Cifuentes', 291, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3362]['Texto']))

    def test_parent_3473_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[3473]['Texto']),'c03fa580e2e237483bd5cbb34e226f2f3dd0140c2f40a6dcb13d40886faa3244')
        parts=self.parts(3473)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 767, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3473]['Texto']))

    def test_parent_3536_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[3536]['Texto']),'df0d6be7dbf35afbc0f25fcfc7a38dbfe7905374dd8f1d7e66ded879338818c0')
        parts=self.parts(3536)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 710, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3536]['Texto']))

    def test_parent_3655_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[3655]['Texto']),'5f7db60c2d5eac256e51a4c5f0cc03478f74d0e261e074ffde0c457ea8219f80')
        parts=self.parts(3655)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 366, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 218, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3655]['Texto']))

    def test_parent_4153_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[4153]['Texto']),'da7be869a885800cf3015e7a64ef0bfac816b947ee2e14961d888d8d960d6359')
        parts=self.parts(4153)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 533, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 409, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[4153]['Texto']))

    def test_parent_5578_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[5578]['Texto']),'5de6c365d9b12fdcbf53e4f0e99e1d02ea54e5ce34c8b40a9b0757b3e99a3e12')
        parts=self.parts(5578)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 378, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 271, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[5578]['Texto']))

    def test_parent_6156_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[6156]['Texto']),'3d31c3903f72d575ad6c48792376fb552baa0184f7c6ce08f5a1809aa6bd4389')
        parts=self.parts(6156)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Matías Bernier Bórquez', 392, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Vergara Montes', 162, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6156]['Texto']))

    def test_parent_6250_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[6250]['Texto']),'94255276976e308f0902aad419394fe8d6c50c4a10b51e5d9595ee59ea3f530a')
        parts=self.parts(6250)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Beltrán de Ramón Acevedo', 1479, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6250]['Texto']))

    def test_parent_6456_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[6456]['Texto']),'2cf01efe8f76c5b08f445bd3650fba098de46d4c849f34b0cf2279b9efed120a')
        parts=self.parts(6456)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Pablo García Silva', 828, 'SUJETO_ROL_NOMBRE'), ('Joaquín Vial Ruiz-Tagle', 394, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6456]['Texto']))

    def test_parent_6533_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[6533]['Texto']),'cd39902dc10132ce9de0fce2a1978450d00e27461d2b80fca35d52d2140d8c9a')
        parts=self.parts(6533)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 316, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 399, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6533]['Texto']))

    def test_parent_7096_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[7096]['Texto']),'90ba82a97b53aedf1f1aef9a715d5ddfa55507d14a2364aed372305e7a7f52a0')
        parts=self.parts(7096)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Raddatz Kiefer', 720, 'SUJETO_NOMBRE'), ("Alberto Naudon Dell'Oro", 772, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[7096]['Texto']))

    def test_frozen_revisiones_hablantes_prefix(self):
        es=json.loads((ROOT/'data/curation/revisiones_hablantes.json').read_text())
        self.assertEqual(digest(es[:353]),'9be4c82a8a5202268bb6c9e35f04c84ecea9436da98cd5784285d1a8ac33e803')

    def test_frozen_alertas_contextuales_prefix(self):
        es=json.loads((ROOT/'data/curation/alertas_contextuales.json').read_text())
        self.assertEqual(digest(es[:81]),'b7a5c9d8d9f943291c354fa30ad2519b659c0b2c06210031499f5c6200cfe2d5')

    def test_frozen_revisiones_menciones_actuales_prefix(self):
        es=json.loads((ROOT/'data/curation/revisiones_menciones_actuales.json').read_text())
        self.assertEqual(digest(es[:77]),'96f0f768ca47a908158b53e17d9f01af84c7f18820697dcbd809c722bffd0b30')

    def test_frozen_revisiones_continuidad_hablantes_prefix(self):
        es=json.loads((ROOT/'data/curation/revisiones_continuidad_hablantes.json').read_text())
        self.assertEqual(digest(es[:24]),'018b71de71c52b50063c25ff74df9d712bb6d5eae62e0a571f14ca132fc76b9e')

    def test_frozen_revisiones_documentos_leidos_prefix(self):
        es=json.loads((ROOT/'data/curation/revisiones_documentos_leidos.json').read_text())
        self.assertEqual(digest(es[:12]),'b189d3c4e3f462c05c842650ab5f9608b2cbb2491f033e72c6960defaee5fe0c')

    def test_frozen_revisiones_continuaciones_acta_prefix(self):
        es=json.loads((ROOT/'data/curation/revisiones_continuaciones_acta.json').read_text())
        self.assertEqual(digest(es[:4]),'f77ea02478b722942ef9279ce55176a3a9036d2ae466f0fbdf5d3b3221b93cfa')

    def test_frozen_alertas_contextuales_retiradas_prefix(self):
        es=json.loads((ROOT/'data/curation/alertas_contextuales_retiradas.json').read_text())
        self.assertEqual(digest(es[:3]),'c0ad72321cd33d5b32dc7798ecdcdbb9fd473797e4e2fea992270d3c7caae6c5')

if __name__ == "__main__":
    unittest.main()
