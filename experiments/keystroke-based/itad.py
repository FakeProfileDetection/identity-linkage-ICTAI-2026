"""B-ITAD: identify the probe's author by comparing keystroke timing distributions.

Created: 2026-09-20

ITAD (Instance-based Tail Area Density) compares two typing patterns without
training a model. It is the keystroke representation the paper pairs with the
text embeddings in the fusion experiments, so this script also keeps the score
of every gallery-probe pair for `../similarity-fusion/` to use.

A pattern is built for each person on each side of a rotation, from all of
that person's samples on that side pooled together. Where the probe side holds
two samples per person, the two are treated as one larger sample from that
person. The pattern is:

  for every key            the list of its hold times, press to release
  for every pair of keys   the list of gaps from release of the first key to
                           press of the second

Two patterns are compared on the keys and pairs they both contain, and nothing
is filled in. For each value in the probe pattern, the score is the share of
the gallery pattern's values at or below it when the value sits at or below
the gallery's median, and the share above it otherwise; the comparison score
is the mean over every probe value of every shared key. Higher means more
alike. Each probe is then ranked against all 61 enrolled people, and ACC@k
records whether the right one is in the top k. There is no randomness, so
there are no seeds.

By default only valid key pairs that are not flagged as outliers are used. The
outlier flag marks a hold time over two seconds or a gap over two seconds, which
is the pause rule the paper describes. The published results used every row,
including invalid pairs and outliers; `--filter none` reproduces them.

    python itad.py                  # -> ../results/B-ITAD.tsv and scores/B-ITAD.parquet
    python itad.py --filter none    # the published treatment

Two details are kept from the original implementation because changing them
would change the numbers, and they are harmless: the hold time of a key is
collected both when it is the first key of a pair and when it is the second,
so most presses are counted twice; and the mean is taken over all probe values
at once, so keys with more values weigh more.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from random_forest import OBSERVATION, select, write_table

HERE = Path(__file__).parent
KEYPAIRS = HERE.parent.parent / "datasets" / "clean-data" / "dataset" / "keypairs" / "keypairs.parquet"
RESULTS = HERE.parent / "results"
SCORES = HERE / "scores"


def load_values(filter_rows):
    """One row per timing value: which sample it came from, which key or pair, the value."""
    kp = pd.read_parquet(KEYPAIRS, columns=OBSERVATION + [
        "key1", "key2", "key2_press", "key2_release", "HL", "IL", "valid", "outlier"])
    if filter_rows == "valid":
        kp = kp[kp["valid"] & ~kp["outlier"]]
    kp = kp.dropna(subset=["key1", "key2"])
    kp = kp.assign(key1=kp["key1"].astype(str), key2=kp["key2"].astype(str))

    # The stored HL and IL columns are used, as the original did, rather than
    # recomputing from timestamps. For valid pairs the two are identical; for
    # the invalid pairs that `--filter none` keeps, the stored columns are blank
    # where a timestamp is missing and those values are skipped, which is what
    # produced the published numbers.
    hold_first = kp.assign(feature=kp["key1"], value=kp["HL"])
    hold_second = kp.assign(feature=kp["key2"],
                            value=kp["key2_release"] - kp["key2_press"])
    gap = kp.assign(feature=kp["key1"] + kp["key2"], value=kp["IL"])
    values = pd.concat([hold_first, hold_second, gap])[OBSERVATION + ["feature", "value"]]
    return values.dropna(subset=["value"]).reset_index(drop=True)


def patterns(values, rows):
    """{person: {feature: sorted array of values}} pooled over the selected samples."""
    grouped = values[rows].groupby(["user_id", "feature"], sort=False)["value"]
    out = {}
    for (person, feature), series in grouped:
        out.setdefault(person, {})[feature] = np.sort(series.to_numpy(dtype=float))
    return out


def score_matrix(gallery, probe, people):
    """scores[i, j]: how alike person i's gallery pattern is to person j's probe pattern."""
    n = len(people)
    total = np.zeros((n, n))
    count = np.zeros((n, n))
    index = {person: j for j, person in enumerate(people)}

    for i, person in enumerate(people):
        for feature, g in gallery.get(person, {}).items():
            # every probe value of this feature, tagged with whose it is
            owners, xs = [], []
            for other, pattern in probe.items():
                if feature in pattern:
                    owners.append(np.full(len(pattern[feature]), index[other]))
                    xs.append(pattern[feature])
            if not xs:
                continue
            owners, xs = np.concatenate(owners), np.concatenate(xs)
            below = np.searchsorted(g, xs, side="right") / len(g)   # share of g at or below x
            s = np.where(xs <= np.median(g), below, 1 - below)
            total[i] += np.bincount(owners, weights=s, minlength=n)
            count[i] += np.bincount(owners, minlength=n)

    with np.errstate(invalid="ignore"):
        return np.where(count > 0, total / count, 0.0)


def accuracy(scores):
    """ACC@k for k = 1..5: each probe (column) ranked against every enrolled person."""
    n = scores.shape[0]
    hits = np.zeros(5)
    for j in range(n):
        order = np.argsort(scores[:, j])          # ascending, as the original did
        for k in range(1, 6):
            hits[k - 1] += j in order[-k:]
    return hits / n


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--filter", choices=["valid", "none"], default="valid",
                        help="valid: only valid pairs that are not outliers (default); "
                             "none: every row, as the published results used")
    parser.add_argument("--output", default=None)
    parser.add_argument("--scores", default=None,
                        help="where to keep every gallery-probe score; default scores/B-ITAD.parquet")
    args = parser.parse_args()

    values = load_values(args.filter)
    samples = values[OBSERVATION].drop_duplicates().reset_index(drop=True)
    people = sorted(values["user_id"].unique())
    print(f"{len(values):,} timing values over {len(samples)} samples, {len(people)} people, "
          f"filter: {args.filter}\n")

    scenarios = pd.read_csv(HERE.parent / "gallery-probe-configurations" / "scenarios.csv", dtype=str)
    sample_of_value = values[OBSERVATION].merge(samples.reset_index(), on=OBSERVATION)["index"].to_numpy()

    rows, kept = [], []
    for n, (_, rotation) in enumerate(scenarios.iterrows(), start=1):
        gallery_samples = select(samples, rotation, "gallery")
        probe_samples = select(samples, rotation, "probe")
        gallery = patterns(values, gallery_samples[sample_of_value])
        probe = patterns(values, probe_samples[sample_of_value])
        scores = score_matrix(gallery, probe, people)
        rows.append(accuracy(scores))
        kept.append(pd.DataFrame({
            "rotation_index": n - 1,
            "gallery_person": np.repeat(people, len(people)),
            "probe_person": np.tile(people, len(people)),
            "score": scores.ravel(),
        }))
        if n % 20 == 0 or n == len(scenarios):
            print(f"  {n}/{len(scenarios)} rotations")

    path = Path(args.output) if args.output else RESULTS / "B-ITAD.tsv"
    write_table(rows, path)
    SCORES.mkdir(exist_ok=True)
    scores_path = Path(args.scores) if args.scores else SCORES / "B-ITAD.parquet"
    pd.concat(kept, ignore_index=True).to_parquet(scores_path, index=False)
    print(f"\nwrote {path}\nwrote {scores_path}")

    summary = pd.DataFrame(rows, columns=[f"ACC@{k}" for k in range(1, 6)])
    summary["scenario"] = scenarios["scenario"].to_numpy()
    print()
    print(summary.groupby("scenario")[["ACC@1", "ACC@3", "ACC@5"]].mean().round(3).to_string())
    print(f"\nmean ACC@1 {summary['ACC@1'].mean():.3f}   ACC@5 {summary['ACC@5'].mean():.3f}")


if __name__ == "__main__":
    main()
