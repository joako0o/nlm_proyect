"""Lote3: cierra la lectura del subgrupo, no la revisión semántica del corpus."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_base_referencia as b
from continuity import annotate_turns
from reviewed_continuity import load_reviewed_links,validate_reviewed_links
from reviewed_intrapara_continuity import validate_intrapara_links
from reviewed_intrapara_v2 import load_v2
from reviewed_intrapara_v3 import (load_v3,validate_readings,selection,BASE,PATH,READINGS,
                                  NEW_PAIRS,CASES,PARENTS)
from compare_intrapara_v3 import BASELINE_SHA
from compare_intrapara_release import compare,groups
from auditar_continuidad_turnos import inventory
from diagnosticar_finales import read_rows
from intrapara_profiles import profile_name,load_intrapara_links
from qa_preparacion import validate_continuity


def exported(rows):
    for r in rows:
        for f in ('ID_Ancla_Actor','ID_Antecedente_Continuidad'):
            if r[f]=='':r[f]=None
    return rows


class IntraparaV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={int(r[0]):{'Fecha':b.to_date_str(r[1]),'Texto':str(r[5])} for r in b.data}
        cls.before=read_rows(BASE)
        cls.pkg=json.loads(PATH.read_text())
        cls.readings=json.loads(READINGS.read_text())
        cls.intra=load_v3(cls.raw)
        cls.prior=load_v2(cls.raw)
        cls.inter=load_reviewed_links(cls.raw)
        cls.after=exported(annotate_turns(copy.deepcopy(cls.before),cls.inter,cls.intra))

    def load(self,pkg,loader=load_v3):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'proof.json';p.write_text(json.dumps(pkg))
            return loader(self.raw,p)

    def compare(self,rows):
        return compare(self.before,rows,pairs=NEW_PAIRS,profile='intrapadre-v3',baseline='intrapadre-v2')

    def test_exact_v2_baseline(self):
        self.assertEqual(hashlib.sha256(BASE.read_bytes()).hexdigest(),BASELINE_SHA)
        self.assertEqual(len(groups(self.before)),9251)

    def test_complete_selection_not_all_corpus(self):
        self.assertEqual(len(selection(self.before)),14)
        self.assertEqual({x['Izquierda'] for x in selection(self.before)},set(CASES))
        self.assertEqual(len(selection(self.after)),5)
        self.assertEqual((len(inventory(self.before)),len(inventory(self.after))),(86,77))
        self.assertEqual(sum(x['Mismo_Padre'] for x in inventory(self.after)),28)

    def test_eighteen_full_parents_and_70514_characters(self):
        validate_readings(self.before,self.readings)
        self.assertEqual(len(PARENTS),18)
        self.assertEqual(sum(len(e['Texto_Padre']) for e in self.readings['Padres'].values()),70514)
        for p,e in self.readings['Padres'].items():
            self.assertEqual(e['Texto_Padre'],self.raw[int(p)]['Texto'])
            for side in ('Vecino_Anterior','Vecino_Siguiente'):
                self.assertLessEqual(len(e[side]['Texto']),250)
                self.assertEqual(e[side]['Lectura'],'VENTANA_HASTA_250_CARACTERES')

    def test_all_members_read_including_reserved_2864(self):
        expected={2695:[2695,2696],2754:[2754,2755],2790:[2790,2791],2863:[2863,2864]}
        for p,parents in expected.items():
            case=next(e for e in self.readings['Casos'].values() if e['ID_Padre']==p)
            members=case['Grupos_Leidos']['Derecha']
            self.assertEqual([int(r['ID_Intervencion'].split(':')[1]) for r in members],parents)

    def test_nine_new_fifteen_cumulative_and_24_interparent(self):
        self.assertEqual((len(NEW_PAIRS),len(self.intra),len(self.inter)),(9,15,24))
        self.assertEqual(set(self.intra),set(self.prior)|set(NEW_PAIRS))
        self.assertTrue(all(self.intra[k]==v for k,v in self.prior.items()))

    def test_global_changes_are_only_nine_exact_unions(self):
        r=self.compare(self.after)
        self.assertEqual((r['Grupos_Despues'],len(r['Celdas_Relacionales_Modificadas'])),(9242,18))
        self.assertEqual(len(r['Celdas_ID_Turno_Modificadas']),358)
        self.assertEqual(len(r['Filas_Con_Conjunto_De_Companeros_Distinto']),21)
        self.assertEqual(r['Otros_Campos_Modificados'],0)
        self.assertEqual(r['Grupos_Previos_Divididos'],0)
        self.assertEqual((r['Alertas_Antes'],r['Alertas_Despues']),(465,465))

    def test_all_proofs_and_f1_pass(self):
        self.assertEqual(validate_reviewed_links(self.after,self.inter),[])
        self.assertEqual(validate_intrapara_links(self.after,self.intra),[])
        self.assertEqual(validate_continuity(self.after),[])

    def test_v2_engine_still_reproduces_its_baseline(self):
        self.assertEqual(exported(annotate_turns(copy.deepcopy(self.before),self.inter,self.prior)),self.before)

    def test_context_anchor_stays_null_and_right_own_anchor(self):
        idx={r['ID_Intervencion']:r for r in self.after}
        for a,c in NEW_PAIRS:
            self.assertIsNone(idx[a]['ID_Ancla_Actor'])
            self.assertEqual(idx[c]['ID_Ancla_Actor'],c)
            self.assertEqual(idx[c]['ID_Antecedente_Continuidad'],a)

    def test_full_long_presentations_preserved(self):
        for p,length in [(1092,3097),(2695,2104),(2754,7764),(2778,2613),(2790,6592),
                         (2810,1206),(2909,3069),(3439,2345),(6800,3715)]:
            pair=next(k for k,v in NEW_PAIRS.items() if v[0]==p)
            turn=next(r['ID_Turno'] for r in self.after if r['ID_Intervencion']==pair[0])
            self.assertEqual(sum(len(r['Texto']) for r in self.after if r['ID_Turno']==turn),length,p)

    def test_reserves_are_five_and_not_proven_discontinuities(self):
        reserved={e['ID_Padre'] for e in self.readings['Casos'].values() if e['Decision'].startswith('RESERVA')}
        self.assertEqual(reserved,{780,2661,2863,3646,5252})
        old={rid:g for g in groups(self.before) for rid in g};new={rid:g for g in groups(self.after) for rid in g}
        for r in self.before:
            if r['ID_Padre'] in reserved|{2864}:
                self.assertEqual(old[r['ID_Intervencion']],new[r['ID_Intervencion']])

    def test_780_bridge_not_moved(self):
        r=[r for r in self.after if r['ID_Padre']==780]
        self.assertEqual([len(x['Texto']) for x in r],[5463,1655,1763,2546])
        self.assertEqual(len({x['ID_Turno'] for x in r}),4)
        self.assertIn('En la economía nacional',r[0]['Texto'])

    def test_bare_confirmations_not_invented_as_quotes(self):
        for p,n in [(2661,49),(3646,84)]:
            r=next(r for r in self.after if r['ID_Padre']==p and len(r['Texto'])==n)
            self.assertIn('confirmad',r['Texto'])
            self.assertIsNone(r['ID_Ancla_Actor'])

    def test_damaged_2863_keeps_existing_2864_link(self):
        r=next(r for r in self.after if r['ID_Padre']==2863 and len(r['Texto'])==939)
        following=next(r for r in self.after if r['ID_Padre']==2864)
        self.assertIn('ha caído algo r últimamente',r['Texto'])
        self.assertTrue(r['Texto'].endswith('A continuación,.'))
        self.assertEqual(r['ID_Turno'],following['ID_Turno'])

    def test_other_speakers_stay_separate_in_complex_parents(self):
        for p,n in [(2661,12),(2696,6),(2778,2),(2810,4),(2909,3),(5252,4)]:
            r=[r for r in self.after if r['ID_Padre']==p]
            self.assertEqual(len({x['ID_Turno'] for x in r}),n,p)
        self.assertEqual(max(len(g) for g in groups(self.after)),11)

    def test_company_and_literal_repetitions_not_removed(self):
        r=[r for r in self.after if r['ID_Padre']==2810]
        self.assertIn('Lehman Brothers',r[-1]['Texto'])
        self.assertNotEqual(r[1]['ID_Turno'],r[-1]['ID_Turno'])
        vial=[r for r in self.after if r['ID_Padre']==6800]
        self.assertIn('su voto es por mantener',vial[1]['Texto'])
        self.assertIn('su voto es por mantener',vial[2]['Texto'])

    def test_closed_dispatch_and_old_loaders(self):
        self.assertEqual(profile_name(PATH),'intrapadre-v3')
        with self.assertRaises(ValueError):self.load(self.pkg,load_v2)
        with self.assertRaises(ValueError):load_v3(self.raw,ROOT/'data/curation/continuidades_intrapadre_v2.json')
        p=copy.deepcopy(self.pkg);p['Version']=4
        with self.assertRaises(ValueError):self.load(p,load_intrapara_links)

    def test_missing_duplicate_and_extra_records_rejected(self):
        for entries in [self.pkg['Revisiones'][:-1],self.pkg['Revisiones']*2]:
            p=copy.deepcopy(self.pkg);p['Revisiones']=entries
            with self.assertRaises(ValueError):self.load(p)
        p=copy.deepcopy(self.pkg);p['Revisiones'][-1]['ID_Padre']=5252
        with self.assertRaises(ValueError):self.load(p)

    def test_cannot_rewrite_old_six_records(self):
        p=copy.deepcopy(self.pkg);p['Revisiones'][4]['Justificacion']='otro'
        with self.assertRaises(ValueError):self.load(p)

    def test_changed_intervals_actor_or_source_rejected(self):
        for side in ['Anterior','Siguiente']:
            for field,value in [('Inicio',-1),('Fin',True),('Texto','otro'),('Fuente_Actor','CONTEXTO_REVISADO')]:
                if side=='Anterior' and field=='Fuente_Actor':continue
                p=copy.deepcopy(self.pkg);p['Revisiones'][-1][side][field]=value
                with self.subTest(side=side,field=field),self.assertRaises(ValueError):self.load(p)

    def test_missing_old_or_new_evidence_hash_fails(self):
        for f in ['Lecturas_Lote3','SHA256_Lecturas_Lote3','SHA256_Registro_V2','Lecturas_Lote2']:
            p=copy.deepcopy(self.pkg);p[f]='otro'
            with self.subTest(field=f),self.assertRaises(ValueError):self.load(p)

    def test_members_cannot_be_truncated_to_first_row(self):
        p=copy.deepcopy(self.readings)
        e=next(e for e in p['Casos'].values() if e['ID_Padre']==2754)
        e['Grupos_Leidos']['Derecha']=e['Grupos_Leidos']['Derecha'][:1]
        with self.assertRaises(ValueError):validate_readings(self.before,p)

    def test_missing_continuation_parent_rejected(self):
        p=copy.deepcopy(self.readings);del p['Padres']['2755']
        with self.assertRaises(ValueError):validate_readings(self.before,p)

    def test_reading_mutations_fail(self):
        for f,value in [('Texto_Padre','otro'),('SHA256_Particion','otro'),('Vecino_Siguiente',{}),('Lectura','VENTANA')]:
            p=copy.deepcopy(self.readings);p['Padres']['1092'][f]=value
            with self.subTest(field=f),self.assertRaises(ValueError):validate_readings(self.before,p)

    def test_reserve_cannot_be_promoted(self):
        p=copy.deepcopy(self.readings)
        e=next(e for e in p['Casos'].values() if e['ID_Padre']==780)
        e['Decision']='ENLACE_RESPALDADO_POR_LECTURA'
        with self.assertRaises(ValueError):validate_readings(self.before,p)

    def test_global_gate_rejects_text_warning_anchor_changes(self):
        for f in ['Texto','Motivos_Revision','ID_Ancla_Actor','Actor_Final','Rol_Final']:
            r=copy.deepcopy(self.after);r[0][f]='otro'
            with self.subTest(field=f),self.assertRaises(ValueError):self.compare(r)

    def test_global_gate_rejects_split_continuation_or_extra_merge(self):
        for p in [2755,2791,2864]:
            r=copy.deepcopy(self.after);next(x for x in r if x['ID_Padre']==p)['ID_Turno']='otro'
            with self.subTest(parent=p),self.assertRaises(ValueError):self.compare(r)
        r=copy.deepcopy(self.after);parts=[x for x in r if x['ID_Padre']==780];parts[2]['ID_Turno']=parts[1]['ID_Turno']
        with self.assertRaises(ValueError):self.compare(r)

    def test_unapplied_registry_or_wrong_antecedent_fails(self):
        self.assertTrue(validate_intrapara_links(self.before,self.intra))
        r=copy.deepcopy(self.after);right=next(iter(NEW_PAIRS))[1]
        next(x for x in r if x['ID_Intervencion']==right)['ID_Antecedente_Continuidad']='otro'
        self.assertTrue(validate_intrapara_links(r,self.intra))


if __name__=='__main__':
    unittest.main()
