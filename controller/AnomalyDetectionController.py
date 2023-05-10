ANOMALY_DEFINITION_STD_DEV = 2

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
    answer = {
        'anomaly' : anomaly,
        'closestCluster' : closestCluster,
        'mean' : data[closestCluster]['mean'],
        'distance' : data[closestCluster]['distance'],
        'results' : data[closestCluster]['results'],
        'maxDistance' : data[closestCluster]['maxDistance'],
    }
    return answer