"""Lote4: distingue evidencia de separación, reservas y límites NO aplicados."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import revisar_continuidad_barreras as review
from diagnosticar_finales import read_rows
from auditar_continuidad_turnos import inventory


class BarrierReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=read_rows(review.BASE)
        cls.raw={r['ID']:r for r in read_rows(ROOT/'data/raw/consolidado_final.xlsx')}
        cls.pkg=json.loads(review.READINGS.read_text())

    def validate(self, package=None, rows=None):
        return review.validate(self.rows if rows is None else rows,self.pkg if package is None else package,self.raw)

    def test_baseline_is_v3_unchanged(self):
        self.assertEqual(hashlib.sha256(review.BASE.read_bytes()).hexdigest(),review.BASE_SHA)
        self.assertEqual(len(self.rows),9691)
        self.assertEqual(len({r['ID_Turno'] for r in self.rows}),9242)

    def test_exact_selection_all_15_barriers_and_first_4_types(self):
        sel=review.select(self.rows)
        self.assertEqual(len(sel),19)
        self.assertEqual(sum('BARRERA_LEXICA_IZQUIERDA' in e['Indicadores'] for e in sel),15)
        self.assertEqual({e['Derecha'] for e in sel[-4:]},{'RPM-2011-09-15:4333:1','RPM-2012-04-17:4788:1','RPM-2012-05-17:4849:1','RPM-2012-06-14:4899:1'})

    def test_all_29_parents_and_59698_characters(self):
        self.validate()
        self.assertEqual(len(self.pkg['Padres']),29)
        self.assertEqual(sum(len(e['Texto_Padre']) for e in self.pkg['Padres'].values()),59698)
        for p,e in self.pkg['Padres'].items():
            self.assertEqual(e['Texto_Padre'],self.raw[int(p)]['Texto'])
            for side in ('Vecino_Anterior','Vecino_Siguiente'):
                self.assertEqual(e[side]['Lectura'],'VENTANA_HASTA_250_CARACTERES')
                self.assertLessEqual(len(e[side]['Texto']),250)

    def test_three_left_groups_require_preceding_parent(self):
        for left,previous in [('RPM-2008-12-11:2203:1','RPM-2008-12-11:2202:2'),
                              ('RPM-2010-05-13:3109:1','RPM-2010-05-13:3108:3'),
                              ('RPM-2010-11-16:3572:1','RPM-2010-11-16:3571:2')]:
            group=self.pkg['Casos'][left]['Grupos_Leidos']['Izquierda']
            self.assertEqual([r['ID_Intervencion'] for r in group],[previous,left])

    def test_ten_separations_nine_reserves_no_application(self):
        _,decisions,proposals,summary=review.exports(self.rows,self.pkg)
        self.assertEqual(summary['Separaciones_Respaldadas'],10)
        self.assertEqual(summary['Reservas'],9)
        self.assertEqual(len(proposals),3)
        self.assertTrue(all(e['Aplicado']=='NO' for e in decisions))
        self.assertEqual((summary['Enlaces_Aplicados'],summary['Cortes_Aplicados'],summary['Alertas_Cerradas']),(0,0,0))

    def test_nine_temporal_pauses_not_same_person_rule(self):
        pauses=[(k,e) for k,e in self.pkg['Casos'].items() if e['Decision']=='SEPARAR_POR_PAUSA']
        self.assertEqual(len(pauses),9)
        idx={r['ID_Intervencion']:r for r in self.rows}
        for a,e in pauses:
            b=e['Derecha']
            self.assertEqual(idx[a]['Actor_Final'],idx[b]['Actor_Final'])
            self.assertNotEqual(idx[a]['ID_Turno'],idx[b]['ID_Turno'])
            self.assertIn('horas',idx[b]['Texto'])

    def test_mixed_prefix_is_not_pure_institutional_text(self):
        idx={r['ID_Intervencion']:r for r in self.rows}
        expected={4788:(1947,185),4849:(154,178),4899:(220,178)}
        for e in self.pkg['Casos'].values():
            if e['Decision']!='RESERVA_TRAMO_MIXTO':continue
            bound=e['Limite_Funcional_No_Aplicado'];row=idx[bound['ID_Intervencion']]
            self.assertEqual(row['Tipo_Acta'],'ACUERDO_CONSEJO')
            self.assertEqual((len(bound['Prefijo_Personal']),len(bound['Constancia_Y_Residuo'])),expected[row['ID_Padre']])
            self.assertIn('su voto es por mantener',bound['Prefijo_Personal'])
            self.assertTrue(bound['Constancia_Y_Residuo'].startswith(review.MARKER))
            self.assertEqual(bound['Prefijo_Personal']+bound['Constancia_Y_Residuo'],row['Texto'])
            self.assertEqual(bound['Alcance'],'PROPUESTA_FUNCIONAL_NO_APLICADA_NO_CAMBIO_DE_HABLANTE')

    def test_4333_unanimity_not_personal_vote(self):
        e=self.pkg['Casos']['RPM-2011-09-15:4332:1']
        self.assertEqual(e['Decision'],'SEPARAR_VOTO_Y_CONSTANCIA')
        right=e['Grupos_Leidos']['Derecha'][0]['Texto']
        self.assertIn('por unanimidad',right)
        self.assertNotIn('su voto',right)

    def test_consecutive_cesions_remain_reserves_not_proven_other_voice(self):
        for p in (1603,1630,1840,2203):
            e=next(e for k,e in self.pkg['Casos'].items() if int(k.split(':')[1])==p)
            self.assertTrue(e['Decision'].startswith('RESERVA_'))

    def test_4788_arrival_excuse_and_return_preserved(self):
        r=[r for r in self.rows if r['ID_Padre']==4788]
        self.assertEqual([len(x['Texto']) for x in r],[2132,112,161,333])
        self.assertEqual(r[1]['Actor_Final'],'Consejo del Banco Central de Chile')
        self.assertEqual(len({x['ID_Turno'] for x in r}),4)
        self.assertIn('FINAL_SIN_PUNTUACION',r[0]['Motivos_Revision'])

    def test_long_recipient_presentations_not_merged_into_president(self):
        for p,n in [(1604,6220),(1631,3865),(3193,2764),(3270,7111)]:
            r=[r for r in self.rows if r['ID_Padre']==p]
            self.assertEqual(len(r[-1]['Texto']),n)
            self.assertNotEqual(r[0]['Actor_Final'],r[-1]['Actor_Final'])
            self.assertNotEqual(r[0]['ID_Turno'],r[-1]['ID_Turno'])

    def test_3571_link_only_reaches_suspension(self):
        r=[r for r in self.rows if r['ID_Padre'] in (3571,3572)]
        self.assertEqual([len(x['Texto']) for x in r],[736,390,102,235])
        self.assertEqual(r[1]['ID_Turno'],r[2]['ID_Turno'])
        self.assertNotEqual(r[2]['ID_Turno'],r[3]['ID_Turno'])
        self.assertIsNone(r[1]['ID_Ancla_Actor'])

    def test_77_inventory_pairs_not_58_remaining_errors(self):
        inv,_,_,summary=review.exports(self.rows,self.pkg)
        self.assertEqual(len(inv),77)
        self.assertEqual(sum(e['Estado_Lote4']=='FUERA_DE_ESTE_LOTE' for e in inv),58)
        self.assertEqual(sum(e['Reserva_Lote3'].startswith('RESERVA_') for e in inv),5)
        self.assertEqual(summary['Pares_Inventariados'],77)

    def test_export_does_not_mutate_rows_or_evidence(self):
        original=copy.deepcopy((self.rows,self.pkg))
        review.exports(self.rows,self.pkg)
        self.assertEqual((self.rows,self.pkg),original)

    def test_invalid_scope_and_version_fail(self):
        for f,v in [('Version',True),('Version',2),('Alcance','APLICAR')]:
            p=copy.deepcopy(self.pkg);p[f]=v
            with self.subTest(field=f),self.assertRaises(ValueError):self.validate(p)

    def test_missing_case_parent_or_member_fails(self):
        for field in ['Casos','Padres']:
            p=copy.deepcopy(self.pkg);p[field].pop(next(iter(p[field])))
            with self.assertRaises(ValueError):self.validate(p)
        p=copy.deepcopy(self.pkg);e=p['Casos']['RPM-2010-11-16:3572:1'];e['Grupos_Leidos']['Izquierda']=e['Grupos_Leidos']['Izquierda'][1:]
        with self.assertRaises(ValueError):self.validate(p)

    def test_parent_text_partition_and_window_mutations_fail(self):
        for f,v in [('Texto_Padre','otro'),('SHA256_Particion','otro'),('Vecino_Anterior',{}),('Lectura','VENTANA')]:
            p=copy.deepcopy(self.pkg);p['Padres']['4788'][f]=v
            with self.subTest(field=f),self.assertRaises(ValueError):self.validate(p)

    def test_case_decision_or_empty_reason_fails(self):
        for f,v in [('Decision','APLICAR_ENLACE'),('Justificacion',''),('Reservas',[])]:
            p=copy.deepcopy(self.pkg);p['Casos']['RPM-2007-12-13:1603:1'][f]=v
            with self.subTest(field=f),self.assertRaises(ValueError):self.validate(p)

    def test_mixed_boundary_cannot_move_or_drop_whitespace(self):
        for f,v in [('Posicion_En_Fila',1),('Prefijo_Personal','otro'),('Constancia_Y_Residuo','otro'),('Alcance','APLICADO')]:
            p=copy.deepcopy(self.pkg);p['Casos']['RPM-2012-04-17:4787:2']['Limite_Funcional_No_Aplicado'][f]=v
            with self.subTest(field=f),self.assertRaises(ValueError):self.validate(p)

    def test_cannot_insert_proposal_in_other_case(self):
        p=copy.deepcopy(self.pkg);p['Casos']['RPM-2007-12-13:1603:1']['Limite_Funcional_No_Aplicado']={}
        with self.assertRaises(ValueError):self.validate(p)

    def test_changed_global_groups_and_anchors_fail(self):
        r=copy.deepcopy(self.rows);r[0]['ID_Turno']='otro'
        with self.assertRaises(ValueError):self.validate(rows=r)
        r=copy.deepcopy(self.rows);next(x for x in r if x['ID_Padre']==3571)['ID_Ancla_Actor']='otro'
        with self.assertRaises(ValueError):self.validate(rows=r)

    def test_source_and_previous_evidence_hash_fail(self):
        for field in ['SHA256_Grupos','SHA256_Lecturas_Lote3']:
            p=copy.deepcopy(self.pkg);p[field]='otro'
            with self.assertRaises(ValueError):self.validate(p)
        p=copy.deepcopy(self.pkg);p['SHA256_Fuentes'][str(review.BASE.relative_to(ROOT))]='otro'
        with self.assertRaises(ValueError):self.validate(p)

    def test_cli_deterministic_and_refuses_existing_output(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'.cache') as temp:
            paths=[Path(temp)/'a',Path(temp)/'b']
            for p in paths:
                subprocess.run([sys.executable,str(ROOT/'scripts/revisar_continuidad_barreras.py'),'--salida',str(p)],check=True,capture_output=True)
            for name in ['inventario.csv','decisiones.csv','limites_no_aplicados.csv','resumen.json']:
                self.assertEqual((paths[0]/name).read_bytes(),(paths[1]/name).read_bytes())
            r=subprocess.run([sys.executable,str(ROOT/'scripts/revisar_continuidad_barreras.py'),'--salida',str(paths[0])],capture_output=True)
            self.assertNotEqual(r.returncode,0)

    def test_cli_refuses_protected_data_output(self):
        r=subprocess.run([sys.executable,str(ROOT/'scripts/revisar_continuidad_barreras.py'),'--salida',str(ROOT/'data/releases/no-escribir-lote4')],capture_output=True)
        self.assertNotEqual(r.returncode,0)
        self.assertFalse((ROOT/'data/releases/no-escribir-lote4').exists())


if __name__=='__main__':
    unittest.main()
