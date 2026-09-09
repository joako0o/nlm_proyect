"""Lote6: evidencia/triage sin cambios productivos ni cierres automáticos."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from revisar_reservas_complejas import (BASE,BASE_SHA,READINGS,PARENTS,CASES,validate,exports,inherited_statuses,main)
from diagnosticar_finales import read_rows


class ComplexReserveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=read_rows(BASE);cls.pkg=json.loads(READINGS.read_text())
        cls.raw={r['ID']:r for r in read_rows(ROOT/'data/raw/consolidado_final.xlsx')}

    def test_baseline_and_complete_evidence(self):
        self.assertEqual(hashlib.sha256(BASE.read_bytes()).hexdigest(),BASE_SHA)
        validate(self.rows,self.pkg,self.raw)
        self.assertEqual(len(PARENTS),6)
        self.assertEqual(sum(len(e['Texto_Padre']) for e in self.pkg['Padres'].values()),20797)
        self.assertEqual(sum(r['ID_Padre'] in PARENTS for r in self.rows),28)

    def test_all_members_including_2864(self):
        e=self.pkg['Casos']['RPM-2010-01-14:2863:2']['Grupos_Leidos']
        self.assertEqual([r['ID_Padre'] for r in e['Derecha']],[2863,2864])
        self.assertEqual(sum(len(g) for e in self.pkg['Casos'].values() for g in e['Grupos_Leidos'].values()),11)

    def test_triage_counts_and_no_unread_claim(self):
        inv,dec,block,s=exports(self.rows,self.pkg)
        self.assertEqual((len(inv),len(dec),len(block)),(71,5,3))
        self.assertEqual(s['Estados']['SIN_ADJUDICACION_EN_ESTE_INVENTARIO'],53)
        self.assertEqual(s['Estados']['SEPARACION_RESPALDADA_PREVIAMENTE'],10)
        self.assertEqual(s['Estados']['SEPARACION_FUNCIONAL_V4'],3)
        self.assertEqual(s['Estados']['PROPUESTA_LOCAL_NO_APLICADA'],2)
        self.assertTrue(all('NUNCA_LEIDO' in r['Alcance_Lectura'] for r in inv if not r['Evidencia']))
        self.assertEqual((s['Filas'],s['Grupos'],s['Filas_Alertadas']),(9694,9236,467))

    def test_no_row_or_package_mutation(self):
        rows=copy.deepcopy(self.rows);pkg=copy.deepcopy(self.pkg);exports(rows,pkg)
        self.assertEqual(rows,self.rows);self.assertEqual(pkg,self.pkg)

    def test_proposals_not_applied_or_counted_as_closures(self):
        _,dec,_,s=exports(self.rows,self.pkg)
        proposed=[r['Izquierda'] for r in dec if r['Estado']=='PROPUESTA_LOCAL_NO_APLICADA']
        self.assertEqual(proposed,['RPM-2010-01-14:2863:2','RPM-2011-01-13:3646:2'])
        self.assertTrue(all(r['Aplicado']=='NO' for r in dec))
        self.assertEqual([s[k] for k in ['Enlaces_Aplicados','Cortes_Aplicados','Alertas_Cerradas']],[0,0,0])

    def test_confirmations_have_distinct_positive_evidence(self):
        a=self.pkg['Casos']['RPM-2009-08-13:2661:6'];b=self.pkg['Casos']['RPM-2011-01-13:3646:2']
        self.assertNotEqual(a['Estado'],b['Estado'])
        self.assertIn('El señor Lehmann continúa',b['Grupos_Leidos']['Derecha'][0]['Texto'])
        for e in (a,b):
            self.assertEqual(e['Grupos_Leidos']['Izquierda'][0]['Fuente_Actor'],'CONTEXTO_REVISADO')
            self.assertIsNone(e['Grupos_Leidos']['Izquierda'][0]['ID_Ancla_Actor'])

    def test_780_bridge_and_5252_acta_remain_reserved(self):
        self.assertEqual(self.pkg['Casos']['RPM-2006-07-13:780:2']['Estado'],'RESERVA_COTEJO_INICIO')
        self.assertIn('En la economía nacional',self.pkg['Padres']['780']['Texto_Padre'])
        r=[r for r in self.rows if r['ID_Padre']==5252]
        self.assertEqual([len(x['Texto']) for x in r],[1712,158,162,223])
        self.assertEqual(len({x['ID_Turno'] for x in r}),4)
        self.assertIn('se incorporará posteriormente',r[2]['Texto'])

    def test_2863_literals_and_existing_continuity_kept(self):
        r=[r for r in self.rows if r['ID_Padre'] in (2863,2864)]
        self.assertIn('ha caído algo r últimamente',r[2]['Texto'])
        self.assertTrue(r[2]['Texto'].endswith('A continuación,.'))
        self.assertEqual(r[2]['ID_Turno'],r[3]['ID_Turno'])
        self.assertNotEqual(r[1]['ID_Turno'],r[2]['ID_Turno'])

    def test_inherited_separations_not_new_readings(self):
        self.assertEqual(len(inherited_statuses(self.rows)),13)
        inv,*_=exports(self.rows,self.pkg)
        inherited=[r for r in inv if r['Estado_Revision_Dirigida'].startswith('SEPARACION_')]
        self.assertTrue(all(r['Alcance_Lectura']=='RESPALDO_ANTERIOR_NO_RELECTURA_EN_LOTE6' for r in inherited))

    def test_wrong_scope_version_sources_and_missing_parent_fail(self):
        for k,v in [('Version',True),('Version',6),('Alcance','APLICAR'),('SHA256_Fuentes',{}),('SHA256_Grupos','otro')]:
            pkg=copy.deepcopy(self.pkg);pkg[k]=v
            with self.subTest(field=k),self.assertRaises(ValueError):validate(self.rows,pkg,self.raw)
        pkg=copy.deepcopy(self.pkg);del pkg['Padres']['2864']
        with self.assertRaises(ValueError):validate(self.rows,pkg,self.raw)

    def test_changed_reading_text_window_or_hash_fails(self):
        for k,v in [('Lectura','VENTANA'),('Texto_Padre','otro'),('SHA256_Particion','otro'),('Vecino_Siguiente',{})]:
            pkg=copy.deepcopy(self.pkg);pkg['Padres']['780'][k]=v
            with self.subTest(field=k),self.assertRaises(ValueError):validate(self.rows,pkg,self.raw)

    def test_missing_companion_or_modified_anchor_fails(self):
        for k,v in [('ID_Ancla_Actor','otro'),('Texto','otro'),('Fuente_Actor','SUJETO_NOMBRE')]:
            pkg=copy.deepcopy(self.pkg);pkg['Casos']['RPM-2010-01-14:2863:2']['Grupos_Leidos']['Izquierda'][0][k]=v
            with self.subTest(field=k),self.assertRaises(ValueError):validate(self.rows,pkg,self.raw)
        pkg=copy.deepcopy(self.pkg);pkg['Casos']['RPM-2010-01-14:2863:2']['Grupos_Leidos']['Derecha'].pop()
        with self.assertRaises(ValueError):validate(self.rows,pkg,self.raw)

    def test_decision_cannot_be_promoted_or_marked_applied(self):
        for k,v in [('Estado','APLICADO'),('Estado_Anterior','otro'),('Aplicado',True),('Justificacion',''),('Siguiente_Accion','')]:
            pkg=copy.deepcopy(self.pkg);pkg['Casos'][next(iter(CASES))][k]=v
            with self.subTest(field=k),self.assertRaises(ValueError):validate(self.rows,pkg,self.raw)

    def test_global_group_change_or_row_loss_fails(self):
        rows=copy.deepcopy(self.rows);rows[0]['ID_Turno']='otro'
        with self.assertRaises(ValueError):validate(rows,self.pkg,self.raw)
        with self.assertRaises(ValueError):validate(self.rows[:-1],self.pkg,self.raw)

    def test_inherited_decision_text_cannot_drift(self):
        rows=copy.deepcopy(self.rows)
        next(r for r in rows if r['ID_Intervencion']=='RPM-2010-07-15:3269:1')['Texto']='otro'
        with self.assertRaises(ValueError):validate(rows,self.pkg,self.raw)
        rows=copy.deepcopy(self.rows)
        next(r for r in rows if r['ID_Intervencion']=='RPM-2012-05-17:4849:2')['Tipo_Acta']=None
        with self.assertRaises(ValueError):validate(rows,self.pkg,self.raw)

    def test_raw_source_change_fails(self):
        raw=copy.deepcopy(self.raw);raw[3646]['Texto']+=' '
        with self.assertRaises(ValueError):validate(self.rows,self.pkg,raw)

    def test_export_reproduces_and_never_overwrites(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'.cache') as tmp:
            a,z=Path(tmp)/'a',Path(tmp)/'z';main(['--salida',str(a)]);main(['--salida',str(z)])
            self.assertEqual({p.name:p.read_bytes() for p in a.iterdir()},{p.name:p.read_bytes() for p in z.iterdir()})
            with self.assertRaises(ValueError):main(['--salida',str(a)])
        for p in ['data/new','data/releases/new','data/processed/new','.git/new','docs']:
            with self.assertRaises(ValueError):main(['--salida',str(ROOT/p)])


if __name__=='__main__':unittest.main()
