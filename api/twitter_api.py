import oauth2 as oauth
import json
from time import sleep

class Twitter(object):

  search_end_point = "https://api.twitter.com/1.1/search/tweets.json"

  def __init__(self):
    pass

  def set_creds(self, consumer_key, consumer_secret, access_key, access_secret):
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    access_token = oauth.Token(key=access_key, secret=access_secret)
    self.client = oauth.Client(consumer, access_token)

  def set_creds_from_user(self, user):
    consumer = oauth.Consumer(key=user.consumer_key, secret=user.consumer_secret)
    access_token = oauth.Token(key=user.access_key, secret=user.access_secret)
    self.client = oauth.Client(consumer, access_token)

  def get_by_id(self, tweet_id):
    endpoint = "https://api.twitter.com/1.1/statuses/show/%s.json" %tweet_id
    response, data = self.client.request(endpoint)
    return response, json.loads(data)

  def get_news_stream(self, filter="news", lang="en", count=100, link=None):
    endpoint = self.search_end_point + "?q=.&lang={}&filter={}&count={}".format(lang, filter, count)
    
    if link != None:
      endpoint = self.search_end_point + link 

    endpoint += '&tweet_mode=extended'
    
    response, data = self.client.request(endpoint)
    return response, json.loads(data)

if __name__ == '__main__':
  t = Twitter()
  from settings import TwitterSettings
  t.set_creds_from_user(TwitterSettings.all_users[3])
  
  next_link = None
  while True:
    res, data = t.get_news_stream(link=next_link)
    print data['search_metadata']
    next_link = data['search_metadata']['next_results']
    print res
    print "-"*20
    print data['search_metadata']
    print "{} tweets".format(len(data['statuses']))
    print ""
    print ""
    sleep(1)





