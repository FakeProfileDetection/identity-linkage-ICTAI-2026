"""The two rewrites of the text that reduce its dependence on topic.

Created: 2026-09-20

`pos_tags` replaces open-class words — nouns, verbs, adjectives, adverbs — with
their part-of-speech tag, keeping function words and punctuation:

    "The cat sat on the mat."  ->  "the [NN] [VBD] on the [NN]."

`function_words` keeps only function words and punctuation:

    "The cat sat on the mat."  ->  "the on the."

Both use NLTK's word tokenizer and averaged-perceptron tagger. The word list
and tag sets below are part of the method and are kept exactly as used for the
paper's results.
"""

import string

import nltk
from nltk import pos_tag, word_tokenize

for resource, package in [("tokenizers/punkt", "punkt"),
                          ("tokenizers/punkt_tab", "punkt_tab"),
                          ("taggers/averaged_perceptron_tagger_eng", "averaged_perceptron_tagger_eng")]:
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(package, quiet=True)


# Closed-class words, which carry little about the topic.
FUNCTION_WORDS = {
    # determiners
    'a', 'an', 'the', 'this', 'that', 'these', 'those', 'my', 'your', 'his',
    'her', 'its', 'our', 'their', 'some', 'any', 'no', 'every', 'each', 'all',
    'both', 'half', 'either', 'neither', 'much', 'many', 'more', 'most', 'few',
    'fewer', 'little', 'less', 'other', 'another', 'such', 'what', 'which',
    # pronouns
    'i', 'me', 'we', 'us', 'you', 'he', 'him', 'she', 'her', 'it', 'they',
    'them', 'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves',
    'yourselves', 'themselves', 'who', 'whom', 'whose', 'which', 'that',
    'whoever', 'whomever', 'whatever', 'whichever', 'one', 'ones',
    # prepositions
    'about', 'above', 'across', 'after', 'against', 'along', 'among', 'around',
    'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond',
    'by', 'down', 'during', 'except', 'for', 'from', 'in', 'inside', 'into',
    'like', 'near', 'of', 'off', 'on', 'onto', 'out', 'outside', 'over',
    'past', 'since', 'through', 'throughout', 'to', 'toward', 'towards',
    'under', 'underneath', 'until', 'up', 'upon', 'with', 'within', 'without',
    # conjunctions
    'and', 'but', 'or', 'nor', 'for', 'yet', 'so', 'because', 'although',
    'though', 'while', 'if', 'unless', 'until', 'when', 'whenever', 'where',
    'wherever', 'whether', 'as', 'than', 'once', 'since', 'whereas',
    # auxiliary verbs
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'done',
    'will', 'would', 'shall', 'should', 'can', 'could', 'may', 'might',
    'must', 'ought', 'need', 'dare',
    # particles and other
    'not', "n't", 'to', 'there', 'here',
    'very', 'really', 'quite', 'rather', 'too', 'also', 'just', 'only',
    'even', 'still', 'already', 'always', 'never', 'ever', 'often',
    'sometimes', 'usually', 'perhaps', 'maybe', 'probably', 'certainly',
    'definitely', 'possibly', 'actually', 'basically', 'generally',
    # question words
    'how', 'why', 'when', 'where', 'what', 'which', 'who', 'whom', 'whose',
    # negation
    'no', 'not', 'none', 'nothing', 'nobody', 'nowhere', 'neither', "n't",
    # common contractions without the apostrophe
    "dont", "doesnt", "didnt", "wont", "wouldnt", "cant", "couldnt",
    "shouldnt", "isnt", "arent", "wasnt", "werent", "havent", "hasnt",
    "hadnt", "ive", "youve", "weve", "theyve", "ill", "youll", "hell",
    "shell", "well", "theyll", "im", "youre", "hes", "shes", "its",
    "were", "theyre", "thats", "whats", "whos", "heres", "theres",
}

# Tags whose words are kept as they are.
FUNCTION_TAGS = {'CC', 'DT', 'EX', 'IN', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP',
                 'TO', 'WDT', 'WP', 'WP$', 'WRB', 'UH'}

# Tags whose words are replaced by the tag.
CONTENT_TAGS = {'NN', 'NNS', 'NNP', 'NNPS',
                'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',
                'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'FW'}

PUNCTUATION_TAGS = {'.', ',', ':', ';', '!', '?', '-', '--', '...', '``', "''"}


def pos_tags(text):
    """Open-class words become their tag; function words and punctuation stay."""
    if not text or not text.strip():
        return ""
    try:
        out = []
        for word, tag in pos_tag(word_tokenize(text)):
            lower = word.lower()
            if word in string.punctuation or tag in PUNCTUATION_TAGS:
                out.append(word)
            elif lower in FUNCTION_WORDS or tag in FUNCTION_TAGS:
                out.append(lower)
            elif tag in CONTENT_TAGS:
                out.append(f"[{tag}]")
            elif tag == 'CD':
                out.append("[NUM]")
            else:
                out.append(f"[{tag}]")
        return rejoin(out)
    except Exception:
        return text


def function_words(text):
    """Only function words and punctuation stay; everything else is dropped."""
    if not text or not text.strip():
        return ""
    try:
        out = []
        for word, tag in pos_tag(word_tokenize(text)):
            lower = word.lower()
            if word in string.punctuation or tag in PUNCTUATION_TAGS:
                out.append(word)
            elif lower in FUNCTION_WORDS or tag in FUNCTION_TAGS:
                out.append(lower)
        return rejoin(out)
    except Exception:
        kept = []
        for word in text.split():
            clean = word.lower().strip(string.punctuation)
            if clean in FUNCTION_WORDS or word in string.punctuation:
                kept.append(word.lower())
        return ' '.join(kept)


def rejoin(tokens):
    """Put tokens back into a string, without spaces before closing punctuation."""
    if not tokens:
        return ""
    no_space_before = {'.', ',', ':', ';', '!', '?', ')', ']', '}', "'", '"', "''", '--', '...'}
    no_space_after = {'(', '[', '{', '``', '"'}
    out = []
    for i, token in enumerate(tokens):
        if i == 0 or token in no_space_before or (out and out[-1] in no_space_after):
            out.append(token)
        else:
            out.append(' ' + token)
    return ''.join(out)


TRANSFORMS = {"raw": lambda text: text, "pos-tags": pos_tags, "function-words": function_words}
