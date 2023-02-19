import os
import pandas as pd
from dotenv import load_dotenv

from Moudles.Databases.Dataset import Dataset
from Moudles.Storage.StorageFactory import StorageFactory
from Moudles.Storage.OperationsLocal import OperationsLocal
from Moudles.Users.User import User
from Moudles.Users.UsersController import UsersController

load_dotenv()
MY_ENV_VAR = os.getenv('STORAGE')
# df1 = pd.read_csv('dataset2/adult.data2')

# dataSet1 = Dataset('adult', df1)
# # dataSet1 = Dataset('adult')
# print(dataSet1._id)
# print(dataSet1._name)
# print(dataSet1._timeStamp)
# print(dataSet1._bestModel)
# print(dataSet1._featureNames)
# dataSet1.AddImportantFeature('age')
# print(dataSet1._importantFeatures)
# # print(dataSet1._jsonData)

df2 = pd.read_csv('dataset1/dataWithHeaders.data')
print(df2.values.tolist())

dataSet2 = Dataset('lympho', df2)
# # dataSet2 = Dataset('lympho')
print(dataSet2._id)
print(dataSet2._name)
print(dataSet2._timeStamp)
print(dataSet2._bestModel)
print(dataSet2._featureNames)
dataSet2.AddImportantFeature('age')
print(dataSet2._importantFeatures)
print(dataSet2._jsonData)

operationFactory = StorageFactory()
saver = operationFactory.CreateOperationItem()
# print(saver.getPath())
# saver.Save(dataSet2._name, dataSet2._jsonData, "DATASET")
data = saver.Load(dataSet2._name, "DATASET")
print(data)

# myuser = User("mishasoni","456","regular")
# myuser.SaveUser()
# print(myuser.VerifyPassword("123"))
# print(myuser.VerifyPassword("456"))
# saver.Delete("mishasoni","USER")

# userController = UsersController()
# userController.RegisterUser("noam","123",0)
# userController.RegisterUser("misha","456",0)
# print((userController.GetAllUsers()))
# print(userController.DeleteUser("misha"))
# print(userController.LoginUser("noam","123"))
# print(userController.LoginUser("misha","123"))

