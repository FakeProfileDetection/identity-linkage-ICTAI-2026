# Web Data Collection App for Keystroke Dynamics Research

> **Last updated:** 2026-03-29T16:45-04:00

> **Research Use Only.** This repository and its contents — including video
> clips — are provided strictly for non-commercial academic research purposes.
> The video stimuli included in this repository are copyrighted by their
> respective owners and are used here under fair use (17 U.S.C. Section 107) as
> standardized emotional stimuli in IRB-approved behavioral research. **Any use
> of these materials outside of academic research may require separate copyright
> permissions from the rights holders.** See
> [Video Copyright and Licensing](#video-copyright-and-licensing) below.

## Overview

A self-supervised web application for collecting typing dynamics data from
participants in a simulated social media environment. Participants watch short
video clips, then type responses on feature-reduced clones of Facebook,
Instagram, and Twitter. The app captures keystroke events with millisecond
precision, along with the full text of each response.

The study collects 18 samples per participant: 3 videos x 3 platforms x 2
sessions (rounds).

## Repository Structure

```
web-data-collection-gcs/
├── cloud-functions/saver/     # Google Cloud Function for receiving uploads
│   ├── index.js               # Cloud Function source
│   ├── deployment.sh          # Deployment script
│   └── test-upload.html       # Upload testing page
├── pages/
│   ├── hosting/               # Study flow pages
│   │   ├── consent.html       # Informed consent
│   │   ├── demographics.html  # Demographics survey
│   │   ├── instructions.html  # Participant instructions
│   │   ├── tasks.html         # Video + task controller
│   │   ├── survey-code.html   # Completion code page
│   │   ├── complete.html      # Study completion
│   │   ├── mturk-Design-Layout.html  # HIT layout, if recruiting via MTurk
│   │   └── videos/            # Video stimuli (see copyright section)
│   └── fake_pages/            # Social media platform clones
│       ├── Facebook-Clone/
│       ├── instagram-clone/
│       └── twitter-clone/
├── scripts/
│   ├── tasks-controller.js    # Task sequencing and video assignment
│   └── build-wasm.sh          # Rebuilds the WASM module (see below)
├── utils/
│   ├── common.js              # Shared config, cookie management, upload logic
│   └── wasm-keystroke.js      # WASM keystroke capture bindings
├── wasm-keystroke-capture/    # Rust/WASM keystroke capture module
│   ├── src/lib.rs             # Rust source
│   └── pkg/                   # Build output -- COMMITTED on purpose
└── styles/
    └── global.css
```

## Setup Guide

This app requires a Google Cloud Platform project and static file hosting.
The codebase uses placeholder values (prefixed with `YOUR_`) that you must
replace with your own configuration before deploying.

### Prerequisites

- A [Google Cloud Platform](https://cloud.google.com/) account
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed
- A GitHub account (for GitHub Pages hosting, or any static file host)

### Step 1: Create GCP Resources

1. Create a new GCP project in the [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the **Cloud Functions API** and **Cloud Storage API**
3. Create a Cloud Storage bucket for receiving uploaded data
4. Create a service account with **Storage Object Creator** permissions on the bucket

### Step 2: Configure Your Values

All configurable values are defined in a single file: `config.env`.

1. Open `config.env` and fill in your values:

   ```bash
   # --- Google Cloud Platform ---
   GCP_PROJECT_ID=my-research-project-123456
   GCP_SERVICE_ACCOUNT=my-data-sa
   GCS_BUCKET=my-research-data-bucket

   # --- Hosting ---
   GITHUB_PAGES_URL=https://myorg.github.io/my-repo

   # --- Cloud Function (required — fill in AFTER deploying in Step 3) ---
   CLOUD_FUNCTION_URL=https://us-east1-my-research-project-123456.cloudfunctions.net/saver

   # --- Study Details ---
   STUDY_NAME=Typing Dynamics Study
   STUDY_DESCRIPTION=Multimodal Typing Dynamics Research
   INSTITUTION_NAME=University of Example

   # --- Optional ---
   RESEARCHER_EMAIL=yourlab@university.edu
   VALIDATION_API_URL=https://your-validation-api.example.com/validate-code  # only if using MTurk
   ```

2. Run the configuration script:

   ```bash
   bash configure.sh
   ```

   This reads `config.env`, replaces all `YOUR_*` placeholders across the
   codebase with your values, and reports what was changed. Works on both
   macOS and Linux.

### Step 3: Deploy the Cloud Function

```bash
cd cloud-functions/saver
npm install
bash deployment.sh
```

The deployment output will show your Cloud Function URL. Add it to
`config.env`:

```bash
CLOUD_FUNCTION_URL=https://us-east1-my-research-project-123456.cloudfunctions.net/saver
```

Then run the script again to apply it:

```bash
cd ../..
bash configure.sh
```

### Step 4: Host the App

**GitHub Pages (simplest):**
1. Push the repository to a GitHub org or account
2. Enable GitHub Pages in repo settings (deploy from main branch)
3. The study entry point is `pages/hosting/start_study.html`

**Any static host** works — the app is entirely client-side except for the
Cloud Function upload endpoint.

### Step 5: Customize for Your Study

| What | Where | Notes |
|------|-------|-------|
| Informed Consent PDF | `pages/hosting/Informed Consent.pdf` | A template is provided — edit the `.md` source (see below) and regenerate the PDF, or replace with your own IRB-approved consent form |
| Video stimuli | `pages/hosting/videos/` | See [Replacing Videos](#replacing-videos) below |
| MTurk validation endpoint | `config.env` → `VALIDATION_API_URL` | Set up your own endpoint or leave blank if not using MTurk |

### Verify Your Setup

After completing all steps, confirm no placeholders remain:

```bash
grep -rn "YOUR_" --include="*.js" --include="*.html" --include="*.sh" .
```

This should return no results (aside from this README).

Then confirm uploads actually reach your bucket. Open
`cloud-functions/saver/test-upload.html` in a browser and submit a test file — it
posts to your deployed Cloud Function the same way the study pages do, so a success
here means the function, the bucket, and CORS are all configured correctly. Delete
the test object from your bucket afterwards.

## Rebuilding the WASM Keystroke Module

You only need this if you change the Rust source in
`wasm-keystroke-capture/src/lib.rs`. The prebuilt module is committed, so the app
runs as-is after cloning.

The build output in `wasm-keystroke-capture/pkg/` **is committed on purpose**. The
study pages are plain static files with no bundler or CI build step -- the browser
loads `pkg/keystroke_capture.js` directly -- so participants would hit a broken
page if `pkg/` were missing from the repo.

To rebuild:

```bash
# One-time: install the Rust toolchain (https://rustup.rs) and wasm-pack
cargo install wasm-pack

npm run build:wasm          # or: bash scripts/build-wasm.sh
git add wasm-keystroke-capture/pkg
git commit -m "Rebuild WASM module"
```

**Watch out:** `wasm-pack` writes a `pkg/.gitignore` containing `*` on every build,
which silently hides the freshly built module from git -- you would commit nothing
and deploy a stale (or absent) module. `scripts/build-wasm.sh` deletes that file
after each build. If you run `wasm-pack` directly, delete it yourself and verify:

```bash
git status --short wasm-keystroke-capture/pkg/
```

## Study Flow

1. **Consent** — Participant reviews and accepts informed consent
2. **Demographics** — Age, gender, handedness, education, typing habits
3. **Instructions** — Overview of the study tasks
4. **Task Loop (x18)** — For each task: watch a video, then post a comment on a platform clone. Keystroke timing data is captured and uploaded automatically.
5. **Completion** — Survey code displayed for compensation (if using MTurk)

## Video Copyright and Licensing

The video clips in `pages/hosting/videos/` are used as emotional stimuli to
elicit typed responses from participants. They are included in this repository
under fair use for non-commercial academic research.

| Video | Copyright Holder | Source | Notes |
|-------|-----------------|--------|-------|
| Coach Carter — "Our Deepest Fear" (2005) | Paramount Pictures | [Movieclips (YouTube)](https://www.youtube.com/results?search_query=coach+carter+our+deepest+fear+movieclips) | Scripted film clip |
| Will Smith / Chris Rock — 2022 Oscars | Academy of Motion Picture Arts and Sciences / ABC (Disney) | News broadcast footage | Live event recording |
| Trump, Vance & Zelenskyy — Oval Office (2025) | Public domain / C-SPAN | [C-SPAN](https://www.c-span.org/) | U.S. government event; C-SPAN permits non-commercial use with attribution |

**Fair use justification:** These clips are used as standardized emotional
stimuli in IRB-approved academic research on keystroke biometrics. The use is
non-commercial, transformative in purpose (scientific measurement, not
entertainment), and does not substitute for the original works. This practice
is consistent with established behavioral research methodology (see Gilman et
al., *Behavior Research Methods*, 2017).

**If you are a rights holder** and believe this use does not qualify as fair
use, please open an issue on this repository and we will address your concern
promptly.

### Replacing Videos

You may substitute your own video stimuli:

1. Remove the existing files from `pages/hosting/videos/`
2. Place exactly 3 `.mp4` files in `pages/hosting/videos/` (any filenames).
   To pre-set the order, prefix filenames with numbers:
   ```
   pages/hosting/videos/
   ├── 1-inspirational-speech.mp4    # shown first
   ├── 2-political-debate.mp4        # shown second
   └── 3-comedy-clip.mp4             # shown third
   ```
3. Run the update script:
   ```bash
   bash update-videos.sh
   ```
   The script will:
   - List the detected video files (sorted alphabetically, so numbered
     prefixes control the default order)
   - Let you assign each file to video 1, 2, or 3 (this controls the
     presentation order — video 1 is shown first in each round)
   - Prompt for a short display label for each (e.g., "Watch Funny Cat Video")
   - Automatically update `utils/common.js` and `scripts/tasks-controller.js`

**Tip:** Choose videos that elicit distinct emotional responses (e.g.,
inspirational, shocking, political) to maximize variance in typing behavior.

### Informed Consent Form

A template informed consent form is provided at
`pages/hosting/Informed Consent.pdf`. **You need your own IRB or ethics-board
approval before recruiting anyone** — ours does not cover your deployment.

Every field marked `[FILL IN: ...]` must be replaced with your own details:

- **Study Title** — your study's official title, as approved by your IRB
- **Researcher, Affiliation, and Contact Information** — PI names, emails,
  institutional affiliations
- **Compensation** (Section 7) — what participants receive, if anything
- **Study Contact** (Section 8) — who to contact about the study itself
- **Participant Rights Contact** (Section 9) — your IRB or ethics board: name,
  protocol number, phone, and email

`configure.sh` does not touch this file, so these are edited by hand.

**To customize the template:**

1. Edit the markdown source at `pages/hosting/Informed Consent.md`
2. Confirm nothing was missed:
   ```bash
   grep -n "FILL IN" "pages/hosting/Informed Consent.md"
   ```
3. Delete the template notice at the top of the file
4. Regenerate the PDF:
   ```bash
   npx md-to-pdf "pages/hosting/Informed Consent.md"
   ```
5. The generated PDF will replace the existing one in the same directory

Alternatively, replace `Informed Consent.pdf` entirely with your own
IRB-approved consent form. The `consent.html` page links to this file by
name, so keep the filename as-is or update the link in `consent.html`.

## Credits

This project uses modified versions of:

- [Facebook Clone](https://github.com/KashanAdnan/Facebook-Clone) by Kashan Adnan.
  The upstream was live when we took this copy; GitHub has since blocked it over a
  trademark claim (June 2025), so the link no longer resolves.
- [Instagram Clone](https://github.com/leocosta1/instagram-clone) by Leo Costa
  ([MIT](pages/fake_pages/instagram-clone/LICENSE))
- [Twitter Clone](https://github.com/somanath-goudar/html-css-projects/tree/main/twitter-clone)
  by Somanath Goudar, itself a port of the React
  [Clever Programmer Twitter clone](https://github.com/CleverProgrammers/twitter-clone).
  We changed the `<input>` to a `<textarea>` for multi-line posts and wrote
  `script.js`.

Neither the Twitter clone nor the project it derives from publishes a license, so
neither grants redistribution rights. It is included with attribution for
non-commercial academic research. If you reuse this repository, clear that page with
the author or replace the markup first.

## License

This repository is provided for academic research purposes. See
[Video Copyright and Licensing](#video-copyright-and-licensing) for information
about the included video clips.
