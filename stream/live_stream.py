import time
import logging

from settings import TwitterSettings
from stream.twitter_search import TwitterSearch, TwitterSearchOrder, TwitterSearchException
from database.query import Database


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    user = TwitterSettings.all_users[0]

    consumer_key = user.consumer_key
    consumer_secret = user.consumer_secret
    access_token = user.access_key
    access_token_secret = user.access_secret

    tso = TwitterSearchOrder()
    tso.set_keywords(['.'])
    tso.set_language('en')

    sleep_for = 10
    last_amount_of_queries = 0

    ts = TwitterSearch(consumer_key=consumer_key, consumer_secret=consumer_secret,
                       access_token=access_token, access_token_secret=access_token_secret)

    db = Database()

    while True:
        try:
            logging.debug("getting next batch")
            for tweet in ts.search_tweets_iterable(tso):
                try:
                    db.insert_tweet(tweet)
                    logger.debug(u"inserted tweet {} to db".format(tweet['id']))
                except Exception as e:
                    logger.error(u"error inserting tweet {} to database: {}".format(tweet['id'], e))

                current_amount_of_queries = ts.get_statistics()[0]

                # Handle API rate limit
                if not last_amount_of_queries == current_amount_of_queries:
                    last_amount_of_queries = current_amount_of_queries
                    time.sleep(sleep_for)

        except TwitterSearchException:
            logger.debug("Timeout! waiting... ")
            time.sleep(sleep_for)

        except Exception as e:
            logger.error(u"Error: {}".format(e))


if __name__ == '__main__':
    main()
