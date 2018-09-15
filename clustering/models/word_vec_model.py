"""
word 2 vec model
return tweet vectors by the avg of word2vec of the tweet's words
(run against the brown and all tweet's sentences corpus
"""

import numpy as np
from gensim.models import Word2Vec
from nltk.corpus import brown


class Word2VecModel(object):

    def __init__(self):
        pass

    def build(self, Tweets):
        self.__train(Tweets)

        return [self.__vec(sentence) for sentence in self.sentences]

    def __vec(self, sentence):
        """ get tweet2vec """
        m = np.zeros(self.model.vector_size)
        for word in sentence.split():
            try:
                v = self.model.wv[word]
            except KeyError:
                v = np.zeros(self.model.vector_size)

            m = np.vstack((m, v))
        return np.average(m, axis=0)

    def __train(self, Tweets):
        """ train net """
        self.sentences = [t.text for t in Tweets]
        corpus = [s.split() for s in self.sentences]
        corpus.extend(brown.sents())

        self.model = Word2Vec(corpus)


# Word2VecModel().build(tweets)

