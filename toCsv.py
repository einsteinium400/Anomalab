

import csv
def csv_to_numpy(file_name):
    with open(file_name, 'r') as read_obj:
        # Return a reader object which will
        # iterate over lines in the given csvfile
        csv_reader = csv.reader(read_obj)
        # convert string to list
        list_of_csv = list(csv_reader)
        new_lst = [[int(x) for x in inner] for inner in list_of_csv]
        return new_lst



unlabeled_samples = csv_to_numpy("dataset1/something.csv")
labeled_samples = csv_to_numpy("dataset1/lymphography.csv")

algorithm_result = []
for (u,v) in zip(unlabeled_samples,labeled_samples):
    print(u)
    print(v)