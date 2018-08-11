import networkx as nx

from clustering.models.network_model import NetworkModel
from utils.files import get_tweets_from_file


print("loading data...")
tweets = get_tweets_from_file("2017_03_28.json")

network = NetworkModel().build(tweets)
mst = nx.tree.minimum_spanning_edges(tweets, algorithm='prim', data=False)
edgelist = list(mst)

edgelist.sort(key = lambda i : network.get_edge_data(i[0], i[1])['weight'], reverse=True)

tree = nx.Graph()
tree.add_edges_from(edgelist)

cluster_n = 3

tree.remove_edges_from(edgelist[:cluster_n - 1])
clusters = nx.connected_components(tree)
print(list(clusters))



