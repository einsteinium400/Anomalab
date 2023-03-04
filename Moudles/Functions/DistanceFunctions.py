def Hamming(u,v,type_values):
        distance = 0
        for i in range(len(u)):
            if v[i] != u[i]:
                distance += 1
        return distance    



def MixedDistance(u, v, type_values):
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

