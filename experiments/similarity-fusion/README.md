# Score-level fusion

Created: 2026-09-20

The three representations that combine a keystroke score with a text score.

| Representation | Weight on the keystroke score | Results |
|---|---|---|
| `CB-ITAD.25` | 0.25 | `../results/CB-ITAD.25.tsv` |
| `CB-ITAD.5` | 0.50 | `../results/CB-ITAD.5.tsv` |
| `CB-ITAD.75` | 0.75 | `../results/CB-ITAD.75.tsv` |

## Running it

```bash
python run.py        # a few seconds -> ../results/CB-ITAD.25.tsv, CB-ITAD.5.tsv, CB-ITAD.75.tsv
```

It reads the score tables that the two other experiments keep —
`../keystroke-based/scores/B-ITAD.parquet` and
`../text-based/scores/C-Emb-Nomic.parquet` — so run `../keystroke-based/itad.py`
and `../text-based/run.py` first.

## What it does

For every rotation, each of the two representations has already scored every
pair of an enrolled person and a probe: 61 × 61 numbers. The two tables are
not on the same scale — ITAD scores are fractions near 0.5, cosine similarities
sit near 1 — so each is first rescaled to run from 0 to 1 using its own
smallest and largest entry. They are then combined as

    fused = α × keystroke + (1 − α) × text

with α at 0.25, 0.5 and 0.75. The enrolled people are ranked for each probe by
the fused score and ACC@k records whether the right one is among the top k.
Nothing is trained and nothing is random.

Rescaling uses only the scores, never who anyone is, so nothing about a probe's
identity enters. Because every entry in the table involves one probe, the
rescaling does depend on the set of probes in the rotation; the same table is
used for every probe in it, so no probe is treated differently from another.

## Vocabulary

**Rotation**: one of the 171 individual experiments the ten scenarios expand
into. **Gallery** and **probe**: the enrolled samples and the samples to
identify. The keystroke and text scripts describe how each side is turned into
one pattern or vector per person.
