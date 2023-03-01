import numpy
from math import sqrt

def EuclideanDistance(u,v,type_values):
    diff = u - v
    return sqrt(numpy.dot(diff, diff))