def parse_csv_files():
    dict_entries = dict()
    for index in range(1,6):
        file_name = f"data/rus/{index}v.txt"
        with open(file_name) as f:
            lines = f.readlines()
            value = []
            key = ""
            for line in lines:
                line = line.rstrip('\n')
                if '\t' in line:
                    if key != "":
                        dict_entries[key] = value
                        value = []
                    tokens = line.split('\t')
                    key = tokens[0]
                    value.append(tokens[1])
                else:
                    value.append(line)
    output_file = "data/rus/final.tsv"
    with open(output_file, "w") as f:
        for key in dict_entries.keys():
            value = " ".join(dict_entries[key])
            f.write(f"{key}\t{value}\n")


if __name__ == '__main__':
    parse_csv_files()

