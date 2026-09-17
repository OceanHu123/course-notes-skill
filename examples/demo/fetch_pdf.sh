#!/usr/bin/env bash
# Fetch the OSTEP Ch.4 demo PDF (not vendored in git — authors prefer linking).
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
URL="https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf"
OUT="$DIR/cpu-intro.pdf"
curl -fsSL -A "Mozilla/5.0" -o "$OUT" "$URL"
echo "saved $OUT ($(wc -c <"$OUT") bytes)"
