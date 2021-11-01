import argparse
import json
from datetime import datetime
import pytz
import sys


def load_data(input_file):
    with open(input_file, 'r') as input_f:
        dict_list = input_f.readlines()

    return dict_list


def filter_data(dict_list):
    # convert each string into a dictionary and preprocess
    json_list = []
    for json_str in dict_list:
        try:
            # 5
            data = json.loads(json_str)
        except json.decoder.JSONDecodeError as e:
            continue
        json_list.append(data)

    filtered_data = preprocess_data(json_list)
    return filtered_data


def preprocess_data(json_list):
    filtered_data = []
    for i, json_dict in enumerate(json_list):
        # address 1, 5, 6
        if not decide_membership_from_key(json_dict):
            continue
        if 'title_text' in json_dict:
            json_dict['title'] = json_dict['title_text']
            del json_dict['title_text']

        # standardize all createdAt date times to UTC timezone (3, 4)
        try:
            datetime_entry = datetime.strptime(json_dict['createdAt'], '%Y-%m-%dT%H:%M:%S%z')
            json_dict['createdAt'] = datetime_entry.astimezone(pytz.utc).isoformat()
        except ValueError:
            continue

        # cast float / str to int in total_count, if this key is not there skip this step 7, 8
        if 'total_count' in json_dict:
            try:
                json_dict['total_count'] = int(float(json_dict['total_count']))
            except ValueError:
                continue

        # split tags into individual words, if tag field is not present skip this step
        if 'tags' in json_dict:
            split_tags = []
            for tag in json_dict['tags']:
                split_tags += tag.split(' ')

            json_dict['tags'] = split_tags
        filtered_data.append(json_dict)
    return filtered_data


def decide_membership_from_key(json_dict):
    # 1,6
    return (('title' in json_dict) or ('title_text' in json_dict)) and ('author' in json_dict) and (
        json_dict['author']) and (json_dict['author'] != 'N/A') and 'createdAt' in json_dict


def write_to_file(filtered_data_list, output_path):
    output_str = ''
    for item in filtered_data_list:
        output_str += f'{item}\n'
    with open(output_path, 'w+') as f:
        f.write(output_str)
    return output_str


def pipeline(input_file, output_file):
    dict_list = load_data(input_file)
    filtered_data = filter_data(dict_list)
    return write_to_file(filtered_data, output_file)


def start():
    parser = argparse.ArgumentParser(description='clean the data')
    parser.add_argument('-i', type=str, help='Path to input file')
    parser.add_argument('-o', type=str, help='Path to output file')

    args = parser.parse_args()

    if not args.i or not args.o:
        raise parser.error('No input file or output file specified')

    input_path = args.i
    output_path = args.o
    return pipeline(input_path, output_path)


if __name__ == '__main__':
    try:
        start()
    except Exception as e:
        print(e, file=sys.stderr)
