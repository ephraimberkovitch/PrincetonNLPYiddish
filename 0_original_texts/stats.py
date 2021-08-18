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


if __name__ == '__main__':
    scrape()