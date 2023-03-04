import numpy

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
#
# modelsController.CreateModel("lympho-Hamming",dataSet,"Hamming")
# model = modelsController.GetModel("lympho-Hamming")
# print(model.JsonData)

print(modelsController.GetAllModelsNamesList())
print(modelsController.GetAllInstances())


