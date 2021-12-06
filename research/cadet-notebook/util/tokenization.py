from pathlib import Path
import importlib.util


def tokenization(lang_name: str):
    new_lang = Path.cwd() / "new_lang"
    path = new_lang / "examples.py"
    spec = importlib.util.spec_from_file_location("sentences", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sentences = module.sentences

    # Load language object as nlp
    try:
        mod = __import__(f"new_lang", fromlist=[lang_name.capitalize()])
    except SyntaxError:  # Unable to load __init__ due to syntax error
        # redirect /edit?file_name=examples.py
        message = "[*] SyntaxError, please correct this file to proceed."
        return RedirectResponse(url="/edit?file_name=tokenizer_exceptions.py")
    cls = getattr(mod, lang_name.capitalize())
    nlp = cls()
    spacy_sentences = []
    for sentence in sentences:
        sent = ""
        doc = nlp(sentence)
        for token in doc:
            sent += f"<span style='border: 5px solid blue; margin:5px;'>{token}</span>&nbsp;"
        spacy_sentences.append(sent)
    result = """"""
    for sent in spacy_sentences:
        result += "<div>" + sent + "</div>"
    return result
