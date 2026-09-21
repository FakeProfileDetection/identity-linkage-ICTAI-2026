"""Settings shared by the analysis scripts.

Created: 2026-09-20

Every analysis reads the same file, experiments/results/scenario-results.csv,
which holds ACC@k for k = 1..5 for each of the 171 gallery-probe rotations and
each of the eight identity representations.
"""

import os
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent

# Set RESULTS_CSV to run the analysis on another combined file, for example
# experiments/results/as-published/scenario-results.csv to get the paper's own
# figures. A relative path is taken from this directory.
RESULTS = HERE.parent / "experiments" / "results" / "scenario-results.csv"
if os.environ.get("RESULTS_CSV"):
    RESULTS = (HERE / os.environ["RESULTS_CSV"]).resolve()

# The eight identity representations of Table III, in the order the paper's
# figures use them.
REPRESENTATIONS = [
    "C-Emb-Nomic",
    "CB-POS",
    "CB-FuncW",
    "CB-ITAD.25",
    "CB-ITAD.5",
    "CB-ITAD.75",
    "B-ITAD",
    "B-ML-RF",
]

SCENARIOS = ["1.1", "1.2", "2.1", "2.2", "3.1", "3.2", "4.1", "4.2", "5.1", "5.2"]

# Modality as Table III assigns it: t is text, t+k is score-level fusion,
# k is keystroke dynamics.  Figure 3 separates its rows into these groups, and
# the supporting plots give each modality its own hue.
MODALITY = {
    "t": ["C-Emb-Nomic", "CB-POS", "CB-FuncW"],
    "t+k": ["CB-ITAD.25", "CB-ITAD.5", "CB-ITAD.75"],
    "k": ["B-ITAD", "B-ML-RF"],
}

COLOR = {
    "C-Emb-Nomic": "#1f77b4", "CB-POS": "#6baed6", "CB-FuncW": "#c6dbef",
    "CB-ITAD.25": "#e6550d", "CB-ITAD.5": "#fd8d3c", "CB-ITAD.75": "#fdd0a2",
    "B-ITAD": "#74c476", "B-ML-RF": "#006d2c",
}


def load():
    """ACC@k for every scenario, rotation, representation and k."""
    return pd.read_csv(RESULTS, dtype={"scenario": str})


def mean_top_k(results):
    """Mean of ACC@k over k = 1..5, one value per rotation and representation.

    This is the single summary measure the paper calls AUK.  Figures 3 and 4
    use it to reduce each gallery-probe rotation to one number.
    """
    summary = (
        results.groupby(["scenario", "rotation_index", "rotation", "representation"], as_index=False)
        ["accuracy"].mean()
        .rename(columns={"accuracy": "mean_top_k"})
    )
    # Accuracies are recorded to four decimal places, so two representations
    # whose five accuracies sum to the same total have the same mean.  Adding
    # the same numbers in a different order can leave a difference of about
    # 1e-16, which is enough to break a tie when ranking.  Rounding to six
    # places removes that noise and is still far finer than the smallest real
    # difference between two means, which is 2e-5.
    summary["mean_top_k"] = summary["mean_top_k"].round(6)
    return summary


def light_greens(reverse=False):
    """The Greens colormap without its darkest shades, as the paper's figures use."""
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    cmap = LinearSegmentedColormap.from_list("LightGreens", plt.cm.Greens(np.linspace(0, 0.65, 256)))
    return cmap.reversed() if reverse else cmap


def heatmap(table, title, colorbar_label, path, fmt, cmap, vmin=None, vmax=None):
    """Draw one annotated heatmap in the style shared by Figures 2 and 4."""
    import matplotlib.pyplot as plt
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(14, 5))
    drawn = sns.heatmap(
        table, annot=True, fmt=fmt, annot_kws={"size": 18}, cmap=cmap,
        vmin=vmin, vmax=vmax, linewidths=0.5, linecolor="white", ax=ax,
        cbar_kws={"label": colorbar_label},
        xticklabels=[f"Scenario {s}" for s in table.columns],
    )
    bar = drawn.collections[0].colorbar
    bar.set_label(colorbar_label, fontsize=18, fontweight="bold")
    bar.ax.tick_params(labelsize=14)

    ax.set_xlabel("Scenario", fontsize=20, fontweight="bold")
    ax.set_ylabel("Model", fontsize=20, fontweight="bold")
    ax.set_title(title, fontsize=20, fontweight="bold", pad=15)
    plt.xticks(rotation=45, ha="right", fontsize=16)
    plt.yticks(rotation=0, fontsize=16)
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  wrote {path.name}")
