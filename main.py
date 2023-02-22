from Moudles.Databases.DatasetsController import DatasetsController
from Moudles.Models.ModelController import ModelsController
from Moudles.Users.UsersController import UsersController

userController = UsersController()
databaseController = DatasetsController()
modelsController = ModelsController()

userController.RegisterUser("noam", "123", 0)
userController.RegisterUser("dana", "456", 0)
print(userController.GetAllUsers())
print(userController.DeleteUser("noam"))
print(userController.GetAllUsers())
print("attempt login to user dana first pass 123 and then 456")
print(userController.LoginUser("dana", "123"))
print(userController.LoginUser("dana", "456"))

dataSet1Path= "dataset1/dataWithHeaders.data"
dataSet2Path= "dataset2/adult.data2"
databaseController.CreateDataset("lympho",dataSet1Path)
databaseController.CreateDataset("adults",dataSet2Path)
dataSet = databaseController.GetDataset("adults")
print(dataSet.FeatureNames)

