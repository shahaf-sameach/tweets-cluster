import oauth2 as oauth
import json
from time import sleep


# an api to search tweets by ids


class Twitter(object):
    search_end_point = "https://api.twitter.com/1.1/search/tweets.json"

    def __init__(self):
        pass

    # set creds keys by raw input
    def set_creds(self, consumer_key, consumer_secret, access_key, access_secret):
        consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        access_token = oauth.Token(key=access_key, secret=access_secret)
        self.client = oauth.Client(consumer, access_token)

    # set creds from user object (local_settings.py)
    def set_creds_from_user(self, user):
        consumer = oauth.Consumer(key=user.consumer_key, secret=user.consumer_secret)
        access_token = oauth.Token(key=user.access_key, secret=user.access_secret)
        self.client = oauth.Client(consumer, access_token)

    # get tweet by id
    def get_by_id(self, tweet_id):
        endpoint = "https://api.twitter.com/1.1/statuses/show/%s.json" % tweet_id
        response, data = self.client.request(endpoint)
        return response, json.loads(data)


if __name__ == '__main__':
    t = Twitter()
    from settings import TwitterSettings

    t.set_creds_from_user(TwitterSettings.all_users[3])
    tweet = t.get_by_id("<some_id>")
