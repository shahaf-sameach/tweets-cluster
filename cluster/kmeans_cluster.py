import collections

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class KMeansCluster(object):

    def __init__(self):
        pass

    def cluster(self, x, clusters=3):
        km_model = KMeans(n_clusters=clusters)
        km_model.fit(x)

        clustering = collections.defaultdict(list)

        for idx, label in enumerate(km_model.labels_):
            clustering[label].append(idx)

        silhouette_avg = silhouette_score(x, km_model.labels_)

        return (clustering, silhouette_avg)

    def clusters(self, x):

        silhouette_avgs = []
        for i in range(2, len(x) / 2):
            c, silhouette_avg = self.cluster(x, clusters=i)
            silhouette_avgs.append((i, c, silhouette_avg))

        return silhouette_avg



if __name__ == '__main__':
    pass

