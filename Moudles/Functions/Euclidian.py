import numpy
from math import sqrt
from Moudles.Functions.DistanceFunctions import DistanceFunction

def EuclideanDistance(u,v,type_values):
    diff = u - v
    return sqrt(numpy.dot(diff, diff))