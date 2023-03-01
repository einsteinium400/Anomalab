import json
from Moudles.Clustring.KMeanClusterer import KMeansClusterer

def checkAnomaly(clusterJson):
    print("Distance form centroid: ", clusterJson['distance_from_centroid'])
    print("variance: ", 3*clusterJson['variance'])
    print("average_cluster_distance: ",clusterJson['average_cluster_distance'] )
    return abs(clusterJson['distance_from_centroid'] >= (3*clusterJson['variance'] + clusterJson['average_cluster_distance']))

def mergeClassifcationData(model,classifedClusterIndex,classifedClusterDistancesInfo):
        classicationData = {
            "classifiedCluster": classifedClusterIndex,
        }
        modelData = model.getModelData()
        classicationData['fullClusteringInfo'] = modelData
        for cluster in classicationData['fullClusteringInfo']['clusters_info']:
            for singleClassficationData in classifedClusterDistancesInfo:
                if(cluster['cluster'] == singleClassficationData['cluster']):
                    cluster['distance_from_centroid'] = singleClassficationData['distance']
        return classicationData

def checkSampleForAnomaly(model,sample):
    fakeSample = sample
    cluster,distances = model.classify_vectorspace(fakeSample)
    print(distances)
    print("Classifed Cluster", cluster)
    predictionFullData = mergeClassifcationData(model,cluster,distances)
    for clusterJson in predictionFullData['fullClusteringInfo']['clusters_info']:
        if clusterJson['cluster'] == cluster:
            if(checkAnomaly(clusterJson)):
                return True
            else:
                return False