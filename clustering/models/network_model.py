"""
network model of tweets as tweets_ids are nodes and edges are relations
"""

from collections import defaultdict

import networkx as nx


class NetworkModel(object):

    def __init__(self):
        self.g = nx.Graph()

    def build(self, tweets):
        self.tweets = tweets
        self.g.add_nodes_from([t['id'] for t in self.tweets])
        self.g.add_edges_from(self.__get_edges())

        return self.g

    def __get_edges(self):
        edges = set()
        edges.update(self.__reply_id_edge())
        edges.update(self.__hastags_edges())

        return edges

    def __reply_id_edge(self):
        """ return all edges (tweet1, tweet2): tweet1 -> reply -> tweet2"""
        edges = set()

        reply_dict = defaultdict(list)
        for t in self.tweets:
            reply_dict[t['in_reply_to_status_id']].append(t['id'])

        for k, v in reply_dict.iteritems():
            for t_id in v:
                edges.add((k, t_id))

        return edges


    def __hastags_edges(self):
        """ return all edges (tweet1, tweet2): tweets share hashtag"""
        edges = set()

        hastags_dict = defaultdict(list)
        for i, t in enumerate(self.tweets):
            for h in t['entities']['hashtags']:
                hastags_dict[h['text']].append(t['id'])

        for k, v in hastags_dict.iteritems():
            g = nx.complete_graph(v)
            edges.update(set(g.edges))

        return edges


# NetworkModel().build(tweets)
