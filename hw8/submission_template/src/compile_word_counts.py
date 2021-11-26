import pandas as pd
import argparse
from pathlib import Path
from collections import Counter
import json

STOP_WORDS_PATH = Path('data/stopwords.txt')
MAIN_CHARACTERS = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']
PUNCTUATIONS = '()[],-.?!:;#&'


def start(dialog_path, output_path, main_characters, stopwords, threshold=5):
    # read the dialog file
    df = pd.read_csv(dialog_path)
    count_dict = {}
    result_dict = {}
    counts = Counter()

    df['pony'] = df['pony'].str.lower()

    for character in main_characters:
        count_dict[character] = {}
        acts = df[df['pony'] == character]['dialog'].str.lower()  # get all the acts from that character

        all_words = ' '.join(acts.tolist())  # get all words in a single string
        translator = str.maketrans(PUNCTUATIONS, ' ' * len(PUNCTUATIONS))
        all_words = all_words.translate(translator)

        preprocessed_words = [word for word in all_words.split(' ') if word not in stopwords and word.isalpha()]
        count_dict[character] = Counter(preprocessed_words)
        counts += count_dict[character]

    # keep the entries that has values more than threshold
    for character in main_characters:
        result_dict[character] = {}
        for key in count_dict[character]:
            if counts[key] >= threshold:
                result_dict[character][key] = count_dict[character][key]

    with open(output_path, 'w+') as out:
        json.dump(result_dict, out, indent=4)

    return result_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Count Words')

    parser.add_argument('-o', type=str, help='Specify the absolute path to the output file')
    parser.add_argument('-d', type=str, help='Specify the absolute path to the clean dialog')

    args = parser.parse_args()

    if not args.o or not args.d:
        print('Please Specify the paths for output and dialog file')
        print(parser.print_help())
        exit(1)

    dialog_path = Path(args.d)
    output_path = Path(args.o)

    with open(STOP_WORDS_PATH) as stopf:
        stopwords = stopf.readlines()
        stopwords = [stopword[:-1] for stopword in stopwords]

    start(dialog_path, output_path, MAIN_CHARACTERS, stopwords)
