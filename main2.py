from controller.DatasetController import DatasetController
from controller.DistanceFunctionController import DistanceFunctionController
from controller.ModelController import ModelController

distanceController = DistanceFunctionController()
datasetController = DatasetController()
modelController = ModelController()
# distanceController.add_function('./distanceFunctions/MixedDistance.py')
# data = datasetController.GetDataset('german_20')
# modelController.CreateModel(data,'MixedDistance')
distanceController.delete_function('MixedDistance')
print("end")