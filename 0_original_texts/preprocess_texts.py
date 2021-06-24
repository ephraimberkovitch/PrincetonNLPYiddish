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


if __name__ == '__main__':
    clean_tanach()