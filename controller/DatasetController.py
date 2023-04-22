from model.Dataset import Dataset
from model.Storage.StorageFactory import StorageFactory
import pandas as pd


class DatasetController:
    operationFactory = StorageFactory()
    storage = operationFactory.CreateOperationItem()
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, *args, **kwargs):
        if self.__initialized:
            return
        self.__initialized = True

    def __GetAllDatasetsNamesList(self):
        return self.storage.GetNamesList("DATASET")
    def __GetAllInstances(self):
        availableDatasets = self.__GetAllDatasetsNamesList()
        finalList = []
        for item in availableDatasets:
            finalList.append(self.GetDataset(item))
        return finalList
    
    def CreateDataset(self, name, csvFilePath):
        dataSetsList = self.__GetAllDatasetsNamesList()
        if name in dataSetsList:
            raise Exception(f'Dataset name {name} already taken')
        df = pd.read_csv(csvFilePath)
        dataSet = Dataset(name, df)
        self.storage.Save(dataSet.Name, dataSet.JsonData, "DATASET")

    def GetDataset(self, DatasetName):
        dataSetsList = self.__GetAllDatasetsNamesList()
        if DatasetName not in dataSetsList:
            raise Exception(f"Dataset named {DatasetName} Does not exist")
        return Dataset(DatasetName)

    def DeleteDataset(self, DatasetName):
        dataSetsList = self.__GetAllDatasetsNamesList()
        if DatasetName not in dataSetsList:
            raise Exception(f"Dataset named {DatasetName} Does not exist")
        self.storage.Delete(DatasetName, "DATASET")
        self.storage.DeleteItemsByTypeAndFilter("MODEL",{"datasetName":DatasetName})

    def GetListForQuery(self):
        dataSetList = self.storage.GetListWithSpecificAttributes("DATASET",['name','bestmodel'])
        filtered_list = list(filter(lambda x: bool(x['bestmodel']), dataSetList))
        return filtered_list

    def GetListForManager(self):
        return self.storage.GetListWithSpecificAttributes("DATASET",['name','timestamp','featuresNumber','instancesNumber'])
    
    def GetAttributesList(self,name):
        return self.GetDataset(name).getAttributesTypesAndValuesList()
    
    def CleanModelsFromDatasetsByFunction(self,name):
        allDataSets = self.__GetAllInstances()
        for dataset in allDataSets:
            for modelName in dataset.BestModel:
                if f"-{name}" in modelName['name']:
                    dataset.removeModel(modelName['name'])

    
    # def GetAllDatasetsInfoList(self):
    #     operationFactory = StorageFactory()
    #     self.storage = operationFactory.CreateOperationItem()
    #     fullList = self.storage.GetFullItemsList("DATASET")
    #     finalList = []
    #     for item in fullList:
    #         finalList.append(list((item['id'],item['name'],len(item['featureNames']),len(item['data']),item['timestamp'])))
    #     return finalList

