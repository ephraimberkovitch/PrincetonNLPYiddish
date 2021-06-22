SITES_TO_SCRAPE = [
    "https://forward.com/yiddish/",
    "https://www.gazetaeao.ru/category/idish/",
    "https://yiddishbranzhe.com/",
    "http://www.cs.uky.edu/~raphael/yiddish/sholemAleykhem/contents.html"
]

def validate_id(id):
    even = False if len(id)%2==1 else True
    sum = 0
    for d in id:
        add = int(d) if not even else int(d) * 2
        if add > 9:
            add = add // 10 + add % 10
        even = not even
        sum += add
    return sum % 10 == 0

if __name__ == '__main__':
    print(validate_id("310747928"))