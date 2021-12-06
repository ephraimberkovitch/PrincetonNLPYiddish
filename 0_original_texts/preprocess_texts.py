import numpy as np
import pandas as pd
import os
import re


def clean_tanach():
    with open("YiddishTanakh/_all.txt") as raw, open("YiddishTanakh/_all_cleaned.txt","wt") as clean:
        raw_text = raw.read()
        clean_text = raw_text.replace("/", ".")
        clean_text = clean_text.replace("{", "")
        clean_text = clean_text.replace("}", "")
        clean_text = clean_text.replace(":", "")
        for digit in '0123456789':
            clean_text = clean_text.replace(digit, "")
        for letter in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            clean_text = clean_text.replace(letter, "")
        clean.write(clean_text)


def generate_tanach_stats():
    # how many tokens in total?
    # how many different tokens? - 24,776
    # frequency table - V
    # compare with Finkel's dictionary - 17475 missing
    d = dict()
    with open("YiddishTanakh/_all_cleaned.txt") as all_tanakh:
        text = all_tanakh.read()
        tokens = text.split(' ')
        for token in tokens:
            if token not in [' ', '.']:
                token = token.strip(';,.')
                if token in d:
                    d[token] += 1
                else:
                    d[token] = 1

    (pd.DataFrame.from_dict(data=d, orient='index').to_csv('YiddishTanakh/vocab.csv', header=False))


def finkel_stats():
    finkel_dict = {row[2]: True for _, row in pd.read_csv("../1_lookups_data/wordlist.csv").iterrows()}
    tanakh_dict = {row[0]: row[1] for _, row in pd.read_csv("YiddishTanakh/vocab.csv").iterrows()}

    print(len(finkel_dict))
    print(len(tanakh_dict))

    finkel_missing = 0
    total_tanakh = 0

    for tanakh_token in tanakh_dict:
        if tanakh_token not in finkel_dict:
            finkel_missing += 1
        total_tanakh += tanakh_dict[tanakh_token]

    print(finkel_missing)  # finkel:125059 => tanakh-different:24775 => tanakh-missing-in-finkel:17475
    print(total_tanakh)  # tanakh-total:595287


def add_yiddish_lemmas_to_finkel():
    finkel = pd.read_csv("../1_lookups_data/wordlist.csv")
    # basic_form = finkel[finkel.Gloss == 'NOUN.MASC']
    basic_form = finkel[(finkel.Base == finkel.Romanized) | (finkel.Gloss == 'NOUN.MASC')]
    print(len(basic_form))
    basic_form_dict = {row[0]: row[2] for _, row in basic_form.iterrows()}
    finkel['lemma'] = finkel.apply(lambda row: lemmatize(row, basic_form_dict), axis=1)
    print(len(finkel[finkel.lemma != '']))
    finkel.to_csv("../1_lookups_data/wordlist_with_lemmas.csv", index=False)
    # 5657 lemmas, 23057 did get lemmas - finkel.Gloss == 'NOUN.MASC'
    # 16660 lemmas, 68879 did get lemmas - finkel.Base == finkel.Romanized
    # 16682 lemmas, 68927 did get lemmas - both


def generate_lookup_files():
    """
    with open("../1_lookups_data/wordlist_with_lemmas.csv") as f:
        csv_contents = f.read()
    normalized_csv_contents = normalize(csv_contents,
                                        remove_diacritics=True,
                                        normalize_hyphens=False,
                                        normalize_apostrophe=False,
                                        normalize_double_quotes=False)
    with open("../1_lookups_data/wordlist_with_lemmas_norm.csv", "w") as f:
        f.write(normalized_csv_contents)
    """
    df = pd.read_csv("../1_lookups_data/wordlist_with_lemmas_norm.csv")
    # df.isnull().sum()
    records = df.to_dict(orient="records")
    with open("../research/cadet-notebook/new_lang/lookups/yi_lemma_lookup.json", "w") as f1:
        with open("../research/cadet-notebook/new_lang/lookups/yi_upos_lookup.json", "w") as f2:
            with open("../research/cadet-notebook/new_lang/lookups/yi_features_lookup.json", "w") as f3:
                f1.write("{\n")
                f2.write("{\n")
                f3.write("{\n")
                for record in records:
                    # Base,Romanized,Yiddish,Gloss,Definition,lemma
                    if str(record['lemma']) != 'nan':
                        f1.write(f"\"{record['Yiddish']}\":\"{record['lemma']}\",\n")
                    if record['Gloss']=='N' or str(record['Gloss']).startswith('N.'):
                        # https://universaldependencies.org/cs/feat/NameType.html
                        f3.write(f"\"{record['Yiddish']}\":\"PROPN.Giv\",\n")
                    upos = str(record['Gloss'])
                    if 'ADJ' in upos:
                        upos = 'ADJ'
                    elif 'NOUN' in upos:
                        upos = 'NOUN'
                    elif upos=='N' or upos.startswith('N.'):
                        upos = 'PROPN'
                    elif upos=='PREP':
                        upos = 'ADP'
                    elif upos=='CNJ':
                        upos = 'CCONJ'
                    elif 'V.' in upos:
                        upos = 'VERB'
                    elif 'ADV' in upos:
                        upos = 'ADV'
                    elif 'PART' in upos:
                        upos = 'PART'
                    else:
                        continue
                    f2.write(f"\"{record['Yiddish']}\":\"{upos}\",\n")
                f1.write("}\n")
                f2.write("}\n")
                f3.write("}\n")


def lemmatize (row, basic_form_dict):
   return basic_form_dict.get(row[0], "")


def normalize_texts():
    FOLDERS = [
        'BirobidzhannerShtern',
        'HaifaPrager',
        'SholemAleykhem',
        'YiddishBranzhe' #,
        # 'YiddishTanakh'
    ]

    for folder in FOLDERS:
        files = os.listdir(folder)
        for file in files:
            if not file.endswith('.txt'):
                continue

            f = open(folder + "/" + file)
            file_text = f.read()
            f.close()

            # remove multiple adjacent spaces
            find = r"( )+"
            replace = " "
            file_text = re.sub(find, replace, file_text, 0, re.MULTILINE)

            file_text = normalize(file_text, remove_diacritics=True)

            f = open("../research/cadet-notebook/new_lang/texts/" + folder + "_" + file, "w")
            f.write(file_text)
            f.close()


def normalize(input, remove_diacritics=False, normalize_double_quotes=True, normalize_hyphens=True, normalize_apostrophe=True):
    # https://nlp.stanford.edu/IR-book/html/htmledition/accents-and-diacritics-1.html
    # https://en.wikipedia.org/wiki/Hebrew_(Unicode_block)
    # https://www.cl.cam.ac.uk/~mgk25/ucs/quotes.html
    output = input
    # diacritics - chr(0x0591) - chr(0x05c7), except of chr(0x05be); ײַ שרײַבן
    if remove_diacritics is True:
        for c in range(1425, 1480):
            if c == 1470:
                continue
            output = output.replace(chr(c), "")
    # oy, ey, ... - 05f0, 05f1, 05f2: 'װ ױ ײ'
    output = output.replace(chr(0x05f0), "וו")
    output = output.replace(chr(0x05f1), "וי")
    output = output.replace(chr(0x05f2), "יי")
    # apostrophe - "' ′ ‘ ’ -> ׳" (chr(39)+" "+chr(0x2032)+" "+chr(0x2018)+" "+chr(0x2019)+" -> "+chr(0x05f3))
    if normalize_apostrophe is True:
        for c in [39, 0x2032, 0x2018, 0x2019]:
            output = output.replace(chr(c), chr(0x05f3))
    # double quotes : '" “ ” -> ״' (chr(0x22)+" "+chr(0x201c)+" "+chr(0x201d)+" -> "+chr(0x5f4))
    if normalize_double_quotes is True:
        for c in [0x22, 0x201c, 0x201d]:
            output = output.replace(chr(c), chr(0x05f4))
    # top hyphen 0x05be vs 0x2d: אני כותב בעברית - כך וכך, תל-אביב תל־אביב תל־אביב
    # output = re.sub("(\w+)-(\w+)", r"\1־\2", output)
    if normalize_hyphens is True:
        output = re.sub(r"(\w+)-(\w+)", rf"\1{chr(0x05be)}\2", output)
    # chr(0x05f3)+chr(0x05f3) inside a word -> to chr(0x5f4))
    output = re.sub(rf"(\w+){chr(0x05f3)}{chr(0x05f3)}(\w+)", rf"\1{chr(0x05f4)}\2", output)
    return output


def generate_stopwords():
    with open("YiddishTanakh/_all_cleaned.txt") as f:
        tanakh_text = f.read()
    norm_tanakh_text = normalize(tanakh_text, remove_diacritics=True)
    words_frequency_table = dict()
    words = norm_tanakh_text.split()
    for word in words:
        if word is None or word.strip() == '':
            continue
        if word not in words_frequency_table:
            words_frequency_table[word] = 1
        else:
            words_frequency_table[word] += 1
    with open('../1_lookups_data/stopwords.tsv', 'w') as f:
        for word in sorted(words_frequency_table, key=words_frequency_table.get, reverse=True):
            f.write(f"{word}\t{words_frequency_table[word]}\n")


if __name__ == '__main__':
    # clean_tanach()
    # generate_tanach_stats()  # 24,776
    # finkel_stats()
    # add_yiddish_lemmas_to_finkel()
    # normalize_texts()
    # generate_stopwords()
    generate_lookup_files()