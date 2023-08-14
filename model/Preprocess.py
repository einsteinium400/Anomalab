import pandas as pd
from model.GeneticAlgorithm import genetic_algorithm
from model.elbow import elbowLocator
from distanceFunctions.Hamming import Hamming as hm
from model.KMeanClusterer import KMeansClusterer
from datetime import datetime

MAX_CLUSTERS_IN_ELBOW = 10
MIN_CLUSTERS_IN_ELBOW = 1


def apply_elbow_method(fields_data, vectors, distance_function, triesNumber, _repeats):

    wcss = []
    tries = 0
    i = MIN_CLUSTERS_IN_ELBOW
    model = None
    while i <= MAX_CLUSTERS_IN_ELBOW:
        flag = False
        try:
            if distance_function.__name__ != "Statistic" and distance_function.__name__ != "statisticdistdebug":
                model = KMeansClusterer(hyper_params=dict(), distance=distance_function, num_means=int(i),
                                        type_of_fields=fields_data, repeats=_repeats)
            else:
                model = KMeansClusterer(hyper_params=dict(), distance=hm, num_means=int(i),
                                        type_of_fields=fields_data, repeats=_repeats)
            model.cluster_vectorspace(vectors)
        except Exception as e:
            if str(e) == "bad seed":
                if tries == 3:
                    if i < 3:
                        raise e
                    else:
                        i = MAX_CLUSTERS_IN_ELBOW + 1
                        break
                else:
                    tries += 1
                    flag = True
            else:
                raise e
        if not flag:
            wcss.append(model.get_wcss())
            tries = 0
            i += 1
    elbow_point = elbowLocator(wcss)
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
    time = datetime.now()
    k = apply_elbow_method(type_of_fields, vectors, distance_function, triesNumber, repeats)
    print("ELBOW COMPLETED K IS:", k,"TOOK:", (datetime.now() - time).seconds, "seconds")
    # activate the genetic algorithm
    # z = df.nunique().max()  # max domain size
    time = datetime.now()
    theta1, theta2, betha, gamma = genetic_algorithm(params_dict, distance_function, k, vectors, type_of_fields, z)
    print("GENETIC COMPLETED AND TOOK:", (datetime.now() - time).seconds, "seconds")

    params_dict["theta1"] = theta1  # 3
    params_dict["theta2"] = theta2  # 10
    params_dict["betha"] = betha  # 0.05
    params_dict["gamma"] = gamma  # 0.01
    print('done genetics: ', params_dict)
    return params_dict, k
