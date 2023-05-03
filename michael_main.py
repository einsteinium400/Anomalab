import pandas as pd
from model.DatasetPreProcessor import DatasetPreProcessor
# creating a data frame
df = pd.read_csv("./datasets/german_credit_data_michael_test.csv")

dfProcesor = DatasetPreProcessor()
newdf, values = dfProcesor.dataSetPreProcess('test',df)
# print(newdf)