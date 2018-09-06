import networkx as nx
import numpy as np

from clustering.models.network_model import NetworkModel
from utils.files import get_tweets_from_file, get_ground_truth

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

mst = nx.tree.minimum_spanning_edges(network, algorithm='prim', data=False)
edgelist = list(mst)

edgelist.sort(key = lambda i : network.get_edge_data(i[0], i[1])['weight'], reverse=True)

tree = nx.Graph()
tree.add_edges_from(edgelist)

cluster_n = 3

tree.remove_edges_from(edgelist[:cluster_n - 1])
clusters = nx.connected_components(tree)

