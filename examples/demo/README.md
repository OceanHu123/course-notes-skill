# Demo: before / after for screenshots

Public lecture PDF from **OSTEP** (Operating Systems: Three Easy Pieces), Chapter 4 — *The Abstraction: The Process*.

Source (do not hotlink-scrape forever; re-download if missing):

https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf

Authors ask instructors to link to the chapter rather than permanently mirroring it, so the PDF is **gitignored**. Fetch it locally:

```bash
./examples/demo/fetch_pdf.sh
```

## What was run (Tier 0 skill path)

```bash
python3 course-notes/scripts/fetch_material.py examples/demo/cpu-intro.pdf --out /tmp/material.txt
# → 13 pages, no image-only pages (OCR skipped)
# then notes written with the skill template → after-notes.md
```

## Screenshot

Committed comparison shot used in the README:

![Before / After](before-after.jpg)

| Shot | Open this | Tip |
|---|---|---|
| **Before** | `cpu-intro.pdf` in Preview | Dense textbook prose (e.g. p.2 tip + §4.1) |
| **After** | `after-notes.md` | Keep Overview / section notes on screen |

A copy of the notes is also at: `~/notes/DEMO-OSTEP/cpu-intro-process.md`.

## Attribution

OSTEP © Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau — free online chapters at https://pages.cs.wisc.edu/~remzi/OSTEP/
