from datetime import datetime
ANOMALY_DEFINITION_STD_DEV = 1 ##STD DEV TO DEFINE SUSPECT OF ANOMALY
MAX_ANOMALY_STD_DEV = 3 ##MAX STD DEV TO DEFINE SUSPECT OF ANOMALY
MIN_PTS = 3 ##NEIGHBOR POINTS TO DETERMINE ANOMALY

def checkSampleForAnomaly(model,sample):
    logFile = open("logger/anomalyLogger.txt", "a")
    logFile.write(f'#############################\n')
    logFile.write(f'Time is : {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}\n')
    logFile.write(f'check anomaly for {sample} in model {model.Name}\n')
    data = model.check_sample(sample, MIN_PTS, logFile)
    closestCluster = 0
    closestStandarizeCluster = 0
    anomaly=False
    sampleColumn=0
    for clusterData in data:
        print ('densities of', clusterData['num'],'is:',clusterData['densities']) ## TO DELETE
        logFile.write(f'cluster num: {clusterData["num"]} ,distance: {clusterData["distance"]} ,normalizeDistance: {clusterData["standarizeDistance"]}\n')
        if clusterData['distance']<data[closestCluster]['distance']:
            closestCluster=clusterData['num']
        if clusterData['standarizeDistance']<data[closestStandarizeCluster]['standarizeDistance']:
            closestStandarizeCluster = clusterData['num']
    logFile.write(f'closestCluster: {closestCluster} ,closestStandarizeCluster: {closestStandarizeCluster} ,normalizeDistance: {clusterData["standarizeDistance"]}\n')
    closestClusterData = data[closestCluster]
    ##CHECK ANOMALY
    logFile.write(f'standarize distance: {closestClusterData["standarizeDistance"]} ,do: {closestClusterData["do"]} ,dm: {closestClusterData["dm"]}\n')
    logFile.write('SAMPLE IS ANOMALY: # ')
    if closestClusterData['standarizeDistance']>ANOMALY_DEFINITION_STD_DEV:
        if (closestClusterData['do']>closestClusterData['dm']):
            logFile.write('True # ')
            anomaly = True
    logFile.write('\n')
    ##STANDARIZE RESULTS
    stdResults = []
    for i in range(len(data[closestCluster]['results'])):
        if closestClusterData['results'][i]<=closestClusterData['attributesAverageDistances'][i]:
            stdResults.append(0)
        elif closestClusterData['attributesStdDevs'][i]==0:
            stdResults.append(MAX_ANOMALY_STD_DEV)
        else:
            delta=closestClusterData['results'][i]-closestClusterData['attributesAverageDistances'][i]
            stdResults.append(delta/closestClusterData['attributesStdDevs'][i])
    ##CHECK WHICH COLUMN IN THE GRAPH TO MARK
    if closestClusterData['standarizeDistance']>3:
        sampleColumn = 4
    elif closestClusterData['standarizeDistance']>2:
        sampleColumn = 3
    elif closestClusterData['standarizeDistance']>1:
        sampleColumn = 2
    elif closestClusterData['standarizeDistance']>0:
        sampleColumn = 1
    
    answer = {
        'anomaly' : anomaly,
        'closestCluster' : closestCluster,
        'mean' : closestClusterData['mean'],
        'distance' : closestClusterData['distance'],
        'standarizeDistance' : closestClusterData['standarizeDistance'],
        'stdDev' : closestClusterData['stdDev'],
        'results' : closestClusterData['results'],
        'maxDistance' : closestClusterData['maxDistance'],
        'stadarizedResults': stdResults,
        'densities': closestClusterData['densities'],
        'sampleColumn': sampleColumn,
    }
    logFile.close()
    return answer