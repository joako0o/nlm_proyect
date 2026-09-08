"""Loop13: anáforas revisadas, límites de acta y sesiones, sin perder continuidad."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, validate_speaker_reviews, speaker_intervals
from institutional_reviews import load_institutional_reviews, institutional_parts, validate_institutional_reviews, NOTE
from context_warnings import load_context_warnings, contextual_motives
from continuity import annotate_turns

class LoopThirteenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw)
        cls.institutions=load_institutional_reviews(cls.raw)
    def parts(self,p,**kw):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p),institution=self.institutions.get(p),**kw)
    def load_entries(self,entries,raw=None):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'review.json';path.write_text(json.dumps(entries));return load_institutional_reviews(raw or self.raw,path)
    def inst_row(self):
        e=self.institutions[3110]
        return dict(ID=1,ID_Padre=3110,Fecha=e['Fecha'],Actor_Final=b.CONSEJO,Fuente_Actor='ACTA/META',Fuente_Rol='ACTA_INSTITUCIONAL',Tipo_Acta='ACTA_INSTITUCIONAL',Rol_Final='Consejo',Texto=e['Texto_Padre'],Nota=NOTE+e['Revision_ID']+' (fuente)',ID_Ancla_Actor='',ID_Antecedente_Continuidad='')
    def test_institutional_fragment_is_not_orellana_speech(self):
        self.assertEqual(self.parts(3110),[(self.raw[3110]['Texto'],b.CONSEJO,'ACTA/META')])
        self.assertIn('comunicado oportunamente por el señor Orellana',self.parts(3110)[0][0])
        self.assertFalse(validate_institutional_reviews([self.inst_row()],self.institutions))
    def test_institutional_review_cannot_overlap_person_or_document(self):
        r=self.raw[3110]
        for opts in [dict(review={}),dict(document={})]:
            with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],institution=self.institutions[3110],**opts)
    def test_institutional_review_clears_state_not_creates_anchor(self):
        state=dict(date=self.raw[3110]['Fecha'],anchor=1,roles={'Gerente':'Enrique Orellana Cifuentes'},last_sentence='Texto',pending='Otro')
        self.parts(3110,state=state)
        self.assertFalse(state['anchor']);self.assertFalse(state['roles']);self.assertFalse(state['pending']);self.assertTrue(state['barrier'])
    def test_institutional_target_hash_cannot_change(self):
        raw=copy.deepcopy(self.raw);raw[3110]['Texto']+=' X'
        with self.assertRaises(ValueError):self.load_entries(list(self.institutions.values()),raw)
    def test_institutional_antecedent_hash_cannot_change(self):
        raw=copy.deepcopy(self.raw);raw[3109]['Texto']+=' X'
        with self.assertRaises(ValueError):self.load_entries(list(self.institutions.values()),raw)
    def test_institutional_antecedent_must_be_immediate(self):
        e=copy.deepcopy(self.institutions[3110]);e['ID_Antecedente']=3108
        with self.assertRaises(ValueError):self.load_entries([e])
    def test_institutional_evidence_cannot_cross_session(self):
        raw=copy.deepcopy(self.raw);raw[3109]['Fecha']='2011-01-01'
        with self.assertRaises(ValueError):self.load_entries(list(self.institutions.values()),raw)
    def test_institutional_evidence_must_end_antecedent(self):
        e=copy.deepcopy(self.institutions[3110]);e['Cita_Antecedente']='El Presidente'
        with self.assertRaises(ValueError):self.load_entries([e])
    def test_institutional_review_requires_scope(self):
        for field in ['Cita_Antecedente','Decision','Justificacion','Limitacion','Texto_Padre']:
            e=copy.deepcopy(self.institutions[3110]);e[field]=''
            with self.assertRaises(ValueError):self.load_entries([e])
    def test_institutional_duplicates_rejected(self):
        e=self.institutions[3110]
        with self.assertRaises(ValueError):self.load_entries([e,e])
    def test_institutional_direct_output_rejects_changed_text(self):
        with self.assertRaises(ValueError):institutional_parts('inventado',self.institutions[3110])
    def test_institutional_validation_rejects_personal_actor_and_role(self):
        for field,value in [('Actor_Final','Enrique Orellana Cifuentes'),('Fuente_Actor','CONTEXTO_REVISADO'),('Fuente_Rol','LISTA_ASISTENCIA'),('Tipo_Acta',''),('Rol_Final','Gerente'),('Texto','Inventado'),('Nota',''),('ID_Ancla_Actor','1'),('ID_Antecedente_Continuidad','1')]:
            r=self.inst_row();r[field]=value
            self.assertTrue(validate_institutional_reviews([r],self.institutions))
    def test_institutional_validation_rejects_missing_and_duplicate(self):
        self.assertTrue(validate_institutional_reviews([],self.institutions))
        r=self.inst_row();self.assertTrue(validate_institutional_reviews([r,r],self.institutions))
    def test_institutional_validation_rejects_unregistered_annotation(self):
        self.assertTrue(validate_institutional_reviews([self.inst_row()],{}))
    def test_3110_damaged_links_are_preserved_not_repaired(self):
        self.assertTrue(self.raw[3109]['Texto'].endswith('fijado por.'))
        self.assertTrue(self.parts(3110)[0][0].endswith('A continuación,.'))
    def test_timed_personal_reopening_keeps_named_speaker(self):
        for p in [3067,3109,3193,3328,3421,3572]:
            timed=[(t,a,m) for t,a,m in self.parts(p) if t.startswith('Siendo las')]
            self.assertEqual(len(timed),1)
            self.assertEqual(timed[0][1:],('José De Gregorio Rebeco','SUJETO_ROL_NOMBRE'))
    def test_timed_narrative_without_person_stays_institutional(self):
        for lead in ['Siendo las 16:00 horas,','A las 16:00 horas,']:
            t=lead+' se reanuda la Sesión de Política Monetaria N° 167.'
            self.assertTrue(b._inst_transition(t));self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2011-05-12'))
            self.assertEqual(b.segment_turns(t,'2011-05-12','José De Gregorio Rebeco')[0][1],b.CONSEJO)
    def test_timed_prefix_does_not_accept_invalid_hour_or_attendance(self):
        for t in ['Siendo las 25:00 horas, el Presidente señor José De Gregorio reanuda la sesión.',
                  'Siendo las 16:99 horas, el Presidente señor José De Gregorio reanuda la sesión.',
                  'Siendo las 16:00 horas, el Presidente señor José De Gregorio está presente.',
                  '“Siendo las 16:00 horas, el Presidente señor José De Gregorio reanuda la sesión.”']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(t,'2010-09-16'))
    def test_3881_attendance_not_swallowed_by_presidential_speech(self):
        parts=self.parts(3881);self.assertEqual(len(parts),4)
        self.assertEqual(parts[2][1],b.CONSEJO);self.assertIn('incorporándose',parts[2][0])
        self.assertNotIn('incorporándose',parts[1][0]);self.assertIn('da la bienvenida',parts[3][0])
    def test_reopening_does_not_merge_morning_and_afternoon(self):
        parts=self.parts(3109);self.assertEqual(len(parts),3)
        rows=[dict(ID_Intervencion=str(i),ID_Bloque_Texto=str(i),Fecha=self.raw[3109]['Fecha'],Texto=t,Actor_Final=a,Fuente_Actor=m,Tipo_Acta='' if a!=b.CONSEJO else 'ACTA_INSTITUCIONAL',Motivos_Revision='') for i,(t,a,m) in enumerate(parts)]
        annotate_turns(rows);self.assertNotEqual(rows[0]['ID_Turno'],rows[1]['ID_Turno'])
    def test_same_actor_review_start_keeps_its_own_source_and_note_scope(self):
        parts=self.parts(3421)
        self.assertEqual([m for t,a,m in parts[-2:]],['SUJETO_ROL_NOMBRE','CONTEXTO_REVISADO'])
        self.assertTrue(parts[-1][0].startswith(self.reviews[3421]['Cita_Inicio']))
        rows=[dict(ID=i,ID_Padre=3421,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
        self.assertFalse(validate_speaker_reviews(rows,{3421:self.reviews[3421]}))
    def test_formal_headers_are_not_personal_vote(self):
        for p in [2438,2839,3126,3205]:
            parts=self.parts(p);self.assertEqual(len(parts),2)
            self.assertEqual(parts[0][1],'José De Gregorio Rebeco');self.assertEqual(parts[1][1],b.CONSEJO)
            self.assertRegex(parts[1][0],r'^\d{2,3}-\d{2}-\d{6}-')
    def test_formal_header_requires_code_and_exact_title(self):
        for t in ['T a s a de Política Monetaria.', '154-01-100513-Tasa de inflación.', '154-01-100513-Tasa de Política Monetaria baja.', 'Comenta que 154-01-100513-Tasa de Política Monetaria.', '“154-01-100513-Tasa de Política Monetaria.”']:
            self.assertFalse(b._inst_transition(t))
    def test_new_named_predicates_not_attendance_or_mention(self):
        for head in ['El Consejero señor Enrique Marshall','El Consejero señor Manuel Marfán, como siempre,']:
            self.assertIsNone(b.TURN_DETECTOR.speaker(head+' está presente.','2006-01-12'))
        self.assertIsNone(b.TURN_DETECTOR.speaker('Se refiere al Consejero señor Enrique Marshall que hace una observación.','2006-01-12'))
    def test_1923_keeps_old_minister_review_and_adds_short_lehmann_answer(self):
        entries=speaker_intervals(self.reviews[1923]);self.assertEqual(len(entries),2)
        self.assertEqual(entries[0]['Actor'],'Andrés Velasco Brañes');self.assertEqual(entries[1]['Actor'],'Sergio Lehmann Beresi')
        self.assertGreater(entries[1]['Inicio'],entries[0]['Fin'])
    def test_506_old_short_answer_remains_separate_from_new_exposition(self):
        parts=self.parts(506);self.assertEqual(parts[1][2],'CONTEXTO_REVISADO')
        self.assertEqual(parts[7][2],'CONTEXTO_REVISADO');self.assertEqual(len(parts[7][0]),206)
    def test_legacy_past_verb_review_does_not_relax_mention_guard(self):
        self.assertIsNone(b.TURN_DETECTOR.speaker(self.raw[3126]['Texto'],self.raw[3126]['Fecha']))
        self.assertEqual(self.parts(3126)[0][2],'CONTEXTO_REVISADO')
    def test_named_reviews_keep_cargo_discrepancies_visible(self):
        warnings=load_context_warnings(self.raw)
        for p in [180,5573,6282]:
            t,a,m=self.parts(p)[0];self.assertEqual(m,'CONTEXTO_REVISADO')
            self.assertEqual(contextual_motives(dict(ID_Padre=p,Fecha=self.raw[p]['Fecha'],Actor_Final=a,Texto=t),warnings),['CARGO_EN_DISCURSO_POR_VERIFICAR'])
    def test_unresolved_joint_identity_and_bernier_not_forced(self):
        self.assertFalse({6185,2126,3989}&set(self.reviews))
        self.assertTrue(any(e["Actor"]=="Miguel Ricaurte Bermúdez" for e in speaker_intervals(self.reviews[6443])))  # separación local; variante pendiente
        self.assertIn(780,b.load_context_warnings(self.raw))  # puente inicial todavía pendiente
        self.assertIn(6530,b.load_context_warnings(self.raw))  # nombre literal no certificado
    def test_parent_38_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[38]['Texto'].encode()).hexdigest(),'86e5721e62bd17259186064afba811d40f72d6c6e20bbb99729ed36e51ee7221')
        parts=self.parts(38)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 5917, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[38]['Texto'].split()))
        if 38 in self.reviews:
            rows=[dict(ID=i,ID_Padre=38,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{38:self.reviews[38]}))
    def test_parent_39_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[39]['Texto'].encode()).hexdigest(),'1287aaa3350ee8c3ba5cab088ac2a8af0e7c32d26319de0a9d61e6d50b5b4d4a')
        parts=self.parts(39)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 1047, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[39]['Texto'].split()))
        if 39 in self.reviews:
            rows=[dict(ID=i,ID_Padre=39,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{39:self.reviews[39]}))
    def test_parent_120_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[120]['Texto'].encode()).hexdigest(),'f33d3ed14fc7b8f112ba70a0ddd5e543a4b1f595ed6f70b8712974f13b356508')
        parts=self.parts(120)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 2855, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[120]['Texto'].split()))
        if 120 in self.reviews:
            rows=[dict(ID=i,ID_Padre=120,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{120:self.reviews[120]}))
    def test_parent_121_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[121]['Texto'].encode()).hexdigest(),'1fd7df4fc59ff688edad4f37f6162a6b6f35d41ed40d4b10070de41079642ed9')
        parts=self.parts(121)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 3940, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[121]['Texto'].split()))
        if 121 in self.reviews:
            rows=[dict(ID=i,ID_Padre=121,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{121:self.reviews[121]}))
    def test_parent_180_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[180]['Texto'].encode()).hexdigest(),'78a9eccfa0e38e54f4de38791765728007a3108bbd9cfe3642fa90e71e1851a7')
        parts=self.parts(180)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sergio Lehmann Beresi', 643, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[180]['Texto'].split()))
        if 180 in self.reviews:
            rows=[dict(ID=i,ID_Padre=180,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{180:self.reviews[180]}))
    def test_parent_264_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[264]['Texto'].encode()).hexdigest(),'f231d358e8696661d84e781d491c3c203cb72dfc51b5d624e3cda06e5c7d44be')
        parts=self.parts(264)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 3765, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[264]['Texto'].split()))
        if 264 in self.reviews:
            rows=[dict(ID=i,ID_Padre=264,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{264:self.reviews[264]}))
    def test_parent_265_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[265]['Texto'].encode()).hexdigest(),'ef5431b707bc183d7206a53c4b741660d3f6322ea48bcdc4e308d169d2d3aeb2')
        parts=self.parts(265)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 3854, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[265]['Texto'].split()))
        if 265 in self.reviews:
            rows=[dict(ID=i,ID_Padre=265,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{265:self.reviews[265]}))
    def test_parent_458_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[458]['Texto'].encode()).hexdigest(),'500eca88f7b96f8f480a11bfa4da516aa463898b301b5ce6ba7f7fc2196ebe97')
        parts=self.parts(458)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Pablo García Silva', 105, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[458]['Texto'].split()))
        if 458 in self.reviews:
            rows=[dict(ID=i,ID_Padre=458,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{458:self.reviews[458]}))
    def test_parent_506_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[506]['Texto'].encode()).hexdigest(),'aa7efe74ac2d46954631ae46ff00e6e104e89ba5ee2472c0278c735030ba48b0')
        parts=self.parts(506)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 547, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 8662, 'CONTEXTO_REVISADO'), ('Vittorio Corbo Lioi', 107, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 5743, 'SUJETO_ROL_NOMBRE'), ('Vittorio Corbo Lioi', 49, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 384, 'SUJETO_ROL_NOMBRE'), ('Nicolás Eyzaguirre Guzmán', 135, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 206, 'CONTEXTO_REVISADO'), ('Jorge Desormeaux Jiménez', 272, 'SUJETO_ROL_NOMBRE'), ('Vittorio Corbo Lioi', 533, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[506]['Texto'].split()))
        if 506 in self.reviews:
            rows=[dict(ID=i,ID_Padre=506,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{506:self.reviews[506]}))
    def test_parent_555_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[555]['Texto'].encode()).hexdigest(),'0a8d7a48977fc47d640b90299c859f5d148396546a1cd19fd9e073e32ba0a9a6')
        parts=self.parts(555)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Pablo García Silva', 260, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[555]['Texto'].split()))
        if 555 in self.reviews:
            rows=[dict(ID=i,ID_Padre=555,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{555:self.reviews[555]}))
    def test_parent_569_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[569]['Texto'].encode()).hexdigest(),'67f9f8f72d31bb470f246298d30abb032419634bddfe52c15fa00d67906c737c')
        parts=self.parts(569)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 2698, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[569]['Texto'].split()))
        if 569 in self.reviews:
            rows=[dict(ID=i,ID_Padre=569,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{569:self.reviews[569]}))
    def test_parent_570_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[570]['Texto'].encode()).hexdigest(),'029764cd7732ea699bedc8c694b7c1d52d735626e186ac54ca480074abbb54f1')
        parts=self.parts(570)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 5099, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[570]['Texto'].split()))
        if 570 in self.reviews:
            rows=[dict(ID=i,ID_Padre=570,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{570:self.reviews[570]}))
    def test_parent_752_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[752]['Texto'].encode()).hexdigest(),'0b3217c705e49f20004ce5c48ecad519346158e3e81390f424e2cf878bc38ba7')
        parts=self.parts(752)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 328, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[752]['Texto'].split()))
        if 752 in self.reviews:
            rows=[dict(ID=i,ID_Padre=752,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{752:self.reviews[752]}))
    def test_parent_1923_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[1923]['Texto'].encode()).hexdigest(),'43bc8834429e7dd1c19c068121fef592958a11556fefa8518eaa78d6c5a615c0')
        parts=self.parts(1923)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 85, 'SUJETO_ROL_NOMBRE'), ('Andrés Velasco Brañes', 255, 'CONTEXTO_REVISADO'), ('Sergio Lehmann Beresi', 2100, 'SUJETO_ROL_SESION'), ('José De Gregorio Rebeco', 112, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 88, 'CONTEXTO_REVISADO'), ('José De Gregorio Rebeco', 273, 'SUJETO_NOMBRE'), ('Pablo García Silva', 811, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 6744, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[1923]['Texto'].split()))
        if 1923 in self.reviews:
            rows=[dict(ID=i,ID_Padre=1923,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{1923:self.reviews[1923]}))
    def test_parent_2058_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2058]['Texto'].encode()).hexdigest(),'2fc395fbcec3ed25b3d474918990c3ec5083ed0b65ee1cf85b020ecf6f04ae74')
        parts=self.parts(2058)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 72, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 242, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 265, 'CONTEXTO_REVISADO'), ('José De Gregorio Rebeco', 412, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2058]['Texto'].split()))
        if 2058 in self.reviews:
            rows=[dict(ID=i,ID_Padre=2058,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{2058:self.reviews[2058]}))
    def test_parent_2438_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2438]['Texto'].encode()).hexdigest(),'4bc5829d9e1dbee20cffecba5e927ffd142cb41772f3df765647597ad28737cc')
        parts=self.parts(2438)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 5026, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 1895, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2438]['Texto'].split()))
        if 2438 in self.reviews:
            rows=[dict(ID=i,ID_Padre=2438,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{2438:self.reviews[2438]}))
    def test_parent_2839_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[2839]['Texto'].encode()).hexdigest(),'21524c6553a8081fb48b0d7f5903961adb7a53afeea1bafc52768f0a3253ef93')
        parts=self.parts(2839)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 746, 'SUJETO_ROL_SESION'), ('Consejo del Banco Central de Chile', 1698, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[2839]['Texto'].split()))
        if 2839 in self.reviews:
            rows=[dict(ID=i,ID_Padre=2839,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{2839:self.reviews[2839]}))
    def test_parent_3067_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3067]['Texto'].encode()).hexdigest(),'9ee30ce4acb03f6fb8557f91776bfce7af81583b021ea71d8f8b798632164f56')
        parts=self.parts(3067)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 155, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 99, 'ACTA/META'), ('José De Gregorio Rebeco', 248, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 532, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3067]['Texto'].split()))
        if 3067 in self.reviews:
            rows=[dict(ID=i,ID_Padre=3067,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{3067:self.reviews[3067]}))
    def test_parent_3068_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3068]['Texto'].encode()).hexdigest(),'6c73969c3d79270cb846af25bc010f68c12b5f36145968089eb20f05d20bb6e6')
        parts=self.parts(3068)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Pablo García Silva', 1738, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3068]['Texto'].split()))
        if 3068 in self.reviews:
            rows=[dict(ID=i,ID_Padre=3068,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{3068:self.reviews[3068]}))
    def test_parent_3109_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3109]['Texto'].encode()).hexdigest(),'f2a1f75ab21cc2a640fe19ade11f383544c10a4074425163766187c71bcea186')
        parts=self.parts(3109)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 144, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 548, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 83, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3109]['Texto'].split()))
        if 3109 in self.reviews:
            rows=[dict(ID=i,ID_Padre=3109,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{3109:self.reviews[3109]}))
    def test_parent_3110_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3110]['Texto'].encode()).hexdigest(),'c8c153dc41b37dfaf27576222239bb82960167ab2ed79c5e24ca9d89366ab897')
        parts=self.parts(3110)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Consejo del Banco Central de Chile', 418, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3110]['Texto'].split()))
        if 3110 in self.reviews:
            rows=[dict(ID=i,ID_Padre=3110,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{3110:self.reviews[3110]}))
    def test_parent_3126_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3126]['Texto'].encode()).hexdigest(),'2f23afb48a3ad50a939397d16bb8850ebc7466746583e9e5d72c4f1d65cfc64c')
        parts=self.parts(3126)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 2608, 'CONTEXTO_REVISADO'), ('Consejo del Banco Central de Chile', 1540, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3126]['Texto'].split()))
        if 3126 in self.reviews:
            rows=[dict(ID=i,ID_Padre=3126,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{3126:self.reviews[3126]}))
    def test_parent_3193_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3193]['Texto'].encode()).hexdigest(),'fdec0c1a4a3b2394276e064fdbde6dc0f92554a7cf12da54702f9ef1febc80c8')
        parts=self.parts(3193)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 217, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 246, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 2764, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3193]['Texto'].split()))
        if 3193 in self.reviews:
            rows=[dict(ID=i,ID_Padre=3193,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{3193:self.reviews[3193]}))
    def test_parent_3205_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3205]['Texto'].encode()).hexdigest(),'340f43611a9b2875ab16d7a5146173ca83abd1262cebdb7721f7914fae834c8b')
        parts=self.parts(3205)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 3244, 'SUJETO_NOMBRE'), ('Consejo del Banco Central de Chile', 1687, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3205]['Texto'].split()))
        if 3205 in self.reviews:
            rows=[dict(ID=i,ID_Padre=3205,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{3205:self.reviews[3205]}))
    def test_parent_3328_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3328]['Texto'].encode()).hexdigest(),'a57a126f7057d8456abecec3f31fa577474ac2049e19150e8b9782503bed9226')
        parts=self.parts(3328)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 142, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 245, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 449, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3328]['Texto'].split()))
        if 3328 in self.reviews:
            rows=[dict(ID=i,ID_Padre=3328,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{3328:self.reviews[3328]}))
    def test_parent_3421_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3421]['Texto'].encode()).hexdigest(),'f6f8d7474b7739072034ce6d15db2f7fa6fbf1ee9366cdd00b671fb35a2179cc')
        parts=self.parts(3421)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Enrique Marshall Rivera', 90, 'SUJETO_ROL_NOMBRE'), ('Luis Opazo Roco', 243, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 1143, 'SUJETO_NOMBRE'), ('José De Gregorio Rebeco', 201, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 108, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 797, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3421]['Texto'].split()))
        if 3421 in self.reviews:
            rows=[dict(ID=i,ID_Padre=3421,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{3421:self.reviews[3421]}))
    def test_parent_3572_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3572]['Texto'].encode()).hexdigest(),'8883ad9cbefcc8178d33158fe9df9352aee0c5a83f7c82889bcf80f4e576f977')
        parts=self.parts(3572)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 102, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 235, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3572]['Texto'].split()))
        if 3572 in self.reviews:
            rows=[dict(ID=i,ID_Padre=3572,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{3572:self.reviews[3572]}))
    def test_parent_3881_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[3881]['Texto'].encode()).hexdigest(),'e458cff26e259c2153c6d296cc745629ff93b821d3e99b929c09bb1240dffc1c')
        parts=self.parts(3881)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 173, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 108, 'SUJETO_ROL_SESION'), ('Consejo del Banco Central de Chile', 177, 'ACTA/META'), ('José De Gregorio Rebeco', 257, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[3881]['Texto'].split()))
        if 3881 in self.reviews:
            rows=[dict(ID=i,ID_Padre=3881,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{3881:self.reviews[3881]}))
    def test_parent_5573_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[5573]['Texto'].encode()).hexdigest(),'dfe73faeb0746b803b059cf9c517c3d0c5a2419cc5a1f7216362099d08b5719a')
        parts=self.parts(5573)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Beltrán de Ramón Acevedo', 478, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[5573]['Texto'].split()))
        if 5573 in self.reviews:
            rows=[dict(ID=i,ID_Padre=5573,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{5573:self.reviews[5573]}))
    def test_parent_6282_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6282]['Texto'].encode()).hexdigest(),'954b2910e6d96eed45701365b14b5ed9a0ef49c0b036e5834cbff89e151b8be9')
        parts=self.parts(6282)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Beltrán de Ramón Acevedo', 3253, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6282]['Texto'].split()))
        if 6282 in self.reviews:
            rows=[dict(ID=i,ID_Padre=6282,Texto=t,Actor_Final=a,Fuente_Actor=m) for i,(t,a,m) in enumerate(parts)]
            self.assertFalse(validate_speaker_reviews(rows,{6282:self.reviews[6282]}))
    def test_reviewed_administrative_participle_is_not_press_release(self):
        from institutional_reviews import institutional_type
        e=self.institutions[3110]
        self.assertIn('comunicado oportunamente',e['Texto_Padre'])
        self.assertEqual(institutional_type(e['Texto_Padre'],e),'ACTA_INSTITUCIONAL')
        with self.assertRaises(ValueError):institutional_type('Comunicado inventado',e)
