# TODO — identity-linkage-ICTAI-2026

> Created: 2026-09-07
> Updated: 2026-09-20

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

- [x] **Restore author/maintainer identity** (2026-09-20)
  - [x] `web-data-collection-gcs/package.json` — `homepage`, `bugs.url`, and
    `repository.url` now point at `FakeProfileDetection/identity-linkage-ICTAI-2026`
    (2026-09-20). Confirmed these were *not* adopter-facing placeholders: the README
    never mentions them, they have no `config.env` key, and `configure.sh` only
    rewrites `*.js/*.html/*.sh/*.py`, so no setup step ever filled them in. Also added
    `repository.directory`, since the package sits in a subdirectory of the repo.
  - [x] `web-data-collection-gcs/package.json` — `author` set to
    `Alvin Kuruvilla <alvineasokuruvilla@gmail.com>` (2026-09-20). Code maintainer, not
    paper authorship; the full author list belongs in `CITATION.cff` and the README.
  - [x] `web-data-collection-gcs/wasm-keystroke-capture/Cargo.toml` —
    `authors = ["Lori Pickering"]` (2026-09-20), who wrote the Rust. Name only; her
    commit email is in the git history if we decide the manifest should carry it.
  - [x] `web-data-collection-gcs/wasm-keystroke-capture/pkg/package.json` —
    regenerated via `npm run build:wasm`, `collaborators` now reads `Lori Pickering`
    (2026-09-20). The rebuild also cleared the leaked build path (see Priority 4).
    wasm-bindgen went 0.2.100 → 0.2.128 in the process and rewrote the JS glue
    wholesale, so the regenerated output was checked rather than assumed: both init
    paths and all eight public methods, with the pre-rebuild build run through the
    same checks for comparison. Identical results. `lib.rs` and the pages are
    untouched.
- [x] **Researcher contact email** (2026-09-20) — nothing to restore. The scan is
  clean: `git grep fpd.research.2026` matches nothing outside this file.
  `RESEARCHER_EMAIL` stays blank in `config.env`, which is the adopter's fill-in
  file — every key in it is blank by design, and `README.md:102` already documents
  the key with an example value. The address participants see must be the adopter's,
  since they are running their own study under their own approval.

  The contact address for the *artifact* is a separate question, tracked under
  Priority 2 with `CITATION.cff`.
- [x] **Informed consent document** (2026-09-20) — stays a template. Decided against
  publishing the real IRB-approved form: an adopter running this is doing their own
  research under their own approval, and a form that looks reusable invites someone to
  reuse an approval that does not cover them.
  - The four uniform `"Your Information"` placeholders became self-describing
    `[FILL IN: ...]` markers, greppable so an adopter can confirm none remain.
  - Added a template notice at the top stating the form is unusable as-is and that
    the authors' IRB approval does not extend to an adopter's deployment.
  - Added **Section 9, participant rights contact** — the IRB or ethics board, with
    protocol number. This is new, not a restored placeholder: most boards require a
    rights contact distinct from the study contact, and Section 8 conflated them.
    Section 8 was last, so nothing was renumbered.
  - `README.md` rewritten to match, including that `configure.sh` cannot reach this
    file (it only scans `.js/.html/.sh/.py`), so the fields are hand-edited.
  - PDF regenerated with `npx md-to-pdf` — `consent.html:153` links the PDF, not the
    `.md`, so a stale PDF would have shown participants the old text. Verified with
    `pdftotext`: 7 `FILL IN` markers, notice and Section 9 present, signature block
    intact.
- [x] **Study identity defaults** (2026-09-20) — leaving them blank, for the same
  reason as the contact email. `config.env` is the adopter's fill-in file, and
  `README.md:97-99` already documents all three keys with example values. Shipping
  our real values as defaults would brand an adopter's deployment with our study and
  institution the moment they run `configure.sh`.

  What the paper's own collection used belongs in the repo-root README as a record of
  the deployment, not in a file whose contents get executed (Priority 2).

---

## Priority 2 — Artifact release readiness

- [ ] **Add a LICENSE file.** There is none. `package.json` says `"license": "ISC"`
  but `README.md` says "provided for academic research purposes" — these contradict
  each other. Pick one and make both agree.
- [x] **Credit the Twitter clone** (2026-09-20) — traced and credited in `README.md`.
  Source: [`somanath-goudar/html-css-projects`](https://github.com/somanath-goudar/html-css-projects/tree/main/twitter-clone),
  a tutorial series of HTML/CSS clones, itself a static port of the React
  `CleverProgrammers/twitter-clone` (which is where the `post__*` / `widgets__*` class
  names come from). Identified from the `@somanathg` handle left in our sample posts,
  then confirmed by diff: our `index.html` differs only by Prettier reformatting plus
  the `<textarea id="input_value">` swap and button states. `script.js` is ours.

**Licensing of the clones is unresolved and blocks publication:**

- [ ] **Twitter clone has no license.** `somanath-goudar/html-css-projects` carries no
  LICENSE, and neither does the `CleverProgrammers/twitter-clone` it derives from. No
  license means no redistribution right — shipping it in a public artifact is not
  covered by anything. Options: ask Somanath Goudar to license it (he has a public
  GitHub and the tutorial series is promotional, so a permissive grant is plausible),
  replace the page with markup we write, or drop the Twitter platform from the
  published artifact. The last would diverge from the paper's method.
- [ ] **The Facebook clone's upstream has been taken down.**
  `KashanAdnan/Facebook-Clone`, which the Credits section links, now returns
  `Repository access blocked — reason: trademark` (blocked 2025-06-20). The link in
  our README is dead and the terms we inherited are unknowable. `pages/fake_pages/
  Facebook-Clone/README.md` is the only artifact of it we hold. Decide whether
  shipping it is defensible given a trademark takedown of the source.
- [x] Instagram clone is MIT (Leonardo Costa, 2020), LICENSE shipped at
  `pages/fake_pages/instagram-clone/LICENSE`. Now linked from Credits.
- [ ] **Add citation metadata** — `CITATION.cff` and/or a BibTeX block in the README
  pointing at the ICTAI 2026 paper, so the artifact is citable. Decide the contact
  address that goes on it (moved here from Priority 1): this is the address for
  someone citing or reusing the *code*, and is deliberately not the one participants
  see, which belongs to whoever deploys it.
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

  **That scan has a blind spot: `git grep -I` skips binaries.** The committed
  `wasm-keystroke-capture/pkg/keystroke_capture_bg.wasm` embedded the build machine's
  home directory in panic-message paths and served it to every participant. Found and
  fixed 2026-09-20. Re-run this against any committed binary, not just the text scan
  above:
  ```bash
  strings web-data-collection-gcs/wasm-keystroke-capture/pkg/keystroke_capture_bg.wasm \
    | grep -E "/Users/|/home/"
  ```
  `scripts/build-wasm.sh` now passes `--remap-path-prefix` for all three path sources
  and fails the build if any survive, so a future rebuild cannot silently reintroduce
  it. A plain `wasm-pack build` bypasses that and re-leaks whoever ran it.
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
