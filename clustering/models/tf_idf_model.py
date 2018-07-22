from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from utils.files import get_tweets_by_hashtags_clusters, write_clusters_to_files
import numpy as np

from utils.text_proccesing import process_text


class TfIdfModel(object):

    def __init__(self):
        pass

    def build(self, tweets):
        """ Transform texts to Tf-Idf coordinates """
        text = [t['text'] for t in tweets]
        vectorizer = TfidfVectorizer(tokenizer=process_text,
                                     stop_words=stopwords.words('english'),
                                     max_df=0.5,
                                     min_df=0.1,
                                     lowercase=True,
                                     max_features=10000)

        return vectorizer.fit_transform(text)




if __name__ == "__main__":
    n_clusters = 3

    data = get_tweets_by_hashtags_clusters(n_clusters)
    np.random.shuffle(data)

    true_labels = [d[0] for d in data]
    tweets = [d[1] for d in data]

    model = TfIdfModel()
    X = model.build(tweets)

    # Number of clusters
    kmeans = KMeans(n_clusters=n_clusters)
    # Fitting the input data
    kmeans.fit(X)
    print(kmeans.labels_)
    print(true_labels)
    write_clusters_to_files(kmeans.labels_, tweets, prefix="tf_idf_cluster")
    print('done')