"""Section IV-D: are the differences between representations statistically supported?

Created: 2026-09-20
Updated: 2026-09-25

Within one gallery-probe configuration every representation is evaluated on the
same platform-topic rotations, so the rotations act as blocks and the eight
representations are repeated measurements on them.  The Friedman test asks
whether all eight perform equivalently.  Where it rejects that, the Nemenyi
post hoc procedure compares the average ranks pairwise while controlling the
family-wise error rate.

Two representations whose average ranks differ by less than the critical
difference cannot be told apart at alpha = 0.05.

The average ranks are also drawn as Figure 4: within every rotation the eight
representations are ranked by mean top-k accuracy, best first, and the ranks
are averaged over the rotations of each configuration.  Lower is better.

    python compare_representations.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scikit_posthocs as sp
from scipy.stats import friedmanchisquare, studentized_range

sys.path.append(str(Path(__file__).resolve().parent.parent))
import common

HERE = Path(__file__).parent
ALPHA = 0.05


def rotation_table(summary, scenario):
    """Rows are rotations, columns are representations, values are mean top-k accuracy."""
    table = (
        summary[summary["scenario"] == scenario]
        .pivot_table(index="rotation_index", columns="representation", values="mean_top_k")
    )
    return table[common.REPRESENTATIONS]


def critical_difference(n_representations, n_rotations):
    """The smallest average-rank gap that counts as significant."""
    q = studentized_range.ppf(1 - ALPHA, n_representations, np.inf) / np.sqrt(2)
    return q * np.sqrt(n_representations * (n_representations + 1) / (6 * n_rotations))


def main():
    summary = common.mean_top_k(common.load())

    omnibus = []
    ranks = {}
    for scenario in common.SCENARIOS:
        table = rotation_table(summary, scenario)
        statistic, p = friedmanchisquare(*[table[c].to_numpy() for c in table.columns])
        n_rotations, n_representations = table.shape

        # Kendall's W, how much the rotations agree on the ordering.
        # 0 is no agreement, 1 is every rotation giving the same ordering.
        rank_sums = table.rank(axis=1, ascending=False).sum(axis=0)
        spread = ((rank_sums - rank_sums.mean()) ** 2).sum()
        kendall_w = 12 * spread / (n_rotations ** 2 * (n_representations ** 3 - n_representations))

        omnibus.append({
            "scenario": scenario,
            "rotations": n_rotations,
            "chi_square": round(statistic, 4),
            "p_value": p,
            "kendalls_w": round(kendall_w, 4),
            "significant": p < ALPHA,
            "critical_difference": round(critical_difference(n_representations, n_rotations), 4),
        })

        ranks[scenario] = table.rank(axis=1, ascending=False).mean()

        if p < ALPHA:
            posthoc = sp.posthoc_nemenyi_friedman(table.to_numpy())
            posthoc.index = posthoc.columns = table.columns
            posthoc.round(6).to_csv(HERE / f"nemenyi_{scenario}.csv")

    pd.DataFrame(omnibus).to_csv(HERE / "friedman_results.csv", index=False)
    rank_table = pd.DataFrame(ranks).loc[common.REPRESENTATIONS, common.SCENARIOS]
    rank_table.round(4).to_csv(HERE / "average_ranks.csv")
    print("  wrote friedman_results.csv, average_ranks.csv, and one nemenyi_<scenario>.csv per scenario")

    # Figure 4, drawn as the paper prints it: no title, the scenario labels
    # without the word "Scenario", and wide enough to span both columns.
    common.heatmap(
        rank_table,
        None,
        "Average Rank (1=best)",
        [HERE / "rank_heatmap.pdf", HERE / "rank_heatmap.png"],
        ".1f",
        common.light_greens(reverse=True),
        tick_prefix="",
        figsize=(14, 4),
        colorbar_label_size=15,
    )
    print()
    print(pd.DataFrame(omnibus).to_string(index=False))
    print()
    print("Average rank across all ten configurations, 1 = best:")
    print(rank_table.mean(axis=1).round(2).sort_values().to_string())


if __name__ == "__main__":
    main()
