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
- [ ] **End-to-end test from a clean clone** — `config.env` + `configure.sh`, deploy,
  one full participant run.
- [x] **Video fair-use review** (2026-09-20) — keeping all three clips, resting on
  fair use alone. The old framing ("re-confirm now the repo is attributed") was
  wrong: anonymity is not a fair-use factor. The gap was that the justification
  argued for *using* the clips as stimuli and never addressed *redistributing* them
  by shipping the files. It now does.

  Dropped the claim that the Oval Office clip is "Public domain / C-SPAN". C-SPAN
  puts only House and Senate floor proceedings in the public domain; other federal
  government events are theirs, licensed for non-commercial use with attribution,
  where attribution means keeping their on-screen logo. Frames at 30s and 90s show
  no logo and the file is downscaled to 480x270, so the clip's distributing outlet
  cannot be established and the condition was not met. Fair use carries the other
  two clips regardless, and now carries this one too.
- [ ] **Deposit the artifact on Zenodo** for a permanent DOI. A DMCA notice against
  the repo is the realistic risk to the clips, and it would break the URL printed in
  the paper. Also settles the dataset link below.

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
