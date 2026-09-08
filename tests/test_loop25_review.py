"""LOOP25: intervenciones omitidas y opiniones recibidas para lectura por tercero."""
import copy,hashlib,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews,speaker_intervals,validate_speaker_reviews
from context_warnings import load_context_warnings,contextual_motives
from mention_reviews import load_mention_reviews
from document_reviews import load_document_reviews,AUTHOR_SOURCE,READER_SOURCE,PATH as DOC_PATH
from continuity import update_state
PERSONAL=(586,1627,1680,2698,2918,2948,4926,6073)
DOCUMENTS=(4453,4507,4722)
class LoopTwentyFiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw);cls.docs=load_document_reviews(cls.raw);cls.warnings=load_context_warnings(cls.raw)
    def parts(self,p,review=True):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p) if review else None,document=self.docs.get(p) if review else None)
    def load_docs(self,entries,raw=None):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'docs.json';p.write_text(json.dumps(entries))
            return load_document_reviews(raw if raw is not None else self.raw,p)
    def test_eight_personal_intervals_survive_and_never_anchor_globally(self):
        self.assertEqual(sum('-L25-' in e['Revision_ID'] for p in PERSONAL for e in speaker_intervals(self.reviews[p])),8)
        for p in PERSONAL:
            rows=[dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p))]
            self.assertEqual(validate_speaker_reviews(rows,{p:self.reviews[p]}),[])
            for t,a,m in self.parts(p):
                if m=='CONTEXTO_REVISADO':
                    state={};update_state(state,a,m,t,self.raw[p]['Fecha'],b.TURN_DETECTOR,b.split_sentences,'reviewed');self.assertFalse(state['anchor'])
    def test_nominal_confirmation_is_opt_in_and_preserves_gerund(self):
        self.assertEqual(len(self.parts(2918,False)),1)
        self.assertEqual(self.parts(2918)[1][1],'Claudio Soto Gamboa')
        self.assertTrue(self.parts(2918)[1][0].startswith('confirmando el señor Soto que'))
    def test_confirmation_rejects_wrong_actor_past_role_only_and_quote(self):
        p=2918;r=self.raw[p];entry=self.reviews[p]
        prefix=r['Texto'][:entry['Inicio']];fragment=r['Texto'][entry['Inicio']:]
        cases=[(prefix,fragment,'Rodrigo Vergara Montes'),(prefix,fragment.replace('confirmando','habiendo confirmado'),entry['Actor']),(prefix,fragment.replace('el señor Soto','el señor Gerente'),entry['Actor']),(prefix,fragment.replace('el señor Soto','el señor Desconocido'),entry['Actor']),('“'+prefix,fragment,entry['Actor']),(prefix.rstrip()[:-1]+'. ',fragment,entry['Actor'])]
        for pre,body,actor in cases:
            e=dict(entry,Actor=actor,Inicio=len(pre),Fin=len(pre+body))
            with self.subTest(body=body),self.assertRaises(ValueError):b.segment_turns(pre+body,r['Fecha'],r['Actor'],review=e)
    def test_old_gerund_opt_in_is_not_expanded(self):
        p=2918;r=self.raw[p];e=dict(self.reviews[p],Tipo_Limite='GERUNDIO_NOMINAL_EXPLICITO_REVISADO')
        with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)
    def test_marshall_current_statement_does_not_globalize_past_verbs(self):
        self.assertEqual(self.parts(1627)[1][1],'Enrique Marshall Rivera')
        self.assertIn('hizo presente',self.parts(1627)[1][0]);self.assertIn('e indica',self.parts(1627)[1][0])
        self.assertTrue(any(len(t)==2471 and a=='Rodrigo Valdés Pulido' for t,a,m in self.parts(1013)))
    def test_soto_return_is_explicit_and_long_developments_survive(self):
        self.assertEqual(self.parts(4926)[-1][1:],('Claudio Soto Gamboa','SUJETO_NOMBRE'))
        for p,n in [(1680,5991),(2167,7298),(1456,974),(586,916),(1627,609),(2698,1604),(6073,1862)]:self.assertTrue(any(len(t)==n for t,a,m in self.parts(p)))
    def test_recart_informs_but_attendance_is_not_speech(self):
        self.assertEqual(self.parts(1680)[-1][1: ],('María Olivia Recart Herrera','CONTEXTO_REVISADO'))
        self.assertEqual(self.parts(1680,False)[-1][1],b.CONSEJO)
        self.assertTrue(any(a==b.CONSEJO and 'se reanuda' in t for t,a,m in self.parts(1456)))
    def test_received_reading_and_return_modes_are_opt_in(self):
        entries=json.loads(DOC_PATH.read_text())
        for p in [4453,4507]:
            for key in ['Tipo_Procedencia','Tipo_Retorno']:
                e=copy.deepcopy(next(e for e in entries if e['ID_Padre']==p));e.pop(key)
                with self.subTest(p=p,key=key),self.assertRaises(ValueError):self.load_docs([e])
        self.assertIn('por escrito',self.docs[4722]['Cita_Procedencia'])
        self.assertNotIn('por escrito',self.docs[4453]['Cita_Procedencia'])
    def test_document_provenance_return_modes_and_attendance_are_checked(self):
        original=next(e for e in json.loads(DOC_PATH.read_text()) if e['ID_Padre']==4453)
        for key,value in [('Cita_Procedencia','Se comentó una opinión.'),('Cita_Retorno','A continuación se comenta.'),('Tipo_Procedencia','GENERICO'),('Tipo_Retorno','GENERICO'),('Asistencia_Autor','PRESENTE'),('Autor_Mencion','Rodrigo Cerda')]:
            e=dict(original);e[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.load_docs([e])
    def test_document_quote_boundaries_and_source_hash_are_checked(self):
        original=next(e for e in json.loads(DOC_PATH.read_text()) if e['ID_Padre']==4507)
        for index,delta in [(2,-1),(2,1),(3,-1),(3,1),(4,-1)]:
            e=copy.deepcopy(original);e['Limites'][index]+=delta
            with self.subTest(index=index,delta=delta),self.assertRaises(ValueError):self.load_docs([e])
        raw=copy.deepcopy(self.raw);raw[4507]['Texto']+='X'
        with self.assertRaises(ValueError):self.load_docs([original],raw)
    def test_documents_author_reader_and_recipient_are_distinct(self):
        for p in DOCUMENTS:
            ps=self.parts(p);lector='José De Gregorio Rebeco' if p==4453 else 'Rodrigo Vergara Montes'
            self.assertEqual([a for t,a,m in ps],[lector,lector,'Felipe Larraín Bascuñán',lector])
            self.assertEqual([m for t,a,m in ps][1:],[READER_SOURCE,AUTHOR_SOURCE,READER_SOURCE])
            self.assertEqual(len(self.parts(p,False)),1)
            e=copy.deepcopy(self.docs[p]);e['Lector']='Enrique Marshall Rivera';r=self.raw[p]
            with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],document=e)
    def test_documents_do_not_expand_ordinary_oral_speaker_detection(self):
        for p in DOCUMENTS:
            self.assertNotIn(AUTHOR_SOURCE,[m for t,a,m in self.parts(p,False)])
            self.assertTrue(self.parts(p)[2][0].startswith('“'));self.assertTrue(self.parts(p)[2][0].endswith('”'))
            self.assertEqual(self.docs[p]['Asistencia_Autor'],'NO_INFERIDA_DEL_DOCUMENTO')
    def test_two_exact_damage_warnings_preserve_literal(self):
        for p,n in [(1004,1422),(2948,664)]:
            hits=[t for t,a,m in self.parts(p) if contextual_motives(dict(ID_Padre=p,Fecha=self.raw[p]['Fecha'],Actor_Final=a,Texto=t),self.warnings)]
            self.assertEqual(len(hits),1);self.assertEqual(len(hits[0]),n)
        self.assertIn('porque V Por otra parte',self.parts(1004)[0][0]);self.assertTrue(self.parts(2948)[-1][0].endswith('A continuación,.'))
    def test_five_references_not_new_turns_or_pending_closure(self):
        ms=load_mention_reviews(self.raw)
        for p in [77,1042,1456,2167,1004]:
            self.assertEqual(self.parts(p),self.parts(p,False));self.assertNotIn(p,self.reviews)
        self.assertEqual(sum('-L25-' in e['Revision_ID'] for e in ms.values()),5)
        self.assertEqual({e['ID_Padre'] for e in ms.values() if e['Decision']=='PENDIENTE_DELIMITAR_APORTE'},{6185,3775,4055})
    def test_claro_reference_to_vial_does_not_open_another_voice(self):
        self.assertEqual([a for t,a,m in self.parts(6073)],['Sergio Lehmann Beresi','Sebastián Claro Edwards'])
        self.assertIn('corrobora lo expresado por el Consejero señor Joaquín Vial',self.parts(6073)[-1][0])
    def test_parent_586_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[586]['Texto'].encode()).hexdigest(),'eb534726a5982528b4b37371eade51c6ca979ba5e8fe10c63e4c0d90776cb432')
        ps=self.parts(586)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Nicolás Eyzaguirre Guzmán', 208, 'SUJETO_ROL_SESION'), ('Manuel Marfán Lewis', 591, 'CONTEXTO_REVISADO'), ('Pablo García Silva', 553, 'SUJETO_NOMBRE'), ('Manuel Marfán Lewis', 916, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 612, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[586]['Texto'].split()))
    def test_parent_1627_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1627]['Texto'].encode()).hexdigest(),'84501321e452c5fe0d53aeb03521c25dfcec6d2f7425344c056c0eb98350caaa')
        ps=self.parts(1627)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Beltrán de Ramón Acevedo', 321, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 259, 'CONTEXTO_REVISADO'), ('Pablo García Silva', 609, 'SUJETO_ROL_NOMBRE'), ('Beltrán de Ramón Acevedo', 327, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 516, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[1627]['Texto'].split()))
    def test_parent_1680_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1680]['Texto'].encode()).hexdigest(),'d03a63cbdafce42ccaa728114e3ad6c1cc42255efd39ff0a3e53578b10095223')
        ps=self.parts(1680)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Enrique Marshall Rivera', 5991, 'SUJETO_ROL_NOMBRE'), ('María Olivia Recart Herrera', 245, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[1680]['Texto'].split()))
    def test_parent_2698_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2698]['Texto'].encode()).hexdigest(),'19b9feb37ada808287ae921ca729271300a7d788df66a3b803aa766fb2516532')
        ps=self.parts(2698)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('José De Gregorio Rebeco', 409, 'SUJETO_ROL_NOMBRE'), ('Sebastián Claro Edwards', 823, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 1604, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[2698]['Texto'].split()))
    def test_parent_2918_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2918]['Texto'].encode()).hexdigest(),'a554d225def6b218ab1a7f9d0aa51d50070a014aa05feb5a537586135f92f0bc')
        ps=self.parts(2918)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('José De Gregorio Rebeco', 59, 'SUJETO_ROL_SESION'), ('Claudio Soto Gamboa', 215, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[2918]['Texto'].split()))
    def test_parent_2948_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2948]['Texto'].encode()).hexdigest(),'ed1632fd25757f7e8e0eb9eb2a65b2a346029e25ca248ea19a2f173898cfe4ba')
        ps=self.parts(2948)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Manuel Marfán Lewis', 785, 'SUJETO_ROL_NOMBRE'), ('Beltrán de Ramón Acevedo', 664, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[2948]['Texto'].split()))
    def test_parent_4926_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4926]['Texto'].encode()).hexdigest(),'b91b2650851fe5da1c40db1d501feea2f9319058e28f9df8b27abe515168e419')
        ps=self.parts(4926)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Claudio Soto Gamboa', 1751, 'SUJETO_NOMBRE'), ('Rodrigo Vergara Montes', 148, 'CONTEXTO_REVISADO'), ('Claudio Soto Gamboa', 213, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[4926]['Texto'].split()))
    def test_parent_6073_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[6073]['Texto'].encode()).hexdigest(),'4e65ac598758ed601f9bdb8e5cadd403e2cb99e6fc25bf37ffa472bbc17919b9')
        ps=self.parts(6073)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Sergio Lehmann Beresi', 92, 'SUJETO_NOMBRE'), ('Sebastián Claro Edwards', 1862, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[6073]['Texto'].split()))
    def test_parent_4453_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4453]['Texto'].encode()).hexdigest(),'75591ebe22640bbc5f9ac9586c09911d937d3ad0b85bb0ed659c6fc50638b00b')
        ps=self.parts(4453)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('José De Gregorio Rebeco', 448, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 227, 'LECTOR_DOCUMENTO_REVISADO'), ('Felipe Larraín Bascuñán', 4713, 'DOCUMENTO_ESCRITO_REVISADO'), ('José De Gregorio Rebeco', 136, 'LECTOR_DOCUMENTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[4453]['Texto'].split()))
    def test_parent_4507_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4507]['Texto'].encode()).hexdigest(),'c071228e39ca48d286c0cd779f211a62ca4e071273422b3a8b01a0cd0f335c0d')
        ps=self.parts(4507)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Rodrigo Vergara Montes', 132, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Vergara Montes', 227, 'LECTOR_DOCUMENTO_REVISADO'), ('Felipe Larraín Bascuñán', 6007, 'DOCUMENTO_ESCRITO_REVISADO'), ('Rodrigo Vergara Montes', 135, 'LECTOR_DOCUMENTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[4507]['Texto'].split()))
    def test_parent_4722_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4722]['Texto'].encode()).hexdigest(),'2467cb03bbbaf29156b274c73724fc7483f2d080da98207349aa445b3b57f178')
        ps=self.parts(4722)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Rodrigo Vergara Montes', 119, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Vergara Montes', 239, 'LECTOR_DOCUMENTO_REVISADO'), ('Felipe Larraín Bascuñán', 6828, 'DOCUMENTO_ESCRITO_REVISADO'), ('Rodrigo Vergara Montes', 250, 'LECTOR_DOCUMENTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[4722]['Texto'].split()))
    def test_parent_77_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[77]['Texto'].encode()).hexdigest(),'08778feed8ab852e3aaa6994f85bd77870589f98078545de52d8ff42b9572ba2')
        ps=self.parts(77)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Vittorio Corbo Lioi', 256, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[77]['Texto'].split()))
    def test_parent_1042_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1042]['Texto'].encode()).hexdigest(),'91d284970509d0a12a7ba4592a1f5842c70228acb0236d40e7c1bd248834b65d')
        ps=self.parts(1042)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Vittorio Corbo Lioi', 176, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[1042]['Texto'].split()))
    def test_parent_1456_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1456]['Texto'].encode()).hexdigest(),'7b216248ca6a7cdb65d76834e7789222f7bc99881058c65816c29a7d675ac52c')
        ps=self.parts(1456)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Vittorio Corbo Lioi', 128, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 74, 'ACTA/META'), ('Vittorio Corbo Lioi', 325, 'SUJETO_ROL_SESION'), ('Pablo García Silva', 974, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[1456]['Texto'].split()))
    def test_parent_2167_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2167]['Texto'].encode()).hexdigest(),'10ffe024136b613fd598d95b9ba354dd58fb564f98a7f1e470e45a01ab0aa4b9')
        ps=self.parts(2167)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Enrique Marshall Rivera', 7298, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 229, 'SUJETO_ROL_NOMBRE'), ('Andrés Velasco Brañes', 558, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[2167]['Texto'].split()))
    def test_parent_1004_source_segments_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1004]['Texto'].encode()).hexdigest(),'2f819a38ca9ab8a978874939de938a9d642d4073e9bf3bbd8e4c0eb22f60a2a5')
        ps=self.parts(1004)
        self.assertEqual([(a,len(t),m) for t,a,m in ps],[('Manuel Marfán Lewis', 1422, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in ps),''.join(self.raw[1004]['Texto'].split()))
