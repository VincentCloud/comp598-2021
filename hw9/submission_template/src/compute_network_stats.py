import json
import argparse
from collections import defaultdict
from operator import itemgetter
import networkx as nx


def calculate_most_connected_by_num(graph_dict, top_num=3):
    num_edges_dict = defaultdict(lambda: 0)
    for character in graph_dict:
        num_edges_dict[character] = len(graph_dict[character])
    return sorted(num_edges_dict.keys(), key=lambda k: num_edges_dict[k], reverse=True)[:top_num]


def calculate_most_connected_by_weight(graph_dict, top_num=3):
    weight_dict = defaultdict(lambda: 0)
    for character in graph_dict:
        for to_c in graph_dict[character]:
            weight_dict[character] += graph_dict[character][to_c]

    top_three = sorted(weight_dict.keys(), key=lambda k: weight_dict[k], reverse=True)[:top_num]

    print(itemgetter(*top_three)(weight_dict))

    return sorted(weight_dict.keys(), key=lambda k: weight_dict[k], reverse=True)[:top_num]


def calculate_betweenness(graph_dict, top_num=3):
    G = nx.Graph()
    for character in graph_dict:
        for to_c in graph_dict[character]:
            G.add_edge(character, to_c, weight=graph_dict[character][to_c])

    top_betweenness = sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)[:top_num]
    print(top_betweenness)

    return top_betweenness


def start(input_file, output_file):
    with open(input_file) as jf:
        graph_dict = json.load(jf)

    result_dict = {}

    most_connected_by_num = calculate_most_connected_by_num(graph_dict)
    most_connected_by_weight = calculate_most_connected_by_weight(graph_dict)
    most_betweenness = calculate_betweenness(graph_dict)

    result_dict['most_connected_by_num'] = most_connected_by_num
    result_dict['most_connected_by_weight'] = most_connected_by_weight
    result_dict['most_central_by_betweenness'] = most_betweenness

    with open(output_file, 'w+') as jf:
        json.dump(result_dict, jf, indent=4)
    return result_dict


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
