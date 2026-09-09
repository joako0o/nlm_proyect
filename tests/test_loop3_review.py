"""Bloque encadenado: actos institucionales, retornos y menciones acotadas."""
import copy
import hashlib
import re
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews,validate_speaker_reviews
PRES='José De Gregorio Rebeco'
SOTO='Claudio Soto Gamboa'
MARFAN='Manuel Marfán Lewis'
LEHMANN='Sergio Lehmann Beresi'
HERRERA='Luis Óscar Herrera Barriga'
VICUNA='Ricardo Vicuña Poblete'

class LoopThreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)
    def parts(self,p):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p))
    def test_fixed_read_sources_and_conservation(self):
        compact=lambda t:re.sub(r'\s+','',t)
        for p,h in SOURCE_HASHES.items():
            self.assertEqual(hashlib.sha256(self.raw[p]['Texto'].encode()).hexdigest(),h)
            self.assertEqual(compact(''.join(t for t,a,m in self.parts(p))),compact(self.raw[p]['Texto']))
    def test_3421_personal_gratitude_does_not_remain_in_institutional_block(self):
        parts=self.parts(3421)
        self.assertEqual([a for t,a,m in parts],['Enrique Marshall Rivera','Luis Opazo Roco',SOTO,PRES,PRES,PRES])
        self.assertEqual([len(t) for t,a,m in parts],[90,243,1143,201,108,797])
        self.assertIn('13:20',parts[3][0]);self.assertIn('16:00',parts[4][0])
        self.assertTrue(parts[5][0].startswith('Hace presente que esta es la última Sesión'))
        self.assertIn('da la bienvenida al señor Luis Óscar Herrera',parts[5][0])
        self.assertTrue(parts[5][0].endswith('Presidente.'))
    def test_3476_full_presentation_and_ocr_before_two_president_acts(self):
        parts=self.parts(3476)
        self.assertEqual([a for t,a,m in parts],[SOTO,MARFAN,SOTO,PRES,b.CONSEJO,PRES])
        self.assertEqual(len(parts[2][0]),2853)
        self.assertIn('Claudia Soto',parts[2][0]);self.assertIn('De Gregario',parts[3][0])
        self.assertTrue(parts[4][0].endswith('Política Monetaria'))
        self.assertIn('Felipe Larraín',parts[5][0]);self.assertIn('Luis Óscar Herrera',parts[5][0])
    def test_comment_closure_prefix_requires_subject_and_is_not_a_mention(self):
        for t in ['No habiendo comentarios, según el señor Presidente, la inflación aumenta.',
                  'No habiendo comentarios, el señor Presidente está presente.',
                  '“No habiendo comentarios, el señor Presidente agradece la exposición.”']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2010-09-16'))
    def test_explicit_welcome_does_not_certify_prior_anaphoric_gratitude(self):
        # Loop13 reconoce al Presidente que reanuda ANTES de Hace presente.
        # La anáfora aislada no es sujeto explícito; la revisión anterior se conserva.
        r=self.raw[3421];plain=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertEqual([(a,len(t)) for t,a,m in plain[-2:]],[(PRES,201),(PRES,906)])
        self.assertIn('Hace presente que esta es la última Sesión',plain[-1][0])
        self.assertIsNone(b.TURN_DETECTOR.speaker('Hace presente que esta es la última Sesión.',r['Fecha']))
        self.assertEqual([(a,len(t)) for t,a,m in self.parts(3421)[-2:]],[(PRES,108),(PRES,797)])
        r=self.raw[3476];plain=b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])
        self.assertEqual([(a,len(t)) for t,a,m in plain[-2:]],[(b.CONSEJO,66),(PRES,255)])
        self.assertEqual(plain[-1][0],self.parts(3476)[-1][0])
    def test_each_new_interval_survives_and_rejects_truncation(self):
        for p in SOURCE_HASHES.keys() & self.reviews.keys():
            rows=[dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p),1)]
            self.assertEqual(validate_speaker_reviews(rows,{p:self.reviews[p]}),[])
            next(r for r in rows if r['Fuente_Actor']=='CONTEXTO_REVISADO')['Texto']+=' añadido'
            self.assertTrue(validate_speaker_reviews(rows,{p:self.reviews[p]}))

    def test_vicuna_returns_after_soto_without_splitting_initial_exposition(self):
        parts=self.parts(3303)
        self.assertEqual([a for t,a,m in parts],[VICUNA,SOTO,VICUNA])
        self.assertEqual([len(t) for t,a,m in parts],[949,147,114])
        self.assertTrue(parts[2][0].startswith('en tanto que el señor Vicuña complementa'))
    def test_herrera_complement_is_not_president_mention(self):
        parts=self.parts(3650)
        self.assertEqual([a for t,a,m in parts],[LEHMANN,HERRERA])
        self.assertIn('confirma lo expresado por el señor Presidente',parts[0][0])
        self.assertIn('15 y 20%',parts[1][0])
    def test_lehmann_reply_and_exposition_remain_together(self):
        parts=self.parts(3651)
        self.assertEqual([a for t,a,m in parts],[PRES,LEHMANN])
        self.assertEqual(len(parts[1][0]),1283)
        self.assertIn('Al continuar con su presentación',parts[1][0])
        self.assertIn('Indica que esta situación se repite',parts[1][0])
    def test_new_inner_reviews_reject_wrong_actor_and_quotes(self):
        for p in [3303,3650]:
            r=self.raw[p];review=copy.deepcopy(self.reviews[p]);review['Actor']=PRES
            with self.assertRaisesRegex(ValueError,'límite válido'):
                b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=review)
            review=copy.deepcopy(self.reviews[p]);review['Inicio']+=1;review['Fin']+=1
            with self.assertRaisesRegex(ValueError,'límite válido'):
                b.segment_turns('“'+r['Texto']+'”',r['Fecha'],r['Actor'],review=review)
    def test_no_global_splitting_of_new_inner_complements(self):
        for p,count in [(3303,2),(3650,1)]:
            r=self.raw[p]
            self.assertEqual(len(b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])),count)

    def test_president_closes_discussion_after_marfan(self):
        parts=self.parts(3571)
        self.assertEqual([a for t,a,m in parts],[MARFAN,PRES])
        self.assertEqual([len(t) for t,a,m in parts],[736,390])
        self.assertIn('Al respecto, manifiesta',parts[1][0])
    def test_lehmann_explanation_not_absorbed_by_deramon(self):
        parts=self.parts(3737)
        self.assertEqual([a for t,a,m in parts],['Beltrán de Ramón Acevedo',LEHMANN])
        self.assertEqual([len(t) for t,a,m in parts],[429,548])
        self.assertIn('Coincide, además, con el Presidente',parts[0][0])
        self.assertIn('Agrega que en los períodos',parts[1][0])
    def test_new_closings_do_not_create_global_heuristics(self):
        for p,actor in [(3571,MARFAN),(3737,'Beltrán de Ramón Acevedo')]:
            r=self.raw[p]
            self.assertEqual([a for t,a,m in b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])],[actor])

    def test_marshall_remembers_garcia_without_garcia_turn(self):
        parts=self.parts(2768)
        self.assertEqual([a for t,a,m in parts],[PRES,LEHMANN,'Enrique Marshall Rivera',LEHMANN])
        self.assertIn('Pablo García, comentó',parts[2][0])
        self.assertIn('Señala desconocer',parts[2][0])
    def test_deramon_references_claro_and_lehmann_without_their_turns(self):
        parts=self.parts(3147)
        self.assertEqual([a for t,a,m in parts],[PRES,'Beltrán de Ramón Acevedo',PRES])
        self.assertIn('información que consideró el señor Lehmann',parts[1][0])
        self.assertIn('Para resumir',parts[1][0])
    def test_new_mention_annotations_keep_rows_warnings_and_exact_boundaries(self):
        from mention_reviews import load_mention_reviews,validate_mention_reviews
        reviews={k:r for k,r in load_mention_reviews(self.raw).items() if r['ID_Padre'] in [2768,3147]}
        rows=[]
        for p in [2768,3147]:
            for t,a,m in self.parts(p):
                rows.append(dict(ID=len(rows)+1,ID_Padre=p,Fecha=self.raw[p]['Fecha'],Texto=t,Actor_Final=a,Motivos_Revision='POSIBLE_OTRO_HABLANTE_O_MENCION'))
        before=copy.deepcopy(rows);errors,annotations=validate_mention_reviews(rows,reviews)
        self.assertEqual(errors,[]);self.assertEqual(len(annotations),2);self.assertEqual(rows,before)
        for rid in annotations:
            altered=copy.deepcopy(rows);altered[rid-1]['Texto']+=' añadido'
            errors,_=validate_mention_reviews(altered,reviews)
            self.assertTrue(errors)
    def test_joint_3191_is_not_adjudicated_by_single_person_assumption(self):
        # Protección de alcance, no certificación de la atribución heredada.
        self.assertEqual(self.reviews[3191]["Actor"],"Pablo García Silva")
        self.assertTrue(self.reviews[3191]["Cita_Inicio"].startswith("Al finalizar esta discusión"))
        self.assertGreater(self.reviews[3191]["Inicio"],0)
        self.assertIn('el señor Presidente y el señor Claudio Soto coinciden',self.raw[3191]['Texto'])

SOURCE_HASHES = {2768: '6249b0589812347de7c4a9bb5b20e4f78fd9e7137e406a91811116666095b30a', 3147: '89cda9f19ba68255595049376f5a771810604217912df600004dd509e382e5f4', 3191: 'd596d82b964da0af1585fba5293a53767bd77dc6dcf311807f1f4ac82401803d', 3303: '87b8e9aa37152b24797ed4c93baeb38b87bf5844764b2c36071d6d00ed642f66', 3421: 'f6f8d7474b7739072034ce6d15db2f7fa6fbf1ee9366cdd00b671fb35a2179cc', 3476: '38f69a35061dc74e623eb090222b575626caec6a937a3c883c8ec4512d8462ea', 3571: '2152c6d07d89fa7f4ec211ef52b1c67b22a33cb94c8fa0dcfd7a4552e8bfc979', 3650: '410a0347656717088cf9a46b2d5ce4841b634d1580e69b47bfd9eab0cdb7a8c4', 3651: '93271dab9f9aa8b4ba85182d596a89cddb8cae6e4fd2751a192b98748239a44f', 3737: '8a1dc0c8274d61739404f534249c49b02693a31ddcbcaf3790d8a17db0330cd6'}

if __name__=='__main__':unittest.main()
