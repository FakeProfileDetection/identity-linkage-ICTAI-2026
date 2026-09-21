"""Which gallery-probe rotations are hard, seen across all representations at once.

Created: 2026-09-20

The analyses in the paper compare representations.  This one changes the unit:
each of the 171 platform-topic rotations becomes a point, described by the mean
top-k accuracy that each of the eight representations reached on it.  A t-SNE
embedding of those eight-dimensional profiles puts rotations that all the
representations found similar near each other.

Three views of the same embedding:

  difficulty_by_scenario.png     coloured by gallery-probe configuration
  difficulty_by_accuracy.png     coloured by mean accuracy over the eight
                                 representations, so dark is hard
  difficulty_by_disagreement.png coloured by the standard deviation over the
                                 eight, so dark is where they disagree most

t-SNE positions are not distances to be read literally; what the plot shows is
which rotations group together.

    python configuration_difficulty.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE

sys.path.append(str(Path(__file__).resolve().parent.parent))
import common

HERE = Path(__file__).parent
RANDOM_STATE = 42
PERPLEXITY = 30


def main():
    summary = common.mean_top_k(common.load())
    profiles = summary.pivot_table(
        index=["scenario", "rotation_index"], columns="representation", values="mean_top_k"
    )[common.REPRESENTATIONS]

    embedding = TSNE(n_components=2, perplexity=PERPLEXITY, random_state=RANDOM_STATE,
                     init="pca").fit_transform(profiles.to_numpy())

    scenario = profiles.index.get_level_values("scenario")
    accuracy = profiles.to_numpy().mean(axis=1)
    disagreement = profiles.to_numpy().std(axis=1)

    fig, ax = plt.subplots(figsize=(7, 6))
    for name in common.SCENARIOS:
        mask = scenario == name
        ax.scatter(embedding[mask, 0], embedding[mask, 1], s=28, alpha=0.8, label=f"Scenario {name}")
    ax.legend(fontsize=8, markerscale=1.2)
    ax.set_title(f"The {len(profiles)} rotations, grouped by how the representations performed")
    for axis in (ax.xaxis, ax.yaxis):
        axis.set_ticks([])
    fig.tight_layout()
    fig.savefig(HERE / "difficulty_by_scenario.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    for values, name, label, cmap in [
        (accuracy, "difficulty_by_accuracy", "Mean top-k accuracy over the eight representations", "viridis"),
        (disagreement, "difficulty_by_disagreement", "Standard deviation over the eight representations", "magma"),
    ]:
        fig, ax = plt.subplots(figsize=(7, 6))
        points = ax.scatter(embedding[:, 0], embedding[:, 1], c=values, s=28, cmap=cmap)
        fig.colorbar(points, ax=ax, label=label)
        ax.set_title(label)
        for axis in (ax.xaxis, ax.yaxis):
            axis.set_ticks([])
        fig.tight_layout()
        fig.savefig(HERE / f"{name}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    hardest = np.argsort(accuracy)[:5]
    print("  wrote difficulty_by_scenario.png, difficulty_by_accuracy.png "
          "and difficulty_by_disagreement.png")
    print("\n  Hardest rotations, averaged over the eight representations:")
    for i in hardest:
        s, r = profiles.index[i]
        rotation = summary[(summary["scenario"] == s) & (summary["rotation_index"] == r)]["rotation"].iloc[0]
        print(f"    scenario {s}  {rotation:16}  mean top-k accuracy {accuracy[i]:.3f}")


if __name__ == "__main__":
    main()
