
from typing import List, Tuple
from spacy.pipeline import Lemmatizer
from spacy.tokens import Token
from spacy.vocab import Vocab
from typing import Optional, List, Dict, Tuple
from thinc.api import Model
import spacy 

class YiddishLemmatizer(Lemmatizer):
    def __init__(
        self,
        vocab: Vocab,
        model: Optional[Model],
        name: str = "lemmatizer",
        *,
        mode: str = "lookup",
        overwrite: bool = False,
    ) -> None:
        super().__init__(vocab, model, name, mode=mode, overwrite=overwrite)
        
        lookups_tables = spacy.registry.lookups.get(yi)()
        if not nlp.vocab.lookups.has_table('lemma_lookup'):
            language_data = srsly.read_json(lookups_tables["lemma_lookup"])
            nlp.vocab.lookups.add_table("lemma_lookup", language_data)
           
    
    def rule_lemmatize(self, token: Token) -> List[str]:
        pass

    def lookup_lemmatize(self, token: Token) -> List[str]:

        lookup_table = self.lookups.get_table("lemma_lookup")
        string = token.text.lower()
        return [lookup_table.get(string, string)]


