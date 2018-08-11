from collections import Counter

import numpy as np
from scipy.spatial import distance

from sklearn.cluster import AffinityPropagation

from utils.evaluate import evaluate
from clustering.models.sentence_sym_model import SentenceSymModel
from clustering.models.tf_idf_model import TfIdfModel
from clustering.models.word_vec_model import Word2VecModel
from clustering.similarity.word_sym import sentence_distance as sentence_distance1
from clustering.similarity.sentence_sym import sentence_distance as sentence_distance2

from utils.files import get_tweets_from_file, get_ground_truth


tweet_file_name = "2017_03_28.json"
print("loading data from {} ...".format(tweet_file_name))

tweets = get_tweets_from_file(tweet_file_name)
ground_truth_ids = set(map(int, get_ground_truth(tweet_file_name)))

tweets_ids = [t['_id'] for t in tweets]

ground_truth_ids_indx = [i for i, v in enumerate(tweets_ids) if v in ground_truth_ids]
ground_truth_labels = np.zeros(len(tweets))
ground_truth_labels[ground_truth_ids_indx] = 1

for symm_func in [sentence_distance1, sentence_distance2]:
    print("building SentenceSymModel model with {} ...".format(symm_func.__name__))
    X = SentenceSymModel().build(tweets=tweets, method=symm_func)

    af = AffinityPropagation(preference=-50, affinity='precomputed').fit(X)
    labels = af.labels_
    evaluate(ground_truth_labels, labels)
    print("\n")

for model in [TfIdfModel(), Word2VecModel()]:
    print("building {} model...".format(model.__class__.__name__))
    X = model.build(tweets=tweets)

    # transforming in X from vec to sym matrix
    X = distance.pdist(X)

    af = AffinityPropagation(preference=-50, affinity='precomputed').fit(X)
    labels = af.labels_
    evaluate(ground_truth_labels, labels)
    print("\n")




