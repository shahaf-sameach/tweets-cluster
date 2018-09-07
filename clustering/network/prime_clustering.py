import networkx as nx


class PrimCluster(object):

    def __init__(self, n_clusters=30):
        self.n_clusters = n_clusters

    def fit(self, network):
        mst = nx.tree.minimum_spanning_edges(network, algorithm='prim', data=False)
        edgelist = list(mst)

        tree = nx.Graph()
        tree.add_nodes_from(network.nodes())
        tree.add_edges_from(edgelist)

        clusters = list(nx.connected_components(tree))
        while len(clusters) < self.n_clusters and len(edgelist) > 0:
            tree.remove_edges_from(edgelist[0])
            edgelist = edgelist[1:]
            clusters = list(nx.connected_components(tree))

        return list(clusters)



