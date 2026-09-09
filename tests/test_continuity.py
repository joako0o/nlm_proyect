"""Regresiones de exposiciones multipárrafo, referencias y barreras de turno."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_base_referencia as b
from continuity import annotate_turns, update_state
from qa_preparacion import validate_continuity

GARCIA = 'Pablo García Silva'
CORBO = 'Vittorio Corbo Lioi'
MARFAN = 'Manuel Marfán Lewis'
LEHMANN = 'Sergio Lehmann Beresi'
DATE = '2005-02-10'


def sequence(paragraphs):
    """Resuelve y relaciona una secuencia sin reemplazar la evidencia de origen."""
    rows=[]
    states={}
    for parent, date, actor, text in paragraphs:
        state=states.setdefault(date, {'date':date})
        parts=b.segment_turns(text,date,actor,state)
        for number,(body,who,source) in enumerate(parts,1):
            source=source or 'ORIGINAL'
            rid=len(rows)+1
            tipo='META_SESION' if who==b.CONSEJO else ''
            row={'ID':rid,'ID_Padre':parent,'Fecha':date,'Actor_Final':who,'Texto':body,
                 'Fuente_Actor':source,'Tipo_Acta':tipo,'Motivos_Revision':'',
                 'ID_Intervencion':f'RPM-{date}:{parent}:{number}',
                 'ID_Bloque_Texto':f'RPM-{date}:{parent}:B{number}'}
            rows.append(row)
            update_state(state,who,source,body,date,b.TURN_DETECTOR,b.split_sentences,rid,bool(tipo))
    return annotate_turns(rows)


class ContinuityTests(unittest.TestCase):
    def test_long_presentation_without_repeating_name(self):
        paragraphs=[(1,DATE,GARCIA,'El señor Pablo García señala que la actividad aumenta.')]
        paragraphs += [(n,DATE,GARCIA,'Por otra parte, la inflación se mantiene acotada. Agrega que el consumo es dinámico.') for n in range(2,17)]
        rows=sequence(paragraphs)
        self.assertEqual(len(rows),16)
        self.assertEqual({r['Actor_Final'] for r in rows},{GARCIA})
        self.assertEqual(len({r['ID_Turno'] for r in rows}),1)
        self.assertTrue(all(r['Fuente_Actor']=='CONTINUIDAD_PARRAFO' for r in rows[1:]))
        self.assertEqual(validate_continuity(rows),[])

    def test_generic_manager_continues_presentation(self):
        rows=sequence([(1,DATE,GARCIA,'El señor Pablo García señala que la actividad aumenta.'),
                       (2,DATE,GARCIA,'Señala el señor Gerente que la inflación sigue acotada.'),
                       (3,DATE,GARCIA,'El consumo privado crece en línea con lo esperado.')])
        self.assertEqual([r['Fuente_Actor'] for r in rows],['SUJETO_NOMBRE','ANAFORA_CONTINUIDAD','CONTINUIDAD_PARRAFO'])
        self.assertEqual(len({r['ID_Turno'] for r in rows}),1)
        self.assertEqual(validate_continuity(rows),[])

    def test_explicit_same_person_can_span_rows(self):
        rows=sequence([(1,DATE,GARCIA,'El señor Pablo García señala que hay riesgos.'),
                       (2,DATE,GARCIA,'El señor García agrega que son acotados.')])
        self.assertEqual(rows[1]['Relacion_Turno'],'CONTINUIDAD_EXPLICITA')
        self.assertEqual(rows[0]['ID_Turno'],rows[1]['ID_Turno'])

    def test_real_february_presentation(self):
        paragraphs=[(r[0],b.to_date_str(r[1]),r[2],r[5]) for r in b.data if 60<=r[0]<=70]
        rows=sequence(paragraphs)
        self.assertEqual(len(rows),11)
        self.assertEqual({r['Actor_Final'] for r in rows},{GARCIA})
        self.assertEqual(len({r['ID_Turno'] for r in rows}),1)
        self.assertEqual(validate_continuity(rows),[])

    def test_real_march_presentation(self):
        paragraphs=[(r[0],b.to_date_str(r[1]),r[2],r[5]) for r in b.data if 142<=r[0]<=152]
        rows=sequence(paragraphs)
        self.assertEqual({r['Actor_Final'] for r in rows},{GARCIA})
        self.assertEqual(len({r['ID_Turno'] for r in rows}),1)
        self.assertEqual(validate_continuity(rows),[])

    def test_new_session_does_not_inherit(self):
        rows=sequence([(1,DATE,GARCIA,'El señor Pablo García señala que hay riesgos.'),
                       (2,'2005-03-10',GARCIA,'Las perspectivas internacionales mejoraron.')])
        self.assertNotEqual(rows[0]['ID_Turno'],rows[1]['ID_Turno'])
        self.assertEqual(rows[1]['Fuente_Actor'],'ORIGINAL')
        self.assertFalse(rows[1]['ID_Antecedente_Continuidad'])

    def test_different_source_actor_not_overridden_by_proximity(self):
        rows=sequence([(1,DATE,GARCIA,'El señor Pablo García señala que hay riesgos.'),
                       (2,DATE,CORBO,'La inflación se mantiene acotada.')])
        self.assertEqual(rows[1]['Actor_Final'],CORBO)
        self.assertEqual(rows[1]['Fuente_Actor'],'ORIGINAL')
        self.assertFalse(rows[1]['ID_Antecedente_Continuidad'])

    def test_handoff_is_a_barrier_not_recipient_speech(self):
        rows=sequence([(1,DATE,CORBO,'El Presidente señor Corbo ofrece la palabra al señor Pablo García.'),
                       (2,DATE,CORBO,'Se presentan las proyecciones de crecimiento.')])
        self.assertEqual(rows[0]['Actor_Final'],CORBO)
        self.assertFalse(rows[1]['ID_Antecedente_Continuidad'])
        self.assertNotEqual(rows[1]['Fuente_Actor'],'CONTINUIDAD_PARRAFO')

    def test_handoff_can_resolve_next_paragraph_generic_subject(self):
        rows=sequence([(1,DATE,CORBO,'El Presidente señor Corbo ofrece la palabra al Gerente de Análisis Macroeconómico señor Pablo García.'),
                       (2,DATE,GARCIA,'El señor Gerente señala que la actividad se acelera.')])
        self.assertEqual(rows[1]['Actor_Final'],GARCIA)
        self.assertNotEqual(rows[0]['ID_Turno'],rows[1]['ID_Turno'])
        # Evidence is a handoff, not an already established same-person chain.
        self.assertEqual(rows[1]['Fuente_Actor'],'ANAFORA_LOCAL')

    def test_interruption_and_return_are_separate_turns(self):
        rows=sequence([(1,DATE,GARCIA,'El señor Pablo García señala que hay riesgos.'),
                       (2,DATE,MARFAN,'El Consejero señor Marfán pregunta por la inflación.'),
                       (3,DATE,GARCIA,'El señor García retoma su exposición.')])
        self.assertEqual(len({r['ID_Turno'] for r in rows}),3)

    def test_institutional_break_clears_anchor(self):
        rows=sequence([(1,DATE,GARCIA,'El señor Pablo García señala que hay riesgos.'),
                       (2,DATE,b.CONSEJO,'Se suspende la sesión.'),
                       (3,DATE,GARCIA,'La actividad sigue dinámica.')])
        self.assertEqual(rows[-1]['Fuente_Actor'],'ORIGINAL')
        self.assertFalse(rows[-1]['ID_Ancla_Actor'])

    def test_unknown_subject_does_not_get_continuity_label(self):
        rows=sequence([(1,DATE,GARCIA,'El señor Pablo García señala que hay riesgos.'),
                       (2,DATE,GARCIA,'El señor Participante Desconocido explica la proyección.')])
        self.assertNotEqual(rows[1]['Fuente_Actor'],'CONTINUIDAD_PARRAFO')

    def test_unanchored_original_cannot_start_chain(self):
        rows=sequence([(1,DATE,GARCIA,'La actividad aumenta.'),(2,DATE,GARCIA,'La inflación disminuye.')])
        self.assertTrue(all(r['Fuente_Actor']=='ORIGINAL' for r in rows))
        self.assertEqual(len({r['ID_Turno'] for r in rows}),2)

    def test_response_to_question_keeps_respondent(self):
        text=('El señor Sergio Lehmann responde que la actividad mejora. '
              'Ante la consulta del Consejero señor Rodrigo Vergara sobre la inflación, agrega que sigue acotada.')
        parts=b.segment_turns(text,'2011-09-15',LEHMANN)
        self.assertEqual([a for _,a,_ in parts],[LEHMANN])

    def test_reference_to_previous_speaker_is_not_new_turn(self):
        text=('El Presidente señor José De Gregorio señala que los riesgos siguen acotados. '
              'En conclusión, y tal como lo señaló el señor Vicepresidente con un argumento similar, plantea que mantener la tasa es prudente.')
        parts=b.segment_turns(text,'2011-02-17','José De Gregorio Rebeco')
        self.assertEqual([a for _,a,_ in parts],['José De Gregorio Rebeco'])

    def test_real_referential_false_splits(self):
        expected={3454:'Claudio Soto Gamboa',3715:'José De Gregorio Rebeco',4266:'Claudio Soto Gamboa'}
        for parent,actor in expected.items():
            with self.subTest(parent=parent):
                r=next(r for r in b.data if r[0]==parent)
                parts=b.segment_turns(r[5],b.to_date_str(r[1]),r[2])
                self.assertEqual({a for _,a,_ in parts},{actor})

    def test_opinion_after_response_is_genuine_new_speaker(self):
        r=next(r for r in b.data if r[0]==4350)
        parts=b.segment_turns(r[5],b.to_date_str(r[1]),r[2])
        matched=[a for t,a,_ in parts if 'es de opinión' in t]
        self.assertEqual(matched,['Sebastián Claro Edwards'])

    def test_mentioned_manager_responds_after_councillor(self):
        r=next(r for r in b.data if r[0]==2058)
        parts=b.segment_turns(r[5],b.to_date_str(r[1]),r[2])
        self.assertEqual([a for _,a,_ in parts], ['José De Gregorio Rebeco', MARFAN, 'Claudio Soto Gamboa', 'José De Gregorio Rebeco'])

    def test_reference_does_not_imply_turn_without_speech(self):
        text=('El Consejero señor Marfán comenta el informe del Gerente de Análisis Macroeconómico señor Claudio Soto. '
              'Añade que ese informe es muy completo y debe seguir actualizándose.')
        parts=b.segment_turns(text,'2008-09-04',MARFAN)
        self.assertEqual([a for _,a,_ in parts],[MARFAN])

    def test_mutation_cross_actor_chain_fails(self):
        rows=sequence([(1,DATE,GARCIA,'El señor Pablo García señala que hay riesgos.'),
                       (2,DATE,GARCIA,'La actividad aumenta.')])
        rows[1]['Actor_Final']=CORBO
        self.assertTrue(any('cruza actor' in e for e in validate_continuity(rows)))

    def test_mutation_future_anchor_fails(self):
        rows=sequence([(1,DATE,GARCIA,'El señor Pablo García señala que hay riesgos.'),
                       (2,DATE,GARCIA,'El señor García agrega que son acotados.')])
        rows[0]['ID_Ancla_Actor']=rows[1]['ID_Intervencion']
        self.assertTrue(any('ancla' in e for e in validate_continuity(rows)))

    def test_mutation_nonadjacent_antecedent_fails(self):
        rows=sequence([(1,DATE,GARCIA,'El señor Pablo García señala que hay riesgos.'),
                       (2,DATE,GARCIA,'La actividad aumenta.'),(3,DATE,GARCIA,'La inflación disminuye.')])
        rows[2]['ID_Antecedente_Continuidad']=rows[0]['ID_Intervencion']
        self.assertTrue(any('antecedente' in e for e in validate_continuity(rows)))


if __name__=='__main__':
    unittest.main()
