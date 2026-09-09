"""Tercer lote: concentración por padre y preservación de exposiciones extensas."""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import revisar_cola_comas as c

PATHS=[ROOT/f'docs/revision_comas_lote{n}_2026-09-08/revisiones.json' for n in [1,2,3]]

class CommaThirdBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=c.read_rows(ROOT/'data/processed/consolidado_base_referencia.xlsx')
        cls.packages=[json.loads(p.read_text()) for p in PATHS]
        cls.new=cls.packages[-1]

    def parent(self,p):
        return [r for r in self.rows if r['ID_Padre']==p]

    def one(self,e):
        p=e['ID_Padre'];package=copy.deepcopy(self.new)
        package['Revisiones']=[copy.deepcopy(e)];package['Padres']={str(p):package['Padres'][str(p)]}
        return copy.deepcopy(self.parent(p)),package

    def test_previous_lots_frozen(self):
        for path,digest in zip(PATHS[:2],['efd48b25aaa63ca591eb1bd2ca7923edff8bc2ede898c0635f73719b660b80fc','bb343dc2fd538d47a701f9d80a82200d1d9b13088cd70789f79e77efa0b70a99']):
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),digest)

    def test_forty_new_limits_twenty_nine_complete_parents(self):
        self.assertEqual(len(c.validate_reviews(self.rows,self.new)),40)
        self.assertEqual(len(self.new['Padres']),29)
        self.assertEqual(sum(len(e['Texto_Padre']) for e in self.new['Padres'].values()),45575)
        old={p for pkg in self.packages[:2] for p in pkg['Padres']}
        self.assertFalse(old & set(self.new['Padres']))

    def test_one_hundred_twenty_readings_forty_seven_remaining(self):
        package=c.combine_packages(self.packages);before=copy.deepcopy(self.rows)
        queue=c.build_queue(self.rows,package)
        self.assertEqual(len(queue),167);self.assertEqual(len(package['Padres']),104)
        self.assertEqual(sum(q['Estado_Lectura']==c.STATE for q in queue),120)
        self.assertEqual(sum(q['Estado_Lectura']==c.PENDING for q in queue),47)
        remaining=[q for q in queue if q['Estado_Lectura']==c.PENDING]
        self.assertEqual(len({q['ID_Padre'] for q in remaining}),47)
        self.assertEqual(sum('Consejo del Banco' in q['Actor_Izquierda']+q['Actor_Derecha'] for q in remaining),5)
        self.assertEqual(self.rows,before)
        self.assertEqual(sum(bool(r['Motivos_Revision']) for r in self.rows),465)

    def test_long_parent_2765_and_lehmann_8714_preserved(self):
        rows=self.parent(2765)
        self.assertEqual(len(self.new['Padres']['2765']['Texto_Padre']),12127)
        self.assertEqual([(r['Actor_Final'],len(r['Texto'])) for r in rows],
            [('Manuel Marfán Lewis',869),('Sergio Lehmann Beresi',1845),('Sebastián Claro Edwards',387),
             ('José De Gregorio Rebeco',139),('Jorge Desormeaux Jiménez',168),('Sergio Lehmann Beresi',8714)])
        self.assertIn('comentario del señor Claro',rows[3]['Texto'])
        self.assertNotEqual(rows[1]['ID_Turno'],rows[5]['ID_Turno'])
        self.assertEqual(c.compact(self.new['Padres']['2765']['Texto_Padre']),''.join(c.compact(r['Texto']) for r in rows))

    def test_twelve_segments_of_2661_and_own_later_anchor(self):
        rows=self.parent(2661);self.assertEqual(len(rows),12)
        self.assertEqual([len(r['Texto']) for r in rows],[98,219,292,917,193,49,1322,107,375,58,69,208])
        self.assertEqual(rows[6]['ID_Ancla_Actor'],rows[6]['ID_Intervencion'])
        self.assertEqual(len([e for e in self.new['Revisiones'] if e['ID_Padre']==2661]),4)
        self.assertEqual(rows[1]['Motivos_Revision'],'FINAL_SIN_PUNTUACION')

    def test_other_long_presentations_not_split_at_topics(self):
        for p,seg,size in [(2696,3,2570),(2608,6,2323),(2981,4,3212),(2805,1,4385),(2896,4,1249)]:
            r=next(r for r in self.parent(p) if r['Numero_Segmento']==seg)
            self.assertEqual(len(r['Texto']),size)
        self.assertIn('A El señor Lehmann',self.new['Padres']['2805']['Texto_Padre'])
        self.assertIn('V*',self.new['Padres']['2981']['Texto_Padre'])
        self.assertIn('/ Añade',self.new['Padres']['2696']['Texto_Padre'])

    def test_brief_and_duplicate_residual_alerts_preserved(self):
        self.assertEqual(self.parent(2911)[1]['Motivos_Revision'],'FRAGMENTO_BREVE')
        self.assertEqual(self.parent(3186)[1]['Motivos_Revision'],'DUPLICADO_NO_FORMULA')
        self.assertEqual(self.parent(2805)[0]['Motivos_Revision'],'FINAL_SIN_PUNTUACION')
        for p in [2911,3186,2805]:
            self.assertTrue(next(e for e in self.new['Revisiones'] if e['ID_Padre']==p)['Reservas'])

    def test_figures_and_name_in_3313_not_corrected(self):
        text=self.new['Padres']['3313']['Texto_Padre']
        self.assertIn('De Gregario',text);self.assertIn('100.000 Y 150.000 mil personas',text)
        self.assertTrue(next(e for e in self.new['Revisiones'] if e['ID_Padre']==3313)['Reservas'])

    def test_each_endpoint_invalidated_by_changes(self):
        for e in self.new['Revisiones']:
            for side in ['Izquierda','Derecha']:
                for field,value in [('Texto','Cambiado,'),('Actor_Final','Otra persona'),('Fecha','1900-01-01'),('Fuente_Actor','ORIGINAL')]:
                    rows,package=self.one(e)
                    next(r for r in rows if r['ID_Intervencion']==e[side]['ID_Intervencion'])[field]=value
                    with self.subTest(rid=e['Revision_ID'],side=side,field=field),self.assertRaises(ValueError):
                        c.validate_reviews(rows,package)

    def test_change_in_unreviewed_part_of_long_parent_invalidates(self):
        e=next(e for e in self.new['Revisiones'] if e['ID_Padre']==2765)
        for field in ['Texto','Rol_Final','ID_Ancla_Actor','Motivos_Revision']:
            rows,package=self.one(e);rows[-1][field]='Cambio'
            with self.assertRaises(ValueError):c.validate_reviews(rows,package)

    def test_duplicate_cannot_be_counted_as_new_progress(self):
        for prefix in [self.packages,self.packages[::-1]]:
            with self.assertRaisesRegex(ValueError,'duplicado'):c.combine_packages(prefix+[self.new])

    def test_own_returns_and_registered_continuity(self):
        for p,q in [(2911,2912),(2918,2919),(2695,2696)]:
            self.assertEqual(self.parent(p)[-1]['ID_Turno'],self.parent(q)[0]['ID_Turno'])
        for p in [631,2896,3028,3353,2922,3044]:
            rows=self.parent(p)
            for a,b in zip(rows,rows[1:]):
                if a['Actor_Final']!=b['Actor_Final']:self.assertNotEqual(a['ID_Turno'],b['ID_Turno'])
        r=self.parent(3044)[-1];self.assertEqual(r['ID_Ancla_Actor'],r['ID_Intervencion'])

    def test_raw_source_guards_and_new_parent_signatures(self):
        c.check_sources(self.new)
        for p,e in self.new['Padres'].items():
            self.assertEqual(e['SHA256_Texto_Padre'],c.sha(e['Texto_Padre']))
            self.assertEqual(e['SHA256_Particion'],c.parent_signature(self.parent(int(p))))

    def test_cumulative_order_does_not_change_results(self):
        self.assertEqual(c.build_queue(self.rows,c.combine_packages(self.packages)),
                         c.build_queue(self.rows,c.combine_packages(self.packages[::-1])))


if __name__=='__main__':
    unittest.main()
