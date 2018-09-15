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

from clustering.similarity.word_sym import symmetric_sentence_similarity as word_sym
from clustering.similarity.sentence_sym import symmetric_sentence_similarity as sentence_sym
from clustering.similarity.ish import symmetric_sentence_similarity as ish_sym
from utils.evaluate import purity, Rand

from utils.files import get_tweets_from_file, get_ground_truth, write_clusters_to_files

from database.tweet import TweetBuilder

random_tweets_n = 50
n_clusters = 20

af = AffinityPropagation(affinity='precomputed')
db = DBSCAN(eps=0.3, min_samples=3, metric="precomputed")
ag = AgglomerativeClustering(n_clusters=n_clusters)
km = KMeans(n_clusters=n_clusters)

mk = MarkovCluster()
cm = CommunityCluster(n_clusters=n_clusters)
pm = PrimCluster(n_clusters=n_clusters)

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

X_tweets_ids = set([t_id for cluster in y_true for t_id in random.sample(cluster, random_tweets_n)])

# other_ids = tweets_ids.difference(intersection_ids)
# X_tweets_ids = set(random.sample(other_ids, random_tweets_n)).union(intersection_ids)

X_tweets_map = {t.id : t for t in Tweets if t.id in X_tweets_ids}
X_tweets = X_tweets_map.values()
print("running models on {} tweets".format(len(X_tweets)))


models = []
# for model in [TfIdfModel(), Word2VecModel()]:
#     print("building {} model...".format(model.__class__.__name__))
#     t0 = time.time()
#     X = model.build(X_tweets)
#     print("took {:.3f} sec".format(time.time() - t0))
#     print("fitting models:")
#     for alg in [km, ag, af, db]:
#         print("\tfitting {} ...".format(alg.__class__.__name__))
#         t1 = time.time()
#         if alg == af:
#             X = distance_matrix(X,X)
#         model_fit = alg.fit(X)
#         name = "{}_{}".format(alg.__class__.__name__,model.__class__.__name__)
#         models.append({"name": name, "fit": model_fit, 'type': 'vector'})
#         print("\ttook {:.3f} sec".format(time.time() - t1))
#     print("took {:.3f} sec".format(time.time() - t0))
#     print("\n")

for symm, symm_name in [(word_sym, "word_sym"), (sentence_sym, "sentence_sym"), (ish_sym, "ish_sym")]:
    print("building SentenceSymModel model with {} ...".format(symm_name))
    t0 = time.time()
    X = SentenceSymModel().build(tweets=X_tweets, metric=symm)
    print("took {:.3f} sec".format(time.time() - t0))
    print("fitting models:")
    for alg in [af, db]:
        print("\tfitting {} ...".format(alg.__class__.__name__))
        t1 = time.time()
        model_fit = alg.fit(X)
        name = "{}_{}_{}".format(alg.__class__.__name__, SentenceSymModel().__class__.__name__, symm_name)
        models.append({"name": name, "fit": model_fit, 'type': 'simm'})
        print("\ttook {:.3f} sec".format(time.time() - t1))
    print("took {:.3f} sec".format(time.time() - t0))
    print("\n")

# for metric in ['bow', 'tfidf']:
#     print("building StatisticModel model with metric {} ...".format(metric))
#     t0 = time.time()
#     model = StatisticModel(n_cluster=n_clusters, metric=metric).build(tweets=X_tweets)
#     print("took {:.3f} sec".format(time.time() - t0))
#     print("fitting models:")
#     model_fit = model.fit(tweets=X_tweets)
#     name = "StatisticModel_{}".format(metric)
#     models.append({"name": name, "fit": model_fit, 'type': 'stats'})
#     t1 = time.time()
#     print("took {:.3f} sec".format(time.time() - t1))
#     print("\n")


# print("building network model...")
# t0 = time.time()
# network = NetworkModel().build(X_tweets)
# print("took {:.3f} sec".format(time.time() - t0))
# print("fitting models:")
# for alg in [mk, cm, pm]:
#     print("\tfitting {} ...".format(alg.__class__.__name__))
#     t1 = time.time()
#     clusters = alg.fit(network)
#     name = "{}".format(alg.__class__.__name__ )
#     models.append({"name" : name, "fit" : clusters, 'type': 'network'})
#     print("\ttook {:.3f} sec".format(time.time() - t1))
# print("took {:.3f} sec".format(time.time() - t0))
# print("\n")

print("\n")
for i, model in enumerate(models):
    print("evaluating model {} {}/{} ...".format(model['name'], i, len(models)))
    t0 = time.time()
    y_pred = None
    if model['type'] in ['network', 'stats']:
        y_pred = model['fit']
        clusters = [[X_tweets_map[t_id] for t_id in cluster] for cluster in y_pred]
    else:
        fit = model['fit']
        clusters = [[] for l in set(fit.labels_)]
        for idx, t in enumerate(X_tweets):
            clusters[fit.labels_[idx]].append(t)

        y_pred = [[t.id for t in c] for c in clusters]

    purity_score = purity(y_true, y_pred)
    Rand_score = Rand(y_true, y_pred)

    header = "purity: {:.3f}\nRand:   {:.3f}".format(purity_score, Rand_score)

    write_clusters_to_files(clusters, header=header, prefix=model['name'])
    print("took {:.3f} sec".format(time.time() - t0))
    print("\n")

print("took total of {:.3f} sec".format(time.time() - t00))
print("done")
