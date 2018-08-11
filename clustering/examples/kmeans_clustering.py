from collections import Counter
import numpy as np

from sklearn.cluster import KMeans

from clustering.models.tf_idf_model import TfIdfModel
from clustering.models.word_vec_model import Word2VecModel

from utils.files import get_tweets_from_file, get_ground_truth
from utils.evaluate import evaluate


print("loading data...")
tweets = get_tweets_from_file("2017_03_28.json")
true_ids = set(map(int, get_ground_truth("2017_03_28.json")))

tweets_ids = [t['_id'] for t in tweets]

true_ids_indx = [i for i,v in enumerate(tweets_ids) if v in true_ids]
labels_true = np.zeros(len(tweets))
labels_true[true_ids_indx] = 1


for model in [TfIdfModel(), Word2VecModel()]:
    print("building {} model...".format(model.__class__.__name__))
    X = model.build(tweets)

    print("clustering...")
    kmeans = KMeans(n_clusters=3).fit(X)

    common_label = Counter(kmeans.labels_[true_ids_indx]).most_common(1)[0][0]
    common_label_idx = np.where(kmeans.labels_ == common_label)

    labels = np.zeros(len(tweets))
    labels[common_label_idx] = 1

    evaluate(labels_true, labels)
    print("\n")


