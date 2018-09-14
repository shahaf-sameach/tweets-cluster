import numpy as np

from clustering.similarity.word_sym import symmetric_sentence_similarity as word_sym


class SentenceSymModel(object):

    def __init__(self):
        pass

    def build(self, tweets, metric=word_sym):
        """ returns sym matrix based sym method"""
        sentences = [t.text for t in tweets]

        data_len = len(sentences)

        m = np.zeros((data_len, data_len))
        np.fill_diagonal(m, 1.0)

        for i in xrange(data_len):
            for j in xrange(i + 1, data_len):
                m[i][j] = m[j][i] = metric(sentences[i], sentences[j])

        return m




