from Moudles.Databases.DatasetPreProcessor import DatasetPreProcessor
from Moudles.Databases.DatasetsController import DatasetsController
from Moudles.Models.ModelController import ModelsController
from Moudles.Users.UsersController import UsersController

import pymongo

userController = UsersController()
databaseController = DatasetsController()
modelsController = ModelsController()



# import base64
# funcData = 0
# with open("Moudles/Functions/Euclidian.py", "rb") as f:
#     encodedZip = base64.b64encode(f.read())
#     funcData = encodedZip
# print(funcData)
# CLIENT = pymongo.MongoClient("mongodb+srv://anomalab:8EVoc8M9fK387636@anomalab.verl4tn.mongodb.net/?retryWrites=true&w=majority")
# PROJECTDB=CLIENT["AnomaLab"]
# collection = PROJECTDB["functions"]
# data = {"name":"function1","data":funcData}
# collection.insert_one(data)
# print("extract and write to file")
# decodedFile = collection.find_one({"name":"function1"})
# decoded = base64.b64decode(decodedFile['data'])
# filename = f"testFile.py"
# with open(filename, "w") as file:
#     file.write(decoded.decode("utf-8"))


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
# dataSet = databaseController.GetDataset("adults")
# print(dataSet.FeatureNames)
# print(dataSet.Data)

dfProccesor = DatasetPreProcessor()
dataSet2Path= "dataset2/adult.data2"
dfProccesor.dataSetPreProcess("adults",dataSet2Path)