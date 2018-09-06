from collections import Counter, namedtuple

import networkx as nx
import numpy as np

from clustering import markov_clustering
from clustering.models.network_model import NetworkModel
from utils.evaluate import p_r_f_score

from utils.files import get_tweets_from_file, get_ground_truth, write_clusters_to_files


class MarkovCluster(object):

    def __init__(self):
        pass

    def fit(self, graph):
        matrix = nx.to_scipy_sparse_matrix(graph)
        clusters = self.__cluster(matrix)

        self.nodes_ = list(graph.nodes())
        tweets_clusters = [[self.nodes_[idx] for idx in c] for c in clusters]
        tweet_idx_map = {t_id : idx for idx, t_id in enumerate(self.nodes_)}

        self.labels_ = np.full(len(self.nodes_), -1, dtype=int)
        for c, self.nodes_ in enumerate(tweets_clusters):
            self.labels_[[tweet_idx_map[node] for node in self.nodes_]] = c

        return self

    def __cluster(self, matrix):
        result = markov_clustering.run_mcl(matrix)
        clusters = markov_clustering.get_clusters(result)
        return clusters


Model = namedtuple('Model', ['name', 'classification'])


print("loading data...")
date_file = "2017_03_28"
print("loading {} data...".format(date_file))
tweets = get_tweets_from_file("{}.json".format(date_file))
tweets_ids = [t['_id'] for t in tweets]
true_ids = set(map(int, get_ground_truth("{}.json".format(date_file)))).intersection(set(tweets_ids))

# creating a group of random tweets include the grounf truth tweets
random_tweets_ids = set(np.random.choice(tweets_ids, 2, replace=False)).union(true_ids)
random_tweets = [t for t in tweets if t['id'] in random_tweets_ids]

print("run model")
network = NetworkModel().build(random_tweets)
mk = MarkovCluster().fit(network)
random_tweets_ids = mk.nodes_





name = "{}_{}".format("markov", date_file)
print("writing results of {} to file".format(name))









