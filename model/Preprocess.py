import pandas as pd
from model.GeneticAlgorithm import genetic_algorithm
import numpy as np
from itertools import permutations
from kneed import KneeLocator
import matplotlib.pyplot as plt
from distanceFunctions.Hamming import Hamming as hm
from model.KMeanClusterer import KMeansClusterer

def apply_elbow_method(fields_data, vectors):
    wcss=[]

    for i in range(2, 6):
        model = KMeansClusterer(hyper_params=dict(), distance=hm, num_means=int(i), type_of_fields=fields_data)
        model.cluster(vectors)
        wcss.append(model.get_wcss())
        print (f'elbow for {i} clusters wcss is : {model.get_wcss()}')

    kneedle = KneeLocator(range(2, 6), wcss, curve='convex', direction='decreasing')
    elbow_point = kneedle.elbow
    if not isinstance(elbow_point,int):
        elbow_point=3
        print("could not generate elbow point, use default value")
    print(elbow_point)
    return elbow_point

def create_array(i, len, v):
    # Initialize the array with 0
    arr = [0] * (len)
    # Set the value at index `i` to `v`
    arr[i] = v
    return arr

def max_combination(func, params_dict, type_of_fields, fieldsData):
    max_vals_array = [float('-inf')] * len(type_of_fields)
    for i in range(len(type_of_fields)):
        if type_of_fields[i]:
            possible_features = list(fieldsData[i]['values'].keys())
            # Generate all permutations of two values
            perms = permutations(possible_features, 2)
            # Sort each permutation and remove duplicates
            unique_perms = list(set(tuple(sorted(p)) for p in perms))
            for permutation in unique_perms:
                vec1 = create_array(i, len(type_of_fields), permutation[0])
                vec2 = create_array(i, len(type_of_fields), permutation[1])
                print ('cat vec1: ', vec1)
                print ('cat vec2: ', vec2)
                result = func(vec1, vec2, type_of_fields, params_dict)
                print ('cat distance: ', result)
                # Update max_value if the current result is greater
                if result > max_vals_array[i]:
                    max_vals_array[i] = result
        else:
            vec1 = create_array(i, len(type_of_fields), fieldsData[i]['max'])
            vec2 = create_array(i, len(type_of_fields), fieldsData[i]['min'])
            print ('num vec1: ', vec1)
            print ('num vec2: ', vec2)
            result = func(vec1, vec2, type_of_fields, params_dict)
            print ('num distance: ', result)
            max_vals_array[i] = result
            #print("max_vals_array[i]", max_vals_array[i])
            #max_vals_array[i] = fieldsData[i]['max']
    print("max_vals_array: ", max_vals_array)
    return max_vals_array

def preProcess(vectors, fieldsData, distance_function):
    type_of_fields = [True if d['type'] == 'categorical' else False for d in fieldsData]
    params_dict = dict()
    df = pd.DataFrame(vectors)
    domain_sizes = df.nunique()
    params_dict["domain sizes"] = domain_sizes.tolist()
    # params_dict["max_domain_size"] = df.applymap(get_max_domain_size).max().max()
    frequencies_dict = dict()
    minimal_frequencies_dict = dict()
    for i in range(len(fieldsData)):
        if fieldsData[i]['type'] == 'categorical':
            frequencies_dict[str(i)] = fieldsData[i]['frequencies'] ##NOAM DELETE FIX DANA~~~~~~@~@##$#$!!@##$!~@~!@!#$$
            minimal_frequencies_dict[str(i)] = min(frequencies_dict[str(i)].values())
        else:
            frequencies_dict[str(i)] = dict()
            minimal_frequencies_dict[str(i)] = dict()

    params_dict["frequencies"] = frequencies_dict
    params_dict["minimum_freq_of_each_attribute"] = minimal_frequencies_dict
    params_dict["theta"] = 0.1
    k = apply_elbow_method(fieldsData, vectors)
    # activate the genetic algorithm
    z = df.nunique().max()  # max domain size

    theta1, theta2, betha, gamma = genetic_algorithm(params_dict, distance_function, k, vectors, type_of_fields, z)
    params_dict["theta1"] = theta1  # 3
    params_dict["theta2"] = theta2  # 10
    params_dict["betha"] = betha  # 0.05
    params_dict["gamma"] = gamma  # 0.01
    print('done genetics: ', params_dict)
    # calculate max possible distance for every feature, in order to normalize wcss
    # normalize_values=dict()
    normalize_values = max_combination(distance_function, params_dict, type_of_fields, fieldsData)
    if 0 in normalize_values:
        print(normalize_values)
        exit()
    params_dict["normalize_values"] = normalize_values

    print("dict is:", params_dict, k)

    # exit()
    print("params_dict", params_dict)
    return params_dict, k
