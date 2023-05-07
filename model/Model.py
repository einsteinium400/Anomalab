
import uuid
import time
import copy

from model import modular_distance_utils
from model.Storage.StorageFactory import StorageFactory
#from controller.DistanceFunctionController import DistanceFunctionController

OFF_SCALE = 5


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
            # self._distanceFunctionId = modelJson['functionId']
            self._datasetName = modelJson['datasetName']
            self._jsonData = modelJson
            self._jsonData['id'] = self._id
            self._jsonData['timeStamp'] = self._timeStamp
            self._wcss = modelJson['wcss_score_of_model']
            self._numberOfClusters = len(modelJson['clusters_info'])
            self._clusters = modelJson['clusters_info']
            self._fieldTypes = modelJson['fieldTypes']
            self._meanValues = modelJson['meanValues']
            self._hyperParams = modelJson['hyperParams']
            self._distanceFunctionRefrence = modular_distance_utils.get_function_by_name(self._distanceFunction)
        else:
            self._name = name
            self._jsonData = self.LoadModel()
            self._id = self._jsonData['id']
            self._timeStamp = self._jsonData['timestamp']
            # self._distanceFunctionId = self._jsonData['functionId']
            self._distanceFunction = self._jsonData['function']
            self._wcss = self._jsonData['wcss_score_of_model']
            self._numberOfClusters = len(self._jsonData['clusters_info'])
            self._clusters = self._jsonData['clusters_info']
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
    def check_sample(self, vector):
        means = self._meanValues
        clustersInfo = self._clusters
        print ('cluster info is: ', self._clusters)
        print ('means: ',means)
        types=self._fieldTypes
        distanceFunc = self._distanceFunctionRefrence
        clustersDistances = []
        distancesVectors = []
        standarizeDistancesVectors=[]
        hyperParmas = self._hyperParams
        for index in range(len(means)):
            mean = means[index]
            averageDistances = clustersInfo[index]['averageDistances']
            stdDevs = clustersInfo[index]['meansStdDev']
            print ('$$$$cluster number ',index,' $$$$$$$$$$$$$$$$')
            print ('averageDistances: ',averageDistances)
            print ('stdDevs: ',stdDevs)
            distance, results = distanceFunc(vector, mean, types, hyperParmas)
            distancesVectors.append(results)
            print ('results: ', results)
            standarizeDistances = []
            for i in range(len(results)):
                delta = results[i]-averageDistances[i]
                if (delta <= 0):
                    standarizeDistances.append(0)
                elif (stdDevs[i]==0):
                    standarizeDistances.append(OFF_SCALE)
                else:
                    standarizeDistances.append(delta/(stdDevs[i]))
            print ('standarizeDistances: ', standarizeDistances)
            standarizeDistancesVectors.append(standarizeDistances)
            delta = distance-clustersInfo[index]['average_cluster_distance']
            standarizeDistance = 0
            if (delta <= 0):
                standarizeDistance=0
            elif (clustersInfo[index]['variance']==0):
                standarizeDistance=OFF_SCALE
            else:
                standarizeDistance=delta/clustersInfo[index]['variance']
            cluster_info = {
                "distance": distance,
                "standarizeDistance": standarizeDistance
            }
            clustersDistances.append(cluster_info)
        returnObject = {
            "overall": clustersDistances,
            "distancesVectors": distancesVectors,
            "standarizeDistancesVectors": standarizeDistancesVectors,
            "means": means
        }
        return returnObject
