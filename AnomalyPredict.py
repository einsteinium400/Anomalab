import json
import KMeanClusterer
def checkAnomaly(clusterJson):
    return abs(clusterJson['average_cluster_distance']  >= (3*clusterJson['variance'] + clusterJson['average_cluster_distance']))

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
    predictionFullData = mergeClassifcationData(model,cluster,distances)
    for clusterJson in predictionFullData['fullClusteringInfo']['clusters_info']:
        if clusterJson['cluster'] == cluster:
            if(checkAnomaly(clusterJson)):
                return True
            else:
                return False