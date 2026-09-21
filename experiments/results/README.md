# Results

Created: 2026-09-20

ACC@k for k = 1…5, for each of the eight identity representations, on each of
the 171 gallery–probe rotations. These are the numbers behind every figure and
table in Section IV of the paper.

## Files

**`<representation>.tsv`** — one file per representation, in the gallery–probe
format described in `../gallery-probe-configurations/README.md`. One row per
rotation, then a `mean` and a `std` row closing each scenario block. These are
what the experiments in `../text-based/`, `../keystroke-based/` and
`../similarity-fusion/` write.

| File | Representation | Section III-B |
|---|---|---|
| `C-Emb-Nomic.tsv` | Nomic Embed v2 sentence embedding, cosine similarity | text |
| `CB-POS.tsv` | open-class words replaced by part-of-speech tags, then embedded | text |
| `CB-FuncW.tsv` | only function words and punctuation kept, then embedded | text |
| `CB-ITAD.25.tsv` | score-level fusion, keystroke weight α = 0.25 | text + keystroke |
| `CB-ITAD.5.tsv` | score-level fusion, keystroke weight α = 0.50 | text + keystroke |
| `CB-ITAD.75.tsv` | score-level fusion, keystroke weight α = 0.75 | text + keystroke |
| `B-ITAD.tsv` | ITAD keystroke similarity | keystroke |
| `B-ML-RF.tsv` | Random Forest class probability on keystroke features | keystroke |

**`scenario-results.csv`** — the same numbers in one long table, which is what
everything in `analysis/` reads. `combine.py` builds it from the eight tables;
run it after rerunning any experiment.

| Column | Meaning |
|---|---|
| `scenario` | `1.1` … `5.2` |
| `rotation_index` | position of the rotation within its scenario, starting at 0 |
| `rotation` | the rotation's short name, e.g. `F-T1>I-T2` |
| `representation` | one of the eight codes above |
| `k` | 1 to 5 |
| `accuracy` | the share of probes whose correct identity was in the top k |

## Which numbers are which

Every table at this level is written by a script in a sibling directory, and
running those scripts regenerates it:

| Table | Written by | Same as the paper? |
|---|---|---|
| `B-ML-RF.tsv` | `../keystroke-based/random_forest.py` | No. The published results filled in missing feature values in a way that used each probe's identity; `../keystroke-based/README.md` explains; and a person's two probe samples in scenarios 3.x/4.x are now scored as one probe, as the other representations do. Mean ACC@1 0.51 against 0.88 published |
| `B-ITAD.tsv` | `../keystroke-based/itad.py` | Nearly. Invalid key pairs and outliers are now removed, which the published run did not do; the difference is a few thousandths |
| `C-Emb-Nomic.tsv` | `../text-based/run.py` | Yes, from the paper's own embedding files |
| `CB-POS.tsv`, `CB-FuncW.tsv` | `../text-based/run.py` | No. The published tables used embeddings from an earlier version of the Nomic model than the paper states; these use the version the paper describes, and come out a little higher |
| `CB-ITAD.25.tsv`, `CB-ITAD.5.tsv`, `CB-ITAD.75.tsv` | `../similarity-fusion/run.py` | Nearly; they inherit the small change in `B-ITAD.tsv` |

`as-published/` holds the eight tables exactly as they stood behind the
paper's figures, and the `scenario-results.csv` built from them, for anyone
who wants to compare. Within a few scenarios the published tables list the
rotations in a different order from `scenarios.csv`; the values are the same.

