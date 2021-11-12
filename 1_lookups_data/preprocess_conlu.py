from dataclasses import dataclass


@dataclass
class SentenseStats:
    num_of_words: int
    num_of_annotated_words: int


with open("conlu_stats.tsv") as f:
    lines = f.readlines()

preannotated_words_ratio_by_sentence = dict()

contentful_lines = lines[1:]
for line in contentful_lines:
    line = line.rstrip('\n')
    tokens = line.split('\t')
    if len(tokens) < 11 or tokens[2]=='':
        continue
    sentence_id = tokens[0]
    num_of_annotated_words = 1 if any(token not in ['_', ''] for token in tokens[3:]) else 0
    if sentence_id not in preannotated_words_ratio_by_sentence:
        sa = SentenseStats(num_of_words=1,
                           num_of_annotated_words=num_of_annotated_words)
    else:
        sa = preannotated_words_ratio_by_sentence[sentence_id]
        sa.num_of_words += 1
        sa.num_of_annotated_words += num_of_annotated_words
    preannotated_words_ratio_by_sentence[sentence_id] = sa

with open("conlu_stats_output.tsv", "w") as f:
    header_line = lines[0].rstrip('\n') + '\tratio\n'
    f.write(header_line)
    contentful_lines = lines[1:]
    for line in contentful_lines:
        line = line.rstrip('\n')
        tokens = line.split('\t')
        sentence_id = tokens[0]
        sa = preannotated_words_ratio_by_sentence.get(sentence_id)
        if sa is not None:
            ratio = str(round(sa.num_of_annotated_words / sa.num_of_words, 2))
        else:
            ratio = 0.0
        line += f'\t{ratio}\n'
        f.write(line)
