# Context-Robust Identity Linkage in Social Media via Keystroke Dynamics

Created: 2026-09-20

Code and data for the IEEE ICTAI 2026 paper of the same name. A link to the
published paper will be added here once the proceedings are out.

Identity linkage asks whether observations collected under different
conditions come from the same person, and how much that gets harder when the
conditions change. The paper studies it as a closed-set 1:N identification
problem under controlled variation in platform, topic, and session, comparing
three kinds of identity representation — text, keystroke dynamics, and
score-level fusion of the two — across ten gallery–probe configurations.

The dataset has 61 participants and 1,098 paired text and keystroke
observations, collected through replicas of Facebook, Instagram, and X across
three discussion topics and two sessions. Each participant contributed 18
observations: 3 platforms × 3 topics × 2 sessions.

## Citation

Use the "Cite this repository" button in the sidebar, which reads
[`CITATION.cff`](CITATION.cff), or:

```bibtex
@inproceedings{kuruvilla2026identity,
  title     = {Context-Robust Identity Linkage in Social Media via Keystroke Dynamics},
  author    = {Kuruvilla, Alvin and Pickering, Lori and Rentala, Indrani and Kumar, Rajesh},
  booktitle = {Proceedings of the IEEE International Conference on Tools with Artificial Intelligence (ICTAI)},
  year      = {2026}
}
```

Pages and DOI will be added once the proceedings are published.

## Layout

```
├── web-data-collection-gcs/   # The collection app participants used
├── datasets/clean-data/       # The collected data, keyed by pseudonymous IDs
│   └── dataset/
│       ├── keystroke-timing-csv/   # 1,098 per-response keystroke traces
│       ├── text/                   # 1,098 matching response texts
│       ├── keypairs/               # Extracted key-pair timing features
│       └── top-10-aggregated-IL-features/
├── experiments/               # The eight identity representations, evaluated on 171 rotations
└── analysis/                  # The figures and tables of Section IV
```

`web-data-collection-gcs/` is a self-contained study deployment — a consent
flow, demographics survey, video stimuli, and three social-media clones
instrumented to capture keystroke timings, uploading to a Google Cloud
Function. It has its own README covering setup and deployment. Anyone can run
it for their own study; it ships with deployment placeholders rather than our
infrastructure.

Participant IDs are 128-bit random values from `crypto.getRandomValues`, not
derived from any identifying attribute. Demographics and consent records are
not in this repository.

## Getting started

```bash
pip install -r requirements.txt

# regenerate every figure and table from the recorded results
cd analysis && ./run_all.sh
```

That runs in under a minute and needs nothing but the results tables in
`experiments/results/`. Rerunning the experiments themselves takes longer and
is described in `experiments/README.md`.

## The ten gallery–probe configurations

Some observations are enrolled in the **gallery**, the rest are used as
**probes**, and each probe is matched against the gallery. Each configuration
holds some contextual factors fixed and varies others, and expands into several
platform–topic rotations — 171 in total.

In the variation notation, factors before the dot are held constant between
gallery and probe; factors after it are varied. `P` is platform, `T` is topic,
`S` is session.

| # | Variation | Description | Rotations |
|---|---|---|---|
| **1.1** | `PT·S` | Cross-session, same platform and topic. Gallery session 1, probe session 2 | 9 |
| **1.2** | `PT·S` | Cross-session, same platform and topic. Gallery session 2, probe session 1 | 9 |
| **2.1** | `T·PS` | Cross-platform and cross-session, same topic. Gallery session 1, probe session 2 | 18 |
| **2.2** | `T·PS` | Cross-platform and cross-session, same topic. Gallery session 2, probe session 1 | 18 |
| **3.1** | `TS·P` | Cross-platform, both sessions pooled, single-platform gallery | 18 |
| **3.2** | `TS·P` | Cross-platform, both sessions pooled, two-platform gallery | 9 |
| **4.1** | `S·PT` | Cross-platform and cross-topic, both sessions pooled, single-platform gallery | 36 |
| **4.2** | `S·PT` | Cross-platform and cross-topic, both sessions pooled, two-platform gallery | 18 |
| **5.1** | `P·TS` | Cross-topic and cross-session, same platform. Gallery session 1, probe session 2 | 18 |
| **5.2** | `P·TS` | Cross-topic and cross-session, same platform. Gallery session 2, probe session 1 | 18 |

Pairs of configurations isolate one contextual factor at a time: 1.1 against
1.2 for session, 1.1 against 2.1 for platform, 3.1 against 3.2 for gallery
size, and 1.1 against 5.1 for topic. Details are in
`experiments/gallery-probe-configurations/README.md`.

## The eight identity representations

These are Table III of the paper.

| Code | How a probe is scored against an enrolled identity | Modality |
|---|---|---|
| `C-Emb-Nomic` | cosine similarity between Nomic Embed v2 sentence embeddings | text |
| `CB-POS` | open-class words replaced by part-of-speech tags, then embedded and compared | text |
| `CB-FuncW` | only function words and punctuation kept, then embedded and compared | text |
| `CB-ITAD.25` | 0.25 × keystroke score + 0.75 × text score | text + keystroke |
| `CB-ITAD.5` | 0.50 × keystroke score + 0.50 × text score | text + keystroke |
| `CB-ITAD.75` | 0.75 × keystroke score + 0.25 × text score | text + keystroke |
| `B-ITAD` | ITAD similarity between keystroke timing distributions | keystroke |
| `B-ML-RF` | Random Forest class probability on keystroke features | keystroke |

## Where each part of the paper lives

| Paper | Here |
|---|---|
| Section III-A, the dataset | `datasets/clean-data/README.md` |
| Table II, gallery–probe configurations | `experiments/gallery-probe-configurations/` |
| Table III, identity representations | `experiments/{text-based,keystroke-based,similarity-fusion}/` |
| Section IV-A, Figure 2 | `analysis/a-overall-identity-linkage/` |
| Section IV-B, Figure 3 | `analysis/b-contextual-variations/` |
| Section IV-C, fusion weighting | `analysis/c-multi-modal-fusion/` |
| Section IV-D, Figure 4 and the statistical tests | `analysis/d-statistical-analysis/` |

`analysis/extra-plots/` holds supporting views that were left out of the paper
for space.

## Scope and limitations

The paper's findings hold under the conditions it studied, and the same limits
apply to anything built from this repo:

- **Closed-set identification.** Every probe belongs to one of the 61 enrolled
  people; the task never asks whether a probe belongs to someone unknown.
- **Controlled replicas, not live platforms.** The Facebook, Instagram and X
  interfaces were replicas with a standardised commenting task and minimum
  length, so platform differences are smaller than they would be in the wild.
- **A modest population** of 61 participants, and **short-term collection**:
  the two sessions were repeats of the same protocol, not observations
  separated by months or years, so the session results speak to short-term
  stability only.

Open-set linkage, larger and more varied populations, longer time spans,
mobile and cross-device typing, and fusion weights that adapt to the context
are the directions the paper leaves for future work.

## Status

Every experiment in the paper has a script here, and every figure and table in
Section IV regenerates from the results those scripts write. Some of the
numbers differ from the printed paper: the Random Forest results were
recomputed after a flaw in how missing feature values were filled, the
transformed-text representations now use the embedding model the paper names,
and the keystroke matcher now drops invalid key pairs. `experiments/results/README.md`
says which tables changed and by how much; the tables behind the printed
figures are kept in `experiments/results/as-published/`.

## Licensing

The code is MIT — see [`LICENSE`](LICENSE), and [`NOTICE.md`](NOTICE.md) for
what it does not cover.

Four things here are not ours and are **not** MIT-licensed. Each carries its
own `NOTICE.md` or `LICENSE` stating where it came from and what we claim,
which is nothing beyond our own modifications:

- `web-data-collection-gcs/pages/fake_pages/Facebook-Clone/` — third party;
  the upstream repository has since been blocked by GitHub over a trademark
  claim, and its license was never published.
- `web-data-collection-gcs/pages/fake_pages/twitter-clone/` — third party;
  neither it nor its own upstream publishes a license.
- `web-data-collection-gcs/pages/fake_pages/instagram-clone/` — third party,
  MIT, ships its upstream LICENSE.
- `web-data-collection-gcs/pages/hosting/videos/` — three copyrighted clips
  included as short low-resolution excerpts under fair use for non-commercial
  research. We hold no rights in them and grant none.

If you deploy this study yourself, you need your own IRB or ethics-board
approval; ours does not extend to you. The consent form in the app is a
template to be completed with your own details.

`datasets/clean-data/` is human-subjects research data, released under
**CC BY 4.0**: use it for anything, and credit it by citing the paper. Its
[`LICENSE`](datasets/clean-data/LICENSE) has the terms and a request not to
attempt re-identification.

**If you are a rights holder** and object to anything included here, open an
issue and we will remove it.
