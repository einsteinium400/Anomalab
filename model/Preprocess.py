import pandas as pd
from model.GeneticAlgorithm import genetic_algorithm
import numpy as np
from itertools import permutations
from kneed import KneeLocator
import matplotlib.pyplot as plt
from distanceFunctions.Hamming import Hamming as hm
from model.KMeanClusterer import KMeansClusterer
from time import sleep
import random

def apply_elbow_method(fields_data, vectors):
    wcss=[]
    for i in range(1, 10):
        print("round number", i)
        model = KMeansClusterer(hyper_params=dict(), distance=hm, num_means=int(i), type_of_fields=fields_data)
        model.cluster(vectors)
        wcss.append(model.get_wcss())
        print("done round", i)
    kneedle = KneeLocator(range(1, 10), wcss, curve='convex', direction='decreasing')
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
                result = func(vec1, vec2, type_of_fields, params_dict)

                # Update max_value if the current result is greater
                if result > max_vals_array[i]:
                    max_vals_array[i] = result
        else:
            max_vals_array[i] = fieldsData[i]['max']
    return max_vals_array


def preProcess(vectors, fieldsData, distance_function):
    type_of_fields = [True if d['type'] == 'categorical' else False for d in fieldsData]
    params_dict = dict()
    df = pd.DataFrame(vectors)
    domain_sizes = df.nunique()
    params_dict["domain sizes"] = domain_sizes.tolist()
    # params_dict["max_domain_size"] = df.applymap(get_max_domain_size).max().max()

    # make a dict of frequencies={attribute1:{value1:fre1, value2:freq,   }, 1:{}... ak}
    ##[
    #   {
    #       'name': 'Unnamed: 0', 
    #       'type': 'numeric',
    #       'min': 0,
    #       'max': 999
    #   }, 
    #   {
    #       'name': 'Age',
    #       'type': 'numeric',
    #       'min': 19,
    #       'max': 75
    #   },
    #   {
    #       'name': 'Sex',
    #       'type': 'categorical',
    #       'values': {
    #           '0': 'female',
    #           '1': 'male'
    #       }, 
    #       'frequencies': {
    #           '1': 690,
    #           '0': 310
    #       }
    #   },
    #  {'name': 'Job', 'type': 'numeric', 'min': 0, 'max': 3}, {'name': 'Housing', 'type': 'categorical', 'values': {'0': 'free', '1': 'own', '2': 'rent'}, 'frequencies': {'1': 713, '2': 179, '0': 108}}, {'name': 'Saving accounts', 'type': 'categorical', 'values': {'0': 'little', '1': 'moderate', '2': 'quite rich', '3': 'rich', '4': nan}, 'frequencies': {'0': 603, '4': 183, '1': 103, '2': 63, '3': 48}}, {'name': 'Checking account', 'type': 'categorical', 'values': {'0': 'little', '1': 'moderate', '2': 'rich', '3': nan}, 'frequencies': {'3': 394, '0': 274, '1': 269, '2': 63}}, {'name': 'Credit amount', 'type': 'numeric', 'min': 250, 'max': 18424}, {'name': 'Duration', 'type': 'numeric', 'min': 4, 'max': 72}, {'name': 'Purpose', 'type': 'categorical', 'values': {'0': 'business', '1': 'car', '2': 'domestic appliances', '3': 'education', '4': 'furniture/equipment', '5': 'radio/TV', '6': 'repairs', '7': 'vacation/others'}, 'frequencies': {'1': 337, '5': 280, '4': 181, '0': 97, '3': 59, '6': 22, '2': 12, '7': 12}}]
    frequencies_dict = dict()
    minimal_frequencies_dict = dict()
    for i in range(len(fieldsData)):
        if fieldsData[i]['type'] == 'categorical':
            frequencies_dict[i] = fieldsData[i]['frequencies']
            minimal_frequencies_dict[i] = min(frequencies_dict[i].values())
        else:
            frequencies_dict[i] = dict()
            minimal_frequencies_dict[i] = dict()

    params_dict["frequencies"] = frequencies_dict
    print("frequency dict done:", params_dict["frequencies"])
    params_dict["minimum_freq_of_each_attribute"] = minimal_frequencies_dict
    params_dict["theta"] = 0.1

    print("before elbow")
    k = apply_elbow_method(fieldsData, vectors)
    print("done elbow")

    # activate the genetic algorithm
    print(f'start genetic')
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
    return params_dict, k
