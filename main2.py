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
print("end")