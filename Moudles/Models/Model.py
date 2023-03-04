
import uuid
import time

from Moudles.Storage.StorageFactory import StorageFactory


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

    def __str__(self):
        return f"The model name is {self._name}"

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
