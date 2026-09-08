"""Autoría escrita, lectura por tercero y no inferencia de asistencia."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from document_reviews import (PATH, AUTHOR_SOURCE, READER_SOURCE, ROLE_SOURCE, DOCUMENT_TYPE,
                              NOTICE, load_document_reviews, validate_document_reviews)
from continuity import annotate_turns
from review_flags import review_reasons

class DocumentReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.reviews=load_document_reviews(cls.raw)
    def load(self, entries, raw=None):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'reviews.json';p.write_text(json.dumps(entries))
            return load_document_reviews(self.raw if raw is None else raw,p)
    def parts(self,p,review=None):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],document=review or self.reviews[p])
    def rows(self,p):
        e=self.reviews[p];rows=[]
        for i,(text,actor,method) in enumerate(self.parts(p),1):
            doc=method==AUTHOR_SOURCE
            row=dict(ID=i,ID_Padre=p,Fecha=e['Fecha'],Texto=text,Actor_Final=actor,Fuente_Actor=method,
                     Tipo_Acta=DOCUMENT_TYPE if doc else '',Rol_Final=e['Rol_Autor'] if doc else b.roster_role_for(e['Fecha'],actor),
                     Fuente_Rol=ROLE_SOURCE if doc else 'LISTA_ASISTENCIA',Rol_Lista_Asistencia='' if doc else b.roster_role_for(e['Fecha'],actor),
                     Duplicado_Exacto='NO',ID_Intervencion=f'{p}:{i}',ID_Bloque_Texto=f'{p}:{i}')
            row['Motivos_Revision']=';'.join(review_reasons(row,b.TURN_DETECTOR,b.split_sentences))
            rows.append(row)
        return annotate_turns(rows)
    def test_six_exact_sources_are_documented(self):
        self.assertEqual(set(self.reviews),{5212,5742,5802,4453,4507,4722})
    def test_four_complete_parts_with_author_and_reader(self):
        for p,lengths in [(5212,[229,239,6039,250]),(5742,[498,366,4908,322]),(5802,[545,381,5094,322])]:
            parts=self.parts(p)
            self.assertEqual([a for t,a,m in parts],['Luis Óscar Herrera Barriga','Rodrigo Vergara Montes','Felipe Larraín Bascuñán','Rodrigo Vergara Montes'])
            self.assertEqual([len(t) for t,a,m in parts],lengths)
            self.assertEqual([m for t,a,m in parts][1:],[READER_SOURCE,AUTHOR_SOURCE,READER_SOURCE])
    def test_full_source_conservation(self):
        for p in self.reviews:
            self.assertEqual(''.join(''.join(t.split()) for t,a,m in self.parts(p)),''.join(self.raw[p]['Texto'].split()))
    def test_source_change_invalidates_review(self):
        raw=copy.deepcopy(self.raw);raw[5212]['Texto']+=' añadido'
        with self.assertRaisesRegex(ValueError,'texto de origen'):
            load_document_reviews(raw)
    def test_duplicate_and_wrong_date_rejected(self):
        entries=json.loads(PATH.read_text())
        with self.assertRaisesRegex(ValueError,'duplicado'):self.load(entries+[entries[0]])
        entries[0]['Fecha']='2012-11-14'
        with self.assertRaisesRegex(ValueError,'fecha'):self.load(entries)
    def test_partition_has_no_gaps_overlaps_or_truncation(self):
        for bounds in [[0,230,470,6509,6759],[0,230,200,6509,6760],[-1,230,470,6509,6760],[0,230,470,6760],[0,230,470,6509,6761]]:
            entries=json.loads(PATH.read_text());entries[0]['Limites']=bounds
            with self.assertRaisesRegex(ValueError,'partición'):self.load(entries)
    def test_quote_boundary_cannot_move_into_introduction_or_return(self):
        for idx,delta in [(2,-1),(2,1),(3,-1),(3,2)]:
            entries=json.loads(PATH.read_text());entries[0]['Limites'][idx]+=delta
            with self.assertRaisesRegex(ValueError,'límites'):self.load(entries)
    def test_no_author_or_reader_by_proximity(self):
        for key,value in [('Autor','Claudio Soto Gamboa'),('Lector','Enrique Marshall Rivera'),('Actor_Anterior','Claudio Soto Gamboa'),('Actor_Origen','Claudio Soto Gamboa')]:
            e=copy.deepcopy(self.reviews[5212]);e[key]=value
            with self.assertRaisesRegex(ValueError,'incompatibles'):self.parts(5212,e)
    def test_authorship_requires_exact_written_evidence(self):
        for key,value in [('Autor_Mencion','Rodrigo Cerda'),('Cita_Procedencia','Se recibe un documento.'),('Rol_Autor','Asesor')]:
            entries=json.loads(PATH.read_text());entries[0][key]=value
            with self.assertRaises(ValueError):self.load(entries)
    def test_attendance_cannot_be_inferred(self):
        entries=json.loads(PATH.read_text());entries[0]['Asistencia_Autor']='PRESENTE'
        with self.assertRaisesRegex(ValueError,'alcance'):self.load(entries)
        for p in self.reviews:
            row=self.rows(p)[2]
            self.assertEqual(row['Fuente_Rol'],ROLE_SOURCE)
            self.assertFalse(row['Rol_Lista_Asistencia'])
    def test_document_is_not_oral_or_current_council_agreement(self):
        for p in self.reviews:
            row=self.rows(p)[2]
            self.assertEqual(row['Tipo_Acta'],DOCUMENT_TYPE)
            self.assertEqual(row['Relacion_Turno'],'DOCUMENTO_PERSONAL')
            self.assertFalse(row['ID_Ancla_Actor']);self.assertFalse(row['ID_Antecedente_Continuidad'])
            self.assertIn(NOTICE,row['Motivos_Revision'])
    def test_no_automatic_document_detection_without_review(self):
        for p in self.reviews:
            r=self.raw[p]
            self.assertNotIn(AUTHOR_SOURCE,[m for t,a,m in b.segment_turns(r['Texto'],r['Fecha'],r['Actor'])])
    def test_review_conflict_rejected(self):
        r=self.raw[5212]
        with self.assertRaisesRegex(ValueError,'solapan'):
            b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review={'Actor':'x'},document=self.reviews[5212])
    def test_reader_returns_and_handoff_not_attributed_to_recipient(self):
        for p in self.reviews:
            parts=self.parts(p)
            self.assertTrue(parts[-1][0].startswith('A continuación' if p in [4453,4507] else 'Concluida la lectura'))
            self.assertIn({4453:'Rodrigo Vergara',4507:'Sebastián Claro'}.get(p,'Joaquín Vial'),parts[-1][0])
            self.assertEqual(parts[-1][1],'José De Gregorio Rebeco' if p==4453 else 'Rodrigo Vergara Montes')
    def test_ocr_and_quotes_are_not_rewritten(self):
        self.assertTrue(self.parts(5802)[1][0].endswith('( ■'))
        for p in self.reviews:
            text=self.parts(p)[2][0]
            self.assertTrue(text.startswith('“'));self.assertTrue(text.endswith('”'))
    def test_output_validator_and_exported_reader(self):
        for p in self.reviews:
            errors,records=validate_document_reviews(self.rows(p),{p:self.reviews[p]})
            self.assertEqual(errors,[]);self.assertEqual(len(records),1)
            self.assertEqual(records[0]['Autor'],'Felipe Larraín Bascuñán')
            self.assertEqual(records[0]['Lector'],'José De Gregorio Rebeco' if p==4453 else 'Rodrigo Vergara Montes')
            self.assertEqual(records[0]['ID_Documento'],3)
    def test_output_corruption_rejected(self):
        for field,value in [('Texto','truncado'),('Actor_Final','Rodrigo Vergara Montes'),('Fuente_Actor','SUJETO_NOMBRE'),
                            ('Tipo_Acta','ACUERDO_CONSEJO'),('Rol_Final','Consejero'),('Fuente_Rol','LISTA_ASISTENCIA'),
                            ('Rol_Lista_Asistencia','Ministro de Hacienda'),('Motivos_Revision',''),('ID_Ancla_Actor','falsa')]:
            rows=self.rows(5212);rows[2][field]=value
            self.assertTrue(validate_document_reviews(rows,{5212:self.reviews[5212]})[0],field)
    def test_removing_introduction_or_return_rejected(self):
        for index in [0,1,3]:
            rows=self.rows(5212);rows.pop(index)
            self.assertTrue(validate_document_reviews(rows,{5212:self.reviews[5212]})[0])
    def test_unregistered_document_is_rejected(self):
        self.assertTrue(validate_document_reviews(self.rows(5212),{})[0])

if __name__=='__main__':unittest.main()
