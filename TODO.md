# TODO — identity-linkage-ICTAI-2026

> Created: 2026-09-07
> Updated: 2026-09-07

Cleanup items for this repository. The `web-data-collection-gcs/` subdirectory was
imported as a content-only snapshot (no prior commit history) from the
`anonymous-deployment` branch of the original working repo.

**Context change:** that branch was scrubbed for **blind peer review**. The paper has
now been reviewed, so anonymity is no longer required. Most items below are about
*undoing* that anonymization and turning the code into a citable artifact release —
the opposite direction from the original cleanup.

---

## Priority 1 — De-anonymization

The blind-review scrub replaced real identifiers with placeholders. Decide for each
whether to restore the real value or keep the placeholder.

**Rule of thumb:** restore *attribution* (who made this, how to cite it); keep
*deployment* placeholders (`YOUR_GCP_PROJECT_ID`, `YOUR_GCS_BUCKET`,
`YOUR_CLOUD_FUNCTION_URL`, `YOUR_GITHUB_PAGES_URL`) so others can still run it with
their own infrastructure. Never restore our real GCP project ID or bucket name.

- [ ] **Restore author/maintainer identity**
  - `web-data-collection-gcs/package.json` — `"author": ""` is empty; `homepage`,
    `bugs.url`, and `repository.url` all point at `YOUR_GITHUB_ORG/YOUR_REPO`.
    These are repo identity, not deployment config → set to the real
    `FakeProfileDetection/identity-linkage-ICTAI-2026`.
  - `web-data-collection-gcs/wasm-keystroke-capture/Cargo.toml` — `authors = ["Your Name"]`
  - `web-data-collection-gcs/wasm-keystroke-capture/pkg/package.json` —
    `collaborators: ["Your Name"]`. This is **generated** by wasm-pack from
    `Cargo.toml`, so fix `Cargo.toml` first, then run `npm run build:wasm` and commit
    the regenerated output. Do not hand-edit it.
- [ ] **Researcher contact email** — the blind-review address
  `fpd.research.2026@gmail.com` was replaced by a `RESEARCHER_EMAIL` config variable
  (`config.env`). Confirm nothing still hardcodes the anonymous address, and decide
  the real contact address for the published artifact.
- [ ] **Informed consent document** — `pages/hosting/Informed Consent.md` / `.pdf` is
  currently a generic template with every identifying field replaced by the literal
  string `"Your Information"` (study title, researcher, affiliation, IRB contact).
  Decide: publish the *real* IRB-approved consent form now that review is over, or
  keep the template and document that adopters must supply their own. If publishing
  the real one, regenerate the PDF from the `.md`.
- [ ] **Study identity defaults** — `STUDY_NAME`, `STUDY_DESCRIPTION`,
  `INSTITUTION_NAME` in `config.env` are blank. Consider shipping the real values used
  in the paper's data collection as documented defaults, so the artifact matches what
  the paper describes.

---

## Priority 2 — Artifact release readiness

- [ ] **Add a LICENSE file.** There is none. `package.json` says `"license": "ISC"`
  but `README.md` says "provided for academic research purposes" — these contradict
  each other. Pick one and make both agree.
- [ ] **Credit the Twitter clone.** `README.md` Credits lists the Facebook and
  Instagram clones but omits `pages/fake_pages/twitter-clone/`, which has no upstream
  attribution or license file anywhere in the repo. Find its origin and credit it, or
  confirm it was written in-house. The Instagram clone ships an MIT LICENSE
  (Leonardo Costa, 2020); check the Facebook clone's terms too.
- [ ] **Add citation metadata** — `CITATION.cff` and/or a BibTeX block in the README
  pointing at the ICTAI 2026 paper, so the artifact is citable.
- [ ] **Repo-root README.** Currently empty (0 bytes). Should describe the paper, the
  repo layout, and how `web-data-collection-gcs/` relates to the analysis code and
  dataset.
- [ ] **Link to the dataset.** The `fpd-dataset` sibling repo holds the collected data;
  cross-reference it once its public location is settled.

---

## Priority 3 — Dev leftovers

Decide keep-and-document vs. remove for each. None are linked from the participant
flow, so removing them is safe.

- [ ] `pages/hosting/debug-userid.html` and `debug-userid2.html` — debug pages, not
  referenced by any other page. Two near-identical copies.
- [ ] `cloud-functions/saver/test.txt` — contains only `Hello from GCS test`.
- [ ] `cloud-functions/saver/test-upload.html` — manual upload tester. Useful for
  setup verification; if kept, mention it in the README's "Verify Your Setup" step.
- [ ] `km_headless_testbed/` — standalone "GCS Upload Test" harness. Not part of the
  study flow. Keep as a developer tool (documented) or drop it.
- [ ] `pages/hosting/mturk-Design-Layout.html` — MTurk-specific; still carries a
  `YOUR_VALIDATION_API_URL` placeholder with a TODO comment. Keep only if MTurk
  recruitment is part of the published method.

---

## Priority 4 — Verification before publishing

- [ ] **Re-scan for leaked infrastructure and PII.** Checked clean on 2026-09-07 —
  re-run before publishing and after any edit that restores real values.
  ```bash
  # Matches only the real scrubbed values, so any hit is a genuine leak.
  # (:!TODO.md excludes this file, which names them on purpose.)
  git grep -n -I -E \
    "fake-profile-detection-460117|fake-profile-detection-eda-bucket|web-data-collection-sa@|irentala|myharrisburgu" \
    -- . ':!TODO.md'
  ```
  A broader sweep for `iam.gserviceaccount.com` / `cloudfunctions.net` returns only
  `YOUR_*` placeholders and `my-research-project-123456` doc examples — expected, not
  leaks.
- [ ] **Re-scan for participant data.** Confirm no collected keystroke files, real
  participant/user IDs, or survey codes are committed anywhere.
- [ ] **End-to-end test from a clean clone** — run through `config.env` +
  `configure.sh`, deploy, and complete one participant run to confirm the published
  code actually works for a third party.
- [ ] **Video fair-use review.** Three copyrighted clips ship in
  `pages/hosting/videos/` (~12.4 MB) under a fair-use notice in the README. That call
  was made for an anonymous research repo; re-confirm it for a public, attributed one.

---

## Done

- [x] **Import `web-data-collection-gcs/` with no commit history** (2026-09-07) —
  exported via `git archive` from the `anonymous-deployment` branch tip; all 186 file
  modes and blob hashes verified identical to the source tree.
- [x] **Fix the WASM build-output trap** (2026-09-07) — wasm-pack generates a
  `pkg/.gitignore` containing `*`, which silently hid the committed WASM module from
  git (it took a `git add -f` to import). Removed that file, added
  `scripts/build-wasm.sh` (which deletes it after every rebuild), wired up
  `npm run build:wasm`, and documented why `pkg/` is committed in both the root
  `.gitignore` and the README.
