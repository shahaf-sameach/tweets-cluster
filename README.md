## Twitter 
A platform for downloading and storing **news** tweets from twitter and clustering

### Stream to DB
#### Stream from file
`file_stream.py` located at `/stream` folder will read the `id_file_name` (defualt as "tweets_ids.txt") located at `files/tweets` folder
the script will read the ids from the file (each id in separate line) download them from twitter-api and save on the db

#### Stream live
`live_stream.py` located at `/stream` folder will download the tweets from twitter-api and store on the db


both api calls uses a [TwitterSearch](https://github.com/ckoepp/TwitterSearch) <br>
the method `create_search_url@TwitterSearchOrder.py` was modified to return only tweets with the following criteria `filter=news&tweet_mode=extended`

### DataBase ###
the database is MongoDB type, all interaction is done by `Database` class `@ query.py`
connection settings should be at `local_settings.py`