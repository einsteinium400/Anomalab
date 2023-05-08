ANOMALY_DEFINITION_STD_DEV = 2

def checkSampleForAnomaly(model,sample):
    anomalyData = model.check_sample(sample)
    ##print("anomalyData:", anomalyData)
    clustersInfo = anomalyData['clustersInfo']
    clustersNumber = len(clustersInfo)
    closestCluster = 0
    anomaly=False
    for i in range(clustersNumber):
        print (f"clusterDistance {i} : {clustersInfo[i]['distance']}")
        print (f"maxDistance {i} : {clustersInfo[i]['maxDistance']}")
        print (f"stdDistance {i} : {clustersInfo[i]['standarizeDistance']}")
        if clustersInfo[i]['standarizeDistance']<clustersInfo[closestCluster]['standarizeDistance']:
            closestCluster=i
    if clustersInfo[closestCluster]['standarizeDistance']>ANOMALY_DEFINITION_STD_DEV:
        anomaly = True
    answer = {
        'anomaly' : anomaly,
        'closestCluster' : closestCluster,
        'clusterDistance' : clustersInfo[closestCluster]['distance'],
        'maxDistance' : clustersInfo[closestCluster]['maxDistance'],
        'clusterStandarizeDistance' : clustersInfo[closestCluster]['standarizeDistance'],
        'distances' : anomalyData['distancesVectors'][closestCluster],
        'standarizeDistances' : anomalyData['standarizeDistancesVectors'][closestCluster],
        'clusterCenter': anomalyData['means'][closestCluster]
    }
    print ('answer:',answer)
    return answer