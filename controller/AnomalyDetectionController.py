ANOMALY_DEFINITION_STD_DEV = 2

def checkSampleForAnomaly(model,sample):
    anomalyData = model.check_sample(sample)
    print("anomalyData:", anomalyData)
    overall = anomalyData['overall']
    clustersNumber = len(overall)
    closestCluster = 0
    anomaly=False
    for i in range(clustersNumber):
        if overall[i]['standarizeDistance']<overall[closestCluster]['standarizeDistance']:
            closestCluster=i
    if overall[closestCluster]['standarizeDistance']>ANOMALY_DEFINITION_STD_DEV:
        anomaly = True
    answer = {
        'anomaly' : anomaly,
        'closestCluster' : closestCluster,
        'overallDistance' : overall[closestCluster]['distance'],
        'overallStandarizeDistance' : overall[closestCluster]['standarizeDistance'],
        'distances' : anomalyData['distancesVectors'][closestCluster],
        'standarizeDistances' : anomalyData['standarizeDistancesVectors'][closestCluster],
        'clusterCenter': anomalyData['means'][closestCluster]
    }
    print ('answer:',answer)
    return answer