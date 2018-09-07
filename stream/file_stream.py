import threading, Queue
import logging
import os

from settings import TwitterSettings
from database.query import Database
from stream.api.twitter_api import Twitter
from utils.twitter_user_iter import TwitterUsersIterator

# pool for download and db task workers
download_task_pool = Queue.Queue()
db_task_pool = Queue.Queue()

num_worker_threads = 10
id_file_name = "tweets_ids.txt"


def db_worker():
    """worker to get the tweet from the db pool and store to database"""
    while True:
        data = db_task_pool.get()
        try:
            insert_to_db(data)
            logging.debug("inserted tweet {} out of apx {}".format(data[0], db_task_pool.qsize()))
        except Exception as e:
            logging.error("error insert tweet {} to db got {}".format(data[0], e))
        db_task_pool.task_done()



def download_worker():
    """worker to get tweets from twitter api and store to database"""
    for user in TwitterUsersIterator(TwitterSettings.all_users, delay=60):
        while True:
            tweet_id = download_task_pool.get()
            try:
                status, result = get_tweet(tweet_id, user)

                if status == '429':
                    logging.debug("got rate limit, switching user...")
                    break

                db_task_pool.put((tweet_id, status, result))
            except Exception as e:
                logging.error("error handle tweet {} got {}".format(tweet_id, e))

            download_task_pool.task_done()


def get_tweet(tweet_id, user):
    """retrieve tweets from twitter-api by id"""
    logging.debug("trying to download tweet {} out of apx {}".format(tweet_id, download_task_pool.qsize()))

    twitter = Twitter()
    twitter.set_creds_from_user(user)

    res, data = twitter.get_by_id(tweet_id)
    return (res['status'], data)


def insert_to_db(data):
    """insert tweet to the database"""
    tweet_id, status, tweet = data

    db = Database()

    if status == '200':
        db.insert_tweet(tweet)
    elif status == '404' or status == '403':
        logging.debug("status {} tweet {}".format(status, tweet))
        db.insert_4xx_tweet(tweet_id, status, tweet)
    else:
        logging.error("unkown status {} data {}".format(status, data))


if __name__ == "__main__" :
    logging.debug("main start")

    # getting full path of working dir
    dir = os.path.dirname(__file__)
    dir_path = os.path.join(dir, '../files/tweets/file_stream/')

    # reading tweets from file to array
    tweets_to_download = []
    logging.debug("reading {}...".format(id_file_name))
    with open(dir_path + id_file_name, 'r') as f:
        for line in f:
            tweets_to_download.append(line.strip())

    # getting all tweets downloaded from the db
    tweets_2xx = set([str(t) for t in Database().get_all_ids()])
    logging.debug("got {} tweets from 2xx collection".format(len(tweets_2xx)))

    tweets_4xx = set([str(t) for t in Database().get_all_4xx_ids()])
    logging.debug("got {} tweets from 4xx collection".format(len(tweets_4xx)))


    # calculation the diffrence of tweets needed to download - tweets in the database
    tweets = set(tweets_to_download).difference(tweets_2xx.union(tweets_4xx))
    logging.debug("working on {} tweets".format(len(tweets)))

    # spwaning download workers
    for i in range(num_worker_threads):
        t = threading.Thread(target=download_worker, args=())
        t.setDaemon(True)
        t.start()

    t = threading.Thread(target=db_worker, args=())
    t.setDaemon(True)
    t.start()

    # population the queue with tasks
    for tweet in tweets:
        download_task_pool.put(tweet)

    # waiting for all tasks to complete
    download_task_pool.join()
    db_task_pool.join()

    logging.debug("finished")
