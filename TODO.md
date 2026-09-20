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

- [x] **Add a LICENSE file** (2026-09-20) — MIT at the repo root, copyright the four
  paper authors. `package.json` moved ISC → MIT and `CITATION.cff` carries it. The
  LICENSE holds the unmodified MIT text so GitHub's license detection works; the
  carve-outs live in `web-data-collection-gcs/README.md` instead.
- [ ] **License the dataset.** `datasets/clean-data` (79 MB, 2228 files) is
  participant data and sits under the root LICENSE without being covered by it — the
  README says so, but nothing states what *does* cover it. Human-subjects data
  normally carries its own terms (CC-BY-4.0, CC0, or a data-use statement). The
  consent form promises anonymized publication, which permits release but does not
  choose an instrument. Decide, and add it next to the data.
- [x] **Facebook clone upstream is gone** (2026-09-20) — `KashanAdnan/Facebook-Clone`
  returns `Repository access blocked — reason: trademark` (2025-06-20). It was live
  when we took the copy and there is nothing to re-check now. Credits keeps the link
  as a record of origin, noting the block.
- [ ] **Twitter clone license.** Shipping it credited under a no-license caveat;
  asked the author at
  [somanath-goudar/html-css-projects#20](https://github.com/somanath-goudar/html-css-projects/issues/20)
  (2026-09-20, repo dormant since 2024, don't wait on it). If he grants one: add to
  Credits, drop the caveat paragraph from `web-data-collection-gcs/README.md`.
  Fallback if he never replies: rewrite the ~190 lines of markup ourselves.
- [x] **Add citation metadata** (2026-09-20) — `CITATION.cff` at the repo root,
  validated against CFF 1.2.0 with `cffconvert`. Author entries carry the paper's
  addresses; `contact` is Alvin's personal one, since the address on the paper is a
  student account.
  - [ ] Three fields left out rather than invented: `doi` (none assigned yet),
    `license` (blocked on the LICENSE decision above), and the conference edition
    number, location, and dates. Fill them in when known.
  - [ ] Add a BibTeX block to the repo-root README when that gets written —
    `uvx cffconvert -f bibtex -i CITATION.cff` generates it, but needs a real cite key
    and the conference fields above.
- [ ] **Repo-root README.** Empty. Should cover the paper, the repo layout, how
  `web-data-collection-gcs/` relates to the analysis code and dataset, and the
  `STUDY_NAME`/`INSTITUTION_NAME` values our own collection ran under.
- [ ] **Link to the dataset.** `fpd-dataset` sibling repo, once its public location is
  settled.

---

## Priority 2 — Verification before publishing

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
