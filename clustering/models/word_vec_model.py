"""
word 2 vec model
return tweet vectors by the avg of word2vec of the tweet's words
(run against the brown and all tweet's sentences corpus
"""


import numpy as np
from gensim.models import Word2Vec
from nltk.corpus import brown
from tf_idf_model import process_text


class Word2VecModel(object):

    def __init__(self):
        pass

    def build(self, tweets):
        self.__train(tweets)

        return [self.__vec(sentence) for sentence in self.sentences]

    def __vec(self, sentence):
        """ get tweet2vec """
        m = np.zeros(self.model.vector_size)
        for word in sentence:
            try:
                v = self.model.wv[word]
            except KeyError:
                v = np.zeros(self.model.vector_size)

            m = np.vstack((m, v))
        return np.average(m, axis=0)

    def load(self, file_name):
        """ load model from file"""
        self.model.load(file_name)

    def save(self, file_name):
        """ save model to file"""
        self.model.save(file_name)

    def __train(self, tweets):
        """ train net """
        self.sentences = [t['text'] for t in tweets]

        corpus = [process_text(t) for t in self.sentences] + brown.sents()
        self.model = Word2Vec(corpus)


# Word2VecModel().build(tweets)

