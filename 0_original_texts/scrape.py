import re
import requests
from selenium import webdriver


driver = webdriver.Chrome()
def get_page_source(url):
    driver.get(url)
    page_content = driver.page_source
    return page_content


def scrape_bs():

    regex1 = r"<h2 class=\"entry-title\"><a href=\"(.*?)\" rel=\"bookmark\">(.*?)<\/a><\/h2>"
    regex2 = r"<h2 class=\"entry-title idish\"><a href=\"(.*?)\" rel=\"bookmark\">(.*?)<\/a><\/h2>"
    for page_num in range(1, 23):
        url = f"https://www.gazetaeao.ru/category/idish/page/{page_num}/"
        # page = requests.get(url)
        page_content = get_page_source(url)

        matches = re.finditer(regex1, page_content, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):

            print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
                                                                                end=match.end(), match=match.group()))

            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1

                print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                                start=match.start(groupNum),
                                                                                end=match.end(groupNum),
                                                                                group=match.group(groupNum)))


if __name__ == '__main__':
    scrape_bs()
