# Experiments

Created: 2026-09-20

Each experiment reads the dataset in `../datasets/clean-data`, evaluates one or
more identity representations on all 171 gallery–probe rotations, and writes a
results table into `results/`.

## Directories

| Directory | What it produces |
|---|---|
| `gallery-probe-configurations/` | the 171 rotations and the empty results table. Everything else reads these |
| `text-based/` | `C-Emb-Nomic`, `CB-POS`, `CB-FuncW` |
| `keystroke-based/` | `B-ITAD`, `B-ML-RF` |
| `similarity-fusion/` | `CB-ITAD.25`, `CB-ITAD.5`, `CB-ITAD.75` |
| `results/` | the eight results tables, and the combined file the analysis reads |

## Order

`gallery-probe-configurations/scenarios.py` first, since the rest read
`scenarios.csv`. Then the text and keystroke experiments, which can run in
either order. Fusion runs last, because it combines the text similarity scores
with the ITAD keystroke similarity scores. Then `results/combine.py` joins the
eight tables into the one file the analysis reads.

## How a rotation is evaluated

Identity linkage is a closed-set 1:N identification task. For one rotation:

1. Take the gallery observations and the probe observations that the rotation
   names, for all 61 users.
2. Score every probe against every enrolled identity.
3. Rank the identities by score and record whether the correct one is in the
   top k, for k = 1…5.
4. ACC@k is the share of probes for which it is.

The eight representations differ only in step 2, in how the score is computed.

## Status

All eight representations have scripts, and `results/README.md` says for each
table whether it matches the paper. Some differ from the published numbers on
purpose: the Random Forest, whose published results filled in missing feature
values in a way that used each probe's identity; the ITAD matcher, which now
leaves out invalid key pairs and outliers; and the two transformed-text
representations, which now use the embedding model the paper names. The
published tables are kept in `results/as-published/`.
