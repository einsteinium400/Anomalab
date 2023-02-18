from Moudles.Storage.StorageFactory import StorageFactory
from Moudles.Databases.Dataset import Dataset
import pandas as pd


class DatasetsController:
    operationFactory = StorageFactory()
    storage = operationFactory.CreateOperationItem()

    def CreateDataset(self,name, csvFilePath):
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
