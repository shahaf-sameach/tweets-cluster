import datetime

from sklearn.cluster import KMeans

from clustering.models.tf_idf_model import TfIdfModel
from database.query import Database
from database.tweet import TweetBuilder

from utils.files import write_clusters_to_files, get_tweets_from_file


def create_clusters(labels, tweets):
    n_clusters = len(set(labels))
    labels_cluster_idx_map = dict(enumerate(set(labels)))
    clusters = [[] for _ in range(n_clusters)]

    for label, tweet in zip(labels, tweets):
        clusters[labels_cluster_idx_map[label]].append(tweet)

    return clusters

if __name__ == "__main__":

    # tweets = get_tweets_from_file("2017_03_28.json")
    print("getting tweets from db...")
    db_tweets = Database().get_by_date(from_date=datetime.datetime(2018, 3, 21), to=1)
    db_tweets = Database().get_all()

    tweets = [TweetBuilder(t) for t in db_tweets]

    print("building model...")
    model = TfIdfModel().build(tweets)

    print("clustering...")
    labels = KMeans(n_clusters=3).fit_predict(model)

    print("writing results...")
    clusters = create_clusters(labels=labels, tweets=tweets)
    write_clusters_to_files(clusters=clusters)

    print("done")