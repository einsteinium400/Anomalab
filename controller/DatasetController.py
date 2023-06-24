from model.Dataset import Dataset
from model.Storage.StorageFactory import StorageFactory
import pandas as pd

COMMON_MISSING_VALUES=['NA']


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
        if any(item.startswith(name) for item in dataSetsList):
            raise Exception(f'Dataset name {name} already taken')
        df = pd.read_csv(csvFilePath)
        # Replace common missing values conventions with NaN
        for item in COMMON_MISSING_VALUES:
            df = df.replace(item, pd.NaT)
        missing_values_count = df.isnull().sum().sum()
        if(missing_values_count > 0):
            df_copy_common_fill = df.copy()
            df_copy_unique_fill = df.copy()
            dataSet1 = Dataset(f'{name}-common-fillna',"COMMON", df_copy_common_fill)
            self.storage.Save(dataSet1.Name, dataSet1.JsonData, "DATASET")
            dataSet2 = Dataset(f'{name}-unique-fillna',"UNIQUE" ,df_copy_unique_fill )
            self.storage.Save(dataSet2.Name, dataSet2.JsonData, "DATASET")
        else:
            df_copy = df.copy()
            dataSet1 = Dataset(f'{name}',"NONE", df_copy)
            self.storage.Save(dataSet1.Name, dataSet1.JsonData, "DATASET")

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
        self.storage.DeleteItemsByTypeAndFilter("RAW_DATASET",{"name":DatasetName})

    def GetListForQuery(self):
        dataSetList = self.storage.GetListWithSpecificAttributes("DATASET",['name','bestmodel'])
        filtered_list = list(filter(lambda x: bool(x['bestmodel']), dataSetList))
        return filtered_list

    def GetListForManager(self):
        return self.storage.GetListWithSpecificAttributes("DATASET",['name','timestamp','featuresNumber','instancesNumber'])
    
    def GetAttributesList(self,name):
        preFilteredAttributesList = self.GetDataset(name).getAttributesTypesAndValuesList()
        # Iterate over each object in the array
        for item in preFilteredAttributesList:
            if item['type'] == 'categorical':
                values = item['values']
                updated_values = {key: value for key, value in values.items() if not value.startswith('filledNa-')}
                item['values'] = updated_values
        # filter na fill in unique values
        return preFilteredAttributesList
    
    def CleanModelsFromDatasetsByFunction(self,name):
        allDataSets = self.__GetAllInstances()
        for dataset in allDataSets:
            for modelName in dataset.BestModel:
                if f"-{name}" in modelName['name']:
                    dataset.removeModel(modelName['name'])

