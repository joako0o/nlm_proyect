"""LOOP26: voces, documentos leídos y continuidades individuales; OCR literal."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_base_referencia as b
from curation import load_speaker_reviews, speaker_intervals, validate_speaker_reviews
from document_reviews import load_document_reviews, validate_document_reviews, PATH as DOC_PATH
from reviewed_continuity import load_reviewed_links, validate_reviewed_links, RELATION
from continuity import annotate_turns, update_state
from context_warnings import load_context_warnings, contextual_motives
from mention_reviews import load_mention_reviews, validate_mention_reviews

DOCUMENTS = (3071, 3575, 4109, 5257, 5892, 5999)
PERSONAL = (3092, 4143, 4778)
LINKS = ((4745, 4746), (6561, 6562))

class LoopTwentySixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = {r[0]: dict(Fecha=b.to_date_str(r[1]), Texto=r[5], Actor=r[2]) for r in b.data}
        cls.reviews = load_speaker_reviews(cls.raw)
        cls.docs = load_document_reviews(cls.raw)
        cls.links = load_reviewed_links(cls.raw)
        cls.warnings = load_context_warnings(cls.raw)
        cls.mentions = load_mention_reviews(cls.raw)

    def parts(self, p, reviewed=True):
        r = self.raw[p]
        return b.segment_turns(r['Texto'], r['Fecha'], r['Actor'],
            review=self.reviews.get(p) if reviewed else None,
            document=self.docs.get(p) if reviewed else None)

    def load_doc(self, entry, raw=None):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'docs.json'
            path.write_text(json.dumps([entry]))
            return load_document_reviews(self.raw if raw is None else raw, path)

    def entry(self, p):
        return next(e for e in json.loads(DOC_PATH.read_text()) if e['ID_Padre'] == p)

    def doc_rows(self, p):
        # Import local: no rediscovery of the other TestCase in this module.
        from test_document_reviews import DocumentReviewTests
        helper = DocumentReviewTests()
        helper.raw = self.raw
        helper.reviews = self.docs
        return helper.rows(p)

    def pair(self, key):
        e = self.links[key]
        return [dict(ID=i, ID_Padre=side['ID_Padre'], Fecha=e['Fecha'], Texto=side['Texto'],
            Actor_Final=e['Actor'], Fuente_Actor=side['Fuente_Actor'], Tipo_Acta='',
            ID_Intervencion=f'{side["ID_Padre"]}:1', ID_Bloque_Texto=f'{side["ID_Padre"]}:1',
            Motivos_Revision='', Duplicado_Exacto='NO')
            for i, side in enumerate([e['Anterior'], e['Siguiente']], 1)]

    def test_three_new_speaker_intervals_are_exact(self):
        for p in PERSONAL:
            self.assertEqual(sum('-L26-' in e['Revision_ID'] for e in speaker_intervals(self.reviews[p])), 1)
            rows = [dict(ID=i, ID_Padre=p, Texto=t, Actor_Final=a, Fuente_Actor=m)
                for i, (t, a, m) in enumerate(self.parts(p))]
            self.assertFalse(validate_speaker_reviews(rows, {p: self.reviews[p]}))

    def test_personal_reviews_never_become_global_anchors(self):
        for p in PERSONAL:
            for t, a, m in self.parts(p):
                if m == 'CONTEXTO_REVISADO':
                    state = {}
                    update_state(state, a, m, t, self.raw[p]['Fecha'], b.TURN_DETECTOR, b.split_sentences, 'synthetic')
                    self.assertFalse(state['anchor'])

    def test_citing_a_poll_is_vergara_not_a_reference_to_his_speech(self):
        text, actor, method = self.parts(3092)[1]
        self.assertEqual(actor, 'Rodrigo Vergara Montes')
        self.assertIn('cita una encuesta', text)
        self.assertIn('65%', text)
        self.assertFalse(b.TURN_DETECTOR.speaker(text, self.raw[3092]['Fecha']))

    def test_ajuicio_is_not_rewritten_and_bernanke_not_a_turn(self):
        parts = self.parts(4143)
        self.assertTrue(parts[1][0].startswith('Ajuicio del Presidente'))
        self.assertIn('Bernanke', parts[0][0])
        self.assertEqual(len(parts), 2)

    def test_closure_is_not_marshall_or_an_institutional_reopening(self):
        parts = self.parts(4778)
        self.assertEqual(parts[1][1], 'Rodrigo Vergara Montes')
        self.assertTrue(parts[1][0].startswith('Sesión N° 184 Página 15 de 26 Por no haber'))
        self.assertEqual(parts[2][1:], (b.CONSEJO, 'ACTA/META'))
        self.assertTrue(parts[2][0].startswith('Siendo las 16:00 horas'))

    def test_received_comments_do_not_certify_written_sending_medium(self):
        for p in [3071, 3575, 4109]:
            self.assertNotIn('por escrito', self.parts(p)[1][0])
            self.assertIn('Rodrigo Cerda', self.parts(p)[1][0])
            self.assertEqual(self.parts(p)[2][1], 'Felipe Larraín Bascuñán')
            self.assertEqual(self.docs[p]['Asistencia_Autor'], 'NO_INFERIDA_DEL_DOCUMENTO')

    def test_nominal_introductions_retain_explicit_written_provenance(self):
        for p in [5257, 5999]:
            self.assertIn('por escrito', self.parts(p)[1][0])
            self.assertIn('Presidente señor Rodrigo Vergara informa', self.parts(p)[1][0])

    def test_all_new_documents_need_opt_in_not_automatic_detection(self):
        for p in DOCUMENTS:
            self.assertNotIn('DOCUMENTO_ESCRITO_REVISADO', [m for t, a, m in self.parts(p, False)])

    def test_dropping_any_variant_opt_in_rejects_its_source(self):
        for p in DOCUMENTS:
            original = self.entry(p)
            for key in ['Tipo_Procedencia', 'Tipo_Retorno', 'Tipo_Comillas', 'Tipo_Anterior']:
                if key not in original:
                    continue
                with self.subTest(parent=p, option=key):
                    entry = copy.deepcopy(original)
                    del entry[key]
                    with self.assertRaises(ValueError):
                        docs = self.load_doc(entry)
                        b.segment_turns(self.raw[p]['Texto'], self.raw[p]['Fecha'], self.raw[p]['Actor'], document=docs[p])

    def test_unknown_variant_modes_are_rejected(self):
        for key in ['Tipo_Procedencia', 'Tipo_Retorno', 'Tipo_Comillas', 'Tipo_Anterior']:
            entry = self.entry(5257)
            entry[key] = 'INFERENCIA_LIBRE'
            with self.assertRaises(ValueError):
                self.load_doc(entry)

    def test_mixed_quotes_remain_literal(self):
        for p, pair in [(3071, ('"', '”')), (5892, ('“', '"'))]:
            text = self.parts(p)[2][0]
            self.assertEqual((text[0], text[-1]), pair)
            self.assertEqual(sum(text.count(c) for c in '“”"'), 2)

    def test_wrong_mixed_pair_is_not_silently_normalized(self):
        for p in [3071, 5892]:
            for pair in [['“', '”'], ['"', '"'], [], None, ['x', 'y']]:
                entry = self.entry(p)
                entry['Comillas'] = pair
                with self.assertRaises(ValueError):
                    self.load_doc(entry)

    def test_normalizing_source_quotes_invalidates_hash(self):
        for p in [3071, 5892]:
            raw = copy.deepcopy(self.raw)
            raw[p]['Texto'] = raw[p]['Texto'].replace('"', '“' if p == 3071 else '”')
            with self.assertRaises(ValueError):
                self.load_doc(self.entry(p), raw)

    def test_citations_and_bounds_are_not_advisory(self):
        for p in DOCUMENTS:
            for key in ['Cita_Procedencia', 'Cita_Retorno', 'Cita_Anterior']:
                entry = self.entry(p)
                if key in entry:
                    entry[key] += ' alterada'
                    with self.assertRaises(ValueError):
                        self.load_doc(entry)
            for index in [2, 3]:
                entry = self.entry(p)
                entry['Limites'][index] -= 1
                with self.assertRaises(ValueError):
                    self.load_doc(entry)

    def test_coordination_needs_the_presidential_antecedent(self):
        entry = copy.deepcopy(self.docs[3575])
        entry['Actor_Anterior'] = 'Luis Óscar Herrera Barriga'
        entry['_Tramos'][0] = 'El señor Luis Óscar Herrera informa.'
        with self.assertRaises(ValueError):
            b.segment_turns(self.raw[3575]['Texto'], self.raw[3575]['Fecha'], self.raw[3575]['Actor'], document=entry)

    def test_nominal_variant_cannot_be_applied_to_old_impersonal_intro(self):
        entry = self.entry(5212)
        entry['Tipo_Procedencia'] = 'LECTURA_NOMINAL_POR_ESCRITO_REVISADA'
        with self.assertRaises(ValueError):
            self.load_doc(entry)

    def test_arrival_is_institutional_not_presidential_speech(self):
        rows = self.doc_rows(5257)
        self.assertEqual(rows[0]['Actor_Final'], b.CONSEJO)
        self.assertEqual(rows[0]['Fuente_Actor'], 'ACTA/META')
        self.assertEqual(rows[0]['Rol_Final'], 'Consejo')
        self.assertFalse(rows[0]['ID_Ancla_Actor'])
        self.assertFalse(validate_document_reviews(rows, {5257: self.docs[5257]})[0])

    def test_arrival_output_cannot_be_promoted_to_a_speaker_or_anchor(self):
        for key, value in [('Actor_Final', 'Rodrigo Vergara Montes'), ('Fuente_Actor', 'SUJETO_NOMBRE'),
            ('Rol_Final', 'Presidente del Banco Central'), ('Tipo_Acta', ''),
            ('Fuente_Rol', 'LISTA_ASISTENCIA'), ('ID_Ancla_Actor', 'falsa')]:
            rows = self.doc_rows(5257)
            rows[0][key] = value
            self.assertTrue(validate_document_reviews(rows, {5257: self.docs[5257]})[0])

    def test_arrival_exception_cannot_cover_a_different_first_sentence(self):
        entry = self.entry(5999)
        entry.update(Tipo_Anterior='INCORPORACION_INSTITUCIONAL_REVISADA',
            Actor_Anterior=b.CONSEJO, Cita_Anterior=self.parts(5999)[0][0])
        with self.assertRaises(ValueError):
            self.load_doc(entry)

    def test_return_variants_do_not_assign_the_handoff_recipient(self):
        for p in [3071, 3575, 4109]:
            self.assertEqual(self.parts(p)[-1][1:], ('José De Gregorio Rebeco', 'LECTOR_DOCUMENTO_REVISADO'))
        for p in [5257, 5892, 5999]:
            self.assertEqual(self.parts(p)[-1][1:], ('Rodrigo Vergara Montes', 'LECTOR_DOCUMENTO_REVISADO'))

    def test_returning_reader_must_match_the_registered_reader(self):
        entry = copy.deepcopy(self.docs[3575])
        entry['_Tramos'][3] = entry['_Tramos'][3].replace('Presidente señor José De Gregorio', 'Consejero señor Rodrigo Vergara')
        with self.assertRaises(ValueError):
            b.segment_turns(self.raw[3575]['Texto'], self.raw[3575]['Fecha'], self.raw[3575]['Actor'], document=entry)

    def test_document_author_is_never_an_attendance_or_continuity_anchor(self):
        for p in DOCUMENTS:
            row = self.doc_rows(p)[2]
            self.assertEqual(row['Fuente_Rol'], 'CARGO_DOCUMENTAL_REVISADO')
            self.assertFalse(row['Rol_Lista_Asistencia'])
            self.assertFalse(row['ID_Ancla_Actor'])
            self.assertFalse(row['ID_Antecedente_Continuidad'])

    def test_repeated_announcements_and_returns_are_preserved(self):
        for i in [1, 3]:
            self.assertEqual(self.parts(3575)[i][0], self.parts(4109)[i][0])
        for p in [5892, 5999]:
            self.assertEqual(self.parts(p)[3][0], self.parts(5742)[3][0])

    def test_damage_warning_stays_on_the_document_not_the_reader(self):
        for i, (text, actor, method) in enumerate(self.parts(3071)):
            row = dict(ID_Padre=3071, Fecha=self.raw[3071]['Fecha'], Texto=text, Actor_Final=actor)
            self.assertEqual(bool(contextual_motives(row, self.warnings)), i == 2)
        text = self.parts(3071)[2][0]
        for literal in ['constituyó na', '0,1% ensual', 'escenario de onda']:
            self.assertIn(literal, text)

    def test_two_reviewed_links_do_not_merge_physical_texts(self):
        for key in LINKS:
            rows = self.pair(key)
            before = [(r['Texto'], r['Actor_Final']) for r in rows]
            annotate_turns(rows, {key: self.links[key]})
            self.assertEqual(before, [(r['Texto'], r['Actor_Final']) for r in rows])
            self.assertEqual(rows[0]['ID_Turno'], rows[1]['ID_Turno'])
            self.assertEqual(rows[1]['Relacion_Turno'], RELATION)
            self.assertFalse(rows[0]['ID_Ancla_Actor'])
            self.assertEqual(rows[1]['ID_Ancla_Actor'], rows[1]['ID_Intervencion'])
            self.assertFalse(validate_reviewed_links(rows, {key: self.links[key]}))

    def test_links_need_exact_review_not_global_context_inheritance(self):
        for key in LINKS:
            rows = self.pair(key)
            annotate_turns(rows)
            self.assertNotEqual(rows[0]['ID_Turno'], rows[1]['ID_Turno'])
            rows = self.pair(key)
            rows[0]['Texto'] += ' alterado'
            with self.assertRaises(ValueError):
                annotate_turns(rows, {key: self.links[key]})

    def test_links_leave_other_speakers_and_ocr_residues_untouched(self):
        for p, actor in [(4745, 'Claudio Soto Gamboa'), (6561, 'Joaquín Vial Ruiz-Tagle')]:
            self.assertEqual(self.parts(p)[0][1], actor)
            self.assertTrue(self.parts(p)[-1][0].endswith('A continuación,.'))
        self.assertIn('Sesión N° 184 Página 7 de 26', self.parts(4746)[0][0])
        self.assertIn('Quantiative Easing', self.parts(6562)[0][0])

    def test_link_hash_and_bounds_cannot_drift(self):
        for key in LINKS:
            for side in ['Anterior', 'Siguiente']:
                for field, value in [('SHA256_Texto_Padre', 'bad'), ('Inicio', -1)]:
                    entry = copy.deepcopy(self.links[key])
                    entry[side][field] = value
                    with tempfile.TemporaryDirectory() as d:
                        path = Path(d) / 'links.json'
                        path.write_text(json.dumps([entry]))
                        with self.assertRaises(ValueError):
                            load_reviewed_links(self.raw, path)

    def test_links_do_not_override_contextual_warning_barriers(self):
        for key in LINKS:
            rows = self.pair(key)
            rows[0]['Motivos_Revision'] = 'TEXTO_DANADO_POR_COTEJAR'
            with self.assertRaises(ValueError):
                annotate_turns(rows, {key: self.links[key]})

    def test_two_references_do_not_create_replies(self):
        for p in [5276, 5308]:
            self.assertEqual(len(self.parts(p)), 1)
            self.assertEqual(self.parts(p)[0][1], 'Rodrigo Vergara Montes')
            entry = next(e for e in self.mentions.values() if e['ID_Padre'] == p)
            row = dict(ID=1, ID_Padre=p, Fecha=self.raw[p]['Fecha'], Texto=self.parts(p)[0][0],
                Actor_Final='Rodrigo Vergara Montes', Motivos_Revision='')
            before = copy.deepcopy(row)
            errors, annotations = validate_mention_reviews([row], {entry['Revision_ID']: entry})
            self.assertFalse(errors)
            self.assertEqual(row, before)
            self.assertEqual(annotations[1]['Estado_Lectura_Dirigida'], 'MENCION_LEGITIMA_REVISADA')

    def test_lectura_in_economic_interpretation_is_not_a_document(self):
        self.assertEqual(len(self.parts(4096)), 7)
        self.assertNotIn(4096, self.docs)
        self.assertNotIn('DOCUMENTO_ESCRITO_REVISADO', [m for t, a, m in self.parts(4096)])

    def test_four_pending_readings_and_retired_archives_stay_distinct(self):
        self.assertEqual({e['ID_Padre'] for e in self.mentions.values() if e['Decision'] == 'PENDIENTE_DELIMITAR_APORTE'}, {6185, 3775, 4055, 2510})
        self.assertNotIn((5402, 5403), self.links)
        archive = json.loads((DOC_PATH.parent / 'alertas_contextuales_retiradas.json').read_text())
        self.assertEqual({e['Alerta_Original']['ID_Padre'] for e in archive}, {6443, 2704, 2661})

    def test_parent_3092_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3092]['Texto'].encode()).hexdigest(), 'fe0a559921472211e18aa9e6a31c2636258f094267976176950547a9478289d8')
        parts = self.parts(3092)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Manuel Marfán Lewis', 1272, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Vergara Montes', 136, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[3092]['Texto'].split()))

    def test_parent_4143_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4143]['Texto'].encode()).hexdigest(), '7941980cc1e5fd113aa7e807a4668437f67497d81958a4c25bdc96db61a92a56')
        parts = self.parts(4143)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Luis Óscar Herrera Barriga', 562, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 152, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[4143]['Texto'].split()))

    def test_parent_4778_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4778]['Texto'].encode()).hexdigest(), 'f7b011ffe8981c455a3dabc560f3dbaada90210a48d5880edecd9e9fd72e2d5c')
        parts = self.parts(4778)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Enrique Marshall Rivera', 312, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Vergara Montes', 218, 'CONTEXTO_REVISADO'), ('Consejo del Banco Central de Chile', 75, 'ACTA/META')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[4778]['Texto'].split()))

    def test_parent_3071_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3071]['Texto'].encode()).hexdigest(), 'b568e2b93660472ff2c5356701f764426fff11720b5fa3480d1c9c4adb7e68ea')
        parts = self.parts(3071)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('José De Gregorio Rebeco', 71, 'SUJETO_ROL_SESION'), ('José De Gregorio Rebeco', 217, 'LECTOR_DOCUMENTO_REVISADO'), ('Felipe Larraín Bascuñán', 2903, 'DOCUMENTO_ESCRITO_REVISADO'), ('José De Gregorio Rebeco', 115, 'LECTOR_DOCUMENTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[3071]['Texto'].split()))

    def test_parent_3575_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[3575]['Texto'].encode()).hexdigest(), 'aecdcd1b0e277b790d9ad96bfb245997eed3c78ae18df2bd260aae5bd0a24be9')
        parts = self.parts(3575)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('José De Gregorio Rebeco', 120, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 181, 'LECTOR_DOCUMENTO_REVISADO'), ('Felipe Larraín Bascuñán', 4212, 'DOCUMENTO_ESCRITO_REVISADO'), ('José De Gregorio Rebeco', 149, 'LECTOR_DOCUMENTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[3575]['Texto'].split()))

    def test_parent_4109_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4109]['Texto'].encode()).hexdigest(), 'bd9b16a982ee5f9350eb1040cac78f03a8f444b80fbb477409f6fb5ca210ba4b')
        parts = self.parts(4109)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('José De Gregorio Rebeco', 124, 'SUJETO_ROL_NOMBRE'), ('José De Gregorio Rebeco', 181, 'LECTOR_DOCUMENTO_REVISADO'), ('Felipe Larraín Bascuñán', 5788, 'DOCUMENTO_ESCRITO_REVISADO'), ('José De Gregorio Rebeco', 149, 'LECTOR_DOCUMENTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[4109]['Texto'].split()))

    def test_parent_5257_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5257]['Texto'].encode()).hexdigest(), '555fd680304efba8fe10596fe6458ec4a4e38845d54972fa42bfe251f53df712')
        parts = self.parts(5257)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Consejo del Banco Central de Chile', 79, 'ACTA/META'), ('Rodrigo Vergara Montes', 266, 'LECTOR_DOCUMENTO_REVISADO'), ('Felipe Larraín Bascuñán', 6205, 'DOCUMENTO_ESCRITO_REVISADO'), ('Rodrigo Vergara Montes', 265, 'LECTOR_DOCUMENTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[5257]['Texto'].split()))

    def test_parent_5892_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5892]['Texto'].encode()).hexdigest(), 'b82c31d2749fde953286cfb51fe4b4421c5ec324d8235dfc65303a4ca8080ac8')
        parts = self.parts(5892)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Rodrigo Vergara Montes', 123, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Vergara Montes', 387, 'LECTOR_DOCUMENTO_REVISADO'), ('Felipe Larraín Bascuñán', 3606, 'DOCUMENTO_ESCRITO_REVISADO'), ('Rodrigo Vergara Montes', 322, 'LECTOR_DOCUMENTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[5892]['Texto'].split()))

    def test_parent_5999_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5999]['Texto'].encode()).hexdigest(), '0ce3b33b2f42810e950a5bc1fba498e68260b7d78b042bd148e7ab31d079a33c')
        parts = self.parts(5999)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Rodrigo Vergara Montes', 132, 'SUJETO_ROL_NOMBRE'), ('Rodrigo Vergara Montes', 392, 'LECTOR_DOCUMENTO_REVISADO'), ('Felipe Larraín Bascuñán', 3441, 'DOCUMENTO_ESCRITO_REVISADO'), ('Rodrigo Vergara Montes', 322, 'LECTOR_DOCUMENTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[5999]['Texto'].split()))

    def test_parent_4745_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4745]['Texto'].encode()).hexdigest(), '0252c2442e6457a3d39674411a551523d97254e5979562c46cba155260b671d6')
        parts = self.parts(4745)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Claudio Soto Gamboa', 494, 'SUJETO_ROL_NOMBRE'), ('Sergio Lehmann Beresi', 597, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[4745]['Texto'].split()))

    def test_parent_4746_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4746]['Texto'].encode()).hexdigest(), '9e89343fcc0ac4b2ff9175b9c0d44a41968471a6daedf20137f3461b2d2089e4')
        parts = self.parts(4746)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Sergio Lehmann Beresi', 1877, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[4746]['Texto'].split()))

    def test_parent_6561_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[6561]['Texto'].encode()).hexdigest(), '6997135a713ec558fe41c0ce9d7272dc80d036ac2569619ea9e6bdb027a3c51c')
        parts = self.parts(6561)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Joaquín Vial Ruiz-Tagle', 1669, 'SUJETO_ROL_NOMBRE'), ('Miguel Fuentes Díaz', 4261, 'CONTEXTO_REVISADO')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[6561]['Texto'].split()))

    def test_parent_6562_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[6562]['Texto'].encode()).hexdigest(), '205a0a568c36ef6771eda7b4a35000cfc1752a63d060dc2421f4a76a862c6ea1')
        parts = self.parts(6562)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Miguel Fuentes Díaz', 875, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[6562]['Texto'].split()))

    def test_parent_4096_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[4096]['Texto'].encode()).hexdigest(), '5f4ff97d1bf62139df57fc62450655d2224118f57a85824a8baaa0a87cb42821')
        parts = self.parts(4096)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Claudio Soto Gamboa', 657, 'SUJETO_NOMBRE'), ('Kevin Cowan Logan', 150, 'SUJETO_ROL_SESION'), ('Claudio Soto Gamboa', 71, 'SUJETO_NOMBRE'), ('José De Gregorio Rebeco', 160, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 670, 'SUJETO_NOMBRE'), ('Rodrigo Vergara Montes', 224, 'SUJETO_ROL_NOMBRE'), ('Claudio Soto Gamboa', 1886, 'SUJETO_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[4096]['Texto'].split()))

    def test_parent_5276_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5276]['Texto'].encode()).hexdigest(), '9fafa2a8280a7f3178a62280247ac53558814572924942ad2a7ce3935570ed6e')
        parts = self.parts(5276)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Rodrigo Vergara Montes', 441, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[5276]['Texto'].split()))

    def test_parent_5308_source_signature_and_conservation(self):
        self.assertEqual(hashlib.sha256(self.raw[5308]['Texto'].encode()).hexdigest(), '7b6e51ffeddb51e55dd0af765d0ee5af53faf9d1dbc0db28c321d8befe3076e4')
        parts = self.parts(5308)
        self.assertEqual([(a, len(t), m) for t, a, m in parts], [('Rodrigo Vergara Montes', 1034, 'SUJETO_ROL_NOMBRE')])
        self.assertEqual(''.join(''.join(t.split()) for t, a, m in parts), ''.join(self.raw[5308]['Texto'].split()))

if __name__ == '__main__':
    unittest.main()
