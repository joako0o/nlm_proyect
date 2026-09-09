"""LOOP31: asistencia distinta de habla, referencias y reservas textuales."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, text_hash
from institutional_reviews import (load_institutional_reviews, institutional_parts,
    institutional_type, validate_institutional_reviews, MOVEMENT_NOTE)
from mention_reviews import load_mention_reviews, validate_mention_reviews
from context_warnings import load_context_warnings, contextual_motives
from continuity import annotate_turns

ROOT=Path(__file__).resolve().parents[1]
MENTIONS=(202,410,953,1273,2499,2564,2608,2701,2743,3059,3286,3615,5078,6353,6402,6669,6891,6935,7124,7175)
def compact(t):return ''.join(t.split())
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

class LoopThirtyOneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={r[0]:dict(Fecha=b.to_date_str(r[1]),Texto=r[5],Actor=r[2]) for r in b.data}
        cls.institutions=load_institutional_reviews(cls.raw)
        cls.speakers=load_speaker_reviews(cls.raw)
        cls.mentions=load_mention_reviews(cls.raw)
        cls.warnings=load_context_warnings(cls.raw)

    def parts(self,p,reviewed=True):
        r=self.raw[p]
        return b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],review=self.speakers.get(p),
            institution=self.institutions.get(p) if reviewed else None)

    def rows(self,p):
        result=[];entry=self.institutions.get(p)
        for i,(text,actor,source) in enumerate(self.parts(p),1):
            event=bool(entry and text==entry.get('Texto_Acta'))
            result.append(dict(ID=i,ID_Padre=p,Fecha=self.raw[p]['Fecha'],Texto=text,Actor_Final=actor,
                Fuente_Actor=source,Rol_Final='Consejo' if actor==b.CONSEJO else 'persona',
                Fuente_Rol='ACTA_INSTITUCIONAL' if actor==b.CONSEJO else 'LISTA_ASISTENCIA',
                Tipo_Acta=institutional_type(text,entry) if entry else '',Motivos_Revision='',
                ID_Intervencion=f'{p}:{i}',ID_Bloque_Texto=f'{p}:{i}',
                Nota=MOVEMENT_NOTE+entry['Revision_ID']+' (prueba)' if event else ''))
        return annotate_turns(result)

    def load_entry(self,e,raw=None):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'r.json';p.write_text(json.dumps([e]))
            return load_institutional_reviews(self.raw if raw is None else raw,p)

    def test_only_two_new_institutional_reviews_not_new_personal_voices(self):
        self.assertEqual(set(self.institutions),{601,3110,4788,6808})
        self.assertNotIn(4788,self.speakers);self.assertNotIn(6808,self.speakers)
        for p in [4788,6808]:
            self.assertEqual(self.parts(p)[1][1:],(b.CONSEJO,'ACTA/META'))
            self.assertEqual(len(self.parts(p)),len(self.parts(p,False))+1)
            self.assertEqual(compact(self.raw[p]['Texto']),''.join(compact(t) for t,a,m in self.parts(p)))

    def test_no_global_arrival_or_retirement_detector(self):
        self.assertIn('se incorpora a la Sesión',self.parts(4788,False)[0][0])
        self.assertIn('se retiran de la Sala',self.parts(6808,False)[0][0])
        self.assertEqual(self.parts(4788,False)[0][1],'Rodrigo Vergara Montes')
        self.assertEqual(self.parts(6808,False)[0][1],'Rodrigo Valdés Pulido')

    def test_arrival_is_not_apology_or_vote(self):
        parts=self.parts(4788)
        self.assertEqual([len(t) for t,a,m in parts],[2132,112,161,333])
        self.assertTrue(parts[0][0].endswith('Sesión N° 184 Página 23 de 26'))
        self.assertIn('su voto es por mantener la TPM en 5% anual',parts[0][0])
        self.assertTrue(parts[2][0].startswith('El señor Ministro presenta sus excusas'))
        self.assertEqual(parts[2][1],'Felipe Larraín Bascuñán')
        self.assertEqual(parts[3][1],'Rodrigo Vergara Montes')
        self.assertEqual(len(self.parts(4789)[0][0]),8541)

    def test_retirement_is_not_joint_speech_or_communique(self):
        rows=self.rows(6808)
        self.assertEqual([len(r['Texto']) for r in rows],[518,114,1940])
        self.assertEqual([r['Tipo_Acta'] for r in rows],['','ACTA_INSTITUCIONAL','ACUERDO_CONSEJO'])
        self.assertNotIn('Claudio Soto Gamboa',[r['Actor_Final'] for r in rows])
        self.assertTrue(rows[0]['Texto'].startswith('El señor Rodrigo Valdés, antes de retirarse'))
        self.assertTrue(rows[2]['Texto'].startswith('A continuación, el Consejo procede'))
        self.assertNotEqual(rows[1]['ID_Turno'],rows[2]['ID_Turno'])

    def test_movement_has_no_anchor_and_note_does_not_leak(self):
        for p in [4788,6808]:
            rows=self.rows(p)
            self.assertFalse(validate_institutional_reviews(rows,{p:self.institutions[p]}))
            self.assertFalse(rows[1]['ID_Ancla_Actor'])
            self.assertFalse(rows[1]['ID_Antecedente_Continuidad'])
            self.assertEqual(sum(MOVEMENT_NOTE in r['Nota'] for r in rows),1)
        rows=self.rows(4788)
        for r in rows[2:]:self.assertEqual(r['ID_Ancla_Actor'],r['ID_Intervencion'])
        self.assertEqual(self.rows(6808)[0]['ID_Ancla_Actor'],'6808:1')

    def test_hash_date_antecedent_evidence_and_bounds_fail_closed(self):
        for p in [4788,6808]:
            for key,value in [('SHA256_Texto_Padre','0'*64),('SHA256_Texto_Antecedente','0'*64),
                    ('ID_Antecedente',p-2),('Fecha','1900-01-01'),('Inicio',0),('Inicio',True),
                    ('Fin',len(self.raw[p]['Texto'])),('Texto_Acta','otro texto'),('Movimiento','OTRO'),
                    ('Decision','CONTINUACION_INSTITUCIONAL_NO_HABLA_PERSONAL'),('Evidencia',[])]:
                e=copy.deepcopy(self.institutions[p]);e[key]=value
                with self.subTest(p=p,key=key),self.assertRaises(ValueError):self.load_entry(e)
            e=copy.deepcopy(self.institutions[p]);e['Evidencia'][0]['SHA256_Texto_Padre']='0'*64
            with self.assertRaises(ValueError):self.load_entry(e)

    def test_quote_and_separator_guards(self):
        for prefix in ['“','«','"']:
            e=copy.deepcopy(self.institutions[6808]);raw=copy.deepcopy(self.raw)
            text=prefix+raw[6808]['Texto'];raw[6808]['Texto']=text;e['Texto_Padre']=text
            e['SHA256_Texto_Padre']=text_hash(text);e['Inicio']+=1;e['Fin']+=1
            with self.assertRaises(ValueError):self.load_entry(e,raw)
        e=copy.deepcopy(self.institutions[6808]);raw=copy.deepcopy(self.raw)
        text=raw[6808]['Texto'];i=text.rfind('.',0,e['Inicio']);text=text[:i]+','+text[i+1:]
        raw[6808]['Texto']=text;e['Texto_Padre']=text;e['SHA256_Texto_Padre']=text_hash(text)
        with self.assertRaises(ValueError):self.load_entry(e,raw)

    def test_partitions_cannot_invent_or_discard_personal_speech(self):
        for p in [4788,6808]:
            for key,value in [('Actor','Sergio Lehmann Beresi'),('Fuente_Actor','CONTEXTO_REVISADO'),('Texto','texto inventado')]:
                e=copy.deepcopy(self.institutions[p]);e['Tramos_Resultado'][0][key]=value;r=self.raw[p]
                with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],institution=e)
            with self.assertRaises(ValueError):institutional_parts(self.raw[p]['Texto'],self.institutions[p])
            with self.assertRaises(ValueError):institutional_type('texto fuera del padre',self.institutions[p])

    def test_builder_rejects_overlapping_reviews_and_wrong_context(self):
        for p in [4788,6808]:
            e=self.institutions[p];r=self.raw[p]
            for kwargs in [dict(review={}),dict(document={})]:
                with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],r['Actor'],institution=e,**kwargs)
            with self.assertRaises(ValueError):b.segment_turns(r['Texto'],'1900-01-01',r['Actor'],institution=e)
            with self.assertRaises(ValueError):b.segment_turns(r['Texto'],r['Fecha'],'Sergio Lehmann Beresi',institution=e)

    def test_export_validation_rejects_actor_type_role_anchor_and_note_drift(self):
        for p in [4788,6808]:
            for key,value in [('Actor_Final','Claudio Soto Gamboa'),('Tipo_Acta','COMUNICADO'),
                    ('Fuente_Rol','LISTA_ASISTENCIA'),('Rol_Final','Ministro de Hacienda'),
                    ('ID_Ancla_Actor','falsa'),('ID_Antecedente_Continuidad','falso'),('Nota','')]:
                rows=self.rows(p);rows[1][key]=value
                self.assertTrue(validate_institutional_reviews(rows,{p:self.institutions[p]}))
            rows=self.rows(p);rows[0]['Nota']=rows[1]['Nota']
            self.assertTrue(validate_institutional_reviews(rows,{p:self.institutions[p]}))
            self.assertTrue(validate_institutional_reviews(self.rows(p)[1:],{p:self.institutions[p]}))
            self.assertTrue(validate_institutional_reviews(self.rows(p),{}))

    def test_twenty_new_mentions_do_not_rewrite_or_close_warnings(self):
        for p in MENTIONS:
            rows=self.rows(p);before=copy.deepcopy(rows)
            rv={k:e for k,e in self.mentions.items() if e['ID_Padre']==p and '-L31-' in k}
            self.assertEqual(len(rv),1)
            errors,annotations=validate_mention_reviews(rows,rv)
            self.assertFalse(errors);self.assertEqual(len(annotations),1);self.assertEqual(rows,before)
            for mutation,value in [('Actor_Final',b.CONSEJO),('Texto','otra cosa')]:
                altered=copy.deepcopy(rows);rid=next(iter(annotations));next(r for r in altered if r['ID']==rid)[mutation]=value
                self.assertTrue(validate_mention_reviews(altered,rv)[0])

    def test_three_rereadings_do_not_duplicate_old_records(self):
        for p in [1338,3147,5658]:
            rv={k:e for k,e in self.mentions.items() if e['ID_Padre']==p}
            self.assertEqual(len(rv),1);self.assertNotIn('-L31-',next(iter(rv)))
            self.assertFalse(validate_mention_reviews(self.rows(p),rv)[0])

    def test_foreign_president_and_silva_are_references_not_alias_closure(self):
        for p,actor,quote in [(5658,'Joaquín Vial Ruiz-Tagle','Banco Central de Reserva de Perú'),
                (6402,'Rodrigo Vergara Montes','la señora Silva ha prometido')]:
            parts=self.parts(p);self.assertEqual(len(parts),1);self.assertEqual(parts[0][1],actor)
            self.assertIn(quote,parts[0][0])

    def test_four_warnings_are_bounded_and_literal(self):
        for p,index,quote in [(202,0,'octubre de 2005'),(2701,0,'hace prensar'),(3147,1,'AA Dado eso'),(5078,0,'V')]:
            rows=self.rows(p);w=self.warnings[p]
            self.assertIn(quote,rows[index]['Texto'])
            self.assertEqual([i for i,r in enumerate(rows) if contextual_motives(r,{p:w})],[index])
            changed=copy.deepcopy(rows[index]);changed['Texto']+='!'
            self.assertFalse(contextual_motives(changed,{p:w}))
        self.assertTrue(self.parts(5078)[0][0].endswith('V'))
        self.assertEqual(self.raw[202]['Fecha'],'2005-04-07')
        self.assertIn('7 de abril de 2005',self.raw[201]['Texto'])
        self.assertEqual(len(self.parts(202)[1][0]),11028)

    def test_complements_and_actual_returns_stay_distinct(self):
        for p,who in [(3615,'Claudio Soto Gamboa'),(7124,'Rodrigo Vergara Montes')]:
            rows=self.rows(p)
            self.assertEqual(rows[0]['Actor_Final'],who);self.assertEqual(rows[-1]['Actor_Final'],who)
            self.assertEqual(rows[-1]['ID_Ancla_Actor'],rows[-1]['ID_Intervencion'])
            self.assertNotEqual(rows[0]['ID_Turno'],rows[-1]['ID_Turno'])
        self.assertEqual(self.parts(7175)[1][1],'Mario Marcel Cullell')
        self.assertEqual(len(self.parts(2608)),6)
        self.assertEqual(self.parts(2608)[-1][2],'CONTEXTO_REVISADO')

    def test_pending_joint_or_uncertain_readings_remain_pending(self):
        for p in [6185,3775,4055,2510]:
            e=next(e for e in self.mentions.values() if e['ID_Padre']==p)
            self.assertEqual(e['Decision'],'PENDIENTE_DELIMITAR_APORTE')

# Frozen source/signature and registry tests are appended below.

    def test_parent_202_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[202]['Texto']),'f744a11cebfa1e44ec1d0603a99c1d62d471787565bbe1c78a13820d5e846fbe')
        parts=self.parts(202)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 767, 'SUJETO_ROL_SESION'), ('Pablo García Silva', 11028, 'SUJETO_ROL_NOMBRE'), ('Vittorio Corbo Lioi', 88, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[202]['Texto']))

    def test_parent_410_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[410]['Texto']),'1e71ec213ee6cb711fde57b2d3d68d4d9dbe6b70fe228972e8d180669eb1e8fb')
        parts=self.parts(410)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Beltrán de Ramón Acevedo', 558, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[410]['Texto']))

    def test_parent_953_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[953]['Texto']),'164512117106b84eb746393c7dc134d7e9b0ac92c6aaf521d1188e4e818dd273')
        parts=self.parts(953)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sergio Lehmann Beresi', 1037, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[953]['Texto']))

    def test_parent_1273_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[1273]['Texto']),'091f55e0803f268f76163bef11c7a588cdf75dc95b1a8da8d7e7bb774e36354f')
        parts=self.parts(1273)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 165, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[1273]['Texto']))

    def test_parent_1338_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[1338]['Texto']),'b5671da33cc8aa975aab8b5677bfd45ae12fb11d727ea7284bed516af3d068a3')
        parts=self.parts(1338)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Vittorio Corbo Lioi', 470, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 74, 'ACTA/META'), ('Esteban Jadresic Marinovic', 3316, 'SUJETO_ROL_NOMBRE'), ('Vittorio Corbo Lioi', 139, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[1338]['Texto']))

    def test_parent_2499_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[2499]['Texto']),'7748d6f484ac5ef61e7e17b857546c0952409fb76a4c7ca227af873593c0cb2d')
        parts=self.parts(2499)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Jorge Desormeaux Jiménez', 6880, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2499]['Texto']))

    def test_parent_2564_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[2564]['Texto']),'32e7e5441abb9af25a19680d40bf8e1e605516ea1746704a2ecde99f1aab8c87')
        parts=self.parts(2564)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 311, 'SUJETO_ROL_NOMBRE'), ('Beltrán de Ramón Acevedo', 688, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2564]['Texto']))

    def test_parent_2608_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[2608]['Texto']),'9be87c4bedff1acd74d3960aa69b54e1f9c5099b04d017c829b72ebcc03f9cd3')
        parts=self.parts(2608)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sergio Lehmann Beresi', 1036, 'SUJETO_ROL_SESION'), ('Andrés Velasco Brañes', 714, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 252, 'SUJETO_ROL_SESION'), ('Andrés Velasco Brañes', 106, 'SUJETO_NOMBRE'), ('Jorge Desormeaux Jiménez', 169, 'SUJETO_ROL_SESION'), ('Sergio Lehmann Beresi', 2323, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2608]['Texto']))

    def test_parent_2701_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[2701]['Texto']),'eead6604919346ce6694c245f4a81b8fa8d5ff0208c00fba2b372261f442729c')
        parts=self.parts(2701)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 3144, 'SUJETO_NOMBRE'), ('Sebastián Claro Edwards', 251, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 838, 'SUJETO_ROL_NOMBRE'), ('Kevin Cowan Logan', 503, 'SUJETO_ROL_NOMBRE'), ('Manuel Marfán Lewis', 836, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2701]['Texto']))

    def test_parent_2743_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[2743]['Texto']),'260048d124b4be52becebcc63d5678a33b8bac37cd3c3cc9701149a591563c29')
        parts=self.parts(2743)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Jorge Desormeaux Jiménez', 169, 'SUJETO_NOMBRE'), ('Andrés Velasco Brañes', 69, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[2743]['Texto']))

    def test_parent_3059_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[3059]['Texto']),'aa3f6718fb185fec90ae4c4540deffa9c5fe69aedb2522835b479b1c4919a8b2')
        parts=self.parts(3059)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 754, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3059]['Texto']))

    def test_parent_3147_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[3147]['Texto']),'89cda9f19ba68255595049376f5a771810604217912df600004dd509e382e5f4')
        parts=self.parts(3147)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('José De Gregorio Rebeco', 203, 'SUJETO_ROL_NOMBRE'), ('Beltrán de Ramón Acevedo', 900, 'SUJETO_ROL_SESION'), ('José De Gregorio Rebeco', 185, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3147]['Texto']))

    def test_parent_3286_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[3286]['Texto']),'0e833f6192d9afab604ba34bac7f284c47d6723aa232fd13a7e345eec807f4c9')
        parts=self.parts(3286)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Luis Felipe Céspedes Cifuentes', 500, 'SUJETO_ROL_NOMBRE'), ('Enrique Marshall Rivera', 284, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 1547, 'SUJETO_ROL_SESION')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3286]['Texto']))

    def test_parent_3615_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[3615]['Texto']),'500591dc69853d8d0c713e2ef6681ec8240b544df8b2a6600fd8eeb2c62713a0')
        parts=self.parts(3615)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Claudio Soto Gamboa', 198, 'SUJETO_NOMBRE'), ('Ricardo Vicuña Poblete', 565, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 946, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[3615]['Texto']))

    def test_parent_4787_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[4787]['Texto']),'6c8eea4b429fff0950190e102e2478e02bbb2b62190efc40a353d2d4c5951500')
        parts=self.parts(4787)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Manuel Marfán Lewis', 3844, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Vergara Montes', 1423, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[4787]['Texto']))

    def test_parent_4788_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[4788]['Texto']),'5e6168f1c610bac2f3ab5bfeab1f0928645f53e639ca799121cf03771fed927d')
        parts=self.parts(4788)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 2132, 'SUJETO_ROL_NOMBRE'), ('Consejo del Banco Central de Chile', 112, 'ACTA/META'), ('Felipe Larraín Bascuñán', 161, 'SUJETO_ROL_SESION'), ('Rodrigo Vergara Montes', 333, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[4788]['Texto']))

    def test_parent_4789_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[4789]['Texto']),'58bd5a5ec08e55978c5e5f27dbd11a467d3d673a63529a03f2450af819f2c0e9')
        parts=self.parts(4789)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Felipe Larraín Bascuñán', 8541, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[4789]['Texto']))

    def test_parent_5078_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[5078]['Texto']),'56a207e93143678474b771d3becce4f5b71c0081fd3b7e9836e0b151627e78ad')
        parts=self.parts(5078)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Luis Óscar Herrera Barriga', 286, 'SUJETO_NOMBRE'), ('Sergio Lehmann Beresi', 1926, 'SUJETO_ROL_NOMBRE'), ('Luis Óscar Herrera Barriga', 623, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[5078]['Texto']))

    def test_parent_5658_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[5658]['Texto']),'dd64f78c2b0a39fdee35f6e803852fc819640ed7eaba58df72e54f1f65517e4e')
        parts=self.parts(5658)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Joaquín Vial Ruiz-Tagle', 477, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[5658]['Texto']))

    def test_parent_6353_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[6353]['Texto']),'9a05c25c248ad0d6dca09595c30e79522197f21f9dc8ca3634844e0842b6c675')
        parts=self.parts(6353)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Joaquín Vial Ruiz-Tagle', 1904, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6353]['Texto']))

    def test_parent_6402_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[6402]['Texto']),'eefea13f5cebfaa579975652ae4e298b3c466f33f85db62a32b4f2cd653b795d')
        parts=self.parts(6402)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 736, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6402]['Texto']))

    def test_parent_6669_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[6669]['Texto']),'26b9bd3dd60b9961136b6ed37543bdbfa3d0dfae080bfc51017dd99ef887fdfc')
        parts=self.parts(6669)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Sebastián Claro Edwards', 703, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6669]['Texto']))

    def test_parent_6807_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[6807]['Texto']),'3cbf67d828141b3678c86c4d90717c12cc0e9962a93c3c26e451b1533b17fcd2')
        parts=self.parts(6807)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 260, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6807]['Texto']))

    def test_parent_6808_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[6808]['Texto']),'32abf83e1251ea0d3989e22a0b41f9fbc50367ff3d1d859cdb2c80dee08bc3c3')
        parts=self.parts(6808)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Valdés Pulido', 518, 'SUJETO_NOMBRE'), ('Consejo del Banco Central de Chile', 114, 'ACTA/META'), ('Consejo del Banco Central de Chile', 1940, 'ACTA/META')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6808]['Texto']))

    def test_parent_6809_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[6809]['Texto']),'e2830184137f9b2fa510d995d31fd6ecedcfa509b6c26a118d28a7f5ee05b8bf')
        parts=self.parts(6809)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Consejo del Banco Central de Chile', 149, 'ACTA/META')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6809]['Texto']))

    def test_parent_6891_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[6891]['Texto']),'1f44948a5ba317375070893420394aae08c3b394a8fd477d119c11dede1912f6')
        parts=self.parts(6891)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Miguel Fuentes Díaz', 275, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6891]['Texto']))

    def test_parent_6935_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[6935]['Texto']),'cccc3b532972f2feca6d8b13a419a044c161511fe770e05a72d5e97e6f6ed2b4')
        parts=self.parts(6935)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[("Alberto Naudon Dell'Oro", 413, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[6935]['Texto']))

    def test_parent_7124_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[7124]['Texto']),'2fe0f46f6d5b93714baeae3d6331441fce42b2d3e2c449eee3be7f6ef24e0f9c')
        parts=self.parts(7124)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[('Rodrigo Vergara Montes', 1413, 'SUJETO_ROL_NOMBRE'), ("Alberto Naudon Dell'Oro", 1348, 'SUJETO_NOMBRE'), ('Rodrigo Vergara Montes', 192, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[7124]['Texto']))

    def test_parent_7175_source_signature_and_conservation(self):
        self.assertEqual(text_hash(self.raw[7175]['Texto']),'c4b74aba5a9408cca9542dd180fd3dc7ff840399ab9ef5832078e40fb81dc67c')
        parts=self.parts(7175)
        self.assertEqual([(a,len(t),m) for t,a,m in parts],[("Alberto Naudon Dell'Oro", 776, 'SUJETO_NOMBRE'), ('Mario Marcel Cullell', 350, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(compact(t) for t,a,m in parts),compact(self.raw[7175]['Texto']))

    def test_frozen_revisiones_hablantes_prefix(self):
        es=json.loads((ROOT/'data/curation/revisiones_hablantes.json').read_text())
        self.assertEqual(digest(es[:353]),'9be4c82a8a5202268bb6c9e35f04c84ecea9436da98cd5784285d1a8ac33e803')

    def test_frozen_alertas_contextuales_prefix(self):
        es=json.loads((ROOT/'data/curation/alertas_contextuales.json').read_text())
        self.assertEqual(digest(es[:77]),'f1894feef5dc8661626c4c3efe5c7de3aa2df01702753d86f67739b0c6da3a17')

    def test_frozen_revisiones_menciones_actuales_prefix(self):
        es=json.loads((ROOT/'data/curation/revisiones_menciones_actuales.json').read_text())
        self.assertEqual(digest(es[:57]),'98ddbfdfab0baa8fd77f5bb26a9fc4f7014dc238a60fe590d07b6a5724135409')

    def test_frozen_revisiones_continuidad_hablantes_prefix(self):
        es=json.loads((ROOT/'data/curation/revisiones_continuidad_hablantes.json').read_text())
        self.assertEqual(digest(es[:24]),'018b71de71c52b50063c25ff74df9d712bb6d5eae62e0a571f14ca132fc76b9e')

    def test_frozen_revisiones_documentos_leidos_prefix(self):
        es=json.loads((ROOT/'data/curation/revisiones_documentos_leidos.json').read_text())
        self.assertEqual(digest(es[:12]),'b189d3c4e3f462c05c842650ab5f9608b2cbb2491f033e72c6960defaee5fe0c')

    def test_frozen_revisiones_continuaciones_acta_prefix(self):
        es=json.loads((ROOT/'data/curation/revisiones_continuaciones_acta.json').read_text())
        self.assertEqual(digest(es[:2]),'997074a565a0e1605055f6c568e349841ad2d1c2f158257591011d8d5454e2fe')

    def test_frozen_alertas_contextuales_retiradas_prefix(self):
        es=json.loads((ROOT/'data/curation/alertas_contextuales_retiradas.json').read_text())
        self.assertEqual(digest(es[:3]),'c0ad72321cd33d5b32dc7798ecdcdbb9fd473797e4e2fea992270d3c7caae6c5')

if __name__ == "__main__":
    unittest.main()
