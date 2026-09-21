"""Small helpers every experiment needs: which rows a rotation uses, and how to write results.

Created: 2026-09-20

    from rotations import load, select, write_table, rank_accuracy
"""

import csv
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent


def load():
    """The 171 rotations, as written by scenarios.py."""
    return pd.read_csv(HERE / "scenarios.csv", dtype=str)


def select(samples, rotation, side):
    """Which rows of `samples` this rotation puts on the given side, "gallery" or "probe".

    `samples` needs platform_id, video_id and session_id columns.
    """
    ids = lambda field: [int(x) for x in str(rotation[f"{side}_{field}"]).split(",")]
    return (samples["platform_id"].isin(ids("platforms"))
            & samples["video_id"].isin(ids("topics"))
            & samples["session_id"].isin(ids("sessions"))).to_numpy()


def rank_accuracy(scores):
    """ACC@k for k = 1..5 from a score table with one column per probe.

    Each column is one probe; each row is one enrolled person; the person in
    row j is the true author of the probe in column j. The probe is counted
    correct at k if that person is among the k highest scores in its column.
    """
    n = scores.shape[0]
    hits = np.zeros(5)
    for j in range(n):
        order = np.argsort(scores[:, j])
        for k in range(1, 6):
            hits[k - 1] += j in order[-k:]
    return hits / n


def write_table(rows, path):
    """Fill the gallery-probe results template with one row of ACC@1..5 per rotation."""
    template = list(csv.reader((HERE / "results_template.tsv").open(newline=""), delimiter="\t"))
    out, i, seen = [], 0, {}
    for line in template:
        line = list(line)
        if line[0] == "scenario":
            out.append(line)
        elif line[2] in ("mean", "std"):
            frame = pd.DataFrame(seen[line[0]])
            summary = frame.mean() if line[2] == "mean" else frame.std(ddof=1)
            line[6:11] = [f"{v:.4f}" for v in summary]
            out.append(line)
        else:
            line[6:11] = [f"{v:.4f}" for v in rows[i]]
            seen.setdefault(line[0], []).append(rows[i])
            out.append(line)
            i += 1
    assert i == len(rows), f"{i} rotations written, {len(rows)} expected"
    with Path(path).open("w", newline="") as f:
        csv.writer(f, delimiter="\t").writerows(out)
