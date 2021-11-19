import json
import argparse
from random import shuffle
import pandas as pd


def select_from_json(json_file_path, num_of_posts):
    with open(json_file_path) as jf:
        jsons = jf.readlines()

    if num_of_posts > len(jsons):
        return jsons

    # shuffle the list and select num_of_posts
    jsons_copy = jsons.copy()
    shuffle(jsons_copy)
    return jsons_copy[:num_of_posts]  # return the first num_of_posts from the shuffled jsons


def parse_jsons_to_df(jsons):
    result_list = []
    for post in jsons:
        post = post.rstrip('\n')
        post_json = json.loads(post)
        name = post_json['data']['name']
        title = post_json['data']['title']
        coding = ''
        row = {
            'Name': name,
            'title': title,
            'coding': coding
        }
        result_list.append(row)
    result_df = pd.json_normalize(result_list)
    result_df.set_index('Name')
    return result_df


def start(json_file, num_posts, output_file):
    jsons = select_from_json(json_file, num_posts)
    result_df = parse_jsons_to_df(jsons)
    # write to tsv file
    result_df.to_csv(output_file, sep='\t', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Provide the name of the output file, name of the json file, and number of posts to extract')

    parser.add_argument('-o', type=str, help='The name of the output file')
    parser.add_argument('json_file', help='The name of the json file')
    parser.add_argument('num_posts_to_output')

    args = parser.parse_args()

    if not args.o or not args.json_file or not args.num_posts_to_output:
        raise parser.error('Invalid argument input')

    json_file_path = args.json_file
    num_of_posts = int(args.num_posts_to_output)
    output_path = args.o
    start(json_file_path, num_of_posts, output_path)
