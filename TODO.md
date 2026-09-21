# TODO — identity-linkage-ICTAI-2026

> Created: 2026-09-07
> Updated: 2026-09-20

The checklist for publishing this repository as the artifact for the ICTAI
2026 paper. The repo stays **private until the paper is released**. Open items
first; what has been settled, with the decision taken, is under **Done** at the
end so nothing is re-decided.

`web-data-collection-gcs/` was imported as a content-only snapshot of the
`anonymous-deployment` branch, which had been scrubbed for blind review; the
paper has since been reviewed, so much of the early work was undoing that
scrub (see Done).

---

## Last of all — before the repo goes public

Only after everything below is closed and the paper is out.

- [ ] Delete `PAPER-FIXES.md`, `TODO.md` and `SESSION.md`. They are internal
  working notes, pushed to the private repo on purpose so the team can use them
  from one place; readers are not meant to see them.
- [ ] Delete `temp-repos/` from the working copy (gitignored, never committed),
  then re-run the scans in Priority 3 with the private repo names added to the
  pattern: `temp-repos|keystroke-scripts|fpd_etl_pipeline|fusion_id|keystroke_stats`.
- [ ] Squash the commit history to one commit and force-push. Then make the repo
  public.

---

## Priority 1 — Get the paper corrections into the manuscript

Every experiment-side decision is taken (Done, "Results correction"). What
remains is on the writer's side.

- [ ] `PAPER-FIXES.md` at the repo root is the hand-off. Items 1–8 are
  one-paragraph edits with replacement text; sections 9–12 are Sections IV-A
  to IV-D with every change marked. The Abstract, Sections I–II, III-A,
  Tables I–II and most of Section V were checked and need nothing.
- [ ] Figures to drop into the manuscript: Figure 2 panels in
  `analysis/a-overall-identity-linkage/`, Figure 3 in
  `analysis/b-contextual-variations/`, Figure 4 in
  `analysis/d-statistical-analysis/`.
- [ ] `datasets/clean-data/README.md` — its imputation section describes only
  the top-ten digrams (3.4% filled, correct) and not the 420 per-key
  hold-latency features the Random Forest used (67.7% filled). Check whether
  this text is shared with the dataset paper before editing.

---

## Priority 2 — Artifact release readiness

- [x] **License the dataset** — decided 2026-09-21 (Lori): **CC BY 4.0**, anyone
  may use it provided they cite the paper. `datasets/clean-data/LICENSE` states
  the terms, the citation, and a (non-binding) request not to re-identify
  participants; root README and `NOTICE.md` updated to match.
- [ ] **Final paper citation.** The BibTeX in the root README, `CITATION.cff` and
  `datasets/clean-data/LICENSE` all cite the paper without DOI or pages, because
  neither exists yet. Fill all three in when the proceedings are published
  (same item as the `CITATION.cff` fields below).
- [ ] **Twitter clone license.** Shipping it credited under a no-license caveat;
  asked the author at
  [somanath-goudar/html-css-projects#20](https://github.com/somanath-goudar/html-css-projects/issues/20)
  (2026-09-20, repo dormant since 2024, don't wait on it). If he grants one: add to
  Credits, drop the caveat paragraph from `web-data-collection-gcs/README.md`.
  Fallback if he never replies: rewrite the ~190 lines of markup ourselves — which is
  the only thing that fully clears it anyway, since he can license only his own
  contribution and his source, `CleverProgrammers/twitter-clone`, is likewise
  unlicensed.
- [ ] **`CITATION.cff` fields left out rather than invented:** `doi` (none
  assigned yet) and the conference edition number, location, and dates. Fill them
  in when known.
- [x] **`STUDY_NAME`/`INSTITUTION_NAME`** — closed 2026-09-21 (Lori): there is
  no institution or named study; the work was done by the four authors as an
  independent group from industry and academia, which is what `CITATION.cff`
  records. The `config.env` placeholders stay blank for adopters.
- [x] **The paper PDF in the repo root** — it was a draft; deleted 2026-09-21
  after a last pass (its scope-and-limitations statement now lives in the root
  README; everything else was already in the READMEs). The root README will
  link to the published paper.

---

## Priority 3 — Verification before publishing

- [x] **Re-scan for leaked infrastructure and PII** — clean 2026-09-20. Re-run before
  publishing and after any edit that restores a real value.
  ```bash
  # Matches only the real scrubbed values, so any hit is a genuine leak.
  git grep -n -I -E \
    "fake-profile-detection-460117|fake-profile-detection-eda-bucket|web-data-collection-sa@|irentala|myharrisburgu" \
    -- . ':!TODO.md'

  # git grep -I skips binaries, so sweep every tracked binary separately. The
  # committed .wasm was leaking a build-machine home directory until 2026-09-20.
  git ls-files -z | xargs -0 file --mime | grep -v "text/" | cut -d: -f1 \
    | xargs -I{} sh -c 'strings "{}" | grep -oE "(/Users/|/home/)[^ ]*" | sed "s|^|{}: |"'
  ```
- [x] **Re-scan for participant data** — clean 2026-09-20. Two separate questions,
  since `datasets/clean-data` is committed on purpose:
  - Nothing stray in `web-data-collection-gcs/`: no loose CSVs, `_raw.txt`,
    `_metadata.json`, consent or demographics files, no 32-hex IDs outside the
    documented `a1b2c3…` sample in `test-upload.html`, no survey codes.
  - The dataset itself holds only keystroke timings, typed text, keypairs, and
    aggregate features — no demographics, consent, or survey records, which stay
    wherever the demographics mapping lives. IDs are
    `crypto.getRandomValues` over 16 bytes (`utils/common.js:7`), not derived from
    email, so they do not link back on their own. The 1098 text files carry no email
    addresses, phone numbers, or self-identifying phrases.
- [ ] **Re-scan for references to the private working repos** before publishing
  (see "Last of all").
- [ ] **End-to-end test from a clean clone** — `config.env` + `configure.sh`, deploy,
  one full participant run.
- [ ] **Deposit the artifact on Zenodo** for a permanent DOI. A DMCA notice against
  the repo is the realistic risk to the clips, and it would break the URL printed in
  the paper.

---

## Priority 4 — Repo cleanup

- [x] `experiments/keystroke-based/features_wide.parquet` (12 MB) dropped
  2026-09-20; `random_forest_intersection.py` now reads `features.parquet`, on
  which its strict-threshold result is the same 0.469 the README quotes.
- [x] `experiments/keystroke-based/random-forest-imputation-strategy.png` — an
  earlier diagram, superseded by `imputation.png`, referenced by nothing.
  Deleted 2026-09-20.
- [x] `.claude/` added to `.gitignore`; `features_all_keys.parquet` removed,
  byte-identical to `features.parquet` (2026-09-20).
- [ ] `SESSION.md` lists deferred issues in `web-data-collection-gcs/configure.sh`
  and the ignored `Cargo.lock`. Fix or consciously leave; it is deleted with the
  other notes at the end either way.

---

## Priority 5 — Fixes for the private working repos

Not part of this repo and not blocking publication. Worth filing as issues on
those repos so they are not lost.

- [ ] `keystroke-scripts`: `ml_utils.perform_grid_search` reports the wrong
  hyperparameters when it cannot cross-validate — it fits with library defaults but
  returns the first value of each grid entry. This is what made the Random Forest
  settings hard to pin down.
- [ ] `fpd_etl_pipeline`: the `extended_features` output for version
  `2025-09-07_00-27-43` is missing from the artifacts directory although the run
  configs point at it. Regenerating it does not reproduce it bit for bit.
- [ ] The `samples per user` columns disagree across the result tables for
  configurations 3.2 and 4.2 (worksheet and templates say 4 on both sides; the
  ITAD fusion tables say 2 on both sides; the right values are 4 enrolled and 2
  probed). Nothing reads these columns, so no result is affected.

---

## Done

### Results correction (2026-09-20)

Found while rebuilding the analysis: the paper and the code disagreed in
several places, and one disagreement was an experiment-design error. All
settled; the paper edits are in `PAPER-FIXES.md`. **Decisions confirmed by
Lori on 2026-09-20** (no committee needed): Nomic v2 for CB-POS/CB-FuncW,
pooled probe sessions for every representation, AUK equations corrected
without a re-run.

- [x] **AUK.** Section III-C defines it as the area under a Cohen's kappa curve;
  the code averaged ACC@k over k = 1..5 (the normalized area under the CMC curve
  to rank 5). Decision: correct equations 1 and 2 and rename the symbol; nothing
  re-run, no number changes. `PAPER-FIXES.md` item 1.
- [x] **Random Forest settings.** The original run used three seeds averaged, no
  class weights, 100 or 300 trees by configuration. The re-run holds one set of
  settings fixed — 500 trees, unrestricted depth, square-root sampling, balanced
  class weights (a no-op with equal classes), seeds 42/123/456 — so the paper's
  paragraph is replaced to describe the re-run. Item 2.
- [x] **Keystroke feature set.** 620 features (84 keys × 5 hold statistics + 10
  digraphs × 4 interval types × 5), not the ~55 the paper describes. Item 3.
- [x] **Imputation leaked the probe identity.** 67.7% of hold-latency cells were
  empty and were filled with the participant's own mean over all 18 observations,
  including for probes. Decision, on principle: keep the paper's feature set and
  fill every empty cell, gallery and probe alike, with the feature's average over
  the rotation's gallery; features absent from the whole gallery set to 0.
  Chosen because it is closest to the paper's design, uses only enrolment data,
  treats both sides the same (asymmetric filling was measured to be harmful) and
  makes the paper's sentence "imputed using feature means estimated from the
  gallery data" literally true. Alternatives measured — the observation's own
  other keys 0.471, only features every gallery sample produced 0.469, looser
  per-gallery thresholds 0.43–0.45, a 20-key set 0.46 — all in the same band, so
  the choice does not rest on score. B-ML-RF mean ACC@1 0.882 → 0.513. Written up
  in `experiments/keystroke-based/README.md` and item 3.
- [x] **The thesis survives; the ranking claim does not.** Under topic change
  B-ML-RF loses ΔAUK +0.090 (p < 0.01) and B-ITAD +0.016 (ns), against +0.26 to
  +0.44 for text; B-ML-RF ranks first in every cross-topic configuration but about
  fourth under a matched topic, and ties CB-ITAD.5 for best average rank (2.5 vs
  2.4). Items 6 and 9–12.
- [x] **Probe sessions pooled for every representation** in 3.x/4.x. ITAD and
  the text representations pool the data (timing lists, mean vectors) before
  scoring; the Random Forest scores each session and averages the class
  probabilities, since pooling its rows would leave one training row per class.
  Both treat the two sessions as one unknown account, and the paper sentence in
  item 3 says exactly that. `random_forest.py --probe pooled` is the default.
- [x] **CB-POS / CB-FuncW recomputed with Nomic v2** (0.295 / 0.272 → 0.317 /
  0.303); the published tables had been made from v1.5 vectors by mistake. Item 7.
- [x] **ITAD** now drops invalid key pairs and outliers, as the paper says it
  did; mean ACC@1 0.113 vs 0.115 published. Fusion tables inherit the change.
- [x] **Fusion normalisation wording** corrected in Section III-D and the Table
  III caption (item 8); **direction of time** sentence added (item 5); **Figure
  4 caption** clause (item 4); **Figure 3 row groups** now `t / t+k / k` as in
  Table III instead of the undefined `C / C+B / B` — the text never uses the
  letters, so the regenerated figure is the only change.
- [x] **Section III-A verified against the data**: 61 participants × 18
  observations = 1,098; every participant above 1,000 key pairs (minimum 3,052)
  and 95% valid pairs (minimum 99.2%); every response at least 150 characters.
- [x] **Every table regenerated** by scripts in `experiments/`; `results/combine.py`
  rebuilds `scenario-results.csv`; `analysis/run_all.sh` regenerates every figure;
  `analysis/reproduce_paper.sh` regenerates the printed paper's figures from
  `results/as-published/` (verified cell for cell: Figure 2 240/240, Figure 3
  32/32, Figure 4 80/80, every range quoted in IV-C).
- [x] **Per-section READMEs** in `analysis/{a,b,c,d}-*/` explain the figures and
  carry the corrected narrative of Sections IV-A to IV-D.

Checked and needs nothing: observations per user for configurations 3.2 and
4.2. The private worksheet records 4 on both sides and the ITAD fusion tables
2 on both sides, but the real values are 4 enrolled and 2 probed and this repo
records them so. The paper states no counts, so a reader sees nothing wrong.

### Artifact release (2026-09-20)

- [x] **LICENSE** — MIT at the repo root, copyright the four paper authors.
  `package.json` moved ISC → MIT and `CITATION.cff` carries it. The scope — what
  MIT does not cover — lives in the root `NOTICE.md`, because putting it in
  `LICENSE` broke GitHub's detection (`NOASSERTION — Other`); it reads `MIT`
  again with `LICENSE` bare. Detection is a similarity match against the plain
  license text, so leave that file alone. Verify with:
  ```bash
  gh api repos/FakeProfileDetection/identity-linkage-ICTAI-2026/license --jq '.license.spdx_id'
  ```
- [x] **Citation metadata** — `CITATION.cff` validated against CFF 1.2.0 with
  `cffconvert`; author entries carry the paper's addresses; `contact` is Alvin's
  personal one, since the address on the paper is a student account. BibTeX block
  in the root README written by hand as `@inproceedings` (`cffconvert -f bibtex`
  emits an unusable `@misc`).
- [x] **Repo-root README** — paper summary, layout, licensing scope, plus the
  configuration and representation tables and where each part of the paper
  lives. Counts cross-checked against the abstract.
- [x] **Facebook clone upstream is gone** — `KashanAdnan/Facebook-Clone` returns
  `Repository access blocked — reason: trademark` (2025-06-20). Credits keeps the
  link as a record of origin, noting the block.
- [x] **Link to the dataset** — obsolete; the data is in this repo under
  `datasets/clean-data`.
- [x] **Video fair-use review** — keeping all three clips, resting on fair use
  alone; the justification now addresses redistributing the files, not only
  using them as stimuli. Dropped the claim that the Oval Office clip is "Public
  domain / C-SPAN": C-SPAN puts only House and Senate floor proceedings in the
  public domain, and the clip carries no logo at 480×270, so the outlet cannot be
  established.
- [x] **De-anonymization** — author/repo identity restored in `package.json` and
  `Cargo.toml`, `pkg/` regenerated. Contact email and study identity defaults
  stay blank: `config.env` is the adopter's fill-in file.
- [x] **Informed consent stays a template** — `[FILL IN: ...]` markers, notice
  that our IRB approval doesn't extend to adopters, new §9 participant-rights
  contact, PDF regenerated.
- [x] **Twitter clone traced and credited** — Somanath Goudar's HTML/CSS clones
  series, itself a port of the React `CleverProgrammers/twitter-clone`. Instagram
  clone confirmed MIT, LICENSE linked from Credits.
- [x] **Fix a leaked build path in the committed `.wasm`** — it embedded the
  builder's home directory and shipped to every participant. `build-wasm.sh` now
  remaps all three path prefixes and fails the build if any survive.

### Earlier

- [x] **Import `web-data-collection-gcs/` with no commit history** (2026-09-07) —
  `git archive` from the `anonymous-deployment` tip; 186 file modes and blob hashes
  verified identical.
- [x] **Fix the WASM build-output trap** (2026-09-07) — wasm-pack writes a
  `pkg/.gitignore` containing `*`, silently hiding the committed module from git.
  Removed it, added `scripts/build-wasm.sh` to delete it after every rebuild.
