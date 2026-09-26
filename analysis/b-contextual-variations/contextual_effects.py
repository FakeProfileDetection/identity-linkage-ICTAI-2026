"""Figure 3: the effect of session, platform, gallery size, and topic.

Created: 2026-09-20
Updated: 2026-09-25

Each of the four contextual factors is isolated by comparing two gallery-probe
configurations that differ only in that factor:

    Session   1.1 vs 1.2   the session direction is reversed
    Platform  1.1 vs 2.1 and 1.2 vs 2.2   a platform change is added
    Size      3.1 vs 3.2   the gallery holds two platforms instead of one
    Topic     1.1 vs 5.1 and 1.2 vs 5.2   a topic change is added

The reported quantity is

    delta AUK = AUK(reference) - AUK(varied)

so a positive value means the varied condition performed worse.  For size the
reference is the larger gallery, 3.2, so a positive value means the larger
gallery performed better.

The session comparison is paired: the two configurations use the same nine
platform-topic rotations in the same order, so a Wilcoxon signed-rank test
applies.  The other three comparisons are between configurations with different
rotations, so they use the Mann-Whitney U test.  Where a factor has two
comparisons, the reported delta is their mean and the reported p-value is the
smaller of the two.

P-values are Bonferroni corrected over all 32 comparisons in the figure: eight
representations times one comparison for session and for size, and eight times
two comparisons for platform and for topic.

Each heatmap is written as a PDF for the paper and a PNG for the README.  The
cells are shaded on a single grey ramp, white for not significant through dark
grey for p < 0.001, so the figure reads the same for colour-blind readers and
in a black-and-white print; the stars and bold text repeat the same
information.

    python contextual_effects.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import mannwhitneyu, wilcoxon

sys.path.append(str(Path(__file__).resolve().parent.parent))
import common

HERE = Path(__file__).parent
FACTORS = ["Session", "Platform", "Size", "Topic"]


def rank_biserial_wilcoxon(x, y):
    """Matched-pairs rank-biserial correlation."""
    differences = np.array(x) - np.array(y)
    differences = differences[differences != 0]
    if len(differences) == 0:
        return 0.0
    ranks = pd.Series(np.abs(differences)).rank()
    positive = ranks[differences > 0].sum()
    negative = ranks[differences < 0].sum()
    total = positive + negative
    return (positive - negative) / total if total else 0.0


def rank_biserial_mannwhitney(u, n1, n2):
    return 1 - (2 * u) / (n1 * n2)


def paired_comparison(reference, varied, n_models):
    """Session effect: the same rotations in both configurations."""
    _, p = wilcoxon(reference, varied)
    return {
        "delta": np.mean(reference) - np.mean(varied),
        "p": min(p * n_models, 1.0),
        "r": rank_biserial_wilcoxon(reference, varied),
    }


def unpaired_comparison(reference, varied, n_models, n_comparisons):
    u, p = mannwhitneyu(reference, varied, alternative="two-sided")
    return {
        "delta": np.mean(reference) - np.mean(varied),
        "p": min(p * n_models * n_comparisons, 1.0),
        "r": rank_biserial_mannwhitney(u, len(reference), len(varied)),
    }


def combine(comparisons):
    """Average the deltas, keep the strongest p-value and its effect size."""
    best = min(range(len(comparisons)), key=lambda i: comparisons[i]["p"])
    return {
        "delta": float(np.mean([c["delta"] for c in comparisons])),
        "p": comparisons[best]["p"],
        "r": comparisons[best]["r"],
    }


def effects(summary):
    """One row per representation, one column per contextual factor."""
    n_models = len(common.REPRESENTATIONS)

    def auk(scenario, representation):
        rows = summary[(summary["scenario"] == scenario)
                       & (summary["representation"] == representation)]
        return rows.sort_values("rotation_index")["mean_top_k"].to_numpy()

    records = []
    for representation in common.REPRESENTATIONS:
        record = {"representation": representation}
        record["Session"] = paired_comparison(
            auk("1.1", representation), auk("1.2", representation), n_models)
        record["Platform"] = combine([
            unpaired_comparison(auk(same, representation), auk(cross, representation), n_models, 2)
            for same, cross in [("1.1", "2.1"), ("1.2", "2.2")]])
        record["Size"] = unpaired_comparison(
            auk("3.2", representation), auk("3.1", representation), n_models, 1)
        record["Topic"] = combine([
            unpaired_comparison(auk(same, representation), auk(cross, representation), n_models, 2)
            for same, cross in [("1.1", "5.1"), ("1.2", "5.2")]])
        records.append(record)
    return records


def stars(p):
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return ""


def draw(records, value="delta", stem="variable_effect_heatmap"):
    """Cells are shaded by how significant they are, white to dark grey.

    `value` picks what the cells report: the change in AUK, or the
    rank-biserial effect size `r` that goes with the same test.  The figure
    is written as `<stem>.pdf` and `<stem>.png`.  It carries no title: the
    paper's caption says what the cells hold, as it does for Figures 2 and 4.

    The figure is drawn at the paper's column width, 3.5 inches, with the
    fonts at their printed size, so the rows are only as tall as their text
    needs and the figure takes as little of the column as it can.

    The shade follows -log10 of the corrected p-value on one grey ramp, so a
    darker cell always means a smaller p-value.  A single hue is used rather
    than the usual green-to-red so that readers with colour-vision deficiency,
    and a black-and-white print, see the same figure as everyone else.
    """
    significance = np.array([[-np.log10(max(r[f]["p"], 1e-10)) for f in FACTORS] for r in records])

    fig, ax = plt.subplots(figsize=(3.5, 1.5))
    cmap = LinearSegmentedColormap.from_list("significance", [
        (0.00, "#ffffff"),   # not significant
        (0.26, "#f0f0f0"),   # p = 0.05
        (0.40, "#8c8c8c"),   # p = 0.01
        (0.60, "#5a5a5a"),   # p = 0.001
        (1.00, "#262626"),   # far below p = 0.001
    ], N=256)
    ax.imshow(significance, cmap=cmap, aspect="auto", vmin=0, vmax=5.0)

    # Light grey lines between the cells, so that neighbouring white cells
    # still read as separate cells.
    ax.set_xticks(np.arange(-0.5, len(FACTORS)), minor=True)
    ax.set_yticks(np.arange(-0.5, len(records)), minor=True)
    ax.grid(which="minor", color="#d9d9d9", linewidth=0.5)
    ax.tick_params(which="minor", length=0)

    for i, record in enumerate(records):
        for j, factor in enumerate(FACTORS):
            cell = record[factor]
            ax.text(j, i, f"{cell[value]:+.3f}{stars(cell['p'])}",
                    ha="center", va="center", fontsize=6,
                    fontweight="bold" if cell["p"] < 0.05 else "normal",
                    # White text on the two- and three-star cells, which
                    # are dark enough that black is hard to read.
                    color="white" if significance[i, j] >= 2.0 else "black")

    # Separate the representations by modality, as Table III groups them.
    row = 0
    for label, members in common.MODALITY.items():
        if row > 0:
            ax.axhline(y=row - 0.5, color="black", linewidth=1.2)
        ax.text(len(FACTORS) - 0.4, row + (len(members) - 1) / 2, label,
                ha="left", va="center", fontsize=6.5, fontstyle="italic", color="#555555")
        row += len(members)

    ax.set_xticks(range(len(FACTORS)))
    ax.set_xticklabels(FACTORS, fontsize=7, fontweight="bold")
    ax.set_yticks(range(len(records)))
    ax.set_yticklabels([r["representation"] for r in records], fontsize=6)
    ax.tick_params(which="major", length=2, pad=1.5)
    # The star key sits a fixed distance under the factor labels, in points,
    # so it does not drift with the height of the grid.
    ax.annotate("*** p<0.001   ** p<0.01   * p<0.05   no star: not significant",
                xy=(0.5, 0), xycoords="axes fraction", xytext=(0, -14),
                textcoords="offset points", ha="center", va="top", fontsize=5.5)

    fig.tight_layout()
    for suffix in (".pdf", ".png"):
        fig.savefig(HERE / (stem + suffix), dpi=300, bbox_inches="tight")
        print(f"  wrote {stem}{suffix}")
    plt.close(fig)


def main():
    records = effects(common.mean_top_k(common.load()))
    draw(records)
    # The same comparisons reported as effect size rather than change in AUK.
    # This one is not in the paper; it was left out for space.
    draw(records, value="r", stem="effect_size_heatmap")

    table = pd.DataFrame([
        {"representation": r["representation"], "factor": f,
         "delta_auk": round(r[f]["delta"], 4),
         "p_corrected": r[f]["p"], "effect_size_r": round(r[f]["r"], 4),
         "significance": stars(r[f]["p"]) or "ns"}
        for r in records for f in FACTORS
    ])
    table.to_csv(HERE / "contextual_effects.csv", index=False)
    print("  wrote contextual_effects.csv")
    print()
    print(table.pivot(index="representation", columns="factor", values="delta_auk")
          .loc[common.REPRESENTATIONS, FACTORS].to_string())


if __name__ == "__main__":
    main()
