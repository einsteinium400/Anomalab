from sklearn.metrics.pairwise import euclidean_distances


def pairwise_eucledean(vector1, vector2, j, k):
    distance = euclidean_distances([vector1], [vector2])[0][0]
    return distance, [0, 0]
