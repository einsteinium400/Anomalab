import pandas as pd


def preProcess(vectors):
    params_dict = dict()
    df = pd.DataFrame(vectors)
    domain_sizes = df.nunique()
    params_dict["domain sizes"] = domain_sizes.tolist()
    params_dict["theta"] = 0.1
    params_dict["theta1"] = 3
    params_dict["theta2"] = 10
    params_dict["betha"] = 0.05
    params_dict["gamma"] = 0.01

    # make a dict of frequencies={attribute1:{value1:fre1, value2:freq,   }, 1:{}... ak}

    frequencies_dict = dict()
    minimal_frequencies_dict = dict()
    for col in df.columns:
        value_counts = df[col].value_counts()
        col_dict = value_counts.to_dict()
        frequencies_dict[col] = col_dict
        minimal_frequencies_dict[col] = min(col_dict.values())

    params_dict["frequencies"] = frequencies_dict
    params_dict["minimum_freq_of_each_attribute"] = minimal_frequencies_dict
    print(params_dict)

    return params_dict
