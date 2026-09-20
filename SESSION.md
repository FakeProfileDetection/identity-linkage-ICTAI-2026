# Session notes

Incidental issues found while working, deferred rather than fixed.

## `web-data-collection-gcs/configure.sh`

- `EXCLUDE_FILES` (line 19) names `REPO-CLEANUP-PLAN.md`, which no longer exists —
  it became this repo's root `TODO.md`, outside the directory the script scans.
  Harmless today, but the exclusion no longer protects the file it was written for.
- The script rewrites the working tree in place with no dry-run and no revert path
  other than `git checkout`. Running it twice with different `config.env` values does
  not undo the first run: the second pass looks for placeholder tokens that the first
  pass already replaced, so the earlier values stay baked in.
- `do_replace` only scans `*.js`, `*.html`, `*.sh`, `*.py`. Placeholders in `*.json`,
  `*.toml`, and `*.md` are invisible to it — including `"Your Information"` in
  `pages/hosting/Informed Consent.md`, which the README tells adopters to fill in.

## `wasm-keystroke-capture/Cargo.lock` is gitignored

`web-data-collection-gcs/.gitignore:10` ignores the lock file, but `pkg/` — the build
output — is committed and served to participants. So the one artifact that must be
reproducible is built from unpinned dependencies: the 2026-09-20 rebuild picked up
`once_cell` 1.21.3 → 1.21.4 and `wasm-bindgen` 0.2.100 → 0.2.128 with no source
change. For a citable artifact the lock file should be committed instead.
