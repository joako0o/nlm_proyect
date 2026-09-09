"""Lote4: voto/exposición largos, turnos breves y final dañado no reconstruido."""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import revisar_cola_comas as c
PATHS=[ROOT/f'docs/revision_comas_lote{n}_2026-09-08/revisiones.json' for n in [1,2,3,4]]

class CommaFourthBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=c.read_rows(ROOT/'data/processed/consolidado_base_referencia.xlsx')
        cls.packages=[json.loads(p.read_text()) for p in PATHS]
        cls.new=cls.packages[-1]

    def parent(self,p):return [r for r in self.rows if r['ID_Padre']==p]

    def one(self,e):
        p=e['ID_Padre'];package=copy.deepcopy(self.new)
        package['Revisiones']=[copy.deepcopy(e)];package['Padres']={str(p):package['Padres'][str(p)]}
        return copy.deepcopy(self.parent(p)),package

    def test_previous_packages_frozen(self):
        hashes=['efd48b25aaa63ca591eb1bd2ca7923edff8bc2ede898c0635f73719b660b80fc','bb343dc2fd538d47a701f9d80a82200d1d9b13088cd70789f79e77efa0b70a99','28f16b295bb6d3502e39545ac3fcef19f9054817aa6b2f7765e9ca4faa94ca52']
        for path,h in zip(PATHS[:3],hashes):self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),h)

    def test_twenty_two_limits_and_complete_parents(self):
        self.assertEqual(len(c.validate_reviews(self.rows,self.new)),22)
        self.assertEqual(len(self.new['Padres']),22)
        self.assertEqual(sum(len(e['Texto_Padre']) for e in self.new['Padres'].values()),57607)
        self.assertFalse(set(self.new['Padres']) & {p for pkg in self.packages[:3] for p in pkg['Padres']})

    def test_cumulative_progress_not_alert_closure(self):
        before=copy.deepcopy(self.rows);package=c.combine_packages(self.packages);queue=c.build_queue(self.rows,package)
        self.assertEqual(len(queue),167);self.assertEqual(len(package['Padres']),126)
        self.assertEqual(sum(q['Estado_Lectura']==c.STATE for q in queue),142)
        remaining=[q for q in queue if q['Estado_Lectura']==c.PENDING]
        self.assertEqual(len(remaining),25);self.assertEqual(len({q['ID_Padre'] for q in remaining}),25)
        self.assertEqual(sum('Consejo del Banco' in q['Actor_Izquierda']+q['Actor_Derecha'] for q in remaining),5)
        self.assertEqual(self.rows,before);self.assertEqual(sum(bool(r['Motivos_Revision']) for r in self.rows),465)

    def test_marshall_vote_and_cespedes_exposition_remain_complete(self):
        self.assertEqual([(r['Actor_Final'],len(r['Texto'])) for r in self.parent(3123)],
            [('Enrique Marshall Rivera',5484),('José De Gregorio Rebeco',108),('Manuel Marfán Lewis',57)])
        self.assertEqual([(r['Actor_Final'],len(r['Texto'])) for r in self.parent(2644)],
            [('José De Gregorio Rebeco',99),('Luis Felipe Céspedes Cifuentes',4101),('José De Gregorio Rebeco',142)])
        self.assertTrue(self.parent(2644)[1]['Texto'].startswith('quien comienza'))

    def test_fifteen_turns_1718_not_merged_or_split(self):
        rows=self.parent(1718);self.assertEqual(len(rows),15)
        self.assertEqual([len(r['Texto']) for r in rows],[690,89,181,139,705,644,266,187,266,119,132,323,283,171,948])
        self.assertIn('Selaive y Rappaport',rows[2]['Texto'])
        self.assertEqual(rows[9]['Motivos_Revision'],'FINAL_SIN_PUNTUACION')

    def test_2938_only_start_identified_damage_stays(self):
        rows=self.parent(2938);self.assertEqual([len(r['Texto']) for r in rows],[105,51,634])
        self.assertTrue(rows[1]['Texto'].endswith('tendrá efectos en los'))
        self.assertEqual(rows[1]['Motivos_Revision'],'FINAL_SIN_PUNTUACION;TEXTO_DANADO_POR_COTEJAR')
        e=next(e for e in self.new['Revisiones'] if e['ID_Padre']==2938)
        self.assertTrue(e['Reservas']);self.assertIn('sin reconstruir',e['Justificacion'])

    def test_other_literals_and_reservations_remain(self):
        p=self.new['Padres']
        for n in ['2956','2567','2863']:self.assertTrue(p[n]['Texto_Padre'].endswith('A continuación,.'))
        self.assertIn('ha caído algo r últimamente',p['2863']['Texto_Padre'])
        self.assertIn('/ .',p['2699']['Texto_Padre'])
        self.assertIn('relaciones menores',p['3303']['Texto_Padre'])
        self.assertIn('Lehman Brothers',p['2810']['Texto_Padre'])

    def test_each_endpoint_invalidated_by_changes(self):
        for e in self.new['Revisiones']:
            for side in ['Izquierda','Derecha']:
                for field,value in [('Texto','Cambio,'),('Actor_Final','Otra persona'),('Fecha','1900-01-01'),('Fuente_Actor','ORIGINAL')]:
                    rows,package=self.one(e)
                    next(r for r in rows if r['ID_Intervencion']==e[side]['ID_Intervencion'])[field]=value
                    with self.subTest(rid=e['Revision_ID'],side=side,field=field),self.assertRaises(ValueError):c.validate_reviews(rows,package)

    def test_nonfocal_vote_change_invalidates_fiche(self):
        e=next(e for e in self.new['Revisiones'] if e['ID_Padre']==3123)
        for field in ['Texto','Rol_Final','ID_Ancla_Actor','Motivos_Revision']:
            rows,package=self.one(e);rows[0][field]='Cambio'
            with self.assertRaises(ValueError):c.validate_reviews(rows,package)

    def test_registered_links_and_returns_preserved(self):
        for p,q in [(3123,3124),(1386,1387),(2863,2864),(2566,2567),(2956,2957)]:
            self.assertEqual(self.parent(p)[-1]['ID_Turno'],self.parent(q)[0]['ID_Turno'])
        for p in [2931,2740,2697,2699,2567,3303]:
            rows=self.parent(p)
            for a,b in zip(rows,rows[1:]):
                if a['Actor_Final']!=b['Actor_Final']:self.assertNotEqual(a['ID_Turno'],b['ID_Turno'])

    def test_raw_source_guards_and_signatures(self):
        c.check_sources(self.new)
        for p,e in self.new['Padres'].items():
            self.assertEqual(e['SHA256_Texto_Padre'],c.sha(e['Texto_Padre']))
            self.assertEqual(e['SHA256_Particion'],c.parent_signature(self.parent(int(p))))
            self.assertEqual(c.compact(e['Texto_Padre']),''.join(c.compact(r['Texto']) for r in self.parent(int(p))))

    def test_duplicate_cannot_inflate_progress(self):
        with self.assertRaisesRegex(ValueError,'duplicado'):c.combine_packages(self.packages+[self.new])

if __name__=='__main__':unittest.main()
