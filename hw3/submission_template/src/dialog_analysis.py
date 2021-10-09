import pandas as pd
import numpy as np
import json
from collections import defaultdict
import sys

output_file, input_file = sys.argv[2], sys.argv[3]

DATA_PATH = input_file
OUTPUT_PATH = output_file
json_dict = {'count': defaultdict(lambda: 0), 'verbosity': {}}
main_characters = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']

df = pd.read_csv(DATA_PATH)
df['pony'] = df['pony'].str.lower()
value_c_dict = df['pony'].value_counts().to_dict()

# for each value in the value dictionary, check if each character is included in the dictionary, if so increment the count of that character by 1. We have to check each main character because there might be more than 1 spearking.
for key in value_c_dict:
  # result = contain_one_character(key, main_characters)
  # if result[0]:
  if key in main_characters:
    json_dict['count'][key] += value_c_dict[key]

for character in main_characters:
  json_dict['verbosity'][character] = round(json_dict['count'][character] / df.shape[0], 2)

with open(OUTPUT_PATH, 'w+') as output_file:
  json_object = json.dump(json_dict, output_file, indent=4)

