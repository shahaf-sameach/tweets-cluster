import numpy as np
from time import time

from clustering.metric.word_sym import symmetric_sentence_similarity
from utils.files import get_from_binary_file
from utils.text_proccesing import process_text


class SentenceSymModel(object):

    def __init__(self):
        pass

    def build(self, tweets, method=symmetric_sentence_similarity):
        sentences = [process_text(t['text']) for t in tweets]

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


if __name__ == "__main__":
    t0 = time()

    tweets = get_from_binary_file()[:30]
    t1 = time()
    print  "loading took {}".format(t1 - t0)
    model = SentenceSymModel()
    dist_matrix = model.build(tweets)
    print dist_matrix
    t2 = time()
    print "calc matrix took {}".format(t2 - t1)

    # sents = np.array([[t['text']] for t in tweets])
    # d = distance.cdist(sents, sents, lambda u, v : sentence_distance(u[0],v[0]))
