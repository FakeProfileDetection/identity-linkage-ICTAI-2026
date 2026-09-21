"""CB-ITAD.25, CB-ITAD.5, CB-ITAD.75: combine the keystroke score and the text score.

Created: 2026-09-20

Score-level fusion, equation 3 of the paper. For one rotation, the keystroke
representation (`../keystroke-based/itad.py`) and the text representation
(`../text-based/run.py`) have each already produced a table of scores, one
for every pair of an enrolled person and a probe. Each table is rescaled to
run from 0 to 1 using its own smallest and largest entry, and the two are
then combined as

    fused = alpha * keystroke + (1 - alpha) * text

with alpha, the weight on the keystroke score, at 0.25, 0.5 and 0.75. The
enrolled people are ranked for each probe by the fused score, and ACC@k
records whether the right one is among the top k. Nothing is trained and
nothing is random.

Both inputs are the score tables the other two scripts keep in their
`scores/` directories, so run those first.

    python run.py

writes ../results/CB-ITAD.25.tsv, CB-ITAD.5.tsv and CB-ITAD.75.tsv.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "gallery-probe-configurations"))
from rotations import load, rank_accuracy, write_table

RESULTS = HERE.parent / "results"
WEIGHTS = {0.25: "CB-ITAD.25", 0.5: "CB-ITAD.5", 0.75: "CB-ITAD.75"}


def score_tables(path):
    """{rotation_index: 61 x 61 array}, rows enrolled people, columns probes, people sorted."""
    scores = pd.read_parquet(path)
    people = sorted(scores["gallery_person"].unique())
    tables = {}
    for index, part in scores.groupby("rotation_index"):
        table = part.pivot(index="gallery_person", columns="probe_person", values="score")
        tables[int(index)] = table.reindex(index=people, columns=people).to_numpy(dtype=float)
    return tables, people


def rescaled(table):
    """The table mapped onto 0..1 by its own minimum and maximum; unchanged if flat."""
    low, high = table.min(), table.max()
    return (table - low) / (high - low) if high > low else table


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keystroke-scores", default=str(HERE.parent / "keystroke-based" / "scores" / "B-ITAD.parquet"))
    parser.add_argument("--text-scores", default=str(HERE.parent / "text-based" / "scores" / "C-Emb-Nomic.parquet"))
    parser.add_argument("--results-dir", default=str(RESULTS))
    args = parser.parse_args()

    keystroke, people_k = score_tables(args.keystroke_scores)
    text, people_t = score_tables(args.text_scores)
    assert people_k == people_t, "the two score tables cover different people"
    scenarios = load()
    assert len(keystroke) == len(text) == len(scenarios), "score tables do not cover all rotations"
    print(f"{len(scenarios)} rotations, {len(people_k)} people")

    rows = {alpha: [] for alpha in WEIGHTS}
    for index in range(len(scenarios)):
        k, t = rescaled(keystroke[index]), rescaled(text[index])
        for alpha in WEIGHTS:
            rows[alpha].append(rank_accuracy(alpha * k + (1 - alpha) * t))

    for alpha, code in WEIGHTS.items():
        path = Path(args.results_dir) / f"{code}.tsv"
        write_table(rows[alpha], path)
        summary = pd.DataFrame(rows[alpha], columns=[f"ACC@{k}" for k in range(1, 6)])
        print(f"{code}: mean ACC@1 {summary['ACC@1'].mean():.3f}   ACC@5 {summary['ACC@5'].mean():.3f}   -> {path}")


if __name__ == "__main__":
    main()
