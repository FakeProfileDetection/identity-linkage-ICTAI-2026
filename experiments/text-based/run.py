"""C-Emb-Nomic, CB-POS, CB-FuncW: identify the probe's author by comparing text embeddings.

Created: 2026-09-20

For one rotation, every person's gallery samples are averaged into one vector,
and their probe samples into another; where the probe side holds two samples
per person they are treated as one larger sample, as for the keystroke
representations. Each probe vector is scored against every gallery vector by
cosine similarity, the enrolled people are ranked by that score, and ACC@k
records whether the right one is among the top k. Nothing is trained and
nothing is random.

The three representations differ only in which embeddings they read:

    C-Emb-Nomic   embeddings/text_embeddings_nomic_v2.csv        the text as written
    CB-POS        embeddings/text_embeddings_pos_tags.csv        open-class words replaced by tags
    CB-FuncW      embeddings/text_embeddings_function_words.csv  only function words kept

Every gallery-probe score is kept in scores/, because the fusion experiments
combine these scores with the keystroke ones.

    python run.py                      # all three -> ../results/<code>.tsv
    python run.py --only CB-POS
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "gallery-probe-configurations"))
from rotations import load, rank_accuracy, select, write_table

RESULTS = HERE.parent / "results"
SCORES = HERE / "scores"
IDS = ["user_id", "platform_id", "video_id", "session_id"]
REPRESENTATIONS = {
    "C-Emb-Nomic": "text_embeddings_nomic_v2.csv",
    "CB-POS": "text_embeddings_pos_tags.csv",
    "CB-FuncW": "text_embeddings_function_words.csv",
}


def person_vectors(table, rows, people):
    """One vector per person: the mean of their selected samples, scaled to unit length."""
    columns = [c for c in table.columns if c.startswith("emb_")]
    means = table[rows].groupby("user_id")[columns].mean().reindex(people)
    vectors = means.to_numpy(dtype=float)
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / np.where(norms == 0, 1, norms)


def evaluate(code, filename, embeddings_dir, results_dir):
    table = pd.read_csv(embeddings_dir / filename)
    people = sorted(table["user_id"].unique())
    scenarios = load()
    rows, kept = [], []
    for n, (_, rotation) in enumerate(scenarios.iterrows(), start=1):
        gallery = person_vectors(table, select(table, rotation, "gallery"), people)
        probe = person_vectors(table, select(table, rotation, "probe"), people)
        scores = gallery @ probe.T                # cosine: rows = enrolled people, columns = probes
        rows.append(rank_accuracy(scores))
        kept.append(pd.DataFrame({"rotation_index": n - 1,
                                  "gallery_person": np.repeat(people, len(people)),
                                  "probe_person": np.tile(people, len(people)),
                                  "score": scores.ravel()}))
    write_table(rows, results_dir / f"{code}.tsv")
    SCORES.mkdir(exist_ok=True)
    pd.concat(kept, ignore_index=True).to_parquet(SCORES / f"{code}.parquet", index=False)

    summary = pd.DataFrame(rows, columns=[f"ACC@{k}" for k in range(1, 6)])
    summary["scenario"] = scenarios["scenario"].to_numpy()
    print(f"{code}: mean ACC@1 {summary['ACC@1'].mean():.3f}   ACC@5 {summary['ACC@5'].mean():.3f}"
          f"   -> {results_dir / (code + '.tsv')}")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", choices=list(REPRESENTATIONS), default=None)
    parser.add_argument("--embeddings-dir", default=str(HERE / "embeddings"))
    parser.add_argument("--results-dir", default=str(RESULTS))
    args = parser.parse_args()

    for code, filename in REPRESENTATIONS.items():
        if args.only and code != args.only:
            continue
        evaluate(code, filename, Path(args.embeddings_dir), Path(args.results_dir))


if __name__ == "__main__":
    main()
