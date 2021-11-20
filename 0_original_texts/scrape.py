import re
import requests
from selenium import webdriver


driver = webdriver.Chrome()


def get_page_source(url):
    driver.get(url)
    page_content = driver.page_source
    return page_content


def is_yiddish_title(title):
    heb_ab = [chr(1488+code) for code in range(27)]
    return any(char in title for char in heb_ab)


def scrape_bs():
    regex1 = r"<h2 class=\"entry-title(?: idish)*\"><a href=\"(.*?)\" rel=\"bookmark\">(.*?)<\/a><\/h2>"
    # regex2 = r"<h2 class=\"entry-title idish\"><a href=\"(.*?)\" rel=\"bookmark\">(.*?)<\/a><\/h2>"
    counter = 1000
    for page_num in range(1, 23):
        url = f"https://www.gazetaeao.ru/category/idish/page/{page_num}/"
        # page = requests.get(url)
        page_content = get_page_source(url)

        matches = re.finditer(regex1, page_content, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            article_url = match.group(1)
            article_title = match.group(2)

            if is_yiddish_title(article_title):
                article_page_content = get_page_source(article_url)
                res = re.findall(r"<div class=\"entry-content(?: idish)*\">((.|\n)*?)<\/div>", article_page_content)
                try:
                    clean_text = re.sub(r"<.*?>", " ", res[0][0], 0, re.MULTILINE)
                except:
                    clean_text = ""
                    print(f"{counter}: {article_url}")
                file_yaml = open(f"BirobidzhannerShtern/{counter}.yaml", "w")
                file_yaml.write(f"url: {article_url}\n")
                file_yaml.write(f"title: {article_title}")
                file_yaml.close()
                with open(f"BirobidzhannerShtern/{counter}.txt", "w") as file_txt:
                    file_txt.write(clean_text)
                counter += 1

    driver.close()


if __name__ == '__main__':
    scrape_bs()
