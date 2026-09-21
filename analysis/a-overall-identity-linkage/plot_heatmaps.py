"""Figure 2: overall identity linkage performance across the ten configurations.

Created: 2026-09-20

Three heatmaps of mean ACC@1, ACC@3, and ACC@5 for every representation in
every gallery-probe configuration.  Each cell averages over the platform-topic
rotations that the configuration covers.  (Figure 4, the average ranks, is
drawn by ../d-statistical-analysis/compare_representations.py, which computes
the ranks for the statistical tests.)

    python plot_heatmaps.py
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
import common

HERE = Path(__file__).parent


def accuracy_table(results, k):
    """Mean ACC@k per representation and scenario."""
    table = (
        results[results["k"] == k]
        .pivot_table(index="representation", columns="scenario", values="accuracy")
    )
    return table.loc[common.REPRESENTATIONS, common.SCENARIOS]


def main():
    results = common.load()

    # Figure 2.  All three panels share one colour scale so they can be read
    # against each other.
    tables = {k: accuracy_table(results, k) for k in (1, 3, 5)}
    low = min(t.values.min() for t in tables.values())
    high = max(t.values.max() for t in tables.values())
    for k, table in tables.items():
        common.heatmap(
            table,
            f"Model Accuracy Across All Scenarios (Top-{k})\nHigher accuracy = better performance",
            f"Mean Top-{k} Accuracy",
            HERE / f"accuracy_heatmap_k{k}.png",
            ".2f",
            common.light_greens(),
            vmin=low, vmax=high,
        )


if __name__ == "__main__":
    main()
