"""Turn the 1,098 text samples into embedding vectors, one CSV per representation.

Created: 2026-09-20

Reads every text file under datasets/clean-data/dataset/text, optionally
rewrites it (see transforms.py), sends it to an embedding backend (see
backends.py), and writes one row per sample:

    user_id, platform_id, video_id, session_id, emb_0 ... emb_767

That CSV is the only thing the scoring script reads, so this step can be
swapped for any other embedding method that writes the same columns.

    python embed.py                              # raw text     -> embeddings/text_embeddings_nomic_v2.csv
    python embed.py --transform pos-tags         # CB-POS       -> embeddings/text_embeddings_pos_tags.csv
    python embed.py --transform function-words   # CB-FuncW     -> embeddings/text_embeddings_function_words.csv
    python embed.py --backend sentence-transformers   # without LM Studio

The embeddings used for the paper are already in embeddings/; running this
overwrites them. They were made with LM Studio on another machine, and running
it again here reproduces them to a cosine similarity of about 0.9996 rather
than exactly, because the quantized model file is not the same build.
"""

import argparse
import datetime
import json
from pathlib import Path

import numpy as np
import pandas as pd

from backends import BACKENDS
from transforms import TRANSFORMS

HERE = Path(__file__).parent
TEXT = HERE.parent.parent / "datasets" / "clean-data" / "dataset" / "text"
OUTPUT_NAMES = {"raw": "nomic_v2", "pos-tags": "pos_tags", "function-words": "function_words"}


def load_texts():
    """Every sample's text, with its ids, in a fixed order. File names are platform_video_session_user.txt."""
    rows = []
    for path in sorted(TEXT.glob("*/*.txt")):
        platform, video, session, user = path.stem.split("_", 3)
        rows.append({"user_id": user, "platform_id": int(platform), "video_id": int(video),
                     "session_id": int(session), "text": path.read_text(encoding="utf-8").strip()})
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transform", choices=list(TRANSFORMS), default="raw")
    parser.add_argument("--backend", choices=list(BACKENDS), default="lm-studio")
    parser.add_argument("--model", default=None, help="model name for the backend; each has a default")
    parser.add_argument("--url", default="http://localhost:1234", help="LM Studio server")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    samples = load_texts()
    print(f"{len(samples)} texts from {samples['user_id'].nunique()} people")

    texts = [TRANSFORMS[args.transform](t) for t in samples["text"]]
    empty = sum(1 for t in texts if not t.strip())
    if empty:
        print(f"  {empty} texts are empty after the {args.transform} rewrite; they get a zero vector")
    if args.transform != "raw":
        print(f"  example: {texts[0][:120]!r}")

    embed = BACKENDS[args.backend]
    kwargs = {"url": args.url} if args.backend == "lm-studio" else {}
    if args.model:
        kwargs["model"] = args.model
    filled = [t if t.strip() else " " for t in texts]
    vectors = embed(filled, **kwargs)
    vectors[[not t.strip() for t in texts]] = 0.0
    print(f"  {vectors.shape[0]} vectors of {vectors.shape[1]} dimensions")

    name = OUTPUT_NAMES[args.transform]
    out = Path(args.output) if args.output else HERE / "embeddings" / f"text_embeddings_{name}.csv"
    out.parent.mkdir(exist_ok=True)
    table = pd.concat([samples.drop(columns="text").reset_index(drop=True),
                       pd.DataFrame(vectors, columns=[f"emb_{i}" for i in range(vectors.shape[1])])], axis=1)
    table.to_csv(out, index=False)
    out.with_suffix(".json").write_text(json.dumps({
        "transform": args.transform, "backend": args.backend,
        "model": args.model or embed.__defaults__[0], "dimensions": int(vectors.shape[1]),
        "unit_length": True, "samples": int(len(table)),
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
    }, indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
