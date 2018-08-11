import itertools

from networkx.algorithms import community
from clustering.models.network_model import NetworkModel
from utils.files import get_tweets_from_file


tweets = get_tweets_from_file("2017_03_28.json")

network = NetworkModel().build(tweets)

communities_generator = community.girvan_newman(network)

k = 10
k_communities = itertools.takewhile(lambda c: len(c) <= k, communities_generator)
for communities in k_communities:
    print(tuple(sorted(c) for c in communities))

