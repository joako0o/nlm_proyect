"""
Descarga las Actas de las Reuniones de Política Monetaria (RPM) desde el
repositorio digital del Banco Central de Chile, usando el navegador de la
máquina local para sortear el bloqueo anti-bot (Incapsula).

Basado en el script que compartiste, con estos arreglos:
  - Corregido el typo `item['href']..startswith` -> `startswith`.
  - URLs resueltas con `urljoin` (evita URLs relativas mal formadas).
  - Nombre de archivo incluye AÑO + sesión: `Acta_RPM_2013_N205.pdf`.
    (El nombre original solo usaba la sesión y podía colisionar entre años.)
  - Descubrimiento dinámico de las colecciones anuales desde la página
    principal (para no depender de handles y para incluir 2015+).
  - `No.\s*(\d+)` solo se usa como respaldo; primero se extrae el número
    desde el título del ítem (más confiable).
  - Reintentos de descarga y comprobación de cabecera `%PDF`.
  - Muestra progreso y guarda un manifest JSON.

Uso (en tu máquina, con Python y Playwright instalados):

    python descargar_actas_rpm.py
    python descargar_actas_rpm.py --output-dir "D:/RPM/Actas" --years 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015
    python descargar_actas_rpm.py --years 2005 --solo-faltantes

Cuando Incapsula pida verificación humana, el script abre el navegador para
que completes el captcha; luego continúa solo.
"""

import argparse
import asyncio
import json
import os
import re
import sys
from datetime import datetime
from urllib.parse import urljoin

from playwright.async_api import async_playwright

# Rutas por defecto (puedes cambiarlas con argumentos CLI).
DEFAULT_OUTPUT_DIR = r"C:\Users\joaqu\Desktop\RPM_HawkDove\data\pdfs\Actas"
DEFAULT_USER_DATA = r"C:\Users\joaqu\Desktop\RPM_HawkDove\extraccion_limpia\browser_data"

REPOSITORY_ROOT = "https://repositoriodigital.bcentral.cl/xmlui/handle/20.500.12580/4514"

# Handles conocidos; se usan como respaldo si el descubrimiento dinámico falla.
FALLBACK_COLLECTIONS = {
    "2005": "4529",
    "2006": "4530",
    "2007": "4525",
    "2008": "4521",
    "2009": "6087",
    "2010": "7034",
    "2011": "7483",
    "2012": "7987",
    "2013": "10450",
    "2014": "10677",
}

TITLE_SESSION_RE = re.compile(r"RPM\s+N?[°ºo.]?\s*(\d+)", re.IGNORECASE)
BODY_SESSION_RE = re.compile(r"(?:Sesión|Sesi\u00f3n|Sesion|No\.)\s+N?[°ºo.]?\s*(\d+)", re.IGNORECASE)
YEAR_RE = re.compile(r"RPM\s+(20\d{2})\b", re.IGNORECASE)


def q(text: str) -> str:
    """Abreviar texto largo para logs."""
    text = text or ""
    return text if len(text) <= 80 else text[:77] + "..."


def is_pdf(body: bytes) -> bool:
    return body[:4] == b"%PDF"


async def wait_until_verification_passes(page, timeout_minutes: float = 6.0):
    """Si Incapsula muestra 'Verificación', espera a que el usuario la resuelva."""
    title = await page.title()
    if "Verificaci" not in title:
        return

    print(">>> Detecté la pantalla de verificación humana.")
    print(">>> Completa el captcha en el navegador; el script continuará solo.")
    budget = timeout_minutes * 60.0
    waited = 0.0
    while waited < budget:
        await asyncio.sleep(2)
        waited += 2.0
        title = await page.title()
        if "Verificaci" not in title:
            print(">>> Verificación resuelta.")
            return
    print(">>> No se resolvió la verificación a tiempo; siguiendo de todos modos.")


async def discover_collections(page):
    """Devuelve {año: url_browse}. Primero intenta automático, luego respaldo."""
    try:
        await page.goto(REPOSITORY_ROOT, timeout=60000, wait_until="domcontentloaded")
        await asyncio.sleep(3)
        await wait_until_verification_passes(page)

        links = await page.eval_on_selector_all(
            "a[href*='/xmlui/handle/20.500.12580/']",
            """
            (links) => links.map(a => ({href: a.href, text: a.textContent.trim()}))
                .filter(x => /Actas y documentaci[oó]n RPM\\s+20\\d{2}/i.test(x.text))
            """,
        )

        collections = {}
        for link in links:
            m = YEAR_RE.search(link["text"]) or re.search(r"RPM\s+(20\d{2})\b", link["text"])
            if not m:
                continue
            year = m.group(1)
            browse_url = link["href"].split("?")[0] + "/browse?type=title"
            collections[year] = browse_url
        if collections:
            print(f"Colecciones descubiertas: {', '.join(sorted(collections))}")
            return collections
    except Exception as exc:  # noqa: BLE001 - la red/anti-bot puede fallar de muchas formas
        print(f"No se pudieron descubrir las colecciones automáticamente: {exc}")

    # Respaldo con handles conocidos.
    print("Usando handles de respaldo.")
    return {
        year: f"https://repositoriodigital.bcentral.cl/xmlui/handle/20.500.12580/{handle}/browse?type=title"
        for year, handle in FALLBACK_COLLECTIONS.items()
    }


async def scrape_items(page, browse_url: str):
    await page.goto(browse_url, timeout=60000, wait_until="domcontentloaded")
    await asyncio.sleep(2)
    await wait_until_verification_passes(page)

    raw = await page.eval_on_selector_all(
        "h4.artifact-title a, .artifact-title a, div.artifact-title a",
        """
        (anchors) => anchors.map(a => ({href: a.href, text: a.textContent.trim()}))
        """,
    )
    items = []
    seen = set()
    for item in raw:
        href = item.get("href") or ""
        text = item.get("text") or ""
        if not href or href in seen:
            continue
        seen.add(href)
        if not re.search(r"^RPM\s+(\d+|N[°ºo.]?)\s+", text, re.IGNORECASE) and \
           not re.search(r"^RPM\s+20\d{2}", text, re.IGNORECASE):
            continue
        items.append({"url": href, "title": text})
    return items


def extract_session(item: dict, page_body: str):
    m = TITLE_SESSION_RE.search(item["title"])
    if m:
        return m.group(1)
    m = BODY_SESSION_RE.search(page_body)
    if m:
        return m.group(1)
    return None


async def find_acta_bitstream(page, ctx_request):
    """Busca el link al PDF del acta dentro del item."""
    hrefs = await page.eval_on_selector_all(
        "a[href*='bitstream']",
        "(links) => links.map(a => a.href)",
    )
    if not hrefs:
        return None

    acta_like = [h for h in hrefs if re.search(r"acta", h, re.IGNORECASE)]
    candidates = acta_like or hrefs
    for href in candidates:
        try:
            response = await ctx_request.get(href)
            if response.ok:
                body = await response.body()
                if is_pdf(body):
                    return href
        except Exception:  # noqa: BLE001
            continue
    return None


async def download_acta(page, ctx_request, item_url: str, year: str, output_dir: str):
    await page.goto(item_url, timeout=60000, wait_until="domcontentloaded")
    await asyncio.sleep(1)
    await wait_until_verification_passes(page, timeout_minutes=1.0)

    page_body = await page.evaluate("() => document.body.innerText")
    sess = extract_session({"title": q("")}, page_body)  # respaldo por cuerpo
    # Reintentar con el título correcto del ítem:
    title = await page.title()
    sess = extract_session({"title": title}, page_body) or sess

    if not sess:
        return None

    filename = f"Acta_RPM_{year}_N{sess}.pdf"
    filepath = os.path.join(output_dir, filename)
    if os.path.exists(filepath):
        return {"filename": filename, "reason": "ya_existia"}

    bitstream_href = await find_acta_bitstream(page, ctx_request)
    if not bitstream_href:
        return {"filename": filename, "reason": "sin_bitstream"}

    last_err = None
    for attempt in range(3):
        try:
            response = await ctx_request.get(bitstream_href, timeout=120000)
            if response.ok:
                body = await response.body()
                if is_pdf(body):
                    with open(filepath, "wb") as fh:
                        fh.write(body)
                    return {"filename": filename, "reason": "descargado", "size_kb": len(body) // 1024}
                last_err = "el archivo no tiene cabecera PDF"
            else:
                last_err = f"HTTP {response.status}"
        except Exception as exc:  # noqa: BLE001
            last_err = str(exc)
        await asyncio.sleep(2 * (attempt + 1))

    return {"filename": filename, "reason": f"fallo_descarga: {last_err}"}


async def main() -> int:
    parser = argparse.ArgumentParser(description="Descargar Actas RPM desde el repositorio BCCh.")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Carpeta donde guardar los PDFs.")
    parser.add_argument("--user-data", default=DEFAULT_USER_DATA, help="Perfil persistente de Chromium.")
    parser.add_argument("--years", nargs="*", default=None, help="Años a descargar, p.ej. --years 2005 2006 2007")
    parser.add_argument("--headless", action="store_true", help="No abrir ventana (no recomendado si hay captcha).")
    parser.add_argument("--manifest", default=None, help="JSON de resultados (por defecto dentro de output_dir).")
    args = parser.parse_args()

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    manifest_path = args.manifest or os.path.join(output_dir, "manifest_descarga.json")

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            args.user_data,
            headless=args.headless,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
            locale="es-CL",
        )
        page = context.pages[0] if context.pages else await context.new_page()

        collections = await discover_collections(page)
        if args.years:
            years = args.years
            collections = {y: url for y, url in collections.items() if y in years}
        else:
            years = sorted(collections, key=int)
        print(f"Años a procesar: {years}")

        results = []
        for year, browse_url in sorted(collections.items(), key=lambda kv: int(kv[0])):
            try:
                items = await scrape_items(page, browse_url)
            except Exception as exc:  # noqa: BLE001
                print(f"  {year}: error al listar: {exc}")
                continue

            print(f"  {year}: {len(items)} actas")
            for idx, item in enumerate(items, start=1):
                try:
                    result = await download_acta(
                        page,
                        context.request,
                        urljoin(browse_url, item["url"]),
                        year,
                        output_dir,
                    )
                except Exception as exc:  # noqa: BLE001
                    result = {"filename": f"{year}_item_{idx}", "reason": f"error: {exc}"}

                if result is None:
                    continue
                note = result.get("reason", "")
                if note == "descargado":
                    print(f"    [{idx}] {result['filename']} OK ({result.get('size_kb', 0)} KB)")
                elif note == "ya_existia":
                    print(f"    [{idx}] {result['filename']} ya existe.")
                else:
                    print(f"    [{idx}] {result['filename']} -> {note}")

                result.update({"year": year, "titulo": item.get("title", ""), "url": item["url"]})
                results.append(result)

        await context.close()

    now = datetime.now().isoformat(timespec="seconds")
    manifest = {"generado": now, "output_dir": output_dir, "resultados": results}
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)

    ok = [r for r in results if r.get("reason") == "descargado"]
    print(f"\nManifest: {manifest_path}")
    print(f"Descargadas: {len(ok)}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
