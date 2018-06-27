import string
from nltk import word_tokenize
from nltk.stem import PorterStemmer

from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from utils.stuff import get_tweets_by_hashtags_clusters, write_clusters_to_files
import numpy as np


class TfIdfModel(object):

    def __init__(self):
        pass

    def build(self, text):
        """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
        vectorizer = TfidfVectorizer(tokenizer=process_text,
                                     stop_words=stopwords.words('english'),
                                     max_df=0.5,
                                     min_df=0.1,
                                     lowercase=True)

        return vectorizer.fit_transform(text)


def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation """
    try:
        text = text.encode('ascii', 'ignore')
        text = text.translate(None, string.punctuation)
    except Exception as e:
        print text
        raise e
    tokens = word_tokenize(text)

    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]

    return tokens


if __name__ == "__main__":
    n_clusters = 3

    data = get_tweets_by_hashtags_clusters(n_clusters)
    np.random.shuffle(data)

    true_labels = [d[0] for d in data]
    tweets = [d[1] for d in data]

    tweets_sentences = [t['text'] for t in tweets]

    model = TfIdfModel()
    model.build(tweets_sentences)
    X = model.build(tweets_sentences)

    # Number of clusters
    kmeans = KMeans(n_clusters=n_clusters)
    # Fitting the input data
    kmeans = kmeans.fit(X)
    # Getting the cluster labels
    labels = kmeans.predict(X)
    print(labels)
    print(true_labels)
    write_clusters_to_files(labels, tweets, prefix="tf_idf_cluster")
    print('----')