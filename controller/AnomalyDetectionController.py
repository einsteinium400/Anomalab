
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
    #closestStandarizeClusterData = data[closestStandarizeCluster]
    ##CHECK ANOMALY
    print ('standarize distance is:',closestClusterData['standarizeDistance'])
    if closestClusterData['standarizeDistance']>ANOMALY_DEFINITION_STD_DEV:
        print ('SUSPECT OF ANOMALY','do is',closestClusterData['do'],'dm is',closestClusterData['dm'])
        if (closestClusterData['do']>closestClusterData['dm']):
            print ('SAMPLE IS ANOMALY')
            anomaly = True
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
        'standarizeDistance' : closestClusterData['standarizeDistance'],
        'stdDev' : closestClusterData['stdDev'],
        'results' : closestClusterData['results'],
        'maxDistance' : closestClusterData['maxDistance'],
        'stadarizedResults': stdResults
    }
    return answer