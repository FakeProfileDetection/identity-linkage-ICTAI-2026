#!/usr/bin/env bash
# Rebuild the Rust/WASM keystroke capture module.
# Created: 2026-09-07
#
# The build output in wasm-keystroke-capture/pkg/ IS committed to this repo on
# purpose: the study pages are served as static files (GitHub Pages) and load
# pkg/keystroke_capture.js directly in the browser. There is no bundler or CI
# build step, so participants would get a broken page if pkg/ were absent.
#
# wasm-pack writes a pkg/.gitignore containing "*" on every build, which silently
# hides that output from git. This script deletes it after each build. If you run
# wasm-pack by hand instead, delete pkg/.gitignore yourself, then confirm with:
#   git status --short wasm-keystroke-capture/pkg/

set -euo pipefail

CRATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../wasm-keystroke-capture" && pwd)"

if ! command -v wasm-pack >/dev/null 2>&1; then
  echo "Error: wasm-pack not found." >&2
  echo "Install it with: cargo install wasm-pack" >&2
  echo "(Rust toolchain: https://rustup.rs)" >&2
  exit 1
fi

# Rust bakes source paths into panic messages, and in a release build those are the
# build machine's own paths — including the builder's home directory, which then
# ships to every participant's browser. Until 2026-09-20 the committed .wasm carried
# one. `git grep -I` skips binaries, so no text scan of this repo catches it.
#
# Three prefixes carry a real path: the dependency registry, the crate itself, and
# the toolchain's copy of the Rust standard library (reached through panics in std,
# e.g. a Vec growth failure). Remapping all three makes the output independent of
# who builds it.
REMAP_FLAGS=(
  "--remap-path-prefix=${CARGO_HOME:-$HOME/.cargo}/registry=/cargo-registry"
  "--remap-path-prefix=${CRATE_DIR}=/keystroke-capture"
  "--remap-path-prefix=$(rustc --print sysroot)=/rust-toolchain"
)

echo "Building keystroke-capture WASM module (target: web)..."
RUSTFLAGS="${RUSTFLAGS:-} ${REMAP_FLAGS[*]}" \
  wasm-pack build "$CRATE_DIR" --target web --release

# Remove the "*" .gitignore wasm-pack regenerates, so pkg/ stays tracked.
rm -f "$CRATE_DIR/pkg/.gitignore"

# Fail loudly rather than commit another leaked path: any /Users/ or /home/ left in
# the binary means a prefix escaped the remap above and needs a new entry.
if strings "$CRATE_DIR/pkg/keystroke_capture_bg.wasm" | grep -qE "/Users/|/home/"; then
  echo "Error: build-machine paths remain in the .wasm after remapping:" >&2
  strings "$CRATE_DIR/pkg/keystroke_capture_bg.wasm" | grep -oE "(/Users/|/home/)[^ ]*" | sort -u >&2
  exit 1
fi

echo
echo "Build complete. Output in wasm-keystroke-capture/pkg/"
echo "Commit the regenerated files so the hosted pages pick them up:"
echo "  git add wasm-keystroke-capture/pkg && git commit -m 'Rebuild WASM module'"
