def Hamming(u,v,type_values, hyperparams):
    distance = 0
    results = []
    for i in range(len(u)):
        if float(v[i]) != float(u[i]):
            results.append(1)
            distance += 1
        else:
            results.append(0)
    return distance,results


import numpy as np
import math

def Statistic(u, v, type_values, parameters):
    distance = 0
    results = []
    
    def f_freq(z, theta1, betha, theta2, gamma):
        if z <= theta1:
            return 1
        if theta1 < z <= theta2:
            return 1 - betha * (z - theta1)
        if z > theta2:
            return 1 - betha * (theta2 - theta1) - gamma * (z - theta2)

    betha = parameters["betha"]
    theta1 = parameters["theta1"]
    theta2 = parameters["theta2"]
    theta = parameters["theta"]
    gamma = parameters["gamma"]

    for i in range(len(v)):
        # catrgorical handle
        if type_values[i]:
            # if attributes are same
            if u[i] == v[i]:
                results.append(0)
            # attributes are not the same - calculate max{f(|vak|), dfr(vi, ui), theta)
            else:
                specific_domain_size = parameters["domain sizes"][i]
                f_v_ak = f_freq(specific_domain_size, theta1, betha, theta2, gamma)
                fr_u = f_freq(parameters["frequencies"][str(i)][str(int(u[int(i)]))], theta1, betha, theta2, gamma)
                fr_v = f_freq(parameters["frequencies"][str(i)][str(int(v[int(i)]))], theta1, betha, theta2, gamma)
                m_fk = parameters["minimum_freq_of_each_attribute"][str(i)]
                d_fr = (abs(fr_u - fr_v) + m_fk) / max(fr_u, fr_v)
                results.append(abs(max(d_fr, theta, f_v_ak)))
                distance+=pow(max(d_fr, theta, f_v_ak), 2)
        # numberic handle
        else:
            results.append(abs(np.int64(u[i]) - np.int64(v[i])))
            distance+=pow(np.int64(u[i]) - np.int64(v[i]), 2)
    
    distance = math.sqrt(distance)
    return distance,results


from scipy.spatial.distance import euclidean

def scikit_euclidian(u, v, type_values, parameters):

    distance = 0.0
    results = []
    for i in range(len(u)):
        results.append((u[i] - v[i]) ** 2)
        distance += results[i]
    return euclidean(u,v), results

from sklearn.metrics.pairwise import euclidean_distances


def pairwise_eucledean(vector1, vector2, j, k):
    distance = euclidean_distances([vector1], [vector2])[0][0]
    results = []
    for i in range(len(vector1)):
        results.append(0)
    return distance, results
