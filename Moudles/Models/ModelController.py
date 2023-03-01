import numpy as np

from Moudles.Storage.StorageFactory import StorageFactory
from Moudles.Models.Model import Model
from Moudles.Clustring.KMeanClusterer import KMeansClusterer



class ModelsController:
    operationFactory = StorageFactory()
    storage = operationFactory.CreateOperationItem()

    def CreateModel(self, name, dataset, distanceName):
        '''dataSet = dataset
        distanceFunction = MixedDistance()
        mean  =dataSet.MeanValues
        types = dataSet.getAttributesTypesList()
        print(dataSet.Data)
        clusterer = KMeansClusterer(num_means=2,
                                    distance=distanceFunction,
                                    repeats=9,
                                    mean_values=mean,
                                    type_of_fields=types)
        data = np.array(dataSet.Data)
        trained = 0
        while trained == 0:
            try:
                clusterer.cluster(data)
                trained =1
            except:
                trained = 0
        modelJson = clusterer.getModelData()
        self.storage.Save(name, modelJson, "MODEL")'''
        pass

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
        self.storage.Delete(modelsList, "Model")

    def GetAllInstances(self):
        availableDatasets = self.GetAllModelsNamesList()
        finalList = []
        for item in availableDatasets:
            finalList.append(self.GetModel(item))
        return finalList
