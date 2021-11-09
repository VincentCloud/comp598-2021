import json
import sys
from pathlib import Path


def compute_average_title_lengths(input_file_path):
    len_sum = 0
    with open(input_file_path) as f:
        jsons = f.readlines()

    for post in jsons:
        post = post.rstrip('\n')
        post_json = json.loads(post)
        len_sum += len(post_json['data']['title'])

    return len_sum / len(jsons)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Input file missing')
    else:
        try:
            input_file_path = Path(sys.argv[1])
            print(f'The average title length is {compute_average_title_lengths(input_file_path)}')
        except Exception as e:
            print(e)
