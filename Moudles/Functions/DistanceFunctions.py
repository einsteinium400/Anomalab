from math import sqrt
import numpy
from abc import ABC, abstractmethod

class DistanceFunction:
    def __init__(
            self,
            name  # Function name
            ):
            self._name = name
    @abstractmethod
    def calculate(self,u, v, type_values):
        pass

    def getName(self):
        return self._name

    def __str__(self):
        return f"The Function name is {self._name}"

def hamming(u, v, type_values):
    distance = 0
    for i in range(len(u)):
        if v[i] != u[i]:
            distance += 1
    return distance


def euclidean_distance(u, v, type_values):
    diff = u - v
    return sqrt(numpy.dot(diff, diff))


def mixed_distance(u, v, type_values):
    distance = 0

    for i in range(len(u)):
        # if type is categorical
        if type_values[i]:
            if v[i] != u[i]:
                distance += 1
        # if type is numeric
        else:
            distance += abs(u[i] - v[i])

    return distance
