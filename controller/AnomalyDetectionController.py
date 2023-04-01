import json
from model.KMeanClusterer import KMeansClusterer


def checkSampleForAnomaly(model,sample):
    def checkAnomaly(clusterJson):
        print("Distance form centroid: ", clusterJson['distance_from_centroid'])
        print("variance: ", clusterJson['variance'])
        print("average_cluster_distance: ",clusterJson['average_cluster_distance'] )
        return abs(clusterJson['distance_from_centroid'] >= (1*clusterJson['variance'] + clusterJson['average_cluster_distance']))

    def mergeClassifcationData(model,classifedClusterIndex,classifedClusterDistancesInfo):
            classicationData = {
                "classifiedCluster": classifedClusterIndex,
            }
            modelData = model.JsonData
            classicationData['fullClusteringInfo'] = modelData
            for cluster in classicationData['fullClusteringInfo']['clusters_info']:
                for singleClassficationData in classifedClusterDistancesInfo:
                    if(cluster['cluster'] == singleClassficationData['cluster']):
                        cluster['distance_from_centroid'] = singleClassficationData['distance']
            return classicationData
    fakeSample = sample
    cluster,distances = model.classify_vectorspace(fakeSample)
    str = ""
    str += f'distances: {distances}\n'
    print(distances)
    print("Classifed Cluster", cluster)
    str += f'classified Cluster {cluster}\n'
    predictionFullData = mergeClassifcationData(model,cluster,distances)
    for clusterJson in predictionFullData['fullClusteringInfo']['clusters_info']:
        if clusterJson['cluster'] == cluster:
            str+=f'Distance form centroid: {clusterJson["distance_from_centroid"]}\n'
            str+=f'variance: {clusterJson["variance"]}\n'
            str+=f'average_cluster_distance: {clusterJson["average_cluster_distance"]}\n'
            if(checkAnomaly(clusterJson)):
                return True,str
            else:
                return False,str