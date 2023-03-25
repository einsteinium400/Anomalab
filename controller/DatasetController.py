from model.Dataset import Dataset
from controller.ModelController import ModelController
from model.Storage.StorageFactory import StorageFactory
import pandas as pd


class DatasetController:
    operationFactory = StorageFactory()
    storage = operationFactory.CreateOperationItem()

    def CreateDataset(self, name, csvFilePath):
        dataSetsList = self.GetAllDatasetsNamesList()
        if name in dataSetsList:
            raise Exception(f'Dataset name {name} already taken')
        df = pd.read_csv(csvFilePath)
        dataSet = Dataset(name, df)
        self.storage.Save(dataSet.Name, dataSet.JsonData, "DATASET")

    def GetAllDatasetsNamesList(self):
        operationFactory = StorageFactory()
        self.storage = operationFactory.CreateOperationItem()
        return self.storage.GetList("DATASET")

    def GetAllDatasetsInfoList(self):
        operationFactory = StorageFactory()
        self.storage = operationFactory.CreateOperationItem()
        fullList = self.storage.GetFullItemsList("DATASET")
        finalList = []
        for item in fullList:
            finalList.append(list((item['id'],item['name'],len(item['featureNames']),len(item['data']),item['timestamp'])))
        return finalList

    def SetBestModel(self,databaseName,modelName):
        modelsController = ModelsController()
        self.GetDataset(databaseName).BestModel = modelsController.GetModel(modelName)

    def GetDataset(self, DatasetName):
        dataSetsList = self.GetAllDatasetsNamesList()
        if DatasetName not in dataSetsList:
            raise Exception(f"Dataset named {DatasetName} Does not exist")
        return Dataset(DatasetName)

    def DeleteDataset(self, DatasetName):
        dataSetsList = self.GetAllDatasetsNamesList()
        if DatasetName not in dataSetsList:
            raise Exception(f"Dataset named {DatasetName} Does not exist")
        self.storage.Delete(DatasetName, "DATASET")

    def GetAllInstances(self):
        availableDatasets = self.GetAllDatasetsNamesList()
        finalList = []
        for item in availableDatasets:
            finalList.append(self.GetDataset(item))
        return finalList


