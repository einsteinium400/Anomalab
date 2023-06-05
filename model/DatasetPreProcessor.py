import uuid
from sklearn import preprocessing
import pandas as pd
import faker




def fill_with_most_frequent(dataframe, columns):
    for column in columns:
        most_frequent = dataframe[column].mode()[0]
        dataframe[column].fillna(most_frequent, inplace=True)
    return dataframe

def create_unique_string(dataframe, columns):
    # Loop over each column and fill missing values with unique strings
    for col in columns:
        # Get the locations of missing values in the column
        missing_mask = dataframe[col].isnull()
        missing_locs = missing_mask[missing_mask].index.tolist()

        # Generate unique strings with prefix and fill missing values
        unique_strings = [f"filledNa-{str(uuid.uuid4())}" for _ in range(len(missing_locs))]
        dataframe.loc[missing_locs, col] = unique_strings
    # for column in columns:
    #     dataframe[column] = dataframe[column].fillna('filledNa-' + dataframe[column].astype(str))

def apply_swap_function(dataframe, columns, function_name):
    switch_case = {
        'COMMON': fill_with_most_frequent,
        'UNIQUE': create_unique_string
    }

    function = switch_case.get(function_name)
    dataframe = function(dataframe, columns)

class DatasetPreProcessor:
    def dataSetPreProcess(self,name,df, method = 'NONE'):
        featuresInfo =[]
        # Extract columns names
        cols = df.columns

        print (f'cols are: {cols}')
        # Takes only numerical colums
        num_cols = df._get_numeric_data().columns

        for col in num_cols:
            # Fills missing values with avreage
            df[col] = df[col].fillna(df[col].mean())
            featuresInfo.append({
                "name":col,
                "type": "numeric",
                "min":float(df[col].min()),
                "max":float(df[col].max()),
                "stdDev":float(df[col].std())
            })
        categorical_cols = list(set(cols) - set(num_cols))
        if (method != "NONE"):
            apply_swap_function(dataframe=df,columns=categorical_cols,function_name=method)

        for col in categorical_cols:
            le = preprocessing.LabelEncoder()
            # Normalizes categorical values
            df[col] =le.fit_transform(df[col])
            # Takes out the normalization table
            le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
            # Inverts the normalization table
            inv_map = {str(v): k for k, v in le_name_mapping.items()}
            # Counts values freq
            value_counts = {str(k): v for k, v in df[col].value_counts().to_dict().items()}
            # Appends it to a list
            featuresInfo.append ( {
                "name":col,
                "type":"categorical",
                "values":inv_map,
                "frequencies": value_counts
            })
        
        return df,featuresInfo