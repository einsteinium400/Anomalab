
import numpy as np
import traceback
import uuid
import time

from model.Storage.StorageFactory import StorageFactory
from model.Model import Model
from model.KMeanClusterer import KMeansClusterer
from model import modular_distance_utils
from model.utils import csv_to_nested_list


class ModelController:
    operationFactory = StorageFactory()
    storage = operationFactory.CreateOperationItem()

    def CreateModel(self, name, dataset, distanceName):
        dataSet = dataset
        distanceFunction = modular_distance_utils.get_function_by_name(distanceName)
        mean = dataSet.MeanValues
        types = dataSet.getAttributesTypesList()
        clusterer = KMeansClusterer(num_means=3, # TODO: Change to elbow to get the right K for the dataset
                                    distance=distanceFunction,
                                    repeats=1,
                                    mean_values=mean,
                                    type_of_fields=types)
        data = np.array(dataSet.Data)
        #TODO: Deal with bad seeds
        trained = 0
        while trained == 0:
            try:
                clusterer.cluster(data)
                trained =1
            except Exception as e:
                print(f"Error {e}")
                traceback.print_exc()
                trained = 0
        modelJson = clusterer.getModelData()
        modelJson['datasetName']=dataset.Name
        modelJson['function'] = distanceName
        modelJson['name'] = name
        modelJson['id'] = str(uuid.uuid1())
        modelJson['timestamp'] = time.time()
        modelJson['fieldTypes'] = types
        meanValues = []
        for item in modelJson['clusters_info']:
            meanValues.append(item['mean'])
        modelJson['meanValues'] = meanValues

        self.storage.Save(name, modelJson, "MODEL")
        if dataset.BestModel == "":
            dataset.BestModel =modelJson['name']
            dataset.SaveDataset()
        else:
            oldModel = self.GetModel(dataset.BestModel)
            if oldModel.Wcss > modelJson['wcss_score_of_model']:
                dataset.BestModel = modelJson['name']
                dataset.SaveDataset()

    def GetAllModelsNamesList(self):
        operationFactory = StorageFactory()
        self.storage = operationFactory.CreateOperationItem()
        return self.storage.GetList("MODEL")

    def GetModel(self, modelName):
        modelsList = self.GetAllModelsNamesList()
        if modelName not in modelsList:
            raise Exception(f"Model named {modelName} Does not exist")
        return Model(modelName)

    def DeleteModel(self, modelName):
        modelsList = self.GetAllModelsNamesList()
        if modelName not in modelsList:
            raise Exception(f"Model named {modelName} Does not exist")
        self.storage.Delete(modelName, "MODEL")

    def GetAllInstances(self):
        availableDatasets = self.GetAllModelsNamesList()
        finalList = []
        for item in availableDatasets:
            finalList.append(self.GetModel(item))
        return finalList

    def GetModelsStatus(self):
        datasetList = self.storage.GetList("DATASET")
        functionNames = self.storage.GetList("FUNCTION")
        modelList = self.GetAllInstances()
        finalList = []
        for dataset in datasetList:
            # initialize an empty dictionary for the current key
            Item = []
            Item.append(dataset)
            # iterate through each item in the modelList and add it to the innerDict with a value of False
            _modelsList=[]
            for function in functionNames:
                _model=[]
                _model.append(function)
                _model.append("")
                for model in modelList:
                    if(model.DatasetName == dataset and model.DistanceFunction == function):
                        _model[1]=model.Name
                _modelsList.append(_model)
            Item.append(_modelsList)
            # add the innerDict to the newDict with the current key as its key
            finalList.append(Item)
        return finalList