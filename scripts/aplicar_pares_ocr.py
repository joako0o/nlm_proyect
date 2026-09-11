#!/usr/bin/env python3
"""Construye un lote de correcciones a partir de pares «forma dañada -> forma buena».

Existe porque el builder de lotes vivía en ``.cache/`` y el workspace se ha
reiniciado diez veces, borrándolo. Cada vez hubo que reescribirlo, y cada
reescritura reintrodujo algún bug ya conocido. Ahora está versionado.

No aplica nada: escribe un lote JSON para ``agregar_correcciones_ocr.py``.

Reglas que aplica, todas aprendidas a golpes:

1. **``Antes`` se compone sobre el texto virgen**, no sobre la salida. El
   validador exige que cada ``Antes`` aparezca exactamente las veces declaradas
   en la fila original.
2. **Una ``Antes`` no puede ser substring de otra** ni solaparse con una
   operación ya registrada: reescribiría ocurrencias ajenas.
3. **Las repeticiones dentro de una misma fila se tratan todas.** Un dedupe por
   forma corregía sólo la primera y dejaba el resto: se detectó porque la salida
   daba 6 cuando el detector ya decía 0.
4. **«Sigue viva» se cuenta por ocurrencia, no por fila**, y una operación
   registrada sólo la resuelve si la cubre **por completo**: si corta a mitad de
   palabra, el defecto sobrevive.
5. **El orden importa** cuando una forma es prefijo de otra: hay que ir de más
   larga a más corta.

Uso::

    python scripts/aplicar_pares_ocr.py pares.json -o lote.json
    python scripts/aplicar_pares_ocr.py pares.json -o lote.json --aplicar
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import correcciones_ocr_v1 as core  # noqa: E402
from diagnosticar_finales import read_rows  # noqa: E402


LETRA = set('ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜÑabcdefghijklmnopqrstuvwxyzáéíóúüñ')


def ocurrencias(texto: str, frag: str) -> list[int]:
    """Posiciones de ``frag`` en ``texto`` respetando frontera de palabra.

    Imprescindible: sin frontera, el par ``ultimo`` -> ``último`` empareja dentro
    de ``multimodal`` y lo convierte en ``múltimodal``, que está mal (el prefijo
    multi- no se acentúa). Ocurrió de verdad en 4 operaciones de §16 grupo B1 y
    hubo que retirarlas. Los conteos por substring sin delimitar ya habían
    mordido antes en otras partes del proyecto.
    """
    out, pos = [], texto.find(frag)
    while pos >= 0:
        antes = texto[pos - 1] if pos > 0 else ' '
        despues = texto[pos + len(frag)] if pos + len(frag) < len(texto) else ' '
        if antes not in LETRA and despues not in LETRA:
            out.append(pos)
        pos = texto.find(frag, pos + 1)
    return out


def construir(pares: dict[str, str], tipo: str, justificacion: str,
              aplicar: bool) -> int:
    reg = core.cargar()
    ok, problemas, corregidas, _ = core.validar(reg=reg, base=core.BASE)
    if not ok:
        for p in problemas[:10]:
            print('ERROR:', p)
        return 1
    bx = {r['ID_Intervencion']: r for r in read_rows(core.BASE)}
    base = {k: (r['Texto'] or '') for k, r in bx.items()}
    salida = {rid: corregidas.get(rid, t) for rid, t in base.items()}
    exis = {e['ID_Intervencion']: e for e in reg['Correcciones']}

    # regla 5: de más larga a más corta
    orden = sorted(pares, key=len, reverse=True)

    viva = defaultdict(int)
    for rid, t in salida.items():
        for malo in orden:
            viva[malo] += len(ocurrencias(t, malo))
    print('apariciones vivas en la salida: %d | formas: %d'
          % (sum(viva.values()), sum(1 for m in orden if viva[m])))
    sin = [m for m in orden if viva[m] == 0]
    if sin:
        print('  sin apariciones (revisar el par):', sin)

    def ops_de(rid):
        return exis.get(rid, {}).get('Operaciones', [])

    def resuelta(rid, f0, f1, malo):
        """True si una operación registrada cubre TOTALMENTE y ya lo resuelve."""
        t = base[rid]
        for o in ops_de(rid):
            j = t.find(o['Antes'])
            if j >= 0 and j <= f0 and f1 <= j + len(o['Antes']) and malo not in o['Despues']:
                return True
        return False

    por_fila = defaultdict(list)
    for rid, t in sorted(base.items()):
        for malo in orden:
            buenas = len(ocurrencias(salida[rid], malo))
            if not buenas:
                continue
            coladas = 0
            for pos in ocurrencias(t, malo):
                if coladas >= buenas:
                    break
                f0, f1 = pos, pos + len(malo)
                if not resuelta(rid, f0, f1, malo):
                    por_fila[rid].append((f0, f1, pares[malo]))
                    coladas += 1

    ops, saltadas = [], 0
    for rid, items in sorted(por_fila.items()):
        t = base[rid]
        items.sort(key=lambda x: x[0])
        ocupados = []
        for o in ops_de(rid):
            j = t.find(o['Antes'])
            if j >= 0:
                ocupados.append((j, j + len(o['Antes'])))
        previas = [o['Antes'] for o in ops_de(rid)]
        usados = []
        for a, b, nuevo in items:
            # Ventanas a probar. La tercera existe porque si una operación ya
            # registrada termina justo antes del defecto, la ventana amplia se
            # solapa con ella y la estrecha no es única (caso «que podrian …»
            # repetido dos veces en 2857:1): hay que anclar a la derecha del
            # tramo que bloquea.
            izq = max(0, a - 20)
            for x, y in ocupados + usados:
                if izq < y and x < b + 16 and y <= a:
                    izq = max(izq, y)
            candidatas = ((max(0, a - 20), min(len(t), b + 16)),
                          (izq, min(len(t), b + 16)),
                          (max(0, a - 1), min(len(t), b + 1)))
            elegido = None
            for ia, ib in candidatas:
                antes = t[ia:ib]
                if t.count(antes) != 1:
                    continue
                if any(p and (p in antes or antes in p) for p in previas):
                    continue
                if any(ia < y and x < ib for x, y in ocupados + usados):
                    continue
                elegido = (ia, ib)
                break
            if elegido is None:
                saltadas += 1
                print('  SALTADA %s %r' % (rid, t[a:b]))
                continue
            ia, ib = elegido
            antes = t[ia:ib]
            despues = t[ia:a] + nuevo + t[b:ib]
            if antes == despues:
                saltadas += 1
                continue
            ops.append({'ID_Intervencion': rid, 'Tipo': tipo, 'Antes': antes,
                        'Despues': despues, 'Ocurrencias': 1,
                        'Contexto': t[max(0, ia - 60):ib + 40].replace('\n', ' '),
                        'Justificacion': justificacion})
            usados.append((ia, ib))
            previas.append(antes)

    por_id = defaultdict(list)
    for o in ops:
        por_id[o.pop('ID_Intervencion')].append(o)
    lote = {'Correcciones': [
        {'ID_Intervencion': rid, 'Fecha': bx[rid]['Fecha'].strftime('%Y-%m-%d'),
         'Actor': bx[rid]['Actor_Final'], 'Operaciones': v}
        for rid, v in sorted(por_id.items())],
        'Revisiones_Sin_Correccion': []}
    return lote, len(ops), len(por_id), saltadas


def extender_cubiertas(pares: dict[str, str], nota: str) -> int:
    """Resuelve lo que el builder salta porque una operación ya cubre el sitio.

    Cuando una operación registrada cubre el defecto **parcialmente** —su
    ``Antes`` corta a mitad de palabra— el defecto sobrevive aunque el fragmento
    no aparezca literal en el ``Despues``, y el builder no puede añadir una
    operación nueva sin solaparse. La salida no es forzarla: es **extender** la
    operación existente. Nuevo ``Antes`` = unión de tramos; nuevo ``Despues`` =
    trozo izquierdo + ``Despues`` viejo + trozo derecho, y sobre eso se aplica el
    par. Es la misma regla que resolvió ``3703:1`` y las 5 de §16.
    """
    reg = core.cargar()
    base = {r['ID_Intervencion']: (r['Texto'] or '') for r in read_rows(core.BASE)}
    exis = {e['ID_Intervencion']: e for e in reg['Correcciones']}
    n = 0
    for rid, entrada in exis.items():
        t = base[rid]
        for malo, bueno in pares.items():
            for pos in ocurrencias(t, malo):
                f0, f1 = pos, pos + len(malo)
                cubre = x = y = None
                for o in entrada['Operaciones']:
                    j = t.find(o['Antes'])
                    if j >= 0 and j < f1 and f0 < j + len(o['Antes']):
                        cubre, x, y = o, j, j + len(o['Antes'])
                        break
                if cubre is None:
                    continue
                total = x <= f0 and f1 <= y
                if total and malo not in cubre['Despues']:
                    continue                       # ya resuelta
                x2, y2 = min(x, f0), max(y, f1)
                choca = False
                for o in entrada['Operaciones']:
                    if o is cubre:
                        continue
                    j = t.find(o['Antes'])
                    if j >= 0 and j < y2 and x2 < j + len(o['Antes']):
                        choca = True
                        break
                if choca:
                    print('  COLISION %s %r: no se puede extender' % (rid, malo))
                    continue
                na = t[x2:y2]
                if t.count(na) != 1:
                    print('  NO UNICA %s %r' % (rid, na))
                    continue
                nd = (t[x2:x] + cubre['Despues'] + t[y:y2]).replace(malo, bueno, 1)
                if na == nd or malo in nd:
                    continue
                cubre['Antes'], cubre['Despues'] = na, nd
                cubre['Justificacion'] += nota
                n += 1
                print('  extendida %-22s %-14s -> %r' % (rid, malo, na[:44]))
    if n:
        core.REGISTRO.write_text(
            json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('operaciones extendidas:', n)
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('pares', type=Path, help='JSON {"Pares": {...}, "Tipo": ..., "Justificacion": ...}')
    ap.add_argument('-o', '--salida', type=Path, required=True)
    ap.add_argument('--aplicar', action='store_true',
                    help='fusionar el lote en el registro con --parche al terminar')
    ap.add_argument('--extender', action='store_true',
                    help='en vez de construir un lote, extender las operaciones que '
                         'cubren parcialmente un defecto y por eso lo dejan vivo')
    a = ap.parse_args()
    cfg = json.loads(a.pares.read_text(encoding='utf-8'))
    if a.extender:
        extender_cubiertas(cfg['Pares'], ' | ' + cfg.get('Nota_Extension',
            'Se extiende esta operación ya registrada en vez de añadir otra: el defecto '
            'cae dentro del mismo tramo y dos defectos en un mismo tramo se resuelven '
            'extendiendo, no apilando.'))
        return 0
    lote, n, filas, saltadas = construir(cfg['Pares'], cfg['Tipo'], cfg['Justificacion'], a.aplicar)
    a.salida.write_text(json.dumps(lote, ensure_ascii=False, indent=1), encoding='utf-8')
    print('operaciones: %d | filas: %d | saltadas: %d' % (n, filas, saltadas))
    print('escrito:', a.salida)
    if n == 0:
        return 0
    if a.aplicar:
        import subprocess
        r = subprocess.run([sys.executable, 'scripts/agregar_correcciones_ocr.py',
                            str(a.salida), '--parche'], capture_output=True, text=True)
        print(r.stdout.strip())
        if r.returncode != 0:
            print(r.stderr.strip())
        return r.returncode
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
