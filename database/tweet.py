from utils.data_structres import dnamedtuple


TWEET_ATTR = ['text',
              'id',
              'entities',
              'in_reply_to_user_id',
              'user',
              'created_at',
              'in_reply_to_status_id']

Tweet = dnamedtuple('Tweet', TWEET_ATTR)

def TweetBuilder(tweet):
    return Tweet(**{k : tweet[k] for k in Tweet._fields})




