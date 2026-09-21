# Analysis

Created: 2026-09-20
Updated: 2026-09-20

Everything here reads one file, `experiments/results/scenario-results.csv`, and
writes the figures and tables of Section IV of the paper. The subdirectories
follow the sections.

Run all of it with:

```bash
cd analysis && ./run_all.sh
```

Or run any script on its own from its own directory.

The figures here are made from the current results tables, which differ from
the published paper in the ways `experiments/results/README.md` lists. To
regenerate the paper's own figures, point the scripts at the published
numbers:

```bash
RESULTS_CSV=../experiments/results/as-published/scenario-results.csv ./run_all.sh
```

## What each directory produces

| Directory | Paper | Script | Output |
|---|---|---|---|
| `a-overall-identity-linkage/` | Section IV-A, Figure 2 | `plot_heatmaps.py` | `accuracy_heatmap_k{1,3,5}.png`; its README explains the figure |
| `b-contextual-variations/` | Section IV-B, Figure 3 | `contextual_effects.py` | `variable_effect_heatmap.png`, `contextual_effects.csv`, `effect_size_heatmap.png`; its README explains the comparisons and the plots |
| `c-multi-modal-fusion/` | Section IV-C | `fusion_weights.py` | `fusion_weights.csv`, `fusion_weight_sweep.png`; its README explains the sweep |
| `d-statistical-analysis/` | Section IV-D, Figure 4 | `compare_representations.py` | `rank_heatmap.png`, `friedman_results.csv`, `average_ranks.csv`, `nemenyi_<scenario>.csv`; its README explains the tests and Figure 4 |
| `extra-plots/` | not in the paper | four scripts, see below | supporting views that were cut for space |

`common.py` holds the settings the scripts share: where the results live, the
eight representations in the order the paper uses them, the ten configurations,
and the colours. Setting `RESULTS_CSV` (a path relative to this directory)
makes every script read a different combined file.

`effect_size_heatmap.png`, next to Figure 3, is not in the paper. It shows the
rank-biserial correlation for the same 32 comparisons: −1 means every rotation
of the varied configuration scored below every rotation of the reference, +1
the reverse, 0 no tendency. It saturates at −1 for every text and fusion
representation under topic change because the two sets of rotations do not
overlap at all, which is the same fact Figure 3 shows as a large ΔAUK.

## The measure the figures use

Figures 3 and 4 summarise each gallery–probe rotation with a single number that
the paper calls AUK. `common.mean_top_k` computes it as the mean of ACC@k over
k = 1…5.

## Extra plots

These were left out of the paper for space. They use the same results file.

| Script | Output |
|---|---|
| `per_scenario_accuracy.py` | `accuracy_by_k_<scenario>.png` — accuracy at every k, not just 1, 3 and 5. `spread_<scenario>.png` — how much the rotations within one configuration vary, which the paper's averages hide |
| `critical_difference.py` | `critical_difference_<scenario>.png` — the Nemenyi result behind Section IV-D, showing which representations cannot be told apart |
| `contextual_panels.py` | `effect_<factor>.png` and `effect_summary.png` — the two sides of each comparison in Figure 3, rather than only the difference |
| `configuration_difficulty.py` | `difficulty_by_*.png` — a t-SNE view with the rotations as the unit instead of the representations, showing which rotations every representation found hard |

## Checks against the paper

The results tables were corrected after the paper was printed (see
`experiments/results/README.md`), so the figures these scripts write by default
differ from the published ones. `reproduce_paper.sh` runs the same scripts on
the published numbers (`experiments/results/as-published/`) into a separate
directory, leaving the current figures alone:

```bash
./reproduce_paper.sh            # prints where it put the figures
```

On those numbers the scripts reproduce the printed paper exactly:

- Figure 2: all 240 cells across the ACC@1, ACC@3 and ACC@5 panels match.
- Figure 3: all 32 cells match, both the values and the significance stars.
- Figure 4: all 80 cells match.
- Section IV-C: every accuracy range quoted in the text is reproduced by
  `fusion_weights.py`.
- Section IV-D: the Friedman test rejects the null hypothesis in all ten
  configurations, as the paper reports.

That is the evidence that the scripts are the paper's analysis; the current
figures then differ only because the inputs do.

One detail matters for Figure 4. Accuracies are recorded to four decimal
places, so two representations whose five accuracies sum to the same total
have the same mean top-k accuracy and should tie. Adding the same numbers in a
different order can leave a difference of about 1e-16, which is enough to break
the tie. `common.mean_top_k` rounds to six decimal places first. Without that,
one rotation in scenario 3.2 loses its tie and two cells of Figure 4 come out
0.1 away from the published values.
