import csv


def translate_gibberish_to_unicode_russian():

    r = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
    g = "°Ð?Ñ?Ò?Ó?Ô?Õ?ñ?Ö?×?Ø?Ù?Ú?Û?Ü?Ý?Þ?ß?à?á?â?ã?ä?å?æ?ç?è?é?ê?ë?ì?í?î?ï"

    rm = dict()
    gm = dict()

    for i in range(len(r)):
        rm[i] = r[i]

    for i in range(len(g)):
        gm[g[i]] = i

    root = "/Users/ephraimberkovitch/workspace/berkotech/yiddish/verterbuch/data/rus/"
    for i in [1,2,3,4,5]:
        f1 = root + f'{i}c.txt'
        file = open(f1)
        text = file.read()
        txt2 = ""
        for c in text:
            if c not in gm:
                txt2 += c
            else:
                txt2 += rm[gm[c]]
        f2 = root + f'{i}v.txt'
        file2 = open(f2,"w")
        file2.write(txt2)
        file2.close()


def analyze_yid_eng_csv():
    # Base,Romanized,Yiddish,Gloss,Definition
    base_set = set()
    glossary = set()
    f = "/Users/ephraimberkovitch/workspace/berkotech/yiddish/verterbuch/data/eng/wordlist.csv"
    with open(f) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            base_set.add(row['Base'])
            gloss = row['Gloss'].replace('?','')
            variants = gloss.split(' ')
            for variant in variants:
                partsOfSpeach = variant.split('.')
                for partOfSpeach in partsOfSpeach:
                    options = partOfSpeach.split('/')
                    for option in options:
                        glossary.add(option)
    print(len(base_set))
    print(glossary)


def generate_yid_rus_csv():
    # Base,Romanized,Yiddish,Gloss,Definition
    root = "/Users/ephraimberkovitch/dev/yiddish/verterbuch/data/rus/"
    r = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
    with open(root + "wordlist3.csv", 'w') as csvfile:
        fieldnames = ['Base', 'Romanized', 'Yiddish', 'Gloss', 'Definition']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        yid = ""
        rus = ""
        for i in [1,2,3,4,5]:
            f1 = root + f'{i}v.txt'
            file = open(f1)
            lines = file.readlines()
            for line in lines:
                if '\t' in line or not any(l in r for l in line.strip('\n')):
                    if yid != "" or rus != "":
                        writer.writerow({'Yiddish': yid, 'Definition': rus})
                        yid = ""
                        rus = ""
                else:
                    rus += line.replace('\n',' ')

                if yid is not None:
                    rus = line.strip('\n')
                    # writer.writerow({'Yiddish': yid, 'Definition': rus})
                    # yid = None
                elif not any(l in r for l in line):
                    yid = line.strip('\n')
                else:
                    yid = ""
                    if '\t' not in line:
                        continue
                    else:
                        yid = line.split('\t')[0]
                        rus = line.split('\t')[1].strip('\n')
                        # writer.writerow({'Yiddish': line.split('\t')[0], 'Definition': line.split('\t')[1].strip('\n')})
            file.close()


def yid_grammar():
    partsOfSpeech = ['ADV','ADJ','NOUN','N','ART','INF','V.1','V.2','V.3','PTCP']
    genders = ['FEM','NEUT','MASC']
    cases = ['NOM','ACC','DAT']
    many = ['SG','PL']
    others = ['DIM','CNJ','PART','PRES','PTCP','PRED','INDF','DEF']
    # { '2', 'PTCP', 'SUPL', 'ADV', 'NOM', 'DIM', 'ADJ', 'ADV-V', '3', 'CORREL',
    # 'UNK1', 'PL', 'MASC', 'DAT', 'N', 'EXCLAM', 'ART', 'ATTR', 'NOUN', 'ACC', 'POSS',
    # 'INDF', 'PRES', 'PAST', 'PRED', 'PREP', 'PN', 'DEF', '1', 'PART', 'SUBR', 'COMP',
    # 'NUM', 'FEM', 'PREFIX', 'V', 'INF', 'PTCL', 'SG', 'NEUT', 'CNJ'}


if __name__ == '__main__':
    # translate_gibberish_to_unicode_russian()
    generate_yid_rus_csv()
    # analyze_yid_eng_csv()