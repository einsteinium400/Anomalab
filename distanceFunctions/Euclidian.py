def Euclidean(u, v, type_values, parameters):
    distance = 0.0
    results = []
    for i in range(len(type_values)):
        if type_values[i]:
            raise "EUCLIDEAN DON'T KNOW TO HANDLE CATEGORIC DATA"
        results.append(u[i] - v[i])
        distance += (u[i] - v[i])**2
    return distance**0.5, results