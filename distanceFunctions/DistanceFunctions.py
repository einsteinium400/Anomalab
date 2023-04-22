def Hamming(u,v,type_values, hyperparams):
        distance = 0
        for i in range(len(u)):
            if v[i] != u[i]:
                distance += 1
        return distance    


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


def statisticdist(u, v, type_values, parameters):
    
    normalize_values = []
    if "normalize_values" in parameters:
        normalize_values= parameters["normalize_values"]
    else:
        normalize_values=[1]*len(v)

    def f_freq(z, theta1, betha, theta2, gamma):
        if z <= theta1:
            return 1
        if theta1 < z <= theta2:
            return 1 - betha * (z - theta1)
        if z > theta2:
            return 1 - betha * (theta2 - theta1) - gamma * (z - theta2)

    betha=parameters["betha"]
    theta1=parameters["theta1"]
    theta2=parameters["theta2"]
    theta=parameters["theta"]
    gamma=parameters["gamma"]
    numeric_dist = 0
    categoric_dist = 0
    for i in range(len(v)):
        # catrgorical handle

        if type_values[i]:
            # if attributes are same
            if u[i] == v[i]:
                categoric_dist += 0

            # attributes are not the same - calculate max{f(|vak|), dfr(vi, ui), theta)
            else:
                specific_domain_size = parameters["domain sizes"][i]
                f_v_ak = f_freq(specific_domain_size,theta1,betha,theta2,gamma)
                try:
                    fr_u = f_freq(parameters["frequencies"][str(int(i))][str(int(u[int(i)]))],theta1,betha,theta2,gamma)
                    fr_v = f_freq(parameters["frequencies"][str(int(i))][str(int(v[int(i)]))],theta1,betha,theta2,gamma)
                    m_fk = parameters["minimum_freq_of_each_attribute"][str(i)]
                except Exception as e:
                    print (str(e))
                    print("feature number", i)
                    print("u", u, "v", v)
                    print(parameters)
                    exit()
                d_fr = (abs(fr_u - fr_v) + m_fk) / max(fr_u, fr_v)

                #categoric_dist += max(d_fr, theta, f_v_ak)
                # print ("d_fr: ",d_fr," theta: ",theta, " f_v_ak: ", f_v_ak, "normalize: ", normalize_values[i])
                categoric_dist += (max(d_fr, theta, f_v_ak) / normalize_values[i])

        # numberic handle
        else:
           #numeric_dist += pow((np.int64(u[i]) - np.int64(v[i])),2)
            numeric_dist += (pow((np.int64(u[i]) - np.int64(v[i])),2) / normalize_values[i])

    categoric_dist=pow(categoric_dist,2)
    return math.sqrt(categoric_dist + numeric_dist)


