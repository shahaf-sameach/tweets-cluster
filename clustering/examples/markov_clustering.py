import networkx as nx

from clustering.utils import markov_clustering
from clustering.models.network_model import NetworkModel

from utils.files import get_tweets_from_file

print("loading data...")
tweets = get_tweets_from_file("2017_03_28.json")

network = NetworkModel().build(tweets)

# then get the adjacency matrix (in sparse form)
matrix = nx.to_scipy_sparse_matrix(network)

# run MCL with default parameters
result = markov_clustering.run_mcl(matrix)

# get clusters
clusters = markov_clustering.get_clusters(result)




