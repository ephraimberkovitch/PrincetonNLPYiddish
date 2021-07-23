import pandas as pd


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

    for tanakh_token in tanakh_dict:
        if tanakh_token not in finkel_dict:
            finkel_missing += 1

    print(finkel_missing)

if __name__ == '__main__':
    # clean_tanach()
    # generate_tanach_stats()  # 24,776
    finkel_stats()