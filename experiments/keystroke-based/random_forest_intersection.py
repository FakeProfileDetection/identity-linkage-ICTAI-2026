"""B-ML-RF, second design: choose the features from the gallery, for each rotation.

Created: 2026-09-20

This is an alternative to `random_forest.py` and is kept beside it. The two
differ in one decision. `random_forest.py` uses the same features for every
rotation and fills the empty cells. This script chooses the features afresh
for each rotation, looking only at that rotation's gallery, and fills as
little as the chosen threshold allows.

How one rotation is evaluated:

1. Look at the gallery only. Keep a feature if the key or digraph behind it
   was produced in at least a given share of the gallery's samples. The probe
   is not consulted, so nothing about the probe influences what is measured.

2. Any cell still empty — a gallery sample that happened to lack one of the
   kept keys, or a probe that did — is filled. A probe cell always takes the
   average of that feature over the whole gallery: the same number for every
   probe, never depending on whose sample it is. A gallery cell takes the same
   gallery-wide average by default (`--gallery-fill average`), or, with
   `--gallery-fill person`, first the average over that participant's other
   gallery samples, falling back to the gallery-wide average when they have
   none containing that key. The second is defensible because identities are
   known at enrolment; it can only make a difference where a participant has
   more than one gallery sample, which is scenarios 3.1, 3.2, 4.1 and 4.2.

3. Train the Random Forest on the gallery and rank the enrolled identities
   for each probe, exactly as in `random_forest.py`.

The threshold trades data against filling. At 100% only keys and digraphs
present in every gallery sample are kept: nothing is filled on the gallery
side, but almost no digraphs survive. Lowering it keeps more digraphs at the
cost of more filling. The script reports both, per rotation, so the trade-off
is visible rather than assumed.

The feature set differs from one rotation to the next, which is the cost of
this design: comparisons between configurations are then partly comparisons
between different feature sets. The report shows how many features each
rotation used.

    python random_forest_intersection.py --present-in 0.9

writes to experiments/results/ as B-ML-RF-intersection.tsv by default.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from random_forest import FOREST, OBSERVATION, SEEDS, select, write_table

HERE = Path(__file__).parent
RESULTS = HERE.parent / "results"


def chosen_features(missing, gallery, present_in):
    """Positions of the features present in at least `present_in` of the gallery samples."""
    share_present = 1 - missing[gallery].mean(axis=0)
    return (share_present >= present_in).nonzero()[0]


def fill_from_gallery(values, users, gallery, columns, gallery_fill):
    """Fill empty cells. Probes always take the gallery-wide average; see the docstring."""
    chosen = values[:, columns]
    average = np.nanmean(chosen[gallery], axis=0)
    average = np.where(np.isnan(average), 0.0, average)    # present nowhere in the gallery
    filled = np.where(np.isnan(chosen), average, chosen)
    if gallery_fill == "person":
        for user in np.unique(users[gallery]):
            rows = (users == user) & gallery
            own = np.nanmean(chosen[rows], axis=0)
            own = np.where(np.isnan(own), average, own)
            filled[rows] = np.where(np.isnan(chosen[rows]), own, chosen[rows])
    return filled


def accuracy(matrix, users, gallery, probe):
    """ACC@k for k = 1..5, averaged over the seeds."""
    per_seed = []
    for seed in SEEDS:
        forest = RandomForestClassifier(random_state=seed, n_jobs=-1, **FOREST)
        forest.fit(matrix[gallery], users[gallery])
        ranked = forest.classes_[np.argsort(-forest.predict_proba(matrix[probe]), axis=1)]
        correct = ranked == users[probe][:, None]
        per_seed.append([correct[:, :k].any(axis=1).mean() for k in range(1, 6)])
    return np.mean(per_seed, axis=0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", default="features.parquet",
                        help="a table with many keys and digraphs, since this script "
                             "does its own choosing")
    parser.add_argument("--present-in", type=float, default=1.0,
                        help="keep a feature if present in at least this share of the "
                             "gallery's samples; 1.0 keeps only what every sample has")
    parser.add_argument("--gallery-fill", choices=["average", "person"], default="average",
                        help="how an empty GALLERY cell is filled: the gallery-wide average, "
                             "or that participant's other gallery samples first")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    features = pd.read_parquet(HERE / args.features)
    columns = [c for c in features.columns if c not in OBSERVATION]
    values = features[columns].to_numpy(dtype=float)
    missing = np.isnan(values)
    users = features["user_id"].to_numpy()
    print(f"{len(columns)} features to choose from, {len(features)} observations")
    print(f"keeping features present in at least {args.present_in:.0%} of each gallery; "
          f"empty gallery cells filled from: {args.gallery_fill}\n")

    scenarios = pd.read_csv(HERE.parent / "gallery-probe-configurations" / "scenarios.csv",
                            dtype=str)
    rows, report = [], []
    for n, (_, rotation) in enumerate(scenarios.iterrows(), start=1):
        gallery, probe = select(features, rotation, "gallery"), select(features, rotation, "probe")
        chosen = chosen_features(missing, gallery, args.present_in)
        matrix = fill_from_gallery(values, users, gallery, chosen, args.gallery_fill)
        rows.append(accuracy(matrix, users, gallery, probe))
        report.append({
            "scenario": rotation["scenario"],
            "features": len(chosen),
            "filled gallery": missing[np.ix_(gallery.nonzero()[0], chosen)].mean(),
            "filled probe": missing[np.ix_(probe.nonzero()[0], chosen)].mean(),
        })
        if n % 20 == 0 or n == len(scenarios):
            print(f"  {n}/{len(scenarios)} rotations")

    path = Path(args.output) if args.output else RESULTS / "B-ML-RF-intersection.tsv"
    write_table(rows, path)
    print(f"\nwrote {path}")

    summary = pd.DataFrame(report)
    for k in (1, 3, 5):
        summary[f"ACC@{k}"] = [r[k - 1] for r in rows]
    print()
    print(summary.groupby("scenario").agg(
        {"ACC@1": "mean", "ACC@3": "mean", "ACC@5": "mean",
         "features": ["min", "max"], "filled gallery": "mean", "filled probe": "mean"}
    ).round(3).to_string())
    print(f"\nmean ACC@1 {summary['ACC@1'].mean():.3f}   ACC@5 {summary['ACC@5'].mean():.3f}   "
          f"filled gallery {summary['filled gallery'].mean():.1%}   probe {summary['filled probe'].mean():.1%}")


if __name__ == "__main__":
    main()
