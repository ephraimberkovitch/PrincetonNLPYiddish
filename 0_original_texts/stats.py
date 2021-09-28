import os
import requests
from bs4 import BeautifulSoup


SITES_TO_SCRAPE = [
    "https://forward.com/yiddish/",
    "https://www.gazetaeao.ru/category/idish/",
    "https://yiddishbranzhe.com/",
    "http://www.cs.uky.edu/~raphael/yiddish/sholemAleykhem/contents.html"
]

def analyze_yiddish_tanakh():
    # how many tokens in total?
    # how many different tokens?
    # frequency table
    # compare with Finkel's dictionary
    pass


def scrape():
    main = requests.get("http://www.cs.uky.edu/~raphael/yiddish/sholemAleykhem/contents.html")
    soup = BeautifulSoup(main.content, 'html.parser')
    links = soup.find_all('tr')
    counter = 0
    for tr in links:
        cont = tr.find_all("td")
        for td in cont:
            if td.text != 'גאַנץ':
                continue
            counter += 1
            href = "http://www.cs.uky.edu/~raphael/yiddish/sholemAleykhem/" + td.find_all("a")[0].get("href")
            try:
                page = requests.get(href)
                s = BeautifulSoup(page.content, 'html.parser')
                with open(f"../0_original_texts/SholemAleykhem/{counter}.txt", "wt") as output:
                    output.write(str(s.body))
            except:
                pass


def scrape_yiddish_branzhe():
    counter = 0
    for page_num in range(1,172):
        main = requests.get(f"https://yiddishbranzhe.com/page/{page_num}")
        soup = BeautifulSoup(main.content, 'html.parser')
        articles = soup.find_all("article")
        for article in articles:
            try:
                if 'featured-secondary' in article.attrs['class']:
                    continue
                divs = article.find_all("div")
                a = divs[1].find("a")
                detail = requests.get(a["href"])
                soup2 = BeautifulSoup(detail.text, 'html.parser')
                article_tags = soup2.find_all("article")
                h1 = article_tags[0].find_all("h1")
                article_title = h1[0].text
                article_content = article_tags[0].get_text()
                with open(f"../0_original_texts/YiddishBranzhe/{counter}.yaml", "wt") as output:
                    output.write(f'link: {a["href"]}\ntitle: {article_title}')
                with open(f"../0_original_texts/YiddishBranzhe/{counter}.txt", "wt") as output:
                    output.write(article_content)
                counter += 1
            except:
                pass


def fix_yb_dir():
    yb_root_location = "../0_original_texts/YiddishBranzhe"
    files = os.listdir(yb_root_location)
    for file in files:
        if '.txt' in file:
            full_file_path = os.path.join(yb_root_location, file)
            with open(full_file_path) as f:
                content = f.read()
            if 'נאָטיצן פֿונעם רעדאַקטאָר — 48' in content:
                file_counter = int(file.split(".")[0])
                full_text_path = os.path.join(yb_root_location, str(file_counter)+".txt")
                os.remove(full_text_path)
                full_yaml_path = os.path.join(yb_root_location, str(file_counter)+".yaml")
                os.remove(full_yaml_path)


if __name__ == '__main__':
    # scrape_yiddish_branzhe()
    fix_yb_dir()