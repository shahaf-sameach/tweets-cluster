import os
import json

from utils.converter import custom_converter


def write_clusters_to_files(labels, tweets, prefix="clustering"):
    """write clusters to file
       input: labels - ordered array of labels e.g [0,1,1,2,0,2,....]
              tweets - ordered array of tweets e.g [tweet0, tweet1...]
       output: a new file under /output folder"""

    cur_dir = os.path.dirname(__file__) or '.'
    dir_path = os.path.join(cur_dir, "../output/")

    data = zip(labels, tweets)

    for cluster in range(min(labels), max(labels) + 1):
        file_name = "{}{}_{}.txt".format(dir_path, prefix, cluster)
        with open(file_name, 'w') as f:
            tweets = [d[1] for d in filter(lambda i: i[0] == cluster, data)]
            json.dump(tweets, f, default=custom_converter)


def get_tweets_from_file(file_name):
    "read tweets from file (json)"
    cur_dir = os.path.dirname(__file__) or '.'
    dir_path = os.path.join(cur_dir, "../files/tweets/")

    with open(dir_path + file_name, 'r') as f:
        tweets = json.load(f)

    return tweets


def get_ground_truth(file_name):
    """get tweets ids from ground truth files"""
    cur_dir = os.path.dirname(__file__) or '.'
    dir_path = os.path.join(cur_dir, "../files/tweets/ground_truth/")

    with open(dir_path + file_name, 'r') as f:
        tweets_ids = json.load(f)

    return tweets_ids
