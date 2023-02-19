from Moudles.Functions.DistanceFunctions import DistanceFunction


class Hamming(DistanceFunction):
    def __init__(
            self,
            ):
            self._name = "Hamming"
    def calculate(self,u, v, type_values):
        distance = 0
        for i in range(len(u)):
            if v[i] != u[i]:
                distance += 1
        return distance