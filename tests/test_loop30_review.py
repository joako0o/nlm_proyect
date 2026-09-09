"""LOOP30: opinión relativa, cierre presidencial y referencias sin voces inventadas."""
import copy, hashlib, json, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, validate_speaker_reviews
from continuity import annotate_turns, update_state
from context_warnings import load_context_warnings, contextual_motives
from mention_reviews import load_mention_reviews, validate_mention_reviews

ROOT=Path(__file__).resolve().parents[1]
MENTIONS=(649,1298,1379,1930,1941,2058,2201,2206,2220,2853,3570,4193,4910,4989)
def compact(t):return ''.join(t.split())
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

class LoopThirtyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)
        cls.warnings=load_context_warnings(cls.raw)
        cls.mentions=load_mention_reviews(cls.raw)

    def parts(self,p,reviewed=True):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p) if reviewed else None)

    def rows(self,p):
        return [dict(ID=i,ID_Padre=p,Fecha=self.raw[p]['Fecha'],Texto=t,Actor_Final=a,Fuente_Actor=m,
            Tipo_Acta='META_SESION' if a==b.CONSEJO else '',Motivos_Revision='',
            ID_Intervencion=f'{p}:{i}',ID_Bloque_Texto=f'{p}:{i}') for i,(t,a,m) in enumerate(self.parts(p),1)]

    def test_two_exact_speaker_intervals(self):
        for p in [2705,2706]:self.assertFalse(validate_speaker_reviews(self.rows(p),{p:self.reviews[p]}))

    def test_no_automatic_opinion_or_handoff_rule(self):
        self.assertEqual(len(self.parts(2705,False)),6)
        self.assertEqual(len(self.parts(2706,False)),2)
        self.assertIn('a juicio del señor Presidente',self.parts(2705,False)[2][0])
        self.assertIn('da paso a la votación',self.parts(2706,False)[1][0])

    def test_opinion_without_opt_in_is_rejected(self):
        r=self.raw[2705];e=copy.deepcopy(self.reviews[2705]);del e['Tipo_Limite']
        with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)

    def test_wrong_role_connector_or_predicate_rejected(self):
        r=self.raw[2705]
        for before,after in [('señor Presidente','señor Ministro'),('lo cual, a juicio','lo cual a juicio'),('es muy curioso','era muy curioso')]:
            e=copy.deepcopy(self.reviews[2705]);a,z=e['Inicio'],e['Fin'];old=r['Texto'][a:z];new=old.replace(before,after,1)
            self.assertNotEqual(old,new);text=r['Texto'][:a]+new+r['Texto'][z:];e['Fin']+=len(new)-len(old);e['Cita_Inicio']=new[:65]
            with self.subTest(before=before),self.assertRaises(ValueError):b.segment_turns(text,r['Fecha'],r['Actor'],review=e)

    def test_separator_and_quote_guards(self):
        r=self.raw[2705]
        for change in ['separator','quote']:
            e=copy.deepcopy(self.reviews[2705]);text=r['Texto']
            if change=='separator':
                k=text[:e['Inicio']].rfind(',');text=text[:k]+':'+text[k+1:]
            else:text='“'+text;e['Inicio']+=1;e['Fin']+=1
            with self.assertRaises(ValueError):b.segment_turns(text,r['Fecha'],r['Actor'],review=e)

    def test_wrong_actor_is_rejected(self):
        r=self.raw[2705];e=copy.deepcopy(self.reviews[2705]);e['Actor']='Claudio Soto Gamboa'
        with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)

    def test_hash_date_and_citation_mutations_fail(self):
        for p in [2705,2706]:
            for field,value in [('SHA256_Texto_Padre','0'*64),('Fecha','1900-01-01'),('Cita_Inicio','inventado'),('Inicio',1)]:
                e=copy.deepcopy(self.reviews[p]);e[field]=value
                with tempfile.TemporaryDirectory() as d:
                    path=Path(d)/'r.json';path.write_text(json.dumps([e]))
                    with self.subTest(p=p,field=field),self.assertRaises(ValueError):load_speaker_reviews(self.raw,path)

    def test_relative_is_exported_literally_not_projection(self):
        t,a,m=self.parts(2705)[3]
        self.assertTrue(t.startswith('lo cual, a juicio del señor Presidente, es '))
        self.assertNotIn('El señor Presidente señala que',t)
        self.assertEqual(a,'José De Gregorio Rebeco')
        self.assertEqual(len(t),281)

    def test_cowan_soto_returns_and_institutional_resumption_remain(self):
        rows=annotate_turns(self.rows(2705))
        for i,actor in [(4,'Kevin Cowan Logan'),(5,'Claudio Soto Gamboa')]:
            self.assertEqual(rows[i]['Actor_Final'],actor)
            self.assertEqual(rows[i]['ID_Ancla_Actor'],rows[i]['ID_Intervencion'])
            self.assertNotEqual(rows[i]['ID_Turno'],rows[i-1]['ID_Turno'])
        self.assertEqual(rows[-1]['Actor_Final'],b.CONSEJO)
        self.assertFalse(rows[-1]['ID_Ancla_Actor'])
        self.assertTrue(rows[-1]['Texto'].startswith('Siendo las 16:00 horas'))

    def test_presentation_complete_and_closing_distinct(self):
        rows=annotate_turns(self.rows(2706))
        self.assertEqual(len(rows[1]['Texto']),6820)
        self.assertEqual(rows[1]['Actor_Final'],'Pablo García Silva')
        self.assertTrue(rows[2]['Texto'].startswith('Concluida la presentación de las Opciones'))
        self.assertEqual(rows[2]['Actor_Final'],'José De Gregorio Rebeco')
        self.assertEqual(len({r['ID_Turno'] for r in rows}),3)
        self.assertFalse(rows[2]['ID_Ancla_Actor'])
        self.assertNotIn('DOCUMENTO_ESCRITO_REVISADO',[r['Fuente_Actor'] for r in rows])

    def test_reviewed_fragments_do_not_grant_global_anchors(self):
        for p in [2705,2706]:
            for t,a,m in self.parts(p):
                if m=='CONTEXTO_REVISADO':
                    state={};update_state(state,a,m,t,self.raw[p]['Fecha'],b.TURN_DETECTOR,b.split_sentences,'review')
                    self.assertFalse(state['anchor'])

    def test_metaphorical_da_paso_not_presidential_speech(self):
        for p in [3340,5584]:
            parts=self.parts(p)
            self.assertIn('da paso a',parts[0][0])
            self.assertEqual(parts[0][1],'Sebastián Claro Edwards')
        self.assertEqual(len(self.parts(3340)),2)
        self.assertEqual(len(self.parts(5584)),1)

    def test_fourteen_readings_are_exact_and_do_not_alter_rows(self):
        for p in MENTIONS:
            rows=self.rows(p);before=copy.deepcopy(rows)
            rv={k:e for k,e in self.mentions.items() if e['ID_Padre']==p and '-L30-' in k}
            self.assertEqual(len(rv),1)
            errors,annotations=validate_mention_reviews(rows,rv)
            self.assertFalse(errors);self.assertEqual(len(annotations),1);self.assertEqual(rows,before)
            self.assertEqual(next(iter(annotations.values()))['Estado_Lectura_Dirigida'],'MENCION_LEGITIMA_REVISADA')

    def test_warning_is_not_closed_by_legitimate_mention(self):
        for p in [1298,1379,3340]:
            rows=self.rows(p)
            self.assertEqual(contextual_motives(rows[0],self.warnings),['TEXTO_DANADO_POR_COTEJAR'])
            for row in rows[1:]:self.assertFalse(contextual_motives(row,self.warnings))
        self.assertEqual(len(self.parts(1298)),1)
        self.assertEqual(self.parts(1379)[1][1],'José De Gregorio Rebeco')
        self.assertEqual(self.parts(3340)[1][1],'Enrique Marshall Rivera')

    def test_damage_and_discrepant_numbers_are_literal(self):
        for p,terms in [(1298,['/aíer','80 puntos base','4,5% a 6,2%']),(1379,['U) compensaciones']),(3340,['rV- financieros'])]:
            for term in terms:self.assertIn(term,self.parts(p)[0][0])

    def test_reference_and_real_reply_remain_separate(self):
        for p,actors in [(1930,['José De Gregorio Rebeco','Jorge Desormeaux Jiménez','Claudio Soto Gamboa']),
            (2206,['Claudio Soto Gamboa','Jorge Desormeaux Jiménez','Claudio Soto Gamboa'])]:
            self.assertEqual([a for t,a,m in self.parts(p)],actors)
        self.assertEqual(len(self.parts(2206)[0][0]),6097)
        self.assertEqual(len(self.parts(2206)[2][0]),118)

# Fixed source and segmentation fixtures follow.
    def test_parent_649_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[649]['Texto'].encode()).hexdigest(),'ce40dae6c34bba4e6f35f4b97f186e51eb676268c922eeaa05c0d8ba67ef74aa')
        parts=self.parts(649)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 550, 'SUJETO_ROL_NOMBRE'), ('Andrés Velasco Brañes', 341, 'SUJETO_ROL_SESION'), ('Manuel Marfán Lewis', 2174, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[649]['Texto']))

    def test_parent_1298_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1298]['Texto'].encode()).hexdigest(),'d4163bb84f46c829f30a05757536254da7b54d91e3900d64a6a9c924570aee1a')
        parts=self.parts(1298)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Klaus Schmidt-Hebbel Dunker', 5985, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[1298]['Texto']))

    def test_parent_1379_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1379]['Texto'].encode()).hexdigest(),'3c15725ee3498a6033f328f62674d0c56e10701ca8a5a06cffdfaf1a620b8eef')
        parts=self.parts(1379)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Beltrán de Ramón Acevedo', 1187, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 731, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[1379]['Texto']))

    def test_parent_1930_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1930]['Texto'].encode()).hexdigest(),'fc61d240681d337e026fb49ebb401012fe4c58c4891af298dab47cb8dafa8da6')
        parts=self.parts(1930)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 74, 'SUJETO_ROL_NOMBRE'), ('Jorge Desormeaux Jiménez', 340, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 414, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[1930]['Texto']))

    def test_parent_1941_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1941]['Texto'].encode()).hexdigest(),'16288cead028e17839377561614470db4c9a52f41c7fc54eb160c154be6d3a40')
        parts=self.parts(1941)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 359, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 1071, 'SUJETO_ROL_NOMBRE'), ('Andrés Velasco Brañes', 867, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[1941]['Texto']))

    def test_parent_2058_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2058]['Texto'].encode()).hexdigest(),'2fc395fbcec3ed25b3d474918990c3ec5083ed0b65ee1cf85b020ecf6f04ae74')
        parts=self.parts(2058)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 72, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 242, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 265, 'CONTEXTO_REVISADO'), ('José De Gregorio Rebeco', 412, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2058]['Texto']))

    def test_parent_2201_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2201]['Texto'].encode()).hexdigest(),'7bfd0dfe928dc454eba37d91006ace4db88fe6579a74ea4fad94aee9b81596a3')
        parts=self.parts(2201)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 2688, 'SUJETO_ROL_NOMBRE'), ('Jorge Desormeaux Jiménez', 1605, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2201]['Texto']))

    def test_parent_2206_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2206]['Texto'].encode()).hexdigest(),'0e3701a343a69b37bca7f15e6fc5e6e5ef78b99e64c9ba3b156acae404e1f411')
        parts=self.parts(2206)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 6097, 'SUJETO_NOMBRE'), ('Jorge Desormeaux Jiménez', 303, 'SUJETO_ROL_SESION'), ('Claudio Soto Gamboa', 118, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2206]['Texto']))

    def test_parent_2220_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2220]['Texto'].encode()).hexdigest(),'c647f47ec64ddaa910485cc65bd47e481e4aadd23ec31dc06255fe0e4085f899')
        parts=self.parts(2220)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Pablo García Silva', 433, 'CONTEXTO_REVISADO'), ('Sebastián Claro Edwards', 356, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2220]['Texto']))

    def test_parent_2705_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2705]['Texto'].encode()).hexdigest(),'2b2e790dcc652db32659ef1efb4e304d7f6d749f6c27387e163fccdc42586e58')
        parts=self.parts(2705)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 430, 'SUJETO_ROL_NOMBRE'), ('Kevin Cowan Logan', 194, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 664, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 281, 'CONTEXTO_REVISADO'), ('Kevin Cowan Logan', 136, 'SUJETO_NOMBRE'), ('Claudio Soto Gamboa', 1096, 'SUJETO_NOMBRE'), ('Consejo del Banco Central de Chile', 199, 'ACTA/META')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2705]['Texto']))

    def test_parent_2706_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2706]['Texto'].encode()).hexdigest(),'c0ec21f91c1f2502fe543727c5f8d55049ec16a28a6a944942d4c121de9a974d')
        parts=self.parts(2706)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 162, 'SUJETO_ROL_SESION'), ('Pablo García Silva', 6820, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 194, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2706]['Texto']))

    def test_parent_2707_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2707]['Texto'].encode()).hexdigest(),'bf565a96234d9becf62acfb1bc905c781e8bc86fbacf79e09dc7d5de2e98a3c4')
        parts=self.parts(2707)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 3973, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 139, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2707]['Texto']))

    def test_parent_2853_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2853]['Texto'].encode()).hexdigest(),'fff7b56b330e20d261e62c81f5c4790ad8d58487bbd7e0f653d4910e72ed1aa1')
        parts=self.parts(2853)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Matías Bernier Bórquez', 757, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 462, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2853]['Texto']))

    def test_parent_3340_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3340]['Texto'].encode()).hexdigest(),'91ef4f79ce4cd49e2cd5dde464676e1a9abb978bab6a39915baadf0133e93a3c')
        parts=self.parts(3340)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 7642, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 2692, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3340]['Texto']))

    def test_parent_3570_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3570]['Texto'].encode()).hexdigest(),'9c442931a2e2dae3152cf6a4291c10272e83f011fee2934d334050435dc1b991')
        parts=self.parts(3570)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Luis Felipe Céspedes Cifuentes', 746, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3570]['Texto']))

    def test_parent_4193_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4193]['Texto'].encode()).hexdigest(),'0f7b40846709210233b207f48bc09a63c52057e5e9e451eb152822308832bb08')
        parts=self.parts(4193)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 385, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[4193]['Texto']))

    def test_parent_4910_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4910]['Texto'].encode()).hexdigest(),'eb18043aab984885c0ea04b2639f65910b0b47d4c9970af089e65ba195076eb5')
        parts=self.parts(4910)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Joaquín Vial Ruiz-Tagle', 2000, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[4910]['Texto']))

    def test_parent_4989_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4989]['Texto'].encode()).hexdigest(),'0aec62c57b52006d3f9de4701e7af893567e62b4ee3b3197288184491bfccaac')
        parts=self.parts(4989)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Luis Óscar Herrera Barriga', 2160, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[4989]['Texto']))

    def test_parent_5584_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5584]['Texto'].encode()).hexdigest(),'bb618a097a8817f699e095af7a18be721a59b145ab3ffe8902bc4c42af585c7c')
        parts=self.parts(5584)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 1277, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[5584]['Texto']))

    def test_frozen_revisiones_continuidad_hablantes_prefix(self):
        es=json.loads((ROOT/'data/curation/revisiones_continuidad_hablantes.json').read_text())
        self.assertEqual(digest(es[:24]),'018b71de71c52b50063c25ff74df9d712bb6d5eae62e0a571f14ca132fc76b9e')

    def test_frozen_revisiones_menciones_actuales_prefix(self):
        es=json.loads((ROOT/'data/curation/revisiones_menciones_actuales.json').read_text())
        self.assertEqual(digest(es[:43]),'bc5f94b41a02d96b301e42758ecce14c9308541b6bd0a33659b4546f0bdc9383')

    def test_frozen_alertas_contextuales_prefix(self):
        es=json.loads((ROOT/'data/curation/alertas_contextuales.json').read_text())
        self.assertEqual(digest(es[:74]),'7379696692f397e88568166bf521df193fecba3773c6bf1a2d93013abdc1f575')

    def test_frozen_revisiones_continuaciones_acta_prefix(self):
        es=json.loads((ROOT/'data/curation/revisiones_continuaciones_acta.json').read_text())
        self.assertEqual(digest(es[:2]),'997074a565a0e1605055f6c568e349841ad2d1c2f158257591011d8d5454e2fe')

if __name__ == '__main__':
    unittest.main()
