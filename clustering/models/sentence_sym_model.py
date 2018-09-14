import time

import numpy as np

from clustering.similarity.word_sym import symmetric_sentence_similarity



class SentenceSymModel(object):

    def __init__(self):
        pass

    def build(self, tweets, method=symmetric_sentence_similarity):
        """ returns sym matrix based sym method"""
        print("retrive sentences from {} tweets".format(len(tweets)))
        sentences = [t.text for t in tweets]

        data_len = len(sentences)

        m = np.zeros((data_len, data_len))
        np.fill_diagonal(m, 1.0)

        total_count, count = 1, 1
        for i in xrange(data_len):
            for j in xrange(i + 1, data_len):
                total_count += 1

        print("building simm matrix")
        for i in xrange(data_len):
            for j in xrange(i + 1, data_len):
                t0 = time.time()
                print("calc sim {}/{}".format(count, total_count))
                sim = method(sentences[i], sentences[j])
                m[i][j] = sim
                m[j][i] = sim
                count += 1
                print("took {:.3f}".format(time.time() - t0))

        return m




