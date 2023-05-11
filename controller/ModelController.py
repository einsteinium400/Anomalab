
import numpy as np
import traceback
import uuid
import time

from model.Preprocess import preProcess
from model.Storage.StorageFactory import StorageFactory
from model.Model import Model
from model.KMeanClusterer import KMeansClusterer
from model import modular_distance_utils

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
    
    def __GetAllModelsWithSpecificAttributes(self,attributesList):
        return self.storage.GetListWithSpecificAttributes("MODEL",attributesList)

    def CreateModel(self, dataset, distanceName):
        name = f'{dataset.Name}-{distanceName}'
        modelsList = self.__GetAllModelsNamesList()
        if name in modelsList:
            raise Exception(f"Model named {name} exist")
        dataSet = dataset
        distanceFunction = modular_distance_utils.get_function_by_name(distanceName)
        #mean = dataSet.MeanValues
        fieldsData = dataSet.getAttributesTypesAndValuesList()
        types = [True if d['type'] == 'categorical' else False for d in fieldsData]
        data = np.array(dataSet.Data)
        hp, k = preProcess(data, fieldsData, distanceFunction)
        print("done preprocess - start k means")
        try:
            clusterer = KMeansClusterer(num_means=k,
                distance=distanceFunction,
                repeats=1,
                #mean_values=mean,
                type_of_fields=types,
                hyper_params=hp)
        except Exception as e:
            print(f"Error {e}")
            traceback.print_exc()
            raise e


        print ('done k means start training')
        
        trained = 0
        while trained == 0:
            try:
                clusterer.cluster(data)
                trained =1
            except Exception as e:
                print(f"Error {e}")
                traceback.print_exc()
                trained = 0
        print ('done training')
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
        dataset.addNewModel({
            'name':modelJson['name'],
            'wcss_score':modelJson['wcss_score_of_model']
        })

        print("########################## MODEL FINISHED#############################")

    def GetModel(self, modelName):
        modelsList = self.__GetAllModelsNamesList()
        if modelName not in modelsList:
            raise Exception(f"Model named {modelName} Does not exist")
        return Model(modelName)

    def DeleteModel(self, modelName,dataset):
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
    
    def GetListForManager(self):
        return self.storage.GetListWithSpecificAttributes("MODEL",['name','timestamp','wcss_score_of_model','datasetName','function'])
    
    def GetListOfModelsWithDistanceFunction(self,distanceFunctionName):
        models = self.__GetAllModelsWithSpecificAttributes(['name','function'])
        names = [model["name"] for model in models if model["function"] == distanceFunctionName]
        return names
