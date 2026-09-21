"""Critical difference diagrams, one per gallery-probe configuration.

Created: 2026-09-20

These show the Nemenyi post hoc result behind Section IV-D.  Representations
are placed on an axis by their average rank, best on the left.  Any two whose
positions differ by less than the critical difference cannot be told apart at
alpha = 0.05; those groups are joined by a horizontal bar.

    python critical_difference.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import studentized_range

sys.path.append(str(Path(__file__).resolve().parent.parent))
import common

HERE = Path(__file__).parent
ALPHA = 0.05


def draw(scenario, ranks, cd):
    ordered = ranks.sort_values()
    names = list(ordered.index)
    positions = ordered.to_numpy()
    n = len(names)

    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.set_xlim(0.5, n + 0.5)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # The rank axis.
    ax.plot([0.5, n + 0.5], [0.62, 0.62], color="black", linewidth=1.2)
    for tick in range(1, n + 1):
        ax.plot([tick, tick], [0.60, 0.64], color="black", linewidth=1)
        ax.text(tick, 0.55, str(tick), ha="center", va="top", fontsize=9, color="#555555")
    ax.text((n + 1) / 2, 0.42, "Average rank (lower is better)", ha="center", fontsize=10)

    # The critical difference bar.
    ax.plot([1, 1 + cd], [0.90, 0.90], color="black", linewidth=2.5)
    ax.plot([1, 1], [0.87, 0.93], color="black", linewidth=2.5)
    ax.plot([1 + cd, 1 + cd], [0.87, 0.93], color="black", linewidth=2.5)
    ax.text(1 + cd / 2, 0.94, f"CD = {cd:.2f}", ha="center", fontsize=10, fontweight="bold")

    # Each representation, labelled above or below the axis in turn.
    for i, (name, position) in enumerate(zip(names, positions)):
        above = i % 2 == 0
        y_label = 0.78 if above else 0.28
        ax.plot([position, position], [0.62, y_label], color=common.COLOR[name], linewidth=1.2)
        ax.scatter([position], [0.62], color=common.COLOR[name], s=30, zorder=3)
        ax.text(position, y_label, f"{name} ({position:.2f})",
                ha="center", va="bottom" if above else "top", fontsize=8.5,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                          edgecolor=common.COLOR[name], linewidth=0.8))

    # Bars joining representations that are not significantly different.
    groups = []
    for i in range(n):
        j = i
        while j + 1 < n and positions[j + 1] - positions[i] <= cd:
            j += 1
        if j > i and not any(start <= i and j <= end for start, end in groups):
            groups.append((i, j))

    for depth, (start, end) in enumerate(groups):
        y = 0.70 - depth * 0.035
        ax.plot([positions[start] - 0.05, positions[end] + 0.05], [y, y],
                color="#333333", linewidth=3, solid_capstyle="butt")

    ax.set_title(f"Scenario {scenario}: critical difference diagram (mean top-k accuracy)",
                 fontsize=11, fontweight="bold")
    fig.tight_layout()
    fig.savefig(HERE / f"critical_difference_{scenario}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    summary = common.mean_top_k(common.load())
    for scenario in common.SCENARIOS:
        table = (summary[summary["scenario"] == scenario]
                 .pivot_table(index="rotation_index", columns="representation", values="mean_top_k")
                 [common.REPRESENTATIONS])
        n_rotations, n_representations = table.shape
        q = studentized_range.ppf(1 - ALPHA, n_representations, np.inf) / np.sqrt(2)
        cd = q * np.sqrt(n_representations * (n_representations + 1) / (6 * n_rotations))
        draw(scenario, table.rank(axis=1, ascending=False).mean(), cd)
    print(f"  wrote critical_difference_<scenario>.png for {len(common.SCENARIOS)} scenarios")


if __name__ == "__main__":
    main()
