from pymongo import MongoClient
from settings import MongoSettings
from model.tweet import Tweet

class Database(object):

  def __init__(self):
    self.client = MongoClient()
    self.client = MongoClient(MongoSettings.host, MongoSettings.port)
    self.db = self.client[MongoSettings.db]
    #self.db.authenticate(MongoSettings.user, MongoSettings.pwd)

  def get_all_tweets_ids(self):
    return [t['id'] for t in self.db.tweets.find({}, {'id' : 1})]

  def insert_tweet(self, tweet):
    tweet.update({"_id" : tweet['id']})
    return self.db.tweets.insert_one(tweet)

  def insert_4xx_tweet(self, tweet_id, status, msg):
    return self.db['tweet_4xx'].insert_one({"_id" : tweet_id, "status" : status, 'msg' : msg})

  def get_all_4xx_tweets_ids(self):
    return [t['_id'] for t in self.db['tweet_4xx'].find({}, {'_id' : 1})]

  def find_tweet(self, tweet_id):
    return self.db.tweets.find({"id" : tweet_id})

  def find_any(self):
    return self.db.tweets.find_one()

  def get_urls(self):
    tweets = [t for t in self.db.tweets.find({}, {'entities.urls' : 1})]
    urls = []
    for t in tweets:
      if len(t['entities']['urls']) > 0:
        for entry in t['entities']['urls']:
          urls.append(entry['url'])

    return urls

  def get_random_tweet(self):
    return self.db.tweets.find_one()

if __name__ == '__main__':
  db = Database()
  t = db.get_random_tweet()
  tweet = Tweet(t)
  print tweet.hashtags
  

