import json
import argparse
import pandas as pd
from collections import defaultdict


def find_top_characters(df, top_num=101):
    occ_dict = defaultdict(lambda: 0)
    for pony in df['pony'].tolist():
        if valid_pony(pony):
            occ_dict[pony] += 1
    return sorted(occ_dict.keys(), key=lambda k: occ_dict[k], reverse=True)[:top_num]


def valid_pony(pony):
    return not ('others' in pony.split(' ') or 'ponies' in pony.split(' ') or 'and' in pony.split(' ') or 'all' in pony.split(' '))


def divide_into_episodes(df):
    curr_title = df['title'][0]
    ponies_by_episode = []
    ponies_in_one_episode = []
    for i, title in enumerate(df['title']):
        if title != curr_title:
            curr_title = title
            ponies_by_episode.append(ponies_in_one_episode)
            ponies_in_one_episode = [df['pony'][i]]
        else:
            ponies_in_one_episode.append(df['pony'][i])

    if ponies_in_one_episode:
        ponies_by_episode.append(ponies_in_one_episode)

    return ponies_by_episode


def calculate_conversations(top_characters, ponies_by_episode):
    conversation_dict = defaultdict(lambda: defaultdict(lambda: 0))
    for ponies_in_one_episode in ponies_by_episode:
        for i in range(len(ponies_in_one_episode)):
            from_c = ponies_in_one_episode[i]
            to_c = ponies_in_one_episode[i + 1] if i + 1 < len(ponies_in_one_episode) else 'null'
            if valid_pony(from_c) and from_c in top_characters and (
              to_c in top_characters) and from_c != to_c:
                conversation_dict[from_c][to_c] += 1
                conversation_dict[to_c][from_c] += 1
    return conversation_dict


def start(input_file, output_file):
    # read the data
    df = pd.read_csv(input_file)
    df['pony'] = df['pony'].str.lower()
    # Iterate through the column and find the top 100 most occurring characters without the listed words
    top_characters = find_top_characters(df)
    # Divide the dataframe into episodes
    ponies_by_episode = divide_into_episodes(df)
    # For each episode, calculate the conversations
    conversation_dict = calculate_conversations(top_characters, ponies_by_episode)

    with open(output_file, 'w+') as jf:
        json.dump(conversation_dict, jf, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Build Interaction Network')

    parser.add_argument('-o', type=str, help='The path to the output file')
    parser.add_argument('-i', type=str, help='The path to the input dataset')
    args = parser.parse_args()
    if not args.o or not args.i:
        parser.print_help()
        exit(1)

    input_file = args.i
    output_file = args.o
    start(input_file, output_file)
