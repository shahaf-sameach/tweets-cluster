import json

from pymongo import MongoClient
from settings import MongoSettings
from dateutil.parser import parse
import datetime

from utils.converter import custom_converter


class Database(object):

    def __init__(self):
        self.client = MongoClient()
        self.client = MongoClient(MongoSettings.host, MongoSettings.port)
        self.db = self.client[MongoSettings.db]
        try:
            self.db.authenticate(MongoSettings.user, MongoSettings.pwd)
        except:
            pass

    def get_all_tweets_ids(self):
        return [t['_id'] for t in self.db.tweets.find({}, {'_id': 1})]

    def get_all(self):
        return [t for t in self.db.tweets.find({})]

    def insert_tweet(self, tweet):
        tweet.update({"_id": tweet['id'], 'created_at_date': parse(tweet['created_at'])})
        return self.db.tweets.insert_one(tweet)

    def insert_4xx_tweet(self, tweet_id, status, msg):
        return self.db['tweet_4xx'].insert_one({"_id": tweet_id, "status": status, 'msg': msg})

    def get_all_4xx_tweets_ids(self):
        return [t['_id'] for t in self.db['tweet_4xx'].find({}, {'_id': 1})]

    def find_tweet(self, tweet_id):
        return self.db.tweets.find({"_id": tweet_id})

    def find_any(self):
        return self.db.tweets.find_one()

    def get_urls(self):
        tweets = [t for t in self.db.tweets.find({}, {'entities.urls': 1})]
        urls = []
        for t in tweets:
            if len(t['entities']['urls']) > 0:
                for entry in t['entities']['urls']:
                    urls.append(entry['url'])

        return urls

    def get_random_tweet(self):
        return self.db.tweets.find_one()

    def update_date(self):
        count = self.db.tweets.find({"created_at_date": {"$exists": False}}).count()
        counter = 1
        for t in self.db.tweets.find({"created_at_date": {"$exists": False}}):
            t['created_at_date'] = parse(t['created_at'])
            self.db.tweets.save(t)
            print "{}/{}".format(counter, count)
            counter += 1

    def count(self):
        return self.db.tweets.count()

    def get_tweets_by_date(self, from_date=datetime.datetime.now(), to=1):
        return [t for t in self.db.tweets.find(
                {"created_at_date": {"$gte": from_date, "$lt": from_date + datetime.timedelta(days=to)}})]


if __name__ == '__main__':
    print("start...")
    db = Database()
    for d in ["20170321"]:
        date = datetime.datetime.strptime(d,"%Y%m%d")
        print("querying for %s" % date)
        tweets = db.get_tweets_by_date(from_date=date, to=1)
        file_name = date.strftime("%Y_%m_%d.json")
        with open(file_name, 'w') as outfile:
            json.dump(tweets, outfile, default=custom_converter)
        print("wrote %s to %s" %(len(tweets), file_name))
    print "done"
