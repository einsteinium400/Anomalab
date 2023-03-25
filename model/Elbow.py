import matplotlib.pyplot as plt
from model.KMeanClusterer import KMeansClusterer

import numpy as np

def elbow_method(distance, data, mean_values, type_of_fields):
    # elbow method
    wcss = []
    for k in range(1, 6):
        clusterer = KMeansClusterer(num_means=k, distance=distance, repeats=9, mean_values=mean_values,
                                    type_of_fields=type_of_fields)
        clusterer.cluster(data)
        # print(clusterer.get_wcss())
        # print(clusterer.get_means())
        # print(clusterer.get_variance())
        # print(clusterer.get_average_distance_list())
        wcss.append(clusterer.get_wcss())

    # plotting the points
    plt.plot(range(1, len(wcss) + 1), wcss)
    plt.xlabel('x axis-wcss')
    plt.ylabel('y axis - k')
    plt.title('wcss vals')
    # plt.show() # if you wanna see the graph remove this comment...

    # todo: return the optimal k value

    return 3
