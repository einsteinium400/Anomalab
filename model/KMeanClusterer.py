REPEATS_NUM = 5

import json
# import traceback
import numpy as np
import math
import model.utils as utils
from collections import Counter

MAX_ITERATION = 30


class KMeansClusterer:

    def __init__(
            self,
            num_means,  # k value
            distance,  # distance function
            repeats=REPEATS_NUM,
            mean_values=None,
            conv_test=1e-6,  # threshold for converging
            type_of_fields=None,
            repeats_method="best_wcss",
            hyper_params=dict()):
        self.repeats_method = repeats_method
        self._num_means = num_means
        self._distance = distance
        self._repeats = repeats
        self._mean_values = mean_values
        self._type_of_fields = type_of_fields
        self._means = None
        ##NOAM LINES FOR ANOMALIES
        self.clustersAverageDistance = None
        self.clustersStdDev = None
        self.clustersMaxDistances = None
        self.attributesAverageDistances = None
        self.attributesStdDevs = None

        self.silhouette = None
        self._max_difference = conv_test
        self._wcss = None
        self._normalized_wcss = None
        self._clusters_info = []
        self._model_json_info = 0
        self._hyper_parameters = hyper_params
        self._overall_mean = None
        self._overall_std = None

    def createClusterJson(self):
        jsonData = {
            "wcss": self._wcss,
            "silhouette": self.silhouette,
        }
        listObj = []
        for i in range(len(self._means)):
            listObj.append(
                {
                    "cluster": i,
                    "mean": self._means[i].tolist(),
                    "averageDistance": self.clustersAverageDistance[i],
                    "maxDistance": self.clustersMaxDistances[i],
                    "stdDev": self.clustersStdDev[i],
                    "attributesAverageDistances": self.attributesAverageDistances[i],
                    "attributesStdDevs": self.attributesStdDevs[i],
                }
            )
        jsonData['clusters_info'] = listObj
        jsonData['cluster_values'] = self._clusters_info
        jsonData['hyperParams'] = self._hyper_parameters
        self._model_json_info = jsonData

    def getModelData(self):
        return self._model_json_info

    def store_model(self, filename):
        jsonData = self.getModelData()

        with open(filename, 'w') as json_file:
            json.dump(jsonData, json_file,
                      indent=4,
                      separators=(',', ': '))

    # calculates the mean of a cluster
    def _centroid(self, cluster, mean):
        # initialize an empty list, with size of number of features
        if len(cluster):
            # temp_centroid = [[] for columns in range(cluster[0].shape[0])]
            # for sample in cluster:
            #     for j in range(len(temp_centroid)):
            #         temp_centroid[j].append(sample[j])
            # temp_centroid.append(mean)
            # extract the most frequenct value in each index
            frequent_value_list = []
            for ind in range(len(cluster[0])):
                # print("cluster is:", cluster)
                # if type if categorical, take the most frequent value.
                # if type is numerical, make avg
                if self._type_of_fields[ind]:
                    counter = Counter(arr[ind] for arr in cluster if len(arr) > ind)
                    frequent_value_list.append(counter.most_common(1)[0][0])

                    #l = max(Counter(cluster[ind]), key=lambda x: Counter(cluster[ind])[x])
                    #frequent_value_list.append(max(Counter(cluster[ind]), key=lambda x: Counter(cluster[ind])[x]))
                    # frequent_value_list.append(int(max(set(cluster[x]), key=cluster[x].count)))
                else:
                    frequent_value_list.append(np.mean([arr[ind] for arr in cluster], axis=0))

            centroid = np.array(frequent_value_list)
            #            print("new centroid is:", centroid)
            return centroid
        else:
           # print(cluster)
            raise Exception("bad seed")

    def get_means(self):
        return self._means

    def get_wcss(self):
        if self._wcss is None:
            self.wcssCalculate()
        return self._wcss

    def wcssCalculate(self):
        wcss = 0
        for i in range(len(self._clusters_info)):
            for vec in self._clusters_info[i]:
                distance, results = self._distance(list(vec), self._means[i], self._type_of_fields,
                                                   self._hyper_parameters)
                wcss += distance ** 2
        self._wcss = wcss

    def get_Silhouette(self):
        if self.silhouette is None:
            self.SilhouetteCalculate()
        return self.silhouette

    def SilhouetteCalculate(self):

        ##handling one cluster only
        if len(self._clusters_info) < 2:
            self.silhouette = 0
            return

        totalVectors = 0
        totalSilhouette = 0
        clustersRange = [*range(len(self._clusters_info))]
        ##count vectors
        for cluster in self._clusters_info:
            totalVectors += len(cluster)

        for index in range(len(self._clusters_info)):
            for vec in self._clusters_info[index]:
                ##silhouette
                sumInCluster = 0
                sumOutCluster = 0
                numOutCluster = 0

                ##calculate inner cluster distances (ai)
                for otherVector in self._clusters_info[index]:
                    distance, results = self._distance(vec, otherVector, self._type_of_fields, self._hyper_parameters)
                    sumInCluster += distance

                ##calculate outer clusters distances (bi)
                clustersRange.remove(index)
                for otherClusters in clustersRange:
                    for otherVector in self._clusters_info[otherClusters]:
                        distance, results = self._distance(vec, otherVector, self._type_of_fields,
                                                           self._hyper_parameters)
                        sumOutCluster += distance
                        numOutCluster += 1
                clustersRange.append(index)
                ##summarize silhouette
                ai = sumInCluster / len(self._clusters_info[index])
                bi = sumOutCluster / numOutCluster
                si = (bi - ai) / max(ai, bi)
                totalSilhouette += si

        self.silhouette = totalSilhouette / totalVectors

    def metaDataCalculation(self):
        numberOfFeatures = len(self._means[0])
        numberOfClusters = len(self._means)

        self.clustersAverageDistance = []
        self.clustersStdDev = []
        self.attributesStdDevs = [[] for _ in range(numberOfClusters)]
        self.attributesAverageDistances = [[] for _ in range(numberOfClusters)]
        self.clustersMaxDistances = []

        # calculate average
        for index in range(numberOfClusters):
            maxDistance = 0
            sumOfTotalDistance = 0
            sumOfAttributesDistances = [0 for _ in range(numberOfFeatures)]
            self.attributesAverageDistances[index] = [0 for _ in range(numberOfFeatures)]
            for vec in self._clusters_info[index]:
                ##check distance between vec in cluster with the cluster mean
                distance, results = self._distance(vec, self._means[index], self._type_of_fields,
                                                   self._hyper_parameters)
                ##check for max distance
                if distance > maxDistance:
                    maxDistance = distance
                ##sum total distance for average calculate
                sumOfTotalDistance += distance
                ##sum each distances for average calculate
                for i in range(numberOfFeatures):
                    sumOfAttributesDistances[i] += abs(results[i])
            self.clustersMaxDistances.append(maxDistance)
            self.clustersAverageDistance.append(sumOfTotalDistance / len(self._clusters_info[index]))
            for i in range(numberOfFeatures):
                self.attributesAverageDistances[index][i] = sumOfAttributesDistances[i] / len(
                    self._clusters_info[index])

        # calculate standard deviation
        for index in range(numberOfClusters):
            sumOfSquareDistances = 0
            squareDeltaDistances = [0 for _ in range(numberOfFeatures)]
            for vec in self._clusters_info[index]:
                distance, results = self._distance(vec, self._means[index], self._type_of_fields,
                                                   self._hyper_parameters)
                for i in range(numberOfFeatures):
                    squareDeltaDistances[i] += (results[i] - self.attributesAverageDistances[index][i]) ** 2
                sumOfSquareDistances += (distance - self.clustersAverageDistance[index]) ** 2
            ##deal with clusters with only one data sample
            if len(self._clusters_info[index]) < 2:
                self.clustersStdDev.append(0)
                for i in range(numberOfFeatures):
                    self.attributesStdDevs[index].append(0)
            else:
                self.clustersStdDev.append(math.sqrt(sumOfSquareDistances / (len(self._clusters_info[index]) - 1)))
                for i in range(numberOfFeatures):
                    self.attributesStdDevs[index].append(
                        math.sqrt(squareDeltaDistances[i] / (len(self._clusters_info[index]) - 1)))

    def _sum_distances(self, vectors1, vectors2):
        difference = 0.0
        for u, v in zip(vectors1, vectors2):
            distance, results = self._distance(u, v, self._type_of_fields, self._hyper_parameters)
            difference += distance
        return difference

    # cluster the data given to kmeans
    def cluster_vectorspace(self, vectors):
        meanss = []
        wcsss = []
        # make _repeats repeats to get the best means
        for trial in range(self._repeats):
         #   print("kmeans cluster_vectorspace, doing repeats", trial)
            # generate new means
            try:
                self._means = utils.mean_generator(self._num_means, vectors)
                # cluster the vectors to the given means
                try:
                    self._cluster_vectorspace(vectors)
                except Exception as e:
                    raise e
                # add the new means each time
                meanss.append(self._means)
                self.wcssCalculate()
                wcsss.append(self._wcss)
            except Exception as e:
                # print(e, ": ", trial)
                raise e
        # at this point meanss holds an array of arrays, each array has k means in it.
        if len(meanss) > 1:
            if self.repeats_method == "best_wcss":
                #print(wcsss)
                lowest_wcss = wcsss.index(min(wcsss, key=lambda x: x))
                self._wcss = wcsss[lowest_wcss]
                self._means = meanss[lowest_wcss]

            elif self.repeats_method == "minimal_difference":
                # find the set of means that's minimally different from the others
                min_difference = min_means = None
                for i in range(len(meanss)):
                    d = 0
                    for j in range(len(meanss)):
                        if i != j:
                            d += self._sum_distances(meanss[i], meanss[j])
                    if min_difference is None or d < min_difference:
                        min_difference, min_means = d, meanss[i]

                    # use the best means
                    self._means = min_means

    # cluster for specific mean values
    def _cluster_vectorspace(self, vectors):
        #print("in cluster vectorspace")
        if self._num_means < len(vectors):
            # max iteration if there is no conversion
            current_iteration = 0
            # perform k-means clustering
            converged = False
            while not converged:
                current_iteration += 1
                # assign the tokens to clusters based on minimum distance to
                # the cluster means

                clusters = [[] for m in range(self._num_means)]

                for vector in vectors:
                    index, distances = self.classify_vectorspace(vector)
                    clusters[index].append(vector.tolist())
                # for i in range(len(clusters)):
                # print("cluster is",len(clusters[i]))
                # print("generating new means")
                try:
                    new_means = list(map(self._centroid, clusters, self._means))
                except Exception as e:
                    # Propagate the exception from function c to function a
                    raise e
                # print("new means are:", new_means)
                # recalculate cluster means by computing the centroid of each cluster
                ###### new_means = list(map(self._centroid, clusters, self._means))

                # measure the degree of change from the previous step for convergence
                difference = self._sum_distances(self._means, new_means)
                # remember the new means

                self._means = new_means

                if difference < self._max_difference or current_iteration == MAX_ITERATION:
                    converged = True

            self._clusters_info = clusters
            # self.createClusterJson()
            # print ('cluster means: ', self._means)
        else:
            print("erorr!!!!")
            pass  # todo: return error here

    def classify_vectorspace(self, vector):
        # finds the closest cluster centroid
        # returns that cluster's index
        best_distance = best_index = None
        distances = []
        for index in range(len(self._means)):
            mean = self._means[index]
            distance, results = self._distance(vector, mean, self._type_of_fields, self._hyper_parameters)
            cluster_info = {
                "cluster": index,
                "distance": distance
            }
            distances.append(cluster_info)
            if best_distance is None or distance < best_distance:
                best_index, best_distance = index, distance

        return best_index, distances
