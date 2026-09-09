"""LOOP29: respuestas nominales acotadas, retorno propio y continuidad de Soto."""
import copy, hashlib, json, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, validate_speaker_reviews, speaker_intervals
from continuity import annotate_turns, update_state
from reviewed_continuity import load_reviewed_links, validate_reviewed_links
from context_warnings import load_context_warnings, contextual_motives
from mention_reviews import load_mention_reviews, validate_mention_reviews

MODE='GERUNDIO_RESPUESTA_VARIANTE_REVISADA'
PERSONAL=(2931,3044,5003)
ROOT=Path(__file__).resolve().parents[1]

def compact(text):return ''.join(text.split())
def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

class LoopTwentyNineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)
        cls.links=load_reviewed_links(cls.raw)
        cls.warnings=load_context_warnings(cls.raw)
        cls.mentions=load_mention_reviews(cls.raw)

    def parts(self,p,reviewed=True):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p) if reviewed else None)

    def rows(self,parents):
        rows=[]
        for p in parents:
            for i,(text,actor,method) in enumerate(self.parts(p),1):
                rows.append(dict(ID=len(rows)+1,ID_Padre=p,Fecha=self.raw[p]['Fecha'],Texto=text,
                    Actor_Final=actor,Fuente_Actor=method,Tipo_Acta='',Motivos_Revision='',
                    ID_Intervencion=f'{p}:{i}',ID_Bloque_Texto=f'{p}:{i}',Duplicado_Exacto='NO'))
        return rows

    def load_one(self,entry,raw=None):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'review.json';path.write_text(json.dumps([entry]))
            return load_speaker_reviews(self.raw if raw is None else raw,path)

    def test_three_exact_intervals_validate(self):
        for p in PERSONAL:
            self.assertEqual(self.reviews[p]['Tipo_Limite'],MODE)
            self.assertEqual(len(speaker_intervals(self.reviews[p])),1)
            self.assertFalse(validate_speaker_reviews(self.rows([p]),{p:self.reviews[p]}))

    def test_no_opt_in_means_no_new_automatic_cut(self):
        for p,count in [(2931,2),(3044,1),(5003,1)]:
            self.assertEqual(len(self.parts(p,False)),count)
            self.assertNotIn('CONTEXTO_REVISADO',[m for t,a,m in self.parts(p,False)])

    def test_old_gerund_modes_do_not_accept_new_predicates(self):
        for p in PERSONAL:
            r=self.raw[p]
            for mode in [None,'GERUNDIO_NOMINAL_EXPLICITO_REVISADO','GERUNDIO_CONFIRMACION_NOMINAL_REVISADA']:
                e=copy.deepcopy(self.reviews[p]);e['Tipo_Limite']=mode
                with self.subTest(parent=p,mode=mode),self.assertRaises(ValueError):
                    b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)

    def test_source_hash_date_and_citation_are_mandatory(self):
        for p in PERSONAL:
            for key,value in [('SHA256_Texto_Padre','0'*64),('Fecha','1900-01-01'),('Cita_Inicio','inventado'),('Tipo_Limite','LIBRE')]:
                e=copy.deepcopy(self.reviews[p]);e[key]=value
                with self.subTest(parent=p,key=key),self.assertRaises(ValueError):self.load_one(e)

    def test_changed_source_requires_new_adjudication(self):
        for p in PERSONAL:
            raw=copy.deepcopy(self.raw);raw[p]['Texto']+=' cambio'
            with self.assertRaises(ValueError):self.load_one(self.reviews[p],raw)

    def test_subject_mismatch_is_rejected(self):
        for p in PERSONAL:
            e=copy.deepcopy(self.reviews[p]);e['Actor']='Sergio Lehmann Beresi';r=self.raw[p]
            with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=e)

    def test_no_separator_no_cut(self):
        for p in PERSONAL:
            e=copy.deepcopy(self.reviews[p]);r=self.raw[p];a=e['Inicio'];prefix=r['Texto'][:a]
            comma=prefix.rfind(',');self.assertGreaterEqual(comma,0)
            text=r['Texto'][:comma]+':'+r['Texto'][comma+1:]
            with self.assertRaises(ValueError):b.segment_turns(text,r['Fecha'],r['Actor'],review=e)

    def test_open_quote_is_not_ignored_by_variant(self):
        for p in PERSONAL:
            r=self.raw[p];e=copy.deepcopy(self.reviews[p]);e['Inicio']+=1;e['Fin']+=1
            with self.assertRaises(ValueError):b.segment_turns('“'+r['Texto'],r['Fecha'],r['Actor'],review=e)

    def test_nominal_subject_not_bare_role_is_required(self):
        for p,subject,role in [(2931,'el señor Pablo García','el señor Gerente'),(3044,'el señor Vergara','el señor Consejero'),(5003,'el señor Claudio Soto','el señor Gerente')]:
            r=self.raw[p];e=copy.deepcopy(self.reviews[p]);a=e['Inicio'];original=r['Texto'][a:e['Fin']]
            fragment=original.replace(subject,role,1);text=r['Texto'][:a]+fragment+r['Texto'][e['Fin']:]
            e['Fin']+=len(fragment)-len(original);e['Cita_Inicio']=fragment[:65]
            with self.assertRaises(ValueError):b.segment_turns(text,r['Fecha'],r['Actor'],review=e)

    def test_que_declaration_is_required(self):
        for p in PERSONAL:
            r=self.raw[p];e=copy.deepcopy(self.reviews[p]);a=e['Inicio'];fragment=r['Texto'][a:e['Fin']].replace(' que ',' sin ',1)
            text=r['Texto'][:a]+fragment+r['Texto'][e['Fin']:];e['Cita_Inicio']=fragment[:65]
            with self.assertRaises(ValueError):b.segment_turns(text,r['Fecha'],r['Actor'],review=e)

    def test_unlisted_gerund_remains_rejected(self):
        for p in PERSONAL:
            r=self.raw[p];e=copy.deepcopy(self.reviews[p]);a=e['Inicio'];original=r['Texto'][a:e['Fin']]
            first=original.split()[0];fragment='considerando'+original[len(first):]
            text=r['Texto'][:a]+fragment+r['Texto'][e['Fin']:];e['Fin']+=len(fragment)-len(original);e['Cita_Inicio']=fragment[:65]
            with self.assertRaises(ValueError):b.segment_turns(text,r['Fecha'],r['Actor'],review=e)

    def test_replicando_is_literal_not_responde_in_output(self):
        text,actor,source=self.parts(3044)[1]
        self.assertTrue(text.startswith('replicando el señor Vergara que '))
        self.assertEqual(actor,'Rodrigo Vergara Montes')
        self.assertNotIn('responde',text)

    def test_marfan_returns_with_own_explicit_anchor(self):
        rows=annotate_turns(self.rows([3044]));last=rows[-1]
        self.assertTrue(last['Texto'].startswith('El señor Marfán agrega'))
        self.assertEqual(last['Actor_Final'],'Manuel Marfán Lewis')
        self.assertEqual(last['Fuente_Actor'],'SUJETO_NOMBRE')
        self.assertEqual(last['ID_Ancla_Actor'],last['ID_Intervencion'])
        self.assertEqual(len({r['ID_Turno'] for r in rows}),3)
        self.assertFalse(last['ID_Antecedente_Continuidad'])

    def test_garcia_does_not_jump_over_marshall(self):
        rows=annotate_turns(self.rows([2931]))
        self.assertEqual(rows[0]['Actor_Final'],rows[-1]['Actor_Final'])
        self.assertEqual(len({r['ID_Turno'] for r in rows}),3)
        self.assertFalse(rows[-1]['ID_Ancla_Actor'])

    def test_reviewed_replies_are_not_global_anchors(self):
        for p in PERSONAL:
            t,a,m=next(x for x in self.parts(p) if x[2]=='CONTEXTO_REVISADO');state={}
            update_state(state,a,m,t,self.raw[p]['Fecha'],b.TURN_DETECTOR,b.split_sentences,'review')
            self.assertFalse(state['anchor'])

    def test_soto_link_excludes_president_and_keeps_all_text(self):
        key=(5003,5004);rows=self.rows(key);before=copy.deepcopy(rows)
        annotate_turns(rows,{key:self.links[key]})
        self.assertEqual(len(rows),3)
        self.assertNotEqual(rows[0]['ID_Turno'],rows[1]['ID_Turno'])
        self.assertEqual(rows[1]['ID_Turno'],rows[2]['ID_Turno'])
        self.assertFalse(rows[1]['ID_Ancla_Actor'])
        self.assertEqual(rows[2]['ID_Ancla_Actor'],rows[2]['ID_Intervencion'])
        self.assertEqual(rows[2]['ID_Antecedente_Continuidad'],rows[1]['ID_Intervencion'])
        self.assertFalse(validate_reviewed_links(rows,{key:self.links[key]}))
        self.assertEqual(before,[{k:r[k] for k in old} for old,r in zip(before,rows)])
        self.assertEqual(len(rows[2]['Texto']),2849)

    def test_without_link_opt_in_soto_stays_separate(self):
        rows=annotate_turns(self.rows([5003,5004]))
        self.assertNotEqual(rows[1]['ID_Turno'],rows[2]['ID_Turno'])

    def test_warning_cannot_be_bypassed_by_reviewed_link(self):
        for i in [1,2]:
            rows=self.rows([5003,5004]);rows[i]['Motivos_Revision']='TEXTO_DANADO_POR_COTEJAR'
            with self.assertRaises(ValueError):annotate_turns(rows,{(5003,5004):self.links[(5003,5004)]})

    def test_warning_3045_does_not_reassign_claro(self):
        self.assertEqual(self.parts(3045),self.parts(3045,False))
        row=self.rows([3045])[0]
        self.assertEqual(contextual_motives(row,self.warnings),['TEXTO_DANADO_POR_COTEJAR'])
        row['Actor_Final']='Manuel Marfán Lewis'
        self.assertFalse(contextual_motives(row,self.warnings))

    def test_text_artifacts_and_numbers_remain_literal(self):
        self.assertTrue(self.parts(5003)[-1][0].endswith('A continuación,.'))
        for term in ['bottom fine','ser- 1,2%','Yque','Oy -1,2%']:self.assertIn(term,self.parts(3045)[0][0])
        self.assertIn('ios Estados Unidos',self.parts(1370)[0][0])
        self.assertIn('baja de los PPM transitoria',self.parts(3044)[1][0])

    def test_two_reference_readings_do_not_modify_rows(self):
        for p in [1142,1370]:
            rows=self.rows([p]);before=copy.deepcopy(rows)
            reviews={k:e for k,e in self.mentions.items() if e['ID_Padre']==p}
            errors,annotations=validate_mention_reviews(rows,reviews)
            self.assertFalse(errors);self.assertEqual(len(annotations),1);self.assertEqual(rows,before)
            self.assertEqual(self.parts(p),self.parts(p,False))
            self.assertEqual(len(self.parts(p)),1)

    def test_existing_2219_reference_still_is_not_a_marfan_reply(self):
        self.assertEqual(len(self.parts(2219)),2)
        self.assertIn('está señalando el Consejero',self.parts(2219)[1][0])
        self.assertEqual(self.parts(2219)[1][1],'José De Gregorio Rebeco')
        self.assertFalse(any(e['ID_Padre']==2219 and '-L29-' in e['Revision_ID'] for e in self.mentions.values()))

# Fixed source signatures and reviewed segmentation fixtures follow.
    def test_parent_1142_exact_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1142]['Texto'].encode()).hexdigest(),'3f8c715f709cb88a285d60af1e4986a6817954f13c903eb06b03675daa5f205b')
        parts=self.parts(1142)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 424, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[1142]['Texto']))

    def test_parent_1370_exact_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[1370]['Texto'].encode()).hexdigest(),'a09ed58249595ca252444e501ca6f19f9575fc36ebf970472fd974d5f96a4c15')
        parts=self.parts(1370)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Jorge Desormeaux Jiménez', 509, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[1370]['Texto']))

    def test_parent_2219_exact_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2219]['Texto'].encode()).hexdigest(),'7899c455442a19c92887e9ea500bf2a89ad56ff4ee98dddc91d43a4b3e17b0db')
        parts=self.parts(2219)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 786, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 297, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2219]['Texto']))

    def test_parent_2930_exact_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2930]['Texto'].encode()).hexdigest(),'0000b1e02df487caeb9c66c7ccecaff4f1f504163d8d66ed0831de08e2a1790b')
        parts=self.parts(2930)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Pablo García Silva', 325, 'SUJETO_NOMBRE'), ('Claudio Soto Gamboa', 275, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2930]['Texto']))

    def test_parent_2931_exact_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2931]['Texto'].encode()).hexdigest(),'0a414d26473f6596ce4286566f46bb2b3925f7261df2f3eb8b905d1fba47b412')
        parts=self.parts(2931)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Pablo García Silva', 310, 'SUJETO_NOMBRE'), ('Enrique Marshall Rivera', 172, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 242, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2931]['Texto']))

    def test_parent_2932_exact_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2932]['Texto'].encode()).hexdigest(),'bfefc9678f3c7237af34ebc85d2dd6361f334e73c4e1744b13aa8b44c4c7fa9a')
        parts=self.parts(2932)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 1555, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2932]['Texto']))

    def test_parent_3043_exact_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3043]['Texto'].encode()).hexdigest(),'53a4602c27f2772f94eba4de4b0121294fb0c1e78465be7c06e28eeb3eb51c5e')
        parts=self.parts(3043)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 305, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3043]['Texto']))

    def test_parent_3044_exact_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3044]['Texto'].encode()).hexdigest(),'03a220efc41d58e1d273a951bc323c7d17c855bcdad471a5ebdf580a5a21a1ea')
        parts=self.parts(3044)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 135, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Vergara Montes', 141, 'CONTEXTO_REVISADO'), ('Manuel Marfán Lewis', 221, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3044]['Texto']))

    def test_parent_3045_exact_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3045]['Texto'].encode()).hexdigest(),'36d6c3323db19071a1b04c09193abe8cc45a6f40db189b58138757b2b70c6aaa')
        parts=self.parts(3045)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 461, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3045]['Texto']))

    def test_parent_5002_exact_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5002]['Texto'].encode()).hexdigest(),'b4a941da7f5d944d5732ab4689e8c584995eda0dfd863e860d0513f3f97c1a74')
        parts=self.parts(5002)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 5703, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[5002]['Texto']))

    def test_parent_5003_exact_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5003]['Texto'].encode()).hexdigest(),'7661ea8389b101d2a64f958f23cbfe1a7cd21c9b9234476bd2570a3884395c5a')
        parts=self.parts(5003)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 130, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 280, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[5003]['Texto']))

    def test_parent_5004_exact_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5004]['Texto'].encode()).hexdigest(),'a4cb900b3abaee92ba1f29fbf4a002432cbe9a508ce32920a571f82e204c37b6')
        parts=self.parts(5004)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 2849, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[5004]['Texto']))

    def test_frozen_revisiones_continuidad_hablantes_prefix(self):
        entries=json.loads((ROOT/'data/curation/revisiones_continuidad_hablantes.json').read_text())
        self.assertEqual(digest(entries[:23]),'92e5fe0eae035da7c6b3a1835a0b07189571732dde26ab12dd59b61b0e4e0a28')

    def test_frozen_revisiones_menciones_actuales_prefix(self):
        entries=json.loads((ROOT/'data/curation/revisiones_menciones_actuales.json').read_text())
        self.assertEqual(digest(entries[:41]),'42fbcd6b4f167acfe1f82cfcdf3e142facd2b934cfc431458299413ccc7ae38c')

    def test_frozen_alertas_contextuales_prefix(self):
        entries=json.loads((ROOT/'data/curation/alertas_contextuales.json').read_text())
        self.assertEqual(digest(entries[:73]),'e7c5126a7bb28c341a14d8b3224aa699ad11f38beb28b41ef0c7fb01ccf9f178')

    def test_frozen_revisiones_continuaciones_acta_prefix(self):
        entries=json.loads((ROOT/'data/curation/revisiones_continuaciones_acta.json').read_text())
        self.assertEqual(digest(entries[:2]),'997074a565a0e1605055f6c568e349841ad2d1c2f158257591011d8d5454e2fe')

if __name__ == '__main__':
    unittest.main()
