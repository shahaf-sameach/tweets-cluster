import argparse
import json
from database_handler import Database

parser = argparse.ArgumentParser(description='read tweets file')
parser.add_argument('file_name', type=str, help='file name to read from')
args = parser.parse_args()

tweets = []
with open(args.file_name, 'r') as f:
  for line in f:
    tweets.append(json.loads(line.strip()))

print "working on {} tweets".format(len(tweets))

db = Database()
for i, tweet in enumerate(tweets):
  try :
    db.insert_tweet(tweet)
    print "inserted {}/{}".format(i + 1, len(tweets))
  except Exception as e:
    print "Error : {}".format(e)

print "done"

  