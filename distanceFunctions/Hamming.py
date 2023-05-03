def Hamming(u,v,type_values, hyperparams):
    distance = 0
    for i in range(len(u)):
        if int(v[i]) != int(u[i]):
            distance += 1
    return distance
