
tweets = []

with open("live_stream.log", 'r') as f:
  for line in f:
    if 'inserted tweet' in line:
      tweet_id = line.split(' ')[9]
      tweets.append(tweet_id)

print tweets[5]

print len(tweets)
print len(set(tweets))

