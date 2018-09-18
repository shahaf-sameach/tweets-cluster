import random
import time
from scipy.spatial import distance_matrix

from sklearn.cluster import KMeans, AffinityPropagation, DBSCAN, AgglomerativeClustering

from clustering.models.statistic_model import StatisticModel
from clustering.network.community_clustering import CommunityCluster
from clustering.network.markov_cluster import MarkovCluster
from clustering.network.prime_clustering import PrimCluster

from clustering.models.network_model import NetworkModel
from clustering.models.sentence_sym_model import SentenceSymModel
from clustering.models.tf_idf_model import TfIdfModel
from clustering.models.word_vec_model import Word2VecModel

from clustering.similarity.word_sym import symmetric_sentence_similarity as word_dist
from clustering.similarity.sentence_sym import symmetric_sentence_similarity as sentence_dist
from clustering.similarity.ish import symmetric_sentence_similarity as ish_dist
from utils.evaluate import purity, Rand

from utils.files import get_tweets_from_file, get_ground_truth, write_clusters_to_files

from database.tweet import TweetBuilder

def clusters_from_labels(Tweets, labels):
    clusters = [[] for l in set(labels)]
    for idx, t in enumerate(Tweets):
        clusters[labels[idx]].append(t.id)

    return clusters


random_tweets_n = 1000
n_clusters = 20

file_list = list(map(lambda f: "2017_{}".format(f),
                     ["03_28", "04_06", "04_07", "04_17", "05_24", "08_09",
                      "08_13", "08_18", "08_25", "08_27", "09_10"]))


Tweets = []
golden_standard_clusters = []
print("loading data from {} files...".format(len(file_list)))
t00 = time.time()
for idx, tweet_file in enumerate(file_list,1):
    print("\tloading data from {} [{}/{}]...".format(tweet_file, idx, len(file_list)))
    Tweets.extend([TweetBuilder(t) for t in get_tweets_from_file("{}.json".format(tweet_file))])
    golden_standard_clusters.append(map(int, get_ground_truth("{}.json".format(tweet_file))))

print("took {:.3f} sec".format(time.time() - t00))
print("golden standart clusters size: {}".format([len(c) for c in golden_standard_clusters]))
print("total tweets from files: {}".format(len(Tweets)))

golden_standard_ids = set([t_id for cluster in golden_standard_clusters for t_id in cluster])
tweets_ids = set([t.id for t in Tweets])
intersection_ids = golden_standard_ids.intersection(tweets_ids)
print("common ids: {}".format(len(intersection_ids)))

y_true = [[t for t in c if t in intersection_ids] for c in golden_standard_clusters]
# y_true = [random.sample(cluster, random_tweets_n) for cluster in y_true]
# X_tweets_ids = set([t_id for cluster in y_true for t_id in cluster])

other_ids = tweets_ids.difference(intersection_ids)
X_tweets_ids = set(random.sample(other_ids, random_tweets_n)).union(intersection_ids)

X_tweets_map = {t.id : t for t in Tweets if t.id in X_tweets_ids}
X_tweets = X_tweets_map.values()
print("running models on {} tweets".format(len(X_tweets)))


models = []

# Vector Model
# TF-IDF
X = TfIdfModel().build(X_tweets)
model_name = "TF-IDF"

# KMeans
labels = KMeans(n_clusters=n_clusters).fit_predict(X)
clusters = clusters_from_labels(X_tweets, labels)
models.append({"name": "KMeans_{}".format(model_name), "clusters": clusters})

# Agglomerative Clustering
labels = AgglomerativeClustering(n_clusters=n_clusters).fit_predict(X)
clusters = clusters_from_labels(X_tweets, labels)
models.append({"name": "Agglomerative_{}".format(model_name), "clusters": clusters})

# Affinity Propagation
X = distance_matrix(X,X)
labels = AffinityPropagation(affinity='precomputed').fit_predict(X)
clusters = clusters_from_labels(X_tweets, labels)
models.append({"name": "AffinityPropagation_{}".format(model_name), "clusters": clusters})

# DBSCAN
labels = DBSCAN(eps=0.3, min_samples=3, metric="precomputed").fit_predict(X)
clusters = clusters_from_labels(X_tweets, labels)
models.append({"name": "DBSCAN_{}".format(model_name), "clusters": clusters})



# Word2Vec
X = Word2VecModel().build(X_tweets)
model_name = "Word2Vec"

# KMeans
labels = KMeans(n_clusters=n_clusters).fit_predict(X)
clusters = clusters_from_labels(X_tweets, labels)
models.append({"name": "KMeans_{}".format(model_name), "clusters": clusters})

# Agglomerative Clustering
labels = AgglomerativeClustering(n_clusters=n_clusters).fit_predict(X)
clusters = clusters_from_labels(X_tweets, labels)
models.append({"name": "Agglomerative_{}".format(model_name), "clusters": clusters})

# Affinity Propagation
X = distance_matrix(X,X)
labels = AffinityPropagation(affinity='precomputed').fit_predict(X)
clusters = clusters_from_labels(X_tweets, labels)
models.append({"name": "AffinityPropagation_{}".format(model_name), "clusters": clusters})

# DBSCAN
labels = DBSCAN(eps=0.3, min_samples=3, metric="precomputed").fit_predict(X)
clusters = clusters_from_labels(X_tweets, labels)
models.append({"name": "DBSCAN_{}".format(model_name), "clusters": clusters})


# # Similarity Model
# # Word Distance
# X = SentenceSymModel().build(tweets=X_tweets, metric=word_dist)
# model_name="WordDist"
#
# # Affinity Propagation
# labels = AffinityPropagation(affinity='precomputed').fit_predict(X)
# clusters = clusters_from_labels(X_tweets, labels)
# models.append({"name": "AffinityPropagation_{}".format(model_name), "clusters": clusters})
#
# # DBSCAN
# labels = DBSCAN(eps=0.3, min_samples=3, metric="precomputed").fit_predict(X)
# clusters = clusters_from_labels(X_tweets, labels)
# models.append({"name": "DBSCAN_{}".format(model_name), "clusters": clusters})
#
#
# # Sentence Distance
# X = SentenceSymModel().build(tweets=X_tweets, metric=sentence_dist)
# model_name="SentenceDist"
#
# # Affinity Propagation
# labels = AffinityPropagation(affinity='precomputed').fit_predict(X)
# clusters = clusters_from_labels(X_tweets, labels)
# models.append({"name": "AffinityPropagation_{}".format(model_name), "clusters": clusters})
#
# # DBSCAN
# labels = DBSCAN(eps=0.3, min_samples=3, metric="precomputed").fit_predict(X)
# clusters = clusters_from_labels(X_tweets, labels)
# models.append({"name": "DBSCAN_{}".format(model_name), "clusters": clusters})
#
#
# # ish Distance
# X = SentenceSymModel().build(tweets=X_tweets, metric=ish_dist)
# model_name="ishDist"
#
# # Affinity Propagation
# labels = AffinityPropagation(affinity='precomputed').fit_predict(X)
# clusters = clusters_from_labels(X_tweets, labels)
# models.append({"name": "AffinityPropagation_{}".format(model_name), "clusters": clusters})
#
# # DBSCAN
# labels = DBSCAN(eps=0.3, min_samples=3, metric="precomputed").fit_predict(X)
# clusters = clusters_from_labels(X_tweets, labels)
# models.append({"name": "DBSCAN_{}".format(model_name), "clusters": clusters})


# Statistic Model
# TF-IDF
model = StatisticModel(n_cluster=n_clusters, metric='tf-idf').build(tweets=X_tweets)
clusters = model.fit(tweets=X_tweets)
models.append({"name": "Statistic_TF-IDF", "clusters": clusters})

# Bag of Words
model = StatisticModel(n_cluster=n_clusters, metric='bow').build(tweets=X_tweets)
clusters = model.fit(tweets=X_tweets)
models.append({"name": "Statistic_BOW", "clusters": clusters})


# Network model
network = NetworkModel().build(X_tweets)

# Markov
clusters = MarkovCluster().fit(network)
models.append({"name": "Markov_Clustering", "clusters": clusters})

# Community
clusters = CommunityCluster(n_clusters=n_clusters).fit(network)
models.append({"name": "Community_Clustering", "clusters": clusters})

# Prim
clusters = PrimCluster(n_clusters=n_clusters)
models.append({"name": "Prim_Clustering", "clusters": clusters})


# evaluate models
print("\n")
for i, model in enumerate(models):
    print("evaluating model {} {}/{} ...".format(model['name'], i, len(models)))
    t0 = time.time()
    y_pred = model['clusters']
    complete_clusters = [[X_tweets_map[t_id] for t_id in cluster] for cluster in y_pred]

    purity_score = purity(y_true, y_pred)
    Rand_score = Rand(y_true, y_pred)

    header = "purity: {:.3f}\nRand:   {:.3f}".format(purity_score, Rand_score)

    write_clusters_to_files(complete_clusters, header=header, prefix=model['name'])
    print("took {:.3f} sec".format(time.time() - t0))
    print("\n")

print("took total of {:.3f} sec".format(time.time() - t00))
print("done")
