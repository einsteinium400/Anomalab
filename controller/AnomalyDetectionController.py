
ANOMALY_DEFINITION_STD_DEV = 1
MAX_ANOMALY_STD_DEV = 3
MIN_PTS = 3

def checkSampleForAnomaly(model,sample):
    data = model.check_sample(sample, MIN_PTS)
    closestCluster = 0
    closestStandarizeCluster = 0
    anomaly=False
    for clusterData in data:
        print ("cluster num",clusterData['num'],"distance",clusterData['distance'],"normalizeDistance",clusterData['standarizeDistance'])
        if clusterData['distance']<data[closestCluster]['distance']:
            closestCluster=clusterData['num']
        if clusterData['standarizeDistance']<data[closestStandarizeCluster]['standarizeDistance']:
            closestStandarizeCluster = clusterData['num']
    print ('closestCluster',closestCluster)
    print ('closestStandarizeCluster',closestStandarizeCluster)
    closestClusterData = data[closestCluster] ## FOR USE OF REAL DISTANCE
    closestStandarizeClusterData = data[closestStandarizeCluster]
    ##CHECK ANOMALY
    print ('standarize distance is:',closestStandarizeClusterData['standarizeDistance'])
    if closestStandarizeClusterData['standarizeDistance']>ANOMALY_DEFINITION_STD_DEV:
        print ('SUSPECT OF ANOMALY','do is',closestStandarizeClusterData['do'],'dm is',closestStandarizeClusterData['dm'])
        if (closestStandarizeClusterData['do']>closestStandarizeClusterData['dm']):
            print ('SAMPLE IS ANOMALY')
            anomaly = True
    ##standarize results
    stdResults = []
    for i in range(len(data[closestCluster]['results'])):
        if closestStandarizeClusterData['results'][i]<=closestStandarizeClusterData['attributesAverageDistances'][i]:
            stdResults.append(0)
        elif closestStandarizeClusterData['attributesStdDevs'][i]==0:
            stdResults.append(MAX_ANOMALY_STD_DEV)
        else:
            delta=closestStandarizeClusterData['results'][i]-closestStandarizeClusterData['attributesAverageDistances'][i]
            stdResults.append(delta/closestStandarizeClusterData['attributesStdDevs'][i])
    
    answer = {
        'anomaly' : anomaly,
        'closestCluster' : closestStandarizeCluster,
        'mean' : closestStandarizeClusterData['mean'],
        'distance' : closestStandarizeClusterData['distance'],
        'stdDev' : closestStandarizeClusterData['stdDev'],
        'results' : closestStandarizeClusterData['results'],
        'maxDistance' : closestStandarizeClusterData['maxDistance'],
        'stadarizedResults': stdResults
    }
    return answer