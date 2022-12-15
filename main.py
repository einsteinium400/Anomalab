# todo: handle exception of "no centroid defined for empty cluster." which means one cluster is empty
# todo: make sure there are no duplicates in input -- I DON'T SEE PROBLEN IN IT
# todo: complete accuracy test
import csv

import numpy

from KMeanClusterer import *
from DistanceFunctions import *
from ClassIntegrator import *

# number of means.
K = 4   #todo: need to be defined by elbow algorithm
# name of unlabeled csv file
UNLABELED_FILE_NAME = "dataset1/lymphography.csv"   #todo: need to be find by DATA ANALYST
# name of labeled file name. label is last coloumn
LABLED_FILE_NAME = "dataset1/labeled_data.csv"  #todo: should be determant during running

# max value for each feature by index
MEAN_VALUES = [4, 2, 2, 2, 2, 2, 2, 2, 4, 4, 3, 4, 4, 8, 3, 2, 2, 8]    #todo: should be determent during running
# True means categorical value. False means numeric value.
TYPE_OF_FIELDS = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
                  True, True]   #todo: should be determant by the user


def csv_to_nested_list(file_name):
    with open(file_name, 'r') as read_obj:
        # Return a reader object which will
        # iterate over lines in the given csvfile
        csv_reader = csv.reader(read_obj)
        # convert string to list
        list_of_csv = list(csv_reader)
        new_lst = [[int(x) for x in inner] for inner in list_of_csv]
        return new_lst


# the label should be the last feature!
def test_accuracy(clusterer, unlabeled_data_file, labeled_data_file):
    unlabeled_samples = csv_to_nested_list(unlabeled_data_file)
    labeled_samples = csv_to_nested_list(labeled_data_file)
    print("stiff")
    print(unlabeled_samples)
    print(labeled_samples)
    algorithm_result = []
    for unlabeled_sample, labeled_sample in zip(unlabeled_samples, labeled_samples):
        vector = numpy.array(unlabeled_sample)
        result = clusterer.classify(vector)
        # append sample with the model result label
        unlabeled_sample.append(result)
        # append sample with actual label
        unlabeled_sample.append(labeled_sample[-1])
        algorithm_result.append(unlabeled_sample)
    # print(algorithm_result) #todo: מיכאל זו הרשימה שהאיבר האחרון זה הקטלוג האמיתי והאיבר לפני אחרון זה קטלוג מהמודל

    # this might be unnecessary
    # write labeled results in file
    myFile = open('output.csv', 'w')
    writer = csv.writer(myFile)
    for data_list in algorithm_result:
        writer.writerow(data_list)
    myFile.close()

    return algorithm_result


def main():
    vectors = [numpy.array(f) for f in csv_to_nested_list(UNLABELED_FILE_NAME)]
    print("vectors:", vectors)
    clusterer = KMeansClusterer(num_means=K, distance=hamming, repeats=3, mean_values=MEAN_VALUES,
                                type_of_fields=TYPE_OF_FIELDS)
    clusters = clusterer.cluster(vectors, True)
    print("Clustered:", vectors)
    print("As:", clusters)
    print("Means:", clusterer.means())

    result = test_accuracy(clusterer, UNLABELED_FILE_NAME, LABLED_FILE_NAME)

    classIntegrator(result)

    # classify a new vector
    # vector = numpy.array([3, 3])
    # print("classify(%s):" % vector, end=" ")
    # print(clusterer.classify(vector))
    print()


if __name__ == "__main__":
    main()
