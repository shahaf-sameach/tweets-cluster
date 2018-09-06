from scipy.spatial import distance
from sklearn.cluster import AffinityPropagation, DBSCAN, AgglomerativeClustering, KMeans

from clustering.models.sentence_sym_model import SentenceSymModel
from clustering.models.tf_idf_model import TfIdfModel
from clustering.models.word_vec_model import Word2VecModel

from clustering.similarity.word_sym import sentence_distance as word_symm
from clustering.similarity.sentence_sym import sentence_distance as sentence_symm
from clustering.similarity.ish import sentence_distance as ish_symm

# # Similarity Model
# # build model using word similarity
# X = SentenceSymModel().build(tweets=tweets, method=word_symm)

# # build model using sentence similarity
# X = SentenceSymModel().build(tweets=tweets, method=sentence_symm)

# # build model using ish similarity
# X = SentenceSymModel().build(tweets=tweets, method=ish_symm)


# af = AffinityPropagation(preference=-50, affinity='precomputed').fit(X)
# db = DBSCAN(eps=0.3, min_samples=3, metric="precomputed").fit(X)
# ward = AgglomerativeClustering(n_clusters=6, affinity="precomputed").fit(X)
# km = KMeans(n_clusters=3).fit(X)
#
#
# # Vector Model
# # build model using Tf-Idf
# X = TfIdfModel().build(tweets=tweets)
# # build model using
# X = Word2VecModel().build(tweets=tweets)
#
# km = KMeans(n_clusters=3).fit(X)
#
# # for all other clustered alg need to precompute the distance matrix
# X = distance.pdist(X)
# ward = AgglomerativeClustering(n_clusters=6, affinity="precomputed").fit(X)
# af = AffinityPropagation(preference=-50, affinity='precomputed').fit(X)
# db = DBSCAN(eps=0.3, min_samples=3, metric="precomputed").fit(X)


