import pandas as pd
#from model.GeneticAlgorithm import genetic_algorithm
from model.noamGeneticAlgorithm import genetic_algorithm
from itertools import permutations
from model.elbow import elbowLocator
import matplotlib.pyplot as plt
from distanceFunctions.Hamming import Hamming as hm
from model.KMeanClusterer import KMeansClusterer
from datetime import datetime

MAX_CLUSTERS_IN_ELBOW = 10
MIN_CLUSTERS_IN_ELBOW = 1
AVERAGE_CALCULATION_TIMES = 5
KMEANS_ELBOW_REPEATS = 20


def apply_elbow_method(fields_data, vectors, distance_function):
    wcss = []
    tries = 0
    i = MIN_CLUSTERS_IN_ELBOW
    wcssCalc = []
    model = None
    while i <= MAX_CLUSTERS_IN_ELBOW:
        wcssCalc = []
        j = 0
        while j < AVERAGE_CALCULATION_TIMES:
            flag = False
            try:
                if distance_function.__name__ != "Statistic":
                    model = KMeansClusterer(hyper_params=dict(), distance=distance_function, num_means=int(i),
                                            type_of_fields=fields_data, repeats=KMEANS_ELBOW_REPEATS)
                else:
                    model = KMeansClusterer(hyper_params=dict(), distance=hm, num_means=int(i),
                                            type_of_fields=fields_data, repeats=KMEANS_ELBOW_REPEATS)
                model.cluster(vectors)
            except Exception as e:
                print('exception is:', e, 'i:', i, 'tries:', tries)
                if str(e) == "bad seed":
                    if tries == 3:
                        if i < 3:
                            raise e+"three tries"
                        else:
                            print('three tries with', i)
                            i = MAX_CLUSTERS_IN_ELBOW+1
                            break
                    else:
                        tries += 1
                        j -= 1
                        print('another try')
                        flag = True
                else:
                    raise e
            if not flag:
                wcssCalc.append(model.get_wcss())
                print('wcss for',i,'is',wcssCalc[-1])
                tries = 0
            j += 1
        print ("wcssCalc for",i,"clusters:",wcssCalc)
        if (len(wcssCalc)>0):
            wcss.append(sum(wcssCalc)/len(wcssCalc))        
        i += 1
    print("wcss list is: ", wcss)
    elbow_point = elbowLocator(wcss)
    print('elbow point is:', elbow_point)
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

                distance, results = func(vec1, vec2, type_of_fields, params_dict)
                # Update max_value if the current distance is greater
                if distance > max_vals_array[i]:
                    max_vals_array[i] = distance
        else:
            vec1 = create_array(i, len(type_of_fields), fieldsData[i]['max'])
            vec2 = create_array(i, len(type_of_fields), fieldsData[i]['min'])
            # print ('num vec1: ', vec1)
            # print ('num vec2: ', vec2)
            distance, results = func(vec1, vec2, type_of_fields, params_dict)
            # print ('num distance: ', result)
            max_vals_array[i] = distance
            # print("max_vals_array[i]", max_vals_array[i])
            # max_vals_array[i] = fieldsData[i]['max']
    print("max_vals_array: ", max_vals_array)
    return max_vals_array

def preProcess(vectors, fieldsData, distance_function):
    type_of_fields = [True if d['type'] == 'categorical' else False for d in fieldsData]
    params_dict = dict()
    df = pd.DataFrame(vectors)
    domain_sizes = df.nunique()
    params_dict["domain sizes"] = domain_sizes.tolist()
    frequencies_dict = dict()
    minimal_frequencies_dict = dict()
    max_frequencies_dict = dict()
    z = 0
    for i in range(len(fieldsData)):
        if fieldsData[i]['type'] == 'categorical':

            frequencies_dict[str(i)] = fieldsData[i]['frequencies']

            minimal_frequencies_dict[str(i)] = min(frequencies_dict[str(i)].values())
            max_frequencies_dict[str(i)] = max(frequencies_dict[str(i)].values())
            if max(frequencies_dict[str(i)].values())>z:
                z=max(frequencies_dict[str(i)].values())
        else:
            frequencies_dict[str(i)] = dict()
            minimal_frequencies_dict[str(i)] = dict()
            max_frequencies_dict[str(i)] = dict()

    params_dict["frequencies"] = frequencies_dict
    params_dict["minimum_freq_of_each_attribute"] = minimal_frequencies_dict
    params_dict["theta"] = 0.1
    k = apply_elbow_method(fieldsData, vectors, distance_function)
    # activate the genetic algorithm
    #z = df.nunique().max()  # max domain size
    time = datetime.now()
    print("START GENETIC!!! Current Time =", time.strftime("%H:%M:%S"))
    theta1, theta2, betha, gamma = genetic_algorithm(params_dict, distance_function, k, vectors, type_of_fields, z)
    print("FINISH GENETIC!!! Current Time =", datetime.now().strftime("%H:%M:%S"))
    print("IT TOOK:", (datetime.now()-time).seconds,"seconds")

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

    # exit()
    print("params_dict", params_dict)
    return params_dict, k
