from sklearn import preprocessing
import pandas as pd
import faker
COMMON_MISSING_VALUES=['NA']

class DatasetPreProcessor:
    def dataSetPreProcess(self,name,df):
        # Replace common missing values conventions with NaN
        for item in COMMON_MISSING_VALUES:
            df = df.replace(item, pd.NaT)
        featuresInfo =[]
        print(df)
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

        # # Add unique string to dataframe in NA for Data imputation
        # fake = faker.Faker()
        # # Loop over each column and fill missing values with unique strings
        # for col in categorical_cols:
        #     # Get the locations of missing values in the column
        #     missing_mask = df[col].isnull()
        #     missing_locs = missing_mask[missing_mask].index.tolist()

        #     # Generate unique strings with prefix and fill missing values
        #     unique_strings = ["fillna-" + fake.text() for _ in range(len(missing_locs))]
        #     df.loc[missing_locs, col] = unique_strings
        

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
        print(df)
        print (featuresInfo)
        return df,featuresInfo