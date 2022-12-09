# Natural Language Toolkit: K-Means Clusterer
#
# Copyright (C) 2001-2022 NLTK Project
# Author: Trevor Cohn <tacohn@cs.mu.oz.au>
# URL: <https://www.nltk.org/>
# For license information, see LICENSE.TXT

import numpy
import pandas as pd
from math import sqrt
from KMeanClusterer import *

K = 3  # number of means
iterations=10 #number of iterations for kmeans

#################################################################################

def csv_to_numpy(file_name):
    return pd.read_csv(file_name, header=None).values


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
    # example from figure 14.9, page 517, Manning and Schutze

    # from nltk.cluster import KMeansClusterer, euclidean_distance

    #vectors is a list of numpy arrays
    vectors = [numpy.array(f) for f in [[2, 1], [1, 3], [4, 7], [6, 7]]]

    means = [[4, 3], [5, 5], [4, 5]]  # todo: correlated to k, choose randomly from the list.

    clusterer = KMeansClusterer(K, euclidean_distance, initial_means=means)

    clusters = clusterer.cluster(vectors, True, trace=True)

    print("Clustered:", vectors)
    print("As:", clusters)
    print("Means:", clusterer.means())
    print()


    vectors = [numpy.array(f) for f in [[3, 3], [1, 2], [4, 2], [4, 0], [2, 3], [3, 1]]]



    print("vectors:", vectors)
    # test k-means using the euclidean distance metric, 2 means and repeat
    # clustering 10 times with random seeds

    clusterer = KMeansClusterer(K, euclidean_distance, repeats=iterations)
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
