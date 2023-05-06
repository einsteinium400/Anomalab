from math import sqrt

def EuclideanDistance(u, v, type_values, parameters):
    distance = 0.0
    results = []
    for i in range(len(u)):
        results.append((u[i] - v[i]) ** 2)
        distance += results[i]
    return sqrt(distance), results