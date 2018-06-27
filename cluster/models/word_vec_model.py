
import numpy as np
from gensim.models import Word2Vec
from sklearn.cluster import KMeans

from utils.stuff import get_tweets_by_hashtags_clusters, write_clusters_to_files
from tf_idf_model import process_text

from nltk.corpus import brown


class Word2VecModel(object):

    def __init__(self, sentences):
        corpus = [process_text(t) for t in sentences] + brown.sents()
        self.model = Word2Vec(corpus)

    def build(self, sentences):
        return [self.vec(sentence) for sentence in sentences]

    def vec(self, sentence):
        m = np.zeros(self.model.vector_size)
        for word in sentence:
            try:
                v = self.model.wv[word]
            except KeyError:
                v = np.zeros(self.model.vector_size)

            m = np.vstack((m, v))
        return np.average(m, axis=0)

    def load(self, file_name):
        self.model.load(file_name)

    def save(self, file_name):
        self.model.save(file_name)

if __name__ == '__main__':
    n_clusters = 3
    data = get_tweets_by_hashtags_clusters(n_clusters)
    np.random.shuffle(data)

    true_labels = [d[0] for d in data]
    tweets = [d[1] for d in data]

    tweets_sentences = [t['text'] for t in tweets]

    model = Word2VecModel(tweets_sentences)
    X = model.build(tweets_sentences)

    # Number of clusters
    kmeans = KMeans(n_clusters=n_clusters)
    # Fitting the input data
    kmeans = kmeans.fit(X)
    # Getting the cluster labels
    labels = kmeans.predict(X)
    print(labels)
    print(true_labels)
    write_clusters_to_files(labels, tweets)
    print('----')

