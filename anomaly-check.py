# Controllers import
from controller.DistanceFunctionController import DistanceFunctionController
from controller.DatasetController import DatasetController
from controller.ModelController import ModelController
from controller.AnomalyDetectionController import checkSampleForAnomaly
import pandas as pd
import csv
import os

distaneFunction = "Statistic"

datasetCtrler = DatasetController()
modelCtrler = ModelController()
distCtrler = DistanceFunctionController()

def append_list_to_csv(file_path,headears, data_list):
    try:
        file_exists = os.path.exists(file_path)
        with open(file_path, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            if not file_exists:
                csv_writer.writerow(headears)  # Add headers if file is newly created
            csv_writer.writerow(data_list)
    except Exception as e:
        print("Error:", e)

def append_data_to_file(file_path,headear, data):
    try:
        file_exists = os.path.exists(file_path)
        with open(file_path, 'a', newline='') as file:
            if not file_exists:
                file.write(headear)  # Add headers if file is newly created
            file.write(data)
    except Exception as e:
        print("Error:", e)




def make_cluster(datasetName,datasetCsv,iteration):
    try:
        dataset1 = datasetCtrler.GetDataset(f"{datasetName}-{iteration}")
        # model1 = modelCtrler.GetModel(f"{datasetName}-1")
        datasetCtrler.DeleteDataset(f"{datasetName}-{iteration}")
        modelCtrler.DeleteModel(f"{datasetName}-{iteration}",dataset1)
    except Exception as e:
        print(e)
    try:
        print(f"Making dataset {datasetName}-{iteration}")
        print(f"with csv {datasetCsv}")
        datasetCtrler.CreateDataset(f"{datasetName}-{iteration}",datasetCsv)
        dataset1 = datasetCtrler.GetDataset(f"{datasetName}-{iteration}")
        modelCtrler.CreateModel(dataset1,distaneFunction)
        model1 = modelCtrler.GetModel(f"{datasetName}-{iteration}-{distaneFunction}")
        print(f"Created model {model1.Name}")
        rawdata1Ins= dataset1.getRawData()
        rawData1 = rawdata1Ins
        append_data_to_file("datasets-checkin/outputs/results.txt","Iteration   |   Rows    | Shiloutte\n",f"{iteration}   | {len(rawData1)}    | {model1.Silhouette}\n")
        
        for row in rawData1:
            if checkSampleForAnomaly(model1,row)['anomaly']:
                pass
            else:
                append_list_to_csv(f"datasets-checkin/{datasetName}-{iteration+1}.csv",dataset1.FeatureNames,dataset1.sampleDecyper(row))

    except Exception as e:
        print(e)

    # Cleanup Phase
    try:
        dataset1 = datasetCtrler.GetDataset(f"{datasetName}-1")
        model1 = modelCtrler.GetModel(f"{datasetName}-1")
        modelCtrler.DeleteModel(f"{datasetName}-1",dataset1)
        datasetCtrler.DeleteDataset(f"{datasetName}-1")
    except:
        pass


datasetName= "testing-Dataset"
datasetCsv = "datasets-checkin/adult1000.csv"

make_cluster(datasetName,datasetCsv,1)
for i in range (2,11):
    make_cluster(f"{datasetName}",f"datasets-checkin/{datasetName}-{i}.csv",i)