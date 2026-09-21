"""Section IV-C: how the fusion weight changes identity linkage performance.

Created: 2026-09-20

Score-level fusion combines the text similarity and the ITAD keystroke
similarity as

    S_f = alpha * S_keystroke + (1 - alpha) * S_text

The five representations below form a sweep over alpha.  The two ends are the
single-modality representations: at alpha = 0 only text is used, at alpha = 1
only keystroke timing.

    alpha  representation
    0.00   C-Emb-Nomic
    0.25   CB-ITAD.25
    0.50   CB-ITAD.5
    0.75   CB-ITAD.75
    1.00   B-ITAD

Performance is reported for three groups of gallery-probe configurations. The
first two keep the topic fixed, the third changes it.

    PT.S   1.1 and 1.2   same platform and topic
    T.PS   2.1 and 2.2   platform changes, topic fixed
    P.TS   5.1 and 5.2   topic changes, platform fixed

    python fusion_weights.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
import common

HERE = Path(__file__).parent

KEYSTROKE_WEIGHT = {
    "C-Emb-Nomic": 0.00,
    "CB-ITAD.25": 0.25,
    "CB-ITAD.5": 0.50,
    "CB-ITAD.75": 0.75,
    "B-ITAD": 1.00,
}

GROUPS = {
    "PT.S (same platform and topic)": ["1.1", "1.2"],
    "T.PS (platform changes, topic fixed)": ["2.1", "2.2"],
    "P.TS (topic changes, platform fixed)": ["5.1", "5.2"],
}


def table(results):
    """Mean ACC@k per representation and configuration, for the fusion sweep."""
    rows = []
    for representation, alpha in KEYSTROKE_WEIGHT.items():
        for group, scenarios in GROUPS.items():
            for scenario in scenarios:
                subset = results[(results["representation"] == representation)
                                 & (results["scenario"] == scenario)]
                for k in (1, 5):
                    rows.append({
                        "representation": representation,
                        "keystroke_weight": alpha,
                        "group": group,
                        "scenario": scenario,
                        "k": k,
                        "accuracy": round(subset[subset["k"] == k]["accuracy"].mean(), 4),
                    })
    return pd.DataFrame(rows)


def draw(accuracy):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    for ax, k in zip(axes, (1, 5)):
        for group in GROUPS:
            line = (accuracy[(accuracy["k"] == k) & (accuracy["group"] == group)]
                    .groupby("keystroke_weight")["accuracy"].mean())
            ax.plot(line.index, line.values, marker="o", label=group)
        ax.set_xlabel("Keystroke weight α")
        ax.set_title(f"ACC@{k}")
        ax.set_xticks(sorted(KEYSTROKE_WEIGHT.values()))
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Mean accuracy")
    axes[0].legend(fontsize=8)
    fig.suptitle("Identity linkage accuracy against the fusion weight")
    fig.tight_layout()
    fig.savefig(HERE / "fusion_weight_sweep.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("  wrote fusion_weight_sweep.png")


def main():
    accuracy = table(common.load())
    accuracy.to_csv(HERE / "fusion_weights.csv", index=False)
    print("  wrote fusion_weights.csv")
    draw(accuracy)

    for k in (1, 5):
        print(f"\nMean ACC@{k} by configuration")
        print(accuracy[accuracy["k"] == k]
              .pivot_table(index="representation", columns="scenario", values="accuracy")
              .loc[list(KEYSTROKE_WEIGHT), ["1.1", "1.2", "2.1", "2.2", "5.1", "5.2"]]
              .to_string())


if __name__ == "__main__":
    main()
