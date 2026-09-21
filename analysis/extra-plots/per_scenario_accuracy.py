"""Per-configuration views that did not fit in the paper.

Created: 2026-09-20

For each of the ten gallery-probe configurations this writes two plots.

  accuracy_by_k_<scenario>.png   mean ACC@k for k = 1..5, with one line per
                                 representation and error bars showing the
                                 standard deviation across rotations.  The
                                 paper reports only k = 1, 3, and 5.

  spread_<scenario>.png          the distribution of mean top-k accuracy over
                                 the rotations of that configuration.  The
                                 heatmaps in the paper show only the average,
                                 so this is where the spread is visible.

    python per_scenario_accuracy.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent.parent))
import common

HERE = Path(__file__).parent
DESCRIPTIONS = {
    "1.1": "same platform and topic, session 1 to 2",
    "1.2": "same platform and topic, session 2 to 1",
    "2.1": "platform changes, topic fixed, session 1 to 2",
    "2.2": "platform changes, topic fixed, session 2 to 1",
    "3.1": "platform changes, sessions pooled, one-platform gallery",
    "3.2": "platform changes, sessions pooled, two-platform gallery",
    "4.1": "platform and topic change, one-platform gallery",
    "4.2": "platform and topic change, two-platform gallery",
    "5.1": "topic changes, platform fixed, session 1 to 2",
    "5.2": "topic changes, platform fixed, session 2 to 1",
}


def accuracy_by_k(results, scenario):
    fig, ax = plt.subplots(figsize=(7, 5))
    for representation in common.REPRESENTATIONS:
        subset = results[(results["scenario"] == scenario)
                         & (results["representation"] == representation)]
        stats = subset.groupby("k")["accuracy"].agg(["mean", "std"])
        ax.errorbar(stats.index, stats["mean"], yerr=stats["std"], marker="o",
                    capsize=3, label=representation, color=common.COLOR[representation])
    ax.set_xlabel("k")
    ax.set_ylabel("Accuracy")
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_ylim(0, 1.05)
    ax.grid(alpha=0.3)
    ax.set_title(f"Scenario {scenario}: accuracy against k\n{DESCRIPTIONS[scenario]}")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(HERE / f"accuracy_by_k_{scenario}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def spread(summary, scenario):
    values = [summary[(summary["scenario"] == scenario)
                      & (summary["representation"] == r)]["mean_top_k"].to_numpy()
              for r in common.REPRESENTATIONS]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    parts = ax.violinplot(values, showmeans=True, showextrema=False)
    for body, representation in zip(parts["bodies"], common.REPRESENTATIONS):
        body.set_facecolor(common.COLOR[representation])
        body.set_alpha(0.7)
    for i, column in enumerate(values, start=1):
        ax.scatter(np.full(len(column), i), column, s=10, color="black", alpha=0.5, zorder=3)

    ax.set_xticks(range(1, len(common.REPRESENTATIONS) + 1))
    ax.set_xticklabels(common.REPRESENTATIONS, rotation=45, ha="right")
    ax.set_ylabel("Mean top-k accuracy")
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", alpha=0.3)
    ax.set_title(f"Scenario {scenario}: spread across the {len(values[0])} rotations\n"
                 f"{DESCRIPTIONS[scenario]}")
    fig.tight_layout()
    fig.savefig(HERE / f"spread_{scenario}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    results = common.load()
    summary = common.mean_top_k(results)
    for scenario in common.SCENARIOS:
        accuracy_by_k(results, scenario)
        spread(summary, scenario)
    print(f"  wrote accuracy_by_k_<scenario>.png and spread_<scenario>.png "
          f"for {len(common.SCENARIOS)} scenarios")


if __name__ == "__main__":
    main()
