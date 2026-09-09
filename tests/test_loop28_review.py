"""LOOP28: enlaces individuales sin fusionar textos, voces ni atravesar pausas."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews
from continuity import annotate_turns, update_state, boundary
from reviewed_continuity import load_reviewed_links, validate_reviewed_links, RELATION, PATH
from mention_reviews import load_mention_reviews, validate_mention_reviews

LINKS = ((121,122),(727,728),(2027,2028),(2838,2839),(2911,2912),(2918,2919),
         (3123,3124),(3571,3572),(4470,4471),(4903,4904),(5168,5169),(5872,5873),
         (6118,6119),(6394,6395))
ROOT = Path(__file__).resolve().parents[1]
def compact(text): return ''.join(text.split())
def digest(value): return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

class LoopTwentyEightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {r[0]: dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews = load_speaker_reviews(cls.raw)
        cls.links = load_reviewed_links(cls.raw)
        cls.mentions = load_mention_reviews(cls.raw)

    def parts(self,p):
        r = self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p))

    def rows(self,key):
        rows=[]
        for p in key:
            for i,(text,actor,source) in enumerate(self.parts(p),1):
                rows.append(dict(ID=len(rows)+1,ID_Padre=p,Numero_Segmento=i,
                    ID_Intervencion=f'{p}:{i}',ID_Bloque_Texto=f'{p}:{i}',
                    Fecha=self.raw[p]['Fecha'],Texto=text,Actor_Final=actor,
                    Fuente_Actor=source,Tipo_Acta='ACTA_INSTITUCIONAL' if actor==b.CONSEJO else '',
                    Motivos_Revision='',Duplicado_Exacto='NO'))
        return rows

    def endpoints(self,key,rows):
        return [r for r in rows if r['ID_Padre']==key[0]][-1], next(r for r in rows if r['ID_Padre']==key[1])

    def load_one(self,e,raw=None):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'links.json';p.write_text(json.dumps([e]))
            return load_reviewed_links(self.raw if raw is None else raw,p)

    def check_link(self,key):
        rows=self.rows(key);before=copy.deepcopy(rows)
        annotate_turns(rows,{key:self.links[key]})
        left,right=self.endpoints(key,rows)
        self.assertEqual(left['ID_Turno'],right['ID_Turno'])
        self.assertEqual(right['Relacion_Turno'],RELATION)
        self.assertEqual(right['ID_Antecedente_Continuidad'],left['ID_Intervencion'])
        self.assertFalse(left['ID_Ancla_Actor'])
        self.assertEqual(right['ID_Ancla_Actor'],right['ID_Intervencion'])
        self.assertEqual(len(rows),len(before))
        for old,new in zip(before,rows):
            self.assertEqual(old,{k:new[k] for k in old})
        self.assertFalse(validate_reviewed_links(rows,{key:self.links[key]}))
        members=[r['ID_Intervencion'] for r in rows if r['ID_Turno']==right['ID_Turno']]
        self.assertEqual(members,[left['ID_Intervencion'],right['ID_Intervencion']])

    def test_opt_in_required_for_every_pair(self):
        for key in LINKS:
            rows=annotate_turns(self.rows(key));left,right=self.endpoints(key,rows)
            self.assertNotEqual(left['ID_Turno'],right['ID_Turno'])

    def test_reviewed_left_sides_never_create_global_anchors(self):
        for key in LINKS:
            left,_=self.endpoints(key,self.rows(key));state={}
            update_state(state,left['Actor_Final'],left['Fuente_Actor'],left['Texto'],left['Fecha'],b.TURN_DETECTOR,b.split_sentences,'synthetic')
            self.assertFalse(state['anchor'])

    def test_changed_hash_or_bounds_reject_each_pair(self):
        for key in LINKS:
            for side in ['Anterior','Siguiente']:
                for field,value in [('SHA256_Texto_Padre','0'*64),('Fin',1),('Texto','inventado')]:
                    e=copy.deepcopy(self.links[key]);e[side][field]=value
                    with self.subTest(key=key,side=side,field=field),self.assertRaises(ValueError):self.load_one(e)

    def test_changed_actor_date_or_source_never_matches(self):
        for key in LINKS:
            for index in [0,1]:
                for field,value in [('Actor_Final','Otra persona'),('Fecha','1900-01-01'),('Fuente_Actor','CONTINUIDAD_PARRAFO')]:
                    rows=self.rows(key);pair=self.endpoints(key,rows);pair[index][field]=value
                    with self.subTest(key=key,index=index,field=field),self.assertRaises(ValueError):annotate_turns(rows,{key:self.links[key]})

    def test_pending_motives_on_either_endpoint_block_all_links(self):
        for key in LINKS:
            for index in [0,1]:
                for motive in ['TEXTO_DANADO_POR_COTEJAR','PASAJES_CONJUNTOS_POR_DELIMITAR','POSIBLE_OTRO_HABLANTE_O_MENCION']:
                    rows=self.rows(key);self.endpoints(key,rows)[index]['Motivos_Revision']=motive
                    with self.subTest(key=key,index=index,motive=motive),self.assertRaises(ValueError):annotate_turns(rows,{key:self.links[key]})

    def test_interposed_voice_prevents_matching(self):
        for key in LINKS:
            rows=self.rows(key);left,right=self.endpoints(key,rows);i=rows.index(right)
            extra=copy.deepcopy(left);extra.update(ID_Intervencion='insertada',ID_Bloque_Texto='insertada',Actor_Final='Otra persona')
            rows.insert(i,extra)
            with self.assertRaises(ValueError):annotate_turns(rows,{key:self.links[key]})

    def test_suspension_ends_group_before_same_actor_reopening(self):
        key=(3571,3572);rows=annotate_turns(self.rows(key),{key:self.links[key]})
        left,right=self.endpoints(key,rows);reopening=rows[-1]
        self.assertFalse(boundary(left['Texto']))
        self.assertTrue(boundary(right['Texto']))
        self.assertEqual(right['Actor_Final'],reopening['Actor_Final'])
        self.assertNotEqual(right['ID_Turno'],reopening['ID_Turno'])
        self.assertEqual(reopening['ID_Ancla_Actor'],reopening['ID_Intervencion'])
        self.assertFalse(reopening['ID_Antecedente_Continuidad'])
        self.assertIn('reanuda la sesión',reopening['Texto'])

    def test_institutional_and_other_speaker_tails_stay_separate(self):
        for key,actor in [((2838,2839),b.CONSEJO),((3123,3124),'José De Gregorio Rebeco')]:
            rows=annotate_turns(self.rows(key),{key:self.links[key]});_,right=self.endpoints(key,rows)
            self.assertEqual(rows[-1]['Actor_Final'],actor)
            self.assertNotEqual(rows[-1]['ID_Turno'],right['ID_Turno'])

    def test_short_duplicate_and_punctuation_flags_are_not_removed(self):
        for key,side,motive in [((2911,2912),0,'FRAGMENTO_BREVE'),((4470,4471),0,'DUPLICADO_NO_FORMULA')]:
            rows=self.rows(key);self.endpoints(key,rows)[side]['Motivos_Revision']=motive
            annotate_turns(rows,{key:self.links[key]})
            self.assertEqual(self.endpoints(key,rows)[side]['Motivos_Revision'],motive)
        self.assertTrue(self.parts(2918)[0][0].endswith(','))

    def test_damage_is_literal_not_a_certification_or_new_voice(self):
        self.assertTrue(self.parts(6118)[-1][0].startswith('V A juicio'))
        self.assertIn('procesos equivalentes en Al continuar',self.parts(6119)[0][0])
        self.assertIn('pendiente de cotejo',self.links[(6118,6119)]['Limitacion'])
        self.assertIn('mo erada',self.parts(6395)[0][0])

    def test_foreign_names_are_references_not_local_speakers(self):
        parts=self.parts(6394)
        self.assertEqual(len(parts),1)
        self.assertEqual(parts[0][1],'Sergio Lehmann Beresi')
        for name in ['Mario Draghi','Emmanuel Macron','Marina Silva']:self.assertIn(name,parts[0][0])

    def test_three_readings_are_scoped_and_do_not_change_rows(self):
        for p in [2839,3124,6394]:
            rows=self.rows((p,));before=copy.deepcopy(rows)
            reviews={k:e for k,e in self.mentions.items() if e['ID_Padre']==p and '-L28-' in k}
            self.assertEqual(len(reviews),1)
            errors,annotations=validate_mention_reviews(rows,reviews)
            self.assertFalse(errors);self.assertEqual(len(annotations),1)
            self.assertEqual(rows,before)
            self.assertEqual(next(iter(annotations.values()))['Estado_Lectura_Dirigida'],'MENCION_LEGITIMA_REVISADA')

    def test_f0_f1_are_not_claimed_as_exhaustive_ocr_review(self):
        for key in LINKS:
            self.assertIn('no certifica integridad del OCR',self.links[key]['Limitacion'])
            self.assertIn('Sin nuevo cotejo PDF ni muestra independiente',self.links[key]['Limitacion'])

    def test_fin_alone_is_not_boundary_or_anchor(self):
        self.assertFalse(boundary('Fin.'))
        state={};update_state(state,'Sergio Lehmann Beresi','CONTEXTO_REVISADO','Fin.','2014-09-11',b.TURN_DETECTOR,b.split_sentences,'fin')
        self.assertFalse(state['anchor'])

# Fixed source/segment and pre-existing registry fixtures follow. Generated once
# from the frozen LOOP27 baseline, not calculated from the current output.
    def test_link_121_122(self):
        self.check_link((121,122))

    def test_link_727_728(self):
        self.check_link((727,728))

    def test_link_2027_2028(self):
        self.check_link((2027,2028))

    def test_link_2838_2839(self):
        self.check_link((2838,2839))

    def test_link_2911_2912(self):
        self.check_link((2911,2912))

    def test_link_2918_2919(self):
        self.check_link((2918,2919))

    def test_link_3123_3124(self):
        self.check_link((3123,3124))

    def test_link_3571_3572(self):
        self.check_link((3571,3572))

    def test_link_4470_4471(self):
        self.check_link((4470,4471))

    def test_link_4903_4904(self):
        self.check_link((4903,4904))

    def test_link_5168_5169(self):
        self.check_link((5168,5169))

    def test_link_5872_5873(self):
        self.check_link((5872,5873))

    def test_link_6118_6119(self):
        self.check_link((6118,6119))

    def test_link_6394_6395(self):
        self.check_link((6394,6395))

    def test_parent_121_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[121]['Texto'].encode()).hexdigest(),'1fd7df4fc59ff688edad4f37f6162a6b6f35d41ed40d4b10070de41079642ed9')
        parts=self.parts(121)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Rodrigo Valdés Pulido', 3331, 'CONTEXTO_REVISADO', '0cc87eaafd3eeda7d83ad86c2d749d5151949a73c006e49c39c01d116e30578c')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[121]['Texto']))

    def test_parent_122_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[122]['Texto'].encode()).hexdigest(),'46d84f2879721fe69c9aabb5647164c2e0a6623d58b0b5214f0d149bd4065013')
        parts=self.parts(122)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Rodrigo Valdés Pulido', 959, 'SUJETO_ROL_SESION', '44c3032633fda7513d0c93414f5621f207f76129026306f0877f9c69c535c978')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[122]['Texto']))

    def test_parent_727_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[727]['Texto'].encode()).hexdigest(),'bd50b967cae2dde601931f5df0eac5638ddfd6bec2cdea185dae705309046d4d')
        parts=self.parts(727)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Vittorio Corbo Lioi', 231, 'SUJETO_ROL_SESION', 'f861a40348674df4ee97f3d801fe1ff734bcbd18df0db5fc0795c6a72e0ed7e9'), ('Consejo del Banco Central de Chile', 144, 'ACTA/META', 'f1f614ab68fccad8476ebf34507e7e3a56fcc9055f491427fa91b74a2b2d623c'), ('Vittorio Corbo Lioi', 139, 'SUJETO_ROL_NOMBRE', 'c00517fc234a759bf2647d2cbd9fcc14cf4c98914c6d2b9c3a00ff7a947a9e40'), ('Rodrigo Valdés Pulido', 53, 'CONTEXTO_REVISADO', '4e6e12f99a53a1f9ada1189b4b8e79949852dcd9cb8001d6fc9be189f4a2b0a5')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[727]['Texto']))

    def test_parent_728_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[728]['Texto'].encode()).hexdigest(),'08fd090ce5e4b9ef5d0ea72181cc20ed731f292b09131e0a38b4ad6926abcd32')
        parts=self.parts(728)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Rodrigo Valdés Pulido', 7984, 'SUJETO_ROL_SESION', '9cc6a1b66a065d9c68e7c25ca150831d35b6eac24497d9b2c57b93c1de96fa17')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[728]['Texto']))

    def test_parent_2027_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2027]['Texto'].encode()).hexdigest(),'ec828c142ff8416a1ccabb28ecfaac6c9a2c30c3428472e17562e47b1ad618f2')
        parts=self.parts(2027)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Jorge Desormeaux Jiménez', 127, 'SUJETO_ROL_NOMBRE', 'c9cdb4a9b0180f197ac0a938e5e3ed13cdc96cf2c713956dd7a18aa7121cf1a6'), ('Claudio Soto Gamboa', 56, 'CONTEXTO_REVISADO', 'f713b3066d44cfca25d2a8bfe8e1052349b823e35a5b23cb4381bb26023565e2')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2027]['Texto']))

    def test_parent_2028_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2028]['Texto'].encode()).hexdigest(),'8163ec5f2a57d960600bc92c84eb556c06588faf9f5b7ce6351bdd168e486b35')
        parts=self.parts(2028)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Claudio Soto Gamboa', 586, 'SUJETO_ROL_NOMBRE', '2e7a4aea88dcce4585429c4a599bdf8504926eb0e1ce0ea55d2471a712675bb8')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2028]['Texto']))

    def test_parent_2838_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2838]['Texto'].encode()).hexdigest(),'7334060401fd9477090cc4a154e523e3ef13244b82d218474a25306067f72057')
        parts=self.parts(2838)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Manuel Marfán Lewis', 1932, 'SUJETO_ROL_NOMBRE', '7b5b9137483ee3461e7dc3a5a31d6008dfa382d8a43c219ffce60d8b15c08764'), ('José De Gregorio Rebeco', 1431, 'CONTEXTO_REVISADO', 'ae2e6ea2d3ef82d776c6bf68c5829cce616652bcbb23b14fe49984a171c17de5')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2838]['Texto']))

    def test_parent_2839_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2839]['Texto'].encode()).hexdigest(),'21524c6553a8081fb48b0d7f5903961adb7a53afeea1bafc52768f0a3253ef93')
        parts=self.parts(2839)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('José De Gregorio Rebeco', 622, 'SUJETO_ROL_SESION', '01b99320ba0f5616da73739fa5c7d5fed3d6f24401dcdf9b00d57f0fda1f5ac2'), ('Consejo del Banco Central de Chile', 1431, 'ACTA/META', 'fb9b6559b374d54bc7241f0e75d8714731bf0b1a713ede1a3e5e174026b6754d')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2839]['Texto']))

    def test_parent_2911_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2911]['Texto'].encode()).hexdigest(),'757fea8bb62ce93702579737d1bcdf1fa3098d6355a72db4084310d9ee4c9755')
        parts=self.parts(2911)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Rodrigo Vergara Montes', 102, 'SUJETO_ROL_NOMBRE', '497c8ea81fb37e185dcc77a1da0847925f33173e5f9c59c9c5cb6f897f32ee3e'), ('Claudio Soto Gamboa', 37, 'CONTEXTO_REVISADO', '201c082ff471fe3b69347bd611b7eca03394713facb16f3bebba08bc6f100b05')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2911]['Texto']))

    def test_parent_2912_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2912]['Texto'].encode()).hexdigest(),'c91a63e301141645e684dbda326c6d499e94a5efa5b7a237876158dc3ed7a01c')
        parts=self.parts(2912)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Claudio Soto Gamboa', 1577, 'SUJETO_NOMBRE', '2a6340dd79254046fc2745e3617dabc8f75d8f5c0360adc4fcb4c6ce2ad2ce4f')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2912]['Texto']))

    def test_parent_2918_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2918]['Texto'].encode()).hexdigest(),'a554d225def6b218ab1a7f9d0aa51d50070a014aa05feb5a537586135f92f0bc')
        parts=self.parts(2918)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('José De Gregorio Rebeco', 50, 'SUJETO_ROL_SESION', '76d86f896ec26b68de0b45e343744b3d41bae736097831fd8c96d1c2c79a351e'), ('Claudio Soto Gamboa', 176, 'CONTEXTO_REVISADO', 'd9b0e2dbfbbcdaa7d38b5da61e4f5b879c7074ea2871e9e8788fc5300a0b571c')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2918]['Texto']))

    def test_parent_2919_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2919]['Texto'].encode()).hexdigest(),'a2440cd4ca75ef21b9e2b98fa7499dbe35376696eed1b2714c8ab4319941110e')
        parts=self.parts(2919)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Claudio Soto Gamboa', 994, 'SUJETO_NOMBRE', 'dc8632b7b26a50f31ea42b6c3391420fd25af507f9c96dbb746ae34af62eb417')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2919]['Texto']))

    def test_parent_3123_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3123]['Texto'].encode()).hexdigest(),'c84f302301f80057608ad0c754229a67ba49fb00415d524684d51d9814b2c2f6')
        parts=self.parts(3123)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Enrique Marshall Rivera', 4601, 'SUJETO_NOMBRE', 'a37ce3faccd1a46a6a264d4fe2656af214d3c83db9ebb80ce4bd48dcf1546688'), ('José De Gregorio Rebeco', 93, 'SUJETO_ROL_SESION', 'd0dac4f8445fe4e07db6bd15d36c8bf00d7e18fb10ee410fa5c487dbad36a324'), ('Manuel Marfán Lewis', 49, 'CONTEXTO_REVISADO', '78c1c05145d7da02e1dc5f478f45b95faec2c1878503aa3df378480c398a4aa5')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3123]['Texto']))

    def test_parent_3124_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3124]['Texto'].encode()).hexdigest(),'27e8835ce94ac8c5c435f47f59d3432cd975de59852afb9c25a277aa507cc4e3')
        parts=self.parts(3124)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Manuel Marfán Lewis', 5434, 'SUJETO_NOMBRE', '13e3657cb900c611c088f05dd75dbb337775c36efedbdb0e2f69501bc1e5e356'), ('José De Gregorio Rebeco', 711, 'SUJETO_ROL_NOMBRE', 'e7edc61bed34e69b8c863a9c6eaace17973effc09874875417e15f4e7ae0568b')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3124]['Texto']))

    def test_parent_3571_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3571]['Texto'].encode()).hexdigest(),'2152c6d07d89fa7f4ec211ef52b1c67b22a33cb94c8fa0dcfd7a4552e8bfc979')
        parts=self.parts(3571)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Manuel Marfán Lewis', 610, 'SUJETO_ROL_NOMBRE', '84258b6da8c3a96be0e315e5bd4e8d1cc41b02bd5fcf8498d3a49117520e6a9a'), ('José De Gregorio Rebeco', 325, 'CONTEXTO_REVISADO', '0c5632964b1d36c8a84dfe2fd600c2d37b76b075cbfbeed80d96ca73fea2b0db')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3571]['Texto']))

    def test_parent_3572_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3572]['Texto'].encode()).hexdigest(),'8883ad9cbefcc8178d33158fe9df9352aee0c5a83f7c82889bcf80f4e576f977')
        parts=self.parts(3572)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('José De Gregorio Rebeco', 85, 'SUJETO_ROL_NOMBRE', '65bb37a4839001e2d33076f2968c7db0c9ccd965fe0c2575c77f49e534f802f7'), ('José De Gregorio Rebeco', 198, 'SUJETO_ROL_NOMBRE', '9edf911f8cd362e4f58ada018b533781dddb98b780776acb20fab4b3451c9bd3')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3572]['Texto']))

    def test_parent_4470_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4470]['Texto'].encode()).hexdigest(),'f3126dd95e950b2596e2405c74085bdc3731fcc05842ec25c6acd700013550a1')
        parts=self.parts(4470)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Rodrigo Vergara Montes', 114, 'SUJETO_ROL_NOMBRE', 'cec40f73cf7e3606f012840255b55dc7f8e840d0fdc5bd0654b46e5ace70d02c'), ('Sergio Lehmann Beresi', 36, 'CONTEXTO_REVISADO', '32f8c017dc63b73272063a17033424e43f0b63de40c7a055719acdcb18b48739')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[4470]['Texto']))

    def test_parent_4471_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4471]['Texto'].encode()).hexdigest(),'d370da9db231b3fd40a343d35795f5899477097a7f846c2d62b54bb45cda440c')
        parts=self.parts(4471)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Sergio Lehmann Beresi', 2322, 'SUJETO_NOMBRE', 'e3d7eef8c56fabd5da678e30235418c771377ac928c880b69ecf13bbef6b2b52')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[4471]['Texto']))

    def test_parent_4903_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4903]['Texto'].encode()).hexdigest(),'35c0ddc674d67a974cbd7c8fbaaf21e9528e469c4e2eeeb1e36a8f852c05b525')
        parts=self.parts(4903)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Rodrigo Vergara Montes', 141, 'SUJETO_ROL_NOMBRE', 'cef5ceb4653438941829769729079676cdb600fb11df072263a0ba228d96e2b1'), ('Sergio Lehmann Beresi', 385, 'CONTEXTO_REVISADO', '17622cf07fb538d3791b2ff2a83d1546447746cfcd1685fed368d8eb2812e112')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[4903]['Texto']))

    def test_parent_4904_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4904]['Texto'].encode()).hexdigest(),'6fb53dd1e092c66c10aa41544a5d9e48f5cefc52a12c61847c387bbc21975663')
        parts=self.parts(4904)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Sergio Lehmann Beresi', 1518, 'SUJETO_NOMBRE', 'b0f8768b3b5648caad39f7961ee5337e5677ce52624835033818951eb635f829')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[4904]['Texto']))

    def test_parent_5168_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5168]['Texto'].encode()).hexdigest(),'f60e1de9b4fde7a0e4e993f2528427b6c6d794c1a10e4942eb2cb6738898ac07')
        parts=self.parts(5168)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Manuel Marfán Lewis', 155, 'SUJETO_ROL_SESION', '7ebb94b51e8d2b50afeaa6507ceba0a32cd92c04ecfcea307ed8aa5268d61155'), ('Sergio Lehmann Beresi', 149, 'CONTEXTO_REVISADO', '086b6c66852b8e058b6b81757061a1e3f501577920569e39ba792dff151f80fc')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[5168]['Texto']))

    def test_parent_5169_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5169]['Texto'].encode()).hexdigest(),'cf8c5461fd360d6fe137ba002da0fd4dbc4f58d103a876a8950fc654e049fe5e')
        parts=self.parts(5169)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Sergio Lehmann Beresi', 357, 'SUJETO_NOMBRE', 'b13a92f2694c8578024632dfb85d2c1b89bc706644ed22d1e98dc88b799d25b9')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[5169]['Texto']))

    def test_parent_5872_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5872]['Texto'].encode()).hexdigest(),'4a7f5819440fe8c2e3b2ee86e83c4c19be37baec8cf6d2c527341cd053d4c7b8')
        parts=self.parts(5872)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Manuel Marfán Lewis', 109, 'SUJETO_ROL_NOMBRE', 'dc214b69ca3d56de9e045e6fdbce6b0e8008bb46112f6d91fa5f396ea7930dcd'), ('Claudio Soto Gamboa', 98, 'CONTEXTO_REVISADO', 'd2ac70ef1aad45b7a888f4321399e1ddf8a24363bd2c384f4feff4610392d356')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[5872]['Texto']))

    def test_parent_5873_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5873]['Texto'].encode()).hexdigest(),'1d88cfe4dc6eb5522b1dd97697c17b4fc289902d39bd60d99da7a454cd679fb0')
        parts=self.parts(5873)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Claudio Soto Gamboa', 2809, 'SUJETO_NOMBRE', '59824b1fc73b4a9b2ae48d0d074f69df1f0f6f6a218a6d94e99bb7737a2eca61')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[5873]['Texto']))

    def test_parent_6118_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[6118]['Texto'].encode()).hexdigest(),'0ad5752390a1a76a704b1e2ba88432734ba20ec8657e063d065c85e9ab892579')
        parts=self.parts(6118)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Sebastián Claro Edwards', 416, 'SUJETO_ROL_NOMBRE', 'f16846ed8e57e152532cff01da72b6796385e8041f4f48b41d04f2f75e77c693'), ('Sergio Lehmann Beresi', 711, 'CONTEXTO_REVISADO', '83d71dd5ff9715f4c879ae17e370061d36b89a4aaa3318f22c052ad990c68c83')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6118]['Texto']))

    def test_parent_6119_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[6119]['Texto'].encode()).hexdigest(),'724e552c8ff45df07829a7b61f99740e17519adfb1dfa6632662733e137909b1')
        parts=self.parts(6119)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Sergio Lehmann Beresi', 9082, 'SUJETO_NOMBRE', 'fca6c6008abc403fdcd3a2297c5320c741e22ee94e1cbf65b2e2b1a654f723de')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6119]['Texto']))

    def test_parent_6394_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[6394]['Texto'].encode()).hexdigest(),'9a2478c3b2be188ddbc29ae461778225b2a6c1736bf7729a54bd63c1d69c7211')
        parts=self.parts(6394)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Sergio Lehmann Beresi', 1917, 'CONTEXTO_REVISADO', '8817527dd3d07446c6b303a806defc14741395539bb514be3e2968fa4c95ec28')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6394]['Texto']))

    def test_parent_6395_frozen_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[6395]['Texto'].encode()).hexdigest(),'6afb80ad0c83bbb1ada312c4ac754243cd5b658457bce538617ad62c00ea286b')
        parts=self.parts(6395)
        self.assertEqual([(a,len(compact(t)),m,hashlib.sha256(compact(t).encode()).hexdigest()) for t,a,m in parts],[('Sergio Lehmann Beresi', 12159, 'SUJETO_NOMBRE', '441d259310dd2b350855a4bbac78b7c77a266f1b01a8da191288f3c4e8cea041')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6395]['Texto']))

    def test_frozen_revisiones_continuidad_hablantes_prefix(self):
        entries=json.loads((ROOT/'data/curation/revisiones_continuidad_hablantes.json').read_text())
        self.assertEqual(digest(entries[:9]),'7eca014ea34e0818ad544e37a415eac605db38b20e710580c28fd86f14f9937c')

    def test_frozen_revisiones_menciones_actuales_prefix(self):
        entries=json.loads((ROOT/'data/curation/revisiones_menciones_actuales.json').read_text())
        self.assertEqual(digest(entries[:38]),'3102762bae3ec2f1f94797148b7be9071904b74536ae870d29d8d490183385fa')

    def test_frozen_revisiones_documentos_leidos_prefix(self):
        entries=json.loads((ROOT/'data/curation/revisiones_documentos_leidos.json').read_text())
        self.assertEqual(digest(entries[:12]),'b189d3c4e3f462c05c842650ab5f9608b2cbb2491f033e72c6960defaee5fe0c')

    def test_frozen_revisiones_continuaciones_acta_prefix(self):
        entries=json.loads((ROOT/'data/curation/revisiones_continuaciones_acta.json').read_text())
        self.assertEqual(digest(entries[:2]),'997074a565a0e1605055f6c568e349841ad2d1c2f158257591011d8d5454e2fe')

    def test_frozen_alertas_contextuales_retiradas_prefix(self):
        entries=json.loads((ROOT/'data/curation/alertas_contextuales_retiradas.json').read_text())
        self.assertEqual(digest(entries[:3]),'c0ad72321cd33d5b32dc7798ecdcdbb9fd473797e4e2fea992270d3c7caae6c5')

if __name__ == '__main__':
    unittest.main()
