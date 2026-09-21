# Text-based representations

Created: 2026-09-20

Identity signals taken from what was written.

| Representation | Input text | Results |
|---|---|---|
| `C-Emb-Nomic` | the response as written | `../results/C-Emb-Nomic.tsv` |
| `CB-POS` | open-class words replaced by part-of-speech tags | `../results/CB-POS.tsv` |
| `CB-FuncW` | only function words and punctuation kept | `../results/CB-FuncW.tsv` |

All three turn each response into a 768-number vector with the Nomic Embed
Text v2 model and compare vectors by cosine similarity. They differ only in
what text is given to the model.

## Running it

```bash
python run.py        # scores the embeddings in embeddings/ -> ../results/, about a minute
```

The embedding files used for the paper are in `embeddings/`, so this is all
that is needed to reproduce the text results. To remake the embeddings from
the text:

```bash
python embed.py                              # response as written  -> embeddings/text_embeddings_nomic_v2.csv
python embed.py --transform pos-tags         # part-of-speech tags  -> embeddings/text_embeddings_pos_tags.csv
python embed.py --transform function-words   # function words only  -> embeddings/text_embeddings_function_words.csv
```

## The three scripts

**`embed.py`** reads the 1,098 text files under `datasets/clean-data/dataset/text`,
rewrites each one if asked (see below), sends the texts to an embedding model,
and writes one row per sample: the four ids, then `emb_0` … `emb_767`. Every
vector is scaled to unit length. A small `.json` beside each CSV records how it
was made.

**`backends.py`** holds the two ways of getting vectors from a model, and is
where to add a third:

- `lm-studio` (default) — what the paper's embeddings were made with. LM Studio
  must be running with the model `text-embedding-nomic-embed-text-v2-moe`
  loaded and its server on port 1234. Vectors made this way agree with the
  shipped files to a cosine similarity of about 0.9996; they are not identical
  because the quantized model file differs between machines.
- `sentence-transformers` — the same model downloaded from Hugging Face and run
  in-process, for anyone without LM Studio.

Each backend is one function: a list of strings in, a numpy array of
unit-length vectors out. Nothing downstream knows which was used.

**`run.py`** reads an embedding CSV and scores every rotation. For each
person, their gallery samples are averaged into one vector, and their probe
samples into another — where the probe side holds two samples per person, the
two count as one larger sample, as for the keystroke representations. Every
probe vector is scored against every gallery vector by cosine similarity, the
enrolled people are ranked, and ACC@k records whether the right one is among
the top k. Nothing is trained and nothing is random. Every gallery–probe score
is also kept in `scores/`, because the fusion experiments combine these with
the keystroke scores.

## The two rewrites

Both live in `transforms.py`, use NLTK's tokenizer and part-of-speech tagger,
and are the method as used for the paper, word lists included.

**Part-of-speech tags.** Nouns, verbs, adjectives, adverbs and foreign words
become their tag in brackets; numbers become `[NUM]`; function words and
punctuation stay. "The cat sat on the mat." becomes "the [NN] [VBD] on the
[NN]."

**Function words only.** Only words on a fixed list of determiners, pronouns,
prepositions, conjunctions, auxiliaries and similar — plus punctuation — are
kept; everything else is dropped. "The cat sat on the mat." becomes "the on
the."

The idea in both is to keep how someone writes while removing most of what
they are writing about.

## Vocabulary

**Sample**: one person's response on one platform, about one topic, in one
session; 1,098 in all. **Rotation**: one of the 171 individual experiments the
ten scenarios expand into, listed in
`../gallery-probe-configurations/scenarios.csv`. **Gallery** and **probe**: the
enrolled samples and the samples to identify; no sample is on both sides.
