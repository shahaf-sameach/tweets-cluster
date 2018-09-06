from utils.data_structres import dnamedtuple


TWEET_ATTR = ['text',
              'id',
              'entities',
              'in_reply_to_user_id',
              'user',
              'created_at']

Tweet = dnamedtuple('Tweet', TWEET_ATTR)

def TweetBuilder(tweet):
    return Tweet(**{k : tweet[k] for k in Tweet._fields})




