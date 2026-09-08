"""LOOP17: diálogos omitidos, nueva participante y conservación de pendientes."""
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

IDS=(4364,6013,6014,6015,6016,6019,6441,6442,6443,6451,6769,6770)
R='Miguel Ricaurte Bermúdez'
class LoopSeventeenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_speaker_reviews(cls.raw);cls.warnings=load_context_warnings(cls.raw)
    def parts(self,p):
        r=self.raw[p];return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.reviews.get(p))
    def rows(self,p):
        return [dict(ID=i,ID_Padre=p,ID_Intervencion=f'{p}:{i}',ID_Bloque_Texto=f'{p}:{i}',Fecha=self.raw[p]['Fecha'],Texto=t,Actor_Final=a,Fuente_Actor=m,Fuente_Rol='LISTA_ASISTENCIA',Duplicado_Exacto='NO',Duplicado_Formula='NO',Tipo_Acta='INTERVENCION') for i,(t,a,m) in enumerate(self.parts(p))]
    def test_all_bounded_intervals_validate(self):
        for p in IDS:self.assertFalse(validate_speaker_reviews(self.rows(p),{p:self.reviews[p]}))
    def test_every_new_ricaurte_turn_retains_identity_warning(self):
        n=0
        for p in IDS:
            for r in self.rows(p):
                if r['Actor_Final']==R:
                    n+=1;self.assertIn('VARIANTE_IDENTIDAD_POR_VERIFICAR',review_reasons(r,b.TURN_DETECTOR,b.split_sentences))
        self.assertEqual(n,12)
    def test_long_developments_not_split_by_subject_or_country(self):
        self.assertEqual([len(t) for t,a,m in self.parts(6015) if a==R],[562,8218])
        self.assertEqual([len(t) for t,a,m in self.parts(6443) if a==R],[7178,6399])
    def test_claro_returns_are_independent(self):
        self.assertEqual([a for t,a,m in self.parts(6016)],['Sebastián Claro Edwards',R,'Sebastián Claro Edwards',R])
    def test_beltran_and_garcia_not_absorbed_by_ricaurte(self):
        self.assertEqual([a for t,a,m in self.parts(6443)],['Beltrán de Ramón Acevedo','Pablo García Silva',R,'Beltrán de Ramón Acevedo',R])
    def test_6451_closing_and_incorporation_remain_separate(self):
        parts=self.parts(6451)
        self.assertEqual([a for t,a,m in parts],['Rodrigo Vergara Montes',R,'Rodrigo Vergara Montes',b.CONSEJO])
        self.assertIn('Siendo las 12:30',parts[-1][0]);self.assertEqual(parts[-1][2],'ACTA/META')
    def test_reviewed_speakers_never_create_global_anchors(self):
        for p in IDS:
            rows=self.rows(p);annotate_turns(rows)
            for r in rows:
                if r['Fuente_Actor']=='CONTEXTO_REVISADO':self.assertFalse(r['ID_Ancla_Actor'])
    def test_new_gloria_label_has_roster_and_discourse_not_attendance_alone(self):
        self.assertIn('Gloria Peña Tapia',b.REAL)
        for p in [6769,6770]:
            e=self.reviews[p];self.assertEqual(e['Actor'],'Gloria Peña Tapia')
            self.assertTrue(any(x['ID_Padre']==6755 and 'doña Gloria Peña Tapia' in x['Cita'] for x in e['Evidencia']))
            self.assertIn('Gloria Peña',self.parts(p)[1][0])
            self.assertEqual(b.roster_role_for(self.raw[p]['Fecha'],'Gloria Peña Tapia'),'Gerente de División Estadísticas (S)')
    def test_6930_gloria_reference_is_not_a_turn(self):
        parts=self.parts(6930)
        self.assertEqual(len(parts),1);self.assertEqual(parts[0][1],'Rodrigo Vergara Montes')
    def test_ricaurte_rosters_are_local_and_alias_ambiguity_remains(self):
        for p in IDS:
            for e in speaker_intervals(self.reviews[p]):
                if e['Actor']==R:
                    self.assertTrue(any(x['ID_Padre']==(6008 if p<6400 else 6440) and 'Miguel Ricaurte Bermúdez' in x['Cita'] for x in e['Evidencia']))
                    self.assertIn('no equivalencia global',e['Limitacion'])
    def test_three_new_contextual_warnings_are_exact(self):
        for p,motive,needle in [(6013,'TEXTO_DANADO_POR_COTEJAR','Agrega que la proyección de En lo referente'),(6015,'TEXTO_DANADO_POR_COTEJAR','quien hace que'),(4364,'NOMBRE_EN_DISCURSO_POR_VERIFICAR','Claudios Soto')]:
            hits=[r for r in self.rows(p) if contextual_motives(r,self.warnings)]
            self.assertEqual(len(hits),1);self.assertIn(needle,hits[0]['Texto'])
            self.assertEqual(contextual_motives(hits[0],self.warnings),[motive])
    def test_retired_6443_warning_is_archived_without_erasing_identity_pending(self):
        archive=json.loads((Path(b.__file__).resolve().parents[1]/'data/curation/alertas_contextuales_retiradas.json').read_text())
        entry=next(e for e in archive if e['Alerta_Original']['ID_Padre']==6443)
        old=entry['Alerta_Original'];self.assertNotIn(6443,self.warnings)
        self.assertEqual(old['Actor_Provisional'],'Beltrán de Ramón Acevedo')
        self.assertEqual(''.join(old['Texto_Intervalo'].split()),''.join(self.raw[6443]['Texto'].split()))
        self.assertEqual(old['SHA256_Texto_Padre'],hashlib.sha256(self.raw[6443]['Texto'].encode()).hexdigest())
        self.assertEqual(set(entry['Revisiones_Sustitutas']),{e['Revision_ID'] for e in speaker_intervals(self.reviews[6443])})
        self.assertEqual(sum('VARIANTE_IDENTIDAD_POR_VERIFICAR' in review_reasons(r,b.TURN_DETECTOR,b.split_sentences) for r in self.rows(6443)),2)
    def test_old_ambiguous_passages_not_forced(self):
        self.assertFalse({6185,2126,3989}&set(self.reviews))
        for p in [780,4433,6530,3191,5367]:self.assertIn(p,self.warnings)
    def test_changed_source_hash_rejects_new_review(self):
        raw=copy.deepcopy(self.raw);raw[6015]['Texto']+=' X'
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'review.json';path.write_text(json.dumps([self.reviews[6015]]))
            with self.assertRaises(ValueError):load_speaker_reviews(raw,path)
    def test_parent_4364_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[4364]['Texto'].encode()).hexdigest(),'a27840f1167520cd66d6b20edec131de6ed11abd56e5f22d27e555d348f8f21d')
        parts=self.parts(4364)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 125, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 154, 'CONTEXTO_REVISADO'), ('José De Gregorio Rebeco', 346, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[4364]['Texto'].split()))
    def test_parent_6013_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6013]['Texto'].encode()).hexdigest(),'fa15249996be5d8b511b0a80e76e088323fd133d18ec75ab1ff3c636d6d12768')
        parts=self.parts(6013)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 283, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 4473, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6013]['Texto'].split()))
    def test_parent_6014_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6014]['Texto'].encode()).hexdigest(),'be2778aafdcd48de669ecaff9b53daa3aa4822a27ab0e4caa3d6363e23fc24c1')
        parts=self.parts(6014)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Pablo García Silva', 409, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 172, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6014]['Texto'].split()))
    def test_parent_6015_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6015]['Texto'].encode()).hexdigest(),'acb4c4f6186d24f1319c100abdbd37ff97922665e159067a55c507f4caca0010')
        parts=self.parts(6015)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 112, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 562, 'CONTEXTO_REVISADO'), ('Rodrigo Vergara Montes', 170, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 8218, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6015]['Texto'].split()))
    def test_parent_6016_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6016]['Texto'].encode()).hexdigest(),'5d10dc9a3c82a10e0836332c7f67fbc61ff6615c305f51bd9ec303e6d440f180')
        parts=self.parts(6016)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 536, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 785, 'CONTEXTO_REVISADO'), ('Sebastián Claro Edwards', 461, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 1007, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6016]['Texto'].split()))
    def test_parent_6019_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6019]['Texto'].encode()).hexdigest(),'a2964f9152fa3445ee5200c6383aebaf6a6b0c3361703e481c3ada41f17b71d6')
        parts=self.parts(6019)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Beltrán de Ramón Acevedo', 373, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 4364, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6019]['Texto'].split()))
    def test_parent_6441_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6441]['Texto'].encode()).hexdigest(),'6c8a87dbc872f7fde6fb4f32e8a56d9cb3848429cedc3cc89d12cf9af2bf2f40')
        parts=self.parts(6441)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 455, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 5897, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6441]['Texto'].split()))
    def test_parent_6442_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6442]['Texto'].encode()).hexdigest(),'a1fbd8cb82b69f4442d1d38da4443b2405090a0f88d69eed57e35965b6f8578e')
        parts=self.parts(6442)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 276, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 550, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6442]['Texto'].split()))
    def test_parent_6443_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6443]['Texto'].encode()).hexdigest(),'c2f9531c9d1bfad7d90bd4731fed1edd0d36feed20585aeb0a4be34609fa6f1a')
        parts=self.parts(6443)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Beltrán de Ramón Acevedo', 734, 'SUJETO_ROL_NOMBRE'), ('Pablo García Silva', 305, 'CONTEXTO_REVISADO'), ('Miguel Ricaurte Bermúdez', 7178, 'CONTEXTO_REVISADO'), ('Beltrán de Ramón Acevedo', 480, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 6399, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6443]['Texto'].split()))
    def test_parent_6451_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6451]['Texto'].encode()).hexdigest(),'b7f82052b2ad646f7c8788b8e951ed46a4575311047f05462b54e8942a558a21')
        parts=self.parts(6451)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 970, 'SUJETO_ROL_NOMBRE'), ('Miguel Ricaurte Bermúdez', 329, 'CONTEXTO_REVISADO'), ('Rodrigo Vergara Montes', 239, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 111, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6451]['Texto'].split()))
    def test_parent_6769_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6769]['Texto'].encode()).hexdigest(),'307a0512401af79f74265d693225dbab072b345a263ca7f3c3ab4936ff32aed4')
        parts=self.parts(6769)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Miguel Fuentes Díaz', 1122, 'SUJETO_NOMBRE'), ('Gloria Peña Tapia', 339, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6769]['Texto'].split()))
    def test_parent_6770_exact_source_and_segments(self):
        self.assertEqual(hashlib.sha256(self.raw[6770]['Texto'].encode()).hexdigest(),'be9dd3f7999b1597f5a9aa9f83cd52455cacc11e776fd39add7b4f46f08f39a1')
        parts=self.parts(6770)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 94, 'SUJETO_ROL_NOMBRE'), ('Gloria Peña Tapia', 342, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in parts),''.join(self.raw[6770]['Texto'].split()))
