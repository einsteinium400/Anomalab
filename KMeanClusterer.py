from nltk.cluster.util import VectorSpaceClusterer

import copy
import random
import sys
import numpy as np


def mean_generator(K, values):
    means = []
    for i in range(K):
        means.append([])
        for j in values:
            means[i].append(random.randint(1, j))
    return means


class KMeansClusterer(VectorSpaceClusterer):
    """
    The K-means clusterer starts with k arbitrary chosen means then allocates
    each vector to the cluster with the closest mean. It then recalculates the
    means of each cluster as the centroid of the vectors in the cluster. This
    process repeats until the cluster memberships stabilise. This is a
    hill-climbing algorithm which may converge to a local maximum. Hence the
    clustering is often repeated with random initial means and the most
    commonly occurring output means are chosen.
    """

    def __init__(
            self,
            num_means,
            distance,
            repeats=1,
            conv_test=1e-6,
            initial_means=None,
            normalise=False,
            svd_dimensions=None,
            rng=None,
            mean_values=None,
            type_of_fields=None,
            #   avoid_empty_clusters=False,
    ):

        """
        :param  num_means:  the number of means to use (may use fewer)
        :type   num_means:  int
        :param  distance:   measure of distance between two vectors
        :type   distance:   function taking two vectors and returning a float
        :param  repeats:    number of randomised clustering trials to use
        :type   repeats:    int
        :param  conv_test:  maximum variation in mean differences before
                            deemed convergent
        :type   conv_test:  number
        :param  initial_means: set of k initial means
        :type   initial_means: sequence of vectors
        :param  normalise:  should vectors be normalised to length 1
        :type   normalise:  boolean
        :param svd_dimensions: number of dimensions to use in reducing vector
                               dimensionsionality with SVD
        :type svd_dimensions: int
        :param  rng:        random number generator (or None)
        :type   rng:        Random
        :param avoid_empty_clusters: include current centroid in computation
                                     of next one; avoids undefined behavior
                                     when clusters become empty
        :type avoid_empty_clusters: boolean
        """
        VectorSpaceClusterer.__init__(self, normalise, svd_dimensions)
        self._num_means = num_means
        self._distance = distance
        self._max_difference = conv_test
        assert not initial_means or len(initial_means) == num_means
        self._means = initial_means
        assert repeats >= 1
        assert not (initial_means and repeats > 1)
        self._repeats = repeats
        self.mean_values = mean_values
        self.type_of_fields = type_of_fields

    #        self._avoid_empty_clusters = avoid_empty_clusters

    def cluster_vectorspace(self, vectors, trace=False):
        if self._means and self._repeats > 1:
            print("Warning: means will be discarded for subsequent trials")

        meanss = []
        for trial in range(self._repeats):
            if trace:
                print("k-means trial", trial)
            if not self._means or trial > 1:
                self._means = mean_generator(self._num_means,
                                             self.mean_values)
                print("means are:", self._means)
            self._cluster_vectorspace(vectors, trace)
            meanss.append(self._means)

        if len(meanss) > 1:
            # sort the means first (so that different cluster numbering won't
            # effect the distance comparison)
            for means in meanss:
                means.sort(key=sum)

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

    def _cluster_vectorspace(self, vectors, trace=False):
        if self._num_means < len(vectors):
            # perform k-means clustering
            converged = False
            while not converged:
                # assign the tokens to clusters based on minimum distance to
                # the cluster means
                clusters = [[] for m in range(self._num_means)]
                for vector in vectors:
                    index = self.classify_vectorspace(vector)
                    clusters[index].append(vector)

                if trace:
                    print("iteration")

                # recalculate cluster means by computing the centroid of each cluster
                new_means = list(map(self._centroid, clusters, self._means))

                # measure the degree of change from the previous step for convergence
                difference = self._sum_distances(self._means, new_means)
                if difference < self._max_difference:
                    converged = True

                # remember the new means
                self._means = new_means

    def classify_vectorspace(self, vector):
        # finds the closest cluster centroid
        # returns that cluster's index
        best_distance = best_index = None
        for index in range(len(self._means)):
            mean = self._means[index]
            dist = self._distance(vector, mean)
            if best_distance is None or dist < best_distance:
                best_index, best_distance = index, dist
        return best_index

    def num_clusters(self):
        if self._means:
            return len(self._means)
        else:
            return self._num_means

    def means(self):
        """
        The means used for clustering.
        """
        return self._means

    def _sum_distances(self, vectors1, vectors2):
        difference = 0.0
        for u, v in zip(vectors1, vectors2):
            difference += self._distance(u, v)
        return difference

    def _centroid(self, cluster, mean):
        # initialize an empty list, with size of number of features
        if len(cluster):
            temp_centroid = [[] for columns in range(cluster[0].shape[0])]
            for sample in cluster:
                for j in range(len(temp_centroid)):
                    temp_centroid[j].append(sample[j])

            # extract the most frequenct value in each index
            frequent_value_list = []
            for x in range(len(temp_centroid)):
                if self.type_of_fields[x]:
                    frequent_value_list.append(max(set(temp_centroid[x]), key=temp_centroid[x].count))
                else:
                    frequent_value_list.append(sum(temp_centroid[x])/len(temp_centroid[x]))

            centroid = np.array(frequent_value_list)
            return centroid

        else:
            print("bad seed") #todo: handle this with re-run
            exit()
        # todo: cluster is empty and needs to re-run. handle this in code
        if not len(cluster):
            sys.stderr.write("Error: no centroid defined for empty cluster.\n")
            sys.stderr.write(
                "Try setting argument 'avoid_empty_clusters' to True\n"
            )
            assert False

    def __repr__(self):
        return "<KMeansClusterer means=%s repeats=%d>" % (self._means, self._repeats)
