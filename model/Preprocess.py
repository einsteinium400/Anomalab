import pandas as pd
from model.GeneticAlgorithm import genetic_algorithm
import numpy as np
from itertools import permutations

# def get_max_domain_size(lst):
#     return len(set(lst))


def create_array(i, len, v):
    # Initialize the array with 0
    arr = [0] * (len)
    # Set the value at index `i` to `v`
    arr[i] = v
    return arr

def max_combination(vectors, func, params_dict, type_of_fields, fieldsData):
    #fields data: [{'name': 'Unnamed: 0', 'type': 'numeric'}, {'name': 'Age', 'type': 'numeric'}, {'name': 'Sex', 'type': 'categorical', 'values': {'0': 'female', '1': 'male'}}, {'name': 'Job', 'type': 'numeric'}, {'name': 'Housing', 'type': 'categorical', 'values': {'0': 'free', '1': 'own', '2': 'rent'}}, {'name': 'Saving accounts', 'type': 'categorical', 'values': {'0': 'little', '1': 'moderate', '2': 'quite rich', '3': 'rich', '4': nan}}, {'name': 'Checking account', 'type': 'categorical', 'values': {'0': 'little', '1': 'moderate', '2': nan}}, {'name': 'Credit amount', 'type': 'numeric'}, {'name': 'Duration', 'type': 'numeric'}, {'name': 
    print("fields data:", fieldsData)
    # exit()
    max_vals_array=[float('-inf')]*len(type_of_fields)
    for i in range(len(type_of_fields)):
        if type_of_fields[i]:
            possible_features=list(fieldsData[i]['values'].keys())
            # Generate all permutations of two values
            perms = permutations(possible_features, 2)
            # Sort each permutation and remove duplicates
            unique_perms = list(set(tuple(sorted(p)) for p in perms))
            for permutation in unique_perms:
                vec1=create_array(i, len(type_of_fields), permutation[0])
                vec2=create_array(i, len(type_of_fields), permutation[1])
                result = func(vec1, vec2, type_of_fields, params_dict)

                # Update max_value if the current result is greater
                if result > max_vals_array[i]:
                    max_vals_array[i] = result 
        else:
            max_vals_array[i]=10

    print('max vals: ',max_vals_array)
    #exit()
    return max_vals_array


    # # Get the number of vectors and the length of the first element
    # num_vectors, n = vectors.shape[0], vectors[0].shape[0]

    # # Initialize an array to store the maximum values
    # max_values = np.empty(n)

    # # Iterate through all possible indices
    # for i in range(n):
    #     # Initialize max_value with the minimum possible value
    #     max_value = float('-inf')

    #     # Iterate through all combinations of first elements at the current index
    #     for j in range(num_vectors):
    #         for k in range(j + 1, num_vectors):
    #             print("checking feature", i, k)
    #             # Calculate the result of applying the function to the pair of first elements at the current index
                
    #             vec1=create_array(i, vectors[0].shape[0], vectors[j][i])
    #             vec2=create_array(i, vectors[0].shape[0], vectors[k][i])
    #             result = func(vec1, vec2, type_of_fields, params_dict)

    #             # Update max_value if the current result is greater
    #             if result > max_value:
    #                 max_value = result

    #     # Store the maximum value for the current index
    #     max_values[i] = max_value

    # # Convert the max_values numpy array to a list of integers
    # max_values = max_values.astype(int).tolist()

    # return max_values

def preProcess(vectors, fieldsData, distance_function):
    print (fieldsData)
    type_of_fields = [True if d['type'] == 'categorical' else False for d in fieldsData]

    params_dict = dict()
    df = pd.DataFrame(vectors)
    domain_sizes = df.nunique()
    params_dict["domain sizes"] = domain_sizes.tolist()
    # params_dict["max_domain_size"] = df.applymap(get_max_domain_size).max().max()

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
    print("frequency dictionary done")

    params_dict["frequencies"] = frequencies_dict
    print("freqs are:", params_dict["frequencies"])
    #exit()
    params_dict["minimum_freq_of_each_attribute"] = minimal_frequencies_dict
    params_dict["theta"] = 0.1

    # todo: get the k value using hamming
    k = 3

    # activate the genetic algorithm
    print (f'start genetic')
    z = df.nunique().max() # max domain size

    theta1, theta2, betha, gamma = genetic_algorithm(params_dict, distance_function, k, vectors, type_of_fields, z)
    print("done genetic")
    params_dict["theta1"] = theta1  # 3
    params_dict["theta2"] = theta2  # 10
    params_dict["betha"] = betha  # 0.05
    params_dict["gamma"] = gamma  # 0.01

    # calculate max possible distance for every feature, in order to normalize wcss
    # normalize_values=dict()
    normalize_values=max_combination(vectors, distance_function, params_dict, type_of_fields, fieldsData)
    if 0 in normalize_values:
        print(normalize_values)
        exit()
    params_dict["normalize_values"]=normalize_values
    
    print("dict is:", params_dict, k)

    # exit()
    return params_dict, k

