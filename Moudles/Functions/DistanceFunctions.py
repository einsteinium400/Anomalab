def Hamming(u,v,type_values,hyper_parameters=0):
        distance = 0
        for i in range(len(u)):
            if v[i] != u[i]:
                distance += 1
        return distance    



def MixedDistance(u, v, type_values,hyper=0):
    distance = 0

    for i in range(len(u)):
        # if type is categorical
        if type_values[i]:
            if v[i] != u[i]:
                    distance += 1
        # if type is numeric
        else:
            distance += abs(u[i] - v[i])

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
import math


def statisticdist(u, v, type_values, parameters):

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
                fr_u = f_freq(parameters["frequencies"][i][u[i]],theta1,betha,theta2,gamma)
                fr_v = f_freq(parameters["frequencies"][i][v[i]],theta1,betha,theta2,gamma)
                m_fk = parameters["minimum_freq_of_each_attribute"][i]

                d_fr = (abs(fr_u - fr_v) + m_fk) / max(fr_u, fr_v)

                categoric_dist += max(d_fr, theta, f_v_ak)

        # numberic handle
        else:
            numeric_dist += (u[i] - v[i]) ** 2

    return math.sqrt(categoric_dist + numeric_dist)


