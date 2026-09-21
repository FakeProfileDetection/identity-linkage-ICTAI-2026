#!/bin/sh
# Regenerate the figures from the numbers as published, without touching the
# figures made from the current results. Copies the scripts to a separate
# directory, points them at experiments/results/as-published/, and runs them
# there. The output directory is printed at the end.
# Created: 2026-09-20
#
#   ./reproduce_paper.sh            # writes into a temporary directory
#   ./reproduce_paper.sh some/dir   # writes into some/dir
set -e
cd "$(dirname "$0")"
OUT="${1:-$(mktemp -d -t paper-figures)}"
mkdir -p "$OUT"
for d in */; do
    case "$d" in __pycache__/) continue;; esac
    mkdir -p "$OUT/$d"
    cp "$d"*.py "$OUT/$d"
done
cp common.py run_all.sh "$OUT/"
RESULTS_CSV="$(pwd)/../experiments/results/as-published/scenario-results.csv" sh "$OUT/run_all.sh" > "$OUT/run.log" 2>&1
echo "Figures from the published numbers are in: $OUT"
