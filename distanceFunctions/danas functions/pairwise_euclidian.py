from sklearn.metrics.pairwise import euclidean_distances


def pairwise_eucledean(vector1, vector2, j, k):
    distance = euclidean_distances([vector1], [vector2])
    print ('vector1:',vector1)
    print ('vector2:',vector2)
    print ('distance:',distance)
    results = []
    for i in range(len(vector1)):
        results.append(0)
    return distance, results
