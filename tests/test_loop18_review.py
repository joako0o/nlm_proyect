"""LOOP18: voces omitidas, retornos tras comunicado y nombres literales."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews,speaker_intervals,validate_speaker_reviews
from context_warnings import load_context_warnings,contextual_motives
from continuity import annotate_turns
from review_flags import review_reasons
IDS=(1003,1424,1663,1742,1860,2354,2473,2778,2865,2909,2957,2990,3476,3619,4054,4594,5105,5106,5107,5108,5183,6113,6277)
N='Miguel Ángel Nacrur Gazali'
class LoopEighteenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw);cls.warnings=load_context_warnings(cls.raw)
    def parts(self,p,review=None):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p) if review is None else review)
    def rows(self,p):
        return [dict(ID=i,ID_Padre=p,ID_Intervencion=f'{p}:{i}',ID_Bloque_Texto=f'{p}:{i}',Fecha=self.raw[p]['Fecha'],Texto=t,Actor_Final=a,Fuente_Actor=m,Fuente_Rol='LISTA_ASISTENCIA',Duplicado_Exacto='NO',Duplicado_Formula='NO',Tipo_Acta='INTERVENCION') for i,(t,a,m) in enumerate(self.parts(p))]
    def test_all_bounded_intervals_validate(self):
        for p in IDS:self.assertFalse(validate_speaker_reviews(self.rows(p),{p:self.reviews[p]}))
    def test_legal_answers_and_marshall_return(self):
        for p in [5105,5106,5107]:self.assertEqual(self.parts(p)[1][1],N)
        self.assertEqual([a for t,a,m in self.parts(5108)],['Enrique Marshall Rivera',N,'Enrique Marshall Rivera',N])
    def test_6277_honoree_mention_is_not_first_speaker(self):
        parts=self.parts(6277)
        self.assertEqual([a for t,a,m in parts],['Rodrigo Vergara Montes',N,'Rodrigo Vergara Montes'])
        self.assertIn('Miguel Ángel Nacrur Gazali',parts[0][0]);self.assertEqual(len(parts[1][0]),95)
    def test_mattar_confirmation_not_a_vote_or_institutional_agreement(self):
        parts=self.parts(6113)
        self.assertEqual([a for t,a,m in parts],['Rodrigo Vergara Montes','Pablo Mattar Oyarzún',b.CONSEJO])
        self.assertIn('a solicitud del Presidente',parts[1][0]);self.assertNotIn('Comunicado',parts[1][0])
    def test_new_actors_have_explicit_roster_evidence(self):
        for p,actor in [(1742,'Luis Alberto Álvarez Vallejos'),(2354,'Luis Alberto Álvarez Vallejos'),(5105,N),(6113,'Pablo Mattar Oyarzún')]:
            e=self.reviews[p];self.assertEqual(e['Actor'],actor)
            self.assertTrue(any(e['ID_Padre']!=x['ID_Padre'] and b.norm(actor) in b.norm(x['Cita']) for x in e['Evidencia']))
    def test_5183_final_decision_is_institutional(self):
        parts=self.parts(5183)
        self.assertEqual([a for t,a,m in parts],['Ricardo Vicuña Poblete',N,'Ricardo Vicuña Poblete',b.CONSEJO])
        self.assertTrue(parts[-1][0].startswith('Se determinó,'));self.assertEqual(parts[-1][2],'ACTA/META')
    def test_institutional_exception_is_not_generic_se_determino(self):
        self.assertFalse(b._inst_transition('Se determinó que la inflación subiría.'))
    def test_4054_preserves_communicado_and_personal_change_of_vote(self):
        parts=self.parts(4054)
        self.assertEqual([a for t,a,m in parts],['Manuel Marfán Lewis',b.CONSEJO,'Manuel Marfán Lewis'])
        self.assertTrue(parts[1][0].endswith('política.”'))
        self.assertIn('sumarse al voto de mayoría',parts[2][0]);self.assertIn('reservar su disidencia',parts[2][0])
    def test_post_quote_return_requires_opt_in(self):
        e=copy.deepcopy(self.reviews[4054]);e.pop('Tipo_Limite')
        with self.assertRaises(ValueError):self.parts(4054,e)
    def test_post_quote_return_rejects_missing_close_quote(self):
        r=self.raw[4054];e=self.reviews[4054];t=r['Texto'];a=e['Inicio'];prefix=t[:a];pos=prefix.rfind('”');bad=t[:pos]+' '+t[pos+1:]
        with self.assertRaises(ValueError):b.segment_turns(bad,r['Fecha'],r['Actor'],review=e)
    def test_post_quote_return_requires_matching_explicit_actor(self):
        e=copy.deepcopy(self.reviews[4054]);e['Actor']='Pablo García Silva'
        with self.assertRaises(ValueError):self.parts(4054,e)
    def test_gerund_reply_in_2957_separates_question_and_president(self):
        parts=self.parts(2957)
        self.assertEqual([a for t,a,m in parts],['Kevin Cowan Logan','Pablo García Silva','José De Gregorio Rebeco','Manuel Marfán Lewis','Claudio Soto Gamboa'])
        self.assertTrue(parts[2][0].startswith('señalando el señor Presidente'))
    def test_gerund_requires_its_bounded_type(self):
        e=copy.deepcopy(self.reviews[2957]);e['Revisiones_Adicionales'][0].pop('Tipo_Limite')
        with self.assertRaises(ValueError):self.parts(2957,e)
    def test_new_reviewed_sources_never_create_anchors(self):
        for p in IDS:
            rows=self.rows(p);annotate_turns(rows)
            for r in rows:
                if r['Fuente_Actor']=='CONTEXTO_REVISADO':self.assertFalse(r['ID_Ancla_Actor'])
    def test_posterior_soto_anchors_stay_explicit(self):
        for p,n in [(2778,1810),(2909,2465)]:
            rows=self.rows(p);annotate_turns(rows)
            self.assertEqual(len(rows[-1]['Texto']),n);self.assertTrue(rows[-1]['ID_Ancla_Actor'])
    def test_fin_alone_does_not_create_posterior_anchor(self):
        for p in [2778,2909]:
            e=copy.deepcopy(self.reviews[p]);e.pop('Cita_Ancla_Posterior')
            self.assertLess(len(self.parts(p,e)),len(self.parts(p)))
    def test_long_reviewed_soto_development_not_fragmented_by_ocr_name(self):
        for p,n in [(2990,2689),(3476,2853),(3619,4133)]:
            self.assertTrue(any(len(t)==n and a=='Claudio Soto Gamboa' and m=='CONTEXTO_REVISADO' for t,a,m in self.parts(p)))
    def test_names_and_damaged_prefix_remain_warned_literally(self):
        for p,needle in [(1424,'Marshali'),(1663,'Manual Marfán'),(1860,'Oesormeaux'),(2865,'Rabio'),(2957,'Rabio'),(1003,'Madgenzo'),(2990,'Claudia Soto'),(3476,'Claudia Soto'),(3619,'Claudia Soto'),(2473,'Al Presidente')]:
            hits=[r for r in self.rows(p) if contextual_motives(r,self.warnings)]
            self.assertEqual(len(hits),1);self.assertIn(needle,hits[0]['Texto'])
    def test_4594_ricaurte_identity_still_pending(self):
        r=self.rows(4594)[1]
        self.assertEqual(r['Actor_Final'],'Miguel Ricaurte Bermúdez')
        self.assertIn('VARIANTE_IDENTIDAD_POR_VERIFICAR',review_reasons(r,b.TURN_DETECTOR,b.split_sentences))
    def test_3476_previous_closing_review_remains(self):
        self.assertEqual(len(speaker_intervals(self.reviews[3476])),2)
        self.assertEqual(len(self.parts(3476)[-1][0]),255)
    def test_pending_cases_and_226_continuation_not_forced(self):
        self.assertFalse({226,6185,2126,3989}&set(self.reviews))
        for p in [780,4433,6530,3191,5367]:self.assertIn(p,self.warnings)
    def test_changed_source_rejects_new_review(self):
        raw=copy.deepcopy(self.raw);raw[4054]['Texto']+=' X'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'r.json';p.write_text(json.dumps([self.reviews[4054]]))
            with self.assertRaises(ValueError):load_speaker_reviews(raw,p)
    def test_parent_1003_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1003]['Texto'].encode()).hexdigest(),'b68231dcb9bfd1989c15c4c1cd450326e8910da5492c34e032ade1ba84ae59b3')
        parts=self.parts(1003)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 82, 'SUJETO_ROL_SESION'), ('José De Gregorio Rebeco', 145, 'SUJETO_ROL_NOMBRE'), ('Igal Magendzo Weinberger', 996, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 346, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 372, 'SUJETO_ROL_NOMBRE'), ('Igal Magendzo Weinberger', 223, 'SUJETO_ROL_NOMBRE'), ('Andrés Velasco Brañes', 108, 'SUJETO_ROL_SESION'), ('Igal Magendzo Weinberger', 687, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 618, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Valdés Pulido', 745, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1003]['Texto'].split()))
    def test_parent_1424_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1424]['Texto'].encode()).hexdigest(),'3a0d157ee8b72c3cf681d582b0911e80a8bb022cf629a58028d967c3a206f372')
        parts=self.parts(1424)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 266, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 200, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1424]['Texto'].split()))
    def test_parent_1663_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1663]['Texto'].encode()).hexdigest(),'78012bb10422d06cf0116b6f5d53a5cdd6b74fc65c5edb0195136b3cd43041d4')
        parts=self.parts(1663)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Pablo García Silva', 416, 'SUJETO_ROL_NOMBRE'), ('Igal Magendzo Weinberger', 452, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 1662, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1663]['Texto'].split()))
    def test_parent_1742_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1742]['Texto'].encode()).hexdigest(),'6efc0b61e73af2dd960adc89b84c18097978c8deab6dfd768bd078515fb80d98')
        parts=self.parts(1742)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 893, 'SUJETO_ROL_NOMBRE'), ('Luis Alberto Álvarez Vallejos', 316, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1742]['Texto'].split()))
    def test_parent_1860_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1860]['Texto'].encode()).hexdigest(),'227ea475cd0c457f2c23720a2575767be3cad408626e4e83efae87f17c7219f0')
        parts=self.parts(1860)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 183, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 1716, 'SUJETO_ROL_NOMBRE'), ('Jorge Desormeaux Jiménez', 692, 'CONTEXTO_REVISADO'), ('Sergio Lehmann Beresi', 260, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1860]['Texto'].split()))
    def test_parent_2354_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2354]['Texto'].encode()).hexdigest(),'bc08a4fafedfe170375d96f3fbb9c4c053485c675ecbf62a74ebec1db8853c10')
        parts=self.parts(2354)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 112, 'SUJETO_ROL_NOMBRE'), ('Luis Alberto Álvarez Vallejos', 686, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2354]['Texto'].split()))
    def test_parent_2473_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2473]['Texto'].encode()).hexdigest(),'d4bfd592899ddf3deb76e4ff15723b2b216a212d352adfa7bd93091e31367af3')
        parts=self.parts(2473)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 644, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 158, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2473]['Texto'].split()))
    def test_parent_2778_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2778]['Texto'].encode()).hexdigest(),'eee788b3aac2d7f00fc7f4ef78ad8e4c2e0121fb9ecf0a3a02b54c6f0cc76516')
        parts=self.parts(2778)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 519, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 803, 'CONTEXTO_REVISADO'), ('Claudio Soto Gamboa', 1810, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2778]['Texto'].split()))
    def test_parent_2865_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2865]['Texto'].encode()).hexdigest(),'f81e8509254b070c8bfb22547be2b9f9dfd4e732076682eb0c87afb5bdda254e')
        parts=self.parts(2865)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 177, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 335, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2865]['Texto'].split()))
    def test_parent_2909_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2909]['Texto'].encode()).hexdigest(),'cf247ccb606ae1f6d3a657706704c4b41e7601092f6055e1ac2eff2558dfaa98')
        parts=self.parts(2909)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 1806, 'SUJETO_NOMBRE'), ('Manuel Marfán Lewis', 1244, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 604, 'CONTEXTO_REVISADO'), ('Claudio Soto Gamboa', 2465, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2909]['Texto'].split()))
    def test_parent_2957_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2957]['Texto'].encode()).hexdigest(),'c6417350f1954be7272763cbdd19e4d21ecd20f095dee2ddeec2ddbc19dfa048')
        parts=self.parts(2957)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Kevin Cowan Logan', 772, 'SUJETO_NOMBRE'), ('Pablo García Silva', 73, 'CONTEXTO_REVISADO'), ('José De Gregorio Rebeco', 117, 'CONTEXTO_REVISADO'), ('Manuel Marfán Lewis', 907, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 1626, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2957]['Texto'].split()))
    def test_parent_2990_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2990]['Texto'].encode()).hexdigest(),'e3228baa9adc030b515ebaa5a5eef383a9ab78f836ee12d1a074aaf358334449')
        parts=self.parts(2990)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 2689, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2990]['Texto'].split()))
    def test_parent_3476_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3476]['Texto'].encode()).hexdigest(),'38f69a35061dc74e623eb090222b575626caec6a937a3c883c8ec4512d8462ea')
        parts=self.parts(3476)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 925, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 766, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 2853, 'CONTEXTO_REVISADO'), ('José De Gregorio Rebeco', 236, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 66, 'ACTA/META'), ('José De Gregorio Rebeco', 255, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3476]['Texto'].split()))
    def test_parent_3619_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3619]['Texto'].encode()).hexdigest(),'a4bfca6b45a79760879d2a98756c8f409a43960f9058bdafe1cd437f88c4db5a')
        parts=self.parts(3619)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 4133, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3619]['Texto'].split()))
    def test_parent_4054_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[4054]['Texto'].encode()).hexdigest(),'ea9baf2d6fa6a1c6897a6aaaffdc1c656cdc2a1cda5a0d69799eb474ef52dc98')
        parts=self.parts(4054)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 191, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 1399, 'ACTA/META'), ('Manuel Marfán Lewis', 539, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4054]['Texto'].split()))
    def test_parent_4594_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[4594]['Texto'].encode()).hexdigest(),'6b573417922dfc64bca0ca221d9dd7b7c2a2a85576fc75d7e6af3e397b4f06d2')
        parts=self.parts(4594)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Luis Óscar Herrera Barriga', 1149, 'SUJETO_NOMBRE'), ('Miguel Ricaurte Bermúdez', 1567, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4594]['Texto'].split()))
    def test_parent_5105_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[5105]['Texto'].encode()).hexdigest(),'2d09a363a43e525759eb6057f7d3ef0154919ef89307d64ad37afb0b5bbaa326')
        parts=self.parts(5105)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 168, 'SUJETO_ROL_NOMBRE'), ('Miguel Ángel Nacrur Gazali', 468, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5105]['Texto'].split()))
    def test_parent_5106_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[5106]['Texto'].encode()).hexdigest(),'e191698dead806d3033e8e160f8001245978acde7053c2253bb0f7d6566ae54a')
        parts=self.parts(5106)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 106, 'SUJETO_ROL_NOMBRE'), ('Miguel Ángel Nacrur Gazali', 1395, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5106]['Texto'].split()))
    def test_parent_5107_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[5107]['Texto'].encode()).hexdigest(),'33afeae09f5e488d092d939f0b26af26b82204d9d038a5117043c6d220944e2b')
        parts=self.parts(5107)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 169, 'SUJETO_ROL_NOMBRE'), ('Miguel Ángel Nacrur Gazali', 213, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5107]['Texto'].split()))
    def test_parent_5108_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[5108]['Texto'].encode()).hexdigest(),'49eea3c54b9d8af60d288223cc1eb5a71c7ebbd9a096a6f03f659fdc13d2bf3d')
        parts=self.parts(5108)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 289, 'SUJETO_ROL_NOMBRE'), ('Miguel Ángel Nacrur Gazali', 465, 'CONTEXTO_REVISADO'), ('Enrique Marshall Rivera', 510, 'SUJETO_ROL_NOMBRE'), ('Miguel Ángel Nacrur Gazali', 613, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5108]['Texto'].split()))
    def test_parent_5183_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[5183]['Texto'].encode()).hexdigest(),'17a3d1ddda94e1bcec81d0f018239e1a65822bc45ec211606d3a0d51f93639e3')
        parts=self.parts(5183)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Ricardo Vicuña Poblete', 401, 'SUJETO_NOMBRE'), ('Miguel Ángel Nacrur Gazali', 316, 'CONTEXTO_REVISADO'), ('Ricardo Vicuña Poblete', 656, 'SUJETO_NOMBRE'), ('Consejo del Banco Central de Chile', 212, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5183]['Texto'].split()))
    def test_parent_6113_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6113]['Texto'].encode()).hexdigest(),'d7c377f5b39512958e0b649b3d7641368654034b2506d2ebbdcc91d7dcd7a4da')
        parts=self.parts(6113)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 5063, 'SUJETO_ROL_NOMBRE'), ('Pablo Mattar Oyarzún', 229, 'CONTEXTO_REVISADO'), ('Consejo del Banco Central de Chile', 2334, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6113]['Texto'].split()))
    def test_parent_6277_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6277]['Texto'].encode()).hexdigest(),'720a8dd6ff973c60e8b73366a41b4ac2ddfe692c7eb59ec2361efd5e55a44144')
        parts=self.parts(6277)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 960, 'CONTEXTO_REVISADO'), ('Miguel Ángel Nacrur Gazali', 95, 'CONTEXTO_REVISADO'), ('Rodrigo Vergara Montes', 373, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6277]['Texto'].split()))
