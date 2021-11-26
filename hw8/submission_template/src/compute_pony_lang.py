import argparse
from pathlib import Path
import json
import math
from pprint import pprint

MAIN_CHARACTERS = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']


def tf(word, pony, word_count):
    return word_count[pony][word]


def idf(word, word_count):
    total_num = len(MAIN_CHARACTERS)
    num_use_word = 0
    for character in main_characters:
        if word in word_count[character]:
            num_use_word += 1
    return math.log2(total_num / num_use_word)


def compute_tfidf(word, character, word_count):
    return tf(word, character, word_count) * idf(word, word_count)


def start(word_count_file, number_of_words, main_characters):
    # read the json file
    score_dict = {}
    with open(word_count_file) as wcf:
        word_count = json.load(wcf)

    for character in main_characters:
        score_dict[character] = {}
        for word in word_count[character]:
            score_dict[character][word] = compute_tfidf(word, character, word_count)

    result_dict = {}
    for character in main_characters:
        words = score_dict[character].keys()
        words_sorted = sorted(words, key=lambda word: score_dict[character][word], reverse=True)
        result_dict[character] = words_sorted[:number_of_words]

    return result_dict


if __name__ == '__main__':

    parser = argparse.ArgumentParser('Compute pony langs')

    parser.add_argument('-c', type=str, help='Word counts in json')
    parser.add_argument('-n', type=str, help='Number of words')

    args = parser.parse_args()

    main_characters = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']

    if not args.c or not args.n:
        print('Please enter path to the word count file AND the number of words to show')
        print(parser.print_help())
        exit(1)

    word_counts = Path(args.c)
    number_of_words = int(args.n)

    pprint(start(word_counts, number_of_words, MAIN_CHARACTERS))
