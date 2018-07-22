from collections import Counter

import numpy as np
from scipy.spatial import distance

from sklearn.cluster import DBSCAN

from clustering.metric.evaluate import eval_model
from clustering.models.sentence_sym_model import SentenceSymModel
from clustering.models.tf_idf_model import TfIdfModel
from clustering.models.word_vec_model import Word2VecModel
from clustering.metric.word_sym import sentence_distance as sentence_distance1
from clustering.metric.sentence_sym import sentence_distance as sentence_distance2

from utils.files import get_tweets_from_file, get_ground_truth


def cluster(X):
    db = DBSCAN(eps=0.3, min_samples=3, metric="precomputed").fit(X)

    common_label = Counter(db.labels_[true_ids_indx]).most_common(1)[0][0]
    common_label_idx = np.where(db.labels_ == common_label)

    labels = np.zeros(len(db.labels_))
    labels[common_label_idx] = 1

    return labels


print("loading data...")
tweets = get_tweets_from_file("2017_03_28.json")
true_ids = set(map(int, get_ground_truth("2017_03_28.json")))

tweets_ids = [t['_id'] for t in tweets]

true_ids_indx = [i for i,v in enumerate(tweets_ids) if v in true_ids]
labels_true = np.zeros(len(tweets))
labels_true[true_ids_indx] = 1


for symm in [sentence_distance1, sentence_distance2]:
    print("building SentenceSymModel model with fn1...")
    X = SentenceSymModel().build(tweets=tweets, method=symm)

    labels = cluster(X)

    eval_model(labels_true, labels)
    print("\n")


for model in [TfIdfModel(), Word2VecModel()]:
    print("building {} model...".format(model.__class__.__name__))
    X = model.build(tweets=tweets)
    X = distance.pdist(X)

    labels = cluster(X)

    eval_model(labels_true, labels)
    print("\n")

