import datetime

from sklearn.cluster import KMeans

from clustering.models.tf_idf_model import TfIdfModel
from database.query import Database

from utils.files import write_clusters_to_files, get_tweets_from_file

if __name__ == "__main__":

    # tweets = get_tweets_from_file("2017_03_28.json")
    print("getting tweets from db...")
    tweets = Database().get_tweets_by_date(from_date=datetime.datetime(2018, 3,21), to=1)

    print("building model...")
    tf_idf_model = TfIdfModel()
    X = tf_idf_model.build(tweets)

    print("clustering...")
    kmeans = KMeans(n_clusters=3).fit(X)

    print("writing results...")
    write_clusters_to_files(labels=kmeans.labels_, tweets=tweets)

    print("done")