from sklearn.cluster import KMeans
import numpy as np

X = np.array([[1, 2, 3], [1, 4, 7], [1, 0, 8],
            [4, 2, 1], [4, 4, 4], [4, 0, 8]])
# X.append((np.random,[5,6,7]))
print X
# Number of clusters
kmeans = KMeans(n_clusters=3)
# Fitting the input data
kmeans = kmeans.fit(X)
# Getting the cluster labels
labels = kmeans.predict(X)
print labels