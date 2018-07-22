import networkx as nx


from clustering.metric import markov_clustering
from clustering.models.network_model import NetworkModel
from utils.files import get_tweets_from_file

print("loading data...")
tweets = get_tweets_from_file("2017_03_28.json")

network = NetworkModel().build(tweets)
network.to_undirected()

# then get the adjacency matrix (in sparse form)
matrix = nx.to_scipy_sparse_matrix(network)

result = markov_clustering.run_mcl(matrix)           # run MCL with default parameters
clusters = markov_clustering.get_clusters(result)    # get clusters




