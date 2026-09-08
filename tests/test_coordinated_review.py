"""Coordinaciones adjudicadas: no convertir toda «y» en un corte global."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, validate_speaker_reviews, SPEAKER_REVIEWS
from review_queue import track


class CoordinatedReviewTests(unittest.TestCase):
    def setUp(self):
        self.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        self.reviews=load_speaker_reviews(self.raw)

    def parts(self,p,review=None):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=review if review is not None else self.reviews[p])

    def test_twenty_three_coordinations_are_documented(self):
        self.assertEqual({p for p,r in self.reviews.items() if r.get('Tipo_Limite')=='COORDINACION_Y_EXPLICITA'},
            {1457,1737,1923,2392,2443,2555,2583,2608,2621,2661,2765,2768,2826,3158,3449,3650,3871,4233,6407,4857,6293,7044,5418})

    def test_votes_are_not_conflated_and_garcia_starts_afterwards(self):
        parts=self.parts(1737)
        self.assertEqual([a for t,a,m in parts],['Jorge Desormeaux Jiménez','Sebastián Claro Edwards','Pablo García Silva'])
        self.assertIn('6,50%',parts[1][0]);self.assertNotIn('6,50%',parts[0][0])
        self.assertTrue(parts[2][0].startswith('Una vez adoptado el Acuerdo'))

    def test_presenter_resumes_after_short_clarification(self):
        for p,expected in [(3449,['Sebastián Claro Edwards','José De Gregorio Rebeco','Luis Óscar Herrera Barriga','Sebastián Claro Edwards']),
            (2768,['José De Gregorio Rebeco','Sergio Lehmann Beresi','Enrique Marshall Rivera','Sergio Lehmann Beresi']),
            (4233,['Luis Óscar Herrera Barriga','Sergio Lehmann Beresi'])]:
            with self.subTest(parent=p):self.assertEqual([a for t,a,m in self.parts(p)],expected)

    def test_titles_in_quotes_do_not_block_real_speakers_outside(self):
        parts=self.parts(3871)
        self.assertEqual([a for t,a,m in parts],['Luis Óscar Herrera Barriga','José De Gregorio Rebeco'])
        self.assertIn('“Indicador',parts[0][0]);self.assertIn('“índice',parts[1][0])

    def test_unreviewed_coordination_is_not_automatically_split(self):
        r=self.raw[6407]
        self.assertEqual(len(b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])),1)

    def test_wrong_subject_blocks_inner_review(self):
        review=copy.deepcopy(self.reviews[1457]);review['Actor']='Vittorio Corbo Lioi'
        with self.assertRaisesRegex(ValueError,'límite válido'):self.parts(1457,review)

    def test_review_inside_quotation_is_rejected(self):
        review=copy.deepcopy(self.reviews[6407]);r=self.raw[6407]
        t='“'+r['Texto']+'”';review['Inicio']+=1;review['Fin']+=1
        with self.assertRaisesRegex(ValueError,'límite válido'):
            b.segment_turns(t,r['Fecha'],r['Actor'],review=review)

    def test_mention_without_finite_speech_is_rejected(self):
        text='El Presidente señor Corbo saluda y el Consejero señor Marfán está presente.'
        review=dict(Actor='Manuel Marfán Lewis',Inicio=text.index('y el'),Fin=len(text),Tipo_Limite='COORDINACION_Y_EXPLICITA')
        with self.assertRaisesRegex(ValueError,'límite válido'):
            b.segment_turns(text,'2005-02-10','Vittorio Corbo Lioi',review=review)

    def test_invalid_boundary_type_is_rejected(self):
        entries=json.loads(SPEAKER_REVIEWS.read_text());entries[-1]['Tipo_Limite']='CUALQUIER_CORTE'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'r.json';p.write_text(json.dumps(entries))
            with self.assertRaisesRegex(ValueError,'Tipo de límite'):load_speaker_reviews(self.raw,p)

    def test_all_reviewed_intervals_survive_with_exact_actor(self):
        rows=[]
        for p in self.reviews:
            for t,a,m in self.parts(p):rows.append(dict(ID=len(rows)+1,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m))
        self.assertEqual(len(self.reviews),91)
        self.assertEqual(validate_speaker_reviews(rows,self.reviews),[])

    def test_tracking_distinguishes_directed_correction(self):
        p=6407;r=self.raw[p]
        old=dict(ID=1,ID_Padre=p,Fecha=r['Fecha'],Texto=r['Texto'],Actor_Final=r['Actor'],Fuente_Actor='SUJETO_ROL_NOMBRE',
            Motivos_Revision='POSIBLE_OTRO_HABLANTE_O_MENCION',Inicio_Compacto=0,Fin_Compacto=len(''.join(r['Texto'].split())),SHA256_Texto='fixture')
        rows=[dict(ID=i,ID_Padre=p,Fecha=r['Fecha'],Texto=t,Actor_Final=a,Fuente_Actor=m,Motivos_Revision='FINAL_SIN_PUNTUACION' if i==1 else '')
              for i,(t,a,m) in enumerate(self.parts(p),1)]
        item=track(rows,{'Filas':[old]}, {},self.reviews)[0]
        self.assertEqual(item['Estado_Seguimiento'],'CORRECCION_DIRIGIDA_APLICADA')
        self.assertIn('HAB-20260907-6407',item['Justificacion'])
        self.assertIn('FINAL_SIN_PUNTUACION',item['Alertas_Actuales'])


if __name__=='__main__':unittest.main()
