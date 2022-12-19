import json
THRESHOLD = 10

EXAMPLE_PREDICT = {
    "cluster": 0,
    "distance": [
        {
            "cluster": 0,
            "centroid_distance": 10,
            "mean_distance": 5,
            "deviation":1,
            "mean_point":[
                0,4,3,2,1,0
            ]
        },
        {
            "cluster": 1,
            "centroid_distance": 20,
            "mean_distance": 5,
            "deviation":1,
            "mean_point":[
                0,4,3,2,1,0
            ]
        },
        {
            "cluster": 2,
            "centroid_distance": 20,
            "mean_distance": 5,
            "deviation":1,
            "mean_point":[
                0,4,3,2,1,0
            ]
        },
        {
            "cluster": 3,
            "centroid_distance": 30,
            "mean_distance": 5,
            "deviation":1,
            "mean_point":[
                0,4,3,2,1,0
            ]
        },
        {
            "cluster": 4,
            "centroid_distance": 40,
            "mean_distance": 5,
            "deviation":1,
            "mean_point":[
                0,4,3,2,1,0
            ]
        }
    ]
}

def parseResult(res):
    return json.load(res)
def fakePredict(sample):
    res = EXAMPLE_PREDICT
    return res['cluster'], res
def checkAnomaly(sample):
    fakeSample = sample
    cluster,predData = fakePredict(fakeSample)
    for clusterJson in predData['distance']:
        if clusterJson['cluster'] == cluster:
            if(clusterJson['centroid_distance'] >= THRESHOLD):
                print("ANOMALY")
            else:
                print(clusterJson)

checkAnomaly(1)