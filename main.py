import numpy

from Moudles.Anomaly.AnomalyPredict import checkSampleForAnomaly
from Moudles.Databases.DatasetPreProcessor import DatasetPreProcessor
from Moudles.Databases.DatasetsController import DatasetsController
from Moudles.Models.ModelController import ModelsController
from Moudles.Users.UsersController import UsersController
from distance_functions_controller import Distance_Functions_Controller
import traceback

import pymongo



userController = UsersController()
databaseController = DatasetsController()
modelsController = ModelsController()
functionController = Distance_Functions_Controller()

# functionController.add_function("./Moudles/Functions/MixedDistance.py")

# userController.RegisterUser("reg", "reg", 0)
# userController.RegisterUser("analyst", "analyst", 1)
# userController.RegisterUser("admin", "admin", 2)
# print(userController.GetAllUsers())
# print(userController.DeleteUser("noam"))
# print(userController.GetAllUsers())
# print("attempt login to user dana first pass 123 and then 456")
# print(userController.LoginUser("dana", "123"))
# print(userController.LoginUser("dana", "456"))
#
# dataSet1Path= "dataset1/dataWithHeaders.data"
# dataSet2Path= "dataset2/adult.data2"
# databaseController.CreateDataset("lympho",dataSet1Path)
# databaseController.CreateDataset("adults",dataSet2Path)
# dataSet2 = databaseController.GetDataset("adults")
# print(dataSet.FeatureNames)
# print(dataSet.Data)

# dataSet = databaseController.GetDataset("lympho")
# modelsController.CreateModel("lympho-MixedDistance",dataSet,"MixedDistance")
# model = modelsController.GetModel("lympho-MixedDistance")
# print(model.JsonData)
# dataSample = [4, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 4, 8, 1, 1, 2, 2, 3]
# print(model.classify_vectorspace(dataSample))
# checkSampleForAnomaly(model,dataSample)
#


# print(modelsController.GetAllModelsNamesList())
# for model in modelsController.GetAllInstances():
#     print(model)

# print(modelsController.GetModelsStatus())


# modelsController.CreateModel("lympho2-MixedDistance",dataSet,"MixedDistance")
# model = modelsController.GetModel("lympho2-MixedDistance")
# print(model.JsonData)
modelsController.DeleteModel("lympho-MixedDistance")
