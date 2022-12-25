from matplotlib import pyplot as plt

from Moudles.Clustring.KMeanClusterer import KMeansClusterer
from Moudles.Functions.DistanceFunctions import *
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

# check elbow for mixed data
k=elbow_method(mixed_distance,mixed_data,MIXED_DATA_MEAN_VALUES,MIXED_DATA_TYPE_OF_FIELDS)

clusterer = KMeansClusterer(num_means=k, distance=mixed_distance, repeats=9, mean_values=MIXED_DATA_MEAN_VALUES,
                            type_of_fields=MIXED_DATA_TYPE_OF_FIELDS)
clusterer.cluster(mixed_data)
clusterer.store_model("storage.json")


clusterer2 = KMeansClusterer(num_means=k, distance=hamming, repeats=9, mean_values=MIXED_DATA_MEAN_VALUES,
                            type_of_fields=MIXED_DATA_TYPE_OF_FIELDS)
clusterer2.cluster(mixed_data)
clusterer2.store_model("storage2.json")

sample = loadItemFromJson('dataSample.json')
if(checkSampleForAnomaly(clusterer,sample)):
    print("Cluster: Anomaly Detected")

else:
    print("Cluster: Regular data")

if(checkSampleForAnomaly(clusterer2,sample)):
    print("Cluster2: Anomaly Detected")

else:
    print("Cluster2: Regular data")


