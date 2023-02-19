
def classIntegrator(data):
    rows, cols = (5, 4)
    arr = [[0 for i in range(cols)] for j in range(rows)]
    for row in data:
        actualClass = row[-1]
        clusterClass = row[-2]
        print(f'Actual Class: {actualClass} Cluster Class: {clusterClass}')
        arr[actualClass][clusterClass] += 1
    for row in arr:
        print(row)
    for i in range(1, 5):
        sumItems = sum(arr[i])
        print(f'Actual Class: {i}'
              f'\n\t ClusterClass 0: {(arr[i][0]/sumItems)*100}'
              f'\n\t ClusterClass 1: {(arr[i][1]/sumItems)*100}'
              f'\n\t ClusterClass 2: {(arr[i][2]/sumItems)*100}'
              f'\n\t ClusterClass 3: {(arr[i][3]/sumItems)*100}'
              f'\n\t Max: {arr[i].index(max(arr[i]))}')
