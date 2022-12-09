import csv

import numpy

vectors = [numpy.array(f) for f in [[2, 1], [1, 3], [4, 7], [6, 7]]]
print(vectors)
print(type(vectors))
print(vectors[1])
print(type(vectors[1]))
with open('dataset1/lymphography.csv', 'r') as read_obj:
    # Return a reader object which will
    # iterate over lines in the given csvfile
    csv_reader = csv.reader(read_obj)

    # convert string to list
    list_of_csv = list(csv_reader)

    print(list_of_csv)

    new_lst = [[int(x) for x in inner] for inner in list_of_csv]
    print(new_lst)

# def csv_to_numpy():
#     return numpy.loadtxt('dataset1/lymphography.csv', delimiter=',')
#
#
#
#
# a = csv_to_numpy()
# b=map(zip, a)
# print("b", b)
# print(b[1])
# print(csv_to_numpy())
# print(type(csv_to_numpy()))
