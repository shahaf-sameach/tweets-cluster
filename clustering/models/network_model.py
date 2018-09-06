"""
network model of tweets as tweets_ids are nodes and edges are relations
"""

from collections import defaultdict

import networkx as nx


class NetworkModel(object):

    def __init__(self, reply_weight = 3, hash_tag_weight = 2):
        self.g = nx.Graph()
        self.reply_weight = reply_weight
        self.hash_tag_weight = hash_tag_weight

    def build(self, Tweets):
        self.tweets = Tweets
        self.g.add_nodes_from([t.id for t in self.tweets])
        self.__add_edges()

        return self.g

    def __add_edges(self):
        self.__add_weighted_edges(self.__reply_id_edge(), weight=self.reply_weight)
        self.__add_weighted_edges(self.__hastags_edges(), weight=self.reply_weight)

    def __add_weighted_edges(self, edges, weight=0):
        for edge in edges:
            edge_weight = self.g.get_edge_data(*edge)['weight'] if edge in self.g.edges else 0
            edge_weight += weight
            self.g.add_edge(*edge, weight=edge_weight)

    def __reply_id_edge(self):
        """ return all edges (tweet1, tweet2) s.t. tweet1 -> reply -> tweet2"""
        edges = set()

        reply_dict = defaultdict(list)
        for t in self.tweets:
            if t.in_reply_to_status_id in self.g.nodes:
                reply_dict[t.in_reply_to_status_id].append(t.id)

        for k, v in reply_dict.iteritems():
            for t_id in v:
                edges.add((k, t_id))

        return edges


    def __hastags_edges(self):
        """ return all edges (tweet1, tweet2) s.t. tweets share hashtag"""
        edges = set()

        hastags_dict = defaultdict(list)
        for i, t in enumerate(self.tweets):
            for h in t.entities['hashtags']:
                hastags_dict[h['text']].append(t.id)

        for k, v in hastags_dict.iteritems():
            g = nx.complete_graph(v)
            edges.update(set(g.edges))

        return edges


# NetworkModel().build(tweets)
