"""Cubre el puntaje hawkish/dovish, la muestra sorteada, las etiquetas oro y el modelo.

Cada prueba ejecuta el código que se entrega: el léxico, el join turno/texto, el
sorteo estratificado, el validador de etiquetas y el clasificador entrenado,
incluida la reproducción de los puntajes publicados desde el JSON del modelo.
"""
import csv
import json
import math
import random
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import hawkish_dovish as hd
import entrenar_hawkish_dovish as ent
import etiquetar_hawkish_dovish as etq
import diagnosticar_fallos_hawkish_dovish as diag
import validar_ensemble_hawkish_dovish as ens
import estimar_prevalencia_hawkish_dovish as prev
import medir_ruido_oro_hawkish_dovish as ruido
import auditar_hawkish_dovish as aud
import medir_efecto_ventana_hawkish_dovish as ven
import contrastar_lexico_publicado_hawkish_dovish as lexpub

RELEASE = ROOT / 'data/releases/hawkish_dovish_v1'
PUNTAJES_AUD = RELEASE / 'puntajes_hawkish_dovish.csv'
DOCS = ROOT / 'docs'
ETIQUETAS = ROOT / 'data/curation/hawkish_dovish_etiquetas_v1.json'
from collections import defaultdict  # noqa: E402


class LexicoTests(unittest.TestCase):
    def test_direccion_hawkish_y_dovish(self):
        hawk = hd.puntuar_lexico('Hay presiones inflacionarias y exceso de demanda, '
                                 'las holguras se han reducido y corresponde subir la tasa.')
        dove = hd.puntuar_lexico('Quedan holguras de capacidad amplias, la inflación '
                                 'está bajo la meta y es transitoria; habría que bajar la tasa.')
        neutro = hd.puntuar_lexico('El Gerente da cuenta de los antecedentes de la reunión.')
        self.assertGreater(hawk['score'], 0.3)
        self.assertEqual(hd.clase(hawk['score']), 'HAWKISH')
        self.assertLess(dove['score'], -0.3)
        self.assertEqual(hd.clase(dove['score']), 'DOVISH')
        self.assertEqual(neutro['score'], 0.0)
        self.assertEqual(hd.clase(0.0), 'NEUTRAL')

    def test_negacion_descuenta_la_locucion(self):
        afirmado = hd.puntuar_lexico('Corresponde subir la tasa de política.')
        negado = hd.puntuar_lexico('No corresponde subir la tasa de política.')
        self.assertGreater(afirmado['peso_hawkish'], negado['peso_hawkish'])
        self.assertLess(negado['peso_hawkish'], 0)

    def test_score_acotado_y_evidencia(self):
        r = hd.puntuar_lexico('Presiones inflacionarias, presiones inflacionarias, '
                              'presiones inflacionarias y sobrecalentamiento de la economía.')
        self.assertLessEqual(abs(r['score']), 1.0)
        self.assertTrue(r['hits_hawkish'])
        self.assertIn('sobrecalentamiento', [h for h, _ in r['hits_hawkish']])

    def test_grupo_actor(self):
        # Presidente y Vicepresidente votan: no pueden caer en el grupo del staff
        self.assertEqual(hd.grupo_actor('Presidente del Banco Central'), 'CONSEJO')
        self.assertEqual(hd.grupo_actor('Vicepresidente del Banco Central'), 'CONSEJO')
        self.assertEqual(hd.grupo_actor('Consejero'), 'CONSEJO')
        self.assertEqual(hd.grupo_actor('Consejo'), 'CONSEJO')
        self.assertEqual(hd.grupo_actor('Ministro de Hacienda'), 'HACIENDA')
        self.assertEqual(hd.grupo_actor('Asesor del Ministerio de Hacienda'), 'HACIENDA')
        self.assertEqual(hd.grupo_actor('Gerente de División Estudios'), 'STAFF')
        self.assertEqual(hd.grupo_actor('Gerente General'), 'STAFF')


class TurnosTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.turnos = hd.cargar_turnos()

    def test_join_turno_texto(self):
        self.assertEqual(len(self.turnos), 9257)
        for t in self.turnos:
            self.assertEqual(len(t['Texto'].split()), t['Palabras'])
            self.assertEqual(len(t['SHA256_Texto']), 64)

    def test_universo_etiquetable(self):
        univ = hd.universo(self.turnos)
        self.assertEqual(len(univ), 2789)
        self.assertTrue(all(t['Naturaleza_Turno'] == 'INTERVENCION' for t in univ))
        self.assertTrue(all(t['Palabras'] >= hd.MIN_PALABRAS_UNIVERSO for t in univ))


class MuestraTests(unittest.TestCase):
    def test_muestra_500_determinista_y_estratificada(self):
        turnos = hd.cargar_turnos()
        a, pool = hd.muestra(turnos, n=500)
        b, _ = hd.muestra(turnos, n=500)
        self.assertEqual(len(a), 500)
        self.assertEqual([t['ID_Turno'] for t in a], [t['ID_Turno'] for t in b])
        self.assertEqual(len({t['ID_Turno'] for t in a}), 500)
        deciles = Counter(t['Decile_Lex'] for t in a)
        self.assertEqual(sorted(deciles), list(range(1, 11)))
        self.assertEqual(sum(deciles.values()), 500)
        # los extremos del espectro léxico llevan más cupo que el centro
        self.assertEqual(deciles[1], deciles[10])
        self.assertEqual(deciles[5], deciles[6])
        self.assertGreater(deciles[1], deciles[5])
        self.assertTrue(all(t['Palabras'] >= hd.MIN_PALABRAS_UNIVERSO for t in a))
        self.assertTrue(all(t['Naturaleza_Turno'] == 'INTERVENCION' for t in a))
        self.assertEqual(len(pool), 2789)

    def test_las_etiquetas_previas_entran_en_la_muestra(self):
        paquete = json.loads((hd.CURATION / 'hawkish_dovish_etiquetas_v1.json').read_text(encoding='utf-8'))
        forzar = [e['ID_Turno'] for e in paquete['Etiquetas']]
        turnos = hd.cargar_turnos()
        elegidos, _ = hd.muestra(turnos, n=500, forzar=forzar)
        ids = {t['ID_Turno'] for t in elegidos}
        self.assertEqual(len(ids), 500)
        self.assertEqual(set(forzar) - ids, set())
        self.assertEqual(sum(1 for t in elegidos if t['Forzada']), len(forzar))

    def test_csv_publicado_coincide_con_la_muestra(self):
        filas, _ = etq.cargar_muestra()
        self.assertEqual(len(filas), 500)
        self.assertEqual(len({r['ID_Turno'] for r in filas}), 500)


class EtiquetasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.muestra, cls.campos = etq.cargar_muestra()
        cls.paquete = json.loads(etq.ETIQUETAS.read_text(encoding='utf-8'))

    def test_todas_las_etiquetas_validan_sin_errores(self):
        validas, errores, fuera = etq.validar(self.paquete, self.muestra)
        self.assertEqual(errores, [])
        self.assertEqual(fuera, [])
        n = len(self.paquete['Etiquetas'])
        self.assertEqual(len(validas), n)
        self.assertEqual({v['ID_Turno'] for v in validas},
                         {e['ID_Turno'] for e in self.paquete['Etiquetas']})
        # la muestra vigente conserva todas las intervenciones ya leídas
        self.assertEqual(sum(1 for r in self.muestra if r['Etiqueta_Previa'] == 'SI'), n)
        self.assertEqual(sum(1 for r in self.muestra if r['HD_Clase_Oro']), n)

    def test_cobertura_recalculada_no_declarada(self):
        validas = etq.validar(self.paquete, self.muestra)[0]
        por_lote = {int(r['Lote']): r for r in self.muestra}
        for v in validas:
            esperado = etq.chars_leidos(por_lote[v['Lote']]['Texto'])
            self.assertEqual(v['Chars_Leidos'], esperado)
            self.assertLessEqual(v['Cobertura'], 1.0)
            self.assertGreater(v['Cobertura'], 0.0)

    def test_rechaza_clase_incoherente_y_evidencia_falsa(self):
        falso = json.loads(json.dumps(self.paquete))
        falso['Etiquetas'][0]['HD_Clase'] = 'DOVISH'
        falso['Etiquetas'][1]['Evidencia'] = 'esta cita no existe en el acta'
        _, errores, _ = etq.validar(falso, self.muestra)
        self.assertTrue(any('incoherente' in e for e in errores))
        self.assertTrue(any('no aparece en el texto' in e for e in errores))

    def test_rechaza_duplicados_y_turnos_ajenos(self):
        falso = json.loads(json.dumps(self.paquete))
        falso['Etiquetas'][1]['ID_Turno'] = falso['Etiquetas'][0]['ID_Turno']
        _, errores, _ = etq.validar(falso, self.muestra)
        self.assertTrue(any('duplicados' in e for e in errores))

        ajeno = json.loads(json.dumps(self.paquete))
        ajeno['Etiquetas'][0]['ID_Turno'] = 'RPM-2005-01-11:T1'   # institucional, fuera del universo
        validas, _, fuera = etq.validar(ajeno, self.muestra)
        self.assertIn('RPM-2005-01-11:T1', fuera)
        self.assertEqual(len(validas), len(self.paquete['Etiquetas']) - 1)


class TokenizadorTests(unittest.TestCase):
    def test_tokens_y_bigramas(self):
        cuenta = ent.rasgos_texto('El señor Consejero señala que hay presiones inflacionarias.')
        self.assertIn('presiones', cuenta)
        self.assertIn('presiones inflacionarias', cuenta)
        self.assertNotIn('señor', cuenta)          # stopword del corpus
        self.assertNotIn('que', cuenta)
        self.assertEqual(cuenta['presiones'], 1)

    def test_seleccion_respeta_df_minimo_y_descarta_los_ubiguos(self):
        docs = [Counter({'a': 2, 'b': 1, 'z': 1}), Counter({'a': 1, 'c': 1, 'z': 1}),
                Counter({'a': 1, 'd': 1, 'z': 1}), Counter({'e': 1, 'z': 1}),
                Counter({'f': 1, 'z': 1}), Counter({'g': 1, 'z': 1})]
        y = ['HAWKISH', 'DOVISH', 'NEUTRAL', 'HAWKISH', 'DOVISH', 'NEUTRAL']
        sel = ent.seleccionar(docs, y, max_rasgos=10, min_df=2)
        self.assertIn('a', sel)                 # df=3, discriminativo
        self.assertNotIn('b', sel)              # df=1, bajo el mínimo
        self.assertNotIn('z', sel)              # en el 100% de los documentos


class ModeloTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.muestra, _ = etq.cargar_muestra()
        cls.oro = [r for r in cls.muestra if r['HD_Clase_Oro']]
        cls.cuentas = [ent.rasgos_texto(r['Texto']) for r in cls.oro]
        cls.y = [r['HD_Clase_Oro'] for r in cls.oro]
        cls.vocab = ent.seleccionar(cls.cuentas, cls.y, 120)
        cls.idf = ent.idf_de(cls.cuentas, cls.vocab)
        cls.X = ent.vectorizar(cls.cuentas, cls.vocab, cls.idf)
        cls.modelo = ent.entrenar(cls.X, cls.y, iteraciones=25, p=len(cls.vocab))

    def test_probabilidades_normalizadas(self):
        pred = ent.predecir(self.modelo, self.X[0])
        self.assertAlmostEqual(sum(pred['probs']), 1.0, places=6)
        self.assertIn(pred['clase'], ent.CLASES)
        self.assertGreaterEqual(pred['margen'], 0.0)
        self.assertLessEqual(abs(pred['score']), 1.0)

    def test_documento_vacio_no_rompe(self):
        pred = ent.predecir(self.modelo, {})
        self.assertAlmostEqual(sum(pred['probs']), 1.0, places=6)

    def test_aprende_un_patron_separable(self):
        docs = [Counter({'alza': 3, 'tasa': 2}) for _ in range(6)] + \
               [Counter({'holgura': 3, 'baja': 2}) for _ in range(6)]
        y = ['HAWKISH'] * 6 + ['DOVISH'] * 6
        vocab = ent.seleccionar(docs, y, 10, min_df=2)
        X = ent.vectorizar(docs, vocab, ent.idf_de(docs, vocab))
        m = ent.entrenar(X, y, iteraciones=40, p=len(vocab))
        predichas = [ent.predecir(m, d)['clase'] for d in X]
        self.assertEqual(predichas, y)

    def test_validacion_cruzada_supera_a_la_mayoria(self):
        m = ent.validacion_cruzada(self.cuentas, self.y,
                                   [r['HD_Score_Oro'] for r in self.oro],
                                   [r['Lex_Score'] for r in self.oro],
                                   max_rasgos=150, iteraciones=20, k=5)
        self.assertGreater(m['macro_f1'], m['baseline_mayoria']['macro_f1'])
        self.assertEqual(m['predicciones_fuera_de_pliegue'], len(self.oro))


class PublicacionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(RELEASE / 'puntajes_hawkish_dovish.csv', encoding='utf-8') as f:
            cls.puntajes = list(csv.DictReader(f))
        cls.modelo = json.loads((RELEASE / 'modelo_hawkish_dovish.json').read_text(encoding='utf-8'))
        cls.resumen = json.loads((RELEASE / 'resumen_entrenamiento.json').read_text(encoding='utf-8'))

    def test_cobertura_de_turnos(self):
        self.assertEqual(len(self.puntajes), 9257)
        self.assertEqual(len({r['ID_Turno'] for r in self.puntajes}), 9257)
        self.assertEqual(sum(1 for r in self.puntajes if r['En_Universo_Entrenado'] == 'true'), 2789)
        self.assertEqual(sum(1 for r in self.puntajes if r['En_Muestra_500'] == 'true'), 500)
        with open(etq.ETIQUETAS, encoding='utf-8') as f:
            n_oro = len(json.load(f)['Etiquetas'])
        self.assertEqual(sum(1 for r in self.puntajes if r['HD_Clase_Oro']), n_oro)

    def test_el_json_del_modelo_reproduce_los_puntajes_publicados(self):
        muestra, _ = etq.cargar_muestra()
        texto = {r['ID_Turno']: r['Texto'] for r in muestra}
        modelo = {'W': self.modelo['pesos'], 'b': self.modelo['sesgo']}
        indice = {t: i for i, t in enumerate(self.modelo['vocabulario'])}
        idf = self.modelo['idf']
        revisados = 0
        for r in self.puntajes:
            if r['ID_Turno'] not in texto:
                continue
            cuenta = ent.rasgos_texto(texto[r['ID_Turno']])
            v = {indice[t]: (1 + math.log(tf)) * idf[indice[t]]
                 for t, tf in cuenta.items() if t in indice}
            norma = math.sqrt(sum(w * w for w in v.values())) or 1.0
            pred = ent.predecir(modelo, {i: w / norma for i, w in v.items()})
            self.assertEqual(pred['clase'], r['HD_Clase_Modelo'], r['ID_Turno'])
            self.assertAlmostEqual(pred['score'], float(r['HD_Score_Modelo']), places=3,
                                   msg=r['ID_Turno'])
            revisados += 1
        # toda la muestra de 500 aparece en la publicación: se reproduce completa
        self.assertEqual(revisados, 500)

    def test_metricas_publicadas_coherentes(self):
        cv = self.resumen['validacion_cruzada']
        with open(etq.ETIQUETAS, encoding='utf-8') as f:
            n_oro = len(json.load(f)['Etiquetas'])
        self.assertEqual(self.resumen['etiquetas_oro'], n_oro)
        self.assertEqual(cv['predicciones_fuera_de_pliegue'], n_oro)
        self.assertGreater(cv['macro_f1'], cv['baseline_mayoria']['macro_f1'])
        # el autoajuste se publica como sobreajuste, no como métrica: siempre supera al CV
        self.assertGreaterEqual(self.resumen['autoajuste_sobre_oro']['accuracy'], cv['accuracy'])
        self.assertLess(cv['macro_f1'], 1.0)
        # el balanceo por clases está declarado en la configuración publicada
        self.assertIn('balancear_clases', json.loads(
            (RELEASE / 'modelo_hawkish_dovish.json').read_text(encoding='utf-8'))['config'])


class ReglaSeleccionTests(unittest.TestCase):
    """Cubre el desempate por CV repetida que decide la configuración publicada."""

    @staticmethod
    def _sintetico(n_por_clase=12, semilla=0):
        rng = random.Random(semilla)
        marcas = {'HAWKISH': ('subir', 'inflacion', 'ajuste'),
                  'NEUTRAL': ('dato', 'informe', 'reunion'),
                  'DOVISH': ('bajar', 'holgura', 'debil')}
        punt = {'HAWKISH': 0.75, 'NEUTRAL': 0.0, 'DOVISH': -0.75}
        # Lexico deliberadamente invertido: un baseline debil, que es el caso real del
        # corpus (el lexico yerra en un tercio). Con un lexico casi perfecto ninguna
        # candidata supera el filtro de la curva y el desempate no llega a correr.
        errado = {'HAWKISH': -0.75, 'NEUTRAL': 0.0, 'DOVISH': 0.75}
        cuentas, y, oro, lex = [], [], [], []
        for c in ('HAWKISH', 'NEUTRAL', 'DOVISH'):
            for _ in range(n_por_clase):
                toks = list(marcas[c]) * 3 + [rng.choice(['ruido1', 'ruido2', 'ruido3'])]
                cuentas.append(Counter(toks))
                y.append(c)
                oro.append(str(punt[c]))
                lex.append(str(errado[c]))
        return cuentas, y, oro, lex

    def test_desviacion_estandar_muestral(self):
        self.assertEqual(ent.desviacion([]), 0.0)
        self.assertEqual(ent.desviacion([0.5]), 0.0)
        self.assertAlmostEqual(ent.desviacion([1.0, 2.0, 3.0]), 1.0)
        self.assertAlmostEqual(ent.desviacion([2.0, 2.0, 2.0]), 0.0)
        # coincide con la definicion n-1 sobre valores conocidos
        vals = [0.61, 0.66, 0.64, 0.70]
        media = sum(vals) / len(vals)
        esperada = math.sqrt(sum((v - media) ** 2 for v in vals) / (len(vals) - 1))
        self.assertAlmostEqual(ent.desviacion(vals), esperada)

    def test_semilla_de_particion_es_reproducible_y_estratificada(self):
        y = ['HAWKISH'] * 10 + ['NEUTRAL'] * 20 + ['DOVISH'] * 10
        a = ent.pliegues(y, k=5, semilla=0)
        b = ent.pliegues(y, k=5, semilla=0)
        c = ent.pliegues(y, k=5, semilla=1)
        self.assertEqual([sorted(f) for f in a], [sorted(f) for f in b])
        self.assertNotEqual([sorted(f) for f in a], [sorted(f) for f in c])
        self.assertEqual(sorted(i for f in a for i in f), list(range(len(y))))
        for f in a:
            self.assertEqual(Counter(y[i] for i in f),
                             Counter({'NEUTRAL': 4, 'HAWKISH': 2, 'DOVISH': 2}))

    def test_cv_repetida_cubre_todo_el_conjunto_en_cada_semilla(self):
        cuentas, y, oro, lex = self._sintetico()
        for sem in (0, 3):
            m = ent.validacion_cruzada(cuentas, y, oro, lex, 10, 5, k=3, semilla=sem)
            self.assertEqual(m['predicciones_fuera_de_pliegue'], len(y))

    def test_diagnostico_desempata_por_cv_repetida_no_por_curva(self):
        cuentas, y, oro, lex = self._sintetico()
        diag = ent.diagnostico(cuentas, y, oro, lex,
                               rejilla=[(5, 5, False), (10, 5, True)],
                               curva_puntos=[12, 24], pliegues=3, semillas_cv=(0, 1, 2))
        self.assertTrue(diag['cv_repetida'])
        for clave, v in diag['cv_repetida'].items():
            self.assertEqual(len(v['macro_f1_por_semilla']), 3, clave)
            self.assertLessEqual(v['semillas_ganando_al_lexico'], 3)
            self.assertAlmostEqual(v['macro_f1_desviacion'],
                                   ent.desviacion(v['macro_f1_por_semilla']), places=3)
        # la publicada es la de mayor macro-F1 medio en CV repetida, no la de la curva
        medios = {k: v['macro_f1_medio'] for k, v in diag['cv_repetida'].items()}
        self.assertEqual(diag['clave_mejor_configuracion'], max(medios, key=medios.get))
        mejor = diag['mejor_configuracion']
        self.assertEqual(
            f"{mejor['max_rasgos']}/{mejor['iteraciones']}/bal={mejor['balancear_clases']}",
            diag['clave_mejor_configuracion'])

    def test_release_publica_lo_que_elige_la_regla(self):
        d = json.loads((RELEASE / 'diagnostico_capacidad.json').read_text(encoding='utf-8'))
        cfg = json.loads((RELEASE / 'modelo_hawkish_dovish.json').read_text(encoding='utf-8'))['config']
        mejor = d['mejor_configuracion']
        self.assertEqual(cfg['max_rasgos'], mejor['max_rasgos'])
        self.assertEqual(cfg['iteraciones'], mejor['iteraciones'])
        self.assertEqual(cfg['balancear_clases'], mejor['balancear_clases'])
        self.assertEqual(set(cfg['origen_configuracion'].values()), {'regla_diagnostico'})
        # el desempate publicado es por CV repetida sobre el conjunto completo; si el
        # filtro de la curva no dejo candidatas, cv_repetida va vacio y no hay desempate
        if d['cv_repetida']:
            medios = {k: v['macro_f1_medio'] for k, v in d['cv_repetida'].items()}
            self.assertEqual(d['clave_mejor_configuracion'], max(medios, key=medios.get))
            self.assertIn(d['clave_mejor_configuracion'], medios)
        else:
            self.assertTrue(d['descartadas_por_curva'],
                            'cv_repetida vacia solo es licita si el filtro descarto candidatas')
        # el macro-F1 publicado es el de una sola semilla: no puede superar al maximo de la rejilla
        self.assertLessEqual(d['mejor_configuracion']['macro_f1'],
                             max(g['macro_f1'] for g in d['rejilla']) + 1e-9)


class DiagnosticoFallosTests(unittest.TestCase):
    """Cubre el diagnóstico de fallos sobre predicciones fuera de pliegue."""

    @classmethod
    def setUpClass(cls):
        cls.resumen = json.loads((RELEASE / 'resumen_entrenamiento.json').read_text(encoding='utf-8'))
        cls.modelo = json.loads((RELEASE / 'modelo_hawkish_dovish.json').read_text(encoding='utf-8'))
        cls.ruta = RELEASE / 'fallos_fuera_de_pliegue.csv'
        cls.filas = []
        if cls.ruta.exists():
            with open(cls.ruta, encoding='utf-8') as f:
                cls.filas = list(csv.DictReader(f))

    def test_el_csv_cubre_las_500_etiquetas(self):
        self.assertTrue(self.filas, 'falta fallos_fuera_de_pliegue.csv; ejecute diagnosticar_fallos_hawkish_dovish.py')
        with open(etq.ETIQUETAS, encoding='utf-8') as f:
            oro = json.load(f)['Etiquetas']
        self.assertEqual(len(self.filas), len(oro))
        self.assertEqual({r['ID_Turno'] for r in self.filas}, {e['ID_Turno'] for e in oro})

    def test_grupo_actor_valido_en_cada_fila(self):
        for r in self.filas:
            self.assertIn(r['Grupo_Actor'], ('CONSEJO', 'STAFF', 'HACIENDA'), r['ID_Turno'])
            self.assertEqual(r['Grupo_Actor'], hd.grupo_actor(r['Rol_Final']), r['ID_Turno'])

    def test_aciertos_coinciden_con_la_matriz_publicada(self):
        # el CSV es fuera de pliegue; la matriz del resumen también, así que deben cuadrar
        self.assertEqual(sum(1 for r in self.filas if r['Acierta'] == 'NO'),
                         sum(self.resumen['validacion_cruzada']['matriz_real_x_predicha'][o][p]
                             for o in ('HAWKISH', 'NEUTRAL', 'DOVISH')
                             for p in ('HAWKISH', 'NEUTRAL', 'DOVISH') if o != p))
        for r in self.filas:
            espera = 'SI' if r['Pred_Fuera_De_Pliegue'] == r['HD_Clase_Oro'] else 'NO'
            self.assertEqual(r['Acierta'], espera, r['ID_Turno'])
        # la distribución predicha del CSV es la de la validación cruzada, no la del release
        por_clase = Counter(r['Pred_Fuera_De_Pliegue'] for r in self.filas)
        matriz = self.resumen['validacion_cruzada']['matriz_real_x_predicha']
        for c in ('HAWKISH', 'NEUTRAL', 'DOVISH'):
            self.assertEqual(por_clase[c], sum(matriz[o][c] for o in matriz), c)

    def test_fuera_de_pliegue_reproduce_el_cv_publicado(self):
        cfg = self.modelo['config']
        with open(etq.ETIQUETAS, encoding='utf-8') as f:
            paq = json.load(f)['Etiquetas']
        turnos = {t['ID_Turno']: t for t in hd.cargar_turnos()}
        _, y, oro, _, oof = diag.fuera_de_pliegue(paq, turnos, cfg, k=5, semilla=0)
        m = ent.metricas(y, [o['clase'] for o in oof], oro, [o['score'] for o in oof])
        cv = self.resumen['validacion_cruzada']
        self.assertEqual(m['macro_f1'], cv['macro_f1'])
        self.assertEqual(m['accuracy'], cv['accuracy'])
        self.assertEqual(len(oof), len(y))
        self.assertTrue(all(o is not None for o in oof))


class EnsembleAnidadoTests(unittest.TestCase):
    """La mezcla modelo+léxico se evalúa con el peso elegido dentro del pliegue."""

    @classmethod
    def setUpClass(cls):
        cls.ruta = RELEASE / 'ensemble_anidado.json'
        cls.res = json.loads(cls.ruta.read_text(encoding='utf-8')) if cls.ruta.exists() else {}

    def test_la_rejilla_incluye_no_mezclar(self):
        # si w=1.0 no está, la CV interna no puede descartar la mezcla y el veredicto es forzado
        self.assertIn(1.0, ens.PESOS)
        self.assertEqual(len(ens.PESOS), len(set(ens.PESOS)))

    def test_el_control_reproduce_el_cv_publicado(self):
        self.assertTrue(self.res, 'falta ensemble_anidado.json; ejecute validar_ensemble_hawkish_dovish.py')
        self.assertTrue(self.res['control_reproduce_cv_publicado'])
        publicado = json.loads((RELEASE / 'resumen_entrenamiento.json').read_text(encoding='utf-8'))
        self.assertEqual(self.res['macro_f1_por_semilla'][0]['modelo_argmax'],
                         publicado['validacion_cruzada']['macro_f1'])

    def test_veredicto_coherente_con_la_diferencia(self):
        gana = self.res['diferencia_mezcla_menos_umbral'] > 0
        self.assertIn('no mejora' if not gana else 'mejora', self.res['veredicto'])
        self.assertEqual(self.res['semillas_ganando_la_mezcla'],
                         sum(1 for f in self.res['macro_f1_por_semilla']
                             if f['mezcla'] > f['modelo_umbral']))

    def test_elegir_peso_devuelve_un_peso_de_la_rejilla(self):
        # subconjunto chico y 3 pliegues internos para no alargar la suite
        cuentas, y, oro, lex = ens.cargar()
        sub = list(range(150))
        cfg = {'max_rasgos': 150, 'iteraciones': 30, 'balancear': True}
        w, tabla = ens.elegir_peso(cuentas, y, oro, lex, sub, cfg, k=3, semilla=0)
        self.assertIn(w, ens.PESOS)
        self.assertEqual(set(tabla), set(ens.PESOS))
        # el peso elegido es el de mayor macro-F1 de la tabla interna
        self.assertEqual(tabla[w], max(tabla.values()))


class ReglaDeDecisionTests(unittest.TestCase):
    """La clase publicada es argmax del softmax, NO el umbral sobre el puntaje."""

    @classmethod
    def setUpClass(cls):
        with open(RELEASE / 'puntajes_hawkish_dovish.csv', encoding='utf-8') as f:
            cls.filas = list(csv.DictReader(f))

    def test_la_clase_publicada_no_es_el_umbral_del_puntaje(self):
        # 531 de 9.257: argmax ve hawkish/dovish pero el puntaje cae en la banda neutra.
        # Si esto cambiara a 0, alguien habría redefinido la clase y hay que revisarlo.
        discrepa = [r for r in self.filas
                    if r['HD_Clase_Modelo'] != hd.clase(float(r['HD_Score_Modelo']))]
        self.assertEqual(len(discrepa), 531)
        for r in discrepa:
            self.assertEqual(hd.clase(float(r['HD_Score_Modelo'])), 'NEUTRAL', r['ID_Turno'])
            self.assertNotEqual(r['HD_Clase_Modelo'], 'NEUTRAL', r['ID_Turno'])

    def test_la_clase_publicada_es_reproducible_desde_el_modelo(self):
        # argmax sobre las probabilidades del JSON, no umbral: ésa es la semántica publicada
        modelo = json.loads((RELEASE / 'modelo_hawkish_dovish.json').read_text(encoding='utf-8'))
        clases = modelo['clases']
        for r in self.filas[:400]:
            puntaje = float(r['HD_Score_Modelo'])
            if r['HD_Clase_Modelo'] == 'NEUTRAL':
                self.assertLess(abs(puntaje), 1.0)
                continue
            # si argmax dice hawkish/dovish, el signo del puntaje debe concordar
            self.assertEqual(r['HD_Clase_Modelo'], 'HAWKISH' if puntaje > 0 else 'DOVISH',
                             r['ID_Turno'])
        self.assertEqual(clases, ['HAWKISH', 'NEUTRAL', 'DOVISH'])

    def test_el_csv_de_fallos_usa_la_misma_regla_que_el_release(self):
        # las predicciones fuera de pliegue deben sumar igual que las columnas de la matriz
        with open(RELEASE / 'fallos_fuera_de_pliegue.csv', encoding='utf-8') as f:
            fallos = list(csv.DictReader(f))
        resumen = json.loads((RELEASE / 'resumen_entrenamiento.json').read_text(encoding='utf-8'))
        matriz = resumen['validacion_cruzada']['matriz_real_x_predicha']
        por_clase = Counter(r['Pred_Fuera_De_Pliegue'] for r in fallos)
        for c in ('HAWKISH', 'NEUTRAL', 'DOVISH'):
            self.assertEqual(por_clase[c], sum(matriz[o][c] for o in matriz), c)


class CifrasDelInformeTests(unittest.TestCase):
    """Las cifras del informe deben estar bien atribuidas, no sólo presentes.

    Un chequeo de presencia no detecta una atribución invertida: el informe llegó a
    decir que el umbral daría la distribución que en realidad publica el argmax. Aquí
    se verifica en qué lado de la frase cae cada cifra.
    """

    @classmethod
    def setUpClass(cls):
        with open(RELEASE / 'puntajes_hawkish_dovish.csv', encoding='utf-8') as f:
            filas = list(csv.DictReader(f))
        pub = Counter(r['HD_Clase_Modelo'] for r in filas)
        umb = Counter(hd.clase(float(r['HD_Score_Modelo'])) for r in filas)

        def fmt(c):
            return (f"{c['HAWKISH']:,} H / {c['DOVISH']:,} D / "
                    f"{c['NEUTRAL']:,} N").replace(',', '.')

        cls.publicada, cls.umbral = fmt(pub), fmt(umb)
        cls.doc = (ROOT / 'docs' / 'HAWKISH_DOVISH_V1_2026-09-11.md').read_text(encoding='utf-8')

    def test_las_dos_reglas_no_dan_la_misma_distribucion(self):
        self.assertNotEqual(self.publicada, self.umbral)

    def test_la_frase_atribuye_cada_cifra_a_su_regla(self):
        inicio = self.doc.index('Aplicar\n`|HD_Score_Modelo|')
        fin = self.doc.index('ordenar, no para reclasificar')
        frase = self.doc[inicio:fin]
        self.assertIn('en vez de', frase)
        antes, despues = frase.split('en vez de')
        # antes de "en vez de" va lo que daría el umbral; después, lo que publica el release
        self.assertIn(self.umbral, antes, 'el umbral debe ir antes de "en vez de"')
        self.assertIn(self.publicada, despues, 'la publicada debe ir después de "en vez de"')
        self.assertNotIn(self.publicada, antes, 'cifra publicada atribuida al umbral')
        self.assertNotIn(self.umbral, despues, 'cifra del umbral atribuida a la publicada')

    def test_el_umbral_da_menos_hawkish_y_dovish_que_el_argmax(self):
        # las 531 discrepancias van siempre en este sentido: argmax ve H/D, el puntaje no
        with open(RELEASE / 'puntajes_hawkish_dovish.csv', encoding='utf-8') as f:
            filas = list(csv.DictReader(f))
        pub = Counter(r['HD_Clase_Modelo'] for r in filas)
        umb = Counter(hd.clase(float(r['HD_Score_Modelo'])) for r in filas)
        self.assertLess(umb['HAWKISH'], pub['HAWKISH'])
        self.assertLess(umb['DOVISH'], pub['DOVISH'])
        self.assertGreater(umb['NEUTRAL'], pub['NEUTRAL'])


class PrevalenciaReponderadaTests(unittest.TestCase):
    """La muestra no es proporcional: la prevalencia exige post-estratificar por decil."""

    @classmethod
    def setUpClass(cls):
        cls.ruta = RELEASE / 'prevalencia_reponderada.json'
        cls.res = json.loads(cls.ruta.read_text(encoding='utf-8')) if cls.ruta.exists() else {}

    def test_las_prevalencias_suman_uno(self):
        self.assertTrue(self.res, 'falta prevalencia_reponderada.json; ejecute estimar_prevalencia_hawkish_dovish.py')
        self.assertAlmostEqual(sum(self.res['prevalencia'].values()), 1.0, places=3)

    def test_ponderar_cambia_el_resultado(self):
        # si ponderar no cambiara nada, la muestra ya sería proporcional y el aviso del
        # informe estaría de más
        n = self.res['etiquetas']
        for c in ('HAWKISH', 'NEUTRAL', 'DOVISH'):
            crudo = self.res['crudo_sin_ponderar'][c] / n
            self.assertGreater(abs(self.res['prevalencia'][c] - crudo), 0.01, c)
        # el sentido es el esperado: la muestra sobre-representó los extremos
        self.assertLess(self.res['prevalencia']['HAWKISH'],
                        self.res['crudo_sin_ponderar']['HAWKISH'] / n)
        self.assertGreater(self.res['prevalencia']['NEUTRAL'],
                           self.res['crudo_sin_ponderar']['NEUTRAL'] / n)

    def test_los_pesos_reconstruyen_el_universo(self):
        # la suma de pesos debe dar el tamaño del universo, no el de la muestra
        self.assertEqual(self.res['suma_pesos'], float(self.res['universo']))
        self.assertEqual(sum(self.res['N_por_decil'].values()), self.res['universo'])
        self.assertEqual(sum(self.res['n_por_decil'].values()), self.res['etiquetas'])
        # las claves de decil viajan como string en el JSON
        for d, w in self.res['peso_por_decil'].items():
            self.assertIn(d, self.res['N_por_decil'])
            self.assertAlmostEqual(w, self.res['N_por_decil'][d]
                                   / self.res['n_por_decil'][d], places=3)

    def test_el_ic95_contiene_la_estimacion_y_es_coherente(self):
        for c in ('HAWKISH', 'NEUTRAL', 'DOVISH'):
            lo, hi = self.res['ic95'][c]
            p = self.res['prevalencia'][c]
            self.assertLessEqual(lo, p)
            self.assertLessEqual(p, hi)
            self.assertGreater(hi - lo, 0.0)
            self.assertLess(hi - lo, 0.15, f'IC de {c} implausiblemente ancho para n=500')

    def test_el_efecto_de_disenio_es_modesto(self):
        # 10 deciles con 30-83 casos cada uno: ponderar no debería costar mucha precisión
        self.assertGreater(self.res['tamanio_efectivo_muestra'], 300)
        self.assertLess(self.res['efecto_de_disenio'], 1.5)

    def test_los_deciles_estan_casi_balanceados_en_el_universo(self):
        # se definen por rango, así que salen de tamaño casi igual: ~279 cada uno
        vals = list(self.res['N_por_decil'].values())
        self.assertEqual(len(vals), 10)
        self.assertLess(max(vals) - min(vals), 3)

    def test_dentro_del_decil_la_muestra_es_aproximadamente_representativa(self):
        # ésta es la hipótesis que justifica ponderar a nivel de decil y no de celda fina
        tv = [v['variacion_total'] for v in self.res['representatividad_por_decil'].values()]
        self.assertEqual(len(tv), 10)
        self.assertLess(sum(tv) / len(tv), 0.25, 'composición media demasiado desviada')
        self.assertLess(max(tv), 0.40, 'hay un decil con composición muy sesgada')

    def test_deciles_lexico_es_determinista_y_cubre_el_universo(self):
        pool = [{'ID_Turno': f'T{i}', 'Lex': {'score': (i % 7) / 7.0}} for i in range(100)]
        a = prev.deciles_lexico(pool)
        b = prev.deciles_lexico(pool)
        self.assertEqual(a, b)
        self.assertEqual(len(a), 100)
        self.assertEqual(set(a.values()), set(range(1, 11)))
        self.assertEqual(Counter(a.values())[1], 10)

    def test_el_oro_reponderado_concuerda_con_el_modelo(self):
        # dos rutas independientes hacia la misma cantidad: deben quedar cerca
        contraste = self.res.get('contraste_con_el_modelo')
        self.assertTrue(contraste, 'falta el contraste contra la predicción del modelo')
        for c, v in contraste.items():
            self.assertLess(abs(v['diferencia']), 60, c)


class CoherenciaReadmeInformeTests(unittest.TestCase):
    """El README y el informe no pueden contradecirse.

    El README llegó a decir que la muestra "no sirve para estimar prevalencia" cuando
    el informe ya publicaba la estimación reponderada. Nadie lo cazó porque se leían
    por separado. Aquí se contrastan contra el mismo artefacto.
    """

    @classmethod
    def setUpClass(cls):
        cls.readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        cls.doc = (ROOT / 'docs' / 'HAWKISH_DOVISH_V1_2026-09-11.md').read_text(encoding='utf-8')
        cls.prev = json.loads((RELEASE / 'prevalencia_reponderada.json').read_text(encoding='utf-8'))
        cls.ruido = json.loads((RELEASE / 'ruido_oro.json').read_text(encoding='utf-8'))

    def test_el_readme_no_niega_la_prevalencia_que_el_informe_publica(self):
        self.assertNotIn('no sirve para estimar prevalencia', self.readme)
        self.assertNotIn('no se puede leer prevalencia', self.readme)
        # y si el informe la estima, el README debe citarla
        self.assertIn('10,8%', self.doc)
        self.assertIn('10,8%', self.readme)

    def test_ambos_citan_la_misma_prevalencia_que_el_artefacto(self):
        for c, esperado in (('HAWKISH', '10,8%'), ('NEUTRAL', '73,5%'), ('DOVISH', '15,7%')):
            pct = f"{self.prev['prevalencia'][c] * 100:.1f}".replace('.', ',') + '%'
            self.assertEqual(pct, esperado, c)
            self.assertIn(pct, self.doc, f'{c} falta en el informe')
            self.assertIn(pct, self.readme, f'{c} falta en el README')

    def test_ambos_citan_el_mismo_contraste_con_el_modelo(self):
        c = self.prev['contraste_con_el_modelo']

        def mil(n):   # separador de miles como lo escriben el README y el informe
            return f'{n:,}'.replace(',', '.')

        oro = [mil(c[k]['oro_reponderado']) for k in ('HAWKISH', 'NEUTRAL', 'DOVISH')]
        mod = [mil(c[k]['modelo_sobre_universo']) for k in ('HAWKISH', 'NEUTRAL', 'DOVISH')]
        self.assertEqual(oro, ['301', '2.051', '438'])
        self.assertEqual(mod, ['321', '2.058', '410'])
        # las seis cifras tienen que aparecer en los dos documentos
        for texto, nombre in ((self.doc, 'informe'), (self.readme, 'README')):
            for v in oro + mod:
                self.assertIn(v, texto, f'{v} falta en el {nombre}')

    def test_ambos_citan_el_mismo_ruido_del_oro_que_el_artefacto(self):
        # el acuerdo y el kappa deben salir del artefacto, no estar escritos a mano
        acuerdo = f"{self.ruido['acuerdo_clase']:.3f}".replace('.', ',')
        kappa = f"{self.ruido['kappa']:.3f}".replace('.', ',')
        self.assertEqual((acuerdo, kappa), ('0,825', '0,582'))
        for texto, nombre in ((self.doc, 'informe'), (self.readme, 'README')):
            self.assertIn(acuerdo, texto, f'{acuerdo} falta en el {nombre}')
            self.assertIn(kappa, texto, f'{kappa} falta en el {nombre}')

    def test_el_informe_cita_el_contraste_con_el_modelo_desde_el_artefacto(self):
        cm = self.ruido['contraste_con_el_modelo']
        sub = f"{cm['modelo_en_la_submuestra']:.3f}".replace('.', ',')
        todas = f"{cm['modelo_en_las_500']:.3f}".replace('.', ',')
        self.assertEqual((sub, todas), ('0,625', '0,780'))
        for v in (sub, todas, cm['modelo_aciertos_en_la_submuestra']):
            self.assertIn(v, self.doc, f'{v} falta en el informe')

    def test_ninguno_presenta_el_test_retest_como_si_fuera_un_segundo_revisor(self):
        # es la misma revisora re-leyendo; llamarlo "segundo revisor" sería falso
        for texto, nombre in ((self.doc, 'informe'), (self.readme, 'README')):
            self.assertNotIn('segundo revisor validó', texto.lower(), nombre)
            self.assertNotIn('doble codificación', texto.lower(), nombre)
        unido = (self.doc + self.readme).lower()
        self.assertIn('test-retest', unido)
        self.assertIn('techo optimista', unido)

    def test_la_cobertura_de_lectura_es_la_misma_en_ambos(self):
        # la ventana real es 520 iniciales + 280 finales, no "800 caracteres" a secas:
        # usar los primeros 800 fue exactamente el error que invirtio una conclusion
        self.assertIn('520', self.readme)
        self.assertIn('280', self.readme)
        self.assertIn('520', self.doc)
        self.assertIn('280', self.doc)
        self.assertNotIn('Cobertura media de lectura: **35% de cada texto**', self.readme)
        # y las constantes del codigo tienen que coincidir con lo que dicen los textos
        self.assertEqual((etq.LECTURA_CABEZA, etq.LECTURA_COLA), (520, 280))



class RuidoDelOroTests(unittest.TestCase):
    """Re-lectura ciega de 40 etiquetas: la única cuantificación posible del límite nº1."""

    @classmethod
    def setUpClass(cls):
        cls.ciego_p = ROOT / 'data/curation/relectura_ciega_40_textos.json'
        cls.re_p = ROOT / 'data/curation/relectura_ciega_40.json'
        cls.res_p = RELEASE / 'ruido_oro.json'
        cls.ciego = json.loads(cls.ciego_p.read_text(encoding='utf-8'))
        cls.re = json.loads(cls.re_p.read_text(encoding='utf-8'))['Relectura']
        cls.res = json.loads(cls.res_p.read_text(encoding='utf-8'))
        cls.oro = {e['ID_Turno']: e for e in
                   json.loads((ROOT / 'data/curation/hawkish_dovish_etiquetas_v1.json')
                              .read_text(encoding='utf-8'))['Etiquetas']}

    def pares(self):
        return [{'id': o['ID_Turno'],
                 're_score': float(self.re[o['ID_Turno']]),
                 're_clase': hd.clase(float(self.re[o['ID_Turno']])),
                 'oro_score': float(self.oro[o['ID_Turno']]['HD_Score']),
                 'oro_clase': self.oro[o['ID_Turno']]['HD_Clase']} for o in self.ciego]

    def test_la_submuestra_ciega_no_filtra_la_etiqueta(self):
        # si la ventana llevara la clase o el score, la re-lectura no mediría nada
        self.assertEqual(len(self.ciego), ruido.N_RELECTURA)
        for o in self.ciego:
            for token in ruido.TOKENS_PROHIBIDOS:
                self.assertNotIn(token, o['Ventana'], f'{token} filtrado en {o["ID_Turno"]}')

    def test_el_sorteo_ciego_se_reproduce_con_la_semilla(self):
        # mismo sorteo => misma submuestra; sin esto el 0,825 no es reproducible
        regen = ruido.muestra_ciega()
        self.assertEqual([o['ID_Turno'] for o in regen],
                         [o['ID_Turno'] for o in self.ciego])

    def test_la_relectura_cubre_exactamente_la_submuestra(self):
        self.assertEqual(set(self.re), {o['ID_Turno'] for o in self.ciego})
        for v in self.re.values():
            self.assertGreaterEqual(float(v), -1.0)
            self.assertLessEqual(float(v), 1.0)

    def test_las_cifras_del_artefacto_se_recalculan_desde_las_entradas(self):
        rec = ruido.comparar(self.pares(), semilla=ruido.SEMILLA_RELECTURA)
        for clave in ('acuerdo_clase', 'kappa', 'mae_puntaje', 'correlacion_puntaje',
                      'inversiones_de_signo'):
            self.assertEqual(rec[clave], self.res[clave], clave)
        self.assertEqual(rec['matriz_relectura_contra_oro'],
                         self.res['matriz_relectura_contra_oro'])

    def test_la_matriz_cuadra_con_n_y_toda_discrepancia_es_de_clase_vecina(self):
        m = self.res['matriz_relectura_contra_oro']
        total = sum(v for fila in m.values() for v in fila.values())
        self.assertEqual(total, self.res['n'])
        diag = sum(m[c][c] for c in ('HAWKISH', 'NEUTRAL', 'DOVISH'))
        self.assertEqual(diag / total, self.res['acuerdo_clase'])
        # cero inversiones de signo: el ruido mueve la frontera, no el sentido
        self.assertEqual(self.res['inversiones_de_signo'], 0)
        for d in self.res['discrepancias']:
            self.assertNotEqual({d['relectura'], d['oro']}, {'HAWKISH', 'DOVISH'})

    def test_el_contraste_con_el_modelo_sale_del_csv_de_fallos(self):
        # el 0,625 del informe debe poder reproducirse desde el release, no de memoria
        rec = ruido.contraste_modelo(self.pares())
        self.assertEqual(rec, self.res['contraste_con_el_modelo'])
        self.assertEqual(rec['modelo_aciertos_en_la_submuestra'], '25/40')
        self.assertEqual(rec['modelo_en_la_submuestra'], 0.625)
        self.assertEqual(rec['modelo_en_las_500'], 0.78)
        # con n=40 el modelo rinde menos que en las 500: fluctuación, no hallazgo
        self.assertLess(rec['modelo_en_la_submuestra'], rec['modelo_en_las_500'])

    def test_el_intervalo_del_acuerdo_contiene_al_accuracy_del_modelo(self):
        # ésta es la única conclusión que el dato permite: no se puede afirmar que el
        # modelo haya alcanzado el techo del ruido, ni que le falte mucho
        lo, hi = self.res['acuerdo_ic95']
        self.assertLess(lo, self.res['contraste_con_el_modelo']['modelo_en_las_500'])
        self.assertLess(self.res['contraste_con_el_modelo']['modelo_en_las_500'], hi)

    def test_los_intervalos_envuelven_la_estimacion_y_son_honestos(self):
        for punto, ic in (('acuerdo_clase', 'acuerdo_ic95'),
                          ('kappa', 'kappa_ic95'),
                          ('mae_puntaje', 'mae_ic95')):
            v = self.res[punto]
            self.assertLessEqual(self.res[ic][0], v, f'{ic} no envuelve por abajo')
            self.assertLessEqual(v, self.res[ic][1], f'{ic} no envuelve por arriba')
        # con n=40 el intervalo de kappa es ancho y debe decirse, no ocultarse
        ancho = self.res['kappa_ic95'][1] - self.res['kappa_ic95'][0]
        self.assertGreater(ancho, 0.4)

    def test_los_limites_estan_declarados_en_el_artefacto(self):
        unido = ' '.join(self.res['limites']).lower()
        self.assertIn('una sola revisora', unido)
        self.assertIn('techo optimista', unido)
        self.assertIn('test-retest', unido)


class AuditoriaMetodologicaTests(unittest.TestCase):
    """Bloquea las cuatro cifras de la auditoría y su coherencia con el informe."""

    @classmethod
    def setUpClass(cls):
        cls.ruta = RELEASE / 'auditoria_metodologica.json'
        cls.aud = json.loads(cls.ruta.read_text(encoding='utf-8'))
        cls.doc = (ROOT / 'docs' / 'AUDITORIA_HAWKISH_DOVISH_V1_2026-09-11.md').read_text(encoding='utf-8')
        cls.informe = (ROOT / 'docs' / 'HAWKISH_DOVISH_V1_2026-09-11.md').read_text(encoding='utf-8')
        cls.readme = (ROOT / 'README.md').read_text(encoding='utf-8')

    def test_la_cv_aleatoria_filtra_entre_sesiones(self):
        f = self.aud['fuga_por_sesion']
        self.assertGreater(f['fraccion_sesiones_repartidas_en_varios_pliegues'], 0.8)
        # agrupar por sesion tiene que bajar el numero: si no bajara, no habria fuga
        self.assertLess(f['macro_f1_cv_por_sesion'], f['macro_f1_cv_por_turno'])
        self.assertGreater(f['semillas_donde_por_sesion_es_menor'], len(f['semillas']) / 2)
        # y el efecto es chico: no invalida el ranking de configuraciones
        self.assertLess(abs(f['diferencia_media']), 0.03)

    def test_el_modelo_no_generaliza_en_el_tiempo(self):
        g = self.aud['generalizacion_temporal']
        self.assertGreaterEqual(len(g['rolling_origin']), 6)
        # el hallazgo central: el rolling-origin cae muy por debajo del numero publicado
        self.assertLess(g['macro_f1_medio'], 0.55)
        # pero la accuracy se sostiene porque NEUTRAL domina: hay que mirar el macro-F1
        self.assertGreater(g['accuracy_media'], 0.65)
        # y sigue ganandole al lexico en los cortes: la conclusion comparativa aguanta
        for r in g['rolling_origin']:
            self.assertGreater(r['macro_f1'], 0.2)

    def test_el_modelo_le_gana_al_lexico_en_todos_los_cortes_temporales(self):
        # la conclusion comparativa aguanta aunque el nivel absoluto no
        cortes = self.aud['cortes_temporales']
        self.assertEqual([c['corte'] for c in cortes], [2011, 2012, 2013])
        for c in cortes:
            self.assertGreater(c['macro_f1'], c['macro_f1_lexico'], c['corte'])
        # la cifra que cita el informe debe salir de aqui, no de un calculo suelto
        c2013 = next(c for c in cortes if c['corte'] == 2013)
        self.assertEqual(round(c2013['macro_f1'], 3), 0.671)
        self.assertEqual(round(c2013['macro_f1_lexico'], 3), 0.493)
        self.assertIn('0,671 contra 0,493', self.informe)

    def test_hay_desplazamiento_real_de_etiquetas(self):
        ep = {e['periodo']: e for e in self.aud['desplazamiento_de_etiquetas']}
        # dovish pasa de 8,4% a 30,7% a 9,2% a 23,8%: eso rompe la intercambiabilidad
        self.assertAlmostEqual(ep['2005-2007']['DOVISH'], 0.084, places=3)
        self.assertAlmostEqual(ep['2008-2009']['DOVISH'], 0.3068, places=3)
        self.assertAlmostEqual(ep['2013-2015']['DOVISH'], 0.2384, places=3)
        self.assertGreater(ep['2008-2009']['DOVISH'], 3 * ep['2005-2007']['DOVISH'])

    def test_la_extraccion_de_decisiones_es_internamente_coherente(self):
        x = self.aud['validez_de_constructo']['extraccion_de_decisiones']
        self.assertGreaterEqual(x['sesiones_con_decision'], 100)
        self.assertEqual(x['incoherencias_verbo_nivel'], [])
        self.assertGreater(x['transiciones_consecutivas_comparadas'], 80)

    def test_la_validez_de_constructo_sobrevive_a_quitar_el_anuncio(self):
        v = self.aud['validez_de_constructo']
        sucia = v['contemporanea_con_anuncio']['spearman']
        limpia = v['tono_t_contra_decision_t1']['spearman']
        # quitar el anuncio baja la correlacion (habia contaminacion) pero no la mata
        self.assertLess(limpia, sucia)
        self.assertGreater(limpia, 0.5)
        # y el orden ALZA > SIN CAMBIO > RECORTE se mantiene en las tres versiones
        for clave in ('contemporanea_con_anuncio', 'contemporanea_sin_anuncio',
                      'tono_t_contra_decision_t1'):
            m = v[clave]['tono_medio_por_decision']
            self.assertGreater(m['ALZA']['tono_medio'], m['SIN_CAMBIO']['tono_medio'], clave)
            self.assertGreater(m['SIN_CAMBIO']['tono_medio'], m['RECORTE']['tono_medio'], clave)

    def test_la_extraccion_de_decisiones_se_recalcula_desde_el_corpus(self):
        # recomputo real: no lee el artefacto, vuelve a extraer del texto
        turnos = hd.cargar_turnos()
        dec = aud.decidir(turnos)
        cal = aud.cohorte(turnos, dec)
        self.assertEqual(cal, self.aud['validez_de_constructo']['extraccion_de_decisiones'])

    def test_el_spearman_de_validez_se_recalcula_desde_las_entradas(self):
        # tono desde el CSV de puntajes + decisiones desde el corpus -> mismo rho
        turnos = {t['ID_Turno']: t for t in hd.cargar_turnos()}
        dec = aud.decidir(list(turnos.values()))
        ses_corpus = sorted({i.split(':')[0] for i in turnos})
        siguiente = {s: ses_corpus[i + 1] for i, s in enumerate(ses_corpus[:-1])}
        anuncio = {r['ID_Turno'] for r in csv.DictReader(
                       PUNTAJES_AUD.open(newline='', encoding='utf-8'))
                   if r['En_Universo_Entrenado'] == 'true'
                   and aud.ANUNCIO.search(turnos[r['ID_Turno']]['Texto'])}
        tono = defaultdict(list)
        with PUNTAJES_AUD.open(newline='', encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                if r['Grupo_Actor'] == 'CONSEJO' and r['En_Universo_Entrenado'] == 'true' \
                        and r['ID_Turno'] not in anuncio:
                    tono[r['ID_Turno'].split(':')[0]].append(float(r['HD_Score_Modelo']))
        pares = [(aud.direccion(dec[siguiente[s]]['verbo']),
                  sum(tono[s]) / len(tono[s]))
                 for s in ses_corpus if tono[s] and siguiente.get(s) in dec]
        rho = aud.spearman([t for _, t in pares], [d for d, _ in pares])
        esperado = self.aud['validez_de_constructo']['tono_t_contra_decision_t1']
        self.assertEqual(len(pares), esperado['n'])
        self.assertEqual(round(rho, 4), esperado['spearman'])

    def test_la_particion_por_sesion_no_rompe_ninguna_sesion(self):
        sesiones = ['RPM-A', 'RPM-A', 'RPM-B', 'RPM-C', 'RPM-C', 'RPM-C', 'RPM-D', 'RPM-E']
        y = ['NEUTRAL'] * len(sesiones)
        total = 0
        for fold in aud.particion_sesion(y, sesiones, k=3, semilla=0):
            en_el_pliegue = [sesiones[i] for i in fold]
            total += len(en_el_pliegue)
            # todos los turnos de una sesion deben caer juntos en el mismo pliegue
            for s_ in set(en_el_pliegue):
                self.assertEqual(en_el_pliegue.count(s_), sesiones.count(s_), s_)
        self.assertEqual(total, len(sesiones))  # ningun turno se pierde ni se duplica
        # cada sesion aparece en exactamente un pliegue
        veces = defaultdict(int)
        for fold in aud.particion_sesion(y, sesiones, k=3, semilla=0):
            for s in {sesiones[i] for i in fold}:
                veces[s] += 1
        self.assertEqual(set(veces.values()), {1})

    def test_el_oro_queda_bajo_el_umbral_de_fiabilidad_citado(self):
        # 0,667 es el umbral de "conclusiones tentativas"; el oro no lo alcanza
        ruido_json = json.loads((RELEASE / 'ruido_oro.json').read_text(encoding='utf-8'))
        self.assertLess(ruido_json['kappa'], 0.667)
        self.assertIn('0,582', self.doc)
        self.assertIn('0,667', self.doc)

    def test_el_informe_y_el_readme_advierten_sobre_el_numero_temporal(self):
        # la correccion principal: el 0,685 no sirve para proyectar hacia adelante
        for texto, nombre in ((self.informe, 'informe'), (self.readme, 'README')):
            self.assertIn('0,456', texto, f'falta el macro-F1 temporal en el {nombre}')
            self.assertIn('rolling-origin', texto.lower(), f'falta el termino en el {nombre}')


class EfectoVentanaTests(unittest.TestCase):
    """El límite nº2 (ventana 520+280 vs texto completo) dejó de ser una conjetura."""

    @classmethod
    def setUpClass(cls):
        cls.res = json.loads((RELEASE / 'efecto_ventana.json').read_text(encoding='utf-8'))
        cls.ids = [o['ID_Turno'] for o in json.loads(
            (ROOT / 'data/curation/relectura_ciega_40_textos.json').read_text(encoding='utf-8'))]
        cls.vent = json.loads((ROOT / 'data/curation/relectura_ciega_40.json')
                              .read_text(encoding='utf-8'))['Relectura']
        cls.comp = json.loads((ROOT / 'data/curation/lectura_completa_40.json')
                              .read_text(encoding='utf-8'))['Lectura']
        cls.oro = {e['ID_Turno']: e for e in json.loads(
            (ROOT / 'data/curation/hawkish_dovish_etiquetas_v1.json')
            .read_text(encoding='utf-8'))['Etiquetas']}

    def pares(self):
        return [{'id': i,
                 'co_score': float(self.comp[i]), 'co_clase': hd.clase(float(self.comp[i])),
                 've_score': float(self.vent[i]), 've_clase': hd.clase(float(self.vent[i])),
                 'or_score': float(self.oro[i]['HD_Score']),
                 'or_clase': self.oro[i]['HD_Clase']} for i in self.ids]

    def test_las_tres_pasadas_cubren_la_misma_submuestra(self):
        self.assertEqual(set(self.comp), set(self.ids))
        self.assertEqual(set(self.vent), set(self.ids))
        for v in self.comp.values():
            self.assertGreaterEqual(float(v), -1.0)
            self.assertLessEqual(float(v), 1.0)

    def test_las_tres_comparaciones_se_recalculan_desde_las_entradas(self):
        pares = self.pares()
        for clave, ka, kb in (('ventana_contra_oro', 've', 'or'),
                              ('completo_contra_oro', 'co', 'or'),
                              ('completo_contra_ventana', 'co', 've')):
            rec = ven.comparar(pares, ka, kb, semilla=20260911)
            for campo in ('acuerdo', 'kappa', 'mae', 'inversiones_de_signo'):
                self.assertEqual(rec[campo], self.res[clave][campo], f'{clave}.{campo}')

    def test_la_ventana_cuesta_poco_pero_no_nada(self):
        puro = self.res['completo_contra_ventana']
        # efecto puro de la ventana: mismo lector, mismo día, sólo cambia cuánto texto vio
        self.assertGreater(puro['acuerdo'], 0.85)
        # los cambios de clase listados deben ser exactamente los desacuerdos contados
        self.assertEqual(len(puro['cambios_de_clase']),
                         puro['n'] - round(puro['acuerdo'] * puro['n']))
        self.assertEqual(len(puro['cambios_de_clase']), 3)
        # y no es cero: hay casos donde la ventana oculta el voto
        self.assertGreater(len(self.res['completo_contra_oro']['cambios_de_clase']), 0)

    def test_ninguna_comparacion_invierte_el_signo(self):
        for clave in ('ventana_contra_oro', 'completo_contra_oro', 'completo_contra_ventana'):
            self.assertEqual(self.res[clave]['inversiones_de_signo'], 0, clave)

    def test_leer_completo_no_empeora_el_acuerdo_con_el_oro(self):
        # contra-intuitivo y hay que fijarlo: el texto completo acuerda MAS con el oro
        self.assertGreaterEqual(self.res['completo_contra_oro']['acuerdo'],
                                self.res['ventana_contra_oro']['acuerdo'])
        self.assertGreater(self.res['completo_contra_oro']['kappa'],
                           self.res['ventana_contra_oro']['kappa'])

    def test_los_limites_estan_declarados(self):
        unido = ' '.join(self.res['limites']).lower()
        self.assertIn('n=40', unido)
        self.assertIn('misma revisora', unido)
        self.assertIn('subestimado', unido)



class DerivaTemporalTests(unittest.TestCase):
    """El remedio por recencia se probó y se refutó; aquí queda fijado."""

    @classmethod
    def setUpClass(cls):
        cls.res = json.loads((RELEASE / 'deriva_temporal.json').read_text(encoding='utf-8'))

    def test_el_veredicto_es_refutada_y_todas_pierden(self):
        self.assertEqual(self.res['veredicto'], 'REFUTADA')
        self.assertEqual(len(self.res['deslizantes']), 3)
        for d in self.res['deslizantes']:
            self.assertLess(d['diff_contra_expansiva'], 0.0, d['estrategia'])
            # gana en 1 de 8: no es un empate ruidoso, pierde casi siempre
            self.assertLessEqual(d['gana_en'], 2)
            self.assertEqual(d['cortes'], 8)

    def test_el_mecanismo_es_tamano_de_muestra_no_relevancia(self):
        base = self.res['expansiva']['n_entrena_medio']
        for d in self.res['deslizantes']:
            self.assertLess(d['n_entrena_medio'], base, d['estrategia'])
        # cuanto más corta la ventana, menos datos: el orden debe ser monotono
        ns = [d['n_entrena_medio'] for d in self.res['deslizantes']]
        self.assertEqual(ns, sorted(ns, reverse=True))
        self.assertLess(ns[-1], base * 0.6)

    def test_la_linea_base_coincide_con_la_auditoria(self):
        # el 0,4559 debe ser el mismo rolling-origin que reporta la auditoría
        aud = json.loads((RELEASE / 'auditoria_metodologica.json').read_text(encoding='utf-8'))
        self.assertEqual(self.res['expansiva']['macro_f1_medio'],
                         aud['generalizacion_temporal']['macro_f1_medio'])
        self.assertEqual(self.res['cortes_evaluados'],
                         [r['anio_prueba'] for r in aud['generalizacion_temporal']['rolling_origin']])

    def test_el_alcance_queda_declarado(self):
        self.assertIn('este tamaño de oro', self.res['alcance'])
        self.assertIn('No se publica ningún cambio al release', self.res['lectura'])



class CalibracionConfianzaTests(unittest.TestCase):
    """Prioridad nº6: qué columna del release sirve para ordenar por certeza."""

    @classmethod
    def setUpClass(cls):
        cls.res = json.loads((RELEASE / 'calibracion_confianza.json').read_text(encoding='utf-8'))

    def test_max_prob_es_la_unica_medida_monotona_y_bien_calibrada(self):
        c = self.res['candidatos']
        self.assertTrue(c['max_prob']['monotona'])
        self.assertLess(c['max_prob']['ece'], 0.06)
        # las otras dos NO son monotonas: no sirven para ordenar por certeza
        self.assertFalse(c['margen']['monotona'])
        self.assertFalse(c['abs_score']['monotona'])
        self.assertGreater(c['margen']['ece'], c['max_prob']['ece'])

    def test_el_margen_publicado_esta_mal_calibrado_en_el_extremo_bajo(self):
        # el cubo bajo del margen promete 0,40 y entrega 0,69: subestima mucho
        bajo = next(f for f in self.res['candidatos']['margen']['curva']
                    if f['cubo'] == '[0.30,0.50)')
        self.assertGreater(bajo['gap'], 0.2)

    def test_abs_score_reproduce_el_patron_no_monotono_ya_publicado(self):
        curva = self.res['candidatos']['abs_score']['curva']
        # el artefacto guarda 4 decimales; el informe cita 3
        prec = [round(f['precision_real'], 3) for f in curva]
        self.assertEqual(prec, [0.836, 0.678, 0.625, 0.797])
        # y ese es exactamente el patron no monotono que el informe ya publicaba
        self.assertLess(prec[2], prec[0])
        self.assertLess(prec[2], prec[3])

    def test_la_precision_de_max_prob_cubre_todo_el_rango(self):
        prec = [f['precision_real'] for f in self.res['candidatos']['max_prob']['curva']]
        self.assertAlmostEqual(prec[0], 0.500, places=3)
        self.assertAlmostEqual(prec[-1], 0.910, places=3)
        self.assertEqual(sum(f['n'] for f in self.res['candidatos']['max_prob']['curva']),
                         self.res['n'])

    def test_el_alcance_queda_declarado(self):
        unido = ' '.join(self.res['limites'])
        self.assertIn('FUERA DE PLIEGUE', unido)
        self.assertIn('8.757', unido)
        self.assertIn('0,988', unido)



class AuditoriaDocumentadaTests(unittest.TestCase):
    """Toda cifra citada en el documento de auditoría, recomputada desde los artefactos.

    El documento es la entrega legible; si se edita a mano puede desviarse de los
    JSON. Estas aserciones lo impiden. Los redondeos se hacen desde el valor
    completo, no desde el valor ya redondeado del artefacto: 107/142 = 75,3521%
    da 75,4%, pero 0,7535*100 cae en el empate 75,35 y Python redondea hacia abajo.
    """

    @classmethod
    def setUpClass(cls):
        cls.aud = json.loads((RELEASE / 'auditoria_metodologica.json').read_text(encoding='utf-8'))
        cls.rui = json.loads((RELEASE / 'ruido_oro.json').read_text(encoding='utf-8'))
        cls.ven = json.loads((RELEASE / 'efecto_ventana.json').read_text(encoding='utf-8'))
        cls.der = json.loads((RELEASE / 'deriva_temporal.json').read_text(encoding='utf-8'))
        cls.cal = json.loads((RELEASE / 'calibracion_confianza.json').read_text(encoding='utf-8'))
        cls.doc = (DOCS / 'AUDITORIA_HAWKISH_DOVISH_V1_2026-09-11.md').read_text(encoding='utf-8')

    @staticmethod
    def coma(x, n=3):
        return f"{x:.{n}f}".replace('.', ',')

    def test_h1_filas_de_rolling_origin(self):
        g = self.aud['generalizacion_temporal']
        self.assertEqual(self.coma(g['macro_f1_medio']), '0,456')
        self.assertEqual(self.coma(g['macro_f1_sd']), '0,105')
        self.assertEqual(self.coma(g['accuracy_media']), '0,727')
        for f in g['rolling_origin']:
            m, a = self.coma(f['macro_f1']), self.coma(f['accuracy'])
            plana = f"| {f['anio_prueba']} | {f['n_prueba']} | {m} | {a} |"
            negrita = f"| {f['anio_prueba']} | {f['n_prueba']} | **{m}** | {a} |"
            self.assertIn(plana if plana in self.doc else negrita, self.doc)
        peor = min(g['rolling_origin'], key=lambda z: z['macro_f1'])
        self.assertEqual(peor['anio_prueba'], 2009)
        self.assertIn('**0,301**', self.doc)

    def test_h1_filas_de_desplazamiento_de_etiquetas(self):
        # recomputo desde las etiquetas: el artefacto guarda 4 decimales y
        # redondear desde ahí introduce el empate 75,35 en el período 2010-2012
        et = json.loads(ETIQUETAS.read_text(encoding='utf-8'))['Etiquetas']
        for e in self.aud['desplazamiento_de_etiquetas']:
            lo, hi = (int(z) for z in e['periodo'].split('-'))
            sub = [x for x in et if lo <= int(x['ID_Turno'].split('-')[1]) <= hi]
            c = Counter(x['HD_Clase'] for x in sub)
            self.assertEqual(len(sub), e['n'])
            pcts = [self.coma(c[k] / len(sub) * 100, 1) for k in ('HAWKISH', 'NEUTRAL', 'DOVISH')]
            plana = f"| {e['periodo']} | {e['n']} | {pcts[0]}% | {pcts[1]}% | {pcts[2]}% |"
            negrita = f"| {e['periodo']} | {e['n']} | {pcts[0]}% | {pcts[1]}% | **{pcts[2]}%** |"
            self.assertIn(plana if plana in self.doc else negrita, self.doc)
            self.assertAlmostEqual(c['DOVISH'] / len(sub), e['DOVISH'], places=3)

    def test_h2_fuga_por_sesion(self):
        f = self.aud['fuga_por_sesion']
        self.assertEqual(self.coma(f['fraccion_sesiones_repartidas_en_varios_pliegues']), '0,907')
        self.assertEqual(self.coma(f['macro_f1_cv_por_turno'], 4), '0,6848')
        self.assertEqual(self.coma(f['macro_f1_cv_por_sesion'], 4), '0,6724')
        for cifra in ('90,7%', '0,6848', '0,6724', '−0,0124', '0,0183'):
            self.assertIn(cifra, self.doc)

    def test_h3_fiabilidad(self):
        self.assertEqual(self.coma(self.rui['kappa']), '0,582')
        for cifra in ('0,582', '0,667', '0,80'):
            self.assertIn(cifra, self.doc)

    def test_h4_validez_de_constructo(self):
        v = self.aud['validez_de_constructo']
        x = v['extraccion_de_decisiones']
        self.assertEqual((x['sesiones_con_decision'], x['sesiones_del_corpus']), (104, 132))
        self.assertEqual(x['transiciones_consecutivas_comparadas'], 92)
        # es la lista de casos incoherentes, no un conteo: vacía = cero incoherencias
        self.assertEqual(x['incoherencias_verbo_nivel'], [])
        self.assertIn('104 de 132', self.doc)
        self.assertIn('92 transiciones', self.doc)
        for k, esp in (('contemporanea_con_anuncio', '+0,788'),
                       ('contemporanea_sin_anuncio', '+0,705'),
                       ('tono_t_contra_decision_t1', '+0,615')):
            self.assertEqual(f"{v[k]['spearman']:+.3f}".replace('.', ','), esp)
            self.assertIn(esp, self.doc)
            m = v[k]['tono_medio_por_decision']
            for kk, s in (('ALZA', '+'), ('SIN_CAMBIO', '−'), ('RECORTE', '−')):
                self.assertIn(f"{s}{abs(m[kk]['tono_medio']):.3f}".replace('.', ','), self.doc)

    def test_h6_deriva_temporal(self):
        e = self.der['expansiva']
        self.assertEqual(self.coma(e['macro_f1_medio']), '0,456')
        # la base de la deriva debe ser la misma cifra que el rolling-origin de H1
        self.assertEqual(e['macro_f1_medio'],
                         self.aud['generalizacion_temporal']['macro_f1_medio'])
        self.assertIn(str(round(e['n_entrena_medio'])), self.doc)
        for d in self.der['deslizantes']:
            self.assertIn(self.coma(d['macro_f1_medio']), self.doc)
            self.assertIn(str(round(d['n_entrena_medio'])), self.doc)
            self.assertIn(f"{d['gana_en']}/8", self.doc)
        self.assertEqual(self.der['veredicto'], 'REFUTADA')
        self.assertIn('**Refutada', self.doc)

    def test_h7_calibracion(self):
        c = self.cal['candidatos']
        self.assertTrue(c['max_prob']['monotona'])
        self.assertFalse(c['margen']['monotona'])
        self.assertFalse(c['abs_score']['monotona'])
        # no basta con que el artefacto diga 0,041: el documento tiene que citarlo
        self.assertEqual(self.coma(c['max_prob']['ece']), '0,041')
        self.assertEqual(self.coma(c['margen']['ece']), '0,091')
        # assertIn no basta: '0,041' aparece 3 veces en el documento, así que
        # mutar la fila de la tabla pasaría inadvertido. Se ata la fila completa.
        filas = {
            'max_prob': '| **max-prob** (p de la clase predicha) | **s\u00ed** | **{ece}** | usable |',
            'margen': '| `Margen` (p\u2081 \u2212 p\u2082) \u2014 publicada | no | {ece} | no usable |',
        }
        for cand, plantilla in filas.items():
            self.assertIn(plantilla.format(ece=self.coma(c[cand]['ece'])), self.doc)
        for f in c['max_prob']['curva']:
            self.assertIn(self.coma(f['precision_real']), self.doc)
        bajo = next(z for z in c['margen']['curva'] if z['cubo'] == '[0.30,0.50)')
        self.assertIn(self.coma(bajo['confianza_media']), self.doc)
        self.assertIn(self.coma(bajo['precision_real']), self.doc)
        self.assertEqual(f"{bajo['gap']:+.3f}".replace('.', ','), '+0,288')
        self.assertIn('166 de las 500', self.doc)

    def test_los_tres_hallazgos_nuevos_estan_en_ambos_documentos(self):
        inf = (DOCS / 'HAWKISH_DOVISH_V1_2026-09-11.md').read_text(encoding='utf-8')
        for t in (self.doc, inf):
            self.assertIn('0,456', t)
        for cifra in ('0,925', '0,806', 'max-prob'):
            self.assertIn(cifra, inf)
        self.assertIn('max-prob', self.doc)



class ConfianzaPublicadaTests(unittest.TestCase):
    """La columna HD_Confianza_Modelo del release: la medida calibrada, ahora publicada.

    Cierra la prioridad nº6 de la auditoría. El release publicaba dos medidas de
    confianza mal calibradas (Margen y |HD_Score_Modelo|) y no la buena.
    """

    @classmethod
    def setUpClass(cls):
        with (RELEASE / 'puntajes_hawkish_dovish.csv').open(newline='', encoding='utf-8') as fh:
            cls.filas = list(csv.DictReader(fh))
        cls.cal = json.loads((RELEASE / 'calibracion_confianza.json').read_text(encoding='utf-8'))

    def test_la_columna_esta_publicada_y_cubre_todo_el_corpus(self):
        self.assertIn('HD_Confianza_Modelo', self.filas[0])
        self.assertEqual(len(self.filas), 9257)
        self.assertTrue(all(r['HD_Confianza_Modelo'] for r in self.filas))

    def test_es_una_probabilidad_y_domin_al_margen(self):
        for r in self.filas:
            c = float(r['HD_Confianza_Modelo'])
            self.assertGreaterEqual(c, 1 / 3 - 1e-9)
            self.assertLessEqual(c, 1.0)
            # la p mayor nunca puede ser menor que la diferencia entre las dos mayores
            self.assertGreaterEqual(c, float(r['Margen']) - 1e-9)

    def test_reproducible_desde_el_json_del_modelo(self):
        # no basta con que la columna exista: tiene que salir del modelo publicado
        m = json.loads((RELEASE / 'modelo_hawkish_dovish.json').read_text(encoding='utf-8'))
        modelo = {'W': m['pesos'], 'b': m['sesgo']}
        indice = {t: i for i, t in enumerate(m['vocabulario'])}
        idf = m['idf']
        turnos = hd.cargar_turnos()
        por_id = {r['ID_Turno']: r for r in self.filas}
        for t in turnos[:400]:
            r = por_id[t['ID_Turno']]
            doc = ent.rasgos_texto(t['Texto'])
            v = {}
            for tt, tf in doc.items():
                i = indice.get(tt)
                if i is not None:
                    v[i] = (1 + math.log(tf)) * idf[i]
            norma = math.sqrt(sum(w * w for w in v.values())) or 1.0
            pred = ent.predecir(modelo, {i: w / norma for i, w in v.items()})
            self.assertEqual(round(max(pred['probs']), 4),
                             float(r['HD_Confianza_Modelo']),
                             t['ID_Turno'])
            self.assertEqual(pred['clase'], r['HD_Clase_Modelo'])

    def test_es_la_medida_calibrada_no_las_que_ya_estaban(self):
        c = self.cal['candidatos']
        self.assertTrue(c['max_prob']['monotona'])
        self.assertFalse(c['margen']['monotona'])
        self.assertFalse(c['abs_score']['monotona'])

    def test_la_recomendacion_del_informe_apunta_a_la_columna_publicada(self):
        inf = (DOCS / 'HAWKISH_DOVISH_V1_2026-09-11.md').read_text(encoding='utf-8')
        # el informe ya no debe decir que max-prob "no está publicada"
        self.assertIn('HD_Confianza_Modelo', inf)
        self.assertNotIn('no está publicada pero se recalcula', inf)



class ValidacionPorSesionTests(unittest.TestCase):
    """La CV agrupada por sesión, publicada junto a la aleatoria por turno.

    Prioridad nº5 de la auditoría. La aleatoria baraja por turno y reparte el 90,7%
    de las 130 sesiones en más de un pliegue, así que filtra información. Se publica
    la cifra limpia AL LADO de la otra, no en su lugar: el release v1 está hasheado y
    reescribir sus titulares sería publicar un v2, no parchear v1.
    """

    @classmethod
    def setUpClass(cls):
        cls.res = json.loads((RELEASE / 'resumen_entrenamiento.json').read_text(encoding='utf-8'))
        cls.aud = json.loads((RELEASE / 'auditoria_metodologica.json').read_text(encoding='utf-8'))
        cls.vt = cls.res['validacion_cruzada']
        cls.vs = cls.res['validacion_cruzada_por_sesion']

    def test_la_particion_no_parte_ninguna_sesion(self):
        et = json.loads(ETIQUETAS.read_text(encoding='utf-8'))['Etiquetas']
        sesiones = [e['ID_Turno'].split(':')[0] for e in et]
        p = ent.pliegues_por_sesion(sesiones, 5, 0)
        self.assertEqual(sum(len(f) for f in p), len(sesiones))
        de_que = {}
        for f, fold in enumerate(p):
            for i in fold:
                de_que.setdefault(sesiones[i], set()).add(f)
        self.assertEqual(sum(1 for v in de_que.values() if len(v) > 1), 0)

    def test_coincide_con_la_particion_que_midio_la_auditoria(self):
        # si difirieran, el 0,682 y el 0,6724 de la auditoria no serian comparables
        et = json.loads(ETIQUETAS.read_text(encoding='utf-8'))['Etiquetas']
        y = [e['HD_Clase'] for e in et]
        sesiones = [e['ID_Turno'].split(':')[0] for e in et]
        for sem in range(5):
            propia = [sorted(f) for f in ent.pliegues_por_sesion(sesiones, 5, sem)]
            ajena = [sorted(f) for f in aud.particion_sesion(y, sesiones, 5, sem)]
            self.assertEqual(propia, ajena, f'semilla {sem}')

    def test_agrupar_por_sesion_baja_el_numero(self):
        self.assertLess(self.vs['macro_f1'], self.vt['macro_f1'])
        self.assertEqual((self.vt['macro_f1'], self.vs['macro_f1']), (0.702, 0.682))
        # los baselines no dependen de la particion: predicen igual en ambas
        self.assertEqual(self.vs['baseline_lexico']['macro_f1'],
                         self.vt['baseline_lexico']['macro_f1'])
        self.assertEqual(self.vs['baseline_mayoria']['macro_f1'],
                         self.vt['baseline_mayoria']['macro_f1'])

    def test_no_cambia_el_modelo_publicado_ni_la_configuracion(self):
        # la regla de seleccion elige la misma configuracion con ambas particiones,
        # asi que el modelo hasheado no se mueve
        self.assertEqual(self.res['sha256_modelo'][:16], 'b631f10fd59a8ade')
        self.assertEqual(self.res['configuracion_publicada']['max_rasgos'], 600)
        self.assertEqual(self.res['configuracion_publicada']['iteraciones'], 30)
        self.assertTrue(self.res['configuracion_publicada']['balancear_clases'])

    def test_la_cifra_limpia_queda_documentada_en_el_informe(self):
        inf = (DOCS / 'HAWKISH_DOVISH_V1_2026-09-11.md').read_text(encoding='utf-8')
        self.assertIn('0,682', inf)
        self.assertIn('validacion_cruzada_por_sesion', inf)



class ContrasteLexicoPublicadoTests(unittest.TestCase):
    """Prioridad nº4: validez convergente contra un léxico publicado.

    El contraste pleno no es realizable y la prueba fija también eso: que el
    artefacto declare por qué, en vez de dejarlo como una omisión silenciosa.
    """

    @classmethod
    def setUpClass(cls):
        cls.res = json.loads(
            (RELEASE / 'contraste_lexico_publicado.json').read_text(encoding='utf-8'))

    def test_cobertura_de_dominios_recalculada(self):
        frases = [p for _, p in hd.HAWKISH] + [p for _, p in hd.DOVISH]
        for d in self.res['detalle_dominios']:
            esperado = bool(lexpub.DOMINIOS[[x[0] for x in lexpub.DOMINIOS].index(d['dominio'])][1]
                            and [p for p in frases
                                 if any(x in p for x in dict(lexpub.DOMINIOS)[d['dominio']])])
            self.assertEqual(d['cubierto_por_lexico_propio'], esperado, d['dominio'])
        self.assertEqual(self.res['dominios_cubiertos'], 7)
        self.assertEqual(self.res['dominios_publicados'], 11)

    def test_los_dominios_ausentes_son_los_medidos(self):
        self.assertEqual(self.res['dominios_ausentes'],
                         ['wage', 'oil price', 'development', 'recovery'])

    def test_no_hay_punto_ciego_porque_el_universo_esta_peor(self):
        # la brecha solo importaria si esos turnos quedaran mas a ciegas que el
        # promedio; quedan menos, porque la señal les llega por otro dominio
        base = self.res['baseline_universo']['fraccion_sin_senal_universo']
        self.assertAlmostEqual(base, 0.418, places=3)
        for nombre in self.res['dominios_ausentes']:
            d = next(x for x in self.res['detalle_dominios'] if x['dominio'] == nombre)
            self.assertLess(d['fraccion_de_esos_sin_senal'], base, nombre)
        self.assertFalse(self.res['hay_punto_ciego_medible'])
        self.assertEqual(self.res['veredicto'], 'BRECHA REAL, IMPACTO NO MEDIBLE')

    def test_el_artefacto_declara_por_que_el_contraste_pleno_no_es_posible(self):
        self.assertFalse(self.res['contraste_pleno_posible'])
        unido = ' '.join(self.res['por_que_no'])
        # las dos razones de fondo: sin serie de mercado, y léxicos publicados en inglés
        self.assertIn('mercado', unido)
        self.assertIn('ingleses', unido)
        self.assertIn('circularidad', unido)
        self.assertTrue(self.res['limites'])

    def test_el_baseline_se_recalcula_desde_el_corpus(self):
        turnos = hd.cargar_turnos()
        universo = [t for t in turnos
                    if t['Naturaleza_Turno'] == 'INTERVENCION' and t['Palabras'] >= 150]
        b = self.res['baseline_universo']
        self.assertEqual(b['turnos_universo'], len(universo))
        self.assertEqual(b['palabras_universo'], sum(t['Palabras'] for t in universo))
        sin = sum(1 for t in universo if hd.puntuar_lexico(t['Texto'])['score'] == 0.0)
        self.assertEqual(b['sin_senal_lexica'], sin)



class EnsemblePorSesionTests(unittest.TestCase):
    """El veredicto del ensemble, bajo la partición agrupada por sesión.

    El hallazgo 2 mostró que la CV por turno filtra entre sesiones. Eso deja una
    pregunta sobre todo veredicto publicado que descanse en esa CV: ¿la fuga lo
    sostiene? Para el ensemble la respuesta es que no lo sostiene —sobrevive y se
    refuerza—, pero sólo si se mira el comparador correcto.
    """

    @classmethod
    def setUpClass(cls):
        cls.res = json.loads((RELEASE / 'ensemble_por_sesion.json').read_text(encoding='utf-8'))
        cls.pub = json.loads((RELEASE / 'ensemble_anidado.json').read_text(encoding='utf-8'))

    def test_el_veredicto_publicado_se_mantiene(self):
        self.assertTrue(self.res['el_veredicto_se_mantiene'])
        self.assertEqual(self.res['veredicto_publicado'], 'la mezcla no mejora al modelo')
        self.assertEqual(self.res['veredicto_por_sesion'], 'la mezcla no mejora al modelo')

    def test_el_comparador_tecnico_cambia_de_signo_pero_es_ruido(self):
        tec = self.res['comparadores']['mezcla_menos_umbral']
        self.assertTrue(tec['cambia_de_signo'])
        self.assertLess(tec['por_turno'], 0)
        self.assertGreater(tec['por_sesion'], 0)
        # ambos son del orden de la sd: no es un efecto, es ruido
        self.assertLess(abs(tec['por_turno']), self.pub['desviacion_diferencia'])
        self.assertLess(abs(tec['por_sesion']), self.res['por_sesion']['desviacion_diferencia'])

    def test_el_comparador_decisorio_no_cambia_de_signo_y_se_agranda(self):
        dec = self.res['comparadores']['mezcla_menos_argmax']
        self.assertFalse(dec['cambia_de_signo'])
        self.assertLess(dec['por_turno'], 0)
        self.assertLess(dec['por_sesion'], dec['por_turno'])

    def test_la_mezcla_no_supera_a_la_regla_publicada_en_ninguna_particion(self):
        # argmax es la regla que el release publica; ésa es la comparación que decide
        p = self.res['por_sesion']
        self.assertLess(p['macro_f1_medio_mezcla'], p['macro_f1_medio_argmax'])
        self.assertLess(self.pub['macro_f1_medio_mezcla'], self.pub['macro_f1_medio_argmax'])

    def test_el_documento_lo_recoge_y_cita_el_script(self):
        doc = (DOCS / 'AUDITORIA_HAWKISH_DOVISH_V1_2026-09-11.md').read_text(encoding='utf-8')
        self.assertIn('## Hallazgo 9 — La fuga por sesión no sostiene ningún veredicto publicado', doc)
        self.assertIn('probar_ensemble_por_sesion_hawkish_dovish.py', doc)
        # los dos comparadores, con sus cifras, deben estar visibles: ése es el punto del hallazgo
        self.assertIn('mezcla − umbral', doc)
        self.assertIn('mezcla − argmax', doc)
        self.assertIn('+0,0030', doc)
        self.assertIn('−0,0332', doc)

    def test_el_encuadre_cita_los_artefactos_que_existen(self):
        # El número de hallazgos crece con cada medición nueva, así que atar la
        # cifra entera en el texto obliga a editar la prueba cada vez. Lo que sí
        # hay que atar es que cada artefacto y script citados existan de verdad.
        doc = (DOCS / 'AUDITORIA_HAWKISH_DOVISH_V1_2026-09-11.md').read_text(encoding='utf-8')
        self.assertIn('`ensemble_por_sesion.json`', doc)
        self.assertIn('`probar_ensemble_por_sesion_`', doc)
        for a in ('auditoria_metodologica.json', 'ruido_oro.json', 'efecto_ventana.json',
                  'deriva_temporal.json', 'calibracion_confianza.json',
                  'contraste_lexico_publicado.json', 'ensemble_por_sesion.json',
                  'rendimiento_reponderado.json'):
            self.assertIn(a, doc, a)
            self.assertTrue((RELEASE / a).exists(), a)

    def test_el_encuadre_concuerda_con_los_hallazgos_y_artefactos_reales(self):
        # atado al conteo real, no a una cifra escrita a mano
        import re
        doc = (DOCS / 'AUDITORIA_HAWKISH_DOVISH_V1_2026-09-11.md').read_text(encoding='utf-8')
        n_hallazgos = len(re.findall(r'(?m)^## Hallazgo \d+ —', doc))
        cab = doc.split('\n\n')[1]
        n_json = len(re.findall(r'`([a-z_0-9]+\.json)`', cab))
        n_scripts = len(re.findall(r'`([a-z_0-9]+)_`', cab))
        self.assertEqual(n_hallazgos, 10)
        self.assertEqual(n_json, n_hallazgos - 2)   # H5 y H6 no producen artefacto propio
        self.assertEqual(n_scripts, n_json)
        palabras = {8: 'Ocho', 9: 'Nueve', 10: 'Diez', 11: 'Once'}
        self.assertIn(f'**{palabras[n_hallazgos]} hallazgos**', doc)

    def test_solo_cambio_la_particion_no_el_procedimiento(self):
        # mismo harness: pesos candidatos, pliegues, semillas y config publicados
        self.assertEqual(self.res['config_publicada'], self.pub['config_publicada'])
        self.assertEqual(self.res['semillas'], self.pub['semillas'])
        self.assertIn('solo la partición', self.res['cambio_respecto_del_harness_publicado'])
        self.assertEqual(len(self.res['por_sesion']['por_semilla']), self.res['semillas'])


class RendimientoReponderadoTests(unittest.TestCase):
    """El rendimiento publicado, reponderado por el diseño de muestreo.

    Las 500 etiquetas se sortearon por decil léxico x anio x grupo con cuotas no
    proporcionales, y el docstring de `muestra()` ya advierte que eso no sirve
    para estimar prevalencia. La prevalencia se reponderó; el rendimiento nunca.
    Aquí se mide: el efecto existe pero es chico y va en contra del publicado,
    así que el 0,702 no está inflado por el diseño.
    """

    @classmethod
    def setUpClass(cls):
        cls.res = json.loads((RELEASE / 'rendimiento_reponderado.json').read_text(encoding='utf-8'))
        cls.pub = json.loads((RELEASE / 'resumen_entrenamiento.json').read_text(encoding='utf-8'))

    def test_los_dos_controles_internos_pasan(self):
        # el decil recalculado debe coincidir con el declarado en la muestra,
        # y el acierto recalculado con la columna Acierta del CSV
        self.assertTrue(self.res['deciles_control_coinciden'])
        self.assertEqual(self.res['deciles_control_desacuerdos'], [])
        self.assertTrue(self.res['acierto_recalculado_coincide_con_el_csv'])
        self.assertEqual(self.res['acierto_recalculado_desacuerdos'], [])

    def test_la_accuracy_recalculada_es_la_publicada(self):
        self.assertAlmostEqual(self.res['accuracy_sin_ponderar'],
                               self.pub['validacion_cruzada']['accuracy'], places=4)

    def test_el_macro_f1_sin_ponderar_reproduce_el_publicado(self):
        self.assertAlmostEqual(self.res['macro_f1_recalculado_sin_ponderar'],
                               self.res['macro_f1_publicado'], delta=0.001)

    def test_reponderar_no_cambia_materialmente_el_veredicto(self):
        # éste es el hallazgo: el efecto existe pero es chico y sube, no baja
        dif = self.res['diferencia_reponderado_menos_publicado']
        self.assertGreater(dif, 0)
        self.assertLess(dif, 0.02)

    def test_el_disenio_sobremuestrea_los_deciles_extremos(self):
        d = {x['decil']: x for x in self.res['por_decil']}
        # extremos con peso < 1 (sobremuestreados), centro con peso > 1
        self.assertLess(d[1]['peso_disenio'], 1)
        self.assertLess(d[10]['peso_disenio'], 1)
        self.assertGreater(d[6]['peso_disenio'], 1.5)
        self.assertGreater(d[7]['peso_disenio'], 1.5)

    def test_los_pesos_suman_el_total_de_etiquetas(self):
        self.assertAlmostEqual(self.res['suma_pesos'], float(self.res['etiquetas']), delta=0.01)


if __name__ == '__main__':
    unittest.main(verbosity=2)
