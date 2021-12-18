import re
import requests
from itertools import chain

reg1 = r"<a href=\"(.*?)\"(?:.*?)<span class=\"hname\">(.*?)<\/span><\/a>"  # titles + urls
reg2 = r"<p[^>]*>(.*?)</p>"# all <p>
reg3 = r"<.*?>" #cleaning up HTML tags

def scrape_forverts():
    global_list = list()
    for yiddish_page in range(1, 379):

        page_content = requests.get(f"https://forward.com/yiddish/?p={yiddish_page}")
        contenttxt = page_content.text
        contenthtml = open(f"/Users/rabea/PycharmProjects/Forverts/html_{yiddish_page}.txt", "w")
        contenthtml.write(contenttxt)
        contenthtml.close()

        matches1 = re.finditer(reg1, contenttxt, re.MULTILINE)

        file_txt_1 = open(f"/Users/rabea/PycharmProjects/Forverts/{yiddish_page}_1.txt", "w")
        file_txt_2 = open(f"/Users/rabea/PycharmProjects/Forverts/{yiddish_page}_2.txt", "w")

        for matchNum, match in enumerate(matches1, start=1):
            file_txt_1.write(match.group(1))
            file_txt_1.write('\n')
            file_txt_2.write(match.group(2))
            file_txt_2.write('\n')

        file_txt_1.close()
        file_txt_2.close()

        article_list = [line.split() for line in open(f"{yiddish_page}_1.txt")]
        global_list += article_list
    #print(global_list)
    yiddish_alphabet = []
    yiddish = chain(range(1488, 1515), range(1519, 1523), range(1425, 1442), range(1443, 1466), range(1467, 1470),
                    range(1471, 1472), range(1473, 1475), range(1476, 1477))
    for u in yiddish:
        yiddish_alphabet += chr(u)

    print(yiddish_alphabet)

    for i, link in enumerate (global_list):
        link_html = requests.get(link[0])
        link_html_text = link_html.text
        matches = re.finditer(reg2, link_html_text, re.MULTILINE)

        txt = ""
        for match in matches:
            grp = match.group()

            if grp[3] in yiddish_alphabet:
                txt += match.group() + "\n"
        txt = re.sub(reg3, " ", txt, 0, re.MULTILINE)
        if txt.strip()!='':
            link_html_text = open(f"/Users/rabea/PycharmProjects/Forverts/{i}_allPs.txt", "w")
            link_html_text.write(txt)
            link_html_text.close()



scrape_forverts()