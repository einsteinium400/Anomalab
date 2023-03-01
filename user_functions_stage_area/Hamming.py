from Moudles.Functions.DistanceFunctions import DistanceFunction


def Hamming(u,v,type_values):
        distance = 0
        for i in range(len(u)):
            if v[i] != u[i]:
                distance += 1
        return distance    
