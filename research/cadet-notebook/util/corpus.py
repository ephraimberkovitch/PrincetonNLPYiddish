import srsly
from spacy.tokens import Doc
from spacy.lang.char_classes import HYPHENS, PUNCT, UNITS, CONCAT_QUOTES

import re
from pathlib import Path
from typing import List, Optional, Set
from collections import Counter, namedtuple
from functools import lru_cache
import importlib

Token = namedtuple("Token", ["text", "lemma_", "pos_", "morph", "is_stop"])


def is_stop(word: str, STOP_WORDS: Set):
    """JavaScript will interpret 'False' as a boolean, so I need to an alternative value"""
    if word in STOP_WORDS:
        return 1
    else:
        return 0


def load_stopwords():
    new_lang = Path.cwd() / "new_lang"
    path = new_lang / "stop_words.py"
    spec = importlib.util.spec_from_file_location("STOP_WORDS", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    STOP_WORDS = module.STOP_WORDS
    return STOP_WORDS


def load_lookups():
    new_lang = Path.cwd() / "new_lang"
    if len(list(new_lang.iterdir())) > 0:
        lang_name = list(new_lang.iterdir())[0].name
        lookups_path = new_lang / "lookups"
        for lookup in lookups_path.iterdir():
            key = lookup.stem[lookup.stem.find("_") + 1 :]
            if "lemma" in key:
                lemma_data = srsly.read_json(lookup)
            if "features" in key:
                features_data = srsly.read_json(lookup)
            if "pos" in key:
                pos_data = srsly.read_json(lookup)
        return lemma_data, features_data, pos_data


def make_corpus(lang_name: str):
    new_lang = Path.cwd() / "new_lang"
    lemma_data, features_data, pos_data = load_lookups()
    STOP_WORDS = load_stopwords()
    text_path = new_lang / "texts"
    corpus = ""
    text_count = 0
    token_count = 0
    max_length = 0
    corpus = []
    tokens = []

    for text in text_path.iterdir():
        corpus.append(text.read_text())
        if len(text.read_text()) > max_length:
            max_length = len(text.read_text()) + 1
        text_count += 1
    # create doc from corpus with obj, count tokens
    try:
        mod = __import__(f"new_lang", fromlist=[lang_name.capitalize()])
    except SyntaxError:  # Unable to load __init__ due to syntax error
        # redirect /edit?file_name=examples.py
        print("[*] SyntaxError, please correct this file to proceed.")

    ignore = [
        "\n",
        " ",
        "\n\n",
        "\n     ",
        "\n\n\n\n",
    ]  # TODO option in the UI to show/hide the following:
    #    LIST_UNITS = split_chars(_units)
    #     LIST_CURRENCY = split_chars(_currency)
    #     LIST_QUOTES = split_chars(_quotes)
    #     LIST_PUNCT = split_chars(_punct)
    #     LIST_HYPHENS = split_chars(_hyphens)
    #     LIST_ELLIPSES = [r"\.\.+", "…"]
    #     LIST_ICONS = [r"[{i}]".format(i=_other_symbols)]

    cls = getattr(mod, lang_name.capitalize())
    nlp = cls()
    nlp.max_length = max_length
    for doc in nlp.pipe(corpus):
        token_count += len([t for t in doc])

        tokens.extend(
            [
                Token(
                    text=t.text,
                    lemma_=lemma_data.get(t.text, ""),
                    pos_=pos_data.get(t.text, ""),
                    morph=features_data.get(t.text, ""),
                    is_stop=is_stop(t.text, STOP_WORDS),
                )
                for t in doc
                if not t.text in ignore
            ]
        )
    to_json = []
    counter = token_count
    rank = 1
    for i in Counter(tokens).most_common():
        dict_ = i[0]._asdict()
        dict_["count"] = i[1]
        counter = counter - i[1]
        dict_["rank"] = rank
        rank += 1
        dict_["remain"] = counter
        to_json.append(dict_)
    tokens_json = srsly.json_dumps(to_json)

    stats = {
        "texts": text_count,
        "tokens": token_count,
        "unique_tokens": len(set([t.text for t in tokens])),
    }
    print(stats)
    stats_json = srsly.json_dumps(stats)

    # save json to disk
    corpus_dir = Path.cwd() / "new_lang" / "corpus_json"
    if (
        not corpus_dir.exists()
    ):  # Directory does not exist the first time the app is used
        corpus_dir.mkdir(parents=True, exist_ok=True)

    srsly.write_json((corpus_dir / "tokens.json"), tokens_json)
    srsly.write_json((corpus_dir / "stats.json"), stats_json)
