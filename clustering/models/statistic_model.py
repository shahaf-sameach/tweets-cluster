import gensim
from utils.text_proccesing import process_text


class StatisticModel(object):

    def __init__(self, n_cluster=10, metric='bow'):
        self.n_cluster = n_cluster
        self.metric = metric


    def build(self, tweets):
        processed_docs = map(process_text, (t.text for t in tweets))

        self.dictionary = gensim.corpora.Dictionary(processed_docs)
        bow_corpus = [self.dictionary.doc2bow(doc) for doc in processed_docs]

        if self.metric == 'bow':
            corpus = bow_corpus
        else:
            self.tfidf = gensim.models.TfidfModel(bow_corpus)
            corpus = self.tfidf[bow_corpus]

        self.lda_model = gensim.models.LdaMulticore(corpus, num_topics=self.n_cluster, id2word=self.dictionary, passes=2, workers=2)

        return self


    def fit(self, tweets):
        processed_docs = map(process_text, (t.text for t in tweets))
        bow_matrix = [self.dictionary.doc2bow(doc) for doc in processed_docs]

        if self.metric == 'bow':
            corpus = bow_matrix
        else:
            corpus = self.tfidf[bow_matrix]

        clusters = [[] for _ in xrange(self.n_cluster)]
        for idx, result in enumerate(self.lda_model[corpus]):
            cluster = max(result, key=lambda k:k[1])
            clusters[cluster[0]].append(tweets[idx].id)

        return clusters



# StatisticModel().build(Tweets).fit(Tweets)

