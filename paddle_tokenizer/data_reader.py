from tokenizer_tools.conll.reader import read_conll


def parse_fn(word_tag_pairs, vocabulary, tag_vocabulary):
    words = [vocabulary[i[0]] for i in word_tag_pairs]
    tags = [tag_vocabulary[i[1]] for i in word_tag_pairs]

    return words, tags


def read_vocabulary(vocabulary_file):
    vocabulary = {}
    with open(vocabulary_file) as fd:
        for line in fd:
            word = line.strip()
            vocabulary[word] = len(vocabulary)

    return vocabulary


def generator_fn(input_file, vocabulary_file, tag_file):
    vocabulary = read_vocabulary(vocabulary_file)
    tag = read_vocabulary(tag_file)

    sentence_list = read_conll(input_file, sep=None)
    for sentence in sentence_list:
        word_tag_pairs = [(i[0], i[1]) for i in sentence]

        yield parse_fn(word_tag_pairs, vocabulary, tag)


if __name__ == "__main__":
    for i, j in enumerate(
        generator_fn("data/train.txt", "data/unicode_char_list.txt", "data/tags.txt")
    ):
        if i < 20:
            print(j)
        else:
            break
