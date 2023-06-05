import uuid
import time
from datetime import datetime

from model import modular_distance_utils
from model.Storage.StorageFactory import StorageFactory
#from controller.DistanceFunctionController import DistanceFunctionController

class Model:
    _id = 0
    _jsonData = 0
    _name = 0
    _distanceFunction = 0
    _distanceFunctionId = 0
    _timeStamp = 0
    _wcss = 0
    _numberOfClusters = 0
    _clusters = 0
    _hyperParams = 0
    _clustersValues=0

    def __init__(
            self,
            name,
            modelJson=None
    ):
        if (modelJson is not None):
            self._name = name
            self._id = str(uuid.uuid1())
            self._timeStamp = time.time()
            self._distanceFunction = modelJson['function']
            self._datasetName = modelJson['datasetName']
            self._jsonData = modelJson
            self._jsonData['id'] = self._id
            self._jsonData['timeStamp'] = self._timeStamp
            self._wcss = modelJson['wcss']
            self._silhouette=modelJson['silhouette']
            self._numberOfClusters = len(modelJson['clusters_info'])
            self._clusters = modelJson['clusters_info']
            self._clustersValues = modelJson['cluster_values']
            self._fieldTypes = modelJson['fieldTypes']
            self._meanValues = modelJson['meanValues']
            self._hyperParams = modelJson['hyperParams']
            self._distanceFunctionRefrence = modular_distance_utils.get_function_by_name(self._distanceFunction)
        else:
            self._name = name
            self._jsonData = self.LoadModel()
            self._id = self._jsonData['id']
            self._timeStamp = self._jsonData['timestamp']
            self._distanceFunction = self._jsonData['function']
            self._silhouette=self._jsonData['silhouette']
            self._wcss = self._jsonData['wcss']
            self._silhouette=self._jsonData['silhouette']
            self._numberOfClusters = len(self._jsonData['clusters_info'])
            self._clusters = self._jsonData['clusters_info']
            self._clustersValues = self._jsonData['cluster_values']
            self._datasetName = self._jsonData['datasetName']
            self._fieldTypes = self._jsonData['fieldTypes']
            self._meanValues = self._jsonData['meanValues']
            self._hyperParams = self._jsonData['hyperParams']
            self._distanceFunctionRefrence = modular_distance_utils.get_function_by_name(self._distanceFunction)

    def __str__(self):
        return f"The model name is {self._name} function {self._distanceFunction} dataset {self._datasetName}"

    @property
    def Id(self):
        return self._id

    @property
    def Name(self):
        return self._name

    @property
    def Timestamp(self):
        return self._timeStamp

    @property
    def Wcss(self):
        return self._wcss
    
    @property
    def Silhouette(self):
        return self._silhouette

    @property
    def NumberOfClusters(self):
        return self._numberOfClusters

    @property
    def Clusters(self):
        return self._clusters

    @property
    def DistanceFunction(self):
        return self._distanceFunction

    @DistanceFunction.setter
    def ImportFeatures(self, value):
        self._distanceFunction = value
        self.SaveModel()

    @property
    def DatasetName(self):
        return self._datasetName

    @DatasetName.setter
    def DatasetName(self, value):
        self._datasetName = value
        self.SaveModel()

    @property
    def HyperParams(self):
        return self._hyperParams

    @HyperParams.setter
    def HyperParams(self, value):
        self._hyperParams = value
        self.SaveModel()

    @property
    def DistanceFunctionId(self):
        return self._distanceFunctionId

    @DistanceFunctionId.setter
    def ImportFeatures(self, value):
        self._distanceFunctionId = value
        self.SaveModel()

    @property
    def JsonData(self):
        return self._jsonData

    @JsonData.setter
    def ImportFeatures(self, value):
        self._jsonData = value
        self.SaveModel()
    
    @property
    def ClusterValues(self):
        return self._clustersValues


    def SaveModel(self):
        operationFactory = StorageFactory()
        saver = operationFactory.CreateOperationItem()
        saver.Save(self._name, self._jsonData, "MODEL")

    def LoadModel(self):
        operationFactory = StorageFactory()
        loader = operationFactory.CreateOperationItem()
        jsonData = loader.Load(self._name, "MODEL")
        return jsonData

    # Classify a new sample
    def check_sample(self, vector, minPts, logFile):
        ##CALCULATE DO AND DM FOR ANOMALY DETECTION METHOD
        def calculateDOandDM(distanceFunc, fieldTypes, hyperParams, vector, clusterDataSamples, minPts, logFile):
            ##calculate DO return 3 closest point and 3 closest distances
            def calculateDO(distanceFunc, fieldTypes, hyperParams, vector, clusterDataSamples, minPts=3, deleteMyself=False):            
                closestDataSamples = []
                for dataSample in clusterDataSamples:
                    distance, results = distanceFunc(vector, dataSample, fieldTypes, hyperParams)
                    if (distance==0 and deleteMyself==True):
                        deleteMyself=False
                    else:
                        ## IF STILL DON'T HOLD ENOUGH POINTS ADD POINT
                        if len(closestDataSamples)<minPts:
                            closestDataSamples.append((dataSample,distance))
                            closestDataSamples = sorted(closestDataSamples,key=lambda x: x[1],reverse=True)
                        ## IF HOLD ENOUGH CHECK IF NEED TO CHANGE POINTS
                        elif distance<closestDataSamples[0][1]:
                            closestDataSamples[0]=(dataSample,distance)
                            closestDataSamples = sorted(closestDataSamples,key=lambda x: x[1],reverse=True)
                return closestDataSamples
            
            ##DEAL WITH SMALL CLUSTER THAN MIN PTS
            if (len(clusterDataSamples)<minPts):
                return -1,-1
            closestSamples=calculateDO(distanceFunc, fieldTypes, hyperParams, vector, clusterDataSamples, minPts)
            logFile.write(f'closest neighbors of the query: {vector} are: {closestSamples}\n')
            dmArr=[]
            for sample in closestSamples:
                closestneighbors = calculateDO(distanceFunc, fieldTypes, hyperParams, sample[0], clusterDataSamples, minPts, deleteMyself=True)
                dmArr.append(sum(tupleObj[1] for tupleObj in closestneighbors))
                logFile.write(f'closest neighbors of neighbor: {vector} are: {closestSamples}\n')
            do = sum(tupleObj[1] for tupleObj in closestSamples)/minPts
            dm = sum(dmArr)/(minPts**2)
            return do,dm
        ## USED FOR GRAPH
        def calculateDensities(distanceFunc, fieldTypes, hyperParams, center, clusterDataSamples, averageDistance, stdDev):
            densities = {
                            "lessThanAvg":0,
                            "avgTo1stdDev":0,
                            "1stdDevTo2stdDev":0,
                            "2stdDevTo3stdDev":0,
                            "moreThan3stdDev":0
                        }
            for dataSample in clusterDataSamples:
                distance, results = distanceFunc(center, dataSample, fieldTypes, hyperParams)
                standarizeDistance = (distance-averageDistance)/stdDev
                if standarizeDistance<=0:
                    densities['lessThanAvg']=densities['lessThanAvg']+1
                elif standarizeDistance<=1:
                    densities['avgTo1stdDev']=densities['avgTo1stdDev']+1
                elif standarizeDistance<=2:
                    densities['1stdDevTo2stdDev']=densities['1stdDevTo2stdDev']+1
                elif standarizeDistance<=3:
                    densities['2stdDevTo3stdDev']=densities['2stdDevTo3stdDev']+1
                else:
                    densities['moreThan3stdDev']=densities['moreThan3stdDev']+1
            return densities
        
        means = self._meanValues
        clustersInfo = self._clusters
        returnObject = []
        for index in range(len(means)):
            mean = means[index]
            logFile.write(f'cluster: {index} ,centroid: {mean}\n')
            distance, results = self._distanceFunctionRefrence(vector, mean, self._fieldTypes, self._hyperParams)
            for i in range(len(results)):
                results[i]=abs(results[i])
            logFile.write(f'distance:{distance} ,results:{results}\n')
            averageDistance = clustersInfo[index]['averageDistance']
            maxDistance = clustersInfo[index]['maxDistance']
            stdDev = clustersInfo[index]['stdDev']
            attributesAverageDistances = clustersInfo[index]['attributesAverageDistances']
            attributesStdDevs = clustersInfo[index]['attributesStdDevs']
            standarizeDistance = (distance-averageDistance)/stdDev
            ##deal with the donut problem
            if standarizeDistance < 0 :
                standarizeDistance = 0
            logFile.write(f'averageDistance: {averageDistance}, maxDistance: {maxDistance}, stdDev: {stdDev}, standarizeDistance: {standarizeDistance}\n')
            logFile.write(f'attributesAverageDistances: {attributesAverageDistances}, attributesStdDevs: {attributesStdDevs}\n')
            do,dm = calculateDOandDM(self._distanceFunctionRefrence, self._fieldTypes, self._hyperParams ,vector,self._clustersValues[index],minPts,logFile)
            logFile.write(f'do: {do}, dm: {dm}\n')
            densities = calculateDensities(self._distanceFunctionRefrence, self._fieldTypes, self._hyperParams ,mean, self._clustersValues[index], averageDistance, stdDev)
            clusterReturnObject = {
                "num": index,
                "mean": mean,
                "distance": distance,
                "results": results,
                "averageDistance": averageDistance,
                "maxDistance": maxDistance,
                "standarizeDistance": standarizeDistance,
                "stdDev" : stdDev,
                "attributesAverageDistances": attributesAverageDistances,
                "attributesStdDevs": attributesStdDevs,
                "do": do,
                "dm": dm,
                "densities": densities,
            }
            returnObject.append(clusterReturnObject)
        return returnObject
