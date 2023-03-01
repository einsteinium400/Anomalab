import json
from abc import abstractmethod
import os
import uuid
import pandas as pd
import time
from sklearn import preprocessing




class DatasetPreProcessor:
    def dataSetPreProcess(self,name,csvFilePath):
        featuresInfo =[]
        df = pd.read_csv(csvFilePath)
        cols = df.columns
        num_cols = df._get_numeric_data().columns
        for col in cols:
            featuresInfo.append ( {
                "name":col,
                "type":"numeric"
            })
        categorical_cols = list(set(cols) - set(num_cols))

        for col in categorical_cols:
            le = preprocessing.LabelEncoder()
            df[col] =le.fit_transform(df[col])
            le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
            inv_map = {v: k for k, v in le_name_mapping.items()}
            featuresInfo.append ( {
                "name":col,
                "type":"categorical",
                "values":inv_map,
                "reversedValues":le_name_mapping
            })
        return df,featuresInfo