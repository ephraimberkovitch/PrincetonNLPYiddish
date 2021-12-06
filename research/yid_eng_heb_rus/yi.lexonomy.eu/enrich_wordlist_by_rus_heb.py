import csv
import os

from google.cloud import translate

ROOT_PATH = os.getcwd()


def analyze_yid_eng_csv():

    with open(ROOT_PATH + "/data/wordlist.csv") as input_csvfile:
        distinct_english_definitions = set()
        reader = csv.DictReader(input_csvfile)
        for row in reader:
            if row["Definition"] not in distinct_english_definitions:
                distinct_english_definitions.add(row["Definition"])

    counter = 0
    for d in distinct_english_definitions:
        counter += len(d)

    return counter


def generate_enriched_csv():
    # input - Base,Romanized,Yiddish,Gloss,Definition
    # output - Base,Romanized,Yiddish,Gloss,English,Russian,Hebrew
    translations = dict()
    translate_client = translate.Client()
    with open(ROOT_PATH + "/data/wordlist.csv") as input_csvfile, open(ROOT_PATH + "/data/wordlist2.csv", 'w') as output_csvfile:
        reader = csv.DictReader(input_csvfile)
        fieldnames = ['Base', 'Romanized', 'Yiddish', 'Gloss', 'English', 'Russian', 'Hebrew']
        writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
        counter = 0
        for row in reader:
            counter += 1
            eng = row['Definition']
            if eng in translations:
                rus = translations[eng]['rus']
                heb = translations[eng]['heb']
            else:
                try:
                    translation = translate_client.translate(eng, target_language='ru')
                    rus = translation['translatedText']
                except Exception as err:
                    rus = ""
                    print("\t"+str(err))
                try:
                    translation = translate_client.translate(eng, target_language='he')
                    heb = translation['translatedText']
                except Exception as err:
                    heb = ""
                    print("\t"+str(err))
                if heb != "" or rus != "":
                    translations[eng] = {'rus': rus, 'heb': heb}
            writer.writerow({'Base': row['Base'],
                             'Romanized': row['Romanized'],
                             'Yiddish': row['Yiddish'],
                             'Gloss': row['Gloss'],
                             'English': eng,
                             'Russian': rus,
                             'Hebrew': heb,
                             })
            print(counter)


def strip_special_yiddish_characters(word):
    return word.replace('אָ','א').replace('אַ','א').replace('ײַ','יי').\
        replace('ײ','יי').replace('פֿ','פ').replace('בֿ','ב').\
        replace('ױ','וי').replace('װ','וו').replace('פּ','פ')


def generate_lexonomy_xml():
    # input - Base,Romanized,Yiddish,Gloss,English,Russian,Hebrew
    with open(ROOT_PATH + "/data/wordlist2.csv") as input_csvfile, open(ROOT_PATH + "/data/yiddish.xml", 'w') as output_xmlfile:
        reader = csv.DictReader(input_csvfile)
        output_xmlfile.write("<yiddish>")
        counter = 1
        for row in reader:
            xml_entry = """
    <entry xmlns:lxnm='http://www.lexonomy.eu/' lxnm:entryID='{counter}'>
        <yiddish>{yid}</yiddish>
        <gloss>{gloss}</gloss>
        <base>{base}</base>
        <romanized>{roman}</romanized>
        <eng>{eng}</eng>
        <heb>{heb}</heb>
        <rus>{rus}</rus>
        <simpleForm>{simple}</simpleForm>
    </entry>
            """.format(
                counter=counter,
                yid=row["Yiddish"],
                gloss=row["Gloss"],
                base=row["Base"],
                roman=row["Romanized"],
                eng=row["English"],
                heb=row["Hebrew"],
                rus=row["Russian"],
                simple=strip_special_yiddish_characters(row["Yiddish"])
            )
            counter += 1
            if counter % 100 == 0:
                print(counter)
            output_xmlfile.write(xml_entry)
        output_xmlfile.write("</yiddish>")


if __name__ == '__main__':
    # generate_enriched_csv()
    # print(analyze_yid_eng_csv())
    generate_lexonomy_xml()