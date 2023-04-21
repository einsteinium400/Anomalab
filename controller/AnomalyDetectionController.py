def checkSampleForAnomaly(model,sample):
    
    def checkAnomaly(clusterJson):
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
    cluster,distances,detailedDistances = model.classify_vectorspace(fakeSample)
    print("detailed distances: ", detailedDistances)
    print("Classifed Cluster: ", cluster)
    predictionFullData = mergeClassifcationData(model,cluster,distances)
    answer = {}
    answer['anomaly'] = []
    answer['clusters'] = cluster
    answer['detailedDistances'] = detailedDistances
    answer['predictionFullData'] = predictionFullData['fullClusteringInfo']['clusters_info']
    for clusterJson in answer['predictionFullData']:
        print ("clusterJson: ", clusterJson)
        if(checkAnomaly(clusterJson)):
            answer['anomaly'].append(True)
        else:
            answer['anomaly'].append(False)
    return answer