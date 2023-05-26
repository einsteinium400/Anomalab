
ANOMALY_DEFINITION_STD_DEV = 1
MAX_ANOMALY_STD_DEV = 3
MIN_PTS = 3

def checkSampleForAnomaly(model,sample):
    data = model.check_sample(sample)
    ##print("data:", data)
    closestCluster = 0
    anomaly=False
    for clusterData in data:
        if clusterData['distance']<data[closestCluster]['distance']:
            closestCluster=clusterData['num']
    if data[closestCluster]['distance']>data[closestCluster]['maxDistance']:
        anomaly = True
    print ('anomaly',anomaly)
    print ('closestCluster',closestCluster)
    closestClusterData = data[closestCluster]
    ##standarize results
    stdResults = []
    for i in range(len(data[closestCluster]['results'])):
        if closestClusterData['results'][i]<=closestClusterData['attributesAverageDistances'][i]:
            stdResults.append(0)
        elif closestClusterData['attributesStdDevs'][i]==0:
            stdResults.append(MAX_ANOMALY_STD_DEV)
        else:
            delta=closestClusterData['results'][i]-closestClusterData['attributesAverageDistances'][i]
            stdResults.append(delta/closestClusterData['attributesStdDevs'][i])
    
    answer = {
        'anomaly' : anomaly,
        'closestCluster' : closestCluster,
        'mean' : closestClusterData['mean'],
        'distance' : closestClusterData['distance'],
        'stdDev' : closestClusterData['stdDev'],
        'results' : closestClusterData['results'],
        'maxDistance' : closestClusterData['maxDistance'],
        'stadarizedResults': stdResults
    }
    return answer