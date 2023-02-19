import numpy
from math import sqrt
from Moudles.Functions.DistanceFunctions import DistanceFunction


class EuclideanDistance(DistanceFunction):
    def __init__(
            self,
            ):
            self._name = "Euclidean"
    def calculate(self,u, v, type_values):
        diff = u - v
        return sqrt(numpy.dot(diff, diff))