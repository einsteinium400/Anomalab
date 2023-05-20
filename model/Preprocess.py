import pandas as pd
from model.GeneticAlgorithm import genetic_algorithm
#from model.noamGeneticAlgorithm import genetic_algorithm
from itertools import permutations
from model.elbow import elbowLocator
import matplotlib.pyplot as plt
from distanceFunctions.Hamming import Hamming as hm
from model.KMeanClusterer import KMeansClusterer
from datetime import datetime

MAX_CLUSTERS_IN_ELBOW = 10
MIN_CLUSTERS_IN_ELBOW = 1


def apply_elbow_method(fields_data, vectors, distance_function, triesNumber, _repeats):
    print("in elbow")
    wcss = []
    tries = 0
    triesNumber=1 ###
    i = MIN_CLUSTERS_IN_ELBOW
    wcssCalc = []
    model = None
    while i <= MAX_CLUSTERS_IN_ELBOW:
        wcssCalc = []
        j = 0
        while j < triesNumber:
            flag = False
            try:
                if distance_function.__name__ != "Statistic" and distance_function.__name__ != "statisticdistdebug":
                    #exit()
                    model = KMeansClusterer(hyper_params=dict(), distance=distance_function, num_means=int(i),
                                            type_of_fields=fields_data, repeats=_repeats)
                else:
                    model = KMeansClusterer(hyper_params=dict(), distance=hm, num_means=int(i),
                                            type_of_fields=fields_data, repeats=_repeats)
                model.cluster_vectorspace(vectors)
            except Exception as e:
                print('exception is:', e, 'i:', i, 'tries:', tries)
                if str(e) == "bad seed":
                    if tries == 3:
                        if i < 3:
                            print("three tries")
                            raise e

                        else:
                            print('three tries with', i)
                            i = MAX_CLUSTERS_IN_ELBOW + 1
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
                if i == 1:
                    j = triesNumber
                tries = 0
            j += 1
        if (len(wcssCalc) > 0):
            print("wcssCalc for", i, "clusters:", wcssCalc, "average:", sum(wcssCalc) / len(wcssCalc))
            wcss.append(sum(wcssCalc) / len(wcssCalc))
        i += 1
    print("wcss list is: ", wcss)
    elbow_point = elbowLocator(wcss)
    print('elbow point is:', elbow_point)
    return elbow_point


def preProcess(vectors, fieldsData, distance_function, triesNumber, repeats):
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
            if max(frequencies_dict[str(i)].values()) > z:
                z = max(frequencies_dict[str(i)].values())
        else:
            frequencies_dict[str(i)] = dict()
            minimal_frequencies_dict[str(i)] = dict()
            max_frequencies_dict[str(i)] = dict()

    params_dict["frequencies"] = frequencies_dict
    params_dict["minimum_freq_of_each_attribute"] = minimal_frequencies_dict
    params_dict["theta"] = 0.1
    print("starting elbow")
    k = apply_elbow_method(type_of_fields, vectors, distance_function, triesNumber, repeats)
    # activate the genetic algorithm
    # z = df.nunique().max()  # max domain size
    time = datetime.now()
    print("START GENETIC!!! Current Time =", time.strftime("%H:%M:%S"))
    theta1, theta2, betha, gamma = genetic_algorithm(params_dict, distance_function, k, vectors, type_of_fields, z)
    print("FINISH GENETIC!!! Current Time =", datetime.now().strftime("%H:%M:%S"))
    print("IT TOOK:", (datetime.now() - time).seconds, "seconds")

    params_dict["theta1"] = theta1  # 3
    params_dict["theta2"] = theta2  # 10
    params_dict["betha"] = betha  # 0.05
    params_dict["gamma"] = gamma  # 0.01
    print('done genetics: ', params_dict)
    return params_dict, k
