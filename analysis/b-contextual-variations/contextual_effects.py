"""Figure 3: the effect of session, platform, gallery size, and topic.

Created: 2026-09-20

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


def draw(records, value="delta", title="Δ AUK", filename="variable_effect_heatmap.png"):
    """Cells are coloured by how significant they are, green to red.

    `value` picks what the cells report: the change in AUK, or the
    rank-biserial effect size `r` that goes with the same test.
    """
    significance = np.array([[-np.log10(max(r[f]["p"], 1e-10)) for f in FACTORS] for r in records])

    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    cmap = LinearSegmentedColormap.from_list("significance", [
        (0.00, "#c8e6c9"),   # not significant
        (0.10, "#e8f5e9"),
        (0.20, "#ffffff"),   # around p = 0.05
        (0.45, "#ffcdd2"),
        (1.00, "#ef5350"),   # p < 0.001
    ], N=256)
    ax.imshow(significance, cmap=cmap, aspect="auto", vmin=0, vmax=5.0)

    for i, record in enumerate(records):
        for j, factor in enumerate(FACTORS):
            cell = record[factor]
            ax.text(j, i, f"{cell[value]:+.3f}{stars(cell['p'])}",
                    ha="center", va="center", fontsize=8,
                    fontweight="bold" if cell["p"] < 0.05 else "normal",
                    color="white" if significance[i, j] >= 4.0 else "black")

    # Separate the representations by modality, as Table III groups them.
    row = 0
    for label, members in common.MODALITY.items():
        if row > 0:
            ax.axhline(y=row - 0.5, color="black", linewidth=1.5)
        ax.text(len(FACTORS) - 0.35, row + (len(members) - 1) / 2, label,
                ha="left", va="center", fontsize=8, fontstyle="italic", color="#555555")
        row += len(members)

    ax.set_xticks(range(len(FACTORS)))
    ax.set_xticklabels(FACTORS, fontsize=10, fontweight="bold")
    ax.set_yticks(range(len(records)))
    ax.set_yticklabels([r["representation"] for r in records], fontsize=9)
    ax.set_title(f"Variable Effect by Model\n({title}, colored by significance)", fontsize=11, pad=10)
    ax.text(0.5, -0.22,
            "*** p<0.001 (99.9%)   ** p<0.01 (99%)   * p<α (95%)   no star = ns   α=0.05",
            transform=ax.transAxes, ha="center", fontsize=7, color="black")

    fig.tight_layout()
    fig.savefig(HERE / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {filename}")


def main():
    records = effects(common.mean_top_k(common.load()))
    draw(records)
    # The same comparisons reported as effect size rather than change in AUK.
    # This one is not in the paper; it was left out for space.
    draw(records, value="r", title="effect size r", filename="effect_size_heatmap.png")

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
