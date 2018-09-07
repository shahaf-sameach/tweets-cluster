import networkx as nx

from clustering import markov_clustering


class MarkovCluster(object):

    def __init__(self):
        pass

    def fit(self, network):
        matrix = nx.to_scipy_sparse_matrix(network)
        idx_clusters = self.__cluster(matrix)

        nodes = list(network.nodes())
        clusters = []

        for cluster in idx_clusters:
            clusters.append([nodes[idx] for idx in cluster])

        return clusters

    def __cluster(self, matrix):
        result = markov_clustering.run_mcl(matrix)
        return markov_clustering.get_clusters(result)


