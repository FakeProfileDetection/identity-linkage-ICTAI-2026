"""Figure 2: overall identity linkage performance across the ten configurations.

Created: 2026-09-20
Updated: 2026-09-25

Three heatmaps of mean ACC@1, ACC@3, and ACC@5 for every representation in
every gallery-probe configuration.  Each cell averages over the platform-topic
rotations that the configuration covers.  The three panels are written both
one per file and stacked into the single figure the paper prints, saved as a
PDF for the paper and a PNG for the README.  (Figure 4, the average ranks, is
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


def stacked_heatmaps(tables, vmin, vmax, paths):
    """Figure 2 as printed: the three panels stacked, one colour bar, one axis.

    The layout copies the paper's figure so that it fits the same column
    space: titles are just "Top k", the scenario labels appear only under the
    bottom panel, the shared colour bar sits beside the middle panel, and the
    panels are as close as the titles allow.  The one departure from the
    printed figure: the tick labels are "1.1" rather than "Scenario 1.1",
    since the axis is already labelled "Scenario".
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    fig = plt.figure(figsize=(14, 11.4))
    grid = fig.add_gridspec(
        nrows=3, ncols=2, width_ratios=[1, 0.02], wspace=0.03, hspace=0.15,
    )
    colorbar_ax = fig.add_subplot(grid[1, 1])
    axes = [fig.add_subplot(grid[row, 0]) for row in range(3)]
    for ax, (k, table) in zip(axes, tables.items()):
        bottom = ax is axes[-1]
        sns.heatmap(
            table, annot=True, fmt=".2f", annot_kws={"size": 18},
            cmap=common.light_greens(), vmin=vmin, vmax=vmax,
            linewidths=0.5, linecolor="white", ax=ax,
            cbar=(k == 3), cbar_ax=colorbar_ax if k == 3 else None,
            xticklabels=list(table.columns) if bottom else False,
        )
        ax.set_title(f"Top {k}", fontsize=20, fontweight="bold", pad=4)
        ax.set_ylabel("Model", fontsize=20, fontweight="bold")
        ax.set_xlabel("Scenario" if bottom else "", fontsize=20, fontweight="bold")
        ax.tick_params(axis="y", rotation=0, labelsize=16)
        if bottom:
            ax.tick_params(axis="x", labelsize=16)
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        else:
            ax.tick_params(axis="x", bottom=False)

    colorbar_ax.set_ylabel("Mean Accuracy", fontsize=18, fontweight="bold")
    colorbar_ax.tick_params(labelsize=14)

    for path in paths:
        fig.savefig(path, dpi=200, bbox_inches="tight")
        print(f"  wrote {path.name}")
    plt.close(fig)


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
    stacked_heatmaps(
        tables, low, high,
        [HERE / "accuracy_heatmaps.pdf", HERE / "accuracy_heatmaps.png"],
    )


if __name__ == "__main__":
    main()
