import numpy as np
from scipy.spatial import distance
from sklearn.cluster import AgglomerativeClustering

from clustering.models.sentence_sym_model import SentenceSymModel
from clustering.models.tf_idf_model import TfIdfModel
from clustering.models.word_vec_model import Word2VecModel
from clustering.similarity.word_sym import sentence_distance as sentence_distance1
from clustering.similarity.sentence_sym import sentence_distance as sentence_distance2

from utils.files import get_tweets_from_file, get_ground_truth
from utils.evaluate import evaluate


print("loading data...")
tweets = get_tweets_from_file("2017_03_28.json")
true_ids = set(map(int, get_ground_truth("2017_03_28.json")))

tweets_ids = [t['_id'] for t in tweets]

true_ids_indx = [i for i,v in enumerate(tweets_ids) if v in true_ids]
labels_true = np.zeros(len(tweets))
labels_true[true_ids_indx] = 1


for symm in [sentence_distance1, sentence_distance2]:
    print("building SentenceSymModel model with {}...".format(symm.__name__))
    X = SentenceSymModel().build(tweets=tweets, method=symm)

    ward = AgglomerativeClustering(n_clusters=6, affinity="precomputed").fit(X)
    labels = ward.labels_

    evaluate(labels_true, labels)
    print("\n")


for model in [TfIdfModel(), Word2VecModel()]:
    print("building {} model...".format(model.__class__.__name__))
    X = model.build(tweets=tweets)
    # transforming in X from vec to sym matrix
    X = distance.pdist(X)

    ward = AgglomerativeClustering(n_clusters=6, affinity="precomputed").fit(X)
    labels = ward.labels_

    evaluate(labels_true, labels)
    print("\n")







