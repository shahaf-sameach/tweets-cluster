
class Tweet(object):
  
  def __init__(self, tweet):
    self.id = tweet['id']
    self.text = tweet['text']
    self.retweet_count = tweet['retweet_count']
    self.user_id = tweet['user']['id']
    self.in_reply_to_user_id = tweet['in_reply_to_user_id']
    self.created_at = tweet['created_at']
    self.hashtags = tweet['entities']['hashtags']

    