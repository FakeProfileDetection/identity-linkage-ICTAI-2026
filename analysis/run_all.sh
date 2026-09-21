#!/bin/sh
# Regenerate every figure and table in this directory.
# Created: 2026-09-20
set -e
cd "$(dirname "$0")"

for script in \
    a-overall-identity-linkage/plot_heatmaps.py \
    b-contextual-variations/contextual_effects.py \
    c-multi-modal-fusion/fusion_weights.py \
    d-statistical-analysis/compare_representations.py \
    extra-plots/per_scenario_accuracy.py \
    extra-plots/critical_difference.py \
    extra-plots/contextual_panels.py \
    extra-plots/configuration_difficulty.py
do
    echo "== $script"
    (cd "$(dirname "$script")" && python3 "$(basename "$script")")
done
