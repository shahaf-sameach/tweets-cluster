import os
import json
import re

from utils.converter import custom_converter


def write_clusters_to_files(clusters, header=None, prefix="clusters"):
    """write clusters to file
       input: clusters - tuple of tuples e.g ((tweet0, tweet1,(tweet2...)...)
       output: a new file under /output folder"""

    cur_dir = os.path.dirname(__file__) or '.'
    dir_path = os.path.join(cur_dir, "../output/")

    file_name = "{}{}_{}.txt".format(dir_path, prefix, len(clusters))
    with open(file_name, 'w') as f:
        if header != None:
            f.write("{}\n\n".format(header))

        for cluster in clusters:
            for tweet in cluster:
                f.write("[{}] - {}\n".format(tweet.id, format_tweet_text(tweet.text)))
            f.write("\n\n\n")
        f.write("\n")



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


def format_tweet_text(text):
    return re.sub('\s+', ' ', text.encode('utf-8')).strip()
