# Corrections needed in the paper

Created: 2026-09-20
Updated: 2026-09-25

For whoever is editing the manuscript. Each item says what the paper currently
says, what is true, and gives replacement text in the paper's voice. **Text in
a grey box is proposed replacement text**; everything around it is context so
you can reword it yourself. This file is a hand-off note and is not published
with the repo.

Every figure has already been regenerated with the corrected results and is in
the repo under `analysis/`; item 6 says which file is which.

Summary:

| # | Where | What to do |
|---|---|---|
| 1 | Section III-C, equations 1 and 2 | Replace the AUK definition and rename the symbol where it appears. No number changes |
| 2 | Section III-D, Random Forest settings | Replace one paragraph |
| 3 | Section III-D, keystroke features and how missing values were filled | Replace one paragraph and add one sentence in III-C. **The B-ML-RF numbers change** |
| 4 | Figure 4 caption | One clause |
| 5 | Section III-C, the direction of time across configurations | One sentence to add |
| 6 | Figures 2, 3, 4 and Sections IV-A to IV-D, V | Every number and sentence that changes, with proposed wording |
| 7 | Sections IV-A and IV-B, the CB-POS and CB-FuncW numbers | Numbers change; the method text is already right |
| 8 | Section III-D, score-level fusion | One sentence |
| 9 | Section IV-B and the Figure 3 caption | The full text with the changes marked, ready to paste back and shorten |
| 10 | Section IV-A and the Figure 2 caption | The same, for IV-A. Four paragraphs change |
| 11 | Section IV-C | The same, for IV-C. Five numbers change, no wording |
| 12 | Section IV-D and the Figure 4 caption | The same, for IV-D. Three paragraphs change; this is where the headline conclusion moves |

Items 3, 6 and 7 change numbers; the rest is wording.

Checked and needing nothing: the Abstract, Sections I and II, Section III-A
(the dataset counts and inclusion rules were verified against the data in the
repo: 61 participants × 18 observations, every participant above 1,000 key
pairs and 95% valid pairs, every response at least 150 characters), Tables I
and II, and Section V apart from the one clause in item 6.

---

## 1. What AUK means (Section III-C)

### What the paper says

Equations 1 and 2 define AUK as the area under a threshold-dependent Cohen's
kappa curve: every gallery–probe pair is labelled genuine or impostor, kappa is
evaluated at 101 thresholds over [0, 1], and the curve is integrated.

### What was computed

The mean of ACC@K over K = 1…5. No Cohen's kappa was computed anywhere in the
code that produced the results. The two are different kinds of measure: the
kappa curve scores a threshold that accepts or rejects each pair (a
verification measure), while the mean of ACC@K scores how highly the correct
identity is ranked (an identification measure). The paper frames the task as
closed-set 1:N identification throughout, so the measure that was computed is
the one that fits the study.

It also has a standard name. Plotting ACC@K against K gives the cumulative
match characteristic (CMC) curve, and the mean of ACC@K over K = 1…5 is the
normalized area under that curve up to rank 5.

### Decision

The equations are corrected to describe what was computed. Nothing is re-run,
and no number in the paper changes because of this item.

### Replacement text

Replace the two paragraphs from "Before threshold evaluation, the scores
produced by each representation were mapped to [0,1]…" to "…Larger AUK values
indicate stronger agreement across the evaluated similarity thresholds." with:

> To summarize identification performance across ranks, we compute a single
> rank-based measure for each gallery–probe rotation. Reporting ACC@K at one
> value of K describes a single point of the cumulative match characteristic
> (CMC) curve, which plots ACC@K against K. We therefore summarize the curve
> over the evaluated range by its normalized area,
>
> A = (1 / K_max) · Σ_{K=1}^{K_max} ACC@K,   (1)
>
> with K_max = 5. Larger values of A indicate that the correct identity is
> ranked highly more often. Because A aggregates ranks 1 through 5, it is less
> sensitive than ACC@1 to small reorderings among the leading candidates while
> remaining a measure of identification rather than verification performance.

The sentence about min–max normalization goes with it: it described a step
taken "before threshold evaluation", and there is no threshold evaluation. The
normalization the study does use is the one before score-level fusion, which
Section III-D already describes (item 8).

### Where else the symbol appears

AUK means area under the kappa curve, so it should not be kept for a different
quantity. Using A as above:

- Equation 4 becomes `ΔA = A_reference − A_varied`, and the sentence beginning
  "where AUK is the area under the threshold-dependent Cohen's kappa curve
  defined in Eq. 2" becomes "where A is the normalized area under the CMC curve
  defined in Eq. 1".
- Section IV-B: "ΔAUK" → "ΔA" throughout, and "Positive values indicate lower
  threshold-dependent agreement under the varied condition" becomes "Positive
  values indicate lower identification performance under the varied condition".
- Figure 3 caption: "the signed change in the area under the Cohen's kappa
  curve" becomes "the signed change in A". The axis label inside the figure
  changes from "Δ AUK" to "Δ A"; that is a one-line change in the repo and the
  figure can be regenerated on request.
- Section IV-C: "the ΔAUK analysis" → "the ΔA analysis".
- Section IV-D: "the underlying rotation-level AUK measurements" → "the
  underlying rotation-level values of A".

Equation numbering shifts by one, since two equations become one.

---

## 2. Random Forest settings (Section III-D)

### What the paper says

> The Random Forest used 500 trees, unrestricted tree depth, the square-root
> feature-sampling strategy, balanced class weights, and a random seed of 42.
> These settings were held fixed across all gallery–probe configurations and
> platform–topic rotations.

### What is true

The original run did not match that paragraph: three seeds were used and
averaged (42, 123 and 456), class weights were never set, the tree count was
100 or 300 depending on the configuration, and the settings were not the same
across configurations. The Random Forest has since been re-run (item 3) with
one set of settings held fixed throughout, so the paragraph can now describe
the re-run simply; the history of the original run does not need to appear in
the paper.

### Replacement text

> The Random Forest was trained separately for each gallery–probe configuration
> and platform–topic rotation, with one class per enrolled participant. It used
> 500 trees, unrestricted tree depth, the square-root feature-sampling
> strategy, and balanced class weights; because every participant contributes
> the same number of gallery observations, the classes are balanced by
> construction and the weighting has no effect. Each rotation was evaluated
> with three random seeds (42, 123 and 456), and the reported ACC@K values are
> the mean over the three runs. These settings were held fixed across all
> configurations and rotations.

That is close to the original; the only changes are the three seeds and the
remark about class balance.

---

## 3. The keystroke feature set and how missing values were filled (Section III-D)

This is the one correction that changes the paper's numbers.

### What the paper says

> For each gallery–probe configuration, the ten most frequent digraphs were
> selected from the gallery partition. For each digraph, the mean, median,
> standard deviation, first quartile, and third quartile were computed,
> together with aggregate hold-latency statistics. Missing values were imputed
> using feature means estimated from the gallery data.

That describes roughly 55 features: ten digraphs times five statistics, plus a
few aggregate hold-latency values.

### What was actually used

620 features:

| Group | Count | Detail |
|---|---|---|
| Hold latency | 420 | 84 distinct keys × 5 statistics, one set per key, not aggregated |
| Inter-key latency, four types | 200 | 10 digraphs × 5 statistics × 4 interval types |

The four interval types are press-to-press, release-to-release,
release-to-press, and press-of-first to release-of-second. Section III-B
describes only hold latency and one inter-key latency, so the four types need
a mention there too. The ten digraphs were selected once, over the whole
dataset, by how many observations contain them — not per configuration and
not from a gallery partition.

### How missing values were filled, and why that had to change

**What a missing value is.** A response of about 150 characters contains only
some of the 84 keys, so for most keys, in most observations, there is nothing
to measure; the same applies, less often, to the ten digraphs. A Random Forest
cannot take an empty cell, so every empty cell has to be given a number before
training. The rate:

| Feature group | Cells filled | Rate |
|---|---|---|
| Hold latency, per key | 312,330 of 461,160 | 67.7% |
| Digraph intervals | 7,440 of 219,600 | 3.4% |
| Combined | 319,770 of 680,760 | 47.0% |

**How the published results filled them.** Each empty cell was given that
participant's average for that feature, taken over all 18 of their
observations. This was done once, over the whole dataset, before any
observation was assigned to a gallery or a probe.

**Why that is not legitimate.** The rule fills a probe observation using the
identity of the person who produced it. But the identity of a probe is what
the experiment is trying to determine; at the moment a probe arrives, nothing
about who typed it may be used. It also fills gallery observations from
observations that, in the experiment, are on the probe side. The effect is
large: with 47% of cells filled, two observations from the same participant
carry identical values in nearly half their columns, and that shared
fingerprint — not the typing — is most of what the classifier learned. That
is why B-ML-RF scored so much higher than every other representation.

**The rule now used.** For each rotation, and for each feature, take the
average over the gallery observations that contain that key or digraph. Put
that one number into every empty cell of that feature, in gallery and probe
observations alike.

- The number is computed from the enrolled data only, and it is the same for
  every observation it goes into, so it cannot carry identity.
- Gallery and probe are filled from the same source, so the classifier is
  tested on the same kind of input it was trained on.
- A feature whose key appears in no gallery observation at all has no average
  to take; it is set to zero on both sides, which the classifier ignores.

**A wording note.** The old rule is sometimes called "global imputation" in
our notes and diagrams. The word *global* should not appear in the paper: it
is exactly the description of the rule being removed. Say "the mean over the
gallery" or "the gallery average".

**Other rules that were tried, so the choice is defensible.** All on the
paper's feature set, all legitimate, mean ACC@1 over the ten configurations
with each probe observation scored on its own:

| Rule | Mean ACC@1 |
|---|---|
| Gallery average, both sides — **the rule now used** | **0.488** |
| Each observation's own other keys, both sides | 0.471 |
| Participant's own gallery observations for the gallery; gallery average for the probe | 0.419 |
| Published rule (participant's average over all 18 observations) | 0.882 — not legitimate |

Filling the gallery from a participant's own gallery observations is
legitimate on its own, but pairing it with the gallery average for probes
loses, because the two sides then hold different kinds of value in the same
column. Variants of the feature set (fewer keys; features chosen afresh from
each gallery) all land between 0.43 and 0.47. That every legitimate treatment
agrees to within a few hundredths is the strongest reason to trust the
corrected figure, and the paper's own feature set scores best, so it is kept.

### Replacement text for the paragraph

> Keystroke-based representations were computed from per-key hold latencies
> and from digraph interval statistics. For every key observed in the corpus,
> the mean, median, standard deviation, first quartile, and third quartile of
> its hold latency were computed, giving 420 features across 84 keys. The ten
> digraphs with the broadest coverage across the corpus were selected, and for
> each the same five statistics were computed for four interval types —
> press-to-press, release-to-release, release-to-press, and press-of-first to
> release-of-second — giving a further 200 features. Where a participant did
> not produce a given key or digraph in an observation, the corresponding
> features were set to the mean of that feature over the gallery observations
> of the same configuration; the same gallery mean was used for gallery and
> probe observations alike, so that no probe was filled using information
> about its own identity.

### Probes of two sessions: one sentence to add in Section III-C

In configurations 3.x and 4.x each person has two probe sessions. The
published Random Forest scored each session on its own (122 probes), while the
other seven representations pooled a person's two sessions into one probe
(61). The gallery side is pooled for all eight — the forest trains on every
enrolled observation of a person as one class — so the Random Forest now
averages its class probabilities over a person's two probe sessions. All eight
representations then treat a probe the same way, and 3.x/4.x measure the
larger probe that Table II describes, not only the larger gallery. This
raises the Random Forest in those four configurations only (ACC@1 3.1 0.61 →
0.69, 3.2 0.76 → 0.82, 4.1 0.52 → 0.59, 4.2 0.65 → 0.70). Pooling presumes the
two sessions are known to come from one account, so the paper should say so:

> Where a probe comprises two sessions (configurations 3.x and 4.x), they are
> treated as one unknown account: the text and keystroke streams are pooled
> before scoring, and for the Random Forest the class probabilities of the
> two sessions are averaged.

Scored one session at a time, the Random Forest gives ACC@1 0.61–0.76 in 3.x
and 0.52–0.65 in 4.x, which is worth a clause if space allows.

### The corrected B-ML-RF results

Mean over the rotations of each configuration, three seeds, probe sessions
pooled as above. These replace the published B-ML-RF row wherever it appears.

| Scenario | ACC@1 published → corrected | ACC@3 published → corrected | ACC@5 published → corrected |
|---|---|---|---|
| 1.1 | 0.828 → 0.424 | 0.959 → 0.741 | 0.985 → 0.853 |
| 1.2 | 0.841 → 0.422 | 0.951 → 0.715 | 0.975 → 0.834 |
| 2.1 | 0.825 → 0.400 | 0.959 → 0.720 | 0.986 → 0.851 |
| 2.2 | 0.824 → 0.405 | 0.956 → 0.718 | 0.981 → 0.833 |
| 3.1 | 0.968 → 0.686 | 0.995 → 0.945 | 0.999 → 0.991 |
| 3.2 | 0.997 → 0.816 | 1.000 → 0.989 | 1.000 → 0.998 |
| 4.1 | 0.955 → 0.591 | 0.988 → 0.865 | 0.995 → 0.949 |
| 4.2 | 0.987 → 0.699 | 0.998 → 0.953 | 1.000 → 0.995 |
| 5.1 | 0.805 → 0.347 | 0.934 → 0.622 | 0.963 → 0.743 |
| 5.2 | 0.792 → 0.341 | 0.933 → 0.640 | 0.959 → 0.757 |
| **mean** | **0.882 → 0.513** | **0.967 → 0.791** | **0.984 → 0.880** |

What this does to the paper's claims, sentence by sentence, is in item 6.
Only B-ML-RF is affected by this item; the ITAD matcher works from the raw
key pairs and fills nothing.

---

## 4. Figure 4 caption

> Rankings summarize ACC@1, ACC@3 and ACC@5

The ranks are computed from the mean of ACC@K over all five values of K, not
three. Suggested: "Rankings are computed from the mean of ACC@K over K = 1…5".
With item 1, this becomes "Rankings are computed from A". The full caption
with this marked is in section 12.

---

## 5. The direction of time across configurations

Section III describes enrolment and then identification, which reads as
"collect the gallery first, collect the probe later". That is true of only
three of the ten configurations:

- **1.1, 2.1, 5.1** — gallery from session 1, probe from session 2. Enrol,
  then later identify.
- **1.2, 2.2, 5.2** — gallery from session 2, probe from session 1. The probe
  is *earlier* than the enrolment. These exist deliberately, to test whether
  the direction of the session change matters, and Section IV-B reports that
  it does not.
- **3.1, 3.2, 4.1, 4.2** — both sides pool sessions 1 and 2, so the two are
  interleaved in time and are separated by platform, or by platform and
  topic, instead.

None of this is leakage — no observation is on both sides of any rotation, and
that was checked across all 171 — but a reader should not assume a temporal
protocol that only three configurations follow. One sentence in Section III-C,
where the configurations are introduced, would cover it. Suggested:

> Configurations that vary the session evaluate both directions of the session
> change, and those that pool sessions separate gallery and probe by platform
> or topic rather than by time; the experimental protocol therefore does not
> assume that the probe was collected after the gallery.

---

## 6. What changes in Section IV, number by number

Everything below comes from `analysis/run_all.sh` run on the rebuilt
`experiments/results/scenario-results.csv` (20 September 2026), which carries
the corrected Random Forest (item 3, including pooled probes), the Nomic v2
POS and function-word tables (item 7), and the ITAD tables with invalid pairs
and outliers removed. The regenerated figures are in the repo:

| Paper | File |
|---|---|
| Figure 2 (three panels stacked, for the paper) | `analysis/a-overall-identity-linkage/accuracy_heatmaps.pdf` (panels one per file: `accuracy_heatmap_k{1,3,5}.png`) |
| Figure 3 | `analysis/b-contextual-variations/variable_effect_heatmap.png` |
| Figure 4 | `analysis/d-statistical-analysis/rank_heatmap.pdf` (PNG alongside) |
| Friedman / Nemenyi / ranks | `analysis/d-statistical-analysis/*.csv` |

C-Emb-Nomic and the three fusion representations move by at most 0.01 in any
cell; every number quoted for them below still holds unless listed.

One cosmetic change comes with the regenerated Figure 3: its row groups are
labelled *t*, *t+k* and *k*, as in Table III, instead of the printed figure's
C, C+B and B, which the paper never defines. The text never uses those letters,
so nothing else changes.

### Figure 2 and Section IV-A

B-ML-RF row, ACC@1 / ACC@3 / ACC@5, published → now:

| | 1.1 | 1.2 | 2.1 | 2.2 | 3.1 | 3.2 | 4.1 | 4.2 | 5.1 | 5.2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ACC@1 | 0.83→0.42 | 0.84→0.42 | 0.83→0.40 | 0.82→0.40 | 0.97→0.69 | 1.00→0.82 | 0.96→0.59 | 0.99→0.70 | 0.81→0.35 | 0.79→0.34 |
| ACC@3 | 0.96→0.74 | 0.95→0.72 | 0.96→0.72 | 0.96→0.72 | 1.00→0.95 | 1.00→0.99 | 0.99→0.87 | 1.00→0.95 | 0.93→0.62 | 0.93→0.64 |
| ACC@5 | 0.98→0.85 | 0.98→0.83 | 0.99→0.85 | 0.98→0.83 | 1.00→0.99 | 1.00→1.00 | 0.99→0.95 | 1.00→0.99 | 0.96→0.74 | 0.96→0.76 |

CB-POS and CB-FuncW rise by 0.01–0.07 in every cell (ACC@1 cross-topic, 4.x
and 5.x: CB-POS 0.21–0.25 and 0.15, CB-FuncW 0.21–0.25 and 0.16–0.17).

The full text of Section IV-A with every change marked is section 10 below.

### Figure 3 and Section IV-B

ΔAUK, published → now (stars after Bonferroni correction across the 32
comparisons; ns = not significant):

| | Session | Platform | Size | Topic |
|---|---|---|---|---|
| CB-POS | −0.012 → −0.015 | +0.012 → +0.018 | +0.086** → +0.094*** | +0.296*** → +0.308*** |
| CB-FuncW | +0.011 → −0.005 | −0.007 → +0.001 | +0.102** → +0.100*** | +0.264*** → +0.264*** |
| CB-ITAD.5 | −0.020 → −0.016 | | | +0.307*** → +0.303*** |
| CB-ITAD.75 | −0.041 → −0.039 | +0.027 → +0.024 | | +0.206*** → +0.204*** |
| B-ITAD | −0.075 → −0.061 | +0.013 → +0.012 | +0.032 → +0.027 | +0.019 → +0.016 (ns) |
| B-ML-RF | +0.001 → +0.015 | +0.001 → +0.008 | +0.010** → +0.058*** | +0.024 (ns) → **+0.090**** |

C-Emb-Nomic and CB-ITAD.25 are unchanged to three decimals. The Session and
Platform statements ("small and predominantly non-significant") hold. The
Topic paragraph changes in one place: "B-ML-RF remains highly accurate and
B-ITAD experiences comparatively little degradation" → B-ML-RF now shows a
significant but small topic effect (+0.09, against +0.26 to +0.44 for the
text representations), and B-ITAD none. The Size row for B-ML-RF also grows
(3.2 gains more than 3.1 from pooling the probe sessions, because its gallery
is twice as large); the paper does not quote that number.

The full text of Section IV-B and the Figure 3 caption, with every change
marked, is section 9 below.

### Section IV-C

Five numbers change, no wording; the full text with them marked is section
11 below.

### Figure 4 and Section IV-D

The Friedman test still rejects in all ten configurations (p < 10⁻⁹). Average
rank over the ten configurations, 1 = best:

| CB-ITAD.5 | B-ML-RF | CB-ITAD.75 | CB-ITAD.25 | B-ITAD | C-Emb-Nomic | CB-POS | CB-FuncW |
|---|---|---|---|---|---|---|---|
| 2.4 | 2.5 | 2.8 | 3.6 | 5.8 | 5.9 | 6.3 | 6.8 |

B-ML-RF's row of Figure 4 goes from 1.0 in every column to 3.9, 4.3, 3.8, 4.3
(1.x, 2.x), 2.3, 1.4 (3.x), 1.0, 1.0, 1.1, 1.6 (4.x, 5.x). Every other row
moves too, because ranks are relative. The full text with the changes marked
is section 12 below.

### Abstract and Section V

The abstract quotes no numbers and its claims hold as written. In Section V,
"with the Random Forest keystroke-based representation providing the strongest
overall combination of accuracy and robustness" → "with the Random Forest
keystroke-based representation the strongest wherever the discussion topic
changed, and score-level fusion the strongest when it did not".

---

## 7. CB-POS and CB-FuncW: the numbers change; the method text is already right

**Section III-D stays as written.** It says both transformed texts were encoded
with the same Nomic embedding model as C-Emb-Nomic — Nomic Embed v2 — and that
is what the repo does.

What happened: the published CB-POS and CB-FuncW tables had been computed from
embedding files made with an earlier model, Nomic Embed v1.5, by mistake,
while the other text representation and the fusion representations used v2.
The two tables have been recomputed with v2, so the paper's description and
its numbers now agree. The numbers rise a little:

| | published | corrected |
|---|---|---|
| CB-POS, mean ACC@1 over the 171 rotations | 0.295 | 0.317 |
| CB-FuncW, mean ACC@1 | 0.272 | 0.303 |

Every configuration moves up by 0.01–0.06. The qualitative statements in
Section IV-A hold: both remain far below the raw embedding under matched topic
and only slightly above it under topic change. The per-configuration values
that change are in item 6.

---

## 8. How fusion scores were normalised (Section III-D and the Table III caption)

Section III-D says the min–max normalisation parameters were "estimated from
the gallery scores within each experimental configuration and then applied
unchanged to the corresponding probe scores", and the Table III caption
repeats it ("independently min–max normalized using parameters estimated from
the gallery partition"). What the code did is simpler: in
each rotation, the full table of scores between enrolled people and probes was
rescaled to 0–1 by its own minimum and maximum, separately for the keystroke
scores and the text scores, before the two were combined. No parameters were
carried from one set of scores to another. Suggested:

> Within each platform–topic rotation, the keystroke and text score matrices
> were each rescaled to [0, 1] by their own minimum and maximum before being
> combined, so that the fusion weights reflect the relative contribution of the
> two modalities rather than differences in score range.

For the Table III caption: "Before fusion, the text and keystroke scores are
independently min–max normalized within each rotation."

---

## 9. Section IV-B and the Figure 3 caption, full text with the changes marked

The paper's own words, checked sentence by sentence against the current
Figure 3 and Figure 2. Meant to be pasted back and then shortened. Markup:
**bold** is new wording, ~~struck~~ is removed wording, and *[bracketed
italics]* are notes to you, not for the paper. Paragraphs with no markup are
unchanged and still correct.

Two things to know before reading:

- Only two sentences change, both about B-ML-RF under topic change. Its ΔAUK
  is now +0.090 and significant at p < 0.01 (was +0.024, not significant),
  and its ACC@1 falls from 0.42 to 0.35 under topic change (was 0.83 to 0.80).
  Everything else in IV-B holds: session and platform effects are small and
  non-significant, text effects are large and significant, the joint
  configurations behave as described. Numbers for the other cells are in
  item 6.
- **A pre-existing sign issue, not caused by our corrections.** In the Size
  column the reference is the *larger* gallery (3.2) and the varied
  configuration is the smaller one (3.1), so a positive value means the larger
  gallery did better — the opposite of what the caption and the first
  paragraph say positive means. The text never discusses the Size column, so
  nothing in the body is wrong, but the caption should say so. Suggested
  addition is marked in the caption below.

### Figure 3 caption

> Fig. 3: Controlled analysis of contextual effects. Numerical values report
> the signed change in the area under the Cohen's kappa curve, computed as the
> reference configuration minus the corresponding varied configuration.
> Positive values indicate reduced agreement under contextual variation,
> negative values indicate improvement, and values near zero indicate little
> change. **For gallery size the reference is the larger gallery, so a
> positive value indicates that the larger gallery performed better.** Cell
> colors show significance after Bonferroni correction across the 32
> contextual comparisons. Session and platform variation produce comparatively
> small changes, whereas topic variation produces the largest degradation for
> text-based and text-dominant fusion representations.

*[If item 1 is resolved by correcting the AUK definition, "the area under the
Cohen's kappa curve" becomes "the mean top-K accuracy (AUK, Eq. 2)".]*

### B. Effect of Contextual Variation

> Figure 3 summarizes the controlled contextual comparisons using ΔAUK. For
> each comparison, ΔAUK is defined as
>
> ΔAUK = AUK<sub>reference</sub> − AUK<sub>varied</sub>, (4)
>
> where AUK is the area under the threshold-dependent Cohen's kappa curve
> defined in Eq. 2. The reference configuration represents the baseline
> condition, whereas the varied configuration introduces the session,
> platform, gallery-size, or topic change under evaluation. Positive values
> indicate lower threshold-dependent agreement under the varied condition,
> negative values indicate improvement, and values near zero indicate little
> change. Statistical tests were applied to the underlying rotation-level AUK
> measurements rather than to the aggregated ΔAUK values shown in the figure.
> Cell colors indicate the corresponding Bonferroni-corrected significance
> results.

*[Unchanged. Same dependency on item 1 as the caption: "the area under the
threshold-dependent Cohen's kappa curve defined in Eq. 2" and "lower
threshold-dependent agreement" would become "the mean top-K accuracy defined
in Eq. 2" and "lower performance".]*

> *1) Session Variation:* Session variation is evaluated using the two PT·S
> configurations, which reverse the gallery and probe sessions while holding
> platform and topic fixed. Because these configurations differ only in
> session direction, they isolate the effect of repeating the collection
> protocol. Across all representations, ΔAUK values remain close to zero and
> are predominantly non-significant. Figure 2 likewise shows little difference
> between the two PT·S configurations, indicating that neither text-based nor
> keystroke-based representations change systematically across sessions.
>
> This stability is consistent with the experimental design. The repeated
> sessions use the same platform and discussion topic, preserving substantial
> linguistic similarity despite differences in wording, while keystroke-timing
> characteristics remain stable across repeated observations. Consequently,
> session contributes little to the observed degradation within the time span
> represented by this dataset.
>
> This conclusion should be interpreted within the scope of the study. The
> two sessions represent repeated executions of the same controlled protocol
> rather than observations separated by months or years. The results
> therefore support short-term stability but do not establish long-term
> permanence.

*[Unchanged. Session column now: text −0.013 to −0.005, fusion −0.039 to
−0.016 with CB-ITAD.25 at −0.030\*, B-ITAD −0.061, B-ML-RF +0.015; all but
CB-ITAD.25 non-significant, as before.]*

> *2) Platform Variation:* Platform variation is evaluated by comparing the
> PT·S and T·PS configurations, which preserve topic and session direction
> while introducing a platform change between the gallery and probe.
>
> For most representations, ΔAUK values remain small and statistically
> non-significant, and the ACC@K heatmaps show nearly identical performance
> between the two configuration groups. These findings indicate that changing
> the interface alone has little effect when the discussion topic remains
> fixed.
>
> This result reflects the controlled study design. Although real social-media
> platforms differ in audience, editing behavior, message constraints, and
> social conventions, the replicas used here standardized the commenting task
> and minimum response length. Under these conditions, platform variation
> contributes far less to linkage degradation than changes in discussion
> topic. Keystroke-based representations exhibit similar stability,
> suggesting that the interface differences among the three replicas do not
> substantially alter the extracted timing features.

*[Unchanged. Platform column: every cell between +0.001 and +0.024, none
significant. B-ML-RF ACC@1 is 0.42/0.42 in 1.x and 0.40/0.40 in 2.x.]*

> *3) Topic Variation:* Topic variation is isolated by comparing the PT·S and
> P·TS configurations with the same session direction. Both configurations
> include a session change and hold platform constant, making discussion
> topic the only additional factor.
>
> This comparison produces the clearest separation among the representation
> families. Text representations exhibit large ΔAUK values and strong
> statistical significance, whereas the keystroke-based representations show
> substantially smaller changes. The ACC@K heatmaps reveal the same pattern:
> text performance declines sharply under topic variation, while B-ML-RF
> ~~remains highly accurate~~ **degrades only modestly (ΔAUK = 0.090)** and
> B-ITAD ~~experiences comparatively little degradation~~ **shows no
> significant change**.

*[Changed. B-ML-RF's ACC@1 under topic change is now 0.35 (from 0.42 with a
matched topic), so "remains highly accurate" no longer describes it; its
topic effect is +0.090, significant at p < 0.01. B-ITAD's is +0.016, not
significant. Text: +0.265 to +0.442, all p < 0.001.]*

> The raw embedding representation is particularly sensitive because it
> directly encodes semantic content. Under matched-topic conditions, shared
> semantics increase similarity between gallery and probe observations. When
> the topic changes, this information no longer reflects identity and may
> instead increase similarity between different users discussing the same
> subject, substantially reducing identification performance.
>
> The POS and function-word representations partially mitigate this effect by
> suppressing lexical content and emphasizing structural characteristics.
> Their modest improvement over raw embeddings under cross-topic conditions
> suggests that reducing semantic overlap is beneficial, but the remaining
> degradation demonstrates that topic influences more than content words.
> Sentence organization, discourse structure, punctuation, function-word
> usage, and grammatical patterns also vary with topic, and the contextual
> embedding model continues to encode some of these effects. These
> representations should therefore be viewed as topic-reduced rather than
> topic-independent.

*[Unchanged. With the v2 embeddings (item 7) CB-POS and CB-FuncW are at
+0.308 and +0.265 against C-Emb-Nomic's +0.442, so "modest improvement" still
fits.]*

> Keystroke-based representations provide a useful contrast because they rely
> on motor behavior rather than linguistic content. Their comparatively small
> performance changes indicate that keystroke dynamics remain **largely**
> stable across discussion topics. B-ML-RF combines ~~strong discrimination
> with contextual robustness~~ **the strongest cross-topic discrimination with
> a small but significant topic effect**, whereas B-ITAD achieves lower
> absolute accuracy but ~~exhibits similarly limited~~ **shows no significant**
> topic-induced degradation.

*[Changed. The two keystroke representations no longer behave alike: B-ML-RF
has a real, if small, topic effect and B-ITAD has none. "The strongest
cross-topic discrimination" is literally true — B-ML-RF ranks first in every
cross-topic configuration (Figure 4) — and is the claim that survives.]*

> These comparisons identify topic as the dominant contextual factor because
> it changes the linguistic artifact itself, whereas platform and short-term
> session changes primarily alter the conditions under which that artifact is
> produced. Text-based representations therefore encode both identity-related
> characteristics and topic-dependent information.
>
> *4) Joint Contextual Variation:* The preceding analyses isolate the
> individual effects of session, platform, and topic. The remaining
> configurations evaluate more realistic scenarios in which multiple
> contextual factors vary simultaneously or the gallery composition changes.
>
> The T·PS configurations jointly vary platform and session while holding
> topic fixed. Their performance remains similar to that of PT·S, indicating
> that combining two individually weak contextual effects introduces little
> additional degradation.
>
> The TS·P configurations evaluate platform variation after pooling
> observations across both sessions. Because one configuration also increases
> gallery diversity and enrollment evidence, performance differences reflect
> changes in both platform coverage and gallery composition rather than a
> single contextual factor.
>
> The S·PT configurations jointly vary platform and topic while pooling both
> sessions, representing the strongest cross-context condition. Their
> performance closely resembles that of the topic-changing P·TS
> configurations rather than the platform-changing T·PS configurations. Text
> and text-heavy fusion representations degrade substantially, whereas
> keystroke-based representations remain comparatively stable, indicating
> that topic—not platform—is the primary source of degradation.
>
> Comparing S·PT with P·TS further reinforces this conclusion. Although one
> combines topic with platform variation and the other with session
> variation, both exhibit similar performance patterns. Once the discussion
> topic changes, the additional platform or session shift contributes
> relatively little. The impact of joint contextual variation is therefore
> governed primarily by the extent to which a representation depends on
> topic-sensitive information.

*[Unchanged. Checked against Figure 2: B-ML-RF goes from 0.69/0.82 (3.x) to
0.59/0.70 (4.x) while C-Emb-Nomic goes from 0.66/0.75 to 0.13/0.14, so
"comparatively stable" holds; and 4.x resembles 5.x in which representations
lose and which do not, which is what "similar performance patterns" claims.
Note that the Random Forest now pools the two probe sessions in 3.x/4.x (item
3), which is why 3.x and 4.x are well above 1.x and 5.x for it.]*


### Shortened Section IV-B and Figure 3 caption, paste-ready (2026-09-25)

The section above cut to about half its length, with items 1 (ΔAUK → ΔA),
7 and 9 applied and every number checked against
`analysis/b-contextual-variations/contextual_effects.csv`. What is new in
substance, beyond the cuts: the first paragraph says that for gallery size the
smaller gallery is the varied configuration, so the sign rule holds for that
column too; the Size column, which the paper never discussed, gets one
sentence in the last subsection, whose heading gains "and Gallery Size"; the
session paragraph names the one significant cell. The definition and sign
convention that the caption now carries are stated once in the text and not
repeated. Labels and notation follow the source: `fig:heatmap_confounding`,
`fig:model-mean-accuracy`, `eq:auk`, `eq:delta-auk`, `$PT\cdot S$`, `ACC@$K$`.
The same text is in `section-IV-B.tex` at the repo root as plain LaTeX.

```latex
\caption{Controlled analysis of contextual effects. Each cell is
$\Delta A = A_{\mathrm{reference}} - A_{\mathrm{varied}}$ for one
representation and one factor; positive values mean the varied condition
performed worse. For gallery size the reference is the larger gallery, so
positive means the larger gallery did better. Shading gives
Bonferroni-corrected significance over the 32 comparisons, darker for
smaller $p$; rows are grouped by modality as in Table~III.}
```

```latex
\subsection{Effect of Contextual Variation}
\label{ContextVariation}

Figure~\ref{fig:heatmap_confounding} summarizes the controlled contextual comparisons. For each comparison,

\begin{equation}
\Delta A
=
A_{\mathrm{reference}}
-
A_{\mathrm{varied}},
\label{eq:delta-auk}
\end{equation}

where $A$ is the normalized area under the CMC curve defined in Eq.~\ref{eq:auk}. The reference configuration is the baseline and the varied configuration adds the session, platform, or topic change under evaluation; for gallery size, the varied configuration is the smaller gallery. Positive values indicate lower identification performance under the varied condition. Statistical tests were applied to the rotation-level values of $A$ rather than to the aggregated $\Delta A$, with Bonferroni correction across the 32 comparisons.

\subsubsection{Session Variation}

The two $PT\cdot S$ configurations reverse the gallery and probe sessions while holding platform and topic fixed, isolating the effect of repeating the collection protocol. Across all representations, $\Delta A$ remains close to zero and, except for CB-ITAD.25 ($p<0.05$), non-significant; Figure~\ref{fig:model-mean-accuracy} likewise shows little difference between the two configurations. The repeated sessions use the same platform and topic, which preserves linguistic similarity, and keystroke timing is stable across repeated observations. Because the sessions are repeated executions of one protocol rather than observations separated by months or years, this supports short-term stability but does not establish long-term permanence.

\subsubsection{Platform Variation}

Comparing the $PT\cdot S$ and $T\cdot PS$ configurations preserves topic and session direction while adding a platform change between gallery and probe. Every $\Delta A$ is below 0.025 and none is significant, and the ACC@$K$ heatmaps are nearly identical across the two groups, so changing the interface alone has little effect when the topic is fixed. This reflects the study design: the replicas standardized the commenting task and minimum response length, and awareness of data collection may influence typing behavior, so absolute performance may differ in natural settings. The interface differences among the three replicas also do not substantially alter the extracted timing features.

\subsubsection{Topic Variation}

Comparing the $PT\cdot S$ and $P\cdot TS$ configurations with the same session direction holds platform constant and makes topic the only additional factor. This produces the clearest separation among the representation families. Text representations show large, highly significant effects ($\Delta A$ of $0.26$--$0.44$, $p<0.001$), the fusion representations follow them ($0.20$--$0.39$), B-ML-RF degrades only modestly ($\Delta A = 0.090$, $p<0.01$), and B-ITAD shows no significant change.

The raw embedding is the most sensitive because it encodes semantic content: under a matched topic, shared semantics raise gallery--probe similarity, and when the topic changes that information no longer reflects identity and may instead raise similarity between different users discussing the same subject. The POS and function-word representations suppress lexical content and degrade less than the raw embedding, but only modestly, which shows that topic influences more than content words: sentence organization, punctuation, function-word usage, and grammatical patterns also vary with topic, and the contextual embedding model continues to encode some of these effects. These representations are topic-reduced rather than topic-independent.

Keystroke-based representations rely on motor behavior rather than linguistic content. B-ML-RF combines the strongest cross-topic discrimination with a small but significant topic effect, whereas B-ITAD has lower absolute accuracy but no significant topic-induced degradation. Topic is therefore the dominant contextual factor: it changes the linguistic artifact itself, whereas platform and short-term session changes alter only the conditions under which it is produced. Text-based representations encode both identity-related and topic-dependent information.

\subsubsection{Joint Variation and Gallery Size}

The remaining configurations vary several factors at once or change the gallery. The $T\cdot PS$ configurations vary platform and session together with topic fixed and perform much like $PT\cdot S$, so combining two individually weak effects adds little degradation. The $TS\cdot P$ configurations pool both sessions and differ in whether the gallery holds one platform or two; the Size column of Figure~\ref{fig:heatmap_confounding} isolates this comparison, and the larger gallery improves every representation, most clearly the text representations ($\Delta A$ of $0.07$--$0.10$, $p<0.001$) and B-ML-RF ($0.058$, $p<0.001$).

The $S\cdot PT$ configurations vary platform and topic while pooling both sessions, the strongest cross-context condition. Their performance resembles the topic-changing $P\cdot TS$ configurations rather than the platform-changing $T\cdot PS$ configurations: text and text-heavy fusion representations degrade substantially, whereas keystroke-based representations remain comparatively stable. Comparing $S\cdot PT$ with $P\cdot TS$ shows the same pattern although one adds platform and the other session variation to the topic change. Once the topic changes, the additional platform or session shift contributes little; the impact of joint variation is governed by how far a representation depends on topic-sensitive information.
```

---

## 10. Section IV-A and the Figure 2 caption, full text with the changes marked

Same markup as section 9: **bold** is new wording, ~~struck~~ is removed,
*[bracketed italics]* are notes to you. This section carries most of the
changes in the paper, because it is where the Random Forest's numbers are
quoted. In short: B-ML-RF is no longer the best representation everywhere. It
is the best wherever the topic changes (4.x and 5.x) and the fusion
representations are better when the topic matches (1.x and 2.x). Its ACC@1
under a matched topic is 0.40–0.42, not 0.82–0.84.

The Figure 2 caption is unchanged. Figure 4's caption is item 4; its text is
in Section IV-D.

### A. Overall Cross-Context Identity Linkage Performance

> Figure 2 summarizes the mean identification performance of all
> representations across the ten experimental configurations. The three
> heatmaps report ACC@1, ACC@3, and ACC@5. Rows correspond to the
> representations in Table III, columns correspond to the gallery–probe
> configurations in Table II, and each cell reports accuracy averaged across
> the associated platform and topic rotations.

*[Unchanged.]*

> The results distinguish absolute identification accuracy from robustness
> under contextual variation. Among all evaluated approaches, the Random
> Forest keystroke-based representation (B-ML-RF) ~~consistently achieves the
> strongest overall performance across nearly every configuration and rank
> threshold~~ **achieves the strongest performance in every configuration in
> which the topic changes (S·PT and P·TS), whereas under same-topic conditions
> the fusion representations are more accurate at ACC@1**. Under same-topic
> conditions (PT·S and T·PS), **its** ACC@1 ranges from approximately ~~0.82
> to 0.84~~ **0.40 to 0.42**, while under topic variation (P·TS) it ~~remains
> between 0.79 and 0.81~~ **falls to 0.34–0.35**. ~~Likewise,~~ ACC@5
> decreases ~~only slightly~~ from approximately ~~0.98–0.99 to about 0.96~~
> **0.83–0.85 to 0.74–0.76, a smaller loss than for any text
> representation**, indicating that topic variation has ~~little~~ **a
> limited** effect on its ability to rank the correct identity near the top
> of the gallery.

*[Changed. Current B-ML-RF row of Figure 2, ACC@1: 0.42 0.42 0.40 0.40 |
0.69 0.82 | 0.59 0.70 | 0.35 0.34; ACC@5: 0.85 0.83 0.85 0.83 | 0.99 1.00 |
0.95 0.99 | 0.74 0.76. Under a matched topic CB-ITAD.5 leads at ACC@1
(0.50–0.53) and at every rank; under topic change B-ML-RF leads at every
rank. The drop under topic change is 0.07 at ACC@1 against 0.35 for
C-Emb-Nomic, which is what "a smaller loss than for any text representation"
refers to. If you want the pooled-session numbers too: 0.69–0.82 in TS·P and
0.59–0.70 in S·PT at ACC@1.]*

> The distribution-based keystroke representation (B-ITAD) exhibits a
> different tradeoff. Although its ACC@1 is lower than that of several text
> and fusion representations under same-topic conditions, its performance
> changes very little when the topic varies. At ACC@5, performance ranges
> from approximately 0.73–~~0.80~~**0.79** under PT·S and T·PS, and from
> ~~0.72~~**0.71**–0.78 under P·TS. Thus, while B-ITAD is less accurate than
> B-ML-RF, its limited degradation indicates that timing distributions encode
> an identity signal that is comparatively insensitive to semantic context.

*[Two digits, from removing invalid key pairs and outliers in the ITAD run.
"Less accurate than B-ML-RF" still holds at every rank.]*

> The text-based representations exhibit the opposite behavior. The raw
> embedding representation (C-Emb-Nomic) performs best among the text models
> when the gallery and probe share the same topic because semantic overlap
> directly contributes to similarity. This advantage largely disappears under
> topic variation, where ACC@1 falls to approximately 0.09–0.14. The POS
> (CB-POS) and function-word (CB-FuncW) representations perform slightly
> better under cross-topic conditions, reaching approximately ~~0.13–0.22~~
> **0.15–0.25** and ~~0.12–0.21~~ **0.16–0.25**, respectively. Although these
> transformations reduce direct lexical overlap, all three text
> representations remain substantially weaker when the discussion topic
> changes.

*[Numbers only, from item 7. C-Emb-Nomic is unchanged.]*

> The effect is even more apparent at higher ranks. For comparable gallery
> sizes, C-Emb-Nomic decreases by approximately 0.32–0.37 at ACC@1 and by
> 0.40–0.47 at ACC@5 when moving from same-topic to cross-topic conditions.
> This decline indicates that topic variation affects more than the ordering
> of highly ranked candidates; it can move the correct identity well outside
> the top-ranked portion of the gallery. Likewise, replacing lexical content
> with POS tags or function words reduces, but does not eliminate,
> topic-dependent linguistic structure.

*[Unchanged — C-Emb-Nomic did not move. Pre-existing and optional: computed
from Figure 2 (1.x and 2.x against 5.x), the drops are 0.35–0.37 at ACC@1
and 0.44–0.47 at ACC@5, so the ranges could be tightened.]*

> The fusion representations occupy an intermediate position. Under
> same-topic conditions, text-heavy fusion benefits from semantic overlap and
> achieves ~~competitive~~ **the highest** ACC@1. Under topic variation,
> however, representations assigning greater weight to text experience
> substantially larger performance losses, whereas keystroke-dominant fusion
> more consistently retains the correct identity within the top-ranked
> candidates. Fusion therefore inherits the contextual characteristics of its
> dominant modality rather than producing a uniformly context-invariant
> representation.

*[One word. With B-ML-RF at 0.40–0.42 under a matched topic, CB-ITAD.25 and
CB-ITAD.5 at 0.50–0.53 are now the highest ACC@1 there, not merely
competitive. The fusion numbers themselves are unchanged.]*

> Overall, Figure 2 shows that representation choice affects both absolute
> identification accuracy and robustness to contextual variation. Platform
> and session changes produce relatively small differences, whereas topic
> changes create the clearest separation between text-based and
> keystroke-based representations. The following analysis examines these
> effects directly.

*[Unchanged.]*

### Figure 2 caption

> Fig. 2: Mean cross-context identity-linkage accuracy for each
> representation across the experimental configurations. Heatmaps report
> ACC@1 (top), ACC@3 (middle), and ACC@5 (bottom). Rows correspond to the
> representations in Table III, and columns correspond to the controlled
> gallery–probe configurations in Table II. Each cell is averaged across the
> platform and topic rotations represented by that configuration.

*[Unchanged. Drop in the regenerated panels from
`analysis/a-overall-identity-linkage/`.]*

---

## 11. Section IV-C, full text with the changes marked

Same markup as sections 9 and 10. Nothing in the argument changes here: the
fusion representations' numbers moved by at most 0.01, all from removing
invalid key pairs and outliers in the ITAD run, and every statement holds.
Five numbers in two paragraphs are updated; the rest is verbatim.

### C. Effect of Multimodal Fusion

> We evaluate the three score-level fusion configurations introduced in
> Section III-D, which combine the text-embedding similarity S_t and the ITAD
> keystroke similarity S_k according to Eq. 3. We consider α ∈ {0.25, 0.50,
> 0.75}, where α denotes the weight assigned to the keystroke score.
> Accordingly, CB-ITAD.25, CB-ITAD.50, and CB-ITAD.75 use keystroke weights of
> 0.25, 0.50, and 0.75, respectively.

*[Unchanged.]*

> These configurations allow us to examine how modality weighting affects
> robustness when a topic-sensitive text representation is combined with a
> comparatively context-stable keystroke representation. Under same-topic
> conditions, the text-heavy fusion models achieve the highest ACC@1.
> CB-ITAD.25 and CB-ITAD.50 reach approximately 0.50–0.53 across the PT·S and
> T·PS configurations, whereas CB-ITAD.75 ranges from approximately ~~0.35 to
> 0.47~~ **0.34 to 0.46**. In these configurations, semantic similarity
> provides a useful identity signal, allowing stronger text weighting to
> improve first-rank identification despite the lower ACC@1 of ITAD alone.

*[Two digits. "The highest ACC@1" is now true across all eight
representations, not only among the fusion ones, since B-ML-RF is at
0.40–0.42 under a matched topic.]*

> The trend changes at higher ranks and becomes more pronounced under topic
> variation. For the same-topic configurations, CB-ITAD.75 achieves
> approximately 0.90–0.93 at ACC@5, compared with approximately 0.86–0.87 for
> CB-ITAD.25, indicating that keystroke-dominant fusion more consistently
> retains the correct identity within the highest-ranked candidates.

*[Unchanged.]*

> Topic variation amplifies this difference. Although ACC@1 does not change
> monotonically with fusion weight, ACC@5 improves consistently as the
> keystroke contribution increases. Under P·TS, CB-ITAD.25 achieves
> approximately 0.47–0.49, CB-ITAD.50 improves to approximately 0.61–0.62,
> and CB-ITAD.75 further increases to approximately ~~0.74–0.76~~
> **0.73–0.75**. The same trend appears in the ΔAUK analysis, where
> degradation decreases from 0.387 to ~~0.307~~ **0.303** and then to
> ~~0.206~~ **0.204** as the keystroke weight increases. Because the three
> fusion models differ only in their weighting, this ordered reduction
> demonstrates that the context sensitivity of the fused representation is
> primarily inherited from its text component.

*[Three numbers. The ordering 0.387 > 0.303 > 0.204 that the argument rests
on is unchanged. With item 1, "the ΔAUK analysis" becomes "the ΔA
analysis".]*

> These results also explain why multimodal fusion does not uniformly
> outperform every unimodal representation. Fusion is beneficial only when
> both modalities provide reliable evidence under the deployment conditions.
> Under matched-topic conditions, semantic similarity improves identification
> accuracy by complementing the weaker ITAD representation. Under topic
> variation, however, the same semantic signal becomes less reliable and can
> shift the fused score toward topic-similar rather than identity-similar
> candidates.
>
> Nevertheless, the results demonstrate meaningful complementarity between
> the two modalities. Although B-ITAD alone has relatively weak ACC@1, adding
> a modest text contribution improves its ranking under same-topic
> conditions. Conversely, keystroke-dominant fusion often outperforms B-ITAD
> under cross-topic conditions despite the poor performance of the text
> representation alone. A limited amount of textual information therefore
> remains useful when constrained by a more stable keystroke signal.
>
> Overall, the results show that no single fusion weight is optimal across
> all contexts. Text-heavy fusion performs best when gallery and probe share
> the same topic, whereas keystroke-dominant fusion provides greater
> robustness when topics differ. These findings motivate context-aware fusion
> strategies that adapt modality weights according to the expected
> reliability of each identity signal rather than using a fixed weighting
> scheme.

*[Unchanged. Checked: under P·TS, CB-ITAD.75 beats B-ITAD at ACC@1 in both
configurations (0.21/0.26 against 0.09/0.16) and at ACC@5 in one of two,
which is what "often" claims.]*

### Shortened Section IV-C, paste-ready (2026-09-25)

The section above with the five numbers updated, ΔAUK → ΔA (item 1), and
the wording tightened from about 520 to 380 words; every claim is kept.
Labels and notation follow the source. The same text is in
`section-IV-B.tex` at the repo root, after IV-B.

```latex
\subsection{Effect of Multimodal Fusion}
\label{FusionAnalysis}

We evaluate the three score-level fusion configurations introduced in Section~III-D, which combine the text-embedding similarity $S_t$ and the ITAD keystroke similarity $S_k$ according to Eq.~\ref{fusion-score} with keystroke weight $\alpha \in \{0.25,0.50,0.75\}$; CB-ITAD.25, CB-ITAD.50, and CB-ITAD.75 use $\alpha$ of 0.25, 0.50, and 0.75, respectively. They show how modality weighting affects robustness when a topic-sensitive text representation is combined with a comparatively context-stable keystroke representation.

Under same-topic conditions, the text-heavy fusion models achieve the highest ACC@$1$: CB-ITAD.25 and CB-ITAD.50 reach approximately $0.50$--$0.53$ across the $PT\cdot S$ and $T\cdot PS$ configurations, whereas CB-ITAD.75 ranges from approximately $0.34$ to $0.46$. Here semantic similarity is a useful identity signal, so stronger text weighting improves first-rank identification despite the lower ACC@$1$ of ITAD alone. The trend changes at higher ranks: in the same configurations, CB-ITAD.75 reaches approximately $0.90$--$0.93$ at ACC@$5$ against $0.86$--$0.87$ for CB-ITAD.25, so keystroke-dominant fusion more consistently retains the correct identity among the highest-ranked candidates.

Topic variation amplifies this difference. Although ACC@$1$ does not change monotonically with the fusion weight, ACC@$5$ improves consistently as the keystroke contribution increases: under $P\cdot TS$, CB-ITAD.25 achieves approximately $0.47$--$0.49$, CB-ITAD.50 $0.61$--$0.62$, and CB-ITAD.75 $0.73$--$0.75$. The $\Delta A$ analysis shows the same ordering, with the topic effect falling from $0.387$ to $0.303$ and then to $0.204$ as the keystroke weight increases. Because the three models differ only in their weighting, this ordered reduction shows that the context sensitivity of the fused representation is inherited primarily from its text component.

These results explain why fusion does not uniformly outperform every unimodal representation: it helps only when both modalities provide reliable evidence under the deployment conditions. Under a matched topic, semantic similarity complements the weaker ITAD representation; under topic variation, the same signal becomes less reliable and can shift the fused score toward topic-similar rather than identity-similar candidates. The two modalities are nevertheless complementary. Adding a modest text contribution improves the ranking of B-ITAD, which alone has weak ACC@$1$, under same-topic conditions, and keystroke-dominant fusion often outperforms B-ITAD under cross-topic conditions despite the poor performance of the text representation alone. A limited amount of textual information therefore remains useful when constrained by a more stable keystroke signal.

No single fusion weight is optimal across contexts: text-heavy fusion performs best when gallery and probe share a topic, and keystroke-dominant fusion is more robust when topics differ. This motivates context-aware fusion that adapts modality weights to the expected reliability of each identity signal rather than a fixed weighting.
```

---

## 12. Section IV-D and the Figure 4 caption, full text with the changes marked

Same markup as sections 9–11. This is the section where the paper's headline
conclusion lives, so three paragraphs change. The tests themselves do not:
the Friedman test still rejects in all ten configurations, and the
description of the methods is unchanged. What changes is who wins. On the
current numbers CB-ITAD.50 and B-ML-RF share the best average rank (2.4 and
2.5); the fusion representations lead when the topic matches and B-ML-RF
leads whenever it changes. The Nemenyi procedure gives that a clean
statement: it separates the two leaders in the T·PS configurations (fusion
higher) and in the S·PT configurations (B-ML-RF higher), and nowhere else.

### Figure 4 caption

> Fig. 4: Average rank of each identity representation across the
> experimental configurations. Lower values indicate stronger overall
> performance. Rankings ~~summarize ACC@1, ACC@3, and ACC@5~~ **are computed
> from the mean of ACC@K over K = 1…5** and should be interpreted together
> with the contextual analyses in Figures 2 and 3.

*[Item 4. With item 1, "the mean of ACC@K over K = 1…5" becomes "A".]*

### D. Statistical Analysis

> We conducted two complementary statistical analyses. First, the effect of
> each controlled variation was evaluated separately for every identity
> representation using the underlying rotation-level AUK measurements.
>
> Session effects were evaluated using paired comparisons because the
> corresponding AUK measurements could be matched by platform–topic rotation
> across the two session directions. Platform, gallery-size, and topic effects
> were evaluated using independent comparisons because the corresponding
> configurations did not produce directly matched sets of rotation-level
> measurements. Accordingly, the Wilcoxon signed-rank test was used for the
> session comparison, whereas the Mann–Whitney U test was used for the
> platform, gallery-size, and topic comparisons. The Bonferroni correction was
> applied jointly across the 32 contextual comparisons shown in Fig. 3,
> corresponding to eight identity representations evaluated under four
> contextual factors. The family-wise significance threshold was therefore
> α_corr = 0.05/32 ≈ 0.00156.
>
> Second, differences among the identity representations were assessed using
> the Friedman test over the repeated experimental conditions. When the
> omnibus test was significant, the Nemenyi post hoc procedure was used to
> compare the average ranks of the representations at α = 0.05.

*[Unchanged; this is what the code does. With item 1, "AUK measurements"
becomes "values of A".]*

> *1) Statistical Evidence for Contextual Effects:* The significance results
> in Fig. 3 support the descriptive patterns reported above. Session and
> platform comparisons yield small ΔAUK values and are predominantly
> non-significant. Topic variation, in contrast, produces significant
> degradation for the text-based representations and for fusion methods with
> greater text weight. The keystroke-based representations exhibit smaller
> changes. These results confirm that sensitivity to topic depends on the
> underlying identity modality rather than reflecting a uniform increase in
> task difficulty.

*[Unchanged. "Smaller changes" still describes the keystroke row: B-ML-RF's
topic effect is now significant (+0.090, p < 0.01) but a third of the
smallest text effect; B-ITAD's is not significant. Pre-existing and
optional: all three fusion representations are significant under topic, not
only those "with greater text weight" — true of the printed figure as well.]*

> *2) Comparison Across Identity Representations:* Figure 4 summarizes the
> average rank of each representation across all experimental configurations,
> where lower values indicate stronger overall performance.
>
> The Friedman test rejects the null hypothesis that all representations
> perform equivalently across the evaluated configurations (p < 0.05),
> indicating that the observed differences are unlikely to result from random
> variation. Pairwise differences are subsequently examined using the Nemenyi
> post hoc procedure at α = 0.05.

*[Unchanged. Friedman p is below 10⁻⁹ in every configuration.]*

> ~~B-ML-RF achieves the strongest overall ranking and is the only
> representation that consistently combines high identification accuracy with
> limited degradation across contextual conditions. Its performance remains
> particularly stable when transitioning from same-topic to cross-topic
> scenarios.~~ **CB-ITAD.50 and B-ML-RF share the strongest overall ranking,
> with average ranks of 2.4 and 2.5, but they earn it in different places: the
> fusion representations lead under same-topic conditions, whereas B-ML-RF
> ranks first in every configuration in which the topic changes. The Nemenyi
> procedure separates the two in the T·PS configurations, where CB-ITAD.50
> ranks higher, and in the S·PT configurations, where B-ML-RF does. B-ML-RF is
> thus the representation whose standing depends least on the discussion
> topic.**

*[Rewritten. Figure 4 rows: CB-ITAD.5 is 1.2–2.9 under a matched topic and
3.4–3.7 under a topic change; B-ML-RF is 3.8–4.3 under a matched topic with
one session per side, 1.4–2.3 with pooled sessions, and 1.0–1.6 under a topic
change. Nemenyi p for the pair: 2.1 0.030, 2.2 0.006, 4.1 < 0.001, 4.2 0.046;
0.07 or above in the other six. The Nemenyi sentence is new and can be cut
if space is short; the rest is the minimum that states the result.]*

> The remaining representations exhibit greater context dependence. Although
> B-ITAD ranks lower under same-topic conditions because of its comparatively
> weak ACC@1, its relative standing improves when the discussion topic
> changes because its performance degrades far less than that of the text
> representations. Conversely, C-Emb-Nomic benefits substantially from
> semantic overlap under matched-topic conditions but drops markedly under
> cross-topic evaluation. This contrast illustrates that high average accuracy
> under favorable conditions does not necessarily imply robustness to
> contextual variation.
>
> The POS and function-word representations generally rank below the
> strongest keystroke-based and fusion approaches. Although suppressing
> lexical content reduces semantic dependence, the resulting representations
> do not recover sufficient author-specific information to compensate for the
> loss of lexical evidence.

*[Unchanged. B-ITAD 7.1–8.0 under a matched topic, 2.4–3.4 under a topic
change; C-Emb-Nomic 4.3–4.8 then 7.7–8.0; CB-POS and CB-FuncW 5.2–7.4
throughout.]*

> The fusion representations ~~occupy an intermediate position, with their
> rankings reflecting~~ **rank according to** the balance between text and
> keystroke contributions. Keystroke-dominant fusion performs more
> consistently under topic variation, whereas text-heavy fusion benefits
> primarily from matched-topic conditions. These rankings therefore reinforce
> the ACC@K and ΔAUK analyses while emphasizing two complementary
> observations: the choice of matching algorithm influences absolute
> identification accuracy, whereas the choice of identity modality largely
> determines robustness to contextual change.

*[Three words. "Intermediate" no longer fits when CB-ITAD.50 has the best
average rank. The rest holds: CB-ITAD.75 is 2.1–2.3 under a topic change and
CB-ITAD.25 is 1.9–3.0 under a matched topic against 5.1–5.4 under a change.]*

> Overall, the ranking analysis identifies B-ML-RF as the strongest method
> ~~across the evaluated conditions~~ **under topic change and score-level
> fusion as the strongest under matched-topic conditions**, and shows that
> the relative performance of the remaining representations depends strongly
> on topic compatibility and fusion weighting.

*[The closing sentence, to match the rewritten paragraph above. Section V's
matching clause is in item 6.]*
