import json
import csv
import sys
import operator



def print_dict(dict):
    '''
    Function to print the dictionary in a json format
    :param dict: Dictionary file passed onto the function
    :return: prints the dictionary as a properly formatted json dump
    '''
    print(json.dumps(dict, indent=2, sort_keys=True))


def dictionary_sort(dict, reverse=True):
    sorted_dict = sorted(dict.items(), key = operator.itemgetter(1), reverse = reverse)
    return sorted_dict