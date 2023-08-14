def EuclideanHamming(u, v, type_values, parameters):
    distance = 0.0
    results = []
    hammingResults = 0.0
    euclideanResults = 0.0
    for i in range(len(type_values)):
        if type_values[i]:
            if int(v[i]) != int(u[i]):
                results.append(1)
                hammingResults+=1
            else:
                results.append(0)
        else:
            x = u[i]-v[i]
            results.append(x)
            euclideanResults+=(x**2)
    distance = (euclideanResults**0.5)+hammingResults
    return distance, results
