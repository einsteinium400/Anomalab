import json
from abc import abstractmethod
import os
import uuid
import pandas as pd
import time

from model.DatasetPreProcessor import DatasetPreProcessor
from model.RawDatasetData import RawDatasetData
from model.Storage.StorageFactory import StorageFactory

def remove_duplicates(objects):
    unique_objects = {}
    for obj in objects:
        name = obj['name']
        if name not in unique_objects:
            unique_objects[name] = obj

    # Extract the unique objects from the dictionary
    unique_list = list(unique_objects.values())
    return unique_list


class Dataset:
    _id = 0
    _jsonData = 0
    _name = 0
    _bestModel = []
    _timeStamp = 0
    _featureNames = 0
    _importantFeatures = 0
    _data = 0

    def __init__(
            self,
            name,
            filling = "NONE",
            dataFrame=None
    ):
        if (dataFrame is not None):
            dfProccesor = DatasetPreProcessor()

            self._name = name
            newData, attribuesInfo = dfProccesor.dataSetPreProcess(self._name,dataFrame,filling)
            self._id = str(uuid.uuid1())
            self._timeStamp = time.time()
            self._featuresNumber = len(dataFrame.columns.values.tolist())
            self._featureNames = dataFrame.columns.values.tolist()
            self._instancesNumber = len(dataFrame.values.tolist())
            self._featuresInfo = attribuesInfo
            self._data = self._name
            self._importantFeatures = []
            self._bestModel = []
            self._maxValues = []
            # Get mean values
            for item in self._featureNames:
               self._maxValues.append(int(newData[item].max()))
            self._jsonData = {
                "name": self._name,
                "id": self._id,
                "timestamp": self._timeStamp,
                "bestmodel": self._bestModel,
                "featuresNumber": self._featuresNumber,
                "featureNames": self._featureNames,
                "importantfeatures":self._importantFeatures,
                "instancesNumber":self._instancesNumber,
                "featuresInfo":self._featuresInfo,
                "maxValues":self._maxValues,
                "data": self._data
            }
            RawDatasetData(self._name,newData)
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
            self._maxValues = self._jsonData['maxValues']
            self._bestModel = self._jsonData['bestmodel']
            self._featuresInfo = self._jsonData['featuresInfo']

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
    def AttributesInfo(self):
        return self._featuresInfo

    @AttributesInfo.setter
    def AttributesInfo(self, value):
        self._featuresInfo = value
        self.SaveDataset()

    @property
    def BestModel(self):
        return self._bestModel

    @BestModel.setter
    def BestModel(self, value):
        self._bestModel = value
        self.SaveDataset()

    @property
    def name(self):
        return self._name

    @property
    def jsonData(self):
        return self._jsonData

    @property
    def MaxValues(self):
        return self._maxValues

    def __str__(self):
        return f"The dataset name is {self._name}"

    def SaveDataset(self):
        self._jsonData = {
            "name": self._name,
            "id": self._id,
            "timestamp": self._timeStamp,
            "bestmodel": self._bestModel,
            "featuresNumber": self._featuresNumber,
            "featureNames": self._featureNames,
            "importantfeatures": self._importantFeatures,
            "instancesNumber": self._instancesNumber,
            "featuresInfo": self._featuresInfo,
            "maxValues": self._maxValues,
            "data": self._data
        }
        operationFactory = StorageFactory()
        saver = operationFactory.CreateOperationItem()
        saver.Save(self._name, self._jsonData, "DATASET")

    def LoadDataset(self):
        operationFactory = StorageFactory()
        loader = operationFactory.CreateOperationItem()
        jsonData = loader.Load(self._name, "DATASET")
        return jsonData

    def getRawData(self):
        return RawDatasetData(self._name).Data

    def getAttributesTypesList(self):
        featuresList = self._featureNames
        featuresInfo = self._featuresInfo
        finalList = []
        for item in featuresList:
            for feature in featuresInfo:
                if(item == feature['name']):
                    if feature['type'] == 'categorical':
                        finalList.append(True)
                    else:
                        finalList.append(False)
        return finalList
    
    def getAttributesTypesAndValuesList(self):
        featuresList = self._featureNames
        featuresInfo = self._featuresInfo
        finalList = []
        for item in featuresList:
            for feature in featuresInfo:
                if(item == feature['name']):
                    finalList.append(feature)
        return finalList

    def addNewModel(self,model):
        operationFactory = StorageFactory()
        saver = operationFactory.CreateOperationItem()
        returnDataFromMongo = saver.GetListWithSpecificAttributesWithName(self._name,"DATASET",['name','bestmodel'])
        currentDatasetDataBestModel = returnDataFromMongo[0]['bestmodel']
        self._bestModel.append({
            'name':model['name'],
            'wcss':model['wcss'],
            'silhouette':model['silhouette']
        })
        self._bestModel = self._bestModel + currentDatasetDataBestModel
        self._bestModel = remove_duplicates(self._bestModel)
        self._bestModel = sorted(self._bestModel, key=lambda x: x['silhouette'],reverse=True)
        self.SaveDataset()

    def removeModel(self,modelName):
        self._bestModel = [m for m in self._bestModel if m['name'] != modelName]
        self.SaveDataset()

    def sampleDecyper(self,sample):
        decoded_sample = []
        for i, value in enumerate(sample):
            feature_name = self._featureNames[i]
            feature_info = next(item for item in self._featuresInfo if item['name'] == feature_name)
            
            if 'values' in feature_info:
                value_key = str(value)
                if value_key in feature_info['values']:
                    decoded_value = feature_info['values'][value_key]
                    decoded_sample.append(decoded_value)
                else:
                    decoded_sample.append(value)  # Keep the original value if not found in 'values'
            else:
                decoded_sample.append(value)
        return decoded_sample

