from controller.DatasetController import DatasetController
from controller.DistanceFunctionController import DistanceFunctionController
from controller.ModelController import ModelController

distanceController = DistanceFunctionController()
datasetController = DatasetController()
modelController = ModelController()
# add function flow
# distanceController.add_function('./distanceFunctions/MixedDistance.py')
# data = datasetController.GetDataset('german_20')
# modelController.CreateModel(data,'MixedDistance')
# distanceController.delete_function('MixedDistance')

#  Add dataset flow 
try:
    datasetController.DeleteDataset("test")
except:
    pass
datasetController.CreateDataset("test","./datasets/german_credit_data_michael_test.csv")
print("end")