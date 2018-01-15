import argparse
import json

parser = argparse.ArgumentParser(description='read tweets file')
parser.add_argument('file_name', type=str, help='file name to read from')
args = parser.parse_args()

tweets = []
with open(args.file_name, 'r') as f:
  for line in f:
    tweets.append(json.loads(line.strip()))

for tweet in tweets:
  print tweet['id']