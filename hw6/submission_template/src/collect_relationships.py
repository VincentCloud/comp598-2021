import json
from pathlib import Path
import argparse
import hashlib
import bs4
import requests

BASE_URL = 'https://www.whosdatedwho.com/dating'


def read_config(config_file_path):
    with open(Path(f'{config_file_path}')) as config:
        config_json = json.load(config)

    return config_json['cache_dir'], config_json['target_people']


def fetch_content(cache_dir, target_person):
    print(f'target person: {target_person}')
    url = f'{BASE_URL}/{target_person}'
    file_name = f'{hashlib.sha1(url.encode("UTF-8")).hexdigest()}'
    if Path(f'{cache_dir}/{file_name}').exists():
        print('load from cache')
        with open(Path(f'{cache_dir}/{file_name}')) as target_person_file:
            soup = bs4.BeautifulSoup(target_person_file, 'html.parser')
    else:
        print('downloading...')
        with open(Path(f'{cache_dir}/{file_name}'), 'w+') as target_person_file:
            content = requests.get(url).content.decode('utf-8')
            soup = bs4.BeautifulSoup(content, 'html.parser')
            target_person_file.write(content)
    return soup


def get_dating_history(soup):
    history_soup = soup.find('div', {'id': 'ff-dating-history-grid'}).findChildren('div', {'class': 'ff-grid-box'}, recursive=False)
    history = []
    for person in history_soup:
        history.append('-'.join(person.get('id').split('-')[1:]))
    return history


def start(config_path, output_path):
    cache_dir, target_people = read_config(config_path)
    output_dict = {}
    for person in target_people:
        soup = fetch_content(cache_dir, person)
        history = get_dating_history(soup)
        output_dict[person] = history
    with open(Path(output_path), 'w+') as output_file:
        json.dump(output_dict, output_file, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Provide configuration file and output file')

    parser.add_argument('-c', type=str, help='path to the configuration file')
    parser.add_argument('-o', type=str, help='path to the output file')

    args = parser.parse_args()

    if not args.c or not args.o:
        raise parser.error('No configuration file given or not output file specified')

    config_path = args.c
    output_path = args.o
    start(config_path, output_path)
