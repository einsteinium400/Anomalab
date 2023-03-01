import json
from abc import abstractmethod
import os
import uuid
import pandas as pd
import time

from Moudles.Databases.RawDatasetData import RawDatasetData
from Moudles.Storage.StorageFactory import StorageFactory

class Dataset:
    _id = 0
    _jsonData = 0
    _name = 0
    _bestModel = 0
    _timeStamp = 0
    _featureNames = 0
    _importantFeatures = 0
    _data = 0

    def __init__(
            self,
            name,
            dataFrame=None
    ):
        if (dataFrame is not None):
            self._name = name
            self._id = str(uuid.uuid1())
            self._timeStamp = time.time()
            self._featuresNumber = len(dataFrame.columns.values.tolist())
            self._featureNames = dataFrame.columns.values.tolist()
            self._instancesNumber = len(dataFrame.values.tolist())
            self._data = self._name
            self._importantFeatures = []
            self._bestModel = "none"
            self._jsonData = {
                "name": self._name,
                "id": self._id,
                "timestamp": self._timeStamp,
                "bestmodel": self._bestModel,
                "featuresNumber": self._featuresNumber,
                "featureNames": self._featureNames,
                "importantfeatures":self._importantFeatures,
                "instancesNumber":self._instancesNumber,
                "data": self._data
            }
            RawDatasetData(self._name,dataFrame)
        else:
            self._name = name
            self._jsonData = self.LoadDataset()
            self._id = self._jsonData['id']
            self._timeStamp = self._jsonData['timestamp']
            self._featuresNumber = self._jsonData['featuresNumber']
            self._featureNames = self._jsonData['featureNames']
            self._instancesNumber = self._jsonData['instancesNumber']
            self._data = self._jsonData['data']
            self._importantFeatures = self._jsonData['featureNames']
            self._bestModel = self._jsonData['bestmodel']

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
    def FeatureNames(self):
        return self._featureNames
    
    @property
    def featuresNumber(self):
        return self._featuresNumber
    
    @property
    def instancesNumber(self):
        return self._instancesNumber

    @property
    def Data(self):
        return self.getRawData()

    @property
    def JsonData(self):
        return self._jsonData

    @property
    def ImportFeatures(self):
        return self._importantFeatures

    @ImportFeatures.setter
    def ImportFeatures(self, value):
        self._importantFeatures = value
        self.SaveDataset()

    @property
    def BestModel(self):
        return self._bestModel

    @BestModel.setter
    def BestModel(self, value):
        self._bestModel = value
        self.SaveDataset()

    def AddImportantFeature(self, value):
        if value not in self._featureNames:
            return
        if value in self._importantFeatures:
            return
        self._importantFeatures.append(value)
        self.SaveDataset()

    def SaveDataset(self):
        operationFactory = StorageFactory()
        saver = operationFactory.CreateOperationItem()
        saver.Save(self._name, self._jsonData, "DATASET")

    def LoadDataset(self):
        operationFactory = StorageFactory()
        loader = operationFactory.CreateOperationItem()
        jsonData = loader.Load(self._name, "DATASET")
        return jsonData

    @property
    def name(self):
        return self._name

    @property
    def jsonData(self):
        return self._jsonData

    def __str__(self):
        return f"The dataset name is {self._name}"

    def getRawData(self):
        return RawDatasetData(self._name).Data
