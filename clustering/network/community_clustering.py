from networkx.algorithms import community


class CommunityCluster(object):

    def __init__(self, n_clusters=30):
        self.n_clusters = n_clusters

    def fit(self, network):
        for clusters in community.girvan_newman(network):
            if len(clusters) > self.n_clusters:
                return clusters

        return [(n) for n in network.nodes()]


