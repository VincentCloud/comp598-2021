import argparse
from collections import defaultdict
from pprint import pprint

import pandas as pd
from pathlib import Path
import json


def analyze(coded_file_input, output_file):
    result = defaultdict(lambda: 0)

    # read the input file
    df = pd.read_csv(coded_file_input, sep='\t')
    annotations = df['coding']
    entry_dict = {
        'c': 'course-related',
        'f': 'food-related',
        'r': 'residence-related',
        'o': 'other'
    }
    for annotation in annotations:
        result[entry_dict[annotation]] += 1

    if output_file:
        print('writing')
        with open(Path(output_file), 'w+') as f:
            json.dump(result, f)
    else:
        pprint(dict(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Provide the name of the coded_file.tsv')
    parser.add_argument('-i', type=str, help='The name of the coded file input')
    parser.add_argument('-o', type=str, help='The name of the output file', required=False)

    args = parser.parse_args()

    if not args.i:
        raise parser.error('The coded file name required')

    coded_file_input = args.i
    output_file = args.o if args.o else ''

    analyze(coded_file_input, output_file)
