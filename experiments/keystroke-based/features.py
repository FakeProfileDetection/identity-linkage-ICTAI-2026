"""Build keystroke timing features from the keypairs table.

Created: 2026-09-20

Each observation — one participant, on one platform, for one topic, in one
session — becomes one row of timing statistics.

Two kinds of timing are used, following Section III-B of the paper:

  hold latency    how long a key is held down, from press to release
  interval times  the timing between two consecutive keys, in four forms:
                    press of the first to press of the second
                    release of the first to press of the second
                    release of the first to release of the second
                    press of the first to release of the second

For every key and every digraph we record the median, mean, standard
deviation, first quartile, and third quartile.

By default every key seen in the data is kept, along with the ten digraphs
that appear in the most observations. That is the feature set the paper used.
Both choices can be changed from the command line: --key-coverage 0.9 keeps
only keys appearing in at least 90% of observations, and --digram-coverage
widens the digraphs. The experiment script that chooses features per gallery
needs a wide table to choose from, and a column that is computed but never
chosen costs nothing.

A cell is left empty when the participant did not produce that key or digraph
in that observation. Filling those in is the job of the experiment script, not
this one, because what may legitimately be used to fill them depends on which
observations are in the gallery.

    python features.py

writes features.parquet, one row per observation.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
KEYPAIRS = HERE.parent.parent / "datasets" / "clean-data" / "dataset" / "keypairs" / "keypairs.parquet"

KEY_COVERAGE = 0.0     # keep every key: the feature set the paper used
N_DIGRAMS = 10
OBSERVATION = ["user_id", "platform_id", "video_id", "session_id"]
STATISTICS = ["median", "mean", "std", "q1", "q3"]


def load_keypairs():
    """Valid, non-outlier key pairs."""
    kp = pd.read_parquet(KEYPAIRS, columns=OBSERVATION + [
        "key1", "key2", "key1_press", "key1_release", "key2_press", "key2_release",
        "valid", "outlier"])
    kp = kp[kp["valid"] & ~kp["outlier"]].copy()
    kp["key1"] = kp["key1"].astype(str)
    kp["digram"] = kp["key1"] + kp["key2"].astype(str)
    # Every timing is taken straight from the four press and release
    # timestamps, so nothing averaged or filled in upstream can reach here.
    kp["HL"] = kp["key1_release"] - kp["key1_press"]     # hold latency
    kp["IL"] = kp["key2_press"] - kp["key1_release"]     # release of first to press of second
    kp["PL"] = kp["key2_press"] - kp["key1_press"]       # press to press
    kp["RL"] = kp["key2_release"] - kp["key1_release"]   # release to release
    kp["FD"] = kp["key2_release"] - kp["key1_press"]     # press of first to release of second
    return kp


def coverage(kp, column):
    """Share of observations in which each key, or digraph, appears."""
    n = kp.groupby(OBSERVATION, observed=True).ngroups
    return kp.groupby(column, observed=True)[OBSERVATION].apply(
        lambda g: len(g.drop_duplicates())) / n


def statistics(kp, column, kept, value_columns, prefix):
    """Five statistics per observation, for each kept key or digraph."""
    sub = kp[kp[column].isin(kept)]
    grouped = sub.groupby(OBSERVATION + [column], observed=True)[value_columns]
    table = grouped.agg(["median", "mean", "std", "count",
                         ("q1", lambda s: s.quantile(0.25)),
                         ("q3", lambda s: s.quantile(0.75))])

    frames = []
    for value in value_columns:
        part = table[value].copy()
        # A key seen once has no spread.  That is a measurement of zero, not a
        # missing value, so it must not be confused with one.
        part["std"] = part["std"].where(part["count"] > 1, 0.0)
        part = part.drop(columns="count")
        part = part.unstack(column)
        part.columns = [f"{prefix}{value}_{name}_{stat}" for stat, name in part.columns]
        frames.append(part)
    return pd.concat(frames, axis=1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key-coverage", type=float, default=KEY_COVERAGE,
                        help="keep keys appearing in at least this share of observations; "
                             "the default of 0 keeps every key, which is the set the paper used")
    parser.add_argument("--digram-coverage", type=float, default=None,
                        help="keep every digraph appearing in at least this share of "
                             "observations, instead of the ten most widely seen")
    parser.add_argument("--output", default="features.parquet")
    args = parser.parse_args()

    kp = load_keypairs()
    observations = kp[OBSERVATION].drop_duplicates().sort_values(OBSERVATION)
    print(f"{len(kp):,} key pairs over {len(observations):,} observations")

    key_cov = coverage(kp, "key1")
    keys = sorted(key_cov[key_cov >= args.key_coverage].index)
    digram_cov = coverage(kp, "digram").sort_values(ascending=False)
    if args.digram_coverage is None:
        digrams = sorted(digram_cov.head(N_DIGRAMS).index)
    else:
        digrams = sorted(digram_cov[digram_cov >= args.digram_coverage].index)
    print(f"kept {len(keys)} of {len(key_cov)} keys, each in at least "
          f"{args.key_coverage:.0%} of observations")
    print(f"kept {len(digrams)} of {len(digram_cov)} digraphs, the least covered in "
          f"{digram_cov[digrams].min():.0%} of observations")

    hold = statistics(kp, "key1", keys, ["HL"], "")
    intervals = statistics(kp, "digram", digrams, ["IL", "PL", "RL", "FD"], "")
    features = observations.set_index(OBSERVATION).join([hold, intervals]).reset_index()

    value_columns = [c for c in features.columns if c not in OBSERVATION]
    missing = features[value_columns].isna().to_numpy()
    print(f"\n{len(value_columns)} features, {features.shape[0]} rows")
    for label, cols in [("hold latency", [c for c in value_columns if c.startswith("HL_")]),
                        ("interval times", [c for c in value_columns if not c.startswith("HL_")])]:
        share = features[cols].isna().to_numpy().mean()
        print(f"  {label:15} {len(cols):4d} features, {share:5.1%} of cells empty")
    print(f"  {'overall':15} {len(value_columns):4d} features, {missing.mean():5.1%} of cells empty")

    out = HERE / args.output
    features.to_parquet(out, index=False)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
