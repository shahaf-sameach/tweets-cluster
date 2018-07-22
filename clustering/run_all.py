from collections import Counter

import numpy as np
from scipy.spatial import distance

from sklearn.cluster import AgglomerativeClustering, KMeans, DBSCAN, AffinityPropagation

from clustering.metric.evaluate import eval_model
from clustering.models.sentence_sym_model import SentenceSymModel
from clustering.models.tf_idf_model import TfIdfModel
from clustering.models.word_vec_model import Word2VecModel
from clustering.metric.word_sym import symmetric_sentence_similarity as word_sym
from clustering.metric.sentence_sym import symmetric_sentence_similarity as sentence_sym
from clustering.metric.ish import symmetric_sentence_similarity as ish_sym

from utils.files import get_tweets_from_file, get_ground_truth


def cluster(clustering_instance, X):
    c = clustering_instance.fit(X)

    common_label = Counter(c.labels_[true_ids_indx]).most_common(1)[0][0]
    common_label_idx = np.where(c.labels_ == common_label)

    labels = np.zeros(len(c.labels_))
    labels[common_label_idx] = 1

    return labels


print("loading data...")
tweets = get_tweets_from_file("2017_03_28.json")
true_ids = set(map(int, get_ground_truth("2017_03_28.json")))

tweets_ids = [t['_id'] for t in tweets]

true_ids_indx = [i for i,v in enumerate(tweets_ids) if v in true_ids]
labels_true = np.zeros(len(tweets))
labels_true[true_ids_indx] = 1

kmeans = KMeans(n_clusters=3)
db = DBSCAN(eps=0.3, min_samples=3, metric="precomputed")
af = AffinityPropagation(preference=-50, affinity='precomputed')
ward = AgglomerativeClustering(n_clusters=6, affinity="precomputed")

for clustering in [kmeans, db, af, ward]:
    print("{} Clusetring".format(clustering.__class__.__name__))
    for model in [TfIdfModel(), Word2VecModel()]:
        print("building {} model...".format(model.__class__.__name__))
        X = model.build(tweets=tweets)
        if type(clustering) is not KMeans:
            X = distance.pdist(X)

        labels = cluster(clustering_instance=clustering, X=X)

        eval_model(labels_true, labels)
        print("\n")

    if type(clustering) is not KMeans:
        for i, symm in enumerate([word_sym, sentence_sym, ish_sym]):
            print("building SentenceSymModel model with {}...".format(['word_sym', 'sentence_sym', 'ish_sym'][i]))
            X = SentenceSymModel().build(tweets=tweets, method=symm)

            labels = cluster(X)

            eval_model(labels_true, labels)
            print("\n")

