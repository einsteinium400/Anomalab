import json

import numpy as np

import model.utils as utils



class KMeansClusterer:

    def __init__(
            self,
            num_means,  # k value
            distance,  # distance function
            repeats=1,
            mean_values=None,
            conv_test=1e-6,  # threshold for converging
            type_of_fields=None,
            hyper_params=dict()):

        self._num_means = num_means
        self._distance = distance
        self._repeats = repeats
        self._mean_values = mean_values
        self._type_of_fields = type_of_fields
        self._means = None
        self._max_difference = conv_test
        self._wcss = None
        self._variance_list = []
        self._average_distance_list = []
        self._clusters_info = []
        self._model_json_info = 0
        self._hyper_parameters = hyper_params

    def createClusterJson(self):
        jsonData = {
            "wcss_score_of_model": self._wcss,
        }
        listObj = []
        for i in range(len(self._means)):
            # cluster_info_list = []
            # for item in self._clusters_info[i]:
            #     cluster_info_list.append(item.tolist())
            listObj.append(
                {
                    "cluster": i,
                    "average_cluster_distance": self._average_distance_list[i],
                    "variance": self._variance_list[i],
                    "mean": self._means[i].tolist(),
                    # "dataPoints":cluster_info_list
                }
            )
        jsonData['clusters_info'] = listObj
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

    def cluster(self, vectors):
        # self._hyper_parameters = preProcess(vectors, self._type_of_fields)
        # call abstract method to cluster the vectors
        self.cluster_vectorspace(vectors)

    # calculates the mean of a cluster
    def _centroid(self, cluster, mean):
        # initialize an empty list, with size of number of features

        if len(cluster):

            temp_centroid = [[] for columns in range(cluster[0].shape[0])]

            for sample in cluster:
                for j in range(len(temp_centroid)):
                    temp_centroid[j].append(sample[j])

            # temp_centroid.append(mean)

            # extract the most frequenct value in each index
            frequent_value_list = []
            for x in range(len(temp_centroid)):

                # if type if categorical, take the most frequent value.
                # if type is numerical, make avg
                if self._type_of_fields[x]:
                    frequent_value_list.append(max(set(temp_centroid[x]), key=temp_centroid[x].count))
                else:
                    frequent_value_list.append(sum(temp_centroid[x]) / len(temp_centroid[x]))

            centroid = np.array(frequent_value_list)
            return centroid

        else:
            print("bad seed")
            raise Exception("bad seed")  # todo: handle this with re-run

    def get_wcss(self):
        return self._wcss

    def get_variance(self):
        return self._variance_list

    def get_average_distance_list(self):
        return self._average_distance_list

    def get_means(self):
        return self._means

    def _wcss_calculate(self, clusters):
        wcss = 0
        for index in range(len(clusters)):
            for vec in clusters[index]:
                # wcss += self._distance.calculate(vec, self._means[index],self._type_of_fields) ** 2
                wcss += self._distance(vec, self._means[index], self._type_of_fields,self._hyper_parameters) ** 2

        self._wcss = wcss

    def _variance_average_calculate(self, clusters):

        self._average_distance_list = [[0] for _ in range(len(self._means))]
        self._variance_list = [[0] for _ in range(len(self._means))]

        # calculate average mean
        for index in range(len(clusters)):
            self._average_distance_list[index] = 0
            for vec in clusters[index]:
                # self._average_distance_list[index] += self._distance.calculate(vec, self._means[index],
                # self._type_of_fields)
                self._average_distance_list[index] += self._distance(vec, self._means[index], self._type_of_fields,self._hyper_parameters)
            self._average_distance_list[index] /= len(clusters[index])

        # calculate variance
        for index in range(len(clusters)):
            self._variance_list[index] = 0
            for vec in clusters[index]:
                # distance_of_element_from_mean = self._distance.calculate(vec, self._means[index],self._type_of_fields)
                distance_of_element_from_mean = self._distance(vec, self._means[index], self._type_of_fields,self._hyper_parameters)

                self._variance_list[index] += (distance_of_element_from_mean - self._average_distance_list[index]) ** 2
            self._variance_list[index] /= len(clusters[index])

    def _sum_distances(self, vectors1, vectors2):
        difference = 0.0
        for u, v in zip(vectors1, vectors2):
            # difference += self._distance.calculate(u, v,self._type_of_fields)
            difference += self._distance(u, v, self._type_of_fields,self._hyper_parameters)
        return difference

    # cluster the data given to kmeans
    def cluster_vectorspace(self, vectors):
        meanss = []

        # make _repeats repeats to get the best means
        for trial in range(self._repeats):
            # generate new means
            self._means = utils.mean_generator(self._num_means, vectors)

            # cluster the vectors to the given means
            self._cluster_vectorspace(vectors)

            # add the new means each time
            meanss.append(self._means)

        # at this point meanss holds an array of arrays, each array has k means in it.
        if len(meanss) > 1:
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

        if self._num_means < len(vectors):
            # perform k-means clustering
            converged = False
            while not converged:
                # assign the tokens to clusters based on minimum distance to
                # the cluster means
                clusters = [[] for m in range(self._num_means)]
                for vector in vectors:
                    index, distances = self.classify_vectorspace(vector)
                    clusters[index].append(vector)

                # recalculate cluster means by computing the centroid of each cluster
                new_means = list(map(self._centroid, clusters, self._means))

                # measure the degree of change from the previous step for convergence
                difference = self._sum_distances(self._means, new_means)
                # remember the new means

                self._means = new_means

                if difference < self._max_difference:
                    converged = True
                    # calculate wcss score
                    self._wcss_calculate(clusters)

                    # calculate variance and average distance
                    self._variance_average_calculate(clusters)
            self._clusters_info = clusters
            self.createClusterJson()
        else:
            pass  # todo: return error here

    def classify_vectorspace(self, vector):
        # finds the closest cluster centroid
        # returns that cluster's index
        best_distance = best_index = None
        distances = []
        for index in range(len(self._means)):
            mean = self._means[index]
            # dist = self._distance.calculate(vector, mean,self._type_of_fields)
            dist = self._distance(vector, mean, self._type_of_fields, self._hyper_parameters)
            cluster_info = {
                "cluster": index,
                "distance": dist
            }
            distances.append(cluster_info)
            if best_distance is None or dist < best_distance:
                best_index, best_distance = index, dist

        return best_index, distances
