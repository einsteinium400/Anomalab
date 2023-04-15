import pandas as pd
from model.GeneticAlgorithm import genetic_algorithm
import numpy as np

def max_combination(vectors, func, params_dict, type_of_fields):
    # Convert the list of numpy arrays to a 2D numpy array
    vectors = np.array(vectors)

    # Get the number of vectors and the length of the first element
    num_vectors, n = vectors.shape[0], vectors.shape[1]

    # Initialize an array to store the maximum values
    max_values = np.empty(n)

    # Iterate through all possible indices
    for i in range(n):
        # Initialize max_value with the minimum possible value
        max_value = float('-inf')

        # Iterate through all combinations of first elements at the current index
        for j in range(num_vectors):
            for k in range(j + 1, num_vectors):
                # Calculate the result of applying the function to the pair of first elements at the current index
                result = func(vectors[j, i], vectors[k, i], type_of_fields, params_dict)

                # Update max_value if the current result is greater
                if result > max_value:
                    max_value = result

        # Store the maximum value for the current index
        max_values[i] = max_value

    # Convert the max_values numpy array to a list of integers
    max_values = max_values.astype(int).tolist()

    return max_values

def preProcess(vectors, type_of_fields, distance_function):
    params_dict = dict()
    df = pd.DataFrame(vectors)
    domain_sizes = df.nunique()
    params_dict["domain sizes"] = domain_sizes.tolist()

    # make a dict of frequencies={attribute1:{value1:fre1, value2:freq,   }, 1:{}... ak}

    frequencies_dict = dict()
    minimal_frequencies_dict = dict()
    for col in df.columns:

        # if type of fields is categorical
        if type_of_fields[col]:
            value_counts = df[col].value_counts()
            col_dict = value_counts.to_dict()
            string_dict = {str(key): value for key, value in col_dict.items()}
            frequencies_dict[str(col)] = string_dict
            minimal_frequencies_dict[str(col)] = min(col_dict.values())

        # if type of fields is numeric, frequencies is not relevant
        else:
            frequencies_dict[str(col)] = dict()
            minimal_frequencies_dict[str(col)] = dict()

    params_dict["frequencies"] = frequencies_dict
    params_dict["minimum_freq_of_each_attribute"] = minimal_frequencies_dict
    params_dict["theta"] = 0.1

    # todo: get the k value using hamming
    k = 3

    # activate the genetic algorithm
    theta1, theta2, betha, gamma = genetic_algorithm(params_dict, distance_function, k, vectors, type_of_fields)

    params_dict["theta1"] = theta1  # 3
    params_dict["theta2"] = theta2  # 10
    params_dict["betha"] = betha  # 0.05
    params_dict["gamma"] = gamma  # 0.01

    # calculate max possible distance for every feature, in order to normalize wcss
    # normalize_values=dict()
    params_dict["normalize_values"]=max_combination(vectors, distance_function, params_dict, type_of_fields)

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~dict is:", params_dict, k)


    return params_dict, k
