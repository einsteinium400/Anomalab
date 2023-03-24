import csv
import random



def mean_generator(K, values):
    items = random.sample(list(values), K)
    listed_items = [list(arr) for arr in items]
    return listed_items

    # means = []
    # for i in range(K):
    #     means.append([])
    #     for j in values:
    #         means[i].append(random.randint(1, j))
    # print("inside mean generator")
    # print(means)
    # return means



def csv_to_nested_list(file_name):
    with open(file_name, 'r') as read_obj:
        # Return a reader object which will
        # iterate over lines in the given csvfile
        csv_reader = csv.reader(read_obj)
        # convert string to list
        list_of_csv = list(csv_reader)
        new_lst = [[int(x) for x in inner] for inner in list_of_csv]
        return new_lst
