import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from models.sentence_sym_model import SentenceSymModel

from utils.stuff import get_tweets_by_hashtags_clusters, write_clusters_to_files

n_clusters = 3

data = get_tweets_by_hashtags_clusters(n_clusters)
np.random.shuffle(data)

true_labels = [d[0] for d in data]
tweets = [d[1] for d in data]

tweets_sentences = [t['text'] for t in tweets]

model = SentenceSymModel()
X = model.build(tweets_sentences)

db = DBSCAN(eps=0.3, min_samples=3, metric="precomputed").fit(X)
labels = db.labels_

write_clusters_to_files(labels, tweets, prefix="db_scan_cluster")

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(true_labels, labels))
print("Completeness: %0.3f" % metrics.completeness_score(true_labels, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(true_labels, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(true_labels, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(true_labels, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels))


