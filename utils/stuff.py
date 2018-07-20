import datetime
import pickle
from collections import Counter
import os
import random

from time_wrapper import timewrapper
import json

from utils.converter import custom_converter


def get_from_binary_file(tweets_num=100):
    cur_dir = os.path.dirname(__file__) or '.'
    dir_path = os.path.join(cur_dir, "../database/")

    tweets = pickle.load(open(dir_path + "tweets.p", "rb"))
    if tweets_num == -1:
        return tweets

    return random.sample(tweets, tweets_num)

@timewrapper
def get_tweets_by_hashtags_clusters(clusters_num = 7):
    dir = os.path.dirname(__file__) or '.'
    dir_path = os.path.join(dir, "../database/")

    tweets = pickle.load(open(dir_path + "tweets.p", "rb"))
    hashtag_tweets = filter(lambda i: len(i['entities']['hashtags']) > 0, tweets)

    counter = Counter([h['text'] for t in hashtag_tweets for h in t['entities']['hashtags']])
    most_common_hashtags = set([i[0] for i in counter.most_common(clusters_num)])

    clusters = []
    for hashtag in most_common_hashtags:
        tweets_cluster = []
        for t in hashtag_tweets:
            set1 = set([h['text'] for h in t['entities']['hashtags']])
            if hashtag in set1 and len(set1 & most_common_hashtags) == 1:
                tweets_cluster.append(t)
        clusters.append(tweets_cluster)

    return [(i,t) for i, c in enumerate(clusters) for t in c]


def write_clusters_to_files(labels, tweets, prefix="cluster"):
    cur_dir = os.path.dirname(__file__) or '.'
    dir_path = os.path.join(cur_dir, "../output/")

    data = zip(labels, tweets)

    for cluster in range(min(labels), max(labels) + 1):
        file_name = "{}{}_{}.txt".format(dir_path, prefix, cluster)
        with open(file_name, 'w') as f:
            tweets = [d[1] for d in filter(lambda i:i[0] == cluster, data)]
            json.dump(tweets, f, default=custom_converter)



if __name__ == "__main__":

    c = get_tweets_by_hashtags_clusters()
    t = c[0]

    with open("file.txt", 'w') as f:
        json.dump(t,f, default=custom_converter)
