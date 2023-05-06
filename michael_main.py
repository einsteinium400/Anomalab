import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from scipy.spatial.distance import hamming
from sklearn.cluster import KMeans

# Load the iris dataset
iris = load_iris()

# Convert the dataset to a pandas DataFrame
df = pd.DataFrame(iris.data, columns=iris.feature_names)

# Define the Hamming distance function
def hamming_distance(x, y):
    return hamming(np.array(x > np.mean(x)).astype(int), np.array(y > np.mean(y)).astype(int))

# Use KMeans clustering with Hamming distance metric
kmeans = KMeans(n_clusters=3, init='k-means++', n_init=10, max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x=True, algorithm='auto', metric=hamming_distance)
# Fit the KMeans model to the iris dataset
kmeans.fit(df)

# Print the centroids of the clusters
print(kmeans.cluster_centers_)


# Calculate the WCSS score for the clusters
wcss = []

for i in range(1, 11):
    kmeans = KMeans(n_clusters=3, init='k-means++', n_init=10, max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x=True, algorithm='auto', metric=hamming_distance)    
    kmeans.fit(df)
    wcss.append(kmeans.inertia_)

# Plot the WCSS scores for different values of k
import matplotlib.pyplot as plt

plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()