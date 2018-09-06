import numpy as np
from time import time

from clustering.similarity.word_sym import symmetric_sentence_similarity
from utils.files import get_tweets_from_file
from utils.text_proccesing import process_text


class SentenceSymModel(object):

    def __init__(self):
        pass

    def build(self, Tweets, method=symmetric_sentence_similarity):
        """ returns sym matrix based sym method"""
        sentences = [process_text(t.text) for t in Tweets]

        data_len = len(sentences)

        m = np.zeros((data_len, data_len))
        for i in xrange(data_len):
            for j in xrange(i, data_len):
                if i == j:
                    m[i][j] = 1.0
                else:
                    sim = method(sentences[i], sentences[j])
                    m[i][j] = sim
                    m[j][i] = sim
        return m


# SentenceSymModel().build(tweets)
