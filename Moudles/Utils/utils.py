import csv
import random

def mean_generator(K, values):
    means = []
    for i in range(K):
        means.append([])
        for j in values:
            means[i].append(random.randint(1, j))
    return means


def csv_to_nested_list(file_name):
    with open(file_name, 'r') as read_obj:
        # Return a reader object which will
        # iterate over lines in the given csvfile
        csv_reader = csv.reader(read_obj)
        # convert string to list
        list_of_csv = list(csv_reader)
        new_lst = [[int(x) for x in inner] for inner in list_of_csv]
        return new_lst
