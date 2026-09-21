"""Combine the eight results tables into scenario-results.csv.

Created: 2026-09-20

Reads <representation>.tsv for each of the eight representations, drops the
mean and std rows, and writes one long table with a row per rotation,
representation and k. That table is what everything in ../../analysis reads.
Run it after any of the experiments has been rerun:

    python combine.py
"""

import csv
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
SCENARIOS = HERE.parent / "gallery-probe-configurations" / "scenarios.csv"
REPRESENTATIONS = ["C-Emb-Nomic", "CB-POS", "CB-FuncW", "CB-ITAD.25", "CB-ITAD.5",
                   "CB-ITAD.75", "B-ITAD", "B-ML-RF"]


def read_table(path):
    """The per-rotation rows of a results table, as an array of ACC@1..5."""
    with open(path, newline="") as f:
        rows = [r for r in csv.reader(f, delimiter="\t")]
    body = [r for r in rows[1:] if r[2] not in ("mean", "std")]
    return [[float(x) for x in r[6:11]] for r in body]


def main():
    rotations = pd.read_csv(SCENARIOS, dtype=str)
    rotations["rotation_index"] = rotations.groupby("scenario").cumcount()
    records = []
    for code in REPRESENTATIONS:
        table = read_table(HERE / f"{code}.tsv")
        if len(table) != len(rotations):
            raise SystemExit(f"{code}.tsv has {len(table)} rotations, expected {len(rotations)}")
        for (_, r), acc in zip(rotations.iterrows(), table):
            for k, value in enumerate(acc, start=1):
                records.append((r.scenario, r.rotation_index, r.rotation, code, k, f"{value:.4f}"))
    out = pd.DataFrame(records, columns=["scenario", "rotation_index", "rotation",
                                         "representation", "k", "accuracy"])
    out.to_csv(HERE / "scenario-results.csv", index=False)
    print(f"{len(out)} rows -> {HERE / 'scenario-results.csv'}")


if __name__ == "__main__":
    main()
