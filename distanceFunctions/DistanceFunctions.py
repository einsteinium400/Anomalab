def Euclidean(u, v, type_values, parameters):
    distance = 0.0
    results = []
    for i in range(len(type_values)):
        if type_values[i]:
            raise "EUCLIDEAN DON'T KNOW TO HANDLE CATEGORIC DATA"
        results.append(u[i] - v[i])
        distance += (u[i] - v[i])**2
    return distance**0.5, results
def Hamming(u,v,type_values, hyperparams):
    distance = 0
    results = []
    for i in range(len(u)):
        if int(v[i]) != int(u[i]):
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
        if type_values[i] == True:
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
                distance += pow(max(d_fr, theta, f_v_ak), 2)
        # numberic handle
        else:
            results.append(abs(np.int64(u[i]) - np.int64(v[i])))
            distance += pow(np.int64(u[i]) - np.int64(v[i]), 2)

    distance = math.sqrt(distance)
    return distance, results
'''

dict=
{
"domain_sizes": [2,0,3,2,0,1,3]
"theta": 0.1
"theta1":3
"theta2":10
"betha":0.05
"gamma":0.01
frequencies={0:{0:1, 2:4,   }, 1:{}... ak features}  # first index is for first feature. inside is the frequency of each attribute this feature could get
minimum_freq_of_each_attribute={0:1, 1:4, 2:2}
}

'''
import numpy as np
import math

def statisticdistdebug(u, v, type_values, parameters):
    distance = 0
    results = []
    
    normalize_values = []
    if "normalize_values" in parameters:
        normalize_values = parameters["normalize_values"]
    else:
        normalize_values = [1] * len(v)

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
    numeric_dist = 0
    categoric_dist = 0
    for i in range(len(v)):
        # catrgorical handle
        if type_values[i]:
            print("handle categoric data")
            # if attributes are same
            if u[i] == v[i]:
                categoric_dist += 0
            # attributes are not the same - calculate max{f(|vak|), dfr(vi, ui), theta)
            else:
                try:
                    specific_domain_size = parameters["domain sizes"][i]
                    f_v_ak = f_freq(specific_domain_size, theta1, betha, theta2, gamma)
                    fr_u = f_freq(parameters["frequencies"][str(i)][str(int(u[int(i)]))], theta1, betha, theta2, gamma)
                    fr_v = f_freq(parameters["frequencies"][str(i)][str(int(v[int(i)]))], theta1, betha, theta2, gamma)
                    m_fk = parameters["minimum_freq_of_each_attribute"][str(i)]
                    d_fr = (abs(fr_u - fr_v) + m_fk) / max(fr_u, fr_v)
                    categoric_dist += (max(d_fr, theta, f_v_ak)) #/ normalize_values[i])

                except Exception as e:
                    print("EXCEPTION- ",e)
                    print(parameters["frequencies"])
                    print(str(int(i)))
                    print(str(int(u[int(i)])))
                    print("theta", theta)
                    print("f_v_ak", f_v_ak)
                    print(parameters)
                    print("freqs", parameters["frequencies"])
                    print(u)
                    print(v)
                    print("index", i)
                    exit()
        # numberic handle
        else:
            print("u", u)
            print("v", v)
            print("i", i)
            print(pow((np.int64(u[i]) - np.int64(v[i])),2))
            numeric_dist += pow((np.int64(u[i]) - np.int64(v[i])),2) #/ normalize_values[i]
            #if numeric_dist > 1:
                        # print ('distance is: ',max(d_fr, theta, f_v_ak))
                        # print ('normalize distance is: ',categoric_dist)
                        # print ("u is: ",u)
                        # print ("v is: ",v)
                        # print ('param index is: ',i)

    categoric_dist = pow(categoric_dist, 2)
    return math.sqrt(categoric_dist + numeric_dist)
