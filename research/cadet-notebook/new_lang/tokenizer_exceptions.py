
from spacy.lang.tokenizer_exceptions import BASE_EXCEPTIONS
from spacy.symbols import ORTH, NORM, LEMMA
from spacy.util import update_exc

exclusions = [

]

TOKENIZER_EXCEPTIONS = update_exc(BASE_EXCEPTIONS, *exclusions)
