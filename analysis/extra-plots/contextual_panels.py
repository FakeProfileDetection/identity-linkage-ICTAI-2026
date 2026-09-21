"""The four contextual comparisons behind Figure 3, drawn one factor at a time.

Created: 2026-09-20

Figure 3 compresses each comparison into a single number.  These panels show
the two sides of each comparison directly: for every representation, mean top-k
accuracy under the reference configuration next to the varied one.  The gap
between the pair of bars is the delta AUK that Figure 3 reports.

  effect_session.png    1.1 against 1.2
  effect_platform.png   1.1 against 2.1, and 1.2 against 2.2
  effect_size.png       3.2 against 3.1
  effect_topic.png      1.1 against 5.1, and 1.2 against 5.2
  effect_summary.png    all four in one 2 by 2 figure

    python contextual_panels.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent.parent))
import common

HERE = Path(__file__).parent

# factor -> (reference scenarios, varied scenarios, label for each side)
COMPARISONS = {
    "session": (["1.1"], ["1.2"], "session 1 to 2", "session 2 to 1"),
    "platform": (["1.1", "1.2"], ["2.1", "2.2"], "same platform", "platform changes"),
    "size": (["3.2"], ["3.1"], "two-platform gallery", "one-platform gallery"),
    "topic": (["1.1", "1.2"], ["5.1", "5.2"], "same topic", "topic changes"),
}


def panel(ax, summary, factor):
    reference, varied, reference_label, varied_label = COMPARISONS[factor]

    def means(scenarios):
        return [summary[(summary["scenario"].isin(scenarios))
                        & (summary["representation"] == r)]["mean_top_k"]
                for r in common.REPRESENTATIONS]

    positions = np.arange(len(common.REPRESENTATIONS))
    width = 0.38
    for offset, values, hatch, alpha in [(-width / 2, means(reference), None, 0.85),
                                         (+width / 2, means(varied), "///", 0.45)]:
        ax.bar(positions + offset, [v.mean() for v in values], width,
               yerr=[v.std() for v in values], capsize=2,
               color=[common.COLOR[r] for r in common.REPRESENTATIONS],
               edgecolor="black", linewidth=0.5, hatch=hatch, alpha=alpha)

    ax.set_xticks(positions)
    ax.set_xticklabels(common.REPRESENTATIONS, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Mean top-k accuracy")
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", alpha=0.3)
    ax.set_title(f"{factor.capitalize()}: {reference_label} vs {varied_label}", fontsize=10)

    from matplotlib.patches import Patch
    ax.legend(handles=[
        Patch(facecolor="gray", edgecolor="black", alpha=0.85, label=reference_label),
        Patch(facecolor="gray", edgecolor="black", alpha=0.45, hatch="///", label=varied_label),
    ], fontsize=7, loc="upper left")


def main():
    summary = common.mean_top_k(common.load())

    for factor in COMPARISONS:
        fig, ax = plt.subplots(figsize=(7, 4))
        panel(ax, summary, factor)
        fig.tight_layout()
        fig.savefig(HERE / f"effect_{factor}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    for ax, factor in zip(axes.flat, COMPARISONS):
        panel(ax, summary, factor)
    fig.suptitle("Each contextual factor, reference condition against varied condition", fontsize=12)
    fig.tight_layout()
    fig.savefig(HERE / "effect_summary.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    print("  wrote effect_session.png, effect_platform.png, effect_size.png, "
          "effect_topic.png and effect_summary.png")


if __name__ == "__main__":
    main()
