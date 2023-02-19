from matplotlib import pyplot as plt

from Moudles.Clustring.KMeanClusterer import KMeansClusterer
from Moudles.Functions.DistanceFunctions import *
from Moudles.Functions.Hamming import Hamming
from Moudles.Functions.MixedDistance import MixedDistance
from Moudles.Functions.Euclidian import EuclideanDistance
from Moudles.Utils.utils import *
from Moudles.Clustring.Elbow import elbow_method
from Moudles.Utils.LoadUtils import loadItemFromJson
from Moudles.Anomaly.AnomalyPredict import *

# name of labeled file name. label is last coloumn
LABLED_FILE_NAME = "dataset1/labeled_data.csv"  #todo: should be determant during running

# max value for each feature by index
CATEGORICAL_DATA_MEAN_VALUES = [4, 2, 2, 2, 2, 2, 2, 2, 4, 4, 3, 4, 4, 8, 3, 2, 2, 8, 4]
MIXED_DATA_MEAN_VALUES = [15, 4, 2, 2, 2, 2, 2, 2, 2, 4, 4, 3, 4, 4, 8, 3, 2, 2, 8, 4]

# True means categorical value. False means numeric value.
CATEGORIC_DATA_TYPE_OF_FIELDS = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
                                 True, True, True]

MIXED_DATA_TYPE_OF_FIELDS = [False,True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
                                 True, True, True]

categoric_data = [numpy.array(f) for f in csv_to_nested_list("dataset1\labeled_data.csv")]
mixed_data = [numpy.array(f) for f in csv_to_nested_list("dataset1\labeled_data_numeric.csv")]

# Cluster 1
mixed = MixedDistance()

# check elbow for mixed data
k=elbow_method(mixed,mixed_data,MIXED_DATA_MEAN_VALUES,MIXED_DATA_TYPE_OF_FIELDS)

clusterer = KMeansClusterer(num_means=k, distance=mixed, repeats=9, mean_values=MIXED_DATA_MEAN_VALUES,
                            type_of_fields=MIXED_DATA_TYPE_OF_FIELDS)
clusterer.cluster(mixed_data)
clusterer.store_model("MixedCluster.json")


# Cluster 2
hammingFunc = Hamming()
clusterer2 = KMeansClusterer(num_means=k, distance=hammingFunc, repeats=9, mean_values=MIXED_DATA_MEAN_VALUES,
                            type_of_fields=MIXED_DATA_TYPE_OF_FIELDS)
clusterer2.cluster(mixed_data)
clusterer2.store_model("HammingCluster.json")

# Sample Load
sample1 = loadItemFromJson('dataSample-1.json')
sample2 = loadItemFromJson('dataSample-2.json')


## POC ## Sample Checks
print("Cluster 1: Distance Function: ", clusterer._distance.getName())
print("Sample 1:")
if(checkSampleForAnomaly(clusterer,sample1)):
    print("Cluster 1 Sample 1: Anomaly Detected")

else:
    print("Cluster 1 Sample 1: Regular data")

print("Sample 2:")
if(checkSampleForAnomaly(clusterer,sample2)):
    print("Cluster 1 Sample 2: Anomaly Detected")
else:
    print("Cluster 1 Sample 2: Regular data")

print ("##################################################")
print("Cluster 2: Distance Function: ", clusterer2._distance.getName())
print("Sample 1:")
if(checkSampleForAnomaly(clusterer2,sample1)):
    print("Cluster 2 Sample 1: Anomaly Detected")
else:
    print("Cluster 2 Sample 1: Regular data")
    
print("Sample 2:")
if(checkSampleForAnomaly(clusterer2,sample2)):
    print("Cluster 2 Sample 2: Anomaly Detected")

else:
    print("Cluster 2 Sample 2: Regular data")



