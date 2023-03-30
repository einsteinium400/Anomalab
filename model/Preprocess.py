import pandas as pd
from model.GeneticAlgorithm import genetic_algorithm

def preProcess(vectors, type_of_fields, distance_function):
    params_dict = dict()
    df = pd.DataFrame(vectors)
    domain_sizes = df.nunique()
    params_dict["domain sizes"] = domain_sizes.tolist()


    # make a dict of frequencies={attribute1:{value1:fre1, value2:freq,   }, 1:{}... ak}

    frequencies_dict = dict()
    minimal_frequencies_dict = dict()
    for col in df.columns:

        #if type of fields is categorical
        if type_of_fields[col]:
            value_counts = df[col].value_counts()
            col_dict = value_counts.to_dict()
            string_dict = {str(key): value for key, value in col_dict.items()}
            frequencies_dict[str(col)] = string_dict
            minimal_frequencies_dict[str(col)] = min(col_dict.values())
        
        #if type of fields is numeric, frequencies is not relevant 
        else:
            frequencies_dict[str(col)]=dict()
            minimal_frequencies_dict[str(col)]=dict()

    params_dict["frequencies"] = frequencies_dict
    params_dict["minimum_freq_of_each_attribute"] = minimal_frequencies_dict
    params_dict["theta"] = 0.1

    #todo: get the k value
    k= 3

    # activate the genetic algorithm
    theta1, theta2, betha, gamma = genetic_algorithm(params_dict, distance_function, k, vectors, type_of_fields)

    params_dict["theta1"] = theta1#3
    params_dict["theta2"] = theta2#10
    params_dict["betha"] = betha#0.05
    params_dict["gamma"] = gamma#0.01
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~dict is:", params_dict, k)
    return params_dict, k


