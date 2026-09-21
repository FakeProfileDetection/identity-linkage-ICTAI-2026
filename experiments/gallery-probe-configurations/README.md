# Gallery–probe configurations

Created: 2026-09-20

Identity linkage is evaluated as a closed-set 1:N identification task. Some
observations are enrolled in the **gallery**, the rest are used as **probes**,
and each probe is matched against the gallery. A gallery–probe configuration
says which observations go on each side.

The ten configurations in Table II of the paper hold some contextual factors
fixed between gallery and probe and vary others. Each one expands into several
platform–topic rotations: scenario 1.1, for example, covers three platforms and
three topics, so nine rotations. There are 171 rotations in total, and every
experiment reports accuracy for each one.

## The ten configurations

In the variation notation, factors written before the dot are held constant
between gallery and probe; factors after it are varied. `P` is platform, `T` is
topic, `S` is session.

| # | Variation | Description | Rotations |
|---|---|---|---|
| **1.1** | `PT·S` | Cross-session, same platform and topic. Gallery session 1, probe session 2 | 9 (3 platforms × 3 topics) |
| **1.2** | `PT·S` | Cross-session, same platform and topic. Gallery session 2, probe session 1 | 9 (3 platforms × 3 topics) |
| **2.1** | `T·PS` | Cross-platform and cross-session, same topic. Gallery session 1, probe session 2 | 18 (6 platform pairs × 3 topics) |
| **2.2** | `T·PS` | Cross-platform and cross-session, same topic. Gallery session 2, probe session 1 | 18 (6 platform pairs × 3 topics) |
| **3.1** | `TS·P` | Cross-platform, both sessions pooled, single-platform gallery | 18 (6 platform pairs × 3 topics) |
| **3.2** | `TS·P` | Cross-platform, both sessions pooled, two-platform gallery | 9 (3 platform groups × 3 topics) |
| **4.1** | `S·PT` | Cross-platform and cross-topic, both sessions pooled, single-platform gallery | 36 (3 gallery platforms × 3 gallery topics × 2 probe platforms × 2 probe topics) |
| **4.2** | `S·PT` | Cross-platform and cross-topic, both sessions pooled, two-platform gallery | 18 (3 platform groups × 6 topic pairs) |
| **5.1** | `P·TS` | Cross-topic and cross-session, same platform. Gallery session 1, probe session 2 | 18 (3 platforms × 6 topic pairs) |
| **5.2** | `P·TS` | Cross-topic and cross-session, same platform. Gallery session 2, probe session 1 | 18 (3 platforms × 6 topic pairs) |

The pairs of configurations support the controlled comparisons in Section IV-B
of the paper:

| Effect | Comparison | What differs |
|---|---|---|
| Session | 1.1 vs 1.2 | Only the direction of the session change |
| Platform | 1.1 vs 2.1, 1.2 vs 2.2 | A platform change is added |
| Gallery size | 3.1 vs 3.2 | The gallery holds two platforms instead of one |
| Topic | 1.1 vs 5.1, 1.2 vs 5.2 | A topic change is added |

## Ids

Platform, topic, and session ids follow the dataset in `datasets/clean-data`:

| Platform | | Topic | | Session |
|---|---|---|---|---|
| 1 = Facebook (F) | | 1 = Coach Carter (T1) | | 1 = first session (S1) |
| 2 = Instagram (I) | | 2 = Oscar Slap (T2) | | 2 = second session (S2) |
| 3 = X (X) | | 3 = Trump/Zelensky (T3) | |

## Files

Run `python scenarios.py` to regenerate both files.

**`scenarios.csv`** — the 171 rotations, one per row. Every experiment reads
this to know which observations to enroll and which to use as probes.

| Column | Meaning |
|---|---|
| `scenario` | `1.1` … `5.2` |
| `variation` | the notation from Table II, e.g. `PT.S` |
| `description` | the configuration in words |
| `rotation` | a short name for this platform–topic rotation, ignoring session. Rotations of 1.1 and 1.2 share a label so they can be paired in the session comparison |
| `gallery_platforms`, `gallery_topics`, `gallery_sessions` | comma-separated ids enrolled in the gallery |
| `probe_platforms`, `probe_topics`, `probe_sessions` | comma-separated ids used as probes |
| `gallery_samples_per_user`, `probe_samples_per_user` | observations per user on each side |

**`results_template.tsv`** — an empty results table in the gallery–probe
format. Each experiment fills in `k=1` through `k=5` for every rotation, writes
the per-scenario mean and standard deviation into the two summary rows at the
end of each block, and saves the result under `experiments/results/`.

