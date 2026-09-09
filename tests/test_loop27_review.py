"""LOOP27: pausa institucional, voces entre artefactos y pasajes conjuntos."""
import copy, hashlib, json, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, validate_speaker_reviews
from institutional_reviews import (load_institutional_reviews, validate_institutional_reviews,
    institutional_type, NOTE, RESUME_NOTE, PATH as INST_PATH)
from context_warnings import load_context_warnings, contextual_motives
from mention_reviews import load_mention_reviews
from continuity import annotate_turns, update_state

class LoopTwentySevenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)
        cls.institutions=load_institutional_reviews(cls.raw)
        cls.warnings=load_context_warnings(cls.raw)
        cls.mentions=load_mention_reviews(cls.raw)

    def parts(self,p,reviewed=True):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],
            review=self.reviews.get(p) if reviewed else None,
            institution=self.institutions.get(p) if reviewed else None)

    def load_inst(self,entry,raw=None):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'review.json';p.write_text(json.dumps([entry]))
            return load_institutional_reviews(self.raw if raw is None else raw,p)

    def rows(self):
        rows=[]
        for p in [600,601]:
            for i,(text,actor,method) in enumerate(self.parts(p),1):
                meta=actor==b.CONSEJO
                note=''
                if p==601:note=(NOTE if meta else RESUME_NOTE)+self.institutions[p]['Revision_ID']+' (fuente)'
                rows.append(dict(ID=len(rows)+1,ID_Padre=p,ID_Intervencion=f'{p}:{i}',ID_Bloque_Texto=f'{p}:{i}',
                    Fecha=self.raw[p]['Fecha'],Texto=text,Actor_Final=actor,Fuente_Actor=method,
                    Rol_Final='Consejo' if meta else 'Gerente de Análisis Macroeconómico',
                    Fuente_Rol='ACTA_INSTITUCIONAL' if meta else 'LISTA_ASISTENCIA',
                    Tipo_Acta='ACTA_INSTITUCIONAL' if meta else '',Nota=note,Motivos_Revision=''))
        return annotate_turns(rows)

    def test_three_reviewed_intervals_have_exact_output(self):
        for p in [3120,4064,4476]:
            rows=[dict(ID=i,ID_Padre=p,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(self.parts(p))]
            self.assertFalse(validate_speaker_reviews(rows,{p:self.reviews[p]}))

    def test_context_review_is_not_a_global_anchor(self):
        for p in [3120,4064,4476]:
            for t,a,m in self.parts(p):
                if m=='CONTEXTO_REVISADO':
                    state={};update_state(state,a,m,t,self.raw[p]['Fecha'],b.TURN_DETECTOR,b.split_sentences,'review')
                    self.assertFalse(state['anchor'])

    def test_artifact_is_preserved_before_lehmann(self):
        parts=self.parts(4064)
        self.assertTrue(parts[0][0].endswith('-4 . f . • " \' A)'))
        self.assertTrue(parts[1][0].startswith('El señor Sergio Lehmann insiste en que '))
        self.assertTrue(parts[1][0].endswith('de cada país.'))
        self.assertEqual(len(self.parts(4064,False)),1)

    def test_artifact_mode_is_required(self):
        entry=copy.deepcopy(self.reviews[4064]);del entry['Tipo_Limite']
        with self.assertRaises(ValueError):
            b.segment_turns(self.raw[4064]['Texto'],self.raw[4064]['Fecha'],self.raw[4064]['Actor'],review=entry)

    def test_artifact_citation_and_actor_cannot_be_changed(self):
        for key,value in [('Cita_Artefacto','" '),('Actor','Rodrigo Vergara Montes')]:
            entry=copy.deepcopy(self.reviews[4064]);entry[key]=value
            with self.assertRaises(ValueError):
                b.segment_turns(self.raw[4064]['Texto'],self.raw[4064]['Fecha'],self.raw[4064]['Actor'],review=entry)

    def test_artifact_mode_does_not_bypass_a_real_unclosed_quote(self):
        entry=copy.deepcopy(self.reviews[4064]);entry['Inicio']+=1;entry['Fin']+=1
        with self.assertRaises(ValueError):
            b.segment_turns('“'+self.raw[4064]['Texto'],self.raw[4064]['Fecha'],self.raw[4064]['Actor'],review=entry)

    def test_artifact_mode_is_not_generic_missing_punctuation(self):
        entry=copy.deepcopy(self.reviews[4064])
        text=self.raw[4064]['Texto'].replace('A) ','B) ')
        with self.assertRaises(ValueError):
            b.segment_turns(text,self.raw[4064]['Fecha'],self.raw[4064]['Actor'],review=entry)

    def test_percibe_not_added_to_global_grammar(self):
        parts=self.parts(4476)
        self.assertEqual(parts[1][1],'Sergio Lehmann Beresi')
        self.assertIn('percibe que',parts[1][0])
        self.assertFalse(b.TURN_DETECTOR.speaker(parts[1][0],self.raw[4476]['Fecha']))
        self.assertEqual(parts[-1][1:],('Rodrigo Vergara Montes','SUJETO_ROL_NOMBRE'))
        self.assertEqual(len(parts[-1][0]),103)

    def test_minister_live_contribution_is_not_a_document(self):
        parts=self.parts(3120)
        self.assertEqual(parts[1][1:],('Felipe Larraín Bascuñán','SUJETO_ROL_SESION'))
        self.assertEqual(len(parts[1][0]),6723)
        self.assertIn('inflación vi* acotada',parts[1][0])
        self.assertNotIn('DOCUMENTO_ESCRITO_REVISADO',[m for t,a,m in parts])
        self.assertEqual(parts[-1][1],'José De Gregorio Rebeco')
        self.assertIn('Rodrigo Vergara',parts[-1][0])

    def test_pause_is_metadata_not_corbo_or_velasco_speech(self):
        parts=self.parts(601)
        self.assertEqual(parts[0][1:],(b.CONSEJO,'ACTA/META'))
        self.assertIn('interrumpe la sesión por diez minutos',parts[0][0])
        self.assertIn('Andrés Velasco',parts[0][0])
        self.assertEqual(parts[1][1:],('Pablo García Silva','SUJETO_NOMBRE'))
        self.assertTrue(parts[1][0].startswith('quien señala que '))
        self.assertNotIn('El señor Pablo García señala',parts[1][0])

    def test_economic_exposition_is_complete_after_pause(self):
        text=self.parts(601)[1][0]
        for phrase in ['Las tasas de interés','La demanda interna','Respecto de los precios','Las expectativas de mercado']:
            self.assertIn(phrase,text)
        self.assertTrue(text.endswith('mientras a dos años sigue en 3%.'))
        self.assertEqual(len(self.parts(601)),2)

    def test_pause_mode_requires_source_hash_bounds_and_nominal_evidence(self):
        entry=self.institutions[601]
        for key,value in [('SHA256_Texto_Padre','bad'),('Limite',1),('Texto_Acta','pausa'),
            ('Texto_Exposicion','informa'),('Nombre_Expositor','Sergio Lehmann'),
            ('Actor_Expositor','Vittorio Corbo Lioi'),('Decision','CONTINUACION_INSTITUCIONAL_NO_HABLA_PERSONAL')]:
            altered=copy.deepcopy(entry);altered[key]=value
            with self.assertRaises(ValueError):self.load_inst(altered)

    def test_unknown_scope_cannot_silently_reclassify_a_parent(self):
        e=copy.deepcopy(self.institutions[601]);e['Tipo_Alcance']='GENERAL'
        with self.assertRaises(ValueError):self.load_inst(e)

    def test_pause_requires_correct_input_date_and_actor(self):
        r=self.raw[601]
        for date,actor in [('2007-03-16',r['Actor']),(r['Fecha'],'Vittorio Corbo Lioi')]:
            with self.assertRaises(ValueError):b.segment_turns(r['Texto'],date,actor,institution=self.institutions[601])

    def test_pause_review_cannot_overlap_personal_or_documentary_review(self):
        r=self.raw[601]
        for kwargs in [dict(review={}),dict(document={})]:
            with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],institution=self.institutions[601],**kwargs)

    def test_type_only_applies_to_institutional_prefix(self):
        e=self.institutions[601]
        self.assertEqual(institutional_type(e['Texto_Acta'],e),'ACTA_INSTITUCIONAL')
        self.assertEqual(institutional_type(e['Texto_Exposicion'],e),'')
        with self.assertRaises(ValueError):institutional_type('otra oración',e)
        with self.assertRaises(ValueError):institutional_type(e['Texto_Padre'],e)

    def test_retired_edge_is_archived_not_silently_lost(self):
        e=self.institutions[601];archive=e['Enlace_Retirado']
        self.assertEqual(archive['Anterior']['ID_Padre'],600)
        self.assertEqual(archive['Siguiente']['ID_Padre'],601)
        self.assertEqual(archive['Anterior']['ID_Turno'],archive['Siguiente']['ID_Turno'])
        self.assertIn('interrupción',archive['Motivo'])
        rows=self.rows()
        self.assertNotEqual(rows[0]['ID_Turno'],rows[-1]['ID_Turno'])
        self.assertFalse(rows[1]['ID_Ancla_Actor'])
        self.assertEqual(rows[-1]['ID_Ancla_Actor'],rows[-1]['ID_Intervencion'])
        self.assertFalse(validate_institutional_reviews(rows,self.institutions_subset()))

    def institutions_subset(self):
        return {601:self.institutions[601]}

    def test_retired_archive_rejects_wrong_text_actor_parent_and_old_group(self):
        for side,key,value in [('Anterior','ID_Padre',599),('Siguiente','Texto','inventado'),
            ('Siguiente','Actor_Final','Vittorio Corbo Lioi'),('Siguiente','ID_Turno','otro')]:
            e=copy.deepcopy(self.institutions[601]);e['Enlace_Retirado'][side][key]=value
            with self.assertRaises(ValueError):self.load_inst(e)

    def test_institutional_output_cannot_hide_missing_or_corrupted_parts(self):
        for index in [1,2]:
            rows=self.rows();rows.pop(index)
            self.assertTrue(validate_institutional_reviews(rows,self.institutions_subset()))
        for index,key,value in [(1,'Actor_Final','Vittorio Corbo Lioi'),(1,'Tipo_Acta',''),
            (1,'ID_Ancla_Actor','fake'),(2,'Texto','truncado'),(2,'Actor_Final','Andrés Velasco Brañes'),
            (2,'Rol_Final','Consejo'),(2,'Fuente_Rol','ACTA_INSTITUCIONAL'),(2,'Tipo_Acta','ACTA_INSTITUCIONAL'),(2,'Nota',''),(2,'ID_Antecedente_Continuidad','600:1')]:
            rows=self.rows();rows[index][key]=value
            self.assertTrue(validate_institutional_reviews(rows,self.institutions_subset()))

    def test_original_3110_review_still_has_whole_parent_scope(self):
        e=self.institutions[3110]
        self.assertNotIn('Tipo_Alcance',e)
        self.assertEqual(self.parts(3110),[(self.raw[3110]['Texto'],b.CONSEJO,'ACTA/META')])

    def test_joint_passage_stays_pending_not_two_invented_voices(self):
        self.assertNotIn(2510,self.reviews)
        self.assertEqual(len(self.parts(2510)),4)
        e=next(e for e in self.mentions.values() if e['ID_Padre']==2510)
        self.assertEqual(e['Decision'],'PENDIENTE_DELIMITAR_APORTE')
        self.assertIn('Presidente y el Consejero señor Sebastián Claro comentan',self.parts(2510)[0][0])
        self.assertEqual([len(t) for t,a,m in self.parts(2510)][1:],[2071,243,503])

    def test_warnings_only_apply_to_exact_target_intervals(self):
        for p in [2510,4064]:
            for i,(t,a,m) in enumerate(self.parts(p)):
                row=dict(ID_Padre=p,Fecha=self.raw[p]['Fecha'],Texto=t,Actor_Final=a)
                self.assertEqual(bool(contextual_motives(row,self.warnings)),i==0)

    def test_negative_references_do_not_change_speakers(self):
        for p in [870,6601]:
            e=next(e for e in self.mentions.values() if e['ID_Padre']==p)
            self.assertEqual(e['Decision'],'MENCION_LEGITIMA_REVISADA')
        self.assertEqual(self.parts(870)[0][1],'Esteban Jadresic Marinovic')
        self.assertEqual(self.parts(6601)[0][1],"Alberto Naudon Dell'Oro")
        self.assertEqual(self.parts(6601)[-1][1: ],('Pablo García Silva','CONTEXTO_REVISADO'))

    def test_previous_pending_readings_are_not_closed(self):
        pending={e['ID_Padre'] for e in self.mentions.values() if e['Decision']=='PENDIENTE_DELIMITAR_APORTE'}
        self.assertEqual(pending,{6185,3775,4055,2510})

    def test_parent_4064_raw_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4064]['Texto'].encode()).hexdigest(), '92448b1cd681cd9809ba4df4f3e1899f10a50d9fdd3c9109943a5157df9cac48')
        parts = self.parts(4064)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Luis Óscar Herrera Barriga', 462, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 222, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[4064]['Texto'].split()))

    def test_parent_4476_raw_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4476]['Texto'].encode()).hexdigest(), '3b2d4250975a680529af9898f50d1d04a5991a5eaf6caf2e70c4dfd7699d746b')
        parts = self.parts(4476)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Rodrigo Vergara Montes', 395, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 797, 'CONTEXTO_REVISADO'), ('Rodrigo Vergara Montes', 103, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[4476]['Texto'].split()))

    def test_parent_3120_raw_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3120]['Texto'].encode()).hexdigest(), '57eb3416b57a1ce3e21592909b35ddf17936a33701faef8beb3ecc544c686584')
        parts = self.parts(3120)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('José De Gregorio Rebeco', 161, 'SUJETO_ROL_SESION'), ('Felipe Larraín Bascuñán', 6723, 'SUJETO_ROL_SESION'), ('José De Gregorio Rebeco', 162, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[3120]['Texto'].split()))

    def test_parent_600_raw_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[600]['Texto'].encode()).hexdigest(), '71e60e255b08471c87a34b351e3627433d927ba5ba94e8294f6467d9da019de3')
        parts = self.parts(600)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Pablo García Silva', 1896, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[600]['Texto'].split()))

    def test_parent_601_raw_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[601]['Texto'].encode()).hexdigest(), '1c3e2866efb830e60bc2e96887522cd8a7b6557d599ed2568fd078aec39d79cf')
        parts = self.parts(601)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Consejo del Banco Central de Chile', 310, 'ACTA/META'), ('Pablo García Silva', 3733, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[601]['Texto'].split()))

    def test_parent_2510_raw_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[2510]['Texto'].encode()).hexdigest(), 'b6bd404e4738d5b185086ac4752ad8ecdc46639381120451cb58f92297ba6b2a')
        parts = self.parts(2510)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('José De Gregorio Rebeco', 699, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 2071, 'SUJETO_NOMBRE'), ('José De Gregorio Rebeco', 243, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 503, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[2510]['Texto'].split()))

    def test_parent_870_raw_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[870]['Texto'].encode()).hexdigest(), '1a4f23d5de053f0ffce2e151fd12adba9c2692aa12e10368a9a1e891a084abb2')
        parts = self.parts(870)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Esteban Jadresic Marinovic', 1877, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[870]['Texto'].split()))

    def test_parent_6601_raw_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[6601]['Texto'].encode()).hexdigest(), 'd09e27e7abe213204a5ddda08e3ac34f9a4e28ec328e41b536ab9c26a7da7c51')
        parts = self.parts(6601)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [("Alberto Naudon Dell'Oro", 833, 'SUJETO_ROL_NOMBRE'), ('Beltrán de Ramón Acevedo', 311, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 542, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[6601]['Texto'].split()))

if __name__=='__main__':unittest.main()
