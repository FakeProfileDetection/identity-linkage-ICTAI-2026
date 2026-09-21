"""Two ways to turn a list of texts into embedding vectors. Add a third by writing one function.

Created: 2026-09-20

Each backend takes a list of strings and returns one unit-length vector per
string, as a numpy array with one row per text. That is the whole interface;
everything downstream reads only the CSV that `embed.py` writes, so any
embedding method can be substituted here without touching the experiments.

`lm_studio` is what the paper's embeddings were made with: Nomic Embed Text v2
served by LM Studio through its OpenAI-style HTTP endpoint. Start LM Studio,
load the model, and leave its server running on port 1234.

`sentence_transformers` runs the same model in-process from Hugging Face, for
anyone without LM Studio. Vectors from the two differ slightly, because the
model files are quantized differently.
"""

import numpy as np


def lm_studio(texts, model="text-embedding-nomic-embed-text-v2-moe@q8_0",
              url="http://localhost:1234", batch_size=32):
    import requests

    vectors = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        reply = requests.post(f"{url}/v1/embeddings", json={"model": model, "input": batch},
                              timeout=600)
        reply.raise_for_status()
        vectors.extend(item["embedding"] for item in reply.json()["data"])
    return unit_length(np.array(vectors, dtype=np.float32))


def sentence_transformers(texts, model="nomic-ai/nomic-embed-text-v2-moe", url=None, batch_size=32):
    from sentence_transformers import SentenceTransformer

    encoder = SentenceTransformer(model, trust_remote_code=True)
    return unit_length(encoder.encode(list(texts), batch_size=batch_size, convert_to_numpy=True))


def unit_length(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / np.where(norms == 0, 1, norms)


BACKENDS = {"lm-studio": lm_studio, "sentence-transformers": sentence_transformers}
