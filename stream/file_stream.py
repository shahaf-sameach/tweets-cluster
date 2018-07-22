import threading, Queue
import logging
import os

from time import sleep
from settings import TwitterSettings
from database.query import Database
from stream.api.twitter_api import Twitter

download_task_pool = Queue.Queue()
db_task_pool = Queue.Queue()

num_worker_threads = 10

def db_worker():
  while True:
    data = db_task_pool.get()
    try:
      insert_to_db(data)
      logging.debug("inserted tweet {} out of apx {}".format(data[0], db_task_pool.qsize()))
    except Exception as e:
      logging.error("error insert tweet {} to db got {}".format(data[0], e))
    db_task_pool.task_done()


def download_worker():
  current_user, cycled_users = 0, 0
  while True:
    if cycled_users == 1:
      logging.debug("sleeping for 1 min...")
      sleep(60)
      logging.debug("woke up!")
      cycled_users = 0

    if current_user == len(TwitterSettings.all_users):
      current_user = 0
      cycled_users += 1

    user = TwitterSettings.all_users[current_user]
    while True:
      tweet_id = download_task_pool.get()
      try:
        status, result = get_tweet(tweet_id, user)
        
        if status == '429':
          logging.debug("got rate limit, switching user...")
          current_user += 1
          break

        db_task_pool.put((tweet_id, status, result))
      except Exception as e:
        logging.error("error handle tweet {} got {}".format(tweet_id, e))
      
      download_task_pool.task_done()

def get_tweet(tweet_id, user):
  logging.debug("trying to download tweet {} out of apx {}".format(tweet_id, download_task_pool.qsize()))
  
  twitter = Twitter()
  
  twitter.set_creds_from_user(user)
    
  res, data = twitter.get_by_id(tweet_id)
  
  return (res['status'], data)

def insert_to_db(data):
  tweet_id, status, tweet = data

  db = Database()

  if status == '200':
    db.insert_tweet(tweet)

  elif status == '404' or status == '403':
    logging.debug("status {} tweet {}".format(status, tweet))
    db.insert_4xx_tweet(tweet_id, status, tweet)

  else:
    logging.error("unkown status {} data {}".format(status, data))

logging.debug("main start")

dir = os.path.dirname(__file__)
dir_path = os.path.join(dir, '../files/tweets/')

tweets_to_download = []
logging.debug("reading tweets_ids.txt...")
with open(dir_path + 'tweets_ids.txt', 'r') as f:
  for line in f:
    tweets_to_download.append(line.strip())

#with open(dir_path + 'tweets_ids2.txt', 'r') as f:
#  for line in f:
#    tweets_to_download.append(line.strip())
#logging.debug("read {} tweets".format(len(tweets_to_download)))

tweets_2xx = set([str(t) for t in Database().get_all_tweets_ids()])
logging.debug("got {} tweets from 2xx collection".format(len(tweets_2xx)))

tweets_4xx = set([str(t) for t in Database().get_all_4xx_tweets_ids()])
logging.debug("got {} tweets from 4xx collection".format(len(tweets_4xx)))

tweets = set(tweets_to_download).difference(tweets_2xx.union(tweets_4xx))
logging.debug("working on {} tweets".format(len(tweets)))

for i in range(num_worker_threads):
  t = threading.Thread(target=download_worker, args=())
  t.setDaemon(True)
  t.start()

t = threading.Thread(target=db_worker, args=())
t.setDaemon(True)
t.start()

for tweet in tweets:
  download_task_pool.put(tweet)

download_task_pool.join()
db_task_pool.join()

logging.debug("finished")
  
