# Natural Language Toolkit: K-Means Clusterer
#
# Copyright (C) 2001-2022 NLTK Project
# Author: Trevor Cohn <tacohn@cs.mu.oz.au>
# URL: <https://www.nltk.org/>
# For license information, see LICENSE.TXT

# todo: handle exception of "no centroid defined for empty cluster." which means one cluster is empty
import csv

import numpy
import pandas as pd
from math import sqrt
from KMeanClusterer import *

K = 3  # number of means
ITERATIONS = 10  # number of iterations for kmeans
FILE_NAME = "dataset1/lymphography.csv"  # name of csv file


def csv_to_numpy(file_name):
    with open(file_name, 'r') as read_obj:
        # Return a reader object which will
        # iterate over lines in the given csvfile
        csv_reader = csv.reader(read_obj)
        # convert string to list
        list_of_csv = list(csv_reader)
        new_lst = [[int(x) for x in inner] for inner in list_of_csv]
        return new_lst

# distance function
def hamming(vec1, vec2):
    pass


def euclidean_distance(u, v):
    """
    Returns the euclidean distance between vectors u and v. This is equivalent
    to the length of the vector (u - v).
    """
    diff = u - v
    return sqrt(numpy.dot(diff, diff))


#################################################################################

def demo():
    means = [[3, 3], [1, 2], [4, 2]]  # todo: correlated to k, choose randomly from the list.
    vectors = [numpy.array(f) for f in [[3, 3], [1, 2], [4, 2], [4, 0], [2, 3], [3, 1]]]

    print("vectors:", vectors)
    clusterer = KMeansClusterer(K, euclidean_distance, repeats=ITERATIONS, initial_means=means)
    clusters = clusterer.cluster(vectors, True)
    print("Clustered:", vectors)
    print("As:", clusters)
    print("Means:", clusterer.means())
    print()

    # classify a new vector
    vector = numpy.array([3, 3])
    print("classify(%s):" % vector, end=" ")
    print(clusterer.classify(vector))
    print()


if __name__ == "__main__":
    demo()
