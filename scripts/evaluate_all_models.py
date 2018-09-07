import random
import time
from scipy.spatial import distance_matrix

from sklearn.cluster import KMeans, AffinityPropagation, DBSCAN, AgglomerativeClustering

# from clustering.examples.markov_cluster import MarkovCluster
from clustering.models.sentence_sym_model import SentenceSymModel
from clustering.models.tf_idf_model import TfIdfModel
from clustering.models.word_vec_model import Word2VecModel

from clustering.similarity.word_sym import symmetric_sentence_similarity as word_sym
from clustering.similarity.sentence_sym import symmetric_sentence_similarity as sentence_sym
from clustering.similarity.ish import symmetric_sentence_similarity as ish_sym
from utils.evaluate import purity, Rand

from utils.files import get_tweets_from_file, get_ground_truth, write_clusters_to_files

from database.tweet import TweetBuilder

random_tweets_n = 1000
n_clusters = 10

af = AffinityPropagation(affinity='precomputed')
db = DBSCAN(eps=0.3, min_samples=3, metric="precomputed")
ag = AgglomerativeClustering(n_clusters=n_clusters)
km = KMeans(n_clusters=n_clusters)

file_list = list(map(lambda f: "2017_{}".format(f),
                     ["03_28", "04_06", "04_07", "04_17", "05_24", "08_09",
                      "08_13", "08_18", "08_25", "08_27", "09_10"]))


file_list = file_list[:2]

Tweets = []
golden_standard_clusters = []
print("loading data from {} files...".format(len(file_list)))
t00 = time.time()
for idx, tweet_file in enumerate(file_list,1):
    print("\tloading data from {} [{}/{}]...".format(tweet_file, idx, len(file_list)))
    Tweets.extend([TweetBuilder(t) for t in get_tweets_from_file("{}.json".format(tweet_file))])
    golden_standard_clusters.append(map(int, get_ground_truth("{}.json".format(tweet_file))))

print("took {:.3} sec".format(time.time() - t00))
print("golden standart clusters size: {}".format([len(c) for c in golden_standard_clusters]))
print("total tweets from files: {}".format(len(Tweets)))

golden_standard_ids = set([t_id for cluster in golden_standard_clusters for t_id in cluster])
tweets_ids = set([t.id for t in Tweets])
intersection_ids = golden_standard_ids.intersection(tweets_ids)
print("common ids: {}".format(len(intersection_ids)))

y_true = [[t for t in c if t in intersection_ids] for c in golden_standard_clusters]
other_ids = tweets_ids.difference(intersection_ids)
X_tweets_ids = set(random.sample(other_ids, random_tweets_n)).union(intersection_ids)
X_tweets = [t for t in Tweets if t.id in X_tweets_ids]
print("running models on {} tweets".format(len(X_tweets)))


models = []
for model in [TfIdfModel(), Word2VecModel()]:
    print("building {} model...".format(model.__class__.__name__))
    t0 = time.time()
    X = model.build(X_tweets)
    print("took {:.3} sec".format(time.time() - t0))
    print("fitting models:")
    for alg in [km, ag, af, db]:
        print("\tfitting {} ...".format(alg.__class__.__name__))
        t1 = time.time()
        if alg == af:
            X = distance_matrix(X,X)
        model_fit = alg.fit(X)
        name = "{}_{}".format(model_fit.__class__.__name__ ,model.__class__.__name__)
        models.append({"name" : name, "fit" : model_fit})
        print("\ttook {:.3} sec".format(time.time() - t1))
    print("took {:.3} sec".format(time.time() - t0))
    print("\n")


for symm_name, symm in zip(['word_sym', 'sentence_sym', 'ish_sym'],[word_sym, sentence_sym, ish_sym]):
    print("building SentenceSymModel model with {} ...".format(symm_name))
    t0 = time.time()
    X = SentenceSymModel().build(tweets=X_tweets, method=symm)
    print("took {:.3} sec".format(time.time() - t0))
    print("fitting models:")
    for alg in [af, db]:
        print("\tfitting {} ...".format(alg.__class__.__name__))
        t1 = time.time()
        model_fit = alg.fit(X)
        name = "{}_{}_{}".format(model_fit.__class__.__name__, SentenceSymModel().__class__.__name__, symm_name)
        models.append({"name": name, "fit": model_fit})
        print("\ttook {:.3} sec".format(time.time() - t1))
    print("took {:3.} sec".format(time.time() - t0))
    print("\n")



print("\n")
for i, model in enumerate(models):
    print("evaluating model {} {}/{} ...".format(model['name'], i, len(models)))
    t0 = time.time()
    fit = model['fit']
    clusters = [[] for l in set(fit.labels_)]
    for idx, t in enumerate(X_tweets):
        clusters[fit.labels_[idx]].append(t)

    y_pred = [[t.id for t in c] for c in clusters]
    purity_score = purity(y_true, y_pred)
    Rand_score = Rand(y_true, y_pred)

    header = "purity: {:.3}\nRand:   {:.3}".format(purity_score, Rand_score)

    name = "{}_{}".format(model['name'], len(clusters))
    write_clusters_to_files(clusters, header=header)
    print("took {:.3} sec".format(time.time() - t0))
    print("\n")

print("took total of {:.3} sec".format(time.time() - t00))
print("done")


