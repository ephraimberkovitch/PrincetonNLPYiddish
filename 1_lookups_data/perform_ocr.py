import os
import sys
from tqdm import tqdm


def run_tesseract(file_name_template, lang, from_page, to_page):
    for i in tqdm(range(from_page, to_page+1)):
        page = str(i)
        if i < 10:
            page = "00" + page
        if 10 <= i < 100:
            page = "0" + page

        # gk_136_Page_[PAGE]_Image_0001.png
        file_name = file_name_template.replace("[PAGE]", page)
        os.system(f"tesseract {file_name} stdout -l {lang} > {page}.txt")


if __name__ == '__main__':
    # https://transkribus.eu/lite/collection/129964, eScriptorium
    # https://medium.datadriveninvestor.com/review-for-tesseract-and-kraken-ocr-for-text-recognition-2e63c2adedd0
    print(sys.argv)
    run_tesseract(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    print(os.getcwd())
