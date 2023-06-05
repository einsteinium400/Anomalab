import multiprocessing

from controller.DatasetController import DatasetController
from controller.DistanceFunctionController import DistanceFunctionController
from controller.ModelController import ModelController

from colorama import Fore, Style

def print_status_message(status, text):
    if status == 'S':
        print(f"{Fore.GREEN}Success: {text}{Style.RESET_ALL}")
    elif status == 'F':
        print(f"{Fore.RED}Fail: {text}{Style.RESET_ALL}")
    else:
        print("Invalid status provided. Please use 'S' or 'F'.")


distanceController = DistanceFunctionController()
datasetController = DatasetController()
modelController = ModelController()
# add function flow
# distanceController.add_function('./distanceFunctions/MixedDistance.py')
# datasetController.CreateDataset("german_20",'./datasets/german_credit_data_michael_test.csv')
# data = datasetController.GetDataset('german_20')
# modelController.CreateModel(data,'Statistic')
# model = modelController.GetModel('german_20-Statistic')
# print(model.ClusterValues)
# distanceController.delete_function('MixedDistance')
# data= datasetController.GetDataset('german_20')
# print(data.BestModel)

#  Add dataset flow 
try:
    datasetController.DeleteDataset("test-unique-fillna")
except:
    pass
try:
    datasetController.DeleteDataset("test-common-fillna")
except:
    pass
try:
    datasetController.DeleteDataset("test-no-fill")
except:
    pass
datasetController.CreateDataset("test","./datasets/german_credit_data_michael_test.csv")
# datasetController.CreateDataset("test-no-fill","./datasets/iris-wcss-test.csv")
s = datasetController.GetDataset("test-unique-fillna")
print(s.getAttributesTypesAndValuesList())

print(datasetController.GetAttributesList("test-unique-fillna"))
datasetController.DeleteDataset("test-unique-fillna")
datasetController.DeleteDataset("test-common-fillna")
print("end")


# Job queue tester

# from controller.JobController import JobController
# import time

# def infinite_loop():
#     while True:
#         print("Running...")
#         time.sleep(1)
# if __name__ == '__main__':
#     # Create an instance of JobController
#     job_controller = JobController()
    
#     # Define a new job by adding the infinite_loop function
#     job_controller.add_job(infinite_loop)

#     time.sleep(10)  # Let the job run for 5 seconds
#     # Stop the job
#     job_controller.stop_all_running_jobs()

#     print("Job stopped.")

