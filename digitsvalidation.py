import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA

digits = load_digits()
X = digits.data
y = digits.target

# concatenate X and y
Xy = np.concatenate((X, y.reshape(-1,1)), axis=1)

pca = PCA(n_components=2)
Xy_pca = pca.fit_transform(Xy)

# list of WCSS values
wcss = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(Xy_pca)
    wcss.append(kmeans.inertia_)

print(wcss)
# elbow plot
plt.plot(range(1, 11), wcss, marker='o')
plt.title('Elbow Plot')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()

# K-means clustering
kmeans = KMeans(n_clusters=4, random_state=42)
y_pred = kmeans.fit_predict(Xy_pca)

plt.scatter(Xy_pca[:, 0], Xy_pca[:, 1], c=y_pred, cmap='viridis')
plt.title('K-means Clustering of Digits')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.colorbar()
plt.show()
