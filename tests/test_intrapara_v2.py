"""Lote2: cuatro continuidades, cinco padres completos y reserva5252 explícita."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import build_base_referencia as b
from continuity import annotate_turns
from reviewed_continuity import load_reviewed_links, validate_reviewed_links
from reviewed_intrapara_continuity import load_intrapara_links as load_v1, validate_intrapara_links, ALLOWED as V1
from reviewed_intrapara_v2 import PATH, BASE, READINGS, NEW_PAIRS, load_v2, validate_readings
from intrapara_profiles import profile_name, load_intrapara_links
from compare_intrapara_release import compare, groups
from compare_intrapara_v2 import BASELINE_SHA
from diagnosticar_finales import read_rows
from auditar_continuidad_turnos import inventory
from qa_preparacion import validate_continuity


def exported(rows):
    for r in rows:
        for f in ('ID_Ancla_Actor','ID_Antecedente_Continuidad'):
            if r[f] == '':
                r[f] = None
    return rows


class IntraparaV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {int(r[0]): {'Fecha':b.to_date_str(r[1]),'Texto':str(r[5])} for r in b.data}
        cls.before = read_rows(BASE)
        cls.pkg = json.loads(PATH.read_text())
        cls.readings = json.loads(READINGS.read_text())
        cls.intra = load_v2(cls.raw)
        cls.inter = load_reviewed_links(cls.raw)
        cls.after = exported(annotate_turns(copy.deepcopy(cls.before),cls.inter,cls.intra))

    def load(self, package, loader=load_v2):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)/'registry.json'
            p.write_text(json.dumps(package))
            return loader(self.raw,p)

    def compare(self, rows):
        return compare(self.before,rows,pairs=NEW_PAIRS,profile='intrapadre-v2',baseline='intrapadre-v1')

    def test_baseline_exact_v1_not_loop32(self):
        self.assertEqual(hashlib.sha256(BASE.read_bytes()).hexdigest(),BASELINE_SHA)
        self.assertEqual(len(groups(self.before)),9255)

    def test_inventory_counts_are_not_approvals(self):
        a,c = inventory(self.before), inventory(self.after)
        self.assertEqual((len(a),len(c)),(90,86))
        self.assertEqual(sum(x['Mismo_Padre'] for x in a),41)
        self.assertEqual(sum(x['Mismo_Padre'] for x in c),37)

    def test_five_full_parents_and_ten_complete_singleton_groups(self):
        validate_readings(self.before,self.readings)
        self.assertEqual(set(self.readings['Padres']),{'663','1871','2692','5252','6813'})
        self.assertEqual(sum(len(e['Texto_Padre']) for e in self.readings['Padres'].values()),8314)
        for e in self.readings['Padres'].values():
            self.assertEqual(e['Lectura'],'PADRE_Y_GRUPOS_COMPLETOS')
            self.assertTrue(all(len(g)==1 for g in e['Grupos_Leidos'].values()))
            for side in ('Vecino_Anterior','Vecino_Siguiente'):
                self.assertLessEqual(len(e[side]['Texto']),250)
                self.assertEqual(e[side]['Lectura'],'VENTANA_HASTA_250_CARACTERES')

    def test_six_exact_proofs_with_v1_records_unchanged(self):
        self.assertEqual(set(self.intra),set(V1)|set(NEW_PAIRS))
        prior=load_v1(self.raw)
        self.assertTrue(all(self.intra[k]==v for k,v in prior.items()))
        self.assertEqual(len(self.inter),24)

    def test_v1_loader_rejects_v2(self):
        with self.assertRaises(ValueError):
            self.load(self.pkg,load_v1)

    def test_v2_loader_rejects_v1(self):
        with self.assertRaises(ValueError):
            load_v2(self.raw,ROOT/'data/curation/continuidades_intrapadre_v1.json')

    def test_profile_dispatch_is_explicit(self):
        self.assertEqual(profile_name(PATH),'intrapadre-v2')
        p=ROOT/'data/curation/continuidades_intrapadre_v1.json'
        self.assertEqual(profile_name(p),'intrapadre-v1')
        self.assertEqual(load_intrapara_links(self.raw,p),load_v1(self.raw))

    def test_invalid_profile_rejected(self):
        for field,value in [('Version',True),('Version',3),('Alcance','CONTINUIDAD_INTRAPADRE_V1')]:
            p=copy.deepcopy(self.pkg);p[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                self.load(p,load_intrapara_links)

    def test_v1_annotations_still_reproduce_v1(self):
        self.assertEqual(exported(annotate_turns(copy.deepcopy(self.before),self.inter,load_v1(self.raw))),self.before)

    def test_full_partition_and_all_other_cells_preserved(self):
        r=self.compare(self.after)
        self.assertEqual((r['Grupos_Antes'],r['Grupos_Despues']),(9255,9251))
        self.assertEqual(len(r['Celdas_Relacionales_Modificadas']),8)
        self.assertEqual(len(r['Celdas_ID_Turno_Modificadas']),215)
        self.assertEqual(len(r['Filas_Con_Conjunto_De_Companeros_Distinto']),8)
        self.assertEqual((r['Otros_Campos_Modificados'],r['Grupos_Previos_Divididos']),(0,0))
        self.assertEqual((r['Alertas_Antes'],r['Alertas_Despues']),(465,465))

    def test_all_old_24_and_new_6_proofs_and_f1_pass(self):
        self.assertEqual(validate_reviewed_links(self.after,self.inter),[])
        self.assertEqual(validate_intrapara_links(self.after,self.intra),[])
        self.assertEqual(validate_continuity(self.after),[])

    def test_context_never_becomes_global_anchor(self):
        idx={r['ID_Intervencion']:r for r in self.after}
        for a,c in NEW_PAIRS:
            self.assertIsNone(idx[a]['ID_Ancla_Actor'])
            self.assertEqual(idx[c]['ID_Ancla_Actor'],c)
            self.assertEqual(idx[c]['ID_Antecedente_Continuidad'],a)

    def test_magendzo_not_joined_across_marfan(self):
        r=[r for r in self.after if r['ID_Padre']==663]
        self.assertEqual([len(x['Texto']) for x in r],[332,347,370,316,661,304,660])
        self.assertEqual(r[1]['ID_Turno'],r[2]['ID_Turno'])
        self.assertEqual(len({x['ID_Turno'] for x in r}),6)
        self.assertNotEqual(r[2]['ID_Turno'],r[4]['ID_Turno'])
        self.assertIn('Sebastián Edwards',r[-1]['Texto'])

    def test_lehmann_preserves_presidential_question_and_return(self):
        r=[r for r in self.after if r['ID_Padre']==1871]
        self.assertEqual([len(x['Texto']) for x in r],[123,148,401,192])
        self.assertEqual(len({x['ID_Turno'] for x in r}),3)
        self.assertNotEqual(r[0]['ID_Turno'],r[-1]['ID_Turno'])
        self.assertEqual(r[0]['Motivos_Revision'],'FINAL_SIN_PUNTUACION')

    def test_lehmann_2692_question_excluded(self):
        r=[r for r in self.after if r['ID_Padre']==2692]
        self.assertEqual([len(x['Texto']) for x in r],[98,385,416])
        self.assertNotEqual(r[0]['ID_Turno'],r[1]['ID_Turno'])
        self.assertEqual(r[1]['ID_Turno'],r[2]['ID_Turno'])

    def test_gianelli_no_draghi_turn_or_merge_through_vergara(self):
        r=[r for r in self.after if r['ID_Padre']==6813]
        self.assertEqual([len(x['Texto']) for x in r],[115,141,793,240])
        self.assertEqual(len({x['ID_Turno'] for x in r}),3)
        self.assertIn('Mario Draghi',r[2]['Texto'])
        following=next(x for x in self.after if x['ID_Padre']==6814)
        self.assertNotEqual(r[2]['ID_Turno'],following['ID_Turno'])

    def test_5252_remains_reserved_with_four_groups(self):
        r=[r for r in self.after if r['ID_Padre']==5252]
        self.assertEqual([len(x['Texto']) for x in r],[1712,158,162,223])
        self.assertEqual(len({x['ID_Turno'] for x in r}),4)
        self.assertEqual(self.readings['Padres']['5252']['Decision'],'RESERVA_FUNCIONES_DISTINTAS')
        self.assertIn('se incorporará posteriormente',r[2]['Texto'])

    def test_other_voices_and_groups_globally_preserved(self):
        a={rid:g for g in groups(self.before) for rid in g}
        c={rid:g for g in groups(self.after) for rid in g}
        changed={rid for pair in NEW_PAIRS for rid in pair}
        self.assertEqual({rid for rid in a if a[rid]!=c[rid]},changed)
        self.assertEqual(max(len(g) for g in groups(self.after)),11)

    def test_missing_extra_duplicate_pair_rejected(self):
        for entries in (self.pkg['Revisiones'][:-1],self.pkg['Revisiones']*2):
            p=copy.deepcopy(self.pkg);p['Revisiones']=entries
            with self.assertRaises(ValueError):self.load(p)

    def test_cannot_rewrite_v1_proof(self):
        p=copy.deepcopy(self.pkg);p['Revisiones'][0]['Justificacion']='otra lectura'
        with self.assertRaises(ValueError):self.load(p)

    def test_cannot_approve_5252_by_registry_edit(self):
        p=copy.deepcopy(self.pkg);p['Revisiones'][-1]['Siguiente']['ID_Intervencion']='RPM-2012-12-13:5252:4'
        with self.assertRaises(ValueError):self.load(p)

    def test_registry_literal_interval_or_actor_changes_rejected(self):
        for side in ('Anterior','Siguiente'):
            for field,value in [('Inicio',-1),('Texto','otro'),('Fuente_Actor','CONTINUIDAD_PARRAFO')]:
                p=copy.deepcopy(self.pkg);p['Revisiones'][-1][side][field]=value
                with self.subTest(side=side,field=field),self.assertRaises(ValueError):self.load(p)
        p=copy.deepcopy(self.pkg);p['Revisiones'][-1]['Actor']='Otra persona'
        with self.assertRaises(ValueError):self.load(p)

    def test_reading_hash_required(self):
        for field in ('Lecturas_Lote2','SHA256_Lecturas_Lote2'):
            p=copy.deepcopy(self.pkg);p[field]='otro'
            with self.assertRaises(ValueError):self.load(p)

    def test_reading_incomplete_modified_parent_or_group_rejected(self):
        for field,value in [('Texto_Padre','otro'),('SHA256_Particion','0'*64),('Grupos_Leidos',{}),
                            ('Vecino_Anterior',{}),('Decision','APLICAR_TODO'),('Reservas',[])]:
            p=copy.deepcopy(self.readings);p['Padres']['663'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):validate_readings(self.before,p)

    def test_reserve_cannot_be_promoted_in_reading(self):
        p=copy.deepcopy(self.readings);p['Padres']['5252']['Decision']='ENLACE_RESPALDADO_POR_LECTURA'
        with self.assertRaises(ValueError):validate_readings(self.before,p)

    def test_missing_parent_and_changed_global_groups_rejected(self):
        p=copy.deepcopy(self.readings);del p['Padres']['5252']
        with self.assertRaises(ValueError):validate_readings(self.before,p)
        p=copy.deepcopy(self.readings);p['SHA256_Grupos']='otro'
        with self.assertRaises(ValueError):validate_readings(self.before,p)

    def test_global_gate_rejects_warning_text_and_anchor_changes(self):
        for field in ('Texto','Motivos_Revision','Actor_Final','ID_Ancla_Actor'):
            r=copy.deepcopy(self.after);r[0][field]='otro'
            with self.subTest(field=field),self.assertRaises(ValueError):self.compare(r)

    def test_global_gate_rejects_extra_union_and_lost_old_link(self):
        for p in (5252,2797):
            r=copy.deepcopy(self.after);i=next(i for i,x in enumerate(r) if x['ID_Padre']==p)
            if p==5252:r[i+3]['ID_Turno']=r[i+2]['ID_Turno']
            else:r[i]['ID_Turno']='nuevo'
            with self.subTest(parent=p),self.assertRaises(ValueError):self.compare(r)

    def test_declared_but_unapplied_and_unknown_proofs_fail(self):
        self.assertTrue(validate_intrapara_links(self.before,self.intra))
        self.assertTrue(validate_intrapara_links(self.after,load_v1(self.raw)))


if __name__ == '__main__':
    unittest.main()
