"""Lote2 y acumulación segura: lecturas previas inmutables, sin cierres implícitos."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import revisar_cola_comas as c

FIRST = ROOT / 'docs/revision_comas_lote1_2026-09-08/revisiones.json'
SECOND = ROOT / 'docs/revision_comas_lote2_2026-09-08/revisiones.json'


class CommaSecondBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = c.read_rows(ROOT / 'data/processed/consolidado_base_referencia.xlsx')
        cls.first = json.loads(FIRST.read_text())
        cls.second = json.loads(SECOND.read_text())

    def one(self, e):
        p = e['ID_Padre']; package = copy.deepcopy(self.second)
        package['Revisiones'] = [copy.deepcopy(e)]
        package['Padres'] = {str(p): package['Padres'][str(p)]}
        return copy.deepcopy([r for r in self.rows if r['ID_Padre'] == p]), package

    def test_first_batch_frozen_byte_for_byte(self):
        self.assertEqual(hashlib.sha256(FIRST.read_bytes()).hexdigest(), 'efd48b25aaa63ca591eb1bd2ca7923edff8bc2ede898c0635f73719b660b80fc')

    def test_new_forty_limits_and_thirty_nine_full_parents(self):
        self.assertEqual(len(c.validate_reviews(self.rows, self.second)), 40)
        self.assertEqual(len(self.second['Padres']), 39)
        self.assertEqual(sum(len(e['Texto_Padre']) for e in self.second['Padres'].values()), 42333)
        self.assertEqual({r['ID_Padre'] for r in self.second['Revisiones'] if r['ID_Padre'] in {int(p) for p in self.first['Padres']}}, set())

    def test_cumulative_eighty_without_mutation(self):
        originals = copy.deepcopy([self.first,self.second]); rows = copy.deepcopy(self.rows)
        package = c.combine_packages([self.first,self.second])
        self.assertEqual(len(c.validate_reviews(self.rows, package)), 80)
        self.assertEqual(len(package['Padres']), 75)
        self.assertEqual([self.first,self.second], originals); self.assertEqual(self.rows, rows)
        package['Revisiones'][0]['Justificacion'] = 'mutado'
        self.assertEqual([self.first,self.second], originals)

    def test_eighty_reviewed_eighty_seven_without_fiche(self):
        queue = c.build_queue(self.rows,c.combine_packages([self.first,self.second]))
        self.assertEqual(len(queue),167)
        self.assertEqual(sum(q['Estado_Lectura']==c.STATE for q in queue),80)
        self.assertEqual(sum(q['Estado_Lectura']==c.PENDING for q in queue),87)
        self.assertEqual({q['Motivo_Original'] for q in queue},{'FINAL_SIN_PUNTUACION'})

    def test_order_of_packages_does_not_change_queue(self):
        self.assertEqual(c.build_queue(self.rows,c.combine_packages([self.first,self.second])),
                         c.build_queue(self.rows,c.combine_packages([self.second,self.first])))

    def test_same_package_twice_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicado'):c.combine_packages([self.first,self.first])

    def test_renamed_duplicate_limit_rejected(self):
        duplicate = copy.deepcopy(self.first); duplicate['Revisiones'][0]['Revision_ID'] += '-nuevo'
        with self.assertRaisesRegex(ValueError,'duplicado'):c.combine_packages([self.first,duplicate])

    def test_duplicate_revision_id_on_different_limit_rejected(self):
        altered = copy.deepcopy(self.second); altered['Revisiones'][0]['Revision_ID'] = self.first['Revisiones'][0]['Revision_ID']
        with self.assertRaisesRegex(ValueError,'duplicado'):c.combine_packages([self.first,altered])

    def test_conflicting_source_or_parent_rejected(self):
        altered = copy.deepcopy(self.second)
        key = next(iter(altered['SHA256_Fuentes'])); altered['SHA256_Fuentes'][key] = '0'*64
        with self.assertRaisesRegex(ValueError,'fuente'):c.combine_packages([self.first,altered])
        altered = copy.deepcopy(self.first); key = next(iter(altered['Padres'])); altered['Padres'][key]['Texto_Padre'] += '!'
        with self.assertRaisesRegex(ValueError,'padre'):c.combine_packages([self.first,altered])

    def test_empty_or_malformed_packages_rejected(self):
        for packages in [[],[None],[{}],[{'Version':2}],[{'Version':1}]]:
            with self.assertRaises(ValueError):c.combine_packages(packages)

    def test_each_side_invalidated_by_changes(self):
        for e in self.second['Revisiones']:
            for side in ['Izquierda','Derecha']:
                for field,value in [('Texto','Cambio,'),('Actor_Final','Otra persona'),('Fecha','1900-01-01'),('Fuente_Actor','ORIGINAL')]:
                    rows,package = self.one(e)
                    next(r for r in rows if r['ID_Intervencion']==e[side]['ID_Intervencion'])[field] = value
                    with self.subTest(rid=e['Revision_ID'],side=side,field=field),self.assertRaises(ValueError):
                        c.validate_reviews(rows,package)

    def test_nonfocal_partition_change_invalidates(self):
        e = next(e for e in self.second['Revisiones'] if e['ID_Padre']==6862)
        rows,package = self.one(e); rows[-1]['Texto'] += ' Cambio.'
        with self.assertRaises(ValueError):c.validate_reviews(rows,package)

    def test_long_presentation_not_cut_at_topic_changes(self):
        rows = [r for r in self.rows if r['ID_Padre']==2738]
        self.assertEqual([(r['Actor_Final'],len(r['Texto'])) for r in rows],
                         [('Claudio Soto Gamboa',4743),('José De Gregorio Rebeco',105),('Claudio Soto Gamboa',947),('Manuel Marfán Lewis',401)])
        self.assertNotEqual(rows[0]['ID_Turno'],rows[2]['ID_Turno'])
        self.assertIn('comentando el Presidente',rows[1]['Texto'])
        self.assertIn('continúa el señor Gerente',rows[2]['Texto'])

    def test_raw_residues_and_names_not_normalized(self):
        p = self.second['Padres']
        self.assertIn('señor Claudia Soto',p['3620']['Texto_Padre'])
        self.assertIn('~ .,',p['3620']['Texto_Padre'])
        self.assertIn('Sebastián Sobre el particular',p['4366']['Texto_Padre'])
        for n in ['4826','5003']:self.assertTrue(p[n]['Texto_Padre'].endswith('A continuación,.'))

    def test_residual_alerts_preserved(self):
        for p,seg,motive in [(4470,2,'DUPLICADO_NO_FORMULA'),(5643,1,'TEXTO_DANADO_POR_COTEJAR'),(6862,4,'TEXTO_DANADO_POR_COTEJAR')]:
            r = next(r for r in self.rows if r['ID_Padre']==p and r['Numero_Segmento']==seg)
            self.assertIn(motive,r['Motivos_Revision'])
        package = c.combine_packages([self.first,self.second]); before = copy.deepcopy(self.rows)
        c.build_queue(self.rows,package); self.assertEqual(self.rows,before)

    def test_existing_links_and_returns_remain(self):
        for p,q in [(4470,4471),(5003,5004),(5872,5873)]:
            a=[r for r in self.rows if r['ID_Padre']==p][-1];b=next(r for r in self.rows if r['ID_Padre']==q)
            self.assertEqual(a['ID_Turno'],b['ID_Turno'])
        for p in [3388,3395,3620,3843,4341,6135]:
            rows=[r for r in self.rows if r['ID_Padre']==p]
            for a,b in zip(rows,rows[1:]):
                if a['Actor_Final']!=b['Actor_Final']:self.assertNotEqual(a['ID_Turno'],b['ID_Turno'])

    def test_prior_windows_only_promoted_after_new_full_reading(self):
        reviewed=c.validate_reviews(self.rows,self.second)
        for p in [4096,6415,7176]:
            self.assertTrue(any(e['ID_Padre']==p for e in reviewed.values()))
            self.assertEqual(self.second['Padres'][str(p)]['Lectura'],'PADRE_COMPLETO')

    def test_five_institutional_limits_still_not_approved(self):
        queue=c.build_queue(self.rows,c.combine_packages([self.first,self.second]))
        institutional=[q for q in queue if 'Consejo del Banco' in q['Actor_Izquierda']+q['Actor_Derecha']]
        self.assertEqual({q['ID_Padre'] for q in institutional},{601,1901,2112,2803,5252})
        self.assertEqual({q['Estado_Lectura'] for q in institutional},{c.PENDING})

    def test_cli_accepts_multiple_packages(self):
        with tempfile.TemporaryDirectory() as temp:
            args=['revisar_cola_comas','--revisiones',str(FIRST),'--revisiones',str(SECOND),'--salida',temp]
            with patch.object(sys,'argv',args),patch('builtins.print'):
                c.main()
            s=json.loads((Path(temp)/'resumen.json').read_text())
            self.assertEqual((s['Lotes'],s['Limites_Con_Ficha'],s['Limites_Sin_Ficha']),(2,80,87))
            self.assertIsNone(s['SHA256_Revisiones']);self.assertEqual(len(s['SHA256_Lotes']),2)

    def test_cli_validates_each_package_before_combining(self):
        with tempfile.TemporaryDirectory() as temp:
            altered=copy.deepcopy(self.first);del altered['Padres'][next(iter(altered['Padres']))]
            path=Path(temp)/'incompleto.json';path.write_text(json.dumps(altered))
            args=['revisar_cola_comas','--revisiones',str(path),'--revisiones',str(SECOND),'--salida',str(Path(temp)/'out')]
            with patch.object(sys,'argv',args),patch.object(c,'read_rows',return_value=self.rows),self.assertRaises(ValueError):
                c.main()
            self.assertFalse((Path(temp)/'out/resumen.json').exists())


if __name__=='__main__':
    unittest.main()
