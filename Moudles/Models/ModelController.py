from Moudles.Storage.StorageFactory import StorageFactory
from Moudles.Models.Model import Model


class ModelsController:
    operationFactory = StorageFactory()
    storage = operationFactory.CreateOperationItem()
    def CreateModel(self,modelJson):
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
