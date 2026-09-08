"""Límites OCR, prefijos temáticos y adjudicación sin suprimir advertencias."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from review_queue import load_baseline, track
from turns import normalize


class MentionReviewTests(unittest.TestCase):
    def parts(self,p):
        r=next(r for r in b.data if r[0]==p)
        return b.segment_turns(r[5],b.to_date_str(r[1]),r[2])

    def test_broken_handoff_does_not_own_claro_vote(self):
        for p in [2121,2166,2293,2434]:
            with self.subTest(parent=p):
                parts=self.parts(p)
                self.assertEqual([a for t,a,m in parts],['José De Gregorio Rebeco','Sebastián Claro Edwards'])
                self.assertEqual(parts[0][0],'El Presidente ofrece la palabra a los señores Consejeros para proceder a la')
                self.assertTrue(parts[1][0].startswith('El Consejero señor Sebastián Claro'))
                self.assertEqual(parts[1][2],'SUJETO_ROL_NOMBRE')

    def test_quoted_broken_handoff_does_not_cut_quote(self):
        t='El Presidente señor Corbo señala: “El Presidente ofrece la palabra a los señores Consejeros para proceder a la El Consejero señor Marfán señala que apoya la opción”.'
        self.assertEqual(len(b.segment_turns(t,'2005-02-10','Vittorio Corbo Lioi')),1)

    def test_en_el_is_not_ocr_garbage(self):
        t='En el mismo sentido, el señor Soto agrega que existen riesgos.'
        self.assertEqual(b.TURN_DETECTOR.speaker(t,'2009-05-07')['actor'],'Claudio Soto Gamboa')

    def test_preposition_is_not_stripped_to_make_subject(self):
        self.assertIsNone(b.TURN_DETECTOR.speaker('De el señor Soto señala el informe varias observaciones.','2009-05-07'))

    def test_grammatical_role_variant(self):
        p=self.parts(2213)
        self.assertEqual([a for t,a,m in p],['Manuel Marfán Lewis','Pablo García Silva'])
        self.assertIn('Gerente de la División Estudios',p[-1][0])
        self.assertEqual(normalize(normalize(p[-1][0])),normalize(p[-1][0]))

    def test_habitual_thanks_stay_with_person_thanking(self):
        for p,actor in [(1565,'Enrique Marshall Rivera'),(1566,'Jorge Desormeaux Jiménez')]:
            with self.subTest(parent=p):
                parts=self.parts(p)
                self.assertTrue(parts[1][0].startswith('Como es habitual'))
                self.assertEqual(parts[1][1],actor)
                self.assertNotIn('Como es habitual',parts[0][0])

    def test_reviewed_aircraft_reply_and_return(self):
        from curation import load_speaker_reviews, validate_speaker_reviews
        raw={r[0]:{'Fecha':b.to_date_str(r[1]),'Texto':r[5]} for r in b.data}
        review=load_speaker_reviews(raw)[6135]
        parts=b.segment_turns(raw[6135]['Texto'],raw[6135]['Fecha'],'Miguel Fuentes Díaz',review=review)
        self.assertEqual([a for t,a,m in parts],['Miguel Fuentes Díaz','Claudio Soto Gamboa',
            'Miguel Fuentes Díaz','Ricardo Vicuña Poblete','Miguel Fuentes Díaz'])
        self.assertTrue(parts[3][0].startswith('en tanto el Gerente de División Estadísticas'))
        self.assertTrue(parts[4][0].startswith('El señor Miguel Fuentes retoma'))
        rows=[dict(ID=i,ID_Padre=6135,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts,1)]
        self.assertEqual(validate_speaker_reviews(rows,{6135:review}),[])

    def test_reference_locution_not_recipient_attribution(self):
        self.assertEqual([a for t,a,m in self.parts(7032)],['Beltrán de Ramón Acevedo'])
        self.assertEqual([a for t,a,m in self.parts(7058)],['Joaquín Vial Ruiz-Tagle',
            "Alberto Naudon Dell'Oro",'Joaquín Vial Ruiz-Tagle','Rodrigo Vergara Montes','Claudio Raddatz Kiefer'])

    def test_eight_mentions_are_documented(self):
        baseline,decisions=load_baseline()
        self.assertEqual({i for i,d in decisions.items() if d['Decision']=='MENCION_LEGITIMA_REVISADA'},
                         {710,854,1447,1721,1741,2061,3259,3301})

    def test_review_does_not_erase_automatic_reason(self):
        baseline,decisions=load_baseline();old=next(r for r in baseline['Filas'] if r['ID']==1447)
        # Un solo intervalo en una fixture: conservar el offset original.
        row={**old,'ID':1,'Motivos_Revision':'POSIBLE_OTRO_HABLANTE_O_MENCION'}
        old={**old,'Inicio_Compacto':0,'Fin_Compacto':len(''.join(old['Texto'].split()))}
        item=track([row],{'Filas':[old]},decisions)[0]
        self.assertEqual(item['Estado_Seguimiento'],'MENCION_LEGITIMA_REVISADA')
        self.assertIn('POSIBLE_OTRO_HABLANTE_O_MENCION',item['Alertas_Actuales'])


if __name__=='__main__':unittest.main()
