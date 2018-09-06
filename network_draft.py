import random
import networkx as nx
from networkx.algorithms.tree.mst import prim_mst_edges

from utils.files import get_tweets_from_file


G = nx.cycle_graph(4)
G.add_edge(0, 3, weight=2)
G.add_edge(0, 1, weight=3)
print(nx.info(G))

mst = nx.tree.minimum_spanning_edges(G, algorithm='prim', data=False)
edgelist = list(mst)
print(edgelist)

# nx.draw_networkx(G, with_labels=True)
# # nx.draw_networkx_edge_labels(G,pos=nx.spring_layout(G))
# import matplotlib.pyplot as plt
# plt.show()
# plt.waitforbuttonpress()
# plt.clf()
#
#
# g = nx.Graph()
# g.add_nodes_from(G.nodes)
# g.add_edges_from(edgelist)
# nx.draw_networkx(g, with_labels=True)
# plt.show()

# nx.connected_components(G)
