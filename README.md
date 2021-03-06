# Twitter Clustering
A platform for downloading, storing and **clustering** twitter's tweets

## Collect Data
##### File Stream
`file_stream.py` located at `/stream` folder will read the `id_file_name` (defualt as "tweets_ids.txt") located at `files/tweets` folder
the script will read the ids from the file (each id in separate line) download them from twitter-api and save on the db

##### Live Stream
`live_stream.py` located at `/stream` folder will download the tweets from twitter-api and store on the db<br>
api calls uses [TwitterSearch](https://github.com/ckoepp/TwitterSearch) <br>
(method `create_search_url` @ `TwitterSearchOrder.py` was modified to return only tweets meets the following criteria `filter=news&tweet_mode=extended`)

## DataBase ###
the database is MongoDB type, all interaction is done by `Database` class @ `query.py`<br>
connection settings should be at `local_settings.py`

## Clustering ###
Architecture: 
> 1. get data from source (file | db) 
> 2. build model 
> 3. run clustering algorithm
> 4. evaluate the results

the `examples` folder contains various algorithms runs such as

Similarity distance clustering based models:
- Affinity Propagation 
- Db Scan
- Hierarchical 
- Kmeans

_(all models are using the all similarity measures and modles list below)_

Network clustering based models:
- Community
- Markov
- Prime


### Models 
##### Sentence Similarity
Similarity Based Model as distance matrix<br> 
distance is computed based on tweets sentence similarity

##### TF-IDF
TF-IDF based model based on tweet's text<br>
_this model build an array of vectors, to get distance matrix use `scipy.spatial.distance.pdist(X)`_

##### Word2Vec
Word2Vec based model, trained from the tweets sentences and _brown_ corpus<br>
_this also returns array of vectors

##### Network
Network based model, where nodes are tweets and edges are relations


### Similarity 
Similarity between tweets based on
- ish similarity
- sentence similarity
- word similarity

## requirements
- python 2.7
- python packages as listed at `requirements.txt`

