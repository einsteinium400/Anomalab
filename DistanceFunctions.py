from math import sqrt
import numpy


def hamming(u, v):
    distance = 0
    for i in range(len(u)):
        if v[i] != u[i]:
            distance += 1
    return distance


def euclidean_distance(u, v):
    diff = u - v
    return sqrt(numpy.dot(diff, diff))
