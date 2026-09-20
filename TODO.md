# TODO — identity-linkage-ICTAI-2026

> Created: 2026-09-07
> Updated: 2026-09-20

Turning `web-data-collection-gcs/` into a citable artifact release. It was imported
as a content-only snapshot of the `anonymous-deployment` branch, which had been
scrubbed for blind review; the paper has since been reviewed, so most of this is
undoing that scrub.

De-anonymization (former Priority 1) is done — see Done.

---

## Priority 1 — Artifact release readiness

- [ ] **Add a LICENSE file.** There is none. `package.json` says `"license": "ISC"`,
  `README.md` says "provided for academic research purposes". Pick one, make both
  agree.
- [ ] **Facebook clone upstream is gone.** `KashanAdnan/Facebook-Clone`, linked from
  Credits, returns `Repository access blocked — reason: trademark` (2025-06-20). Dead
  link, and the terms we inherited are unknowable. Decide whether shipping it is
  defensible.
- [ ] **Twitter clone license.** Shipping it credited under a no-license caveat;
  asked the author at
  [somanath-goudar/html-css-projects#20](https://github.com/somanath-goudar/html-css-projects/issues/20)
  (2026-09-20, repo dormant since 2024, don't wait on it). If he grants one: add to
  Credits, drop the caveat paragraph from `web-data-collection-gcs/README.md`.
  Fallback if he never replies: rewrite the ~190 lines of markup ourselves.
- [ ] **Add citation metadata** — `CITATION.cff` and/or a BibTeX block pointing at the
  ICTAI 2026 paper. Needs a contact address for people citing the *code* (not the one
  participants see, which belongs to whoever deploys it).
- [ ] **Repo-root README.** Empty. Should cover the paper, the repo layout, how
  `web-data-collection-gcs/` relates to the analysis code and dataset, and the
  `STUDY_NAME`/`INSTITUTION_NAME` values our own collection ran under.
- [ ] **Link to the dataset.** `fpd-dataset` sibling repo, once its public location is
  settled.

---

## Priority 2 — Dev leftovers

Keep-and-document vs. remove. None are linked from the participant flow.

- [ ] `pages/hosting/debug-userid.html` + `debug-userid2.html` — unreferenced debug
  pages, two near-identical copies.
- [ ] `cloud-functions/saver/test.txt` — contains only `Hello from GCS test`.
- [ ] `cloud-functions/saver/test-upload.html` — manual upload tester. If kept,
  mention it in the README's "Verify Your Setup" step.
- [ ] `km_headless_testbed/` — standalone "GCS Upload Test" harness, not part of the
  study flow.
- [ ] `pages/hosting/mturk-Design-Layout.html` — carries a `YOUR_VALIDATION_API_URL`
  placeholder. Keep only if MTurk recruitment is part of the published method.

---

## Priority 3 — Verification before publishing

- [ ] **Re-scan for leaked infrastructure and PII.** Text scan was clean 2026-09-07;
  re-run before publishing and after any edit restoring real values.
  ```bash
  # Matches only the real scrubbed values, so any hit is a genuine leak.
  git grep -n -I -E \
    "fake-profile-detection-460117|fake-profile-detection-eda-bucket|web-data-collection-sa@|irentala|myharrisburgu" \
    -- . ':!TODO.md'
  ```
  `git grep -I` skips binaries, so scan those separately — the committed `.wasm` was
  leaking a home directory until 2026-09-20:
  ```bash
  strings web-data-collection-gcs/wasm-keystroke-capture/pkg/keystroke_capture_bg.wasm \
    | grep -E "/Users/|/home/"
  ```
- [ ] **Re-scan for participant data.** No keystroke files, real participant IDs, or
  survey codes committed anywhere.
- [ ] **End-to-end test from a clean clone** — `config.env` + `configure.sh`, deploy,
  one full participant run.
- [ ] **Video fair-use review.** Three copyrighted clips in `pages/hosting/videos/`
  (~12.4 MB) ship under a fair-use notice. That call was made for an anonymous repo;
  re-confirm it for a public, attributed one.

---

## Done

- [x] **De-anonymization** (2026-09-20) — author/repo identity restored in
  `package.json` and `Cargo.toml`, `pkg/` regenerated. Contact email and study
  identity defaults stay blank: `config.env` is the adopter's fill-in file.
- [x] **Informed consent stays a template** (2026-09-20) — `[FILL IN: ...]` markers,
  notice that our IRB approval doesn't extend to adopters, new §9 participant-rights
  contact, PDF regenerated.
- [x] **Twitter clone traced and credited** (2026-09-20) — Somanath Goudar's HTML/CSS
  clones series, itself a port of the React `CleverProgrammers/twitter-clone`.
  Instagram clone confirmed MIT, LICENSE linked from Credits.
- [x] **Fix a leaked build path in the committed `.wasm`** (2026-09-20) — it embedded
  the builder's home directory and shipped to every participant. `build-wasm.sh` now
  remaps all three path prefixes and fails the build if any survive.
- [x] **Import `web-data-collection-gcs/` with no commit history** (2026-09-07) —
  `git archive` from the `anonymous-deployment` tip; 186 file modes and blob hashes
  verified identical.
- [x] **Fix the WASM build-output trap** (2026-09-07) — wasm-pack writes a
  `pkg/.gitignore` containing `*`, silently hiding the committed module from git.
  Removed it, added `scripts/build-wasm.sh` to delete it after every rebuild.
