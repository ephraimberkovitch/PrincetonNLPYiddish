
import spacy
from spacy.language import Language
from spacy.lang.tokenizer_exceptions import URL_MATCH
#from thinc.api import Config
from .stop_words import STOP_WORDS
from .tokenizer_exceptions import TOKENIZER_EXCEPTIONS
from .punctuation import TOKENIZER_PREFIXES, TOKENIZER_SUFFIXES, TOKENIZER_INFIXES
from .lex_attrs import LEX_ATTRS
from .tag_map import TAG_MAP
from .syntax_iterators import SYNTAX_ITERATORS
from spacy.tokens import Doc
from typing import Optional
from thinc.api import Model
import srsly
from .lemmatizer import YiddishLemmatizer

# https://nightly.spacy.io/api/language#defaults
class YiddishDefaults(Language.Defaults):
    stop_words = STOP_WORDS
    tokenizer_exceptions = TOKENIZER_EXCEPTIONS
    prefixes = TOKENIZER_PREFIXES
    suffixes = TOKENIZER_SUFFIXES
    infixes = TOKENIZER_INFIXES
    token_match = None
    url_match = URL_MATCH
    tag_map = TAG_MAP
    writing_system = {"direction": "rtl", "has_case": False, "has_letters": True}

@spacy.registry.languages("yi") #https://nightly.spacy.io/api/top-level#registry
class Yiddish(Language):
    lang = "yi"
    Defaults = YiddishDefaults

    #custom on init

@Yiddish.factory(
    "lemmatizer",
    assigns=["token.lemma"],
    default_config={"model": None, "mode": "lookup", "overwrite": False},
    default_score_weights={"lemma_acc": 1.0},
)
def make_lemmatizer(
    nlp: Language, model: Optional[Model], name: str, mode: str, overwrite: bool
):
    return YiddishLemmatizer(nlp.vocab, model, name, mode=mode, overwrite=overwrite)

#Add locations of lookups data to the registry
@spacy.registry.lookups("yi")
def do_registration():
    from pathlib import Path
    cadet_path = Path.cwd()
    lookups_path = cadet_path / "new_lang" / "lookups"
    result = {}
    for lookup in lookups_path.iterdir():
        key = lookup.stem[lookup.stem.find('_') + 1:]
        result[key] = str(lookup)
    return result

__all__ = ["Yiddish"]
