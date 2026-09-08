# -*- coding: utf-8 -*-
"""
Genera textos_completos.jsonl con el texto íntegro re-extraído desde los PDFs
para las filas del consolidado que exceden o rozan el límite de Excel (32.767).

Cubre:
  - ID 280  -> 2005-06-09 (PDF: 2005-06-09 - Actas.pdf). Ya está completo en el
               Excel (32.498 caracteres); se guarda igual para trazabilidad.
  - ID 297  -> 2005-07-12 (PDF: 2005-07-12 - Actas.pdf, páginas 1-12). La celda
               Excel quedó cortada en 32.767 (límite XLSX); aquí se guarda el
               texto íntegro re-extraído.

El Excel conserva la celda Texto <= 32.767 caracteres (limitación del formato XLSX);
este archivo guarda el texto completo con la misma ID para no perder información.
"""
import json
import re
from pathlib import Path

import openpyxl
import pypdf

from paths import REPO, DATA_RAW, DATA_PROC
SRC = DATA_RAW / "consolidado_final.xlsx"
OUT = DATA_PROC / "textos_completos.jsonl"

# id -> (archivo PDF, fecha, primera_página, última_página)
PDFS = {
    280: (DATA_RAW / "2005-06-09 - Actas.pdf", "2005-06-09", 1, 9),
    297: (DATA_RAW / "2005-07-12 - Actas.pdf", "2005-07-12", 1, 12),
}

HEADER_LINE = re.compile(
    r"^("
    r"Sesi[oó]n\s+N[°º]?\s*\d+"
    r"|Pol[ií]tica\s+[Mm]onetaria"
    r"|P[áa]gina\s*\d+\s+de\s+\d+"
    r"|[A-ZÁÉÍÓÚÑ]"
    r")$"
)

# encabezado/pie embebido al final o inicio de una línea:
#   09.06.2005 3.-    12.07.2005 12.-    3.-   12.-   9
DATE_FOOTER_LINE = re.compile(r"^\d{2}\.\d{2}\.\d{4}(?:\s+\d{1,3}(?:\.-|[.-])?)?$")

DATE_PAGE_TAIL = re.compile(r"\s*\d{2}\.\d{2}\.\d{4}\s+\d{1,3}(?:\.-|[.-])?\s*$")
DATE_PAGE_HEAD = re.compile(r"^\s*\d{2}\.\d{2}\.\d{4}\s+\d{1,3}(?:\.-|[.-])?\s*")


def clean_pdf_line(line):
    """Quita firmas de pie/encabezado, jamás números económicos genéricos."""
    line = line.strip()
    if HEADER_LINE.fullmatch(line) or DATE_FOOTER_LINE.fullmatch(line):
        return ''
    line = DATE_PAGE_TAIL.sub('', line)
    line = DATE_PAGE_HEAD.sub('', line)
    return reremove_artifacts(line).strip()


def pdf_text(path, start_page, end_page):
    reader = pypdf.PdfReader(str(path))
    pages = []
    for i in range(start_page - 1, min(end_page, len(reader.pages))):
        raw = reader.pages[i].extract_text() or ""
        lines = []
        for orig in raw.split("\n"):
            ln = clean_pdf_line(orig)
            if not ln:
                continue
            lines.append(ln)
        pages.append(" ".join(lines))
    text = " ".join(pages)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def reremove_artifacts(s):
    # números de página sueltos o letras huérfanas del pie (ej. "H")
    if re.fullmatch(r"\d{1,3}\.-", s):
        return ""
    if re.fullmatch(r"[A-ZÁÉÍÓÚÑ]", s):
        return ""
    return s


def slice_from_marker(full_text, marker):
    idx = full_text.find(marker)
    if idx < 0:
        idx = full_text.lower().find(marker.lower())
    if idx < 0:
        raise ValueError(f"No se encontró el marcador: {marker!r}")
    return full_text[idx:]


def main():
    DATA_PROC.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
    ws = wb["Consolidado"]
    rows = iter(ws.iter_rows(values_only=True))
    next(rows)
    data = {int(r[0]): r for r in rows}

    markers = {
        280: "El Presidente fija la sesión de política monetaria del mes de diciembre de 2005",
        297: "El Presidente fija la sesión de política monetaria del mes de enero de 2006",
    }

    records = []
    for rid, (pdf, fecha, p_start, p_end) in PDFS.items():
        row = data[rid]
        original = str(row[5])
        full = pdf_text(pdf, p_start, p_end)
        full = slice_from_marker(full, markers[rid])

        # Para 280 el texto del Excel ya está completo (única fuente fiable de
        # la segmentación original), así que lo conservamos como referencia.
        if rid == 280:
            texto_referencia = original
            fuente = "XLSX_original_verificado_PDF"
        else:
            texto_referencia = full
            fuente = "PDF"

        rec = {
            "ID": rid,
            "Id_Sesion": f"RPM-{fecha}",
            "Fecha": fecha,
            "Página": row[4],
            "Paginas_PDF": f"{p_start}-{p_end}",
            "Archivo_PDF": pdf.name,
            "Actor": row[2],
            "Rol": row[3],
            "Tema": row[6],
            "Palabra_Clave": row[7],
            "Texto_Completo": texto_referencia,
            "Longitud_Excel": len(original),
            "Longitud_Texto_Completo": len(texto_referencia),
            "Fuente": fuente,
        }
        records.append(rec)
        print(
            f"ID {rid}: {pdf.name} | Excel={len(original)} | "
            f"texto_completo={len(texto_referencia)} | fuente={fuente}"
        )

    with open(OUT, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"Escribí {OUT} con {len(records)} registros.")


if __name__ == "__main__":
    main()
