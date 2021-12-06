from spacy.lang.tokenizer_exceptions import BASE_EXCEPTIONS
from spacy.symbols import ORTH, NORM, LEMMA
from spacy.util import update_exc

exclusions = [

]

# אינעם, אויפן, ביים
# ס׳איז,
# האסטו, ביסטו, דארפסטו
_exc = {
    "אויפן": [{ORTH: "אויפ", NORM: "אויף"}, {ORTH: "ן", NORM: "דעם"}],
    "אינעם": [{ORTH: "אינ", NORM: "אין"}, {ORTH: "עם", NORM: "דעם"}],
    "ביים": [{ORTH: "ביי"}, {ORTH: "ם", NORM: "דעם"}],

    "ס׳איז": [{ORTH: "ס׳", NORM: "עס"}, {ORTH: "איז"}],
    "כ׳בין": [{ORTH: "כ׳", NORM: "איך"}, {ORTH: "בין"}],
    "ר׳האט": [{ORTH: "ר׳", NORM: "ער"}, {ORTH: "האט"}],

    "האסטו": [{ORTH: "האסט"}, {ORTH: "ו", NORM: "דו"}],
    "ביסטו": [{ORTH: "ביסט"}, {ORTH: "ו", NORM: "דו"}],
    "דארפסטו": [{ORTH: "דארפסט"}, {ORTH: "ו", NORM: "דו"}],
}

TOKENIZER_EXCEPTIONS = update_exc(BASE_EXCEPTIONS, _exc)
