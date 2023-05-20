def Hamming(u,v,type_values, hyperparams):
    distance = 0
    results = []
    for i in range(len(u)):
        if int(v[i]) != int(u[i]):
            results.append(1)
            distance += 1
        else:
            results.append(0)
    return distance,results
