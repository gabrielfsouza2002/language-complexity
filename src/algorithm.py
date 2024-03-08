from functools import partial
from math import log10
from operator import ne
from random import Random
from unicodedata import category as cat

from text.tokenizer import tokens
from text.translit import Transliterator


def apply_at_indexes(func, elements, indexes):
    ret = [(func(e) if i in indexes else e) for (i, e) in enumerate(elements)]
    return ret


def replace_at_indexes(sequence, indexes, e):
    return apply_at_indexes(lambda x: e, sequence, indexes)


def map_at_indexes(sequence, indexes, d):
    return apply_at_indexes(lambda x: d[x], sequence, indexes)


def remove_empty(seq):
    return filter(partial(ne, ""), seq)


def remove_random_verses(verses, p: float, rng: Random) -> str:
    n = len(verses)
    indexes = set(rng.sample(range(n), k=int(p * n)))
    return "\n".join(remove_empty(replace_at_indexes(verses, indexes, "")))


def remove_random_words(text, p: float, rng: Random) -> str:
    words = tokens(text)
    n = len(words)
    indexes = set(rng.sample(range(n), k=int(p * n)))
    return " ".join(remove_empty(replace_at_indexes(words, indexes, "")))


def remove_random_chars(text, p: float, rng: Random) -> str:
    notspaces = [i for i, c in enumerate(text) if not cat(c).startswith("Z")]
    n = len(notspaces)
    indexes = set(rng.sample(notspaces, k=int(p * n)))
    return "".join(remove_empty(replace_at_indexes(text, indexes, "")))


def build_word_transliterator(text, rng: Random) -> Transliterator:
    tok = tokens(text)
    rng.shuffle(tok)
    tr = Transliterator.from_list(tok)
    return tr


def replace_word_for_index(text, tr: Transliterator) -> str:
    nzeros = int(log10(len(tr.encode_table)) + 1)

    def word_to_index(word):
        return f"%0{nzeros}d" % tr.encode([word])[0]

    words = tokens(text)
    n = len(words)
    return " ".join(apply_at_indexes(word_to_index, words, range(n)))


def replace_index_for_word(text, tr: Transliterator) -> str:
    def index_to_word(index):
        return tr.decode([int(index)])[0]

    words = tokens(text)
    n = len(words)
    return " ".join(apply_at_indexes(index_to_word, words, range(n)))
