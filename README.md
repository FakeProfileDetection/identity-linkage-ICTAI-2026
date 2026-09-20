# Context-Robust Identity Linkage in Social Media via Keystroke Dynamics

Code and data for the ICTAI 2026 paper. Identity linkage asks whether observations
collected under different conditions come from the same person. We study it as a
closed-set 1:N identification problem under controlled variation in platform, topic,
and session, comparing text-based, keystroke-based, and score-level fusion
representations across ten linkage scenarios.

The dataset is 61 participants and 1,098 paired text–keystroke observations, collected
on replicas of Facebook, Instagram, and X across three discussion topics and two
sessions — 18 observations per participant.

To cite this work, see `CITATION.cff`.

## Layout

```
├── web-data-collection-gcs/   # The collection app participants used
├── datasets/clean-data/       # The collected data, keyed by pseudonymous IDs
│   └── dataset/
│       ├── keystroke-timing-csv/   # 1,098 per-response keystroke traces
│       ├── text/                   # 1,098 matching response texts
│       ├── keypairs/               # Extracted key-pair timing features
│       └── top-10-aggregated-IL-features/
├── analysis/
└── experiments/
```

`web-data-collection-gcs/` is a self-contained study deployment — a consent flow,
demographics survey, video stimuli, and three social-media clones instrumented to
capture keystroke timings, uploading to a Google Cloud Function. It has its own README
covering setup and deployment. Anyone can run it for their own study; it ships with
deployment placeholders rather than our infrastructure.

Participant IDs are 128-bit random values from `crypto.getRandomValues`, not derived
from any identifying attribute. Demographics and consent records are not in this
repository.

## Licensing

The code is MIT — see `LICENSE`.

Four things here are not ours and are **not** MIT-licensed. Each carries its own
`NOTICE.md` or `LICENSE` stating where it came from and what we claim, which is
nothing beyond our own modifications:

- `web-data-collection-gcs/pages/fake_pages/Facebook-Clone/` — third party; the
  upstream repository has since been blocked by GitHub over a trademark claim, and its
  license was never published.
- `web-data-collection-gcs/pages/fake_pages/twitter-clone/` — third party; neither it
  nor its own upstream publishes a license.
- `web-data-collection-gcs/pages/fake_pages/instagram-clone/` — third party, MIT,
  ships its upstream LICENSE.
- `web-data-collection-gcs/pages/hosting/videos/` — three copyrighted clips included
  as short low-resolution excerpts under fair use for non-commercial research. We hold
  no rights in them and grant none.

If you deploy this study yourself, you need your own IRB or ethics-board approval;
ours does not extend to you. The consent form in the app is a template to be completed
with your own details.

`datasets/` is human-subjects research data. Its terms are not settled yet — treat it
as all rights reserved until they are.

**If you are a rights holder** and object to anything included here, open an issue and
we will remove it.
