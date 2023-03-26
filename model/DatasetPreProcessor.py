from sklearn import preprocessing


class DatasetPreProcessor:
    def dataSetPreProcess(self,name,df):
        featuresInfo =[]
        cols = df.columns
        print (f'cols are: {cols}')
        num_cols = df._get_numeric_data().columns
        for col in num_cols:
            featuresInfo.append ({
                "name":col,
                "type":"numeric"
            })
        categorical_cols = list(set(cols) - set(num_cols))
        for col in categorical_cols:
            le = preprocessing.LabelEncoder()
            df[col] =le.fit_transform(df[col])
            le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
            inv_map = {str(v): k for k, v in le_name_mapping.items()}

            featuresInfo.append ( {
                "name":col,
                "type":"categorical",
                "values":inv_map
            })
        print (featuresInfo)
        return df,featuresInfo