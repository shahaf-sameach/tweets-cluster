import random
import networkx as nx

from utils.files import get_tweets_from_file


def reply_id_edge(tweet1, tweet2):
    if tweet1['in_reply_to_status_id'] == tweet2['id'] or \
        tweet2['in_reply_to_status_id'] == tweet1['id']:
        return True

    return False

def reply_user_edge(tweet1, tweet2):
    if tweet1['user']['id'] == tweet2['in_reply_to_user_id'] or \
        tweet2['user']['id'] == tweet1['in_reply_to_user_id']:
        return True

    return False


def user_mention_edge(tweet1, tweet2):
    if tweet1['user']['id'] in [i['id'] for i in tweet2['entities']['user_mentions']] or \
            tweet2['user']['id'] in [i['id'] for i in tweet1['entities']['user_mentions']]:
        return True

    return False

def hastags_edge(tweet1, tweet2):
    set1 = set([i['text'] for i in tweet1['entities']['hashtags']])
    set2 = set([i['text'] for i in tweet2['entities']['hashtags']])

    if len(set1.intersection(set2)) > 0:
        return True

    return False

def any_edge(tweet1, tweet2):
    for method in [reply_id_edge, reply_user_edge, user_mention_edge, hastags_edge]:
        if method(tweet1, tweet2):
            return True
    return False



print("loading data...")
tweets = get_tweets_from_file("2017_03_28.json")[:100]


print("adding nodes to graph...")
g = nx.Graph()
g.add_nodes_from([t['id'] for t in tweets])

print("building edge sets...")
edges = set()
for i, _ in enumerate(tweets):
    print("working on tweet {}/{}".format(i, len(tweets)))
    for j in xrange(i, len(tweets)):
        if (tweets[i]['id'], tweets[j]['id']) not in edges and (tweets[j]['id'], tweets[i]['id']):
            if any_edge(tweets[i], tweets[j]):
                edges.add((tweets[i]['id'], tweets[j]['id']))


print("adding adges to graph...")
g.add_edges_from(edges)

print(nx.info(g))
nx.write_edgelist(g, "graph.txt")
print("done")
#
# print("drawing...")
# sp = nx.spring_layout(g)
# print("----")
# nx.draw_networkx(g, with_labels=False)
# import matplotlib.pyplot as plt
# plt.show()
