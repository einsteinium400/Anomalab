import numpy as np
import traceback
import uuid
import time
from datetime import datetime

from model.Preprocess import preProcess
from model.Storage.StorageFactory import StorageFactory
from model.Model import Model
from model.KMeanClusterer import KMeansClusterer
from model import modular_distance_utils

CLUSTERING_TRIES = 2
REPEATS = 8

class ModelController:
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
        # initialization code here

    def __GetAllModelsNamesList(self):
        return self.storage.GetNamesList("MODEL")

    def __GetAllInstances(self):
        availableDatasets = self.__GetAllModelsNamesList()
        finalList = []
        for item in availableDatasets:
            finalList.append(self.GetModel(item))
        return finalList

    def __GetAllModelsWithSpecificAttributes(self, attributesList):
        return self.storage.GetListWithSpecificAttributes("MODEL", attributesList)

    def CreateModel(self, dataset, distanceName):
        logFile = open("logger/createModelLogger.txt", "a")
        try:
            _time = datetime.now()
            logFile.write(f'################################################\n')
            name = f'{dataset.Name}-{distanceName}'
            logFile.write(f'Start Create Model {name} Time is : {_time.strftime("%d/%m/%Y, %H:%M:%S")}\n')
            modelsList = self.__GetAllModelsNamesList()
            if name in modelsList:
                raise Exception(f"Model named {name} exist")
            dataSet = dataset
            distanceFunction = modular_distance_utils.get_function_by_name(distanceName)
            fieldsData = dataSet.getAttributesTypesAndValuesList()
            types = [True if d['type'] == 'categorical' else False for d in fieldsData]
            data = np.array(dataSet.Data)
            hp, k = preProcess(data, fieldsData, distanceFunction, CLUSTERING_TRIES, REPEATS)
            logFile.write("done preprocess\n")
            modelsTries = []
            for i in range(CLUSTERING_TRIES):
                try:
                    modelsTries.append(KMeansClusterer(num_means=k,
                                                    distance=distanceFunction,
                                                    repeats=REPEATS,
                                                    type_of_fields=types,
                                                    hyper_params=hp))
                except Exception as e:
                    traceback.print_exc()
                    raise e
            logFile.write('create k means models and start training\n')
            for i in range(CLUSTERING_TRIES):
                trained = 0
                while trained == 0:
                    try:
                        modelsTries[i].cluster_vectorspace(data)
                        logFile.write(f"create model num {i} wcss is:{modelsTries[i].get_wcss()}\n")
                        trained = 1
                    except Exception as e:
                        traceback.print_exc()
                        trained = 0
            best = 0
            for i in range(1, CLUSTERING_TRIES):
                if (modelsTries[best].get_wcss() > modelsTries[i].get_wcss()):
                    best = i
            logFile.write(f"FINISH TRAINING- IT TOOK: {(datetime.now() - _time).seconds} seconds\n")
            logFile.write(f'wcss is: {modelsTries[best].get_wcss()}\n')
            logFile.write(f'silhouette is: {modelsTries[best].get_Silhouette()}\n')
            modelsTries[best].metaDataCalculation()
            modelsTries[best].createClusterJson()
            modelJson = modelsTries[best].getModelData()
            modelJson['datasetName'] = dataset.Name
            modelJson['function'] = distanceName
            modelJson['name'] = name
            modelJson['id'] = str(uuid.uuid1())
            modelJson['timestamp'] = time.time()
            modelJson['fieldTypes'] = types
            meanValues = []
            for item in modelJson['clusters_info']:
                meanValues.append(item['mean'])
            modelJson['meanValues'] = meanValues
            logFile.write(f"{modelJson['meanValues']}\n")
            self.storage.Save(name, modelJson, "MODEL")
            dataset.addNewModel({
                'name': modelJson['name'],
                'wcss':modelJson['wcss'],
                'silhouette': modelJson['silhouette']
            })

            logFile.write(f"OVERALL IT TOOK: {(datetime.now() - _time).seconds} seconds\n")
            logFile.write("########################## MODEL FINISHED#############################\n")
            
        except Exception as e:
            traceback.print_exc()
            self.storage.Delete(name, "MODEL")
            dataset.removeModel(name)
            

    def GetModel(self, modelName):
        modelsList = self.__GetAllModelsNamesList()
        if modelName not in modelsList:
            raise Exception(f"Model named {modelName} Does not exist")
        return Model(modelName)

    def DeleteModel(self, modelName, dataset):
        modelsList = self.__GetAllModelsNamesList()
        if modelName not in modelsList:
            raise Exception(f"Model named {modelName} Does not exist")
        dataset.removeModel(modelName)
        self.storage.Delete(modelName, "MODEL")

    def GetModelsStatus(self):
        datasetList = self.storage.GetNamesList("DATASET")
        functionNames = self.storage.GetNamesList("FUNCTION")
        modelList = self.__GetAllInstances()
        finalList = []
        for dataset in datasetList:
            # initialize an empty dictionary for the current key
            Item = []
            Item.append(dataset)
            # iterate through each item in the modelList and add it to the innerDict with a value of False
            _modelsList = []
            for function in functionNames:
                _model = []
                _model.append(function)
                _model.append("")
                for model in modelList:
                    if (model.DatasetName == dataset and model.DistanceFunction == function):
                        _model[1] = model.Name
                _modelsList.append(_model)
            Item.append(_modelsList)
            # add the innerDict to the newDict with the current key as its key
            finalList.append(Item)
        return finalList
