"""783 alertas: distinción entre revisión dirigida, comparación y pendientes."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_base_referencia as b
from procedural import is_formula, load_formula_reviews, PATH
from review_queue import load_baseline, track


class ReplyClauseTests(unittest.TestCase):
    def test_inline_response_has_two_actors_and_preserves_connector(self):
        t='El Presidente señor Corbo consulta por la inflación, a lo cual el Consejero señor Marfán responde que sigue estable.'
        p=b.segment_turns(t,'2005-02-10','Vittorio Corbo Lioi')
        self.assertEqual([a for t,a,m in p],['Vittorio Corbo Lioi','Manuel Marfán Lewis'])
        self.assertTrue(p[1][0].startswith('a lo cual'))
        self.assertEqual(''.join(''.join(t.split()) for t,a,m in p),''.join(t.split()))

    def test_embedded_quote_is_not_new_turn(self):
        t='El Presidente señor Corbo señala: “Consulta por la inflación, a lo cual el Consejero señor Marfán responde que sigue estable”.'
        self.assertEqual(len(b.segment_turns(t,'2005-02-10','Vittorio Corbo Lioi')),1)

    def test_relative_clause_without_reply_comma_is_not_split(self):
        t='El Presidente señor Corbo se refiere a lo que el Consejero señor Marfán señala en su minuta.'
        self.assertEqual(len(b.segment_turns(t,'2005-02-10','Vittorio Corbo Lioi')),1)

    def test_mention_without_speech_verb_is_not_split(self):
        t='El Presidente señor Corbo comenta la inflación, a lo cual el Consejero señor Marfán prestó atención.'
        self.assertEqual(len(b.segment_turns(t,'2005-02-10','Vittorio Corbo Lioi')),1)

    def test_first_speaker_not_lost_when_source_names_second(self):
        r=next(r for r in b.data if r[0]==3369)
        self.assertEqual([a for t,a,m in b.segment_turns(r[5],b.to_date_str(r[1]),r[2])],['Manuel Marfán Lewis','Rodrigo Vergara Montes'])

    def test_presenter_returns_after_inline_response(self):
        expected={3189:['Enrique Marshall Rivera','Pablo García Silva','Manuel Marfán Lewis'],
                  6415:['Rodrigo Vergara Montes','Matías Bernier Bórquez','Miguel Fuentes Díaz','Rodrigo Vergara Montes'],
                  1857:['Manuel Marfán Lewis','Sergio Lehmann Beresi']}
        for p,actors in expected.items():
            r=next(r for r in b.data if r[0]==p)
            with self.subTest(parent=p):
                parts=b.segment_turns(r[5],b.to_date_str(r[1]),r[2])
                # El constructor aplica detect al tramo inicial sin método explícito.
                actual=[a if m else b.detect(t,b.to_date_str(r[1]))[0] for t,a,m in parts]
                self.assertEqual(actual,actors)


class QueueReviewTests(unittest.TestCase):
    def test_snapshot_contains_exactly_783_unique_alerts(self):
        baseline,decisions=load_baseline()
        self.assertEqual(len(baseline['Filas']),783)
        self.assertEqual(len(decisions),16)

    def test_reviewed_formulas_have_quotes_in_raw_parents(self):
        raw={r[0]:{'Texto':r[5]} for r in b.data}
        self.assertEqual(len(load_formula_reviews(raw_by_id=raw)),21)

    def test_substantive_recommendation_is_not_cleared_as_formula(self):
        text='El Gerente de División Estudios señor Luis Óscar Herrera concluye su exposición manifestando que conforme a las consideraciones expuestas, esa Gerencia propone al Consejo mantener la Tasa de Política Monetaria en su nivel actual.'
        self.assertFalse(is_formula(text))

    def test_exact_formula_does_not_license_substantive_tail(self):
        text=next(iter(load_formula_reviews()))
        self.assertTrue(is_formula(text))
        self.assertFalse(is_formula(text+' Propone aumentar la tasa en 50 puntos base.'))

    def test_tampered_formula_hash_fails(self):
        entries=json.loads(PATH.read_text());entries[0]['Texto']+=' cambio'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'f.json';p.write_text(json.dumps(entries))
            with self.assertRaisesRegex(ValueError,'hash'):load_formula_reviews(p)

    def test_tracking_rejects_missing_source_interval(self):
        baseline,_=load_baseline()
        with self.assertRaisesRegex(ValueError,'no se conserva'):track([],baseline,{})

    def test_tracking_does_not_call_unchanged_row_reviewed(self):
        row={'ID':1,'ID_Padre':1,'Texto':'Texto.','Fecha':'2005-01-11','Actor_Final':'Actor',
             'Fuente_Actor':'ORIGINAL','Motivos_Revision':'ATRIBUCION_HEURISTICA_LEGADA'}
        old={**row,'Inicio_Compacto':0,'Fin_Compacto':6,'SHA256_Texto':'hash'}
        item=track([row],{'Filas':[old]}, {})[0]
        self.assertEqual(item['Estado_Seguimiento'],'PENDIENTE_LECTURA_CONTEXTUAL')
        self.assertEqual(item['Tipo_Revision'],'TRIAJE_AUTOMATICO')


if __name__=='__main__':unittest.main()
