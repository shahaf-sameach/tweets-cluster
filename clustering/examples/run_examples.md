### Similarity Model
build model using word similarity<br>
`X = SentenceSymModel().build(tweets=tweets, method=word_symm)`

build model using sentence similarity<br>
`X = SentenceSymModel().build(tweets=tweets, method=sentence_symm)`

build model using ish similarity<br>
`X = SentenceSymModel().build(tweets=tweets, method=ish_symm)`


`af = AffinityPropagation(preference=50, affinity='precomputed').fit(X)`<br>
`db = DBSCAN(eps=0.3, min_samples=3, metric="precomputed").fit(X)`<br>
`ward = AgglomerativeClustering(n_clusters=6, affinity="precomputed").fit(X)`<br>
`km = KMeans(n_clusters=3).fit(X)`


### Vector Model
build model using Tf-Idf<br>
`X = TfIdfModel().build(tweets=tweets)`

build model using<br>
`X = Word2VecModel().build(tweets=tweets)`

`km = KMeans(n_clusters=3).fit(X)`

for all other clustered alg need to precompute the distance matrix
`X = scipy.spatial.distance_matrix(X,X)`

`af = AffinityPropagation(preference=50, affinity='precomputed').fit(X)`<br>
`db = DBSCAN(eps=0.3, min_samples=3, metric="precomputed").fit(X)`


