#!/usr/bin/env python3
"""OCR selected pages of a PDF (or a single image file).

usage:
    python3 ocr_pages.py <pdf-or-image> <pages|all> [--dpi 200]

Engine order: tesseract if installed, otherwise the bundled Swift helper that
uses the macOS Vision framework (compiled once and cached).  Rendered PNGs are
deleted when the run finishes.
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile

SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
CACHE_DIR = pathlib.Path.home() / ".cache" / "course-notes"


def parse_pages(spec: str, total: int) -> list[int]:
    if spec.lower() == "all":
        return list(range(1, total + 1))
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if part:
            pages.append(int(part))
    return pages


def vision_binary() -> pathlib.Path | None:
    """Compile scripts/ocr.swift once, then reuse the cached binary."""
    if not shutil.which("swiftc"):
        return None
    src = SKILL_DIR / "scripts" / "ocr.swift"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    binary = CACHE_DIR / "ocr"
    if binary.exists() and binary.stat().st_mtime >= src.stat().st_mtime:
        return binary
    result = subprocess.run(
        ["swiftc", "-O", str(src), "-o", str(binary)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        return None
    return binary


def pick_engine():
    if shutil.which("tesseract"):
        return "tesseract", None
    binary = vision_binary()
    if binary:
        return "vision", binary
    return None, None


def ocr_image(engine: str, binary, image: pathlib.Path) -> str:
    if engine == "tesseract":
        cmd = ["tesseract", str(image), "stdout"]
    else:
        cmd = [str(binary), str(image)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return f"[ocr error] {result.stderr.strip()}"
    return result.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="PDF path, or a single image path")
    ap.add_argument("pages", help="page numbers like 19,20 or 'all'")
    ap.add_argument("--dpi", type=int, default=200)
    args = ap.parse_args()

    engine, binary = pick_engine()
    if engine is None:
        print("no OCR engine: install tesseract, or run on macOS with swiftc available",
              file=sys.stderr)
        return 1
    print(f"# engine: {engine}", file=sys.stderr)

    source = pathlib.Path(args.source)
    if not source.exists():
        print(f"no such file: {source}", file=sys.stderr)
        return 1

    workdir = pathlib.Path(tempfile.mkdtemp(prefix="course-notes-ocr-"))
    try:
        if source.suffix.lower() in {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}:
            print(ocr_image(engine, binary, source))
            return 0

        import fitz  # PyMuPDF
        doc = fitz.open(source)
        for number in parse_pages(args.pages, doc.page_count):
            if not 1 <= number <= doc.page_count:
                print(f"===== PAGE {number} (OCR) =====\n[out of range]\n")
                continue
            png = workdir / f"p{number}.png"
            doc[number - 1].get_pixmap(dpi=args.dpi).save(png)
            print(f"===== PAGE {number} (OCR) =====")
            print(ocr_image(engine, binary, png))
            print()
        return 0
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
