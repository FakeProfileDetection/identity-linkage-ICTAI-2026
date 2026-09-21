"""B-ML-RF: identify the probe's author with a Random Forest over keystroke timings.

Created: 2026-09-20

For one gallery-probe rotation, a Random Forest is trained on the gallery
observations with one class per enrolled participant. Each probe observation is
then scored against every enrolled identity with predict_proba, the identities
are ranked by that score, and ACC@k records whether the correct one is among
the top k. The classifier is fitted once per seed and the accuracies are
averaged over the seeds.

Some feature cells are empty, because a participant did not produce that key or
digraph in that observation. How they are filled matters, and it is the reason
this script exists rather than a shorter one:

All three apply the same rule to the gallery and to the probe, and differ only
in where the filling value comes from.

  gallery   The default, and the rule used for the results in this repository.
            An empty cell takes the average of that feature over the gallery
            samples that contain it. The same number goes into every empty
            cell of that feature, on either side. It is computed from the
            enrolled data alone and never depends on whose sample it is, so it
            carries no identity, and because both sides are filled the same
            way the classifier is tested on the same kind of input it was
            trained on. A feature present in no gallery sample at all is set
            to zero on both sides.

  self      From the observation itself: a missing hold-latency median takes
            the median hold latency this observation shows across the keys it
            does contain. Nothing outside the observation is consulted. Kept
            for comparison; it scores slightly lower.

    python random_forest.py                      # the results in this repository
    python random_forest.py --imputation dataset # reproduce the published numbers

writes the results table to experiments/results/.
"""

import argparse
import csv
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

HERE = Path(__file__).parent
SCENARIOS = HERE.parent / "gallery-probe-configurations"
RESULTS = HERE.parent / "results"

# Averaging over an empty selection is expected here: a rare key may appear in
# no gallery observation at all.  Those cases are handled explicitly below.
warnings.filterwarnings("ignore", message="Mean of empty slice", category=RuntimeWarning)

SEEDS = [42, 123, 456]
OBSERVATION = ["user_id", "platform_id", "video_id", "session_id"]
TIMINGS = ("HL", "IL", "PL", "RL", "FD")
STATISTICS = ("median", "mean", "std", "q1", "q3")

# Held fixed across every rotation.  Classes are balanced by construction, as
# every participant contributes the same number of gallery observations, so the
# class weighting has no effect and is set only to make that explicit.
FOREST = dict(n_estimators=500, max_depth=None, max_features="sqrt",
              class_weight="balanced")


def select(features, row, side):
    """The rows of `features` that this rotation puts in the gallery, or the probe."""
    ids = lambda field: [int(x) for x in str(row[f"{side}_{field}"]).split(",")]
    return (features["platform_id"].isin(ids("platforms"))
            & features["video_id"].isin(ids("topics"))
            & features["session_id"].isin(ids("sessions"))).to_numpy()


def fill_from_dataset(values, users):
    """Every observation filled from that participant's mean over all of theirs.

    This does not depend on the rotation, so it is computed once.
    """
    filled = values.copy()
    everyone = np.nanmean(values, axis=0)
    for user in np.unique(users):
        rows = users == user
        mean = np.nanmean(values[rows], axis=0)
        mean = np.where(np.isnan(mean), everyone, mean)
        filled[rows] = np.where(np.isnan(values[rows]), mean, values[rows])
    return filled


def timing_groups(columns):
    """Column positions grouped by what they measure, e.g. every hold-latency median.

    Used by the `self` strategy, which fills a missing feature from the same
    kind of measurement elsewhere in the same observation.
    """
    groups = {}
    for position, name in enumerate(columns):
        for timing in TIMINGS:
            if not name.startswith(timing + "_"):
                continue
            for statistic in STATISTICS:
                if name.endswith("_" + statistic):
                    groups.setdefault((timing, statistic), []).append(position)
                    break
            break
    return {key: np.array(positions) for key, positions in groups.items()}


def fill(values, users, gallery, probe, strategy, groups):
    """Fill empty cells, using the same rule for the gallery and the probe.

    Filling the two sides by different rules is not an option even when each
    rule is defensible on its own. Where a cell is empty on both sides — and
    with the full key set that is most of them — the two sides would then hold
    different kinds of quantity, and the classifier would be tested on inputs
    unlike the ones it was trained on. So each strategy below applies one rule
    everywhere, and they differ only in where the filling value comes from.
    """
    filled = values.copy()
    missing = np.isnan(values)

    if strategy == "self":
        # From the observation itself: a missing hold-latency median takes the
        # median hold latency this observation shows across the keys it does
        # contain. Nothing outside the observation is consulted.
        for row in range(len(values)):
            for positions in groups.values():
                absent = missing[row, positions]
                if not absent.any():
                    continue
                present = values[row, positions][~absent]
                filled[row, positions[absent]] = present.mean() if present.size else 0.0
        return filled

    if strategy == "gallery":
        # From an average over the gallery, across all enrolled participants.
        # No identity is used, but a probe's representation then depends on
        # which gallery it is matched against.
        across = np.nanmean(values[gallery], axis=0)
        across = np.where(np.isnan(across), 0.0, across)
        return np.where(missing, across, values)

    raise ValueError(strategy)


def accuracy(values, users, gallery, probe, pooled=False):
    """ACC@k for k = 1..5, averaged over the seeds.

    With `pooled`, a person's probe samples count as one probe: the forest's
    class probabilities are averaged over them before ranking. Otherwise every
    probe sample is identified on its own.
    """
    probe_users = users[probe]
    people, member = np.unique(probe_users, return_inverse=True)
    per_seed = []
    for seed in SEEDS:
        forest = RandomForestClassifier(random_state=seed, n_jobs=-1, **FOREST)
        forest.fit(values[gallery], users[gallery])
        scores = forest.predict_proba(values[probe])
        truth = probe_users
        if pooled:
            summed = np.zeros((len(people), scores.shape[1]))
            np.add.at(summed, member, scores)
            scores = summed / np.bincount(member)[:, None]
            truth = people
        ranked = forest.classes_[np.argsort(-scores, axis=1)]
        correct = ranked == truth[:, None]
        per_seed.append([correct[:, :k].any(axis=1).mean() for k in range(1, 6)])
    return np.mean(per_seed, axis=0)


def write_table(rows, path):
    """Fill the gallery-probe results template and save it."""
    template = list(csv.reader((SCENARIOS / "results_template.tsv").open(newline=""), delimiter="\t"))
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
    with path.open("w", newline="") as f:
        csv.writer(f, delimiter="\t").writerows(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--imputation", choices=["gallery", "self", "dataset"], default="gallery")
    parser.add_argument("--features", default="features.parquet")
    parser.add_argument("--probe", choices=["pooled", "separate"], default="pooled",
                        help="pooled (default): a person's probe samples count as one probe, "
                             "with the class probabilities averaged over them, as the other "
                             "representations do; separate: identify every probe sample on its own")
    parser.add_argument("--output", default=None,
                        help="results file; defaults to B-ML-RF.tsv under experiments/results")
    args = parser.parse_args()

    features = pd.read_parquet(HERE / args.features)
    columns = [c for c in features.columns if c not in OBSERVATION]
    values = features[columns].to_numpy(dtype=float)
    users = features["user_id"].to_numpy()
    print(f"{len(columns)} features, {len(features)} observations, "
          f"{np.isnan(values).mean():.1%} of cells empty")
    print(f"imputation: {args.imputation}; probes: {args.probe}\n")

    precomputed = fill_from_dataset(values, users) if args.imputation == "dataset" else None
    groups = timing_groups(columns)

    scenarios = pd.read_csv(SCENARIOS / "scenarios.csv", dtype=str)
    rows = []
    for n, (_, rotation) in enumerate(scenarios.iterrows(), start=1):
        gallery, probe = select(features, rotation, "gallery"), select(features, rotation, "probe")
        prepared = (precomputed if precomputed is not None
                    else fill(values, users, gallery, probe, args.imputation, groups))
        rows.append(accuracy(prepared, users, gallery, probe, pooled=args.probe == "pooled"))
        if n % 20 == 0 or n == len(scenarios):
            print(f"  {n}/{len(scenarios)} rotations")

    path = Path(args.output) if args.output else RESULTS / "B-ML-RF.tsv"
    write_table(rows, path)
    print(f"\nwrote {path}")

    summary = pd.DataFrame(rows, columns=[f"ACC@{k}" for k in range(1, 6)])
    summary["scenario"] = scenarios["scenario"].to_numpy()
    print()
    print(summary.groupby("scenario")[["ACC@1", "ACC@3", "ACC@5"]].mean().round(3).to_string())


if __name__ == "__main__":
    main()
