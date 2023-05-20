def MixedDistance(u, v, type_values, parameters):
    distance = 0
    results = []
    for i in range(len(u)):
        # if type is categorical
        if type_values[i]:
            if v[i] != u[i]:
                distance += 1
                results.append(1)
        # if type is numeric
        else:
            distance += (u[i] - v[i]) ** 2
            results.append(u[i] - v[i])
            # distance += abs(u[i] - v[i])

    return distance, results
