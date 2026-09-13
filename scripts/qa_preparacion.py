"""F1: integridad, trazabilidad, proyección, duplicados y alertas de preparación.

No certifica exactitud semántica de cada atribución. Publica la cola de revisión
conservando las diferencias entre alertas y errores bloqueantes.
"""
import argparse
import collections
import csv
import hashlib
import importlib.metadata
import json
import platform
import re
from pathlib import Path

from review_queue import build_report
from context_warnings import load_context_warnings, validate_context_warnings, has_context_warning
from institutional_reviews import load_institutional_reviews, validate_institutional_reviews
from document_reviews import load_document_reviews, validate_document_reviews, FIELDS as DOCUMENT_FIELDS
from mention_reviews import load_mention_reviews, validate_mention_reviews, annotation_for, FIELDS as MENTION_FIELDS
from procedural import is_formula, load_formula_reviews
import openpyxl
import build_base_referencia as builder
from crear_consolidado_final import SOURCE_COLUMNS
from continuity import EXPLICIT, boundary, SECTION, normalize
from reviewed_continuity import load_reviewed_links, validate_reviewed_links, RELATION
from reviewed_intrapara_continuity import validate_intrapara_links, RELATION as INTRA_RELATION
from intrapara_profiles import load_intrapara_links, profile_name
from functional_refinements import active_refinements, refined_institutions, validate_refinements
import functional_refinements_v5 as functional_v5
from reviewed_procedural_v5 import (active_reviews as active_procedural, matching_review as matching_procedural,
                                    validate_reviews as validate_procedural, RELATION as PROCEDURAL_RELATION)
import os
from curation import load_role_reviews, REVIEW_SOURCES, load_speaker_reviews, validate_speaker_reviews, SPEAKER_REVIEW_SOURCE
from qa_gate_f0 import audit as audit_tpm, load_base, load_tpm

ROOT = Path(__file__).resolve().parents[1]


def read_rows(path):
    with path.open('rb') as fh:
        wb = openpyxl.load_workbook(fh, read_only=True, data_only=True)
        it = wb['Consolidado'].values
        header = next(it)
        rows = [dict(zip(header, row)) for row in it]
        wb.close()
    return header, rows


def compact(text):
    return re.sub(r'\s+', '', text or '')


def validate(rows, raw, full, final, role_reviews=None, procedural_reviews=None):
    role_reviews = role_reviews or {}
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    check(bool(rows), 'Base vacía')
    check([r['ID'] for r in rows] == list(range(1, len(rows)+1)), 'IDs no consecutivos/únicos')
    check(len({r['ID_Intervencion'] for r in rows}) == len(rows), 'Clave de intervención duplicada')
    raw_by_id = {r['ID']:r for r in raw}
    by_parent = collections.defaultdict(list)
    blocks = collections.defaultdict(list)
    exact = collections.Counter(r['Texto'] for r in rows)
    raw_exact = collections.Counter(r['Texto'] for r in raw)
    formula = is_formula
    for row in rows:
        rid = row['ID']
        parent = row['ID_Padre']
        by_parent[parent].append(row)
        blocks[row['ID_Bloque_Texto']].append(row)
        for field in ['ID','ID_Padre','Fecha','Id_Sesion','Actor_Final','Rol_Final','Texto',
                      'Fuente_Actor','Fuente_Rol','ID_Intervencion','ID_Bloque_Texto','Fuente_Texto','Estado_Revision']:
            check(row.get(field) not in (None,''), f'ID {rid}: vacío {field}')
        check(row['Actor_Final'] in set(builder.REAL) | {builder.CONSEJO}, f'ID {rid}: actor fuera de registro')
        check(row['Texto_Truncado'] == 'NO', f'ID {rid}: texto truncado/no revisado')
        check(len(row['Texto'] or '') <= 32767, f'ID {rid}: supera límite XLSX')
        check(row['Id_Sesion'] == 'RPM-'+builder.to_date_str(row['Fecha']), f'ID {rid}: sesión incorrecta')
        check(parent in raw_by_id, f'ID {rid}: padre inexistente')
        if parent not in raw_by_id:
            continue
        source = raw_by_id[parent]
        check(row['Fecha'] == source['Fecha'], f'ID {rid}: fecha distinta del padre')
        check(row['Página'] == source['Pagina'], f'ID {rid}: página de origen distinta')
        check(row['Duplicado_Exacto'] == ('SI' if exact[row['Texto']]>1 else 'NO'), f'ID {rid}: duplicado incorrecto')
        check(row['Duplicado_Formula'] == ('SI' if exact[row['Texto']]>1 and formula(row['Texto']) else 'NO'), f'ID {rid}: fórmula incorrecta')
        check(row['Duplicado_Exacto_Origen'] == ('SI' if raw_exact[source['Texto']]>1 else 'NO'), f'ID {rid}: duplicado origen incorrecto')
        if row['Fuente_Rol'] in REVIEW_SOURCES:
            review = role_reviews.get((parent,row['Actor_Final']))
            check(bool(review and review['Rol']==row['Rol_Final'] and review['Fuente_Rol']==row['Fuente_Rol']),
                  f'ID {rid}: cargo revisado sin evidencia aplicable')
        if row['Fuente_Rol'] == 'LISTA_ASISTENCIA':
            check(row['Rol_Final'] == builder.roster_role_for(builder.to_date_str(row['Fecha']), row['Actor_Final']), f'ID {rid}: cargo no coincide con asistencia')
        for original, category in [('Tema_Original','Tema_Categoria'),('Palabra_Clave_Original','Palabra_Clave_Categoria')]:
            check(row[category] == builder.cat(row[original]), f'ID {rid}: categoría no reproducible')
        check((row['Estado_Revision']=='PENDIENTE_REVISION') == bool(row['Motivos_Revision']), f'ID {rid}: estado/alertas inconsistentes')
    check(set(by_parent) == set(raw_by_id), 'No se preservan todos los padres')
    for parent, group in by_parent.items():
        if parent not in raw_by_id:
            continue
        source = full.get(parent,{}).get('Texto_Completo', raw_by_id[parent]['Texto'])
        check(compact(''.join(r['Texto'] for r in group)) == compact(source), f'Padre {parent}: pérdida/alteración de texto')
        check([r['Numero_Segmento'] for r in group] == list(range(1,len(group)+1)), f'Padre {parent}: orden de segmentos')
    for block, group in blocks.items():
        check(len({r['Actor_Final'] for r in group}) == 1, f'Bloque {block}: más de un actor')
        if len(group)>1:
            check(all(r['Fuente_Actor']=='CONTINUACION_XLSX' for r in group[1:]), f'Bloque {block}: fracciones sin marcar')
    errors.extend(validate_continuity(rows,procedural_reviews))
    check(len(final)==len(rows), 'Base final: cardinalidad distinta')
    check(all({k:r[k] for k in SOURCE_COLUMNS} == f for r,f in zip(rows,final)), 'Base final: proyección distinta')
    return errors


def validate_continuity(rows,procedural_reviews=None):
    """Verifica eslabones de continuidad: orden, identidad, sesión y ancla."""
    errors = []
    by_id = {r['ID_Intervencion']:r for r in rows}
    closed = set()
    previous = None
    for row in rows:
        rid = row['ID']
        turn = row.get('ID_Turno')
        if not turn or not row.get('Relacion_Turno'):
            errors.append(f'ID {rid}: falta identificación de turno')
        if previous and previous.get('ID_Turno') != turn:
            closed.add(previous.get('ID_Turno'))
        if turn in closed:
            errors.append(f'ID {rid}: turno no contiguo')
        antecedent = row.get('ID_Antecedente_Continuidad')
        anchor = row.get('ID_Ancla_Actor')
        procedural = matching_procedural(previous,row,procedural_reviews)
        if antecedent:
            if not previous or antecedent != previous['ID_Intervencion']:
                errors.append(f'ID {rid}: antecedente no es la fila previa')
            elif (previous['Actor_Final'] != row['Actor_Final'] or previous['Fecha'] != row['Fecha']
                  or previous['ID_Turno'] != turn):
                errors.append(f'ID {rid}: continuidad cruza actor/sesión/turno')
            elif (previous['Actor_Final'] == builder.CONSEJO or previous.get('Tipo_Acta')
                  or (boundary(previous['Texto']) and not (procedural and row.get('Relacion_Turno')==PROCEDURAL_RELATION)) or
                  'POSIBLE_OTRO_HABLANTE_O_MENCION' in (previous.get('Motivos_Revision') or '') or
                  has_context_warning(previous.get('Motivos_Revision'))):
                errors.append(f'ID {rid}: continuidad atraviesa barrera')
        elif previous and previous.get('ID_Turno') == turn:
            errors.append(f'ID {rid}: turno compartido sin antecedente')
        if row.get('Relacion_Turno') in (RELATION, INTRA_RELATION) and (row.get('Tipo_Acta')
                or SECTION.search(normalize(row['Texto']))
                or has_context_warning(row.get('Motivos_Revision'))
                or 'POSIBLE_OTRO_HABLANTE_O_MENCION' in (row.get('Motivos_Revision') or '')):
            errors.append(f'ID {rid}: continuidad revisada atraviesa barrera actual')
        if anchor:
            root = by_id.get(anchor)
            if (not root or root['ID'] > rid or root['Actor_Final'] != row['Actor_Final']
                or root['Fecha'] != row['Fecha'] or root['Fuente_Actor'] not in EXPLICIT
                or root['ID_Turno'] != turn):
                errors.append(f'ID {rid}: ancla de actor inválida')
        if row['Fuente_Actor'] in ('CONTINUIDAD_PARRAFO','ANAFORA_CONTINUIDAD') and (not anchor or not antecedent):
            errors.append(f'ID {rid}: herencia de actor sin cadena de evidencia')
        previous = row
    errors.extend(validate_procedural(rows,procedural_reviews or {}))
    return errors


def write_csv(path, rows, fields):
    with path.open('w', encoding='utf-8-sig', newline='') as fh:
        writer=csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--processed', type=Path, default=builder.DATA_PROC)
    args=parser.parse_args()
    out=args.processed
    header, rows=read_rows(out/'consolidado_base_referencia.xlsx')
    final_header, final=read_rows(out/'consolidado_base_referencia_final.xlsx')
    _, raw=read_rows(ROOT/'data/raw/consolidado_final.xlsx')
    full=builder.load_full_texts(out/'textos_completos.jsonl')
    load_formula_reviews(raw_by_id={r["ID"]:r for r in raw})
    role_reviews=load_role_reviews({r['ID']:r for r in raw})
    procedural=active_procedural({r["ID"]:r for r in raw})
    errors=validate(rows,raw,full,final,role_reviews,procedural)
    speaker_reviews=load_speaker_reviews({r["ID"]:r for r in raw})
    errors.extend(validate_speaker_reviews(rows,speaker_reviews))
    reviewed_links=load_reviewed_links({r["ID"]:r for r in raw})
    errors.extend(validate_reviewed_links(rows,reviewed_links))
    intra_path = os.environ.get('NLM_INTRAPARA_REVIEWS')
    intrapara_links = load_intrapara_links({r['ID']:r for r in raw}, intra_path) if intra_path else {}
    errors.extend(validate_intrapara_links(rows, intrapara_links))
    mention_reviews=load_mention_reviews({r["ID"]:r for r in raw})
    mention_errors, mention_annotations=validate_mention_reviews(rows,mention_reviews)
    errors.extend(mention_errors)
    documents=load_document_reviews({r['ID']:r for r in raw})
    document_errors, document_records=validate_document_reviews(rows,documents)
    errors.extend(document_errors)
    institutions=load_institutional_reviews({r['ID']:r for r in raw})
    functional_path = os.environ.get('NLM_FUNCTIONAL_REVIEWS')
    functional = active_refinements({r['ID']:r for r in raw})
    # v5 extiende el mismo criterio a 29 padres; se valida con su propio comparador.
    refinements_v5 = functional_v5.active_refinements({r['ID']:r for r in raw})
    perfil = os.environ.get('NLM_PERFIL_CONSTRUCCION')
    if refinements_v5:
        from compare_functional_v7 import compare as compare_v7, BASE as BASE_V6
        compare_v7(read_rows(BASE_V6)[1],rows,refinements_v5)
    if procedural:
        # v6 se compara contra la entrega v5; los perfiles históricos contra v4.
        if perfil == 'procedimental-v6':
            from compare_procedural_v6 import BASE as BASE_V5, verify
            verify(read_rows(BASE_V5)[1], rows)
        elif perfil != 'procedimental-v7':
            from compare_procedural_v5 import compare, BASE
            compare(read_rows(BASE)[1],rows)
    elif functional:
        from compare_functional_v4 import compare, BASE
        compare(read_rows(BASE)[1],rows,functional)
    errors.extend(validate_institutional_reviews(rows,refined_institutions(institutions,functional)))
    errors.extend(validate_refinements(rows,functional))
    errors.extend(functional_v5.validate_refinements(rows,refinements_v5))
    context_alerts=load_context_warnings({r['ID']:r for r in raw})
    errors.extend(validate_context_warnings(rows,context_alerts))
    for (parent,actor),review in role_reviews.items():
        if not any(r['ID_Padre']==parent and r['Actor_Final']==actor and r['Rol_Final']==review['Rol'] for r in rows):
            errors.append(f'{review["Revision_ID"]}: revisión ya no aplica a la salida')
    if list(final_header)!=SOURCE_COLUMNS:
        errors.append('Esquema final distinto al esperado')
    tpm=audit_tpm(load_base(out/'consolidado_base_referencia.xlsx'), load_tpm(ROOT/'data/external/tpm_oficial_bcch.csv'))
    errors.extend(tpm['errores'])
    reasons=collections.Counter(reason for r in rows for reason in (r['Motivos_Revision'] or '').split(';') if reason)
    pending=[r for r in rows if r['Estado_Revision']=='PENDIENTE_REVISION']
    report={
        'pasa_controles_bloqueantes': not errors, 'errores': errors,
        'estado_semantico': 'REQUIERE_REVISION_DIRIGIDA; no certifica pureza total de hablante',
        'filas_originales':len(raw), 'filas_procesadas':len(rows),
        'bloques_texto':len({r['ID_Bloque_Texto'] for r in rows}),
        'grupos_turno':len({r['ID_Turno'] for r in rows}),
        'relaciones_turno':dict(collections.Counter(r['Relacion_Turno'] for r in rows)),
        'grupos_multiparrafo':sum(n>1 for n in collections.Counter(r['ID_Turno'] for r in rows).values()),
        'max_filas_por_turno':max(collections.Counter(r['ID_Turno'] for r in rows).values()),
        'columnas_auditoria':len(header), 'columnas_final':len(final_header),
        'sesiones':len({r['Fecha'] for r in rows}), 'actores':len({r['Actor_Final'] for r in rows}),
        'padres_con_texto_conservado': len(raw)-sum('pérdida/alteración de texto' in e for e in errors),
        'filas_origen_divididas':sum(n>1 for n in collections.Counter(r['ID_Padre'] for r in rows).values()),
        'palabras':sum(len(r['Texto'].split()) for r in rows),
        'max_caracteres_celda':max(len(r['Texto']) for r in rows),
        'fuente_actor':dict(collections.Counter(r['Fuente_Actor'] for r in rows)),
        'fuente_rol':dict(collections.Counter(r['Fuente_Rol'] for r in rows)),
        'alertas_contextuales_documentadas':len(context_alerts),
        'documentos_escritos_revisados':len(document_records),
        'menciones_actuales_documentadas':len(mention_annotations),
        'lecturas_actuales_por_estado':dict(collections.Counter(e['Estado_Lectura_Dirigida'] for e in mention_annotations.values())),
        'continuidades_hablantes_revisadas':len(reviewed_links),
        'continuidades_intrapadre_revisadas':len(intrapara_links),
        'hablantes_revision_documentada':sum(r['Fuente_Actor']==SPEAKER_REVIEW_SOURCE for r in rows),
        'cargos_revision_documentada':sum(r['Fuente_Rol'] in REVIEW_SOURCES for r in rows),
        'tipos_acta':dict(collections.Counter(r['Tipo_Acta'] or 'INTERVENCION_SIN_TIPO_INSTITUCIONAL' for r in rows)),
        'categorias_tema':dict(collections.Counter(r['Tema_Categoria'] for r in rows)),
        'categorias_palabra_clave':dict(collections.Counter(r['Palabra_Clave_Categoria'] for r in rows)),
        'duplicados_exactos':sum(r['Duplicado_Exacto']=='SI' for r in rows),
        'duplicados_formula':sum(r['Duplicado_Formula']=='SI' for r in rows),
        'filas_con_alertas':len(pending), 'alertas_por_motivo':dict(reasons),
        'f0':{k:v for k,v in tpm.items() if k!='decisiones'},
        'formulas_tpm_contrastadas':sum(d['Formulas_Contrastadas'] for d in tpm['decisiones']),
        'nota': 'Las alertas se superponen; no son un conteo de errores. Página y etiquetas temáticas se heredan del padre. La conservación compara caracteres ignorando sólo espacios.'
    }
    if procedural:
        report['continuidades_procedimentales_revisadas']=len(procedural)
    if functional:
        # El resumen cuenta ambos refinamientos; v5 no puede quedar invisible.
        report['refinamientos_funcionales']=len(functional)+len(refinements_v5)
        report['continuidades_personales_funcionales']=len(functional)+len(refinements_v5)
        if refinements_v5:
            report['refinamientos_funcionales_v4']=len(functional)
            report['refinamientos_funcionales_v5']=len(refinements_v5)
    (out/'qa_preparacion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fields=['ID','ID_Intervencion','ID_Padre','Fecha','Actor_Final','Rol_Final','Fuente_Actor','Fuente_Rol',
            'Motivos_Revision','ID_Turno','Relacion_Turno','ID_Antecedente_Continuidad','ID_Ancla_Actor',
            'ID_Anterior','Actor_Anterior','Final_Anterior','Extracto','Evidencia_Alerta',
            'ID_Siguiente','Actor_Siguiente','Inicio_Siguiente'] + list(MENTION_FIELDS)
    queue=[]
    for i,r in enumerate(rows):
        if r['Estado_Revision']!='PENDIENTE_REVISION':
            continue
        item={k:r[k] for k in fields[:13]}
        prev=rows[i-1] if i and rows[i-1]['Fecha']==r['Fecha'] else {}
        following=rows[i+1] if i+1<len(rows) and rows[i+1]['Fecha']==r['Fecha'] else {}
        evidence=''
        if 'POSIBLE_OTRO_HABLANTE_O_MENCION' in (r['Motivos_Revision'] or ''):
            for a,b in builder.split_sentences(r['Texto']):
                sent=r['Texto'][a:b]
                if any(c['actor']!=r['Actor_Final'] for c in builder.TURN_DETECTOR.candidates(
                        sent,builder.to_date_str(r['Fecha']),r['Actor_Final'],allow_embedded=True)):
                    evidence=sent[:650]
                    break
        item.update(ID_Anterior=prev.get('ID_Intervencion',''),Actor_Anterior=prev.get('Actor_Final',''),
                    Final_Anterior=(prev.get('Texto') or '')[-350:],Extracto=r['Texto'][:350],
                    Evidencia_Alerta=evidence,ID_Siguiente=following.get('ID_Intervencion',''),
                    Actor_Siguiente=following.get('Actor_Final',''),Inicio_Siguiente=(following.get('Texto') or '')[:350])
        item.update(annotation_for(r,mention_annotations))
        queue.append(item)
    write_csv(out/'revision_pendientes.csv',queue,fields)
    write_csv(out/'documentos_leidos.csv',document_records,DOCUMENT_FIELDS)
    grouped=collections.defaultdict(list)
    for r in rows:
        grouped[r['ID_Turno']].append(r)
    documents_by_turn={r['ID_Turno']:r for r in document_records}
    turns=[{'ID_Turno':key,'Fecha':group[0]['Fecha'],'Actor_Final':group[0]['Actor_Final'],
            'Naturaleza_Turno':('ESCRITO_LEIDO_POR_TERCERO' if key in documents_by_turn else
                ('DOCUMENTO_PERSONAL' if group[0]['Relacion_Turno']=='DOCUMENTO_PERSONAL' else
                ('INSTITUCIONAL' if group[0]['Relacion_Turno']=='INSTITUCIONAL' else 'INTERVENCION'))),
            'Lector_Documento':documents_by_turn.get(key,{}).get('Lector',''),
            'ID_Desde':group[0]['ID'],'ID_Hasta':group[-1]['ID'],'Numero_Filas':len(group),
            'Padres':';'.join(map(str,dict.fromkeys(r['ID_Padre'] for r in group))),
            'Filas_Con_Alertas':sum(r['Estado_Revision']=='PENDIENTE_REVISION' for r in group),
            'Palabras':sum(len(r['Texto'].split()) for r in group)} for key,group in grouped.items()]
    write_csv(out/'turnos_habla.csv',turns,['ID_Turno','Fecha','Actor_Final','ID_Desde','ID_Hasta',
                                        'Numero_Filas','Padres','Filas_Con_Alertas','Palabras','Naturaleza_Turno','Lector_Documento'])
    decisions=[{**d,'IDs_Evidencia':';'.join(map(str,d['IDs_Evidencia']))} for d in tpm['decisiones']]
    write_csv(out/'decisiones_tpm.csv',decisions,['Fecha','Tasa_Antes','Tasa_Despues','Delta_PB','IDs_Evidencia','Formulas_Contrastadas'])
    build_report(rows,out,speaker_reviews,mention_annotations)
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()
    files=sorted((ROOT/'data/raw').glob('*'))+sorted((ROOT/'data/external').glob('*'))+sorted((ROOT/'data/curation').glob('*.json'))+sorted((ROOT/'scripts').glob('*.py'))+sorted((ROOT/'tests').glob('*.py'))+[ROOT/'requirements.txt']
    manifest={'python':platform.python_version(),'dependencias':{name:importlib.metadata.version(name) for name in ['openpyxl','pypdf']},
              'sha256_entradas_codigo':{str(p.relative_to(ROOT)):digest(p) for p in files},
              'sha256_salidas':{p.name:digest(p) for p in sorted(out.iterdir()) if p.is_file() and p.name!='manifiesto_preparacion.json'}}
    manifest['perfil_continuidad'] = profile_name(intra_path) if intra_path else 'legacy'
    if functional_path:
        manifest['perfil_entrega'] = 'funcional-v4'
        manifest['pruebas_funcionales'] = {'archivo': str(Path(functional_path).resolve().relative_to(ROOT)), 'sha256': digest(Path(functional_path)), 'refinamientos': len(functional)}
    if refinements_v5:
        # Sin esto el manifiesto no registraba el registro que produjo 29 de los 32 cortes.
        p5 = Path(os.environ['NLM_FUNCTIONAL_V5_REVIEWS'])
        manifest['pruebas_funcionales_v5'] = {
            'archivo': str(p5.resolve().relative_to(ROOT)), 'sha256': digest(p5),
            'refinamientos': len(refinements_v5),
            'lecturas': str(functional_v5.READINGS.relative_to(ROOT)),
            'sha256_lecturas': digest(functional_v5.READINGS),
            'base': str(functional_v5.BASE.relative_to(ROOT)),
            'sha256_base': functional_v5.BASE_SHA}
    if procedural:
        manifest['perfil_entrega'] = os.environ.get('NLM_PERFIL_CONSTRUCCION') or 'procedimental-v5'
        pp=Path(os.environ['NLM_PROCEDURAL_REVIEWS'])
        manifest['pruebas_procedimentales'] = {'archivo':str(pp.resolve().relative_to(ROOT)), 'sha256':digest(pp), 'enlaces':len(procedural)}
    if intra_path:
        manifest['pruebas_intrapadre'] = {'archivo': str(Path(intra_path).resolve().relative_to(ROOT)), 'sha256': digest(Path(intra_path))}
    (out/'manifiesto_preparacion.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return int(bool(errors))


if __name__=='__main__':
    raise SystemExit(main())
