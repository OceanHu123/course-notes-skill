#!/usr/bin/env python3
"""Extract page-by-page text from a course PDF.

usage:
    python3 fetch_material.py <url-or-local-pdf> [--out FILE]

Prints which pages contain no extractable text (image-only) so they can be
sent to ocr_pages.py afterwards.  Requires PyMuPDF (fitz), which ships with
the system python3 on this machine.
"""

import argparse
import pathlib
import sys
import tempfile
import urllib.request


def download(url: str) -> pathlib.Path:
    suffix = pathlib.Path(url.split("?")[0]).suffix or ".pdf"
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="course-notes-")) / ("material" + suffix)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        tmp.write_bytes(resp.read())
    return tmp


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="URL or local PDF path")
    ap.add_argument("--out", help="write the text here instead of stdout")
    args = ap.parse_args()

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("PyMuPDF missing. Try: python3 -m pip install --user pymupdf", file=sys.stderr)
        return 1

    path = args.source
    if path.startswith(("http://", "https://")):
        path = str(download(path))
        print(f"# downloaded {path}", file=sys.stderr)
    if not pathlib.Path(path).exists():
        print(f"no such file: {path}", file=sys.stderr)
        return 1

    doc = fitz.open(path)
    chunks, empty = [], []
    for i, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if not text:
            empty.append(i)
        chunks.append(f"===== PAGE {i} =====\n{text}\n")

    body = "\n".join(chunks)
    if args.out:
        pathlib.Path(args.out).write_text(body, encoding="utf-8")
        print(f"# wrote {args.out}", file=sys.stderr)
    else:
        print(body)

    print(f"# pages: {doc.page_count}", file=sys.stderr)
    if empty:
        joined = ",".join(str(p) for p in empty)
        print(f"# image-only pages (need OCR): {joined}", file=sys.stderr)
        print(f"#   python3 ocr_pages.py {path} {joined}", file=sys.stderr)
    else:
        print("# no image-only pages", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
